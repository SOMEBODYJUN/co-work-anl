"""Exact regression for the general role-coupon theorem, not a SPE scan.

One fixed history-labelled DAG has customer-mixture rows, past terminal
coupons, future branches and merges, and two contexts at the same role.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

ROWS = {
    (0, "a"): ((F(2, 3), (1, 3)), (F(1, 3), (2, 4))),
    (0, "b"): ((F(1, 2), (1, 2, 4)), (F(1, 2), (3,))),
    (1, "a"): ((F(1, 3), (0, 2, 4)), (F(2, 3), (3,))),
    (2, "a"): ((F(1, 2), (0, 3, 4)), (F(1, 2), (1, 4))),
    (2, "b"): ((F(3, 4), (0, 1, 3)), (F(1, 4), (4,))),
    (3, "a"): ((F(2, 5), (0, 1, 4)), (F(3, 5), (2,))),
    (3, "b"): ((F(1, 2), (1, 4)), (F(1, 2), (0, 2))),
    (4, "a"): ((F(1, 2), (0, 2)), (F(1, 2), (1, 3))),
    (4, "b"): ((F(1, 3), (0, 1, 2)), (F(2, 3), (3,))),
}
FUTURE = {
    (0, "a"): {1: (1, "a"), 2: (2, "a"), 3: (3, "a"), 4: (4, "a")},
    (0, "b"): {1: (1, "a"), 2: (2, "b"), 3: (3, "b"), 4: (4, "b")},
    (1, "a"): {2: (2, "b"), 3: (3, "b"), 4: (4, "a")},
    (2, "a"): {3: (3, "a"), 4: (4, "b")},
    (2, "b"): {3: (3, "b"), 4: (4, "a")},
    (3, "a"): {4: (4, "a")},
    (3, "b"): {4: (4, "b")},
    (4, "a"): {}, (4, "b"): {},
}
M = 5
row = {}
mixture_checks = 0
for state, components in ROWS.items():
    i = state[0]
    assert sum(w for w, _ in components) == 1
    p = [F(0)] * M
    for weight, subset in components:
        assert i not in subset and len(set(subset)) == len(subset)
        each = weight / (len(subset) + 1)
        p[i] += each
        for j in subset:
            p[j] += each
    assert sum(p) == 1
    assert all(x <= p[i] for x in p)
    # Independently reconstruct the threshold-mixture representation.
    cuts = sorted({F(0), p[i], *(p[j] for j in range(M) if j != i)})
    recovered = [F(0)] * M
    mixture_mass = F(0)
    for lo, hi in zip(cuts, cuts[1:]):
        if hi == lo:
            continue
        mid = (lo + hi) / 2
        subset = [i] + [j for j in range(M) if j != i and p[j] >= mid]
        weight = (hi - lo) * len(subset)
        mixture_mass += weight
        for j in subset:
            recovered[j] += weight / len(subset)
    assert mixture_mass == 1 and recovered == p
    row[state] = p
    mixture_checks += 1

terminal = {}
for state in sorted(ROWS, reverse=True):
    i = state[0]
    p = row[state]
    out = [F(0)] * M
    out[i] += p[i]
    for j in range(M):
        if j == i:
            continue
        if j < i:
            out[j] += p[j]
        elif p[j]:
            child = FUTURE[state][j]
            assert child[0] > i
            for k in range(M):
                out[k] += p[j] * terminal[child][k]
    assert sum(out) == 1
    terminal[state] = out

set_checks = price_checks = aggregate_checks = 0
for state, out in terminal.items():
    i = state[0]
    for bits in product((0, 1), repeat=M):
        k = sum(bits)
        if not bits[i]:
            assert sum(v for j, v in enumerate(out) if bits[j]) <= F(k, k + 1)
            set_checks += 1
    for prices in product(range(3), repeat=M):
        high = sorted((prices[j] for j in range(M) if j != i and prices[j] > prices[i]), reverse=True)
        envelope = F(prices[i], len(high) + 1)
        envelope += sum((F(v, k * (k + 1)) for k, v in enumerate(high, 1)), F(0))
        actual = sum(out[j] * prices[j] for j in range(M))
        assert actual <= envelope
        price_checks += 1

for injections in (
    {s: F(1, s[0] + 1) for s in ROWS},
    {s: (F(1) if s[0] == 0 else F(0)) for s in ROWS},
):
    final = [sum(injections[s] * terminal[s][j] for s in ROWS) for j in range(M)]
    for bits in product((0, 1), repeat=M):
        k = sum(bits)
        inside = sum(v for s, v in injections.items() if bits[s[0]])
        outside = sum(v for s, v in injections.items() if not bits[s[0]])
        assert sum(final[j] for j in range(M) if bits[j]) <= inside + F(k, k + 1) * outside
        aggregate_checks += 1

report = {
    "status": "passed",
    "scope": "one fixed role-coupon mixture DAG; definition-level, not a game or SPE scan",
    "roles": M, "history_contexts": len(ROWS),
    "local_threshold_mixtures": mixture_checks,
    "global_target_set_checks": set_checks,
    "global_weighted_price_checks": price_checks,
    "multisource_cut_checks": aggregate_checks,
    "claims_actual_wallet_capacity": False,
    "claims_half": False,
}
with Path(__file__).with_name("global_role_coupon_hitting_audit.json").open("x", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(json.dumps(report, ensure_ascii=False))
