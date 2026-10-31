---
id: "unrelated-machines/minrep-degree-alphabet-hardness-manurangsi"
kind: "literature"
type_tag: "文献"
title: "MinRep 度数与字母表逼近困难"
status: "full-source-read-with-explicit-proof-corrections"
truth_status: "randomized-hardness-with-scoped-generic-lemma-reconstruction"
review_level: "nine-page-pdf-full-read-formula-image-check-and-independent-tail-derivation"
summary: "完整整理 Manurangsi 的 Min-Rep 随机稀疏化：保留 gap g、degree O(g log g)、alphabet O(g^4 log^2 g)、0.9 概率和全列表量词；逐项修正冻结 PDF 的参数、删边尺度和下尾推导，并比较仓内 partial-MinRep v2/v3/v5 与 Minzer–Zheng 后续应用的实际边界。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/manurangsi_minrep_degree_1807_00936v1.pdf"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/manurangsi_minrep_degree_1807_00936v1.pdf"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/partial_minrep_linear_degree_source_review.md"
source_id: "533900faa02356c5f2df"
source_sha256: "259edd7e850da816ddb5c318287a7a3a525ccc8963f07918787156384d7153d8"
evidence_paths:
  - "../../tools/evidence/Boss7-minrep-restored/"
related_objects:
  - "../资料/partial-MinRep线性degree删边源与外部边界--资料.md"
  - "../审查/部分MinRep费用桥与pDM阈值双源审查--审查.md"
  - "../审查/部分MinRep高围长v3读后后缀三源与概率措辞校正--审查.md"
  - "四对一与字母表soundness两篇文献整理--文献.md"
---

【数学审查】

## 实读对象及错误的层次

