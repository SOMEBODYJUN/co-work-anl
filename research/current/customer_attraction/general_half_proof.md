# 一般半覆盖证明工作稿：通用关系与尚未闭合的步骤

2026-10-23。目标身份 **Q-CAG-HALF**，状态 **OPEN**。本稿把已经成立的全范围关系接成可直接修改的数学推导，并在尚未证明的连接处停止。它不是完整证明，也不把某条充分路线规定为必须采用的方法。原模型、已有引理、反例与独立审查各自以所链接正文为唯一来源；本稿的重述不新增其证明状态或新颖性声明。

## 1. 固定实例、完整策略和待证不等式

采用 [CAG-MODEL](model.md)。有限单位客户集 N，有限非空共同目录 S⊆2^N，m≥1 位单位提供者依次各选一次主题，允许空主题和重复选择。每位观察全部有序历史；纯策略 σ 在每个合法有序历史独立指定行动，任意平局均保留。

对完整终局 z=(S_1,…,S_m)，记

\[
c_x(z)=\sum_{i=1}^m\mathbf1_{x\in S_i},\qquad
u_i(z)=\sum_{x\in S_i}\frac1{c_x(z)},\qquad
W(z)=\left|\bigcup_iS_i\right|=\sum_i u_i(z).
\tag{1}
\]

固定**任意一份完整历史依赖纯 SPE** σ，实际根终局记为 z，实际最终收益为 u_i。固定任意 m 个合法比较主题 T_1,…,T_m，令

\[
C=\bigcup_{j=1}^m T_j,\qquad O=|C|.
\]

欲对每个这样的比较元组证明

\[
\boxed{2W\ge O.}\tag{Q}
\]

然后取最大比较联合便得到原目标 `2W≥OPT_m`。比较主题允许重复；少于 m 个主题的组合可重复补齐。m=1 时实际主题最大，W=OPT_1。若 W=0，根改任意主题 T 的收益至少 |T|/m，根最优性迫使所有主题为空，故 OPT_m=0。以下可设 m≥2、O>0；整个论证不需要定义零福利效率比。

### 全部真实 SPE 行

对任意长度 i−1 的有序历史 h 和任意合法主题 A，记 Z_h 为从 h 沿 σ 得到的完整终局，Z_{h,A} 为在 h 强制当前玩家选 A、以后沿**同一份原 σ** 得到的完整终局。定义

\[
\Gamma_{h,A}=u_i(Z_h)-u_i(Z_{h,A})\ge0.
\tag{2}
\]

(2) 是本稿所有动态比较的依据。Z_{h,A} 中全部后继都可改变行动；过去固定，后继不冻结。相同客户负载的两个有序历史不必具有相同指定续局。下文若只保留计数，必须保留的是可实现续局的全集，不能据此改写 σ。

## 2. 从真实行得到的无条件保证

在任意历史 h，令 b_x 为已行动者的客户负载，尚有 r 位玩家。当前改选 T 后，x∈T 的最终负载最多为 b_x+r，所以由(2)

\[
\boxed{u_{\mathrm{current}}\ge
\max_{T\in S}\sum_{x\in T}\frac1{b_x+r}.}
\tag{3}
\]

这个下界对任意真实后继均有效，因而不需要在不同分支间搬动策略。任意历史都有 b_x+r≤m，故若 K=max_T|T|，则每个实际玩家 u_i≥K/m，进而 W≥K≥OPT_m/m。这是全范围弱保证；常数随 m 变化。

另一个反复可用的事实是：在**同一个终局**中选择相同主题的两位单位玩家收益完全相等。若在某个偏离分支中复制了已固定的主题，可以使用这个同枝等式；不能把该分支的旧玩家收益替换为原根路径的旧玩家收益。原始推导及失败边界见[续局引理](continuation_lemmas.md)。

### 同背景的末两人恒等式

固定任意合法前缀背景 b，恰剩两人。写

\[
F_b(A)=\sum_{x\in A}\frac1{b_x+1},\quad
U_b(A,B)=\sum_{x\in A}\frac1{b_x+1+\mathbf1_{x\in B}}.
\]

逐客户消去共同项可得

\[
U_b(A,B)-U_b(B,A)=F_b(A)-F_b(B).
\tag{4}
\]

令 `θ_2(b)=min_A max_B U_b(B,A)`。若 A 最大化 F_b，则对其后原策略的任意末位最佳回复 B，有

\[
U_b(A,B)\ge U_b(B,A)\ge\theta_2(b).
\]

倒二玩家可以合法改选这个 A，故任意完整 SPE 的末两人各至少获得 θ_2(b)。这个结论适用于任意 m 的每个倒二历史；它没有把 θ 保底推广给更早玩家。

还可保留全部末位回复的信用。令 B(A) 为当前选 A 后的真实末位回复。对独立 A,A'∼p，末位真实最优性给

\[
L(A,A')=U_b(B(A),A)-U_b(B(A'),A)\ge0,
\]

