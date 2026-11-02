"""Self-contained exact audit of the eight-unit-customer CCE bridge failure.

No canonical solver, LP solver, or discovery script is imported.
"""
import json
import sys
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path

CUSTOMERS = [{1} for _ in range(4)] + [{2}, {3}, {0, 2, 3}, {0, 2, 3}]
ROOT = 0
SECOND = (1, 2, 1, 1)
LAST = ((1, 1, 1, 1), (1, 2, 1, 2), (1, 3, 1, 1), (1, 2, 1, 1))
Y_SIMPLE = (F(0), F(1, 3), F(2, 9), F(2, 9))
Y_SHARP = (F(0), F(9, 29), F(20, 87), F(20, 87))
COUNT_PROBS = {(0, 1, 1): F(17, 87), (1, 1, 2): F(29, 87),
               (1, 1, 3): F(29, 87), (2, 2, 2): F(6, 87),
               (3, 3, 3): F(6, 87)}


def utilities(s):
    result = [F(0)] * len(s)
    for customer in CUSTOMERS:
        attracted = [i for i, a in enumerate(s) if a in customer]
        for i in attracted:
            result[i] += F(1, len(attracted))
    return result


def welfare(s):
    return sum(any(a in customer for a in s) for customer in CUSTOMERS)


def action(h):
    return ROOT if not h else SECOND[h[0]] if len(h) == 1 else LAST[h[0]][h[1]]


def follow(h):
    while len(h) < 3:
        h += (action(h),)
    return h


def f(a, b):
    return utilities((a,) + b)[0]


def main():
    histories, margins = [], []
    for depth in range(3):
        for h in product(range(4), repeat=depth):
            current = utilities(follow(h))[depth]
            alternatives = [utilities(follow(h + (a,)))[depth] for a in range(4)]
            assert current == max(alternatives)
            margins.extend(current - alt for alt in alternatives)
            histories.append({"history": h, "action": action(h), "alternatives": alternatives})
    path = follow(())
    assert path == (0, 1, 1) and utilities(path) == [2, 2, 2] and welfare(path) == 6
    assert sum(margins, F(0)) >= 0 and min(margins) == 0 and len(margins) == 84
    optimum = max(welfare(s) for s in product(range(4), repeat=3))
    assert optimum == 8
    dual_rows = []
    for s in combinations_with_replacement(range(4), 3):
        w = welfare(s)
        aggregate_deviations = [sum(utilities(s[:i] + (a,) + s[i + 1:])[i]
                                   for i in range(3)) for a in range(4)]
        g = [w - dev for dev in aggregate_deviations]
        simple = w - sum(y * gap for y, gap in zip(Y_SIMPLE, g))
        sharp = w - sum(y * gap for y, gap in zip(Y_SHARP, g))
        assert simple >= F(56, 9) and sharp >= F(544, 87)
        dual_rows.append({"counts_as_sorted_profile": s, "welfare": w, "G": g,
                          "L_simple": simple, "L_sharp": sharp,
                          "261_L_sharp": 261 * sharp})
    ordered_probs = {}
    for profile, prob in COUNT_PROBS.items():
        orbit = set(permutations(profile))
        for s in orbit:
            ordered_probs[s] = prob / len(orbit)
    assert sum(ordered_probs.values()) == 1
    cce_gaps = []
    for i in range(3):
        gaps = []
        for a in range(4):
            gap = sum(prob * (utilities(s)[i] - utilities(s[:i] + (a,) + s[i + 1:])[i])
                      for s, prob in ordered_probs.items())
            assert gap == (F(220, 261) if a == 0 else 0)
            gaps.append(gap)
        cce_gaps.append(gaps)
    expected_welfare = sum(prob * welfare(s) for s, prob in ordered_probs.items())
    assert expected_welfare == F(544, 87)
    p = (F(0), F(15, 23), F(4, 23), F(4, 23))
    q = {(1, 1): F(3, 23), (1, 2): F(10, 23), (1, 3): F(10, 23)}
    security_rows = [(b, sum(p[a] * f(a, b) for a in range(4)))
                     for b in combinations_with_replacement(range(4), 2)]
    assert min(value for b, value in security_rows) == F(44, 23)
    security_dual = [sum(prob * f(a, b) for b, prob in q.items()) for a in range(4)]
    assert security_dual == [F(26, 23)] + [F(44, 23)] * 3
    result = {"status": "all-exact-checks-passed", "customers": [sorted(c) for c in CUSTOMERS],
              "path": path, "utilities": utilities(path), "welfare": 6, "optimum": optimum,
              "history_count": len(histories), "comparison_count": len(margins),
              "histories": histories, "dual_rows": dual_rows,
              "sharp_cce_welfare": expected_welfare,
              "ordered_cce_distribution": [{"profile": s, "probability": prob} for s, prob in ordered_probs.items()],
              "individual_cce_gaps": cce_gaps, "security_primal_rows": security_rows,
              "security_dual_query_values": security_dual, "security_value": F(44, 23)}
    rendered = json.dumps(result, default=str, ensure_ascii=False, indent=2)
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(rendered)
    print(rendered)


if __name__ == "__main__":
    main()
