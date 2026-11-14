# SUMmin 条件与恰六人静态 2m 链：完整比较复核

任务：`Boss7-summin-six-half-3b-3b-17d90d43aa54c665`。本说明只交付本任务的边、阅读台账与收据；没有修改 source、registry、其它任务、Git 或原生队列，也没有运行 checkpoint、commit、push 或 map done。

## 1. 端点和问题

源对象是 `customer-attraction/e7-summin-full-common-budget-exact-discount-and-finite-tests`（当前 v2、truth open、registration pin `e37e6d0b6d0236152b44c5bd1d840157a5f2673bfcf99f9170af932a33e87332`）。它固定有限标签目录、任意人数 m、完整有序历史纯 SPE、actual 叶 z，并在实际第 i 个前缀强制 A 后沿同一 σ 的真实后继得到完整 m 槽叶 `Z_i(A)`；对同一个合法查询分布 p 定义

\[
 K_i(T,A)=\sum_{x\in T}\frac1{1+c_x(Z_i(A))},\qquad
 R_i(p)=\min_{A\in\mathcal S}\mathbb E_{T\sim p}K_i(T,A).
\]

候选 `SUMmin-full` 是 `\sum_iR_i(p)\le W` 对全部有限实例、全部完整纯 SPE σ 和全部混合 p 的共同预算。候选正文明确：纯查询已付，但混合查询的 min/expectation 不能交换，一般共同预算仍开放；有限保存 p 只作有限证据。

目标对象是 `customer-attraction/six-providers/exact-six-full-history-half-cover`（当前 v1、truth open、registration pin `2d5b191271cb052c435121a41935eb3958540d5a53cb05013f13dd45a70f6e31`）。它量化任意有限共同标签目录（允许空覆盖、同覆盖异标签、重复和所有弱平局）及全部有序历史定义的六人完整纯 SPE，要求 `2W(σ)\ge OPT_6`；原题仍开放。

## 2. 已证明的条件边

边的精确前提是：对每个有限共同目录、每份完整纯 SPE σ（先取一般 m，最后置 m=6）和每个合法混合查询 p，假设

\[
 (U)\qquad \sum_{i=1}^{m}\min_A\mathbb E_pK_i(T,A)\le W(σ).
\]

在此前提下，静态 2m 链是完整的：

1. 置 `R_i(p)=min_A E_p K_i(T,A)`。由 (U)，对每个 p 有 `min_iR_i(p)\le W/m`。
2. 令有限完整路径菜单为 `\mathcal M_σ=\{Z_i(A):i,A\}`，并令
   \[
   M_{path}=\max_{p\in\Delta(\mathcal S)}\min_{i,A}\mathbb E_pK_i(T,A).
   \]
   这是有限矩阵的 max-min；minimax 给出等价的列混合表述 `M_path=\min_Q\max_T E_Q\sum_{x\in T}(1+c_x(y))^{-1}`，其中 Q 只在菜单终局 `Z_i(A)` 上取值。故 (U) 给 `M_path\le W/m`。
3. 任取任意合法 m 槽静态背景分布 Q（不要求来自 SPE），写 `L_x=E_Qc_x(y)`、`a_A=m^{-1}E_Q[#\{j:y_j=A\}]`，于是 `L_x=m\sum_{A\ni x}a_A`。定义
   \[
   f_L(T)=\sum_{x\in T}(1+L_x)^{-1},\qquad M_L=\max_Tf_L(T).
   \]
   对任意 m 个比较主题 `T_1,…,T_m`，并集 O 的逐客户分解给出
   \[
   |O|\le\sum_{j=1}^mf_L(T_j)+\sum_x\frac{L_x}{1+L_x}
   =\sum_{j=1}^mf_L(T_j)+m\sum_Aa_Af_L(A)\le2mM_L.
   \]
   这里第二项正是 m 个竞争槽的总平均，不是 m−1 个竞争槽。
4. 倒数函数凸，逐客户 Jensen 给 `f_L(T)\le E_Q\sum_{x\in T}(1+c_x(y))^{-1}`。令 `v_{m+1}(0)` 为所有合法 m 槽静态背景分布的有限安全值 `min_Q max_T E_QK(T,y)`，则静态分解得到 `OPT_m\le2m v_{m+1}(0)`。
5. 路径菜单只是全部合法 m 槽背景的子集，故 `v_{m+1}(0)\le M_path`。合并为
   \[
   OPT_m\le2m v_{m+1}(0)\le2mM_{path}\le2W.
   \]
   对 m=6，`2m=12`，于是 `OPT_6\le12(W/6)=2W`，正好是六人 half 目标。

这一推导只把 (U) 当作前提；它没有把路径菜单误当作全静态背景，也没有把一个静态背景误称为顺序 SPE。零客户、全目录零覆盖或 `OPT_6=0` 时按模型约定直接成立，不取 `0/0`。

## 3. 纯 p 的逐行证明和混合缺口

若 `p=δ_T` 是纯查询，对每个 i 取强制列 `A=T`，则

\[
R_i(δ_T)\le K_i(T,T)
=\sum_{x\in T}\frac1{1+c_x(Z_i(T))}
\le\sum_{x\in T}\frac1{c_x(Z_i(T))}
=u_i(Z_i(T))\le u_i(z).
\]

第二个不等式的分母正性来自强制者本人覆盖 T；最后一个不等式正是原 actual 前缀处的完整纯 SPE 偏离约束，且偏离后继沿同一 σ 的真实改变历史完成。故纯点逐行求和确实给 `\sum_iR_i(δ_T)\le W`。

混合 p 时却不能把各个 T 的上述列选择平均：一般只有

\[
\min_A\mathbb E_pK_i(T,A)\ \ge\ \mathbb E_p\min_AK_i(T,A),
\]

而不是等号。纯证明为每个被查询 T 选择 `A=T`，选择依赖 T；`R_i(p)` 要求在抽样 T 公开前固定同一个 A，且该列可以依 i、p 变化但不能依实际抽样变化。候选页、末位精确引理及五人程序合同都明确保留这一未证的 min/expectation 交换缺口。五份保存 p 的精确负余量以及浮点锥探针只属有限固定策略/固定 p 观测，不覆盖全部 p、全部目录或全部完整 σ。

## 4. 边界：不能升级的结论

* 该边是 `relation_mode: conditional`：条件 (U) 下到六人 half 的推导已完整，(U) 本身仍是 open candidate。因此不能填写“已证明 SUMmin”，也不能把目标六人原题的 `truth_status` 改为 proved。
* 静态计数恰有 m 个比较主题与 m 个竞争槽，第二个 m 来自 `m\sum_Aa_Af_L(A)`。当前证书没有删去强制者或证明 m−1 竞争槽的共同付款，所以不能把 `2m` 改写成锐的 `2m−1`；任何 `2m−1` 断言都需要另一个静态接口和动态支付证明。
* 末位公式 `R_m(p)=G_b(p)-\max_AD_b^p(A)` 只支付末位。早期强制会改变全部真实后继，不能机械递推末位折扣到全部 i；不能把末两位储备或五人有限探针当作全路径共同预算。
* 有限 p/浮点锥搜索、静态 PNE 或固定离轨终局均不替代“每个有限目录、每份完整历史纯 SPE、每个混合 p”的量词；没有独立的 SUMmin 全称证明或六人反例。

因此本包交付唯一数学关系：`SUMmin-full (作为共同预算前提) ⇒ six-provider exact-half target`，承重前提为 ALL 的完整模型量词和静态 2m 证明；其余仍明确保留。
