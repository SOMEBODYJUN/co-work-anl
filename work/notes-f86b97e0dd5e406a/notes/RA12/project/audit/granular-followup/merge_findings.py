"""Boss synthesis of the three actual failed 7f2b9670fcd1 reviews.

No pass observations, reviewer decisions, or final approvals are generated here.
The original review files and frozen version are retained without modification.
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

SNAPSHOT = '7f2b9670fcd152d0b6063e42be72d373976253cec1b571497d51d215efbbfdd4'
BOSS = 'BossNotes-2ff3215d6446'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

freeze = read(P / 'audit/final-freeze.json')
assert freeze['snapshot_sha256'] == SNAPSHOT
before = {name: sha(P / name) for name in ['source-transcript.md', 'study-notes.md', 'source-target-map.json']}
reports = []
for role in ['visual', 'math', 'adversarial']:
    path = P / f'proposals/ra12_{role}/final-7f2b9670fcd1/final-report.json'
    report = read(path)
    assert report['reviewer_id'] == '/root/ra12_' + role
    assert report['snapshot_sha256'] == SNAPSHOT and report['findings']
    assert report['document_hashes_start'] == before == report['document_hashes_end']
    reports.append({'reviewer_id': report['reviewer_id'], 'path': str(path.relative_to(P)), 'sha256': sha(path), 'findings': report['findings']})

archive = P / 'history/final-review-7f2b9670fcd1'
archive.mkdir(parents=True, exist_ok=False)
for name in ['content-plan.json', 'authored-content.json', 'ledger.json', 'source-transcript.md', 'study-notes.md', 'source-target-map.json', 'audit-report.json', 'audit-prefinal-report.json']:
    shutil.copy2(P / name, archive / name)
shutil.copy2(P / 'audit/final-freeze.json', archive / 'final-freeze.json')
write(archive / 'actual-failed-reviews.json', {'snapshot_sha256': SNAPSHOT, 'reports': reports, 'sealed': False})

plan = read(P / 'content-plan.json')
assert len(plan['recoveries']) == 21 and len(plan['issues']) == 21
original_plan = copy.deepcopy(plan)
plan['observations'] = [x for x in plan['observations'] if x['pass'] == 1]

def block(kind, number):
    return plan['transcription_blocks' if kind == 'T' else 'study_blocks'][number - 1]

def replace(kind, number, old, new):
    b = block(kind, number)
    assert old in b['text'], (kind, number, old)
    b['text'] = b['text'].replace(old, new)

def append_blue(kind, number, text):
    b = block(kind, number)
    assert b['origin'] == 'supplement'
    b['text'] += '\n>\n> ' + text.replace('\n', '\n> ')

def add_sources(kind, number, sources):
    b = block(kind, number)
    b['source_ids'] = list(dict.fromkeys(b['source_ids'] + sources))

def sid(page, unit):
    return f'RA12-P{page:03d}-U{unit:02d}'

# Exact original connectors, repetition and outer grouping.
replace('T', 7, '设 $f:X\\to Y$。$X$ 有一个开覆盖', '设 $f:X\\to Y$。〔择优校读：且〕$X$ $\\exists$ 一个开覆盖')
replace('T', 7, r'\bigcup_{a\in A}(f|_{X_a})^{-1}(U)', r'\bigcup_{a\in A}\bigl((f|_{X_a})^{-1}(U)\bigr)')
append_blue('T', 8, r'$Y$ 的句点与下一 $X$ 之间另有完整字簇，择优读“且”，中至较高置信；同手第 3 页“且”的左直、右包和下拖支持此读，“因／即／则”等为备选。数学证明只需独立的开覆盖条件，不能证明该字唯一。$X$ 后实见 $\exists$ 样量词，原口语排为“$X$ $\exists$ 一个开覆盖”。末并项的外括与限制函数括各自可见，已保留两枚左括和 $U$ 后两枚右括。')
replace('S', 10, r'=\bigcup_a(f|_{X_a})^{-1}(U)', r'=\bigcup_a\bigl((f|_{X_a})^{-1}(U)\bigr)')
append_blue('S', 11, r'原引理在 $Y$ 句点后、下一 $X$ 前有独立字簇，保真稿以中至较高置信校读“且”，并保留 $X$ 后的 $\exists$；本节将其连成规范条件句。最后逆像并项的外括也照原保留。')

# A disputed small cluster is described, not silently dropped or forced to a word.
append_blue('T', 8, '下一行“注意”右下的小簇有两点及卧钩。视觉、对抗复读更倾向它是“意”的偏位心底；数学复读倾向另一个草写“则”。此处择优保留“注意”，并明确登记小簇及“独立则”备选，不声称已唯一分字，也不把它当不存在。“到”候选欠至和刂的独立结构。两种有据解释均只引出限制连续，不改变证明方向。')
add_sources('T', 8, [sid(1, 12)])
append_blue('S', 11, '“注意”右下小簇的分字另有“意的偏位心底／独立则”两读；采用前者保留主文，后者及不同审阅意见均入台账。学习证明不据该语气字改变任何假设。')
replace('T', 10, '$U$ 只与有限多个 $X_a$ 相交', '$U$ 只与有有限个 $X_a$ 相交')
append_blue('T', 11, '邻域句“只与”后实见连续两个“有”形，后接“限、个”，没有独立“多”字；上文保留“只与有有限个”的复写。学习稿用通常说法“只与有限多个”，含义是交到的覆盖成员数量有限。')
add_sources('T', 11, [sid(1, 17), sid(1, 18)])
replace('S', 12, '局部有限的定义是：', '按原句的数学含义规范表述局部有限：')
append_blue('S', 13, '原邻域句实写“只与有有限个”，重复“有”且未另写“多”。保真稿留出这两处字面特点；本节的“只与有限多个”是规范表述。')

replace('T', 13, '可测函数。$\\forall\\delta', '可测函数，则 $\\forall\\delta')
replace('T', 13, r'm(E\setminus F_\delta)<\delta,\qquad f|_{F_\delta}', r'm(E\setminus F_\delta)<\delta,\qquad \text{s.t.}\ f|_{F_\delta}')
replace('T', 14, r'\exists F_{i,\delta}\overset{\text{紧闭}}{\subset}E_i,\qquad', r'\exists F_{i,\delta}\overset{\text{紧闭}}{\subset}E_i,\qquad\text{s.t.}\,')
replace('T', 20, r'F_\delta\overset{\text{闭}}{\subset}E,\qquad', r'F_\delta\overset{\text{闭}}{\subset}E,\qquad\text{s.t.}\,')
append_blue('T', 15, '原姓名连写近 Lebegue，未见 e 与 g 间独立的 s；上文按所指的内正规性定理统一排作 Lebesgue，不把标准拼法当作逐字原迹。两处存在式后的 s.t. 以及本页定理限制连续式前的 s.t. 保留原位置，缩写的点号按通常形式排印。')
# The paragraph refers to the actual two P2 s.t. locations: U05 and U12.
replace('T', 15, '两处存在式后的 s.t. 以及本页定理限制连续式前的 s.t. 保留原位置', '本页紧闭集存在式后及定理限制连续式前的两处 s.t. 保留原位置')
add_sources('T', 15, [sid(2, 5)])
append_blue('S', 21, '原定理“可测函数”后还有“则”，限制连续式前实写 s.t.；本节分别连为条件与结论，s.t. 译作“使”。')
append_blue('S', 23, '内正规性姓名的原形近 Lebegue，本节采用通行的 Lebesgue；闭集损失式前原 s.t. 译作“满足”。原损失链的并项有两枚左括、仅一枚右括，保真稿照录省写，以下数学分组均规范闭合。')
append_blue('S', 25, '第 3 页首个测度预算前原有 s.t.，保真稿已照录；本节把它并入选集条件。该页后续联合损失式原只在测度层写一对括弧，未另给每个差集加内括；这里的逐项分组是规范排印。')

replace('T', 16, r'&=m\left(\bigcup_{i=1}^{\ell}(E\setminus F_{i,\delta})\right)', r'&=m\bigl(\bigcup_{i=1}^{\ell}\bigl(E\setminus F_{i,\delta}\bigr)')
append_blue('T', 17, '该并项的原迹是两枚左括、只有一枚右括，上式按原数目排印；唯一右括配哪一层不强判。学习稿使测度作用于整个并并补足分组。补括本身不能纠正差项中漏写下标的 $E$。')
replace('T', 20, r'=m\left(\bigcup_{k=1}^{\infty}(E\setminus F_k)\right)', r'=m\bigl(\bigcup_{k=1}^{\infty}E\setminus F_k\bigr)')
append_blue('T', 21, r'后一个测度项的原迹只见 $m$ 后及末 $F_k$ 后的一对括弧，并号与 $E$ 间无独立内左括。上式保留原省写，数学含义为对各个 $E\setminus F_k$ 取并；学习稿可补内括明确作用域。')

replace('T', 22, r'因 $f$ a.e. 有限，$m(E(|f|=+\infty))=0$。', r'因 $f$ a.e. 有限，$m(E(|f|=+\infty))=0$〔括弧及绝对值左界作规范排印；原迹见下述说明〕。')
append_blue('T', 23, r'零测式在 $+\infty$ 后至等号前只见一枚独立右弧；$m$ 后和 $E$ 后有左弧样轮廓，但 $E$ 后的小弯及短线是否兼作绝对值左界存在分笔歧义，不强判为两个清楚独立的左括。上文完整双层括及 $|f|$ 明示为数学规范化。前文“a.e. 有限”恢复的集合是 $\{x\in E:|f(x)|=\infty\}$；只取 $f=+\infty$ 会漏掉负无穷值。原右弧计数比左界分笔更确定。')
replace('S', 26, r'原稿用 a.e. 有限性写 $m(E(|f|=+\infty))=0$，令', r'原稿以 a.e. 有限性给出无穷值集零测；将原省写的括弧和左界规范排为 $m(E(|f|=+\infty))=0$，再令')
append_blue('S', 27, r'这条零测式的原末只见一个右括样弧，$E$ 后左弧与绝对值左界的分笔不能唯一确定。前面的完整公式是明确标出的规范分组；数学根据是排除正、负两个无穷值层，不能反推原笔已经写全双右括及绝对值左界。')

replace('T', 28, r'=((E\setminus G_\delta)\setminus H_\delta)\cup', r'=(E\setminus G_\delta\setminus H_\delta)\cup')
append_blue('T', 29, r'分解式首个并项原只见 $E$ 前、$H_\delta$ 后的一对括弧，$G_\delta$ 到 $H_\delta$ 间只见一条斜竖样笔。上式保留这一省写，按集合差左结合解释；也保留该笔兼作内右括及差集线的连写候选，不声称原有完整的两层分组。')
add_sources('T', 29, [sid(4, 13)])
replace('S', 28, '并写\n\n$$\nE\\setminus H_\\delta=', '并给出差集分解（原首项仅一对括弧，以下按左结合规范分组）\n\n$$\nE\\setminus H_\\delta=')
append_blue('S', 29, r'原首项 $E\setminus G_\delta\setminus H_\delta$ 仅写一对括弧，$G_\delta/H_\delta$ 间的单笔还可能兼作括样与差集线。由前面的 $H_\delta\subset E\setminus G_\delta$，采用左结合 $(E\setminus G_\delta)\setminus H_\delta$；若右结合为 $E\setminus(G_\delta\setminus H_\delta)$，会把应删的 $H_\delta$ 留回首项，不能给出原所需分解。')

replace('T', 35, '$A$ 和 $B$', '$A\\,\\&\\,B$')
replace('S', 41, '$A$ 和 $B$', '$A\\,\\&\\,B$')
append_blue('T', 36, r'$A$ 与 $B$ 间的原符号有交叉斜笔和闭回环，较合手写 &；上文保留为 $\&$，学习解释可译作“和”。备选“及”欠其通常的末捺，不能把中文译写当原字。')
append_blue('S', 42, r'残句里 $A$、$B$ 之间保留手写 $\&$ 的校录；证明中的“且／和”是对连接作用的中文解释。')
add_sources('S', 42, [sid(5, u) for u in range(8, 11)])
replace('T', 39, r'**Pf. (1) $\Rightarrow$ (3).**', r'**Pf. (1) $\to$ (3).**')
append_blue('T', 40, r'页首的原箭头只有单杆，保真写 $\to$；这里连接的是前页的条件编号，数学上表示从 (1) 推出 (3)，学习稿以 $\Rightarrow$ 规范表示蕴涵。')
add_sources('T', 40, [sid(6, 1)])
replace('S', 45, r'第 6 页明写并证明 (1) $\Rightarrow$ (3)。', r'第 6 页以单杆箭头写 (1) $\to$ (3)，并证明这个方向；本节以 $\Rightarrow$ 规范表示蕴涵。')

replace('T', 42, '（几乎处处）', '（几乎〔择优校读：任意〕）')
replace('S', 48, '随后取好集，写几乎处处', '随后取好集，原括语保留为“（几乎〔择优校读：任意〕）”，其数学含义为对几乎处处的 $x$：')
append_blue('T', 43, '定理名原形近 Borel Cantell，第二词末的 i 未明显成形；本文依可和失配事件的语境采用通行拼法 Borel–Cantelli。“几乎”后有大小不等的两组笔迹：第一组斜起、左短竖和右折，第二组点、叠折及下部卧钩。视觉与对抗复读较支持“任意”，故中等置信择优校读；数学复读提出“大组为在，右侧纵向小字疑为处处／旁补”的备选，另有径读“处处”候选。原两组形态不同于第 5 页两个近同形的“处”，不能称“处处”为清楚直读。候选及审阅分歧均保存，数学只确定整句表示全测度点的量词，不证明某一字值唯一。')
append_blue('S', 49, r'原定理名近 Borel Cantell，按通行姓名排作 Borel–Cantelli；原括语“几乎”后的字形择优校读“任意”，保留“在＋纵向小字”和“处处”备选，详见保真稿。这里的标准结论“对几乎处处的 $x$”来自零测坏集及取补运算。不能删去“几乎”：若 $E=[0,1]$ 且所有 $D_k=\{0\}$，坏 limsup 仍零测，而点 $0$ 从不进入好集。')

add_sources('S', 3, [sid(1, 6), sid(2, 16), sid(2, 2), sid(5, 19), sid(2, 5), sid(2, 12), sid(3, 2)])
replace('S', 3, '> | a.e. | 关于 Lebesgue 测度，除一个零测集外成立 |', '> | a.e. | 关于 Lebesgue 测度，除一个零测集外成立 |\n> | s.t. | such that，“使／满足”；保真稿在原位置保留缩写 |')
add_sources('S', 5, [sid(1, 5), sid(1, 6)])

# Update the summary only for statements it actually makes and attach direct units.
replace('S', 52, '保留三类拼接 |', '保留三类拼接；另记“且”、原 $\\exists$、“有”的复写及注意字簇分读 |')
replace('S', 52, '“紧闭” |', '“紧闭”；则、s.t.、Lebegue 近形及两左一右括 |')
replace('S', 52, '原错误与重复均保留，', '零测式的省写括弧及左界明示规范化；原错误与重复均保留，')
replace('S', 52, '次可加性用 $\\le$ |', '次可加性用 $\\le$，差集首项明确左结合 |')
replace('S', 52, '旁注到“分”止 |', '旁注以 $\\&$ 连接并到“分”止 |')
replace('S', 52, '内并上限省写 |', '内并上限省写；单杆箭头、Cantell 近形及“任意”限定校读 |')
add_sources('S', 52, [sid(2, 2), sid(2, 5), sid(6, 1)])

labels = {
    sid(1, 8): 'Y的句点之后另有独立字簇，择优校读且（中至较高置信，因/即/则为备选）；随后X及独立存在量词∃、一个开覆盖，X=并X_i。索引全集A/Δ/Λ样异写统一A。',
    sid(1, 11): '逆像并分解及定义等号；首逆像上标仅短横，恢复−1明示；定义右侧末并项有外括包住限制逆像，两左及U后两右各自可见。',
    sid(1, 12): '注意 f|Xa 连续；意右下小簇择优作偏位心底，数学复读另读独立则；点/卧钩存在明确，分字有限置信，正文注记备选，不省略墨迹。',
    sid(1, 18): 'U只与有有限个Xa相交。只与后两个有形均有穿横和下弯，限后直接个，未见独立多；保真留复写，学习规范为有限多个。',
    sid(2, 2): '设f是E上a.e.有限的可测函数，则。数字后独立则形及U钩清楚，与P3则g同手可比。',
    sid(2, 15): '原m(并(E\\Fiδ)中两左一右，后等于求和m(E\\Fiδ)<δ。两处E缺i，等号保持；完整数学分组与下标订正另标。',
    sid(3, 5): '原m(E\\Fδ)=m(并E\\Fk)≤求和δ/(2k)，测度层一对括，无内差项括。末k低位，保留2k及低指数备选；学习按首行几何预算订正。',
    sid(3, 11): '无穷值零测式：+∞后只一枚右弧；m后及E后左弧样笔，后者与绝对值左界的分笔不唯一。m(E(|f|=+∞))=0明确作为规范排印，集合由a.e.有限恢复。',
    sid(4, 13): 'E\\Hδ=(E\\Gδ\\Hδ)∪(Gδ\\Hδ)。首项一对括，G/H间仅一斜竖；按左结合解释，也保留内右括与差线兼写候选，完整内分组属规范排印。',
    sid(5, 12): 'Remark外测度中不对，m*(A∪B)〔上下文恢复除非〕A & B可被可测集分〔右缘止〕；连接符为交叉闭环&样，及为弱备选。',
    sid(6, 1): 'Pf. (1) → (3)，原细单杆右箭；学习逻辑蕴涵⇒属于规范表达。',
    sid(6, 14): '（几乎〔择优校读任意〕）x。后两组字形不同于P5两个处，取中等置信任意；数学员另提在+纵向小字（疑处处/旁补），保留分歧和处处备选。数学义为对几乎处处x。',
}
for source in plan['sources']:
    if source['id'] in labels:
        source['label'] = labels[source['id']]

artifacts = plan['evidence_artifacts']
by_path = {x['path']: x['id'] for x in artifacts}
by_id = {x['id'] for x in artifacts}
all_crops = []

def register(path, crop=None):
    relative = str(path)
    assert (P / relative).is_file(), relative
    if relative in by_path:
        return 'artifact:' + by_path[relative]
    identifier = 'granular-' + hashlib.sha256(relative.encode()).hexdigest()[:18]
    assert identifier not in by_id
    record = {'id': identifier, 'path': relative, 'kind': 'evidence', 'format': 'image' if crop else 'text'}
    if crop:
        assert sha(P / relative) == crop['sha256']
        record['source_crop'] = {key: crop[key] for key in ['page_id', 'bbox_px', 'dpi']}
    artifacts.append(record)
    by_path[relative] = identifier
    by_id.add(identifier)
    return 'artifact:' + identifier

# Register actual historical failed reports, actual readings, and original-PDF crops.
report_evidence = []
for role, index_name in [('visual', 'targeted-crops.json'), ('math', 'crop-index.json'), ('adversarial', 'crop-index.json')]:
    folder = Path(f'proposals/ra12_{role}/final-7f2b9670fcd1')
    for path in sorted((P / folder).glob('*')):
        if path.suffix in ['.json', '.md']:
            eid = register(path.relative_to(P))
            if path.name in ['final-report.json', 'findings.md', 'full-review-notes.md', 'final-review-notes.md']:
                report_evidence.append(eid)
    index = read(P / folder / index_name)
    for crop in index if isinstance(index, list) else index['crops']:
        crop = dict(crop)
        crop['evidence_id'] = register(crop['path'], crop)
        all_crops.append(crop)

pool = Path('audit/granular-reread-7f2b9670fcd1')
register(pool / 'crop-index.json')
units = {}
for crop in read(P / pool / 'crop-index.json')['crops']:
    crop = dict(crop)
    crop['evidence_id'] = register(crop['path'], crop)
    all_crops.append(crop)
    units[crop['source_unit_id']] = crop['evidence_id']
assert len(units) == len(plan['sources']) == 111
for kind in ['transcription_blocks', 'study_blocks']:
    for b in plan[kind]:
        b['evidence_ids'] = sorted(set(b.get('evidence_ids', []) + [units[s] for s in b['source_ids']]))

# Direct comparison links are evidence, not artificial content-origin edges.
comparisons = {
    ('T', 8): ['proposals/ra12_adversarial/final-7f2b9670fcd1/p3-qie-comparison-1200.png', 'proposals/ra12_math/final-7f2b9670fcd1/crops/p3-comparison-ze-g-1200.png', 'proposals/ra12_adversarial/final-7f2b9670fcd1/p1-lemma-zhuyi-following-1200.png'],
    ('S', 11): ['proposals/ra12_adversarial/final-7f2b9670fcd1/p3-qie-comparison-1200.png', 'proposals/ra12_math/final-7f2b9670fcd1/crops/p3-comparison-ze-g-1200.png'],
    ('T', 43): ['proposals/ra12_adversarial/final-7f2b9670fcd1/p5-two-chu-1200.png', 'proposals/ra12_math/final-7f2b9670fcd1/crops/p3-comparison-zai-full-1200.png', 'proposals/ra12_math/final-7f2b9670fcd1/crops/p4-comparison-zai-correct-1200.png'],
    ('S', 49): ['proposals/ra12_adversarial/final-7f2b9670fcd1/p5-two-chu-1200.png', 'proposals/ra12_math/final-7f2b9670fcd1/crops/p3-comparison-zai-full-1200.png', 'proposals/ra12_math/final-7f2b9670fcd1/crops/p4-comparison-zai-correct-1200.png'],
}
for (kind, number), paths in comparisons.items():
    b = block(kind, number)
    b['evidence_ids'] = sorted(set(b['evidence_ids'] + ['artifact:' + by_path[path] for path in paths]))

decisions = []
def decision(number, source_ids, problem, candidates, observation, forward, backward, pages):
    decisions.append({'number': number, 'source_ids': source_ids, 'problem': problem, 'candidates': candidates, 'observation': observation, 'forward': forward, 'backward': backward, 'pages': pages})

decision(22, [sid(1, 8)], '开覆盖前独立字及X后的存在符号未在保真中记录',
 ['择优且，保留Y后句点、X后的∃及一个开覆盖；且为中至较高置信，不称唯一。', '因/即/则或普通句读；分别有字形弱点，句读不能解释完整独立字簇。', '把∃直接翻成有且不披露；语义相同，无法追溯原量词形。'],
 '三人原PDF800/1200读图，且与P3U03同手比对支持；seq256范围在U08内，X后独立反E样符号为∃，不是漏框。视觉员仅确定字簇存在，未独自确认且；Boss保留该分歧。',
 '且引入独立开覆盖条件，已给f及其连续限制的开逆像在各Xa中相对开，再由Xa开得到X中开。∃与存在覆盖语义相容。',
 '给定映射本身不能决定某个指定族是开覆盖；即/则的句法不能代替独立覆盖条件。数学同义并不能证明字形，比较图与原路径才支持选读。', ['p0001', 'p0003'])
decision(23, [sid(1, 12)], '注意右下小簇的归字有真实分歧，必须在当前正文显示其存在和两种解释',
 ['择优意的偏位心底，保留注意；明确记小簇两点卧钩及独立则备选，不声称唯一分字。', '数学员择优另一个草写则，其右U钩与别处则相似；作为独立异读保留。', '到或小；欠至/刂或中主竖布局，弱于前两种。'],
 '111单元逐张实读后，三人各自800/1200裁图。视觉及对抗倾心底，数学倾则；框[373,3171,410,3237]中的墨迹实际存在且在U12内。Boss选择保留注意并就地解释分笔边界。',
 '两种有据读法都引出同一限制连续事实；正文完整保留该事实，蓝注描述小簇而不漏字形信息。',
 '连续性证明对注意/注意则不敏感，不能由证明决定字值。若直接加到或声称无墨迹，分别超出笔形依据或违反原像。当前有限置信的选读不是声称消除了全部古字形不确定性。', ['p0001', 'p0003', 'p0006'])
decision(24, [sid(1, 18)], '邻域定义的两个有被改成有限多个，遗漏原复写并加入未见的多',
 ['原只与有有限个，保留两个有且不添多；学习稿明确作规范表达有限多个。', '原只与有限多个，首有为连写重笔；两个分离的穿横/月样组与限后直连个反对该读法。'],
 'U18直接800图及对抗1200图均见两完整有形，限后紧接个。',
 '按有限数量的相交成员定义局部有限，足够证明局部有限闭并闭和连续拼接。',
 '两种口语表达同一有限数量，数学正确不能授权隐藏复写或声称存在多字；原像独立两组是判据。', ['p0001'])
decision(25, [sid(1, 11)], '引理最后并项的整项外括被排版省去而未交代',
 [r'原并项为((f|Xa)^−1(U))，在保真和原式引述中恢复整项外括。', '外左弧属f运笔，原仅限制函数括；f自身低位左探与U后双右弧反对此读。'],
 '视觉800定向和已有逆像1200对照见并号后两左及U后两右，独立笔分开。',
 '外括包住一个逆像集合，不改变限制与并的数学对象。',
 '去掉外括仍等价，但不能称原无此括；首项−1中1另属上下文恢复，不能因末括清楚而提高其视觉置信。', ['p0001'])
decision(26, [sid(2, 2), sid(2, 5), sid(2, 12), sid(3, 2)], '可测函数后的则及三处实际s.t.未逐处保留',
 ['原句保留则，三个s.t.分别回到限制连续、紧闭损失、首几何预算前；学习稿用使/满足并披露译写。', '把则并入数的收笔、把s.t.当空白或间隔；独立字形和同手重复缩写反对。'],
 '数学员P2句尾1200与P3则g对照；视觉三处1200及全组三幅800图确认s和交叉t，点号规范排印。',
 '则连接假设与结论，s.t.各自修饰相邻的选集条件；三个预算/连续限制的定义域没有迁移。',
 '删这些词仍可成立数学命题，故不能从同义性推断纸面未写；若把s.t.错误挂到非相邻对象会破坏原选集条件的依赖关系。', ['p0002', 'p0003'])
decision(27, [sid(2, 10), sid(6, 8)], '通行姓名排印未登记原Lebegue和Borel Cantell近形',
 ['保留通行Lebesgue、Borel–Cantelli，蓝注具体说明原近形Lebegue及Borel Cantell，缺少独立s/末i的可见证据。', '原图已经清楚写全标准拼法；无法找到相应分立笔画。', '把手写近形当另一位作者或定理；内正规性与可和失配事件上下文排除。'],
 '视觉1200及Boss实际800逐源图分别见e后直接g样、Cantell末双直后冒号；按近形记录而非宣称每个连写字母唯一。',
 '内正规性和可和事件的零测limsup确定所引用定理，采用通行姓名便于学习。',
 '定理内容能识别姓名却不能补出物理上不可辨的字母；将近形误当不同定理与后续证明不合。', ['p0002', 'p0006'])
decision(28, [sid(2, 15)], '简单函数损失链原两左一右被排成两左两右',
 ['保真留两左一右，不强配唯一右弧；学习稿补完整分组并另订正两个E漏i。', '原已写两右重叠，或第二左是并号右笔；原独立笔及同页并号对照反对。'],
 '800/1200原图见m后左弧、并号自有右直、E前独立长左弧，Fiδ后只有一右随等号。',
 'm的输入为整个并；正确差项应来自各值层Ei，分组与漏下标是两种独立问题。',
 '取E为两个互不交正测度紧块且Fi=Ei，原裸E差的并为E而总损失为0；补括不足以修正原数学错，也不能证明第二右弧存在。', ['p0002'])
decision(29, [sid(3, 5)], '共同闭集的联合损失式内差项括被规范增补而未说明',
 ['保真测度层只一对括，蓝注按并(E\\Fk)理解作用域；学习稿内括标为规范分组。', '原已有独立内括，或让并只作用E再减单个Fk；前者无笔，后者留下未绑定k。'],
 '原PDF800/1200见m后及最后Fk后各一弧，并号第二笔至E间没有独立内左括。',
 'De Morgan给E\\交Fk=并(E\\Fk)，测度次可加接逐k预算；原低位2k另案保真。',
 '若将k范围移出差项，则Fk成为游离索引，不能接求和预算；数学分组可恢复，但不能声称原有两层括弧。', ['p0003'])
decision(30, [sid(3, 11)], '无穷值零测式的右括与绝对值左界规范化未披露',
 ['保留规范m(E(|f|=+∞))=0并就地明示原末仅一右弧、E后左弧/绝对值左界分笔未唯一；以a.e.有限恢复谓词。', '原清楚写全双左双右和两条绝对值界；右弧计数与左边界实际分笔不支持。', '只恢复f=+∞；会漏负无穷值，不能完整表达有限性。'],
 '三人原800/1200独立见∞后一大型右弧；m后、E后有弧样，E后短线与绝对值左界可兼写，不强给唯一笔数。',
 'a.e.有限等价于无穷模值层零测；规范式中m作用该谓词集合，后续有界变换在有限点上定义。',
 '仅f=+∞的零测不排除f=-∞正测集；m只作用E则会错误要求整个E零测。上述数学排除不证明原括和左竖已经写齐。', ['p0003'])
decision(31, [sid(4, 13)], '差集分解首项的单对括及G/H间单笔被无说明排成完整嵌套',
 ['保真(E\\Gδ\\Hδ)只有一对括，按左结合；保留中间单笔也可能兼内右括/差线的说明。', '原完整两层括，或按E\\(Gδ\\Hδ)右结合；前者无足够笔，后者数学错误。'],
 '视觉1200及全组800原图只见E前/H后外括，G到H之间一斜竖，无可分第二笔。',
 '由H⊂E\\G，先取E\\G再减H，与G\\H=G不交并，得到E\\H。',
 '右结合时G\\H=G，首项E\\G包含H，再并G变回E；当H非空与左端E\\H不同。', ['p0004'])
decision(32, [sid(5, 12), sid(6, 1)], '原A/B连接&及页首单杆箭头被无说明译写',
 ['保真及原引述用&和单杆→；学习解释明示中文连接及逻辑⇒属规范表达。', '原写中文和/及及双杆⇒；闭回环&样和只有一根细杆反对。'],
 '数学员P5连接1200、视觉P6箭头1200及Boss两幅800核见交叉闭环和单杆，原条件编号清楚。',
 'A与B同为可测分隔条件的两对象；(1)到(3)由Lusin、延拓、可和失配完成。',
 '把&当交集会改变语句类型；把单杆反作从(3)到(1)与后续选闭集及延拓步骤不符。用中文和及⇒虽语义对，也不能称原笔确如此。', ['p0005', 'p0006'])
decision(33, [sid(6, 14)], '几乎后的大小字簇被直接写成清楚的处处，未保存真实分歧',
 ['择优任意，取中等置信并保留两组墨迹；保真（几乎〔择优校读任意〕），学习规范为对几乎处处x。', '数学员大组在，右纵小组疑处处/旁补；此为真实独立异读，不抹去。', '径读处处；P5两处的同形长扫脚及右竖与目标两组不合，低于前述有分笔说明的读法。'],
 '视觉/对抗分别800/1200看斜起、人旁短竖、右折及第二字点/叠折/卧钩，较支持任意；数学实际P3/P4在对照支持在+纵字。Boss选中等置信任意并在正文与台账明确异读，不伪称三人同字一致。',
 '坏集limsup零测，E内取补得到好集liminf全测度，量词为几乎每点存在最终相等阈值。',
 'E=[0,1]、全部Dk={0}时坏limsup零测而0从不进好集，否证去掉几乎的任意x。数学只确定语义范围，无法排除字形备选或把它们变成直接观测。', ['p0005', 'p0006', 'p0003', 'p0004'])
decision(34, [sid(1, 5), sid(1, 6), sid(2, 2), sid(2, 16), sid(5, 19)] + [sid(5, u) for u in range(8, 11)], '术语表、Littlewood下一题引用与Urysohn旁注缺精确来源边',
 ['S003连Δ到P1U06、M(E)到P2U16、a.e.到P2U02及P5U19；S005连例题P1U05/U06；S042连P5U08–10。新增文字按实际来源补边和逐源图，机械同步逆向。', '源在其他目标出现已足够，或把所有源笼统连每块；前者不能追该块的明确引用，后者制造无据关系。'],
 '三人完整语义反查发现目标现有文字的直接原迹不在该块source_ids；现有互逆边通过不等于语义完整。每个新原字边都有已实际看过的800单元图。',
 '从目标中的原记号、下一题条件、上一节闭A/B连续分离回原指定源，补真实关联；新增s.t.表行连它的实际三处。',
 '由每个新增源反查目标确有该原记号/引用，不把字体比较图当内容出处；双向边与行hash由更新文本重算，正文不靠笼统同页来源替代定位。', ['p0001', 'p0002', 'p0005'])

decision_path = Path('audit/granular-followup/recovery-decisions.json')
write(P / decision_path, {'note_id': 'RA12', 'boss': BOSS, 'superseded_snapshot': SNAPSHOT, 'actual_failed_reports': reports, 'decisions': decisions, 'latest_second_pass_pending': True, 'additional_nonfindings': ['P4U16重描上限保留∞，+∞仅为兼容备选；不从数学等价伪称独立加号存在。']})
synthesis_id = register(decision_path)
register(Path('audit/granular-followup/merge_findings.py'))
for d in decisions:
    rid = f'RA12-REC-{d["number"]:02d}'
    evidence = sorted(set(report_evidence + [synthesis_id] + [c['evidence_id'] for c in all_crops if c['page_id'] in d['pages']]))
    plan['recoveries'].append({'id': rid, 'source_ids': d['source_ids'], 'problem': d['problem'],
        'candidates': [{'id': f'candidate-{i}', 'text': value, 'evidence_ids': evidence} for i, value in enumerate(d['candidates'], 1)],
        'selected_candidate_id': 'candidate-1', 'status': 'unresolved', 'evidence_ids': evidence,
        'forward_validation': {'status': 'pass', 'method': '原像及对象依赖的正向检验', 'inputs': d['observation'], 'result': d['forward'], 'evidence_ids': evidence},
        'backward_validation': {'status': 'pass', 'method': '备选、反例、类型或反向出处检验', 'inputs': d['candidates'][0], 'result': d['backward'], 'evidence_ids': evidence},
        'return_to_image': {'observation': d['observation'], 'evidence_ids': evidence}, 'reviewer_id': BOSS, 'session_id': BOSS})
    plan['issues'].append({'id': f'RA12-ISSUE-{d["number"]:02d}', 'status': 'open', 'description': d['problem'] + '；Boss合并实际失败报告后的当前提议，等待同组三人最新版本复核。', 'related_ids': d['source_ids'] + [rid], 'evidence_ids': evidence, 'resolution': ''})

for number, extras in [(1, [22,23,24,25]), (3, [27,33]), (5, [26,27,28]), (6,[26,29]), (7,[30]), (8,[31]), (11,[32]), (12,[32]), (21,[34])]:
    rec = plan['recoveries'][number - 1]
    rec['problem'] += '；逐来源终审的新细项另见' + '、'.join(f'RA12-REC-{i:02d}' for i in extras) + '。'
    issue = plan['issues'][number - 1]
    issue['related_ids'] = list(dict.fromkeys(issue['related_ids'] + [f'RA12-REC-{i:02d}' for i in extras]))
for rec in plan['recoveries']:
    rec['status'] = 'unresolved'
for issue in plan['issues']:
    issue['status'], issue['resolution'] = 'open', ''
for source in plan['sources']:
    source['status'] = 'unresolved'
for key in ['transcription_blocks', 'study_blocks']:
    for b in plan[key]:
        b['status'] = 'unresolved'

# Keep content reproducible without rerunning historical merge scripts.
override = {'source_updates': {s['id']: {'label': s['label'], 'bbox_px': s['bbox_px']} for s in plan['sources']}, 'block_updates': {}}
for kind, key in [('TRANSCRIPTION', 'transcription_blocks'), ('STUDY', 'study_blocks')]:
    for index, b in enumerate(plan[key], 1):
        override['block_updates'][f'RA12-{kind}-{index:03d}'] = {k: b[k] for k in ['text', 'source_ids', 'evidence_ids', 'explanation', 'origin'] if k in b}
override_path = Path('audit/granular-followup/body-and-source-overrides.json')
write(P / override_path, override)
register(override_path)
write(P / 'content-plan.json', plan)
authored = read(P / 'authored-content.json')
for key in ['sources', 'transcription_blocks', 'study_blocks']:
    authored[key] = copy.deepcopy(plan[key])
write(P / 'authored-content.json', authored)
(P / 'audit/final-freeze.json').unlink()
result = build(P)
after = {name: sha(P / name) for name in before}
write(P / 'audit/granular-followup/change-summary.json', {'before_document_hashes': before, 'after_document_hashes': after, 'old_snapshot': SNAPSHOT, 'recoveries_before': 21, 'recoveries_after': len(plan['recoveries']), 'issues_before': 21, 'issues_after': len(plan['issues']), 'actual_failed_reviewers': reports, 'final_chain_invalidated': True, 'new_second_pass_pending': True})
print(json.dumps({**result, 'hashes': after, 'failed_snapshot_archived': str(archive.relative_to(P))}, ensure_ascii=False))
