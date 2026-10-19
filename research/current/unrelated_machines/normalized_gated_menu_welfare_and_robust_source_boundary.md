# 归一化门控菜单的真实值、加权福利舍入与近二源边界

读取目的：判断“四层私有标签、任意权资源束”能否承载近二困难性。本文给该完整普通矩阵类的确定性位多项式 **13/8 近似**，并给近完美 YES／少量部分高质量组 NO 的显式 LP 判别。它不覆盖一般 UM 或原 flat 的全组 selector；UM-TARGET-v1 及其反面保持 OPEN。

福利舍入机制归属 DNS 作者稿 §3.2 Theorem3.2/Lemma3.3：独立取配置、取 additive clause、把物品给最大系数组。原文甚至给有限组数的更强因子。本文不认领该算法、1−1/e 或条件期望新颖；新增用途为精确门控作业桥、任意权未知 OPT 的结构后果及 robust 比例纠错。原字节、实际定位与审查分别登记，非全球新颖性认证。

## 1. 对象、原任务与平衡值

组集 G 非空，n=|G|≥1；资源集 U 有限，m=|U|≥1。每组 g 有非空有限、显式 indexed states A_g。state s 列 distinct 资源集合 U_gs，系数 p_gsu 为二进制非负有理数，且每个 state 的系数总和**恰一**。允许显式零、unused 资源、重复 indexed states。未列项用于效用时作零，但不据此生成新任务。令 S=Σ_g|A_g|、I=Σ_g,s|U_gs|，I_+ 为正 incidence 数。

真实 allocation 是两两不交 B_g⊆U，允许空 bundle 和未分配资源。定义

\[
v_g(B)=\max_{s\in A_g}\sum_{u\in B\cap U_{gs}}p_{gsu}\in[0,1],
\quad W^*=\max_{(B_g)\text{不交}}\sum_gv_g(B_g),
\]
\[
\beta^*=\max\left(\{0\}\cup\left\{
\min\bigl(|H|/n,\min_{g\in H}v_g(B_g)\bigr):
\varnothing\ne H\subseteq G,\ (B_g)_{g\in H}\text{不交}\right\}\right).
\tag{1}
\]

这些 max 都在有限集合取到；算法不免费调用 W* 或 β* oracle。

构造 **P_gate**：根 R、每组 gate X_g、每 state private M_gs、每资源 Q_u，四类机器全部互异。全部且仅以下任务、端点存在：

| 不同原任务 | 有限端及处理时间 |
| --- | --- |
| J₀ | 仅 R：1 |
| 每组 connector C_g | R：1/n；X_g：1 |
| 每组 selector T_g | X_g 及该组全部 M_gs：各1 |
| 每列 incidence I_gsu | M_gs：p_gsu；Q_u：1 |

其余均 ∞；所有任务必须恰执行一次，无拒绝、抢占或额外约束。机器、任务、有限条目数依次为

\[
1+n+S+m,\quad1+2n+I,\quad1+3n+S+2I.
\tag{2}
\]

零 incidence 也有一件真实任务；未选 states 的任务不消失。稠密输入另列 ∞，规模仍多项式。

## 2. UM-NORMALIZED-GATED-MENU-VALUE-v1：精确双向实际值

**Exact Statement / Quantifiers。** 对第1节每份输入，无 LP 可行前提，

\[
\boxed{\operatorname{OPT}(P_{\rm gate})=2-\beta^*\in[1,2].}
\tag{3}
\]

给任何实际完整调度 C<2，可位多项式提取 |H|/n≥2−C 且每个选中原组质量≥2−C 的不交 bundles；给任何这样的 β≥0 见证，可位多项式排完全部任务，峰≤2−β。

