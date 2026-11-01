#!/usr/bin/env python3
"""Discover a nonnegative fixed-tree flow using pair and six-payoff circuits.

This is an exploratory LP. Accepted certificates are checked with Fraction;
the independent verifier will not import this file or an optimizer.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog


P = 6
M = 3


def counts(hist):
    return tuple(hist.count(a) for a in range(P))


def strategy(hist):
    if not hist:
        return 0
    if len(hist) == 1:
        return 3 if hist[0] < 3 else 0
    group = range(3) if hist[1] < 3 else range(3, 6)
    return next(a for a in group if a not in hist)


def terminal(hist):
    hist = tuple(hist)
    while len(hist) < M:
        hist += (strategy(hist),)
    return counts(hist)


def main():
    qs = sorted(set(counts(h) for h in product(range(P), repeat=M)))
    vertices = [(q, a) for q in qs for a in range(P) if q[a]]
    ix = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)

    def row(terms):
        out = [F(0)]*n
        for coefficient, q, a in terms:
            out[ix[(q, a)]] += coefficient
        return out

    def total(q):
        return row([(F(q[a]), q, a) for a in range(P) if q[a]])

    inequalities, inames, equalities, enames = [], [], [], []
    for depth in range(M):
        for h in product(range(P), repeat=depth):
            for b in range(P):
                inequalities.append(row([(F(1), terminal(h), strategy(h)),
                                         (F(-1), terminal(h+(b,)), b)]))
                inames.append({"kind": "true_edge", "history": h, "deviation": b})
    for q, a in vertices:
        for r, b in vertices:
            if a != b or q == r:
                continue
            kappa = max(F(sum(r[c] for c in range(P) if mask >> c & 1),
                          sum(q[c] for c in range(P) if mask >> c & 1))
                        for mask in range(1, 1 << P) if mask >> a & 1)
            inequalities.append(row([(kappa, r, a), (F(-1), q, a)]))
            inames.append({"kind": "dilution", "q": q, "r": r,
                           "topic": a, "kappa": str(kappa)})
    for a, b in combinations(range(P), 2):
        pa = counts((a, a, a)); pb = counts((b, b, b))
        q = counts((a, a, b)); r = counts((a, b, b))
        specs = [([(1, r, a), (-1, q, b), (-3, pa, a), (3, pb, b)], "difference_1"),
                 ([(2, q, a), (-2, r, b), (-3, pa, a), (3, pb, b)], "difference_2"),
                 ([(2, q, a), (2, r, b), (-1, r, a), (-3, pb, b)], "pair_positive")]
        for terms, label in specs:
            equalities.append(row([(F(c), q0, a0) for c, q0, a0 in terms]))
            enames.append({"kind": label, "a": a, "b": b})
    for triple in combinations(range(P), 3):
        for c in triple:
            a, b = [j for j in triple if j != c]
            abc, aac, bbc = counts(triple), counts((a,a,c)), counts((b,b,c))
            equalities.append(row([(F(4), abc, a), (F(8), bbc, b), (F(1), bbc, c),
                                   (F(-4), abc, b), (F(-8), aac, a), (F(-1), aac, c)]))
            enames.append({"kind": "six_payoff", "a": a, "b": b, "background": c})
    root = total(terminal(()))
    objective = total(counts((1,2,4)))
    eq = [root]+equalities
    rhs = [F(1)]+[F(0)]*len(equalities)
    result = linprog(-np.array(objective, float),
                     A_ub=-np.array(inequalities, float), b_ub=np.zeros(len(inequalities)),
                     A_eq=np.array(eq, float), b_eq=np.array(rhs, float),
                     bounds=(0,None), method="highs")
    assert result.success, result.message
    y = [F(float(z)).limit_denominator(10**7) for z in result.x]
    mu = [F(float(-z)).limit_denominator(10**7) for z in result.ineqlin.marginals]
    nu = [F(float(-z)).limit_denominator(10**7) for z in result.eqlin.marginals]
    dot = lambda a, b: sum(x*y for x, y in zip(a,b))
    assert all(z >= 0 for z in y)
    assert all(dot(r,y) >= 0 for r in inequalities)
    assert all(dot(r,y) == z for r,z in zip(eq,rhs))
    slack = [sum(z*r[j] for z,r in zip(nu,eq))
             - sum(z*r[j] for z,r in zip(mu,inequalities)) - objective[j] for j in range(n)]
    assert all(z >= 0 for z in mu) and all(z >= 0 for z in slack)
    assert dot(objective,y) == nu[0]
    # Select a cheaper flow at the already certified 8/5 objective.  The
    # equality multipliers are split into two nonnegative parts; this keeps
    # their signed role distinct from incentive/dilution multipliers.
    beta = nu[0]
    rr = np.array(inequalities, float).T
    ee = np.array(equalities, float).T
    dual_matrix = np.column_stack((rr, ee, -ee, np.eye(n)))
    costs = np.concatenate((np.ones(len(inequalities)),
                            np.ones(2*len(equalities)), np.ones(n)))
    selected = linprog(costs, A_eq=dual_matrix,
                       b_eq=np.array([beta*x-z for x,z in zip(root,objective)], float),
                       bounds=(0,None), method="highs")
    assert selected.success, selected.message
    z = [F(float(v)).limit_denominator(10**7) for v in selected.x]
    cut = len(inequalities)
    mu2 = z[:cut]
    theta2 = [z[cut+j]-z[cut+len(equalities)+j] for j in range(len(equalities))]
    slack2 = z[-n:]
    assert all(v >= 0 for v in mu2+slack2)
    for j in range(n):
        assert beta*root[j]-objective[j] == (sum(v*r[j] for v,r in zip(mu2,inequalities))
                                            +sum(v*r[j] for v,r in zip(theta2,equalities))
                                            +slack2[j])
    mu, nu, slack = mu2, [beta]+theta2, slack2
    report = {"status": "Fraction primal and dual checked", "bound": str(nu[0]),
              "scope": "One complete policy and comparison support; abstract payoff relaxation.",
              "players": M, "topics": P, "root": terminal(()), "comparison": [1,2,4],
              "primal": [{"q": q, "a": a, "value": str(z)}
                         for (q,a), z in zip(vertices,y) if z],
              "nonnegative_rows": [{**name, "multiplier": str(z)}
                                   for name,z in zip(inames,mu) if z],
              "circuit_rows": [{**name, "multiplier": str(z)}
                               for name,z in zip(enames,nu[1:]) if z],
              "slack": [{"q": q, "a": a, "coefficient": str(z)}
                        for (q,a), z in zip(vertices,slack) if z],
              "counts": {"vertices": n, "true_edges": 258, "dilutions": 2520,
                         "pair_circuits": 45, "six_payoff_circuits": 60,
                         "positive_rows_used": sum(bool(z) for z in mu),
                         "identities_used": sum(bool(z) for z in nu[1:])}}
    target = Path(__file__).with_name("circuit_flow_certificate.json")
    target.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items()
                      if k not in ("primal", "nonnegative_rows", "circuit_rows", "slack")}))


if __name__ == "__main__":
    main()
