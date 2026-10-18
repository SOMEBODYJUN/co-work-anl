# q元 affine 菜单：线性 recoupling 与坐标一致性的精确差异

ID: UM-QARY-AFFINE-MENU-RECOUPLING-CONSISTENCY-v1。
作者 boss11 内部 typed_edge_gap，2026-10-18。Exact-first，未在本页附作者证明；仅 scratch。二元无约束tensor原Claim及审查另存，不在这里重复登记。

## 1. 完整对象及 ordinary P

q≥2 为 prime power，F_q 使用给定的标准有限域显式表示，基本域运算可按其表示位多项式执行。整数t≥1。groups 是全部 g∈F_q^t；resources 是全部(a,b)∈F_q^t×F_q^t；每group有全部 indexed states ℓ∈F_q^t。

state(g,ℓ) 支持精确为

S_(g,ℓ)={(a,b): b_i+g_i a_i=ℓ_i 对 i=1,...,t}。

它恰有q^t项，每项非负有理private权q^(−t)，总质量1。这里的加法/乘法是域运算，private时间则是普通有理数q^(−t)。

全部普通UM矩阵：每resource一台R_(a,b)，每indexed state一台M_(g,ℓ)；每group恰一件selector J_g，在自己所有state private机上时间1。每state中每resource各一件不同incidence job，仅可在自身M时间q^(−t)或其唯一R上时间1；其余∞。没有其它资格、预载或免费约束。全部未选states的jobs也在P内、必须执行。

对任意完整选择函数 ℓ:F_q^t→F_q^t，定义

V(ℓ)=max_(B_g⊆S_(g,ℓ(g)), B_g两两不交) min_g |B_g|/q^t。

partial子集的选择始终是完全自由的全局资源分配，不要求它们本身按坐标分解。

## 2. 三种 selector 选择域

cyclic函数固定为 ℓ_i(g)=g_(i+1)，下标t+1按1循环，记其值V_cyc。

affine域允许 ℓ(g)=Ag+c，A∈F_q^(t×t)、c∈F_q^t 任意。V_aff 是该域内V(ℓ)的最大值。

coordinatewise域允许分别取任意函数f_i:F_q→F_q，要求 ℓ_i(g)=f_i(g_i) 对全部g和i成立。f_i 可不线性，可因坐标i而不同，但不准看其它g_j。V_sep 是该域内V(ℓ)的最大值。

这些域是供分析的全局 selector-position 条件，**普通P本身没有附带这些条件**。不声称可用免费一致性约束把普通P修改为这些受限问题。

## 3. 待独立攻击的 Exact Statements

(A) 对全部上述q,t，有

V_cyc=V_aff=1−ceil((q−1)^t/q)/q^t。

特别cyclic函数不只给一个去除全部奇异a的下界；Claim允许对奇异a所对应的resources作最优任意partial领取，并断言其精确最优。affine上界需涵盖全部A,c，不预设A的形状或rank。

本式未声称q>2时能上界全部nonlinear函数ℓ；q>2的无约束最优另为OPEN。q2时它退化为已知无约束值1−2^(−t)。

(B) coordinatewise一致域的精确值为

V_sep=floor((q−1+1/q)^t)/q^t。

此处先对任意coordinatewise selector函数取最优，再允许任意全局partial资源分配。不是只分析B_g也必须product的较弱受限模型。floor作用于普通有理数(q−1+1/q)^t。

(C) 上述每个受限selector域的最佳**全部jobs实际makespan**恰为2减其相应V；特别存在完整cyclic-selector实际调度，峰

C_cyc=1+ceil((q−1)^t/q)/q^t；

任意coordinatewise-selector完整实际调度，峰至少

C_sep=2−floor((q−1+1/q)^t)/q^t，

且存在同域完整调度达到此值。必须覆盖任意未选state exports，不能先把资源partial方案当作已完成全部jobs。

(D) 每个固定q≥2，t→∞ 时 V_cyc→1 而 V_sep→0。因此不存在常数c>0，使每个t的cyclic高值partial分配（或任意普通P高值分配）总能被改成coordinatewise-selector一致分配并保留至少c倍其最小导出质量。该不可能性不依赖计算效率；输出域根本没有足够高值分配。

这仅排除这种特定“事后修复到coordinatewise函数”的常数保值合同。它不排除其它形式的一致性、译码器直接处理nonlinear state recoupling、或具有额外physical结构的compiler image。

## 4. 大小、表示与证据域

groups q^t；indexed states/private机器q^(2t)；resource机器q^(2t)；incidence jobs q^(3t)；selectors q^t。sparse finite时间条目2q^(3t)+q^(2t)，机器共2q^(2t)，jobs共q^(3t)+q^t。所有private时间均为同一binary rational q^(−t)，位长O(t log q)。

Exact中构造及达到(C)的见证算法按完整显式实例总位长polynomial；不是poly(t,log q)大小或运行时间声明。可使用标准整数matching/flow恢复真正的资源选择，但所有选择只针对显式resources/incidences；没有按更大未显式数值复制。若给dense P，按对应完整矩阵条目数计费。

本页不提供YES1/NO任意tiny的复杂性源。cyclic/all-affine与coordinatewise之间的巨大差异只量化一种真实state-copy一致性义务；既有线性代数、有限网格计数、整数matching不主张原创。
