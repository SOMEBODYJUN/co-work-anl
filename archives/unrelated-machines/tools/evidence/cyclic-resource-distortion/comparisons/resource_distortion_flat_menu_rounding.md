# 逐资源正权畸变有界的完整菜单：实际次二界与反面源筛选

读取目的：反面归约若仍输出下面的完整 flat 矩阵，不能仅靠增加菜单数、资源重数或共同束宽得到趋二困难性。逐资源正权畸变有界时，已有 restricted Santa Claus 算法直接给实际次二调度。本文是标准取最小正值比较与已知算法的结构推论，不认领新近似技术或一般 `UM-TARGET-v1` 的突破。

## 1. 精确身份

**ID / version：`UM-RESOURCE-DISTORTION-FLAT-MENU-APPROX-v1`。**

**Objects / Domain / Definitions。** 非空有限组集 G；每组有非空显式 indexed states S_g。每个 x=(g,s) 有独占机器 M_x，每个资源 u 有机器 R_u，所有这些机器两两不同。每组恰一件 selector，只可在本组的 M_x 上耗时1。每个显式 incidence (x,u) 是一件不同的原 job，只可在 M_x 耗时 p_xu≥0 或在 R_u 耗时1；其余边为∞。同一 state 不重复列资源；允许零项、空 incidence 集、重复 indexed states 和 unused resources。所有未选 states 的原 jobs 都保留。无其它任务、资格、预载或约束。所有时间均为二进制有理数，且

\[
 W_x=\sum_u p_{xu}\le1,\quad b_x=1-W_x.
\]

对资源 u，令 P_u 是全部 states 在该资源上的**正** private 时间的多重集，定义

\[
 \kappa(P)=\max\left(\{1\}\cup
 \left\{\frac{\max P_u}{\min P_u}:P_u\ne\varnothing\right\}\right).
 \tag{1}
\]

零项不参与比值；unused/all-zero 资源不产生0/0。κ 可随输入增长，算法不按它的数值循环。

**Quantifiers / Exact Statement / Conclusion。** 对每个固定实常数 α>4，存在确定性总位多项式算法，对本域的每个 P 输出全部原 jobs 的合法具体分配 σ，满足

\[
 C_{\max}(\sigma)\le
 2-\frac{2-\mathrm{OPT}(P)}{\alpha\kappa(P)}
 \le\left(2-\frac1{\alpha\kappa(P)}\right)\mathrm{OPT}(P).
 \tag{2}
\]

程序不输入 OPT、最优见证、配置证书或 κ 上界。α 固定后的次数可以依赖 α；未声称输入 α 时的统一多项式次数。G 非空保证 OPT≥1；空组集不属于式(2)的中间不等式链，空任务可另行直接输出空分配。

