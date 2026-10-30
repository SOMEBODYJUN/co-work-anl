#!/usr/bin/env python3
"""Literal Fraction audit of WC-R2-DENSITY-MOMENT / WEIGHT-DENSITY v1.

This finite audit does not prove either arbitrary-real theorem. Power p=1/m
is represented by rational roots h_i; w_i=h_i**m. Every inequality involving
the possibly irrational bound B is checked by raising nonnegative sides to m.
No approximate roots, floating tolerances, or equilibrium ratios at 0/0 occur.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import platform
import random
import subprocess

ROOT = Path(__file__).resolve().parents[2]
SEED = 20261014


def density(weights, ratio):
    """Exact maximum half-open window count, including multiplicities."""
    return max((sum(x <= w < ratio*x for w in weights)
                for x in weights), default=0)


def a_power(m, q):
    # R=q**m, p=1/m, so A_R(p)**m is rational.
    return (1-F(1, q**m))/(1-F(1, q))**m


def moment_audit():
    rng = random.Random(SEED)
    count = 0
    sharp_ratios = []
    for m, q in product(range(2, 6), (2, 3, 5)):
        ratio = F(q**m)
        am = a_power(m, q)
        for multiplicity, length in product(range(1, 5), (0, 1, 2, 5, 9, 24)):
            roots = [F(1, q**j) for j in range(length)
                     for _ in range(multiplicity)]
            weights = [h**m for h in roots]
            k = density(weights, ratio)
            assert not roots or k == multiplicity
            lhs = sum(roots, F(0))**m
            rhs = am*k**(m-1)*sum(weights, F(0))
            assert lhs <= rhs
            count += 1
            if length == 24:
                sharp_ratios.append({"m":m, "q":q, "K":k,
                                     "lhs_over_bound":str(lhs/rhs)})
        for _ in range(80):
            roots = [F(rng.randrange(1, 15), rng.randrange(1, 15))
                     *F(q)**rng.randrange(-5, 6)
                     for _ in range(rng.randrange(1, 20))]
            weights = [h**m for h in roots]
            k = density(weights, ratio)
            assert sum(roots, F(0))**m <= (
                am*k**(m-1)*sum(weights, F(0)))
            count += 1
    # The exact endpoint matters: [1,4) includes 1 and excludes 4.
    assert density([F(1), F(4), F(16)], F(4)) == 1
    assert density([F(1), F(4)-F(1, 1000)], F(4)) == 2
    return {"checks":count, "sharp_finite_sequence_ratios":sharp_ratios}


def costs(state, strategies, weights, coeff):
    loads = [F(0) for _ in coeff]
    for i, action in enumerate(state):
        for e in strategies[i][action]:
            loads[e] += weights[i]
    values = [sum((a*loads[e]**k for k,a in enumerate(poly)), F(0))
              for e,poly in enumerate(coeff)]
    own = [sum((values[e] for e in strategies[i][action]), F(0))
           for i,action in enumerate(state)]
    return own, loads, values


def audit_game(roots, m, q, strategies, coeff):
    weights = [h**m for h in roots]
    d = max(len(poly)-1 for poly in coeff)
    n = len(roots)
    potential_users = [[i for i in range(n)
                        if any(e in action for action in strategies[i])]
                       for e in range(len(coeff))]
    k = max(density([weights[i] for i in users], F(q**m))
            for users in potential_users)
    bm = a_power(m,q)*k**(m-1)*d
    states = list(product(*(range(len(s)) for s in strategies)))
    data = {s:costs(s,strategies,weights,coeff) for s in states}
    potentials = {s:sum((roots[i]*data[s][0][i] for i in range(n)),F(0))
                  for s in states}
    best = min(potentials.values())
    minima = [s for s in states if potentials[s] == best]
    moves = acquired = zero_new = common = 0
    for s in states:
        old_cost, loads, old_values = data[s]
        for i in range(n):
            for action in range(len(strategies[i])):
                if action == s[i]:
                    continue
                new = list(s)
                new[i] = action
                new = tuple(new)
                nc, nl, nv = data[new]
                old_strategy = strategies[i][s[i]]
                new_strategy = strategies[i][action]
                common += bool(old_strategy & new_strategy)
                assert all(loads[e] == nl[e] for e in old_strategy & new_strategy)
                if nc[i] == 0:
                    zero_new += 1
                # Check every newly acquired resource's externality exactly.
                for e in new_strategy-old_strategy:
                    acquired += 1
                    inc = [j for j in range(n) if j != i
                           and e in strategies[j][s[j]]]
                    ext = sum((roots[j] for j in inc),F(0))*(nv[e]-old_values[e])
                    assert ext >= 0
                    if nv[e] == 0:
                        assert ext == 0
                    else:
                        assert (ext/(roots[i]*nv[e]))**m <= bm
                # The full move inequality is L <= B*C_i(new), where
                # L = DeltaPsi/h_i + C_i(old)-C_i(new).
                dp = potentials[new]-potentials[s]
                left = dp/roots[i]+old_cost[i]-nc[i]
                if nc[i] == 0:
                    assert left <= 0
                elif left > 0:
                    assert (left/nc[i])**m <= bm
                # Exact comparison with alpha=1+B, avoiding an irrational root.
                violates = old_cost[i] > nc[i] and (
                    nc[i] == 0 or ((old_cost[i]/nc[i])-1)**m > bm)
                if violates:
                    assert dp < 0
                    assert s not in minima
                moves += 1
    return {"states":len(states), "moves":moves, "acquired":acquired,
            "zero_new":zero_new, "common":common, "minima":len(minima),
            "K_R":k, "B_to_m":str(bm)}


def game_audit():
    rng = random.Random(SEED+1)
    totals = {key:0 for key in ("games","states","moves","acquired",
                               "zero_new","common","minima")}
    parameters = []
    for m,q in product((2,3,4),(2,3)):
        for trial in range(8):
            n = 3+trial%3
            roots = ([F(1,q**j) for j in range(n)] if trial < 4
                     else [F(rng.randrange(1,8),rng.randrange(1,8))
                           for _ in range(n)])
            # Every player has empty, shared, and random actions. e=0 retained
            # by the nonempty actions and e=3 has identically zero latency.
            strategies = [[frozenset(), frozenset((0,3)),
                           frozenset((0,1+(i%2),3))] for i in range(n)]
            d = (1,2,3,4,7,9,12,16)[trial]
            coeff = [[F(rng.randrange(3),rng.randrange(1,5))
                      for _ in range(d+1)] for _ in range(3)] + [[F(0)]]
            result = audit_game(roots,m,q,strategies,coeff)
            totals["games"] += 1
            for key in totals:
                if key != "games":
                    totals[key] += result[key]
            parameters.append({"m":m,"q":q,"trial":trial,"d":d,
                               "roots":[str(h) for h in roots], **result})
    # All-zero costs: every state minimizes; empty strategies cause no 0/0.
    result = audit_game([F(1),F(1,2)],2,2,
                        [[frozenset(),frozenset((0,))]]*2, [[F(0),F(0)]])
    totals["games"] += 1
    for key in totals:
        if key != "games":
            totals[key] += result[key]
    parameters.append({"case":"all_zero", **result})
    return {"totals":totals,"parameters":parameters}


def endpoint_audit():
    checks = 0
    for d,m,q in product((3,4,8,16,32,64),(2,3,4),(2,3)):
        # Complete geometric spectrum: exact K_d is the largest number of
        # q**m-spaced weights in a half-open d window.
        weights = [F(q)**(m*j) for j in range(30)]
        k = density(weights,F(d))
        expected = 1
        while q**(m*expected) < d:
            expected += 1
        assert k == expected
        checks += 1
    # Degree zero: arbitrary strategy costs are independent of the profile.
    coeff = [[F(3)],[F(0)],[F(7)]]
    strategies = [[frozenset((0,)),frozenset((1,))],
                  [frozenset((2,)),frozenset()]]
    weights = [F(1,10**12),F(10**12)]
    for s in product((0,1),repeat=2):
        ci,_,_ = costs(s,strategies,weights,coeff)
        assert ci == [F(3) if s[0]==0 else F(0),
                      F(7) if s[1]==0 else F(0)]
        checks += 1
    return {"checks":checks}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    report = {"schema_version":1,"claims":["WC-R2-DENSITY-MOMENT v1",
                                         "WC-R2-WEIGHT-DENSITY v1"],
              "seed":SEED,"python_version":platform.python_version(),
              "arithmetic":"fractions.Fraction; exact nonnegative mth-power comparisons",
              "base_commit":subprocess.check_output(["git","rev-parse","HEAD"],
                                                    cwd=ROOT,text=True).strip(),
              "replay_command":"python3 tests/audits/weighted_congestion_density.py --output evidence/runs/2026-10-14/weighted_congestion_density.json",
              "moment":moment_audit(),"games":game_audit(),
              "endpoints":endpoint_audit(),
              "limitations":"Finite rational audit, not a proof for arbitrary real weights, coefficients, R or p. No tolerance and no numerical root approximation used."}
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"status":"passed","moment_checks":report["moment"]["checks"],
                      **report["games"]["totals"],
                      "endpoint_checks":report["endpoints"]["checks"]}))


if __name__ == "__main__":
    main()
