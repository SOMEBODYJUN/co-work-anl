"""Boss-authored RA12 content after the three independent initial records.

The literal readings, corrections and mathematical supplements below are authored
decisions. Geometry and references are compiled from actual visual records.
This file does not create pass-2 observations or final-review findings.
"""
from pathlib import Path
import json
import hashlib
import re

P = Path(__file__).resolve().parents[2]
load = lambda p: json.loads(p.read_text(encoding="utf-8"))
write = lambda p, v: p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
vunits = load(P / "proposals/ra12_visual/source-units-suggested.json")["source_units"]
ids = {}
sources = []
for u in vunits:
    if u["page_id"] == "p0007":
        continue
    pn, un = int(u["id"][3:6]), int(u["id"][-2:])
    if pn == 1:
        un = {4: 7, 7: 4}.get(un, un)
    if pn == 6:
        un = {2: 11, 11: 2}.get(un, un)
    sid = f"RA12-P{pn:03d}-U{un:02d}"
    ids[u["id"]] = sid
    sources.append({"id": sid, "page_id": u["page_id"], "bbox_px": u["bbox_px"],
                    "label": u["suggested_content"], "status": "resolved"})

def refs(p, first, last=None):
    return [ids[f"V-P{p:03d}-{n:02d}"] for n in range(first, (last or first) + 1)]

for source in sources:
    if source["id"] == "RA12-P002-U06":
        source["label"] = "并给出闭集构造 F_delta 的表达式；1200 dpi 与长框确认首语并给出。"
    if source["id"] == "RA12-P001-U19":
        source["label"] = "可测函数〔校读：近似〕，要求可数个覆盖；优势字形候选，解释另标补充。"
    if source["id"] == "RA12-P006-U10":
        source["label"] = "〔左缘边字；原矢量补证、择优校读：易〕 考察；原 PDF 页外矢量为首字提供补证。"

trans, study = [], []
def block(dest, text, source_ids=(), origin="source", label=""):
    # Keep display equations and tables valid in both Obsidian and standard
    # Markdown parsers; this does not change the mathematical text.
    lines = text.strip().splitlines()
    normalized = []
    in_math = False
    for i, line in enumerate(lines):
        if re.fullmatch(r"(?:> ?)?\$\$", line):
            blank = ">" if line.startswith(">") else ""
            if not in_math:
                if normalized and normalized[-1].lstrip("> "):
                    normalized.append(blank)
                normalized.append(line)
                in_math = True
            else:
                normalized.append(line)
                in_math = False
                if i + 1 < len(lines) and lines[i + 1].lstrip("> "):
                    normalized.append(blank)
        else:
            normalized.append(line)
    text = "\n".join(normalized)
    dest.append({"text": text.strip(), "source_ids": list(source_ids),
                 "origin": origin, "status": "resolved",
                 "explanation": label or ("原图所列内容，保持页内顺序与笔迹区别。" if origin == "source"
                                          else "Boss依据三份独立原图记录所加的明确编辑说明或数学补证。")})

def blue(dest, text, source_ids=(), title="模型补充"):
    lines = text.strip().splitlines()
    for i, line in enumerate(lines):
        if line.startswith("|"):
            lines[i] = re.sub(r"\$[^$]+\$", lambda m:m[0].replace("|",r"\vert{}"), line)
    text = "\n".join(lines)
    body = f"> [!note] <span style=\"color:blue\">{title}</span>\n>\n"
    body += "\n".join("> " + x if x else ">" for x in text.strip().splitlines())
    block(dest, body, source_ids, "supplement")

def ed(dest, text):
    block(dest, text, (), "editorial")

