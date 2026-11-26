"""One-time author merge of real b95f findings and three independent proposals.

This registers evidence and makes a pending authored revision. It does not
generate independent observations, acceptance records, or final reviews.
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


inputs = read(P / 'audit/u12-followup/synthesis-inputs.json')
proposal = read(P / 'audit/u12-followup/boss-proposals.json')
plan, ledger = (read(P / name) for name in ['content-plan.json', 'ledger.json'])
frozen = read(P / 'audit/final-freeze.json')
assert frozen['snapshot_sha256'] == proposal['basis_snapshot'] == current(P)[4]
assert len(plan['recoveries']) == len(plan['issues']) == 48
assert not ledger['final_rounds']
assert [d['number'] for d in proposal['decisions']] == [49, 50]
before = {name: sha(P / name) for name in frozen['document_hashes']}
assert before == frozen['document_hashes']
actual_final = []
for role in ['visual', 'math', 'adversarial']:
    relative = f'proposals/ra12_{role}/final-b95fedadb1c7/final-report.json'
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

archive = P / 'history/final-review-b95fedadb1c7'
archive.mkdir(parents=True, exist_ok=False)
for name in ['content-plan.json', 'authored-content.json', 'ledger.json',
             'source-transcript.md', 'study-notes.md', 'source-target-map.json',
             'audit-prefinal-report.json', 'audit-report.json']:
    if (P / name).is_file():
        shutil.copy2(P / name, archive / name)
shutil.copy2(P / 'audit/final-freeze.json', archive / 'final-freeze.json')
shutil.copy2(P / 'audit/granular-followup/body-and-source-overrides.json',
             archive / 'body-and-source-overrides.json')
write(archive / 'actual-final-reports.json', {
    'snapshot_sha256': frozen['snapshot_sha256'], 'document_hashes': before,
    'reports': actual_final, 'accepted_as_final_chain': False,
    'reason': 'Actual visual final identified unqualified glyph transcription and a geometric assertion.'})

texts = list(inputs['text_files']) + [
    'audit/u12-followup/boss-check.md', 'audit/u12-followup/boss-proposals.json',
    'audit/u12-followup/synthesis-inputs.json', 'audit/u12-followup/merge_findings.py']
for role in ['visual', 'math', 'adversarial']:
    folder = P / f'proposals/ra12_{role}/final-b95fedadb1c7'
    texts.extend(str(path.relative_to(P)) for path in sorted(folder.iterdir())
                 if path.suffix in {'.json', '.md'})
evidence = catalog(P, {'text_files': sorted(set(texts)), 'crop_indexes': inputs['crop_indexes']})
existing = {item['path']: item['id'] for item in plan['evidence_artifacts']}
for item in evidence['evidence_artifacts']:
    if item['path'] in existing:
        continue
    record = dict(item)
    record.pop('sha256', None)
    plan['evidence_artifacts'].append(record)
    existing[item['path']] = item['id']


def eid(path):
    return 'artifact:' + existing[path]


decision_path = 'audit/u12-followup/recovery-decisions.json'
write(P / decision_path, {
    'note_id': 'RA12', 'boss': 'BossNotes-2ff3215d6446',
    'before_snapshot': frozen['snapshot_sha256'], 'before_document_hashes': before,
    'actual_final_reports': actual_final,
    'actual_independent_recovery_reports': inputs['actual_recovery_reports'],
    'decisions': proposal['decisions'], 'latest_second_pass_pending': True})
plan['evidence_artifacts'].append({'id': 'u12-followup-recovery-decisions',
    'path': decision_path, 'kind': 'evidence', 'format': 'text'})
existing[decision_path] = 'u12-followup-recovery-decisions'
common = [eid(decision_path), eid('audit/u12-followup/boss-check.md')]
common.extend(eid(item['path']) for item in inputs['actual_recovery_reports'])
common.extend(eid(item['path']) for item in actual_final)
for decision in proposal['decisions']:
    ids = sorted(set(common + [eid(path) for path in decision['direct_evidence_paths']]))
    rid = f'RA12-REC-{decision["number"]:02d}'
    plan['recoveries'].append({
        'id': rid, 'source_ids': decision['source_ids'], 'problem': decision['problem'],
        'candidates': [{'id': f'candidate-{i}', 'text': candidate, 'evidence_ids': ids}
                       for i, candidate in enumerate(decision['candidates'], 1)],
        'selected_candidate_id': 'candidate-1', 'status': 'unresolved', 'evidence_ids': ids,
        'forward_validation': {'status': 'pass', 'method': '原字笔形、相交几何与证明上下文正向核验',
            'inputs': decision['observation'], 'result': decision['forward'], 'evidence_ids': ids},
        'backward_validation': {'status': 'pass', 'method': '竞争字形、缺失笔画及集合相交的反向检验',
            'inputs': decision['candidates'][0], 'result': decision['backward'], 'evidence_ids': ids},
        'return_to_image': {'observation': decision['observation'], 'evidence_ids': ids},
        'reviewer_id': 'BossNotes-2ff3215d6446', 'session_id': 'BossNotes-2ff3215d6446'})
    plan['issues'].append({
        'id': f'RA12-ISSUE-{decision["number"]:02d}', 'status': 'open',
        'description': decision['problem'] + '；实际三人独立补核后的作者修订，待当前完整第二遍接受。',
        'related_ids': decision['source_ids'] + [rid], 'evidence_ids': ids, 'resolution': ''})

u12 = next(s for s in plan['sources'] if s['id'] == 'RA12-P006-U12')
u12['label'] = '字簇〔低至中等置信择优校读：得；备选：仍有〕后接 $m(\\limsup_{k\\to\\infty}E(g_k\\ne f))=0$。'
for key, number in [('transcription_blocks', 41), ('study_blocks', 48)]:
    block = plan[key][number - 1]
    assert block['text'].count('\n仍有\n') == 1
    block['text'] = block['text'].replace('\n仍有\n', '\n〔择优校读：得〕\n')
local_note = ('\n>\n> 第二个零测 limsup 式前的字簇择优校读为单字“得”，取低至中等置信，'
              '保留两字“仍有”的备选。左侧两撇及下接竖、右侧紧连弧点和下回环较支持单字；'
              '右部潦草，不能当作清楚直读。两种读法都可承接此前包含关系和零测结论，'
              '数学推导不能证明原字唯一。')
plan['transcription_blocks'][42]['text'] += local_note
plan['study_blocks'][48]['text'] += local_note
block = plan['study_blocks'][51]
old = '单杆箭头、Cantell 近形及“任意”限定校读'
assert old in block['text']
block['text'] = block['text'].replace(old, '单杆箭头、Cantell 近形、“得／仍有”及“任意”限定校读')
e49 = plan['recoveries'][-2]['evidence_ids']
for key, number in [('transcription_blocks', 41), ('transcription_blocks', 43),
                    ('study_blocks', 48), ('study_blocks', 49), ('study_blocks', 52)]:
    block = plan[key][number - 1]
    assert 'RA12-P006-U12' in block['source_ids']
    block['evidence_ids'] = sorted(set(block.get('evidence_ids', []) + e49))
r20 = next(r for r in plan['recoveries'] if r['id'] == 'RA12-REC-20')
old = '扩大仅数像素，不跨新的分区边界；'
assert old in r20['backward_validation']['result']
r20['backward_validation']['result'] = r20['backward_validation']['result'].replace(
    old, '相交分区集合不变；P5新右界确从1741越过左下区右缘1753到1760，但旧框已与始于1553的右下区相交；')
e50 = plan['recoveries'][-1]['evidence_ids']
r20['evidence_ids'] = sorted(set(r20['evidence_ids'] + e50))
r20['backward_validation']['evidence_ids'] = sorted(set(r20['backward_validation']['evidence_ids'] + e50))

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
overrides = {
    'source_updates': {s['id']: {k: copy.deepcopy(v) for k, v in s.items() if k != 'id'}
                       for s in plan['sources']},
    'block_updates': {f'RA12-{prefix}-{i:03d}': copy.deepcopy(block)
                      for key, prefix in [('transcription_blocks', 'TRANSCRIPTION'), ('study_blocks', 'STUDY')]
                      for i, block in enumerate(plan[key], 1)}}
write(P / 'audit/granular-followup/body-and-source-overrides.json', overrides)
write(P / 'content-plan.json', plan)
(P / 'audit/final-freeze.json').unlink()
result = build(P)
after = {name: sha(P / name) for name in before}
assert before['source-transcript.md'] != after['source-transcript.md']
assert before['study-notes.md'] != after['study-notes.md']
assert len(plan['recoveries']) == len(plan['issues']) == 50
write(P / 'audit/u12-followup/change-summary.json', {
    'before_document_hashes': before, 'after_document_hashes': after,
    'recovery_count_before': 48, 'recovery_count_after': 50,
    'issue_count_before': 48, 'issue_count_after': 50,
    'actual_final_reports_retained': actual_final, 'old_final_chain_abandoned': True,
    'final_rounds': 0, 'latest_second_pass_pending': True})
print(json.dumps({**result, 'document_hashes': after}, ensure_ascii=False))
