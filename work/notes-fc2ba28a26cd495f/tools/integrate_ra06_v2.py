"""One-time authored integration of actual VISUAL_SECOND findings.

Keeps the compared rebuild drafts unchanged. This script writes prose and
mapping proposals; it does not create independent observations or approvals.
"""
from pathlib import Path
import json
import re
import shutil

RUN = Path(__file__).resolve().parent.parent
P = RUN / "notes/RA06/project"
OLD = P / "proposals/rebuild"
NEW = P / "proposals/integration-v2"
NEW.mkdir()
for f in OLD.iterdir():
    if f.is_file():
        shutil.copy2(f, NEW / f.name)
shutil.copy2(P / "ledger.json", P / "ledger-first-pass.json")

def parse(path):
    parts = re.split(r"(?m)^<!-- unit: ([^\s]+) -->\n", path.read_text())
    assert not parts[0].strip()
    return [(parts[i], parts[i + 1].strip()) for i in range(1, len(parts), 2)]

docs = {k: parse(OLD / n) for k, n in
        [("T", "source-transcript.md"), ("N", "study-notes.md")]}
mapping = json.loads((NEW / "mapping.json").read_text())
byid = {t["id"]: t for t in mapping["targets"]}
changes = []

def get(uid):
    return next(text for ident, text in docs[uid[0]] if ident == uid)

def setblock(uid, text):
    items = docs[uid[0]]
    at = next(i for i, item in enumerate(items) if item[0] == uid)
    items[at] = (uid, text.strip())
    changes.append(uid)

def replace(uid, old, new):
    value = get(uid)
    assert old in value, (uid, old)
    setblock(uid, value.replace(old, new))

def add(uid, text, after, sources=(), origin="supplement", evidence=(),
        explanation="新增蓝色完整补证；不冒充原稿字迹。", status="resolved"):
    assert uid not in byid
    items = docs[uid[0]]
    at = next(i for i, item in enumerate(items) if item[0] == after)
    items.insert(at + 1, (uid, text.strip()))
    target = dict(id=uid, artifact_id="study" if uid[0] == "N" else "transcription",
                  source_ids=list(sources), status=status, origin=origin,
                  old_ids=[], evidence_ids=list(evidence),
                  explanation=explanation)
    mapping["targets"].append(target)
    byid[uid] = target
    changes.append(uid)

def red(text):
    return '\n\n<span style="color:red">' + text + '</span>'

# p1: exact original wording, two distinct separation labels, annotation,
# missing subscript, and original/new-content boundaries.
for uid in ["T-p1-03", "N-p1-03"]:
    replace(uid, "逆不一定", "逆不真")
replace("T-p1-08", r"由 $T_2$，$\forall y", r"由 $T_1$，$\forall y")
setblock("N-p1-08", r"""原稿写：“由 $T_1$，$\forall y\in M$，由 $T_2$，$\exists\delta_y>0$”，使
$$
B(x,\delta_y)\cap B(y,\delta_y)=\varnothing.\tag{2.1}
$$""")
replace("N-p1-radius",
        "此处“$T_2$”表示 Hausdorff 分离性；",
        "原稿的两处记号分别为 $T_1$、$T_2$。$T_1$ 表示单点闭，单凭这一条件不能推出两个点有不交开邻域；$T_2$ 表示 Hausdorff 分离性。上面的度量估计直接给出了所需的两个球；")
replace("T-p1-09", "（有限）", "（有界）")
replace("N-p1-09", r"M\subset\bigcup_{i=1}^{m}B(y_i,\delta_{y_i}).",
        r"M\subset\bigcup_{i=1}^{m}B(y_i,\delta_{y_i})\qquad\text{（有界）}.")
