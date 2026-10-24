# 条件倒数账：自由源公式及已失败的逐客户自动单调

2026-10-24，个人研究 checkpoint。**Q-CAG-HALF、自由逐位置 Mfull、自由聚合 Mpath 仍 OPEN。** 下文是全输入代数与一条条件的精确失败边界；没有一般福利新下界。不把同分布推送、指定源选择器和自由菜单混淆。

## 1. 对象与独立性

固定任意完整历史纯策略及实际位置 i。对每个强制合法主题 A，Z_i(A) 是含固定实际过去、当前 A 及原策略真实后继的完整 m 槽终局。令

\[
I_A(x)=\mathbf1_{x\in A},\quad c_A(x)=c_x(Z_i(A)),\quad
h_A(x)=c_A(x)-I_A(x),
\]

\[
R_A(x)=\frac1{1+h_A(x)},\qquad
J_A(x)=\frac1{(1+h_A(x))(2+h_A(x))}.
\]

过去也计入 h；没有冻结后继。令 p 是查询分布，Q 是与查询独立的自由列源分布，q_x=Pr_p(x∈T)、r_x=Pr_Q(x∈A)。定义

\[
C_i(p,Q)=\mathbb E_{A\sim Q}\sum_x\frac{q_x}{1+c_A(x)},\qquad
D_i(Q)=\mathbb E_{A\sim Q}\sum_xI_A(x)R_A(x).
\]

\(\psi_i(p)=\min_Q C_i(p,Q)=\min_A C_i(p,\delta_A)\) 是该查询的自由完整菜单价格。SPE 仅用于 e_i(Q)=u_i-D_i(Q)≥0。

## 2. 自由列源的精确倒数协方差公式

对每个客户，逐样本有

\[
\frac1{1+c_A}=R_A-I_AJ_A.
\]

因此任意 p、Q 均满足

\[
\boxed{C_i(p,Q)-D_i(Q)=\sum_x\left[(q_x-r_x)\mathbb E_QR_A(x)
-\operatorname{Cov}_Q(I_A(x),R_A(x))
-q_x\mathbb E_Q[I_A(x)J_A(x)]\right].}\tag{FQ}
\]

所有分母至少为一；不需条件事件、不出现 0/0。该式不需 SPE。它给自由菜单的准确接口

\[
\boxed{\psi_i(p)-u_i=\min_Q\left\{\sum_x[(q_x-r_x)\mathbb E_QR_A
-\operatorname{Cov}_Q(I_A,R_A)-q_x\mathbb E_Q(I_AJ_A)]-e_i(Q)\right\}.}\tag{FM}
\]

当 Q=p 时 q_x=r_x，组成错配项消失。写 H^b=E_p[R_A|I_A=b]，便得 boss20 的正确恒等式

\[
C_i(p,p)-D_i(p)
=\sum_x\left[q_x(1-q_x)(H^0-H^1)-q_x^2E_p[J_A|I_A=1]\right].\tag{DI}
\]

\(q_x\in\{0,1\}\) 时按原始无条件式处理。特别地，令 L_i(p)=C_i(p,p)-ψ_i(p)≥0，有**精确等式**

\[
\sum_i\psi_i(p)-W
=\sum_{i,x}\{q_x(1-q_x)(H^0-H^1)-q_x^2J^1\}
-\sum_ie_i(p)-\sum_iL_i(p).\tag{PATH}
\]

该等式没有给右侧符号。它对应比自由 Mpath 更强的均匀时间条件 Σ_iψ_i(p)≤W。若自由 Mpath 真失败，则其分离查询 p 对每个 i 都有 ψ_i(p)>W/m，故该 p 的 PATH 右侧必为正；这个必要诊断是有效的。

**量词边界。** 任意纯 Q 的 Cov_Q 都为零，而组成错配项一般仍在。故“只有协方差造成正债”准确限定于 Q=p 的推送账。自由菜单优化不能先去掉 (q-r) 项再让 Q 自由；要求 Q 与 p 具有相同客户边际也是额外限制，未由 minimax 保证。

## 3. 对所有查询的逐客户条件有精确旧身份

固定位置 i、客户 x，以下三项等价：

1. 对每个具有正概率覆盖/不覆盖 x 的 p，H^0≤H^1。
2. 对每个 p，该客户的同分布推送贡献满足 C_{i,x}(p,p)≤D_{i,x}(p)。
3. 每对 A∋x、B∌x 都满足 h_A(x)≤h_B(x)，等价于
   \(c_A(x)-c_B(x)\le1\)。

3⇒1⇒2 直接由倒数单调与 DI。为证 2⇒3，假设某对 a=h_A>b=h_B，取 p(A)=ε、p(B)=1−ε。置

\[
\Delta=\frac1{b+1}-\frac1{a+1}>0,\quad j=\frac1{(a+1)(a+2)}.
\]

则

\[
C_{i,x}-D_{i,x}=\epsilon(1-\epsilon)\Delta-\epsilon^2j>0
\quad\text{只要}\quad0<\epsilon<\frac\Delta{\Delta+j}.
\]