ed(trans, """# 实分析 12｜原稿保真转写

按原 PDF 的 7 个物理页排列。正文保留笔误、重复、旁注和三处原待填横线；蓝色说明用于识读或规范化，红色只标原稿明确留空。原有编号与本文来源编号分别保留。英文姓名按通行拼法排印；手写异体在说明中登记。数学订正及完整补证见独立的《study-notes.md》。

来源：本项目只读的 source.pdf。精确坐标、图片、裁图及双向去向见 manifest.json、source-target-map.json、ledger.json。""")
ed(trans, "## 第 1 页")
block(trans, """### Littlewood 3 定律

1. 每一个可测集几乎是有限个开区间并。
2. 每一个可测函数几乎连续。
3. 每个可测收敛的几乎一致收敛。""", refs(1,1,4))
blue(trans, "标题尾字按“律”形排印；第三句的“收敛的”保留原口语省略，数学意思是收敛的可测函数列。此处没有把原“几乎”改写为“几乎处处”。", refs(1,1,4), "识读说明")
block(trans, r"""**Ex.** 设 $E\in M$，$m(E)<+\infty$。$\forall\varepsilon>0$，$\exists I_i,\ldots,I_n$ 开区间，s.t.
$$
m\left(E\mathbin{\Delta}\left(\bigcup_{i=1}^n I_i\right)\right)<\varepsilon.
$$""", refs(1,5,6))
blue(trans, "题面第一个区间下标形近 $i$，公式的并从 $1$ 到 $n$；学习稿规范成 $I_1,\\ldots,I_n$。原运算是对称差，原区间确写“开”。", refs(1,5,6), "识读说明")
block(trans, r"""**Lemma.** 设 $f:X\to Y$。$X$ 有一个开覆盖，$X=\bigcup_{i\in A}X_i$。

若 $\forall a\in A$，$f_a:X_a\to Y$ 连续，则 $f:X\to Y$ 连续。
$$
f^{-1}(U)=\bigcup_{a\in A}\bigl(f^{-1}(U)\cap X_a\bigr)
\overset{\text{定义}}{=}\bigcup_{a\in A}(f|_{X_a})^{-1}(U).
$$""", refs(1,7,11))
blue(trans, "覆盖的索引全集写出了 $A/\\Delta/\\Lambda$ 样的不同笔形，本段统一排作 $A$，保留先 $i$ 后 $a$ 的索引变化。首项上标只见短横，减号旁没有可分辨的独立 $1$；据后两项清楚的 $-1$、限制线和等式含义恢复为逆像，不声称首项的 $1$ 已逐笔读出。$f_a=f|_{X_a}$ 是从同段定义等号与限制记号恢复的关系，不是原题另写的一行。", refs(1,7,11), "识读与上下文恢复")
block(trans, r"""注意 $f|_{X_a}$ 连续，
$$
(f|_{X_a})^{-1}(U)\in\tau_{X_a}=C\cap X_a,\qquad C\in\tau_X.
$$
由 $X_a$ 都 $\in\tau_X$，$C\cap X_a$ 是 $X$ 中开集。〔段末证毕样收笔〕""", refs(1,12,15))
block(trans, r"""但即使是闭覆盖，无限个，但改成局部有限闭覆盖。

即：给定 $x\in X$，$\exists U\in N(x)$，$U$ 只与有限多个 $X_a$ 相交。

可测函数〔校读：近似〕，要求可数个覆盖。""", refs(1,16,19))
blue(trans, "1200 dpi 与作者同页‘函’‘数’及走之笔对照后，择优校读‘近似’：前一字有独立低位底捺，后一字更像亻加以，缺少第二条走之，故优于‘逼近’；‘类似’虽符合拼接语境，却欠清楚的米、大结构。此为有依据的字形校读，置信度中等，不称逐笔唯一。‘要求可数个覆盖’可由可测拼接解释，但孤句本身没有给出一条完整的函数近似定理；学习稿中的可测拼接证明单独标为补充。", refs(1,19), "字形校读及解释范围")
ed(trans, "## 第 2 页")
block(trans, r"""### Lusin

设 $f$ 是 $E$ 上 a.e. 有限的可测函数。$\forall\delta>0$，$\exists F_\delta\overset{\text{闭}}{\subset}E$，满足
$$
m(E\setminus F_\delta)<\delta,\qquad f|_{F_\delta}\in C(F_\delta).
$$

并给出闭集构造 $F_\delta$ 的表达式。""", refs(2,1,6))
block(trans, r"""**Pf. (1)** $f\in S(E)$。$\exists E_1,\ldots,E_\ell\in M$，s.t. $E=\cup X_i$，
$$
f=\sum_{i=1}^{\ell}c_i\chi_{E_i}.
$$
$\forall\delta$，由 Lebesgue 的内正规性，
$$
\exists F_{i,\delta}\overset{\text{紧闭}}{\subset}E_i,\qquad
m(E_i\setminus F_{i,\delta})<\frac{\delta}{\ell}.
$$""", refs(2,7,12))
blue(trans, "覆盖式右端按交叉笔形记 $X_i$，上下文数学对象为 $E_i$；函数展开式的 $f$ 后原见上下两点，本文以等式规范排印，不声称原图有两横。“紧闭”两字可见。原稿暂未区分有限与无限测度，紧集逼近在学习稿中先限定有限测度，随后使用第 4 页局部化。", refs(2,8,12), "原记号说明")
block(trans, r"""令
$$
F_\delta=\bigcup_{i=1}^{\ell}F_{i,\delta}.
$$
$$
\begin{aligned}
m(E\setminus F_\delta)
&=m(E\setminus\cup F_{i,\delta})\\
&=m\left(\bigcup_{i=1}^{\ell}(E\setminus F_{i,\delta})\right)
=\sum m(E\setminus F_{i,\delta})<\delta.
\end{aligned}
$$""", refs(2,13,15))
blue(trans, "后两个 $E$ 未见下标 $i$，链中的等号保留。这是原稿集合运算错误，不在保真稿内暗改成正确式。", refs(2,14,15), "原稿错误标识")
block(trans, r"""**(2)** $f\in M(E)$，则 $\exists\{\varphi_k\}\subset S(E)$，s.t.
$$
\lim_{k\to\infty}\varphi_k(x)=f(x),\qquad\forall x\in E.
$$""", refs(2,16,18))
ed(trans, "## 第 3 页")
block(trans, r"""由 (1)，$\forall\delta$、$\forall k\in\mathbb N^*$，
$$
F_\delta\overset{\text{闭}}{\subset}E,\qquad
m(E\setminus F_k)<\frac{\delta}{2^k}.
$$
且 $\varphi_k\in C(F_k)$。令 $F_\delta=\bigcap_{k=1}^{\infty}F_k$，则
$$
m(E\setminus F_\delta)
=m\left(\bigcup_{k=1}^{\infty}(E\setminus F_k)\right)
\le\sum\frac{\delta}{2k}.
$$

$\varphi_k$ 在 $F_k$ 上连续。$\varphi_k$ 在 $\bigcap F_k$ 上连续，下证一致收敛。""", refs(3,1,8))
blue(trans, "首行左侧字面为 $F_\\delta$，同一行右侧与下一行是 $F_k$。末和的 $k$ 起笔与 $2$ 近乎等高，按 $2k$ 笔形存留；另有低写指数 $2^k$ 候选，预期几何预算由首行明确的 $2^k$ 恢复。$\\varphi_k\\in C(F_k)$ 是省写限制。", refs(3,1,8), "识读说明")
block(trans, r"""但 Egorov 要求 $m(E)<+\infty$。

因 $f$ a.e. 有限，$m(E(|f|=+\infty))=0$。

令
$$
g(x)=\frac{f(x)}{1+|f(x)|},
\qquad |f(x)|=\frac{|g(x)|}{1-|g(x)|}.
$$
则 $g$ 有界。
$$
f(x)=\frac{g(x)}{1-g(x)}.
$$
$g(x)$ 有界。""", refs(3,9,15))
blue(trans, "Egorov 手写有 Englov/Engrov 样连写，依本段指称统一姓名。带符号逆式分母原未写绝对值，保留原式；模值逆式中确有绝对值。两个“有界”提示都保留。", refs(3,9,15), "识读说明")
block(trans, r"""或用 Egorov 定理。

当 $m(E)<+\infty$，$\exists\varphi_k\to f$，
$\forall\delta>0$，$\exists F_\delta\overset{\text{闭}}{\subset}E$，s.t.
$$
m(E\setminus F_\delta)\quad\underline{\hspace{1cm}}
$$
<span style="color:red">〔原稿待填 B1：测度后的比较号及界值〕</span>""", refs(3,16,20))
ed(trans, "## 第 4 页")
block(trans, r"""用 Egorov，$\exists G_\delta\subset E$，s.t.
$$
m(E\setminus G_\delta)\quad\underline{\hspace{1cm}}
$$
<span style="color:red">〔原稿待填 B2：测度后的比较号及界值〕</span>

$\varphi_k$ 在 $E\setminus G_\delta$ 上一致 $f$。""", refs(4,1,4))
block(trans, r"""考虑 $F_\delta\cap(E\setminus G_\delta)$，由可测的内正规性，
$$
H_\delta\overset{\text{闭}}{\subset}E\setminus G_\delta,\qquad
m((E\setminus G_\delta)\setminus H_\delta)<\underline{\hspace{2cm}}.
$$
<span style="color:red">〔原稿待填 B3：不等号后的界值〕</span>""", refs(4,5,9))
block(trans, r"""$$
\widehat F_\delta=F_\delta\cap H_\delta.
$$
要估
$$
\begin{aligned}
&m\bigl((E\setminus F_\delta)\cup(E\setminus H_\delta)\bigr)\\
&\qquad <m(E\setminus F_\delta)+m(E\setminus H_\delta).
\end{aligned}
$$
$$
E\setminus H_\delta
=((E\setminus G_\delta)\setminus H_\delta)\cup(G_\delta\setminus H_\delta).
$$""", refs(4,10,13))
blue(trans, "“要估”对应原引导字的估／求候选，不影响后面的完整公式；测度次可加位置原写严格小于号，学习稿另订正。", refs(4,11,12), "识读说明")
block(trans, r"""$m(E)=+\infty$：
$$
A_k=B(0,k)\setminus B(0,k-1),\qquad
E=\bigcup_{k=1}^{\infty}(A_k\cap E).
$$
但在 $A_k\cap E$ 上的有一个闭集。

需要用局部有限性质。""", refs(4,14,18))
ed(trans, "## 第 5 页")
block(trans, "Lusin 逆定理也成立。", refs(5,1))
block(trans, r"""**Th.** 设 $(X,\tau)$，则下述等价：

1. $X$ 正规。
2. $\forall E\overset{\text{闭}}{\subset}X$，若 $f\in C(F)$，则 $\exists F\in C(X)$，s.t. $F|_E=f$。（Tietze）
3. $\forall A,B\overset{\text{闭}}{\subset}X$，$A\cap B=\varnothing$，则存在连续函数 $f:X\to[0,1)$，s.t. $f|_A=0$ 且 $f|_B=1$。（Urysohn）""", refs(5,2,11))
blue(trans, "第 (2) 条括号内的原字为两横的 $F$，第 (3) 条区间右端形如圆括号。两处数学订正分别为 $C(E)$ 和 $[0,1]$，在学习稿标明。两个限制等式之间原有形近 $B$ 的独写连接记号，本文依语法校读为‘且’；该字形与同页字母 $B$、第 3 页‘且’分别比较后仍不称逐笔唯一，不把它当作额外集合运算。", refs(5,4,11), "原稿记号及校读说明")
block(trans, r"""**Remark.** 外测度中不对，$m^*(A\cup B)$〔上下文恢复：除非〕$A$ 和 $B$ 可被可测集分〔本行止于右缘〕。
$$
C=A\cup B.
$$""", refs(5,12,13))
blue(trans, "起句校读为‘外测度中不对’。连接词取优势候选‘除非’：首形的阝与余形连笔、次形双竖及后接条件的语法共同支持，‘所谓’欠斤、讠和胃结构，‘可加性’的字数及笔形不合。其置信度中等，恢复性质已就地标明。右缘只写到‘分’，原 PDF 右页外没有后续绘画路径，故不把‘分开／分隔’补成已写原文。$C=A\\cup B$ 原为下一独立行。学习稿仅给出可测分离推出加性的充分条件，不从残句反推无条件的必要性。", refs(5,12,13), "上下文恢复及残句范围")
block(trans, r"""**Th.** 设 $f$ 是 $E$ 上几乎处处有限函数，$E\in M$：

1. $f$ 可测。
2. $\exists\{\varphi_k\}\subset S(E)$，s.t. $\varphi_k\to f$ 逐点。
3. $\exists\{\varphi_k\}\subset C(\mathbb R^n)$，s.t. $\varphi_k\xrightarrow{\mathrm{a.e.}}f$。""", refs(5,14,19))
ed(trans, "## 第 6 页")
block(trans, r"""**Pf. (1) $\Rightarrow$ (3).**
$$
\exists g\in C(\mathbb R^n),\qquad g|_{F_\delta}=f.
$$
$\forall k\in\mathbb N^+$，$\exists F_k\overset{\text{闭}}{\subset}E$，
$$
g_k\in C(\mathbb R^n),\qquad g|_{F_k}=f,\qquad
m(E\setminus F_k)<\frac1{2^k}.
$$""", refs(6,1,7))
blue(trans, "量词中的自然数上标按正整数语境恢复为 $+$。存在式写 $g_k$，右侧限制式只见 $g$，保留原漏下标。右端 $f$ 原省写限制。", refs(6,4,7), "识读说明")
block(trans, r"""由 Borel–Cantelli：
$$
m\left(\limsup_{n\to\infty}E_n\right)=0.
$$
〔左缘边字；原矢量补证、择优校读：易〕 考察
$$
E\{g_k\ne f\}\subset E\setminus F_k.
$$
仍有
$$
m\left(\limsup_{k\to\infty}E(g_k\ne f)\right)=0.
$$""", refs(6,8,12))
block(trans, r"""$$
m\left(\bigcap_{N=1}^{\infty}\bigcup_{k=N}E(g_k\ne f)\right)=0.
$$
（几乎处处）
$$
x\in\bigcup_{N=1}^{\infty}\bigcap_{k=N}^{\infty}E(f=g_k).
$$
$$
\exists N(x)\ \text{s.t.}\ k\ge N,\qquad f=g_k\ \text{恒等}.
$$""", refs(6,13,17))
blue(trans, "首式的 $E_n$ 没有在这一行定义；后文以失配事件明确其用途。花括／圆括均作原谓词集合写法保存；包含式的右端 $F_k$ 后原另有孤立闭圆括样笔，左端没有成对开括，排式未把它当作运算。上式内并原只有下标 $k=N$，未另写上标无穷；下式两个无穷上标均可见。左缘首字受页面及 Form 裁框截切，在内存放宽裁框后补见原有矢量笔画，未改绘画路径；下部围笔内两处墨迹支持‘易’优于‘另’，上部仍潦草，故取低至中等置信的字形择优校读；左缘边字可能独立于‘考察’，不强行连成一句。‘考察’与第 4 页‘考虑’中的‘考’的对照及宀、示笔形相符。末行阈值择优排作 $k\\ge N$，另有 $k>N$ 候选，只差起点平移，均是逐点最终恒等。", refs(6,8,17), "识读与省记说明")
ed(trans, "## 第 7 页\n\n本物理页为空白页。整页与六个重叠区均无正文、页码、旁注、图形或原待填标记。")