add("N-p1-cover-bounded-note", r"""> [!info] 补证：有限覆盖后的“有界”括注
> 这一括注也给出一条有界性证明。若覆盖有 $m\ge1$ 个球，以 $y_1$ 为基点，令
> $$R=1+\max_{1\le i\le m}\bigl(d(y_1,y_i)+\delta_{y_i}\bigr).$$
> 对任意 $z\in M$，选一个含它的覆盖球，三角不等式给出 $d(z,y_1)<\delta_{y_i}+d(y_i,y_1)<R$。故 $M\subset B(y_1,R)$，所以有界。若有限子覆盖为空族，则 $M=\varnothing$，也有界。§2.3 另保留固定中心、递增整数半径的证明路线。""",
    "N-p1-09", sources=["RA06-P001-U09"],
    evidence=["image:p0001"],
    explanation="原稿“有界”括注的就地完整补证；与固定中心开球覆盖路线分别保留。")
replace("T-p1-10", r"\bigcup_{i=1}^{m}B(y_i,\delta_{y_i})",
        r"\bigcup_{i=1}^{m}B(y,\delta_{y_i})")
setblock("N-p1-10", r"""令 $\delta=\min\{\delta_{y_1},\ldots,\delta_{y_m}\}$。原稿由前面的不交式写
$$
B(x,\delta)\cap\left(\bigcup_{i=1}^{m}B(y,\delta_{y_i})\right)=\varnothing
\qquad\text{（闭集）}.
$$""")
add("N-p1-index-and-conclusion", r"""> [!info] 记号订正与补证：补齐球心下标及闭性收尾
> 原稿这一行的球心 $y$ 未见下标 $i$；与上一行有限覆盖相接，应写为 $B(y_i,\delta_{y_i})$。当 $M\ne\varnothing$ 时，所取有限覆盖非空，各半径均正，故其最小值 $\delta>0$。
> 因为 $\delta\le\delta_{y_i}$，有 $B(x,\delta)\subset B(x,\delta_{y_i})$；后者与 $B(y_i,\delta_{y_i})$ 不交。因此 $B(x,\delta)$ 与覆盖 $M$ 的有限并不交，得到 $B(x,\delta)\subset M^c$。任取 $x\in M^c$ 都有这样的开球，故 $M^c$ 开、$M$ 闭。""",
    "N-p1-10", sources=["RA06-P001-U10"], evidence=["image:p0001"],
    explanation="把原稿漏下标与省略的闭性推理明确移入蓝色，黑色只保留原式和原括注。")

# p2: record actual ambiguity, preserve a recoverable local term, and distinguish
# source glyphs from the mathematical cube and finite-dimensional candidates.
setblock("T-p2-01", r"""有限[Q006]：iff 列紧 $\Longleftrightarrow$ 闭集有界。

可以定义有限[Q006]（某些教材）。""")
setblock("N-p2-01", r"""<a id="s3-2"></a>
### 3.2 原稿的等价关系提要

原稿写：“有限[Q006]：iff 列紧 $\Longleftrightarrow$ 闭集有界。可以定义有限[Q006]（某些教材）。”""")
setblock("N-p2-scope", r"""> [!info] 补充：提要的两种相关数学问题
> 两处“有限”后的字仍待唯一辨定，故不把这一行强行定为紧性的定义。下面先证明一般度量空间中紧与列紧等价；在 $\mathbb R^n$ 中，再结合 Heine–Borel 定理，便得到紧、列紧、有界闭三者等价。
> 一般度量空间中的“有界闭”不能单独推出紧：无限集合配离散度量 $d(x,y)=1$（$x\ne y$）时，整个空间有界且闭，但单点开集组成的覆盖没有有限子覆盖。若原词意为“有限维”，则还需讨论整个赋范空间的每个闭有界子集；该候选题意的准确量词和完整证明放在 §3.5。""")
replace("T-p2-02", "（闭[Q001]性）", "（闭传递性）〔按局部笔画恢复；恢复依据另存 Q001。〕")
replace("N-p2-02", "原稿括注：“闭[Q001]性”。", "原稿括注：“闭传递性”〔局部笔画恢复，见 Q001 记录〕。")
replace("N-p2-closed-proof",
        "原稿括注中间的两个字尚在独立识读记录 Q001 中保留候选，不影响引理正文和证明。",
        "原稿的“闭传递性”按本次局部笔画恢复保留；通常名称“闭遗传性”放在蓝色说明中，不替换课堂原词。")
