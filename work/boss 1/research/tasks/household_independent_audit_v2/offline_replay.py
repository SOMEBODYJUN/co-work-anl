"""Real local file:// Playwright audit. Uses only an already installed, authorized local Chromium.
No installation, network requests or serving via HTTP. A failed launch is recorded as blocked.
Example: python offline_replay.py --chromium /path/to/installed/chrome
"""
import argparse
import collections
import csv
import datetime as dt
import gzip
import hashlib
import io
import json
import os
import shutil
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--chromium', type=Path)
parser.add_argument('--html', type=Path, default=HERE.parent / 'household_engine' / 'calculator.html')
args = parser.parse_args()
source = args.html.resolve()
artifact = HERE / 'browser_artifacts'
runtime = HERE / 'browser_tmp'
runtime.mkdir(exist_ok=True)
os.environ['TMPDIR'] = str(runtime)
sha = lambda b: hashlib.sha256(b).hexdigest()
log = {'schema': 'independent-offline-audit.v1', 'reviewer': '/root/household_independent_audit', 'file': str(source),
    'uri': source.as_uri(), 'htmlSha256': sha(source.read_bytes()),
    'startedUtc': dt.datetime.now(dt.timezone.utc).isoformat(), 'actions': [], 'network': [], 'consoleErrors': [],
    'downloads': [], 'screenshots': [], 'geometry': [], 'pending': []}
steps = ['Open the actual file in an offline browser, verify missing amounts and reject incomplete input',
    'Explicitly load demo, change an income range, add and value a property, vehicle and linked loan',
    'Edit a scenario value, range and assumption type, rerun and switch rankings and scenarios',
    'Export JSON, all strategies, all months and selected months with file contents checked',
    'Delete the three new records, recompute and reimport edited JSON, reproduce the 120-month table',
    'Read monthly table and chart, change visible selectors and run reverse stress',
    'Open at 390px and 320px, check document geometry, scroll wide tables, save screenshots',
    'Confirm zero external requests and zero console or script errors throughout']

def success(what, details=None):
    log['actions'].append({'operation': what, 'result': details})

def expect(name, actual, expected):
    if actual != expected:
        raise AssertionError(f'{name} observed {actual!r}, expected {expected!r}')
    success(name, actual)

def opened(locator):
    return locator.evaluate('x=>x.open')

def expand(page, selector):
    box = page.locator(selector)
    if not opened(box):
        box.locator(':scope > summary').click()

def edit(page, selector, value):
    item = page.locator(selector)
    item.fill(str(value))
    item.press('Tab')

def run(page):
    page.locator('#run').click()
    page.locator('#results:not([hidden]) #allCSV').wait_for(timeout=120000)
    success('Run complete', page.locator('#status').inner_text())

def select_tab(page, id):
    page.locator(f'[data-tab="{id}"]').click()
    page.locator(f'#{id}:not([hidden])').wait_for()

def select(page, id, value):
    page.locator(id).select_option(value)

