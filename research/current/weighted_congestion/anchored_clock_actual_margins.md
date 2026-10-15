# 锚定双轮时钟的有向差分、线性预算与逐次数锐效率

## 精确身份与研究层级

**ID/version。** `WC-ANCHORED-ACTUAL-MARGIN-INTERFACE-v1`。

**对象、定义域、量词和范围。** 对每个整数 n≥3、每组正实玩家权 w_0,...,w_{n−1}、每个 α≥1，考虑每玩家恰有两个动作、满足 MODEL 真实负载规则的任意基体游戏 G。假设从全 0 起按 0,...,n−1 翻至 1，再同序翻回的 2n 条边均严格 α 改善。对于每个 1≤i<j≤n−1，允许加入一对互补时钟资源，费用同为任意非负系数多项式 c_ij（可为零，次数可不相同）。玩家 (0,i,j) 的目标模式为 (0,1,0)：玩家 k 使用编号 s_k xor p_k 的资源。时钟不改变玩家权、两个旧动作或旧资源。

**结论。** 下文给出所有合法半轮 margin 的精确公式、任意非法状态指定偏离的精确分解、O(n²) 条全状态充分不等式，以及保留整个合法环的必要总成本预算。固定次数下，每个三元的增益/预算效率有精确有限列最大值；一般不能只取最高次数。另给有序权重下 anchor 这一条边的必要预算及其真实次数效率估计。

**依赖。** 只依直接资源用户集、非负系数与有限和；不引用外部定理。它加强了已存 `anchored_cycle_lock.md` 的数值接口，不改变其全状态编译结论。所有次数效率只限制明示 clock 架构或指定偏离选择器，不是全类存在性上界或次数下界。唯一全类 C d/ln d 判定仍开放。

**证据/反驳/状态。** 作者先独立重构，向 boss 报告公式后才读既有两份正文；独立 Fraction 审计从资源 literal 实现计算全部状态后检验恒等式。已完成先独立重构后冻结攻击；无尚成立的致命反驳。Status：complete stated-scope interface proof; independently reconstructed and exactly audited; unrefereed。Truth为所述条件接口；Value为真实差分、预算及有限证书；Mechanism为逐三元真实负载和非负列凸组合；Ambition保留全类目标OPEN。无外部评审或新颖性认证。

## 一、记号与合法半轮的真实有向差

写 a=w_0。在三元 (0,i,j) 中简写 b=w_i,c=w_j，且 c_ij 的函数名不会与权重 c 混淆。将 anchor 的当前动作通过全体互补归为 0。四种局部模式、两个用户群为

| (s_i,s_j) | 使用资源的两群 |
| --- | --- |
| (0,0) | {0,j} 与 {i} |
| (0,1) | {0} 与 {i,j} |
| (1,0) | {0,i,j} 与空集 |
| (1,1) | {0,i} 与 {j} |

全体互补只交换一对资源编号，因此时钟各玩家成本和翻位 margin 不变。

对玩家 0 取全 0 状态翻位；对玩家 i≥1，取状态 L_i=(0^i,1^{n−i})，即第 i 位是首个 1，翻 i 从 1 为 0。它及其全体互补恰对应双轮环中该玩家的两条边；玩家 0 的两条边是全 0 / 全 1 的翻位。记时钟在该边的 α margin 为 g_i，即旧成本减 α 倍真实偏离后成本。逐群读得

\[
g_0=\sum_{1\le i<j\le n-1}
 [c_{ij}(a+w_j)-\alpha c_{ij}(a+w_i)], \tag{1}
\]

\[
g_i=\sum_{j>i}[c_{ij}(a+w_i)-\alpha c_{ij}(w_i+w_j)]
+\sum_{1\le k<i}[c_{ki}(w_k+w_i)-\alpha c_{ki}(a+w_i)]\quad(i\ge1). \tag{2}
\]

公式包括当前、偏离后都仍使用的资源，不是只计算切换资源的费用。

## 二、非法状态与 first opposite 的精确分解