setblock("T-p2-04", r"""**pf.** $M$ 有界，$\exists a>0$，s.t.
$$
M\subset[-a,\text{[Q002a]}]^{\text{[Q002b]}}.
$$
〔Q002a、Q002b 分别定位原式的右端点与指数；左端点 $-a$ 可读。〕""")
setblock("N-p2-04", r"""原稿从有界性开始：$\exists a>0$，使
$$M\subset[-a,\text{[Q002a]}]^{\text{[Q002b]}}.$$
右端点与指数分别保留中性定位；下一行明确出现指数 $n$。""")
setblock("N-p2-cube-exponent", r"""> [!info] 数学恢复：初始方块的端点与维数
> 由 $M\subset\mathbb R^n$ 且有界，可以选足够大的 $a>0$，使 $M\subset[-a,a]^n$。后续的 $2^n$ 等分和直径公式也使用这个 $n$ 维闭方块。这里同时恢复右端点为 $a$、指数为 $n$，是明确的数学补充；Q002a、Q002b 的原笔候选仍保留，不能仅凭证明成立判定字形。""")
replace("T-p2-07", "存在一个小集", "存在一个闭集")
setblock("N-p2-07", r"""将 $Q_0$ 等分，得到 $2^n$ 个；原稿写“存在一个闭集，无有限子覆盖”，记为 $Q_m$。""")
replace("N-p2-first-index", "为使递归编号连贯，", "此处选出的闭集是细分所得的闭小方块。为使递归编号连贯，")

# p3: keep the complete faint equality chain and avoid claiming that a dot-union
# or an uncertain superscript was directly present in the manuscript.
for uid in ["T-p3-06", "N-p3-06"]:
    setblock(uid, r"""$$
\exists B(x_0,\delta)\subset G_{\lambda_0}.
$$
〔Q007：$\delta$ 右下有点状附笔，是否为下标尚未唯一辨定；此处保留可辨主符号。〕""")
add("N-p3-radius-convention", r"""> [!info] 补充：统一后续半径记号
> 由 $G_{\lambda_0}$ 开且含 $x_0$，可取一个正半径，使相应开球包含于 $G_{\lambda_0}$。在蓝色完整证明中统一把这个正半径记为 $\delta$，后续采用 $\delta/2$。这只统一补证的记号，不决定 Q007 的附笔究竟为何。""",
    "N-p3-06", sources=["RA06-P003-U06"], status="unresolved",
    evidence=["image:p0003"], explanation="对未决半径附笔给出中性说明，并明确补证的统一记号。")
for uid in ["T-p3-13", "N-p3-13"]:
    setblock(uid, r"""原稿右下浅色旁注，$\Rightarrow$ 方向：
$$
\overline E=E'=E'\cup\operatorname{Iso},
\qquad\operatorname{Iso}\notin E'.
$$""")
replace("N-derived-basic-proof", "这一公式即原稿浅色旁注所用的分解。",
        "这是对原稿普通并号分解的准确补充；点并符号由编者加入，原笔没有该点。")
