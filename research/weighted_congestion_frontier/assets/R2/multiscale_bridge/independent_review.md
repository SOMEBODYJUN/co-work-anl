# R2 多尺度接口独立重构审查 v1

日期：2026-10-14。第一阶段审查在阅读候选／冻结证明之前，仅依据 `MODEL.md`、`ACCEPTANCE.md` 和给定精确接口重构证明；下文末尾另附第二阶段的冻结文本对照。本记录不作 Git 写入或公屏发送。

## 结论与修正

两条数值接口和最终资源混合桥接**成立**，但候选叙述中一个证明推理必须修正：

> 从降序势的弱下界 \(\Delta\Phi_e\ge (w_i/R_e)c_e\) 出发，乘 \(M_e^p/m_e\) 并不能推出 \(\Delta\widetilde\Phi_e\ge w_i^pc_e\)。

其实际所得仅为 \(M_e^{p-1}w_i c_e\)，通常小于 \(w_i^pc_e\)。例如 \(M_e=4,m_e=1,p=1/2,w_i=1\)，弱下界经缩放只有 \(c_e/2\)，而目标下界是 \(c_e\)。这是推理缺口，不是实际降序势的反例。

精确修复是独立证明更强的下界

\[
\boxed{m_e c_e(W+w_i)\le\Delta_i\Phi_e\le w_i c_e(W+w_i).}
\]

这条更强下界使指定缩放和共享 \(h_i=w_i^p\) 完全成立。以下给出不依赖候选证明的重构。

## 对象、量词与状态

Claim ID：`R2-MSB-INDEPENDENT-v1`。对象采用 WC-TARGET v1：有限玩家及资源，任意正实权重，任意非空有限策略族（允许空策略），非负系数、次数至多整数 \(d\ge0\) 的费用多项式。玩家成本不乘权重。

对资源 \(e\)，令 \(U_e=\{i:\exists s_i\in S_i, e\in s_i\}\) 为潜在用户集合。对非空 \(U_e\)，定义

\[
m_e=\min_{i\in U_e}w_i>0,\quad M_e=\max_{i\in U_e}w_i<\infty,
\quad R_e=M_e/m_e\ge1.
\]

为避免与跨度 \(R_e\) 混淆，下文用 \(\rho>1\) 表示 packing 窗口倍率。固定共享 \(p\in(0,1)\)。取整数 \(K_e\ge1\)，使任意 \(x>0\) 的半开窗口 \([x,\rho x)\) 至多容纳 \(U_e\) 的 \(K_e\) 名玩家，按玩家数计重数。所有活动用户子集继承此条件。

空潜在用户资源始终没有负载，可令其势恒为零并从最大值中删去。若所有资源均无潜在用户，任意状态均为精确 PNE，并令最终因子为 1。也可统一给空资源约定 \(R_e=1,K_e=0\)。

第一阶段状态：独立重构已证明；当时未读候选冻结文本。证据为下面一般论证，非有限实验。Counterevidence：未发现结论反例；上述弱下界缩放的推理缺口已给精确修正。Scope：这是依赖资源权重密度及跨度的保证，尚不是 WC 全类的 \(o(d)\) 上界。

## Packing 不等式

对任意有限正实数多集 \(v_1,\ldots,v_n\)，若任意 \([x,\rho x)\) 至多有 \(K\) 项，则

\[
\sum_jv_j^p\le A_\rho(p)K^{1-p}\Bigl(\sum_jv_j\Bigr)^p,
\qquad A_\rho(p)=\frac{(1-\rho^{-1})^p}{1-\rho^{-p}}.
\]

重构：令 \(r=\rho^{-1}\)，将多集降序排列为 \(a_1\ge\cdots\ge a_n\)。窗口条件等价于 \(a_{j+K}\le r a_j\)。若严格大于，则窗口 \([a_{j+K},\rho a_{j+K})\) 已含连续 \(K+1\) 项；反向亦同。端点等于时因右端不计入，完全合法。

