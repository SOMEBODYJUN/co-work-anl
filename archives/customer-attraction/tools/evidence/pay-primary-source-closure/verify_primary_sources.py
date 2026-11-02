"""Verify preserved frozen inputs and inspect the full saved PAY action table.

This consumes existing source bytes and execution records. It does not rerun
the original mathematical entry points or infer unbounded claims from samples.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'cleanup/inventory.jsonl').is_file())
OLD = ROOT / 'archives/customer-attraction/tools/evidence/pay-original-implementation-comparison'
IDS = ['be291aa649fa6bd1377d', '373d0259e7b3ecea0d5e',
       'ed7db7c28c0bd44b2c9a', '11d8ac688fe00b2073c3', '77eab72e4fed4356a179',
       '44a62657484ed4b665b5', 'cbb00c0d7e3ba0af602e']
inventory = {r['id']: r for r in map(json.loads, (ROOT / 'cleanup/inventory.jsonl').read_text().splitlines())}
old_manifest = json.loads((OLD / 'source-and-dependency-manifest.json').read_text())
old_rows = {r['id']: r for r in old_manifest['original_related_sources']['rows']}
rows, data = [], {}
for sid in IDS:
    row = inventory[sid]
    path = ROOT / old_rows[sid]['preserved_at']
    raw = path.read_bytes()
    assert len(raw) == row['size'] and sha256(raw).hexdigest() == row['sha256']
    data[sid] = raw
    rows.append({'id': sid, 'source_path': row['path'], 'source_refs': row['sources'],
                 'preserved_at': str(path.relative_to(ROOT)), 'size': len(raw),
                 'sha256': sha256(raw).hexdigest(), 'matches_frozen_inventory': True})

tree = json.loads(data[IDS[4]])
assert set(tree) == {'status', 'scope', 'instance', 'certificate', 'checked_histories',
                     'checked_deviations', 'unique_optimal_counts', 'prefixes'}
actions = tree['certificate']['actions']
expected = {h for d in range(5) for h in product(range(5), repeat=d)}
actual = [tuple(a['history']) for a in actions]
assert len(actual) == len(set(actual)) == 781 and set(actual) == expected
assert all(set(a) == {'history', 'action'} and a['action'] == 0 for a in actions)
assert tree['certificate']['terminal_counts'] == [5, 0, 0, 0, 0]
assert tree['instance'] == {'topics': ['B', 'L1', 'L2', 'L3', 'L4'],
    'customers': [{'topics': [0], 'multiplicity': 12}]+
                 [{'topics': [j], 'multiplicity': 1} for j in range(1,5)], 'players': 5}
assert tree['checked_histories'] == 781 and tree['checked_deviations'] == 3124
assert tree['unique_optimal_counts'] == [1]*5

# Independent direct finite evaluation: both endpoints and every actual kink.
prefix_rows = []
for p in range(4):
    k, types = 5-p, [(12,p,1),(4,0,1)]
    knots = {F(0), F(4)} | {F(20*(b+1), d*(k-1)+5*(b+1)) for _,b,d in types}
    def raw(t):
        return sum(w*(1-F(2*(k-2)*d,5*(b+k))-
            min(t*d/(5*(b+1)), (t*d/5+4-t)/(b+k))) for w,b,d in types)
    score, t = min((raw(t)-F(24*p,5),t) for t in knots)
    prefix_rows.append({'p':p,'k':k,'best_t':str(t),'charge_minus_2E':str(score),
                        'all_breakpoints':list(map(str,sorted(knots)))})
assert [(r['best_t'],r['charge_minus_2E']) for r in prefix_rows] == [
    ('20/9','1136/225'),('40/13','1056/325'),('20/7','176/525'),('10/3','-46/15')]
for saved,p in zip(tree['prefixes'],[1,2]):
    assert saved == {'length':p,'best_t':prefix_rows[p]['best_t'],
                     'minimum_PAY_margin':prefix_rows[p]['charge_minus_2E']}

jsonl = [json.loads(s) for s in data[IDS[1]].decode().splitlines()]
old_comparison = json.loads((OLD / 'comparison-results.json').read_text())
assert len(jsonl) == len(old_comparison['three_input_JSONL']) == 3
for row, old in zip(jsonl,old_comparison['three_input_JSONL']):
    compared = old['old_and_new_finite_results']
    assert row.keys() == compared.keys()
    assert {k:v for k,v in row.items() if k != 'seconds'} == {k:v for k,v in compared.items() if k != 'seconds'}
    assert row['seconds'] == old['frozen_seconds']
report = json.loads(data[IDS[3]])
assert report['quantile_vs_all_breakpoints'] == 180
assert report['ordered_history_policies_enumerated'] == 128
assert report['ordered_history_SPE_policies'] == 14
assert report['independent_exhaustive_policy_max_min'] == report['count_DAG_max_min'] == '-1'
assert report['sharp_big_theme_family_checks'] == 38
assert report['prefix_balance_family_checks'] == 37
assert report['monotone_parameter_family_checks'] == 36
assert report['m5_complete_SPE_histories'] == 781 and report['m5_complete_SPE_deviations'] == 3124
parent_report = json.loads(data[IDS[6]])
parent_stdout = json.loads((OLD / 'runs/parent-explicit-path-audit/stdout.txt').read_text())
assert set(parent_report)-set(parent_stdout) == {'command'}
assert {k:v for k,v in parent_report.items() if k != 'command'} == parent_stdout
assert [(c['all_ordered_SPE_paths'],c['optimal_counts'],c['literal_breakpoint_and_DAG_value'])
        for c in parent_report['cases']] == [(81,15,'0'),(6,3,'-3'),(2,9,'-59/15')]
result = {'scope':'source identity and full saved structure; no original mathematical CLI rerun',
    'sources':rows,'all_781_history_rows_consumed':True,'histories_exactly_all_ordered_decision_histories':True,
    'all_actions_B':True,'three_JSONL_all_fields_compared_preserving_seconds':True,
    'author_report':report,'m5_prefix_direct_fraction_evaluation':prefix_rows,
    'parent_report':parent_report,'parent_all_fields_match_saved_stdout_except_additional_command':True,
    'prior_execution_record':'archives/customer-attraction/tools/evidence/pay-original-implementation-comparison/execution-summary.json',
    'original_mathematical_entry_executions_this_batch':0}
(HERE/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'verified_source_count':len(rows),'history_rows':len(actions),
                  'original_CLI_reruns':0,'last_allowed_prefix_margin':prefix_rows[-1]['charge_minus_2E']}))
