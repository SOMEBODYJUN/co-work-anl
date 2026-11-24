"""Assemble explicitly authored RA06 metadata; never invent review observations."""
from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'notes/RA06/project'
D = P / 'proposals/rebuild'

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def sid(page, *numbers):
    return [f'RA06-P{page:03d}-U{n:02d}' for n in numbers]

# Each entry is an editorial judgment by /root after reading both complete drafts.
SUPPLEMENTS = {
    'N-p1-definition': (sid(1, 1, 2), '补入开覆盖和紧性的定义，说明子空间定义与环境开集覆盖等价。'),
    'N-p1-countable-proof': (sid(1, 3), '从可数基为任意开覆盖选取可数子覆盖，逐点验证仍覆盖。'),
    'N-p1-margin-explanation': (sid(1, 4), '不强指原箭头；另用可数球覆盖构造稠密集，再构造有理半径基。'),
    'N-p1-nonconverse': (sid(1, 3), '余可数拓扑给出 Lindeloff 但不第二可数的完整反例。'),
    'N-p1-radius': (sid(1, 8), '选两点距离的三分之一，并用三角不等式验证开球不交。'),
    'N-p1-empty': (sid(1, 6, 10), '补入空紧集情形，避免对空半径集取最小值。'),
    'N-p1-example-explain': (sid(1, 11), '完整核验两点拓扑的单点紧、开但不闭；另存有限枚举输入输出。'),
    'N-compact-bounded-proof': (sid(1, 6), '固定中心，用整数半径球的有限子覆盖给出紧集有界性。'),
    'N-p2-closed-proof': (sid(2, 2), '补完整闭子集紧性引理，括注字形仍与原稿疑点分开。'),
    'N-p1-exercise-answer': (sid(1, 5), '用嵌套闭方块公共点独立完成原练习，与原稿子列路线分别保留。'),
    'N-p2-scope': (sid(2, 1), '保留有限性原用词，限定有限维等价关系并给无限离散空间反例。'),
    'N-sequential-equivalence-proof': (sid(2, 1), '以有限覆盖、分离点列和 Lebesgue 数论证给出度量空间紧与列紧双向证明。'),
    'N-bw-tool': (sid(3, 3), '在调用前用闭区间套与有限次坐标抽列证明 Bolzano–Weierstrass。'),
    'N-norm-equivalence-tool': (sid(2, 3, 10), '用标准基上界及有界点列子列证明任意有限维范数等价，说明直径常数。'),
    'N-p2-cube-correction': (sid(2, 4, 5), '区分指数的上下文恢复与笔画确认；半开方块反例说明必须使用闭方块。'),
    'N-p2-first-index': (sid(2, 7), '第一次细分应编号 Q1；补上有限个有限覆盖合并的反证。'),
    'N-p3-subsequence-explain': (sid(3, 2, 3), '用已先证明的 BW 定理及 Q0 闭性解释子列极限，避免循环。'),
    'N-p3-index-repair': (sid(3, 1, 7, 8), '依差集选点把直径估计改用 Q_{m_k-1}，另保留改选 x_m 的方案。'),
    'N-derived-definition': (sid(3, 9, 12), '补入导集、去心邻域、孤立点、闭包及边界的准确记号。'),
    'N-derived-basic-proof': (sid(3, 9, 13, 14), '逐点证明闭包为 E 与导集之并，再证明导集与孤立点的不交分解。'),
    'N-p3-forward-repair': (sid(3, 13), '把集合不属于的类型混用改为两集不交，并完成自密推出无孤立点。'),
    'N-p3-backward-explain': (sid(3, 14), '说明反向推导使用孤立点集为空这一前提。'),
    'N-derived-closed-proof': (sid(3, 15), '以补集中的邻域直接证明度量空间导集闭，供后文下降性调用。'),
    'N-derived-iteration': (sid(3, 10, 11), '定义递归导集、区分 n≥2 与 n=1，给出开区间反例。'),
    'N-p3-closure-scope': (sid(3, 16), '指出闭包等于原集及导集包含均要求原集闭。'),
    'N-perfect-proof': (sid(4, 1), '证明完全集等价自密闭集并给出闭区间、开区间、收敛点列的例子。'),
    'N-cardinality-distinction': (sid(4, 2, 4), '分开幂集、通常开集和所有拓扑的计数；完整证明通常开集有 c 个。'),
    'N-ball-count-answer': (sid(4, 5), '用正半径区间作下界、所有实半径作上界，证明合格同心球恰有 c 个。'),
    'N-ball-max-answer': (sid(4, 6), '用到补集距离求最大同心球，另分 U=R 及含点开区间族的最大性。'),
    'N-p4-family-notation': (sid(4, 10, 11, 12), '区分区间族 Gx 与其并 Ix，说明无穷端点时族需扩充。'),
    'N-component-construction-proof': (sid(4, 10, 11, 13), '依左右端点上下确界分别覆盖 y<x 与 y>x，并验证最大性。'),
    'N-component-endpoint-proof': (sid(4, 14), '以开性扩张区间反证有限端点不属于 U，限定无穷端点的语义。'),
    'N-basis-count-proof': (sid(4, 7, 8), '用开集族幂集给上界，固定可数基任添其余开集给下界。'),
    'N-basis-criterion': (sid(4, 9), '分别列出给定拓扑下细化开邻域及抽象集合族基的交叠条件。'),
    'N-interval-connected-proof': (sid(5, 10, 11), '原进制提示尚未唯一读定；给出完整上确界证明且不冒充原路线。'),
    'N-connected-subset-interval': (sid(5, 10), '以遗漏中间点产生分离，证明实轴连通子集必为区间。'),
    'N-component-definition-scope': (sid(5, 1, 2), '补明开集、有限端点条件和无穷端点约定，连接最大区间与连通分支。'),
    'N-components-disjoint-proof': (sid(5, 3, 4), '保留原反证提示，分别用最大性和端点条件完成不同区间不交。'),
    'N-components-corollary-proof': (sid(5, 5), '从不同分支不交说明两点可以属于同一个区间，并给具体例子。'),
    'N-open-decomposition-proof': (sid(5, 6), '把开区间唯一表示订正为开集分解，用有理数枚举证明可数性和唯一性。'),
    'N-rn-boxes-proof': (sid(5, 7), '明确高维旁注对象为开集，利用有理端点基及重叠覆盖给出存在性和非唯一例子。'),
    'N-local-connected-definition': (sid(5, 8, 9), '定义分支和局部连通，用共有点连通集之并说明分支存在与划分。'),
    'N-local-connected-theorem-proof': (sid(5, 8, 9), '补上 U 开条件；先证分支开再嵌入可数基，反例用无理数集。'),
}