按下标模 \(K\) 拆成至多 \(K\) 条链，每条链满足 \(b_{j+1}\le r b_j\)。令 \(C=(1-r)^p/(1-r^p)\)。对一条有限链，首项为 \(b\)，尾和为 \(T\)，有 \(T/b<r/(1-r)\)。函数

\[
g(t)=C\bigl[(1+t)^p-t^p\bigr]
\]

严格递减，并满足 \(g(r/(1-r))=1\)。所以 \(b^p+CT^p\le C(b+T)^p\)。对尾链作归纳，得到 \(\sum b_j^p\le C(\sum b_j)^p\)。最后对各链总和 \(T_\ell\) 用凹性：\(\sum_{\ell=1}^K T_\ell^p\le K^{1-p}(\sum_\ell T_\ell)^p\)。空链贡献为零。

锐性（统一常数的上确界）：每个层级 \(1,r,\ldots,r^{N-1}\) 取 \(K\) 份，满足半开窗口条件，其比值为

\[
K^{1-p}A_\rho(p)\frac{1-r^{pN}}{(1-r^N)^p}
\longrightarrow K^{1-p}A_\rho(p).
\]

因此该常数不能统一缩小。任意实数正权均可，不使用整数、格点或有理数限制。

## 稀疏谱势的插入界

令活动用户集合为 \(P\subseteq U_e\)，\(i\notin P\)，并写

\[
W=\sum_{j\in P}w_j,\quad B=\sum_{j\in P}w_j^p,\quad t=w_i>0,
\qquad \Psi_e(P)=B c_e(W).
\]

则精确恒等式为

\[
\Delta_i\Psi_e=t^pc_e(W+t)+B\,[c_e(W+t)-c_e(W)].
\]

费用单调，故下界是 \(t^pc_e(W+t)\)。若 \(W=0\)，第二项为零，直接获得等号；若费用恒为零，同样全部为零，无须作比值。

当 \(W>0\)，非负系数与次数至多 \(d\) 给出

\[
c_e(W)\ge\left(\frac{W}{W+t}\right)^d c_e(W+t).
\]

逐单项验证即可；常数项对应倍率 1。结合 packing 界并令 \(S=W/t>0\)，得到

\[
t^pc_e(W+t)\le\Delta_i\Psi_e
\le\bigl[1+A_\rho(p)K_e^{1-p}H_d(p)\bigr]t^pc_e(W+t),
\]

其中

\[
H_d(p)=\sup_{S>0}S^p\left[1-\left(\frac{S}{1+S}\right)^d\right].
\]

\(d=0\) 时明定 \(H_0(p)=0\)，并且插入边际恰为 \(t^pc_e\)。\(d\ge1\) 时该被取上确界的函数在 \(S\downarrow0\) 和 \(S\uparrow\infty\) 均趋于零，因此 \(H_d(p)\) 有限且在内部取得。

令 \(y=d/S\)。由 \(\log(1+y/d)\le y/d\)，

\[
\begin{aligned}
S^p\left[1-\left(\frac{S}{1+S}\right)^d\right]
&=d^p\frac{1-(1+y/d)^{-d}}{y^p}\\
&\le d^p\frac{1-e^{-y}}{y^p}
\le\kappa_p d^p,
\end{aligned}
\]

\[
\kappa_p=\sup_{y>0}\frac{1-e^{-y}}{y^p}\in(0,1).
\]

其唯一正极大点 \(y_p\) 满足 \(p(e^{y_p}-1)=y_p\)，且 \(\kappa_p=y_p^{1-p}/(p+y_p)\)。取 \(S=d/y_p\) 可得 \(H_d(p)/d^p\to\kappa_p\)，所以 \(\kappa_p\) 是对所有整数次数的最优统一常数；固定有限 \(d\ge1\) 时该界严格。

## 降序势及必要的更强下界

将 \(P\) 中玩家按权重非增排列，定义

