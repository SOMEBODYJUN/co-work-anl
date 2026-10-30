#!/usr/bin/env python3
"""Fraction author audit of forcing/target tradeoff; finite evidence, no imports from old audits."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import sys

SEED = 441073
rng = random.Random(SEED)


def polynomial(coefficients, x):
    value = Q(0)
    for coefficient in reversed(coefficients):
        value = value * x + coefficient
    return value


def serial(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def kappa(d, t):
    return min(d * t, t + 1)


def literal_game(case):
    n, u = case['hubs'], case['u']
    lights, sides, F = case['lights'], case['sides'], case['F']
    weights = [u] * n + [light['w'] for light in lights]
    latency, strategies = {}, []
    for v in range(n):
        for bit in (0, 1):
            latency[('A', v, bit)] = F[v]
    for j, side in enumerate(sides):
        for bit in (0, 1):
            latency[('B', j, bit)] = side['G']
    for v in range(n):
        strategies.append([
            {('A', v, bit)} | {('B', j, bit) for j, side in enumerate(sides) if v in side['H']}
            for bit in (0, 1)
        ])
    for l, light in enumerate(lights):
        strategies.append([
            {('A', light['source'], bit)} | {('B', j, 1 - bit) for j, side in enumerate(sides) if l in side['L']}
            for bit in (0, 1)
        ])

    def load(state):
        output = {resource: Q(0) for resource in latency}
        for player, bit in enumerate(state):
            for resource in strategies[player][bit]:
                output[resource] += weights[player]
        return output

    def costs(state):
        loads = load(state)
        return [sum((polynomial(latency[e], loads[e]) for e in strategies[p][state[p]]), Q(0))
                for p in range(len(weights))]

    def potential(state):
        loads = load(state)
        answer = Q(0)
        for j, side in enumerate(sides):
            for bit in (0, 1):
                e = ('B', j, bit)
                count = sum(e in strategies[v][state[v]] for v in range(n))
                exterior = loads[e] - count * u
                answer += sum((polynomial(side['G'], exterior + rank * u)
                               for rank in range(1, count + 1)), Q(0))
        return answer

    return costs, potential


def forcing_data(case, factor):
    lights, sides, F, u = case['lights'], case['sides'], case['F'], case['u']
    records = []
    for l, light in enumerate(lights):
        v, w = light['source'], light['w']
        W = sum((other['w'] for other in lights if other['source'] == v), Q(0))
        good = polynomial(F[v], u + w)
        bad = polynomial(F[v], W)
        for side in sides:
            if l in side['L']:
                T = sum((lights[k]['w'] for k in side['L']), Q(0))
                good += polynomial(side['G'], w)
                bad += polynomial(side['G'], T + len(side['H']) * u)
        records.append({'light': l, 'good': good, 'bad': bad, 'slack': good - factor * bad})
    return records


def generate(d, tau, alpha, index):
    n = rng.randint(1, 3)
    u = Q(rng.randint(1, 4), rng.randint(1, 3))
    ceiling_tau = (tau.numerator + tau.denominator - 1) // tau.denominator
    lights = []
    for v in range(n):
        count = rng.randint(0, 2)
        for _ in range(count):
            lights.append({'source': v, 'w': u * Q(rng.randint(1, 3), 16 * d * ceiling_tau * max(1, count))})
    sides = []
    for j in range(rng.randint(0, 4)):
        if (index + j) % 5 == 0:
            G = [Q(0)] * (d + 1)
        elif (index + j) % 5 == 1:
            G = [Q(rng.randint(0, 3))] + [Q(0)] * d
        else:
            G = [Q(rng.randint(0, 2), rng.randint(1, 3)) if rng.randrange(3) == 0 else Q(0)
                 for _ in range(d + 1)]
        sides.append({'H': [v for v in range(n) if rng.randrange(2)],
                      'L': [l for l in range(len(lights)) if rng.randrange(2)], 'G': G})
    F = []
    for v in range(n):
        local = [l for l, light in enumerate(lights) if light['source'] == v]
        W = sum((lights[l]['w'] for l in local), Q(0))
        if not local:
            F.append([Q(rng.randrange(3)) for _ in range(d + 1)] if index % 3 else [Q(0)])
            continue
        coefficient = Q(1)
        for l in local:
            w = lights[l]['w']
            need = Q(0)
            for side in sides:
                if l in side['L']:
                    Y = sum((lights[k]['w'] for k in side['L']), Q(0)) + len(side['H']) * u
                    need += tau * polynomial(side['G'], Y) - polynomial(side['G'], w)
            denominator = (u + w) ** d - tau * W ** d
            assert denominator > 0
            coefficient = max(coefficient, need / denominator)
        F.append([Q(0)] * d + [coefficient])
    return {'name': f'random-{d}-{tau}-{alpha}-{index}', 'd': d, 'tau': tau, 'alpha': alpha,
            'hubs': n, 'u': u, 'lights': lights, 'sides': sides, 'F': F}


def audit(case):
    d, tau, alpha, n, u = (case[k] for k in ('d', 'tau', 'alpha', 'hubs', 'u'))
    assert d >= 2 and tau > 1 and alpha >= 1
    assert (tau - 1) * (alpha - 1) >= d
    assert all(record['slack'] >= 0 for record in forcing_data(case, tau))
    costs, E = literal_game(case)
    lights, sides, F = case['lights'], case['sides'], case['F']
    result = {'anti_states': 0, 'hub_reset_checks': 0, 'local_minima': 0, 'player_PNE_checks': 0,
              'fails_UFalpha': any(record['slack'] < 0 for record in forcing_data(case, alpha))}
    for hub_bits in product((0, 1), repeat=n):
        def anti(bits):
            return list(bits) + [1 - bits[light['source']] for light in lights]
        state = anti(hub_bits)
        current = costs(state)
        eold = E(state)
        local_minimum = True
        for v in range(n):
            moved_hubs = list(hub_bits)
            moved_hubs[v] ^= 1
            reset = anti(moved_hubs)
            actual = state.copy()
            actual[v] ^= 1
            new_cost = costs(actual)
            W = sum((light['w'] for light in lights if light['source'] == v), Q(0))
            side_before = current[v] - polynomial(F[v], u)
            side_after = new_cost[v] - polynomial(F[v], u + W)
            assert side_before - side_after == eold - E(actual)
            reset_bound = Q(0)
            source_scalar = Q(0)
            for l, light in enumerate(lights):
                if light['source'] != v:
                    continue
                w = light['w']
                side_total = Q(0)
                for side in sides:
                    if l in side['L']:
                        Y = sum((lights[k]['w'] for k in side['L']), Q(0)) + len(side['H']) * u
                        side_total += polynomial(side['G'], Y)
                reset_bound += kappa(d, w / u) * side_total
                source_scalar += kappa(d, w / u) * (polynomial(F[v], u + w) - tau * polynomial(F[v], W))
            large = polynomial(F[v], u + W)
            budget = alpha * large - polynomial(F[v], u)
            assert E(reset) - E(actual) <= reset_bound
            assert reset_bound <= source_scalar / (tau - 1)
            assert source_scalar <= d * large
            assert d * large / (tau - 1) <= (alpha - 1) * large <= budget
            assert reset_bound <= budget
            result['hub_reset_checks'] += 1
            if E(reset) < eold:
                local_minimum = False
        result['anti_states'] += 1
        if local_minimum:
            result['local_minima'] += 1
            for player in range(len(state)):
                actual = state.copy()
                actual[player] ^= 1
                after = costs(actual)[player]
                assert current[player] <= alpha * after
                if player >= n:
                    assert tau * current[player] <= after
                result['player_PNE_checks'] += 1
    assert result['local_minima'] > 0
    return result


def scalar_audit():
    checks = 0
    for d in (2, 3, 4, 7, 12):
        for tau in (Q(1), Q(101, 100), Q(3, 2), Q(3), Q(19)):
            for _ in range(32):
                values = [Q(rng.randint(1, 15), rng.randint(1, 19)) for _ in range(rng.randint(0, 5))]
                T = sum(values, Q(0))
                u = Q(rng.randint(1, 4), rng.randint(1, 5))
                for degree in range(d + 1):
                    lhs = sum((kappa(d, t) * ((u * (1 + t)) ** degree - tau * (u * T) ** degree)
                               for t in values), Q(0))
                    rhs = d * (u * (1 + T)) ** degree
                    assert lhs <= rhs, (d, tau, values, degree)
                    # Reverse-substitution check of the normalized monomial identity.
                    normal = sum((kappa(d, t) * ((1 + t) ** degree - tau * T ** degree)
                                  for t in values), Q(0))
                    assert lhs == u ** degree * normal
                    checks += 1
    return checks


def main():
    scalar_checks = scalar_audit()
    cases = []
    settings = [(2, Q(3, 2)), (4, Q(2)), (4, Q(3)), (4, Q(9)),
                (4, Q(1001, 1000)), (9, Q(4)), (9, Q(31))]
    for d, tau in settings:
        alpha = 1 + Q(d, 1) / (tau - 1)
        for index in range(10):
            cases.append(generate(d, tau, alpha, index))
    # Equality UFtau with a side genuinely shared by multiple sources; UFalpha fails strictly.
    d, tau, alpha, w = 4, Q(2), Q(5), Q(1, 10)
    G = [Q(0)] * d + [Q(1)]
    coefficient = (tau * (2 + 2 * w) ** d - w ** d) / ((1 + w) ** d - tau * w ** d)
    cases.append({'name': 'strictly-weaker-UFtau-multisource', 'd': d, 'tau': tau, 'alpha': alpha,
                  'hubs': 2, 'u': Q(1), 'lights': [{'source': v, 'w': w} for v in (0, 1)],
                  'sides': [{'H': [0, 1], 'L': [0, 1], 'G': G}],
                  'F': [[Q(0)] * d + [coefficient] for _ in (0, 1)]})
    cases.append({'name': 'no-lights-constant-zero-empty-subsets', 'd': 2, 'tau': Q(2), 'alpha': Q(3),
                  'hubs': 2, 'u': Q(3, 2), 'lights': [], 'F': [[Q(0)], [Q(4)]],
                  'sides': [{'H': [0, 1], 'L': [], 'G': [Q(7)]},
                            {'H': [], 'L': [], 'G': [Q(5)]}]})
    cases.append({'name': 'zero-costs-large-weights-cross-source', 'd': 3, 'tau': Q(4), 'alpha': Q(2),
                  'hubs': 2, 'u': Q(2, 3),
                  'lights': [{'source': 0, 'w': Q(100)}, {'source': 1, 'w': Q(7, 3)}],
                  'F': [[Q(0)], [Q(0)]],
                  'sides': [{'H': [0, 1], 'L': [0, 1], 'G': [Q(0)]},
                            {'H': [], 'L': [0], 'G': [Q(0)]},
                            {'H': [1], 'L': [], 'G': [Q(8)]}]})
    records = [{'parameters': serial(case), 'checks': audit(case)} for case in cases]
    separated = next(record for record in records if record['parameters']['name'] == 'strictly-weaker-UFtau-multisource')
    assert separated['checks']['fails_UFalpha']
    all_orders = {'less': False, 'equal': False, 'greater': False}
    for case in cases:
        order = 'less' if case['tau'] < case['alpha'] else ('equal' if case['tau'] == case['alpha'] else 'greater')
        all_orders[order] = True
    assert all(all_orders.values())
    summary = {key: sum(record['checks'][key] for record in records)
               for key in ('anti_states', 'hub_reset_checks', 'local_minima', 'player_PNE_checks')}
    summary.update({'games': len(cases), 'scalar_monomial_checks': scalar_checks,
                    'UFalpha_failure_games': sum(record['checks']['fails_UFalpha'] for record in records),
                    'tau_alpha_orders': all_orders})
    print(json.dumps({'audit': 'forcing-target product budget author Fraction audit',
                      'claim': 'WC-MULTISOURCE-FORCING-TARGET-TRADEOFF-v1',
                      'scope': 'finite exact evidence only; general real-parameter proof is section 9',
                      'command': 'python3 tests/audits/weighted_congestion/verify_multisource_forcing_target_tradeoff.py',
                      'python': sys.version, 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      'seed': SEED, 'generation': 'random.Random; all parameters recorded; rational product boundary equality; main monomials scaled from exact UFtau slack; literal resource reconstruction; scalar tests do not assume individual source brackets nonnegative',
                      'summary': summary, 'cases': records}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
