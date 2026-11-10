"""Read-only frozen-template/budget/archived-certificate identity checks.

Does not construct coefficients, evaluate hidden minima, import old generators,
run LPs, reconstruct the necessary graph, or repeat archived numerical audits.
"""
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def verify(repo):
    ev = repo / 'archives/customer-attraction/tools/evidence'
    paths = {
        'nested': ev / 'nested-reply-projection-cut-data/original/nested_reply_cuts.json',
        'v2': ev / 'local-reply-portfolio-joint-cuts/original/joint_local_v2_cuts.json',
        'base': ev / 'local-reply-joint-cuts/original/joint_local_cuts.json',
        'nested_audit': ev / 'nested-reply-projection-cut-data/five-cut-definition-audit.json',
        'joint_audit': ev / 'local-reply-portfolio-joint-cuts/exact-audit.json',
        'base_audit': ev / 'local-reply-joint-cuts/base-table-definition-audit.json',
        'nested_audit_code': ev / 'nested-reply-projection-cut-data/audit_five_cuts.py',
        'joint_audit_code': ev / 'local-reply-portfolio-joint-cuts/audit_joint_cuts.py',
        'base_audit_code': ev / 'local-reply-joint-cuts/audit_base_table.py',
        'point': ev / 'nested-reply-projection-program/related/combined_branch_latest_exact.json',
        'interface': ev / 'nested-reply-projection-program/input-interface-report.json',
    }
    expected = {
        'nested': '933a18540d8ea69058cf5e23f999c17b5c69bda7624c817a9e0034fca2f97295',
        'v2': '49aaf81f49aac3b544cf38ed97efdb6fa1849e1c810ff1705b7dd313052017a1',
        'base': '891561660fda75c722b970082f4f16fd7a65e2dc8fb368f35ec5e54b047183da',
        'nested_audit': '2887edc052ad8d775d44818bcd88b0664ed516eadc4c0acd1ff702ae380cc7b1',
        'joint_audit': '63f801c55d6f4be32bf939e22d01b519e577c6c258a80e987cda269cce458c6f',
        'base_audit': '2a0afe163cba17f506e702c09927e53fbd6d71724c25d6083f3ff9f0ad45b8a6',
        'point': '50d51fadd1bd5cc6f2eb2230f1c35ac7001e21a5a75d11e91f4e259c1bf69224',
        'interface': 'bb4afb74cf5f004073b03caba9ee963e23f09dac6829a61e8709a26ebe8aa057',
    }
    for key, value in expected.items():
        assert sha(paths[key]) == value, key
    data = {k: json.loads(paths[k].read_text()) for k in
            ('nested', 'v2', 'base', 'nested_audit', 'joint_audit', 'base_audit', 'interface')}
    nested, v2, base = (data[k] for k in ('nested', 'v2', 'base'))
    na, ja, ba = (data[k] for k in ('nested_audit', 'joint_audit', 'base_audit'))
    for name, cert in (('nested', na), ('joint', ja), ('base', ba)):
        assert cert['audit_sha256'] == sha(paths[name + '_audit_code'])
    assert set(v2) == {'scope', 'nested', 'requery', 'portfolio'}
    assert [len(v2[k]) for k in ('nested', 'requery', 'portfolio')] == [5, 5, 8]
    assert nested['selected'] == v2['nested'] == base['nested']
    assert v2['requery'][:4] == base['requery']
    assert nested['source_sha256'] == expected['point'] == data['interface']['sha256']
    assert ja['inputs']['point']['sha256'] == expected['point']
    assert ja['inputs']['joint']['sha256'] == expected['v2']
    assert ja['inputs']['nested_audit']['sha256'] == expected['nested_audit']
    assert ja['inputs']['input_interface']['sha256'] == expected['interface']
    assert data['interface']['bytes'] == paths['point'].stat().st_size == 823005
    nested_summary = []
    for cut, saved in zip(v2['nested'], na['all_five_cuts']):
        assert all(F(x) >= 0 for x in cut['weights'].values())
        assert sum(map(F, cut['weights'].values())) == 1
        assert cut['weights'] == saved['weights']
        assert F(cut['slack']) == F(saved['exact_slack']) < 0
        assert saved['K_coefficient'] == '0' and not saved['depends_on_single_Y']
        nested_summary.append({'member': cut['member'], 'orb': cut['orb'],
                               'K_coefficient': '0', 'weights_sum': '1',
                               'stored_negative_slack': cut['slack']})
    pars = tuple(map(F, ('4/7', '1/7', '1/14', '3/28', '1/28', '2/7')))
    assert [(x['member'], x['orb']) for x in v2['requery']] == [
        (1, [1, 0]), (1, [0, 0]), (1, [1, 1]), (0, [1, 0]), (0, [0, 0])]
    for cut in v2['requery']:
        assert cut['i'] == 3 and cut['query'] == 5
        assert tuple(map(F, cut['parameters'])) == pars
    budgets = []
    expected_last = list(map(F, ('61/360', '41/225', '5/32', '2/13', '7/36', '5/16', '61/360', '5/16')))
    for pos, cut in enumerate(v2['portfolio']):
        mus = tuple(map(F, cut['mu']))
        assert len(mus) == 13 and sum(bool(x) for x in mus) == 1 and min(mus) >= 0
        n = 5-cut['i']
        am, al, bm, bl = (F(cut[k]) for k in ('alpha_middle', 'alpha_last', 'beta_middle', 'beta_last'))
        assert min(am, al, bm, bl) >= 0 and bm == 0
        last, cap = (n-1)*am+al, (n-1)*bm+bl
        assert last == expected_last[pos]
        qi = next(i for i, v in enumerate(mus) if v)
        budgets.append({'position': pos, 'source_i_zero_based': cut['i'], 'tail_n': n,
                        'single_query_slot': qi, 'mu': str(mus[qi]),
                        'source_budget': '1', 'actual_last_budget': str(last),
                        'K_budget': str(cap), 'compressed_candidates': 2*n,
                        'mu_16_tail_zero_padding': ['0', '0', '0']})
    rows = []
    assert len(ja['all_rows']) == 18
    for family in ('nested', 'requery', 'portfolio'):
        cert_rows = [r for r in ja['all_rows'] if r['family'] == family]
        assert [r['cut'] for r in cert_rows] == v2[family]
        for r in cert_rows:
            assert F(r['exact_slack_on_frozen_5180_point']) < 0
            if family == 'nested': expected_cap = F()
            elif family == 'requery': expected_cap = pars[4]
            else: expected_cap = F(budgets[r['position']]['K_budget'])
            assert F(r['K_coefficient']) == expected_cap
            rows.append({k: r[k] for k in ('family', 'position', 'global_position', 'K_coefficient',
                         'row_sha256', 'exact_slack_on_frozen_5180_point', 'slack_origin')})
    assert len({r['row_sha256'] for r in rows}) == 18
    return {
        'status': 'PASS_FROZEN_TEMPLATE_BUDGET_AND_ARCHIVED_CERTIFICATE_CONTRACT_ONLY',
        'scope': 'New small exact metadata/template/budget comparison; archived minima, coefficient vectors, and fixed-point evaluation are reused, not rerun.',
        'inputs': {k: {'path': str(p.relative_to(repo)), 'sha256': sha(p), 'bytes': p.stat().st_size} for k, p in paths.items()},
        'nested_templates_equal_in_all_three_files': True,
        'base_requery_four_equal_first_four_of_current_five': True,
        'nested_five': nested_summary,
        'requery_budget': {'source': str(pars[0] + 1-pars[0]), 'actual_last': str(pars[2]+pars[3]), 'K': str(pars[4]),
                          'first_source_weight': str(pars[0]), 'second_source_weight': str(1-pars[0]),
                          'six_parameter_sum_not_simplex': str(sum(pars))},
        'portfolio_eight_budgets': budgets,
        'reused_joint_eighteen_row_summaries': rows,
        'reused_certificate_scope': {'nested': '120 coefficients/5760 literal intersection states',
                                   'base_requery': '48 minima/768 literal states and four fixed-point diagnostics',
                                   'joint': '1536 P actual-input comparisons/12800 literal P states; 24 R minima/384 R states; 34290 coefficients'},
        'new_runs': {'LPs': 0, 'old_graphs': 0, 'hidden_minimum_or_maximum_evaluations': 0,
                     'row_coefficient_reconstructions': 0, 'new_fixed_point_dot_products': 0},
        'not_certified': ['new necessary-graph infeasibility or optimum', 'rank 18', 'full query/parameter closure',
                          'joint directory realization', 'complete-history SPE', 'six-player half'],
    }


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python -B verify-template-contract.py REPO OUTPUT')
    report = verify(Path(sys.argv[1]).resolve())
    output = Path(sys.argv[2]).resolve()
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'status': report['status'], 'output': str(output), 'sha256': sha(output)}, ensure_ascii=False))
