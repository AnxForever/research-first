import assert from 'node:assert/strict'
import { execFileSync } from 'node:child_process'
import { mkdirSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import path from 'node:path'

const [projectArgument, outputArgument, baseUrl = 'http://127.0.0.1:4173/tasks', ...extra] = process.argv.slice(2)
if (!projectArgument || !outputArgument || extra.length > 0) {
  console.error('Usage: node evals/verify-shadcn-export.mjs <project-dir> <new-output-dir> [base-url]')
  process.exit(2)
}

const projectDirectory = path.resolve(projectArgument)
const outputDirectory = path.resolve(outputArgument)
const browserChannel = process.env.CSV_BROWSER_CHANNEL || 'chromium'
const pythonCommand = process.env.CSV_PYTHON || (process.platform === 'win32' ? 'python' : 'python3')

// Refuse an existing directory, including one from a failed earlier run. Each
// execution owns a new evidence directory and never overwrites previous results.
mkdirSync(path.dirname(outputDirectory), { recursive: true })
mkdirSync(outputDirectory)

const result = {
  startedAt: new Date().toISOString(),
  projectDirectory,
  baseUrl,
  browser: browserChannel,
  mechanism: 'real Playwright download event and saveAs; no Blob/anchor mocks',
  checks: [],
  downloads: [],
}

let browser
let page
let expect
let exportButton
const downloadEvents = []

async function displayedTask(row) {
  const cells = row.locator('td')
  return {
    id: await cells.nth(1).innerText(),
    title: await cells.nth(2).locator('span.truncate').innerText(),
    status: (await cells.nth(3).innerText()).toLowerCase(),
    label: (await cells.nth(2).locator('[data-slot="badge"]').innerText()).toLowerCase(),
    priority: (await cells.nth(4).innerText()).toLowerCase(),
  }
}

async function saveAndVerify(name, expectedTasks) {
  const downloadPromise = page.waitForEvent('download')
  await exportButton.click()
  const download = await downloadPromise
  const target = path.join(outputDirectory, name)
  await download.saveAs(target)
  assert.equal(await download.failure(), null)
  assert.match(download.suggestedFilename(), /^tasks-\d{4}-\d{2}-\d{2}T[\d-]+Z\.csv$/)

  // A separate implementation decodes/parses the actual saved file.
  const inspection = JSON.parse(execFileSync(pythonCommand, ['-c', `
import csv, io, json, pathlib, sys
raw = pathlib.Path(sys.argv[1]).read_bytes()
assert raw[:3] == bytes([239, 187, 191]), 'missing UTF-8 BOM'
text = raw.decode('utf-8-sig')
rows = list(csv.DictReader(io.StringIO(text, newline='')))
assert list(rows[0]) == ['id', 'title', 'status', 'label', 'priority']
assert '\\r\\n' in text, 'missing CRLF records'
print(json.dumps({'bytes': len(raw), 'bomHex': raw[:3].hex(), 'rows': rows}, ensure_ascii=True))
`, target], { encoding: 'utf8' }))
  assert.deepEqual(inspection.rows, expectedTasks)
  const entry = {
    scenario: name,
    path: target,
    suggestedFilename: download.suggestedFilename(),
    failure: await download.failure(),
    ...inspection,
  }
  result.downloads.push(entry)
  return entry
}

try {
  const require = createRequire(path.join(projectDirectory, 'package.json'))
  const playwright = require('playwright/test')
  expect = playwright.expect
  browser = await playwright.chromium.launch({
    headless: true,
    ...(browserChannel === 'chromium' ? {} : { channel: browserChannel }),
  })
  const context = await browser.newContext({ acceptDownloads: true })
  page = await context.newPage()
  page.on('download', (download) => downloadEvents.push(download))
  exportButton = page.getByRole('button', { name: 'Export tasks', exact: true })
  result.browserVersion = browser.version()
  await page.goto(result.baseUrl, { waitUntil: 'networkidle' })
  await expect(page.getByRole('heading', { name: 'Tasks', exact: true })).toBeVisible()
  await expect(exportButton).toHaveCount(0)
  assert.equal(downloadEvents.length, 0)
  result.checks.push('No export control and no download with empty selection')

  const first = await displayedTask(page.locator('tbody tr').first())
  await page.locator('tbody tr').first().getByRole('checkbox', { name: 'Select row', exact: true }).check()
  await page.getByRole('button', { name: 'Go to next page', exact: true }).click()
  await expect(page.locator('tbody tr').first().locator('td').nth(1)).not.toHaveText(first.id)
  const second = await displayedTask(page.locator('tbody tr').first())
  await page.locator('tbody tr').first().getByRole('checkbox', { name: 'Select row', exact: true }).check()
  await expect(page.getByRole('toolbar', { name: 'Bulk actions for 2 selected tasks', exact: true })).toBeVisible()
  await saveAndVerify('cross-page.csv', [first, second])
  result.checks.push('Two selected tasks across pages downloaded; all five fields equal full displayed values')
  await expect(page.getByRole('toolbar', { name: 'Bulk actions for 2 selected tasks', exact: true })).toBeVisible()

  await page.getByRole('textbox', { name: 'Filter by title or ID...' }).fill(first.id)
  await expect(page.locator('tbody tr')).toHaveCount(1)
  await expect(page.getByRole('toolbar', { name: 'Bulk actions for 1 selected task', exact: true })).toBeVisible()
  await saveAndVerify('filtered.csv', [first])
  result.checks.push('Filter narrows export to exactly the one selected matching task')

  await page.getByRole('textbox', { name: 'Filter by title or ID...' }).fill('')
  await expect(page.getByRole('toolbar', { name: 'Bulk actions for 2 selected tasks', exact: true })).toBeVisible()
  await expect(page.locator('tbody tr').first().getByRole('checkbox', { name: 'Select row', exact: true })).toBeChecked()
  await page.getByRole('button', { name: 'Go to next page', exact: true }).click()
  await expect(page.locator('tbody tr').first().locator('td').nth(1)).toHaveText(second.id)
  await expect(page.locator('tbody tr').first().getByRole('checkbox', { name: 'Select row', exact: true })).toBeChecked()
  result.checks.push('Clearing filter restores both selections, verified on both pages')

  await page.getByRole('button', { name: 'Title', exact: true }).click()
  await page.getByRole('menuitem', { name: 'Desc', exact: true }).click()
  const descending = [first, second].sort((a, b) => b.title.localeCompare(a.title))
  await saveAndVerify('sorted-descending.csv', descending)
  result.checks.push('CSV rows follow current descending title sort across pages')

  await page.getByRole('button', { name: 'Clear selection', exact: true }).click()
  await expect(exportButton).toHaveCount(0)
  assert.equal(downloadEvents.length, 3)
  result.checks.push('Clearing selection removes export control and creates no extra download')
  result.status = 'passed'
} catch (error) {
  result.status = 'failed'
  result.error = { message: String(error.message), stack: String(error.stack) }
  if (page) {
    await page.screenshot({ path: path.join(outputDirectory, 'failure.png'), fullPage: true }).catch(() => {})
  }
  process.exitCode = 1
} finally {
  if (browser) {
    await browser.close().catch((error) => {
      result.status = 'failed'
      result.closeError = String(error.message)
      process.exitCode = 1
    })
  }
  result.completedAt = new Date().toISOString()
  writeFileSync(path.join(outputDirectory, 'result.json'), JSON.stringify(result, null, 2))
  console.log(JSON.stringify(result, null, 2))
}
