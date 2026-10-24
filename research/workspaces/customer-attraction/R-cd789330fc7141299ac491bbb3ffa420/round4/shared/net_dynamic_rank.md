# NET 的真实价格—Hall cut 表示：取消量可完整消元

2026-10-23，shared。对象为一般人数、一般有限共同目录及任意完整历史纯 SPE。本文固定一次最优 matching/owner，把原递增捕获流的 whole-IC 价格与实际 Hall 取消网络共同处理；不扩静态结构类。RANK、BASE、GREEDY、TOTAL、DEFICIT、NET-DUAL、精确margin式及NET-FRAC充分性已经credible[独立重构对稿通过](../credible/review_net_dynamic_rank.md)（首次读取含作者证明，不称盲审）。它没有证明最后的动态 cut 上界，因此 Q-CAG-HALF 仍 OPEN。

## 1. 固定原流价格，不改变 whole-IC 系数

固定最优有序元组 T 与 owner 分割 Q_i⊆T_i；O 为最优并集。实际覆盖 C，R=O\\C、I=O∩C、G=C\\O。写实际玩家利润 u_i、I 利润 I_i=u_i(I)、G 利润 g_i=u_i(G)。

对每个 x∈R，从其 owner 槽 o(x) 的合法查询 T_o(x) 注入一单位，使用原[递增角色捕获流](../../round3/credible/increasing_role_capture_flow.md)。每个查询状态 s=(i,a) 读取原实际前缀下的完整真实叶；其完整收益 D_s 固定。客户源流对初始质量线性，所以同一个标量

\[
w_s=A_s/D_s
\]

产生的实际付款，也能按初始客户线性分拆。令 p_ix≥0 为单位 x 源在 role i 的付款价，则对残源 ρ_x：

\[
K_i(\rho)=\sum_{x\in R}p_{ix}\rho_x.
\]

这里不是按客户重权 IC；原整体 w_s 只是在计算中按分子 A_s 的线性来源分解。三角支持 p_ix=0 对 i<o(x) 成立。令 v_x=Σ_i p_ix。每单位流总吸收为1，完整 SPE 又给 u_i≥D_s，因此 v_x≥1。

## 2. 实际取消网络的终端 rank

实际 Hall-A 网络的 source→role 容量为 g_i。对实际覆盖客户 x∈I，从其 owner 向每个非owner实际覆盖者 i 加容量1/c_x(C)。令 c_I(J,J^c) 为这些 I 边从角色集 J 向补集的总容量。真正遗漏 x∈R 的单位 sink 库存位于 o(x)。

对 S⊆R，定义 r(S) 为只开放 S 中 sink 库存时的最大 source 流量。有限最大流最小割给

\[
\boxed{r(S)=\min_{J\subseteq[m]}
\bigl[g(J^c)+c_I(J,J^c)+|S\cap Q(J)|\bigr],}\tag{RANK}
\]

其中 Q(J)=∪_(i∈J)Q_i。原 Hall-A 给 r(R)=|G|。并有 r(空)=0、r 单调、0≤r(S)≤min(|G|,|S|)。

**子模性。** 写 f(J)=g(J^c)+c_I(J,J^c)，这是有向 cut 加模函数，满足 f(A)+f(B)≥f(A∩B)+f(A∪B)。取 r(S)、r(T) 的最小割 J_S、J_T，逐客户有

\[
|S\cap Q(J_S)|+|T\cap Q(J_T)|
\ge |(S\cup T)\cap Q(J_S\cap J_T)|
+|(S\cap T)\cap Q(J_S\cup J_T)|.
\]

与 f 的子模式相加，并把两个交叉割用于 r(S∪T)、r(S∩T)，即得 r(S)+r(T)≥r(S∪T)+r(S∩T)。

**终端需求可实现性。** 非负向量 γ 可由原 source/I 网络送到指定 R 终点，当且仅当

\[
\gamma(S)\le r(S)\quad(S\subseteq R).
\]

必要性由限制到 S 的子流得到。反向将每个 R sink 容量改为 γ_x；任意角色割 J 的容量至少 γ(R)，等价于 γ(R\\Q(J))≤f(J)。取 S=R\\Q(J)，上述需求条件给 γ(S)≤r(S)≤f(J)，足够饱和全部 sink。单点需求又自动给 γ_x≤r({x})≤1。因此原完整 Hall 允许的取消集合恰为

\[
\Gamma=\{\gamma\ge0:\gamma(S)\le r(S)\ (S\subseteq R),
\quad\gamma(R)=|G|\}.\tag{BASE}
\]

这些取消量允许分数；未改变单位客户博弈。

## 3. 任意动态客户价格的最优取消可显式构造