def take(page, name):
    p = artifact / name
    page.screenshot(path=str(p), animations='disabled')
    log['screenshots'].append({'file': p.name, 'sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size})

def retrieve(page, button, name):
    with page.expect_download(timeout=180000) as event:
        page.locator(button).click()
    d = event.value
    d.save_as(str(artifact / name))
    p = artifact / name
    data = p.read_bytes()
    log['downloads'].append({'name': name, 'offeredName': d.suggested_filename, 'sha256': sha(data), 'bytes': len(data)})
    return p

def csv_rows(p):
    with p.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def slim(p):
    compressed = p.with_suffix(p.suffix + '.gz')
    compressed.write_bytes(gzip.compress(p.read_bytes(), mtime=0))
    p.unlink()
    log['downloads'][-1]['compressedFile'] = compressed.name

def watch(context):
    context.on('request', lambda r: log['network'].append({'url': r.url,
        'mode': r.resource_type}) if r.url.startswith(('http:', 'https:', 'ws:', 'wss:')) else None)
    context.on('page', lambda p: (p.on('pageerror', lambda e: log['consoleErrors'].append(str(e))), p.on('console',
        lambda m: log['consoleErrors'].append(m.text) if m.type == 'error' else None)))

def geometry(page, tab):
    g = page.evaluate("() => ({viewport:innerWidth, page:document.documentElement.scrollWidth, body:document.body.scrollWidth, bad:[...document.querySelectorAll('button,select,svg.chart,input,textarea')].filter(e=>{\n      if(!e.getClientRects().length||e.closest('.scroll')||e.closest('.tabs'))return false;\n      const r=e.getBoundingClientRect();return r.right>innerWidth+2||r.left< -2;\n    }).map(e=>e.id||e.tagName), chart:document.querySelector('svg.chart')?.getBoundingClientRect().width||0})")
    log['geometry'].append(dict(g, tab=tab))
    if g['page'] > g['viewport'] + 2 or g['body'] > g['viewport'] + 2 or g['bad']:
        raise AssertionError(f'clipped page/control {tab}: {g}')

def edit_collections(page):
    chosen = {}
    for group, fieldvals in [('properties', {'name': '审计新增住宅', 'city': '独立测试城', 'value': 50000, 'saleValue': 44123,
        'rent': 199, 'carry': 54}), ('vehicles', {'name': '审计新增车辆', 'value': 4500, 'saleValue': 3200, 'carry': 8}),
        ('loans', {'name': '审计新增关联贷款', 'principal': 4230, 'annualRate': 5, 'months': 10})]:
        expand(page, '#g-' + group)
        n = page.locator(f'#g-{group} > .in > .item').count()
        page.locator(f'[data-add="{group}"]').click()
        i = n
        for k, v in fieldvals.items():
            edit(page, f'#f-{group}-{i}-{k}', v)
        if group == 'loans':
            select(page, f'#f-{group}-{i}-kind', 'mortgage')
            edit(page, f'#f-{group}-{i}-collateral', chosen['properties']['id'])
        chosen[group] = {'index': i, 'id': page.locator(f'#f-{group}-{i}-id').input_value()}
        expect('Added ' + group, page.locator(f'#g-{group} > .in > .item').count(), n + 1)
    return chosen

def change_paths(page):
    expand(page, '#g-scenario')
    values = json.loads(page.locator('#rawPaths').input_value())
    s = next((v for v in values if v.get('role') == 'severe' or v['id'] == 'severe'))
    select(page, '#editScenario', s['id'])
    i = next((i for i, p in enumerate(s['paths']) if p['key'] == 'wageFactor'))
    edit(page, f'[data-pi="{i}"][data-pp="value"]', 0.81)
    expand(page, '#scenarioEditor > details')
    values = json.loads(page.locator('#rawPaths').input_value())
    s = next((x for x in values if x['id'] == s['id']))
    row = s['paths'][i]
    if row['value'] != 0.81:
        raise AssertionError('path table edit did not reach the JSON data')
    row.update(value={'low': 0.72, 'base': 0.81, 'high': 1.09}, range=[0.72, 1.09], assumption='historical',
        sourceId='independent-synthetic-ui-fixture')
    page.locator('#rawPaths').fill(json.dumps(values, ensure_ascii=False))
    page.locator('#applyPaths').click()
    expect('Applied an explicit alternative assumption', page.locator('#status').inner_text(), '情景输入已应用。')
    return s['id']

def get_month_table(page, scenario, plan, tag):
    select_tab(page, 'ledger')
    select(page, '#ledger #resultScenario', scenario)
    select(page, '#ledger #selectedPlan', plan)
    expect('Visible ledger selector changed after tab switch', page.locator('#ledger #selectedPlan').input_value(), plan)
    p = retrieve(page, '#ledger #oneCSV', tag + '.csv')
    rows = csv_rows(p)
    expect('Selected CSV scenario and plan', sorted({(r['scenario'], r['strategy']) for r in rows}), [(scenario, plan)])
    expect('Selected CSV month coverage', [int(r['month']) for r in rows], list(range(1, 121)))
    return rows

def inspect_ui(browser):
    artifact.mkdir(exist_ok=True)
    ctx = browser.new_context(viewport={'width': 1280, 'height': 900}, offline=True, accept_downloads=True,
        locale='zh-CN')
    watch(ctx)
    page = ctx.new_page()
    page.goto(source.as_uri(), wait_until='load')
    page.set_default_timeout(20000)
    expect('Initial original amounts empty', [page.locator('#f-base-0-cash').input_value(),
        page.locator('#f-base-0-minimumLiving').input_value()], ['', ''])
    expect('No sample enabled initially', '示例' in page.locator('#kind').inner_text(), False)
    page.locator('#run').click()
    page.locator('#status.error').wait_for()
    success('Rejected blank household', page.locator('#status').inner_text())
    take(page, 'desktop_blank.png')
    page.locator('#loadDemo').click()
    expect('Sample appears only after action', '合成示例' in page.locator('#kind').inner_text(), True)
    select(page, '#limit', '100')
    run(page)
    raw = retrieve(page, '#exportJSON', 'demo_before.json')
    bundle = json.loads(raw.read_text())
    severe = next((s['id'] for s in bundle['scenarios'] if s.get('role') == 'severe' or s['id'] == 'severe'))
    before = get_month_table(page, severe, 'S000', 'before_months')
    select_tab(page, 'inputs')
    expand(page, '#g-incomes')
    expand(page, '[data-row="incomes-0"]')
    edit(page, '#f-incomes-0-monthly', '17000~18000~20000')
    select(page, '#f-base-0-preference', 'wealth')
    created = edit_collections(page)
    severe = change_paths(page)
    run(page)
    expect('Synthetic label survives editing and calculation', '合成示例' in page.locator('#kind').inner_text(), True)
    select(page, '#results #resultScenario', severe)
    select(page, '#results #objective', 'regret')
    expect('Objective changed on results', page.locator('#results #objective').input_value(), 'regret')
    take(page, 'desktop_results.png')
    table_first = page.locator('#results .scroll.tall tbody tr').first.locator('td').first.inner_text().strip()
    results_file = retrieve(page, '#allCSV', 'strategies.csv')
    results = csv_rows(results_file)
    plans = sorted({r['strategy'] for r in results})
    scenarios = sorted({r['scenario'] for r in results})
    expect('Unique policy / scenario exports', len(results), len(plans) * len(scenarios))
    expect('Actual candidate count', len(plans), 100)
    common = {r['strategy']: float(r['maxRegretReal']) for r in results if r['commonFeasible'] == 'true'}
    if common and abs(common[table_first] - min(common.values())) > 1e-06:
        raise AssertionError('UI regret sort differs from exported feasible set')
    edited = retrieve(page, '#exportJSON', 'edited_input.json')
    editbundle = json.loads(edited.read_text())
    expect('Exported edited income range', editbundle['household']['incomes'][0]['monthly'], {'low': 17000,
        'base': 18000, 'high': 20000})
    expect('New asset-to-loan link preserved', editbundle['household']['loans'][-1]['collateral'],
        created['properties']['id'])
    ex = next((p for sc in editbundle['scenarios'] if sc['id'] == severe for p in sc['paths'] if p['key'] == 'wageFactor'))
    expect('Scenario metadata and range persist', [ex['assumption'], ex['value']], ['historical', {'low': 0.72,
        'base': 0.81, 'high': 1.09}])
    expect('Demo still marked in exported household', editbundle['household']['dataKind'], 'synthetic_example')
    full = retrieve(page, '#fullCSV', 'all_months.csv')
    states = collections.Counter()
    ledger = {}
    n = 0
    with full.open(encoding='utf-8-sig', newline='') as f:
        for r in csv.DictReader(f):
            n += 1
            key = (r['scenario'], r['strategy'])
            ledger[key] = ledger.get(key, 0) + 1
            states[r['state']] += 1
            if r['state'] == 'truncated' and (r['cash'] or r['netWorth']):
                raise AssertionError('post-failure CSV has cash/wealth')
    expect('All-policy / scenario / monthly data exported', [len(ledger), n, set(ledger.values()) == {120}],
        [len(results), len(results) * 120, True])
    success('Full CSV outcome states', dict(states))
    slim(full)
    edited_rows = get_month_table(page, severe, 'S000', 'edited_months')
    expect('Editing materially changed the first income, debt and cash',
        [edited_rows[0][k] != before[0][k] for k in ('income', 'debt', 'cash')], [True] * 3)
    expect('Actual ledger presents month rows', page.locator('#ledger .scroll.tall tbody tr').count(),
        sum((r['state'] != 'truncated' for r in edited_rows)))
    amount = page.locator('#ledger svg.chart path').last.get_attribute('d')
    select(page, '#ledger #chartKey', 'debt')
    after = page.locator('#ledger svg.chart path').last.get_attribute('d')
    expect('Chart reflects a new real series', bool(after and after != amount), True)
    expect('English chart title', page.locator('#ledger svg.chart title').text_content(), 'Debt balance by month')
    take(page, 'desktop_ledger.png')
    alt = next((x for x in plans if x != 'S000'))
    select(page, '#ledger #selectedPlan', alt)
    select(page, '#ledger #comparePlan', 'S000')
    expect('Ledger redraw links visible selected action',
        alt in page.locator('#ledger #selectedPlan option:checked').inner_text(), True)
    select_tab(page, 'reverse')
    select(page, '#reverse #resultScenario', severe)
    select(page, '#reverse #selectedPlan', alt)
    page.locator('#stressRun').click()
    page.locator('#stressOutput table').first.wait_for(timeout=180000)
    success('Reverse stress contains numerical outputs', page.locator('#stressOutput table tbody tr').first.inner_text())
    select_tab(page, 'inputs')
    for group in ('loans', 'vehicles', 'properties'):
        meta = created[group]
        expand(page, '#g-' + group)
        expand(page, f'''[data-row="{group}-{meta['index']}"]''')
        page.locator(f'''[data-remove="{group}"][data-i="{meta['index']}"]''').click()
        expect('Deleted added ' + group, page.locator(f'#g-{group} > .in > .item').count(), meta['index'])
    run(page)
    deleted = get_month_table(page, severe, 'S000', 'after_delete_months')
    expect('Deleting loan altered baseline debt', float(deleted[0]['debt']) < float(edited_rows[0]['debt']), True)
    select_tab(page, 'inputs')
    page.locator('#clearInputs').click()
    expect('Cleared input cash', page.locator('#f-base-0-cash').input_value(), '')
    page.locator('#importFile').set_input_files(str(edited))
    page.get_by_text('JSON 已载入，请运行当前输入。').wait_for()
    run(page)
    reloaded = get_month_table(page, severe, 'S000', 'roundtrip_months')
    expect('Edited JSON restores all 120 baseline rows', edited_rows == reloaded, True)
    fixture = {'schema': 'household-offline.bundle.v1', 'household': {'schema': 'household-cny.v1',
        'dataKind': 'synthetic_example', 'rangeCase': 'base', 'cash': 10, 'cashAnnual': 0, 'reserveMonths': 0,
        'minimumLiving': 70, 'cutFraction': 0, 'maxSaleWait': 120, 'preference': 'cash', 'incomes': [], 'expenses': [],
        'financial': [], 'properties': [], 'vehicles': [], 'loans': [], 'citySources': []}, 'scenarios': [{'id': 'ui',
        'name': 'audit', 'paths': []}]}
    f = artifact / 'failure_input.json'
    f.write_text(json.dumps(fixture, ensure_ascii=False))
    select_tab(page, 'inputs')
    page.locator('#importFile').set_input_files(str(f))
    page.get_by_text('JSON 已载入，请运行当前输入。').wait_for()
    run(page)
    expect('Visible no-feasible warning and next cash gap',
        '无共同可行方案' in page.locator('#results').inner_text() and '60' in page.locator('#results .verdict').inner_text(),
        True)
    truncated = get_month_table(page, 'ui', 'S000', 'failure_months')
    expect('Correct failure and blank wealth in later encoded rows', [truncated[0]['state'], truncated[0]['unpaid'],
        truncated[1]['state'], truncated[1]['netWorth'], truncated[-1]['realNetWorth']], ['cash_failure', '60',
        'truncated', '', ''])
    ctx.close()
    for width in (390, 320):
        mobile = browser.new_context(viewport={'width': width, 'height': 844}, is_mobile=True, has_touch=True,
            device_scale_factor=1, offline=True, accept_downloads=True, locale='zh-CN')
        watch(mobile)
        p = mobile.new_page()
        p.goto(source.as_uri())
        geometry(p, 'blank')
        p.locator('#importFile').set_input_files(str(edited))
        p.get_by_text('JSON 已载入，请运行当前输入。').wait_for()
        select(p, '#limit', '100')
        take(p, f'mobile_{width}_input.png')
        run(p)
        geometry(p, 'results')
        take(p, f'mobile_{width}_results.png')
        select_tab(p, 'ledger')
        geometry(p, 'ledger')
        p.locator('#ledger svg.chart').scroll_into_view_if_needed()
        take(p, f'mobile_{width}_chart.png')
        v = p.locator('#ledger .scroll.tall').evaluate('x=>{const w=x.scrollWidth;const client=x.clientWidth;x.scrollLeft=w;return {scrollWidth:w,viewport:client,moved:x.scrollLeft>0}}')
        expect('Wide table can be scrolled inside its visible panel ' + str(width), v['moved'], True)
        mobile.close()
    expect('External requests', log['network'], [])
    expect('Browser console/script errors', log['consoleErrors'], [])

def main():
    started = False
    try:
        with sync_playwright() as pw:
            selected = args.chromium or (Path(os.environ['AUDIT_CHROMIUM']) if os.getenv('AUDIT_CHROMIUM') else None)
            stock = Path(pw.chromium.executable_path)
            system = shutil.which('chromium')
            choices = [selected] if selected else [stock, Path('/usr/lib/chromium/chromium'),
                Path(system) if system else None]
            log['candidateBinaries'] = [{'path': str(p), 'isFile': p.is_file()} for p in choices if p]
            exe = next((p for p in choices if p and p.is_file()), None)
            if not exe:
                raise RuntimeError('No installed local Chromium executable or launcher')
            log['launchExecutable'] = str(exe)
            browser = pw.chromium.launch(headless=True, executable_path=str(exe), args=['--no-sandbox',
                '--disable-dev-shm-usage'])
            started = True
            log['browserVersion'] = browser.version
            try:
                inspect_ui(browser)
            finally:
                browser.close()
        log['verdict'] = 'automated_interactions_pass'
        log['pending'] = ['Independent reviewer must visually inspect the saved desktop and mobile screenshots.']
        return 0
    except Exception as exc:
        log['verdict'] = 'fail' if started else 'blocked'
        log['stage'] = 'interaction' if started else 'browser-launch'
        log['reason'] = str(exc)
        log['pending'] = steps if not started else ['See last completed operation and error before continuing.']
        return 1 if started else 3
    finally:
        log['finishedUtc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        (HERE / 'offline_attempt.json').write_text(json.dumps(log, indent=2, ensure_ascii=False) + '\n')
        print(json.dumps({k: log.get(k) for k in ('verdict', 'stage', 'reason', 'launchExecutable', 'htmlSha256')},
            ensure_ascii=False))
        shutil.rmtree(runtime, ignore_errors=True)
if __name__ == '__main__':
    sys.exit(main())
