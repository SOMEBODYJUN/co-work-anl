"""Attack OPT_m(uncovered) <= W inside an explicit full m=2 strategy cone."""
from fractions import Fraction
from itertools import combinations
import json

import numpy as np
from scipy.optimize import linprog


def signatures(k):
    return tuple(frozenset(s) for size in range(1, k + 1)
                 for s in combinations(range(k), size))


def coefficient(signature, terminal, player):
    return (Fraction(1, sum(a in signature for a in terminal))
            if terminal[player] in signature else Fraction(0))


def run():
    k = 5
    sigs = signatures(k)
    response = (1, 2, 1, 2, 0)
    actual = (4, response[4])
    comparisons = []
    for first in range(k):
        selected = (first, response[first])
        for deviated in range(k):
            branch = (first, deviated)
            comparisons.append(tuple(coefficient(s, selected, 1) -
                                     coefficient(s, branch, 1) for s in sigs))
    for deviated in range(k):
        branch = (deviated, response[deviated])
        comparisons.append(tuple(coefficient(s, actual, 0) -
                                 coefficient(s, branch, 0) for s in sigs))
    cover = tuple(Fraction(bool(set(actual) & s)) for s in sigs)
    reports = []
    for topics in combinations(range(k), 2):
        residual = tuple(Fraction(not (set(actual) & s) and bool(set(topics) & s))
                         for s in sigs)
        opt = linprog(-np.array(residual, dtype=float),
                      A_ub=-np.array(comparisons, dtype=float),
                      b_ub=np.zeros(len(comparisons)),
                      A_eq=np.array([cover], dtype=float), b_eq=np.ones(1),
                      bounds=(0, None), method="highs")
        report = {"topics": topics, "status": opt.message}
        if opt.success:
            weights = tuple(Fraction(float(x)).limit_denominator(100000) for x in opt.x)
            report["maximum_residual_over_W"] = str(sum(x*y for x,y in zip(residual, weights)))
            report["verified_feasible"] = all(sum(x*y for x,y in zip(row, weights)) >= 0
                                              for row in comparisons)
            report["support"] = [{"topics": sorted(s), "weight": str(w)}
                                 for s,w in zip(sigs,weights) if w]
        reports.append(report)
    print(json.dumps(reports, indent=2))


if __name__ == "__main__":
    run()
