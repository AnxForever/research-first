from __future__ import annotations

import json
import argparse
import re
import sys
from pathlib import Path
from typing import Callable
from urllib.parse import urlsplit

from playwright.sync_api import Browser, BrowserContext, Page, TimeoutError as PlaywrightTimeoutError, expect, sync_playwright

BASE = "http://127.0.0.1:4314"
STORAGE_KEY = "shadcn-admin.tasks.saved-views.v1"
VIEW_NAME = "QA Canceled Medium"
OUT: Path


def allow_local_only(context: BrowserContext) -> None:
    context.route(
        "**/*",
        lambda route: route.continue_()
        if (urlsplit(route.request.url).scheme, urlsplit(route.request.url).netloc)
        == (urlsplit(BASE).scheme, urlsplit(BASE).netloc)
        or route.request.url.startswith("data:")
        else route.abort(),
    )


def wait_tasks_ready(page: Page) -> None:
    """Wait for mounted, visible task-list controls; DOMContentLoaded is insufficient."""
    page.goto(BASE + "/tasks", wait_until="domcontentloaded", timeout=30_000)
    page.get_by_role("button", name="Save current view", exact=True).wait_for(
        state="visible", timeout=20_000
    )
    page.locator('button[aria-label="Saved task views"]').wait_for(
        state="visible", timeout=10_000
    )
    page.get_by_placeholder("Filter by title or ID...").wait_for(
        state="visible", timeout=10_000
    )
    page.locator("tbody tr").first.wait_for(state="visible", timeout=10_000)
    if "/tasks" not in page.url:
        raise AssertionError(f"task route did not mount; URL={page.url}")


def select_facet(page: Page, title: str, value: str) -> None:
    button = page.locator('button[data-slot="popover-trigger"]').filter(has_text=title)
    if button.count() != 1:
        raise AssertionError(
            f"locator issue for {title}: expected one facet button, found {button.count()}"
        )
    button.wait_for(state="visible", timeout=5_000)
    button.click()
    option = page.get_by_role("option").filter(has_text=value)
    try:
        option.wait_for(state="visible", timeout=5_000)
    except PlaywrightTimeoutError as exc:
        visible_options = page.get_by_role("option").all_text_contents()
        raise AssertionError(
            f"option locator/timing issue for {title}={value}; visible options={visible_options}"
        ) from exc
    option.click()
    page.keyboard.press("Escape")
    page.locator('button[data-slot="popover-trigger"]').filter(has_text=title).wait_for(
        state="visible", timeout=5_000
    )


def saved_blob(page: Page):
    raw = page.evaluate("key => window.localStorage.getItem(key)", STORAGE_KEY)
    return raw, json.loads(raw) if raw is not None else None


def visible_task_rows(page: Page) -> list[str]:
    return [text.strip() for text in page.locator("tbody tr").all_text_contents()]


