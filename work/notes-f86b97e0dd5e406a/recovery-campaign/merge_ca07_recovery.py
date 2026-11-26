#!/usr/bin/env python3
"""Compile the Boss's authored CA07 merge; never infer review acceptance.

The three original proposal sets remain immutable. This script uses only CA07
material. Its output stays unresolved until the actual current nonauthor review.
"""
from pathlib import Path
import copy
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "work/notes-f86b97e0dd5e406a/notes/CA07/project"
sys.path.insert(0, str(ROOT))
from tools.catalog_note_evidence import catalog
from tools.build_note_ledger import build

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def note(title, body):
    return "> [!note] " + title + "\n>\n" + "\n".join(
        "> " + line if line else ">" for line in body.strip().splitlines())

plan = read(PROJECT / "content-plan.json")
if plan.get("recoveries") or any(x["pass"] == 2 for x in plan["observations"]):
    raise SystemExit("This one-time merge refuses an already-merged/reviewed plan.")
T = copy.deepcopy(read(PROJECT / "proposals/ca07_visual/recovery/transcription-blocks-revised.json"))
S = copy.deepcopy(read(PROJECT / "proposals/ca07_math/recovery/study-blocks-revised.json"))
tb = {x["id"].removeprefix("CA07-TRANSCRIPTION-"): x for x in T}
sb = {x["id"].removeprefix("CA07-STUDY-"): x for x in S}

def set_t(key, text, sources=None):
    b = tb[key]
    b["text"] = text.strip()
    if sources is not None:
        b["source_ids"] = list(dict.fromkeys(sources))

def set_s(key, text, sources=None):
    b = sb[key]
    b["text"] = text.strip()
    if sources is not None:
        b["source_ids"] = list(dict.fromkeys(sources))

def from_t(key, *keys):
    set_s(key, "\n\n".join(tb[k]["text"] for k in keys),
          [sid for k in keys for sid in tb[k]["source_ids"]])

def extend_sources(block, *ids):
    block["source_ids"] = sorted(set(block["source_ids"]) | set(ids))

set_t("001", r"""# 交换代数 7 · 原稿逐页转写

按原 PDF 物理页序编排。黑字记录原稿，红字保留原有明确提问，蓝色提示块给出释义、恢复理由、订正和补证。局部方括说明原笔形；上下文恢复不等同于逐笔清晰可读。两条原红问均紧接蓝色解答。

## 物理页 1""")
set_t("004", r"""$Q_k=\{a\in k\mid f(x)\in\mathbb Z[x]\ \text{〔独竖〕不可约多项式}\}$〔首圈下有长尾；“不可约多项式”末三字草连。〕""")
set_t("005", r"""$V(Q_k)$ 的根是代数整数，〔首符为下弯上扬的 $V$ 形；$Q$ 圈内有交叉尾。〕""")
set_t("V-005", note("代数整数：原限定与规范定义", r"""
原集合使用带尾的 $Q_k$ 记号，并写“不可约多项式”。这里另用规范记号 $\mathcal O_k$ 表示代数整数环。定义应为

$$
\mathcal O_k=\{a\in k\mid \exists f\in\mathbb Z[T]\text{ 首一},\ f(a)=0\}.
$$

原集合未明确写出存在量词和求根条件；前面的 $f(a)=0$ 属于上一语段。不可约也不能替代首一：$2T-1$ 是本原一次整系数不可约式，根为 $1/2$。若 $1/2$ 满足次数 $n\ge1$ 的首一整系数关系，乘以 $2^n$ 得到 $1$ 加偶数等于 $0$，矛盾。

下一行的 $V(Q_k)$ 没有在此稿中定义，不能直接当成一个已定义多项式的根集。可成立的相关命题是：一个首一多项式若系数均为代数整数，其根仍为代数整数；完整的有限模证明见学习稿“代数整数的和、积及首一方程的根”。这里保留原记号和“根”字，不把该句暗改成“和”。
"""))
extend_sources(tb["V-005"], "CA07-P002-U12", "CA07-P002-U14",
               "CA07-P004-U08", "CA07-P004-U10", "CA07-P004-U11",
               "CA07-P006-U12", "CA07-P006-U13")
