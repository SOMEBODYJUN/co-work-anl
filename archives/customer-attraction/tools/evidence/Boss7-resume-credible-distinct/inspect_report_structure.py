"""Read every stored record without running the source game/DP/LP/SPE checker.

The output describes preserved bytes and policy layout.  It does not certify
equilibrium incentives, solver optimality, or the original execution history.
"""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def inspect_trial(path):
    data = json.loads(path.read_text())
    exact = data['exact']
    rows = exact['strategy']['actions']
    policy = {}
    for row in rows:
        assert set(row) == {'history', 'action'}
        h, a = tuple(row['history']), row['action']
        assert len(h) < 5 and all(type(b) is int and 0 <= b < 7 for b in h)
        assert type(a) is int and 0 <= a < 7 and h not in policy
        policy[h] = a
    expected = {h for depth in range(5) for h in product(range(7), repeat=depth)}
    assert set(policy) == expected and len(rows) == 2801
    clones = exact['integer_clones']
    assert len(clones) == 127 and all(type(v) is int and v >= 0 for v in clones)
    positive = [{'mask': b, 'topics': [a for a in range(7) if b >> a & 1],
                 'multiplicity': v} for b, v in enumerate(clones, 1) if v]
    topic_types = [tuple(r['mask'] for r in positive if r['mask'] >> a & 1)
                   for a in range(7)]
    groups = defaultdict(list)
    for h, a in policy.items():
        groups[tuple(h.count(b) for b in range(7))].append((h, a))
    different = [v for v in groups.values() if len({a for _, a in v}) > 1]
    branches = []
    for b in range(7):
        branch_policy = {h: a for h, a in policy.items() if h and h[0] == b}
        selected = data['milp']['selected'][b]
        digest = sha256(repr(sorted(branch_policy.items())).encode()).hexdigest()
        assert selected['branch'] == b and selected['digest'] == digest
        h = (b,)
        while len(h) < 5:
            h += (policy[h],)
        counts = [h.count(a) for a in range(7)]
        assert selected['target'] == counts
        branches.append({'branch': b, 'path': h, 'counts': counts,
                         'selected_digest_matches': True})
    scalar_report = {k: v for k, v in data.items() if k != 'exact'}
    scalar_report['exact'] = {k: v for k, v in exact.items()
                              if k not in {'strategy', 'integer_clones'}}
    return {'source_sha256': sha256(path.read_bytes()).hexdigest(),
            'all_nondatatable_fields': scalar_report,
            'all_positive_customer_types': positive,
            'zero_type_entries': 127-len(positive),
            'distinct_topic_coverage_sets': len(set(topic_types)),
            'all_action_records_read': len(rows),
            'ordered_history_key_set_complete': True,
            'action_frequencies_by_depth': [dict(sorted(Counter(
                policy[h] for h in expected if len(h) == depth).items()))
                for depth in range(5)],
            'same_count_groups_with_different_actions': len(different),
            'same_count_different_action_examples': different[:2],
            'all_root_branch_paths_and_digest_bindings': branches}


def main():
    manifest = json.loads((HERE/'source-manifest.json').read_text())
    output = {'status': 'PASS_FROZEN_REPORT_STRUCTURE_AND_COMPLETE_DATA_READING',
              'scope': 'byte identity, full schema/data traversal, policy layout only',
              'no_original_solver_checker_or_optimization_executed': True,
              'trials': {}}
    for item in manifest['primary'] + manifest['related']:
        p = HERE/item['local_path']
        assert sha256(p.read_bytes()).hexdigest() == item['sha256']
        assert len(p.read_bytes()) == item['size']
        if item['id'] in {'7454db09c8a5783bc881', 'd94a54c87c4c880c05ba'}:
            output['trials'][item['id']] = inspect_trial(p)
        elif item['id'] == '91067a0274482845371c':
            d = json.loads(p.read_text())
            assert set(d) == {'status', 'seed', 'cases'} and len(d['cases']) == 40
            groups = defaultdict(list)
            for r in d['cases']:
                assert set(r) == {'players', 'topics', 'case', 'root_outcomes'}
                assert all(type(v) is int for v in r.values())
                groups[r['players'], r['topics']].append(r)
            assert set(groups) == {(2, 3), (3, 4), (4, 4), (5, 3)}
            for rs in groups.values():
                assert [r['case'] for r in rs] == list(range(10))
            output['dp_crosscheck_all_fields_and_all_cases'] = d
    (HERE/'complete-data-read-index.json').write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': output['status'], 'trial_action_records': 5602,
                      'trial_clone_entries': 254, 'dp_records': 40,
                      'mathematical_checks_replayed': 0}, ensure_ascii=False))


if __name__ == '__main__':
    main()
