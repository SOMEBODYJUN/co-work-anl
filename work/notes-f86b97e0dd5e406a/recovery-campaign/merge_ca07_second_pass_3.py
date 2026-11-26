#!/usr/bin/env python3
"""Apply the Boss's explicit decisions after three frozen CA07 second reviews.

This mechanically binds authored edits and evidence. It does not read images,
accept a review, resolve statuses, or manufacture final-review records.
"""
from pathlib import Path
import copy
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
from build_note_ledger import build
from catalog_note_evidence import catalog

P = ROOT / 'work/notes-f86b97e0dd5e406a/notes/CA07/project'
OUT = P / 'audit/second-pass-3-merge'
EXPECTED = {
    'source-transcript.md': 'e4b14dd20fcc6417b4c4ccd63d26036e6f4ea9a56bbc3fb53eb5b72f487be675',
    'study-notes.md': 'fd4f6af0d34e69c6e95791f753931481488f969460e17ee87b861716cdad3126',
    'source-target-map.json': 'ec2bf62d11595d896a94ce555b03768bbd2429b3de65b0aea485cf29fa2bf23a',
}


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert {n: sha(P / n) for n in EXPECTED} == EXPECTED, 'formal content changed'
    receipt = load(OUT / 'independent-frozen-receipts.json')
    assert receipt['boss_read_all_independent_records'] is True
    assert {r['reviewer_id'] for r in receipt['records']} == {
        '/root/ca07_math', '/root/ca07_visual', '/root/ca07_adversarial'}
    for record in receipt['records']:
        for name, digest in record['files'].items():
            assert sha(P / name) == digest, name
    decisions = load(OUT / 'boss-decisions.json')
    assert decisions['status'] == 'authored after all three independent records'
    assert decisions['document_hashes_before'] == EXPECTED
    plan = load(P / 'content-plan.json')
    before = copy.deepcopy(plan)
    blocks = {b['id']: b for k in ('transcription_blocks', 'study_blocks') for b in plan[k]}
    changes = []

    for change in decisions['target_edits']:
        block = blocks[change['target_id']]
        if 'before_text_sha256' in change:
            assert hashlib.sha256(block['text'].encode()).hexdigest() == change['before_text_sha256']
        old = copy.deepcopy(block)
        if 'text' in change:
            block['text'] = change['text']
        block['source_ids'] = sorted((set(block['source_ids']) | set(change.get('add_source_ids', [])))
                                     - set(change.get('remove_source_ids', [])))
        changes.append({'target_id': block['id'], 'before': old, 'after': copy.deepcopy(block)})

    for change in decisions['source_labels']:
        source = next(s for s in plan['sources'] if s['id'] == change['source_id'])
        source['label'] = change['label']

    catalogued = catalog(P, load(OUT / 'evidence-inputs.json'))
    by_path = {a['path']: a for a in plan['evidence_artifacts']}
    for artifact in catalogued['evidence_artifacts']:
        if artifact['path'] in by_path:
            assert by_path[artifact['path']]['id'] == artifact['id'], artifact['path']
        by_path[artifact['path']] = artifact
    plan['evidence_artifacts'] = list(by_path.values())
    path_ids = {a['path']: 'artifact:' + a['id'] for a in plan['evidence_artifacts']}
    for page in load(P / 'manifest.json')['pages']:
        path_ids[page['image']['path']] = 'image:' + page['id']
        for region in page['regions']:
            path_ids[region['image']['path']] = 'image:' + region['id']
    decision_id = path_ids['audit/second-pass-3-merge/boss-decisions.json']

    def evidence(paths):
        return sorted({path_ids[p] for p in paths} | {decision_id})

    for change in decisions['target_edits']:
        block = blocks[change['target_id']]
        added = evidence(change.get('evidence_paths', []))
        block['evidence_ids'] = sorted(set(block.get('evidence_ids', []) + added))

    source_observations = decisions['source_observation_record']
    observation = load(P / source_observations)
    assert len(observation['pages']) == 8 and len(observation['regions']) == 48
    plan['observations'] = [{'pass': 1, 'reviewer_id': '/root/ca07_visual',
        'session_id': '/root/ca07_visual', 'path': source_observations,
        'artifact_id': path_ids[source_observations].removeprefix('artifact:')}]

    for change in decisions['recoveries']:
        rid = change['recovery_id']
        recovery = next(r for r in plan['recoveries'] if r['id'] == rid)
        issue = next(i for i in plan['issues'] if i['id'] == rid.replace('-R', '-I'))
        proofs = evidence(change['evidence_paths'])
        recovery['source_ids'] = sorted(set(change.get('source_ids', recovery['source_ids'])))
        if 'selected_text' in change:
            candidate_id = 'boss-second-pass-3-revised'
            assert not any(c['id'] == candidate_id for c in recovery['candidates'])
            recovery['candidates'].append({'id': candidate_id, 'text': change['selected_text'], 'evidence_ids': proofs})
            recovery['selected_candidate_id'] = candidate_id
        selected = next(c for c in recovery['candidates'] if c['id'] == recovery['selected_candidate_id'])
        selected['evidence_ids'] = sorted(set(selected['evidence_ids'] + proofs))
        for candidate in change.get('additional_candidates', []):
            assert not any(c['id'] == candidate['id'] for c in recovery['candidates'])
            recovery['candidates'].append({'id': candidate['id'], 'text': candidate['text'],
                'evidence_ids': evidence(candidate.get('evidence_paths', change['evidence_paths']))})
        recovery['problem'] += '\n第三次完整复核处理：' + change['correction']
        recovery['evidence_ids'] = sorted(set(recovery['evidence_ids'] + proofs))
        for key in ('forward_validation', 'backward_validation', 'return_to_image'):
            recovery[key].update(change.get(key, {}))
            recovery[key]['evidence_ids'] = sorted(set(recovery[key]['evidence_ids'] + proofs))
        recovery['status'] = 'unresolved'
        prior_targets = [x for x in issue['related_ids'] if x.startswith(('CA07-TRANSCRIPTION-', 'CA07-STUDY-'))]
        issue['related_ids'] = sorted(set(recovery['source_ids'] + [rid] + prior_targets + change.get('related_target_ids', [])))
        issue['description'] += '\n第三次完整复核处理：' + change['correction']
        issue['evidence_ids'] = sorted(set(issue['evidence_ids'] + proofs))
        issue['status'], issue['resolution'] = 'open', ''

    for change in decisions['new_recoveries']:
        proofs = evidence(change['evidence_paths'])
        rid, iid = change['recovery_id'], change['issue_id']
        assert not any(r['id'] == rid for r in plan['recoveries'])
        plan['recoveries'].append({
            'id': rid, 'source_ids': change['source_ids'], 'problem': change['problem'],
            'candidates': [{'id': c['id'], 'text': c['text'], 'evidence_ids': proofs} for c in change['candidates']],
            'selected_candidate_id': change['selected_candidate_id'], 'status': 'unresolved', 'evidence_ids': proofs,
            'forward_validation': {**change['forward_validation'], 'evidence_ids': proofs},
            'backward_validation': {**change['backward_validation'], 'evidence_ids': proofs},
            'return_to_image': {'page_ids': [], 'region_ids': [], 'observation': change['observation'], 'evidence_ids': proofs},
            'reviewer_id': '/root/ca07_adversarial', 'session_id': '/root/ca07_adversarial'})
        plan['issues'].append({'id': iid, 'status': 'open', 'description': change['problem'],
            'related_ids': sorted(set(change['source_ids'] + [rid] + change['related_target_ids'])),
            'evidence_ids': proofs, 'resolution': ''})

    assert len(plan['recoveries']) == len(plan['issues']) == 58
    assert len(plan['sources']) == 133
    assert len(plan['transcription_blocks']) + len(plan['study_blocks']) == 160
    assert all(x['status'] == 'unresolved' for x in plan['recoveries'])
    save(OUT / 'content-plan-before-revision.json', before)
    save(OUT / 'explicit-edit-receipt.json', {'boss_id': 'BossNotes-2ff3215d6446',
        'document_hashes_before': EXPECTED, 'changes': changes,
        'status': 'authored corrections; latest-content review still required'})
    save(P / 'content-plan.json', plan)
    result = build(P)
    result['document_hashes'] = {n: sha(P / n) for n in EXPECTED}
    save(OUT / 'new-content-hashes.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
