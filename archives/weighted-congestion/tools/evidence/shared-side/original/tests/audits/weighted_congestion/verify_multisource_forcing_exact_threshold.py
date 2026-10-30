#!/usr/bin/env python3
"""Exact author audit for v2; intentionally reuses v1 literal-resource helpers."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import random
import sys

SEED = 441079


def scalar_audit():
    checks = 0
    grid = [Q(1, 100), Q(1, 7), Q(1, 2), Q(1), Q(2), Q(7)]
    for d in range(2, 11):
        for tau in (Q(1), Q(1001, 1000), Q(2), Q(17)):
            for n in range(1, 4):
                for ts in product(grid, repeat=n):
                    T = sum(ts, Q(0))
                    for degree in range(d + 1):
                        left = sum((min(d*t, t+1)*((1+t)**degree-tau*T**degree) for t in ts), Q(0))
                        increment = (1+T)**degree-1
                        assert left <= d*increment, (d, tau, ts, degree)
                        checks += 1
    # Non-unit u, empty source and arbitrary mixed polynomial coefficients.
    rng = random.Random(SEED)
    mixed = 0
    for _ in range(400):
        d = rng.randint(2, 13)
        tau = Q(rng.randint(1, 33), rng.randint(1, 9))
        tau = max(Q(1), tau)
        u = Q(rng.randint(1, 8), rng.randint(1, 9))
        ts = [Q(rng.randint(1, 11), rng.randint(1, 23)) for _ in range(rng.randint(0, 6))]
        T = sum(ts, Q(0))
        coefficients = [Q(rng.randint(0, 3), rng.randint(1, 7)) for _ in range(d+1)]
        F = lambda x: sum((c*x**k for k, c in enumerate(coefficients)), Q(0))
        left = sum((min(d*t, t+1)*(F(u*(1+t))-tau*F(u*T)) for t in ts), Q(0))
        assert left <= d*(F(u*(1+T))-F(u))
        mixed += 1
    return {'monomial_checks': checks, 'mixed_polynomial_checks': mixed}


def audit(case, helper):
    d, tau, alpha, n, u = (case[k] for k in ('d', 'tau', 'alpha', 'hubs', 'u'))
    assert d >= 2 and tau > 1 and alpha >= 1 and alpha*(tau-1) >= d
    assert all(record['slack'] >= 0 for record in helper.forcing_data(case, tau))
    costs, E = helper.literal_game(case)
    lights, sides, F = case['lights'], case['sides'], case['F']
    result = {'anti_states': 0, 'reset_checks': 0, 'local_minima': 0, 'player_checks': 0,
              'exact_PNE': alpha == 1, 'outside_v1_parameter_domain': (tau-1)*(alpha-1) < d,
              'r_le_one': Q(d)/(tau-1) <= 1,
              'cross_source_multilight_side': any(len({lights[l]['source'] for l in side['L']}) >= 2 for side in sides),
              'positive_side_cost': any(any(coefficient > 0 for coefficient in side['G']) and side['H'] and side['L'] for side in sides)}
    for h in product((0, 1), repeat=n):
        def anti(hub_bits):
            return list(hub_bits) + [1-hub_bits[light['source']] for light in lights]
        state = anti(h)
        eold, current = E(state), costs(state)
        local = True
        for v in range(n):
            hp = list(h)
            hp[v] ^= 1
            reset = anti(hp)
            actual = state.copy()
            actual[v] ^= 1
            moved = costs(actual)
            W = sum((light['w'] for light in lights if light['source'] == v), Q(0))
            main_old = helper.polynomial(F[v], u)
            main_new = helper.polynomial(F[v], u+W)
            assert current[v]-main_old-(moved[v]-main_new) == eold-E(actual)
            reset_bound, source_sum = Q(0), Q(0)
            for l, light in enumerate(lights):
                if light['source'] != v:
                    continue
                w = light['w']
                light_side_total = Q(0)
                for side in sides:
                    if l in side['L']:
                        Y = sum((lights[k]['w'] for k in side['L']), Q(0))+len(side['H'])*u
                        light_side_total += helper.polynomial(side['G'], Y)
                kap = min(d*w/u, w/u+1)
                reset_bound += kap*light_side_total
                source_sum += kap*(helper.polynomial(F[v], u+w)-tau*helper.polynomial(F[v], W))
            delta = main_new-main_old
            r = Q(d)/(tau-1)
            main_budget = alpha*main_new-main_old
            assert E(reset)-E(actual) <= reset_bound
            assert reset_bound <= source_sum/(tau-1)
            assert source_sum <= d*delta
            assert reset_bound <= r*delta <= alpha*delta <= main_budget
            if r <= 1:
                assert r*delta <= delta <= main_budget
            else:
                assert main_budget-r*delta == (alpha-r)*main_new+(r-1)*main_old >= 0
            result['reset_checks'] += 1
            if E(reset) < eold:
                local = False
        result['anti_states'] += 1
        if local:
            result['local_minima'] += 1
            for player, before in enumerate(current):
                actual = state.copy()
                actual[player] ^= 1
                after = costs(actual)[player]
                assert before <= alpha*after
                if player >= n:
                    assert tau*before <= after
                result['player_checks'] += 1
    assert result['local_minima'] > 0
    return result


def explicit_exact(d, tau, name):
    # Two nonempty sources feed a genuinely shared nonlinear side.
    w = Q(1, 10*d)
    Y = 2+2*w
    main_coefficient = (tau*Y**d-w**d)/((1+w)**d-tau*w**d)
    assert main_coefficient > 0
    return {'name': name, 'd': d, 'tau': tau, 'alpha': Q(1), 'hubs': 2, 'u': Q(1),
            'lights': [{'source': v, 'w': w} for v in (0, 1)],
            'F': [[Q(0)]*d+[main_coefficient] for _ in (0, 1)],
            'sides': [{'H': [0, 1], 'L': [0, 1], 'G': [Q(0)]*d+[Q(1)]}]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--helper', type=Path, default=Path(__file__).with_name('verify_multisource_forcing_target_tradeoff.py'),
                        help='exact v1 author helper file; default is adjacent frozen source')
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('v1_author_resource_helper', args.helper)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    helper.rng.seed(SEED)
    scalar = scalar_audit()
    cases = []
    for d, tau in [(2, Q(3, 2)), (2, Q(2)), (2, Q(3)), (2, Q(7)),
                   (4, Q(2)), (4, Q(3)), (4, Q(5)), (4, Q(9)), (4, Q(1001, 1000)),
                   (6, Q(3)), (9, Q(4)), (9, Q(10)), (9, Q(31)), (16, Q(17))]:
        alpha = max(Q(1), Q(d)/(tau-1))
        for index in range(12):
            cases.append(helper.generate(d, tau, alpha, index))
    cases.append(explicit_exact(4, Q(5), 'exact-threshold-tau-d-plus-one'))
    cases.append(explicit_exact(4, Q(13), 'strict-large-tau-exact-multisource'))
    cases.append({'name': 'exact-no-lights-zero-and-constant', 'd': 3, 'tau': Q(4), 'alpha': Q(1),
                  'hubs': 2, 'u': Q(3, 2), 'lights': [], 'F': [[Q(0)], [Q(7)]],
                  'sides': [{'H': [0, 1], 'L': [], 'G': [Q(3)]},
                            {'H': [], 'L': [], 'G': [Q(11)]}]})
    cases.append({'name': 'exact-zero-fees-large-light-weights', 'd': 2, 'tau': Q(9), 'alpha': Q(1),
                  'hubs': 2, 'u': Q(2, 7),
                  'lights': [{'source': 0, 'w': Q(100)}, {'source': 1, 'w': Q(3)}],
                  'F': [[Q(0)], [Q(0)]],
                  'sides': [{'H': [0, 1], 'L': [0, 1], 'G': [Q(0)]},
                            {'H': [], 'L': [0], 'G': [Q(0)]}]})
    records = [{'parameters': helper.serial(case), 'checks': audit(case, helper)} for case in cases]
    for name in ('exact-threshold-tau-d-plus-one', 'strict-large-tau-exact-multisource'):
        record = next(row for row in records if row['parameters']['name'] == name)
        assert record['checks']['exact_PNE'] and record['checks']['positive_side_cost']
        assert record['checks']['cross_source_multilight_side'] and record['checks']['outside_v1_parameter_domain']
    summary = {key: sum(row['checks'][key] for row in records)
               for key in ('anti_states', 'reset_checks', 'local_minima', 'player_checks')}
    summary.update(scalar)
    summary.update({'games': len(cases), 'exact_PNE_games': sum(row['checks']['exact_PNE'] for row in records),
                    'outside_v1_parameter_domain_games': sum(row['checks']['outside_v1_parameter_domain'] for row in records),
                    'r_le_one_games': sum(row['checks']['r_le_one'] for row in records),
                    'r_gt_one_games': sum(not row['checks']['r_le_one'] for row in records)})
    print(json.dumps({'audit': 'v2 main-increment forcing exact-threshold author Fraction audit',
                      'claim': 'WC-MULTISOURCE-FORCING-TARGET-TRADEOFF-v2', 'scope': 'finite evidence only',
                      'command': 'python3 tests/audits/weighted_congestion/verify_multisource_forcing_exact_threshold.py',
                      'python': sys.version, 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      'dependency': {'path': 'tests/audits/weighted_congestion/verify_multisource_forcing_target_tradeoff.py',
                                     'sha256': hashlib.sha256(args.helper.read_bytes()).hexdigest(),
                                     'functions': ['polynomial', 'serial', 'literal_game', 'forcing_data', 'generate'],
                                     'status': 'v1 author helper reuse; this is not the independent audit'},
                      'seed': SEED, 'generation': 'random.Random; all inputs below; exact FT2 boundary including alpha1; monomial grid and mixed-polynomial source tests; literal costs and source-reset comparison',
                      'summary': summary, 'cases': records}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