而(4)中的对称交项给精确恒等式

\[
\mathbb E_AU_b(A,B(A))-
\mathbb E_{A,A'}U_b(A,B(A'))
=\mathbb E L(A,A')\ge0.
\tag{5}
\]

这是任意背景、任意 p、任意历史平局的一后继去相关；整组后继不能由一个玩家作为单一行动选择，所以不能把(5)直接推广到任意剩余人数。唯一正文见[末两人保底](last_two_floor.md)与[自适应后继边界 §2](continuation_security_barriers.md)。

## 3. 已闭合的真实路径跨位置预算

令 P_i=Σ_{j≤i}u_j，P_0=0。对比较集 C 取任意分数覆盖 `z_T≥0`，满足

\[
a_x=\sum_{T\ni x}z_T\ge1\quad(x\in C),\qquad
\tau=\sum_Tz_T\ge1.
\tag{6}
\]

这些权重只组合合法偏离，不改变玩家行为或单位客户模型。在实际位置 i，令 r=m−i+1，b_i(x) 为真实前 i−1 人的负载，并定义截取到 C 的价格

\[
g_i(T)=\sum_{x\in T\cap C}\frac1{b_i(x)+r}.
\]

由(3)，每个合法 T 都有 g_i(T)≤u_i。另一方面逐客户有

\[
\begin{aligned}
O
&\le\sum_{x\in C}\frac{b_i(x)+r a_x}{b_i(x)+r}\\
&=\sum_{j<i}g_i(S_j)+r\sum_Tz_Tg_i(T).
\end{aligned}\tag{7}
\]

现在使用真实旧玩家的**最终利润**支付前一项。真实终局负载 c_x(z)≤b_i(x)+r；对 j<i，S_j 上的相关 c_x≥1，故

\[
g_i(S_j)\le\sum_{x\in S_j\cap C}\frac1{c_x(z)}\le u_j.
\]

将其代入(7)，得到对全部实例、全部 i 成立的前缀利润关系

\[
\boxed{O\le P_{i-1}+r\tau u_i.}\tag{8}
\]

这里旧利润和当前偏离下界都来自原同一实例；没有对离轨旧玩家利润作跨枝替换。

由(8)，

\[
P_i\ge\left(1-\frac1{r\tau}\right)P_{i-1}+\frac O{r\tau}.
\]

各系数非负，因此从 P_0=0 迭代即得

\[
\boxed{W\ge O F_m(\tau),\qquad
F_m(\tau)=1-\prod_{r=1}^m\left(1-\frac1{r\tau}\right).}\tag{9}
\]

即使 P_i>O，也不影响方向：可对 O−P_i 使用同一非负系数递推，不假定余额逐步非负。原唯一正文及完整边界见[分数覆盖的真实前缀利润预算](fractional_cover_path_budget.md)。

### 将(9)应用到任意最优比较联合

C 是 m 个比较主题的并集，所以这些主题各取权一就给 τ≤m 的覆盖。F_m 随 τ 非增，因此所有实例无条件满足

\[
\boxed{W\ge\operatorname{OPT}_m
\left[1-\prod_{r=1}^m\left(1-\frac1{rm}\right)\right].}\tag{10}
\]

这已经是一条一般 m、一般目录的完整推导，但不是(Q)：`F_m(m)∼H_m/m→0`。更好的比较分数覆盖若满足

\[
\prod_{r=1}^m\left(1-\frac1{r\tau_C}\right)\le\frac12,
\tag{11}
\]

则(9)已经闭合(Q)。一般输入没有已证的统一 τ_C 上界使(11)必然成立。

**第一个明确断点。** (8)—(10)没有利用足够的真实后继理性，尤其没有支付可能随人数增长的比较覆盖复杂度。要沿这条连续推导完成(Q)，需要新的通用信用、不变量或比(8)更强的跨位置关系；不能把 τ_C≤m 误读成(11)。

### 3.1 冻结真实前缀的联合客户席位：一般付款的精细加强

**`CA-PREFIX-COUPLED-SEAT-BUDGET-v1`。** 以下对任意原模型输入及每个完整历史纯 SPE 成立，不给目录或人数加结构限制。不同极大主题记为 B_j，固定实际并集 C，取其实际遗漏全局私有块

\[
Q_j=\left(B_j\setminus\bigcup_{\ell\ne j}B_\ell\right)\setminus C,
\qquad a_j=|Q_j|.
\]

在实际位置 i，冻结真实旧负载 b=b_i 与剩余人数 r=m−i+1。对 1≤k≤r 令

\[
G_j(k)=\frac{a_j}{k}+\sum_{x\in B_j\setminus Q_j}\frac1{b_x+r},
\]

