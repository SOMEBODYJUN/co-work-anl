#!/usr/bin/env python3
"""Exact finite audit for the heterogeneous-macro residual-capacity lemma.

This audit is deliberately independent of the scheduling implementation.  It
enumerates small assignments with Fraction arithmetic, checks OPT directly,
then verifies that every macro perfect matching leaves the tiny load of the
OPT witness below T/2 on each home.  The latter is the only completeness fact
used by the row-capacity LP in the accompanying proof.
"""
from fractions import Fraction as F
from itertools import permutations, product
import random


def optimum(P):
    m, n = len(P), len(P[0]) if P else 0
    best = None
    witnesses = []
    for assignment in product(range(m), repeat=n):
        loads = [F(0) for _ in range(m)]
        legal = True
        for j, i in enumerate(assignment):
            p = P[i][j]
            if p is None:
                legal = False
                break
            loads[i] += p
        if not legal:
            continue
        value = max(loads, default=F(0))
        if best is None or value < best:
            best, witnesses = value, [(assignment, loads)]
        elif value == best:
            witnesses.append((assignment, loads))
    if best is None:
        raise AssertionError("generated instance has no legal assignment")
    return best, witnesses


def macro_matchings(P, macro_count, home_count, T):
    result = []
    for home_order in permutations(range(home_count), macro_count):
        if all(P[h][b] is not None and P[h][b] <= T
               for b, h in enumerate(home_order)):
            result.append(dict(enumerate(home_order)))
    return result


def audit_random(seed=20261017, rounds=10000):
    rng = random.Random(seed)
    T, delta = F(1), F(1, 5)
    checked = 0
    for _ in range(rounds):
        h_count = rng.randint(1, 3)
        z_count = rng.randint(0, 2)
        machine_count = h_count + z_count
        tiny_count = rng.randint(0, 4)
        n = h_count + tiny_count
        P = [[None] * n for _ in range(machine_count)]

        # Macro columns: arbitrary identity-dependent times in (T/2,T],
        # while a planted permutation guarantees a T-feasible macro matching.
        planted = list(range(h_count))
        rng.shuffle(planted)
        for b in range(h_count):
            for h in range(h_count):
                if rng.random() < F(3, 4):
                    P[h][b] = F(rng.randint(51, 100), 100)
            P[planted[b]][b] = F(rng.randint(51, 100), 100)

        # Tiny eligibility and processing times are completely arbitrary.
        # Every finite edge is <= delta*T.
        for j in range(h_count, n):
            eligible = []
            for i in range(machine_count):
                if rng.random() < F(3, 4):
                    P[i][j] = F(rng.randint(0, 20), 100)
                    eligible.append(i)
            if not eligible:
                i = rng.randrange(machine_count)
                P[i][j] = F(rng.randint(0, 20), 100)

        opt, witnesses = optimum(P)
        if opt > T:
            continue
        matchings = macro_matchings(P, h_count, h_count, T)
        assert matchings, (P, opt)
        # Every optimum witness must have tiny home load < T/2.  This is
        # stronger than needed and attacks the strict boundary directly.
        for assignment, _loads in witnesses:
            tiny_home = [F(0) for _ in range(h_count)]
            for j in range(h_count, n):
                i = assignment[j]
                if i < h_count:
                    tiny_home[i] += P[i][j]
            assert all(v < T / 2 for v in tiny_home), (P, opt, assignment, tiny_home)
        # The post-ST bound uses only p_macro<=T, tiny support<=delta*T.
        for matching in matchings:
            for h in range(h_count):
                macro = next(b for b, hh in matching.items() if hh == h)
                assert P[h][macro] + T / 2 + delta * T <= F(3, 2) + delta
        checked += 1
    return checked


def audit_less_macro_boundary():
    # With fewer macros, a uniform T/2 home cap is no longer complete.
    # Five forced tiny jobs preserve every other promise, including delta=1/5.
    T, delta = F(1), F(1,5)
    P = [[F(1)]+[delta]*5, [F(1)]+[None]*5]
    opt, witnesses = optimum(P)
    assert opt == T
    assert witnesses == [((1,0,0,0,0,0), [F(1),F(1)])]
    assert all(P[0][j] <= delta*T for j in range(1,6))
    assert sum((P[0][j] for j in range(1,6)),F(0)) == 1 > T/2
    # No general LP solver is invoked: forced endpoint masses prove infeasibility.
    return {'OPT':str(opt), 'delta':str(delta), 'forced_tiny_load':'1',
            'uniform_home_tiny_cap':'1/2', 'legal_schedule':list(witnesses[0][0]),
            'solver_invoked':False}


if __name__ == "__main__":
    checked = audit_random()
    audit_less_macro_boundary()
    print(f"PASS random_promised={checked}, less_macro_boundary=1")
