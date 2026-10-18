# 资源仅连两组的加权菜单：共同分配与真实OPT的次二界

读取目的：检验加权coordinate-slice或其它显式菜单能否绕过uniform Hall障碍。这里**共同选择重任务状态与分散小任务的资源**，不给未知最优见证，也不把各state拆成必须分别满足的玩家。结论是一个限定结构类的实际近似算法，由既有MaxMin-balancing定理与下述自足转换直接导出；不是一般UM-TARGET-v1的突破。

## 1. 精确输入与陈述

**ID / Version：`UM-DEGREE-TWO-BOUNDED-MENU-JOINT-ROUNDING-v2`。** v1只给strict-unit promise界，v2另加相对真实OPT、非归一化精确保OPT及下述附带边界。原冻结来源保留，不改v1量词。

**Objects / Domain / Definitions / Quantifiers。** 有限非空组集G；每组g有非空**显式列出**的indexed states A_g，K_g=|A_g|、K=max K_g≥1。每state有显式资源集S_gs，组内同一resource可以出现在多个states，但每个resource跨全部states合计只属于至多两个不同groups。资源标识与private state机器标识不交。每incidence给二进制非负有理p_gsu，W_gs=Σ_u p_gsu≤1；资源集可空、private时间可零、indexed states可重复。

完整原UM矩阵只有以下原jobs与有限端，其余为∞：

| 原对象 | 原合法时间与端 |
| --- | --- |
| 每group一件selector J_g | 自己各state机器M_gs，时间均1 |
| 每(g,s,u)一件独立incidence job I_gsu | M_gs耗时p_gsu，R_u耗时1 |

无其它jobs、预载、拒绝、额外side constraints或共享private机器。全部机器、资源、menus、incidences和时间均显式；结构标签是算法输入的一部分，不声称能将一般P免费分解为该形式。

**Exact Statement / Conclusion。** 对所有此类完整输入，有确定性总位多项式算法输出全部原jobs的合法具体σ，且

\[
 C_{\max}(\sigma)\le 2-\frac{2-\mathrm{OPT}(P)}{2K}
 \le\left(2-\frac1{2K}\right)\mathrm{OPT}(P). \tag{1}
\]

不输入OPT、原最优调度、YES witness或state分布。K可随输入增长，算法仍位多项式；固定K时才有本结构类的统一常数改善。不声明该因子锐，不声明覆盖一般UM。G非空的selectors保证OPT≥1，因此本ID没有非空任务OPT0或n0实例；若接口扩展到空G，可单独输出空调度并保留一台idle机，不使用后面的min_g。

**Dependencies / Imported Paper Fact。** 唯一外部近似算法是Verschae–Wiese arXiv:1011.4957v1 §5.1、Theorem12（PDF10–11 / 印9–10）：非负加性MaxMin-balancing、每item至多两个可用玩家、两端价值可不同，有确定性2近似，按二进制输入位长多项式。primary实际读取范围/条件在§5及审查中记录。它不是本文新算法成果，也不使用该论文的makespan CONFIG-gap定理。

## 2. 归一化菜单的精确实际UM/XOS恒等式

先设每state W_gs=1。令

\[
 a_{gs}(B)=\sum_{u\in B\cap S_{gs}}p_{gsu},\quad
 f_g(B)=\max_{s\in A_g}a_{gs}(B),\quad
 V=\max_{B_g\ \text{pairwise disjoint}}\min_g f_g(B_g).
\]

这里XOS仅指显式非负加性clauses的最大值。所有集合有限，0≤V≤1，最优分配达到。实际恒等式为

\[
 \mathrm{OPT}(P)=2-V. \tag{2}
\]

**分配到全部原jobs。** 给任意不交B_g，选一个达到f_g(B_g)的state s(g)，将其selector置该private根；仅将该state在B_g内的incidence jobs导出相应R_u，其它所有incidence jobs一律停在自己的原private根。每resource至多一枚unit，每未选state负载1，每选state负载2−f_g(B_g)。全部原jobs保留且各一次，故实际峰≤2−min_g f_g(B_g)，给OPT≤2−V。

**调度到不交分配。** 所有selector时间1给OPT≥1；全private基线给OPT≤2。若实际最优C<2，则每resource至多一枚unit。每组selector选一个原state；其它未选state的jobs可全部收回自己根，根总负载1≤C且只减资源负载。令B_g为所选state实际导出的资源，跨组不交。选根负载2−a_gs(B_g)≤C，所以f_g(B_g)≥2−C，V≥2−C，得到OPT≥2−V。若OPT=2，不可在2上假设资源独占；但V>0已会从上一段构造<2的实际调度，矛盾，故V=0，式(2)仍成立。零private jobs可留根且工作为零，身份不会被删。

## 3. 一次group平均后的共同资源分配

定义**每组一名**辅助加性玩家

\[
 v_g(u)=\frac1{K_g}\sum_{s\in A_g:u\in S_{gs}}p_{gsu}.
\]

对每个集合B，由所有p非负，

\[
 \frac{f_g(B)}K\le\frac{f_g(B)}{K_g}
 \le v_g(B)\le f_g(B). \tag{3}
\]

