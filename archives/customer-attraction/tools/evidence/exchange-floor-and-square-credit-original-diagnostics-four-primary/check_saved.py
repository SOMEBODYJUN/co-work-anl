"""Bind two stored local negative points to established input bytes; never import source tests."""
from collections import Counter
from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path
import ast
import hashlib
import json
import math


def fingerprint(path):
    raw = path.read_bytes()
    return len(raw), hashlib.sha256(raw).hexdigest()


def check():
    base = Path(__file__).resolve().parent
    primary = json.loads((base / 'source-manifest.json').read_text())
    assert primary['primary_count'] == 4
    assert primary['primary_bytes'] == sum(r['size'] for r in primary['rows']) == 4399
    originals = {}
    for row in primary['rows']:
        path = base / 'original' / row['path']
        raw = path.read_bytes()
        assert fingerprint(path) == (row['size'], row['sha256'])
        assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == row['blob']
        originals[path.name] = path
        if path.suffix == '.py':
            ast.parse(path.read_text())  # No import, exec or source-function invocation.
        else:
            json.loads(path.read_text())
    for filename, count in [('dependency-manifest.json', 2), ('comparison-manifest.json', 8)]:
        manifest = json.loads((base / filename).read_text())
        assert len(manifest['rows']) == count
        for row in manifest['rows']:
            assert fingerprint(base / row['path']) == (row['size'], row['sha256'])
    input_path = base / 'original/examples/customer_attraction/root_tax_failure.json'
    certificate_path = base / 'original/evidence/certificates/customer_attraction/root_tax_failure.json'
    assert fingerprint(input_path)[1] == '864eca4cc1d5df2d039704eb444863405298e6fc6746efb18c49035a801a7ce6'
    assert fingerprint(certificate_path)[1] == '59fd58d85a3c3b989837467eb3523286d1f5ee529b0f119cd4d263bef6984111'
    instance = json.loads(input_path.read_text())
    certificate = json.loads(certificate_path.read_text())
    assert instance['players'] == 4 and instance['topics'] == list('ABCDEF')
    types = [(frozenset(r['topics']), r.get('multiplicity', 1)) for r in instance['customers']]
    assert len(types) == 12 and sum(w for _, w in types) == 61
    rows = certificate['strategy']['actions']
    policy = {tuple(r['history']): r['action'] for r in rows}
    assert len(policy) == len(rows) == 259
    depths = Counter(map(len, policy))
    assert depths == {0: 1, 1: 6, 2: 36, 3: 216}
    for history, action in policy.items():
        assert all(type(a) is int and 0 <= a < 6 for a in history)
        assert type(action) is int and 0 <= action < 6
        expected = 0 if len(history) < 3 or history.count(0) <= 1 else (4 if 5 in history else 5)
        assert action == expected
    history = (0,)
    action = policy[history]
    leaf = list(history)
    while len(leaf) < 4:
        leaf.append(policy[tuple(leaf)])
    leaf = tuple(leaf)
    assert action == 0 and leaf == (0, 0, 0, 5)
    u = sum((Fraction(w, sum(a in B for a in leaf)) for B, w in types if action in B), Fraction(0))
    assert u == 9
    comp = (1, 2, 3)
    forbidden = set(history) | {action}
    private = [sum(w for B, w in types if B.isdisjoint(forbidden) and a in B and len(B.intersection(comp)) == 1) for a in comp]
    assert private == [10, 11, 10]
    floor_report = json.loads(originals['exchange_floor_attack.json'].read_text())
    expected_floor = {'instance': 'root_tax_failure', 'checks': 1971, 'max_violation': '1',
                      'history': [0], 'A': 0, 'leaf': [0, 0, 0, 5],
                      'comparison': [1, 2, 3], 'private': [10, 11, 10], 'u': '9'}
    assert floor_report == expected_floor
    assert min(private) - u == Fraction(floor_report['max_violation'])
    assert sum(number * math.comb(6, 4 - d) for d, number in depths.items()) == 1971
    def load(actions, B):
        return sum(a in B for a in actions)
    def future_total(prefix, tail):
        return sum((Fraction(w * load(tail, B), load(prefix, B) + load(tail, B))
                    for B, w in types if load(tail, B)), Fraction(0))
    tail = leaf[len(history) + 1:]
    deltaH = sum((w * (Fraction(1, (load(history, B) + 1) ** 2)
                       - (Fraction(1, (load(history + (action,), B) + 1) ** 2)
                          if load(tail, B) else 0))
                  for B, w in types if action in B), Fraction(0))
    assert deltaH == Fraction(25, 6)
    tables = []
    maxima = []
    for prefix, remaining in [(history, 3), (history + (action,), 2)]:
        values = [{'tail_multiset': list(t), 'future_total': str(future_total(prefix, t))}
                  for t in combinations_with_replacement(range(6), remaining)]
        maximum = max(Fraction(r['future_total']) for r in values)
        maximizers = [r['tail_multiset'] for r in values if Fraction(r['future_total']) == maximum]
        tables.append({'prefix': list(prefix), 'remaining_players': remaining,
                       'multiset_count': len(values), 'maximum': str(maximum),
                       'all_maximizers': maximizers, 'all_values': values})
        maxima.append(maximum)
    assert [r['multiset_count'] for r in tables] == [56, 21]
    assert maxima == [Fraction(36), Fraction(21)]
    slack = u + deltaH - maxima[0] + maxima[1]
    assert slack == Fraction(-11, 6)
    power_report = json.loads(originals['power_credit_attack.json'].read_text())
    assert power_report == {'instance': 'root_tax_failure', 'power': 2, 'minimum_slack': '-11/6',
                             'history': [0], 'A': 0, 'leaf': [0, 0, 0, 5],
                             'u': '9', 'deltaH': '25/6', 'F_r': '36', 'F_next': '21'}
    return {
        'status': 'passed-byte-binding-and-single-local-negative-point',
        'primary_sources': 4, 'primary_bytes': 4399,
        'input_sha256': fingerprint(input_path)[1],
        'certificate_sha256': fingerprint(certificate_path)[1],
        'certificate_structure_rows_read': len(rows),
        'full_SPE_IC_checks': 0,
        'SPE_status_basis': 'Existing complete root-tax proof and independent full-history audits; not reverified by this local check.',
        'point': {'history': list(history), 'A': action, 'leaf': list(leaf), 'u': str(u),
                  'comparison': list(comp), 'private': private, 'floor_violation': str(min(private) - u),
                  'deltaH': str(deltaH), 'power': 2, 'F_r': str(maxima[0]),
                  'F_next': str(maxima[1]), 'Bellman_slack': str(slack)},
        'future_profit_tables': tables,
        'original_report_global_extrema_independently_rescanned': False,
        'source_entry_invocations': 0, 'source_imports': 0, 'source_function_calls': 0,
        'source_1971_exchange_scan_invocations': 0, 'SPE_solver_or_BI_calls': 0,
        'LP_or_random_or_additional_instance_calls': 0,
        'new_finite_computation_scope': 'Only one fixed history and 56+21 pure comparison-tail multisets; no history/strategy search.',
    }


if __name__ == '__main__':
    result = check()
    target = Path(__file__).with_name('local-point-check.json')
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'future_profit_tables'}, ensure_ascii=False, indent=2))
