---
id: "customer-attraction/full-slot-mean-cap-original-source-norm-ledger"
kind: "lemma"
type_tag: "引理"
title: "完整槽均值cap的原源范数账与付款接口"
status: "proved-exact-ledger-and-calibration; covariance-payment-open"
summary: "完整槽可信端点均值cap对偶围绕同一完整背景展开原删除槽查询，保m‖ρt‖²与精确税相消；静态系数是2m，FPAY金额及低密度共同付款未证。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/aggregate/full_slot_cap_dual_norm_bank.md"
---

# 域和原source各自固定

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)，任意 m≥1、有限单位客户、有限非空目录和每份完整有序历史纯SPE σ。保空主题、重复、零客户与任意离轨平局。实际前缀 h_i、实际收益 u_i、W=Σ_i u_i 固定。

一行候选端点 (A,e) 在 h_i 强制 A 后采用某份真实完整孩子纯SPE；原实际行动标签只允许其原实际端点。写 d_i(A,e) 为进入收益，ell_i(A,e) 为删除同一 i 槽的负载，C_i=ell_i+1_A 为完整负载。定义有限凸分析域

\[
D_i^+=\{E_q C_i(A,e):E_qd_i(A,e)\le u_i\},\qquad
K^+=\frac1m\sum_iD_i^+.
\]

每行 q 归一；背景行动质量 m，非 m−1。端点各自可信，不要求同一 q 的彩票为可执行SPE；原 σ 给非空可行点。此处没有释放实际标签到全部raw叶，也没有引入未来均值floor或统一NET-cap。和[规范门槛均值域](规范门槛均值域与复制偏离的精确成本--引理.md)是不同域。

令 (p,L^+) 是 max_p min_{L∈K+} E_p Σ_{x∈A}(1+L_x)^{-1} 的联合鞍点。置 t_x=(1+L_x^+)^{-1}、ρ_x=Pr_p[x∈A]、w_x=ρ_xt_x²，γ=Σ_xρ_xt_x。所有主题t价格≤γ，p支持的主题等于γ。凸一阶条件给 L^+ 最大化 w·L，所以

\[
H_i^+=\max_{D_i^+}w\cdot C,
\qquad\sum_iH_i^+=m\,w\cdot L^+.
\]

每行均值cap的有限LP对偶给 μ_i≥0、η_i及

\[
H_i^+=\eta_i+\mu_i u_i,\qquad
\eta_i+\mu_i d_i(A,e)\ge w\cdot C_i(A,e).
\tag{FCAP-DUAL}
\]

源始终是原 σ 的 ell_i^0(A)、d_i^0(A)，不是所选端点彩票。原完整IC给 I_i=u_i−E_p d_i^0≥0，原源的约化成本 R_i^+(A)=η_i+μ_i d_i^0−w·C_i^0≥0，故

\[
G^+=\sum_i[H_i^+-E_pw\cdot C_i^0]
=\sum_i\mu_iI_i+\sum_iE_pR_i^+\ge0.\tag{FCAP}
\]

# 用完整背景展开原删除槽查询

所有以下量都围绕**同一** L^+，不得换成各自最优删除槽背景。定义

\[
\mathrm{Cov}_0=\sum_{i,x}t_x^2\operatorname{Cov}_p
                    (\mathbf1_{x\in A},\ell_i^0(A)_x),
\]
\[
D_0=\sum_iE_p\sum_{x\in A}
\frac{t_x^2(\ell_i^0(A)_x-L_x^+)^2}{1+\ell_i^0(A)_x}\ge0.
\]

倒数精确展开为

\[
\frac1{1+\ell}=t-t^2(\ell-L^+)
                  +\frac{t^2(\ell-L^+)^2}{1+\ell}.
\]

对原source及角色求和，用 E_p 1_A t²ell = w E_pell + Cov 的逐坐标分拆，再用 C_i^0=ell_i^0+1_A 与 Σ_iH_i^+=m w·L^+，得到

\[
\boxed{W-m\gamma=\sum_i(1+\mu_i)I_i+\sum_iE_pR_i^+
                    +D_0-\mathrm{Cov}_0+m\|\rho t\|_2^2.}\tag{FNORM}
\]

最后项因每行 E_p[w·1_A]=Σ_xρ_x²t_x² 而来，系数是 mρ²，不能误作 mρ。原I及对偶残差是一次同源库存，未作逐客户重权IC。

若 Cov_+、D_+ 改用完整源 C_i^0、仍围绕相同 L^+，令

\[
\mathrm{Tax}=\sum_iE_p\sum_{x\in A}
\frac1{(1+\ell_i^0(A)_x)(2+\ell_i^0(A)_x)},
\]

同一个倒数展开逐项相减给

