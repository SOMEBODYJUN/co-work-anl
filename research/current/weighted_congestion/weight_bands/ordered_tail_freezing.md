# 有序权组的尾部负载冻结：密集等权群的非势拼接

Claim `WC-ORDERED-COHORT-FREEZING-v1`。完整一般证明；独立重构及冻结攻击见[审查记录](../../../reviews/weighted_congestion/weight_bands/ordered_tail_freezing_review.md)。未外审，优先权未认证。
只给结构子类上界，不解决唯一全类 `O(d/ln d)` 判定。

## 精确身份

**Objects / Domain。** 完全采用 `research/weighted_congestion_frontier/MODEL.md`：有限非空玩家、资源；任意正实权；非空有限资源子集策略族，可含空策略；非负系数次数至多整数 `d≥0` 的多项式；成本不乘权，偏离按真实负载。

**Quantifiers / Assumptions / Definitions。** 对每个此类游戏、玩家集的任意有序划分 `N=B_1\sqcup\cdots\sqcup B_m`，每组非空，令 `U_e` 为资源的潜在用户集，`U_{e,j}=U_e∩B_j`。当 `U_{e,j}≠∅` 时定义

\[
a_{e,j}=\min_{i\in U_{e,j}}w_i,\quad
b_{e,j}=\max_{i\in U_{e,j}}w_i,\quad
L_{e,j}=\sum_{k>j}\sum_{i\in U_e\cap B_k}w_i,
\]
\[
R_{e,j}=b_{e,j}/a_{e,j},\qquad
\beta_{e,j}=(1+L_{e,j}/a_{e,j})^d,\qquad
A=\max_{(e,j):U_{e,j}\ne\varnothing}R_{e,j}\beta_{e,j}.
\]

若没有可用资源，所有成本为零，定义 `A=1`。分组无需先假定按权重降序；小尾部条件本身仅在共享资源处限制相对尺度。

**Exact Statement / Conclusion。** 每个此类游戏存在 `A`-PNE。一个具体有限选择程序是依 `j=1,…,m` 固定前组已选策略、暂忽略后组，在当前组上求下述已缩放资源 Shapley 势的全局最小，然后冻结该组。每阶段任取一个全局最小点，全部完成后均得到 `A`-PNE。没有计算复杂度保证，也没有声称原游戏的全部严格 `A` 改善使同一个势下降。

**Dependencies。** 既有 `WC-R3-DENSE-SHARE v1` 的精确 Shapley 份额包络及其边际势身份、非负多项式平移、逐单项式负载增长不等式、有限最小化。本稿后文重述所需包络，不导入外部存在定理。

**Scope / Evidence / Objections / Status。** 一般证明如下。配套 Fraction 程序逐字实现各阶段势，穷举每阶段全部最小点，并在全部所选最终状态上核验每个合法偏离；有限证据不代替一般证明。主目标未闭合：下文精确两权级反例证明，最佳分组参数本身固定次数仍可无界。本接口通过只选择部分更新和冻结绕开全改善可分势障碍，没有推翻该障碍。

## 证明

阶段 `j` 固定之前各组的策略，记它们在资源 `e` 的总负载为 `h_e≥0`。忽略后续组，只让 `B_j` 玩家按原合法策略选择。当前组看到的费用是

\[
g_e(x)=c_e(h_e+x).
\]

由二项式展开，`g_e` 仍是次数至多 `d` 的非负系数多项式，含正常数项也无妨；固定背景不会改变玩家正权或策略族。

对当前组资源用户子集 `S⊆U_{e,j}`，记 `W(S)=Σ_{i∈S}w_i`，定义 `F_e(x)=xg_e(x)` 和

\[
H_e(S)=\sum_{\varnothing\ne T\subseteq S}
\frac{(|T|-1)!(|S|-|T|)!}{|S|!}F_e(W(T)),\qquad H_e(\varnothing)=0.
\]

既有份额引理给出精确边际 `φ_{i,e}(S)=H_e(S)-H_e(S\setminus\{i\})`，且对所有 `i∈S`

\[
a_{e,j}g_e(W(S))\le\phi_{i,e}(S)
\le b_{e,j}g_e(W(S)). \tag{1}
\]

这里用潜在用户的最小、最大权而不是仅当前用户，因此任何合法偏离后的新用户集也满足同一包络。引理对零费用成立，无需除费用。对 `F=xg(x)`，证明是非负单项式展开后的普通份额随权非减、每权份额随权非增，再用效率 `Σφ=Wg(W)`；详见既有权带正文。

