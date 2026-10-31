"""Preserved files and old-report rational structure only; no research run."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import re

stage = Path(__file__).resolve().parents[4]
repo = stage.parent.parent / "boss4-research"
ws = Path(__file__).resolve().parent
ev = stage / "archives/customer-attraction/tools/evidence/adaptive-relay-source-payment-primary"
primary = json.loads((ev / "source-manifest.json").read_text())
related = json.loads((ev / "related-source-manifest.json").read_text())
checks = []
def check(label, ok):
    assert ok, label
    checks.append(label)
check("five primary MD sources 27821B", len(primary) == 5 and sum(r["size"] for r in primary) == 27821 and all(r["path"].endswith(".md") for r in primary))
check("three related originals 9270B", len(related) == 3 and sum(r["size"] for r in related) == 9270)
for r in primary + related:
    p = stage / r["preserved_path"]
    check("original bytes " + r["id"], p.stat().st_size == r["size"] and hashlib.sha256(p.read_bytes()).hexdigest() == r["sha256"])
byid = {r["id"]: r for r in related}
a = json.loads((stage / byid["cde437a1f0c18a9f7db4"]["preserved_path"]).read_text())
b = json.loads((stage / byid["c4d194bea9e92c7ec3f6"]["preserved_path"]).read_text())
check("historical report counts only", a["status"] == b["status"] == "passed" and a["sources"] == b["sources"] == 9 and a["activation_vectors_per_source"] == 64 and a["state_polynomial_checks"] == b["exact_marginal_comparisons"] == 81 and a["role_entry_checks"] == 18 and b["priority_worlds"] == 720 and b["unit_routes"] == 6480 and b["each_source_unit_in_every_world"] is True and b["proves_general_budget"] is False)
check("nine historical sources unit total absorption", len(a["reports"]) == 9 and all(F(r["total_absorb"]) == 1 and sum((F(s["absorb"]) for s in r["states"]), F()) == 1 for r in a["reports"]))
check("33 serialized positive historical cells", sum(len(r["states"]) for r in a["reports"]) == 33 and all(F(s["absorb"]) > 0 for r in a["reports"] for s in r["states"]))
first = a["reports"][0]
rows = {tuple(r["state"]): r for r in first["states"]}
check("old c4 nonowner Beta2 value", first["source"] == [0, "a"] and rows[1, "b"]["c"] == 4 and F(rows[1, "b"]["absorb"]) == F(1, 20))
check("old same-role entry and absorption sums", F(rows[3, "a"]["entry"]) + F(rows[3, "b"]["entry"]) == F(1, 2) and F(rows[3, "a"]["absorb"]) + F(rows[3, "b"]["absorb"]) == F(1, 12))
receipts = json.loads((ws / "semantic-receipts.json").read_text())
check("five exact primary receipt ids", len(receipts) == 5 and {r["id"] for r in receipts} == {r["id"] for r in primary})
for r in receipts:
    check("full semantic receipt " + r["id"], all(r[k] is True for k in ["full_file_reviewed", "related_material_checked", "unique_content_accounted_for"]) and all(len(r[k]) > 80 for k in ["read_note", "comparison_note", "decision_note"]) and all((stage / p).is_file() for p in r["targets"]))
formal = list(stage.glob("archives/customer-attraction/state/*/*.md"))
check("four distinct formal objects and valid frozen refs", len(formal) == 4 and len({re.search(r"^id: (.+)$", p.read_text(), re.M).group(1) for p in formal}) == 4 and all(c in {"68fad804ec5946cb296f77dc5b336308a66abf12", "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"} for p in formal for c in re.findall(r"source:([^:\s]+):", p.read_text())))
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
check("all local links resolve", links > 20)
result = {"status": "PASS", "scope": "source bytes, receipts, links and frozen-report rational arithmetic; original research program calls: 0; no new activation/rank/SPE enumeration", "checks_passed": len(checks), "links_checked": links, "analytic_math_self_check_items": 20, "checks": checks}
(ws / "evidence-self-check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
