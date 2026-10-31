"""Finite, separately invoked audits.  No brute routine is called by the core."""
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import degree_two_weighted_menu_backend as b


def state(name, *incidences):
    return {'id': name, 'incidences': [{'resource': r, 'p': str(p)} for r, p in incidences]}


def group(name, *states):
    return {'id': name, 'states': list(states)}


FIXTURES = {
    # Committing the shared heavy item to flexible first group would starve g1.
    'joint_bad_heavy_yes': {
        'resources': ['h', 'x', 'y'],
        'groups': [group('g0', state('heavy', ('h', 1)),
                         state('diffuse', ('x', F(1, 2)), ('y', F(1, 2)))),
                   group('g1', state('only_heavy', ('h', 1)))],
    },
    'near_two_single_state_no': {
        'resources': ['h', 'a', 'b'],
        'groups': [group('g0', state('only', ('h', F(16, 17)), ('a', F(1, 17)))),
                   group('g1', state('only', ('h', F(16, 17)), ('b', F(1, 17))))],
    },
    'zero_work_empty_and_duplicate_states': {
        'resources': ['zero', 'unused'],
        'groups': [group('g0', state('empty'), state('zero', ('zero', 0)), state('empty_copy')),
                   group('g1', state('zero', ('zero', 0)))],
    },
    'rational_unequal_menus_and_bonuses': {
        'resources': ['h', 'x', 'a', 'b'],
        'groups': [group('g0', state('s0', ('h', F(1, 3)), ('a', F(1, 6))),
                         state('s1', ('x', F(2, 5))), state('s2', ('h', F(1, 11)))),
                   group('g1', state('s0', ('h', F(2, 7)), ('b', F(1, 7))),
                         state('s1', ('x', F(3, 8))))],
    },
    'aux_opt_zero_fallback': {
        'resources': ['h'],
        'groups': [group('g0', state('only', ('h', 1))),
                   group('g1', state('only', ('h', 1)))],
    },
}


def brute_actual_opt(payload, limit=100000):
    """Independent complete original-job assignment enumeration, audit only."""
    inst = b.parse(payload)
    table = b.original_jobs(inst)
    jobs = list(table)
    choices = [list(table[j]) for j in jobs]
    count = 1
    for x in choices:
        count *= len(x)
    if count > limit:
        raise ValueError('finite audit enumeration limit exceeded')
    best = None
    for assignment in product(*choices):
        loads = {}
        for job, machine in zip(jobs, assignment):
            loads[machine] = loads.get(machine, F(0)) + table[job][machine]
        peak = max(loads.values(), default=F(0))
        if best is None or peak < best:
            best = peak
    return best, count


def normalized_payload(payload):
    result = deepcopy(payload)
    used = set(result['resources'])
    for gi, group in enumerate(result['groups']):
        for si, state in enumerate(group['states']):
            W = sum((F(x['p']) for x in state['incidences']), F(0))
            if W < 1:
                r = '__audit_bonus_%d_%d' % (gi, si)
                while r in used:
                    r += '_'
                used.add(r)
                result['resources'].append(r)
                state['incidences'].append({'resource': r, 'p': str(1 - W)})
    return result


def brute_additive(items, agents):
    best = F(0)
    for owners in product(*(tuple(g for g, _ in e) for _, e in items)):
        utility = [F(0)] * agents
        for (_, e), g in zip(items, owners):
            utility[g] += dict(e)[g]
        best = max(best, min(utility))
    return best


def brute_xos(states, items, agents):
    best = F(0)
    # Unassigned is explicit here; this is a separate finite XOS audit.
    choices = [tuple([None] + [g for g, _ in e]) for _, e in items]
    for owners in product(*choices):
        alloc = {key: g for (key, _), g in zip(items, owners) if g is not None}
        utilities = [max(sum((p for key, p in s.items() if alloc.get(key) == g), F(0))
                         for s in states[g]) for g in range(agents)]
        best = max(best, min(utilities))
    return best