\[
F_j(k)=\min_{\substack{Y\in S^{r-1}\\
\#\{\ell:Y_\ell\cap Q_j\ne\varnothing\}\le k-1}}
\sum_{x\in B_j}\frac1{b_x+1+c_x(Y)}.
\tag{PJS-1}
\]

竞争元组的约束非空：任一实际主题都避开 Q_j，可重复补齐；r=1 使用空元组。逐客户有 F_j(k)≥G_j(k)，两序列均非增。记全部 j,k 的 F 席位第 r 大为 Λ_i、G 席位第 r 大为 λ_i，则

\[
\boxed{u_i\ge\Lambda_i\ge\lambda_i,\qquad
W\ge\sum_i\Lambda_i\ge\sum_i\lambda_i.}
\tag{PJS-2}
\]

**真正使用完整后继的步骤。** 在这一冻结子树内固定阈值 z，令 d_j 为 F_j(k)≥z 的席位数，q_j 为新增历史中触及 Q_j 的动作数。每个合法动作至多触及一个 Q_j，所以剩余容量 Σ_j(d_j−q_j)_+ 每步至多降一。当前选一个有剩余席位的完整 B_j：若未来触及 Q_j，该后来主题包含于 B_j，当前偏离者同叶收益支配后来者，后者由全历史深度归纳达到 z；若未来不触及 Q_j，则当前之外的 r−1 个真实主题是 F_j(q_j+1) 的可行元组，仍达 z。SPE 当前比较遂支付规定收益。归纳始终固定初始 b、r、F，不冻结后继或合并有序历史。取第 r 大阈值即得(PJS-2)，零阈值用非负性处理。

这一预算在**同一项完整利润**中同时计入私有遗漏、共享遗漏和已覆盖客户，仅由同一个 u_i 付款一次。它逐位置不弱于旧固定分母私有谱与(3)的最大值；有完整 SPE 的严格增强例已由另一实现展开单位客户、重构完整策略并逐历史复核。一般性来自上述归纳，不来自该有限例。

**没有完成的连接。** 若全部 Q_j 为空，则复制 B_j 共 r−1 次即可让其所有客户达到分母 b_x+r，故 F=G，整个谱准确退回(3)。尚未证明 ΣΛ_i≥OPT_m/2 或 OPT_m−W≤ΣΛ_i。因此这是一般路径预算的一项强化，未扩大原目标已证范围，不能称共享遗漏已经解决。

完整[定义与证明](../../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/continuation_general/omission/prefix_coupled_seat_budget.md)、[先盲重构 G 后读稿检查 F 的内部审查](../../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/continuation_general/induction/private_offset_spectrum_independent_review.md)、[独立有限证据审查](../../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/continuation_general/menu/refined_spectrum_numerical_review.md)分别保留准确范围。该机制承接已有超集席位归纳；没有外审或新颖性认证。

## 4. 独立成立的静态安全值与最优覆盖比较

固定任意合法前缀负载 b 和剩余人数 r≥1，定义真正静态安全值

\[
v_r(b)=\max_{p\in\Delta(S)}\min_{B\in S^{r-1}}
\sum_Ap_A\sum_{x\in A}\frac1{b_x+1+c_x(B)}.
\tag{12}
\]

静态竞争元组 B 可以内部任意相关，但**不观察查询 A 的抽样实现**。它不是顺序玩家可以隐藏执行的混合承诺。目录有限，有限 minimax 给

\[
v_r(b)=\min_{Q\in\Delta(S^{r-1})}\max_A
\mathbb E_Q\sum_{x\in A}\frac1{b_x+1+c_x(B)}.
\tag{13}
\]

下面只对空背景证明覆盖比较。固定 s≥1 个静态竞争槽的任意联合分布 Q，令

\[
L_x=\mathbb E_Qc_x(B),\quad
q_T=\frac1s\mathbb E_Q\#\{j:B_j=T\},\quad
g(T)=\sum_{x\in T}\frac1{1+L_x},\quad M=\max_Tg(T).
\]

则 `L_x=sΣ_{T∋x}q_T`。对任意 m 个比较主题，其覆盖重数为 d_x；逐客户有

\[
\mathbf1_{d_x>0}\le\frac{d_x+L_x}{1+L_x}.
\]

求和并使用共同目录，得到

\[
\begin{aligned}
O&\le\sum_{j=1}^m g(T_j)+\sum_x\frac{L_x}{1+L_x}\\
&=\sum_{j=1}^m g(T_j)+s\sum_Tq_Tg(T)\le(m+s)M.
\end{aligned}
\]

reciprocal 凸性给 `g(T)≤E_Q f_B(T)`，故对 Q 极小化、使用(13)，可得

\[
\boxed{\operatorname{OPT}_m\le(m+s)v_{s+1}(0).}\tag{14}
\]

特别是

\[
\boxed{\operatorname{OPT}_m\le(2m-1)v_m(0),\qquad
\operatorname{OPT}_m\le2m v_{m+1}(0).}\tag{15}
\]

s=0 时直接为 `OPT_m≤m max_T|T|=m v_1(0)`。上述一般 s 写法只是同一共同目录预算的直接形式；核心来源为[不观察查询的混合安全值](oblivious_security.md)，额外一槽的直接比较亦见[完整根菜单义务](../../workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/induction/full_root_menu_mixed_obligations.md)。

(14)—(15)不使用 SPE 理性，不能单独支付任何早期玩家收益。`θ_m=min_B max_A f_B(A)` 与 `v_m=max_p min_B E_p f_B(A)` 的量词不同，只有 v_m≤θ_m；末两人的 θ 保底不推出全员 θ 保底或 W≥mθ_m。

### iid Nash 福利值不能替换真正安全值

为避免把两种静态基准混同，明确记录已经失败的 iid 替换。对目录分布 q，令 `q_x=Σ_(T∋x)q_T`，定义

\[
\Phi_m^{\mathrm{iid}}(q)=\sum_x\mathbb E H_{\mathrm{Bin}(m,q_x)},\qquad
\Psi_m(q)=\sum_x[1-(1-q_x)^m].
\]

这里 H 是调和数；Φ 与第3节的乘积函数 F_m(τ) 不同。任意 Φ 最大者 q* 是静态对称混合 Nash；所有最大者有同一 Ψ 值，记作 `Z_m=Ψ_m(q*)`。它不是任意 q 的最大期望覆盖。已证静态关系为 `m v_m≤Z_m≤OPT_m`，原定义见[iid 安全基准](iid_security_and_flow_barriers.md)。

强桥 `W≥Z_m` 和较弱的充分桥

\[
W\ge\left(1-\frac1{2m}\right)Z_m
\]

**均已被合法完整 SPE 否定，不能列为开放候选。** 后一桥的原个人正文与独审采用的恰是上述同一个 Z_m：令 A 含2名 core 客户，B 含2(m−1)名不交客户，另有100个主题 `Q_j=A∪{c_j}`、各带一名不同私有客户，共102个主题。其完整 SPE 实际为 `A,B^(m−1)`，W=2m；m=20 时 OPT_20=59 且 `(39/40)Z_20>40`，固定100个花瓣还给每个 m≥41 的严格反例。全部有序历史策略分类、严格有理分离及一般人数估计见[弱 iid 反族原文](../../workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/security/weak_iid_bridge_counterexample.md)和[盲独立审查](../../workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/credible/weak_iid_independent_review.md)。

这个反族没有否定真正安全值桥：静态竞争背景 `A,B^(m−2)` 对查询 A、B、任意 Q_j 的收益分别为1、2、2，因此 v_m≤2，实际反而满足 `W=2m≥m v_m`。Z_m/m 可以严格大于 v_m；不能由 iid 桥失败推断第5节的安全值候选失败。

相应地，[动态 iid 债务](dynamic_iid_debt_boundary.md)中的望远镜恒等式 `Σ_h D_h=Z_m−W` 继续成立，但与弱 iid 桥等价的普遍上界 `Σ_h D_h≤Z_m/(2m)` 已被同一反族否定。局部反例不必然否定全局桥的逻辑仍正确；此处已有独立的完整全局反例，所以不能继续把该上界称为未决义务。

## 5. 真实路径上的安全值链：恒等式与缺失预算

沿实际路径，令 b_i 为前 i−1 人负载、r_i=m−i+1，并写

\[
V_i=v_{r_i}(b_i),\qquad s=v_m(0).
\]

对每个合法主题 A 和 r≥2，固定 A 后允许的静态背景只是原背景集合的一部分，因而

\[
v_{r-1}(b+\mathbf1_A)\ge v_r(b).
\tag{16}
\]

所以 `V_1≤…≤V_m`，末位实际最佳回复还给 `V_m=u_m`。定义

\[
D_i=u_i+(m-i)V_{i+1}-(m-i+1)V_i\quad(i<m).
\]

望远镜相消得到已证精确恒等式

\[
\boxed{\sum_{i<m}D_i=W-mv_m(0).}\tag{17}
\]

由(15)，若能另证

\[
\boxed{\sum_{i<m}D_i\ge-\tfrac12v_m(0),}
\quad\text{即}\quad W\ge(m-\tfrac12)v_m(0),
\tag{18?}
\]

即可推出(Q)。更强的 `W≥m v_m(0)` 也充分。

**第二个明确断点。** (18?)及更强聚合桥均未证明；它们可能比(Q)更强。各步 D_i≥0 已被完整 SPE 反驳，不能作为归纳前提。逐人 `u_i≥v_m(0)` 同样已被反驳。原唯一正文见[安全值链及局部边界](security_chain_and_local_boundary.md)、[逐人安全值反例](individual_security_counterexample.md)。

### 把缺失信用写成真实菜单去相关

在实际位置 i 强制 A 后，令 B_i(A) 为完整终局删除当前玩家之后的 m−1 个竞争主题，包含固定过去和真实后继。对任意查询分布 p，定义

\[
\mathcal D_i(p)=\mathbb E_A f_{B_i(A)}(A),\quad
\mathcal C_i(p)=\mathbb E_{A,A'} f_{B_i(A')}(A),
\]

其中 A,A' 独立同分布 p。令 $e_i=u_i−\mathcal D_i\ge0$、$\kappa_i=\mathcal D_i−\mathcal C_i$，则

\[
\boxed{W-\sum_i\mathcal C_i(p)=\sum_i e_i(p)+\sum_i\kappa_i(p).}\tag{19}
\]

每个 $\mathcal C_i$ 都是在合法 m−1 槽背景上独立查询，所以 `Ccal_i(p)≥min_B E_p f_B`。若存在一个安全最优 p，使(19)右边非负，就得到强聚合桥。

这里的“若”尚未闭合。对全部 p 要求右边非负已有完整 SPE 反例；即使加上节点最优性的松弛 e_i，也不能消除这一失败。只对合适安全最优 p 的总支付仍是不同义务。参见[总去相关预算边界](global_security_budget_boundaries.md)。

## 6. 在任意深度保留真实信用时，已经可用的通用工具

这一节的关系适用于一般模型，但不是新增福利下界。它们说明推导中哪些策略拼合、承诺和终局代数可以合法使用。

### 6.1 路径承诺只限制要实现的终局，旁枝威胁必须重置

令 R(h) 为历史 h 后全部完整纯 SPE 可实现终局集合。若 Π 是祖先收益上限、低福利等**终局条件**，置 `C(h,Π)=R(h)∩Π`。当前玩家在各孩子的不受限最低收益为

\[
\ell_A(h)=\min_{z\in R(h,A)}u_i(z),\qquad M(h)=\max_A\ell_A(h).
\]

则精确地

\[
\boxed{C(h,\Pi)=\bigcup_A
\{z\in C((h,A),\Pi):u_i(z)\ge M(h)\}.}\tag{20}
\]

必要性来自真实子 SPE 与当前比较；充分性则为选定孩子实现 z，对每个其他有序孩子独立选达到其 ℓ_A 的子 SPE，然后拼合。旁枝不需要满足 Π，因而(20)中的 M 不能用受 Π 限制的孩子重算。

这是[可信续局全集拼合](credible_continuations.md)的约束查询形式；具体重置义务见[祖先承诺正文](../../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/full_depth/ancestor_promises_and_reset.md)。它保留全部深度的真实理性，却没有给小状态或福利支付。不能因能够精确表达 R(h)，就把(Q)视为完成。

### 6.2 不交客户的 Cartesian 产品保留完整 SPE

若若干同人数实例客户宇宙互不相交，新目录取各组件主题的全部 Cartesian 组合，并在每个完整产品历史逐坐标执行组件策略，则任意联合行动偏离的收益增量等于各组件合法偏离增量之和。因此组件都是完整 SPE 时，产品也是完整 SPE；全部离轨历史均被验证。

在这种完整目录中 `W_prod=ΣW_k`、`OPT_prod,m=ΣOPT_k,m`，后者因为各组件最优 m 元组可以按位置任意配对。这个引理只构造产品策略，不声称任意产品 SPE 都分解。原文见[产品表示 P1](../../workspaces/customer-attraction/R-24bfbfd5ec7845b79374a1938c335df7/representation_product/product_representation.md)。它可检验候选预算的相容性，不能把组件间独立性免费扩展为一般交叠目录。

### 6.3 分数尾水位：一个终局内的全目录共同查询信用

固定任意整数背景负载 b、一个单位根 A、n 个单位尾主题 S_j 及阈值 t≥0。令辅助尾权 w_j∈[0,1]，`a_x=1_A(x)`、`c_x(w)=Σ_j w_j1_(x∈S_j)`。正权尾的单位密度、根利润分别为

\[
U_j(w)=\sum_{x\in S_j}\frac1{b_x+a_x+c_x(w)},\quad
R(w)=\sum_{x\in A}\frac1{b_x+a_x+c_x(w)}.
\]

初态 w=1，`u_j=U_j(1)`，低尾总缺口 `D=Σ_j(t−u_j)_+`。存在同一 w*，保持原覆盖支撑，所有正权尾密度 U_j(w*)≥t，原来 u_j≥t 的尾保持权一。更重要的是**同一个逐客户池**

\[
H=\sum_x\left[\frac1{b_x+1+c_x(w^*)}
-\frac1{b_x+1+c_x(1)}\right]\le D
\tag{21}
\]

同时支付任意客户子集 T 的两种查询增量：

\[
\begin{aligned}
Q_T(w)&=\sum_{x\in T}\frac1{b_x+1+c_x(w)},\\
J_T(w)&=\sum_{x\in T}\frac1{b_x+1+a_x+c_x(w)},\\
0&\le Q_T(w^*)-Q_T(1)\le H,\\
0&\le J_T(w^*)-J_T(1)\le H.
\end{aligned}\tag{22}
\]

Q 移除旧根再放入查询；J 保留旧根另加查询。H 不是每个主题各得一份的信用。

关键构造是逐尾单遍降权：当前 U_j<t 时，降低自身权到首次达到 t，或在有限零端点停止。其余降权只提高已处理密度。若 j 是某客户唯一覆盖者，自身权趋零时密度发散，所以不会删除最后覆盖。

一次降权 s→s'，该客户密度增加

\[
\frac{s-s'}{(z+s')(z+s)}
\]

