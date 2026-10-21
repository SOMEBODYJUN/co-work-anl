"""Definition-level Fraction audit, independent of the canonical SPE solver.

Prints all full-history incentives and a static CCE lower-bound certificate.
The six customer multiplicities represent distinct unit customers.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
import json
from pathlib import Path

K, M = 4, 3
TYPES = {2: 17, 4: 5, 7: 3, 8: 5, 11: 3, 13: 9}
ROOT, SECOND = 0, (1, 2, 1, 1)
LAST = ((1, 1, 1, 1), (1, 2, 1, 2), (1, 3, 1, 1), (1, 2, 1, 1))
Y = (F(0), F(2, 7), F(1, 4), F(1, 4))


def payoff(s, i):
    a = s[i]
    return sum((F(r, sum((mask >> b) & 1 for b in s))
                for mask, r in TYPES.items() if (mask >> a) & 1), F(0))


def welfare(s):
    return sum(r for mask, r in TYPES.items() if any((mask >> a) & 1 for a in s))


def act(h):
    if not h:
        return ROOT
    if len(h) == 1:
        return SECOND[h[0]]
    return LAST[h[0]][h[1]]


def follow(h):
    while len(h) < M:
        h += (act(h),)
    return h


def main():
    spe_rows, all_margins = [], []
    for depth in range(M):
        for h in product(range(K), repeat=depth):
            s = follow(h)
            incumbent = payoff(s, depth)
            alternatives = [payoff(follow(h + (a,)), depth) for a in range(K)]
            assert incumbent == max(alternatives), (h, incumbent, alternatives)
            all_margins += [incumbent - x for x in alternatives]
            spe_rows.append({"h": h, "action": act(h), "s": s, "u": str(incumbent), "alternatives": list(map(str, alternatives))})
    s = follow(())
    assert s == (0, 1, 1)
    assert welfare(s) == 32
    cce_rows = []
    for q in combinations_with_replacement(range(K), M):
        w = welfare(q)
        deviations = []
        for a in range(K):
            deviations.append(sum((payoff(q[:i] + (a,) + q[i + 1:], i) for i in range(M)), F(0)))
        gains = [F(w) - da for da in deviations]
        lower = F(w) - sum((y * g for y, g in zip(Y, gains)), F(0))
        assert lower >= 33, (q, lower)
        cce_rows.append({"q": q, "w": w, "D": list(map(str, deviations)), "G": list(map(str, gains)), "L": str(lower)})
    out = {"status": "exact-definition-check-passed", "types": TYPES,
           "path": s, "payoffs": [str(payoff(s, i)) for i in range(M)],
           "welfare": welfare(s), "optimum": max(map(welfare, product(range(K), repeat=M))),
           "spe_comparisons": len(all_margins), "spe_min_margin": str(min(all_margins)),
           "dual_y": list(map(str, Y)), "cce_lower_bound": 33,
           "cce_min_dual_expression": min((F(row["L"]) for row in cce_rows)),
           "spe_rows": spe_rows, "cce_rows": cce_rows}
    out["cce_min_dual_expression"] = str(out["cce_min_dual_expression"])
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if len(__import__("sys").argv) > 1:
        Path(__import__("sys").argv[1]).write_text(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