对象为 Pasin Manurangsi，*A Note on Degree vs Gap of Min-Rep Label Cover and Improved Inapproximability for Connectivity Problems*，冻结 URL 为 [arXiv:1807.00936v1](https://arxiv.org/pdf/1807.00936v1)。原件 134,108 字节、9 页，两份冻结提交的字节相同。本次全文读取定义、全部定理/命题/证明、讨论、脚注及参考文献，并逐页查看渲染；特别逐图核对印 1、3、4、5、6、7 页的承重式。PDF 页眉标 2018-07-03，内部日期为 2022-05-27；此差异是实际字节的一部分，不据此改称另一 arXiv 版本。

以下不是 OCR 猜测，均已对照原图。保留原件不改写；后文给出本次可支持的重建，明确区分原文结论与修复。

| 原文位置 | 实际问题 | 本页处理及对结论的影响 |
|---|---|---|
| 印 1 摘要 | 把此前度数写为 `O-tilde(g^(1/2))`，与印 2 的 `O(g² log²g)` 和“改进”方向冲突 | 正文按印 2 的旧 `O-tilde(g²)` 记录；期刊公开摘要也已写为平方。不是把新度数改成平方根 |
| 印 4，Theorem 1 证明 | `δ=min{ε,Cq log q}` 不能保证 NO 值低于 `2C log q/q` | 取 `δ=min{ε,C log q/(2q)}` 足够，保留主定理全部渐近参数 |
| 印 5–6，Proposition 8 | 陈述及期望求和均写 `pΔn`，但原图有 `Dn` 条边；由每边概率 `≤0.0004p` 求和只能得 `0.0004pDn` | 改成 `Pr[删边数>0.1pDn]<0.01`，正好是印 7 最后调用的尺度；不声称原来的更小尺度已证 |
| 印 7，Proposition 12 证明 | 文字把坏事件写成“至少 `0.2pDn`”，与命题的“少于”相反；所写指数 `−(0.6)²(0.5pDn)` 也缺少通常二次 Chernoff 的 `1/2` | 用精确 MGF 重算，得到系数 `0.3−0.2 ln(2.5)>0.1`；因此仍保住最终 `(2Q)^(−10N/√γ)`，无需削弱 Lemma 7 的常数 |
| 印 4，Lemma 7 的字面域 | 写“任意 `ε,γ>0`”；极大 γ 使其显示的 `Δ<1`，于是任何输出必无边，而 NO 下界仍正 | 本页认证实际 hardness 所需的 `0<γ<1`、非空游戏与非空字母表域，不认证无上界 γ 的字面全域 |
| 印 5 脚注及 N 的含义 | 完全 copy-pairs blowup 提高 D，也把顶点数 N 放大；若使用该预处理，后续 N 必须指新图 | 主定理只需相同基准的比值，故不受影响。下文另给不改变 N 的低度分支，闭合有意义域内的 generic 接口 |
| 印 3，VC-kRC 定义 | 有 `D` 对需求却写 `i∈[k]` | 应为每个 `i∈[D]`；不能漏掉需求对 |

印 6 的 `Min-Rep(Γ′)` 是 `Π′` 的符号笔误；邻点集合与数值度数的比较应写集合大小。它们不改变证明。完备性证明最后一行改写成 `E′` 的事件是较小事件，但前面的同一 Markov 计算也直接控制 `E_int`，所以这一处无结论缺口。

## 审查范围与尚未认证的部分

本页独立重建稀疏化的概率链和主定理参数代入；Chan 的 PCP 及 Laekhanukit 等连通性归约仅按本文明确调用的外部定理保存，未声称重读和重新证明所有引用论文。后续 Minzer–Zheng 只实际读取相关定义、主定理、§7.4 印 60–61 页并核图，不把它升级为 106 页全文复审。新颖性、外部同行审查和一般不相关机困难性均不由本页认证。

【修改建议】

1. 使用主结果时引用下文的随机归约、字母表及度数三项完整合同；YES 为近完美单标签源，经补标签后成本 `≤2N`，不能无依据改成每个种子 singleton 完美源。
2. 复用证明时同时改正 `δ`、`pDn` 和尾界推导，不能只改一句摘要。使用原 blowup 时重命名新旧 `N`；需要保持输入 N 时使用下文显式低度分支。
3. 原文 Corollaries 3、5 虽省略随机归约字样，其上游 Theorem 1 是随机归约，故应用继续保留该限定。若转成算法排除，`NP⊄BPP` 是充分假设，不能仅由 `P≠NP` 得出相同结论。
4. 后续论文显示定理与其参数证明分开记录；本页第 7 节指出的 `δ=1/g` 及正则性接口缺口，不能因后续文献较新便自动忽略。

【论文版本】

## 1. 模型及近似的基准

有限投影游戏为
\[
\Pi=(G=(A,B,E),\Sigma,\{\pi_e:\Sigma\to\Sigma\}_{e\in E}),
\qquad Q=|\Sigma|\ge2.
\]
每个投影是全映射，不要求双射、满射或等原像数。边和字母表显式给出，`E≠∅`。单标签赋值 `φ:A∪B→Σ` 的值是满足 `π_(a,b)(φ(a))=φ(b)` 的边比例；`val(Π)` 为最大值。多标签赋值 `ψ(v)⊆Σ` 允许空列表，成本为
\[
\operatorname{cost}(\psi)=\sum_{v\in A\cup B}|\psi(v)|.
\]
边被覆盖指存在端点标签对满足其投影。`MinRep(Π)` 是覆盖**全部**边的最小成本，不是单标签最大满足数，也不是部分覆盖目标。

本次稀疏化输入为正度数 `D` 的 regular 二部游戏。因此两侧同大，记 `|A|=|B|=n`、`N=2n`、`M=Dn`。若按边记录推广到 multigraph，则每条平行约束须分别计度、采样并保留投影；不能用去重的邻点数代替重数度数。原文主要以普通图记法书写。

最大度数为 Δ 时，对每条边任选一对满足标签并加入端点，成本 `≤2M`。任何全覆盖列表必须在每个非孤点处非空，故成本至少非孤点数；而 `2M≤Δ·非孤点数`。这给出 Δ-近似。因此 degree 与 hardness gap 至少需要线性同阶；这里只说明 `O(g log g)` 距此基线至多一个对数，不证明最优字母表或最优常数。

## 2. 主结论及所调用的 PCP

**原文 Theorem 1。** 对每个先固定的整数 `g>1`，在随机多项式归约下，给定字母表
\[
Q=O(g^4\log^2g),\qquad\Delta_{\max}=O(g\log g)
\]
的投影游戏，在因子 g 内逼近 `MinRep` 是 NP-hard。固定 g 的多项式次数可以依赖 g；没有把随 SAT 输入增长的二进制 g 也当作一个统一 PCP 输入参数。

其起点为原文 Theorem 6 对 Chan [Cha16] 的陈述：存在常数 `C>0`，对每个素数幂 q 和每个固定 `δ>0`，在共同字母表大小 `q²` 的 regular 游戏上，NP-hard 区分
\[
\operatorname{val}(\Pi)\ge1-\delta
\quad\text{与}\quad
\operatorname{val}(\Pi)<C\log q/q+\delta.
\]
原文说明 Chan 原构造不一定正规，regularization 另调用 [Lae14, §§4.2–4.3]，并允许近似保值。这个外部接口不能省掉，也不能把近完美 YES 改写成 `val=1`。

## 3. Generic 稀疏化：可核实的精确合同

在 `ε>0`、`0<γ<1` 的有意义域中，置
\[
\Delta=10^6\frac{2\ln(2Q)}{\sqrt\gamma}.
\tag{1}
\]
原文 Lemma 7 声称保持字母表并使最大度数 `≤Δ`，且
\[
\operatorname{val}(\Pi)\ge1-\varepsilon
\Longrightarrow
\Pr[\operatorname{MinRep}(\Pi')\le(1+\varepsilon\Delta)N]\ge0.9,
\tag{2}
\]
\[
\operatorname{val}(\Pi)<\gamma
\Longrightarrow
\Pr[\operatorname{MinRep}(\Pi')>0.06N/\sqrt\gamma]\ge0.9.
\tag{3}
\]
概率分别针对满足相应前提的固定输入；(3) 的好事件同时排除**所有**便宜列表，包括看过随机输出后才选的列表，不是每份列表单独有 0.9 保证。

原算法先通过完全 copy-pairs blowup 假设 `D≥10000Δ`，以
\[
p=10^{-4}\Delta/D
\]
独立保留每条边成 `E_int`；再一次性标记中间度数 `>Δ` 的顶点，删掉这些顶点的全部关联边，得到 `E′`。顶点集和剩余投影不变，孤点保留。最大度数界对每个种子都成立；不是反复按删后度数迭代。

**保持输入 N 的审查修复。** 无须放大 D：若 `D≤Δ`，直接输出原图；若 `D>Δ`，使用同一 p 和一次 trimming。这时 `p<10^{-4}<1`，下文全部估计仍成立。低度分支的完备性由每条未满足边至多补两个标签给
`N+2εM=N+εDN≤(1+εΔ)N`；soundness 由第 4.2 节原图便宜列表上界直接成立。因而这项补充使 (2)–(3) 以**原输入 N**成立，不将原脚注 blowup 后的 N 静默混入陈述。这是本页的证明修复，不冒称原 PDF 已显式写出该分支。

式 (1) 的实数参数按原文概率分析约定理解；若需具体编码，可取整数上取整的度数预算并使用该实际预算重算 ε 和 p，渐近阶不变。本文不把“任意实数 ε、γ”宣传成按其不存在的二进制编码运行的统一位复杂度定理。对主 hardness 的固定参数，有限精度常数选择及显式边扫描均为多项式。

## 4. 完整证明链

### 4.1 高度 trimming 的正确尺度

设 `R=|E_int\E′|`。条件于固定边 `e=(a,b)` 已被采样，a 的中间度数期望为
`1+p(D−1)<1+pD`。由 (1) 有 `Δ>10000`，故
\[
\Pr[\deg_{int}(a)>\Delta\mid e\in E_{int}]
 <1/\Delta+pD/\Delta\le0.0002.
\]
另一端相同。无需两端高度事件独立，union bound 给
\[
\Pr[e\in E_{int}\setminus E']\le0.0004p,
\qquad \mathbb ER\le0.0004pDn.
\]
所以
\[
\Pr[R>0.1pDn]\le0.004<0.01.
\tag{4}
\]
这里严格保留 `D`。较强的 `0.1pΔn` 不是此计算的结果，也不是后续所需的结果。

### 4.2 从总列表成本到原图覆盖率

若 `val(Π)<γ` 且 `cost(ψ)≤0.06N/√γ`，则 ψ 在原图覆盖比例 `<1/2`。证明如下。令长列表阈值 `L=0.3/√γ`，列表长度 `>L` 的 heavy 顶点数严格少于
\[
\frac{0.06N/\sqrt\gamma}{0.3/\sqrt\gamma}=0.2N=0.4n.
\]
正则性使触及 heavy 顶点的边数 `<0.4Dn`。假如 ψ 覆盖至少 `0.5Dn` 条边，则仍有 `>0.1Dn` 条被覆盖边两端均 light。每个非空列表独立均匀取一个标签；空列表处任取合法标签。对这样的 light-covered 边，一对见证标签被抽中的概率至少
\[
1/(|\psi(a)||\psi(b)|)\ge1/L^2=\gamma/0.09>10\gamma.
\]
因而随机单标签赋值的期望满足边数 `>γDn`，与 `val(Π)<γ` 矛盾。空列表不可能见证被覆盖边，故不影响推理。

### 4.3 固定列表的精确下尾修复

固定满足原图覆盖比例 `<1/2` 的 ψ。其未满足边集 U 大小 `>0.5Dn`，采样后仍未满足的边数
\[
Y=|U\cap E_{int}|\sim\operatorname{Bin}(|U|,p),
\qquad \mu=\mathbb EY>0.5x,\quad x=pDn.
\]
需要控制的是坏事件 `Y<0.2x`。取 `s=ln(2.5)`，由二项 MGF 及 `1+u≤e^u`，
\[
\begin{aligned}
\Pr[Y<0.2x]
&\le e^{0.2sx}\mathbb Ee^{-sY}\\
&\le\exp(0.2sx+\mu(e^{-s}-1))\\
&\le\exp[-(0.3-0.2\ln2.5)x]\\
&\le\exp[-10^{-5}\Delta n]
 =(2Q)^{-10N/\sqrt\gamma}.
\end{aligned}
\tag{5}
\]
最后使用 `0.3−0.2ln2.5≈0.1167418536>0.1`、`pD=10^-4Δ` 和 (1)。这直接证明原文 Proposition 12 **最终**所需的指数。若只使用通常的 `exp(−δ²μ/2)`，只能先得 `exp(−9·10^-6Δn)`，不能照抄原印中间式；本页没有把该错误中间式当成真命题。

### 4.4 全列表同时性、整数成本和非空输出

令 `a=0.06N/√γ`、`t=floor(a)`。成本恰为 t 的列表族与 `(A∪B)×Σ` 的 t 元子集一一对应，数量为 `binom(NQ,t)`。非空全投影游戏总有 `val(Π)≥1/Q`，故 NO 前提给 `Q>1/γ`，在 `γ<1` 下有 `a<NQ`。当 `t≥1`，
\[
\binom{NQ}{t}
\le(eNQ/t)^t
\le(eNQ/a)^a
\le(2Q)^{0.5N/\sqrt\gamma}.
\tag{6}
\]
第二步用 `(eM/u)^u` 在 `0<u≤M` 上递增；最后可由
`0.06ln(eQ√γ/0.06)≤0.5ln(2Q)` 直接核算。`t=0` 时只有一份全空列表，计数界仍成立，不能除以 t。

由第 4.2 节、(5)–(6) 和一次 union bound，以至少
\[
1-(2Q)^{-9.5N/\sqrt\gamma}>0.99
\]
的概率，每份成本 t 的列表都在中间图留下至少 `0.2pDn` 条未覆盖边。与共同 trimming 事件 (4) 联合，概率至少 0.98，且每份这样的列表在最终图仍留下至少 `0.1pDn>0` 条未覆盖边。成本低于 t 的列表可补标签到成本 t，覆盖单调，故同一事件排除所有成本 `≤t` 的全覆盖列表。于是 `MinRep(Π′)>a`，特别得到保守的 (3)。这也同时保证好 NO 输出非空，而非另加一个没有计入概率账的假设。

### 4.5 近完美 YES 的补标签成本

取原图中满足率 `≥1−ε` 的单标签 φ，原未满足边集 `U_φ` 大小 `≤εDn`。先给每点 φ 标签，成本 N；对每条 `U_φ∩E′` 再加一对满足其全投影的标签，成本至多
\[
N+2|U_\phi\cap E'|\le N+2|U_\phi\cap E_{int}|.
\]
而
\[
\mathbb E|U_\phi\cap E_{int}|\le\varepsilon pDn
=0.00005\varepsilon\Delta N.
\]
Markov 给 `Pr[|U_φ∩E_int|>0.5εΔN]≤0.0001`，因此 (2) 的 0.9 足够保守。若原源本来 perfect-complete，纯删边当然对每个种子保同一 singleton 赋值；本文主 theorem 调用的 Chan 源却只保证近完美，二者不能混用。

## 5. 主定理的参数代入及严格 gap

先固定整数 `g>1`。取最小的足够大素数幂 q，使
\[
q/\ln q>10^5Cg^2,
\quad s=C\ln q/q,
\quad\gamma=2s,
\quad Q=q^2,
\quad\varepsilon=1/\Delta,
\quad\delta=\min\{\varepsilon,s/2\}.
\]
由素数幂可用二次幂粗定位，`q=Θ(g²logg)`，从而 `γ=Θ(g^-2)`、`Q=O(g⁴log²g)`。必要时为有限的小 g 增大固定常数；不是把 q 当 SAT 大小增长参数。Chan gap 给
\[
\text{YES}:\operatorname{val}(\Pi)\ge1-\delta\ge1-\varepsilon,
\qquad
\text{NO}:\operatorname{val}(\Pi)<s+\delta<2s=\gamma<10^{-4}/g^2.
\]
应用稀疏化后
\[
\Delta=O(\log Q/\sqrt\gamma)=O(g\log g),
\]
YES 以至少 0.9 概率有 `MinRep≤2N`，NO 以至少 0.9 概率有
\[
\operatorname{MinRep}>0.06N/\sqrt\gamma>6gN>2gN.
\]
这就是因子 g 的严格分离。每个输入只属于一种 promise，不需要让两个不同前提下的事件在同一实例上同时成立。确定性近似算法若存在，与此随机归约复合即可给 SAT 有界错误算法；此结论与仅由 `P≠NP` 排除确定性归约是不同层次。

## 6. 连通性应用：保留全部参数及外部依赖

原文研究无向图中的三个目标。RkC 给根 r 和终端集 T，选最少边子图，使每个终端与 r 有至少 k 条内部顶点不交路径。VC-SND 给终端及每对需求 `r_st≥0`，要求满足相应顶点连通度；冻结 PDF 的目标写为最少顶点子图。VC-kRC 给需求对 `(s_i,t_i),i∈[D_dem]`，删最少边使每对顶点连通度 `<k`。顶点不交约束不等于 edge-disjoint；VC-kRC 结果不涵盖允许改变 k 的 bicriteria 近似。

原文 Theorems 2、4 是对 [CLNV14, CK12, CMVZ16, Lae14] 归约的调用，而非本 note 新证明的归约。最大度数 Δ、字母表 Q 的 MinRep 实例经近似保持归约，参数如下。

| 目标 | Theorem 2 的连通度 | 代入本主定理的粗上界 | Corollary 3 的困难因子 |
|---|---|---|---|
| RkC | `k=O(Δ³Q+Δ⁴)` | `O(g⁷ log⁵g)` | `Omega-tilde(k^(1/7))` |
| VC-SND | `k=max r_st=O(ΔQ+Δ²)` | `O(g⁵ log³g)` | `Omega-tilde(k^(1/5))` |
| VC-kRC | `k=O(ΔQ)` | `O(g⁵ log³g)` | `Omega-tilde(k^(1/5))` |

Theorem 4 另给三个问题的需求对数 `D_dem=O(Δ²)`。其中 RkC 的 `D_dem=|T|`，VC-SND 为正需求终端对数，VC-kRC 为给定对数。因此 `D_dem=O(g²log²g)`，Corollary 5 对充分大的 `D_dem` 给 `Omega-tilde(D_dem^(1/2))` 困难性。旧参数 `Δ=O-tilde(g²),Q=O-tilde(g⁴)` 则分别给 k 的 `1/10,1/6,1/6` 幂和需求对数的 `1/4` 幂。波浪符号仅省略对数因子，随机归约限定仍沿用。

这些是本文给出的外部应用合同。VC-SND 的“顶点/边/带权费用”版本必须回到被调用归约核实；本页保留冻结 PDF 的定义，不把它自动推广为任意费用模型。原文当时列出的 `O(klogk)`、`O(k³log|T|)` 和 `O(D_dem k)` 算法仅为历史背景，不声称是 2026 年最新上界。

## 7. 与仓内后续对象和文献的实际比较

### 7.1 partial-MinRep v2 的节省从何而来

本次完整读取冻结 canonical `782a8563344b6f317c3e`（33,322 字节）及审查 `7e6307ae7f378198a89b`（13,306 字节），并读取现有 v2 资料、陈述先行审查、v3 正文/后缀审查及 v4–v5 域修复页。完整源和归档页分别是实际比较对象，不能把其中“早期已阅读 primary”的声明当作本次新阅读证据。

| 对比项 | Manurangsi 本文 | 仓内 partial-MinRep v2 |
|---|---|---|
| NO 原单标签值 | `<γ` | `≤ρ³/(10⁹g⁸)` |
| 列表成本门槛 | `0.06N/√γ` | `gN` |
| 原图便宜列表覆盖界 | `<1/2` | `<τ=ρ/(100g²)` |
| 关键尾事件 | 未覆盖边数的常数偏差下尾 | 极稀覆盖边数的上尾，另共同控制总边数 |
| 最终 NO | 所有便宜列表不能覆盖全部边 | 所有便宜列表覆盖比例严格小于 ρ，且好输出非空 |
| 度数 | `O(logQ/√γ)` | `1000ceil(1000gλ/(ρ floor(log₂g)))`，`λ=1+ceil(log₂Q)` |
| YES | 近完美输入后补标签，概率至少 0.9 | perfect 输入对每个种子保 singleton 完备 |

若 `Q=poly_ρ(g)`，v2 的稀少上尾获得 `ln g` 因子，才有固定 ρ 下 `O_ρ(g)` degree。把本页 Lemma 7 直接代入 `γ≈g^-8` 只给 `O(g⁴logg)`，不能得到该线性阶结论。另一方面，v2 较粗的多项式字母表不自动改善第 6 节各连通性参数，更不构成全球新颖性证据。

v3 还需 arbitrary copy lists、真实 permutations 的相关上尾和有限同 type/layer 换边，才能得到固定 G 下 simple、exact regular、girth>G 的源。v5 以 `t_v=deg(v)z` 质量复制替代原正则性；它另有非空 typed 字母表、`Qγ≥1`、硬随机位及 FAIL 合同。它们的好 NO/非 FAIL 概率、每种子 YES 与“至少一个共同好事件”的量词均不能由本页纯删边自动继承。canonical 中的“非 FAIL 且全列表 sound”的无条件联合概率 `≥0.8`，也不能误说成条件于非 FAIL 后恰为同一概率；后缀审查另校正实际 permutations 数为 dN，而 2dN 是保守多计。

这些 source 尚无 ordinary UM 的实际编译器。条件费用式
`cost≤N+B/F`、`B≤cM` 只能在真实 compiler、全低负载 decoder、正确边身份和不重复计费另证后使用；`F≥cΔ/[2(g−1)]` 是充分代数式，不是已经实现的器件。坐标切片反例还说明，即便保 partial-MinRep NO 与严格单位阈值，也可能存在低负载逃逸。故本文不推出一般 UM 的 near-two hardness 或六人共同目录 SPE 结论。

### 7.2 Minzer–Zheng 后续：显示定理、参数缺口分开

本次复核 [ECCC TR24-027 Revision 1](https://eccc.weizmann.ac.il/report/2024/027/revision/1/download/) 的相关原文；仓内原件为 106 页、1,526,039 字节，SHA-256 `13b8eb55f86cfe28ac8b283fe83612889b335e14b7a87d64d479451693c7dff4`。其 Theorem 1.3 给任意固定 `η,τ>0`、足够大 R 的近完美 projection-game gap `val≥1−τ` 对 `val≤R^−(1−η)`。其 alphabet 定义为两侧大小之和，需统一字母表/正规化后再逐项接本页接口。

§7.4 的 Lemma 7.12 显式导入本篇 Lemma 7，同样写
`d=10⁶·2log(2R)/√γ`。Theorem 7.13 **显示的结论**是：任意固定 `ε′>0`、充分大 g，degree `O(glogg)`、alphabet `O(g^(2+ε′))` 的 MinRep 因子 g 困难性，仍为随机归约。它改善的是 alphabet 起点，没有显示 v2 的线性-degree 部分覆盖合同。

但印 61 页证明实际取 `δ=1/g`，同时以 `γ=2^-11g^-2` 得 `d=Θ(glogg)`，然后声称 YES `MinRep≤2N`。由其前一引理只得到
\[
\operatorname{MinRep}\le(1+\delta d)N
=\bigl(1+\Theta(\log g)\bigr)N,
\]
故显示的 `2N` **不能从该参数行推出**。这是本次新核到的承重缺口，现有仓内 comparison 只保存了显示定理，未指出此行。由于上游允许任意固定完备误差，先固定 g、R 后改取 `δ≤1/d` 可修复这一行。严格性也须重算：若已正规化的上游 NO 值 `≤γ₀=2^-11g^-2`，可以把稀疏化参数取为 `Γ=5γ₀/4`，令 `d=10⁶·2ln(2R)/√Γ` 并取 `δ≤1/d`；这样 NO 值严格小于 Γ，且 `0.03/√Γ>g`，仍足分离 `2N` 与 `2gN`。不得把原来的 δ 行当成正确证明。

此外，其 Lemma 7.12 的表述省掉了本篇 regular 假设，直接写任意 projection 2-CSP。原 heavy-incidence 证明实际用了 regularity；应用须显式经 biregular→balanced regular normalization 并把 N 取为正规化后规模，或另证不正规版本。不能用一个引用免费获得任意原图/原 N 的引理。

其下一段从 `d=O(glogg),R=O(g^(2+ε))` 代入 `d³R`，逐项上界为 `O(g^(5+ε)log³g)`，原印只留一个 log g。该显示式也不能按相同 ε 直接由给定参数推出；若仅要最终 `k^(1/5−ε)`、`k^(1/3−ε)` 这类有固定幂余量的结论，可预留更小 ε 吸收对数，但需重新安排参数。本页据此保留“可修复的应用参数问题”，不宣称推翻其 PCP 主定理，也不声称已完成整个应用链的外审。

## 8. 原讨论、对象关系与如何接续

原文 §4 提出三个当时的开放方向：MaxRep 的 alphabet-gap 交易与随机 `1/Q` 基线及 `Omega(logQ/Q)` 算法之间的差距；MinRep 是否存在只依赖 Q 的近似及 `(Q,Δ,g)` 三参数交易；以变量数 N 表达的多项式幂 hardness。原文并说明 Dinur–Manurangsi [DM18] 的一般 2-CSP `N^(1−o(1))` ETH-hardness 不能直接搬到投影约束。这些是历史问题陈述，不标成截至本日仍未解决。

本对象与 v2 资料页之间应记录“来源框架与明确改用尾界的比较”：共同前提为显式总投影和列表总成本；采样/一次高度 trimming 是来源，rare-covered 上尾和部分覆盖量词是不同的后续增量。与 v3/v5 是 source 框架比较，不是本篇自动推出高围长/typed 质量复制。与两篇 PCP 文献页是 alphabet-to-soundness 与 completeness 的条件接口；本页新增第 7.2 节的参数审查。这里只完成有证据的关系判断，不预造第三阶段全仓超边。

接续者可以直接使用第 3–5 节重建的有意义域内稀疏化，或沿第 7.1 节转到已归档 partial-MinRep source。若需连通性，应先核实际费用模型和所调用外部归约，再从 Δ、Q 重算 k；若需更小 alphabet，应修复第 7.2 节各参数接口；若需 UM，应给真实矩阵、YES 调度、所有弱负载调度的 decoder 和费用核算，不能用文献 hardness 代替这些义务。

原 PDF、完整抽取文本、逐页图像、源清单及本次实读/比较记录保存在 [证据目录](../../tools/evidence/Boss7-minrep-restored/README.md)。源 `533900faa02356c5f2df` 的独有内容已在本页自足整理；本次仅有本地文件，尚未由父 Boss 推送或登记 done，不把待提交回执冒称远端完成。