对任意非负价格 z_x，把 R 排为 z_1≥…≥z_d≥0，S_k={x_1,…,x_k}，z_(d+1)=0。定义

\[
\gamma_{x_k}=r(S_k)-r(S_{k-1}).
\]

单调性给 γ≥0，总和为 r(R)=|G|。对任意 U⊆R，子模的边际递减给每个 x_k∈U 的上述增量不超过 r(U∩S_k)−r(U∩S_(k−1))，相加得 γ(U)≤r(U)。故此 γ 为合法完整取消量。

另一方面每个可行 γ 满足 γ(S_k)≤r(S_k)。分层求和得到

\[
\boxed{\max_{\gamma\in\Gamma}\sum_xz_x\gamma_x
=\sum_{k=1}^d(z_k-z_{k+1})r(S_k).}\tag{GREEDY}
\]

这消去了对取消量的共同选择，而不是只做每个 owner 的本地预取消。

**保留 SOURCE-NET 的指定取消。** 全局价格最优γ不自动满足以前指定的本地δ，不能把两个不同γ的好处相加。若已固定0≤δ_x≤1，且每owner δ_i≤g_i，先按原局部扩充引理直接预发δ，再在残余网络取 source g_i'=g_i−δ_i、库存 a_x=1−δ_x。其rank为

\[
r_\delta(S)=\min_J\bigl[g'(J^c)+c_I(J,J^c)
+a(S\cap Q(J))\bigr].
\]

全部库存cut与全部source同减δ(R)，故 r_δ(R)=G−δ(R)。相同的加权子模/greedy证明给 γ=δ+z≥δ 的最优追加取消；最小总价为

\[
\sum_k(v_k-v_{k+1})[a(S_k)-r_\delta(S_k)].
\]

若δ_i=min(g_i,|Q_i∩R|)，此优化保留SOURCE-NET同时成立。裸GREEDY/TOTAL则优化更大的Γ，不依赖逐source已经付款。两者须按实际选择区分。

## 4. 更弱总价桥的精确动态 cut

取 z_x=v_x=Σ_i p_ix。由 K_i=Σ_x(1−γ_x)p_ix，GREEDY 给

\[
\boxed{\min_{\gamma\in\Gamma}\sum_iK_i
=\sum_k(v_k-v_{k+1})\bigl[|S_k|-r(S_k)\bigr].}\tag{TOTAL}
\]

定义 Hall 缺额 d(S)=|S|−r(S)。RANK 也给

\[
\boxed{d(S)=\max_{L\subseteq[m]}
\bigl[|S\cap Q(L)|-g(L)-c_I(L^c,L)\bigr].}\tag{DEFICIT}
\]

所以对固定 matching/owner，较弱充分桥 ΣK≤W 精确等于一个真实价格分层 cut 上界：

\[
\int_0^\infty d(\{x:v_x\ge t\})\,dt\le W.
\tag{DYNAMIC-CUT?}
\]

由于 v_x≥1、d(R)=|R|−|G|=OPT−W，可分成

\[
\min_\gamma\sum_iK_i
=OPT-W+\int_1^\infty d(\{x:v_x\ge t\})\,dt.
\]

剩余需证的正关系是价格超额层的总 Hall 缺额≤2W−OPT。本文没有证明它；这也准确显示总价接口可能强于单独 half，因为它还要支付此特定递增流产生的 IC slack 费用。

## 5. 逐角色 NET 的完整非负价格对偶

写 d_i=Σ_xp_ix−I_i。NET 要求同一 γ 满足

\[
\sum_x\bigl(p_{ix}+1_{o(x)=i}\bigr)\gamma_x\ge d_i
\quad(1\le i\le m).
\]

Γ 是非空紧凸集。线性可行性分离给：存在这样的 γ，当且仅当对每个 λ_i≥0，

\[
\boxed{\max_{\gamma\in\Gamma}
\sum_x\left(\sum_i\lambda_i p_{ix}+\lambda_{o(x)}\right)\gamma_x
\ge\sum_i\lambda_i d_i.}\tag{NET-DUAL?}
\]

必要性相加即得；反向若 Γ 的线性像不与上正交锥要求相交，分离超平面可取 λ≥0，违反上式。左端由 GREEDY 对 λ-价格逐层计算。

λ全1恰退化TOTAL≤W，因为额外 owner 项对每个可行 γ 恒等于 Σγ=|G|。逐角色 NET 要求全部非负 λ，因此比总价桥更强。自由 matching/owner 仍须在外层共同选择；不同 λ 另选 matching，不自动产生同一份 NET。

还可保留精确行差而非只判断符号。令 h_Γ(z)=max_(γ∈Γ)Σ_xz_xγ_x，由GREEDY显式计算。紧凸Γ与有限单纯形上的线性极小极大给

