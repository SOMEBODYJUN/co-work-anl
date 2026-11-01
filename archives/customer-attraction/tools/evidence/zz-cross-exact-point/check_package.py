"""Static evidence binding only: no original entrypoint or mathematical audit."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import ast
import json
import re

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]


def main():
    manifest = json.loads((HERE / 'source-manifest.json').read_text())
    base = json.loads((REPO / manifest['base_frozen_manifest']).read_text())
    records = base['frozen_sources'] + manifest['supplemental_frozen_sources']
    bypath = {}
    for r in records:
        data = (REPO / r['stored_path']).read_bytes()
        assert len(data) == r['size'] and sha256(data).hexdigest() == r['sha256']
        assert r['path'] not in bypath
        bypath[r['path']] = r
    prior = manifest['reused_independent_interface_audit']
    assert sha256((REPO / prior['stored_path']).read_bytes()).hexdigest() == prior['sha256']
    run = json.loads((HERE / 'rerun/execution.json').read_text())
    assert run['original_main_calls'] == 1 and run['linprog_calls'] == 0
    assert run['effective_argv'] == ['--cross', '--priced', '--optimum', '--verify']
    assert run['capture_sha256'] == sha256((HERE / 'capture_original.py').read_bytes()).hexdigest()
    for r in run['actual_imported_runtime_modules']:
        other = bypath[r['path']]
        assert (r['bytes'], r['sha256']) == (other['size'], other['sha256'])
    for name, r in run['artifacts'].items():
        b = (HERE / 'rerun' / name).read_bytes()
        assert len(b) == r['bytes'] and sha256(b).hexdigest() == r['sha256']
    slacks = json.loads((HERE / 'rerun/all-row-slacks.json').read_text())
    assert len(slacks) == run['total_rows'] == 4987
    for i, row in enumerate(slacks):
        assert row['index'] == i and F(row['slack']) >= 0
    for section in run['sections'].values():
        vals = [F(x['slack']) for x in slacks[section['begin']:section['end_exclusive']]]
        assert len(vals) == section['rows']
        assert sum(x > 0 for x in vals) == section['positive']
        assert sum(x == 0 for x in vals) == section['zero']
        assert sum(x < 0 for x in vals) == section['negative'] == 0
    audit = json.loads((HERE / 'data-audit.json').read_text())
    assert audit['audit_sha256'] == sha256((HERE / 'audit_data.py').read_bytes()).hexdigest()
    reading = json.loads((HERE / 'lossless-reading.json').read_text())
    assert len(reading['all_302_rows']) == audit['records'] == 302
    rebuilt = dict(reading['top_fields_in_original_order'])
    rebuilt['variables'] = [{'hist_column': h, 'left': reading['rational_strings'][l], 'right': reading['rational_strings'][u], 'group': reading['groups'][g], 'r': r, 'weight': reading['rational_strings'][y]} for h, l, u, g, r, y in reading['all_302_rows']]
    assert (json.dumps(rebuilt, indent=2) + '\n').encode() == (REPO / manifest['primary']['stored_path']).read_bytes()
    cube = json.loads((HERE / 'conditional-cube-atoms.json').read_text())
    assert len(cube['slabs']) == audit['slabs'] == 24
    assert sum(len(s['atoms']) for s in cube['slabs']) == audit['conditional_atoms'] == 227
    assert len(cube['unit_customer_scale_after_720_permutations']) == 653
    change = json.loads((HERE / 'changed-coordinates.json').read_text())
    assert len(change['coordinate_changes']) == audit['total_coordinate_changes'] == 268
    assert len(change['Z_marginal_changes']) == audit['Z_marginal_changes'] == 62
    assert F(audit['one_omitted_floor']['slack']) < 0
    for p in HERE.glob('*.py'):
        ast.parse(p.read_text())
    object_path = REPO / manifest['formal_object']
    assert object_path.read_text().startswith('---\n')
    assert 'PLACEHOLDER' not in object_path.read_text()
    links, deferred = 0, []
    for page in (object_path, HERE / 'README.md'):
        for link in re.findall(r'\]\(([^)]+)\)', page.read_text()):
            if '://' not in link and not link.startswith('#'):
                dest = (page.parent / link.split('#')[0]).resolve()
                if dest == HERE / 'self-check.json':
                    deferred.append(dest)
                else:
                    assert dest.exists(), link
                links += 1
    receipt = json.loads((REPO / 'cleanup/workspaces/Boss7/receipts-round13/dc384719f1948419dde1.json').read_text())
    assert receipt['id'] == manifest['primary_source_id'] and receipt['disposition'] == 'integrated'
    assert all(receipt[k] for k in ('full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for'))
    for t in receipt['targets']:
        assert (REPO / t).is_file() or REPO / t == HERE / 'self-check.json'
    result = {'status': 'PASS_STATIC_COMPLETE_SOURCE_AND_EVENT_PACKAGE_CHECK', 'scope': 'Hashes, lossless decoding, saved row/atom/change counts, syntax and links only; no mathematical generator or verifier rerun.', 'frozen_files_checked': len(records), 'imported_modules_bound': len(run['actual_imported_runtime_modules']), 'all_saved_slacks_checked': len(slacks), 'lossless_records': len(rebuilt['variables']), 'saved_atoms': 227, 'receipt_targets': len(receipt['targets']), 'local_links_checked': links, 'formal_sha256': sha256(object_path.read_bytes()).hexdigest(), 'execution_sha256': sha256((HERE / 'rerun/execution.json').read_bytes()).hexdigest(), 'data_audit_sha256': sha256((HERE / 'data-audit.json').read_bytes()).hexdigest()}
    (HERE / 'self-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    assert all(p.is_file() for p in deferred)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
