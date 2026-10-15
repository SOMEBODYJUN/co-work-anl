# 资源局部势拼接：共享乘子、两尺度障碍与两权组锐界

R2，2026-10-14。模型采用 [WC-MODEL](../../weighted_congestion_frontier/MODEL.md)。
作者来源：主对话重建 packing、资源拼接及精确审计；内部 bridge_review 独立先重构；
dense_scales 与 path_obstruction_review 独立得到同一仿射分片势。
本页给出资源局部证书及其准确限制，WC-TARGET v1 仍 OPEN。

## 1. 精确身份与范围

三个命题共用对象：有限玩家与资源、正实权、非负系数次数至多 d 的费用、任意非空有限
多资源策略族；成本不乘权重。潜在用户集 U_e 是至少一个策略含 e 的玩家集合。
W(T)=Σ_{i∈T}w_i，空集势为零。所有边际指 T⊆U_e、i∈U_e\T 的插入边，实际偏离可含多资源。

### WC-R2-RESOURCE-POWER-BRIDGE v1

**Exact Statement / Quantifiers.** 对任意 MODEL 中有限游戏、任意固定 R>1、0<p<1，令
K_e=sup_{x>0} #{i∈U_e:x≤w_i<Rx}；非空 U_e 的 m_e、M_e 为最小、最大权，Q_e=M_e/m_e。
令

\[
A_R(p)=\frac{(1-R^{-1})^p}{1-R^{-p}},\qquad
H_d(p)=\sup_{S\ge0}S^p\left[1-\left(\frac S{1+S}\right)^d\right].
\]

d=0 时明确 H_0=0，包括 S=0；d≥1 时 S=0 的整个表达式为零。
存在 α-PNE，且下面显式势的每个全局最小者都是 α-PNE，其中

\[
\alpha=\max_{e:U_e\ne\varnothing}
\min\{Q_e,\ 1+A_R(p)K_e^{1-p}H_d(p)\}.
\tag{1}
\]

若所有 U_e 为空，取 α=1。所有这些参数是潜在用户参数，不是选定状态参数。
**Assumptions / Scope.** 每个资源预先固定一条规则；同一 p 用于全游戏。排序规则使用
费用凸性；本模型的多项式满足该条件。不限人数、不同策略族、空策略与零费用。
**Dependencies.** 下述 packing、单资源插入比较和有限状态全局最小化。
**Evidence / Status.** 自足一般证明及独立先重构审查；标准库 Fraction 有限核验。
完整内部证明，外审和全球新颖性未认证。排序势及局部边际拼接原理已有文献来源。
**Objections / Conclusion.** (1) 是实例结构上界，K_e、Q_e 无全类控制；不是全类 o(d)。

### WC-R2-POWER-PATH-OBSTRUCTION v1

**Exact Statement.** 对每个固定实数 0≤p<1、每个有限 α≥1，存在有限两权组 U 和 c(x)=x，
没有任意集合函数 F、共同 λ>0 能在全部插入边满足
λw_i^p c(W(T+i))≤Δ_iF≤αλw_i^p c(W(T+i))。
两组人数各可任意大。权比、人数可依赖 p,α。
**Scope / Dependencies.** 全部子集上的固定 power 乘子边际夹逼；仅有限路径求和。
**Evidence / Status.** 下述一般证明及两份独立重构，有限 Fraction 路径核验；内部证明。
**Objections.** 不排除实例相关的其他乘子、状态相关比较、资源间支付和非势存在论证。
**Conclusion.** 固定 p<1 的密集尺度拼接在 d=1 已无全类常数证书；不是 PNE 非存在。

### WC-R2-AFFINE-TWO-TYPE v1

**Exact Statement / Quantifiers.** 固定两正权 a,b 及两正乘子 h_A,h_B。
对费用 c(x)=ℓx+β、ℓ,β≥0，定义
D=max{h_A/a,h_B/b}/min{h_A/a,h_B/b}≥1。
对每个有限两组人数 M,N，存在任意子集上边际夹逼在
[h_i c(W(T+i)), √D h_i c(W(T+i))] 的显式势。
若 ℓ>0，则跨全部有限正 M,N 的最小可行倍率上确界恰为 √D；不声称每个固定 M,N
的最优倍率都等于该值。ℓ=0 时统一最优倍率为 1。
**Objects / Scope.** 玩家在同一类型具有相同权和乘子；势可依赖人数。
两权相等而乘子不同也涵盖。与游戏存在门槛不同。
**Dependencies / Evidence.** C1 分片二次函数、有限差分积分、两条精确添加路径；
两成员先独立重构相同公式，主对话逐计数 Fraction 审计。
**Status / Objections.** 完整内部证明，外审及新颖性未认证；非高次费用的两类型上界。
**Conclusion.** 对 h_i=w_i^p、0≤p≤1，正斜率仿射两权组证书的锐统一损失为
(max{a,b}/min{a,b})^{(1-p)/2}。这量化上一障碍的真实损失。