随其他负载 z 非增；H 使用的其他负载至少是尾密度使用的负载。因此本步 `ΔH≤ΔU_j≤(t−u_j)_+`，每尾至多一次即得(21)，(22)是同池的子集与更大分母比较。

还必须同步扣除返还。令尾质量 `M=Σ_jw_j*`、尾利润 `V(w)=Σ_jw_jU_j(w)`，其中零权尾的利润按零计；再令旧背景利润 `B(w)=Σ_x b_x/[b_x+a_x+c_x(w)]`，根返还 `Δ_R=R(w*)−R(1)`。覆盖支撑保持给

\[
\boxed{V(w^*)=V(1)-\Delta_R-[B(w^*)-B(1)],}
\]

\[
\boxed{\Delta_R+[B(w^*)-B(1)]+tM\le V(1).}\tag{23}
\]

零负载背景项按零计。辅助权一般可无理；它们不是新单位玩家。

**水位接入的断点。** 对 SPE 的每个根分支可以各用(21)—(23)，但降权后的对象不自动是 SPE。原根比较只能保留为

\[
R_{\mathrm{pruned}}(\mathrm{actual})-\Delta_R^{\mathrm{actual}}
\ge R_{\mathrm{pruned}}(A)-\Delta_R^A.
\tag{24}
\]

