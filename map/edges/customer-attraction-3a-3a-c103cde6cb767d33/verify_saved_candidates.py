"""Replay literal saved fractions and complete IC trees; do not solve an LP.

This audits fixed records only. It does not certify sharp dilution, optimality,
nonnegative customer realizability, or a theorem for any unsaved strategy.
"""
from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
import hashlib
import json

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'work.py').is_file())
BASE = ROOT / 'archives/customer-attraction/tools/evidence/boss3-c16-resumed/original/research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/tree'


def exact_ic(n, p, weights, actions):
    required = {h for d in range(n) for h in product(range(p), repeat=d)}
    assert set(actions) == required
    assert all(0 <= a < p for a in actions.values())
    terminal = {h: tuple(h.count(a) for a in range(p))
                for h in product(range(p), repeat=n)}
    for d in range(n - 1, -1, -1):
        for h in product(range(p), repeat=d):
            terminal[h] = terminal[h + (actions[h],)]
    cache = {}

    def utility(q, a):
        if (q, a) not in cache:
            cache[q, a] = sum((v / sum(q[b] for b in range(p) if B >> b & 1)
                               for B, v in weights.items() if B >> a & 1), Q())
        return cache[q, a]

    rows = [(utility(terminal[h], a) - utility(terminal[h + (b,)], b), h, a, b)
            for h, a in actions.items() for b in range(p) if a != b]
    minimum = min(rows)
    q = terminal[()]
    coverage = sum((v for B, v in weights.items()
                    if any(q[a] and B >> a & 1 for a in range(p))), Q())
    return dict(action_count=len(actions), genuine_ic_count=len(rows),
                negative_ic_count=sum(v[0] < 0 for v in rows),
                min_ic=str(minimum[0]), min_ic_decimal=float(minimum[0]),
                witness=dict(history=minimum[1], prescribed=minimum[2],
                             alternative=minimum[3],
                             prescribed_terminal=terminal[minimum[1]],
                             alternative_terminal=terminal[minimum[1] + (minimum[3],)]),
                actual_count=q, actual_coverage=str(coverage))


def main():
    result = {'scope': 'Literal fixed-record exact IC and local-pattern replay only',
              'inputs': {}, 'records': {}}
    for n in (3, 5):
        name = f'signed_policy_n{n}_p6_best.json'
        raw = (BASE / name).read_bytes()
        x = json.loads(raw)
        result['inputs'][name] = hashlib.sha256(raw).hexdigest()
        weights = {v['mask']: Q(v['weight']) for v in x['signed_customer_weights']}
        actions = {tuple(v['history']): v['action'] for v in x['strategy_actions']}
        assert len(actions) == len(x['strategy_actions'])
        record = exact_ic(n, 6, weights, actions)
        record['fixed_target'] = x['target']
        record['fixed_target_coverage'] = str(sum((v for B, v in weights.items()
                                                  if any(B >> a & 1 for a in x['target'])), Q()))
        logs_raw = (BASE / f'signed_policy_n{n}_p6_run.json').read_bytes()
        logs = json.loads(logs_raw)
        result['inputs'][f'signed_policy_n{n}_p6_run.json'] = hashlib.sha256(logs_raw).hexdigest()
        assert [v['trial'] for v in logs] == list(range(len(logs)))
        record['saved_report_count'] = len(logs)
        record['max_saved_float_trial'] = max(logs, key=lambda v: v['value'])['trial']
        result['records'][name] = record
    assert result['records']['signed_policy_n3_p6_best.json']['negative_ic_count'] == 0
    assert result['records']['signed_policy_n5_p6_best.json']['negative_ic_count'] == 75
    for local in (0, 1):
        name = f'symmetric_hub_local{local}.json'
        raw = (BASE / name).read_bytes()
        x = json.loads(raw)
        result['inputs'][name] = hashlib.sha256(raw).hexdigest()
        orbit = {(v['h'], v['k']): Q(v['per_type_weight']) for v in x['orbits']}
        weights = {B: orbit[B & 1, B.bit_count() - (B & 1)] for B in range(1, 32)}
        actions = {h: 0 for d in range(4) for h in product(range(5), repeat=d)}
        record = exact_ic(4, 5, weights, actions)
        patterns = [(sum((v for B, v in weights.items() if B & A == X), Q()), A, X)
                    for k in range(1, 5) for labels in combinations(range(5), k)
                    for A in [sum(1 << a for a in labels)]
                    for X in range(1, 32) if X & A == X]
        least = min(patterns)
        record.update(local_pattern_count=len(patterns),
                      negative_local_patterns=sum(v[0] < 0 for v in patterns),
                      min_local_pattern=str(least[0]),
                      local_pattern_witness={'A_mask': least[1], 'X_mask': least[2]},
                      satellite_coverage=str(sum((v for B, v in weights.items() if B >> 1), Q())))
        assert record['negative_ic_count'] == 0
        assert Q(record['actual_coverage']) == 1
        if local == 1:
            assert record['negative_local_patterns'] == 0
        result['records'][name] = record
    out = Path(__file__).with_name('literal_candidate_report.json')
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    for name, v in result['records'].items():
        print(name, 'IC', v['genuine_ic_count'], 'negative', v['negative_ic_count'],
              'min', v['min_ic_decimal'], 'negative_local', v.get('negative_local_patterns'))


if __name__ == '__main__':
    main()
