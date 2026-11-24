#!/usr/bin/env python3
"""Copy an existing authored ledger into a separately editable integration version.

Only existing records are copied or stripped of mechanically derived fields.
No image observations, judgments, recovery decisions, or review passes are made.
The original ledger and first-draft artifacts remain unchanged.
"""
import argparse
import json
from pathlib import Path
import shutil


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True, type=Path)
    parser.add_argument('--version', default='integration-v2')
    args = parser.parse_args()
    project = args.project.resolve()
    version = args.version
    if '/' in version or version in ('', '.', '..'):
        raise ValueError('Version must be one directory name')
    folder = project / 'proposals' / version
    if folder.exists():
        raise FileExistsError(folder)
    original = project / 'ledger.json'
    ledger = json.loads(original.read_text())
    if ledger['final_rounds']:
        raise ValueError('Do not derive a new version from sealed final-round history')
    folder.mkdir()
    historical = project / 'ledger-first-pass.json'
    if not historical.exists():
        shutil.copy2(original, historical)
    elif historical.read_bytes() != original.read_bytes():
        raise ValueError('Historical first-pass copy already exists and differs')
    artifacts = []
    old_prefix = 'proposals/rebuild/'
    for old in ledger['artifacts']:
        artifact = {k: v for k, v in old.items() if k != 'sha256'}
        if artifact['path'].startswith(old_prefix):
            relative = artifact['path'][len(old_prefix):]
            destination = folder / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(project / artifact['path'], destination)
            artifact['path'] = str(destination.relative_to(project))
        artifacts.append(artifact)
    source_fields = {'id', 'page_id', 'bbox_px', 'label', 'status', 'evidence_ids'}
    target_fields = {'id', 'artifact_id', 'source_ids', 'status', 'origin', 'old_ids', 'evidence_ids', 'explanation'}
    dump(folder / 'source-units.json', [{k: v for k, v in unit.items() if k in source_fields} for unit in ledger['source_units']])
    dump(folder / 'mapping.json', {'targets': [{k: v for k, v in unit.items() if k in target_fields} for unit in ledger['target_units']]})
    dump(folder / 'observations-author.json', {'page_checks': ledger['page_checks'], 'region_checks': ledger['region_checks']})
    dump(folder / 'recoveries-inherited.json', ledger['recoveries'])
    dump(folder / 'issues.json', ledger['issues'])
    # Config paths are interpreted relative to the project root, so do not
    # repeat the project directory name (the copied artifact paths already
    # are project-relative).
    prefix = str(folder.relative_to(project))
    config = {'authors': ledger['authors'], 'manifest': 'manifest.json', 'artifacts': artifacts,
              'source_units': prefix + '/source-units.json', 'mapping': prefix + '/mapping.json',
              'observations': prefix + '/observations-author.json', 'recoveries': prefix + '/recoveries-inherited.json',
              'issues': prefix + '/issues.json', 'output': 'ledger-' + version + '.json'}
    dump(project / ('ledger-config-' + version + '.json'), config)
    print(json.dumps({'version': str(folder), 'source_units': len(ledger['source_units']),
                      'target_units': len(ledger['target_units']), 'observations': 'copied historical records only',
                      'original_preserved': True}, ensure_ascii=False))


if __name__ == '__main__':
    main()