同一池在多分支间如何共同分配、如何保留全部原树激励，尚无一般支付。不能在水位对象上直接调用单位玩家归纳，再免费恢复原收益。原唯一正文及独立审查见[分数尾水位化](fractional_tail_waterfill.md)。

### 6.4 对数变分规范化：零权重入、唯一负载与联合势账

同一终局输入下，另取 t>0，令 `L_x(w)=b_x+a_x+c_x(w)`、`K_sup={x:L_x(1)>0}`。在盒 `[0,1]^n` 最大化

\[
F_t(w)=\sum_{x\in K_{\rm sup}}\log\frac{L_x(w)}{L_x(1)}
+t\left(n-\sum_jw_j\right),
\tag{VAR}
\]

支撑客户负载为零时目标取 −∞。F_t(1)=0，而目标非负的点满足每个原支撑客户 `L_x(w)≥exp(−tn)L_x(1)>0`；限制到这个紧集便得最大元 w* 存在并保持原支撑。其盒 KKT 为

\[
w_j^*=0\Rightarrow U_j(w^*)\le t,\quad
0<w_j^*<1\Rightarrow U_j(w^*)=t,\quad
w_j^*=1\Rightarrow U_j(w^*)\ge t.
\tag{KKT}
\]

特别是零权主题也不能通过单坐标重入改善目标。原 u_j≥t 者保留权一；这份 VAR 最大元不能与任意单遍水位化终点混同。两个最大元若客户负载不同，log 的严格凹性使其中点目标更大；故所有最大元负载相同。目标值再以 t>0 迫使总质量 M 相同，权分解可不唯一；总质量唯一性限 t>0。

