"""Record the actual three-reviewer provenance findings without changing prose."""
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

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

before = {name: sha(P / name) for name in
          ['source-transcript.md', 'study-notes.md', 'source-target-map.json']}
assert before['source-target-map.json'] == '9cd121842c42c40149315162faaea965eed7ec1d564f72494864d665091643dc'
archive = P / 'history/before-provenance-9cd121842c42'
archive.mkdir(parents=True, exist_ok=False)
for name in ['content-plan.json', 'authored-content.json', 'ledger.json',
             'source-transcript.md', 'study-notes.md', 'source-target-map.json', 'audit-report.json']:
    shutil.copy2(P / name, archive / name)
plan = read(P / 'content-plan.json')
authored = read(P / 'authored-content.json')
ledger = read(P / 'ledger.json')
old_map = read(P / 'source-target-map.json')
artifacts = {a['path']: a['id'] for a in ledger['artifacts']}

source_additions = {
    'RA12-STUDY-052': ['RA12-P001-U05', 'RA12-P001-U06', 'RA12-P001-U07'],
    'RA12-TRANSCRIPTION-015': [f'RA12-P004-U{i:02d}' for i in range(14, 19)],
    'RA12-STUDY-013': [f'RA12-P004-U{i:02d}' for i in range(15, 19)],
    'RA12-STUDY-021': [f'RA12-P004-U{i:02d}' for i in range(14, 19)],
    'RA12-STUDY-045': ['RA12-P006-U01'],
}
shi = ['proposals/ra12_visual/final-f733447a84a1/p0002-lusin-shi-1200.png',
       'proposals/ra12_adversarial/final-f733447a84a1/p5-is-in-statement-1200.png']
evidence_paths = {
    'RA12-TRANSCRIPTION-004': shi,
    'RA12-STUDY-005': shi,
    'RA12-TRANSCRIPTION-029': [
        'proposals/ra12_visual/final-f733447a84a1/p0001-yaoqiu-reference-1200.png',
        'proposals/ra12_visual/crops/p0003-second-egorov-yong-1200.png',
        'proposals/ra12_visual/crops/p0004-second-annuli-yong-1200.png'],
    'RA12-TRANSCRIPTION-043': [
        'proposals/ra12_math/second-review-crops/p4-kao-of-kaolu-1200.png',
        'proposals/ra12_math/second-review-crops/p6-left-expanded-clip-1200.png'],
}
evidence_additions = {tid: ['artifact:' + artifacts[path] for path in paths]
                      for tid, paths in evidence_paths.items()}
overrides = {
    'note_id': 'RA12', 'before_document_hashes': before,
    'source_additions': source_additions,
    'evidence_additions': evidence_additions,
    'evidence_paths': evidence_paths,
    'reason': '三份真实第二遍更新报告发现的摘要、明确跨页原稿引用及笔形对照证据漏链。正文和原图均不改。内容来源与仅用于字形比较的图证分别登记。',
}
write(P / 'audit/provenance-update/overrides.json', overrides)

def get_block(content, target_id):
    kind = 'transcription_blocks' if '-TRANSCRIPTION-' in target_id else 'study_blocks'
    return content[kind][int(target_id.rsplit('-', 1)[1]) - 1]

for content in [plan, authored]:
    for tid, ids in source_additions.items():
        block = get_block(content, tid)
        assert not (set(ids) & set(block['source_ids']))
        block['source_ids'].extend(ids)
    for tid, ids in evidence_additions.items():
        block = get_block(content, tid)
        block['evidence_ids'] = sorted(set(block.get('evidence_ids', []) + ids))

registered = []
def register(path, aid):
    assert not any(a['path'] == path or a['id'] == aid for a in plan['evidence_artifacts'])
    plan['evidence_artifacts'].append({'id': aid, 'path': path, 'kind': 'evidence', 'format': 'text'})
    registered.append('artifact:' + aid)

for role, stem in [('visual', 'update-report'), ('math', 'second-pass-report'), ('adversarial', 'second-pass-report')]:
    for extension in ['json', 'md']:
        path = f'proposals/ra12_{role}/post-final-update/{stem}.{extension}'
        register(path, f'post-update-{role}-{extension}')
register('audit/provenance-update/overrides.json', 'provenance-overrides')
register('audit/provenance-update/delta.json', 'provenance-delta')
register('audit/provenance-update/apply_provenance.py', 'provenance-implementation')
evidence = sorted(set(registered + [eid for ids in evidence_additions.values() for eid in ids]))
sources = sorted({sid for ids in source_additions.values() for sid in ids})
selected = '为五个含明确跨页原稿引用的目标补18条精确内容来源边并同步逆向关联；为四个笔形说明目标补9条已存在的1200 dpi比较或原矢量图证链接。两份正文、源框、原PDF均不改变。'
forward = ('逐项将S052第1页摘要对应U05/U06/U07；T015及S021的第4页无限测度引用对应U14–U18；'
           'S013的环带及局部有限引用对应U15–U18；S045所指第6页证明方向对应U01。'
           'T004/S005、T029、T043的笔形比较分别链接是、要求/或用/需要用、考虑/页外既有原矢量。')
