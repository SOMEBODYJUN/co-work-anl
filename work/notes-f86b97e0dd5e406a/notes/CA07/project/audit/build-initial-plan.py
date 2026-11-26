"""Compile this note's frozen first readings; make no recovery decisions."""
from pathlib import Path
import hashlib
import json
import sys

PROJECT = Path(__file__).resolve().parents[1]
ROOT = next(parent for parent in PROJECT.parents if (parent / 'tools/build_note_ledger.py').is_file())
sys.path.insert(0, str(ROOT / 'tools'))
from catalog_note_evidence import catalog
from build_note_ledger import build


def read(relative):
    return json.loads((PROJECT / relative).read_text(encoding='utf-8'))


def write(relative, value):
    path = PROJECT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if (PROJECT / 'content-plan.json').exists():
    raise SystemExit('Initial build only: preserve the existing authored plan.')

receipts = read('audit/first-pass/receipts.json')
text_files = []
for receipt in receipts['receipts']:
    for path, expected in receipt['files'].items():
        assert hashlib.sha256((PROJECT / path).read_bytes()).hexdigest() == expected, path
        if path == 'proposals/ca07_visual/observations.json':
            text_files.append({'path': path, 'id': 'ca07-first-observations'})
        else:
            text_files.append(path)
text_files.extend([
    {'path': 'audit/campaign/participants.json', 'id': 'campaign-participants'},
    'audit/first-pass/receipts.json',
    'audit/first-pass/source-box-check.json',
    'audit/boss-initial-full-pages.md',
    'audit/boss-initial-candidates.md',
    'proposals/ca07_math/study-blocks-mapped.json',
    'proposals/ca07_math/source-coverage.json',
    'proposals/ca07_math/mapping-notes.md',
])
inputs = {'text_files': text_files, 'crop_indexes': ['audit/source-units-800/crop-index.json']}
evidence = catalog(PROJECT, inputs)
write('audit/initial-evidence-inputs.json', inputs)
write('audit/initial-evidence-catalog.json', evidence)

sources = read('proposals/ca07_visual/sources.json')
transcription = read('proposals/ca07_visual/transcription-blocks.json')
study = read('proposals/ca07_math/study-blocks-mapped.json')
transcription[0]['text'] = (
    '# 交换代数 7 · 原稿逐页转写\n\n'
    '按原 PDF 物理页序编排。原内容以普通正文收录，补充与订正使用蓝色提示块；'
    '原有明确提问保留红字。初读疑号对应候选记录。\n\n## 物理页 1'
)
transcription[14]['source_ids'] = [f'CA07-P001-U{i:02d}' for i in range(21, 27)]
for kind, blocks in [('TRANSCRIPTION', transcription), ('STUDY', study)]:
    for index, block in enumerate(blocks, 1):
        block['id'] = f'CA07-{kind}-{index:03d}'
        block['text'] = block['text'].replace('color:#bf3030', 'color:red').replace('color:#b91c1c', 'color:red')
        # A target may share several source units. No source/target is accepted
        # until its connected initial reading and recovery review are complete.
        block['status'] = 'resolved' if block['origin'] == 'editorial' else 'unresolved'
for source in sources:
    source['status'] = 'unresolved'

suspects = read('proposals/ca07_visual/initial-suspects.json')
candidate_artifact = evidence['path_to_evidence_id']['proposals/ca07_visual/initial-suspects.json']
boss_artifact = evidence['path_to_evidence_id']['audit/boss-initial-candidates.md']
issues = []
for index, suspect in enumerate(suspects, 1):
    description = f"首读 {suspect['local_id']}：{suspect['problem']}。候选：" + '；'.join(
        candidate['text'] for candidate in suspect['candidates'])
    refs = [candidate_artifact]
    if suspect['local_id'] == 'P1-04':
        description += '；Boss 另据原分区提出“曲线尖点与参数。”，仍待原 PDF 高分辨率裁图及独立检验。'
        refs.append(boss_artifact)
    issues.append({'id': f'CA07-I{index:03d}', 'status': 'open',
        'description': description, 'related_ids': suspect['source_ids'],
        'evidence_ids': refs, 'resolution': ''})

plan = {
    'note_id': 'CA07',
    'authors': ['BossNotes-2ff3215d6446', '/root/ca07_visual', '/root/ca07_math'],
    'review_policy': {'mode': 'user_requested_fixed_trio', 'note_id': 'CA07',
        'boss_id': 'BossNotes-2ff3215d6446', 'authorization_artifact_id': 'campaign-participants',
        'reviewer_ids': ['/root/ca07_visual', '/root/ca07_math', '/root/ca07_adversarial']},
    'sources': sources,
    'transcription_blocks': transcription,
    'study_blocks': study,
    'evidence_artifacts': [{k: v for k, v in item.items() if k != 'sha256'}
                           for item in evidence['evidence_artifacts']],
    'observations': [{'pass': 1, 'reviewer_id': '/root/ca07_visual',
        'session_id': '/root/ca07_visual', 'path': 'proposals/ca07_visual/observations.json',
        'artifact_id': 'ca07-first-observations'}],
    'recoveries': [],
    'issues': issues,
}
write('content-plan.json', plan)
print(json.dumps(build(PROJECT), ensure_ascii=False))
