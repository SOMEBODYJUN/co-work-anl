#!/usr/bin/env python3
"""Finite exact audits. No finite run proves the general propositions."""
from fractions import Fraction as F
from itertools import product
from math import isqrt
from pathlib import Path
import hashlib
import json
import random
import sys

OUT = Path(__file__).with_name('audit.json')
rng = random.Random(20261021)


def val(coeff, x):
    return sum((a*x**k for k, a in enumerate(coeff)), F(0))


def integ(coeff, lo, hi):
    return sum((a*(hi**(k+1)-lo**(k+1))/F(k+1)
                for k, a in enumerate(coeff)), F(0))


def loads(state, menus, weights, m):
    out = [F(0)]*m
    for i, a in enumerate(state):
        for e in menus[i][a]:
            out[e] += weights[i]
    return out


def cost(state, i, menus, ls, polynomials):
    return sum((val(polynomials[e], ls[e]) for e in menus[i][state[i]]), F(0))


def affine_phi(state, menus, weights, m):
    ls = loads(state, menus, weights, m)
    sq = sum((w*w*len(menus[i][state[i]]) for i, w in enumerate(weights)), F(0))
    return (sum((x*x for x in ls), F(0))+sq)/2


def next_states(state, menus):
    for i, acts in enumerate(menus):
        for a in range(len(acts)):
            if a != state[i]:
                t = list(state)
                t[i] = a
                yield i, tuple(t)


def integral_audits():
    n_games = n_source_states = n_checked_edges = n_descending = 0
    improved_local_contract = 0
    for _ in range(100):
        n, m = 3, 4
        weights = [F(rng.randint(1, 4), rng.randint(1, 3)) for _ in range(n)]
        menus = []
        for i in range(n):
            acts = []
            for j in range(3):
                acts.append(frozenset(e for e in range(m) if rng.randrange(2)))
            menus.append(acts)
        polynomials = []
        for e in range(m):
            d = rng.randint(1, 8)
            c = [F(rng.randint(0, 3), rng.randint(1, 4)) for _ in range(d+1)]
            c[-1] += 1
            polynomials.append(c)
        states = list(product(*(range(len(x)) for x in menus)))
        data = {}
        for s in states:
            ls = loads(s, menus, weights, m)
            ph = sum((integ(polynomials[e], F(0), ls[e]) for e in range(m)), F(0))
            cs = [cost(s, i, menus, ls, polynomials) for i in range(n)]
            data[s] = (ls, ph, cs)
        seed = rng.choice(states)
        cap = data[seed][1]
        src = [s for s in states if data[s][1] <= cap]

        def ratio_min(domain):
            ratios = [F(1)]
            for s in domain:
                ls, _, _ = data[s]
                for i in range(n):
                    deletable = set().union(*(menus[i][s[i]]-a for a in menus[i]))
                    for e in deletable:
                        c = val(polynomials[e], ls[e])
                        if c:
                            ratios.append(integ(polynomials[e], ls[e]-weights[i], ls[e])/(weights[i]*c))
            return min(ratios)

        a = ratio_min(src)
        global_a = ratio_min(states)
        assert 0 < a <= 1 and global_a <= a
        beta = 1/a
        if a > global_a:
            improved_local_contract += 1
        for s in src:
            ls, ph, cs = data[s]
            for i, t in next_states(s, menus):
                _, tph, tcs = data[t]
                # The proof's full-cost bound uses no target-domain assumption.
                assert tph-ph <= weights[i]*(tcs[i]-a*cs[i])
                if cs[i] > beta*tcs[i]:
                    assert tph < ph and tph <= cap
                    n_descending += 1
                n_checked_edges += 1
        n_source_states += len(src)
        n_games += 1
    return dict(games=n_games, source_states=n_source_states,
                all_unrestricted_deviations_checked=n_checked_edges,
                strict_improvement_edges=n_descending,
                games_with_strictly_better_source_than_allstate_integral_contract=improved_local_contract)


