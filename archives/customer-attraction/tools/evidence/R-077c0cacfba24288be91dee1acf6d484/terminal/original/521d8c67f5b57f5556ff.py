"""Fractional price-potential probes on a fixed non-PNE three-player strategy."""

from probe_deficit_cone import strategy_rows, rollout, payoff_row
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, product
from math import lcm
import numpy as np
from scipy.optimize import linprog
import json


def main():
    q, m = 6, 3
    actions = {(): 0}
    for a in range(q):
        actions[(a,)] = 3 if a < 3 else 0
    for a, b in product(range(q), repeat=2):
        group = range(0, 3) if b < 3 else range(3, 6)
        actions[(a, b)] = next(c for c in group if c not in (a, b))
    terminal = rollout(actions, m, ())
    Wrow = [F(any(mask >> j & 1 for j in terminal)) for mask in range(1, 1 << q)]
    Urow = payoff_row(q, terminal, terminal[0])
    rows = list(set(strategy_rows(q, m, actions)))
    Aub = -np.array(rows, dtype=float)
    total = 0
    best = 100
    best_query = None
    for subset_size in range(1, q+1):
        for subset in combinations(range(q), subset_size):
            for tau in [F(1), F(3, 2), F(2), F(5, 2), F(3), F(4), F(5), F(6)]:
                price_query = {topic: tau/subset_size for topic in subset}
                cap = [min(F(1), sum(z for topic, z in price_query.items() if mask >> topic & 1))
                       for mask in range(1, 1 << q)]
                objective = [w+tau*u-c for w, u, c in zip(Wrow, Urow, cap)]
                res = linprog(np.array(objective, dtype=float), A_ub=Aub,
                              b_ub=np.zeros(len(rows)), A_eq=[list(map(float, Wrow))],
                              b_eq=[1], bounds=(0, None), method="highs")
                total += 1
                assert res.status == 0
                if res.fun < best:
                    best, best_query = res.fun, (subset, str(tau))
                if res.fun < -1e-8:
                    x = [F(float(v)).limit_denominator(10**8) for v in res.x]
                    exact_slack = min(sum(a*b for a, b in zip(row, x)) for row in rows)
                    exact_objective = sum(a*b for a, b in zip(objective, x))
                    report = {"status": "floating candidate; exact arithmetic follows",
                              "subset": subset, "tau": str(tau),
                              "exact_min_Gamma": str(exact_slack),
                              "exact_objective": str(exact_objective),
                              "weights": [str(v) for v in x], "path": terminal}
                    Path(__file__).with_name("fractional_deficit_candidate.json").write_text(
                        json.dumps(report, indent=2)+"\n")
                    print(json.dumps(report, indent=2))
                    return
    report = {"status": "no separation in specified finite query family",
              "LPs": total, "best_float": best, "best_query": best_query,
              "strategy": "known two-group six-topic three-player non-PNE strategy",
              "scope": "fixed strategy cone, uniform fractional queries on all topic subsets"}
    Path(__file__).with_name("fractional_deficit_probe_report.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