setblock("N-p3-forward-repair", r"""> [!info] 说明与补证：原等号链及孤立点集
> 原记号 $\operatorname{Iso}\notin E'$ 把集合与元素的“不属于”混用；准确关系是 $\operatorname{Iso}(E)\cap E'=\varnothing$。若 $E$ 自密，先由 $E\subset E'$ 与 $\overline E=E\cup E'$ 得 $\overline E=E'$，所以原等号链的中间一步有明确前提。
> 再由 $\overline E=E'\cup\operatorname{Iso}(E)$，可得 $\operatorname{Iso}(E)\subset E'$；结合不交关系，得到 $\operatorname{Iso}(E)=\varnothing$。原稿的两个 $E'$ 以及普通并号均在黑色原式中保留。""")
setblock("T-p3-15", r"""浅色补记：〔Q008：起首连接语〕（$E'$ 是闭），（闭）$'\subset$（闭）。""")
setblock("N-p3-15", r"""原稿浅色补记：〔Q008：起首连接语〕（$E'$ 是闭），（闭）$'\subset$（闭）。""")
for uid in ["T-p3-16", "N-p3-16"]:
    setblock(uid, r"""闭，
$$
\overline E=E=E^{\text{[Q009]}}\cup\partial E,
\qquad E'\subset E.
$$
〔Q009 定位并号前 $E$ 的小上标；起首“闭”按原笔保留。〕""")
setblock("N-p3-closure-scope", r"""> [!info] 候选辨析与完整说明：闭集分解
> 原稿起首已经写“闭”。若小上标表示内部，则准确结论是：对闭集 $E$，有 $\overline E=E=E^\circ\cup\partial E$，且 $E'\subset E$。因为 $\partial E=\overline E\setminus E^\circ$，前一个分解直接成立；后一个包含关系由闭集的导集判别得到。
> 若小上标是导号，则不能在任意度量空间中无条件将 $E'$ 代替 $E^\circ$。反例：在非空离散度量空间中取单点集 $E=\{x\}$，有 $E$ 闭、$E'= \varnothing$、$\partial E=\varnothing$，而 $E\ne\varnothing$，所以 $E'\cup\partial E\ne E$。
> 若另限定在通常实轴，则对闭集确有 $E'\cup\partial E=E$：每个内点都是聚点，所以 $E^\circ\subset E'$；再结合 $E=E^\circ\cup\partial E$ 与 $E',\partial E\subset E$ 即得。两种范围的区别不能用来消除 Q009 的字形歧义。""")
for uid in ["T-p3-11", "N-p3-11"]:
    setblock(uid, get(uid) + red("原稿待证：此处写出 proof 与下降关系，未给出推导。"))

# p4: retain the source's empty-set equality and abbreviated inf/sup; keep all
# actual unfinished proof starts, and make the supplemental endpoint argument
# valid even when the maximal interval is unbounded.
replace("T-p4-03", r"\varnothing\ne U", r"\varnothing=U")
setblock("N-p4-03", r"""<a id="s5-2"></a>
### 5.2 点的邻域：原稿两问及解答

原稿写 $\forall\varnothing=U\subset(\mathbb R,|\cdot|)$，包含号下标“开”。""")
add("N-p4-nonempty-correction", r"""> [!info] 纠错：后续选点需要非空开集
> 原笔在 $\varnothing$ 与 $U$ 之间可见的是等号；若取 $U=\varnothing$，后面的 $x\in U$ 无法选取。以下问题按“$U$ 为非空开集”给出解答，即采用 $\varnothing\ne U$，并把这个订正与黑色原式分开。""",
    "N-p4-03", sources=["RA06-P004-U03"], evidence=["image:p0004"],
    explanation="保留原等号，蓝色单独订正后续选点所需的非空条件。")
setblock("N-p4-11", r"""原稿简记
$$\alpha=\inf a,\qquad\beta=\sup b.$$""")
add("N-p4-extrema-explanation", r"""> [!info] 补全记号：确界对哪些端点取
> 以上简记可明确写成
> $$\alpha=\inf\{a:(a,b)\in G_x\},\qquad\beta=\sup\{b:(a,b)\in G_x\}.$$
> 这里遍历原稿已经定义的所有含 $x$、且包含于 $U$ 的有限端点开区间；若左端点集无下界或右端点集无上界，分别允许 $\alpha=-\infty$、$\beta=+\infty$。这是编者补全的指标集合，原稿只写了简式。""",
    "N-p4-11", sources=["RA06-P004-U11"], evidence=["image:p0004"],
    explanation="将新增的确界指标集合从黑色原文移到蓝色补充。")
for uid in ["T-p4-13", "N-p4-13"]:
    setblock(uid, get(uid) + red("原稿未完证明：写到任取 y 的起步，尚未写出区间包含于 U 的推导。"))
for uid in ["T-p4-14", "N-p4-14"]:
    setblock(uid, get(uid) + red("原稿未完反证：写到“若不然”，未继续推出端点矛盾。"))
