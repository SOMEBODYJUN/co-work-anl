"""Apply five explicit original-name source edges after actual trio reports.

This authors a bounded provenance correction; no review or acceptance is made.
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

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

before = {name: sha(P / name) for name in ['source-transcript.md', 'study-notes.md', 'source-target-map.json']}
assert before == {
    'source-transcript.md': 'c0fb0c63abf731a3ba5693e14d7f1c93f130296716d7ad5484e4ec41403b095d',
    'study-notes.md': '373e90a051418289d80f176e7ffa9958dfb6fd16bd79b0329c3080d9ad48c1aa',
    'source-target-map.json': '46aee54cef869184c66c6319bfb46cfb37f9f1f1aad9e02f7c8b351e84b2e56b',
}
plan, ledger = (read(P / name) for name in ['content-plan.json', 'ledger.json'])
assert len(plan['recoveries']) == len(plan['issues']) == 41
assert not ledger['final_rounds'] and not (P / 'audit/final-freeze.json').exists()
assert not any(x['pass'] == 2 for x in plan['observations'])
reports, text_files, crop_indexes = [], [], []
for role in ['visual', 'math', 'adversarial']:
    folder = Path(f'proposals/ra12_{role}/current-version-review')
    report = read(P / folder / 'second-pass-report.json')
    assert report['reviewer_id'] == report['session_id'] == '/root/ra12_' + role
    assert report['document_hashes_start'] == before == report['document_hashes_end']
    for key, field in [('source_unit_ids', 'source_units'), ('target_unit_ids', 'target_units'), ('recovery_ids', 'recoveries'), ('issue_ids', 'issues')]:
        assert set(report['reviewed_scope'][key]) == {x['id'] for x in ledger[field]}
    reports.append({'reviewer_id': report['reviewer_id'], 'path': str(folder / 'second-pass-report.json'), 'sha256': sha(P / folder / 'second-pass-report.json'), 'findings': report['findings']})
    text_files += [str(x.relative_to(P)) for x in sorted((P / folder).glob('*')) if x.suffix in ['.json', '.md']]
    if (P / folder / 'crop-index.json').exists():
        crop_indexes.append(str(folder / 'crop-index.json'))

archive = P / 'history/name-reference-46aee54cef86'
archive.mkdir(parents=True, exist_ok=False)
for name in ['content-plan.json', 'authored-content.json', 'ledger.json', 'source-transcript.md', 'study-notes.md', 'source-target-map.json']:
    shutil.copy2(P / name, archive / name)
shutil.copy2(P / 'audit/granular-followup/body-and-source-overrides.json', archive / 'body-and-source-overrides.json')
write(archive / 'actual-review-reports.json', {'document_hashes': before, 'reports': reports, 'accepted_as_pass_2': False})

evidence = catalog(P, {'text_files': text_files, 'crop_indexes': crop_indexes})
existing = {x['path']: x['id'] for x in plan['evidence_artifacts']}
for item in evidence['evidence_artifacts']:
    assert item['path'] not in existing
    record = dict(item)
    record.pop('sha256', None)
    plan['evidence_artifacts'].append(record)
    existing[item['path']] = item['id']

added_edges = []
for key, index, sources in [
    ('transcription_blocks', 23, ['RA12-P003-U16']),
    ('transcription_blocks', 29, ['RA12-P003-U09', 'RA12-P003-U16']),
    ('study_blocks', 29, ['RA12-P003-U09', 'RA12-P003-U16']),
]:
    block = plan[key][index - 1]
    target = f'RA12-{"TRANSCRIPTION" if key == "transcription_blocks" else "STUDY"}-{index:03d}'
    for source in sources:
        assert source not in block['source_ids']
        block['source_ids'].append(source)
        unit_path = f'audit/granular-reread-7f2b9670fcd1/{source}-800.png'
        artifact = 'artifact:' + existing[unit_path]
        block['evidence_ids'] = sorted(set(block.get('evidence_ids', []) + [artifact]))
        added_edges.append({'source_id': source, 'target_id': target, 'reason': '目标明确复述本处原姓名近形，须登记内容来源而不只作为字形比较图证。'})
    block['source_ids'] = sorted(block['source_ids'])

record_path = Path('audit/name-reference-update/decision.json')
write(P / record_path, {
    'note_id': 'RA12', 'boss': 'BossNotes-2ff3215d6446', 'before_document_hashes': before,
    'actual_reports': reports, 'added_edges': added_edges,
    'correction_scope': '仅原姓名直接复述的五条语义来源边。T029/S029先前已有P3U09/U16直接图证，不能误报成缺图；T023本次另加U16原800图。两份正文字节不变。',
    'candidates': ['保留正文，补齐三个目标明确引用的两个原姓名来源，同时给T023补原800直接证据。', '因两个目标已有比较图或来源已指向其他段落便不登记本目标内容边；此法使原姓名复述缺对应语义来源，拒绝。'],
    'forward': '逐一从T023、T029、S029所写的Englov/Engrov返回P3U09及P3U16的原墨位置，补对应目标来源。',
    'backward': '从P3两个原位置反查三个明确复述目标；五条新增关系各自均有实际内容主张，不以纯字形比较制造多余内容边。',
    'latest_second_pass_pending': True,
})
for relative in [record_path, Path('audit/name-reference-update/apply_mapping.py')]:
    ident = 'name-reference-' + relative.stem
    plan['evidence_artifacts'].append({'id': ident, 'path': str(relative), 'kind': 'evidence', 'format': 'text'})
    existing[str(relative)] = ident
new_evidence = ['artifact:' + existing[r['path']] for r in reports] + ['artifact:' + existing[str(record_path)]]
rec = next(x for x in plan['recoveries'] if x['id'] == 'RA12-REC-37')
rec['source_ids'] = sorted(set(rec['source_ids'] + ['RA12-P003-U09', 'RA12-P003-U16']))
rec['problem'] += '；T023、T029、S029直接复述第3页两原姓名，新增五条实际内容来源边；对应字形图与内容来源分开核对。'
rec['candidates'][0]['text'] += ' 对T023补P3U16、对T029/S029各补P3U09及P3U16内容边；保持已有图证并给T023补U16原800图。'
rec['candidates'].append({'id': 'candidate-3', 'text': '已有比较图或来源已映射别段即可省去本目标的直接原姓名内容来源；会遗漏可追溯的实际复述关系，拒绝。', 'evidence_ids': sorted(set(rec['evidence_ids'] + new_evidence))})
rec['evidence_ids'] = sorted(set(rec['evidence_ids'] + new_evidence))
for field in ['forward_validation', 'backward_validation', 'return_to_image']:
    rec[field]['evidence_ids'] = sorted(set(rec[field]['evidence_ids'] + new_evidence))
rec['forward_validation']['result'] += ' 三个目标直接复述原两姓名，分别建立实际五条来源边。'
rec['backward_validation']['result'] += ' 已有P3两裁图只证明图证存在，不能替代目标对原名字母串的内容来源；反向逐源查得三个目标均纳入。'
issue = next(x for x in plan['issues'] if x['id'] == 'RA12-ISSUE-37')
issue['description'] += '；数学员本轮发现的同一姓名引用五条来源边由Boss补齐，仍待最新映射的独立接受。'
issue['related_ids'] = sorted(set(issue['related_ids'] + ['RA12-P003-U09', 'RA12-P003-U16', 'RA12-TRANSCRIPTION-023', 'RA12-TRANSCRIPTION-029', 'RA12-STUDY-029']))
issue['evidence_ids'] = sorted(set(issue['evidence_ids'] + new_evidence))

override = read(P / 'audit/granular-followup/body-and-source-overrides.json')
for name, key in [('TRANSCRIPTION', 'transcription_blocks'), ('STUDY', 'study_blocks')]:
    for index, block in enumerate(plan[key], 1):
        override['block_updates'][f'RA12-{name}-{index:03d}'] = {k: block[k] for k in ['text', 'source_ids', 'evidence_ids', 'explanation', 'origin'] if k in block}
write(P / 'audit/granular-followup/body-and-source-overrides.json', override)
authored = read(P / 'authored-content.json')
for key in ['sources', 'transcription_blocks', 'study_blocks']:
    authored[key] = copy.deepcopy(plan[key])
write(P / 'authored-content.json', authored)
write(P / 'content-plan.json', plan)
result = build(P)
after = {name: sha(P / name) for name in before}
assert all(after[name] == before[name] for name in ['source-transcript.md', 'study-notes.md'])
assert len(added_edges) == 5 and after['source-target-map.json'] != before['source-target-map.json']
write(P / 'audit/name-reference-update/change-summary.json', {'before_document_hashes': before, 'after_document_hashes': after, 'added_edges': added_edges, 'recoveries': 41, 'issues': 41, 'final_rounds': 0, 'latest_second_pass_pending': True})
print(json.dumps({**result, 'added_edges': len(added_edges), 'document_hashes': after}, ensure_ascii=False))