\[
\mathrm{Cov}_+=\mathrm{Cov}_0+m\sum_x\rho_x(1-\rho_x)t_x^2,
\quad D_+=D_0+m\sum_x\rho_xt_x^2-\mathrm{Tax},
\]
\[
\mathrm{Tax}+D_+-\mathrm{Cov}_+
=D_0-\mathrm{Cov}_0+m\|\rho t\|_2^2.\tag{ONE-BANK}
\]

Tax、Bregman差和范数是同一账的不同写法，不能相加领三份信用。

# 完整槽静态比较及未证金额

L^+ 为行动质量 m 的目录分数负载，因此

\[
Q^+=m\gamma-\sum_xL_x^+t_x\ge0,
\qquad \mathrm{OPT}_m\le m\gamma+\sum_xL_x^+t_x
=2m\gamma-Q^+.
\tag{FULL-STATIC}
\]

证明后一式：对最优 m 主题的覆盖计数 c_x^*，逐客户 1_{c_x^*>0}≤(c_x^*+L_x^+)/(1+L_x^+)，再对各最优主题价格用 γ。静态系数是 2m，不是删除槽的2m−1。

因而下列为足够但**未证明**的付款接口：

\[
\mathrm{Cov}_0\le\sum_i(1+\mu_i)I_i+\sum_iE_pR_i^+
                    +D_0+m\|\rho t\|_2^2+Q^+/2.\tag{FPAY?}
\]

若成立，(FNORM)给 W≥mγ−Q^+/2，联合(FULL-STATIC)即half。Q^+>0时无需先证 W≥mγ；也不能把不同域的较小γ与较小静态系数免费拼接。对应的完整/删除槽端点域之间，给同一端点彩票加回当前行动负载可得 γ^+≤γ^-；这不改变各自静态系数和付款金额。

置 z_x=ρ_xt_x，γ=Σ_xz_x。z_x≥1/(2m)的坐标有 mz_x²≥z_x/2，低z部分缺口为 Σ(z_x/2−mz_x²)。低z不意味着私有客户、独立槽位或已有共同付款；(FCAP)只控制共同w，Cov_0仍用条件源指示，二者的低密度自适应金额没有由这些式子桥接。

# 任意人数校准族与全部精确值

取一个含m客户的大主题 B，另有 m−1 个互不交且与B不交的单客户主题。每个有序历史都选 B 是完整纯SPE：任意历史下现在选B后其最终覆盖者至多m，收益至少1，改选单例至多1。实际 W=m、每人 u_i=1，最优 m 主题覆盖2m−1。

强制任一单例后全B尾可信，进入者收益1；强制B也收益1。每行使用同一彩票

\[
p_B=\frac m{2m-1},\quad p_{\rm single}=\frac1{2m-1},\quad
\gamma=\frac{2m-1}{2m},\quad
t_B=\frac{2m-1}{2m^2},\quad t_{\rm single}=\frac{2m-1}{2m}.
\]

它产生 L_B^+=m−1+p_B、每单例L^+=p_single；全部主题价格同为γ，且梯度w的各主题价格也相等。这同时认证无约束完整分数目录背景的凸鞍点；该彩票在本cap域中可行，故也是本域鞍点。每客户 z_x=1/(2m)，原删除槽源恒为 (m−1)B，直接得到

\[
\mathrm{Cov}_0=I=R^+=Q^+=0,\quad
m\|z\|^2=\gamma/2,\quad D_0=1/(4m),\quad
W-m\gamma=1/2=m\|z\|^2+D_0.
\]

m=5给γ=9/10、范数9/20、D_0=1/20、OPT_5=9；m=6直接代入给γ=11/12、范数11/24、D_0=1/24、OPT_6=11。它是一个一般族的校准，既非任意实例half证明，亦非六人目标反例。

# 实读、关系和接续

主源6255字节全文实读；逐式重构FCAP、FNORM、ONE-BANK及静态充分接口，直接核校准族的完整历史IC、背景实现和所有显示值。无程序源，无新有限扫描；原tree/credible内部核符号和mρ²系数，不构成FPAY认证或外部新颖性。原稿已明确完整槽插入折扣/付款机制来自先有材料，本页只保本源展开，未宣称整套机制首次提出。原件及指纹见[证据](../../tools/evidence/prefix-fullslot-primary/README.md)。

本页接[固定过去折扣分解](原策略菜单的固定过去负载与静态折扣分解--引理.md)的价值压力之后，但改变分析域，不能继承其固定P下界到自由选择的可信端点。与[真实重放付款问题](../问题/真实重放协方差的定量付款--问题.md)相连的是完整/删除槽自交叠库存的明确身份，非逐边IC或额外第二份银行。原历史OPEN不覆盖现行另证五人定理；六人每份完整纯SPE的付款缺口仍未闭合。正式超图留第三阶段。
