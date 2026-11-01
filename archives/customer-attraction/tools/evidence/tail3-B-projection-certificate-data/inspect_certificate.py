"""Inspect frozen data and existing evidence; never rebuild hidden projections.

This reads the full 448-cell certificate and the old point's histogram margin.
It does not import the author, parent auditor, or previous 21504-state auditor.
"""
import argparse
import ast
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path
import sys

BASE = Path('archives/customer-attraction/tools/evidence')
BODY = Path('archives/customer-attraction/state/计算/实际末主题三人尾的四百四十八格投影证书--计算.md')
WEIGHTS = {'F':3360,'G':96,'H2Q':660,'H2R':595,'H3R':220,'LQ':522,'LR':522,'E':108}
CERT_SHA = '4d34cd746ce35dd48827c9014a85106c5defac30fc5f1159ae6085d4fd8fa1df'
POINT_SHA = '24a2f9fa7e7a47e26e065b41ada98e1788a5b448251fb8c1e881557c1f7c9f11'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect(repo):
    shared = repo/BASE/'tail3-B-projection-program'
    parent = repo/BASE/'tail3-B-parent-menu-auditor'
    cert_path = shared/'related/tail3_B_projection_certificate.json'
    point_path = shared/'related/full_new_reply_closure_exact.json'
    cert = json.loads(cert_path.read_text())
    point = json.loads(point_path.read_text())
    assert cert_path.stat().st_size == 36617 and sha(cert_path) == CERT_SHA
    assert point_path.stat().st_size == 56652 and sha(point_path) == POINT_SHA
    assert list(cert) == ['status','weights','coefficient_domain','old_point_path',
                          'old_point_sha256','old_point_value','old_point_value_decimal','table']
    assert cert['status'] == 'EXACT_VALID_NECESSARY_PROJECTION_AND_OLD_POINT_SEPARATION_ONLY'
    assert cert['weights'] == WEIGHTS and all(type(x) is int and x > 0 for x in WEIGHTS.values())
    assert cert['coefficient_domain'] == {'actual_bit_patterns':64,'d_values':list(range(7)),
        'hidden_QR_patterns':4,'ell_values':list(range(7)),'endpoint_replay_matches_full':True}
    assert cert['old_point_path'] == 'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/full_new_reply_closure_exact.json'
    assert cert['old_point_sha256'] == POINT_SHA
    table = cert['table']
    expected_keys = [(''.join(map(str,a)),d) for a in product((0,1),repeat=6) for d in range(7)]
    assert len(table) == 448 and [(x['actual_bits'],x['d']) for x in table] == expected_keys
    for x in table:
        assert list(x) == ['actual_bits','d','psi'] and type(x['d']) is int
        assert type(x['psi']) is str and str(F(x['psi'])) == x['psi']
    lookup = {(x['actual_bits'],x['d']):F(x['psi']) for x in table}
    values = list(lookup.values())
    counts = Counter('positive' if v > 0 else 'negative' if v < 0 else 'zero' for v in values)
    assert counts == {'positive':269,'negative':176,'zero':3} and len(set(values)) == 423
    decreasing = all(lookup[a,d] > lookup[a,d+1] for a,d in expected_keys if d < 6)
    assert decreasing
    rendered = []
    for line in (repo/BODY).read_text().splitlines():
        if not line.startswith('| '):
            continue
        parts = [x.strip() for x in line.strip('|').split('|')]
        if len(parts) == 8 and len(parts[0]) == 6 and set(parts[0]) <= {'0','1'}:
            rendered.extend({'actual_bits':parts[0],'d':d,'psi':v} for d,v in enumerate(parts[1:]))
    assert rendered == table
    hist_rows = []
    masses = defaultdict(F)
    for index,c in enumerate(point['columns']):
        if c['kind'] != 'hist':
            continue
        assert len(c['actual_bits']) == 6 and set(c['actual_bits']) <= {'0','1'}
        assert type(c['d']) is int and c['d'] in range(7)
        assert len(c['hist']) == 8 and all(type(v) is int and v >= 0 for v in c['hist'])
        assert sum(c['hist']) == 6 and sum(c['hist'][4:]) == c['d']
        mass = F(c['weight']); assert mass >= 0
        masses[c['actual_bits'],c['d']] += mass
        hist_rows.append({'column':index,**c})
    assert len(hist_rows) == 16 and sum(masses.values()) == 1
    contributions = [{'actual_bits':a,'d':d,'mass':str(m),'psi':str(lookup[a,d]),
                      'contribution':str(m*lookup[a,d])}
                     for (a,d),m in sorted(masses.items()) if m]
    exact = sum((F(x['contribution']) for x in contributions),F())
    assert len(contributions) == 8 and exact == F(cert['old_point_value']) < 0
    assert float(exact) == cert['old_point_value_decimal']
    W = sum(m for (a,d),m in masses.items() if '1' in a)
    O = sum(m for (a,d),m in masses.items() if d)
    assert W == F(point['W']) and O == F(point['O']) == 1
    assert F(point['strict_half_gap']) == O-2*W
    prior = json.loads((shared/'independent-audit.json').read_text())
    assert prior['hist_rows'] == hist_rows and prior['old_point_contributions'] == contributions
    assert prior['raw_overlap_states'] == 21504 and prior['QR_ell_states'] == 12544 and prior['visible_cells'] == 448
    assert all(prior[k] is True for k in ('all_448_coefficients_and_order_equal',
        'overlap_cancels_in_G','endpoint_equals_full_in_every_visible_cell'))
    assert prior['certificate_sha256'] == CERT_SHA and prior['old_point_sha256'] == POINT_SHA
    assert prior['audit_sha256'] == sha(shared/'audit_raw_menu.py')
    author = json.loads((shared/'rerun/execution.json').read_text())
    assert author['exit_code'] == 0 and author['certificate_byte_equal_frozen']
    assert (shared/'rerun/tail3_B_projection_certificate.json').read_bytes() == cert_path.read_bytes()
    assert sha(shared/'rerun/stdout.json') == author['stdout_sha256']
    assert json.loads((shared/'rerun/stdout.json').read_text()) == {k:v for k,v in cert.items() if k != 'table'}
    assert (shared/'rerun/stderr.txt').stat().st_size == 0
    event = json.loads((parent/'rerun/execution.json').read_text())
    output = json.loads((parent/'rerun/stdout.json').read_text())
    assert event['exit_code'] == 0 and sha(parent/'rerun/stdout.json') == event['stdout_sha256']
    assert (parent/'rerun/stderr.txt').stat().st_size == 0
    assert output == {'states':21504,'visible_types':448,'point_value':str(exact),'old_sha256':POINT_SHA}
    review = repo/BASE/'actual-last-theme-families-and-menu-prices-primary/related-small-original/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/tail3_B_projection_review.json'
    historical = json.loads(review.read_text())
    assert historical['raw_states_with_overlap'] == output['states'] and historical['visible_types'] == output['visible_types']
    assert historical['old_point_value'] == str(exact) and historical['old_point_sha256'] == POINT_SHA
    assert (parent/'rerun/stdout.json').read_bytes() != review.read_bytes()
    code = ast.parse((shared/'original/tail3_B_projection.py').read_text())
    assignment = next(n for n in code.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id == 'WEIGHTS' for t in n.targets))
    assert ast.literal_eval(assignment.value) == WEIGHTS
    filelist = [cert_path,point_path,shared/'original/tail3_B_projection.py',shared/'related/audit_tail3_B_projection.py',
        shared/'audit_raw_menu.py',shared/'independent-audit.json',shared/'rerun/execution.json',
        shared/'rerun/tail3_B_projection_certificate.json',shared/'rerun/stdout.json',parent/'rerun/execution.json',
        parent/'rerun/stdout.json',review]
    return {'status':'PASS_DATA_CONTENT_AND_RETAINED_EVIDENCE_CHECK',
        'scope':'No author export, parent audit, hidden-state reconstruction or whole-graph entry was executed.',
        'certificate_top_fields':list(cert),'weights':cert['weights'],'coefficient_domain':cert['coefficient_domain'],
        'complete_unique_ordered_cells':448,'canonical_fraction_strings':True,'all_448_body_cells_equal_frozen':True,
        'coefficient_sign_counts':dict(counts),'distinct_coefficients':len(set(values)),
        'denominator_counts':{str(k):v for k,v in sorted(Counter(v.denominator for v in values).items())},
        'minimum':str(min(values)),'minimum_keys':[[a,d] for (a,d),v in lookup.items() if v == min(values)],
        'maximum':str(max(values)),'maximum_keys':[[a,d] for (a,d),v in lookup.items() if v == max(values)],
        'zero_keys':[[a,d] for (a,d),v in lookup.items() if not v],
        'all_64_d_rows_strictly_decreasing':decreasing,
        'old_point_column_kinds':dict(Counter(c['kind'] for c in point['columns'])),
        'hist_count':len(hist_rows),'positive_hist_count':sum(F(x['weight'])>0 for x in hist_rows),
        'hist_records_equal_prior_independent_report':True,'positive_visible_margins':len(contributions),
        'total_hist_mass':'1','O':str(O),'W':str(W),'old_point_contributions':contributions,
        'old_point_value':str(exact),'old_point_decimal_matches_exact_display':True,
        'author_event_and_byte_equal_certificate_retained':True,'parent_event_and_four_output_fields_retained':True,
        'historical_review_corresponding_fields_equal_not_byte_equal':True,
        'prior_21504_state_independent_report_and_code_hash_retained':True,
        'new_author_entry_invocations':0,'new_parent_entry_invocations':0,
        'new_hidden_state_audit_invocations':0,'new_whole_graph_entry_invocations':0,
        'files':[{'path':str(p.relative_to(repo)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in filelist],
        'not_certified':['all old 1033 inequalities','1097/3889 extension bytes',
            'realizability of each hidden maximizer','complete SPE','six-player half theorem']}


if __name__ == '__main__':
    if sys.flags.optimize:
        raise RuntimeError('Assertions must remain enabled')
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True)
    args = ap.parse_args()
    print(json.dumps(inspect(args.repo.resolve()),ensure_ascii=False,indent=2))
