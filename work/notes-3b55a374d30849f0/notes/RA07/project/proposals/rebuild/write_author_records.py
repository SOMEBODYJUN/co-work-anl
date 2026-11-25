from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).parent;J=P.parents[1]
def write(name,text):
 p=P/name;q=p.with_suffix(p.suffix+'.tmp');q.write_text(text.rstrip()+'\n',encoding='utf-8');q.replace(p)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
write('sources.md',r'''# RA07 来源与作者说明

## 原件

- 原文件：`input/pdf/实分析7.pdf`，13 个物理页，无旧稿。
- 原文件 SHA256：`c053b24757b997ab489d1c18371df9ba44137919d53596b7158856ac1e8746c8`。
- 认领工作区：`work/notes-fc2ba28a26cd495f/notes/RA07/project/`。
- 作者、实际会话：`/root/ra07_rebuild`。协调编辑 `/root` 对第 1 页全页及问题裁图作过局部复读，并提供无限维命题补证；这不计第二遍或最终复核。
- 只使用该 PDF 作字迹来源。下面的数学材料只能支持补充命题，不能支持“原稿写了这些字”的断言。

## 图像与逐区观察

`prepare_pdf.py` 以 300 dpi、重叠 0.12 渲染。13 张整页均为 2480×3509 像素；每页依次实际查看整页，再查看六个高清重叠区。原件末页与空白分区均实际打开，没有用自动空白检测代替视觉阅读。第 7 页有一批工具输出超长被截断，随后将六区分成两批重新查看，记录依据为重看的结果。

真实工具路径为 `functions.exec -> tools.view_image({path: ...}) -> image(image_url)`。各页、各区完整文件路径及 SHA256 见 `project/manifest.json`；逐页布局与逐区首末内容、符号、留白、接续见 `observations-first.json`。11 张补充裁图坐标见 `crops.json`，均已实际打开查看，不只是生成。

## 外部数学核验

1. `/root` 提供并在作者回图后采用的无限维命题材料：`project/evidence/ra07-q001-root.md`。协调编辑实际打开核验了 [USC 大学讲义 Wiener Measure](https://dornsife.usc.edu/sergey-lototsky/wp-content/uploads/sites/211/2023/06/Week8-ByDiogo.pdf) 的相关页。作者复核 Riesz 引理、R/2 中心与 R/8 小球的分离、包含及可分覆盖推导。正文把它写为适用范围明确的蓝色补证，没有把局部有限性、可分性等补充条件改成黑色原文。
2. Solovay 原论文：Robert M. Solovay, *A Model of Set-Theory in Which Every Set of Reals is Lebesgue Measurable*, Annals of Mathematics 92 (1970), 1–56，DOI 10.2307/1970696。[期刊原始页面](https://annals.math.princeton.edu/1970/92-1/p01) 与[原论文 PDF 镜像](https://www.liutianren.com/discrete/ref/Logic%20and%20Set%20Theory/Solovay-ModelSetTheoryEvery-1970.pdf)。本作者实际检索到原论文 Theorem 1 的文字并打开期刊原始书目页面，核对“ZFC 加不可达基数的传递模型”假设以及“ZF+DC、所有实数集 Lebesgue 可测”的结论。没有把 forcing 构造补称为原稿已有证明，也不声称自己逐页视觉读过该 57 页扫描论文。

其余蓝色证明为作者依源内容写出的数学补充；依赖顺序记录于 `study-order.json`。无旧稿，故没有迁移旧稿独有内容。

## 原色与新增内容

转写中的公式错误、重复、残缺、提纲词和原稿用语保留。学习稿用 Obsidian `> [!info]` 标出补充、补证、纠错；原明确提问或 Proof 待填处用红色文字说明。普通物理空白页、边缘留白不标红。两幅原集合图均保留原裁图，使用仓库分支的稳定 raw URL，便于正文原字节复制到 output 后继续显示。
''')
write('terminology.md',r'''# RA07 术语与记号表

| 原稿用语或记号 | 本稿处理 | 约定与限制 |
| --- | --- | --- |
| $\Sigma\subset\mathcal P(X)$、$\sigma$ 代数 | 保留并蓝补封闭条件 | 含全集、对补与可数并封闭 |
| $\mathbb R^+$ | 黑色照录 | 蓝补测度/外测度完整论证使用 $[0,\infty]$，不默认为严格正有限值 |
| $2^X$ | 幂集 $\mathcal P(X)$ | 指集合；$2^{|X|}$ 是其基数 |
| $\overline{\overline A}$ | 集合的势 $|A|$ | 双横线不是闭包 |
| $c,\mathfrak c$ | 连续统基数 | 在集合补上标 $c$ 的位置，仍表示补集，须看上下文 |
| $|E|$ | 计数例中为元素数 | 无限集合的计数测度取 $\infty$，不取某个无限基数 |
| $|I|$ | 长方体体积 | $I=\prod(a_j,b_j)$ 时为 $\prod(b_j-a_j)$ |
| “正规性” | 保留课堂原词 | 原稿未定义，未擅自决定是归一化还是内外正则性；两类性质蓝色分说 |
| “开区间”“矩形” | 在 $\mathbb R^n$ 中为开长方体 | 蓝色精确版本取有界、与坐标轴平行的开长方体 |
| $LC(E),LC_E$ | $E$ 的可列开长方体覆盖之族 | 一个元素是一列 $(I_k)$，不是单个 $I_k$ |
| $m^*$ | Lebesgue 外测度 | 定义于全幂集，通常只有次可加性 |
| $m,m_L$ | 外测度在可测族上的限制 | 第 6 页下标按 Lebesgue 语境整理为 $L$；原局部图保留 |
| $m_*$ | 有界集合的内测度 | 先取闭有界框 $I\supset E$；已蓝证与紧集内逼近上确界相等，故与框无关 |
| 零测集 | 外测度为零的集合 | 原定义未预设可测；随后证明可测及完备性 |
| Jordan 测度/内容 | 有限覆盖与 Darboux 和 | 判据明确补有界性；与 Lebesgue 可数覆盖区分 |
| $T$ 或定义中的 $I$ | 任意测试子集 | 仅矩形判据专门把测试族缩小为矩形 |
| Vatelli | 转写保留可见拼写 | 学习解释使用标准名称 Vitali；该行 Q003 汉字未决 |
| AC、ZF、ZFC、DC | 原逻辑旁注的缩写 | AC 选择公理；ZFC=ZF+AC；DC 依赖选择；模型假设另写清 |
''')
write('author-recovery-notes.md',r'''# RA07 作者候选与数学检验记录

本文件身份为 `/root/ra07_rebuild`，只记录作者识读、回图和数学恢复。它不冒充非作者的正式 `recoveries` 审核记录；ledger 中正式 recoveries 目前为空，由后续独立复核者建立。

## 四项未决

| 编号、源单元 | 候选及回图 | 数学检验与边界 | 当前处理 |
| --- | --- | --- | --- |
| Q001，P001-U013 | 句首曾误推为全幂集问题；实际回看 `p0001-question.png` 并参考 `/root` 的独立局部复读，改为更符合笔画的“无穷维”。中间仍近似量词样符号或“∧m” | 无限维可分赋范空间不存在非零局部有限平移不变 Borel 测度，Riesz 球列给出完整证明；有限维全幂集归一化测度不存在则是另一 Vitali 命题。两者前提不同，不能相互替代来证明原字 | 撤销全幂集黑色原题；保留中性量词疑字。两个补证分别蓝列 |
| Q002，P003-U009 | 覆盖对象候选“闭矩形”；“半开矩形”等对象在数学上也可能。实际查看 `p0003-rectangle.png`，字形尚不足以唯一确定 | 闭矩形、半开矩形都可通过逐项 ε/2^k 放大与收缩得到同一外测度，数学可行不能唯一排除读法 | 片段与裁图保留，闭矩形版本只作为候选补证，不断言原题已读清 |
| Q003，P010-U008 | `p0010-vitali.png` 中首动词与名字后的汉字，候选“将/取”“集于/在于”；Vatelli、[2,3]^c、可测集与2^c可读 | 邻行明确 Φ:2^[2,3]→2^R、A↦A∪V。取V⊂[0,1]可验证构造；不同汉字候选都与之相容，逆向不能选定原字 | 中性汉字片段保留，完整数学论证另蓝列 |
| Q004，P011-U008 | `p0011-bridge.png` 下部公式前三字，候选“待后有/随后有/结合有”等；两项相加公式本体清晰 | 不论衔接词是哪种，A可测均直接给 m*(T∩A)+m*(T∩A^c)=m*(T)。公式正确性不能反证某个衔接字 | 原公式保留，衔接字中性编号；四块补证完整 |

## 已用上下文恢复或原错核验

### 第 6 页定义行扫描右缘截断

候选末项为 $m^*(I\cap E)$ 或 $m^*(I\cap E^c)$。本页中部完整复写明确是后者。正向代入 $E=\mathbb R^n$、$I$ 为体积正的有限矩形：前者会要求 $m^*(I)=2m^*(I)$，不能作通用定义；后者给正确的 $m^*(I)=m^*(I)+0$。逆向回到同页完整式可见 $E^c$，所以采用补集版本，但正文仍注明是同页恢复，没有伪称扫描缺边可见。

### 第 9 页零测集证明末项

实际回图 `p0009-nullproof.png`，第二行末项是 $T\cap E$，未见补集 $c$。数学上它只是单调性真式，不能独自完成分割等式。转写保留 $E$；蓝色收尾改用 $T\cap E^c$，结合第一行已经证明 $m^*(T\cap E)=0$。这是补证与纠错，不能反过来说原字实际写了 $E^c$。

### 第 10 页两处差集方向

两处都能从原高清区域读出 $A\setminus V$。有限反例 $A=\varnothing,V=\{0\}$ 使原恒等式左右不等；正确式 $A\cup V=A\cup(V\setminus A)$ 在三点全集的 64 对子集穷举中全部成立。可测性正确等价式再用并、差封闭完整证明。原错误未删除。

### 第 11 页目标式补集括号

原末项缺少 $A\cup B$ 的成对括号，按字面读为 $(T\cap A)\cup B^c$ 与目标不符。由随后三块集合等式及三圆图，可恢复意图为 $T\cap(A\cup B)^c$。转写仍保留原写，学习稿以蓝色纠错后给四块等式证明。图中数字 1、2、3、4 真实可见，具体 $D_i$ 名称为编者新增。

### 第 2 页 Darboux 判据

原式是 $\sup U=\inf L\Rightarrow$ 可积。它作为充分条件过强，但箭头本身并非反例意义下的假命题；标准充要判据应为 $\inf U=\sup L$。在 $f(x)=x,[0,1]$ 上计算出单格 U=1、L=0，均匀 N 格之差为 1/N，说明标准可积函数未必满足原强条件。正文已作此区分。

## 有限检验与一般证明

实际执行脚本 `finite_checks.py`，输入输出存于 `finite-check-input-output.json`，6 组检验全部通过：Darboux 和、Cantor 有限阶段、差集式 64 对穷举、三圆分块 512 组三集合穷举、几何误差和、Riesz 球常数。

有限检验不能证明无限基数结论、一般测度定理或视觉识读。一般命题的完整蓝色证明都在学习稿，并按以下依赖编排：

```mermaid
flowchart TD
  A[外测度定义与矩形体积] --> B[Carathéodory 与矩形判据]
  B --> C[可测族封闭与可列可加]
  C --> D[零测集与完备性]
  C --> E[有限可加与差集]
  D --> F[内外逼近与不可测构造]
  E --> F
```
''')
ledger=json.loads((J/'ledger.json').read_text());issues=ledger['issues']
write('unresolved.md','# RA07 未决字迹\n\n实际为 4 个语义位置；审计器会分别计入源单元、两稿目标单元、相关补充及问题表，机器的未决记录数不能当作不同问题数。\n\n'+ '\n\n'.join('## '+i['id']+'\n\n'+i['description']+'\n\n处理：'+i['resolution']+'\n\n关联：'+', '.join(i['related_ids']) for i in issues))
counts={f'p{n:04d}':sum(s['page_id']==f'p{n:04d}' for s in ledger['source_units']) for n in range(1,14)}
lines=['# RA07 REBUILD 作者首遍交接','',f'记录时间（运行环境 UTC）：{datetime.datetime.now(datetime.timezone.utc).isoformat()}','',
'状态：13 页首遍视觉和全部可读原内容已完成；第 13 页整页空白。已写两稿、148 个手工来源单元、422 个目标单元、13 个首遍整页观察和 78 个首遍逐区观察，另实际查看 11 张有坐标裁图。没有填写第二遍或最终复核占位。','',
'正文：`source-transcript.md` 按物理页序；`study-notes.md` 按 17 节复习依赖顺序。完整目录、原题及相邻蓝色解答、重复路线、两幅原图、原错误和未完证明均保留。内测度部分另补完整内外逼近与等价判据。','',
'| 物理页 | 来源单元数 | 首遍范围 |','| --- | ---: | --- |']
for pid,c in counts.items():lines.append(f'| {pid} | {c} | 整页及六区；'+('全页空白，不造来源单元' if c==0 else '逐区观察见 observations-first.json')+' |')
lines+=['','## 当前正文哈希','',f'- source-transcript.md：`{sha(P/"source-transcript.md")}`',f'- study-notes.md：`{sha(P/"study-notes.md")}`','',
'## 审计边界','',
'ledger 的 JSON Schema 已实跑，0 错误。首次 check 的 5 个 RESOLUTION_CONFLICT 已修正为保守继承未决来源状态。最终作者阶段 check 另存 `audit-first-pass-final.json`；缺少第二遍整页/区域及连续三轮终审应继续显式报错，不能称最终通过。正文与目标哈希、双向映射、来源边框及图像记录将由该结构检查核验。','',
'正式 recoveries 留空；作者候选、前向/逆向数学检验和真实回图记录在 `author-recovery-notes.md`，供非作者独立检查后另建正式记录。四处未决见 `unresolved.md`。','',
'## 生成与维护','',
'可编辑 `pages/p001.json` 至 `p013.json` 后运行 `build.py`，它会原子更新两正文并刷新 ledger、mapping、source-units 与 observations-first。`study-order.json` 决定学习顺序，并断言所有主体只出现一次；补充单元紧跟其来源主体。旧的 write_pXXX.py、repair_q001.py、refine_first_pass.py 是历史起草工具，含一次性补充，勿重新执行以免重复插入或回退后来订正。','',
'图像路径与 SHA256 在 manifest；两正文图像使用 work/notes 分支的 raw URL。作者未执行 Git 写入；所有本次文件位于获配 RA07/project/。参与身份见 participants.json，/root 的局部复读不计 VISUAL_SECOND。']
write('first-pass-handoff.md','\n'.join(lines))
# Add evidence records, but do not include an audit report whose snapshot refers to this artifact set.
f=P/'extra-evidence.json';extra=json.loads(f.read_text()) if f.exists() else []
for aid,name in [('author-sources','sources.md'),('author-terms','terminology.md'),('author-recovery-notes','author-recovery-notes.md'),('author-finite-checks','finite-check-input-output.json'),('author-unresolved','unresolved.md'),('author-handoff','first-pass-handoff.md')]:
 extra=[x for x in extra if x['id']!=aid]
 extra.append({'id':aid,'path':str((P/name).relative_to(J)),'kind':'evidence','format':'text'})
f.write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Saved six author records and evidence bindings.')
