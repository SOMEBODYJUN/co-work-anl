"""One fixed full-strategy cone / one legal prefix test of u>=OPT_m/(2m).

The original total m, not the remaining population, appears in the denominator.
No strategy walk, no count-anonymous restriction, no special positive theorem.
Any positive numerical proposal must pass exact Fraction checks below.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
from pathlib import Path
import json
import math
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
source = "evidence/certificates/customer_attraction/prefix_balance_failure.json"
obj = json.loads((REPO / source).read_text())
strategy = obj.get("strategy", obj)
actions = {tuple(v["history"]): v["action"] for v in strategy["actions"]}
m = max(map(len, actions)) + 1
k = max(a for h, chosen in actions.items() for a in h + (chosen,)) + 1
target_history = (1,)
types = tuple(mask for mask in range(1, 1 << k))
histories = tuple(h for d in range(m) for h in product(range(k), repeat=d))
assert set(histories) == set(actions)

@lru_cache(None)
def leaf(h):
    return h if len(h) == m else leaf(h + (actions[h],))

def payoff(z, a):
    return tuple(F(1, sum(mask >> b & 1 for b in z)) if mask >> a & 1 else F(0) for mask in types)

def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))

ic = []
for h in histories:
    prescribed = payoff(leaf(h), actions[h])
    for a in range(k):
        if a != actions[h]:
            alternative = payoff(leaf(h + (a,)), a)
            ic.append(tuple(x-y for x, y in zip(prescribed, alternative)))
A = -np.array([[float(v) for v in row] for row in ic])
target = payoff(leaf(target_history), actions[target_history])
supports = tuple(combinations(range(k), min(m, k)))
answers = []
positive = None
for support in supports:
    union = sum(1 << a for a in support)
    cover = tuple(F(bool(mask & union)) for mask in types)
    objective = tuple(2*m*u - o for u, o in zip(target, cover))
    res = linprog(np.array(list(map(float, objective))), A_ub=A,
        b_ub=np.zeros(len(ic)), A_eq=[list(map(float, target))], b_eq=[1.0],
        bounds=[(0, None)]*len(types), method="highs")
    assert res.success, res.message
    row = {"comparison_support": support, "numeric_max_O_minus_2m_u": -res.fun}
    answers.append(row)
    if res.fun < -1e-8:
        w = tuple(F(float(x)).limit_denominator(10**8) for x in res.x)
        assert min(w) >= 0 and dot(target, w) == 1
        slacks = tuple(dot(v, w) for v in ic)
        assert min(slacks) >= 0
        values = [(dot(tuple(F(bool(mask & sum(1 << a for a in ss))) for mask in types), w), ss) for ss in supports]
        OPT, optimum_support = max(values)
        assert OPT > 2*m*dot(target, w)
        den = math.lcm(*(v.denominator for v in w))
        integer = tuple(int(v*den) for v in w)
        gcd = math.gcd(*integer)
        integer = tuple(v//gcd for v in integer)
        scale = F(den, gcd)
        low = []
        for h in histories:
            value = dot(payoff(leaf(h), actions[h]), w)
            if 2*m*value < OPT:
                low.append({"history": h, "root_payoff": str(value*scale),
                    "remaining_players": m-len(h), "node_leaf": leaf(h)})
        last_depth = max(len(v["history"]) for v in low)
        actual = leaf(())
        actual_union = sum(1 << a for a in set(actual))
        W = dot(tuple(F(bool(mask & actual_union)) for mask in types), w)
        positive = {
            "scope": "Exact counterexample to the individual direct floor only; half evaluated separately.",
            "source_strategy": source, "players": m, "topics": k,
            "integer_customer_weights": {str(mask): v for mask, v in zip(types, integer) if v},
            "strategy": strategy, "target_history": target_history,
            "target_payoff": str(scale), "OPT_m": str(OPT*scale),
            "comparison_support": optimum_support,
            "OPT_minus_2m_target": str((OPT-2*m)*scale),
            "minimum_full_tree_IC_slack": str(min(slacks)*scale),
            "actual_root_path": actual, "actual_welfare": str(W*scale),
            "two_W_minus_OPT": str((2*W-OPT)*scale),
            "all_latest_low_nodes": [v for v in low if len(v["history"]) == last_depth],
        }
        (HERE / "direct_floor_counterexample.json").write_text(json.dumps(positive, indent=2)+"\n")
        break

report = {
    "scope": "One existing complete strategy cone and one legal target prefix; finite diagnostic only.",
    "source_strategy": source, "players_original_total": m,
    "target_history": target_history, "remaining_players": m-len(target_history),
    "topic_count": k, "customer_type_variables": len(types),
    "full_ordered_histories": len(histories), "nonself_full_tree_IC_rows": len(ic),
    "normalization": "target node current payoff=1", "factor_in_target": 2*m,
    "comparisons_tested": answers, "exact_positive_witness": positive is not None,
    "interpretation_without_positive": "No witness in this one diagnostic; no general proof and no exact cone bound asserted.",
}
(HERE / "direct_floor_diagnostic.json").write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps({k:v for k,v in report.items() if k != "comparisons_tested"}, indent=2))
print("best_numerical_gap", max(v["numeric_max_O_minus_2m_u"] for v in answers))
