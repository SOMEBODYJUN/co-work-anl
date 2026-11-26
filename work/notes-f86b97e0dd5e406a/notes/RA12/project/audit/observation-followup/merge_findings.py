"""Merge actual failed final-review findings into pending observation recoveries.

This one-time author operation preserves all submitted reports. It creates no
review acceptances or observations; a current actual nonauthor report supplies
the replacement second pass after all three agents review the new records.
"""
from pathlib import Path
import copy
import hashlib
import json
import shutil
import sys

P = Path(__file__).resolve().parents[2]
ROOT = P.parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
from build_note_ledger import build
from catalog_note_evidence import catalog
from final_note_reviews import current


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


inputs = read(P / 'audit/observation-followup/synthesis-inputs.json')
proposal = read(P / 'audit/observation-followup/boss-proposals.json')
plan, ledger = (read(P / name) for name in ['content-plan.json', 'ledger.json'])
frozen = read(P / 'audit/final-freeze.json')
assert frozen['snapshot_sha256'] == proposal['basis_snapshot'] == current(P)[4]
assert len(plan['recoveries']) == len(plan['issues']) == 41
assert not ledger['final_rounds']
assert len(proposal['decisions']) == 7
before = {name: sha(P / name) for name in frozen['document_hashes']}
assert before == frozen['document_hashes']

actual_final = []
for role in ['visual', 'math', 'adversarial']:
    relative = f'proposals/ra12_{role}/final-242d53ba3e21/final-report.json'
    report = read(P / relative)
    assert report['reviewer_id'] == report['session_id'] == '/root/ra12_' + role
    assert report['snapshot_sha256'] == frozen['snapshot_sha256']
    assert report['document_hashes_start'] == before == report['document_hashes_end']
    for key, expected in frozen['scope'].items():
        assert len(report['scope'][key]) == len(set(report['scope'][key]))
        assert set(report['scope'][key]) == set(expected)
    assert sha(P / report['blind_reading']['path']) == report['blind_reading']['sha256']
    actual_final.append({'reviewer_id': report['reviewer_id'], 'path': relative,
                         'sha256': sha(P / relative), 'findings': report['findings']})
assert any(item['findings'] for item in actual_final)
assert {item['reviewer_id'] for item in inputs['actual_recovery_reports']} == {
    '/root/ra12_visual', '/root/ra12_math', '/root/ra12_adversarial'}
for item in inputs['actual_recovery_reports']:
    assert sha(P / item['path']) == item['sha256']

archive = P / 'history/final-review-242d53ba3e21'
archive.mkdir(parents=True, exist_ok=False)
for name in ['content-plan.json', 'authored-content.json', 'ledger.json',
             'source-transcript.md', 'study-notes.md', 'source-target-map.json',
             'audit-prefinal-report.json', 'audit-report.json']:
    if (P / name).is_file():
        shutil.copy2(P / name, archive / name)
shutil.copy2(P / 'audit/final-freeze.json', archive / 'final-freeze.json')
write(archive / 'actual-final-reports.json', {
    'snapshot_sha256': frozen['snapshot_sha256'], 'document_hashes': before,
    'reports': actual_final, 'accepted_as_final_chain': False,
    'reason': 'Actual independent final reviews found current observation errors.'})

texts = list(inputs['text_files']) + [
    'audit/observation-followup/boss-check.md',
    'audit/observation-followup/boss-proposals.json',
    'audit/observation-followup/synthesis-inputs.json',
    'audit/observation-followup/merge_findings.py']
for role in ['visual', 'math', 'adversarial']:
    folder = P / f'proposals/ra12_{role}/final-242d53ba3e21'
    texts.extend(str(path.relative_to(P)) for path in sorted(folder.iterdir())
                 if path.suffix in {'.json', '.md'})
evidence = catalog(P, {'text_files': texts, 'crop_indexes': inputs['crop_indexes']})
existing = {item['path']: item['id'] for item in plan['evidence_artifacts']}
for item in evidence['evidence_artifacts']:
    assert item['path'] not in existing
    record = dict(item)
    record.pop('sha256', None)
    plan['evidence_artifacts'].append(record)
    existing[item['path']] = item['id']


def eid(path):
    return 'artifact:' + existing[path]


