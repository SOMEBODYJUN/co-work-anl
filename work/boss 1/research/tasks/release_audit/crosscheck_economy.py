"""Read-only final-review checks against the preserved source and calculation artifacts."""
import csv
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path
from statistics import mean

import pandas as pd
import xlrd

HERE = Path(__file__).resolve().parent
W = HERE.parents[2]
REPO = HERE.parents[4]
R = W / "research"
BK = R / "tasks/bank_research"
PF = R / "tasks/property_fiscal"


def load(path):
    return json.loads(path.read_text())


def table(path):
    with path.open() as handle:
        return list(csv.DictReader(handle))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def same(actual, expected, atol=1e-8):
    assert abs(actual - expected) <= atol, (actual, expected)


def bank_originals():
    sources = {s["id"]: s for s in load(BK / "sources.json")}
    checks = {
        "icbc_q3": ("BK003", {5:["1,509.22"],25:["3,982,891","30,478,278","13.07"],26:["2.0%","1.5%"]}),
        "icbc_h1": ("BK005", {15:["3,940,780","29,832,780"],73:["123,031"]}),
        "lanzhou_q3": ("BK004", {6:["31,168,341","138.20"],7:["353,312,649","7.46","5.64"],8:["2,691,809"]}),
        "lanzhou_h1": ("BK006", {12:["30,638,408","350,055,742"],46:["1,996,881"]}),
    }
    pdf = {}
    for name, (sid, pages) in checks.items():
        source = BK / "cache" / (name + ".pdf")
        assert digest(source) == sources[sid]["sha256_original"]
        for page, needles in pages.items():
            body = subprocess.check_output(["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(source), "-"]).decode()
            assert all(needle in body for needle in needles), (name, page)
        pdf[sid] = {"file":str(source.relative_to(W)), "source_sha256":digest(source), "PDF_pages_and_figures":pages,
                    "url":sources[sid]["url"]}
    files = {"BK001":"by_type.xls", "BK002":"industry.xls", "BK010":"1208455.xls", "BK011":"1208453.xls",
             "BK012":"1164262.xls", "BK013":"1164263.xls"}
    series = table(BK / "regulatory_series.csv")
    sheets = {}
    for sid, fname in files.items():
        source = BK / "cache" / fname
        assert digest(source) == sources[sid]["sha256_original"]
        book = xlrd.open_workbook(source)
        maximum_error = 0.
        matched = [row for row in series if row["source_id"] == sid]
        for row in matched:
            sheet = book.sheet_by_name(row["sheet"])
            col, num = re.fullmatch(r"([A-Z])([0-9]+)", row["cell"]).groups()
            val = sheet.cell_value(int(num)-1,ord(col)-ord("A"))
            reported = val * (100 if row["unit"] == "百分比" else 1)
            maximum_error = max(maximum_error, abs(reported-float(row["value"])))
        assert maximum_error < 1e-7
        sheets[sid] = {"file":str(source.relative_to(W)), "sha256":digest(source), "cells_compared":len(matched),
                       "maximum_absolute_difference":maximum_error}
    assert sum(v["cells_compared"] for v in sheets.values()) == 770
    industry = xlrd.open_workbook(BK/"cache/industry.xls").sheet_by_index(0)
    assert "2000亿元以上" in industry.cell_value(48,0)
    lcr, nsfr = (round(100*industry.cell_value(i,3),2) for i in (24,25))
    assert (lcr,nsfr)==(155.67,128.89)
    cap = 31168341 / 100000
    rwa = 353312649 / 100000
    annual_extra = 2691809 / 100000 * 12 / 9
    ratio = 100 * (cap-annual_extra) / (rwa*1.05)
    deficit = (cap-annual_extra) - .075*rwa*1.05
    same(ratio, 7.4342, .00001)
    same(deficit, -2.44109, .00001)
    return {"pdfs":pdf, "workbooks":sheets, "lcr_nsfr_percent_large_banks":[lcr,nsfr],
            "lanzhou_q3_conditional_no_new_earnings_cny_100m":{
                "opening_CET1":cap, "opening_RWA":rwa, "extra_annualized_AC_charge":annual_extra,
                "CET1_with_RWA_plus_5_percent":ratio, "headroom_against_7_5_percent":deficit},
            "icbc_q3_static_50bp_requirement_cny_100m":30478278/100*.005}


def sectors():
    fiscal = {r["period"]:r for r in table(PF/"fiscal_releases.csv")}
    fields = ["land_receipts","land_related_outlay","local_general_own_income","local_funds_own_income",
              "local_general_outlay","local_funds_outlay"]
    changes = {k:int(fiscal["2026M10"][k])-int(fiscal["2025M10"][k]) for k in fields}
    assert list(changes.values()) == [-6456,-5833,3001,-6289,336,-6811]
    auxiliary = {(r["indicator"],r["period"]):float(r["value"]) for r in table(PF/"supplemental.csv")}
    share = 100 * auxiliary["refinancing_for_matured_principal","2026M10"] / auxiliary["statutory_bond_principal_due","2026M10"]
    same(share,86.19,.005)
    period = {r["period"]:r for r in table(PF/"property_releases.csv")}
    property_changes = {k:100*(float(period["2025"][k])/float(period["2021"][k])-1)
                        for k in ["sales_value","sales_area","starts_area","developer_funds"]}
    for actual, expected in zip(property_changes.values(), [-53.9,-50.9,-70.5,-53.7]):
        same(actual, expected, .06)
    indices = table(PF/"cities_price_202610.csv")
    cities={}
    for market,n,change in [("new",63,-2.73),("resale",68,-4.36)]:
        sub = [float(x["yoy_index"])-100 for x in indices if x["market"]==market]
        assert len(sub)==70 and sum(x<0 for x in sub)==n
        same(mean(sub),change,.005)
        cities[market]={"down_of_70":n,"equal_weight_index_change_pct":mean(sub)}
    equity = load(R/"models/equity_real_return_input.json")
    nominal = math.prod(1+i/100 for i in equity["annual_net_total_return_percent"])
    prices = equity["cpi_2024_12"]*(1+equity["cpi_2025_12_yoy_percent"]/100)/equity["cpi_2015_12"]
    real = 100*(nominal/prices-1)
    same(real,13.77686,.00001)
    return {"2026_vs_2025_Jan_Oct_changes_cny_100m":changes, "difference_of_two_land_lines":changes["land_receipts"]-changes["land_related_outlay"],
            "executed_matured_principal_refinance_share_pct":share, "2021_to_2025_first_releases_change_pct":property_changes,
            "october_cities":cities, "2016_to_2025_CNY_NET_real_return_pct":real,
            "Setser_3pct_deficit_debt_ratio_pct_at_3_and_4pct_nominal_growth":[100*(.30/(1+r)+.03) for r in [.03,.04]]}


def models():
    outputs = W/"compute/outputs"
    results = {}
    for prefix in ["historical-warning-v1","historical-warning-audit-v2","historical-warning-portable-v3"]:
        p = next(outputs.glob(prefix+"-*"))
        d = load(p)["result"]
        rows = d["test_predictions"]
        scores = {}
        for model, definition in d["models"].items():
            sub = [v for v in rows if v["model"]==model]
            positive = sum(r["event"] for r in sub)
            assert (len(sub),positive,len({r["event_id"] for r in sub if r["event"]})) == (187,39,13)
            for key,threshold,kind in [("raw_score","raw_alarm_threshold","raw_test"),("score","alarm_threshold","calibrated_test")]:
                brier = mean((r[key]-r["event"])**2 for r in sub)
                alarms = [r for r in sub if r[key]>definition[threshold]]
                detected = len({r["event_id"] for r in alarms if r["event"]})
                false = sum(1 for r in alarms if not r["event"])
                stored=definition[kind]
                same(brier,stored["brier"])
                assert (detected,13-detected)==(stored["detected_episodes"],stored["missed_episodes"])
                same(false/(187-positive),stored["false_alarm_fraction_negative_periods"])
                scores[model+"_"+key] = {"Brier":brier,"hit_of_13_events":detected,"false_of_148_non_event_years":false}
        results[prefix] = {"file":str(p.relative_to(W)), "split":[{k:v[k] for k in ["rows","as_of_max","last_label_maturity"]} for v in d["splits"].values()],
                           "baseline_Brier":d["baseline"]["brier"], "scores":scores}
    assert results["historical-warning-audit-v2"]["scores"] == results["historical-warning-portable-v3"]["scores"]
    assert [x["rows"] for x in results["historical-warning-audit-v2"]["split"]]==[1188,223,187]
    for label in ["long","single-vintage"]:
        d = load(next(outputs.glob("china-bridge-"+label+"-*")))["result"]
        r = d["predictions"]
        mae = {k:mean(abs(i[k]-i["actual"]) for i in r) for k in ["bridge","lag_baseline"]}
        same(mae["bridge"],d["bridge_mae"])
        same(mae["lag_baseline"],d["lag_baseline_mae"])
        results["bridge_"+label] = {"evaluation_quarters":len(r), "MAE_pp":mae}
    d=load(next(outputs.glob("china-nowcast-diagnostic-*")))["result"]
    actual=float(next(q for q in table(R/"data/gdp_quarterly_2026vintage.csv") if q["quarter"]=="2026Q3")["real_gdp_yoy"])
    same(d["updated_estimate"]-d["previous_estimate"],d["news_impact"])
    results["mixed_frequency"] = {"target":actual,"updated":d["updated_estimate"],"error_pp":d["updated_estimate"]-actual}
    hist = pd.read_stata(REPO/"research/models/jst_example/JSTdatasetR6.dta",convert_categoricals=False)
    named = {}
    for iso, peak in [("JPN",1991),("USA",2007)]:
        q = hist.loc[hist.iso.eq(iso)].set_index("year").sort_index().loc[peak:peak+10]
        p = q.iloc[-1].cpi/q.iloc[0].cpi
        home = 100 * ((q.iloc[-1].hpnom/q.iloc[0].hpnom)/p-1)
        stock = 100 * (math.prod(1+i for i in q["eq_tr"].iloc[1:])/p-1)
        independent=load(R/"tasks/research_independent_review/independent_history.json")["named"][iso]
        same(home,independent["real_home"])
        same(stock,independent["real_local_equities"])
        named[iso]={"local_peak":peak,"real_house_price_proxy_pct":home,"real_local_equity_total_return_pct":stock}
    results["selected_JST_peak_windows"] = named
    return results


def graph():
    state = load(W/"research_state.json")
    exported = load(R/"graph_current.json")
    formal = load(W/"formal/judgments.json")
    assert exported["revision"]==formal["graph_state_revision"]
    for k in ["nodes","edges"]:
        assert {a["id"]:a for a in exported[k]}==state[k]
    source_ids = set(state["sources"])
    for e in state["edges"].values():
        assert e["mode"]=="ALL" and e["status"]=="current" and len(e["tails"])>=2
        assert all([e["conditions"],e["mechanism"],e["counterevidence"],e["lag"],e["falsifier"]])
        assert set(e["tails"]) <= source_ids|set(state["nodes"])
        assert set(e["counterevidence"])<=source_ids and e["head"] in state["nodes"]
    for j in formal["judgments"]:
        node = state["nodes"][j["id"]]
        assert j["verdict"]==node["statement"] and j["graph_revision"]==node["revision"] and j["evidence_ids"]==node["evidence"]
        assert j["probability"] is None and all([j["mechanism_edges"],j["time_window"],j["change_condition"],j["household_implication"]])
    history = load(R/"receipts/proposals_applied.json")
    proposals = load(R/"tasks/research_independent_review/proposal_receipt.json")
    assert len(history) == len(proposals["reviews"])*3
    for rr in proposals["reviews"]:
        pid = rr["id"]
        assert digest(R/"proposals"/(pid+".json"))==rr["file_sha256"]
        operations = [x["command"][0] for x in history if x["result"]["id"]==pid]
        assert operations==["proposal","proposal-review","apply"]
        assert state["proposals"][pid]["status"]=="applied" and rr["verdict"]=="pass"
        assert state["proposals"][pid]["review"]["reviewer"]==proposals["reviewer"]
        for sid,bound in rr["new_sources"].items():
            src=state["sources"][sid]
            revisions = src.get("versions",[]) + [src]
            assert any(x["revision"]==bound["revision"] and x["body_sha256"]==bound["sha256"] for x in revisions)
    paths=load(W/"formal/scenarios.json")
    for s in paths:
        assert all(p["assumption"]=="stress_test" and p["editable"] and p["sourceId"] in source_ids for p in s["paths"])
    return {"graph_revision":exported["revision"], "nodes":len(state["nodes"]), "edges":len(state["edges"]),
            "adjudicated_judgments":len(formal["judgments"]), "proposal_triplets":len(history)//3,
            "ranked_paths":[p["id"] for p in formal["ranked_paths"]], "stress_parameters":[[p["id"],len(p["paths"])] for p in paths]}


if __name__ == "__main__":
    report = {"reviewer":"/root/release_audit","script_sha256":digest(Path(__file__)),
              "direct_source_check":"Original four bank PDFs and six original NFRA XLS were present in the audit machine's ignored cache. Restoring those raw files requires obtaining their matching original bytes; persistent rows and original hashes are separate.",
              "pdf_visual_scope":"Reviewer rendered ICBC Q3 PDF page 25 (KM1) and Lanzhou Q3 PDF page 6 to verify original column alignment, units and dated headers; other listed pages checked with layout-preserved PDF text.",
              "banks":bank_originals(),"sectors":sectors(),"models":models(),"graph":graph()}
    print(json.dumps(report,ensure_ascii=False,indent=2))
