"""Cross-schema/data reconciliation only: no original import, payoff, BI or LP.

The original two entries were separately replayed once. The earlier Boss4
definition audit is read as existing evidence, never executed or rewritten.
"""
import argparse
import ast
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--repository-root', type=Path, required=True)
args = parser.parse_args()
ROOT = HERE.parent
ORIGINAL = ROOT / 'original'
OLD = args.repository_root / 'archives/customer-attraction/tools/evidence/maximal-population-and-ordered-compression-primary/new-definition-audit'
read_files = []


def read(path):
    b = path.read_bytes()
    read_files.append(dict(path=str(path), sha256=hashlib.sha256(b).hexdigest(), size=len(b)))
    return json.loads(b)


def constants(path):
    b = path.read_bytes()
    read_files.append(dict(path=str(path), sha256=hashlib.sha256(b).hexdigest(), size=len(b)))
    result = {}
    for node in ast.parse(b).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                result[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                pass
    return result


LABEL = 'ABCD'
TYPES = [[0, 1], [2], [1, 2], [0, 3], [0, 1, 3], [2, 3]]
old = read(OLD / 'output.json')
old_input = read(OLD / 'input.json')
old_event = read(OLD / 'event.json')
assert old_event['exit_code'] == 0
assert old_event['output_sha256'] == hashlib.sha256((OLD/'output.json').read_bytes()).hexdigest()
assert old_event['input_sha256'] == hashlib.sha256((OLD/'input.json').read_bytes()).hexdigest()
pop = read(ORIGINAL / 'population_exchange_audit.json')
family = read(ORIGINAL / 'strict_population_family_audit.json')
src = constants(ORIGINAL / 'strict_population_family_audit.py')
assert list(src['BASE']) == old_input['thirteen'] == [3, 1, 2, 1, 3, 3]
assert [[a, b] for a, b in zip(src['BASE'], src['OFFSET'])] == old_input['strict_q_affine']
assert [list(t) for t in src['TYPES']] == family['type_order'] == TYPES
assert family['parameter'] == 'integer q>=22'
assert family['multiplicities'] == ['3q+1', 'q-10', '2q-12', 'q-11', '3q-7', '3q-11']
assert (family['total_and_OPT'], family['minimum_SPE_W2'], family['minimum_SPE_W3'], family['decrease'], family['W3_over_W2_limit']) == ('13q-50', '13q-50', '12q-40', 'q-10', '12/13')
certificates = []
finite_matches = []
policies = {}
for example in pop['examples']:
    name = example['name']
    weights = old_input['thirteen' if name == 'thirteen' else 'forty']
    assert example['unit_customers'] == sum(weights)
    assert example['types'] == [dict(topics=[LABEL[a] for a in t], multiplicity=w) for t, w in zip(TYPES, weights)]
    for m in (2, 3):
        cert = read(ORIGINAL / f'{name}_m{m}_certificate.json')
        expected = {h for d in range(m) for h in itertools.product(range(4), repeat=d)}
        rows = cert['actions']
        assert len(rows) == len(expected)
        assert all(all(type(a) is int and 0 <= a < 4 for a in r['history']) and type(r['action']) is int and 0 <= r['action'] < 4 for r in rows)
        actions = {tuple(r['history']): r['action'] for r in rows}
        assert set(actions) == expected and len(actions) == len(rows)
        assert cert['instance'] == dict(topics=list(LABEL), customers=[dict(topics=t, multiplicity=w) for t, w in zip(TYPES, weights)], players=m)
        decoded = {''.join(LABEL[a] for a in h): LABEL[a] for h, a in actions.items()}
        policies[f'{name}_m{m}'] = decoded
        r = example['players'][str(m)]
        assert len(r['table']) == r['nodes'] == len(expected)
        assert r['comparisons'] == 4*len(expected)
        assert {x['history']: x['chosen'] for x in r['table']} == decoded
        assert r['all_nodes_strict'] == all(x['strict'] for x in r['table'])
        certificates.append(dict(name=name, players=m, nodes=len(expected), exact_instance_metadata=True, no_duplicate_histories=True, all_history_and_action_labels_legal=True, decoded_policy=decoded, nonstrict_histories=[x['history'] for x in r['table'] if not x['strict']]))
        if name == 'thirteen':
            older = old['thirteen'][str(m)]
            assert r['ordered_SPE_paths'] == older['paths']
            assert r['all_SPE_terminal_counts'] == older['terminal_counts']
            assert r['minimum_SPE_welfare'] == older['minimum_W']
            assert r['OPT'] == older['OPT']
            finite_matches.append(dict(name=name, players=m, exact_paths=r['ordered_SPE_paths'], terminal_counts=r['all_SPE_terminal_counts'], minimum_W=r['minimum_SPE_welfare'], OPT=r['OPT'], comparison='root-achievable outcome sets, not the older audit of this selected policy'))
        else:
            older = old['forty'][str(m)]
            assert decoded == {x['history']: x['action'] for x in older['rows']}
            for row, prev in zip(r['table'], older['rows']):
                assert row['history'] == prev['history']
                assert [F(x) for x in row['values']] == [F(x) for x in prev['true_payoffs']]
            assert r['path'] == older['path'] and r['payoffs'] == older['payoffs']
            assert r['welfare'] == older['W'] and r['OPT'] == older['OPT']
            assert r['minimum_nonself_slack'] == older['min_nonself_slack']
            assert r['comparisons'] == 4*older['decision_nodes']
            assert 3*r['nodes'] == older['nonself_IC']
            finite_matches.append(dict(name=name, players=m, all_node_action_payoffs_equal=True, payoff_entries=4*r['nodes'], root_path=r['path'], W=r['welfare'], minimum_nonself_slack=r['minimum_nonself_slack']))

affine_matches = []
for report in family['policies']:
    m = report['players']
    previous = old['strict_q'][str(m)]
    expected = {h for d in range(m) for h in itertools.product(range(4), repeat=d)}
    policy = dict(src[f'P{m}'])
    if m == 3:
        policy.update({(a, b): src['LAST'][a][b] for a in range(4) for b in range(4)})
    decoded = {''.join(LABEL[a] for a in h): LABEL[a] for h, a in policy.items()}
    assert set(policy) == expected
    assert decoded == previous['policy']
    policies[f'q_m{m}'] = decoded
    original_rows = {(''.join(LABEL[a] for a in row['history']), LABEL[row['deviation']]): row for row in report['rows']}
    previous_rows = {(row['history'], gap['alternative']): (row, gap) for row in previous['rows'] for gap in row['gaps']}
    assert len(original_rows) == len(report['rows']) == previous['nonself_IC'] == 3*len(expected)
    assert set(original_rows) == set(previous_rows)
    for key, row in original_rows.items():
        prev, gap = previous_rows[key]
        assert LABEL[row['chosen']] == prev['action'] == decoded[key[0]]
        assert F(row['alpha']) == F(gap['alpha'])
        assert F(row['beta']) == F(gap['beta'])
        assert F(row['slack_q22']) == F(gap['q22_value'])
    assert report['nodes'] == len(expected)
    assert report['all_strict_for_q_ge'] == 22
    assert report['exact_threshold_q_strictly_greater_than'] == previous['max_strict_threshold']
    assert report['minimum_slack_q22'] == str(min(F(gap['q22_value']) for _, gap in previous_rows.values()))
    assert ''.join(LABEL[a] for a in report['path']) == previous['path']
    affine_matches.append(dict(players=m, matched_nonself_rows=len(original_rows), all_chosen_alpha_beta_q22_equal=True, complete_policy_equal=True, threshold=previous['max_strict_threshold'], minimum_slack_q22=report['minimum_slack_q22']))

policy_differences = {}
for left, right in [('thirteen_m3', 'strict_forty_m3'), ('thirteen_m3', 'q_m3'), ('strict_forty_m3', 'q_m3')]:
    a, b = policies[left], policies[right]
    policy_differences[f'{left} -> {right}'] = [dict(history=h, before=a[h], after=b[h]) for h in a if a[h] != b[h]]

out = dict(kind='data/schema cross-check against already completed independent definition audit; no new payoff/BI/LP evaluation', inputs=read_files, existing_definition_run_not_reexecuted=True, original_entries_replayed_separately_once_each=True, certificate_checks=certificates, finite_matches=finite_matches, affine_matches=affine_matches, distinct_m3_policy_differences=policy_differences, tiny_catalog_difference='Original population entry uses four topics A/B/C/D, D empty. Existing formal witness uses three topics A/B/C. Adding D is safe here: last D gets zero versus a positive action; root D gets zero. No tiny BI rerun by this comparison.', original_family_main_assertion_limit='It verifies each affine IC and the path labels; closed-form welfare/OPT claims are string metadata plus partial total checks, whose mathematics is supplied by the existing self-contained proof.')
(HERE/'output.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(dict(status='passed', legal_full_certificates=4, certificate_nodes=sum(r['nodes'] for r in certificates), forty_action_payoff_entries=104, matched_affine_rows=78, independent_definition_entry_runs_this_batch=0, new_payoff_or_BI_evaluations=0)))