\[
\Phi_e(P)=\sum_{j=1}^{|P|}w_{(j)}c_e\left(\sum_{k=1}^j w_{(k)}\right),
\qquad\Phi_e(\varnothing)=0.
\]

同权玩家的排列不会改变数值，可在插入时把 \(i\) 放在所有同权用户之后。令插入之前的较大／同权前缀总重为 \(X\)，尾部为 \(u_1,\ldots,u_q\)，则 \(m_e\le u_j\le t\)，并写 \(b_0=X,b_j=X+\sum_{k\le j}u_k\)。精确边际为

\[
\Delta_i\Phi_e=t c_e(X+t)+\sum_{j=1}^q u_j[c_e(b_j+t)-c_e(b_j)].
\]

下界仅需费用单调。因为 \(t\ge u_j\)，

\[
c_e(b_j+t)-c_e(b_j)\ge c_e(b_j+t)-c_e(b_{j-1}+t)\ge0.
\]

将 \(u_j\ge m_e\) 以及 \(t\ge m_e\) 代入并望远镜求和，得到

\[
\Delta_i\Phi_e\ge m_e c_e(X+t)+m_e\sum_{j=1}^q[c_e(b_j+t)-c_e(b_{j-1}+t)]
=m_e c_e(W+t).
\]

上界使用多项式费用的凸性。在长度 \(t\) 的区间上，平均斜率不超过该区间最后长度 \(u_j\le t\) 部分的平均斜率。因此

\[
u_j[c_e(b_j+t)-c_e(b_j)]\le t[c_e(b_j+t)-c_e(b_{j-1}+t)].
\]

同样望远镜得 \(\Delta_i\Phi_e\le t c_e(W+t)\)。不存在尾部、仅有一名活动用户、同权、常数费用及零费用等情形都包含在此证明中。

因为 \(m_e\ge t/R_e\)，候选弱界 \((t/R_e)c_e\le\Delta_i\Phi_e\le t c_e\) 也成立，但不能替代上面的更强下界用于缩放。

令

\[
\widetilde\Phi_e=\frac{M_e^p}{m_e}\Phi_e.
\]

则

\[
\Delta_i\widetilde\Phi_e\ge M_e^pc_e(W+t)\ge t^pc_e(W+t),
\]

\[
\Delta_i\widetilde\Phi_e\le\frac{M_e^p t}{m_e}c_e(W+t)
=R_e(t/M_e)^{1-p}t^pc_e(W+t)
\le R_e t^pc_e(W+t).
\]

## 混合桥接及 retained 资源

每个非空潜在用户资源**预先固定**选择 \(\Psi_e\) 或 \(\widetilde\Phi_e\)，取相应较小上界；选择仅依赖静态数据与参数，不依赖状态或当次偏离。令选择所得势为 \(F_e\)，则所有资源使用同一玩家尺度 \(h_i=w_i^p\)，满足

\[
h_i c_e(W+w_i)\le\Delta_iF_e\le\beta_e h_i c_e(W+w_i),
\quad
\beta_e=\min\{R_e,\,1+A_\rho(p)K_e^{1-p}H_d(p)\}.
\]

全势 \(F(s)=\sum_e F_e(N_e(s))\)，令 \(\alpha=\max_e\beta_e\ge1\)。考虑 \(s_i\to t_i\)，记移除资源 \(A=s_i\setminus t_i\)、新增资源 \(B=t_i\setminus s_i\)、保留资源 \(D=s_i\cap t_i\)。所有保留资源的用户集合完全不变，故其势贡献精确取消；玩家在保留资源上的费用也相同，记其总和为 \(C_D\ge0\)。于是

\[
F(t_i,s_{-i})-F(s)
\le h_i\bigl(\alpha C_B^{\rm new}-C_A^{\rm old}\bigr).
\]

若当前成本严格大于 \(\alpha\) 倍偏离成本，则

