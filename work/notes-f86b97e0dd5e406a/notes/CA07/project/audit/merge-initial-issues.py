"""Boss's explicit current-note issue union, before any recovery selection."""
from pathlib import Path
import json
import sys

P = Path(__file__).resolve().parents[1]
ROOT = next(parent for parent in P.parents if (parent / 'tools/build_note_ledger.py').is_file())
sys.path.insert(0, str(ROOT / 'tools'))
from catalog_note_evidence import catalog
from build_note_ledger import build


def read(rel):
    return json.loads((P / rel).read_text(encoding='utf-8'))


def write(rel, value):
    (P / rel).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


plan = read('content-plan.json')
assert not plan['recoveries'] and len(plan['issues']) == 46
union = read('proposals/ca07_adversarial/initial-issue-union-additions.json')
records = {r['local_id']: r for r in union['records']}
visual = read('proposals/ca07_visual/initial-suspects.json')
new_groups = {
    'UNION-06': ('第二页生成元题头', ['循环生成元。', '给出／给示生成元。']),
    'UNION-07': ('第一次求和之后的 A 模语尾', ['A 模有限。', 'A 模生成元／生成组。']),
    'UNION-09': ('第二页最后的单字引导', ['找 f(x)∈A[x]。', '求 f(x)∈A[x]。']),
    'UNION-16': ('条件（3）的 C 的数学类型', ['C 是含单位的中间子环，并作为 A 模有限生成。',
        'C 只需是任意包含 A[b] 的有限 A 子模，无须由乘 b 保持。']),
    'UNION-28': ('第一页末行的整性底环字母', ['原句末字为 b；学习稿须说明定义的底环是 A。',
        '末字原写 A，原句已经直接写成 b 整于 A。']),
    'UNION-29': ('尖点分枝图的性质与图前短字', ['两枝在左交汇的尖点曲线示意，前有描述该图的短语。',
        '右侧笔迹是方向箭头或粗括记，并非两枝曲线示意。']),
    'UNION-30': ('等价证明两次方向箭头', ['先写向左蕴含，从 b 整推出有限；后另起向右蕴含，从有限推出 b 整。',
        '第一符是属于号或一般连词，第二符方向相反，不能按上述双向证明归属。']),
    'UNION-31': ('第一次及第二次幂和的实际上限', ['第一次上限 n，后一次为 n−1；两种生成式都成立，首式有冗余项。',
        '两次均为 n−1，第一次短横和 1 只是笔淡。']),
    'UNION-32': ('除法路线之前的方法转换短词', ['也可用。', '也可以／也可以用。']),
    'UNION-33': ('任意交换环上的首一除法及生成式证明', ['因除式首一，逐项消最高次可得余式；代 b 得 g(b)=r(b)，再证两边包含。',
        '必须假定 A 为域才可除，或把纸面可能重复的 g(x) 直接当任意商即可得到结论。']),
}
extra_texts = [
    'proposals/ca07_adversarial/initial-issue-source-map.json',
    'proposals/ca07_adversarial/initial-issue-union-additions.json',
]
added = catalog(P, {'text_files': extra_texts, 'crop_indexes': []})
plan['evidence_artifacts'].extend({k: v for k, v in item.items() if k != 'sha256'}
                                 for item in added['evidence_artifacts'])
union_evidence = added['path_to_evidence_id'][extra_texts[1]]
work = []
for index, (item, issue) in enumerate(zip(visual, plan['issues']), 1):
    supplements = [r for r in union['records']
                   if item['local_id'] in r['visual_local_ids'] and r['local_id'] not in new_groups]
    issue['description'] += ''.join('\n并入 ' + r['local_id'] + '：' + r['why_separate_or_add']
                                    for r in supplements)
    issue['evidence_ids'].append(union_evidence)
    issue['related_ids'] = sorted(set(issue['related_ids']) |
        {sid for r in supplements for sid in r['source_ids']})
    candidates = list(item['candidates'])
    if item['local_id'] == 'P1-04':
        candidates.append({'id': 'boss-c3', 'text': '曲线尖点与参数。',
                           'evidence_paths': ['regions/p0001-r2c1.png', 'audit/boss-initial-candidates.md']})
    work.append({'recovery_id': f'CA07-R{index:03d}', 'issue_id': issue['id'],
        'primary_initial_id': 'visual:' + item['local_id'], 'source_ids': issue['related_ids'],
        'problem': issue['description'], 'initial_candidates': candidates,
        'union_ids': [r['local_id'] for r in supplements]})
for union_id, (title, candidates) in new_groups.items():
    item = records[union_id]
    index = len(plan['issues']) + 1
    issue = {'id': f'CA07-I{index:03d}', 'status': 'open',
        'description': title + '。' + item['why_separate_or_add'] + '\n候选：' + '；'.join(candidates),
        'related_ids': item['source_ids'], 'evidence_ids': [union_evidence], 'resolution': ''}
    plan['issues'].append(issue)
    work.append({'recovery_id': f'CA07-R{index:03d}', 'issue_id': issue['id'],
        'primary_initial_id': union_id, 'source_ids': item['source_ids'],
        'problem': issue['description'], 'initial_candidates': [
            {'id': f'c{i}', 'text': text, 'evidence_paths': extra_texts}
            for i, text in enumerate(candidates, 1)], 'union_ids': [union_id]})

assert {r['local_id'] for r in union['records']} <= {x for w in work for x in w['union_ids']}
write('audit/recovery-worklist.json', {
    'note_id': 'CA07', 'basis': 'Three independently frozen initial readings and Boss union; no candidate selected.',
    'source_count': 133, 'records': work,
    'initial_record_paths': [
        'proposals/ca07_visual/initial-suspects.json',
        'proposals/ca07_math/initial-suspects.json',
        'proposals/ca07_adversarial/initial-suspects.md',
    ] + extra_texts,
    'selection_status': 'All records pending independent native 800/1200 dpi recovery.'
})
work_artifact = catalog(P, {'text_files': ['audit/recovery-worklist.json'], 'crop_indexes': []})
plan['evidence_artifacts'].extend({k: v for k, v in item.items() if k != 'sha256'}
                                 for item in work_artifact['evidence_artifacts'])
write('content-plan.json', plan)
print(json.dumps(build(P), ensure_ascii=False))