setblock("N-component-endpoint-proof", r"""> [!info] 补证：有限端点不属于开集
> 先设 $\alpha\in\mathbb R$。若 $\alpha\in U$，由开性可取 $\varepsilon>0$，使 $(\alpha-\varepsilon,\alpha+\varepsilon)\subset U$。它与 $I_x=(\alpha,\beta)$ 相交，二者之并是包含于 $U$ 的开区间。由于 $x<\beta$，可选有限实数 $b$ 使 $x<b<\beta$（$\beta=+\infty$ 时也能选）。于是有限开区间 $(\alpha-\varepsilon/2,b)$ 属于原定义的 $G_x$，但其左端点小于 $\alpha$，与 $\alpha$ 是全部左端点的下确界矛盾。
> 对右端点，若 $\beta\in\mathbb R\cap U$，取 $\varepsilon>0$ 使 $(\beta-\varepsilon,\beta+\varepsilon)\subset U$；再取有限实数 $a$ 使 $\alpha<a<x$。有限开区间 $(a,\beta+\varepsilon/2)$ 包含于上述邻域与 $I_x$ 的并，故属于 $G_x$，却有右端点大于 $\beta$，与上确界矛盾。
> 因此所有有限端点都不属于 $U$。无穷端点不是实数，不把 $\pm\infty\notin U$ 当作额外的实轴拓扑结论。这个论证始终回代到原先只取有限端点的区间族。""")
replace("N-topology-count-candidate", "**先构造有限独立集族。**",
        "**先构造独立集族（任意有限正负组合非空）。**")
replace("N-topology-count-candidate",
        "有限交封闭已证；非空族的并包含其中任一成员，因而由向上封闭仍在该族中；空族之并则是空集。",
        "有限交中若有空集，交为空集；否则由滤子对有限交封闭得交仍在滤子中，空个集合之交取 $D$。对任意并，若所有成员都是空集（也包括空指标族），并为空集；否则选一个非空成员 $U_0\\in\\mathcal F_\\varepsilon$，该并包含 $U_0$，由向上封闭得并仍在滤子中。")

# p5: complete the radix hint, retain both connectedness proofs, and move the
# connected-component tool before its first use.
setblock("T-p5-10", "**Ex 1：**实区间[Q010]。")
setblock("N-p5-10", r"""<a id="s6-1"></a>
### 6.1 先备例题：实区间连通与进制提示

**原题。**实区间[Q010]。""")
setblock("T-p5-11", r"""**pf：**$p$ 进制小数至多有两种展开。

〔中间字词依局部笔画恢复，记录见 Q005；首符按字母 $p$ 排版。〕""" +
         red("原稿未完证明：此处只有进制展开提示，没有继续写推导。"))
setblock("N-p5-11", r"""原稿证明提示：“$p$ 进制小数至多有两种展开。”〔局部恢复见 Q005 记录。〕""" +
         red("原稿未完证明：这一行提示之后没有继续展开证明。"))
replace("N-interval-connected-proof", "> 原题中的“连”按通常用法理解为连通。",
        "> 若题头 Q010 按“实区间均连”理解，所问命题就是任意实区间连通。下面保留一条独立的上确界证明。")
replace("N-interval-connected-proof",
        "原稿最后一句的中间字形尚未唯一辨定，不能据此声称它已经给出了完整证明。若意在使用进制展开，应另行说明展开规则及它如何推出区间不可分；上述上确界证明给出了本题独立可用的完整解答。",
        "这条上确界路线与前面的进制分割路线分别保留，均属蓝色补证，不把原稿的一行提示扩写成黑色原文。题头 Q010 的字形判断另存。")
for uid in ["T-p5-04", "N-p5-04"]:
    setblock(uid, get(uid) + red("原稿未完反证：只保留了使用两个构成区间的提示，没有写出矛盾步骤。"))