合法状态是动作序列至多一次变化的状态，恰有 2n 个。对任意非法 s，先互补使 s_0=0；令 i=min{k≥1:s_k=1}。必有 j>i 满足 s_j=0。令

\[
J(s)=\{j>i:s_j=0\}\ne\varnothing.
\]

指定玩家 i 翻回 0。设 h_i^H(s)=C_i^H(s)−α C_i^H(s^{xor i}) 是时钟 H 的 margin，则

\[
h_i^H(s)=g_i+\sum_{j\in J(s)}\Delta_{ij}, \tag{3}
\]

其中

\[
\Delta_{ij}=c_{ij}(a+w_i+w_j)-c_{ij}(a+w_i)
+\alpha[c_{ij}(w_i+w_j)-c_{ij}(w_i)]\ge0. \tag{4}
\]

证明：i 作为三元的末位时，所有更早 k 均与 anchor 相同，当前/偏离用户群与合法边相同。i 作为中位且 s_j=1 时也与合法边相同；s_j=0 时当前全员共用、翻位后 i 独用，margin 为 c_ij(a+w_i+w_j)−αc_ij(w_i)，减去式 (2) 对应项即为 (4)。非负系数保证费用单调，故 Δ≥0。零多项式或常数多项式给 Δ=0，不能提供缺陷增益。

n=3 时有两个非法状态 010、101，式 (3) 只有 Δ_12；n=2 才没有非法状态而无需本时钟。n≥3 不需要同权或有理性。

## 三、O(n²) 个充分约束及次数固定后的 LP

令 γ_i>0 为 G 中玩家 i 的两条合法环边 α margin 的较小者。取任意统一界 B≥max_{s,k}C_k^G(s)。严格环保证 B>0。以下有限条件充分保证 G+H 无 α-PNE：

\[
\gamma_i+g_i>0\qquad(0\le i<n), \tag{5}
\]

\[
g_i+\Delta_{ij}>\alpha B\qquad(1\le i<j\le n-1). \tag{6}
\]

合法状态由 (5) 保留环出口。非法状态用 (3)、Δ≥0 和 J 非空，时钟 margin 大于 αB；原游戏 margin 至少 −αB，因此总 margin 严格为正。这样穷尽全部状态，未从一个改善循环推出非存在。

(5) 对保留原环两半的所有严格边也是必要条件；(6) 只是充分条件，可能很保守。若已知玩家界 B_i≥max_s C_i^G(s)，可将其右侧换 αB_i。若已知该 i 类非法状态原 margin 的统一下界 m_i，可将右侧换 −m_i，仍充分。

固定 D≥0，写 c_ij(x)=Σ_{k=0}^D λ_ijk x^k，λ_ijk≥0。g_i、Δ_ij 均为 λ 的线性函数；(5)(6) 只需 n+binom(n−1,2) 个严格线性约束，变量为 binom(n−1,2)(D+1) 个。可用共同正余量 ε>0 把严格不等式改写为有限非严格 LP，并最大化 ε。系数为有理数且严格可行时存在有理可行点；这不保证任何给定 D 可行。计算 B 或 m_i 本身不由这个 O(n²) 约束计数保证多项式时间。

## 四、保留合法环的必要总预算

记

\[
S_{ij}=c_{ij}(a+w_i)+c_{ij}(a+w_j)+c_{ij}(w_i+w_j)\ge0.
\]

把同一三元对 g_0,g_i,g_j 的三项相加得精确恒等式

\[
\sum_{i=0}^{n-1}g_i=-(\alpha-1)\sum_{i<j}S_{ij}. \tag{7}
\]

因此保留全部严格合法边必要有

\[
(\alpha-1)\sum_{i<j}S_{ij}<\sum_i\gamma_i. \tag{8}
\]

α>1 时，这是对所有时钟合法负载费用的必要总预算，不依 uniform δ、统一幅度、同次数或实际状态数。它只是必要条件；逐玩家预算还可能更严格。α=1 时式 (7) 为 Σg_i=0，式 (8) 仅为 0<Σγ_i，不能除以 α−1 或声称获得成本上界。

## 五、逐三元的锐次数效率；最高次数不总是最优