每个负载变化客户至少属于一个降权主题，故终点互补性直接给

\[
H\le\sum_{j:w_j^*<1}[U_j(w^*)-u_j]\le D.
\]

因此(22)的共同查询界与(23)的 CONS 均保留。令 `F*=F_t(w*)`、`ΔB=B(w*)−B(1)`，还有

\[
0\le F^*\le D,\qquad
\boxed{\max\{H,\Delta_R+\Delta B\}+F^*+tM\le tn.}
\tag{JOINT}
\]

其要点是 `L_log=Σ_(K_sup) log[L_x(1)/L_x(w*)]` 同时控制 H 和 `Δ_R+ΔB`，而 `F*=t(n−M)−L_log`。查询项的积分比较使用分母 `L_x+(1−a_x)≥1`，不对可能小于1的 L_x 直接套用同一界。

JOINT 中的 max 不能改成两项之和；H≤D 与 F*≤D 也不能相加后仍只支付一份 D。CONS 始终用原尾利润 V(1)；JOINT 右端 tn 则只有在**另证** V(1)≥tn 后才能再由该利润支付。规范化本身不证明这个条件，不是 SPE，也未支付跨真实子树的切换债务。

此段整理[变分共同信用原文](../../workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/shared/variational_common_credit.md)及已有[tail 盲重构](../../workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/tail/review_variational_blind.md)、[最终对稿审查](../../workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/tail/review_variational_final.md)，不宣称本轮重新完成这些材料的全部独立审查。