**Dependencies / Paper Fact。** [既有 state-dummy 值桥](normalized_weighted_menu_santa_value_and_size.md)给 W=1 时的实际转换；下文独立补齐 W≤1 的 baseline。唯一外部算法为 Cheng–Mao，*Restricted Max-Min Allocation: Approximation and Integrality Gap*，arXiv:1905.06084v1，Theorem1（PDF/印页2）：任意固定 δ>0 的 restricted Santa Claus `(4+δ)` 实际分配算法，时间 `poly(m,n) n^{poly(1/δ)}`。该页定义为每物品有固有值、玩家价值仅为0或该值；定理后说明无需精确配置 oracle，可作目标搜索。[原文](https://arxiv.org/pdf/1905.06084v1)。本文使用此已发表算法合同，没有重证其整个增广结构。

**Status / Evidence / Scope。** 自足转换与外部定理适用条件如下；实际 statement-first 重构、作者读后与有限核验分开记录在[审查](../../reviews/unrelated_machines/resource_distortion_flat_menu_review.md)。完整后端未在仓库实现；精确审计仅检查小输入上的值比较和实际输出接口。外审、全球新颖性及独立论文价值未认证。一般 UM 的正反面均 OPEN。

## 2. 含 baseline 的实际值

对不交资源集合 B_g 定义

\[
 f_g(B)=\max_{x\in S_g}\left(b_x+\sum_{u\in B\cap S_x}p_{xu}\right),
 \qquad V=\max_{B_g\text{ 两两不交}}\min_g f_g(B_g).
 \tag{3}
\]

这里 S_x 指 state 的 incidence 资源集。非负性与 b_x+W_x=1 给0≤V≤1。V 不是 W<1 时旧的无 baseline 菜单值；例如全部 W=0 时本 V=1，而旧无 baseline 值为0。

给 B_g，选达到 f_g 的原 state 放 selector，只将其 B_g 内的 incidence 导出到原 R_u，所有其它原 incidence 留在各自 M_x。未选 private 负载≤1；资源至多一件 unit；选中 private 负载

\[
 1+W_x-\sum_{u\in B_g}p_{xu}=2-f_g(B_g).
\]

故有完整实际调度峰值≤2−V。反向，所有 jobs 留 private 给 OPT≤2，selector 给 OPT≥1。若某实际调度峰 C<2，取每个 selector 真实所在 state 及其实际导出的资源。unit 外端使这些资源跨组不交，选中 private 的同一个负载恒等式给 f_g≥2−C。因此 OPT≥2−V。若 OPT=2 而 V>0，正向构造会给峰<2，矛盾。于是包括 V=0 在内

\[
 \boxed{\mathrm{OPT}(P)=2-V.}\tag{4}
\]

没有在峰恰2时误用资源独占，也没有向外给出未知最优调度。

## 3. 一份显式 restricted Santa 实例

为每个 state x 建一个玩家。每个有正 P_u 的原资源仅建**一件** real item，固有值 q_u=min P_u；它只对 p_xu>0 的玩家有价值 q_u。每个 b_x>0 建一个只有玩家 x 感兴趣的私有 baseline item，固有值 b_x。每组另建 |S_g|−1 件不同 dummy，固有值1，仅本组玩家感兴趣。其它价值全0。

这是 ordinary additive restricted Santa，没有把同一资源按 incidence 复制。记其最优最小值为 V_−。给达到 V 的(3)见证，选中的玩家得对应 real items 和自己的 baseline，其余本组玩家各得一件 dummy。因

\[
 q_u\le p_{xu}\le\kappa q_u\quad(p_{xu}>0),\qquad\kappa\ge1,
\]

选中玩家效用至少

\[
 b_x+\sum q_u\ge\frac{b_x+\sum p_{xu}}\kappa\ge V/\kappa.
\]

其它玩家效用1≥V/κ。所以 V_−≥V/κ。任何实际 Santa 分配中，每组至少一名玩家没有自己的 dummy；其效用不超过 b_x+Σp_xu=1。按组选择这些玩家，real items 不交，且原 p≥q，亦得 V≥V_−。总之

\[
 \boxed{V/\kappa\le V_-\le V\le1.}\tag{5}
\]

V=0、b=0、全零资源均按同式处理，不假定每个 baseline 必被分配。

## 4. 从已知算法到全部原 jobs

先固定一个有理 a 满足4<a<α，调用 Cheng–Mao 的固定 `(4+δ)=a` 后端，得到实际物品分配，最小效用 t≥V_−/a≥V/(ακ)。每组找一名没有本组 dummy 的原 state 玩家，把 selector 放其 M_x；将该玩家收到且有正价值的 real items 对应原 incidence 导出，其余**全部**原 incidence 留 private。

选中 private 负载不超过2−t：即使该玩家没收到自己的 baseline，始终有 `t≤b_x+Σ收到的q_u≤b_x+Σ导出的p_xu`。其它 private≤1，资源≤1；t≤1，故同一2−t控制所有机器。这样得到式(2)第一段，没有删除零 jobs、未选 state jobs 或用辅助 item 代替原任务。实际 σ 是每个原 job 的一个有限机器编号。

令 c=1/(ακ)∈(0,1)，由 O=OPT≥1，

\[
 (2-c)O-[2-c(2-O)]=2(1-c)(O-1)\ge0,
\]

给式(2)第二段。κ 有界时是结构类统一常数改善；κ 无界时不承诺任何统一 ε。

## 5. 位复杂度与文献版本

设显式 state 数为 S、incidence 数为 I、资源数为 U。辅助实例至多 S 玩家、U+2S 件物品；dummy 正值表大小至多 Σ_g|S_g|²。q 的选择、b 的精确求和及实际解码都为总位多项式；大有理分母只增加整数运算位数，不复制其数值份数。κ 只用于分析，不进入循环。

外部后端提供实际 allocation，不能换成纯配置 gap 或估值。其算法使用有理值加和、比较、组合增广与网络流，任意选择可固定输入顺序。固定内部参数取有理数；所有新权值仅为输入值的加和/固定常数倍。有理清分母的公共乘积位长至多输入分母总位长。§4直接导入定理1的**完整 a 近似算法合同**，其未知目标处理已包含在合同中，不再额外损失一个搜索因子。若自行改用几何网格，须先取内部后端常数 a₀<a，再选网格比 g>1 满足 a₀g≤a，不能仍把未付费的 t≥V_−/a 原样保留。

也可不损失因子地使用有界整数目标搜索：清分母后真实 Santa 最优值是整数，全部 item 值之和 U 是上界。目标 t 的组合算法用固定参数多项式时钟截断并验证实际输出；真实最优值≥t 时保证成功，成功则给真实效用≥t/a，失败推出最优值<t。置 lo=0、hi=U+1，成功更新 lo 并保存分配，失败更新 hi，始终有 hi>真实最优值。结束时整数 lo=hi−1≥真实最优值，所以保存的分配足够；不要求成功标签单调。目标0先用任意分配，调用数 O(log(U+1))、目标和中间权值位长均多项式。完整接口及实际核读范围见审查，未把精确配置 LP 当免费 oracle。没有按分母值、κ值或精确配置列数枚举。

Davies–Rothvoss–Zhang arXiv:1807.07189v4（2026-01-04）Theorem3 的当前常数为6+η；其§4明确更正旧4+η分析。它可独立支撑弱版 α>6。本文 α>4 取自**另一篇** Cheng–Mao 定理1，不沿用被撤回的旧版本常数，也不把一般 Santa 与 restricted Santa 混同。

## 6. 对反面源的准确限制

固定 κ₀≥1。若一个确定性多项式归约的所有输出均在本域、κ(P)≤κ₀，YES 输出实际 OPT≤1，NO 输出实际 OPT≥2−ε，且 ε<1/(ακ₀)，则取固定有理 separator θ 满足 `2−1/(ακ₀)<θ<2−ε`，运行本算法并检查实际峰是否≤θ即可判源：YES 一定通过，NO 没有任何这样的调度。θ 可硬编码，不对可能非有理的 α、κ₀ 作精确实数比较。因此在 P≠NP 下，这个像类不能承载这样的 NP-hard promise。

若要对此 flat 编译覆盖任意固定 ε→0 的源族，κ 不能保持统一有界，或必须退出本文其它承重条件。不能倒推任一标准源不难，也不能倒推一般 UM 有统一 ε。共同 uniform 束是 κ=1 的特例；任意复杂 eligibility、菜单数及资源度都不改变此判断。W<1 已被 baseline 覆盖，单纯重新分配各 state 的总质量也不逃离定理。

该必要条件不是充分条件：让κ增长并未自动创造 NO gap。共同非单位内部容量、跨原job物理一致性和所有低载实际分配的 source decoder 仍需另证。已有[unit parking 的 uniform 束算法](uniform_port_parking_matroid_gap_and_actual_approximation.md)在重叠子域可更强；本文增加的是任意资源固有权与有限正畸变的接口，不扩大旧 Claim 身份。

## 7. 可复现实验与未检查范围

[主审计](../../../tests/audits/unrelated_machines/resource_distortion_flat_menu.py)用 Fraction 枚举小完整矩阵的全部原job分配、资源 ownership 和 state-dummy 实际物品分配；[冻结输出](../../../evidence/runs/unrelated_machines/resource_distortion_flat_menu_audit.json)记录参数、seed、代码hash和范围。它没有实现 Cheng–Mao 后端，也不测试一般矩阵或证明一般复杂度下界。独立程序与其实际范围沿[审查](../../reviews/unrelated_machines/resource_distortion_flat_menu_review.md)读取。有限数据仅核公式与转换，不是式(2)的一般证明。
