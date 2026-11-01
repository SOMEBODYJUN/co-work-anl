# 最优参照逆 SD：两份实际预算的初始化审查

2026-10-24，global 对 root 精确合同的独立代数/域核查。**不是新的 HALF 证明；后续共同容量未付。** 本页只核查一般输入下的合法 source 初始化，未运行新有限扫描。

## 1. 参照与源

固定原完整 SPE σ，其实际叶 B=(B_1,…,B_m)，实际收益 u_i。任取最优 m 槽参照 T=(T_1,…,T_m)，允许重复主题，记 O 为最优并集、c_T 为其覆盖者数。T 无需是 SPE。

对 x∈T_i 给源库存 p_ix=1/c_T(x)，故每个 x∈O 有 Σ_i p_ix=1，总源 Σ_i p_i=OPT，其中 p_i=Σ_x p_ix。

在实际历史 B_<i 上强制 T_i，真实完成叶为 W_i。令

\[
\delta_{ix}=c_B(x)+1-\mathbf1_{x\in B_i}\quad(x\in T_i).
\]

这是前文静态中间分母。SD 第一正项定义为

\[
q^B_{i\to j}(x)=
\frac{\mathbf1_{x\in T_i\cap B_j\setminus T_j}}{c_T(x)\delta_{ix}},\qquad j\ne i,
\]

第二正项定义为

\[
q^W_{i\to j}(x)=
\frac{\mathbf1_{x\in T_i\cap W_{i,j}\setminus B_j}}{\delta_{ix}c_{W_i}(x)},\qquad j>i.
\]

记 PB_ix=Σ_j q^B_{i→j}(x)、PW_ix=Σ_j q^W_{i→j}(x)，对应负项为 NB_ix、NW_ix。每个 q^B 的 recipient 是原实际 B_j，故可直接成为实际利润 j 的请求；每个 q^W 的 recipient j>i 是自然 context (W_i,<j,j)，规定叶确为 W_i。

## 2. 标量逆 SD 初始化核查

ROW 逐客户给 PB_ix≤p_ix，因此

\[
r_i=p_i-PB_i\ge0.
\]

真实 actual-prefix IC 给 z_i:=u_i(W_i)≤u_i。逐客户恒等式直接求和给

\[
r_i-u_i=PW_i-(NB_i+NW_i+\ell_i),\qquad
\ell_i=u_i-z_i\ge0.
\]

所以 b_i=(r_i−u_i)_+≤PW_i，可在原第二正边保留总额 b_i；当前实际付款取 d_i=min(u_i,r_i)。严格有

\[
\boxed{OPT=\sum_i d_i+\sum_{i,j}q^B_{i\to j}+\sum_i b_i.}\tag{INIT-2}
\]

固定实际 recipient j，令 Bcol_j=Σ_i q^B_{i→j}。固定 B 的 STATIC-COLUMN 给

\[
Bcol_j\le u_j(B;(O\cap B_j)\setminus T_j)\le u_j.
\]

因此当前 d_j 与 Bcol_j 分别至多使用一份 u_j，尚余非负预算

\[
R_j=2u_j-d_j-Bcol_j
\ge (u_j-d_j)+u_j(B;(B_j\setminus O)\cup(B_j\cap T_j)).
\tag{RESIDUAL}
\]

## 3. root 的逐客户 CLIP 加强：独立重构通过

标量选择可进一步保留全部最优客户库存。令

\[
r_{ix}=p_{ix}-PB_{ix}\ge0,\qquad q_{ix}=PW_{ix}.
\]

直接使用 query 利润 z_i(W_i;x) 而非逐客户 IC slack，精确式为

\[
r_{ix}-q_{ix}
=z_i(W_i;x)-NB_{ix}-NW_{ix}\le z_i(W_i;x).
\]

故

\[
\sum_x(r_{ix}-q_{ix})_+\le z_i\le u_i.
\]

这里只在求和后调用 **一次完整 actual-prefix IC**；没有断言逐客户 ℓ_ix 非负，也没有逐客户重权 IC。由此

\[
\boxed{\sum_x\min(r_{ix},q_{ix})
=r_i-\sum_x(r_{ix}-q_{ix})_+\ge r_i-u_i.}\tag{COORD-CLIP}
\]

因此可选 0≤a_ix≤min(r_ix,q_ix)、Σ_x a_ix=b_i。在 x 的原 W 正边间按比例分配 a_ix（q_ix=0 时 a_ix=0）。原 q^W 边子容量保持，current 源余额 r_ix−a_ix≥0，总额恰为 r_i−b_i=d_i。每个最优源份额都有非负守恒分割

\[
p_{ix}=PB_{ix}+(r_{ix}-a_{ix})+a_{ix}.
\]

对所有拥有 x 的最优角色求和，仍只有一单位 x 库存。当前 d_i 用 actual i 的整行钱包支付；源标签 x 是来源标记，**不意味着实际 B_i 必须覆盖 x**。

## 4. 接 full SAFE/CLIP 后真正的未证步骤

仅把 Σ_i b_i 的 W-future 请求送入原全客户自然图。全部入口自然当前利润为正。固定任意合法 SAFE/CLIP 子核后，原严格角色 DAG 给非负实际终端 Aout_j，且

\[
\sum_j Aout_j=\sum_i b_i.
\]

因而

\[
OPT=\sum_j(d_j+Bcol_j+Aout_j).
\]

以下是准确的充分候选，**尚未证明**：存在最优槽分配、上述逐客户初始化选择及合法 full SAFE/CLIP 核，使

\[
Aout_j\le R_j\quad\text{对所有 }j.
\tag{TWO-BUDGET-CAP?}
\]

它若成立即得 HALF。总量约束本身要求 Σ_i b_i≤Σ_j R_j，等价于 OPT≤2W；没有从非负 residual 或初始化直接得到它。逐角色候选更强。

保留源 i 标签时，初始 W_i-future 入口在 j>i，且其有序前缀与 B 在 i 之前完全相同。后续 reset 只在更晚当前角色发生；past 正 coupon 不可能去 i 以前。因此该源的实际出口只可能位于 j≥i，允许返回 i。此结论不需要初始客户 fresh。

每条初始 q^W_{i→j}(x) 还有 x∈O 且 x∉B_j 的 new-action 支持，但 whole-profit 自然图归一化会重新采客户。没有继承仅 fresh 的 HIT 初始化或 PRICE 数值界，也没有证明此支持持续保留。
