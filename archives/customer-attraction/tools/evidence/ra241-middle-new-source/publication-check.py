#!/usr/bin/env python3
"""Artifact consistency, not an execution of either mathematical audit."""
from pathlib import Path
from fractions import Fraction
import argparse
import hashlib
import json
import re


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', type=Path, required=True)
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--inputs', type=Path, required=True)
    args = ap.parse_args()
    stage, repo, inputs = (p.resolve() for p in (args.stage, args.repo, args.inputs))
    e = stage / 'archives/customer-attraction/tools/evidence/ra241-middle-new-source'
    m = json.loads((e / 'source-manifest.json').read_text())
    expected = {s['id'] for s in m['primary_sources']}
    assert len(expected) == len(m['primary_sources']) == 6
    assert sum(s['size'] for s in m['primary_sources']) == m['primary_bytes'] == 16316
    refs = set()
    reports = []
    for src in m['primary_sources']:
        p = stage / src['preserved_path']
        exported = inputs / src['id'] / Path(src['path']).name
        receipt = json.loads((exported.parent / 'export-receipt.json').read_text())['source']
        assert p.read_bytes() == exported.read_bytes()
        assert p.stat().st_size == src['size'] and sha(p) == src['sha256']
        for k in ('blob', 'id', 'mode', 'path', 'sha256', 'size', 'sources'):
            assert receipt[k] == src[k]
        refs.update(src['source_refs'])
        if src['path'].endswith('.json'):
            reports.append(json.loads(p.read_text()))
    stored_comparisons = json.loads((e / 'comparison-bindings-preprimary.json').read_text())['files']
    cross = json.loads((e / 'cross-agent-stage-readings.json').read_text())['files']
    dependencies = json.loads((e / 'dependency-reuse-manifest.json').read_text())['actual_runtime_input_files']
    entries = stored_comparisons + cross + dependencies
    assert len(entries) == len({x['path'] for x in entries}) == 9
    atoms = 0
    for x in entries:
        p = repo / x['path']
        assert p.stat().st_size == x['bytes'] and sha(p) == x['sha256'], x['path']
    for dep in dependencies:
        d = json.loads((repo / dep['path']).read_text())
        assert list(d) == dep['top_level_fields'] and len(d) == 10
        assert len(d['histograms']) == 16
        assert sum(map(len, d['groups'])) == 194
        assert len(d['atoms']) == dep['atoms']
        for h in d['histograms']:
            assert len(h['actual_bits']) == 6 and set(h['actual_bits']) <= {'0', '1'}
            assert len(h['hist']) == 8 and sum(h['hist']) == 6
        for a in d['atoms']:
            n = len(d['groups'][a['hist_index']])
            assert len(a['R']) == len(a['Z']) == n
            assert set(a['R']) | set(a['Z']) <= {0, 1}
            assert Fraction(a['weight']) > 0
        atoms += len(d['atoms'])
    assert atoms == 55
    # Only check internal arithmetic of frozen reports, never phi/evaluate.
    evals = []
    for report in reports:
        evals += report.get('evaluations', [report])
    assert len(evals) == 3
    for row in evals:
        assert Fraction(row['lhs']) - Fraction(row['rhs']) == Fraction(row['slack']) < 0
    full_read = json.loads((e / 'complete-report-reading.json').read_text())
    assert full_read['total_primitive_fields'] == 30
    recs = json.loads((stage / 'cleanup/workspaces/Boss2/receipts-ra241-middle-new-source-six.json').read_text())
    assert len(recs) == 6 and {x['id'] for x in recs} == expected
    for rec in recs:
        for key in ('full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for'):
            assert rec[key] is True
        assert rec['disposition'] == 'integrated'
        for key in ('read_note', 'comparison_note', 'decision_note'):
            assert isinstance(rec[key], str) and rec[key].strip()
        assert all((stage / p).is_file() for p in rec['targets'])
    formals = sorted((stage / 'archives/customer-attraction/state').rglob('*.md'))
    assert len(formals) == 3
    ids = []
    links = 0
    for p in formals:
        fm = p.read_text().split('---', 2)[1]
        for key in ('id', 'kind', 'type_tag', 'title', 'status', 'summary', 'source_refs'):
            assert re.search(r'^' + key + r':', fm, re.M)
        ids.append(re.search(r'^id:\s*(.*)$', fm, re.M).group(1).strip('"'))
        assert set(re.findall(r'"(source:[^"]+)"', fm)) <= refs
    assert len(set(ids)) == 3
    for p in formals + [e / 'README.md']:
        for target in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if '://' in target or target.startswith('#'):
                continue
            dest = (p.parent / target.split('#', 1)[0]).resolve()
            relative = dest.relative_to(stage)
            assert dest.exists() or (repo / relative).exists(), (p, target)
            links += 1
    for p in stage.rglob('*.json'):
        json.loads(p.read_text())
    result = {'status': 'passed', 'scope': 'Publication consistency only, not either original mathematical audit or a proof of old-system feasibility/SPE.',
              'primary_files': 6, 'primary_bytes': 16316, 'formal_objects': 3, 'receipts': 6,
              'existing_bound_files': 9, 'related_atoms_structurally_read': atoms,
              'original_report_primitive_fields': 30, 'stored_report_arithmetic_records': 3,
              'local_links_checked': links, 'original_audit_runs': 0, 'new_scientific_audit_runs': 0}
    (e / 'publication-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, separators=(',', ':')))


if __name__ == '__main__':
    main()
