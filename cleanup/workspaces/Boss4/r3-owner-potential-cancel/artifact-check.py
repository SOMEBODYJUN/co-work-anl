"""Validate preserved bytes and one-run witness, without source execution."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import re

stage = Path(__file__).resolve().parents[4]
repo = stage.parent.parent / "boss4-research"
ev = stage / "archives/customer-attraction/tools/evidence/owner-potential-cancel-primary"
ws = Path(__file__).resolve().parent
primary = json.loads((ev / "source-manifest.json").read_text())
related = json.loads((ev / "related-source-manifest.json").read_text())
checks = []
def check(label, ok):
    assert ok, label
    checks.append(label)
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
check("five primary / 23959 bytes", len(primary) == 5 and sum(r["size"] for r in primary) == 23959)
check("two related / 7554 bytes", len(related) == 2 and sum(r["size"] for r in related) == 7554)
for r in primary + related:
    p = stage / r["preserved_path"]
    check("preserved bytes " + r["id"], p.stat().st_size == r["size"] and sha(p) == r["sha256"])
byid = {r["id"]: r for r in primary}
old = stage / byid["c1b105cbcfc2cf3c4881"]["preserved_path"]
report = json.loads(old.read_text())
meta = json.loads((ev / "replay/execution.json").read_text())
state = json.loads((ev / "replay/execution-state.json").read_text())
payload = json.loads((ev / "runtime-inputs.json").read_text())
check("true literal inputs: nine cases, no external files", len(payload["cases"]) == 9 and payload["external_files_read"] == [] and len(payload["standard_library_imports"]) == 6)
check("literal input matches all frozen case topics/T/m", all(a["name"] == b["name"] and a["topics"] == b["topics"] and a["optimal_tuple"] == b["optimal_tuple"] and a["players"] == b["players"] for a, b in zip(payload["cases"], report["cases"])))
check("selected owner and label-profile counts", sum(r["owner_choices"] for r in report["cases"]) == 14 and sum(r["profiles"] for r in report["cases"]) == 852 and all(r["profiles"] == r["owner_choices"] * len(r["topics"]) ** r["players"] for r in report["cases"]))
check("all-cut loop domain 11474", sum(r["profiles"] * (1 << r["players"]) for r in report["cases"]) == report["counts"]["cuts"] == report["counts"]["polynomial_integrals"] == 11474)
check("completed namespace counts equal frozen report", state["original_counts_from_completed_namespace"] == report["counts"])
check("one source invocation/module and no calls after return", meta["source_invocations"] == state["source_module_entries"] == 1 and state["source_function_calls_after_runpy_return"] == 0)
check("new report/stdout byte-identical, stderr empty", meta["returncode"] == 0 and old.read_bytes() == (stage / meta["new_report_path"]).read_bytes() == (ev / "replay/stdout.txt").read_bytes() and (ev / "replay/stderr.txt").read_bytes() == b"")
source = ev / "replay/source-root" / byid["cbcbaef21a8b55faeb69"]["path"]
check("runtime original source unchanged", sha(source) == byid["cbcbaef21a8b55faeb69"]["sha256"] == payload["source_sha256"])
rows = state["by_case_and_network"]
check("exactly 18 case/network groups", len(rows) == 18)
expected = {"A": [852, 424, 428, 652, 259], "B": [852, 424, 428, 827, 208]}
for net, values in expected.items():
    subset = [r for r in rows if r["network"] == net]
    totals = [sum(r[k] for r in subset) for k in ["calls", "positive_source_graphs", "zero_source_graphs", "augmentations", "graphs_with_positive_final_net_role_transfer"]]
    check("observed nonzero/zero execution " + net, totals == values and all(r["calls"] == r["positive_source_graphs"] + r["zero_source_graphs"] for r in subset))
check("combined actual observation counts", state["maxflow_function_calls"] == 1704 and state["positive_source_graphs"] == 848 and state["zero_source_graphs"] == 856 and state["positive_augmentations"] == 1479 and state["graphs_with_positive_final_net_role_transfer"] == 467)
for net, flow in [("A", F(1)), ("B", F(1, 2))]:
    w = state["first_observed_role_transfer_witnesses"][net]
    check("real backward role witness " + net, w["profile_bitmasks"] == [12, 20] and w["flow_value"] == "1" and w["positive_final_net_role_edges"] == [{"from": 1, "to": 0, "net_flow": str(flow)}] and F(w["capacity_matrix"][1][0]) >= flow)
receipts = json.loads((ws / "semantic-receipts.json").read_text())
check("receipt ids exactly five primary ids", len(receipts) == 5 and {r["id"] for r in receipts} == {r["id"] for r in primary})
for r in receipts:
    check("full receipt " + r["id"], all(r[k] is True for k in ["full_file_reviewed", "related_material_checked", "unique_content_accounted_for"]) and r["disposition"] == "integrated" and all(len(r[k]) > 80 for k in ["read_note", "comparison_note", "decision_note"]) and all((stage / p).is_file() for p in r["targets"]))
formal = list(stage.glob("archives/customer-attraction/state/*/*.md"))
check("five new formal objects", len(formal) == 5 and all(not (repo / p.relative_to(stage)).exists() for p in formal))
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
check("all local markdown links resolve", links > 25)
result = {"status": "PASS", "scope": "preserved bytes, literal data, saved single-run counts, receipt targets and links; original program executions in this check: 0", "checks_passed": len(checks), "links_checked": links, "analytic_math_self_check_items": 16, "checks": checks}
(ws / "artifact-check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