EDITORIAL = {
    'T-title': '原序转写的笔记题名。',
    **{f'T-p{i}-heading': f'按物理页序标示原稿第 {i} 页；空白第6页只在来源记录中登记。' for i in range(1, 6)},
    'N-title': '依本稿实际主题拟定学习稿题名。',
    'N-editorial': '向读者说明黑色原文、蓝色补证纠错、红色原待填与拼写约定。',
    'N-toc': '为全部七节及其子节列出可点击目录，顺序依据证明依赖安排。',
    'N-derived-heading': '将导集、自密与孤立点的内容集中为第四节。',
    'N-open-heading': '将实轴开集、邻域和基的计数集中为第五节。',
    'N-components-heading': '将实区间连通工具移到构成区间分解之前。',
}

source = json.loads((D / 'source-units.json').read_text())
by_id = {x['id']: x for x in source}
mapping = json.loads((D / 'mapping.json').read_text())
existing = {x['id'] for x in mapping['targets']}
for target, (source_ids, why) in SUPPLEMENTS.items():
    if target in existing:
        continue
    evidence = sorted({f"image:{by_id[x]['page_id']}" for x in source_ids})
    evidence.append('artifact:editorial-record')
    if target == 'N-p1-example-explain':
        evidence.append('artifact:two-point-enumeration')
    mapping['targets'].append({
        'id': target, 'artifact_id': 'study', 'source_ids': source_ids,
        'status': 'unresolved' if any(by_id[x]['status'] == 'unresolved' for x in source_ids) else 'resolved',
        'origin': 'supplement', 'old_ids': [], 'evidence_ids': evidence, 'explanation': why,
    })
for target, why in EDITORIAL.items():
    if target in existing:
        continue
    mapping['targets'].append({
        'id': target, 'artifact_id': 'transcription' if target.startswith('T-') else 'study',
        'source_ids': [], 'status': 'resolved', 'origin': 'editorial', 'old_ids': [],
        'evidence_ids': ['artifact:editorial-record'], 'explanation': why,
    })
write_json(D / 'mapping.json', mapping)

lines = ['# RA06 编排与数学补充依据', '',
         '实际整合者：/root；与原作者 /root/startup_inspection 共同署入 authors。',
         '本记录是作者编辑依据，不是第二遍或最终独立审核。所有新增论证已写入学习稿蓝色块；原稿疑字不得因补证成立而冒充字形确认。',
         '未提供旧稿；不从仓库示例或其他笔记推定原稿内容。', '',
         '## 编排决定', '']
