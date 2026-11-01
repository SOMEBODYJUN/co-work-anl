"""Independent exact audit of one frozen refund witness, from its raw JSON.

Replays all 57 histories and 399 IC comparisons, computes every one of the 84
unordered triples, and checks the projection formulas at all original nodes.
No imported author audit, BI solver, LP, policy/parameter scan, or source writes.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, product
from pathlib import Path
import json


ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / "AGENTS.md").is_file() and (p / "work.py").is_file())
SOURCE = ROOT / ("research/workspaces/customer-attraction/"
                 "R-b659ddeec819493bb10dc58441fa7b3d/refund/"
                 "prefixed_refund_counterexample.json")
NAMES = "ABTQRSP"
source_bytes = SOURCE.read_bytes()
raw = json.loads(source_bytes)
unit_masks = [mask for mask, count in raw["rows"] for _ in range(count)]
assert len(unit_masks) == 179
actions = {tuple(row["history"]): row["action"] for row in raw["actions"]}
histories = [h for depth in range(3) for h in product(range(7), repeat=depth)]
assert set(actions) == set(histories) and len(actions) == 57
assert all(0 <= a < 7 for a in actions.values())


def finish(h):
    while len(h) < 3:
        h = (*h, actions[h])
    return h


def cover(z):
    return frozenset(x for x, mask in enumerate(unit_masks)
                     if any(mask & (1 << a) for a in z))


def utility(z, i, selected=None):
    return sum((F(1, sum(bool(mask & (1 << a)) for a in z))
                for x, mask in enumerate(unit_masks)
                if mask & (1 << z[i]) and (selected is None or x in selected)), F())


ic_rows = []
for h in histories:
    i = len(h)
    prescribed = finish(h)
    current_u = utility(prescribed, i)
    for a in range(7):
        deviation = finish((*h, a))
        alternative_u = utility(deviation, i)
        gap = current_u - alternative_u
        assert gap >= 0, (h, a, gap)
        ic_rows.append({"history": list(h), "deviation": a,
                        "prescribed_leaf": list(prescribed),
                        "deviation_leaf": list(deviation),
                        "current_u": str(current_u),
                        "alternative_u": str(alternative_u), "IC_slack": str(gap)})
assert len(ic_rows) == 399

actual = finish(())
C = cover(actual)
triples = list(combinations_with_replacement(range(7), 3))
assert len(triples) == 84
values = [(z, len(cover(z))) for z in triples]
optimum = max(value for z, value in values)
optimal_multisets = [z for z, value in values if value == optimum]
assert optimal_multisets == [(0, 2, 3)]
assert list(actual) == raw["path"]
assert len(C) == raw["welfare"] and optimum == raw["optimal"]
assert [list(z) for z in optimal_multisets] == raw["optimal_tuples"]
assert [str(utility(actual, i)) for i in range(3)] == raw["profits"]


def projection_audit(O):
    outside = frozenset(range(len(unit_masks))) - O
    D = O - C
    E = C - O
    u = [utility(actual, i) for i in range(3)]
    v = [utility(actual, i, O) for i in range(3)]
    e = [utility(actual, i, outside) for i in range(3)]
    assert all(u[i] == v[i] + e[i] for i in range(3))
    assert sum(e) == len(E)
    f = [0] + [max(len(D & cover(z))
                   for z in combinations_with_replacement(range(7), r))
               for r in range(1, 4)]
    g = [F(f[3-i] - f[2-i]) for i in range(3)]
    gaps = [max(F(), g[i] - u[i]) for i in range(3)]
    surplus = [max(F(), u[i] - g[i]) for i in range(3)]
    assert sum(gaps) - sum(surplus) == len(D) - len(C)
    assert len(O) - 2*len(C) + sum(surplus) == sum(gaps) - len(E)

    rows = []
    for h in histories:
        i = len(h)
        z = finish(h)
        current_v, current_e = utility(z, i, O), utility(z, i, outside)
        current_u = current_v + current_e
        alternatives = []
        for a in range(7):
            z_a = finish((*h, a))
            v_a, e_a = utility(z_a, i, O), utility(z_a, i, outside)
            gamma = current_u - v_a - e_a
            assert gamma >= 0
            assert v_a-current_v == current_e-e_a-gamma
            alternatives.append((a, v_a-current_v, e_a, gamma))
        delta = max(v_gain for a, v_gain, e_a, gamma in alternatives)
        min_e = min(e_a for a, v_gain, e_a, gamma in alternatives)
        min_e_gamma = min(e_a+gamma for a, v_gain, e_a, gamma in alternatives)
        assert delta >= 0 and delta == current_e-min_e_gamma
        assert delta+min_e <= current_e
        rows.append({"history": list(h), "prescribed_leaf": list(z),
                     "v": str(current_v), "e": str(current_e), "delta": str(delta),
                     "min_deviation_e": str(min_e),
                     "min_deviation_e_plus_IC_slack": str(min_e_gamma),
                     "projection_reserve_slack": str(current_e-delta-min_e),
                     "delta_maximizing_deviations":
                         [a for a, gain, e_a, gamma in alternatives if gain == delta]})
    path_rows = [next(row for row in rows if row["history"] == list(actual[:i]))
                 for i in range(3)]
    sum_delta = sum(F(row["delta"]) for row in path_rows)
    sum_min_e = sum(F(row["min_deviation_e"]) for row in path_rows)
    assert sum_delta+sum_min_e <= len(E)
    return {
        "O_size": len(O), "O_is_globally_optimal": len(O) == optimum,
        "L": len(D), "E": len(E), "u": list(map(str, u)),
        "v": list(map(str, v)), "e": list(map(str, e)), "f_D": f,
        "g_by_actual_position": list(map(str, g)),
        "positive_deficits": list(map(str, gaps)),
        "retained_profit_surpluses": list(map(str, surplus)),
        "SHARED_LHS": str(sum(gaps)), "SHARED_RHS": len(E),
        "all_57_projection_nodes": rows, "actual_path_projection_rows": path_rows,
        "path_sum_delta": str(sum_delta), "path_sum_min_deviation_e": str(sum_min_e),
        "PATH_REFUND_slack": str(len(E)-sum_delta-sum_min_e),
    }


optimal_projection = projection_audit(cover((0, 2, 3)))
other_projection = projection_audit(cover((6, 2, 3)))
assert optimal_projection["e"] == ["34", "0", "34"]
assert optimal_projection["f_D"] == [0, 36, 72, 72]
assert optimal_projection["positive_deficits"] == ["0", "1", "0"]
assert [row["delta"] for row in optimal_projection["actual_path_projection_rows"]] == ["32", "0", "34"]
assert other_projection["O_size"] == 110 and other_projection["E"] == 69
assert SOURCE.read_bytes() == source_bytes

report = {
    "scope": "Only the frozen 179-unit witness; all histories and fixed-input optimum; no general search",
    "raw_source": str(SOURCE.relative_to(ROOT)),
    "raw_sha256": sha256(source_bytes).hexdigest(),
    "unit_customers": len(unit_masks), "full_decision_histories": len(histories),
    "IC_comparisons_including_self": len(ic_rows),
    "minimum_IC_slack": str(min(F(row["IC_slack"]) for row in ic_rows)),
    "actual_path_labels": [NAMES[a] for a in actual],
    "actual_profits": [str(utility(actual, i)) for i in range(3)], "welfare": len(C),
    "OPT_3": optimum, "unique_optimal_multisets": [list(z) for z in optimal_multisets],
    "unique_optimal_multiset_labels": [[NAMES[a] for a in z] for z in optimal_multisets],
    "all_84_unordered_triple_coverages": [
        {"tuple": list(z), "labels": [NAMES[a] for a in z], "coverage": value}
        for z, value in values],
    "all_399_IC_rows": ic_rows,
    "optimal_O_A_T_Q": optimal_projection,
    "nonoptimal_O_P_T_Q": other_projection,
    "source_unchanged_after_audit": True,
}
output = Path(__file__).with_suffix(".json")
output.write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps({"status": "PASS", "histories": len(histories), "IC": len(ic_rows),
                  "unique_optimum": ["A", "T", "Q"], "OPT_3": optimum,
                  "u": report["actual_profits"], "E": optimal_projection["E"],
                  "f_D": optimal_projection["f_D"],
                  "path_delta": [row["delta"] for row in optimal_projection["actual_path_projection_rows"]],
                  "other_O_P_T_Q_size": other_projection["O_size"],
                  "other_O_P_T_Q_E": other_projection["E"],
                  "output": str(output.relative_to(ROOT))}, indent=2))