**见证到全部任务。** 对非空 H，各取 attaining 原 state。选中组把 C_g 放 X_g、T_g 放选中 M_gs；未选组把 C_g 放 R、T_g 放 X_g。J₀ 留 R。仅将选中 state 在实际 B_g 中的正 incidence 导出 Q_u，其余全部留各自 private，包括全部未选 state 和零任务。根负载 2−|H|/n；每 gate 恰一 unit；选中 state 负载 2−v_g(B_g)；其他 private 负载一；资源因不交至多一 unit。因此全部机器共同≤2−β。β=0 另用 J₀ 与全部 C_g 在 R、所有 T_g 在 X_g、全部 incidence 私有的峰二基线。

**任意低调度到见证。** 令 H 为 C_g 实际执行在 X_g 的组。根真实负载恰 2−|H|/n≤C，故 |H|/n≥2−C>0。选中 gate 已有 connector unit，selector 不能同住，必须去本组选中 state；该 state 负载是二减实际外送原质量，因而导出质量≥2−C。每资源只接 unit incidence，C<2 迫全局至多一件；选中 states 的实际外送资源于是全部不交。额外未选态外送仅占更多资源，忽略它们不复用任何资源。C≥2 时不使用该独占断言，只用 β*≥0 即得相反下界。J₀ 单端 unit 给 OPT≥1，合成(3)。

**Scope / Dependencies。** 只有第1节完整矩阵、非负负载和 C<2 的 unit 独占；不保原 flat 的 OPT。每转换只扫描显式原任务并做有理求和，总位多项式。

## 3. 共同福利 LP 与标准舍入的显式有理实现

每 state 设 z_gs≥0，每正 incidence 设 x_gsu≥0，零 incidence 的 x 固定零而物理任务保留。求明确 LP

\[
\sum_s z_{gs}=1,\qquad 0\le x_{gsu}\le z_{gs},\qquad
\sum_{g,s}x_{gsu}\le1\ (u\in U),
\quad L=\max\sum_{g,s,u}p_{gsu}x_{gsu}.
\tag{4}
\]

有 S+I_+ 个变量；n 个归一化行、I_+ 个链接和 m 个资源行。任取 state、x=0 即可行。每组 norm1 给 L≤n。任一真实 allocation 逐组选 attaining state，并仅对其收到的正资源置 x=1，给可行点且目标等于真实福利，故

\[
W^*\le L\le n.
\tag{5}
\]

标准确定性有理 LP 算法给多项式位长最优解。这是数学算法规格；有限审计的浮点候选只有在 Fraction 原初／对偶证书同值时才采用，不认证浮点库为通用位多项式后端。

**概念随机分布。** 各组独立按 z 抽一个 state s；只对 z>0 的 state 定义 θ_gsu=x_gsu/z_gs。条件于该 state，各正 incidence 独立以 θ 提议资源。z=0 迫 x=0，绝不算 0/0。每资源给提议者中原系数最大的组，固定编号打平局；无提议则空置。

固定 u，组 g 提议的原系数随机变量记 X_gu，否则为零。不同组独立。对 t>0，q_g(t)=Pr[X_gu≥t]=Σ_(s:p_gsu≥t)x_gsu，故 Σ_g q_g(t)≤1。由

\[
1-\prod_g(1-q_g)\ge1-e^{-\sum_gq_g}
\ge(1-1/e)\sum_gq_g
\]

和有限 tail 求和，赢家总福利 A 满足

\[
\mathbb E A\ge(1-1/e)L>\tfrac58 L\quad(L>0).
\tag{6}
\]

最后严格号由 e>1+1+1/2+1/6=8/3；算法不比较无理常数。

**确定性化及位长。** 对每 u 排所有不同原正系数 0=a_u0<⋯<a_uk。给部分决定，写 Q_gu(a)=Pr[X_gu≥a|当前]。未固定组为 Σ_(s:p≥a)x；组已固定 state、coin 未定时为 1[p≥a]x/z；coin 已定 b 时为 1[p≥a]b。当前期望精确等于

\[
\Phi=\sum_u\sum_{l=1}^{k_u}(a_{ul}-a_{u,l-1})
\left[1-\prod_g(1-Q_{gu}(a_{ul}))\right].
\tag{7}
\]