阶段势取

\[
\Phi_j(s_{B_j})=\sum_{e:U_{e,j}\ne\varnothing}
\frac{\beta_{e,j}}{a_{e,j}}H_e(S_e(s_{B_j})).
\]

这是当前有限状态集上的实函数，全局最小点存在。令 `D_i(s)` 为对应缩放边际之和。任何本阶段单方偏离都精确满足

\[
\Phi_j(t_i,s_{-i})-\Phi_j(s)=D_i(t_i,s_{-i})-D_i(s). \tag{2}
\]

其中删去、新增资源由边际身份处理；保留资源的负载、集合和边际完全相同并取消。因此在本阶段所选全局最小点，`D_i(s)≤D_i(t_i,s_{-i})` 对每个合法偏离成立。

现在冻结当前组，完成所有后组，得到最终状态 `s*`。给定当前组玩家 `i` 及资源 `e∈s_i*`，本阶段结束时该资源的全负载 `z=h_e+W(S_e)` 至少为 `w_i≥a_{e,j}>0`；后组增加的实际负载 `y` 满足 `0≤y≤L_{e,j}`。逐单项式有

\[
(z+y)^k\le(1+L_{e,j}/a_{e,j})^d z^k\quad(0\le k\le d),
\]

故 `c_e(z+y)≤β_{e,j}c_e(z)`。和 (1) 相接，最终玩家当前成本不超过其冻结时的缩放边际：

\[
C_i(s^*)\le\sum_{e\in s_i^*}\beta_{e,j}g_e(W(S_e))\le D_i(s). \tag{3}
\]

任意合法偏离 `t_i`，先在冻结阶段重算其负载。由 (1) 及 `βR≤A`，

\[
D_i(t_i,s_{-i})\le\sum_{e\in t_i}\beta_{e,j}R_{e,j}
g_e(W(S_e(t_i,s_{-i})))\le A C_i^{\rm stage}(t_i,s_{-i}). \tag{4}
\]

后续玩家只增加资源负载，费用非递减，所以本阶段的真实偏离成本不超过最终状态同一偏离成本。合并 (2)--(4)，

\[
C_i(s^*)\le D_i(s)\le D_i(t_i,s_{-i})
\le A C_i^{\rm stage}(t_i,s_{-i})
\le A C_i(t_i,s^*_{-i}).
\]

这对每组每个玩家和每个合法偏离均成立。没有除任何成本，故包括空策略、零资源费用、零偏离成本和保留资源。`d=0` 时 `β=1`，同一证明仍成立；此时另有更强的独立选最廉策略精确均衡结论。

## 易用形式与精确匹配子类

若固定实数 `R≥1,ε≥0`，每个非空 `U_{e,j}` 都有 `R_{e,j}≤R` 且 `L_{e,j}≤εa_{e,j}`，则有 `R(1+ε)^d`-PNE。

特别，对固定绝对 `R`、任意整数 `d≥2`，若

\[
\frac{L_{e,j}}{a_{e,j}}\le
\frac{\ln(d/\ln d)}d=\frac{\ln d-\ln\ln d}{d},
\]

则 `R(1+ε)^d≤R exp(dε)=R d/ln d`。这给一个精确结构子类的匹配阶上界。不可只写 `ε=ln d/d`，那只能给 `Rd`，丢掉所需对数。更宽的精确允许门槛为 `(d/ln d)^(1/d)-1`。

## 任意密集等权群：旧参数都可无界

固定任意整数 `d≥2,n≥d`，两个组各有 `n` 名玩家：先组每人权 `M=dn`，后组每人权 `1`。任意资源及任意策略族只要使用这些玩家，均有组内局部权比 `1`，先组的后续潜在总权至多 `n`，所以 `L/a≤1/d`；后组尾部为零。因此此整个类都有

\[
(1+1/d)^d<e
\]

倍近似均衡，不限制 `n`。若存在费用为 `x^d` 的资源让两个组全部玩家都成为潜在用户（例如每人均可在两个同为 `x^d` 的资源间选择），其资源支持为 `2n`，局部最大最小权比为 `dn`；任意乘性窗口参数 `K_R≥n`，而纯 `d` 次高次份额工具的最小份额为 `q=1/[n(dn+1)]`，该工具给出的倍率至少 `1/(dq)=n(dn+1)/d`。因此既有资源支持、局部权比、权密度、个体份额的直接保证均可随 `n` 无界或退回通用线性界，而冻结界始终小于 `e`。