### 6.5 统一缩尾的条件可信接口：保留完整孩子，不自动保留全树

有一项已证的有条件关系，可在特殊满足条件的**任意人数孩子**中补回可信性。固定旧背景 b、保留单位根 A，记 `β_x=b_x+1_A(x)`、`K_core=∩_(T∈S)T`。根后有 n≥1 位单位尾部，σ 是该固定孩子的完整 SPE。假设对其**全部有序尾历史** h 都有

\[
(\sigma(h)\setminus K_{\rm core})\cap\{x:\beta_x>0\}=\varnothing.
\tag{AVOID}
\]

β 只含这个孩子开始时的固定背景，不含 h 内已行动的尾部。AVOID 只限制规定动作；偏离主题和过去离轨动作可以触及非核心正背景。

给全部 n 位尾部统一固定质量 `0<λ≤1`，旧背景与根保持不变，同一 σ 是辅助加权孩子游戏的完整 SPE。证明逐真实比较进行：规定动作的非核心客户有 β_x=0，其实际质量利润 `λ/(λk_x)=1/k_x` 保持；偏离非核心客户则有

\[
\frac{\lambda}{\beta_x+\lambda k_x}
\le\frac1{\beta_x+k_x}.
\]

每个合法主题都含共同核心，其新旧核心利润分别在两枝相消。故每条新加权 IC 差至少为原差，包含所有离轨历史；不是冻结实际后继的比较。

再固定原孩子的一条实际叶。令 k_x 为其尾负载，

\[
a_j=\sum_{x\in S_j\setminus K_{\rm core}}\frac1{k_x},\quad
a_* =\min_j a_j,\quad
S_{\rm load}=\sum_{x\notin K_{\rm core}:k_x>0}\frac{k_x}{(k_x+1)^2},\quad
K(\lambda)=\sum_{x\in K_{\rm core}}\frac1{\beta_x+n\lambda}.
\]

原 u_j=a_j+K(1)。若 a*>0 且 `S_load≤a*`，对 t>min_j u_j 有唯一正 λ<1 满足 `a*/λ+K(λ)=t`。该叶全部尾部单位密度过线，且同一查询池满足

\[
H(\lambda)\le S_{\rm load}(1/\lambda-1)+K(\lambda)-K(1)
\le(t-\min_j u_j)_+\le D.
\]

t≤min u 时直接取 λ=1，H=0，不需谱条件。利润仍按质量计算，(23)以 M=nλ 成立。a*=0 的纯核心退化及正质量阈值端点另见原文，不能用 λ=0 免费补一个正质量解。

这个接口放弃“原高尾保持质量1”，以全部尾共同缩权换取孩子可信性。AVOID 与谱条件不是一般 SPE 的自动性质；水位和查询界只针对定义该谱的固定叶，不保证所有离轨叶达到同一阈值。它也不保证更早根或其他孩子仍最优，各分支重新选 λ 不会自动成为一份固定质量游戏。因而本段不能撤去第6.3节的全树接入断点。

本段引用[统一缩尾原文](../../workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/credible/waterfill_credibility_uniform_contraction.md)及已有[relay 独立解析审查](../../workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/relay/review_uniform_credible_contraction.md)的明示范围；这里整理其通用有条件关系，不另称一次全量新复审，也不把其中固定客户族的应用当作一般福利引理。

## 7. 直接覆盖证明还差哪一个全范围关系

回到(Q)，对客户兴趣类型 B 记单位客户重数 w_B≥0。固定完整形式策略 σ 后，每条(2)都有逐类型系数 Γ_{h,A;B}；实际覆盖和比较覆盖系数记 c_B、o_B。于是

\[
W=c\cdot w,\qquad O=o\cdot w,\qquad\Gamma w\ge0.
\]

若能对任意 σ、任意比较元组构造非负历史乘子 λ 与非负逐类型余项 η，使

\[
\boxed{2c-o=\Gamma^{\mathsf T}\lambda+\eta,
\qquad\lambda\ge0,\quad\eta\ge0,}\tag{25?}
\]

则与 w 内积立即完成(Q)。λ 可以分别使用每个有序历史、每个单主题偏离，不必先按深度或节点平均。

(25?)是充分的共同支付形式，**其普遍存在性未证明**。固定策略的锥表示、Farkas 对偶或给定证书的运输都不构造这个普遍 λ；不能循环从(Q)推出存在性，再称之为(Q)的证明。原唯一接口见[完整策略锥](strategy_cone.md)；若使用末回复规范化，还需按[末回复运输](terminal_reply_transport.md)保留真实误差，规范化策略不能默认仍为 SPE。

这一接续点与(18?)并列：一个直接支付比较覆盖，一个先支付静态安全值。新证明可以改变状态或绕开二者。

## 8. 额外一槽与完整菜单：另一条充分但未闭合的接续

