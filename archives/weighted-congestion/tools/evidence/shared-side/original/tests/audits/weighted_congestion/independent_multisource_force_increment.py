#!/usr/bin/env python3
"""Independent exact audit of increment source budgets and the alpha=1 boundary.

No author modules are imported. This is finite evidence, not a universal proof.
All generated games use the established literal-resource schema, and every
one-player deviation is evaluated after rebuilding actual resource loads.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import sys

SEED = 1197043
RNG = random.Random(SEED)


def poly(coeffs, load):
    value = Q(0)
    for coefficient in reversed(coeffs):
        value = value * load + coefficient
    return value


def encode(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def kappa(d, t):
    return min(d * t, t + 1)


def scalar_audit():
    checks = 0
    values = [Q(1, 8), Q(1, 2), Q(1), Q(3, 2)]
    for d in (2, 3, 4, 7):
        for count in range(4):
            for ts in product(values, repeat=count):
                T = sum(ts, Q(0))
                for tau in (Q(1), Q(11, 10), Q(3, 2), Q(2), Q(5), Q(21)):
                    alpha = Q(d) / (tau - 1) if tau > 1 else Q(1)
                    for degree in range(d + 1):
                        lhs = sum((kappa(d, t) * ((1 + t) ** degree - tau * T ** degree) for t in ts), Q(0))
                        top = (1 + T) ** degree
                        margin = alpha * top - 1
                        assert lhs <= d * (top - 1)
                        if tau > 1 and alpha >= 1:
                            assert lhs <= (tau - 1) * margin
                        checks += 1
    for d in (2, 3, 4):
        assert Q(100) * (Q(1) - 1) < d
        assert Q(1) * (Q(d + 1) - 1) == d
    return checks


def literal_engine(case):
    n = case['hubs']
    u, lights, sides, main = case['u'], case['lights'], case['sides'], case['F']
    weights = [u] * n + [light['w'] for light in lights]
    resources = {('A', v, b): main[v] for v in range(n) for b in (0, 1)}
    resources.update({('B', j, b): side['G'] for j, side in enumerate(sides) for b in (0, 1)})
    actions = []
    for v in range(n):
        actions.append([{('A', v, b)} | {('B', j, b) for j, side in enumerate(sides) if v in side['H']} for b in (0, 1)])
    for l, light in enumerate(lights):
        actions.append([{('A', light['source'], b)} | {('B', j, 1-b) for j, side in enumerate(sides) if l in side['L']} for b in (0, 1)])

    def costs(state):
        loads = {resource: Q(0) for resource in resources}
        for player, bit in enumerate(state):
            for resource in actions[player][bit]:
                loads[resource] += weights[player]
        result = [sum((poly(resources[e], loads[e]) for e in actions[player][bit]), Q(0)) for player, bit in enumerate(state)]
        potential = Q(0)
        for j, side in enumerate(sides):
            for bit in (0, 1):
                resource = ('B', j, bit)
                count = sum(resource in actions[v][state[v]] for v in range(n))
                background = loads[resource] - count * u
                potential += sum((poly(side['G'], background + r * u) for r in range(1, count + 1)), Q(0))
        return result, potential
    return costs


def random_game(d, tau, alpha, index):
    n = RNG.randint(1, 4)
    u = Q(RNG.randint(1, 4), RNG.randint(1, 3))
    lights = []
    for v in range(n):
        count = RNG.randint(0, 2)
        for _ in range(count):
            lights.append({'source': v, 'w': u * Q(RNG.randint(1, 3), 32 * d * max(1, count)) / tau})
    sides = []
    for j in range(RNG.randint(0, 5)):
        kind = (index + j) % 5
        if kind == 0:
            coefficients = [Q(0)]
        elif kind == 1:
            coefficients = [Q(RNG.randint(1, 3))]
        else:
            coefficients = [Q(RNG.randint(0, 3), RNG.randint(1, 3)) for _ in range(d + 1)]
        sides.append({'H': [v for v in range(n) if RNG.choice((0, 1))], 'L': [l for l in range(len(lights)) if RNG.choice((0, 1))], 'G': coefficients})
    main = []
    for v in range(n):
        members = [l for l, light in enumerate(lights) if light['source'] == v]
        W = sum((lights[l]['w'] for l in members), Q(0))
        if not members:
            main.append([Q((index + v) % 3)])
            continue
        coefficient = Q(1)
        constant = Q((index + v) % 3)
        for l in members:
            w = lights[l]['w']
            budget = Q(0)
            for side in sides:
                if l in side['L']:
                    T = sum((lights[k]['w'] for k in side['L']), Q(0))
                    budget += tau * poly(side['G'], T + len(side['H']) * u) - poly(side['G'], w)
            denominator = (u + w) ** d - tau * W ** d
            assert denominator > 0
            coefficient = max(coefficient, (budget + (tau - 1) * constant) / denominator)
        main.append([constant] + [Q(0)] * (d - 1) + [coefficient])
    return {'name': f'random-d{d}-tau{tau}-alpha{alpha}-{index}', 'd': d, 'tau': tau, 'alpha': alpha, 'hubs': n, 'u': u, 'lights': lights, 'sides': sides, 'F': main}


def check_game(case):
    n, u = case['hubs'], case['u']
    d, tau, alpha = case['d'], case['tau'], case['alpha']
    lights, sides, main = case['lights'], case['sides'], case['F']
    assert d >= 2 and tau > 1 and alpha >= 1
    assert alpha * (tau - 1) >= d
    source_W = [sum((light['w'] for light in lights if light['source'] == v), Q(0)) for v in range(n)]
    top_side = [poly(side['G'], sum((lights[l]['w'] for l in side['L']), Q(0)) + len(side['H']) * u) for side in sides]
    R = [Q(0)] * n
    source_sum = [Q(0)] * n
    for l, light in enumerate(lights):
        v, w = light['source'], light['w']
        old_side = sum((top_side[j] for j, side in enumerate(sides) if l in side['L']), Q(0))
        lower_side = sum((poly(side['G'], w) for side in sides if l in side['L']), Q(0))
        main_slack = poly(main[v], u + w) - tau * poly(main[v], source_W[v])
        assert main_slack >= tau * old_side - lower_side
        weight = kappa(d, w / u)
        R[v] += weight * old_side
        source_sum[v] += weight * main_slack
    for v in range(n):
        top = poly(main[v], u + source_W[v])
        margin = alpha * top - poly(main[v], u)
        assert R[v] * (tau - 1) <= source_sum[v]
        increment = top - poly(main[v], u)
        assert source_sum[v] <= d * increment
        assert d * increment <= (tau - 1) * margin
        assert R[v] <= margin
    costs = literal_engine(case)
    def anti(bits):
        return tuple(bits) + tuple(1 - bits[light['source']] for light in lights)
    local_minima = literal_checks = reset_checks = 0
    for bits in product((0, 1), repeat=n):
        state = anti(bits)
        current, E = costs(state)
        is_local = True
        for v in range(n):
            moved = list(state)
            moved[v] ^= 1
            after, E_fixed = costs(moved)
            new_bits = list(bits)
            new_bits[v] ^= 1
            _, E_reset = costs(anti(new_bits))
            side_old = current[v] - poly(main[v], u)
            side_new = after[v] - poly(main[v], u + source_W[v])
            assert E - E_fixed == side_old - side_new
            assert E_reset - E_fixed <= R[v]
            if E_reset < E:
                is_local = False
            reset_checks += 1
        if is_local:
            local_minima += 1
            for player in range(len(state)):
                moved = list(state)
                moved[player] ^= 1
                after, _ = costs(moved)
                assert current[player] <= alpha * after[player]
                if player >= n:
                    assert tau * current[player] <= after[player]
                literal_checks += 1
    assert local_minima > 0
    return {'anti_states': 2 ** n, 'local_minima': local_minima, 'literal_player_checks': literal_checks, 'reset_checks': reset_checks}


def main_audit():
    parameter_pairs = [(2, Q(2), Q(2)), (2, Q(3), Q(1)), (3, Q(4), Q(1)), (4, Q(5), Q(1)), (9, Q(10), Q(1)), (2, Q(4), Q(1)), (4, Q(6), Q(1)), (2, Q(11, 10), Q(20)), (2, Q(21, 10), Q(20, 11)), (3, Q(5, 2), Q(2)), (4, Q(4), Q(4, 3)), (6, Q(3), Q(3)), (12, Q(4), Q(4))]
    cases = [random_game(d, tau, alpha, i) for d, tau, alpha in parameter_pairs for i in range(8)]
    cases += [
        {'name': 'zero-empty', 'd': 2, 'tau': Q(3), 'alpha': Q(1), 'hubs': 1, 'u': Q(1), 'lights': [], 'sides': [], 'F': [[Q(0)]]},
        {'name': 'constant-empty-lights', 'd': 2, 'tau': Q(3), 'alpha': Q(1), 'hubs': 2, 'u': Q(3, 2), 'lights': [], 'sides': [{'H': [0, 1], 'L': [], 'G': [Q(3)]}, {'H': [], 'L': [], 'G': [Q(5)]}], 'F': [[Q(2)], [Q(0)]]},
        {'name': 'zero-heavy-cross-source', 'd': 4, 'tau': Q(5), 'alpha': Q(1), 'hubs': 3, 'u': Q(2, 3), 'lights': [{'source': 0, 'w': Q(100)}, {'source': 1, 'w': Q(3, 2)}, {'source': 1, 'w': Q(3)}, {'source': 2, 'w': Q(2)}], 'sides': [{'H': [0, 2], 'L': [0, 1, 2, 3], 'G': [Q(0)]}, {'H': [], 'L': [0, 3], 'G': [Q(0)]}, {'H': [1], 'L': [], 'G': [Q(3)]}], 'F': [[Q(0)], [Q(0)], [Q(0)]]},
    ]
    records = [{'parameters': encode(case), 'checks': check_game(case)} for case in cases]
    summary = {key: sum(record['checks'][key] for record in records) for key in ('anti_states', 'local_minima', 'literal_player_checks', 'reset_checks')}
    summary.update({'games': len(cases), 'scalar_monomial_checks': scalar_audit(), 'tau_less_than_alpha_games': sum(case['tau'] < case['alpha'] for case in cases), 'tau_greater_than_alpha_games': sum(case['tau'] > case['alpha'] for case in cases), 'tau_equal_alpha_games': sum(case['tau'] == case['alpha'] for case in cases), 'exact_alpha_one_games': sum(case['alpha'] == 1 for case in cases), 'new_bound_exceeds_v1_scope_games': sum((case['alpha'] - 1) * (case['tau'] - 1) < case['d'] for case in cases)})
    def nonzero_cross_source(case):
        return any(side['H'] and any(c > 0 for c in side['G']) and len({case['lights'][l]['source'] for l in side['L']}) >= 2 for side in case['sides'])
    summary['exact_endpoint_nonzero_crosssource_games'] = sum(case['alpha'] == 1 and case['tau'] == case['d'] + 1 and nonzero_cross_source(case) for case in cases)
    summary['above_endpoint_nonzero_crosssource_games'] = sum(case['alpha'] == 1 and case['tau'] > case['d'] + 1 and nonzero_cross_source(case) for case in cases)
    assert summary['exact_endpoint_nonzero_crosssource_games'] > 0
    assert summary['above_endpoint_nonzero_crosssource_games'] > 0
    assert summary['new_bound_exceeds_v1_scope_games'] == len(cases)
    result = {'audit': 'independent increment-force Fraction audit', 'scope': 'finite exact evidence only; no author modules imported; literal resources and all one-player flips at all anti local minima', 'command': 'python3 tests/audits/weighted_congestion/independent_multisource_force_increment.py', 'python': sys.version, 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'reviewed_freeze_sha256': {'section9_8_onward': '833a5dc4a91b9a6c226bd0a6686a20d2a1b249a843f4626a06d075d3f7f96acb', 'full_manuscript': '316a9d4f64d45e948d50ae85f90212595c47e6d801bd111fdbcbfa12dc7acf52'}, 'reused_own_baseline': {'path': 'tests/audits/weighted_congestion/independent_multisource_force_tradeoff.py', 'sha256': '7f3e049b4d3f0b67d40a85a47be405b4de6a0d4a89ed04e5778d524379c0cc2b', 'relation': 'standalone code derived from the reviewers own literal-resource engine and exact UF generator; no baseline runtime import and no author functions'}, 'seed': SEED, 'generation': 'random.Random with complete parameters below; generated source main constant-plus-monomial polynomials scaled to satisfy exact UF_tau; parameter pairs at/above alpha*(tau-1)=d, including alpha=1 and both multiplier orders; all games outside the old (alpha-1)*(tau-1)>=d domain; deterministic zero/constant/empty/heavy-light boundaries; no floating arithmetic', 'summary': summary, 'cases': records}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main_audit()