decision_path = 'audit/observation-followup/recovery-decisions.json'
write(P / decision_path, {
    'note_id': 'RA12', 'boss': 'BossNotes-2ff3215d6446',
    'before_snapshot': frozen['snapshot_sha256'], 'before_document_hashes': before,
    'actual_final_reports': actual_final,
    'actual_independent_recovery_reports': inputs['actual_recovery_reports'],
    'decisions': proposal['decisions'],
    'latest_second_pass_pending': True,
    'historical_report_clarification':
        'The adversarial final report said another physical line for the conclusion Y; '
        'all three new independent recovery records and the original 800 dpi image '
        'place both clauses on the same physical line. The old report remains immutable.'})
plan['evidence_artifacts'].append({'id': 'observation-followup-recovery-decisions',
    'path': decision_path, 'kind': 'evidence', 'format': 'text'})
existing[decision_path] = 'observation-followup-recovery-decisions'
common = [eid(decision_path), eid('audit/observation-followup/boss-check.md')]
common.extend(eid(item['path']) for item in inputs['actual_recovery_reports'])
common.extend(eid(item['path']) for item in actual_final)
for decision in proposal['decisions']:
    ids = sorted(set(common + [eid(path) for path in decision['direct_evidence_paths']]))
    rid = f'RA12-REC-{decision["number"]:02d}'
    plan['recoveries'].append({
        'id': rid, 'source_ids': decision['source_ids'],
        'problem': decision['current_observation_id'] + '：' + decision['problem'],
        'candidates': [{'id': f'candidate-{i}', 'text': candidate, 'evidence_ids': ids}
                       for i, candidate in enumerate(decision['candidates'], 1)],
        'selected_candidate_id': 'candidate-1', 'status': 'unresolved',
        'evidence_ids': ids,
        'forward_validation': {'status': 'pass', 'method': '原像位置与数学语句作用域正向核验',
            'inputs': decision['observation'], 'result': decision['forward'], 'evidence_ids': ids},
        'backward_validation': {'status': 'pass', 'method': '分区交界、物理原行及括弧配对的反向检验',
            'inputs': decision['candidates'][0], 'result': decision['backward'], 'evidence_ids': ids},
        'return_to_image': {'observation': decision['observation'], 'evidence_ids': ids},
        'reviewer_id': 'BossNotes-2ff3215d6446', 'session_id': 'BossNotes-2ff3215d6446'})
    plan['issues'].append({
        'id': f'RA12-ISSUE-{decision["number"]:02d}', 'status': 'open',
        'description': decision['current_observation_id'] + '：' + decision['problem'] +
            '；三份真实恢复记录后的Boss合并提议，等待当前版本非作者第二遍接受。',
        'related_ids': decision['source_ids'] + [rid], 'evidence_ids': ids, 'resolution': ''})

plan['observations'] = [item for item in plan['observations'] if item['pass'] != 2]
for item in plan['recoveries']:
    item['status'] = 'unresolved'
for item in plan['issues']:
    item['status'], item['resolution'] = 'open', ''
for key in ['sources', 'transcription_blocks', 'study_blocks']:
    for item in plan[key]:
        item['status'] = 'unresolved'
authored = read(P / 'authored-content.json')
for key in ['sources', 'transcription_blocks', 'study_blocks']:
    authored[key] = copy.deepcopy(plan[key])
write(P / 'authored-content.json', authored)
write(P / 'content-plan.json', plan)
(P / 'audit/final-freeze.json').unlink()
result = build(P)
after = {name: sha(P / name) for name in before}
assert before == after, 'Observation recovery must not change either body or the content mapping.'
assert len(plan['recoveries']) == len(plan['issues']) == 48
write(P / 'audit/observation-followup/change-summary.json', {
    'before_document_hashes': before, 'after_document_hashes': after,
    'recovery_count_before': 41, 'recovery_count_after': 48,
    'issue_count_before': 41, 'issue_count_after': 48,
    'actual_final_reports_retained': actual_final,
    'old_final_chain_abandoned': True, 'final_rounds': 0,
    'latest_second_pass_pending': True})
print(json.dumps({**result, 'document_hashes': after,
                  'body_and_mapping_bytes_unchanged': True}, ensure_ascii=False))