对固定正权 (a,b,c)、α≥1、D≥0，定义

\[
S_k=(a+b)^k+(a+c)^k+(b+c)^k>0,
\]

\[
\Delta_k=(a+b+c)^k-(a+b)^k+\alpha[(b+c)^k-b^k],
\quad R_D(a,b,c;\alpha)=\max_{0\le k\le D}\frac{\Delta_k}{S_k}. \tag{9}
\]

则对任意非负系数次数≤D的费用 f，

\[
\Delta(f)\le R_D S(f). \tag{10}
\]

非零 f 时比值 Δ(f)/S(f) 是各 Δ_k/S_k 以 λ_k S_k 为非负权的凸组合，故 (10) 锐：取达到最大值的单项式即可。零费用给 0≤0。常数 k=0 给 Δ_0=0；D=0 时 R_D=0。

**不能把 max 简化为 k=D。** 取 (a,b,c)=(10,1,1)、α=2，直接 Fraction 计算得到 R_0列=0、R_1列=1/8、R_2列=29/246<1/8。因此 degree≤2 的锐效率由一次项取得。

结合 (8)(10)，α>1 时保留严格环的每个时钟满足

\[
\sum_{i<j}\Delta_{ij}
\le\bigl(\max_{i<j}R_D(w_0,w_i,w_j;\alpha)\bigr)\sum_{i<j}S_{ij}
\le\frac{\max R_D}{\alpha-1}\sum_i\gamma_i. \tag{11}
\]

D≥1 时 max R_D>0，式 (11) 的最后一个不等号可加强为严格；D=0 时两边为零。这给可核验的实际增益预算，但尚不能由它推出全状态锁定不可能：真正原游戏的非法态 margin 与所需增益仍须检查。

## 六、有序权谱时的一条 anchor 预算与真实次数效率上界

本节额外假设实际环顺序满足 a=w_0≥w_1≥...≥w_{n−1}>0，且 α>1。对每个 i<j，令

\[
\ell_{ij}=\alpha c_{ij}(a+w_i)-c_{ij}(a+w_j)\ge(\alpha-1)c_{ij}(a+w_i)\ge0.
\]

由 (1)，g_0=−Σℓ_ij；只保留玩家 0 的两条环边已要求

\[
\sum_{i<j}\ell_{ij}<\gamma_0. \tag{12}
\]

每个非零费用的 ℓ_ij 严格为正。相应锐增益效率也是逐单项式有限最大值：

\[
E_D=\max_{0\le k\le D}
\frac{\Delta_k}{\alpha(a+b)^k-(a+c)^k},\qquad
\Delta(f)\le E_D\ell(f). \tag{13}
\]

写 r=c/(a+b)。对 k≥1，因 b+c≤a+b，均值定理或二项展开给

\[
\frac{\Delta_k}{(a+b)^k}
\le (1+r)^D-1+\alpha D r,
\]

故

\[
E_D\le\frac{(1+r)^D-1+\alpha Dr}{\alpha-1}. \tag{14}
\]

证明中只使用 k≤D、(b+c)/(a+b)≤1 和
(b+c)^k−b^k≤k c(b+c)^{k−1}。D=0 时两边均为 0。于是 D r 很小时，这一架构无法从该 pair 的有限 anchor 预算得到大缺陷增益；这是有向真实费用的限制，不是 uniform δ 低泄漏条件。

还可把它变成对指定偏离的条件障碍。玩家 i 的入向项均非正，出向项至多 c_ij(a+w_i)，所以

\[
g_i\le\frac{1}{\alpha-1}\sum_{j>i}\ell_{ij}.
\]

令 E_i^*=max_{j>i}E_D(w_0,w_i,w_j;α)。任意 first-opposite 为 i 的非法态有

\[
h_i^H(s)\le\left(\frac1{\alpha-1}+E_i^*\right)\gamma_0. \tag{15}
\]

因此若该状态的原 margin 不大于右侧的负值，指定 first-opposite 翻位不能成为严格改善出口。这只否定此指定出口；其他玩家可能改善，不能据此声称该状态是 PNE，更不能声称全部时钟或全类题失败。要建立 actual 全状态障碍仍需同时控制其他玩家的出口，或给有限列的完整分离证书。