set_t("006", "曲线尖点与参数。")
set_t("007", r"$X=V(y^2-x^3)$ 在 $\mathbb A^2$ 中的表示")
set_t("V-001", note("图前短语与二维环境", r"""
$A$ 的原上标是短弯钩；两个坐标 $x,y$ 及右侧曲线图支持读为 $\mathbb A^2$。图前小字按“的表示”恢复：首组是小圈接下兜，中组上横交竖、下有衣样折，末两墨团合读为“示”的主笔及右侧点划。末团间距仍是这项上下文恢复的限制，裁图完整保存在证据中。
"""))
extend_sources(tb["V-001"], "CA07-P001-U13", "CA07-P001-U14")
set_t("008", r"""![原稿尖点示意](assets/ca07-cusp.png)

〔原图裁片：两条粗支在左端相接，分别向右上、右下张开。尖端有回圈浓墨及短扫，右下枝外另有一点；图中没有另加坐标轴。〕""")
set_t("010", r"""记 $k[t^2,t^3]$ 中 $t^2-a^2=0$ 不能 $a\in k$。〔“不能”后直接接 $a\in k$；未补成原稿没有写出的连接词。〕""")
set_t("V-006", note("参数环中的整元素", r"""
在 $R=k[t^2,t^3]$ 中所有单项式次数都为 $2i+3j$，故 $t\notin R$。但形式多项式 $T^2-t^2\in R[T]$ 首一，在 $T=t$ 处为零，所以 $t$ 整于 $R$。若取原末尾所写的常数 $a\in k$，则 $t^2-a^2$ 不是零多项式；即使在 $k(t)$ 中求 $a^2=t^2$，因式分解也只给出 $a=\pm t$，不在 $k$ 内。“不能”按此原句保留，补证明确其数学含义。
"""))
set_t("017", r"""循环生成元。 $f(b)=0$ $n\text{—}\deg f(x)$〔横线自 $n$ 右腹起，上方有孤点；题头首二字为同手字形与上下文恢复。〕""")
set_t("V-007", note("次数、生成幂与题头", r"""
此处次数记号按上下文释为 $n=\deg f(x)$。采用后文的首一关系且 $A\ne0$ 时，原首式求和上限为 $n$，加入 $b^n$ 只是多列一个由低次幂表示的生成元。零环按后文元素关系的约定单独处理。

题头取“循环生成元”：首字双斜与低围圈对应“循”，次字与第七页“环”的离横、下折相参。另一独立读法“给示”保留在恢复记录中。这里可把 $A[b]$ 看成由 $1$ 循环生成的 $A[T]$ 模，$T$ 作用为乘 $b$；它的底层 $A$ 模不必循环。例如 $\mathbb Z[\sqrt2]$ 作为 $\mathbb Z$ 模需要 $1,\sqrt2$ 两个生成元。
"""))
extend_sources(tb["V-007"], "CA07-P002-U01", "CA07-P002-U02",
               "CA07-P002-U06", "CA07-P002-U07", "CA07-P002-U10",
               "CA07-P002-U11", "CA07-P002-U12", "CA07-P007-U02")
set_t("022", r"""$\forall m\ge n,$ $1,\ldots,b^{n-1}$ 是一组生成元〔“是”的收笔贴近后一字，按句法恢复。〕""")
tb["V-008"]["text"] = tb["V-008"]["text"].replace(
    "“〔的形〕一组生成元”可按句法读“是一组生成元”。", "")
set_t("030", r"""$\times b\mathrel{\text{〔上圆点、下短斜〕}}\ A[b]\longrightarrow A[b]$""")
set_t("033", "线性：〔首字与第一页“曲线”的“线”同手；次字按连笔及相邻线性式恢复。〕")
set_t("034", r"""$\varphi_b(a_i)=d_{i\,\text{〔离体短横〕}\,1}a_i+\cdots d_{ri}a_i$〔三个被作用或相乘元素都写 $a_i$；首系数的长下笔按 $1$ 恢复，其收笔没有下一行 $j$ 的大回钩，离体短横另存。〕""")
set_t("035", r"""$D=(d_{ij})_{r\times n}\in M_rA$〔首维及 $M$ 下标均为高干单右肩的 $r$ 形；原 $A$ 外未写括号。〕""")
set_t("037", r"""$M_r(A)$ 取 $C^*$ $\exists\ \dfrac{C^*C}{\det(C)}=I$〔$M$ 下标同前一行的单肩形；两处上标为交叉和弯笔，分式前保留 $\exists$ 形。〕""")
set_t("038", r"""<span style="color:red">（找一个自然的方法）</span>""")
set_t("V-012", note("行列式技巧回答原问", r"""
各环与模均带单位。若 $A[b]=0$，则在原包含 $A\subseteq B$ 下 $A=B=0$，直接有元素关系 $b+0=0$；此时不为零多项式赋一次的次数。

以下设 $A[b]\ne0$，取其有限 $A$ 模生成元 $u_1,\ldots,u_n$，$n\ge1$。逐行选 $d_{ij}\in A$ 令 $bu_i=\sum_{j=1}^n d_{ij}u_j$，得到方阵 $D$ 和列 $U=(u_i)^{\mathsf T}$，满足 $(bI_n-D)U=0$。原纸面的 $r\times n$ 及 $M_rA$ 按字面保留；这里同一组生成元同时决定行列数，故补证使用 $n\times n$。

对 $C=bI_n-D$ 左乘伴随矩阵，由 $\operatorname{adj}(C)C=\det(C)I_n$ 得 $F(b)u_i=0$，其中 $F(T)=\det(TI_n-D)\in A[T]$。最高次项 $T^n$ 来自全取对角线的 $T$，其系数为 $1$。以 $1=\sum_i\lambda_i u_i$ 得 $F(b)=0$。这回答“自然的方法”，也说明无需原分式中的除法；行列式为非单位时，原分式没有这种意义。
"""))
extend_sources(tb["V-012"], "CA07-P001-U21", "CA07-P001-U22",
               "CA07-P001-U23", "CA07-P001-U24", "CA07-P001-U25")