这里比较的是存在上界机制，不是游戏非存在下界，也不声称这些游戏没有精确 PNE。密度式中当 `n≥d` 时，`A_R(p)K_R^(1-p)d^p≥d` 对每个 `R>1,0<p<1` 成立，因此选择其自由参数也不能从那一式恢复本常数保证。

## 任意划分仍可能使本参数无界

独立 Claim：`WC-ORDERED-TAIL-PARAMETER-LIMIT-v1`。此项由团队内另一研究者独立提出、独立审查者进一步锐化，主研究者转交，本文重构核对。**Exact Statement / Objects / Domain / Quantifiers：** 对每个整数 `d≥1,K≥1`、每个实数 `H≥1`，取单资源 `e`、一名权 `H` 玩家和 `K` 名权 `1` 玩家，费用 `c_e(x)=x^d`，人人策略族 `{empty,{e}}`。则在上文全部有序划分上，

\[
\min_{\text{ordered partitions of }N} A
=\min\{H,(1+K/H)^d\}.
\]

**证明。** 若重玩家和至少一名轻玩家同组，该组 `R=H`，所以 `A≥H`。否则重玩家独占一组；若前方有轻玩家组，那么该轻组的最小权为 `1`、尾部潜在总权至少 `H`，故其 `β≥(1+H)^d≥H`。若前方没有轻组，重玩家首组，尾部是全部轻玩家，故其 `β=(1+K/H)^d`。这穷尽所有划分，给出所写最小值的下界。全部玩家放同组时 `A=H`；重玩家独占首组、全部轻玩家同在末组时 `A=(1+K/H)^d`。二者给出匹配上界。

**Scope / Conclusion / Objections。** 取 `K=ceil(H²)`，则 `(1+K/H)^d≥(1+H)^d≥H`，所以最优参数恰为 `H`。固定 `d≥1` 而让 `H` 增大，即使自由选择最佳划分，本定理的数值保证也无实例无关的上界。这个游戏同时有全空精确 PNE；本结论仅限制所写潜在尾部最坏放大参数，不否定其他冻结规则、实际而非潜在尾部控制、选择性重开早组或任何一般存在命题。

**Dependencies / Evidence / Status。** 有限三分情况、正权与最坏潜在负载参数，未用其他势障碍。配套程序在明示的有限小参数上穷举全部有序划分并精确复算 `A`；一般证明不依赖有限计算。完整直接证明，独立审查范围见所链记录；外审和新颖性未认证。

## 未闭合义务和证据

关键未解是对任意稠密权谱如何冻结：大尾部可能改变先组费用，强行合并组又会使组内权比很大。下述纯潜在尾部参数已证无全类统一控制；允许重开早组或依实际占用控制的变体仍需新证明。

讨论来源：主团队内部独立重构后提出；主研究者指出公屏 boss3 消息 15 已有未入库的局部 tail 插入预算，应在正式正文中核对并注明该讨论关系，不能宣称全球新颖性。

配套精确程序：`tests/audits/weighted_congestion/weight_bands/verify_ordered_tail_freezing.py`；独立参数审计：`tests/audits/weighted_congestion/weight_bands/independent_tail_parameter.py`。冻结结果分别为 `evidence/runs/weighted_congestion/weight_bands/ordered_tail_freezing.json` 和 `ordered_tail_parameter_independent.json`（同目录）。

从仓库根运行作者程序的 `--check evidence/runs/weighted_congestion/weight_bands/ordered_tail_freezing.json` 复验，或 `--output NEW_PATH` 独占创建新结果；独立程序默认 stdout，`--output NEW_PATH` 拒绝覆盖。作者记录具体 seed、Python 版本、源码 SHA256、实际输入和输入生成规则；Fraction 无容差。独立参数程序枚举全部有序非空组型，按等权轻玩家置换取商，不调用作者实现。有限核验的实际覆盖由冻结结果与审查记录列明，不证明任意实权结论。

Truth：所写结构存在界与参数锐式有一般证明；Value：跨组冻结接口及其精确失败边界；Novelty：未认证；Mechanism：局部份额势和单调尾部扰动；Ambition：全类唯一目标保持 OPEN。