backward = ('逐条反查新增18边均由目标现有文字的明确原页引用支持；笔形对照仅增加证据链接，'
            '不冒充同句原稿内容来源。不删除任何旧边，不把全部来源笼统连至所有目标，正文哈希须保持完全相同。')
recovery = {
    'id': 'RA12-REC-21', 'source_ids': sources,
    'problem': '真实当前第二遍发现的目标语义出处及直接比较证据漏链，待同三人验证本次元数据增量。',
    'candidates': [
        {'id': 'candidate-1', 'text': selected, 'evidence_ids': evidence},
        {'id': 'candidate-2', 'text': '保持旧关联，认为来源已在其他目标出现即足够；不能追溯本目标明示的跨页内容，故拒绝。', 'evidence_ids': evidence},
        {'id': 'candidate-3', 'text': '把所有111个来源接到所有目标；失去逐段真实出处并产生无据关联，故拒绝。', 'evidence_ids': evidence},
    ],
    'selected_candidate_id': 'candidate-1', 'status': 'unresolved',
    'evidence_ids': evidence,
    'forward_validation': {'status': 'pass', 'method': '从目标现有明确引用逐条回原页及原图证',
                           'inputs': '三份独立更新报告、当前目标原文、源单元标签与实际1200 dpi图证。',
                           'result': forward, 'evidence_ids': evidence},
    'backward_validation': {'status': 'pass', 'method': '从每条新增出处返回目标，并核对零正文差异',
                            'inputs': selected, 'result': backward, 'evidence_ids': evidence},
    'return_to_image': {'observation': '本项是原图已实读内容的出处修复。三人当前全量复核记录详列实重开图和同源先前实读；此处不声称新读或产生新字形结论。' + forward,
                        'evidence_ids': evidence},
    'reviewer_id': 'BossNotes-2ff3215d6446', 'session_id': 'BossNotes-2ff3215d6446',
}
assert len(plan['recoveries']) == 20 and len(plan['issues']) == 20
plan['recoveries'].append(recovery)
plan['issues'].append({'id': 'RA12-ISSUE-21', 'status': 'open',
    'description': recovery['problem'], 'related_ids': sources + ['RA12-REC-21'],
    'evidence_ids': evidence, 'resolution': ''})
delta = {'note_id': 'RA12', 'before_document_hashes': before,
         'new_source_edges': [{'target_id': tid, 'source_id': sid} for tid, ids in source_additions.items() for sid in ids],
         'new_evidence_links': [{'target_id': tid, 'evidence_id': eid} for tid, ids in evidence_additions.items() for eid in ids],
         'review_status': 'awaiting_actual_trio_delta_validation',
         'recovery_ids_added': ['RA12-REC-21'], 'issue_ids_added': ['RA12-ISSUE-21']}
write(P / 'audit/provenance-update/delta.json', delta)
write(P / 'authored-content.json', authored)
write(P / 'content-plan.json', plan)
build(P)
after = {name: sha(P / name) for name in before}
assert all(before[n] == after[n] for n in ['source-transcript.md', 'study-notes.md'])
new_map = read(P / 'source-target-map.json')
def edges(mapping):
    return {(target['id'], sid) for target in mapping['target_to_sources'] for sid in target['source_ids']}
added = edges(new_map) - edges(old_map)
expected = {(tid, sid) for tid, ids in source_additions.items() for sid in ids}
assert added == expected and len(added) == 18
assert not edges(old_map) - edges(new_map)
for target in new_map['target_to_sources']:
    kind = 'transcription_target_ids' if target['artifact_id'] == 'transcription' else 'study_target_ids'
    for sid in target['source_ids']:
        assert target['id'] in next(s for s in new_map['source_to_targets'] if s['id'] == sid)[kind]
delta.update(after_document_hashes=after, unchanged_body_hashes=True,
             source_edges_before=len(edges(old_map)), source_edges_after=len(edges(new_map)),
             exact_new_source_edges_verified=True, reverse_edges_verified=True)
write(P / 'audit/provenance-update/delta.json', delta)
build(P)
print(json.dumps({'hashes': after, 'source_edges': [len(edges(old_map)), len(edges(new_map))],
                  'new_direct_evidence_links': len(delta['new_evidence_links']),
                  'recoveries': len(plan['recoveries']), 'issues': len(plan['issues'])}, ensure_ascii=False))