set_t("V-014", note("条件次序、类型和零化子", r"""
四条按内容依次编号为（1）至（4）；第三个原括号仍录为 $(i)$。原链 $(1)\to(3)\to(4)$ 可以成立：先用前页（1）$\Rightarrow$（2），再取 $C=A[b]$ 得（3），最后取 $M=C$ 得（4）。

第（3）条的 $C$ 需要是含同一单位的中间子环；更弱地，有限 $A$ 子模 $C$ 含 $A[b]$ 且满足 $bC\subseteq C$ 也够用。反复作用给每个 $b^jC\subseteq C$，加法及 $A$ 标量的封闭使每个 $A[b]$ 元素的乘法保持 $C$；又因 $1\in C$，零化全部 $C$ 的 $a$ 满足 $a=a\cdot1=0$，故此作用忠实。

单写有限 $A$ 子模而不给乘法稳定性不能推出原结论。取域 $k$，令 $R=k[x,y]$、$A=k+xR$、$B=R[x^{-1}]$、$b=y$ 和 $C=x^{-1}A=kx^{-1}+R$。有 $A[b]=R\subseteq C\subseteq B$，且 $C$ 是由 $x^{-1}$ 生成的 $A$ 模。但 $y/x\notin C$：否则 $y\in A$，对 $x$ 取商后将使非常数 $y$ 属于 $k$。同样，若 $y$ 整于 $A$，其首一关系在注入 $B$ 的 $R$ 中为零，再模 $x$ 得 $k[y]$ 中的首一多项式恒为零，矛盾。

零化子中的 $rM=0$ 指对每个 $m\in M$ 均有 $rm=0$。忠实意为 $\operatorname{Ann}_R(M)=(0)$。
"""))
extend_sources(tb["V-014"], "CA07-P002-U06", "CA07-P002-U07",
               "CA07-P004-U08", "CA07-P004-U10", "CA07-P004-U11",
               "CA07-P004-U20", "CA07-P004-U23")