对每个实际位置 i、每个强制行动 A，保留完整 m 槽终局 Z_i(A)=Z_{h_i,A}，**含固定过去、当前 A 与真实后继**。定义独立额外查询矩阵

\[
K_i(T,A)=\sum_{x\in T}\frac1{1+c_x(Z_i(A))}.
\]

每列是合法 m 槽静态竞争背景。因此其自由混合菜单值

\[
M_i=\min_Q\max_T\mathbb E_Q K_i(T,A)
=\max_p\min_A\sum_Tp_TK_i(T,A)
\]

必满足 `M_i≥v_{m+1}(0)`。如果能够对任意实例及全部实际位置另证

\[
M_i\le u_i,\tag{26?}
\]

则由(15)有 `OPT_m≤2m v_{m+1}(0)≤2Σ_i u_i`，完成(Q)。这就是含根额外一槽的 Mfull 方向；(26?)仍未证明。

也可以允许从全部实际位置的完整菜单共同选列，定义

\[
M_{\mathrm{path}}=
\min_{Q\in\Delta(\{(i,A)\})}\max_T\mathbb E_QK_i(T,A).
\]

它仍有 `M_path≥v_{m+1}(0)`。故更弱的充分候选

\[
M_{\mathrm{path}}\le W/m\tag{27?}
\]

也能与(15)闭合(Q)。若(26?)逐位置成立，混合这些位置的证书便给(27?)；反向不作假设。

这些候选保留查询与背景独立的量词。只用根的 m−1 槽尾菜单、指定推送分布或逐人 `u_i≥v_m` 的失败，均不能直接当作(26?)或(27?)的反例。其产品闭包又给一个已证的兼容性关系：对固定 m，(27?)对全部实例成立，等价于存在只依赖 m 的位置分布 λ，使对全部实例和全部 p 有

\[
\sum_i\lambda_i\min_A\sum_Tp_TK_i(T,A)\le W/m.
\tag{28?}
\]

这个等价没有给出 λ，也没有证明它存在。原唯一正文见[完整根菜单](../../workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/induction/full_root_menu_mixed_obligations.md)和[PRODUCT-MENU-TIME](../../workspaces/customer-attraction/R-4243b113e6fc4c25a197dec299f08049/parent/product_menu_time_obligation.md)。

## 9. 根修复只是一种等价表示，不能填入上述空缺

另有一项适用于任意 m≥2 的可信修复工具。旧完整计划 τ 在所有正深度子博弈均为 SPE，仅根可能有缺陷；令实际根收益 u、强制根 B 的真实收益 d_B，根缺陷 `Δ=max_B d_B−u≥0`。常数三保险编译器可将 Δ>0 的这种计划变成同人数完整 SPE。取正整数 L 使 LΔ 为整数，并共同复制旧客户 L 次；Δ 已为整数时可取 L=1。输出的 half 坏差额为

\[
\operatorname{OPT}_{\mathrm{new}}-2W_{\mathrm{new}}
=L\left[(\operatorname{OPT}_{\mathrm{old}}-2W_{\mathrm{old}})-3\Delta\right].
\tag{29}
\]

所以原(Q)等价于所有这种 root-only 计划满足

\[
\operatorname{OPT}_{\mathrm{old}}\le2W_{\mathrm{old}}+3\Delta.
\tag{30?}
\]

Δ=0 时 τ 已为完整 SPE；Δ>0 的正向由编译和(Q)推出。这个等价仍然没有证明任一边，尚未向一般 half 正面证明贡献闭合的一步。它可作为反例与稳健预算的表示工具，不能替代(18?)、(25?)或(26?)的证明。原唯一正文及缩放条件见[常数三根修复](../../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/compiler/padded_insurer_repair.md)。

## 10. 当前真正能落到纸面的结论

对任意一般输入，目前本稿已完成从真实(2)到(10)的路径利润产品界、(PJS-2)的联合前缀席位付款，以及独立的静态比较(14)—(15)。同背景末两人信用、全部历史的承诺重置、终局水位与变分守恒，以及明示条件下的统一缩尾孩子可信性，均可在各自范围内使用。它们还没有共同推出(Q)。

继续写这份证明时，新增承重关系应明确作用于哪个真实历史或哪些静态背景，使用哪一份已经支付的利润，以及是否保留全部后继最优性。直接目标始终是本实例的 `2W−O≥0`；安全值、菜单和 root-only 表示中的问号均是可更换的接续位置，不是已经成立的前提。

已有失败桥的准确范围见[续局边界](continuation_lemmas.md)、[全分布安全预算边界](global_security_budget_boundaries.md)及[人口删除的全人数边界](../../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/potential/population_deletion_boundary.md)。因此不能通过冻结后继、全员 θ 保底、局部安全余额非负、降权后继承 SPE，或在同覆盖联合内删除玩家重新均衡，补齐本稿的问号。允许采用新的全局关系；原目标仍为 **OPEN**。
