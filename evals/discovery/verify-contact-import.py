"""Reproduce the frozen malformed-CSV regression through a visible import entry.

Requires Python Playwright and an installed Chromium browser channel. This
checks the synthetic contacts fixture's outputs, not arbitrary import products.
Only run known local evaluation artifacts; this is not an HTML sandbox.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

# Exact malformed input, with the CRLF record terminator frozen into the bytes.
DEFAULT_CASE = '姓名,邮箱,公司\r\n星野,malformed@example.test,"unterminated, value\r\n'


def read_rows(page) -> list[list[str]]:
    return page.locator('table tbody tr').evaluate_all(
        'els => els.map(row => Array.from(row.cells).map(cell => cell.innerText.trim()))'
    )


def read_feedback(page) -> str:
    return ' '.join(
        re.sub(r'\s+', ' ', text).strip()
        for text in page.locator('[role="status"], [role="alert"]').all_inner_texts()
        if text.strip()
    )


def main() -> int:
    parser = argparse.ArgumentParser(description='Portable Edge acceptance check for an unterminated quoted CSV field.')
    parser.add_argument('--app-dir', required=True, type=Path, help='Directory containing the application index.html')
    parser.add_argument('--output-dir', required=True, type=Path, help='A new directory for the case, JSON record and screenshot')
    parser.add_argument('--channel', default='msedge', help='Playwright browser channel, for example msedge or chrome')
    parser.add_argument('--input-csv', type=Path, help='Use an existing exact CSV file instead of creating the standard case')
    args = parser.parse_args()

    app_dir = args.app_dir.resolve()
    output_dir = args.output_dir.resolve()
    index = app_dir / 'index.html'
    if not index.is_file():
        raise FileNotFoundError(f'No index.html under --app-dir: {index}')
    if output_dir.exists():
        raise FileExistsError(f'--output-dir must be new; refusing to overwrite: {output_dir}')
    output_dir.mkdir(parents=True, exist_ok=False)

    case = args.input_csv.resolve() if args.input_csv else output_dir / 'unterminated-quote.csv'
    if not args.input_csv:
        case.write_bytes(DEFAULT_CASE.encode('utf-8'))
    raw_case = case.read_bytes()
    case_text = raw_case.decode('utf-8')

    result: dict[str, Any] = {
        'app_dir': str(app_dir),
        'entry': str(index),
        'channel': args.channel,
        'case_file': str(case),
        'case_sha256': hashlib.sha256(raw_case).hexdigest(),
        'case_text': case_text,
        'launch_mode': 'file://',
        'external_requests': [],
        'page_errors': [],
        'dialogs': [],
        'before': None,
        'after': None,
        'outcome_observed': False,
        'checks': {},
    }
    browser = None
    context = None
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel=args.channel, headless=True)
            result['browser_version'] = browser.version
            context = browser.new_context(viewport={'width': 1440, 'height': 1000}, accept_downloads=True)
            context.route('http://**/*', lambda route: route.abort())
            context.route('https://**/*', lambda route: route.abort())
            page = context.new_page()
            page.on('pageerror', lambda error: result['page_errors'].append(str(error)))
            page.on('dialog', lambda dialog: (result['dialogs'].append(dialog.message), dialog.accept()))
            page.on(
                'request',
                lambda request: result['external_requests'].append(request.url[:500])
                if request.url.startswith(('http://', 'https://')) else None,
            )
            # These two apps are file:// runnable; navigation failures are recorded as failures.
            page.goto(index.as_uri(), wait_until='load', timeout=10000)

            before_rows = read_rows(page)
            before_status = read_feedback(page)
            result['before'] = {'rows': before_rows, 'row_count': len(before_rows), 'feedback': before_status}
            file_inputs = page.locator('input[type="file"]')
            if file_inputs.count() == 0:
                raise RuntimeError('Application has no real input[type=file].')

            target = None
            target_kind = None
            target_index = None
            buttons = page.get_by_role('button', name=re.compile(r'CSV|导入|上传|import|upload', re.I))
            for i in range(buttons.count()):
                button = buttons.nth(i)
                if button.is_visible() and button.is_enabled():
                    target, target_kind, target_index = button, 'visible-import-button', i
                    break
            if target is None:
                for i in range(file_inputs.count()):
                    file_input = file_inputs.nth(i)
                    if file_input.is_visible() and file_input.is_enabled():
                        target, target_kind, target_index = file_input, 'visible-file-input', i
                        break
            if target is None:
                raise RuntimeError('No visible user-facing import button or file input was available.')

            try:
                with page.expect_file_chooser(timeout=2500) as chooser_info:
                    target.click(timeout=2500)
                chooser_info.value.set_files(str(case))
                interaction = target_kind + '+native-file-chooser'
            except PlaywrightTimeoutError:
                if target_kind != 'visible-file-input':
                    raise RuntimeError('The visible import button did not open the native file chooser.')
                visible_input = file_inputs.nth(target_index)
                visible_input.set_input_files(str(case), timeout=4000)
                interaction = 'visible-file-input.set_input_files'
            result['interaction'] = interaction

            try:
                # Wait for a meaningful outcome: explicit reject/skip feedback or the malformed row itself.
                page.wait_for_function(
                    """() => {
                      const status = [...document.querySelectorAll('[role=status], [role=alert]')]
                        .map(el => el.innerText).join(' ');
                      const rows = [...document.querySelectorAll('table tbody tr')];
                      const badContact = rows.some(row => row.innerText.includes('malformed@example.test'));
                      const explicitFeedback = /引号|未闭合|失败|错误|无效|拒绝|跳过|未导入|无法|malformed|unclosed|reject|skip|invalid|error|fail/i.test(status);
                      return badContact || explicitFeedback;
                    }""",
                    timeout=8000,
                )
                result['outcome_observed'] = True
                after_rows = read_rows(page)
                after_status = read_feedback(page)
                result['after'] = {'rows': after_rows, 'row_count': len(after_rows), 'feedback': after_status}
                page.screenshot(path=str(output_dir / 'unterminated-quote.png'), full_page=True)
            except PlaywrightTimeoutError:
                result['outcome_timeout'] = 'No explicit reject/skip feedback or malformed contact appeared.'

            after = result['after']
            if after is None:
                rejected_or_skipped = False
                evidence = {'outcome_observed': False}
            else:
                after_rows = after['rows']
                bad_present = any('malformed@example.test' in row for row in after_rows)
                state_unchanged = after_rows == before_rows
                feedback_explicit = bool(re.search(
                    r'引号|未闭合|失败|错误|无效|拒绝|跳过|未导入|无法|malformed|unclosed|reject|skip|invalid|error|fail',
                    after['feedback'], re.I,
                ))
                rejected_or_skipped = state_unchanged and not bad_present and feedback_explicit
                evidence = {
                    'state_unchanged': state_unchanged,
                    'malformed_contact_present': bad_present,
                    'explicit_feedback': feedback_explicit,
                    'final_rows': after_rows,
                    'feedback': after['feedback'],
                }
            result['checks'] = {
                'real_visible_import_entry_used': {'status': 'pass', 'evidence': interaction},
                'unterminated_quote_rejected_or_explicitly_skipped': {
                    'status': 'pass' if rejected_or_skipped else 'fail', 'evidence': evidence,
                },
                'no_external_runtime_observed': {
                    'status': 'pass' if not result['external_requests'] else 'fail',
                    'evidence': result['external_requests'],
                },
            }
            context.close()
            context = None
            browser.close()
            browser = None
    finally:
        if context is not None:
            context.close()
        if browser is not None:
            browser.close()

    target = output_dir / 'unterminated-quote-recheck.json'
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if all(check['status'] == 'pass' for check in result['checks'].values()) else 1


if __name__ == '__main__':
    raise SystemExit(main())
