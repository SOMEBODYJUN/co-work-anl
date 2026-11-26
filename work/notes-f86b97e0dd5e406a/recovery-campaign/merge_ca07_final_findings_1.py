"""Apply only the eight adjudicated findings from three actual CA07 reviews.

No new review or completion decision is generated. All content remains pending
the actual current-version second pass, followed by a new frozen final chain.
"""
from pathlib import Path
import hashlib
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
from build_note_ledger import build
from catalog_note_evidence import catalog
from final_note_reviews import current

P = ROOT / 'work/notes-f86b97e0dd5e406a/notes/CA07/project'
A = P / 'audit/final-e5ab9b2ae651-merge'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    before = load(A / 'invalidated-final-freeze.json')
    assert current(P)[-1] == before['snapshot_sha256']
    assert not (A / 'applied-result.json').exists(), 'do not repeat this merge'
    plan = load(P / 'content-plan.json')
    ledger = load(P / 'ledger.json')
    receipts = load(A / 'independent-final-receipts.json')
    assert len(receipts['actual_reviews']) == 3
    for report in receipts['actual_reviews']:
        assert sha(P / report['path']) == report['sha256']
        assert report['findings'] and report['read_by_boss']

    visual_obs = 'proposals/ca07_visual/post-final-e5ab9b2ae651/corrected-observations-2.json'
    adversarial_obs = 'proposals/ca07_adversarial/post-final-e5ab9b2ae651/corrected-observations.json'
    corrected = load(P / visual_obs)
    prior = load(P / plan['observations'][0]['path'])
    assert corrected['pages'] == prior['pages']
    changes = [(x['region_id'], x['observation']) for x, y in zip(corrected['regions'], prior['regions']) if x != y]
    assert len(corrected['regions']) == len(prior['regions']) == 48
    assert len(changes) == 1 and changes[0][0] == 'p0005-r2c1'
    assert '右上' in changes[0][1] and '细斜' in changes[0][1] and '左下' in changes[0][1] and '圆点' in changes[0][1]

    files = ['audit/final-e5ab9b2ae651-merge/independent-final-receipts.json',
             'audit/final-e5ab9b2ae651-merge/boss-decisions.json', visual_obs, adversarial_obs]
    for role in ['visual', 'math', 'adversarial']:
        directory = P / f'proposals/ca07_{role}/final-e5ab9b2ae651'
        files.extend(str(f.relative_to(P)) for f in sorted(directory.iterdir())
                     if f.is_file() and f.suffix in {'.json', '.jsonl', '.md'})
    indexed = catalog(P, {'text_files': files, 'crop_indexes': []})
    known = {x['path'] for x in plan['evidence_artifacts']}
    plan['evidence_artifacts'].extend(x for x in indexed['evidence_artifacts'] if x['path'] not in known)
    paths = {x['path']: 'artifact:' + x['id'] for x in plan['evidence_artifacts']}
    evidence = [paths['audit/final-e5ab9b2ae651-merge/boss-decisions.json'],
                paths['audit/final-e5ab9b2ae651-merge/independent-final-receipts.json']]
    evidence.extend(paths[x['path']] for x in receipts['actual_reviews'])
    native = {s['id']: paths[f'audit/source-units-800/{s["id"]}-800.png'] for s in plan['sources']}

    def block(kind, identifier):
        return next(x for x in plan[kind] if x['id'] == identifier)

    direct_edges = {
        'CA07-TRANSCRIPTION-037': ['CA07-P003-U06'],
        'CA07-TRANSCRIPTION-060': ['CA07-P005-U04', 'CA07-P005-U05'],
        'CA07-TRANSCRIPTION-068': ['CA07-P005-U18'],
    }
    for identifier, sources in direct_edges.items():
        target = block('transcription_blocks', identifier)
        assert not set(sources) & set(target['source_ids'])
        target['source_ids'] = sorted(target['source_ids'] + sources)
        target['evidence_ids'] = sorted(set(target.get('evidence_ids', [])) | {native[s] for s in sources} | set(evidence))
    for kind, identifier in [('transcription_blocks', 'CA07-TRANSCRIPTION-037'),
                             ('study_blocks', 'CA07-STUDY-016')]:
        target = block(kind, identifier)
        assert target['text'].count('同前一行的单肩形') == 1
        target['text'] = target['text'].replace('同前一行的单肩形', '同上文 $D$ 式右侧的单肩形')

    recoveries = {x['id']: x for x in plan['recoveries']}
    issues = {x['id']: x for x in plan['issues']}
    rec = recoveries['CA07-R026']
    assert 'CA07-P004-U11' not in rec['source_ids']
    rec['source_ids'] = sorted(rec['source_ids'] + ['CA07-P004-U11'])
    rec['problem'] += '\n本轮终审处理：原第(3)条的C有限A模单列在P004-U11；正向链实际使用此条件，补入直接来源及原生图证据。'
    rec['forward_validation']['inputs'] = '(1)整⇒(2)有限，取C=A[b]；原第(3)条同时要求A[b]⊆C⊆B与C有限A模，后续原行另取M=C。'
    rec['forward_validation']['result'] = '由前页已证的整⇒模有限得A[b]有限。取C=A[b]同时满足原第(3)条的夹包含及C有限A模，故原(1)⇒(3)可经过已证(2)而成立。'
    extra = set(evidence + [native['CA07-P004-U11']])
    rec['evidence_ids'] = sorted(set(rec['evidence_ids']) | extra)
    for field in ['forward_validation', 'backward_validation', 'return_to_image']:
        rec[field]['evidence_ids'] = sorted(set(rec[field]['evidence_ids']) | extra)
    selected = next(x for x in rec['candidates'] if x['id'] == rec['selected_candidate_id'])
    selected['evidence_ids'] = sorted(set(selected['evidence_ids']) | extra)
    issues['CA07-I026']['related_ids'] = sorted(set(issues['CA07-I026']['related_ids']) | {'CA07-P004-U11'})

    rec = recoveries['CA07-R056']
    assert '备注代 b 可使 f(b)=0。' in rec['problem']
    rec['problem'] = rec['problem'].replace('备注代 b 可使 f(b)=0。', '原另给 f(b)=0；代入商余式后用这一条件消去商项。')
    rec['forward_validation']['inputs'] = '非零交换系数环A中，f∈A[T]为n≥1次首一式，原另给f(b)=0，g∈A[T]；迭代中的当前非零余项最高项为cT^d，且d≥n。'
    rec['forward_validation']['result'] = '减cT^(d−n)f严格降低当前余项的次数，有限步得g=qf+r，其中r=0或deg r<n。再代入b，用原给f(b)=0得g(b)=q(b)f(b)+r(b)=r(b)，故有低幂表示；反向每个A b^i本就在A[b]中，得到两包含。零系数环另按既有元素关系分支处理。'
    rec['backward_validation']['inputs'] += '；另检验删去f(b)=0后是否仍可由长除转为同值余式。'
    rec['backward_validation']['result'] += ' 若删去f(b)=0，取A=Z、g=f=T、b=1，则长除余式r=0但g(b)=1，故求值后的低幂表示不能仅靠首一性推出。'

    annotations = {
        'CA07-R019': '本轮终审处理：T037补所比较的P003-U06直接边；T037与S016将同前一行改为同上文D式右侧，避免忽略中间列式。原r形选读及蓝色方阵规范不变。',
        'CA07-R032': '本轮终审处理：T060的箭头说明明确引出发式与a·1=0，补P005-U04/U05的直接来源和原生证据。原黑箭、红问与蓝色单位论证不变。',
        'CA07-R037': '本轮终审处理：T068明确比较上行t，补P005-U18直接来源与原生图；第5页末区观察将多、项、式三字与其后独立由形末团分记。',
    }
    for identifier, note in annotations.items():
        recoveries[identifier]['problem'] += '\n' + note
    for identifier in ['CA07-R019', 'CA07-R026', 'CA07-R032', 'CA07-R037', 'CA07-R056']:
        rec = recoveries[identifier]
        rec['evidence_ids'] = sorted(set(rec['evidence_ids']) | set(evidence))
        for field in ['forward_validation', 'backward_validation', 'return_to_image']:
            rec[field]['evidence_ids'] = sorted(set(rec[field]['evidence_ids']) | set(evidence))
        issue = issues[identifier.replace('-R', '-I')]
        issue['description'] = rec['problem']
        issue['evidence_ids'] = sorted(set(issue['evidence_ids']) | set(rec['evidence_ids']))

    old_passes = plan['observations']
    assert [x['pass'] for x in old_passes] == [1, 2]
    write(A / 'superseded-observation-bindings.json', old_passes)
    plan['observations'] = [{**old_passes[0], 'path': visual_obs,
                             'artifact_id': paths[visual_obs].removeprefix('artifact:')}]
    # The previous actual pass remains immutable evidence, but its active binding
    # is explicitly retired. A real report on this new candidate is still needed.
    for key in ['sources', 'transcription_blocks', 'study_blocks', 'recoveries', 'issues']:
        for item in plan[key]:
            item['status'] = 'open' if key == 'issues' else 'unresolved'
    for issue in plan['issues']:
        issue['resolution'] = '当前修订候选等待非作者对最新两稿、映射及全部恢复的实际第二遍确认；历史接受报告保存在证据与归档中。'
    write(P / 'content-plan.json', plan)
    result = build(P)
    assert sha(P / 'audit/final-freeze.json') == sha(A / 'invalidated-final-freeze.json')
    (P / 'audit/final-freeze.json').unlink()
    if (P / 'audit-report.json').exists():
        shutil.copy2(P / 'audit-report.json', A / 'before-audit-report.json')
        (P / 'audit-report.json').unlink()
    hashes = {n: sha(P / n) for n in before['document_hashes']}
    mapping = load(P / 'source-target-map.json')
    edge_count = sum(len(x['source_ids']) for x in mapping['target_to_sources'])
    assert edge_count == 756
    assert all(hashes[n] != before['document_hashes'][n] for n in hashes)
    result.update({'old_snapshot_invalidated': before['snapshot_sha256'],
                   'document_hashes': hashes, 'content_edges': edge_count,
                   'next_gate': 'actual_current_version_second_pass_then_three_new_final_reviews',
                   'review_decisions_generated': False})
    write(A / 'applied-result.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