1⇒3 也可直接取这两点分布。因此 boss20 的**对所有 p**残余负载单调，恰是旧资产 `R-5c4.../global/response_debt_independent_review.md` §2 的跨覆盖枝负载增幅至多一条件 (R)，不是一个更宽的新一般策略类。该旧稿还证明 (R) 等价于对所有 p 的逐客户“平均负载分数背景”比较 D_x≥F_x；那是另一个价格对象，不能逐个 p 互换。

## 4. 旧严格后继 SPE 已明确否定自动单调

复用旧资产 [response_debt_independent_review.md](../../R-5c4f6385eec046eb9a20052facacba11/global/response_debt_independent_review.md) §6 的 8 个单位客户、两位提供者。主题

\[
A=\{x,z_1,z_2\},\quad H=\{y_1,y_2,y_3\},\quad
B=\{x,y_1,y_2,y_3\},\quad C=\{z_1,z_2,w_1,w_2\}.
\]

末位规定 A→B、H→C、B→C、C→B，全部四个末位回复均严格最佳。根收益依 A,H,B,C 为 5/2,3,4,4，根规定 B；实际 (B,C)，u=(4,4)，W=OPT=8。这是完整有序历史 SPE，允许根平局。

对根客户 x：强制 A 后 h_A(x)=1；强制 H 后 h_H(x)=0。所以任意在 A/H 上有正概率的 p 都有 H^0=1>1/2=H^1，严格失败。取 p(A)=1/4、p(H)=3/4，

\[
D_{1,x}=1/8,\quad C_{1,x}(p,p)=5/24,\quad C_{1,x}-D_{1,x}=1/12>0.
\]

但全部客户合计为

\[
D_1(p)=23/8,\quad C_1(p,p)=19/12,\quad
\psi_1(p)=35/24,\quad L_1(p)=1/8.
\]

故 C_1−D_1=−31/24<0，跨客户补偿充足。实际完整叶 (B,C) 的每个主题查询价格至多 2；所以 Mfull≤2<4，Mpath≤2<4。该例只否定自动逐客户条件，不否定任何自由菜单桥，更不是 half 反例。

## 5. 产品/minimax 接续的准确停止点

已有 PRODUCT-MENU-TIME 证明：固定 m 的全输入 Mpath 桥等价于存在跨所有实例、所有 p 的通用位置分布 λ。这里 FQ 对任意源 Q 成立，故可在该机制中保留每个位置自由选源，但它没有给 λ 或 Q。只靠逐客户单调自动化这一具体路线已失败；这不限制跨客户支付、真实离轨 IC 运输、自由源或产品分离等全输入机制。

当前有价值的未付问题仍是：对每个 p，从同一完整 SPE 的真实后继 IC 构造某个 i,Q 使 C_i(p,Q)≤W/m，或提供合法全路径预算。FQ/FM/PATH 只规定该证明需要保留的项，没有付掉任何尚缺项。

## 6. 普遍时机 λ 的无损过滤与预约提升停界

父方独立重构 FQ 确认无误后，追加要求检查 PRODUCT-MENU-TIME 的 λ 形状义务。这里先给一个全输入过滤，不作额外阴性扩样。

实际叶 a 是每个位置的合法菜单列，因为强制当前规定动作 S_i 后仍回到 a。因此对所有 p、每个 i 都有

\[
\psi_i(p)\le G_p(a),\qquad G_p(a)=\sum_x\frac{q_x}{1+c_x(a)}.\tag{ACT}
\]

故查询 p 若 G_p(a)≤W/m，则中心化向量 d_i=ψ_i(p)−W/m 的全部坐标均非正，对 λ∈Δ_m 的不等式 λ·d≤0 全冗余。特别地，若

\[
B(a):=\max_T G_T(a)\le W/m,
\]

则该实例在全部 p 上都不能限制 λ。若所有候选组件都有这个性质，任意整数复制和逐坐标产品也保留这个性质：产品实际列的 cap 恰为各组件 cap 之和，产品福利相加。产品分离不能从这些组件造出时间冲突。

这说明任何有效的有限 λ 压力提案至少需给一个合法实例查询对及某个位置 i，使 ψ_i(p)>W/m；G_p(a)>W/m 是其必要条件。该条件只作过滤，并非充分性。

对当前已知预约前缀见证，这个过滤足以排除继续做 λ-LP 的价值。原 34 客户三人实际叶 cap 为 17/2；增加不交的 J=19 客户预约主题 B、实际只用一次 B 后，完整实际叶 cap 为

\[
\max\{17/2,19/2\}=19/2<51/4=W/4.
\]

因此这个否定“非首位 u_i≥v_m”的正深度见证对自由 Mpath 的普遍 λ 义务是全冗余的。若将来存在保留旧实际叶且每个新不交 J=19 预约主题恰用一次的 k 次提升，其实际 cap 仍为 19/2，而均值为 (32+19k)/(3+k)>19/2，同样全冗余；**这里没有证明反复提升的完整 SPE 拼合存在**，也不为此另开构造项目。

已去重的旧有限工作包括 PRODUCT-MENU-TIME 所附 16 份规范证书切割平面诊断，以及 `R-4243.../independent_attack/probe_time_pressure.py/.json` 的一个旧四人完整策略锥、63 个均匀支撑查询。它们未给正坐标压力，没有被本轮重跑或扩大。现在尚无非冗余普遍 λ 约束，也无产品反例；未发现压力不能推出所有 λ 均可行。