\[
C_A^{\rm old}+C_D>\alpha(C_B^{\rm new}+C_D)
\quad\Longrightarrow\quad
C_A^{\rm old}>\alpha C_B^{\rm new}+(\alpha-1)C_D
\ge\alpha C_B^{\rm new}.
\]

势严格下降。有限状态空间保证势的全局最小状态存在，该状态是包含边界 \(\le\) 的 \(\alpha\)-PNE。零目标成本、两个成本皆零、空策略与多资源策略均无需额外假设；全过程不用 \(0/0\)。

## 端点与否定范围

1. 原接口要求 \(0<p<1\)，该范围内结论完整成立。\(p=0\) 时 packing 的统一常数不存在：固定 \(K=1\) 可取任意长几何链，\(\sum v^0\) 为任意大的项数，而 \((\sum v)^0=1\)。不能将 \(A_\rho(0)\) 当成有限数。降序分支本身可单独延拓到 \(p=0\)，共享尺度为 1；但不能直接代入两分支公式，尤其 \(d=0\) 会产生未定义的 \(\infty\cdot0\)。
2. \(p=1\) 可单独延拓：packing 是恒等式 \(\sum v=\sum v\)，\(A_\rho(1)=1\)，\(H_d(1)=d\)（\(d\ge1\) 时上确界在 \(S\to\infty\)），\(\kappa_1=1\)。混合因子为 \(\max_e\min\{R_e,d+1\}\)。这不改变原 claim 的开区间域。
3. \(d=0\) 给 \(\alpha=1\)，因稀疏分支边际精确。\(d=1\) 的原桥接通常给大于 1 的保证，但这不否定仿射类有精确 PNE，也不应宣称该桥接最优。
4. 每个 \(K_e\) 必须约束全部潜在用户或另一种已证明对所有插入集合有效的静态集合；仅约束某个当前状态不能支持全状态势证明。\(m_e,M_e\) 同样必须预先固定。不同资源若使用不同的玩家指数 \(p_e\)，则通常失去共享 \(h_i\)，上述拼接不能直接使用。
5. 任意 WC 游戏确实都有某个有限 \(R_e,K_e\)，但这些参数不受 \(d\) 单独控制。因而本公式是全类上每个实例都有效的**实例参数界**，没有推出全类阈值 \(a_*(d)=o(d)\)。这不是主目标阶段突破的证据。

## 文献核查与优先权边界

已联网直接打开并核查 Dagstuhl 原始 PDF，而非仅依赖搜索摘要。

Hansknecht–Klimm–Skopalik, *Approximate Pure Nash Equilibria in Weighted Congestion Games*, APPROX/RANDOM 2014, pp.242–257, DOI `10.4230/LIPIcs.APPROX-RANDOM.2014.242`：p.246 的模型采用不乘权重的玩家费用与正实权；Definition 1 定义同一离散积分；Lemma 5（p.249）证明凸费用下降序排序最小化该积分；Theorem 4（p.248）使用各资源最小排序积分之和作为近似势。因此本记录的降序 \(\Phi_e\) **不是新的势构造**。

官方 PDF：<https://drops.dagstuhl.de/storage/00lipics/lipics-vol028-approx-random2014/LIPIcs.APPROX-RANDOM.2014.242/LIPIcs.APPROX-RANDOM.2014.242.pdf>

Caragiannis–Fanelli, *On Approximate Pure Nash Equilibria in Weighted Congestion Games with Polynomial Latencies*, ICALP 2019, Theorem 2（p.133:5）：通过每资源删除边际与 \(w_i c_e\) 的上下区间推出近似势。它是本记录一般局部边际拼接的已有先例；此处共享 \(w_i^p\) 的拼接另由上文直接证明，故无需机械套用其原模型及分母正性。

官方 PDF：<https://drops.dagstuhl.de/storage/00lipics/lipics-vol132-icalp2019/LIPIcs.ICALP.2019.133/LIPIcs.ICALP.2019.133.pdf>

