"""Independent exact reconstruction of the support-conservation relaxation point.

Reads only the frozen rational data. Does not import the author's checker,
discovery tool, canonical solver, or any optimization library.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / "tree_coupling/support_conservation_obstruction.json"
blob = json.loads(DATA.read_text())
m, p = 3, 6
assert (blob["n"], blob["p"]) == (m, p)

def sigma(h):
    if len(h) == 0:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(3) if h[1] < 3 else range(3, 6)
    return min(a for a in group if a not in h)

def finish(h):
    while len(h) < m:
        h += (sigma(h),)
    return h

def counts(h):
    return tuple(h.count(a) for a in range(p))

histories = [h for d in range(m) for h in product(range(p), repeat=d)]
stored = {tuple(z["history"]): z["action"] for z in blob["strategy_actions"]}
assert len(stored) == len(histories) == 43
assert all(stored[h] == sigma(h) for h in histories)
y = {(tuple(z["q"]), z["a"]): Q(z["value"]) for z in blob["y"]}
assert len(y) == len(blob["y"]) == 126
states = sorted({counts(h) for h in product(range(p), repeat=m)})
expected = {(q, a) for q in states for a in range(p) if q[a]}
assert set(y) == expected
assert min(y.values()) >= 0

graph_slacks = []
graph_edges = set()
for h in histories:
    t = finish(h)
    target = (counts(t), sigma(h))
    for a in range(p):
        source = (counts(finish(h + (a,))), a)
        graph_slacks.append(y[target] - y[source])
        graph_edges.add((source, target))
assert len(graph_slacks) == 258
assert min(graph_slacks) >= 0

masks = [tuple(a for a in range(p) if b >> a & 1) for b in range(1, 1 << p)]
dilution_slacks = []
for a in range(p):
    applicable = [q for q in states if q[a]]
    assert len(applicable) == 21
    for q in applicable:
        for r in applicable:
            if q == r:
                continue
            # Direct maximization over the complete customer-type universe.
            kappa = max(Q(sum(r[b] for b in B), sum(q[b] for b in B))
                        for B in masks if a in B)
            dilution_slacks.append(kappa * y[r, a] - y[q, a])
assert len(dilution_slacks) == 2520
assert min(dilution_slacks) >= 0

C = {}
conservation_equalities = 0
for q in states:
    support = tuple(a for a in range(p) if q[a])
    total = sum((q[a] * y[q, a] for a in support), Q())
    if support in C:
        assert total == C[support]
        conservation_equalities += 1
    else:
        C[support] = total
assert len(C) == 41 and conservation_equalities == 15
root_q = counts(finish(()))
portfolio = (1, 2, 4)
assert tuple(blob["portfolio"]) == portfolio
root_total = sum((root_q[a] * y[root_q, a] for a in range(p) if root_q[a]), Q())
assert root_q == (1, 0, 0, 1, 1, 0)
assert root_total == 1 and C[portfolio] == Q(9, 4)

# The alleged common signed-customer representation would obey this identity
# type by type, independently of signs, SPE, or nonnegative coefficients.
a, b, r, s = 0, 1, 2, 1
for B in masks:
    atom_y = Q(int(a in B), r * int(a in B) + s * int(b in B)) if a in B else Q()
    atom_Ca = int(a in B)
    atom_Cb = int(b in B)
    atom_Cab = int(a in B or b in B)
    assert m * r * atom_y == r * atom_Ca + s * (atom_Cab - atom_Cb)
q = (2, 1, 0, 0, 0, 0)
lhs = m * r * y[q, a]
rhs = r * C[(a,)] + s * (C[(a, b)] - C[(b,)])
assert y[q, a] == Q(3, 8)
assert (C[(a,)], C[(b,)], C[(a, b)]) == (Q(3, 4), Q(3, 4), Q(1))
assert lhs == Q(9, 4) and rhs == Q(7, 4)

report = {
    "status": "INDEPENDENT_EXACT_AUDIT_PASSED",
    "scope": "Abstract necessary-condition template obstruction, not a CAG or SPE counterexample",
    "histories": len(histories), "payoff_vertices": len(y),
    "graph_comparisons_with_self": len(graph_slacks),
    "graph_distinct_edges_with_self": len(graph_edges),
    "minimum_graph_slack": str(min(graph_slacks)),
    "same_topic_dilution_comparisons": len(dilution_slacks),
    "minimum_dilution_slack": str(min(dilution_slacks)),
    "support_classes": len(C), "nontrivial_conservation_equalities": conservation_equalities,
    "root_counts": root_q, "root_total": str(root_total),
    "portfolio_support": portfolio, "portfolio_total": str(C[portfolio]),
    "signed_representation_identity_lhs": str(lhs),
    "signed_representation_identity_rhs": str(rhs),
    "signed_representation_identity_gap": str(lhs-rhs),
    "typewise_identity_cases": len(masks)
}
out = HERE / "independent_support_audit.json"
out.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