先逐组测试所有 z>0 的原 states，选 Φ 最大者；当前 Φ 为候选的 z 加权平均。然后逐个已选 state 的 incidence coin，选 Φ 较大的0/1结果；θ 为0/1时只取可能分支。每步均不降。组间仍独立，组内共享 state 不影响对各资源期望求和。**条件化后 ΣQ 可能大于一；只有初始(6)用 Σq≤1，之后仅用精确公式(7)。**

最终逐资源定唯一赢家，输出真实不交 bundles；再在原表取 attaining state，W=Σv_g(B_g)≥A≥(1−1/e)L，L>0 时 W>5L/8。候选 state 次数≤S、coin 决策数≤I_+、全部 level 数≤I_+，无需枚举所有资源子集。

原 p、z、x、所有正 z 对应 x/z 的分母因子总数和总位数均多项式。每次(7)从这些原有理数直接重算，乘积跨至多 n 组，level 差另付一个因子；用这些输入分母的多项式次幂之积作公共分母，位长仍多项式。没有重复平方递推或按分母数值循环。精确排序、加乘和比较因此总位多项式。

## 4. UM-NORMALIZED-GATED-MENU-WELFARE-APPROX-v1：整个加权类的未知 OPT 保证

**Exact Statement。** 存在确定性总位多项式算法，对每个第1节 P_gate（不要求 unit-FSLP 可行），输出全部原任务合法分配 σ，满足

\[
\boxed{C_{\max}(\sigma)\le\tfrac{13}{8}\operatorname{OPT}(P_{\rm gate}).}
\tag{8}
\]

算法依次求(4)、执行(7)、将原质量 r_g 非增排序，扫描 n 个有理候选

\[
\widehat\beta=\max_{1\le k\le n}\min(k/n,r_{(k)}),
\tag{9}
\]

以达到 k 的前 k 组及同一 bundles 调用§2。算法不输入真实 OPT、β*、W*、源 YES 或好分配。

**证明。** 任意 allocation 令 b 为(9)。若 h=#{g:r_g>b} 有 h/n>b，则 k=h 的候选严格大于 b，矛盾。故 h≤bn，其他组≤b、高组≤1，得到 W≤n(2b−b²)，即 b≥1−√(1−W/n)。另一方面，最优 β* 见证有至少 nβ* 组、各质量至少 β*，所以 W*≥n(β*)²。结合(5)–(6)和完整任务桥，输出满足

\[
C\le1+\sqrt{1-\tfrac58(\beta^*)^2}.
\]

对 β∈[0,1]，D=(18−13β)/8≥5/8，而

\[
D^2-[1-\tfrac58\beta^2]
=\frac{209\beta^2-468\beta+260}{64}\ge\frac1{64}>0.
\tag{10}
\]

二次式导数 418β−468≤−50，最小在β=1。两端非负，可平方比较，给 C≤(13/8)(2−β*)，再用(3)。sqrt 只用于分析；算法仅用原有理数。(8)不声明锐性或新颖性。

**全部共同前提。** 完整 norm1 显式域、(3)双向原任务桥、(4)原初可行及 W*≤L、(6)标准福利不等式、(7)精确确定性化、(9)平衡提取与(10)有理比较，缺一不可。空任务／OPT0不属于本结构域，因为有根 pin；这不缩小 UM-TARGET-v1 的域。

## 5. UM-NORMALIZED-ROBUST-PARTIAL-SOURCE-LP-BARRIER-v1：高低比例纠错与源判别

所有量词仍在第1节的显式 normalized 菜单域，NO 必量化**每个真实不交 allocation**，不是只限制整束或某个标签。定义 h_≥(δ)=#{g:v_g(B_g)≥δ}。则

\[
h_{\ge}(\delta)<\gamma_{\rm hi}n
\iff\#\{g:v_g(B_g)<\delta\}>(1-\gamma_{\rm hi})n.
\tag{11}
\]

高端改 >δ 时低端须改 ≤δ。旧[NSW页§F](explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary.md)把此 γ_hi 与其低组下限 γ_lo 当成同一比例，误判“γ_hi≤δ 不在禁区”；这条解释撤回。原低组定理和其日志式本身保留，旧冻结来源／审查不改写，旧 PASS 没有抓出此错误。

