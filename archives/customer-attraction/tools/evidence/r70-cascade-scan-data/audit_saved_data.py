"""Read every saved field/action; no producer import, LP, BI or numerical IC replay.

The complete strategy is certified analytically in the companion Markdown:
all future actions cover the same six-customer block, so u_big=6/(6-s)>=1,
while a singleton deviation yields 1/(q_j+1)<=1 at every ordered history.
"""
import argparse
import collections
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import time


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(scan_path, best_path, output):
    started = time.perf_counter()
    assert not output.exists(), 'preserve the existing data-read event'
    expected = ['eca75e5b362c4581d1ac0cf24e68dec5d7800e69c14c3f41bdd55bfec21746bd',
                '9ce3f7fc519da8b89ed91a0bc0478c27d37536f49a3064fef8d6bdc4a987ae96']
    paths = [scan_path, best_path]
    before = [sha(p) for p in paths]
    assert before == expected
    scan, best = [json.loads(p.read_text()) for p in paths]
    assert set(scan) == {'parameters', 'scope', 'universal_bound_proved', 'history'}
    assert set(scan['parameters']) == {'rounds', 'topics', 'players', 'anchors',
        'private_floor', 'last_count_max', 'output'}
    assert scan['parameters'] == dict(rounds=20, topics=7, players=6, anchors=2,
        private_floor=0, last_count_max=0,
        output='research/workspaces/customer-attraction/R-70d2119f50a642dc94b386eb142f1f2d/six_3/cascade_scan.json')
    assert scan['scope'] == 'targeted anchor-gap cascade family with exact complete-tree cone checks'
    assert scan['universal_bound_proved'] is False
    hrows = scan['history']
    assert len(hrows) == 7
    oldbest, oldtime = Fraction(0), -1
    for i, row in enumerate(hrows):
        assert set(row) == {'iteration', 'source_ratio', 'root', 'on_path', 'rows',
            'seed_support', 'source_maxima', 'best', 'elapsed'} | ({'new_best'} if i == 0 else set())
        assert row['iteration'] == i and row['on_path'] is None
        assert len(row['root']) == 7 and sum(row['root']) == 6
        assert all(type(x) is int and x >= 0 for x in row['root'])
        assert 1 <= row['seed_support'] <= 127 and 1 <= row['source_maxima'] <= 7
        assert row['rows'] > 0 and Fraction(row['source_ratio']) > 0
        assert Fraction(row['best']) >= oldbest and row['elapsed'] >= oldtime
        if 'new_best' in row:
            assert Fraction(row['new_best']) == Fraction(row['best']) > oldbest
        oldbest, oldtime = Fraction(row['best']), row['elapsed']
    assert set(best) == {'best_ratio_lower_bound', 'distinct_maximal_themes', 'target',
        'portfolio', 'instance', 'certificate', 'row_scope', 'note'}
    assert best['best_ratio_lower_bound'] == '11/6' and best['distinct_maximal_themes'] == 6
    assert best['row_scope'] == 'all ordered histories' and best['note'] == 'not a universal bound'
    assert best['target'] == [4, 2, 0, 0, 0, 0, 0]
    assert best['portfolio'] == [0, 2, 3, 4, 5, 6]
    inst = best['instance']
    assert set(inst) == {'topics', 'customers', 'players'}
    assert inst['topics'] == ['T'+str(j) for j in range(7)] and inst['players'] == 6
    assert inst['customers'] == [{'topics': [0, 1], 'multiplicity': 6}] + [
        {'topics': [j], 'multiplicity': 1} for j in range(2, 7)]
    cert = best['certificate']
    assert set(cert) == {'terminal_counts', 'actions'}
    assert cert['terminal_counts'] == best['target']
    actions = {}
    depth = [collections.Counter() for _ in range(6)]
    groups = collections.defaultdict(list)
    canonical = hashlib.sha256()
    zero_private_histories = 0
    for item in cert['actions']:
        assert set(item) == {'history', 'action'}
        h, a = tuple(item['history']), item['action']
        assert len(h) < 6 and all(type(x) is int and 0 <= x < 7 for x in h)
        assert type(a) is int and a in (0, 1), (h, a)
        assert h not in actions
        actions[h] = a
        depth[len(h)][a] += 1
        counts = tuple(h.count(j) for j in range(7))
        groups[counts].append(item)
        if sum(counts[2:]) == 0:
            zero_private_histories += 1
        canonical.update((json.dumps(item, separators=(',', ':'), sort_keys=True)+'\n').encode())
    expected_histories = {h for d in range(6) for h in itertools.product(range(7), repeat=d)}
    assert set(actions) == expected_histories
    assert len(actions) == 19608 and len(groups) == 792
    assert cert['actions'] == sorted(cert['actions'], key=lambda r: (len(r['history']), r['history']))
    nonuniform = [{'counts': list(q), 'records': rows} for q, rows in sorted(groups.items())
                  if len({r['action'] for r in rows}) > 1]
    path = ()
    while len(path) < 6:
        path += (actions[path],)
    assert [path.count(j) for j in range(7)] == best['target']
    assert path == (1, 1, 0, 0, 0, 0)
    # Coverage is read directly from all six types; seven maximal supports suffice
    # by monotonicity for six choices from seven labels, even allowing repetitions.
    covers = []
    for omit in range(7):
        support = set(range(7)) - {omit}
        covers.append(sum(r['multiplicity'] for r in inst['customers'] if support.intersection(r['topics'])))
    assert covers == [11, 11, 10, 10, 10, 10, 10]
    assert sum(r['multiplicity'] for r in inst['customers']) == 11
    assert [sha(p) for p in paths] == before
    result = {
        'status': 'pass', 'scope': 'complete saved-data consumption and analytic-SPE premise validation',
        'input_sha256_before_and_after': before,
        'source_fields_complete': {'history_top': list(scan), 'parameters': scan['parameters'],
            'history_rows': hrows, 'best_top': list(best), 'instance': inst,
            'best_non_action_fields': {k: v for k, v in best.items() if k not in ('instance', 'certificate')},
            'certificate_terminal_counts': cert['terminal_counts']},
        'all_action_records_read': len(actions),
        'ordered_history_domain_complete_and_unique': True,
        'actions_canonical_stream_sha256': canonical.hexdigest(),
        'actions_by_depth': [dict(sorted(c.items())) for c in depth],
        'all_actions_cover_the_same_six_customer_block': True,
        'count_groups': len(groups), 'nonuniform_count_groups': nonuniform,
        'actual_ordered_path': path,
        'actual_payoffs_by_analytic_formula': ['1'] * 6,
        'actual_W': 6, 'all_six_label_support_coverages_by_omitted_label': covers,
        'OPT6': 11, 'ratio_OPT_over_W': '11/6', 'half_slack': 1,
        'analytic_IC_domain_size_nonself_not_numerically_replayed': len(actions)*6,
        'analytic_nonself_ties': len(actions) + 5*zero_private_histories,
        'analytic_nonself_strict': 5*(len(actions)-zero_private_histories),
        'analytic_tie_explanation': 'one alternate big label at each history, plus five singleton ties iff no prior singleton action',
        'new_producer_import_main_LP_BI_or_canonical_verifier_calls': 0,
        'full_numerical_IC_replay_calls': 0,
        'read_elapsed_seconds': time.perf_counter()-started,
    }
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('source_fields_complete', 'nonuniform_count_groups')}, ensure_ascii=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('scan', type=Path)
    ap.add_argument('best', type=Path)
    ap.add_argument('output', type=Path)
    a = ap.parse_args()
    run(a.scan, a.best, a.output)
