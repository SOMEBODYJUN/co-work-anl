#!/usr/bin/env python3
"""Publication consistency only; contains no game solving or scientific audit."""
from pathlib import Path
import argparse
import hashlib
import json
import re


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', type=Path, required=True)
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--inputs', type=Path, required=True)
    args = ap.parse_args()
    stage, repo, inputs = (p.resolve() for p in (args.stage, args.repo, args.inputs))
    evidence = stage / 'archives/customer-attraction/tools/evidence/ra13-terminal-load'
    manifest = json.loads((evidence / 'source-manifest.json').read_text())
    ids = [s['id'] for s in manifest['primary_sources']]
    assert len(ids) == len(set(ids)) == 4
    total = 0
    allowed_refs = set()
    for src in manifest['primary_sources']:
        preserved = stage / src['preserved_path']
        exported = inputs / src['id'] / Path(src['path']).name
        receipt = json.loads((exported.parent / 'export-receipt.json').read_text())['source']
        assert preserved.read_bytes() == exported.read_bytes()
        assert len(preserved.read_bytes()) == src['size']
        assert digest(preserved) == src['sha256']
        for key in ('id', 'blob', 'mode', 'path', 'sha256', 'size', 'sources'):
            assert src[key] == receipt[key], key
        total += src['size']
        allowed_refs.update(src['source_refs'])
    assert total == manifest['primary_bytes'] == 7921
    receipts = json.loads((stage / 'cleanup/workspaces/Boss2/receipts-ra13-terminal-load-four.json').read_text())
    assert {x['id'] for x in receipts} == set(ids) and len(receipts) == 4
    for rec in receipts:
        for key in ('full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for'):
            assert rec[key] is True
        for key in ('read_note', 'comparison_note', 'decision_note'):
            assert len(rec[key]) > 50
        assert rec['disposition'] == 'integrated'
        assert rec['targets'] and all((stage / p).is_file() for p in rec['targets'])
    semantic = json.loads((evidence / 'semantic-units.json').read_text())
    assert {x['id'] for x in semantic['sources']} == set(ids)
    workspace = json.loads((inputs / 'dd7f4fdee45ec9dbf3ad/workspace.json').read_text())
    assert set(workspace) == {'schema', 'save', 'actor', 'instance'}
    deps = []
    for name in ('comparison-bindings-preprimary.json', 'historical-proof-context-bindings.json'):
        for entry in json.loads((evidence / name).read_text())['files']:
            p = repo / entry['path']
            assert p.is_file() and len(p.read_bytes()) == entry['bytes']
            assert digest(p) == entry['sha256'], entry['path']
            deps.append(entry['path'])
    assert len(deps) == len(set(deps)) == 10
    formals = sorted((stage / 'archives/customer-attraction/state').rglob('*.md'))
    assert len(formals) == 3
    object_ids = []
    for path in formals:
        text = path.read_text()
        fm = text.split('---', 2)[1]
        for key in ('id', 'kind', 'type_tag', 'title', 'status', 'summary', 'source_refs'):
            assert re.search(r'^' + key + r':', fm, re.M), (path, key)
        object_ids.append(re.search(r'^id: "([^"]+)"', fm, re.M).group(1))
        refs = re.findall(r'"(source:[^"]+)"', fm)
        assert refs and set(refs) <= allowed_refs
    assert len(set(object_ids)) == 3
    local_links = 0
    for path in list(formals) + [evidence / 'README.md']:
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' in target or target.startswith('#'):
                continue
            target = target.split('#', 1)[0]
            dest = (path.parent / target).resolve()
            relative = dest.relative_to(stage)
            assert dest.exists() or (repo / relative).exists(), (path, target)
            local_links += 1
    for p in stage.rglob('*.json'):
        json.loads(p.read_text())
    result = {'status': 'passed', 'scope': 'Publication artifact consistency only; not a mathematical proof or scientific execution.',
              'primary_files': 4, 'primary_bytes': total, 'receipts': len(receipts), 'formal_objects': len(formals),
              'bound_existing_dependencies': len(deps), 'local_links_checked': local_links,
              'original_or_new_scientific_runs': 0, 'old_witness_replays': 0,
              'mathematics': 'All mathematical arguments are analytic prose; substantive proof/domain/scope review is recorded separately.'}
    (evidence / 'publication-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, separators=(',', ':')))


if __name__ == '__main__':
    main()