ed(study, """# 实分析 12｜从“几乎连续”到连续函数逼近

## 目录

1. 术语、记号与 Littlewood 三原则
2. 有限测度集合的开区间近似
3. 开覆盖、局部有限闭覆盖及可数可测覆盖的拼接
4. Egorov 定理：有限测度下的工具
5. Lusin 定理：简单函数、有界化、Egorov 与无限测度四段
6. Lusin 的逆命题
7. 正规性、Urysohn 与 Tietze
8. 外测度旁注
9. 可测性与两种函数逼近的等价
10. 原稿订正与物理页对照

原稿内容以通常文字保留；蓝色 note 块标明解释、补证或订正。原稿明确留空处保留红色 B1–B3 标记，其完整补答紧随其后。来源编号与精确映射独立保存在 source-target-map.json，本文不能替代原序保真稿。""")
ed(study, "## 1. 术语、记号与 Littlewood 三原则")
blue(study, r"""| 原记号／术语 | 本文含义及适用范围 |
| --- | --- |
| $M$、$M(E)$ | Lebesgue 可测集合族、$E$ 上可测函数族；原记号按上下文区分 |
| $S(E)$ | $E$ 上有限值简单函数 |
| $C(F)$ | 拓扑子空间 $F$ 上的实值连续函数 |
| $\chi_A$ | 集合 $A$ 的示性函数 |
| $A\Delta B$ | $(A\setminus B)\cup(B\setminus A)$，对称差 |
| $E(P)$、$E\{P\}$ | $\{x\in E:P(x)\}$，原作者的谓词集合省写 |
| a.e. | 关于 Lebesgue 测度，除一个零测集外成立 |
| 几乎一致收敛 | 对任意正误差可删去测度小于该误差的集合，余集上一致收敛 |
| 局部有限族 | 每一点有邻域只交有限多个成员 |
| 正规性 | 本文指不交闭集可由不交开集分离；若课程定义还包含 $T_1$，则下文同时以 $T_1$ 为前提 |
| $\limsup D_k$ | $\bigcap_N\bigcup_{k\ge N}D_k$，无穷多次属于 $D_k$ 的点 |
| $\liminf A_k$ | $\bigcup_N\bigcap_{k\ge N}A_k$，最终总属于 $A_k$ 的点 |""",
     refs(1,2,4)+refs(1,17,19)+refs(2,7,9)+refs(5,2,11)+refs(6,11,17), "记号说明")