component_text = get("N-local-connected-definition")
assert "> 局部连通指" in component_text
first, last = component_text.split("> 局部连通指", 1)
first = first.replace("补充：连通分支与局部连通", "补充：连通分支的定义与存在性")
add("N-components-definition-tool", first.strip(), "N-connected-subset-interval",
    sources=["RA06-P005-U01", "RA06-P005-U02"],
    evidence=["image:p0005"],
    explanation="把已写完整的连通分支定义与共有点并连通证明移到首次调用之前。")
setblock("N-local-connected-definition",
         "> [!info] 补充：局部连通\n> 连通分支的定义与存在性已在 §6.1 给出。\n> 局部连通指" + last)

# Complete supplemental math for the two genuinely plausible source questions.
add("N-finite-dimensional-heading", r"""<a id="s3-5"></a>
### 3.5 候选题意：有限维空间的紧性刻画""",
    "N-p3-index-repair", origin="editorial", evidence=["artifact:editorial-record"],
    explanation="新增条件性补证标题，放在BW、范数等价、Heine–Borel与紧/列紧工具之后。")
add("N-finite-dimensional-statement", r"""> [!info] 候选题意的精确陈述
> 若第2页提要的词是“有限维”，对应的准确刻画如下：对实或复赋范空间 $X$，以下三者等价：
>
> 1. $X$ 有限维；
> 2. $X$ 的每个闭有界子集都紧；
> 3. $X$ 的闭单位球紧。
>
> 结合度量空间中紧与列紧等价，还可表述为：对 $X$ 的每个子集 $M$，$M$ 列紧当且仅当 $M$ 在 $X$ 中闭且有界。“每个子集”的量词不能省略；一个特定集合闭有界或紧，不能刻画整个空间的维数。以下证明这一明确命题，不把它当成 Q006 的字形已经确认。""",
    "N-finite-dimensional-heading", evidence=["artifact:finite-dimensional-candidate"])
add("N-finite-dimensional-closed-tool", r"""> [!info] 先备工具及证明：有限维线性子空间闭
> 若 $Y=\operatorname{span}\{e_1,\ldots,e_m\}$，其中 $e_i$ 线性无关，由 §3.3 的有限维范数等价性，存在 $c>0$，使
> $$\left\|\sum_{i=1}^m a_ie_i\right\|\ge c\left(\sum_{i=1}^m|a_i|^2\right)^{1/2}.$$
> 若 $y_k=\sum_i a_{k,i}e_i\in Y$ 且 $y_k\to x\in X$，把上述下界用于 $y_k-y_l$，知每个坐标列 $(a_{k,i})_k$ 都是 Cauchy 列，故收敛到某个 $a_i$。有限和连续，故 $y_k\to\sum_i a_ie_i$；由极限唯一性，$x=\sum_i a_ie_i\in Y$。所以 $Y$ 闭，零子空间也显然闭。复数情形的范数等价可把 $\mathbb C^m$ 识别为 $\mathbb R^{2m}$，使用同一证明。""",
    "N-finite-dimensional-statement", evidence=["artifact:finite-dimensional-candidate"])
add("N-riesz-lemma-tool", r"""> [!info] 先备工具及证明：Riesz 引理
> 若 $Y$ 是赋范空间 $X$ 的真闭线性子空间，且 $0<\theta<1$，则存在单位向量 $u$，使 $d(u,Y)>\theta$。
>
> 取 $z\notin Y$。因为 $Y$ 闭，$d=d(z,Y)>0$；由下确界定义，选 $y_0\in Y$ 使 $\|z-y_0\|<d/\theta$。令 $u=(z-y_0)/\|z-y_0\|$。对任意 $y\in Y$，有 $y_0+\|z-y_0\|y\in Y$，所以
> $$\|u-y\|=\frac{\|z-(y_0+\|z-y_0\|y)\|}{\|z-y_0\|}
> \ge\frac d{\|z-y_0\|}>\theta.$$
> 取下确界便得结论。这里不要求空间完备，也没有假设距离取得最小值。""",
    "N-finite-dimensional-closed-tool", evidence=["artifact:finite-dimensional-candidate"])
