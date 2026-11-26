#!/usr/bin/env python3
"""Apply explicit, independently checked CA07 provenance corrections.

This copies no body text and decides no readings. It binds already-authored
Boss decisions, preserves all independent reports, and refuses any unexpected
body or mapping change. Acceptance and final review happen separately.
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
OUT = P / 'audit/second-pass-4-merge'
EXPECTED = {
    'source-transcript.md': '376ba572a25a48a39487bbfb80ce96bdeaf4e405e4fb5c32e04255f6572e3b64',
    'study-notes.md': '43c1bce76087b71ca5df2c9032e5fbda3ed8677e7d30ec4a41f615d0bb93e7ce',
    'source-target-map.json': 'd003ebfed40cfaa6f7dacc42abf1ea15a40b3f3b57b6eef357fe6c95ddc4efbd',
}


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert not (OUT / 'applied-result.json').exists(), 'already applied'
    assert {name: sha(P / name) for name in EXPECTED} == EXPECTED
    receipt = load(OUT / 'independent-frozen-receipts.json')
    assert receipt['boss_read_all_independent_records'] is True
    assert receipt['post_review_reconciled'] is True
    assert {x['reviewer_id'] for x in receipt['records']} == {
        '/root/ca07_visual', '/root/ca07_math', '/root/ca07_adversarial'}
    for record in receipt['records']:
        for relative, digest in record['files'].items():
            assert sha(P / relative) == digest, relative
    decisions = load(OUT / 'boss-decisions.json')
    assert decisions['status'] == 'authored after all three independent records'
    assert decisions['document_hashes_before'] == EXPECTED
    assert sha(P / 'ledger.json') == decisions['ledger_sha256_before']
    assert sha(P / 'content-plan.json') == decisions['content_plan_sha256_before']
    plan = load(P / 'content-plan.json')
    before = copy.deepcopy(plan)
    assert not load(P / 'ledger.json')['final_rounds']
    catalogued = catalog(P, load(OUT / 'evidence-inputs.json'))
    artifacts = {a['path']: a for a in plan['evidence_artifacts']}
    for artifact in catalogued['evidence_artifacts']:
        if artifact['path'] in artifacts:
            assert artifacts[artifact['path']]['id'] == artifact['id']
        artifacts[artifact['path']] = artifact
    plan['evidence_artifacts'] = list(artifacts.values())
    evidence_by_path = {a['path']: 'artifact:' + a['id'] for a in plan['evidence_artifacts']}
    decision_id = evidence_by_path['audit/second-pass-4-merge/boss-decisions.json']
    changes = []
    for correction in decisions['recoveries']:
        rid = correction['recovery_id']
        recovery = next(x for x in plan['recoveries'] if x['id'] == rid)
        issue = next(x for x in plan['issues'] if x['id'] == rid.replace('-R', '-I'))
        previous_recovery, previous_issue = copy.deepcopy(recovery), copy.deepcopy(issue)
        additions = correction['add_source_ids']
        assert not set(additions).intersection(recovery['source_ids']), rid
        assert set(additions) <= {s['id'] for s in plan['sources']}, rid
        proofs = sorted({evidence_by_path[path] for path in correction['evidence_paths']} | {decision_id})
        recovery['source_ids'] = sorted(set(recovery['source_ids']) | set(additions))
        recovery['problem'] += '\n第四次完整复核处理：' + correction['correction']
        recovery['evidence_ids'] = sorted(set(recovery['evidence_ids'] + proofs))
        for field in ('forward_validation', 'backward_validation', 'return_to_image'):
            recovery[field].update(correction.get(field, {}))
            recovery[field]['evidence_ids'] = sorted(set(recovery[field]['evidence_ids'] + proofs))
        selected = next(c for c in recovery['candidates'] if c['id'] == recovery['selected_candidate_id'])
        selected['evidence_ids'] = sorted(set(selected['evidence_ids'] + proofs))
        assert recovery['status'] == 'unresolved'
        issue['related_ids'] = sorted(set(issue['related_ids']) | set(additions))
        issue['description'] += '\n第四次完整复核处理：' + correction['correction']
        issue['evidence_ids'] = sorted(set(issue['evidence_ids'] + proofs))
        assert issue['status'] == 'open' and not issue['resolution']
        changes.append({'recovery_id': rid, 'before_recovery': previous_recovery,
                        'after_recovery': copy.deepcopy(recovery), 'before_issue': previous_issue,
                        'after_issue': copy.deepcopy(issue)})
    assert len(changes) == 10
    assert sum(len(c['add_source_ids']) for c in decisions['recoveries']) == 17
    observation_path = decisions['source_observation_record']
    observation = load(P / observation_path)
    assert len(observation['pages']) == 8 and len(observation['regions']) == 48
    assert not any(x['pass'] == 2 for x in plan['observations'])
    plan['observations'] = [{'pass': 1, 'reviewer_id': '/root/ca07_visual',
                            'session_id': '/root/ca07_visual', 'path': observation_path,
                            'artifact_id': evidence_by_path[observation_path].removeprefix('artifact:')}]
    for field in ('sources', 'transcription_blocks', 'study_blocks'):
        assert plan[field] == before[field], 'unexpected content change: ' + field
    assert len(plan['sources']) == 133
    assert len(plan['transcription_blocks']) + len(plan['study_blocks']) == 160
    assert len(plan['recoveries']) == len(plan['issues']) == 58
    save(OUT / 'content-plan-before-revision.json', before)
    save(OUT / 'explicit-edit-receipt.json', {
        'boss_id': 'BossNotes-2ff3215d6446', 'document_hashes_before': EXPECTED,
        'changes': changes, 'observations_before': before['observations'],
        'observations_after': plan['observations'],
        'status': 'provenance and observation corrections; latest delta confirmation still required'})
    edit_receipt_path = 'audit/second-pass-4-merge/explicit-edit-receipt.json'
    assert not any(a['path'] == edit_receipt_path for a in plan['evidence_artifacts'])
    plan['evidence_artifacts'].append({
        'id': 'ca07-sp4-explicit-edit-receipt', 'path': edit_receipt_path,
        'sha256': sha(P / edit_receipt_path), 'kind': 'evidence', 'format': 'text'})
    save(P / 'content-plan.json', plan)
    result = build(P)
    current = {name: sha(P / name) for name in EXPECTED}
    assert current == EXPECTED, 'body or map unexpectedly changed'
    result.update({'document_hashes': current, 'body_and_map_unchanged': True,
                   'ledger_sha256': sha(P / 'ledger.json'),
                   'content_plan_sha256': sha(P / 'content-plan.json'),
                   'recovery_source_links_added': 17, 'recovery_records_changed': 10,
                   'acceptance_performed': False})
    save(OUT / 'applied-result.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
