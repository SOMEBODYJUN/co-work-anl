"""New EB controls, not a replay of the missing historical candidate JSONs.

Imports the exact frozen audit() function without calling its glob-based main.
Uses only standard-library arithmetic; never calls a solver or network.
"""
from pathlib import Path
from itertools import product
from copy import deepcopy
from math import comb
import hashlib
import json
import sys


def compositions(n, p):
    if p == 1:
        yield (n,)
    else:
        for a in range(n + 1):
            for tail in compositions(n - a, p - 1):
                yield (a,) + tail


def strategy(p, m, chooser):
    rows = [{'history': list(h), 'action': chooser(h)}
            for depth in range(m) for h in product(range(p), repeat=depth)]
    actions = {tuple(x['history']): x['action'] for x in rows}
    h = ()
    while len(h) < m:
        h += (actions[h],)
    return {'actions': rows, 'terminal_counts': [h.count(a) for a in range(p)]}


def quotient_counts(m, p, d):
    pairs, marked, states = set(), set(), set()
    for total in range(m):
        for k in compositions(total, p):
            states.add(k[:d] + tuple(sorted(k[d:])))
    for c in compositions(m, p):
        for k in product(*(range(x + 1) for x in c)):
            pairs.add(tuple(zip(k[:d], c[:d])) + tuple(sorted(zip(k[d:], c[d:]))))
            for a in range(p):
                if c[a] <= k[a]:
                    continue
                marked.add(tuple((k[b], c[b], int(b == a)) for b in range(d))
                           + tuple(sorted((k[b], c[b], int(b == a)) for b in range(d, p))))
    types = 2 ** d * (p - d + 1) - 1
    binaries = len(pairs) + 2 * len(marked)
    return {'m': m, 'p': p, 'd': d, 'customer_orbits': types,
            'thresholds': len(states), 'Y': len(pairs), 'Z': len(marked),
            'X': len(marked), 'binary_total': binaries,
            'all_variables': binaries + len(states) + types,
            'concrete_nonempty_types': sum(comb(p - d, j) for I in range(2 ** d)
                                          for j in range(p - d + 1) if I or j)}


def main():
    assert sys.flags.optimize == 0, 'Assertions must remain enabled.'
    source, out = map(Path, sys.argv[1:])
    assert out.is_dir() and not list(out.iterdir()), 'Use a fresh empty output directory.'
    payload = source.read_bytes()
    assert hashlib.sha256(payload).hexdigest() == 'c0afb75176e136cb64d30963828f2f9bd4d0b945a93670a6d0bb1dc02e873188'
    namespace = {'__name__': 'eb_frozen_audit_import', '__file__': str(source.resolve())}
    exec(compile(payload, str(source), 'exec'), namespace)
    audit = namespace['audit']
    controls = [
        {'name': 'two_disjoint_singletons',
         'instance': {'topics': ['A', 'B'], 'players': 2,
                      'customers': [{'topics': [0], 'multiplicity': 1}, {'topics': [1], 'multiplicity': 1}]},
         'strategy': strategy(2, 2, lambda h: 0 if not h else 1 - h[0]),
         'expected': {'W': 2, 'OPT': 2, 'histories': 3, 'nonself_deviations': 3}},
        {'name': 'three_player_known_five_thirds_control',
         'instance': {'topics': ['A', 'B', 'C'], 'players': 3,
                      'customers': [{'topics': [0], 'multiplicity': 3}, {'topics': [1], 'multiplicity': 1}, {'topics': [2], 'multiplicity': 1}]},
         'strategy': strategy(3, 3, lambda h: 0),
         'expected': {'W': 3, 'OPT': 5, 'histories': 13, 'nonself_deviations': 26}},
        {'name': 'equal_coverage_labels_with_nonmarkov_actions',
         'instance': {'topics': ['A', 'B'], 'players': 3,
                      'customers': [{'topics': [0, 1], 'multiplicity': 1}]},
         'strategy': strategy(2, 3, lambda h: int(h == (1, 0))),
         'expected': {'W': 1, 'OPT': 1, 'histories': 7, 'nonself_deviations': 7,
                      'equal_count_states_with_different_prescribed_actions': 1}},
        {'name': 'legal_empty_topic',
         'instance': {'topics': ['A', 'empty'], 'players': 2,
                      'customers': [{'topics': [0], 'multiplicity': 1}]},
         'strategy': strategy(2, 2, lambda h: 0),
         'expected': {'W': 1, 'OPT': 1, 'histories': 3, 'nonself_deviations': 3}},
    ]
    results = []
    for case in controls:
        got = audit(case['instance'], case['strategy'])
        for key, value in case['expected'].items():
            assert got[key] == value, (case['name'], key, got[key], value)
        results.append({'name': case['name'], **got})
    mutations = []
    for name in ['missing_history', 'duplicate_history', 'wrong_terminal_counts', 'profitable_off_path_action', 'zero_welfare_ratio']:
        case = deepcopy(controls[-1])
        if name == 'missing_history':
            case['strategy']['actions'].pop()
        elif name == 'duplicate_history':
            case['strategy']['actions'].append(deepcopy(case['strategy']['actions'][0]))
        elif name == 'wrong_terminal_counts':
            case['strategy']['terminal_counts'] = [1, 1]
        elif name == 'profitable_off_path_action':
            case['strategy']['actions'][-1]['action'] = 1
        else:
            case['instance']['customers'] = []
        expected_error = ZeroDivisionError if name == 'zero_welfare_ratio' else AssertionError
        try:
            audit(case['instance'], case['strategy'])
        except expected_error as exc:
            mutations.append({'name': name, 'input': case, 'observed_error': type(exc).__name__})
        else:
            raise AssertionError(('mutation not rejected', name))
    dimensions = [quotient_counts(5, 7, d) for d in [2, 3]]
    assert [(x['all_variables'], x['binary_total']) for x in dimensions] == [(2520, 2446), (6265, 6134)]
    assert all(x['concrete_nonempty_types'] == 127 for x in dimensions)
    unquotiented = {'Y': comb(5 + 2 * 7 - 1, 2 * 7 - 1),
                   'Z': 7 * comb(5 + 2 * 7 - 2, 2 * 7 - 1),
                   'T': comb(5 + 7 - 1, 7), 'types': 127}
    unquotiented['binary_total'] = unquotiented['Y'] + 2 * unquotiented['Z']
    unquotiented['all_variables'] = unquotiented['binary_total'] + unquotiented['T'] + unquotiented['types']
    assert (unquotiented['all_variables'], unquotiented['binary_total']) == (42345, 41888)
    (out / 'new-control-inputs.json').write_text(json.dumps(controls, ensure_ascii=False, indent=2) + '\n')
    report = {'scope': 'new EB controls and quotient-index arithmetic, not original candidate or MIP replay',
              'audit_source_sha256': hashlib.sha256(payload).hexdigest(), 'original_main_called': False,
              'solver_calls': 0, 'positive_controls': results, 'negative_controls': mutations,
              'positive_decision_histories': sum(x['histories'] for x in results),
              'positive_nonself_deviations': sum(x['nonself_deviations'] for x in results),
              'quotient_index_counts': dimensions, 'unquotiented_counts': unquotiented,
              'universal_half_proved': False}
    (out / 'result.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': 'pass', 'positive_controls': len(results), 'negative_controls': len(mutations),
                      'positive_histories': report['positive_decision_histories'],
                      'positive_nonself_deviations': report['positive_nonself_deviations'],
                      'original_main_called': False, 'solver_calls': 0}))


if __name__ == '__main__':
    main()