## 六补、固定原均衡的全玩家条件障碍

这一段来自实际总预算与深稳定态的独立推论，并结合 boss3 公屏消息 seq60 的逐列正部效率；合作来源按当前实际记录，不认定外部新颖性。它适用于任意权重顺序，不采用第六节的有序假设。

假设 α>1，固定 G 的一个 α-PNE b，记

\[
K_i=\alpha C_i^G(b^{\oplus i})-C_i^G(b)\ge0,
\qquad \Gamma=\sum_i\gamma_i>0.
\]

对每个三元 T 含 i，记玩家 i 在 b 中使用的该资源负载为 l_cur(T,i,b)，翻位后使用的另一资源真实负载为 l_post(T,i,b)。二者都包含玩家自身，均为正。定义

\[
\kappa_i(b,D)=\max\left\{0,
\max_{T\ni i,\ 0\le k\le D}
\frac{l_{cur}(T,i,b)^k-\alpha l_{post}(T,i,b)^k}{S_{T,k}}\right\}. \tag{16}
\]

这里 S_T,k 是式 (9) 的三种合法 pair 负载 k 次幂之和，始终严格正。则只要

\[
K_i\ge\frac{\kappa_i(b,D)\Gamma}{\alpha-1}
\qquad\text{对所有玩家 }i, \tag{17}
\]

任意次数≤D的允许时钟，在保留原双轮全部严格 α 改善边后，都仍使 b 为 α-PNE。因此满足 (17) 的这个 G 不可能被该架构以次数≤D全状态锁定。

证明：时钟各单项式系数 λ_T,k 非负。由 (16) 逐列相乘并求和，得到

\[
h_i^H(b)\le\kappa_i(b,D)\sum_T S_T.
\]

若 κ_i>0，由式 (8) 右侧严格小于 κ_i Γ/(α−1)≤K_i，故 h_i^{G+H}(b)<0；若 κ_i=0，直接有 h_i^H(b)≤0，故 h_i^{G+H}(b)≤−K_i≤0。两种情况均满足均衡所需弱不等式，包含 K_i=0 的边界。结论对全部玩家同时成立，不是只阻止 first-opposite 的出口。

式 (16) 的列最大值是单个玩家 margin 相对于总 S 预算的锐效率：正的最大值由相应单项式列取得；若所有列非正，κ=0 是便于处理的正部上界。它不保证同一组时钟能同时达到各玩家最大值，也不声称 (17) 必要。

**完全触发时可只看最高次数，其他情况须另检。** 若 b 在 T 上令三人同用一个资源，则 l_cur=W_T、l_post=w_i。除以 W_T^k 后，该列效率的正部为

\[
\frac{[1-\alpha(w_i/W_T)^k]_+}
{\sum_{\text{三种pair }P}(w_P/W_T)^k}.
\]

分子随 k 非降、分母为正且随 k 非增，因此其比值随 k 非降，0≤k≤D 的最大值在 k=D。这个结论是完全触发 margin 的效率，不是式 (9) 的 Δ/S；后者已有最高次数非最优反例。一般非触发的 l_cur、l_post 不满足此论证，不假设最高次数最优。

实际应用必须给出具体 b 的全部 K_i、原环 Γ 及列效率，或其有理上界。未证明这些数触发 (17) 时，这一条件障碍仍不能排除近线性循环增长族、常数倍次数编译器或全类命题。

## 七、精确审计与剩余研究义务

独立脚本 `tests/audits/weighted_congestion/cyclic_clone/verify_actual_clock_margins.py` 从 literal 所定真实资源用户群计算成本，随后逐状态检查式 (1)–(4)、两半 margin、式 (7)、所有多项式混合的式 (10)(13)(14)、逐状态逐玩家 κ 总预算和完全触发最高次数性质，并核验最高次数非最优的有理反例。包括 n=3 的两个非法态、α=1、零费用、常数费用、混合次数、任意和有序权谱；不导入仓库作者脚本。有限审计不是一般证明，证明是以上逐群恒等式、非负和与凸组合。