block(study, """原题为 **Littlewood 3 定律**，依原序：

1. 每一个可测集几乎是有限个开区间并。
2. 每一个可测函数几乎连续。
3. 每个可测收敛的几乎一致收敛。""", refs(1,1,4))
blue(study, "这三句是原则式概括。第一句在下一题的有限测度条件下以对称差度量；第二句由 Lusin 精确化；第三句的收敛可测函数列在有限测度条件下由 Egorov 精确化。“几乎连续”不等于“函数在几乎处处的点上按整个定义域连续”，而是删去任意小测度部分后，限制在余下闭集上连续。", refs(1,1,4), "解释")
ed(study, "## 2. 有限测度集合的开区间近似")
block(study, r"""**原题。** $E\in M$、$m(E)<\infty$，给定 $\varepsilon>0$，求有限个开区间 $I_1,\ldots,I_n$，使
$$
m\left(E\Delta\bigcup_{i=1}^nI_i\right)<\varepsilon.
$$""", refs(1,5,6))
blue(study, r"""这里的区间版本在 $\mathbb R$ 上表述。由外正规性取开集 $G\supset E$，满足 $m(G\setminus E)<\varepsilon/2$，因而 $m(G)<\infty$。将 $G$ 写成至多可数个两两不交开区间的并 $G=\bigcup_{j\ge1}I_j$；有限个分支时直接取尽。无限个分支时由测度可加性选 $n$ 使 $m(G\setminus\bigcup_{j=1}^nI_j)<\varepsilon/2$。记该有限并为 $U$，则
$$
E\Delta U\subset(G\setminus E)\cup(G\setminus U),
\qquad m(E\Delta U)<\varepsilon.
$$
只控制 $E\setminus U$ 不足以排除 $U$ 伸到 $E$ 外的大块，故原三角符号不可改作单侧集合差。""", refs(1,5,6), "题目完整解答")
ed(study, "## 3. 三种分片拼接")
block(study, r"""### 3.1 原稿的开覆盖引理

设 $f:X\to Y$，$X=\bigcup_{a\in A}X_a$ 为开覆盖。若每个 $f_a:X_a\to Y$ 连续，则 $f$ 连续。原稿用
$$
f^{-1}(U)=\bigcup_a(f^{-1}(U)\cap X_a)
=\bigcup_a(f|_{X_a})^{-1}(U)
$$
说明，并在等号上注“定义”。""", refs(1,7,11))
blue(study, r"""必须明确 $f_a=f|_{X_a}$。任取 $U\in\tau_Y$，每个限制逆像在 $X_a$ 的子空间拓扑中开，故存在 $C_a\in\tau_X$ 使它等于 $C_a\cap X_a$。由于 $X_a$ 本身在 $X$ 中开，该交集在 $X$ 中开；任意并仍开，得到 $f$ 连续。

原稿写 $(f|_{X_a})^{-1}(U)\in\tau_{X_a}=C\cap X_a$，是把“拓扑族”与“族中一个成员”的等式并写。严格式为
$$
\tau_{X_a}=\{C\cap X_a:C\in\tau_X\}.
$$
原“注意限制连续”“由两者都开”“$X$ 中开集”和证毕收笔对应上述三步。若各 $f_a$ 是另行给出的映射，则还须在相交处一致，才能先拼成 $f$；原题已先给定了 $f$。""", refs(1,12,15)+refs(1,7,11), "补全条件与证明")
block(study, r"""### 3.2 局部有限闭覆盖

原稿补充：无限个闭覆盖时改用“局部有限闭覆盖”。局部有限的定义是：给定 $x\in X$，存在 $U\in N(x)$，只与有限多个 $X_a$ 相交。""", refs(1,16,18))
blue(study, r"""若 $X_a$ 在 $X$ 中闭、构成局部有限覆盖，且每个限制连续，则对 $Y$ 中任意闭集 $D$，$(f|_{X_a})^{-1}(D)$ 在 $X_a$ 中闭，也在 $X$ 中闭。这些闭集仍局部有限，它们的并为 $f^{-1}(D)$。

局部有限闭集的并为何闭？若 $x$ 不在并中，先取只交有限多个成员的邻域，再逐一避开这有限多个闭集，就得到不交整个并的开邻域。因此逆像闭，$f$ 连续。

不能删去局部有限条件：在 $X=\{0\}\cup\{1/n:n\ge1\}$ 的单点闭覆盖上，每个限制都连续；但令 $f(0)=0$、$f(1/n)=1$，$f$ 在 $0$ 不连续。第 4 页的环带论证正需要这一工具。""", refs(1,16,18), "补证与条件检验")
block(study, "### 3.3 原页末的可测覆盖旁注\n\n“可测函数〔校读：近似〕，要求可数个覆盖。”", refs(1,19))
blue(study, r"""两疑字采用 1200 dpi 笔形对照后的优势读法，备选“类似／逼近”及理由见保真稿与恢复台账。下面解释可数覆盖在可测拼接中的作用，不把孤句改写成已经陈述的近似定理。

设可测空间 $X$ 被可数个可测子集 $X_j$ 覆盖，$f|_{X_j}$ 对迹 $\sigma$-代数可测。对靶空间任意可测集 $B$，
$$
f^{-1}(B)=\bigcup_{j\ge1}(f|_{X_j})^{-1}(B).
$$
各项都是 $X$ 中可测集，可数并可测，故 $f$ 可测。这里用的是可数并封闭；无需把旁注改写为有界测度控制或任意不可数可测拼接。""", refs(1,19), "旁注补证")
ed(study, "## 4. Egorov 定理：有限测度下的工具")
block(study, r"""原稿在一般可测函数的 Lusin 证明中提醒：“但 Egorov 要求 $m(E)<+\infty$”，随后又开列“或用 Egorov 定理”的路线。""", refs(3,9)+refs(3,16,18))
blue(study, r"""**工具定理。** $m(E)<\infty$，可测函数 $f_k\to f$ 几乎处处，$f$ 几乎处处有限。给定 $\eta>0$，存在可测例外集 $G\subset E$，$m(G)<\eta$，使 $f_k\to f$ 在 $E\setminus G$ 上一致收敛。

先将收敛或有限性失败的零测集 $Z$ 放入 $G$。对 $r,N\ge1$ 定义
$$
A_{r,N}=\bigcup_{k\ge N}\{x\in E\setminus Z:|f_k(x)-f(x)|\ge1/r\}.
$$
固定 $r$，这些集合随 $N$ 递减且交为空；因为第一项测度有限，由测度从上连续性得 $m(A_{r,N})\to0$。选 $N_r$ 使 $m(A_{r,N_r})<\eta/2^{r+1}$，令 $G=Z\cup\bigcup_rA_{r,N_r}$，则 $m(G)<\eta$。给定 $\varepsilon>0$，选 $1/r<\varepsilon$；对所有 $k\ge N_r$ 与 $x\notin G$，误差小于 $1/r$，即一致收敛。

有限测度条件不能删除：$[0,\infty)$ 上的 $\chi_{[k,\infty)}$ 逐点趋于 $0$，但删任一有限测度集后仍有尾部点令误差为 $1$。这里补的是 Egorov 的证明，不把它冒充原稿已完整写出的证明。""", refs(3,9)+refs(4,1,4), "前置工具及完整补证")
ed(study, "## 5. Lusin 定理")
block(study, r"""### 5.1 原定理与构造任务

设 $E\in M$，$f$ 在 $E$ 上可测且 a.e. 有限。对每个 $\delta>0$，存在闭集 $F_\delta\subset E$，使
$$
m(E\setminus F_\delta)<\delta,\qquad f|_{F_\delta}\in C(F_\delta).
$$
原稿紧接要求：“并给出闭集构造 $F_\delta$ 的表达式。”""", refs(2,1,6))
blue(study, r"""以下先在 $m(E)<\infty$ 时使用紧集内近似，最后按原第 4 页的环带处理 $m(E)=\infty$。若 $f$ 允许扩展实值，先令 $Z=\{x\in E:|f(x)|=\infty\}$，$m(Z)=0$，在 $E\setminus Z$ 上作构造；最终闭集取在该集内，测度损失仍按原 $E$ 计算。""", refs(2,1,6)+refs(3,10,11), "适用条件")
block(study, r"""### 5.2 简单函数情形

原稿设 $f\in S(E)$，取 $E_1,\ldots,E_\ell\in M$，写 $E=\cup X_i$，并写
$$
f=\sum_{i=1}^{\ell}c_i\chi_{E_i}.
$$
由 Lebesgue 内正规性取 $F_{i,\delta}\overset{\text{紧闭}}{\subset}E_i$，满足
$$
m(E_i\setminus F_{i,\delta})<\delta/\ell,\qquad
F_\delta=\bigcup_{i=1}^{\ell}F_{i,\delta}.
$$""", refs(2,7,13))
blue(study, r"""将 $E_i$ 取为 $f$ 的互不相交值层，则 $E=\bigsqcup_iE_i$；原覆盖式的 $X_i$ 订正为 $E_i$。在有限测度条件下，内正规性给出所需紧集 $F_{i,\delta}$。有限并 $F_\delta$ 紧且闭，$f$ 在每个 $F_{i,\delta}$ 为常数，有限闭覆盖拼接给出 $f|_{F_\delta}$ 连续。

原稿测度链写了 $\bigcup_i(E\setminus F_{i,\delta})$ 和 $\sum_i m(E\setminus F_{i,\delta})$。正确计算为
$$
E\setminus F_\delta=\bigsqcup_{i=1}^{\ell}(E_i\setminus F_{i,\delta}),
\qquad
m(E\setminus F_\delta)=\sum_i m(E_i\setminus F_{i,\delta})<\delta.
$$
原式不能按字面成立：取 $E=[0,1]\cup[2,3]$、$F_{1,\delta}=[0,1]$、$F_{2,\delta}=[2,3]$，左边的损失为 $0$，而 $\bigcup_i(E\setminus F_{i,\delta})=E$。不相交值层同时解释了正确链中的等号。""", refs(2,8,15), "构造解答与原式订正")
block(study, r"""### 5.3 一般函数的共同闭集

原稿从 $\{\varphi_k\}\subset S(E)$、$\varphi_k(x)\to f(x)$（$\forall x\in E$）出发。由简单函数情形，逐 $k$ 选闭集，原首行写 $F_\delta\subset E$、右端写 $m(E\setminus F_k)<\delta/2^k$，并写 $\varphi_k\in C(F_k)$。再令 $F_\delta=\bigcap_kF_k$，重复说明 $\varphi_k$ 在各 $F_k$ 及共同交集上连续，接“下证一致收敛”。""", refs(2,16,18)+refs(3,1,8))
blue(study, r"""固定总误差 $\eta>0$，为每个 $k$ 分别选 $F_{k,\eta}$，以下简记 $F_k$。原 $\varphi_k\in C(F_k)$ 精写为 $\varphi_k|_{F_k}\in C(F_k)$；函数原先定义在整个 $E$，不是只定义在 $F_k$。令 $F_\eta=\bigcap_kF_k$，则闭性、限制连续性和测度估计分别为
$$
F_\eta\ \text{闭},\qquad
\varphi_k|_{F_\eta}\in C(F_\eta),\qquad
m(E\setminus F_\eta)\le\sum_km(E\setminus F_k)<\sum_k\eta2^{-k}=\eta.
$$
最后严格号可由第一项严格余量与其余项的弱上界得到。原第三行的低位 $2k$ 必须按前一行几何预算订正为 $2^k$；$\sum_k1/(2k)$ 发散，不能提供所需总损失界。

逐点收敛与每项连续仍不足以推出极限连续，例如 $x^k$ 在 $[0,1]$ 上逐点收敛到在 $1$ 不连续的函数。因此必须保留原稿之后的两条路线，不能在此处直接宣布连续。""", refs(3,1,8), "下标、限制与估计订正")
block(study, r"""### 5.4 路线 A：有界化再作一致简单逼近

原稿用 a.e. 有限性写 $m(E(|f|=+\infty))=0$，令
$$
g=\frac{f}{1+|f|},\qquad |f|=\frac{|g|}{1-|g|},
$$
说明 $g$ 有界；另写 $f=g/(1-g)$，并再次提示 $g$ 有界。""", refs(3,10,15))
blue(study, r"""在已去掉 $Z$ 的有限值点上，$|g|<1$，准确的带符号逆变换为
$$
f=\frac{g}{1-|g|}.
$$
这是因为 $1-|g|=1/(1+|f|)$。原 $g/(1-g)$ 对负值错误：$f=-2$ 时 $g=-2/3$，该原式给 $-2/5$，正确逆式才给 $-2$。

取有界 $g$ 的简单量化 $\psi_k=2^{-k}\lfloor2^kg\rfloor$。每个 $\psi_k$ 有有限多个值，且 $0\le g-\psi_k<2^{-k}$，所以在整个定义域上一致逼近。按上一小节为每个 $\psi_k$ 取闭集并总交，得到损失小于 $\delta$ 的闭 $F_\delta$，每个 $\psi_k$ 在其上连续，且 $\psi_k\to g$ 一致。因此 $g|_{F_\delta}$ 连续；函数 $t\mapsto t/(1-|t|)$ 在 $(-1,1)$ 连续，复合即得 $f|_{F_\delta}$ 连续。

这条路线补全了原稿有界化后省略的“一致”环节。它不声称任意逐点简单逼近都会自动一致，也不把无穷值直接代入分式。""", refs(3,1,15), "路线 A 完整补证")
block(study, r"""### 5.5 路线 B：Egorov、内正规性和三项误差

原稿另起“或用 Egorov 定理”，设 $m(E)<\infty$，并在闭集 $F_\delta$ 后留下：

<span style="color:red">B1：$m(E\setminus F_\delta)$ 后的比较号及界值留空。</span>

下一页以 $G_\delta\subset E$ 配合 $\varphi_k$ 在 $E\setminus G_\delta$ 上一致趋于 $f$，并留下：

<span style="color:red">B2：$m(E\setminus G_\delta)$ 后的比较号及界值留空。</span>

再考虑 $F_\delta\cap(E\setminus G_\delta)$，由内正规性取闭 $H_\delta\subset E\setminus G_\delta$，留下：

<span style="color:red">B3：$m((E\setminus G_\delta)\setminus H_\delta)<$ 后的界值留空。</span>

原稿定义 $\widehat F_\delta=F_\delta\cap H_\delta$，用两个补集之并估计损失，并写
$$
E\setminus H_\delta=((E\setminus G_\delta)\setminus H_\delta)
\cup(G_\delta\setminus H_\delta).
$$""", refs(3,16,20)+refs(4,1,13))
blue(study, r"""三处可按相同总预算 $\delta$ 补成：

| 原待填 | 一组相容的完整补答 |
| --- | --- |
| B1 | $m(E\setminus F_\delta)<\delta/3$，用共同闭集步骤时将误差参数取为 $\delta/3$ |
| B2 | $m(E\setminus G_\delta)>m(E)-\delta/3$，等价于 $m(G_\delta)<\delta/3$ |
| B3 | $m((E\setminus G_\delta)\setminus H_\delta)<\delta/3$ |

$G_\delta$ 在原后续式中是要删掉的坏集；故不能把 B2 填成 $m(E\setminus G_\delta)<\delta/3$。因为此处 $m(E)<\infty$，表内 B2 在保留原左端的同时正确表述 Egorov 的小坏集条件。

按 §5.3 的共同闭集构造，同时满足 B1 的测度预算和所有 $\varphi_k|_{F_\delta}$ 的连续性；连续性并非由 B1 单独的不等式推出。由 Egorov，它们在 $E\setminus G_\delta$ 上一致趋于 $f$。内正规性给出 B3 中的闭 $H_\delta$（此处可取紧集），故 $\widehat F_\delta=F_\delta\cap H_\delta$ 闭，$\varphi_k|_{\widehat F_\delta}$ 连续并一致趋于 $f|_{\widehat F_\delta}$，于是该限制连续。

原稿联合估计处的严格号应先写成次可加性的弱号：
$$
\begin{aligned}
m(E\setminus\widehat F_\delta)
&\le m(E\setminus F_\delta)+m(E\setminus H_\delta)\\
&=m(E\setminus F_\delta)
 +m((E\setminus G_\delta)\setminus H_\delta)+m(G_\delta)\\
&<\delta.
\end{aligned}
$$
第二行用 $H_\delta\subset E\setminus G_\delta$，所以分解中的 $G_\delta\setminus H_\delta=G_\delta$，且两块不交。三项各自的严格预算才产生末行严格号。""", refs(3,19,20)+refs(4,1,13), "三处待填完整解答与订正")
block(study, r"""### 5.6 无限测度：原稿的环带与局部有限

当 $m(E)=+\infty$，原稿写
$$
A_k=B(0,k)\setminus B(0,k-1),\qquad
E=\bigcup_{k=1}^{\infty}(A_k\cap E),
$$
并提示每个 $A_k\cap E$ 上有闭集，“需要用局部有限性质”。""", refs(4,14,18))
blue(study, r"""约定 $B(0,0)=\varnothing$，$k\ge1$。每个 $E_k=E\cap A_k$ 有限测度。将有限测度 Lusin 用于 $E_k$，取在 $\mathbb R^n$ 中闭的 $K_k\subset E_k$，使
$$
m(E_k\setminus K_k)<\delta2^{-k},\qquad f|_{K_k}\in C(K_k).
$$
环带族局部有限：任一点的一个有界小邻域只会遇到半径有限范围内的环带。因此子族 $\{K_k\}$ 局部有限，$K=\bigcup_kK_k$ 闭。$f|_K$ 在各 $K_k$ 上连续，由第 3 节的局部有限闭覆盖拼接连续；此外
$$
m(E\setminus K)\le\sum_km(E_k\setminus K_k)<\delta.
$$
这就完成原定理在无限测度上的部分。这里拼接的是限制函数的连续性；没有把 Egorov 错扩张为无限测度上的全局几乎一致收敛。""", refs(4,14,18)+refs(1,16,18), "无限测度情形补证")
ed(study, "## 6. Lusin 的逆命题")
block(study, "原稿第 5 页首句：“Lusin 逆定理也成立。”", refs(5,1))
blue(study, r"""设 $E$ Lebesgue 可测，$f$ a.e. 有限，且对每个 $\eta>0$ 有闭 $F_\eta\subset E$，$m(E\setminus F_\eta)<\eta$、$f|_{F_\eta}$ 连续。取 $\eta=1/n$，记 $F_n=F_{1/n}$，则
$$
Z=E\setminus\bigcup_{n\ge1}F_n
\quad\text{满足}\quad m(Z)\le m(E\setminus F_n)<1/n,
$$
所以 $m(Z)=0$。对任意实直线开集 $O$，集合 $\{x\in F_n:f(x)\in O\}$ 在闭子空间 $F_n$ 中开，故是 Borel 集。$f^{-1}(O)$ 等于这些集合的可数并再加上 $Z$ 的一个子集，后者由 Lebesgue 测度完备性可测。无穷值层也至多落在已剔除零测异常集。故 $f$ 可测。

这给出逆命题的完整理由；原纸上只有提示，补证属于模型新增。""", refs(5,1), "逆命题补证")
ed(study, "## 7. 正规性、Urysohn 与 Tietze")
block(study, r"""### 7.1 原稿三个等价条件

原稿对 $(X,\tau)$ 列出：(1) $X$ 正规；(2) 闭 $E\subset X$ 上的连续实值函数可延拓到 $X$（Tietze）；(3) 不交闭集 $A,B$ 可由连续函数分离，$f|_A=0$、$f|_B=1$（Urysohn）。

原第 (2) 条字面写 $f\in C(F)$、所求 $F\in C(X)$、$F|_E=f$；原第 (3) 条的值域右端笔形为 $[0,1)$。""", refs(5,2,11))
blue(study, r"""第 (2) 条的输入域应为 $C(E)$；令延拓名为 $\widetilde f$ 可避开原字母 $F$ 的双重用途。第 (3) 条必须用 $[0,1]$：若 $B\ne\varnothing$，$f|_B=1$ 与 $f:X\to[0,1)$ 不相容。

**Urysohn $\Rightarrow$ 正规。** 对不交闭集 $A,B$，取分离函数 $u:X\to[0,1]$；开集 $u^{-1}([0,1/3))$、$u^{-1}((2/3,1])$ 不交，分别含 $A,B$。区间在值域子空间中开，故原像在 $X$ 开。""", refs(5,2,11), "订正与第一方向")
blue(study, r"""**正规 $\Rightarrow$ Urysohn。** 先用正规性得到收缩性质：若闭 $K\subset O$ 且 $O$ 开，分离 $K$ 与 $X\setminus O$，可取开 $V$ 使 $K\subset V\subset\overline V\subset O$。对不交闭 $A,B$，取 $U_1=X\setminus B$，再取 $A\subset U_0\subset\overline{U_0}\subset U_1$。按二进有理数逐层插入开集，利用收缩性质使
$$
\overline{U_r}\subset U_s\qquad(0\le r<s\le1,\ r,s\text{ 为二进有理数}).
$$
令 $u(x)=\inf\{r:x\in U_r\}$，空集的下确界在此约定为 $1$。于是 $u|_A=0$、$u|_B=1$。对 $0<t\le1$，$\{u<t\}=\bigcup_{r<t}U_r$ 为开集。对 $0\le t<1$，$\{u>t\}=\bigcup_{r>t}(X\setminus\overline{U_r})$ 也是开集：若 $u(x)>t$，可取 $t<r<s<u(x)$，若 $x\in\overline{U_r}$ 则 $x\in U_s$ 矛盾；反向利用嵌套关系得到 $u(x)\ge r>t$。端点以外原像为空或全空间，故 $u$ 连续。""", refs(5,2,11), "Urysohn 完整补证")
blue(study, r"""**Urysohn $\Rightarrow$ Tietze（有界情形）。** 设闭 $E\subset X$，$h:E\to[-a,a]$ 连续，$a>0$。$A=\{h\le-a/3\}$、$B=\{h\ge a/3\}$ 是 $X$ 中不交闭集。由 Urysohn 取连续 $v:X\to[-a/3,a/3]$，在 $A$、$B$ 分别取端点 $-a/3$、$a/3$。在 $E$ 上分三段检验得到 $|h-v|\le2a/3$。

对余差重复此步骤，得到连续 $v_j$，满足
$$
\|v_j\|_\infty\le\frac a3(2/3)^j,\qquad
\left|h-\sum_{j=0}^{N}v_j\right|_E\le a(2/3)^{N+1}.
$$
几何上界保证 $\sum_jv_j$ 在 $X$ 一致收敛，和函数连续；在 $E$ 上余差趋零，故它延拓 $h$。零函数情形直接处理。

**无界实值情形。** 给定 $f\in C(E)$，先令 $h=f/(1+|f|)\in(-1,1)$，由有界情形延拓为 $H:X\to[-1,1]$。闭集 $D=\{x:|H(x)|=1\}$ 与 $E$ 不交。再用 Urysohn 取 $v:X\to[0,1]$，$v|_E=1$、$v|_D=0$。于是 $K=vH$ 在所有点都满足 $|K|<1$，且 $K|_E=h$，故
$$
\widetilde f=\frac{K}{1-|K|}
$$
为 $X$ 上连续实值延拓。

**Tietze $\Rightarrow$ Urysohn。** 在闭集 $C=A\cup B$ 上分别定义 $h|_A=0$、$h|_B=1$，有限闭覆盖拼接表明 $h$ 连续。延拓后再复合截断函数 $t\mapsto\max(0,\min(1,t))$，即得到所需 $[0,1]$ 值分离函数。至此三条件等价。""", refs(5,2,11)+refs(5,13), "Tietze 完整补证")
ed(study, "## 8. 外测度旁注")
block(study, r"""原稿在拓扑等价条件下另写 Remark，含“外测度”“$m^*(A\cup B)$”“$A$ 和 $B$ 可被可测集分〔止于右缘〕”，下一独立行是 $C=A\cup B$。连接词的原字形与保真排印见原序稿及对应恢复记录。""", refs(5,12,13))
blue(study, r"""由可见关键词可解释为可测分离给出外测度加性。以下是对残句的数学解释，未声称原作者写出了完整命题。若存在 Lebesgue 可测集 $M$，使 $A\subset M$、$B\subset M^c$，取 $C=A\cup B$，由可测性的 Carathéodory 分割性质，
$$
m^*(C)=m^*(C\cap M)+m^*(C\setminus M)
=m^*(A)+m^*(B).
$$
这是充分条件，不能把旁注擅自加强为无条件的外测度可加性或必要充分条件。仅有 $A\cap B=\varnothing$，可数次可加性只给“$\le$”。

对于上一节 Urysohn 分离的闭 $A,B\subset\mathbb R^n$，连续 $u$ 给出可测分隔集 $u^{-1}([0,1/2))$。这说明旁注与相邻拓扑工具的联系；原稿没有把这段推导写完整。右缘“分”后的“开／隔”属于语义补足，不算看见原字。""", refs(5,12,13), "旁注的数学解释")
ed(study, "## 9. 可测性与函数逼近")
block(study, r"""### 9.1 原稿的等价命题

设 $E\in M$，$f$ 是 $E$ 上几乎处处有限的函数。下列条件等价：

1. $f$ 可测。
2. 存在 $\{\varphi_k\}\subset S(E)$，使 $\varphi_k\to f$ 逐点。
3. 存在 $\{\varphi_k\}\subset C(\mathbb R^n)$，使 $\varphi_k\to f$ 几乎处处。

原第 (2) 条为逐点，第 (3) 条为 a.e.，定义域确为 $\mathbb R^n$，不是紧方块。""", refs(5,14,19))
blue(study, r"""**(1) $\Rightarrow$ (2)。** 对实值点令
$$
\varphi_k=2^{-k}\left\lfloor2^k\max(-k,\min(f,k))\right\rfloor.
$$
它取有限多个值，值层可测，故为简单函数。对任意有限 $f(x)$，最终截断失效且量化误差小于 $2^{-k}$，所以趋于 $f(x)$。若保留扩展值点，令截断在 $+\infty$、$-\infty$ 分别为 $k$、$-k$，同样按扩展实值意义逐点收敛。

**(2) $\Rightarrow$ (1)。** 可测函数列的逐点极限可测；具体可写为 $\limsup_k\varphi_k=\inf_N\sup_{k\ge N}\varphi_k$，可数上确界、下确界保持可测。这补足原稿未展开的两个方向。""", refs(5,14,19), "简单逼近两方向")
block(study, r"""### 9.2 原稿的 (1) $\Rightarrow$ (3)

原证明先用延拓得到 $g\in C(\mathbb R^n)$、$g|_{F_\delta}=f$。再逐 $k$ 选闭 $F_k\subset E$ 与 $g_k\in C(\mathbb R^n)$，满足
$$
m(E\setminus F_k)<2^{-k}.
$$
原限制行仍写 $g|_{F_k}=f$。""", refs(6,1,7))
blue(study, r"""对每个 $k\ge1$，由 Lusin 取闭 $F_k\subset E$，使 $m(E\setminus F_k)<2^{-k}$ 且 $f|_{F_k}$ 连续；$\mathbb R^n$ 是正规空间，由 Tietze 将其延拓为 $g_k\in C(\mathbb R^n)$。因此原漏标精写为
$$
g_k|_{F_k}=f|_{F_k}.
$$
这里的预算是新选的 $2^{-k}$，不需要沿用第 3 页某个固定的 $\delta$。如果 $f$ 有无穷值零测集，Lusin 的闭集已选在有限值部分中，所以延拓输入为实值连续函数。""", refs(6,1,7), "延拓步骤与下标订正")
block(study, r"""原稿接 Borel–Cantelli：先写 $m(\limsup_n E_n)=0$，再考察
$$
E\{g_k\ne f\}\subset E\setminus F_k,
$$
仍有
$$
m(\limsup_k E(g_k\ne f))
=m\left(\bigcap_{N\ge1}\bigcup_{k\ge N}E(g_k\ne f)\right)=0.
$$
随后取好集，写几乎处处
$$
x\in\bigcup_{N\ge1}\bigcap_{k\ge N}E(f=g_k),
$$
即存在 $N(x)$，当 $k\ge N(x)$ 时 $f(x)=g_k(x)$ 恒等。""", refs(6,8,17))
blue(study, r"""明确原未定义的泛称：令 $E_k=E\setminus F_k$，$D_k=\{x\in E:g_k(x)\ne f(x)\}$。由延拓相等关系，$D_k\subset E_k$。对每个 $N$，
$$
m(\limsup_kD_k)\le m\left(\bigcup_{k\ge N}D_k\right)
\le\sum_{k\ge N}m(E_k)
\le\sum_{k\ge N}2^{-k}=2^{1-N}.
$$
令 $N\to\infty$ 得零测，这就是此处所用的 Borel–Cantelli 第一部分，不需要事件独立。

相对于 $E$ 取补集，De Morgan 律给
$$
E\setminus\bigcap_N\bigcup_{k\ge N}D_k
=\bigcup_N\bigcap_{k\ge N}(E\setminus D_k)
=\bigcup_N\bigcap_{k\ge N}\{x\in E:f(x)=g_k(x)\}.
$$
逐点量词由“$\forall N\,\exists k\ge N$ 失配”取否定变成“$\exists N\,\forall k\ge N$ 相等”。故结论是几乎处处最终逐点恒等，强于单纯 a.e. 收敛，却不能推出一个与 $x$ 无关的共同阈值，更不能据此宣称一致收敛。

反查并交次序：若某点只在偶数项失配，它在坏集的 $\limsup$ 中而不在 $\liminf$ 中；把零测式写成外并内交会漏掉此类无限次失配。左缘裁切的边字不影响完整事件公式。原展开式内并省写上限，本文用 $k\ge N$ 明确无限尾部。""", refs(6,8,17), "Borel–Cantelli 与量词补证")
blue(study, r"""**(3) $\Rightarrow$ (1)。** 连续 $g_k$ 的限制到可测 $E$ 都可测，$h=\limsup_k g_k|_E$ 作为扩展实值函数可测。在给定的全测度收敛集上 $h=f$；两者仅在一个 Lebesgue 零测集上可能不同，完备性保证其任意子集可测，所以 $f$ 仍可测。结合前述各方向即得等价。

上述最终逐点恒等不蕴含一致收敛的直观例子是 $g_k(x)=\max(0,1-|2kx-1|)$（$x\in[0,1]$）。每个固定点最终取 $0$，但每项在 $1/(2k)$ 的值为 $1$，故 $\sup|g_k|=1$。此例是新增的量词检验，不属于原稿。""", refs(5,14,19)+refs(6,13,17), "剩余方向与结论边界")
ed(study, "## 10. 原稿订正与物理页对照")
blue(study, r"""| 原位置 | 保留的原写法／现象 | 学习时的处理 |
| --- | --- | --- |
| 第 1 页 | $f_a$ 与限制关系省写；索引全集笔形不一；$\tau_{X_a}=C\cap X_a$ 并写 | 明示限制关系，区分拓扑族与其中成员，保留开／局部有限闭／可数可测三类拼接 |
| 第 2 页 | $E=\cup X_i$；测度链中两个 $E$ 漏 $i$；“紧闭” | 取不交值层 $E_i$，修正为值层差集，在有限测度部分先取紧集 |
| 第 3 页 | 首 $F_\delta$ 与后 $F_k$；$\varphi_k\in C(F_k)$；低位 $2k$ | 逐 $k$ 选 $F_{k,\delta}$，明示限制，使用可求和几何预算 |
| 第 3 页 | $f=g/(1-g)$；有界提示重复；B1 横线 | 原错误与重复均保留，带符号逆式补 $|g|$；B1 在路线 B 就地补答 |
| 第 4 页 | $m(E\setminus G_\delta)$ 后 B2；内近似后 B3；并集估计写 $<$ | 以小坏集解释并补等价下界，三项预算，次可加性用 $\le$ |
| 第 5 页 | $C(F)$；区间右端如圆括；外测度旁注到“分”止 | 输入域改 $C(E)$，值域改 $[0,1]$；旁注保留可见残句，语义解释独立标注 |
| 第 6 页 | 延拓限制式 $g$ 漏 $k$；未定义泛称 $E_n$；内并上限省写 | 明确 $g_k$、$E_k$ 与失配集 $D_k$；取补集的并交与最终恒等完整保留 |
| 第 7 页 | 普通空白物理页 | 记录来源，不制造红色待填题 |""", refs(1,7,19)+refs(2,8,15)+refs(3,1,20)+refs(4,1,13)+refs(5,4,13)+refs(6,4,17), "对照索引")

plan = {
    "note_id": "RA12",
    "authors": ["BossNotes-2ff3215d6446", "/root/ra12_visual", "/root/ra12_math"],
    "review_policy": {"mode": "user_requested_fixed_trio", "note_id": "RA12",
                      "boss_id": "BossNotes-2ff3215d6446",
                      "authorization_artifact_id": "campaign-participants",
                      "reviewer_ids": ["/root/ra12_visual", "/root/ra12_math", "/root/ra12_adversarial"]},
    "sources": sources, "transcription_blocks": trans, "study_blocks": study,
    "evidence_artifacts": [], "observations": [], "recoveries": [], "issues": []
}
write(P / "authored-content.json", plan)
write(P / "audit/campaign/source-id-migration.json", ids)
print(json.dumps({"source_units": len(sources), "transcription_blocks": len(trans), "study_blocks": len(study)}))
