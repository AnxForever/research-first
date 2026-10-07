"""Offline browser acceptance for the synthetic async-search fixture and its outputs.

Requires Python Playwright and an installed Chromium browser channel. This is a
task-specific evaluator, not a general skill score or a sandbox for untrusted HTML.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from playwright.async_api import async_playwright

CATALOG = ["快速指南", "慢速连接说明", "异步搜索说明", "连接恢复手册"]
CASES = [
    (" 快 ", "resolved", ["快速指南"], 70, 700),
    ("慢", "resolved", ["慢速连接说明"], 800, 2000),
    ("空", "resolved", [], 140, 650),
    (" 异步 ", "resolved", ["异步搜索说明"], 200, 900),
    ("暂时失败", "rejected", None, 170, 800),
    ("暂时失败", "resolved", ["连接恢复手册"], 170, 800),
]
FAILURE = re.compile(r"不可用|查询失败|搜索失败|请求失败|错误|出错|重试|稍后")
EMPTY = re.compile(r"没有找到|没有匹配|无匹配|暂无匹配|未找到")
PENDING = re.compile(r"正在搜索|搜索中|查询中|处理中|loading", re.I)


async def status_text(page) -> str:
    for selector in ('[role="status"]', '[role="alert"]', '[aria-live]', "#status", "#failure-message", ".status", '[data-testid*="status"]'):
        items = page.locator(selector)
        for i in range(await items.count()):
            item = items.nth(i)
            if await item.is_visible():
                value = (await item.inner_text()).strip()
                if value:
                    return value
    return ""


async def visible_items(page) -> list[str]:
    values = []
    for name in CATALOG:
        items = page.get_by_text(name, exact=True)
        for i in range(await items.count()):
            if await items.nth(i).is_visible():
                values.append(name)
                break
    return values


async def search_input(page):
    items = page.get_by_label(re.compile(r"关键词|搜索|查询"))
    if await items.count():
        return items.first
    items = page.locator('input[type="search"], input[type="text"], input:not([type])')
    if await items.count():
        return items.first
    raise RuntimeError("No search input")


async def submit(page, query: str, method: str) -> None:
    field = await search_input(page)
    await field.fill(query)
    if method == "enter":
        await field.press("Enter")
        return
    items = page.get_by_role("button", name=re.compile(r"搜索|查询"))
    if await items.count():
        await items.first.click()
        return
    items = page.locator('input[type="submit"], button[type="submit"]')
    if await items.count():
        await items.first.click()
        return
    raise RuntimeError("No submit button")


def completed(status: str) -> bool:
    return bool(status) and not PENDING.search(status) and not FAILURE.search(status) and not EMPTY.search(status)


async def wait_state(page, predicate, timeout_ms=3500):
    end = time.monotonic() + timeout_ms / 1000
    last_status, last_items = "", []
    while time.monotonic() < end:
        last_status, last_items = await status_text(page), await visible_items(page)
        if predicate(last_status, last_items):
            return True, last_status, last_items
        await page.wait_for_timeout(75)
    return False, last_status, last_items


async def open_page(browser, app_dir: Path):
    context = await browser.new_context()
    page = await context.new_page()
    external_hosts = []
    page.on("request", lambda request: external_hosts.append(urlsplit(request.url).hostname or "")
            if request.url.startswith(("http://", "https://")) else None)
    async def block_external(route):
        await route.abort()
    await context.route("http://**/*", block_external)
    await context.route("https://**/*", block_external)
    uri = (app_dir / "index.html").resolve().as_uri()
    await page.goto(uri, wait_until="load")
    return context, page, uri, external_hosts


async def api_contract(page) -> dict[str, Any]:
    if not await page.evaluate("typeof localSearch === 'function'"):
        return {"api_exposed_to_page": False, "cases": []}
    observed = []
    for query, expected_state, expected_value, low, high in CASES:
        result = await page.evaluate(
            """async query => {
              const start = performance.now();
              try { const value = await localSearch(query); return {state:"resolved", ms:performance.now()-start, value}; }
              catch (_) { return {state:"rejected", ms:performance.now()-start, value:null}; }
            }""",
            query,
        )
        ms = result.get("ms")
        state_ok = result.get("state") == expected_state
        value_ok = result.get("value") == expected_value
        timing_ok = isinstance(ms, (int, float)) and low <= ms <= high
        observed.append({
            "query": query.strip(),
            "state": result.get("state"),
            "elapsed_ms": round(ms, 1) if isinstance(ms, (int, float)) else None,
            "outcome_matches_fixture": state_ok and value_ok,
            "delay_within_acceptance_window": timing_ok,
            "pass": state_ok and value_ok and timing_ok,
        })
    return {"api_exposed_to_page": True, "cases": observed}


TRACKER = r"""
(() => {
  window.__acceptanceSubmits = [];
  window.__acceptanceCalls = [];
  const form = document.querySelector("form");
  const input = document.querySelector("input");
  form?.addEventListener("submit", () => window.__acceptanceSubmits.push({
    query:(input?.value || "").trim(), at:performance.now()
  }), true);
  const original = window.localSearch;
  if (typeof original === "function") window.localSearch = function(rawQuery) {
    const call = {query:rawQuery, started_at:performance.now(), done:false, state:null};
    window.__acceptanceCalls.push(call);
    let promise;
    try { promise = original.call(this, rawQuery); }
    catch (error) { call.done=true; call.state="rejected"; throw error; }
    return Promise.resolve(promise).then(
      value => { call.done=true; call.state="resolved"; call.elapsed_ms=performance.now()-call.started_at; return value; },
      error => { call.done=true; call.state="rejected"; call.elapsed_ms=performance.now()-call.started_at; throw error; }
    );
  };
})();
"""


async def run_artifact(app_dir: Path, browser_channel: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "artifact_directory": app_dir.name,
        "browser_channel": browser_channel,
        "fresh_contexts": True,
        "checks": {},
    }
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel=browser_channel, headless=True)
        external_host_groups = []
        try:
            context, page, uri, hosts = await open_page(browser, app_dir)
            external_host_groups.append(hosts)
            result["opened_uri"] = uri
            result["checks"]["api_contract"] = await api_contract(page)
            await context.close()

            context, page, _, hosts = await open_page(browser, app_dir)
            external_host_groups.append(hosts)
            await page.add_script_tag(content=TRACKER)
            await submit(page, "慢", "button")
            await page.wait_for_function("() => window.__acceptanceCalls.some(x => x.query === '慢')", timeout=2500)
            await submit(page, "快", "button")
            await page.wait_for_function("() => window.__acceptanceSubmits.some(x => x.query === '快')", timeout=2500)
            slow_pending_at_second_submit = await page.evaluate(
                """() => {
                  const slow=window.__acceptanceCalls.find(x=>x.query==="慢");
                  const fast=window.__acceptanceSubmits.find(x=>x.query==="快");
                  return !!slow && !!fast && !slow.done && fast.at>slow.started_at;
                }"""
            )
            fast_ready, fast_status, fast_items = await wait_state(
                page, lambda s, items: "快速指南" in items and completed(s), 5000
            )
            await page.wait_for_function(
                "() => window.__acceptanceCalls.some(x => x.query === '慢' && x.done)", timeout=4000
            )
            final_status, final_items = await status_text(page), await visible_items(page)
            result["checks"]["latest_submission_wins"] = {
                "second_submission_while_slow_pending": bool(slow_pending_at_second_submit),
                "status_when_fast_result_visible": fast_status,
                "items_when_fast_result_visible": fast_items,
                "status_after_slow_completed": final_status,
                "items_after_slow_completed": final_items,
                "pass": bool(
                    slow_pending_at_second_submit and fast_ready
                    and "快速指南" in final_items and "慢速连接说明" not in final_items
                    and completed(final_status)
                ),
            }
            await context.close()

            context, page, _, hosts = await open_page(browser, app_dir)
            external_host_groups.append(hosts)
            await submit(page, "空", "enter")
            empty_ready, empty_status, empty_items = await wait_state(
                page, lambda s, _: bool(EMPTY.search(s)) and not FAILURE.search(s)
            )
            result["checks"]["empty_is_not_failure"] = {
                "status": empty_status,
                "visible_catalog_items": empty_items,
                "pass": bool(empty_ready and not empty_items and not FAILURE.search(empty_status)),
            }
            await context.close()

            context, page, _, hosts = await open_page(browser, app_dir)
            external_host_groups.append(hosts)
            await submit(page, "暂时失败", "enter")
            failed, fail_status, fail_items = await wait_state(
                page, lambda s, _: bool(FAILURE.search(s)) and not EMPTY.search(s)
            )
            await submit(page, "暂时失败", "button")
            recovered, recovery_status, recovery_items = await wait_state(
                page, lambda s, items: "连接恢复手册" in items and completed(s)
            )
            result["checks"]["temporary_failure_and_recovery"] = {
                "first_status": fail_status,
                "first_items": fail_items,
                "first_distinguished_from_empty": bool(failed),
                "recovery_status": recovery_status,
                "recovery_items": recovery_items,
                "pass": bool(
                    failed and recovered and "连接恢复手册" in recovery_items
                    and completed(recovery_status) and not FAILURE.search(recovery_status)
                ),
            }
            await context.close()

            context, page, _, hosts = await open_page(browser, app_dir)
            external_host_groups.append(hosts)
            await submit(page, "快", "enter")
            enter_ok, enter_status, enter_items = await wait_state(
                page, lambda s, items: "快速指南" in items and completed(s), 2500
            )
            await submit(page, "异步", "button")
            button_ok, button_status, button_items = await wait_state(
                page, lambda s, items: "异步搜索说明" in items and completed(s), 3000
            )
            external_hosts = [host for group in external_host_groups for host in group]
            result["checks"]["basic_use"] = {
                "enter_status": enter_status,
                "enter_items": enter_items,
                "button_status": button_status,
                "button_items": button_items,
                "external_http_request_hosts": external_hosts,
                "pass": bool(enter_ok and button_ok and not external_hosts and "快速指南" in enter_items and "异步搜索说明" in button_items),
            }
            await context.close()
        finally:
            await browser.close()

    return result


def find_failed_checks(result: dict[str, Any]) -> list[str]:
    checks = result.get("checks")
    if not isinstance(checks, dict):
        return ["checks"]

    failed: list[str] = []
    api = checks.get("api_contract")
    if not isinstance(api, dict) or api.get("api_exposed_to_page") is not True:
        failed.append("api_contract.api_exposed_to_page")
    api_cases = api.get("cases") if isinstance(api, dict) else None
    if not isinstance(api_cases, list) or len(api_cases) != len(CASES):
        failed.append("api_contract.cases")
    else:
        for index, case in enumerate(api_cases):
            if not isinstance(case, dict) or case.get("pass") is not True:
                failed.append(f"api_contract.cases[{index}]")

    for check_id in (
        "latest_submission_wins",
        "empty_is_not_failure",
        "temporary_failure_and_recovery",
        "basic_use",
    ):
        check = checks.get(check_id)
        if not isinstance(check, dict) or check.get("pass") is not True:
            failed.append(check_id)
    return failed


def write_new_json(output: Path, result: dict[str, Any]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    # Mode "x" maps to exclusive creation: a competing or pre-existing file is never replaced.
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(serialized)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app-dir", required=True, type=Path, help="Directory containing index.html")
    parser.add_argument("--output", required=True, type=Path, help="New JSON file for this run")
    parser.add_argument("--browser-channel", default="msedge", help="Playwright Chromium channel, for example msedge or chrome")
    args = parser.parse_args()
    try:
        app_dir = args.app_dir.resolve()
        output = args.output.resolve()
        if not (app_dir / "index.html").is_file():
            raise FileNotFoundError("--app-dir must contain index.html")
        if output.exists():
            print("Acceptance output already exists; choose a new --output path.", file=sys.stderr)
            return 2

        async def bounded_run():
            return await asyncio.wait_for(run_artifact(app_dir, args.browser_channel), timeout=60)

        result = asyncio.run(bounded_run())
        failed = find_failed_checks(result)
        result["overall_pass"] = not failed
        result["failed_checks"] = failed
        exit_code = 0 if not failed else 1
    except Exception as error:
        result = {
            "artifact_directory": args.app_dir.name,
            "browser_channel": args.browser_channel,
            "fresh_contexts": True,
            "checks": {},
            "overall_pass": False,
            "failed_checks": ["execution_error"],
            "execution_error": {
                "type": type(error).__name__,
                "message": "Browser or file execution raised an exception; details omitted.",
            },
        }
        output = args.output
        exit_code = 2

    try:
        write_new_json(output, result)
    except FileExistsError:
        print("Acceptance output already exists; it was not overwritten.", file=sys.stderr)
        return 2
    except Exception as error:
        print(f"Could not create acceptance output ({type(error).__name__}); no pass was reported.", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
