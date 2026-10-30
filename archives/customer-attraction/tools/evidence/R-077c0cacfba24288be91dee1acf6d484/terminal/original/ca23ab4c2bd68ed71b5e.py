"""Explore the individual deficit bridge on complete fixed strategy cones.

Only exact post-verification may turn an LP separation into a mathematical result.
"""

from pathlib import Path
import sys
import itertools
import random
import json
from fractions import Fraction as F
from math import lcm
import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import CustomerType, Instance
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import verify_certificate


def rollout(actions, m, hist):
    out = tuple(hist)
    while len(out) < m:
        out += (actions[out],)
    return out


def payoff_row(q, terminal, topic):
    counts = [terminal.count(j) for j in range(q)]
    return tuple(F(int(mask >> topic & 1), sum(c for j, c in enumerate(counts) if mask >> j & 1))
                 if mask >> topic & 1 else F(0)
                 for mask in range(1, 1 << q))


def strategy_rows(q, m, actions):
    rows = []
    for length in range(m):
        for h in itertools.product(range(q), repeat=length):
            actual = rollout(actions, m, h)
            lhs = payoff_row(q, actual, actions[h])
            for a in range(q):
                if a == actions[h]:
                    continue
                changed = rollout(actions, m, h+(a,))
                rhs = payoff_row(q, changed, a)
                rows.append(tuple(x-y for x, y in zip(lhs, rhs)))
    return rows


def main():
    rng = random.Random(90101921)
    best = F(100)
    checked = 0
    for m, q, runs in [(4, 7, 15), (5, 7, 6)]:
        for run in range(runs):
            weights = {}
            for _ in range(rng.randrange(4, 3*q)):
                mask = sum(1 << j for j in rng.sample(range(q), rng.choice([1, 1, 2, 2, 3])))
                weights[mask] = weights.get(mask, 0)+rng.randrange(1, 11)
            seed = Instance(tuple(map(str, range(q))), tuple(
                CustomerType(frozenset(j for j in range(q) if mask >> j & 1), w)
                for mask, w in weights.items()), m)
            sol = ExactSPESolver(seed)
            cert = sol.certificate(min(sol.worst_outcomes()),
                                   action_selector=lambda h, opts: rng.choice(opts))
            actions = cert.actions
            terminal = rollout(actions, m, ())
            actual_support = set(terminal)
            Wrow = [F(any(mask >> j & 1 for j in actual_support))
                    for mask in range(1, 1 << q)]
            Urow = payoff_row(q, terminal, terminal[0])
            rows = list(set(strategy_rows(q, m, actions)))
            Aub = -np.array(rows, dtype=float)
            eq = np.array([Wrow], dtype=float)
            for optset in itertools.combinations(range(q), min(m, q)):
                Orow = [F(any(mask >> j & 1 for j in optset))
                        for mask in range(1, 1 << q)]
                objective = [w+m*u-o for w, u, o in zip(Wrow, Urow, Orow)]
                res = linprog(np.array(objective, dtype=float), A_ub=Aub,
                              b_ub=np.zeros(len(rows)), A_eq=eq, b_eq=[1],
                              bounds=(0, None), method="highs")
                checked += 1
                if res.status != 0:
                    continue
                if res.fun < float(best):
                    best = F(float(res.fun)).limit_denominator(10**6)
                if res.fun >= -1e-8:
                    continue
                rational = [F(float(x)).limit_denominator(10**8) for x in res.x]
                exact_slacks = [sum(a*x for a, x in zip(row, rational)) for row in rows]
                if min(exact_slacks) < 0:
                    print(json.dumps({"floating_negative": res.fun,
                                      "rational_failed": str(min(exact_slacks))}), flush=True)
                    continue
                denom = lcm(*(x.denominator for x in rational))
                integers = [int(x*denom) for x in rational]
                inst = Instance(tuple(map(str, range(q))), tuple(
                    CustomerType(frozenset(j for j in range(q) if mask >> j & 1), w)
                    for mask, w in enumerate(integers, 1) if w), m)
                ver = verify_certificate(inst, cert)
                assert ver.valid
                opt = inst.optimal_welfare()
                W = inst.welfare(inst.counts(terminal))
                u = inst.player_payoffs(terminal)
                assert opt > W+m*u[0]
                result = {"status": "exact counterexample", "instance": inst.to_dict(),
                          "certificate": cert.to_dict(), "path": terminal,
                          "W": W, "OPT": opt, "u": list(map(str, u)),
                          "gap": str(opt-W-m*u[0]), "LPs": checked}
                Path(__file__).with_name("individual_deficit_cone_counterexample.json").write_text(
                    json.dumps(result, indent=2)+"\n")
                print(json.dumps({key: result[key] for key in result if key not in ("certificate",)}, indent=2), flush=True)
                return
            print(json.dumps({"m": m, "q": q, "run": run, "LPs": checked,
                              "best_float": str(best)}), flush=True)


if __name__ == "__main__":
    main()