\[
\min_{\gamma\in\Gamma}\max_i(K_i-\eta_i)
=\max_{\substack{\lambda_i\ge0\\\sum_i\lambda_i=1}}
\left[\sum_i\lambda_i d_i-
h_\Gamma\left(\sum_i\lambda_i p_{ix}+\lambda_{o(x)}\right)\right].
\]

因此一个固定选择的严格NET分离可写为非负角色价格及其嵌套R客户层cut，而不必只报告LP不可行。此处仍未交换外层matching/owner与对偶λ的量词。

## 6. 判别范围

所有价格均来自同一原完整策略、同一合法 actual-prefix 查询和同一 whole-IC 系数。所有取消均由原实际 I/G 网络实现，没有跨真实叶各领一份 G。

本表示给出精确可核查的候选诊断：若某固定 matching/owner 的 NET-DUAL 分离，仅否定该固定选择；须处理允许的全部自由选择才可否定一般 NET。反之，一个既存证书可行不证明一般接口。后续只用既存完整 SPE 证书作这种明确诊断，并把发现的价格 cut 交给真实全树 IC 分析。

## 7. 明确另立的弱化版本 NET-FRAC

若整数owner量词后来显得过强，可以直接允许证明中的分数owner，而不改变原博弈：对x∈O取α_ix≥0、Σ_iα_ix=1，只有x∈T_i时才允许α_ix>0。将实际I客户的owner→coverer边容量改为α_ix/c_x，R的owner终点库存改为α_ix。source仍是原实际g_i。每个积分owner分配都给合法Hall图，平均其可行流，说明任意这样的α仍有送满G source的流；也可直接平均all-J cut证明。

选择其中任一流，设R标签(i,x)的取消为0≤γ_ix≤α_ix，其余ρ_ix=α_ix−γ_ix从合法T_i查询初始化。客户总源量为1−Σ_iγ_ix，全部R残源仍恰为R−G。原真实query收益D_s不变，标量仍只有一个w_s=A_s/D_s。令p_(k;i,x)为从role i的T_i开始的一单位x源在role k的付款价，则

\[
K_k=\sum_{x\in R}\sum_i
p_{k;i,x}(\alpha_{ix}-\gamma_{ix}),
\qquad\eta_k=I_k+\sum_{x\in R}\gamma_{kx}.
\]

流守恒仍给Ση=W。因此另立的NET-FRAC若对全部输入可行，同样足以证明half。整数owner是α为0/1的特例，故原NET蕴含此弱化；不能把一个分数可行点报告成原整数NET见证。

固定OPT matching及不随α、γ改变的捕获路由规则后，α、γ、实际I角色边流及NET-FRAC全部约束均线性；较弱ΣK≤W也成为单个线性系统。它直接共同选择合法R源及实际I/G运输，不需要声称任一选中的分数γ能分解成每个随机owner世界的同一组整数流。若路由也随库存选择改变，不能未经另证仍称一个固定价格LP。

这里α只是原一个单位收益及其库存的代数分拆，所有标签收益相加仍等于原单位收益，原IC没有按标签另乘系数。若还要接owner势/COV，必须按同一个owner标签保留q与error：fresh source标签的e为零，非owner标签才用HIT≤1/2。不能先混合q、再把平均owner误差当成fresh误差。本文没有证明NET-FRAC或总价系统总可行，未以convexification闭合动态cut。

## 8. 与新 R/I 同一激活系数的直接对接

上述消元只用源量到吸收量的线性，不依赖旧fairshare路由。对[mixed的共享R/I激活](../mixed/joint_activation_owner_credit.md)，固定一次owner与路由规则，设其R单位残源价格仍记p_ix；I-query部分的固定付款基线记B_i^I。总吸收先合并再取唯一w=A_s/D_s，线性来源分解给

\[
K_i=B_i^I+\sum_{x\in R}p_{ix}(1-\gamma_x).
\]

这不是两份IC。若该实验的I-query总质量为κ^-、其角色目标为η_i+κ_i^-，只须把NET-DUAL中的d_i改为

\[
d_i'=\sum_xp_{ix}+B_i^I-I_i-\kappa_i^-.
\]

Γ与GREEDY均不变。总价减去相同新增源κ^-后，其最优值为

\[
\boxed{\sum_i B_i^I-\kappa^-+
\sum_k(v_k-v_{k+1})[|S_k|-r(S_k)].}
\]

原完整SPE给ΣB_i^I≥κ^-，因此I-query还携带自己的非负IC-slack费用；不能把它丢掉而只使用实际I停止信用。若联合α标签owner，则I基线、κ、R源费用及Hall边容量都按同一标签线性分解，仍可用一个固定matching的联合线性系统。这个接口没有支付row collision，也没有证明最终总价≤W。
