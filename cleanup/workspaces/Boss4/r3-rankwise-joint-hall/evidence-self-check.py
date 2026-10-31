"""Saved-evidence checks and one already-used world's arithmetic; no source run."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib
import json
import re

stage = Path(__file__).resolve().parents[4]
repo = stage.parent.parent / "boss4-research"
ws = Path(__file__).resolve().parent
ev = stage / "archives/customer-attraction/tools/evidence/rankwise-joint-hall-primary"
manifest = json.loads((ev / "source-manifest.json").read_text())
related = json.loads((ev / "related-source-manifest.json").read_text())
checks = []
def check(label, ok):
    assert ok, label
    checks.append(label)
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
check("five primary 18202B plus one true input 6437B", len(manifest) == 6 and sum(r["size"] for r in manifest if r["role"] == "primary") == 18202 and sum(r["size"] for r in manifest if r["role"] != "primary") == 6437)
check("three related originals 17192B, no new batch", len(related) == 3 and sum(r["size"] for r in related) == 17192)
for r in manifest + related:
    p = stage / r["preserved_path"]
    check("original bytes " + r["id"], p.stat().st_size == r["size"] and sha(p) == r["sha256"])
byid = {r["id"]: r for r in manifest}
normal_path = stage / byid["80afdb959e750084518a"]["preserved_path"]
preferred_path = stage / byid["5469fe74d2c199aeec1a"]["preserved_path"]
normal, preferred = json.loads(normal_path.read_text()), json.loads(preferred_path.read_text())
common = lambda r: {k: v for k, v in r.items() if k != "worlds"}
check("frozen ordinary/prefer-I common summary equal", common(normal) == common(preferred))
differences = []
for i, (a, b) in enumerate(zip(normal["worlds"], preferred["worlds"])):
    check("mode world fields " + str(i), {k: v for k, v in a.items() if k != "canceled_I"} == {k: v for k, v in b.items() if k != "canceled_I"} and a["canceled_I"] == 0 and b["canceled_I"] == b["query_I"] in [15, 21])
    differences.append({"path": f"worlds[{i}].canceled_I", "rank": b["rank"], "ordinary_frozen": a["canceled_I"], "prefer_I_frozen_and_reproduced": b["canceled_I"]})
meta = json.loads((ev / "replay/execution.json").read_text())
state = json.loads((ev / "replay/execution-state.json").read_text())
check("exactly one prefer-I entry and ordinary zero", meta["source_invocations"] == 1 and meta["mode_invocations"] == {"ordinary": 0, "prefer_I": 1} and state["ordinary_mode_invocations"] == 0 and state["source_argv_seen"][-1] == "--prefer-I" and state["function_counts"]["source_module_entries"] == 1 and state["source_function_calls_after_runpy_return"] == 0)
new_report = stage / meta["new_report_path"]
check("full prefer-I report bytes reproduced", meta["returncode"] == 0 and new_report.read_bytes() == preferred_path.read_bytes() and not new_report.with_name("joint_rank_audit.json").exists())
summary = (json.dumps(common(preferred), ensure_ascii=False) + "\n").encode()
check("354B stdout is shared summary, not full report", len(summary) == 354 and (ev / "replay/stdout.txt").read_bytes() == summary and summary != preferred_path.read_bytes() and (ev / "replay/stderr.txt").read_bytes() == b"")
for id in ["911339a7d394ac876337", "73bc0f6d20fe90dbd39c"]:
    r = byid[id]
    check("runtime bytes unchanged " + id, sha(ev / "replay/source-root" / r["path"]) == r["sha256"])
counts = state["function_counts"]
check("observed finite calls and zero query propagation", counts["token_function_calls"] == 768 and counts["token_endpoints_after_owner"] == 0 and state["token_query_state_visit_counts"] == {"1": 768} and state["token_endpoint_price_counts"] == {"1": 768} and counts["maxflow_function_calls"] == 12 and counts["send_function_calls"] == 612)
check("actual nonzero B/seed/residual units", state["send_units"] == {"B_maxflow": 306, "A_seed_R_paths": 198, "A_residual_maxflow": 108} and counts["send_calls_B_maxflow"] == 306 and counts["send_calls_A_seed_R_paths"] == 198 and counts["send_calls_A_residual_maxflow"] == 108)
check("six complete world observations", len(state["world_observations"]) == 6 and len(state["maxflow_returns"]) == 12)
for row, report_row in zip(state["world_observations"], preferred["worlds"]):
    rank = row["rank"]
    flows = [r for r in state["maxflow_returns"] if r["rank"] == rank]
    check("nonzero projection " + str(rank), row["B_canceled_I"] == row["query_I"] == report_row["canceled_I"] and row["A_seeded_R_cancellation"] == row["B_canceled_R"] == 51 - row["query_I"] and row["A_final_R_cancellation"] == 51 and flows == [{"rank": rank, "network": "B", "added_flow": 51}, {"rank": rank, "network": "A", "added_flow": row["query_I"]}] and row["projection_margin"] == row["joint_cost_minus_retained_token_mass"] == row["R_only_cost_minus_net_R_mass"] == "0")
data = json.loads((stage / byid["73bc0f6d20fe90dbd39c"]["preserved_path"]).read_text())
raw = data["instance"]
clients = [set(row["topics"]) for row in raw["customers"] for _ in range(row["multiplicity"])]
actual, T, U = [0, 3, 4], [1, 2, 4], [0, 1, 2]
covered = lambda z: {x for x, likes in enumerate(clients) if likes.intersection(z)}
C, O = covered(actual), covered(T)
R, I, G = O - C, O & C, C - O
owner = {x: next(i for i, a in enumerate(T) if a in clients[x]) for x in O}
J = {x: [i for i, a in enumerate(actual) if a in clients[x]] for x in O}
Im = {x for x in I if owner[x] not in J[x]}
kappa = sum((F(1, len(J[x]) + 1) for x in Im), F())
check("true unit input and complete original IC domain", len(clients) == 430 and len(raw["customers"]) == 17 and len(data["strategy"]["actions"]) == 43 and preferred["IC_comparisons"] == 258)
check("C/O/R/I/G/Im and kappa", (len(C), len(O), len(R), len(I), len(G), len(Im), kappa) == (265, 324, 110, 214, 51, 36, F(18)))
check("582 state checks and positive/zero scope deduction", len(R | Im) == 146 and sum(3 * len(clients[x]) for x in R | Im) == preferred["marginal_state_checks"] == 582)
income, sources = [0, 0, 0], [0, 0, 0]
for x in C:
    winner = max((i for i, a in enumerate(actual) if a in clients[x]), key=lambda i: U[i])
    income[winner] += 1
    sources[winner] += int(x in G)
root_leaf = [1, 3, 4]
Droot = sum((F(1, sum(a in likes for a in root_leaf)) for likes in clients if 1 in likes), F())
menu_D = next(F(r["D"]) for r in state["query_menus"] if r["role"] == 0 and r["action"] == 1)
check("actual-world IC substitution obstruction", income == [45, 108, 112] and sources == [15, 36, 0] == state["world_observations"][0]["sources_by_role"] and Droot == menu_D == 91 and Droot > income[0])
private_root = sum(likes == {1} for likes in clients)
check("offending query has unavoidable residual tokens", private_root == 55 and private_root - len(G) == 4)
check("unvisited menu still has positive price tax", any(r["role"] == 1 and r["action"] == 0 and r["D"] == "66" and r["actual_u"] == "91" for r in state["query_menus"]))
supplement = ev / "supplement"
supplement.mkdir(exist_ok=True)
(supplement / "mode-differences.json").write_text(json.dumps({"scope": "frozen JSON comparison only; ordinary mode executions: 0", "differences": differences, "shared_summary_sha256": hashlib.sha256(summary).hexdigest()}, ensure_ascii=False, indent=2) + "\n")
(supplement / "winner-income-and-scope.json").write_text(json.dumps({"scope": "definition arithmetic on one already-run world, no source function or solver invocation", "rank": U, "winner_income": income, "actual_u": preferred["actual_u"], "winner_G_sources": sources, "root_query_D": str(Droot), "root_winner_income": income[0], "root_private_R": private_root, "minimum_remaining_root_tokens": private_root - len(G), "kappa_minus": str(kappa), "tracked_clients": 146, "state_checks": 582, "nonzero_owner_absorption_entries_deduced": 146, "zero_entries_deduced": 436, "deduction_basis": "all observed endpoints at unique owner query; original total-beta checks positive for every tracked client"}, ensure_ascii=False, indent=2) + "\n")
receipts = json.loads((ws / "semantic-receipts.json").read_text())
check("five complete prepared receipts", len(receipts) == 5 and {r["id"] for r in receipts} == {r["id"] for r in manifest if r["role"] == "primary"} and all(all(r[k] is True for k in ["full_file_reviewed", "related_material_checked", "unique_content_accounted_for"]) and all((stage / p).is_file() for p in r["targets"]) for r in receipts))
formal = list(stage.glob("archives/customer-attraction/state/*/*.md"))
check("five formal objects with valid source commits", len(formal) == 5 and all(c in {"68fad804ec5946cb296f77dc5b336308a66abf12", "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"} for p in formal for c in re.findall(r"source:([^:\s]+):", p.read_text())))
links = 0
for p in stage.rglob("*.md"):
    if any(part in p.parts for part in ["original", "inputs", "related-original", "source-root"]):
        continue
    for target in re.findall(r"\]\(([^)]+)\)", p.read_text()):
        if "://" in target or target.startswith("#"):
            continue
        q = (p.parent / target.split("#")[0]).resolve()
        rel = q.relative_to(stage)
        assert q.exists() or (repo / rel).exists(), (str(p), target)
        links += 1
check("all local links resolve", links > 25)
result = {"status": "PASS", "scope": "saved evidence, exact mode diff and one-world arithmetic only; original program calls in this check: 0", "checks_passed": len(checks), "links_checked": links, "analytic_math_self_check_items": 14, "checks": checks}
(ws / "evidence-self-check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
