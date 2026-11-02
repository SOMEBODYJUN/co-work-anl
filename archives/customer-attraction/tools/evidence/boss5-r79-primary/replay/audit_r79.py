#!/usr/bin/env python3
"""Independent exact audit of the two complete finite examples in R-79.

No solver result or finite example is promoted to a universal half theorem.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sys


def audit(players, labels, sigma, masses):
    types = [b for k in range(1, 1 << labels)
             if (b := frozenset(i for i in range(labels) if k >> i & 1))]
    def rollout(h):
        h = tuple(h)
        while len(h) < players:
            h += (sigma[h],)
        return h
    def coeff(action, leaf, b):
        return F(1, sum(a in b for a in leaf)) if action in b else F(0)
    def utility(action, leaf):
        return sum(masses.get(b, 0) * coeff(action, leaf, b) for b in types)
    rows = []
    for depth in range(players):
        for h in product(range(labels), repeat=depth):
            actual = rollout(h)
            for a in range(labels):
                alternative = rollout(h + (a,))
                gamma = [coeff(sigma[h], actual, b) - coeff(a, alternative, b)
                         for b in types]
                slack = utility(sigma[h], actual) - utility(a, alternative)
                assert slack >= 0, (h, a, slack)
                rows.append({"history": h, "prescribed": sigma[h], "action": a,
                             "actual_leaf": actual, "deviation_leaf": alternative,
                             "gamma": [str(x) for x in gamma], "slack": str(slack)})
    leaf = rollout(())
    used = set(leaf)
    welfare = sum(v for b, v in masses.items() if b & used)
    return {"types": [sorted(b) for b in types], "root_leaf": leaf,
            "root_labels": sorted(used), "welfare": welfare,
            "all_comparisons": len(rows), "minimum_slack": min(F(r["slack"]) for r in rows),
            "rows": rows}


original_sigma = {(): 0, (0,): 1, (1,): 1,
                  (0, 0): 1, (0, 1): 1, (1, 0): 0, (1, 1): 0}
farkas = audit(3, 2, original_sigma, {frozenset({0}): 1, frozenset({1}): 1})
assert farkas["root_leaf"] == (0, 1, 1)
assert farkas["root_labels"] == [0, 1]
farkas["correct_half_target_vector"] = ["1", "1", "1"]
farkas["root_only_certificate"] = {"all_multipliers": "0", "coordinate_residuals": ["1"] * 3}
farkas["source_claim_A_singleton_is_false"] = True
clock_sigma = {(): 1, (0,): 1, (1,): 1, (2,): 1}
clocks = audit(2, 3, clock_sigma,
               {frozenset({0}): 1, frozenset({1}): 5, frozenset({0, 1}): 3})
assert clocks["root_leaf"] == (1, 1)
assert clocks["welfare"] == 8
first_primitive = lambda r: F(2) / (1+r) - F(1) / (1+r)**2
second_primitive = lambda r: -F(8) / (1+r) + F(9) / (1+r)**2
part1 = first_primitive(F(1)) - first_primitive(F(0))
part2 = second_primitive(F(5,4)) - second_primitive(F(1))
assert (part1, part2, part1+part2) == (F(-1,4), F(-1,36), F(-5,18))
clocks["same_clock_weighted_ic"] = {"unweighted_expectation": "3/2",
    "negative_event": "Y0 < (5/4) Y1", "part_Y0_below_Y1": str(part1),
    "part_Y1_below_Y0_below_5Y1_over4": str(part2), "weighted_expectation": str(part1+part2),
    "integration_method": "r=Y0/Y1,t=Y1: density Jacobian t, integral t^2 exp(-(1+r)t)dt=2/(1+r)^3"}
out = {"method": "independent literal ordered histories and Fraction arithmetic; no original solver imported",
       "scope": "two frozen complete strategies only; no universal half claim",
       "farkas_source_example": farkas, "clock_source_example": clocks}
target = Path(sys.argv[1])
target.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str)+"\n")
print(json.dumps({"farkas_comparisons": farkas["all_comparisons"],
                  "clock_comparisons": clocks["all_comparisons"],
                  "correct_root_leaf": farkas["root_leaf"],
                  "clock_negative_expectation": str(part1+part2)}, ensure_ascii=False))