set_t("V-015", note("一般忠实模的反向证明", r"""
（4）回（1）使用忠实性。先处理 $M=0$：若它对 $A[b]$ 忠实，$A[b]=0$，于原同单位包含下 $A=B=0$，关系 $b+0=0$ 直接成立。

若 $M\ne0$，取有限 $A$ 生成元 $u_1,\ldots,u_n$，其中 $n\ge1$ 且 $A\ne0$。把作用写成 $bu_i=\sum_jd_{ij}u_j$，令 $U=(u_i)^{\mathsf T}$、$C=bI_n-D$，则 $CU=0$。在 $M^n$ 上用标量矩阵左乘，得 $\operatorname{adj}(C)CU=\det(C)U=0$。令 $F(T)=\det(TI_n-D)$，于是 $F(b)u_i=0$。每个 $m$ 是生成元的有限 $A$ 线性组合，故 $F(b)M=0$。忠实性给 $F(b)=0$，而展开最高次项可见 $F$ 是次数 $n$ 的首一式。生成元之间可以有关系，未假设 $M$ 自由。下一处原 $a\cdot1$ 则专指 $M=C$ 的构造。
"""))
extend_sources(tb["V-015"], "CA07-P001-U21", "CA07-P001-U22")
set_t("058", r"""$am$ 在 $C$ 中做乘法〔动词的亻、中央短交与右侧独立攵样大交分为三部；“法”右下长笔归厶末点，不另添逗号。〕""")
set_t("061", r"""<span style="color:red">1 哪来的</span>""")
set_t("063", r"""eg. $V$ 是有限 $k$〔后括内有上点、横波、短柱及 B 形连笔，按原缩记保形。〕 $b\in\operatorname{End}_k(V)$〔算子原字为高斜干接低圈的 $b/6$ 形；$E$ 冠横离开主干。〕""")
set_t("064", r"""$$
k[b]=\{f(b):f\in A[T]\}\qquad f(b)\cdot V=f(b)(v)
$$

〔作用左端为大 $V$ 形，右括内为小 $v$ 形；等号右邻接的两个括号压写。〕""")
set_t("065", r"""$V$ 是 $k$ 有限生成〔“限生”中间交叉、回弯密连，按上下文恢复；末“成”右近细点、远处另有短斜墨。〕， $V$ 有一个 $k[b]$ 模""")
set_t("066", r"$V$ 是一个忠实 $k[b]$ 模")
set_t("V-017", note("算子代数、有限生成及记号恢复", r"""
本段高斜干接低圈的算子字按 $b$ 排写；这与把同一算子改名为 $\sigma$ 无关，不将其说成原笔清楚写了希腊字母。第一句原写“有限 $k$”，括内密笔按原形保留；由后文 $\operatorname{End}_k(V)$、标量作用与有限生成的陈述，本例对象释为有限维 $k$ 向量空间，不把该释义冒充括内缩记的逐字展开。后句“有〔连笔〕成”按本页“有限生成 $A$ 模”的同一用法释为“有限生成”：任取有限 $k$ 基，它同时是底层 $k$ 模的有限生成组。这里给出上下文恢复，原连笔的限制仍在上一行说明。

系数应取 $k[T]$，以 $f(T)\mapsto f(b)$ 构成算子子代数 $k[b]$，常数项作为标量乘恒等算子。它通过 $f(b)\cdot v=f(b)(v)$ 作用于 $V$；原左端大 $V$ 在此改为元素 $v$。两个括号压写不必硬判成作者写了 $f(bv)$。零化每个 $v$ 的算子就是零算子，因此该作用忠实。
"""))
extend_sources(tb["V-017"], "CA07-P005-U08", "CA07-P005-U09")
set_t("067", r"""$k[t]$ 多项式〔由形末字：上短斜、长竖穿扁圈；保留原形，数学对象的恢复见下方蓝注。〕""")
set_t("068", r"""在 $V$ 上有 $k[u]$-模结构〔括内按低开弯录 $u$，没有上行 $t$ 的贯横。〕""")
set_t("069", r"""$V\in v,$ $T\cdot v\text{〔低点〕}=b(v)$〔$T$ 冠横分开，干右有小斜笔，$v$ 左边另有较高窄墨点。〕""")
set_t("V-018", note("多项式环及形式变量的恢复", r"""
这里的对象取为多项式环，原末字的竖穿圈形与“环”的通常部件并不逐笔相合，故上行保留原形描述。上行 $k[t]$ 和本行 $k[\text{u 形}]$ 都指形式变量的多项式环；下一个实际作用式又用大写 $T$。补证统一用 $T$，这属于跨行记号统一，不声称各处原字都写成同一个字母。

定义 $f(T)\cdot v=f(b)(v)$，特别有 $T\cdot v=b(v)$。因为评价保加、保乘及单位，此作用满足模公理，因而 $V$ 是 $k[T]$ 模。元素的成员关系应为 $v\in V$；原反序 $V\in v$ 和旁边两枚额外墨点均已照录。
"""))
set_t("071", r"""$m_b\mathrel{\text{〔点横〕}}\{f(x)\mid f(x)=0\}\ \lhd k[T]$〔低附字同算子的短圈形；集合右闭钩下另有细黑点，理想号为弧与离体竖，$T$ 冠横分开。〕""")
set_t("072", r"""$k[b]\cong k[T]/\mathrm{Ann}$〔左括内为高斜底圈；分母原为裸 $\mathrm{Ann}$。〕""")
set_t("V-019", note("评价同态的核与最小多项式", r"""
多项式评价 $\operatorname{ev}_b:k[T]\to k[b]$，$f\mapsto f(b)$ 是满同态。其核

$$
I_b=\operatorname{Ann}_{k[T]}(V)=\{f(T)\in k[T]:f(b)=0\text{ 作为算子}\}
$$

是理想，陪集 $f+I_b\mapsto f(b)$ 良定义且为双射环同态，故 $k[T]/I_b\cong k[b]$。原纸面两个实参都写作 $x$，分母只记 $\mathrm{Ann}$；若把原 $f(x)=0$ 当多项式恒等式便只有零多项式，不能表示此核。例如非零 $V$ 上 $b=0$ 时，$T\in I_b$。

若 $d=\dim_kV>0$，$1,b,\ldots,b^{d^2}$ 在维数 $d^2$ 的 $\operatorname{End}_k(V)$ 中线性相关，故核有非零多项式。选次数最小的首一式 $\mu_b$，任一核内多项式对它长除的余式仍在核内；非零余式会违反最小性，故 $I_b=(\mu_b)$。若 $V=0$，$I_b=k[T]=(1)$，可取 $\mu_b=1$。作为像环的 $k[b]$ 已忠实作用于 $V$，所以 $\operatorname{Ann}_{k[b]}(V)=0$，不能把这个零理想误作原商式的分母。
"""))
set_t("077", r"""Step1. $M$ 是一个 $\bar R$〔右边短下弧〕模结构""")
set_t("078", r"""Step2: $M$ 的 $\bar R$ 模忠的。〔“忠”下有缩写心部；原未另写“实”。〕""")
tb["V-023"]["text"] += r"""
>
> 零环情形用元素关系统一说明：若 $A=0$，保单位的结构同态强制 $B=0$；若仅 $B=0$，其唯一元素直接满足 $b+0=0$。这不需要给 $0[T]$ 中的零多项式赋予次数。"""