Related Files（均相对仓库根）：
`research/reviews/weighted_congestion/power_bridge/independent_review.md`、
`research/reviews/weighted_congestion/power_bridge/path_review.md`、
`research/current/weighted_congestion/power_bridge/affine_two_type.md`、
`research/current/weighted_congestion/power_bridge/path_obstruction.md`；
`tests/audits/weighted_power_bridge.py`；
`evidence/runs/2026-10-14/weighted_power_bridge.json`。
Truth、Value、Novelty、Mechanism、Ambition 分开：本页为内部已证方法资产，价值在于
可复用资源接口与精确失败门槛；机制已显式；新颖性未认证；主目标野心保持全类但未达成。

## 2. 稀疏谱的 power-moment 证明

设正数序列 v_1≥…≥v_n 在每个 [x,Rx) 至多 K 个，则 v_{j+K}≤v_j/R。
否则区间 [v_{j+K},Rv_{j+K}) 会同时容纳 j,…,j+K 共 K+1 项。
按位置模 K 拆为 K 条 R 分离链；等于 R 的端点允许，故半开区间无问题。

单条链首项 a、尾部总和 T≤a/(R−1)。有限长度归纳给
Σ v_j^p≤a^p+A_R(p)T^p≤A_R(p)(a+T)^p：
令 t=T/a，函数 (1+t)^p−t^p 随 t 非增，在 t=1/(R−1) 取 1/A_R(p)。
单项基例使用 A_R(p)≥1（同一等式和单调性亦给出）。
对 K 条链总和 S_r 应用凹性 Σ S_r^p≤K^{1-p}(Σ S_r)^p，得到

\[
\sum_jv_j^p\le A_R(p)K^{1-p}\left(\sum_jv_j\right)^p.\tag{2}
\]

取 Ψ_e(T)=(Σ_{j∈T}w_j^p)c_e(W(T))。插入权 v 的 i，令 S=W(T)/v；则
ΔΨ_e=v^p c_e(v(1+S))+(Σ_{j∈T}w_j^p)[c_e(v(1+S))−c_e(vS)]。
非负次数 ≤d 逐单项给差项≤[1−(S/(1+S))^d]c_e(v(1+S))；零费用直接成立。
(2) 因而给

\[
v^p c_e(W(T+i))\le\Delta_i\Psi_e\le
[1+A_R(p)K_e^{1-p}H_d(p)]v^p c_e(W(T+i)).\tag{3}
\]

对 d=0 直接使用 H_0=0。对 d≥1、S>0，有 H_d≤κ_p d^p，其中 κ_p=sup_{y>0}(1−e^{-y})/y^p<1：
(1+1/S)^{-d}≥e^{-d/S}，令 y=d/S；比值两端趋零，中间严格小于 1。
令 K=max_{e:U_e≠∅}K_e。因此固定 R、K=o(d) 的纯稀疏子类有 o(d) 上界。例如 d/K>e 时取 p=1/log(d/K)，
利用 A_R≤1/(1−R^{-p})≤1+1/(p log R)，给
α≤1+eK[1+log(d/K)/log R]。这不是全类的 K 控制。

## 3. 排序资源与共享乘子拼接

定义降序 Φ_e(T)=Σ_j u_j c_e(Σ_{k≤j}u_k)，u_j 为 T 中权的非增排列。
凸费用下交换相邻逆序项可验证降序最小化该离散积分；故将新玩家放在末尾的候选排列
给 Δ_iΦ_e≤v c_e(W(T+i))。

下界有比 v/Q_e 更强、缩放所必需的形式：Δ_iΦ_e≥m_e c_e(W(T+i))。
证明：设插入点前负载 X，后续权 u_j≤v，B_j=Σ_{k≤j}u_k。
插入自身贡献 v c_e(X+v)≥m_e c_e(X+v)。尾部差项是
Σ_j u_j[c_e(X+v+B_j)−c_e(X+B_j)]。
由于 X+B_j≤X+v+B_{j−1}，它至少为
m_e Σ_j[c_e(X+v+B_j)−c_e(X+v+B_{j−1})]，望远镜完成证明。
该下界只需非减性；上界使用凸性，不能偷换为任意非减费用。

将 Φ_e 乘 M_e^p/m_e，得到
v^p c_e≤Δ_i[(M_e^p/m_e)Φ_e]≤Q_e v^p c_e。
下界实际为 M_e^p c_e≥v^p c_e；上界用 M_e^p v^{1-p}≤M_e。
仅使用弱下界 (v/Q_e)c_e 无法推出这一缩放，应明确避免该推理缺口。