设辅助加性MaxMin最优值为A。将达到V的同一不交B_g代入(3)，得A≥V/K。每resource只对至多两个辅助**groups**有正价值，即使在其中许多states出现亦不增加玩家数。因此可以直接用上述已知2近似，输出共同不交C_g，使所有v_g(C_g)≥A/2≥V/(2K)。零价值item/边可省去，单玩家item允许；A0时任意合法的零最小值分配都满足保证。

然后每组只扫描菜单选一个最大化a_gs(C_g)的原state。式(3)给其实际可导出private质量≥V/(2K)。按§2恢复所有原jobs，得到实际峰≤2−V/(2K)，结合(2)就是式(1)第一项。它不是先选heavy matching、再将剩余资源交给另一独立light算法；重状态与分散状态都由同一辅助分配后选择。

## 4. W≤1的精确保OPT归一化与相对比

对每个W_gs<1的state，只增一个独占新resource z_gs及一枚bonus incidence job：其private端为1−W_gs，独占resource端为1。令N(P)为增广矩阵。每state总private量变1，新resource仅属一个组，不改变旧跨组次数。

任意N(P)调度删bonus及其独占机器，投影为原P调度，故OPT(P)≤OPT(N(P))。反过来，任意原P调度峰C≥1可保持全部原job，并把**每个state**（含未选state）的全部bonus分别导出其独占新resource，新机负载1≤C、旧负载不变。因此

\[
 \mathrm{OPT}(N(P))=\mathrm{OPT}(P). \tag{4}
\]

增广后跑§3，再删bonus，输出恰全部原job，仍有式(1)第一项。令O=OPT(P)≥1、R=2−1/(2K)，直接计算

\[
 RO-\left[2-\frac{2-O}{2K}\right]
 =(2-1/K)(O-1)\ge0,
\]

给式(1)第二项。W0、空state资源集和零private jobs均由同一bonus规则处理；没有分母值展开或隐式job复制。

## 5. 外部定理、位复杂度及准确扣除

primary原件为[已存VW2010v1](../../../history/source/literature/unrelated_machines/verschae_wiese_2010_configuration_lp_v1.pdf)，SHA256 `2a5ec312fb443928b3801af830006b41ef94f4da7f9759bdab22b16a59a88a7a`。root实际读§5.1定义、preassignment、Lemma11、Theorem12及proof，独立审查者亦核原文及PDF10–11图像；未声称重构其technical-report精确二次实现。原算法对每个正整数阈值T，失败证明加性OPT<T，成功只保证输出效用≥T/2，不能把成功当精确T可行。

辅助有理值由显式加和与除K_g形成；若用整数后端，可用全部分母之积清分母，其**位长**至多各分母位长总和，缩放后的数值虽可大，但只按位长运算，不复制数值份数。阈值后端二分按失败的单向证书维护上界并保存成功分配，最后给因子2；不需把接受条件冒称精确feasibility或假设它单调。bonus每state至多一job/机器，全部中间表示与原job输出位长多项式。正utility项至多两个group，符合原定理的全部结构条件；零utility不虚增degree。

扣除已有定理后，本文增量是group平均保住one-state耦合、式(2)的真实UM/XOS转换、式(4)的保OPT归一化与完整原job还原。是直接结构推论，不是新Santa Claus算法；全球新颖性或独立论文价值未认证。

## 6. source界限与已有结果的关系

固定K可据实际输出判promise YES OPT≤1、NO OPT>R：若输出峰≤R回YES，否则NO。YES必得到该阈值，NO不可能有该实际调度；中间情况任意。不能把(1)误读为所有输入都有绝对峰≤R。

在带变量tag的[d]^Q坐标切片中，resource (x,z)能出现的group，其单射incidence index j_x(g)必须等于某个坐标值z_ℓ。因此一个resource跨全部states最多连min(d,Q)个groups。Q2满足本域；K≤7给R≤27/14。这覆盖任意cell private权，包含heavy/diffuse共同选择。已有[uniform cube界](coordinate_slice_source_compilation_counterexample.md)全类绝对≤3/2、DGR特例19/15，在其较窄域仍更强；不改旧Claim。

另有独立的精确unit-threshold边界：若每菜单≤2states，OPT≤1 iff可每组选一个state、其**正private权**support跨组不交。必要性是selector已占private1，正任务全须导出，resource单位容量；充分性按§2原job还原，未选state≤1、选中零项可留根。为每组布尔选态，对每对跨组冲突state加一条禁止二者同时选择的2CNF即可精确判定；不需要degree2。此法只判unit阈值，不求一般OPT，也不是(1)的证明。

**Scope / Limitations。** 算法需要跨组degree≤2、恰unit resource端、显式有界K才能取统一ε；不能由degree3或state-agent degree2K免费导入同一后端。K增长时改善可趋0，不覆盖一般UM的unknown角色选择、medium共居和任意深树；未解主目标存在或反面。

**Evidence / Counterevidence / Status / Related Files。** 当前自足转换证明完整；Exact-first独立重构及作者读后/最终稿实际范围见[审查](../../reviews/unrelated_machines/degree_two_group_bounded_menu_joint_rounding_review.md)。外部Paper Fact与新推导分层，外审、新颖性未认证。软件状态及有限审计另行登记，不能由数学可构造性推定实现完成；有限用例不代全量词证明。主目标`UM-TARGET-v1`仍OPEN。
