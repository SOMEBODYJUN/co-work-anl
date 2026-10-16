from fractions import Fraction as F
from itertools import product
from random import Random
import json

counts = {"tested_pairs": 0, "feasible_pairs": 0, "positive_support_pairs": 0}


def check(p, x, T):
    counts["tested_pairs"] += 1
    if any(xx and pp > T for pp, xx in zip(p, x)):
        return
    if sum((pp * xx for pp, xx in zip(p, x)), F(0)) > T:
        return
    if sum((xx for pp, xx in zip(p, x) if pp > T / 2), F(0)) > 1:
        return
    if sum((xx for pp, xx in zip(p, x) if pp > T / 3), F(0)) > 2:
        return
    if T < 4 and sum(x, F(0)) > T // 1:
        return
    counts["feasible_pairs"] += 1
    ordered = sorted(((pp, xx) for pp, xx in zip(p, x) if xx), reverse=True)
    if not ordered:
        return
    counts["positive_support_pairs"] += 1
    pos = F(0)
    maxima = {}
    for pp, xx in ordered:
        left = xx
        while left:
            s = pos.numerator // pos.denominator
            take = min(left, s + 1 - pos)
            maxima[s] = max(maxima.get(s, F(0)), pp)
            pos += take
            left -= take
    assert sum(maxima.values(), F(0)) <= F(3, 2) * T, (p, x, T, maxima)


times = [F(1), F(3,2), F(2)]
targets = [F(k,2) for k in range(1,11)]
for n in range(5):
    for p in product(times, repeat=n):
        for x in product([F(0), F(1,2), F(1)], repeat=n):
            for T in targets:
                check(p, x, T)

rng = Random(271828)
for _ in range(10000):
    n = rng.randrange(1, 9)
    p = [1 + F(rng.randrange(0,1000004),1000003) for _ in range(n)]
    x = [F(rng.randrange(0,7),6) for _ in range(n)]
    boundary = rng.randrange(1,6)
    T = F(boundary) + F(rng.choice([-1,0,1]),1000003)
    check(p, x, T)

assert F(2,3) + F(1,2) + F(1,3) == F(3,2)
assert F(3,2) - F(1,2) - F(1,3) == F(2,3)
print(json.dumps({"status": "pass", "scope": "single-row slot envelope for all 0..4-job {1,3/2,2} rows, half-integral x, half-integer targets 1/2..5, plus 10000 seeded large-denominator boundary samples", "seed": 271828, "counts": counts}, indent=2))
