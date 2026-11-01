"""Static report/source/observation checks; no source import, rank, basis or payoff run."""
import ast
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
EVIDENCE = HERE.parent
PROGRAM = EVIDENCE / 'fixed-background-circuit-audit-program'
BASIS = EVIDENCE / 'fixed-background-circuit-basis'
BODY = ROOT / 'archives/customer-attraction/state/计算/固定背景收益切片的有限秩与核基审计--计算.md'
SID = 'c3bd87a3e8bc0d0b312e'


def read(path):
    return json.loads(path.read_text())


def fingerprint(path):
    b = path.read_bytes()
    return dict(path=str(path.relative_to(ROOT)), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def inspect_saved_report():
    raw = (HERE/'original/fixed_background_audit.json').read_bytes()
    report = json.loads(raw)
    assert raw == (PROGRAM/'replay/fixed_background_audit.json').read_bytes()
    assert list(report) == ['status', 'identity', 'scope', 'cases', 'case_count',
        'four_slot_cases', 'circuit_vectors_checked', 'all_backgrounds_include_zero_load',
        'aggregate_cases', 'aggregate_case_count', 'aggregate_circuit_vectors_checked',
        'all_unit_cases', 'all_unit_case_count', 'six_row_parameter_cases']
    assert report['status'] == 'passed' and report['all_backgrounds_include_zero_load'] is True
    assert report['identity'] == 'FB-RANK / FB-BASIS / FB-FOUR'
    assert report['scope'] == 'Finite definition-level audit; general proof is in manuscript.'
    backgrounds = [[], [1], [2], [5], [1,1], [1,2], [2,2], [1,3],
                   [1,1,1], [1,2,4], [2,3,5], [1,1,1,1]]
    schemas = {
        'cases': ['M','background','m','loads','d','customer_patterns','rank','complete_basis_size'],
        'aggregate_cases': ['M','background','d','rows','rank','complete_basis_size'],
        'all_unit_cases': ['M','k','rows','rank','kernel_dimension']}
    sizes = {'cases':96, 'aggregate_cases':77, 'all_unit_cases':14}
    for name, fields in schemas.items():
        assert len(report[name]) == sizes[name]
        assert all(list(row) == fields for row in report[name])
    assert [(c['background'],c['M']) for c in report['cases']] == [(v,M) for v in backgrounds for M in range(1,9)]
    assert [(c['background'],c['M']) for c in report['aggregate_cases']] == [(v,M) for v in backgrounds[1:] for M in range(2,9)]
    assert [(c['M'],c['k']) for c in report['all_unit_cases']] == [(M,k) for M in range(2,6) for k in range(M,7)]
    assert report['case_count'] == 96 and report['aggregate_case_count'] == 77
    assert report['all_unit_case_count'] == 14 and report['four_slot_cases'] == 165
    assert report['six_row_parameter_cases'] == 8
    assert sum(c['complete_basis_size'] for c in report['cases']) == report['circuit_vectors_checked'] == 265
    assert sum(c['complete_basis_size'] for c in report['aggregate_cases']) == report['aggregate_circuit_vectors_checked'] == 546
    profiles = {}
    for family in ['cases', 'aggregate_cases']:
        profiles[family] = {}
        for v in backgrounds if family == 'cases' else backgrounds[1:]:
            rows = [c for c in report[family] if c['background'] == v]
            profiles[family][str(v)] = dict(d=rows[0]['d'], M=[c['M'] for c in rows],
                rank=[c['rank'] for c in rows], basis=[c['complete_basis_size'] for c in rows])
    obs_raw = gzip.decompress((PROGRAM/'replay/original-observations.json.gz').read_bytes())
    obs = json.loads(obs_raw)
    summary = read(PROGRAM/'replay/observation-summary.json')
    assert len(obs_raw) == 842445
    mapping = {'base':'cases','aggregate':'aggregate_cases','all_unit':'all_unit_cases'}
    for family, key in mapping.items():
        assert [x['returned'] for x in obs[family]] == report[key]
    assert [(x['bg'],x['r'],x['s']) for x in obs['four']] == [(v,r,s) for v in backgrounds[1:] for r in range(2,7) for s in range(1,r)]
    assert [x['k'] for x in obs['six']] == list(range(1,9))
    assert all(x['returned'] == 1 for family in ['four','six'] for x in obs[family])
    totals = {}
    for family, records in obs.items():
        entries = vectors = coefficients = 0
        for item in records:
            matrix, basis = item.get('rows', []), item.get('circuits', [])
            if matrix:
                columns = len(item['patterns'])
                assert all(len(row) == columns for row in matrix)
                assert item['patterns'][0] == [0]*len(item['patterns'][0])
                assert all(row[0] == '0' for row in matrix)
                assert all(len(row) == len(matrix) for row in basis)
                for row in matrix + basis:
                    for value in row:
                        assert str(Fraction(value)) == value
                entries += sum(map(len,matrix))
                vectors += len(basis)
                coefficients += sum(map(len,basis))
        totals[family] = dict(calls=len(records), matrix_entries_serialized=entries,
            basis_vectors_serialized=vectors, basis_coefficients_serialized=coefficients)
        assert {k:v for k,v in summary[family].items() if k != 'returned_records'} == totals[family]
        assert summary[family]['returned_records'] == [x['returned'] for x in records]
    assert sum(x['matrix_entries_serialized'] for x in totals.values()) == 116096
    assert sum(x['basis_vectors_serialized'] for x in totals.values()) == 811
    assert sum(x['basis_coefficients_serialized'] for x in totals.values()) == 14545
    event = read(PROGRAM/'replay/execution.json')
    process = read(PROGRAM/'replay/process-capture.json')
    assert process['returncode'] == 0 and event['assertions_enabled']
    assert event['source_before'] == event['source_after']
    assert event['original_function_call_events']['main'] == 1
    assert event['original_function_call_events']['rank'] == 525
    for field in ['helper_replacements','additional_original_helper_calls','optimization_calls','SPE_solver_calls','new_independent_mathematical_audits']:
        assert event[field] == 0
    stdout = read(PROGRAM/'replay/stdout.txt')
    assert stdout == {k:v for k,v in report.items() if k not in schemas}
    assert (PROGRAM/'replay/stderr.txt').read_bytes() == b''
    independent = read(BASIS/'related/fixed_background_rank_review.json')
    assert [independent[k] for k in ['background_M_cases','nullspace_basis_vectors','four_slot_cases','aggregate_background_rank_cases','all_unit_background_cases']] == [152,406,270,90,8]
    return dict(status='PASS', scope='Saved-field and serialization checks only, no ranks or identities recomputed',
        original_top_fields=14, original_array_records=187, schemas=schemas, backgrounds=backgrounds,
        saved_rank_profiles=profiles, shared_observation_totals=totals,
        historical_independent_review=independent, new_original_entries=0, new_rank_calls=0,
        new_basis_or_payoff_calls=0, new_optimizer_calls=0, new_independent_mathematical_entries=0)


def main():
    sources = read(HERE/'source-manifest.json')['sources']
    for source in sources:
        p = ROOT/source['preserved_path']
        b = p.read_bytes()
        assert len(b) == source['size'] and hashlib.sha256(b).hexdigest() == source['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() == source['blob']
    report = inspect_saved_report()
    save(HERE/'schema-review.json', report)
    review = read(HERE/'review-record.json')
    for item in review['bindings']:
        assert fingerprint(ROOT/item['path']) == item
    for p in HERE.glob('*.py'):
        ast.parse(p.read_text())
    for p in HERE.rglob('*.json'):
        if p.name != 'self-check.json':
            read(p)
    links = []
    for p in [BODY, HERE/'README.md']:
        s = p.read_text()
        assert not any(ord(c)<32 and c not in '\n\t' for c in s)
        assert s.endswith('\n') and not s.endswith('\n\n')
        assert all(line.rstrip()==line for line in s.splitlines())
        for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)', s):
            if '://' in link or link.startswith('#'):
                continue
            target = (p.parent/link.split('#',1)[0]).resolve()
            assert target.exists(), (str(p),link)
            links.append(dict(source=str(p.relative_to(ROOT)), target=str(target.relative_to(ROOT))))
    front = BODY.read_text().split('---',2)[1]
    for field in ['id','kind','type_tag','title','status','summary','source_refs']:
        assert re.search('^'+field+':',front,re.M)
    receipt_path = ROOT/'cleanup/workspaces/Boss7/receipts-round17'/f'{SID}.json'
    receipt = read(receipt_path)
    assert receipt['id']==SID and receipt['disposition']=='integrated'
    assert receipt['full_file_reviewed'] and receipt['related_material_checked'] and receipt['unique_content_accounted_for']
    assert all((ROOT/p).exists() or ROOT/p == HERE/'self-check.json' for p in receipt['targets'])
    files = [fingerprint(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name != 'self-check.json']
    result = dict(status='PASS', scope='Static package check; no mathematical audit repeated',
        sources_verified=len(sources), comparison_and_shared_bindings=len(review['bindings']),
        report_top_fields=14, report_array_records=187, captured_rational_values_parsed=130641,
        owned_fingerprints=files, body=fingerprint(BODY), receipt=fingerprint(receipt_path),
        links_checked=len(links), links=links, original_entries=0, rank_calls=0, optimizer_calls=0)
    save(HERE/'self-check.json', result)
    assert all((ROOT/p).exists() for p in receipt['targets'])
    print(json.dumps({k:v for k,v in result.items() if k not in ['owned_fingerprints','links']},ensure_ascii=False))


if __name__ == '__main__':
    main()