for target, why in EDITORIAL.items():
    lines += [f'- `{target}`：{why}']
lines += ['', '## 补充证明、订正及依赖', '']
for target, (source_ids, why) in SUPPLEMENTS.items():
    lines += [f'- `{target}`（对应 {", ".join(source_ids)}）：{why}']
lines += ['', '## 数学核验与边界情形', '',
          '紧集闭性的半径取 d(x,y)/3，两个半径之和严格小于两点距离；空集单独处理。两点拓扑的所有子族已实际用 Python 枚举，输入及结果见 two-point-enumeration.json。',
          'Heine–Borel 的公共点路线仅用实数完备性；子列路线先证明 BW，再用闭方块保留极限。任意范数下的下界也以 BW 而非待证紧性为前提。',
          '导集闭性在度量空间中证明；高阶导集下降从二阶起无须 E 闭，一阶则补上闭性条件。',
          '基计数以上下界各自完成；最大同心球与最大含点区间分开，U=R、无穷端点、空集均单独说明。',
          '实区间连通的上确界证明先于连通分支调用；局部连通分解明确要求 U 开，原稿未写条件在原位解释。',
          'Q001—Q005 的视觉候选仍存 unresolved.md，等待实际新读者复查；本记录不宣布恢复通过。', '']
(D / 'editorial-record.md').write_text('\n'.join(lines).rstrip()+'\n')
shutil.copyfile(ROOT / 'research/ra06-two-point-enumeration.json', D / 'two-point-enumeration.json')

crops = [
    {'path':'crops/p0001-margin.png','page_id':'p0001','bbox_px':[1630,400,2290,700]},
    {'path':'crops/p0002-top.png','page_id':'p0002','bbox_px':[110,315,1390,710]},
    {'path':'crops/p0002-cube.png','page_id':'p0002','bbox_px':[1120,1120,1780,1375]},
    {'path':'crops/p0002-reduce.png','page_id':'p0002','bbox_px':[90,1410,820,1610]},
] + json.loads((D / 'new-crop-register.json').read_text())
artifacts = [
    {'id':'transcription','path':'proposals/rebuild/source-transcript.md','kind':'transcription','format':'text'},
    {'id':'study','path':'proposals/rebuild/study-notes.md','kind':'study','format':'text'},
    {'id':'editorial-record','path':'proposals/rebuild/editorial-record.md','kind':'evidence','format':'text'},
    {'id':'two-point-enumeration','path':'proposals/rebuild/two-point-enumeration.json','kind':'evidence','format':'text'},
    {'id':'uncertainties','path':'proposals/rebuild/unresolved.md','kind':'evidence','format':'text'},
]
for crop in crops:
    artifacts.append({'id':Path(crop['path']).stem,'path':crop['path'],'kind':'evidence','format':'image',
                      'source_crop':{'page_id':crop['page_id'],'bbox_px':crop['bbox_px']}})

issues = []
for q, source_id, problem in [
    ('Q001','RA06-P002-U02','闭子集引理括注的两字在闭遗传性与闭传递性之间待辨。'),
    ('Q002','RA06-P002-U04','方块指数原笔形与数学应取的维数 n 尚须区分。'),
    ('Q003','RA06-P004-U02','Ex1 中间词及计数对象尚未唯一确定，原值 2^c 已保留。'),
    ('Q004','RA06-P004-U12','最大区间断言后半含 gamma、G 下标的关系未唯一辨定。'),
    ('Q005','RA06-P005-U11','p进制小数与展开之间的连写及其量词未唯一辨定。'),
]:
    issues.append({'id':q,'status':'open','description':problem,'related_ids':[source_id],
                   'evidence_ids':[f"image:{by_id[source_id]['page_id']}",'artifact:uncertainties'],
                   'resolution':''})
write_json(D / 'issues.json', issues)
write_json(P / 'ledger-config.json', {'authors':['/root','/root/startup_inspection'], 'manifest':'manifest.json',
    'artifacts':artifacts, 'source_units':'proposals/rebuild/source-units.json', 'mapping':'proposals/rebuild/mapping.json',
    'observations':'proposals/rebuild/observations.json', 'issues':'proposals/rebuild/issues.json','output':'ledger.json'})
write_json(D / 'remaining-mapping-ids.json', [])
print(json.dumps({'sources':len(source),'targets':len(mapping['targets']),'artifacts':len(artifacts),
                  'open_interpretations':len(issues),'independent_reviews_added':0},ensure_ascii=False))
