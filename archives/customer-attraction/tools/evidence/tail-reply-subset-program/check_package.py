"""Static package check only; never import or execute mathematical programs."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from collections import Counter
import ast
import json
import re

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]


def main():
    manifest = json.loads((HERE / 'source-manifest.json').read_text())
    for item in manifest['shared_sources']:
        b = (REPO / item['stored_path']).read_bytes()
        assert len(b) == item['size'] and sha256(b).hexdigest() == item['sha256']
    prior = manifest['existing_5075_verify_event']
    assert sha256((REPO / prior['stored_path']).read_bytes()).hexdigest() == prior['sha256']
    for name, record in manifest['artifact_hashes'].items():
        b = (HERE / name).read_bytes()
        assert len(b) == record['bytes'] and sha256(b).hexdigest() == record['sha256']
    old = (HERE / 'attempt1.py').read_text()
    corrected = old.replace('original_states_calls == 192 and original_rows_calls == 576', 'original_states_calls == 96 and original_rows_calls == 288').replace('192 structures', '96 structures').replace('state_mass_one_in_all_192_structures', 'state_mass_one_in_all_96_structures')
    assert corrected == (HERE / 'audit_helpers.py').read_text()
    failure = json.loads((HERE / 'failed-attempt.json').read_text())
    assert failure['exit_code'] == 1
    assert failure['script_sha256'] == sha256((HERE / 'attempt1.py').read_bytes()).hexdigest()
    audit = json.loads((HERE / 'helper-audit.json').read_text())
    assert audit['status'] == 'PASS_FINITE_EXACT_ORIGINAL_HELPER_CONTRACTS'
    assert audit['audit_sha256'] == sha256((HERE / 'audit_helpers.py').read_bytes()).hexdigest()
    assert audit['original_states_calls'] == 96 and audit['original_coefficient_rows_calls'] == 288
    assert audit['exact_coefficient_equalities'] == 288 * 1905 == 548640
    assert audit['explicit_tuple_comparison_checks'] == 14336
    assert audit['fallback_repeated_query_checks'] == 520
    assert audit['main_calls'] == audit['discover_calls'] == audit['linprog_calls'] == 0
    rows = audit['sampled_rows']
    assert len(rows) == 288 and all(F(z['slack']) > 0 for z in rows)
    counts = Counter((z['i'], z['member'], tuple(z['orb']), z['q']) for z in rows)
    assert len(counts) == 96 and set(counts.values()) == {3}
    assert {tuple(x) for x in audit['multiplier_probes']} == {('0', '0'), ('1/3', '2/5'), ('7/5', '3/2')}
    for z in rows:
        assert (z['alpha'], z['gamma']) in {tuple(x) for x in audit['multiplier_probes']}
    py_count = 0
    for p in HERE.glob('*.py'):
        ast.parse(p.read_text())
        py_count += 1
    obj = REPO / manifest['formal_object']
    text = obj.read_text()
    assert text.startswith('---\n') and 'PLACEHOLDER' not in text
    assert 'id: customer-attraction/indexed-reply-true-tail-subset-projection-program' in text
    links = 0
    deferred_output_links = []
    for page in (obj, HERE / 'README.md'):
        for link in re.findall(r'\]\(([^)]+)\)', page.read_text()):
            if '://' not in link and not link.startswith('#'):
                target = (page.parent / link.split('#')[0]).resolve()
                if target == HERE / 'self-check.json':
                    deferred_output_links.append(target)
                else:
                    assert target.exists(), link
                links += 1
    receipt = json.loads((REPO / 'cleanup/workspaces/Boss7/receipts-round12/72c498d7803e037d9c4b.json').read_text())
    assert receipt['id'] == manifest['primary_source_id'] and receipt['disposition'] == 'integrated'
    assert all(receipt[k] is True for k in ('full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for'))
    for target in receipt['targets']:
        assert (REPO / target).is_file() or target.endswith('/self-check.json')
    result = {
        'status': 'PASS_STATIC_PACKAGE_AND_SAVED_EVENT_CHECKS',
        'scope': 'Frozen bytes, saved 288-row report, correction diff, syntax, relative links and receipt only; no mathematical helper or discovery rerun.',
        'shared_frozen_sources': len(manifest['shared_sources']), 'prior_5075_event_preserved': True,
        'saved_structures': len(counts), 'saved_parameter_rows': len(rows),
        'all_saved_slacks_positive': True, 'failed_attempt_preserved': True,
        'second_attempt_changes_only_count_assertion_and_descriptions': True,
        'python_files_parsed_without_execution': py_count, 'local_links_checked': links,
        'formal_object_sha256': sha256(obj.read_bytes()).hexdigest(),
        'helper_report_sha256': sha256((HERE / 'helper-audit.json').read_bytes()).hexdigest(),
        'initial_static_check_note': 'The first package check reached a link to its own not-yet-written self-check.json; the corrected checker validates that output link after writing it. No mathematical helper was rerun.',
    }
    (HERE / 'self-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    assert all(p.is_file() for p in deferred_output_links)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