**完整 YES 的 support-LP 判别。** unit-FSLP 是 λ≥0、逐组和一、每资源正 support 的 λ 总和≤1。令 z=λ、每正 incidence x=λ，(4)得 L=n。此时实际 W>5n/8。对 0≤δ<5/8，高组数（分别用 ≥δ 或 >δ）均严格大于

\[
f(\delta)n=\frac{5/8-\delta}{1-\delta}n.
\tag{12}
\]

因为 W≤δn+(1−δ)h。故固定／输入有理 γ_hi≤f(δ) 时，YES“全部组质量一”与 NO“所有 allocation 的高组数<γ_hi n”由显式 unit-FSLP 可行性分离。YES 的 attaining state 完整正 support 必全归本组，给 integral λ。δ=0、≥端的 NO 是空类，按该退化解释。

**近完美 YES 的一般福利-LP 判别。** 给二进制有理 0≤η<1、0≤δ<1、0<γ_hi≤1，满足

\[
\tfrac58(1-\eta)\ge\gamma_{\rm hi}+(1-\gamma_{\rm hi})\delta.
\tag{13}
\]

YES：至少 (1−η)n 组质量一；NO：每个 allocation 的 ≥δ 高组数<γ_hi n。分别将高端改 >δ 也成立。求(4)的精确最优值 L，以 L≥(1−η)n 判 YES，否则 NO。

YES 给 W*≥(1−η)n，故必接受。NO 下任何实际福利≤[γ_hi+(1−γ_hi)δ]n；若 LP 接受，(6) 给实际 W>(5/8)L≥右侧，矛盾。高端 >δ 的低组≤δ只需该非严格上界；≥δ同样成立。因此(13)的等号有效，LP本身始终可行，判别器不是把 infeasible 当一般调度 NO。

特别 0<γ_hi≤δ≤3/8、0≤η≤1/40 时，右侧≤39/64，左侧≥39/64，全部三重等号也被覆盖。阈值直接有理比较，无整除假设，不按参数倒数展开。此判别无需 unit-FSLP、NSW finder、完整 YES 或同组 repair；不是原 flat 的 minimum-quality finder。

若某 NP 完全语言确定性 Karp-reduces 到上述精确 promise，组合推出 P=NP；随机归约只按其真实成功事件得相应 NP⊆BPP 后果。本页不构造该归约、不无条件宣称其不存在，也不将固定ρ困难性当否定所有ε。

## 6. 有效否定范围、证据与研究前沿

整个 P_gate 类已有(8)，故其内部不能提供 YES≤a、NO>b 且 b>(13/8)a 的困难性归约（按实际复杂度假设理解）。(13)还直接排除一类 near-perfect normalized robust 源。原 flat 每组必须选 state，没有本文新 gate；两组各唯一 unit state 共用一资源时，flat OPT2，P_gate OPT3/2，不能冒称保原问题的 normal form。

共享内部机器、多层一致性、不归一化或隐式指数菜单、不同原任务资格，以及不满足 all-allocation partial NO 的真实困难源均未被排除。真正主反面仍缺每个固定ε的源可靠性、任意低负载完整输出的解码与固定参数多项式规模。正面特殊结构界在这里用于攻击具体困难性接口，不代替 UM-TARGET-v1。

**Evidence / Status / Related Files。** 自足证明完成；各冻结 Exact 先独立重构，再实际读完整作者 Proof，最终规范正文及代码的实际审查按[新审查记录](../../reviews/unrelated_machines/normalized_gated_menu_welfare_review.md)逐项登记。有限 Fraction 运行只核明确输入、原初／对偶证书、状态与非平凡 coins、所有原 jobs 和小例 OPT，不证明一般命题；无通用有理 LP 生产实现。外审、全球新颖性与独立成文价值未认证。冻结源、实际输入／输出和重放命令均由审查定位，不将未发生步骤提前记为通过。
