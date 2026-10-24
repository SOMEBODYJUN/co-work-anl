"""Recheck two explicit attacks on a proposed all-input cross-pair inequality.

No search or strategy optimization. The small complete policy is an unchanged
prior certificate. The large-background calculation checks only the analytic
branch bounds proved in cross_pair_scope.md, not a huge game-tree enumeration.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WORKSPACES = HERE.parents[2]
SOURCE = WORKSPACES / "R-d22a706a03c5499d941a6a97f94128a8/representation/high_insertion_2cycle_348_exact.json"
packet = json.loads(SOURCE.read_text())
inst = packet["instance"]
m = inst["players"]
topics = range(len(inst["topics"]))
types = [(frozenset(t["topics"]), t["multiplicity"]) for t in inst["customers"]]
sigma = {tuple(t["history"]): t["action"] for t in packet["certificate"]["actions"]}

def leaf(h):
    while len(h) < m:
        h = h + (sigma[h],)
    return h

def utility(z, i):
    return sum((F(w, sum(a in T for a in z)) for T, w in types if z[i] in T), F())

def query(a, z):
    return sum((F(w, 1 + sum(b in T for b in z)) for T, w in types if a in T), F())

histories = deviations = comparisons = 0
for i in range(m):
    for h in product(topics, repeat=i):
        histories += 1
        actual = utility(leaf(h), i)
        for a in topics:
            assert actual >= utility(leaf(h + (a,)), i), (h, a)
            comparisons += 1
            deviations += a != sigma[h]

leaves = [leaf((a,)) for a in topics]
ds = [utility(z, 0) for z in leaves]
K = [[query(a, z) for z in leaves] for a in topics]
A, B = 2, 5
pair_left, pair_right = ds[A] + ds[B], K[B][A] + K[A][B]
assert pair_left == F(147) and pair_right == F(159)
diagonal_C = (K[A][A] + K[A][B] + K[B][A] + K[B][B]) / 4
assert diagonal_C == F(737, 12) < ds[0]
pure_column_cap = max(row[0] for row in K)
assert pure_column_cap == F(69) < ds[0]
root = leaf(())
W = sum(w for T, w in types if any(a in T for a in root))

k, d, q, t, r, Q, H, M = 3, 20, 12, 10, 2475, 2063, 100000, 10**9
def f(c):
    return F(q - 1, M + c) + F(1, M + c + 1)
def g(c):
    return F(H * q, H * M + c)

punish = d * (t - 1)
old_nonhot = punish - (t - 1)
empty_after_punish = Q - 1 - old_nonhot
greedy = r - 1 - punish
assert (punish, old_nonhot, empty_after_punish, greedy) == (180, 171, 1891, 2294)
assert greedy > empty_after_punish
assert r - t < 2 * (Q - 1)
background_diagonal = d * (f(t) + (k - 1) * g(r))
background_cross_lower = d * (f(3) + (k - 1) * g(r + 1))
background_gap_lower = 2 * (background_cross_lower - background_diagonal)
assert background_gap_lower > 0
assert 7 * H * M * M > 2 * (M + 11) ** 2

out = {
    "status": "Exact replays of two attacks on the pair strengthening only; general half and root security remain open.",
    "prior_root_certificate": str(SOURCE),
    "root_empty": {
        "customers": sum(w for T, w in types),
        "players": m,
        "histories": histories,
        "comparisons_including_self": comparisons,
        "proper_deviations": deviations,
        "actual_leaf": root,
        "W": W,
        "forced_leaves": leaves,
        "root_payoffs": [str(v) for v in ds],
        "pair": [A, B],
        "pair_left": str(pair_left),
        "pair_right": str(pair_right),
        "pair_deficit": str(pair_left - pair_right),
        "iid_diagonal_C_on_pair": str(diagonal_C),
        "pure_column_0_cap": str(pure_column_cap),
    },
    "existing_arbitrary_background": {
        "parameters": dict(k=k, d=d, q=q, t=t, r=r, Q=Q, H=H, M=M),
        "two_queries": "A picks real block 1 and B real block 2 in every segment; both pick the two dummy blocks.",
        "each_root_profit": str(background_diagonal),
        "each_cross_query_lower": str(background_cross_lower),
        "pair_right_minus_left_lower": str(background_gap_lower),
        "greedy_count": greedy,
        "empty_after_punish": empty_after_punish,
        "scope": "A branch bound inside the already independently reviewed complete SPE; background covers every customer.",
    },
}
output = HERE / "pair_scope_exact.json"
output.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
