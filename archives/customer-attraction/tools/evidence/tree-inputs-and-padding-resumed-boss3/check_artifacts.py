"""Asset/hash/link/table checks only; no payoff, IC, LP or BI evaluation."""
from pathlib import Path
import ast
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
RECORD = REPO/'cleanup/workspaces/Boss3/resume-20261102/a6'


def main():
    source = json.loads((HERE/'source-manifest.json').read_text())
    receipts = json.loads((RECORD/'semantic-receipts.json').read_text())
    delivery = json.loads((RECORD/'delivery.json').read_text())
    assert len(source) == len(receipts) == 16
    assert len({x['id'] for x in source}) == 16
    assert {x['id'] for x in source} == {x['id'] for x in receipts}
    payload = {}
    byname = {}
    py = js = md = 0
    for x in source:
        p = REPO/x['evidence_path']
        raw = p.read_bytes()
        assert len(raw) == x['size']
        assert hashlib.sha256(raw).hexdigest() == x['sha256']
        byname[p.name] = x
        if p.suffix == '.py':
            ast.parse(raw.decode(), filename=x['path'])
            py += 1
        elif p.suffix == '.json':
            payload[p.name] = json.loads(raw)
            js += 1
        elif p.suffix == '.md':
            md += 1
    for x in receipts:
        for k in ('full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for'):
            assert x[k] is True
        for k in ('read_note', 'comparison_note', 'decision_note'):
            assert x[k]
        assert x['disposition'] == 'integrated'
        for p in x['targets']:
            assert (REPO/p).is_file()
    docs = [REPO/p for p in delivery['formal_objects']]
    ids = []
    links = 0
    for p in docs+[HERE/'README.md']:
        text = p.read_text()
        assert '<!--' not in text
        if p in docs:
            assert text.startswith('---\n')
            head = text.split('---', 2)[1]
            for k in ('id', 'kind', 'type_tag', 'title', 'status', 'summary', 'source_refs'):
                assert re.search('^'+k+':', head, re.M), (p, k)
            ids.append(re.search('^id: (.+)', head, re.M).group(1))
        for href in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
            if '://' not in href and not href.startswith('#'):
                assert (p.parent/href.split('#', 1)[0]).resolve().exists(), (p, href)
                links += 1
    assert len(set(ids)) == 4
    core = payload['generic_padding_failure_exact.json']['core_certificate']['actions']
    old = {tuple(x['history']): x['action'] for x in core}
    assert len(core) == len(old) == 21
    counter = next(p for p in docs if p.name.startswith('不交双'))
    table = re.findall(r'^\|([0-3])\|([0-3])\|([0-3])\|([0-3])\|([0-3])\|$', counter.read_text(), re.M)
    assert len(table) == 4
    decoded = {(int(a), b): int(value) for a, *values in table for b, value in enumerate(values)}
    assert decoded == {h: v for h, v in old.items() if len(h) == 2}
    qa = payload['audit_full_actual_branch_inputs.json']
    assert qa['tested_row_module_sha256'] == byname['two_real_weighted_branches.py']['sha256']
    hinge = payload['hinge_independent_audit.json']
    assert hinge['source_sha256'] == byname['exact_projected_hinge.json']['sha256']
    cases = [c for i in qa['inputs'] for c in i['cases']]
    assert len(qa['inputs']) == 3 and len(cases) == 4
    assert all(len(c['exact_row_slacks']) == 747 for c in cases)
    related = json.loads((HERE/'related-reading.json').read_text())
    old_input = next(x for x in related if x['path'].endswith('/weighted_maximum_old_refund_obstruction.json'))
    ten_input = next(x for x in related if x['path'].endswith('/terminal_share_padding_exact.json'))
    assert qa['inputs'][0]['source_sha256'] == old_input['sha256_at_record']
    assert qa['inputs'][1]['source_sha256'] == ten_input['sha256_at_record']
    assert qa['inputs'][2]['source_sha256'] is None
    rawpoint = payload['exact_projected_hinge.json']
    assert len(rawpoint['atoms']) == len(hinge['atom_projection_records']) == 57
    assert len(rawpoint['source_row_slacks']) == 5421
    report = {'status': 'PASS', 'source_files': len(source),
        'source_bytes': sum(x['size'] for x in source), 'python_AST_only': py,
        'JSON_parsed': js, 'original_MD': md, 'formal_docs': len(docs),
        'local_links': links, 'receipts': len(receipts), 'core_last_table_entries_lossless': len(decoded),
        'QA_input_hashes_bound': 2, 'QA_cases': len(cases),
        'named_QA_slack_fields_present': sum(len(c['exact_row_slacks']) for c in cases),
        'hinge_atom_fields_present': len(rawpoint['atoms']), 'stored_old_row_fields_present': len(rawpoint['source_row_slacks']),
        'original_math_program_runs': 0, 'new_math_checker_runs': 0,
        'scope': 'source identity, syntax, links, schema and lossless table; no mathematical execution'}
    for p in (HERE/'artifact-check.json', RECORD/'self-check.json'):
        p.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
