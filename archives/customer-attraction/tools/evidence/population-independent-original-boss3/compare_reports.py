"""Only compare already computed reports and hard-coded input constants.
No import or execution of an audit, no payoff, BI, policy export or LP.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('--repository-root', type=Path, required=True)
args = p.parse_args()
inputs = []


def read(path):
    b = path.read_bytes()
    inputs.append(dict(path=str(path), size=len(b), sha256=hashlib.sha256(b).hexdigest()))
    return json.loads(b)


parent = read(HERE/'original/population_independent_audit.json')
other = read(args.repository_root/'archives/customer-attraction/tools/evidence/population-exchange-family-boss3/original/population_exchange_audit.json')
old = read(args.repository_root/'archives/customer-attraction/tools/evidence/maximal-population-and-ordered-compression-primary/new-definition-audit/output.json')
source = (HERE/'original/population_independent_audit.py').read_bytes()
inputs.append(dict(path=str(HERE/'original/population_independent_audit.py'), size=len(source), sha256=hashlib.sha256(source).hexdigest()))
tree = ast.parse(source)
main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
weights = {n.targets[0].id: ast.literal_eval(n.value) for n in main.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ['small', 'strict']}
matched = []
for name, othername in [('small', 'thirteen'), ('strict', 'strict_forty')]:
    author = next(x for x in other['examples'] if x['name'] == othername)
    masks = {sum(1 << 'ABCD'.index(a) for a in row['topics']): row['multiplicity'] for row in author['types']}
    assert weights[name] == masks
    assert [r['players'] for r in parent[name]] == [1, 2, 3, 4]
    for r in parent[name]:
        m = r['players']
        assert r['nodes'] == sum(4**d for d in range(m))
        assert r['comparisons_including_self'] == 4*r['nodes']
        assert r['total_customers'] == sum(weights[name].values())
        if m in [2, 3]:
            a = author['players'][str(m)]
            assert r['all_terminal_counts'] == a['all_SPE_terminal_counts']
            for pk, ak in [('minimum_welfare', 'minimum_SPE_welfare'), ('optimum', 'OPT'), ('nodes', 'nodes'), ('comparisons_including_self', 'comparisons'), ('all_comparisons_strict', 'all_nodes_strict'), ('minimum_gap', 'minimum_nonself_slack')]:
                assert r[pk] == a[ak], (name, m, pk)
            assert ''.join('ABCD'[a] for a in r['audited_path']) == a['path']
            if name == 'small':
                d = old['thirteen'][str(m)]
                assert r['all_terminal_counts'] == d['terminal_counts']
                assert r['minimum_welfare'] == d['minimum_W'] and r['optimum'] == d['OPT']
            else:
                d = old['forty'][str(m)]
                assert r['minimum_welfare'] == d['W'] and r['optimum'] == d['OPT']
                assert r['minimum_gap'] == d['min_nonself_slack']
            matched.append(dict(instance=name, players=m, all_common_report_fields_equal=True, full_selected_policy_compared=False, reason='parent report does not store complete policy or per-node values'))

out = dict(kind='data/schema reconciliation only', inputs=inputs, exact_bitmask_inputs_equal_to_author=True, common_m2_m3=matched, original_unique_finite_extensions={name:[r for r in rows if r['players'] in [1, 4]] for name, rows in parent.items()}, nodes_across_eight_audits=sum(r['nodes'] for rows in parent.values() for r in rows), comparisons_including_self_across_eight_audits=sum(r['comparisons_including_self'] for rows in parent.values() for r in rows), new_BI_payoff_or_policy_export_runs=0, all_comparisons_strict_field_means_nonself_only=True, no_q_family_in_this_entry=True)
(HERE/'comparison-output.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(dict(status='passed', shared_summary_cases=4, new_finite_extension_cases=4, total_nodes=224, comparisons_including_self=896, new_BI_runs=0)))