set_s("001", r"""# 交换代数 7 · 整元素与模有限性

黑字保留原课文及其原错误，局部方括说明可见墨迹；红字沿用原稿的明确问题，紧接蓝色解答。蓝块用于释义、上下文恢复、订正与补证。物理页序见原稿逐页转写，内容来源通过双向映射逐项对应。""")
from_t("004", "002", "003", "004")
from_t("005", "011", "012", "013", "014")
set_s("006", note("整元素、零环约定与代数整数", r"""
环取带单位的交换环，同态保单位，模也要求单位作用为恒等。对结构同态 $\iota:A\to B$，称 $b\in B$ 整于 $A$，是说存在 $n\ge1$ 及 $a_0,\ldots,a_{n-1}\in A$ 使

$$
b^n+\sum_{j=0}^{n-1}\iota(a_j)b^j=0.
$$

当 $A\ne0$ 时，这等价于 $b$ 满足某个正次数首一多项式。若 $A=0$，保单位强制 $B=0$，取 $n=1,a_0=0$ 即有元素关系；不把 $0[T]$ 的零多项式称为一次式。若 $A\ne0$ 而 $B=0$，则 $T\in A[T]$ 本身就是所需首一式。原稿的同单位包含是其特例。原末句写“$b$ 整于 $b$”，定义中的基环应为 $A$。原次项高位的角折、点与弯笔按系数序次恢复为 $n-1$，不视为清楚的独立数字。

当 $[k:\mathbb Q]=d<\infty$ 时，每个 $a\in k$ 的 $1,a,\ldots,a^d$ 线性相关，产生非零 $f\in\mathbb Q[T]$ 使 $f(a)=0$；$f$ 可随 $a$ 改变。因为系数在域中，可将它首一化。

原集合首圈带下尾，按 $Q_k$ 保留；下面的规范名称另记 $\mathcal O_k$。代数整数要求存在首一 $f\in\mathbb Z[T]$ 且 $f(a)=0$。原集合写“不可约多项式”，没有完整写出这两个条件；不可约不替代首一。$2T-1$ 在 $\mathbb Z[T]$ 中不可约，其根 $1/2$ 却不整：把假定的首一整系数关系乘以 $2^n$ 会得到 $1$ 加偶数等于零。相反，首一式也不要求不可约，例如 $T(T-1)$ 的两个根都是代数整数。
"""))
from_t("009", "017", "018", "019")
sb["010"]["text"] += r"""
>
> 上述带次数的除法用于非零系数环；零系数环中的多项式全为零，所需元素关系直接成立。伴随恒等式本身对零环也成立。"""
from_t("011", "020", "021", "022")
sb["012"]["text"] = sb["012"]["text"].replace(
    "> 令 $n=\\deg f$。", "> 在非零系数环中令 $n=\\deg f$；零环情形已由前述元素关系单独处理。")
from_t("013", "023", "024", "025")
sb["014"]["text"] = sb["014"]["text"].replace(
    "> 任取 $u=g(b)\\in A[b]$。", "> 零系数环的情形由前述约定处理。以下任取 $u=g(b)\\in A[b]$。")
from_t("015", "026", "027", "028", "030", "031")
from_t("016", "032", "033", "034", "035", "036", "037", "039")
from_t("017", "038")
sb["018"]["text"] = sb["018"]["text"].replace(
    "回答原待填", "回答原问")
sb["018"]["text"] = sb["018"]["text"].replace(
    "> 选有限 $A$ 生成元",
    "> 若 $A[b]=0$，原同单位包含迫使 $A=B=0$，元素关系 $b+0=0$ 已成立。以下设 $A[b]\\ne0$，所以 $A\\ne0$。\n>\n> 选有限 $A$ 生成元")
sb["018"]["text"] += r"""
>
> 原 $r\times n$、$M_rA$ 以及系数行中重复的 $a_i$ 均保留在黑字中。本证明统一用同一组 $u_1,\ldots,u_n$ 记录各像，故行列均为 $n$，并不把这种数学规范化说成原笔全部清楚。"""
extend_sources(sb["018"], "CA07-P003-U04", "CA07-P001-U21", "CA07-P001-U22")
from_t("020", "047", "048", "049", "050", "051", "052", "053")
sb["021"]["text"] += r"""
>
> 更弱地，第（3）条可以取有限 $A$ 子模 $C$，要求 $A[b]\subseteq C\subseteq B$ 且 $bC\subseteq C$。这样它对 $b$ 的每个多项式稳定，仍给出 $A[b]$ 模；若 $a\in A[b]$ 零化全部 $C$，由于 $1\in C$，有 $a=a\cdot1=0$，所以此作用忠实。
>
> 单独“有限 $A$ 子模”不足。取域 $k$，令 $R=k[x,y]$、$A=k+xR$、$B=R[x^{-1}]$、$b=y$ 和 $C=x^{-1}A=kx^{-1}+R$。$A$ 是含幺子环，含 $k$ 和 $x$，故 $A[y]=R$；并有 $R\subseteq C\subseteq B$，$C$ 由 $x^{-1}$ 作为 $A$ 模生成。若 $y/x\in C$，则 $y\in A$，但 $A$ 在 $R/(x)=k[y]$ 中的像是 $k$，与 $y$ 非常数矛盾。因此 $C$ 不对乘 $b$ 稳定，也不是子环。
>
> 若 $y$ 整于 $A$，其首一关系在 $B$ 中为零。关系属于 $R$，且局部化 $R\hookrightarrow B$ 单射，故在 $R$ 中已为零。再模 $x$ 得 $k[y]$ 中一个首项系数 $1$ 的多项式为零，矛盾。这说明缺少稳定性时，结论本身也会失败。"""
extend_sources(sb["021"], "CA07-P004-U18", "CA07-P004-U19",
               "CA07-P004-U20", "CA07-P004-U21", "CA07-P004-U22",
               "CA07-P004-U23", "CA07-P005-U01")