def small_raw_backend_checks():
    cases = [
        ('pairing_even_cycle', 3, [
            ('a', ((0, F(1)), (1, F(1)))),
            ('b', ((1, F(1)), (2, F(1)))),
            ('c', ((0, F(1)), (2, F(1)))),
        ]),
        # T=2 can succeed with value 1 although the true integral OPT is 1.
        ('weak_success_above_opt', 4, [
            (str((i, j)), ((i, F(1)), (j, F(1))))
            for i in range(4) for j in range(i + 1, 4)
        ]),
        ('forced_asymmetric', 3, [
            ('a', ((0, F(9)), (1, F(1)))),
            ('b', ((1, F(8)), (2, F(2)))),
            ('c', ((2, F(7)),)),
            ('d', ((0, F(1)), (2, F(1)))),
            ('e', ((1, F(1)),)),
        ]),
        ('rational_values', 2, [
            ('a', ((0, F(1, 3)), (1, F(2, 5)))),
            ('b', ((0, F(1, 7)),)),
            ('c', ((1, F(3, 11)),)),
        ]),
        ('zero_opt', 2, [('a', ((0, F(1)), (1, F(1))))]),
        ('no_positive_items', 2, []),
    ]
    results = []
    for name, agents, items in cases:
        optimum = brute_additive(items, agents)
        answer = b.vw_two_approx(items, agents)
        value = F(min(answer['utility']), answer['scale'])
        assert 2 * value >= optimum
        assert F(answer['low'], answer['scale']) >= optimum
        assert F(answer['high'], answer['scale']) > optimum
        if name == 'weak_success_above_opt':
            assert optimum == value == 1 and answer['low'] == 2
        for T in range(1, 1 + min(12, int(min(
                sum((dict(e).get(g, F(0)) for _, e in items), F(0))
                for g in range(agents))))):
            endpoints = [tuple((g, v.numerator * (answer['scale'] // v.denominator))
                               for g, v in e) for _, e in items]
            result = b.vw_threshold(endpoints, agents, T)
            if result['success']:
                assert 2 * min(result['utility']) >= T
            else:
                assert optimum * answer['scale'] < T
        results.append({'name': name, 'OPT': str(optimum), 'returned': str(value),
                        'oracle_calls': len(answer['calls'])})
    # One meaningful size probe: an alternating cycle beyond Python stack depth.
    agents = 1200
    items = [(str(i), tuple(sorted(((i, F(1)), ((i + 1) % agents, F(1))))))
             for i in range(agents)]
    answer = b.vw_two_approx(items, agents)
    assert min(answer['utility']) == 1 and len(answer['owner']) == agents
    results.append({'name': 'iterative_1200_agent_cycle', 'returned': '1',
                    'oracle_calls': len(answer['calls']), 'brute_used': False})
    return results


def rejection_checks():
    bad = []
    empty = {'resources': [], 'groups': []}
    bad.append(('empty_groups_outside_exact', empty))
    bad.append(('degree_three_even_with_zero_weights', {
        'resources': ['r'], 'groups': [group(str(i), state('s', ('r', 0))) for i in range(3)]}))
    bad.append(('private_sum_above_one', {
        'resources': ['r'], 'groups': [group('g', state('s', ('r', F(3, 2))))]}))
    bad.append(('duplicate_within_state', {
        'resources': ['r'], 'groups': [group('g', state('s', ('r', 0), ('r', 0)))]}))
    bad.append(('inexact_float', {
        'resources': ['r'], 'groups': [{'id': 'g', 'states': [
            {'id': 's', 'incidences': [{'resource': 'r', 'p': 0.1}]}]}]}))
    bad.append(('succinct_exponent_shorthand', {
        'resources': ['r'], 'groups': [{'id': 'g', 'states': [
            {'id': 's', 'incidences': [{'resource': 'r', 'p': '1e-1000000000'}]}]}]}))
    for name, payload in bad:
        try:
            b.solve(payload)
        except ValueError:
            continue
        raise AssertionError('invalid input accepted: ' + name)
    return [name for name, _ in bad]


def main():
    outputs, rows = {}, []
    for name, payload in FIXTURES.items():
        inst = b.parse(payload)
        answer = b.solve(payload)
        assert b.verify(inst, answer)
        optimum, actual_count = brute_actual_opt(payload)
        norm_opt, norm_count = brute_actual_opt(normalized_payload(payload))
        assert optimum == norm_opt
        states, _, items = b.normalized_auxiliary(inst)
        A = brute_additive(items, len(inst.groups))
        V = brute_xos(states, items, len(inst.groups))
        assert norm_opt == 2 - V
        K = answer['K']
        assert A >= V / K
        utility = min(F(x) for x in answer['aux_utility'])
        assert 2 * utility >= A
        C = F(answer['makespan'])
        assert C <= 2 - (2 - optimum) / (2 * K)
        assert C <= (2 - F(1, 2 * K)) * optimum
        assert F(answer['backend']['successful_T']) / F(answer['backend']['integer_scale']) >= A
        assert F(answer['backend']['rejected_T']) / F(answer['backend']['integer_scale']) > A
        if name == 'joint_bad_heavy_yes':
            assert C == optimum == 1
            assert answer['chosen_states'][0]['state'] == 'diffuse'
        if name == 'near_two_single_state_no':
            assert optimum == F(33, 17) and C > F(3, 2)
        if name == 'aux_opt_zero_fallback':
            assert A == 0 and answer['backend']['successful_T'] == '0' and C == 2
        rows.append({'name': name, 'OPT_original': str(optimum), 'OPT_normalized': str(norm_opt),
                     'V': str(V), 'A': str(A), 'aux_returned_min': str(utility),
                     'makespan': str(C), 'K': K, 'original_assignments_enumerated': actual_count,
                     'normalized_assignments_enumerated': norm_count,
                     'original_jobs_output': len(answer['jobs'])})
        outputs[name] = answer
    report = {'result': 'all listed finite audits passed', 'weighted_menu_cases': rows,
              'raw_backend_cases': small_raw_backend_checks(),
              'invalid_inputs_rejected': rejection_checks(),
              'scope': 'explicit degree-two group resources, W<=1, no general UM claim',
              'brute_scope': 'audit module only; core solve/vw routines never call brute'}
    root = Path(__file__).resolve().parent
    (root / 'weighted_menu_backend_audit_results.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    (root / 'weighted_menu_backend_fixture_outputs.json').write_text(
        json.dumps(outputs, ensure_ascii=False, indent=2) + '\n')
    (root / 'weighted_menu_backend_fixtures.json').write_text(
        json.dumps(FIXTURES, ensure_ascii=False, indent=2) + '\n')
    (root / 'weighted_menu_joint_bad_heavy_input.json').write_text(
        json.dumps(FIXTURES['joint_bad_heavy_yes'], ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