add("N-finite-dimensional-proof", r"""> [!info] 完整证明：三种刻画互相推出
> **1 推出 2。**选基将 $X$ 识别为 $\mathbb R^m$ 或 $\mathbb C^m$；范数等价保持拓扑、闭性及有界性。复数情形再识别为 $\mathbb R^{2m}$，用已经证明的欧氏 Heine–Borel 定理，即得每个闭有界子集紧。
>
> **2 推出 3。**范数连续，闭单位球是闭有界集，直接应用前提。
>
> **3 推出 1。**反设 $X$ 无限维。选单位向量 $u_1$。已选 $u_1,\ldots,u_n$ 时，其线性包 $Y_n$ 有限维，故由前面的工具可知它闭；又因 $X$ 无限维，它是真子空间。用 Riesz 引理取 $\theta=1/2$，选单位向量 $u_{n+1}$ 满足 $d(u_{n+1},Y_n)>1/2$。因此 $i<j$ 时有 $\|u_j-u_i\|>1/2$。这个点列全在闭单位球内，却没有 Cauchy 子列，更没有收敛子列；与闭单位球紧、因而列紧矛盾。所以 $X$ 有限维。
>
> 零维空间的三个条件都直接成立。证明没有预设 $X$ 完备，有限维的结论也不是由一个特定闭有界集合的紧性推出。""",
    "N-riesz-lemma-tool", evidence=["artifact:finite-dimensional-candidate"])

add("N-base-expansion-proof", r"""> [!info] 补全原进制提示：存在性与至多两种展开
> 固定整数 $p\ge2$。对 $0\le x<1$，令
> $$a_n=\lfloor p^nx\rfloor-p\lfloor p^{n-1}x\rfloor\in\{0,\ldots,p-1\}.$$
> 望远镜相消给出
> $$S_n=\sum_{j=1}^n a_jp^{-j}=p^{-n}\lfloor p^nx\rfloor,\qquad
> 0\le x-S_n<p^{-n}\longrightarrow0.$$
> 所以 $x=\sum_{j\ge1}a_jp^{-j}$。对 $x=1$，全部数位取 $p-1$，几何级数之和为 $1$。因此 $[0,1]$ 中每个数都有这种小数部分表示。
>
> 若两个表示 $(a_j)$、$(b_j)$ 在第 $k$ 位第一次不同，不妨 $a_k<b_k$。两表示之差给出
> $$0<(b_k-a_k)p^{-k}=\sum_{j>k}(a_j-b_j)p^{-j}
> \le(p-1)\sum_{j>k}p^{-j}=p^{-k}.$$
> 左侧的整数差至少为 $1$，故处处取等号：$b_k=a_k+1$，并且每个 $j>k$ 都有 $a_j=p-1$、$b_j=0$。若某一尾项未取到上界，正权重会使总和严格小于上界，因此这一尾部结论对每一位成立。
>
> 不可能有三个不同表示：按字典序排列 $a<b<c$，比较 $a,b$ 迫使中间序列 $b$ 从某位起全为 $0$；比较 $b,c$ 又迫使它从某位起全为 $p-1$，与 $p\ge2$ 矛盾。因此至多两种，差别只能是终止的全零尾与借一位后的全 $(p-1)$ 尾。例如
> $$0.1000\ldots{}_p=0.0(p-1)(p-1)(p-1)\ldots{}_p=\frac1p.$$
> 只准小数部分的约定下，$0$ 是全零，$1$ 是全 $(p-1)$；若允许整数位，则 $1.000\ldots{}_p$ 也是 $1$ 的表示。一般实数可先处理符号和整数部分。原提示中的“至多”不能改成“恰有”，非终止型的多数数值只有一种表示。""",
    "N-p5-11", evidence=["artifact:base-expansion-candidate", "artifact:base-expansion-finite-check"],
    explanation="补全原p进制提示的存在性、至多两种及尾部关系；一般证明和精确分数例子核验分别保存。")