def transfer_audits():
    cases = states_checked = edges_checked = strict_edges = path_moves = 0
    for _ in range(80):
        n = 3
        weights = [F(1), F(5, 4), F(3, 2)]
        m = 2*n+3
        d = rng.randint(2, 9)
        b = isqrt(8*n)
        if b*b < 8*n:
            b += 1
        cap_coeff = F(1, d*b**(d-1))
        # Two private seed resources per player; seed Phi = 77/8 < 4n.
        menus = []
        for i in range(n):
            acts = [frozenset((2*i, 2*i+1))]
            for j in range(3):
                acts.append(frozenset(e for e in range(m) if rng.randrange(4) == 0))
            menus.append(acts)
        orig = []
        for e in range(m):
            cc = [F(0)]*(d+1)
            cc[1] = 1
            cc[d] = cap_coeff*F(rng.randint(0, 10), 10)
            orig.append(cc)
        base = [[F(0), F(1)] for _ in range(m)]
        allstates = list(product(*(range(len(a)) for a in menus)))
        seed = (0,)*n
        cap = affine_phi(seed, menus, weights, m)
        assert cap <= 4*n
        kappa = F(d+1, d)
        alpha = kappa*kappa
        data = {}
        for s in allstates:
            ls = loads(s, menus, weights, m)
            ph = affine_phi(s, menus, weights, m)
            tc = [cost(s, i, menus, ls, orig) for i in range(n)]
            bc = [cost(s, i, menus, ls, base) for i in range(n)]
            assert all(x <= y for x, y in zip(bc, tc))
            if ph <= cap:
                assert all(x <= b for x in ls)
                assert all(x <= kappa*y for x, y in zip(tc, bc))
            data[s] = (ph, tc, bc)
        for s in allstates:
            ph, tc, bc = data[s]
            if ph > cap:
                continue
            states_checked += 1
            for i, t in next_states(s, menus):
                tph, ttc, tbc = data[t]
                assert tph-ph == weights[i]*(tbc[i]-bc[i])
                assert tph-ph <= weights[i]*(ttc[i]-tc[i]/kappa)
                if tc[i] > alpha*ttc[i]:
                    assert tph < ph and tph <= cap
                    assert ph-tph > F(1, d+1)
                    strict_edges += 1
                edges_checked += 1
        current = seed
        count = 0
        while True:
            ph, tc, bc = data[current]
            candidate = None
            for i, t in next_states(current, menus):
                if tc[i] > alpha*data[t][1][i]:
                    candidate = t
                    break
            if candidate is None:
                # Full original deviation check, no domain filtering.
                assert all(tc[i] <= alpha*data[t][1][i] for i, t in next_states(current, menus))
                break
            current = candidate
            count += 1
            assert count < 4*n*(d+1)
        path_moves += count
        cases += 1
    return dict(games=cases, source_states=states_checked,
                all_unrestricted_deviations_checked=edges_checked,
                strict_improvement_edges=strict_edges,
                complete_original_game_paths=cases, total_path_moves=path_moves)


def boundary_and_example():
    d, n, b = 20, 64, 23
    coeff = F(1, d*b**(d-1))
    globz = coeff*F(80)**(d-1)
    elasticity = (1+d*globz)/(1+globz)
    assert globz > 10**8
    assert elasticity > F(1999, 100)
    assert F(32)*(2*F(1)**2+2*F(3, 2)**2) == 208
    assert F(d+1, d)**2 == F(441, 400)
    poly = [F(1), F(0), F(0), F(0), F(1)]
    rv = {str(t): integ(poly, F(t-1), F(t))/val(poly, F(t)) for t in (1, 2, 100)}
    assert rv['2'] < min(rv['1'], rv['100'])
    # Boundary: source-only equality without global minorant does not close.
    base_cost = [F(1), F(100)]
    true_cost = [F(1), F(0)]
    assert true_cost[0] == base_cost[0]
    assert true_cost[0] > true_cost[1]
    assert base_cost[1] > base_cost[0]
    return dict(n=n, d=d, B=b, seed_affine_phi='208',
                kappa=str(F(d+1, d)), alpha=str(F(441, 400)),
                move_bound_exclusive=4*n*(d+1),
                global_high_degree_to_linear_ratio_exact=str(globz),
                global_high_degree_to_linear_ratio_float=float(globz),
                global_endpoint_elasticity_exact=str(elasticity),
                global_endpoint_elasticity_float=float(elasticity),
                ratio_nonmonotonicity_exact={k: str(v) for k, v in rv.items()},
                missing_global_minorant_counterexample_checked=True)


def main():
    payload = dict(status='PASS', python=sys.version,
                   seed=20261021, arithmetic='fractions.Fraction',
                   source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   integral_source_sublevel=integral_audits(),
                   one_sided_transfer=transfer_audits(),
                   boundary_and_example=boundary_and_example(),
                   scope='Finite exact checks only, not proofs of the general statements.')
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
