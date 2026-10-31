"""Exact witness and artifact checks; never execute/import the frozen program."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

stage = Path(__file__).resolve().parents[4]
ev = stage / "archives/customer-attraction/tools/evidence/net-rank-incoming-payment-primary"
records = json.loads((ev / "source-manifest.json").read_text())
checks = []
def check(name, assertion):
    assert assertion, name
    checks.append(name)
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

for r in records:
    p = stage / r["preserved_path"]
    check("preserved bytes " + r["id"], p.stat().st_size == r["size"] and digest(p) == r["sha256"])
check("five primary / three true dependencies", Counter(r["role"] for r in records) == {"primary": 5, "runtime-json-input": 2, "locator-only-not-imported": 1})
byid = {r["id"]: r for r in records}
inst = json.loads((stage / byid["9780b9fba5ccc0dcc372"]["preserved_path"]).read_text())
raw = json.loads((stage / byid["7e96e4bbfac656c279d7"]["preserved_path"]).read_text())
report_path = stage / byid["537af53f202c65a1cad8"]["preserved_path"]
report = json.loads(report_path.read_text())
meta = json.loads((ev / "replay/execution.json").read_text())
state = json.loads((ev / "replay/execution-state.json").read_text())
clients = [set(row["topics"]) for row in inst["customers"] for _ in range(row["multiplicity"])]
actual, opt = (4, 0), (1, 3)
covered = lambda z: {x for x, likes in enumerate(clients) if likes.intersection(z)}
C, O = covered(actual), covered(opt)
R, I, G = O - C, O & C, C - O
def payoff(z, i, subset):
    return sum((F(1, sum(a in clients[x] for a in z)) for x in subset if z[i] in clients[x]), F())
u = [payoff(actual, i, C) for i in range(2)]
g = [payoff(actual, i, G) for i in range(2)]
check("86 expanded unit clients", len(clients) == 86)
check("one complete two-role strategy with six histories", inst["players"] == 2 and len(inst["topics"]) == 5 and len(raw["actions"]) == 6)
check("set identities and net mass", (len(C), len(O), len(R), len(I), len(G), len(R) - len(G)) == (44, 45, 42, 3, 41, 1))
check("actual/G/I profits", u == [22, 22] and g == [20, 21] and [u[i] - g[i] for i in range(2)] == [2, 1])

unit_records = state["client_records"]
check("exactly all R clients exported", {r["client_index"] for r in unit_records} == R and len(unit_records) == 42)
price_by_likes = {(1,): F(22, 19), (1, 2): F(41, 38), (3,): F(1), (2, 3): F(1)}
check("source prices from two-role algebra", all(F(r["unit_price"]) == price_by_likes[tuple(r["likes"])] for r in unit_records))
check("type counts", Counter(tuple(r["likes"]) for r in unit_records) == {(1,): 15, (1, 2): 5, (3,): 16, (2, 3): 6})
check("unit prices sum to full cost", sum((F(r["unit_price"]) for r in unit_records), F()) == F(1701, 38))
check("full source/incoming decomposition", list(map(F, report["uncancelled_flow"]["source_cost"])) == [F(385, 19), F(22)] and list(map(F, report["uncancelled_flow"]["incoming_cost"])) == [F(), F(5, 2)])
check("positive tax / actual wallet overload", F(report["uncancelled_flow"]["cost"]) - len(R) == F(105, 38) and F(report["uncancelled_flow"]["cost"]) - len(C) == F(29, 38))
check("last row overload exactly incoming", list(map(F, state["fullK"])) == [F(385, 19), F(49, 2)] and F(49, 2) - 22 == F(5, 2))
check("delta gamma same and full", all(F(r["delta"]) == F(r["gamma"]) for r in unit_records) and sum((F(r["delta"]) for r in unit_records), F()) == 41)
check("delta owner totals", [sum((F(r["delta"]) for r in unit_records if r["owner"] == i), F()) for i in range(2)] == [20, 21])
check("unique surviving TD client", [(r["client_index"], r["likes"], r["rho"]) for r in unit_records if F(r["rho"])] == [(63, [2, 3], "1")])
check("same eta and residual role budget", report["eta"] == ["22", "22"] and report["residual_by_role"] == ["22", "21"])
check("cancelled costs zero incoming and zero tax", report["source_cost"] == ["0", "1"] and report["incoming_cost"] == ["0", "0"] and report["total_cost"] == report["absorbed"] == "1" and report["paid_original_IC_slack"] == "0")
check("zero-source maxflow boundary actually exercised", state["residual_source_capacities"] == ["0", "0"] and state["residual_maxflow_value"] == "0" and state["positive_original_forward_edge_flows"] == [])

menus = state["query_menus"]
check("ten exported original menus", len(menus) == 10)
check("all menu denominators equal exact original-client payoff", all(F(q["D"]) == payoff(q["leaf"], q["role"], set(range(86))) for q in menus))
check("last eligible R menus all price one", all(F(q["D"]) == 22 for q in menus if q["role"] == 1 and q["action"] in [1, 2, 3]))
check("all free prices are one", all(r["kappa"] == "1" for r in unit_records))
single = sum(len(r["likes"]) == 1 for r in unit_records)
double = sum(len(r["likes"]) == 2 for r in unit_records)
check("84 client/start comparisons versus 128 policies", (single, double) == (31, 11) and report["bellman_exhaustive_checks"] == state["client_start_comparisons"] == 84 and 31 * 2 + 11 * 6 == state["deterministic_policy_evaluations_from_actual_loop_bounds"] == 128)
check("string sort preserved / numeric ordering distinguished", report["fixed_flow_unit_prices"] == ["1", "22/19", "41/38"] and sorted(map(F, report["fixed_flow_unit_prices"])) == [F(1), F(41, 38), F(22, 19)])
check("one module execution and 44 capture calls", meta["source_invocations"] == 1 and state["function_entries"]["<module>"] == 1 and state["function_entries"]["capture"] == 44)
check("exact report/stdout and empty stderr", meta["returncode"] == 0 and (ev / "replay/stdout.txt").read_bytes() == report_path.read_bytes() == (stage / meta["new_report_path"]).read_bytes() and (ev / "replay/stderr.txt").read_bytes() == b"")
for r in records:
    if r["role"] != "primary" or r["id"] == "6f6bf8816a05a410672c":
        p = ev / "replay/source-root" / r["path"]
        check("runtime bytes unchanged " + r["id"], digest(p) == r["sha256"])
check("primary and dependency byte totals", sum(r["size"] for r in records if r["role"] == "primary") == 37087 and sum(r["size"] for r in records if r["role"] != "primary") == 2107)
result = {"status": "PASS", "scope": "exact algebra and artifact checks of saved one-run witness; frozen program executions in this self-check: 0", "checks_passed": len(checks), "checks": checks, "full_cost": "1701/38", "positive_IC_tax": "105/38", "full_cost_minus_W": "29/38", "cancelled_cost": "1", "incoming_after_cancellation": "0", "residual_Hall_source": "0", "client_start_comparisons": 84, "policy_evaluations": 128}
Path(__file__).with_name("math-self-check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