每个资源选 (3) 或排序势中较小的倍率，势相加。所有边共用 h_i=w_i^p。
玩家单方偏离时保留资源的势完全取消。记删去、新加、保留资源的成本为 C_A、C_B、C_D，
保留资源的负载不变；严格改善给 C_A>αC_B+(α−1)C_D≥αC_B。
删去资源的边际至少 h_i C_A，新加资源的边际至多 αh_i C_B，故总势严格下降。
有限纯状态空间中的全局最小者故为 α-PNE，零成本与空策略直接用不等式处理。
不宣称全局优化可多项式完成。

## 4. 两尺度的路径障碍

若全部边际满足共同夹逼，则任意添加排列 π 的路径和
T(π)=Σ_k h_{π(k)}c(Σ_{j≤k}w_{π(j)}) 满足
λT(π)≤F(U)−F(∅)≤αλT(π)，故任意两路径 T(π)≤αT(ρ)。
这只是必要条件，不能普遍当作充分条件。

一权 1 玩家、n 权 ε 玩家、h=w^p、c(x)=x，两路径和为
T_HL=1+nε^p+Q，T_LH=1+nε+Q，Q=ε^{p+1}n(n+1)/2。
取整数 n→∞、ε=n^{-2/(1+p)}，δ=(1−p)/(1+p)>0，则比值恰为

\[
\frac{3/2+1/(2n)+n^\delta}{3/2+1/(2n)+n^{-\delta}}\longrightarrow\infty.\tag{4}
\]

p=0 也涵盖；有限 n 及正 ε 才是见证。固定任意大的重组人数 M 后同理仍无界。
下一节更精确的两组计数极限同时证明两组都可任意大。
p=1 时 Φ(T)=½[W(T)^2+Σ_{i∈T}w_i^2] 恰有边际 w_iW(T+i)，所以排除 p=1 是必要的。
仿射加权游戏仍有精确 PNE；本障碍绝非游戏非存在定理。

## 5. 仿射两类型的显式锐势

按 q_A=h_A/a≤q_B=h_B/b 重新标号，D=q_B/q_A=k²，k≥1。
令 x=aM_T、y=bN_T 为子集的两类物理负载，定义

\[
F_0(x,y)=
\begin{cases}
\frac12(x^2+2Dxy+Dy^2),&x\ge ky,\\
\frac12(kx^2+2kxy+kD y^2),&x\le ky.
\end{cases}\tag{5}
\]

两分支之差为 −(k−1)(x−ky)^2/2，边界值与梯度相同，F_0 是 C1。
在 x≥ky 区域，F_x=x+Dy，F_y=D(x+y)；在另一域，
F_x=k(x+y)，F_y=kx+kDy。因此全域
x+y≤F_x≤k(x+y)，D(x+y)≤F_y≤kD(x+y)。

定义线性费用势
Φ(T)=q_A F_0(x,y)+½Σ_{i∈T}h_iw_i。
沿加入 A 玩家时 x 增 a，导数积分下界为
q_A∫_0^a(W(T)+t)dt=h_A[W(T)+a/2]；自项补偿 h_A a/2 后为
h_A W(T+i)。上界同理≤k h_A W(T+i)，因为自项只须乘 1≤k。
B 玩家沿 y 增 b 完全相同，包含穿过分支边界的步骤。
仿射费用势为 ℓΦ(T)+βΣ_{i∈T}h_i，仍有倍率 k；零斜率常数资源则精确。

**最优性及端点。** 两组人数 M,N 的两排序路径具有共同自身项
U=½q_A a²M(M+1)+½q_B b²N(N+1)，交叉项分别 q_B abMN 和 q_A abMN。
对 k>1，其比值严格小于 k，因为 U>q_A k abMN。
取 N=floor(aM/(kb))、M→∞，比值趋于 k（仿射常数项只有 O(M)，不影响正斜率极限）。
故每个 α<k 均由某个有限正 M,N 排除，(5) 又在所有 M,N 给 k，所述跨人数 sup 恰为 k。
k=1 时精确，符合 α≥1。有限固定人数可严格小于 k，不能改写这个量词。

## 6. 一手来源与继续义务

Hansknecht–Klimm–Skopalik (2014), Definition 1、Theorem 4、Lemma 5：离散积分、
局部边际势与凸费用降序规则。本轮打开并核对官方完整 PDF：
https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX-RANDOM.2014.242 。
本页排序机制不是新发明；packing 和两类型分片势的新颖性未作穷尽认证。
Caragiannis–Fanelli 的 d 保证与核心无限下界只作已有研究背景，不是本页证明依赖。

下一真正义务是允许跨资源／整次偏离支付或状态相关乘子。
固定 p 可以依 d 变化，但每个 p(d)<1 的资源局部全子集接口仍被仿射族排除。
允许 p 依整个有限实例选取不在此障碍量词中。
更一般固定任意玩家乘子的高次局部夹逼已有公屏 seq8、commit 809b032 的多尺度障碍，
本页不重新宣称这一更广结论为新发现。


---
整理来源与当前文件用途见[逐文件登记](../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
