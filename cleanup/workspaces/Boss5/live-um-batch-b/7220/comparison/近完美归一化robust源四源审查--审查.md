---
id: "unrelated-machines/near-perfect-normalized-robust-source-four-source-review"
kind: "review"
type_tag: "审查"
title: "近完美归一化 robust 源的两阈值判别与四源审查"
status: "proved-with-explicit-menu-scope"
truth_status: "deterministic-rational-promise-decider; no-hardness-reduction-supplied"
review_level: "four-full-sources-and-canonical-welfare-proof-read"
summary: "保留近完美 YES 的福利 LP 判别、两种高质量阈值、严格计数、等号角点及总位复杂度；区分 Exact-first、作者读后和 canonical 交叉核查的真实身份。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/near_perfect_normalized_robust_source_exact.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/near_perfect_normalized_robust_source_author_proof.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/near_perfect_normalized_robust_source_exact_first_attack.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/near_perfect_normalized_robust_source_read_after.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/normalized_gated_menu_welfare_and_robust_source_boundary.md#3"
evidence_manifest: "../../tools/evidence/Boss7-resumed-source-read/manifest.json"
---

# 来源与独有内容

四份冻结全文均已通过 clean show 实读，原字节及 SHA-256 保存在 evidence manifest。冻结来源同时存在于 main 的 aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c；同一路径字节相同。

| 源 ID | 文件尾名 | 独有内容 |
|---|---|---|
| 310bc8389c1a921052c0 | exact.md | 输入参数、两种分别成立的 promise、判别器与统一闭子域 |
| bf8b668075606e641178 | author_proof.md | 福利嵌入、舍入与 NO 严格计数相接的证明 |
| dd74a083ff48dcaf3d39 | exact_first_attack.md | 作者证明读取之前的重构、三重等号与退化参数攻击；审查者已知共同福利前提 |
| 6335192397b247d2f518 | read_after.md | 后读作者证明及 canonical 全文的交叉核查；明确不属于 canonical 盲审或独立代码审查 |

既有[归一化菜单福利与配置证书双源审查](归一化菜单福利与配置证书双源审查--审查.md)已记录该判别结论；[门控菜单 v2 三源审查](归一化门控菜单v2三源精读与13-8算法版本审查--审查.md)详述福利后端。本页补足四源身份、独立性边界以及完整近完美阈值证明，不另宣称一个新算法。

# 1. 精确输入域

有限非空组集 G，n=|G|≥1；有限资源 U；每组有显式有限非空 indexed states A_g。每 state 在互异原资源上给非负二进制有理系数 p_gsu，系数和恰为 1。未列系数在效用中取零；允许显式零、重复 state 与 unused 资源。归一化及非空菜单已排除 U 为空的合法实例。

每组获得真实资源子集 B_g，不同组的 bundles 两两不交，允许空 bundle 与剩余资源。其质量为

\[
r_g=v_g(B_g)=\max_{s\in A_g}\sum_{u\in B_g}p_{gsu}\in[0,1].
\]

没有额外 coherence、AND 或标签相容约束。参数为二进制有理数

\[
0\le\eta<1,\quad 0\le\delta<1,\quad 0<\gamma\le1,
\qquad
\frac58(1-\eta)\ge\gamma+(1-\gamma)\delta.                 \tag{E}
\]

YES：存在一个 allocation，使质量恰为 1 的组数至少 (1−η)n。

NO 分为两个独立合同：

* NO_≥：每个 allocation 都有 #{g:r_g≥δ}<γn；
* NO_>：每个 allocation 都有 #{g:r_g>δ}<γn。

不在两个高端阈值之间偷偷交换语义。非整计数直接与有理阈值比较，例如 h<γn 等价于 h≤ceil(γn)−1，不增加整除前提。

# 2. 总可行的福利 LP

每 state 设 z_gs≥0；仅每个正 incidence 设 x_gsu≥0。求

\[
\sum_s z_{gs}=1,\qquad x_{gsu}\le z_{gs},\qquad
\sum_{g,s}x_{gsu}\le1\quad(u\in U),
\qquad L=\max\sum_{g,s,u}p_{gsu}x_{gsu}.                 \tag{1}
\]

任取每组一个 state 并令全部 x=0 即可行。按组用 x≤z 及 norm1 得 L≤n。对任意真实 allocation，逐组选达到最大值的 state，将相应 z 置 1，并对该 state 真正收到的正资源将 x 置 1；其余为零。资源不交给容量约束，目标恰等于原福利。因此

\[
W^*\le L\le n.                                        \tag{2}
\]

这里不是 positive-support unit-FSLP。近完美 YES 不能保证所有组都可取得完整 support；以该 FSLP 的可行性代替 (1) 会改变命题。

# 3. 舍入前提的自足机制

给 (1) 的有理最优解，组间独立按 z 选 state。条件于 z_gs>0 的选中 state，对每个正 incidence 独立以 x_gsu/z_gs 提议资源。z=0 时由链接约束得 x=0，不作除法。每资源只给提议者中原系数最大的组，平局固定编号。

固定资源 u 和正水平 a，组 g 提议至少 a 的概率为

\[
q_{gu}(a)=\sum_{s:p_{gsu}\ge a}x_{gsu},\qquad
\sum_gq_{gu}(a)\le1.
\]

跨组独立给

\[
\Pr[\max_gX_{gu}\ge a]
=1-\prod_g(1-q_{gu}(a))
\ge(1-1/e)\sum_gq_{gu}(a).
\]