def page_setup(browser: Browser, *, init_script: str | None = None) -> tuple[BrowserContext, Page, list[str]]:
    context = browser.new_context(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
    allow_local_only(context)
    if init_script:
        context.add_init_script(init_script)
    page = context.new_page()
    page_errors: list[str] = []
    page.on("pageerror", lambda error: page_errors.append(str(error)))
    return context, page, page_errors


def run_lifecycle(browser: Browser) -> dict:
    context, page, page_errors = page_setup(browser)
    try:
        response = page.goto(BASE + "/tasks", wait_until="domcontentloaded", timeout=30_000)
        if response is None or response.status != 200:
            raise AssertionError(f"cold-load HTTP status={response.status if response else None}")
        # Explicitly wait for React controls and an actual data row after document load.
        page.get_by_role("button", name="Save current view", exact=True).wait_for(
            state="visible", timeout=20_000
        )
        page.locator('button[aria-label="Saved task views"]').wait_for(state="visible", timeout=10_000)
        search = page.get_by_placeholder("Filter by title or ID...")
        search.wait_for(state="visible", timeout=10_000)
        page.locator("tbody tr").first.wait_for(state="visible", timeout=10_000)
        page.screenshot(path=str(OUT / "cold-load.png"), full_page=True)

        # A generic ID prefix is a filter term, not a stored task row value.
        search.fill("TASK-")
        select_facet(page, "Status", "Canceled")
        select_facet(page, "Priority", "Medium")
        rows_before = visible_task_rows(page)
        if not rows_before or any("No results" in row for row in rows_before):
            raise AssertionError(f"chosen filters unexpectedly produced no tasks: {rows_before}")
        if any("Canceled" not in row or "Medium" not in row for row in rows_before):
            raise AssertionError(f"visible rows do not match selected filters: {rows_before}")

        row_checks = page.get_by_role("checkbox", name="Select row")
        if row_checks.count() < 1:
            raise AssertionError("row selection locator issue: no visible Select row checkbox")
        row_checks.first.check()
        if page.locator('tbody tr[data-state="selected"]').count() != 1:
            raise AssertionError("selected-row state did not appear before saving")

        page.get_by_role("button", name="Save current view", exact=True).click()
        dialog = page.get_by_role("dialog")
        dialog.wait_for(state="visible", timeout=5_000)
        dialog.get_by_label("View name").fill(VIEW_NAME)
        dialog.get_by_role("button", name="Save view", exact=True).click()
        page.get_by_text(f'Saved view "{VIEW_NAME}".', exact=True).wait_for(
            state="visible", timeout=5_000
        )
        dialog.wait_for(state="hidden", timeout=5_000)
        expect(page.locator('button[aria-label="Saved task views"]')).to_contain_text(VIEW_NAME)

        raw, saved = saved_blob(page)
        if not isinstance(saved, list) or len(saved) != 1:
            raise AssertionError(f"storage should contain one saved view, got {raw!r}")
        item = saved[0]
        expected_keys = {"id", "name", "search", "status", "priority"}
        if set(item) != expected_keys:
            raise AssertionError(f"unexpected persisted fields: {sorted(item)}")
        if (
            item["name"] != VIEW_NAME
            or item["search"] != "TASK-"
            or item["status"] != ["canceled"]
            or item["priority"] != ["medium"]
        ):
            raise AssertionError(f"stored filter configuration differs: {item!r}")
        if "TASK-" in str(item.get("id")) or any(
            marker in raw for marker in ("TASK-9366", "TASK-5736", "rowSelection", "selectedRows")
        ):
            raise AssertionError("storage contains row data or row-selection state")
        page.screenshot(path=str(OUT / "view-saved.png"), full_page=True)

        # Reload while the saved filters are still active. React controls and a table row must mount first.
        page.reload(wait_until="domcontentloaded", timeout=30_000)
        page.get_by_role("button", name="Save current view", exact=True).wait_for(
            state="visible", timeout=20_000
        )
        select_trigger = page.locator('button[aria-label="Saved task views"]')
        select_trigger.wait_for(state="visible", timeout=10_000)
        search = page.get_by_placeholder("Filter by title or ID...")
        search.wait_for(state="visible", timeout=10_000)
        page.locator("tbody tr").first.wait_for(state="visible", timeout=10_000)
        expect(select_trigger).to_contain_text(VIEW_NAME)
        if page.locator('tbody tr[data-state="selected"]').count() != 0:
            raise AssertionError("row selection unexpectedly persisted across reload")
        page.screenshot(path=str(OUT / "view-reloaded.png"), full_page=True)

        # Change filters after refresh, then confirm the saved option can be chosen again.
        page.get_by_role("button", name="Reset", exact=True).click()
        search.fill("QA-no-match")
        select_facet(page, "Status", "Done")
        select_facet(page, "Priority", "High")
        expect(page.get_by_text("No results.", exact=True)).to_be_visible(timeout=5_000)
        select_trigger.click()
        saved_option = page.get_by_role("option", name=VIEW_NAME, exact=True)
        saved_option.wait_for(state="visible", timeout=5_000)
        saved_option.click()
        expect(search).to_have_value("TASK-", timeout=5_000)
        expect(select_trigger).to_contain_text(VIEW_NAME, timeout=5_000)
        restored_rows = visible_task_rows(page)
        if restored_rows != rows_before:
            raise AssertionError(
                f"restored results differ; before={rows_before!r}; after={restored_rows!r}"
            )
        if any("Canceled" not in row or "Medium" not in row for row in restored_rows):
            raise AssertionError(f"restored filters do not match visible tasks: {restored_rows}")
        page.screenshot(path=str(OUT / "view-restored-after-refresh.png"), full_page=True)

        # Saving the same name again is rejected clearly and leaves the stored view unchanged.
        page.get_by_role("button", name="Save current view", exact=True).click()
        dialog = page.get_by_role("dialog")
        dialog.wait_for(state="visible", timeout=5_000)
        dialog.get_by_label("View name").fill(VIEW_NAME)
        dialog.get_by_role("button", name="Save view", exact=True).click()
        expect(page.get_by_role("alert")).to_contain_text(
            "A saved view with this name already exists.", timeout=5_000
        )
        raw_after_duplicate, saved_after_duplicate = saved_blob(page)
        if saved_after_duplicate != saved:
            raise AssertionError(f"duplicate save changed storage unexpectedly: {raw_after_duplicate!r}")
        dialog.get_by_role("button", name="Cancel", exact=True).click()
        dialog.wait_for(state="hidden", timeout=5_000)

        # Delete applies only to the currently matched saved view.
        delete_button = page.locator(f'button[aria-label="Delete saved view {VIEW_NAME}"]')
        delete_button.wait_for(state="visible", timeout=5_000)
        expect(delete_button).to_be_enabled()
        delete_button.click()
        page.get_by_text(f'Deleted view "{VIEW_NAME}".', exact=True).wait_for(
            state="visible", timeout=5_000
        )
        expect(select_trigger).to_have_text("No saved views", timeout=5_000)
        raw_after_delete, saved_after_delete = saved_blob(page)
        if saved_after_delete != []:
            raise AssertionError(f"delete did not clear the saved view: {raw_after_delete!r}")
        page.screenshot(path=str(OUT / "view-deleted.png"), full_page=True)

        page.reload(wait_until="domcontentloaded", timeout=30_000)
        page.get_by_role("button", name="Save current view", exact=True).wait_for(
            state="visible", timeout=20_000
        )
        select_trigger = page.locator('button[aria-label="Saved task views"]')
        select_trigger.wait_for(state="visible", timeout=10_000)
        expect(select_trigger).to_have_text("No saved views", timeout=5_000)
        if page_errors:
            raise AssertionError(f"uncaught page errors: {page_errors}")
        return {
            "status": "PASS",
            "details": "Cold load, named save, filter restore, refresh and reselect, duplicate-name rejection, deletion, deleted-after-refresh, exact minimal storage shape, and no persisted row selection passed.",
            "initial_matching_rows": len(rows_before),
            "persisted_keys": sorted(expected_keys),
        }
    finally:
        context.close()


def run_corrupt_storage(browser: Browser) -> dict:
    script = (
        "localStorage.setItem("
        + json.dumps(STORAGE_KEY)
        + ", '{broken json');"
    )
    context, page, page_errors = page_setup(browser, init_script=script)
    try:
        wait_tasks_ready(page)
        trigger = page.locator('button[aria-label="Saved task views"]')
        expect(trigger).to_have_text("No saved views", timeout=5_000)
        if page_errors:
            raise AssertionError(f"uncaught page errors on corrupt storage: {page_errors}")
        page.screenshot(path=str(OUT / "corrupt-storage.png"), full_page=True)
        if page.get_by_text(f'Saved view "QA Recovered".', exact=True).count() != 0:
            raise AssertionError("corrupt storage produced a false save-success message")

        page.get_by_role("button", name="Save current view", exact=True).click()
        dialog = page.get_by_role("dialog")
        dialog.get_by_label("View name").fill("QA Recovered")
        dialog.get_by_role("button", name="Save view", exact=True).click()
        page.get_by_text('Saved view "QA Recovered".', exact=True).wait_for(
            state="visible", timeout=5_000
        )
        dialog.wait_for(state="hidden", timeout=5_000)
        raw, saved = saved_blob(page)
        if not isinstance(saved, list) or len(saved) != 1 or saved[0].get("name") != "QA Recovered":
            raise AssertionError(f"saving after corrupt key did not recover storage: {raw!r}")
        if page_errors:
            raise AssertionError(f"uncaught page errors after recovery: {page_errors}")
        page.screenshot(path=str(OUT / "corrupt-storage-recovered.png"), full_page=True)
        return {"status": "PASS", "details": "Malformed feature key did not crash the page, showed an empty saved-view state without false success, and accepted a later valid save."}
    finally:
        context.close()


def run_setitem_failure(browser: Browser) -> dict:
    init_script = """
(() => {
  const blockedKey = "shadcn-admin.tasks.saved-views.v1";
  const original = Storage.prototype.setItem;
  window.__blockedViewWrites = 0;
  Storage.prototype.setItem = function (key, value) {
    if (key === blockedKey) {
      window.__blockedViewWrites += 1;
      throw new DOMException("Blocked only the saved-views key", "QuotaExceededError");
    }
    return original.call(this, key, value);
  };
})();
"""
    context, page, page_errors = page_setup(browser, init_script=init_script)
    try:
        wait_tasks_ready(page)
        # Prove this fault is scoped to the feature key; unrelated localStorage writes still work.
        unrelated_write = page.evaluate(
            "() => { localStorage.setItem('qa-unrelated-probe', 'ok'); return localStorage.getItem('qa-unrelated-probe'); }"
        )
        if unrelated_write != "ok":
            raise AssertionError("test fault unexpectedly blocked an unrelated localStorage key")
        page.get_by_role("button", name="Save current view", exact=True).click()
        dialog = page.get_by_role("dialog")
        dialog.get_by_label("View name").fill("QA Must Not Claim Success")
        dialog.get_by_role("button", name="Save view", exact=True).click()
        page.get_by_text("Could not save views in this browser.", exact=True).wait_for(
            state="visible", timeout=5_000
        )
        if page.get_by_text('Saved view "QA Must Not Claim Success".', exact=True).count() != 0:
            raise AssertionError("save failure also displayed a false success message")
        if page.evaluate("key => localStorage.getItem(key)", STORAGE_KEY) is not None:
            raise AssertionError("failed setItem left a persisted saved-view value")
        blocked_count = page.evaluate("() => window.__blockedViewWrites")
        if blocked_count != 1:
            raise AssertionError(f"expected exactly one blocked feature-key write, got {blocked_count}")
        expect(dialog).to_be_visible(timeout=5_000)
        if page_errors:
            raise AssertionError(f"uncaught page errors after setItem failure: {page_errors}")
        page.screenshot(path=str(OUT / "setitem-error.png"), full_page=True)
        return {"status": "PASS", "details": "Only the feature key's setItem was faulted; save showed an error, did not claim success or persist data, left the dialog usable, and the page remained live."}
    finally:
        context.close()


def main() -> int:
    results: dict[str, dict] = {}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        scenarios: list[tuple[str, Callable[[Browser], dict]]] = [
            ("lifecycle", run_lifecycle),
            ("corrupt_storage", run_corrupt_storage),
            ("setitem_failure", run_setitem_failure),
        ]
        for name, scenario in scenarios:
            try:
                results[name] = scenario(browser)
                print(f"{name}: PASS - {results[name]['details']}")
            except Exception as exc:
                results[name] = {"status": "FAIL", "error": f"{type(exc).__name__}: {exc}"}
                print(f"{name}: FAIL - {type(exc).__name__}: {exc}")
                print("Classification: inspect mounted controls and locator counts before treating this as a feature failure.")
        browser.close()

    (OUT / "browser-results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    failures = [name for name, result in results.items() if result["status"] != "PASS"]
    return 1 if failures else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replay the saved-views acceptance on the patched public fixture using local Edge.")
    parser.add_argument("--url", default=BASE)
    parser.add_argument("--output", required=True, type=Path, help="New output directory; an existing directory is refused")
    args = parser.parse_args()
    parsed = urlsplit(args.url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in {"localhost", "127.0.0.1", "::1"} or parsed.username or parsed.password:
        parser.error("Use a loopback fixture URL without credentials.")
    BASE = args.url.rstrip("/")
    OUT = args.output.resolve()
    OUT.mkdir(parents=True, exist_ok=False)
    sys.exit(main())
