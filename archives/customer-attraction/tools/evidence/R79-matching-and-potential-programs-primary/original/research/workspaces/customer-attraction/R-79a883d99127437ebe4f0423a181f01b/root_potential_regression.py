#!/usr/bin/env python3
"""Reinterpret one existing complete witness; no new instance or search.

Exact Fraction replay of POT/RESET and every full SPE row of the shared
34-unit-client instance. The output is reproducible; finite replay is not
a proof of the identities or of the general half-coverage conjecture.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

REPO = Path(__file__).resolve().parents[4]
SOURCE = REPO / "examples/customer_attraction/individual_security_failure.json"
raw = SOURCE.read_bytes()
data = json.loads(raw)
types = [(frozenset(c["topics"]), c["multiplicity"]) for c in data["customers"]]
k = len(data["topics"])
m = data["players"]
p = tuple(F(v, 82) for v in (10, 10, 21, 10, 10, 21))


def move(h):
    if not h:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(3) if h[-1] < 3 else range(3, 6)
    return next(a for a in group if a not in h)


def finish(h):
    while len(h) < m:
        h = h + (move(h),)
    return h


def payoff(z, i):
    return sum((v * F(1, sum(a in B for a in z))
                for B, v in types if z[i] in B), F())


def phi(z):
    return sum((v * sum((F(1, j) for j in range(1, sum(a in B for a in z) + 1)), F())
                for B, v in types), F())


nodes = comparisons = 0
for depth in range(m):
    for h in product(range(k), repeat=depth):
        prescribed = payoff(finish(h), depth)
        for a in range(k):
            assert prescribed >= payoff(finish(h + (a,)), depth)
            comparisons += 1
        nodes += 1

R = J = D = C = F()
gammas = resets = F()
for a, t in product(range(k), repeat=2):
    prob = p[a] * p[t]
    za = finish((a,))
    bt = finish((t,))[1:]
    R += prob * (phi(za) - phi((a,) + bt))
    D += prob * payoff(za, 0)
    for B, v in types:
        if t in B:
            load = sum(s in B for s in za)
            C += prob * v * F(1, 1 + load)
            if a in B:
                J += prob * v * F(1, load * (load + 1))
    for j in range(1, m):
        prefix = (a,) + bt[:j - 1]
        prev = finish(prefix)
        nxt = finish(prefix + (bt[j - 1],))
        gamma = payoff(prev, j) - payoff(nxt, j)
        reset = phi(prev[:j] + prev[j+1:]) - phi(nxt[:j] + nxt[j+1:])
        assert gamma >= 0
        assert phi(prev) - phi(nxt) == gamma + reset
        if j == m - 1:
            assert reset == 0
        gammas += prob * gamma
        resets += prob * reset

assert nodes == 43 and comparisons == 258
assert D - C == R + J
assert R == gammas + resets == -F(11, 82)
assert J == F(40571, 20172)
assert C == F(52377, 6724)
out = {
    "source": str(SOURCE.relative_to(REPO)),
    "source_sha256": hashlib.sha256(raw).hexdigest(),
    "arithmetic": "fractions.Fraction",
    "nodes": nodes,
    "IC_comparisons_including_self": comparisons,
    "p": [str(q) for q in p],
    "D": str(D), "C": str(C), "R": str(R), "J": str(J),
    "D_minus_C": str(D-C),
    "true_successor_IC_total": str(gammas),
    "deletion_reset_total": str(resets),
    "interpretation": "existing complete SPE has negative joint suffix potential regret; collision discount pays it here",
    "general_half": "OPEN",
}
print(json.dumps(out, ensure_ascii=False, indent=2))