这是 1−e^(−t) 在 t∈[0,1] 的弦界。对每资源原正系数的有限 levels 求和，所得赢家加性质量期望至少 (1−1/e)L；最终按所得 bundle 重新取 attaining state 只会增加组质量。由于 e>1+1+1/2+1/6=8/3，在 L>0 时存在实际 allocation 满足

\[
W>\frac58L.                                           \tag{3}
\]

确定性化先逐组固定 state，再逐个固定选中 state 的 incidence coin。固定部分决定后，对每个资源的有序 levels 0=a_0<…<a_k，精确条件期望为

\[
\Phi=\sum_u\sum_{\ell=1}^{k_u}(a_\ell-a_{\ell-1})
  \left[1-\prod_g(1-Q_{gu}(a_\ell))\right].
\]

未固定组的 Q 是相应 x 之和；已固定 state、coin 未定时为 1[p≥a]x/z；coin 已定时为 1[p≥a]b。每次取不小于当前加权平均的可行分支，期望不降。条件化后 ΣQ 可能超过 1，此时只用精确乘积公式，不再使用初始容量弦界。

候选 state、coin、levels 的数量均由显式 incidence 数控制。LP 基本最优解有多项式位长，每次从原有理数重算有限乘积；其分母因子的数量与指数有多项式界，避免递推重复平方。因此这个有限显式福利实现是总位多项式的数学算法规格。本批未运行一个通用精确 LP 软件后端，也未新增有限实验。机制是原源明示的标准福利舍入特化，不认领外部方法新颖性。

# 4. 判别器与两个 NO 的分别证明

判别器只求 (1) 的精确 L：L≥(1−η)n 判 YES，否则判 NO；不需实际运行 (3) 的 finder。

YES 中 k 个 unit 组给 W*≥k≥(1−η)n，由 (2) 必接受。

对 NO_≥ 的任意 allocation 令 h=#{r_g≥δ}，高组质量≤1，低组质量<δ；对 NO_> 则令 h=#{r_g>δ}，低组质量≤δ。两版分别都有

\[
W\le h+(n-h)\delta
=\delta n+(1-\delta)h
<[\gamma+(1-\gamma)\delta]n.                            \tag{4}
\]

最后严格号来自 h<γn 与 δ<1，对所有非整阈值也成立。若 NO 被接受，则 L≥(1−η)n>0，(3) 与 (E) 给一个真实 allocation，

\[
W>\frac58L\ge\frac58(1-\eta)n
\ge[\gamma+(1-\gamma)\delta]n,
\]

与 (4) 矛盾。故两种 NO 都有 L<(1−η)n。E 允许等号，不能凭舍入常数的近似小数错误要求正 slack。

YES 和 NO 的互斥也可直接由 E 检查：γ≤(5/8)(1−η)<1−η，unit 组在 δ<1 时属于两版高组，故 YES 的见证已违反任一 NO。

# 5. 统一子域与端点

若 0<γ≤δ≤3/8、0≤η≤1/40，则

\[
\gamma+(1-\gamma)\delta
\le2\delta-\delta^2\le39/64,\qquad
\frac58(1-\eta)\ge\frac58\frac{39}{40}=39/64.
\]

所以全部子域满足 E，包括 η=1/40、γ=δ=3/8 三重等号。它不要求 n 被 8 或 40 整除。

δ=0 的 NO_≥ 是空类，因为所有 n 组质量≥0，不能有 n<γn；NO_> 则按其另一个实际合同读取。η=1、δ=1 都在域外，不能沿用严格正阈值和 (4)。γ=1 与 E 不相容，不造成未处理的合法输入。显式零不生成正 x，但这只是福利对象的变量选择，不能被误读成删去调度模型的物理任务。

# 6. 位复杂度、历史审查和接续边界

令 S 为 state 数、I_+ 为正 incidence 数、m=|U|。(1) 有 S+I_+ 个变量、n 个归一化等式、I_+ 个链接和 m 个容量约束。精确有理 LP 及与 (1−η)n 的比较按菜单和参数总位长多项式；不按 1/η、1/δ、1/γ 或分母数值枚举。

Exact-first 源明确：审查者之前参与一般福利 LP 证明，独立的是先于本次作者 Proof 的合同重构，不是对全部研究的盲审。read-after 源随后读作者 Proof，再读 whole SHA 为 3c0919735dbc90793fe99336e24f3b15d37b09bb8e7e9e138c71437e08acff01 的 canonical；本批实际读取该 canonical 的福利机制及判别段核对。该历史记录对其它章节的逐项核查保留为来源声明，不将其冒充本批对门控机器全部证明或代码的又一次独立审查。

若某 NP 完全语言确定性 Karp-reduces 到这里的完整 promise，复合判别器给 P=NP。这是条件后果，不表示本页提供该归约；随机归约的后果必须随真实成功合同说明。不归一化、隐式指数菜单、真实共享作业/coherence 或只量化完整 sets/固定 labels 的 NO 均在域外。一般 UM-TARGET-v1 和六人完整历史 SPE 的半覆盖命题没有由本对象解决。

第三阶段可建立“Exact→作者证明”“Exact-first→合同复核”“read-after→指定版本交叉核查”关系，并把共同福利机制作为实际前提；不能把三份接受记录计为三次独立代码认证，也不能由源边界制造一般困难性或其否定。
