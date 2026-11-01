"""One fixed complete-strategy cone diagnostic for PI, not a depth relaxation.

For every (r+1)-count q, maximize Phi(q)-P-u subject to all ordered-history
IC and P>=Phi(q') for EVERY r-count q'. No policy changes or cone walk.
Numerics only propose witnesses; every positive is checked with Fraction.
Exact duals, if reconstructible, certify only this fixed cone.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
import math
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
name = "individual_security_failure"
source = "evidence/certificates/customer_attraction/" + name + ".json"
data = json.loads((REPO / source).read_text())["strategy"]
actions = {tuple(row["history"]): row["action"] for row in data["actions"]}
k = 1 + max(a for h in actions for a in h + (actions[h],))
r = 1 + max(map(len, actions))
histories = tuple(h for d in range(r) for h in product(range(k), repeat=d))
assert set(histories) == set(actions)
types = tuple(tuple(a for a in range(k) if mask >> a & 1) for mask in range(1, 1 << k))

@lru_cache(None)
def leaf(h):
    return h if len(h) == r else leaf(h + (actions[h],))

def comps(n, d):
    if d == 1:
        yield (n,)
    else:
        for a in range(n + 1):
            for tail in comps(n - a, d - 1):
                yield (a,) + tail

def payoff(z, a):
    return tuple(F(1, sum(b in t for b in z)) if a in t else F(0) for t in types)

H = [F(0)]
for n in range(1, r + 2):
    H.append(H[-1] + F(1, n))

def phi(q):
    return tuple(H[sum(q[a] for a in t)] for t in types)

def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))

all_r = tuple(comps(r, k))
all_r1 = tuple(comps(r + 1, k))
phis_r = tuple(phi(q) for q in all_r)
u = payoff(leaf(()), actions[()])
constraints = []
for h in histories:
    on = payoff(leaf(h), actions[h])
    for a in range(k):
        if a != actions[h]:
            alt = payoff(leaf(h + (a,)), a)
            constraints.append(tuple(y - x for x, y in zip(on, alt)) + (F(0),))
ic_count = len(constraints)
constraints.extend(p + (F(-1),) for p in phis_r)
A = np.array([[float(x) for x in row] for row in constraints])
eq = u + (F(0),)
eqf = np.array([[float(x) for x in eq]])
rows = []
max_gap = -math.inf
best = None
dual_certificates = []

for q in all_r1:
    pq = phi(q)
    objective = tuple(x - y for x, y in zip(u, pq)) + (F(1),)
    res = linprog(np.array(list(map(float, objective))), A_ub=A,
                  b_ub=np.zeros(len(constraints)), A_eq=eqf, b_eq=[1.0],
                  bounds=[(0, None)] * (len(types) + 1), method="highs")
    assert res.success, (q, res.message)
    gap = -res.fun
    if gap > max_gap:
        max_gap, best = gap, q

    # min objective >= y_eq if y_ub<=0 and c-A^T y_ub-eq*y_eq>=0.
    # Bounds are nonnegative; therefore no separate lower-bound multipliers
    # are required once this exact residual is nonnegative.
    ys = tuple(F(float(x)).limit_denominator(10**7) for x in res.ineqlin.marginals)
    ye = F(float(res.eqlin.marginals[0])).limit_denominator(10**7)
    residual = tuple(objective[j] - sum((row[j] * y for row, y in zip(constraints, ys)), F(0)) - eq[j] * ye for j in range(len(objective)))
    dual_ok = max(ys) <= 0 and min(residual) >= 0 and ye >= 0
    row = {"q": q, "numeric_max_Phi_q_minus_P_r_minus_u": gap,
           "exact_nonpositive_dual_certificate": dual_ok}
    if dual_ok:
        dual_certificates.append({"q": q, "equality_multiplier": str(ye),
            "inequality_multipliers": [[i, str(y)] for i, y in enumerate(ys) if y],
            "minimum_nonnegative_variable_residual": str(min(residual))})
    rows.append(row)
    if gap > 1e-8:
        w = tuple(F(float(x)).limit_denominator(10**7) for x in res.x[:-1])
        assert min(w) >= 0
        assert dot(u, w) == 1
        ic_slacks = tuple(-dot(v[:-1], w) for v in constraints[:ic_count])
        assert min(ic_slacks) >= 0
        opt_r, count_r = max((dot(p, w), count) for p, count in zip(phis_r, all_r))
        opt_r1, count_r1 = max((dot(phi(count), w), count) for count in all_r1)
        exact_gap = opt_r1 - opt_r - dot(u, w)
        assert exact_gap > 0
        denominator = math.lcm(*(x.denominator for x in w))
        ww = tuple(int(x * denominator) for x in w)
        common = math.gcd(*ww)
        ww = tuple(x // common for x in ww)
        scale = F(denominator, common)
        candidate = {
            "scope": "Exact rational witness against PI only; not a half-coverage counterexample.",
            "source_strategy": source,
            "instance": {"players": r, "topics": ["T" + str(a) for a in range(k)],
                "customers": [{"topics": list(t), "multiplicity": x} for t, x in zip(types, ww) if x]},
            "strategy": data,
            "exact_root_payoff": str(scale),
            "P_r": str(opt_r * scale), "P_r1": str(opt_r1 * scale),
            "delta_minus_root": str(exact_gap * scale),
            "minimum_full_tree_IC_slack": str(min(ic_slacks) * scale),
            "potential_maximizers": {str(r): count_r, str(r + 1): count_r1},
        }
        (HERE / "pi_fixed_cone_counterexample.json").write_text(json.dumps(candidate, indent=2) + "\n")
        print("EXACT_PI_COUNTEREXAMPLE", json.dumps(candidate), flush=True)
        break

answer = {
    "scope": "Exactly one fixed complete ordered-history strategy cone, all nonempty customer incidence types; no policy walk.",
    "source_strategy": source, "players": r, "topics": k,
    "customer_type_variables": len(types), "complete_ordered_nodes": len(histories),
    "full_tree_IC_rows": ic_count, "all_r_potential_constraints": len(all_r),
    "candidate_r1_counts_total": len(all_r1), "candidate_r1_counts_tested": len(rows),
    "normalization": "u_root=1", "numeric_best_gap": max_gap,
    "numeric_best_q": best, "all_tested_nonpositive_certified_exactly": len(dual_certificates) == len(rows),
    "candidate_results": rows, "exact_dual_certificates": dual_certificates,
}
(HERE / "pi_fixed_cone_diagnostic.json").write_text(json.dumps(answer, indent=2) + "\n")
print(json.dumps({key: value for key, value in answer.items() if key not in ("candidate_results", "exact_dual_certificates")}, indent=2))
