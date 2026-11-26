#!/usr/bin/env python3
"""Compile authored note blocks and actual observations into exact line mappings.

This tool never reads handwriting, invents observations, resolves an issue, or
creates a final review. All such decisions must be explicitly supplied in the
project's content-plan.json and the named independent observation records.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.agents/skills/math-notes-evidence-audit/scripts'))
from audit import intersects, safe_path, sha256_file


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def build(project: Path):
    project = project.resolve()
    plan_path = project / 'content-plan.json'
    plan = load(plan_path)
    manifest_path = project / 'manifest.json'
    manifest = load(manifest_path)
    page_map = {page['id']: page for page in manifest['pages']}
    ledger_path = project / 'ledger.json'
    if ledger_path.exists():
        old_hash = sha256_file(ledger_path)[:16]
        archive = project / 'history' / ('before-' + old_hash)
        if not archive.exists():
            archive.mkdir(parents=True)
            for filename in ['ledger.json', 'source-transcript.md', 'study-notes.md', 'audit-report.json']:
                path = project / filename
                if path.exists():
                    shutil.copy2(path, archive / filename)

    sources = []
    for item in plan['sources']:
        page = page_map[item['page_id']]
        box = item['bbox_px']
        regions = [region['id'] for region in page['regions'] if intersects(box, region['bbox_px'])]
        sources.append({'id': item['id'], 'page_id': item['page_id'], 'bbox_px': box,
            'region_ids': regions, 'label': item['label'], 'status': item['status'],
            'transcription_target_ids': [], 'study_target_ids': [],
            'evidence_ids': [f'image:{page["id"]}'] + [f'image:{rid}' for rid in regions]})
    source_map = {source['id']: source for source in sources}
    if len(source_map) != len(sources):
        raise ValueError('duplicate source IDs in the authored plan')

    artifacts = [{'id': 'content-plan', 'path': 'content-plan.json', 'sha256': sha256_file(plan_path),
                  'kind': 'evidence', 'format': 'text'}]
    targets = []
    for kind, filename, key in [('transcription', 'source-transcript.md', 'transcription_blocks'),
                                 ('study', 'study-notes.md', 'study_blocks')]:
        lines = []
        for index, block in enumerate(plan[key], 1):
            text = block['text'].strip('\n')
            if not text.strip():
                raise ValueError(f'{kind} block {index} has no text')
            if lines:
                lines.append('')
            start = len(lines) + 1
            lines.extend(text.splitlines())
            tid = block.get('id', f'{plan["note_id"]}-{kind.upper()}-{index:03d}')
            source_ids = block['source_ids']
            evidence = set(block.get('evidence_ids', []))
            for sid in source_ids:
                evidence.update(source_map[sid]['evidence_ids'])
                source_map[sid][f'{kind}_target_ids'].append(tid)
            if block['origin'] in {'editorial', 'supplement'}:
                evidence.add('artifact:content-plan')
            targets.append({'id': tid, 'artifact_id': kind, 'start_line': start, 'end_line': len(lines),
                'text_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(), 'source_ids': source_ids,
                'status': block['status'], 'origin': block['origin'], 'old_ids': [],
                'evidence_ids': sorted(evidence), 'explanation': block['explanation']})
        path = project / filename
        path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        artifacts.append({'id': kind, 'path': filename, 'sha256': sha256_file(path),
                          'kind': kind, 'format': 'text'})

    mapping_path = project / 'source-target-map.json'
    write(mapping_path, {
        'note_id': plan['note_id'], 'source_to_targets': [
            {key: source[key] for key in ('id', 'page_id', 'bbox_px', 'region_ids',
                                          'transcription_target_ids', 'study_target_ids')} for source in sources],
        'target_to_sources': [{key: target[key] for key in ('id', 'artifact_id', 'start_line',
                                                          'end_line', 'source_ids', 'origin')} for target in targets]})
    artifacts.append({'id': 'source-target-map', 'path': mapping_path.name,
                      'sha256': sha256_file(mapping_path), 'kind': 'evidence', 'format': 'text'})
    for artifact in plan['evidence_artifacts']:
        artifact = dict(artifact)
        path = safe_path(project, artifact['path'])
        artifact['sha256'] = sha256_file(path)
        artifacts.append(artifact)

    page_checks, region_checks = [], []
    for observation in plan.get('observations', []):
        number = observation['pass']
        observed = load(safe_path(project, observation['path']))
        obs_pages = {item['page_id']: item for item in observed['pages']}
        obs_regions = {item['region_id']: item for item in observed['regions']}
        artifact_id = observation['artifact_id']
        for page in manifest['pages']:
            actual = obs_pages[page['id']]
            units = [source for source in sources if source['page_id'] == page['id']]
            page_checks.append({'id': f'{plan["note_id"]}-PAGE-{page["id"]}-P{number}',
                'page_id': page['id'], 'pass': number, 'reviewer_id': observation['reviewer_id'],
                'session_id': observation['session_id'], 'assessment': actual['assessment'],
                'source_unit_ids': [source['id'] for source in units],
                'cross_region_unit_ids': [source['id'] for source in units if len(source['region_ids']) > 1],
                'evidence_ids': [f'image:{page["id"]}', f'artifact:{artifact_id}'],
                'observation': actual['observation'], 'layout_observation': actual['layout_observation']})
            for region in page['regions']:
                actual_region = obs_regions[region['id']]
                ids = [source['id'] for source in units if region['id'] in source['region_ids']]
                region_checks.append({'id': f'{plan["note_id"]}-REGION-{region["id"]}-P{number}',
                    'region_id': region['id'], 'pass': number, 'reviewer_id': observation['reviewer_id'],
                    'session_id': observation['session_id'], 'assessment': actual_region['assessment'],
                    'source_unit_ids': ids, 'evidence_ids': [f'image:{region["id"]}', f'artifact:{artifact_id}'],
                    'observation': actual_region['observation']})

    recoveries = []
    for item in plan['recoveries']:
        recovery = dict(item)
        related = [source_map[sid] for sid in recovery['source_ids']]
        pages = sorted({source['page_id'] for source in related})
        regions = sorted({rid for source in related for rid in source['region_ids']})
        images = sorted({eid for source in related for eid in source['evidence_ids']})
        recovery['evidence_ids'] = sorted(set(recovery['evidence_ids']) | set(images))
        recovery['return_to_image'] = {**recovery['return_to_image'], 'page_ids': pages, 'region_ids': regions,
            'evidence_ids': sorted(set(recovery['return_to_image']['evidence_ids']) | set(images))}
        recoveries.append(recovery)
    ledger = {'schema_version': '1.0', 'manifest_sha256': sha256_file(manifest_path),
        'authors': plan['authors'], 'review_policy': plan['review_policy'], 'artifacts': artifacts,
        'source_units': sources, 'target_units': targets, 'old_units': [],
        'page_checks': page_checks, 'region_checks': region_checks, 'recoveries': recoveries,
        'issues': plan['issues'], 'final_rounds': []}
    write(ledger_path, ledger)
    return {'note_id': plan['note_id'], 'source_units': len(sources), 'target_units': len(targets),
            'page_checks': len(page_checks), 'region_checks': len(region_checks),
            'recoveries': len(recoveries), 'issues': len(plan['issues']), 'final_rounds': 0,
            'content_decisions_generated': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.project), ensure_ascii=False, indent=2))
