"""Replay the offline UI checklist on a host with an installed, authorized Chromium."""
import argparse
import csv
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--browser", help="Path to an already-installed Chromium executable")
parser.add_argument("--html", type=Path, default=ROOT/"calculator.html")
parser.add_argument("--output", type=Path, required=True, help="New directory for an independent UI receipt and mobile screenshot")
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
seen, external, errors = [], [], []
with TemporaryDirectory(dir=args.output) as tmp:
    for var in ("TMPDIR", "XDG_CACHE_HOME", "XDG_CONFIG_HOME", "XDG_RUNTIME_DIR"):
        os.environ[var] = tmp
    with sync_playwright() as api:
        options={"headless":True}
        if args.browser:
            options["executable_path"] = args.browser
        browser = api.chromium.launch(**options)
        context = browser.new_context(offline=True, accept_downloads=True, viewport={"width":1200,"height":850})
        page=context.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("request", lambda r: external.append(r.url) if r.url.startswith(("http:", "https:")) else None)
        page.goto(args.html.resolve().as_uri())
        assert page.locator("#f-base-0-cash").input_value()=="" and page.locator("#f-base-0-minimumLiving").input_value()==""
        page.locator("#run").click()
        page.wait_for_function("document.querySelector('#status').classList.contains('error')")
        seen.append("empty form stays empty and rejects incomplete runs")
        page.locator("#loadDemo").click()
        assert "合成示例" in page.locator("#kind").inner_text()
        page.locator("#g-incomes > summary").click()
        page.locator('[data-row="incomes-0"] > summary').click()
        page.locator("#f-incomes-0-monthly").fill("15888")
        page.locator("#f-incomes-0-monthly").press("Tab")
        for group in ("financial","loans"):
            page.locator("#g-"+group+" > summary").click()
            original=page.locator('[data-remove="'+group+'"]').count()
            page.locator('[data-add="'+group+'"]').click()
            assert page.locator('[data-remove="'+group+'"]').count()==original+1
            page.locator('[data-remove="'+group+'"]').last.click()
            assert page.locator('[data-remove="'+group+'"]').count()==original
        seen.append("edited income and added/removed an asset and loan")
        page.locator("#limit").select_option("100")
        page.locator("#run").click()
        page.locator("#allCSV").wait_for(timeout=60000)
        page.locator("#resultScenario").select_option("severe")
        page.locator("#objective").select_option("regret")
        page.locator("#selectedPlan").select_option("S001")
        page.locator("[data-tab=ledger]").click()
        page.locator("#resultScenario").select_option("recovery")
        assert page.locator("#resultScenario").count()==1
        page.locator("#chartKey").select_option("debt")
        assert page.locator("svg.chart title").inner_text()=="Debt balance by month"
        seen.append("selected plan, objective and scenario, changed a bound chart, and viewed month ledger")
        def download(btn,name):
            with page.expect_download(timeout=120000) as d:
                page.locator(btn).click()
            path=Path(tmp)/name
            d.value.save_as(path)
            return path
        selected=download("#oneCSV","one.csv")
        with selected.open(encoding="utf-8-sig",newline="") as f:
            rows=list(csv.DictReader(f))
        assert len(rows)==120 and {r["strategy"] for r in rows}=={"S001"} and {r["scenario"] for r in rows}=={"recovery"}
        page.locator("[data-tab=results]").click()
        all_strats=download("#allCSV","strategies.csv")
        with all_strats.open(encoding="utf-8-sig",newline="") as f:
            assert len(list(csv.DictReader(f)))==300
        all_months=download("#fullCSV","all.csv")
        with all_months.open(encoding="utf-8-sig",newline="") as f:
            assert sum(1 for _ in csv.DictReader(f))==36000
        seen.append("downloaded and parsed selected ledger, every policy, and 36,000 policy/scenario months")
        page.locator("[data-tab=reverse]").click()
        page.locator("#stressRun").click()
        page.locator("#stressOutput table").first.wait_for(timeout=90000)
        seen.append("ran reverse stress and rendered cash thresholds")
        payload=download("#exportJSON","house.json")
        bundle=json.loads(payload.read_text())
        assert bundle["household"]["incomes"][0]["monthly"]==15888
        assert bundle["household"]["dataKind"]=="synthetic_example"
        page.locator("[data-tab=inputs]").click()
        page.locator("#clearInputs").click()
        page.locator("#importFile").set_input_files(payload)
        page.wait_for_function("document.querySelector('#kind').textContent.includes('合成示例')")
        assert page.locator("#f-base-0-cash").input_value()=="280000"
        seen.append("round-tripped synthetic JSON after clearing to a blank household")
        page.set_viewport_size({"width":390,"height":844})
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")
        page.screenshot(path=str(args.output/"mobile.png"),full_page=True)
        assert not external and not errors
        seen.append("390px viewport, no page overflow, no page errors and zero HTTP(S) requests")
        receipt={"status":"pass","file":str(args.html),"browser":browser.version,"operations":seen,"http_requests":external,"page_errors":errors}
        (args.output/"offline_ui.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
        browser.close()