add("N-interval-subdivision-proof", r"""> [!info] 另一条完整路线：p 等分闭区间套证明连通
> “至多两种展开”单独一句还不是区间连通的完整证明。若 Q010 指区间连通，可把进制所对应的逐次分割落实如下，同时保留后面的上确界路线。
>
> 反设实区间 $I=A\cup B$，其中 $A,B$ 非空、不交、相对开；二者互为补集，所以也相对闭。取 $a\in A$、$b\in B$，交换名称后可设 $a<b$，于是 $[a,b]\subset I$。
>
> 将 $[a,b]$ 分成 $p$ 个等长闭小区间。依次看其 $p+1$ 个端点：首端在 $A$、末端在 $B$，故至少有一对相邻端点，左端在 $A$、右端在 $B$。选这对端点构成的 $[a_1,b_1]$，重复此过程，得到嵌套闭区间 $[a_n,b_n]$，满足 $a_n\in A$、$b_n\in B$ 且 $b_n-a_n=(b-a)p^{-n}$。
>
> 由实数完备性，令 $c=\sup_n a_n$，便有每个 $n$ 都满足 $a_n\le c\le b_n$。区间长度趋零，故 $a_n\to c$、$b_n\to c$，且 $c\in[a,b]\subset I$。因为 $A,B$ 在 $I$ 中都闭，得到 $c\in A\cap B$，矛盾。因此实区间连通；空区间和单点区间也按定义连通。
>
> 相邻的 p 进小区间共享端点，对应前面终止尾与循环尾的双重表示。此证明始终保留闭区间的共同端点，没有把两种表示的数遗漏，也没有把原稿提示直接冒称为已经写完的证明。""",
    "N-base-expansion-proof", evidence=["artifact:base-expansion-candidate"],
    explanation="完整保留与p进分割对应的闭区间套路线；与已有上确界法并列，题头字形仍未决。")

replace("N-toc",
        "  - [3.4 原稿路线：二分闭方块证明 Heine–Borel](#s3-4)",
        "  - [3.4 原稿路线：二分闭方块证明 Heine–Borel](#s3-4)\n  - [3.5 候选题意：有限维空间的紧性刻画](#s3-5)")
replace("N-toc", "6.1 先备例题：实区间连通", "6.1 实区间连通、进制提示与连通分支工具")

# Provisional source/target statuses. Finer source splitting and true pass2
# records will be integrated separately from the reviewer's actual files.
sources = json.loads((NEW / "source-units.json").read_text())
statuses = {"RA06-P002-U01": "unresolved", "RA06-P002-U02": "resolved",
            "RA06-P003-U06": "unresolved", "RA06-P003-U15": "unresolved",
            "RA06-P003-U16": "unresolved", "RA06-P005-U10": "unresolved",
            "RA06-P005-U11": "resolved"}
for source in sources:
    if source["id"] in statuses:
        source["status"] = statuses[source["id"]]
for target in mapping["targets"]:
    related = [s for s in sources if s["id"] in target["source_ids"]]
    if related:
        target["status"] = "unresolved" if any(s["status"] == "unresolved" for s in related) else "resolved"
for key, filename in [("T", "source-transcript.md"), ("N", "study-notes.md")]:
    text = "\n\n".join(f"<!-- unit: {uid} -->\n{body}" for uid, body in docs[key]).rstrip() + "\n"
    (NEW / filename).write_text(text)
for name, data in [("mapping.json", mapping), ("source-units.json", sources)]:
    (NEW / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
for filename in ["ra06-finite-dimensional-candidate.md", "ra06-base-expansion-candidate.md",
                 "ra06-base-expansion-finite-check.json"]:
    shutil.copy2(RUN / "research" / filename, P / "research" / filename.removeprefix("ra06-"))
(NEW / "integration-progress.json").write_text(json.dumps({
    "author": "/root", "basis": "VISUAL_SECOND revision-tasks VS-R001..VS-R023 and actual mathematical rechecking",
    "status": "body_revision_complete_metadata_splitting_pending",
    "changed_body_units": list(dict.fromkeys(changes)),
    "preserved_compared_directory": "proposals/rebuild",
    "not_an_independent_review": True
}, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"directory": str(NEW), "transcription_units": len(docs["T"]),
                  "study_units": len(docs["N"]), "changed_units": len(set(changes))}))
