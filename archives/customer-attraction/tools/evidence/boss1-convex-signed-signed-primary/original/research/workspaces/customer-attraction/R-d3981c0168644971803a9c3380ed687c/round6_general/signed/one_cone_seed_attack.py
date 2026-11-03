"""One designated LP attack, freezing genuine complete exit strategies.

No positive inference from feasibility or a nonnegative optimum.  A negative
floating optimum is only a candidate until all constraints pass rational QA.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT))
import numpy as np
from scipy.optimize import linprog
from customer_attraction.exact import ExactSPESolver
from customer_attraction.model import Instance


def main():
    obj = json.loads((ROOT / "examples/customer_attraction/root_tax_failure.json").read_text())
    ins = Instance.from_dict(dict(obj, players=5))
    sol = ExactSPESolver(ins)
    sol.outcomes()
    p, m = ins.topic_count, ins.players
    path = (0, 0, 0, 0, 5)
    types = [tuple(a for a in range(p) if mask >> a & 1) for mask in range(1, 1 << p)]
    q, d = len(types), m - 1
    constraints = set()

    def inc(c, a):
        return c[:a] + (c[a] + 1,) + c[a+1:]

    @lru_cache(None)
    def coeff(c, a):
        return tuple(F(1, sum(c[b] for b in typ)) if a in typ else F(0) for typ in types)

    def diff(a, b):
        return tuple(x-y for x, y in zip(a, b))

    @lru_cache(None)
    def realize(c, terminal):
        if sum(c) == m:
            assert c == terminal
            return terminal
        floor = sol.threshold(c)
        actions = [a for a in range(p) if terminal in sol.outcomes(inc(c, a))
                   and sol._utility(terminal, a) >= floor]
        prescribed = actions[0]
        realize(inc(c, prescribed), terminal)
        for a in range(p):
            if a == prescribed:
                continue
            child = sol.outcomes(inc(c, a))
            alternative = min(child, key=lambda t: (sol._utility(t, a), t))
            realize(inc(c, a), alternative)
            constraints.add(diff(coeff(terminal, prescribed), coeff(alternative, a)))
        return terminal

    exits = []
    for i in range(d):
        c = ins.counts(path[:i])
        row = []
        for a in range(p):
            child = sol.outcomes(inc(c, a))
            terminal = min(child, key=lambda t: (sol._utility(t, a), t))
            realize(inc(c, a), terminal)
            row.append((a, terminal, coeff(terminal, a)))
        exits.append(row)
    final = ins.counts(path, terminal=True)
    upath = [coeff(final, a) for a in path]
    # The target last action remains a true static BR after every weight change.
    c = ins.counts(path[:-1])
    for a in range(p):
        constraints.add(diff(upath[-1], coeff(inc(c, a), a)))

    # Every maximal feasible comparator support has five of the six topics.
    w = tuple(F(bool(set(t) & set(path))) for t in types)
    nvars = q + d + 1
    aub, bub = [], []
    for row in constraints:
        aub.append([-float(x) for x in row] + [0.] * (d+1)); bub.append(0.)
    for i, row in enumerate(exits):
        for a, terminal, values in row:
            ar = list(map(float, values)) + [0.] * (d+1)
            ar[q+i] = -1.
            aub.append(ar); bub.append(0.)
    # K_pm has integral vertices: all coordinates 1/2, with at most one 0 and
    # at most one 3.  Enumerating this superset also includes nonvertices, safely.
    prices = [lam for lam in product(range(4), repeat=d)
              if sum(max(1-x, 0) for x in lam) <= 1
              and sum(max(x-2, 0) for x in lam) <= 1]
    for lam in prices:
        ar = [-float(sum(F(lam[i]) * upath[i][j] for i in range(d))) for j in range(q)]
        ar += list(map(float, lam)) + [-1.]
        aub.append(ar); bub.append(0.)
    aeq = [[1.] * q + [0.] * (d+1)]
    attempts = []
    for omit in range(p):
        comparator = set(range(p)) - {omit}
        o = tuple(F(bool(set(t) & comparator)) for t in types)
        bcoef = tuple(2*x-y for x, y in zip(w, o))
        objective = list(map(float, bcoef)) + [0.] * d + [1.]
        ans = linprog(objective, A_ub=np.array(aub), b_ub=np.array(bub),
                      A_eq=aeq, b_eq=[1.], bounds=[(0, None)]*(q+d) + [(None, None)],
                      method="highs")
        attempts.append((ans.fun, omit, bcoef, ans))
    _, omit, bcoef, ans = min(attempts, key=lambda row: row[0])
    linear_attacks = {}
    for price in (F(1), F(3, 2), F(2)):
        candidates = []
        for excluded in range(p):
            comparator = set(range(p)) - {excluded}
            o = tuple(F(bool(set(typ) & comparator)) for typ in types)
            bc = tuple(2*x-y for x, y in zip(w, o))
            cc = [float(bc[j] - price * sum(upath[i][j] for i in range(d)))
                  for j in range(q)] + [float(price)]*d + [0.]
            la = linprog(cc, A_ub=np.array(aub), b_ub=np.array(bub),
                         A_eq=aeq, b_eq=[1.], bounds=[(0, None)]*(q+d) + [(None, None)],
                         method="highs")
            candidates.append((la.fun, excluded, la))
        value, excluded, la = min(candidates, key=lambda row:row[0])
        linear_attacks[str(price)] = {"minimum_float":value, "comparator_omits":excluded}
    report = {"target": path, "types": q, "exit_IC_rows": len(constraints),
              "complete_subtrees": realize.cache_info().currsize,
              "LP_status": ans.message, "objective_float": ans.fun,
              "all_comparator_objectives_float": {str(a[1]):a[0] for a in attempts},
              "best_comparator_omits": omit,
              "fixed_price_attacks":linear_attacks,
              "scope": "One frozen full-exit-policy cone only; not a universal lower bound."}
    if ans.success:
        values = [F(float(x)).limit_denominator(1000000) for x in ans.x]
        weights, upper, t = values[:q], values[q:q+d], values[-1]
        ic = [sum(x*y for x,y in zip(row, weights)) for row in constraints]
        exit_slack = [upper[i] - sum(x*y for x,y in zip(row[2], weights))
                      for i, rows in enumerate(exits) for row in rows]
        u = [sum(x*y for x,y in zip(row, weights)) for row in upath]
        g = [x-y for x,y in zip(upper, u)]
        pos, neg = [max(x,0) for x in g], [max(-x,0) for x in g]
        cost = 2*sum(pos)-sum(neg)+max(pos)+max(neg)
        b = sum(x*y for x,y in zip(bcoef,weights))
        report.update({"rational_IC_min": str(min(ic)),
                       "rational_exit_slack_min": str(min(exit_slack)),
                       "rational_seed_budget": str(b+cost),
                       "rational_sum_weights": str(sum(weights)),
                       "rational_g": list(map(str,g)),
                       "nonzero_weights": [{"topics": types[j], "weight":str(x)}
                                           for j,x in enumerate(weights) if x],
                       "U": list(map(str,upper)), "u":list(map(str,u)),
                       "B_comparator":str(b)})
    destination = Path(__file__).with_name("one_cone_seed_attack.json")
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