from_t("022", "054", "055", "056", "058", "059", "060")
from_t("023", "061")
from_t("025", "062")
sb["026"]["text"] = sb["026"]["text"].replace(
    "> 给定（4），取有限 $A$ 生成元 $u_1,\\ldots,u_n$，可把 $0$ 也列入以保证 $n\\ge1$。",
    "> 给定（4），若 $M=0$，忠实性使 $A[b]=0$，原同单位包含下 $A=B=0$，直接有 $b+0=0$。以下设 $M\\ne0$，故 $A\\ne0$，取有限 $A$ 生成元 $u_1,\\ldots,u_n$，其中 $n\\ge1$。")
sb["026"]["text"] = sb["026"]["text"].replace(
    "若 $M=0$，忠实性迫使 $A[b]$ 为零环，$b=0$，关系可写作 $b+0=0$。", "")
extend_sources(sb["026"], "CA07-P001-U21", "CA07-P001-U22")
from_t("028", "041", "042", "043", "044", "045", "046")
sb["029"]["text"] = sb["029"]["text"].replace(
    "因为有理根定理给出的 $\\pm1$ 都不是根。",
    "因为若 $\\omega=p/q$ 为既约有理数、$q>0$，关系 $p^2-pq-q^2=0$ 使 $q\\mid p^2$，从而 $q=1$。但整数 $p$ 的 $p^2-p$ 为偶数，不可能等于 $1$。")
from_t("030", "006", "007", "008", "009", "010")
sb["031"]["text"] = sb["031"]["text"].replace(
    "若原句是考虑 $t^2-a^2=0$ 且 $a\\in k$，", "原末句的 $t^2-a^2=0$ 若要求 $a\\in k$，")
sb["031"]["text"] = sb["031"]["text"].replace(
    "如果题头所指的是原点的奇异性，可以按局部环定义检验。",
    "补充：原点的奇异性也可按局部环定义检验；这是在原“曲线尖点与参数”之外补出的论证。")
extend_sources(sb["031"], "CA07-P001-U13")
from_t("033", "073", "074", "075", "076", "077", "078")
from_t("035", "063", "064", "065", "066")
set_s("036", note("算子子代数作用与有限生成", r"""
本段算子原字是高斜干接低圈，按 $b$ 排写；$\sigma$ 可作改名，但不是原笔已清楚分出的希腊字母。原“有限 $k$”后的缩记保留其上点、折波与 B 形。由后文 $\operatorname{End}_k(V)$、作用及有限生成的陈述，本例释为有限维 $k$ 向量空间；这并不是把缩记逐字展开为“向量空间”。“有〔交叉连笔〕成”按同页用法恢复为有限生成，原连笔限制已在黑字旁注明。

把 $f(T)=\sum_i a_iT^i\in k[T]$ 送到 $f(b)=\sum_i a_i b^i$，其中 $b^0=\operatorname{id}_V$，常数项为标量算子 $a_0\operatorname{id}_V$。这些算子形成交换子环 $k[b]$，因为标量算子与 $b$ 的各幂彼此可交换。原系数处写 $A[T]$，本例应为 $k[T]$。

作用定义为 $f(b)\cdot v=f(b)(v)=\sum_i a_i b^i(v)$。原左端大 $V$ 在此规范为元素 $v$；右端两个压写括号可按实际求值分开，不必判成 $f(bv)$。乘法的结合性给 $(SU)(v)=S(U(v))$，单位算子保持 $v$，分配律由算子加法和线性性给出，故是一个 $k[b]$ 模。

若某个 $S\in k[b]$ 令所有 $v$ 都映成零，按映射相等的定义 $S$ 就是零算子，因此作用忠实。又由有限 $k$ 基可知 $V$ 是有限生成的 $k$ 模；这个“有限生成”的含义与本页前一条有限生成 $A$ 模的用法一致。
"""))
extend_sources(sb["036"], "CA07-P005-U08", "CA07-P005-U09")
from_t("037", "067", "068", "069", "071", "072")
sb["038"]["text"] += r"""
>
> 原 $k[t]$ 后的末字仅保留竖穿扁圈的笔形描述，此段由多项式作用确定其数学对象为多项式环。下一行括中的 u 形变量以及作用式的大写 $T$ 在补证中统一为 $T$；不把这种变量统一冒充原稿字母完全一致。"""
from_t("040", "079", "080", "088")
sb["041"]["text"] = sb["041"]["text"].replace(
    "上面淡写的末指标统一记作 $s$，指数 $e_i$ 为非负整数。",
    "原末幂短直尾按 $e_1$ 保留，补证将第 $i$ 个因子的指数统一记为 $e_i$，特别末项为 $e_s$；各指数均为非负整数。")