核查范围只确认上述已有构造及拼接框架，不构成对 packing 常数、\(p\)-谱归一化或整个混合公式的完整新颖性检索。不得据此宣称首次、最优文献界或已完成优先权审查。

## 审查分类

| 维度 | 判断 |
|---|---|
| Truth | 接口与混合结论成立；缩放推理必须采用已证明的 \(m_e c_e\) 强下界。 |
| Value | 产生可复用的密度／跨度实例保证及兼容共享玩家尺度的混合势。 |
| Novelty | 降序势及局部边际拼接有明确已发表先例；其余尚未完成优先权检索。 |
| Mechanism | packing 将幂和压到总负载的 \(p\) 次幂；降序凸性产生望远镜上界；强最小权下界修复归一化。 |
| Ambition | 尚未解决 WC-TARGET 的全类 \(o(d)\) 或严格新无限下界。 |

Related Files：`research/weighted_congestion_frontier/MODEL.md`、`research/weighted_congestion_frontier/ACCEPTANCE.md`、本文件。Dependencies：packing 凹性、费用单调与凸性、非负系数次数界、有限状态最小化。重要未解义务：对冻结证明逐行比对，并独立判定该实例保证如何（若可能）消去不受控的 \(R_e,K_e\) 以到达主目标。

## 第二阶段：冻结文本与精确审计对照 v2

对照对象：`research/current/weighted_congestion_frontier_power_bridge.md` 的 Sections 1–3、6。复核时文本 SHA-256 为 `d63f8488ce1a2d72c8c37ee659671d5925c4ccda4b2137b333639c0e1db7d8a9`；本节判断仅指该版本。本节在上面第一阶段独立证明已完成、文件已交付之后进行。

总体判断：与独立重构一致，未发现实质数学反例。冻结文本已正确采用 \(m_ec_e\) 强下界修复缩放，式 (1) 已正确覆盖所有潜在用户集为空的情形。下列量词和证明表述须补齐，才能按精确文本而非善意解释验收。

