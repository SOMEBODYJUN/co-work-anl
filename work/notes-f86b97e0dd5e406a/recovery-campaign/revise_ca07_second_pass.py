#!/usr/bin/env python3
"""Apply Boss-authored CA07 corrections after three frozen recovery appendices.

This is an explicit one-time edit, not a handwriting recognizer or review.
It neither accepts a second pass nor creates any final review.
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
OUT = P / 'audit/second-pass-merge'


def load(p):
    return json.loads(p.read_text(encoding='utf-8'))


def save(p, x):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    expected = {
        'source-transcript.md': '1d8563780fef910ada59bd17fa4deff3a63fa89af03f13df1f9ea408636a2ea6',
        'study-notes.md': '617cd468582950e8f917013da27f9c4a6b1e6eee6109810bbb30b28d8c4cd232',
        'source-target-map.json': 'a36f150c3fb9855053440e782bdee7e6e2f1c3d1eff0cf5b6582e50096c6030d',
    }
    assert {n: sha(P / n) for n in expected} == expected, 'current content moved'
    receipt = load(OUT / 'independent-post-receipts.json')
    assert receipt['boss_read_all_independent_records'] is True
    assert {x['reviewer_id'] for x in receipt['records']} == {
        '/root/ca07_math', '/root/ca07_visual', '/root/ca07_adversarial'}
    for record in receipt['records']:
        for name, digest in record['files'].items():
            assert sha(P / name) == digest, name
    decisions = load(OUT / 'boss-decisions.json')
    assert decisions['status'] == 'authored after all three independent records'
    plan = load(P / 'content-plan.json')
    original = copy.deepcopy(plan)
    blocks = {b['id']: b for k in ['transcription_blocks', 'study_blocks'] for b in plan[k]}
    changes = []

    def block(short):
        prefix = 'CA07-TRANSCRIPTION-' if short.startswith('T') else 'CA07-STUDY-'
        return blocks[prefix + short[1:]]

    def set_text(short, text):
        b = block(short)
        if b['text'] != text:
            changes.append({'target_id': b['id'], 'before_text_sha256': hashlib.sha256(b['text'].encode()).hexdigest(),
                            'after_text_sha256': hashlib.sha256(text.encode()).hexdigest()})
            b['text'] = text

    def replace(short, old, new):
        b = block(short)
        assert b['text'].count(old) == 1, (short, old)
        set_text(short, b['text'].replace(old, new))

    def shared(short, study, text):
        old = block(short)['text']
        replace(study, old, text)
        set_text(short, text)

    def edge(short, added=(), removed=()):
        b = block(short)
        before = list(b['source_ids'])
        b['source_ids'] = sorted((set(before) | set(added)) - set(removed))
        if before != b['source_ids']:
            changes.append({'target_id': b['id'], 'source_ids_before': before, 'source_ids_after': b['source_ids']})

    def sid(page, unit):
        return f'CA07-P{page:03d}-U{unit:02d}'

    shared('T010', 'S030', r'记 $k[t^2,t^3]$ 中 $t^2-a^2=0$ 不能 $a\in k$。〔$a$ 的高位原为短下弯钩，与左边 $t$ 上完整的 2 形不同；此处按上下文拟读为 2。“不能”后直接接 $a\in k$，原未另写连接词。〕')
    replace('S031', r'原末句的 $t^2-a^2=0$ 若要求 $a\in k$',
            r'将原末句 $a$ 上的短下弯钩按上下文拟读为 2，得到 $t^2-a^2=0$；这一幂值并非仅凭该钩逐笔确定。若要求 $a\in k$')
    replace('TV-006', r'若取原末尾所写的常数 $a\in k$，则 $t^2-a^2$ 不是零多项式；',
            r'把原 $a$ 的高位短下弯钩按上下文恢复为 2 时，若取原末尾所写的常数 $a\in k$，则 $t^2-a^2$ 不是零多项式；该条件性解释不把短钩当作逐笔清晰的 2。')
    replace('S030', r'$X=V(y^2-x^3)$ 在 $\mathbb A^2$ 中的表示',
            r'$X=V(y^2-x^3)$ 在 $\mathbb A^2$ 中的表示〔$A$ 上短弯钩按二维环境恢复为 2；“的表示”为上下文恢复，末“示”合读相隔的两墨团。〕')
    replace('S031', r'两坐标说明环境是 $\mathbb A^2$。',
            r'两坐标说明环境是 $\mathbb A^2$，原 $A$ 上标只有短弯钩。图前短语按“的表示”恢复：首组小圈接下兜，中组横交竖并下折；末两墨团合读“示”，其间距是此读法的限制。')

    shared('T017', 'S009', r'循环生成元。 $f(b)=0$ $n\text{—}\deg f(x)$〔题头首二字以“循环”为较优上下文读法，保留“给示”异读；首字双斜、低围圈未逐笔定字。次数处横线自 $n$ 右腹起，上方有孤点。〕')
    replace('TV-007', r'题头取“循环生成元”：首字双斜与低围圈对应“循”，次字与第七页“环”的离横、下折相参。另一独立读法“给示”保留在恢复记录中。',
            r'题头显示“循环生成元”为较优上下文读法，另保留“给示”异读。首字左侧双长斜、下回和右侧低围圈可拟为“循”，仍不足逐笔排除“给”；第二字的离体短冠、回竖和右侧独斜与第四页“环”更相近。第七页“环”是同手另一写法。这些字形对照先于下面的数学解释，循环模的事实本身不能确定原题头。')
    edge('TV-007', [sid(4, 14)])
    replace('S010', '> [!note] 补充｜两个证明工具', '> [!note] 补充｜题头与两个证明工具')
    replace('S010', '>\n> 除以首一', r'''>
> 题头以“循环”为较优上下文读法，同时保留“给示”异读。首字双斜、下回与低围圈只支持有限的字形恢复；第二字的离冠、回竖和右下独斜可与第四页“环”对照。数学上，$A[b]$ 可看成由 $1$ 循环生成的 $A[T]$ 模，其中 $T$ 作用为乘 $b$；底层 $A$ 模却不必单生成，例如 $\mathbb Z[\sqrt2]$ 需要 $1,\sqrt2$。此数学解释不代替原字判断。
>
> 除以首一''')
    edge('S010', [sid(2, 1), sid(2, 4), sid(2, 6), sid(2, 7), sid(4, 14), sid(7, 2)])

    shared('T018', 'S009', r'$A[b]=\sum_{i=0}^{n}Ab^i$，$A$ 模生成组〔$\Sigma$ 右上另有一枚独立细点，不并入上限。“生成组”为上下文恢复：模后长折接下钩，中字有长交笔，末字左折、右拱及低回。〕')
    shared('T020', 'S011', r'$\Leftarrow$〔原符作曲缘内双横。〕 $b$ 在 $A$ 上整， $\exists n,\ a$〔右低粗短斜、右上远处细点〕 st $f(x)=x^n+a_{n-1}x^{n-1}\cdots a_1x+a_0;0$〔原 st 内无点。展开中段原有两枚疏点；式末为上点下短曲及 0，另见下一行 $f(b)=0$。〕')
    edge('T020', [sid(2, 11)])
    replace('TV-008', '> 把系数随和式指标统一为 $a_k$',
            r'> 存在式中 $a$ 后的高点和低短斜在黑字保形；结合后面的系数列，蓝文将它理解为系数 $a_i\in A$，不把这两笔称为清楚写成的下标 $i$。原 $st$ 表示满足随后关系。把系数随和式指标统一为 $a_k$')
    replace('S012', '> 在非零系数环中令',
            r'> 存在式中 $a$ 后为远高细点及低粗短斜，黑字保留其位置；由后面的系数列，在蓝文按 $a_i\in A$ 理解。这个系数读法属于上下文恢复，原 $st$ 内没有标点。' + '\n>\n> 在非零系数环中令')
    shared('T022', 'S011', r'$\forall m\ge n,$ $1,\ldots,b^{n-1}$ 是一组生成元〔“是一组生成元”为上下文恢复：“是”收笔贴后字，其后有独立一横、左折右拱低回及长挑穿短笔；“成元”较清楚，整句不按每字清晰识读。〕')
    replace('S012', r'前一行原写求和上限 $n$，多列入的 $b^n$ 已在 $S$，仍是同一个生成组。',
            r'前面的第一次生成和原写上限 $n$；多列入的 $b^n$ 已在 $S$，两列生成元张成同一个 $A$ 模 $A[b]$，并非同一个生成组。例如 $A=\mathbb Z$、$b=2$、$f(T)=T-2$ 时，$\{1\}$ 和 $\{1,2\}$ 是不同的生成组，却都生成 $\mathbb Z$。')
    edge('S012', [sid(2, 9), sid(2, 20)])
    edge('TV-010', [sid(2, 6), sid(2, 7), sid(2, 8)])

    edge('TV-014', [sid(4, 14)])
    edge('TV-015', [sid(5, 8), sid(5, 9)])
    edge('S026', [sid(5, 8), sid(5, 9)])
    edge('TV-016', removed=[sid(5, 9)])
    edge('S024', [sid(5, 6)])

    shared('T063', 'S035', r'eg. $V$ 是有限〔此处另有独立上折、下竖与右侧双回字团，按上下文恢复为“维”〕 $k$〔后括内有较高斜点、横波、另一枚细针点、短柱及 B 形连笔，右闭括外下方另有独立小点。〕 $b\in\operatorname{End}_k(V)$〔算子原字为高斜干接低圈的 $b/6$ 形；$E$ 冠横离开主干。〕')
    replace('TV-017', r'第一句原写“有限 $k$”，括内密笔按原形保留；由后文 $\operatorname{End}_k(V)$、标量作用与有限生成的陈述，本例对象释为有限维 $k$ 向量空间，不把该释义冒充括内缩记的逐字展开。',
            r'第一句在完整“限”字之后、$k$ 之前另有上折、下竖和双回的独立字团；按后文的有限生成及 $\operatorname{End}_k(V)$ 语境选读为“维”，黑字仍记录这组笔形。$k$ 后括内另有密笔缩记，括外小点也单独保留。整个对象释为有限维 $k$ 向量空间，不把这个释义冒充括内缩记的逐字展开。')
    replace('S036', r'原“有限 $k$”后的缩记保留其上点、折波与 B 形。由后文 $\operatorname{End}_k(V)$、作用及有限生成的陈述，本例释为有限维 $k$ 向量空间；这并不是把缩记逐字展开为“向量空间”。',
            r'完整“限”字后、$k$ 前有独立的上折、下竖及双回字团，按有限生成和算子空间的上下文选读为“维”，黑字保留其笔形限制。$k$ 后括内的较高斜点、折波、另一枚细针点、短柱及 B 形是另一组缩记，右括外下方另有小点。本例整体释为有限维 $k$ 向量空间，这并不是把括内缩记逐字展开成“向量空间”。')
    shared('T067', 'S037', r'$k[t]$ 多项式〔“项”右部冠横上另有独立细点。末字为由形：上短斜、长竖穿扁圈；保留原形，数学对象的恢复见下方蓝注。〕')
    shared('T069', 'S037', r'$V\in v,$ $T\cdot v\text{〔低点〕}=b(v)$〔$T$ 冠横分开；公式中的乘点就是 $T$ 与 $v$ 之间较高的窄墨点。另有 $T$ 干右小斜笔，式内“低点”对应 $v$ 右下的孤墨，不把同一乘点再记一次。〕')
    replace('TV-018', r'原反序 $V\in v$ 和旁边两枚额外墨点均已照录。',
            r'原反序 $V\in v$ 已照录；乘点之外，另保留 $T$ 干右的小斜笔与 $v$ 右下的低点。')
    edge('TV-019', [sid(5, 10), sid(5, 15)])
    edge('S038', [sid(5, 10), sid(5, 15), sid(5, 17)])

    shared('T080', 'S040', r'$A[b_1,\ldots,b_s]=\sum A\,b_1^{e_1}\cdots b_s^{e_1}$〔左括内首末生成元之间原为小圆点和极淡斜横；右侧幂积中隔原为细短横及较低弯弧，排印省略号只表示省写序列。求和符上下空白，末幂 $e$ 后原为一枚短斜直笔。〕')
    shared('T086', 'S042', r'$B\cong A[x_1,\ldots,x_s]/\ker\varphi$〔首末变量间原有细短斜，偏右较高处另有独立小点；末下标在此为离体的短 s 弯。〕')
    shared('T087', 'S042', r'有限型 $+$ 整 $\Longleftrightarrow$ 模有限。〔第一个“限”字左上另有极淡独立针点，保留为孤墨，不赋字符值。原关系符外有左右两弧，内有两短横。〕')
    shared('T088', 'S040', r'$A[b_1,\ldots,b_s]$ $b_1,\ldots,b_s$ 整元 $\Rightarrow$ $A[b_1,\ldots,d_s]$ 有限 $A$ 模，〔左侧代数括内的中隔为一近一远、不同高度的短墨；整元列的中隔是一条右端下收的长波弯；右侧结论括内的中隔为短点及分离的较长浅折划。结论 $A$ 后左括顶部为独细点、下部长挑。末生成元原字母左抱弯，纸面为 $d$ 形。〕')
    replace('TV-023', "任取 $b\\in B$，有限模判据使 $b$ 满足 $A'$ 系数首一式。",
            "任取 $b\\in B$，有 $A'[b]\\subseteq C=B$；$C$ 是含同一单位的中间环，且为有限 $A'$ 模。由中间环判据，$b$ 满足 $A'$ 系数首一式。")
    edge('TV-023', [sid(4, 8), sid(4, 10), sid(4, 11)], [sid(4, 12), sid(4, 13)])

    # The following metadata and evidence selections are authored separately,
    # after all independent appendices have actually been read by the Boss.
    for change in decisions['source_labels']:
        item = next(x for x in plan['sources'] if x['id'] == change['source_id'])
        item['label'] = change['label']
    for extra in decisions.get('additional_target_edges', []):
        edge(extra['short_target'], extra.get('added', []), extra.get('removed', []))

    inputs = load(OUT / 'evidence-inputs.json')
    cat = catalog(P, inputs)
    evidence_by_path = {x['path']: x for x in plan['evidence_artifacts']}
    for a in cat['evidence_artifacts']:
        if a['path'] in evidence_by_path:
            assert evidence_by_path[a['path']]['id'] == a['id'], a['path']
        evidence_by_path[a['path']] = a
    plan['evidence_artifacts'] = list(evidence_by_path.values())
    path_evidence = {x['path']: 'artifact:' + x['id'] for x in plan['evidence_artifacts']}
    for page in load(P / 'manifest.json')['pages']:
        path_evidence[page['image']['path']] = 'image:' + page['id']
        for region in page['regions']:
            path_evidence[region['image']['path']] = 'image:' + region['id']
    decision_evidence = path_evidence['audit/second-pass-merge/boss-decisions.json']
    source_observations = decisions['source_observation_record']
    observed = load(P / source_observations)
    assert len(observed['pages']) == 8 and len(observed['regions']) == 48
    plan['observations'] = [{'pass': 1, 'reviewer_id': '/root/ca07_visual',
        'session_id': '/root/ca07_visual', 'path': source_observations,
        'artifact_id': path_evidence[source_observations].removeprefix('artifact:')}]

    def ev(paths):
        return sorted({path_evidence[x] for x in paths} | {decision_evidence})

    for d in decisions['recoveries']:
        rid = d['recovery_id']
        r = next(x for x in plan['recoveries'] if x['id'] == rid)
        i = next(x for x in plan['issues'] if x['id'] == rid.replace('-R', '-I'))
        evidence = ev(d['evidence_paths'])
        r['source_ids'] = sorted(set(d.get('source_ids', r['source_ids'])))
        if 'selected_text' in d:
            r['candidates'].append({'id': 'boss-second-pass-revised', 'text': d['selected_text'], 'evidence_ids': evidence})
            r['selected_candidate_id'] = 'boss-second-pass-revised'
        else:
            selected = next(c for c in r['candidates'] if c['id'] == r['selected_candidate_id'])
            selected['evidence_ids'] = sorted(set(selected['evidence_ids'] + evidence))
        for candidate in d.get('additional_candidates', []):
            r['candidates'].append({'id': candidate['id'], 'text': candidate['text'], 'evidence_ids': ev(candidate.get('evidence_paths', d['evidence_paths']))})
        r['problem'] += '\n第二遍处理：' + d['correction']
        r['evidence_ids'] = sorted(set(r['evidence_ids'] + evidence))
        for key in ['forward_validation', 'backward_validation', 'return_to_image']:
            if key in d:
                r[key].update(d[key])
            r[key]['evidence_ids'] = sorted(set(r[key]['evidence_ids'] + evidence))
        r['status'] = 'unresolved'
        i['description'] += '\n第二遍处理：' + d['correction']
        prior_targets = [x for x in i['related_ids'] if x.startswith(('CA07-TRANSCRIPTION-', 'CA07-STUDY-'))]
        i['related_ids'] = sorted(set(r['source_ids'] + [rid] + prior_targets + d.get('related_target_ids', [])))
        i['evidence_ids'] = sorted(set(i['evidence_ids'] + evidence))
        i['status'], i['resolution'] = 'open', ''

    new = decisions['new_recovery']
    e = ev(new['evidence_paths'])
    plan['recoveries'].append({
        'id': 'CA07-R057', 'source_ids': [sid(7, 10)], 'problem': new['problem'],
        'candidates': [{'id': c['id'], 'text': c['text'], 'evidence_ids': e} for c in new['candidates']],
        'selected_candidate_id': new['selected_candidate_id'], 'status': 'unresolved', 'evidence_ids': e,
        'forward_validation': {**new['forward_validation'], 'evidence_ids': e},
        'backward_validation': {**new['backward_validation'], 'evidence_ids': e},
        'return_to_image': {'page_ids': [], 'region_ids': [], 'observation': new['observation'], 'evidence_ids': e},
        'reviewer_id': '/root/ca07_adversarial', 'session_id': '/root/ca07_adversarial',
    })
    plan['issues'].append({'id': 'CA07-I057', 'status': 'open', 'description': new['problem'],
        'related_ids': [sid(7, 10), 'CA07-R057', 'CA07-TRANSCRIPTION-087', 'CA07-STUDY-042'],
        'evidence_ids': e, 'resolution': ''})

    assert len(plan['recoveries']) == len(plan['issues']) == 57
    assert len(plan['sources']) == 133
    assert len(plan['transcription_blocks']) + len(plan['study_blocks']) == 160
    assert not any(x.get('pass') == 2 for x in plan['observations'])
    save(OUT / 'content-plan-before-revision.json', original)
    save(OUT / 'explicit-edit-receipt.json', {'boss_id': 'BossNotes-2ff3215d6446', 'document_hashes_before': expected,
        'changes': changes, 'status': 'authored corrections; awaiting independent current second pass'})
    save(P / 'content-plan.json', plan)
    result = build(P)
    result['document_hashes'] = {n: sha(P / n) for n in expected}
    save(OUT / 'new-content-hashes.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