sb["041"]["text"] = sb["041"]["text"].replace(
    "分别给每个 $b_i$ 选一个次数为",
    "若 $A=0$，保单位使目标环为零，有限生成结论直接成立。以下取 $A\\ne0$，分别给每个 $b_i$ 选一个次数为")
tb["V-021"]["text"] = tb["V-021"]["text"].replace(
    "> 若第 $j$", "> 若 $A=0$，目标环为零，有限生成结论直接成立。以下设 $A\\ne0$。若第 $j$")
from_t("042", "082", "083", "084", "085", "086", "087")
sb["043"]["text"] += r"""
>
> 原首次多项式环末下标写成 n/h 形，此处按 $n$ 照录；商环式则实写离体 s 形。补证中使用同一个变量数 $s$。原末行的 $d_s$ 对应前面生成元 $b_s$，规范证明须指同一组元素。若 $A=0$，则保单位结构同态强制 $B=0$；若仅 $B=0$，唯一元素直接满足关系 $b+0=0$，均符合前述整性定义。"""
sb["043"]["text"] = sb["043"]["text"].replace(
    "> 设结构同态为 $\\iota\\colon A\\to B$。",
    "> 设结构同态为 $\\iota\\colon A\\to B$。若 $B=0$，则 $B=\\iota(A)$，已是有限型代数，也由 $0$ 作为 $A$ 模生成；唯一元素满足 $b+0=0$。以下设 $B\\ne0$，因此 $A\\ne0$。")
from_t("044", "005")
sb["045"]["text"] = sb["045"]["text"].replace(
    "首字和环名尚未定读。按末处可能为「根」的用法，这里证明首一的代数整数系数式的任一根仍是代数整数。",
    "原行保留 $V(Q_k)$ 和“根”，但 $V(Q_k)$ 在稿中未定义；它不能单独充当一个成立的命题。以下给出与“根”相应、条件完整的命题：首一的代数整数系数多项式的任一根仍是代数整数。")
sb["045"]["text"] = sb["045"]["text"].replace(
    "设系数 $c_1,\\ldots,c_n$ 都是代数整数，",
    "设系数 $c_1,\\ldots,c_n$ 都是代数整数，在包含这些系数的同一扩域中取 $\\gamma$，")
extend_sources(sb["045"], "CA07-P002-U10", "CA07-P002-U11",
               "CA07-P002-U12", "CA07-P002-U13", "CA07-P002-U14")

# A source transcript must contain the full source, while each added assertion
# has its actual source edges. The root-closure proof is provided in both bodies.
root_closure = copy.deepcopy(sb["045"])
root_closure["id"] = "CA07-TRANSCRIPTION-B-001"
root_closure["explanation"] = "原根句的条件补全与有限模证明；同篇已实际审读的数学稿蓝注在转写中完整收录。"
root_closure["text"] = root_closure["text"].replace(
    "补充｜代数整数的和、积及首一方程的根", "补证｜代数整数的运算与根")
idx = next(i for i,x in enumerate(T) if x["id"] == "CA07-TRANSCRIPTION-V-005")
T.insert(idx+1, root_closure)

# Preserve proposal history. New content has its own Boss-specific provenance.
for blocks in [T, S]:
    for b in blocks:
        b.pop("evidence_paths", None)
        b["status"] = "resolved" if b["origin"] == "editorial" else "unresolved"
        if b["origin"] != "editorial":
            b["explanation"] += "；Boss 合并三份独立恢复并回图修订；合并时等待当前版本的非作者第二遍，其后接受情况以独立绑定报告为准。"
        if any(ord(c) < 32 and c != "\n" for c in b["text"]):
            raise ValueError("Unexpected control character in " + b["id"])
        if "\notin" in b["text"]:
            raise ValueError("A literal newline corrupted a notin macro in " + b["id"])

decisions_file = PROJECT / "audit/recovery-merge/boss-decisions.json"
if not decisions_file.exists():
    raise SystemExit("Body merge prepared; explicit Boss decisions must be authored before compilation.")
decisions = read(decisions_file)
if len(decisions["records"]) != 56:
    raise ValueError("Every actual worklist item must have a distinct Boss decision.")
for key, needed in {
    "V-005":["CA07-P001-U05","CA07-P001-U06","CA07-P001-U07","CA07-P001-U08","CA07-P001-U09"],
    "V-007":["CA07-P002-U04","CA07-P002-U10"],
    "V-014":["CA07-P004-U15","CA07-P004-U16","CA07-P004-U17","CA07-P004-U18","CA07-P004-U19"],
    "V-015":["CA07-P005-U05"]
}.items():
    if not set(needed).issubset(tb[key]["source_ids"]):
        raise ValueError("A directly cited source edge is missing from "+key)
if "1 形" not in tb["054"]["text"] or r"\mathrm{Ann}(R)(M)" not in tb["074"]["text"] or r"\mathrm{Ann}_R(M)" not in tb["076"]["text"]:
    raise ValueError("A preserved source variant was lost while assembling the bodies.")