1. **插入量词。** Section 1 只写 \(T\subseteq U_e,i\notin T\)，应明确为 \(i\in U_e\setminus T\)。若按字面允许任意非潜在用户插入，静态 \(m_e,M_e,Q_e\) 不再覆盖其权重，资源边际界可假：例如 \(U_e\) 仅有权重 1 的玩家，\(p=1/2,Q_e=1,T=\varnothing\)，外部权重 4 的玩家有降序边际 \(4c_e(4)>2c_e(4)\)；外部权重 \(1/4\) 则违反目标下界。实际游戏偏离不会向资源插入非潜在用户，故补量词后不存在该反例，也不影响游戏存在结论。
2. **Packing 归纳。** Section 2 的尾和 \(T\le a/(R-1)\)、递减函数和端点值方向均正确；单项基例 \(A_R\ge1\) 正确。空集合的 (2) 直接是 \(0\le0\)，非空潜在用户的 \(K_e\ge1\) 才使用模 \(K_e\) 拆链。右开端点及同权重重数均得到处理。
3. **\(H_0\) 与 \(S=0\)。** Section 1 对 \(H_0\) 的定义及对 \(S=0,d\ge1\) 的约定正确。Section 2 的差项核以及 \((1+1/S)^{-d}\ge e^{-d/S}\) 证明应显式先说“\(d=0\) 时直接为零；其余取 \(d\ge1,S>0\)，\(S=0\) 直接处理”。这避免在中间公式出现 \(0^0\)、\(1/0\)。原结果本身没有端点漏洞。共享 \(p\in(0,1)\) 在整个 claim 中正确固定。
4. **稀疏推论的量词。** 固定 \(R\) 且 \(K=o(d)\) 的推论成立，\(1/(1-e^{-z})\le1+1/z\) 的方向正确。应明确这里 \(K=\max_{e:U_e\ne\varnothing}K_e\)，并在一族游戏上要求该最大密度随 \(d\) 为 \(o(d)\)。所得 \(K\log(d/K)/d\to0\)，因此子类结论正确；不能读成全类参数消除。
5. **排序上界。** Section 3 明确使用凸性，且“降序最小化离散积分，旧降序排列后末尾追加新玩家作为候选”确实给 \(\Delta_i\Phi_e\le v c_e(W(T+i))\)。相邻交换的比较等价于比较凸函数在同一右端点的长区间和短区间平均斜率，长区间的平均斜率较小。没有把非减性误用于上界。ties 的数值与玩家身份排列无关。
6. **排序下界及缩放。** \(u_j\le v\) 保证 \(X+B_j\le X+v+B_{j-1}\)，各费用差非负；乘 \(u_j\ge m_e\) 后望远镜下界正确。下界只需非减性与非负性，\(M_e^p v^{1-p}\le M_e\) 的缩放上界也正确。
7. **保留资源。** 保留资源的势贡献精确抵消，玩家保留费用也相同；但是在 \(\alpha\) 倍成本比较中，不能未经说明称其成本“完全取消”。应补上本记录前节的明确式子 \(C_A^{\rm old}>\alpha C_B^{\rm new}+(\alpha-1)C_D\ge\alpha C_B^{\rm new}\)。这使用 \(\alpha\ge1,C_D\ge0\)，之后严格下降和最小者的 \(\le\) 边界均正确。空策略、目标费用零和恒零费用资源无需除法。
8. **Claim 身份与来源。** `WC-R2-RESOURCE-POWER-BRIDGE v1` 的实例范围、静态参数、共享指数及未达到全类 \(o(d)\) 的状态均准确。2014 的降序构造已直接核查，Section 6 不宣称排序为新机制，合适。Section 6 所述更广固定乘子障碍的公屏 seq8／commit 809b032 未由本审查重新验证，且不是当前 proof 的依赖，不能算作本审查证明。Related Files 声称“均相对仓库根”后却裸列 `path_review.md`、`affine_two_type.md`、`path_obstruction.md`；应补其完整研究目录前缀。此为追溯性修正。

### Audit 的实跑结果与证据范围

独立执行 `python3 tests/audits/weighted_power_bridge.py`，退出码 0。脚本 SHA-256 为 `83c4921f09346d55b9b9da3a2b04f7e8d9febad286a1f0e52af00d673344ff25`，运行未使用 `--output`，未修改主代码或证据文件。

| 类别 | 实际计数 |
|---|---:|
| ordered_edges | 35304 |
| power_edges | 35304 |
| packing_vectors | 329 |
| affine_edges | 25000 |
| literal_paths | 490 |
| rational_exponents | 21 |

算术检查：所有相关 `/` 运算均作用于 `Fraction`，整数平方根函数同时断言分子／分母为完全平方；没有隐式浮点比较、随机参数或容差。packing 的 \(p=1/2,R=4\) 平方形式等价于原不等式。density 只在 \(x\) 等于某个权重时取最大是充分的：任意非空窗口取其最小已纳入权重 \(m\ge x\)，原窗口所有成员仍在 \([m,4m)\)。玩家按下标枚举，重复权重正确计为不同玩家。

这些有限核验只覆盖所列权重和系数：packing 与幂和势仅测 \(p=1/2,R=4\)，且四个权重位于倍率 4 的几何格点，未测窗口边界的邻近扰动或一般重叠窗口；没有对 \(\kappa_p,H_d\) 包络作数值核验，没有枚举完整游戏或检验全局最小者的均衡性。脚本中的 rational_exponents 是路径障碍的有限恒等式核验，不能误标为任意指数 packing 证据。脚本的仿射核验为五组参数、各 \(0\le m,n\le24\)，不替代任意实参数和人数的一般证明。当前 account 已将有限核验与一般证明区分，保持该区分即可。

最终状态：数学接口独立通过；以上精确量词及边界表述修正待主对话合入冻结 account。没有新增路线或扩展结论。