下一步优先用此实际线性接口检查近线性倍率的真实双轮环：能否存在 D=O(p) 或更一般 α ln(max{p,D})/max{p,D} 无界的可行族。若 LP 不可行，应给可核验有理 dual 或明确的条件障碍，不从求解器失败升级为数学结论。

## 八、实际四玩家证书：非统一真实预算与43次可行时钟

本节是 boss 在固定基体上发现、由本脚本按显式有理输入独立核验的有限证据；不声称43是最优次数。采用 `anchored_clock_degree_barrier.md` 的四玩家基体：权重 (1,1/2,1/4,1/8)、α=21/20，每个签名引入两互补资源，费用系数及签名为

| 签名 | 费用 |
| --- | --- |
| (0,0,+,+) | (1593928/421875) x³ |
| (0,+,+,0) | (452978/421875) x³ |
| (+,−,−,−) | (23816/5859375) x³ |
| (+,+,−,−) | (855968/17578125) x³ |

只加入 T012、T023 两对时钟，省略 T013；对内两侧仍用相同费用：

- T012：c_12(x)=(21/40)(x/(7/4))^43；
- T023：c_23(x)=(173/500)(x/(11/8))^43。

独立按真实用户负载遍历16个状态，合法8态使用原环出口，其余8态使用 first-opposite 出口；全部严格 α margin 为正，精确值逐态存于 `evidence/runs/weighted_congestion/cyclic_clone/actual_clock_margins.json` 的 `degree43_fixture` 字段，最小值存于该字段的 `minimum_margin`。显式输入存于 `examples/weighted_congestion/anchored_actual_clock_degree43.json`。这证明该固定基体的同费锚定架构在次数43可行，与同次数3障碍相容；也展示实际有向差接口容许非统一幅度、省略某些三元。没有从该固定实例外推增长族或一般 D=O(p) 编译器。

同一显式基体的统一泄漏预算使用 B=56643761/70312500、η=49676111/6750000000、δ=12/13、L=3；脚本以有理数逐次幂检查，满足 δ^D≤η/(4α²BL) 的最小整数为 D=91，并反查 D−1 不满足。因此本固定实例实际43次证书优于这项统一预算选值；不据此声称43最优、此前91为必要实际次数，或得到一般次数改善。


## 规范审查与重现入口

[独立重构与冻结攻击](../../reviews/weighted_congestion/ordinal_potentials/actual_clock_margins_review.md)记录原始冻结hash、先重构的义务、追加κ段的后置核查和最终整合核对。κ状态效率预算接入同级boss3的独立必要预算推导，证明在本文完整重建。

在仓库根执行下列标准库Fraction审计，默认输出stdout，指定`--output NEW_PATH`时独占创建：

- `python3 tests/audits/weighted_congestion/cyclic_clone/verify_actual_clock_margins.py`：一般g/Δ/κ/有序效率及显式43次输入；冻结记录`evidence/runs/weighted_congestion/cyclic_clone/actual_clock_margins.json`。
- `python3 tests/audits/weighted_congestion/cyclic_clone/independent_actual_clock_geometry.py`：读作者稿前完成的独立literal几何/混合费核验；冻结记录`evidence/runs/weighted_congestion/cyclic_clone/independent_actual_clock_geometry.json`。
- `python3 tests/audits/weighted_congestion/cyclic_clone/independent_actual_clock_certificate.py`：独立固定证书、uniform预算反算、κ及次数边界；冻结记录`evidence/runs/weighted_congestion/cyclic_clone/independent_actual_clock_certificate.json`。

输入为`examples/weighted_congestion/anchored_actual_clock_degree43.json`。同一基体的统一预算最小整数为91：B=56643761/70312500、η=49676111/6750000000、δ=12/13、L=3，直接有理幂确认δ^91≤η/(4α²BL)<δ^90。这里比较的是已有充分预算的选值；43不是最优性结论。实际运行参数、seed、Python版本、代码/输入hash及有限覆盖见各JSON。
