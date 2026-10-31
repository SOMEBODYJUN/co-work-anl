"""Read-only artifact/receipt/report-structure checks; no math program invocation."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re

stage = Path(__file__).resolve().parents[4]
repo = stage.parent.parent / "boss4-research"
ev = stage / "archives/customer-attraction/tools/evidence/owner-hybrid-start-prices-primary"
ws = Path(__file__).resolve().parent
primary = json.loads((ev / "source-manifest.json").read_text())
related = json.loads((ev / "related-source-manifest.json").read_text())
checked = []
def check(label, ok):
    assert ok, label
    checked.append(label)
check("five primary MD sources / 43692 bytes", len(primary) == 5 and sum(r["size"] for r in primary) == 43692 and all(r["path"].endswith(".md") for r in primary))
check("five related originals / 21479 bytes", len(related) == 5 and sum(r["size"] for r in related) == 21479)
for r in primary + related:
    p = stage / r["preserved_path"]
    check("original bytes " + r["id"], p.stat().st_size == r["size"] and hashlib.sha256(p.read_bytes()).hexdigest() == r["sha256"])
receipts = json.loads((ws / "semantic-receipts.json").read_text())
check("receipt ids exactly primary ids", len(receipts) == 5 and {r["id"] for r in receipts} == {r["id"] for r in primary})
for r in receipts:
    check("complete receipt " + r["id"], all(r[k] is True for k in ["full_file_reviewed", "related_material_checked", "unique_content_accounted_for"]) and r["disposition"] == "integrated" and all(len(r[k]) > 80 for k in ["read_note", "comparison_note", "decision_note"]) and all((stage / t).is_file() for t in r["targets"]))
formal = list(stage.glob("archives/customer-attraction/state/*/*.md"))
check("five distinct new formal objects", len(formal) == 5 and all(not (repo / p.relative_to(stage)).exists() for p in formal))
links = 0
for p in stage.rglob("*.md"):
    if "original" in p.parts or "related-original" in p.parts:
        continue
    for target in re.findall(r"\]\(([^)]+)\)", p.read_text()):
        if "://" in target or target.startswith("#"):
            continue
        q = (p.parent / target.split("#")[0]).resolve()
        rel = q.relative_to(stage)
        assert q.exists() or (repo / rel).exists(), (str(p), target)
        links += 1
check("local markdown links resolve", links > 20)
byid = {r["id"]: r for r in related}
a = json.loads((stage / byid["c1b105cbcfc2cf3c4881"]["preserved_path"]).read_text())
k = json.loads((stage / byid["9e4d8c1152b183032db1"]["preserved_path"]).read_text())
check("historical A/B report structure and finite counts", a["status"] == "PASS" and a["counts"]["instances"] == len(a["cases"]) == 9 and a["counts"]["owner_partitions"] == 14 and a["counts"]["profiles"] == a["counts"]["maxflow_A"] == a["counts"]["maxflow_B"] == 852 and a["counts"]["cuts"] == a["counts"]["polynomial_integrals"] == 11474)
check("historical kappa report nine names thirteen leaves", len(k) == 13 and len({r["name"] for r in k}) == 9 and all(r["bridge_holds"] is True for r in k))
check("historical kappa counter fields sum 137; no reinterpretation", sum(r["bellman_bruteforce_checks"] for r in k) == 137)
portfolio = next(r for r in k if r["name"] == "portfolio_matching_failure")
check("older portfolio is distinct W41 path21", portfolio["path"] == [2, 1] and portfolio["W"] == "41" and portfolio["G"] == 12 and set(portfolio["kappa"].values()) == {"1", "38/37", "19/18"})
prefix = next(r for r in k if r["name"] == "prefix_balance_failure")
check("older prefix nonunit price and positive-tax cost retained", prefix["cheapest_residual_cost"] == "179/22" and "45/44" in prefix["kappa"].values())
result = {"status": "PASS", "scope": "source bytes, receipt targets, local links, and frozen-report structure only; no source/math program execution", "checks_passed": len(checked), "links_checked": links, "analytic_math_self_check_items": 18, "mathematical_program_invocations_in_batch": 0, "checks": checked}
(ws / "artifact-check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