# Evidence registration only computes metadata; it is not a review.
inputs_file = PROJECT / "audit/recovery-merge/catalog-inputs.json"
inputs = read(inputs_file)
new_catalog = catalog(PROJECT, inputs)
by_path = {x["path"]: x for x in plan["evidence_artifacts"]}
for x in new_catalog["evidence_artifacts"]:
    if x["path"] in by_path and by_path[x["path"]]["id"] != x["id"]:
        raise ValueError("Evidence identity changed for " + x["path"])
    by_path[x["path"]] = x
plan["evidence_artifacts"] = list(by_path.values())
eid = {p: "artifact:"+x["id"] for p,x in by_path.items()}
for page in read(PROJECT/"manifest.json")["pages"]:
    eid[page["image"]["path"]] = "image:"+page["id"]
    for region in page["regions"]:
        eid[region["image"]["path"]] = "image:"+region["id"]

def evidence(paths):
    return sorted({eid[p] for p in paths})

worklist = read(PROJECT / "audit/recovery-worklist.json")["records"]
workmap = {x["recovery_id"]:x for x in worklist}
role_records = {}
for role in ["visual", "math", "adversarial"]:
    doc = read(PROJECT / f"proposals/ca07_{role}/recovery/recoveries-proposal.json")
    rows = doc["records"] if isinstance(doc, dict) else doc
    role_records[role] = {x["recovery_id"]:x for x in rows}

recoveries, issues = [], []
boss_path = "audit/recovery-merge/boss-decisions.json"
old_issues = {x["id"]:x for x in plan["issues"]}
for d in decisions["records"]:
    rid = d["id"]
    original = workmap[rid]
    candidates, supporting = [], [boss_path]
    for role, rows in role_records.items():
        proposal = rows[rid]
        report = f"proposals/ca07_{role}/recovery/recoveries-proposal.json"
        supporting.append(report)
        for i,c in enumerate(proposal["candidates"],1):
            paths = list(dict.fromkeys([report]+c.get("evidence_paths",[])))
            candidates.append({"id":f"{role}-{i}", "text":c["text"],
                               "evidence_ids":evidence(paths)})
        supporting.extend(proposal.get("evidence_paths",[]))
    supporting.extend(d["evidence_paths"])
    selected_evidence = evidence(list(dict.fromkeys([boss_path]+d["evidence_paths"])))
    candidates.append({"id":"boss-merged", "text":d["selected_text"],
                       "evidence_ids":selected_evidence})
    recovery = {
        "id":rid, "source_ids":sorted(set(original["source_ids"]) | set(d.get("extra_source_ids",[]))),
        "problem":original["problem"], "candidates":candidates,
        "selected_candidate_id":"boss-merged", "status":"unresolved",
        "evidence_ids":evidence(list(dict.fromkeys(supporting))),
        "forward_validation":{"status":"pass","method":d["forward_method"],
                              "inputs":d["forward_inputs"],"result":d["forward_result"],
                              "evidence_ids":selected_evidence},
        "backward_validation":{"status":"pass","method":d["backward_method"],
                               "inputs":d["backward_inputs"],"result":d["backward_result"],
                               "evidence_ids":selected_evidence},
        "return_to_image":{"page_ids":[],"region_ids":[],"evidence_ids":selected_evidence,
                           "observation":d["image_observation"]},
        "reviewer_id":"/root/ca07_adversarial","session_id":"/root/ca07_adversarial"
    }
    # Nonacceptance is explicit: the named actual reviewer will independently
    # check this proposal; the unresolved status cannot be used as a pass.
    recoveries.append(recovery)
    old = copy.deepcopy(old_issues[original["issue_id"]])
    old["status"] = "open"
    old["related_ids"] = sorted(set(old["related_ids"] + recovery["source_ids"] + [rid]))
    old["evidence_ids"] = sorted(set(old["evidence_ids"] + selected_evidence))
    old["resolution"] = ""
    issues.append(old)

plan["transcription_blocks"], plan["study_blocks"] = T,S
plan["recoveries"], plan["issues"] = recoveries,issues
plan["observations"] = [{"pass":1,"reviewer_id":"/root/ca07_visual",
                         "session_id":"/root/ca07_visual",
                         "path":"audit/recovery-merge/first-pass-observations.json",
                         "artifact_id":by_path["audit/recovery-merge/first-pass-observations.json"]["id"]}]
labels = read(PROJECT / "audit/recovery-merge/source-labels.json")
for source in plan["sources"]:
    source["label"] = labels[source["id"]]
    source["status"] = "unresolved"
for blocks in [T,S]:
    covered = {s for b in blocks for s in b["source_ids"]}
    if covered != {s["id"] for s in plan["sources"]}:
        raise ValueError("Source coverage gap or alien source in merged body")
write(PROJECT / "content-plan.json", plan)
print(json.dumps(build(PROJECT), ensure_ascii=False, indent=2))
