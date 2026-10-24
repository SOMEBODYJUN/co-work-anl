# 自洽池、自由分数安全值与PB平台：一般方向审查

2026-10-24。供Boss3内部沟通；未发送外部消息、未commit。输入范围固定为任意有限共同目录、任意人数、每个完整有序历史纯SPE。所有有限核算只重放下面两个已经指定的见证，未扫描策略、人数、参数或目录。一般Q-CAG-HALF仍OPEN。

**结论：混合SC存在性、对角Jensen、16客户纯SC反例及PB分数平台的准确范围均成立；尚无新的无条件一般福利界，故本轮不能无条件推出OPT_5≤2W。** 真正缺口是从完整原树IC得到一份可付款的共同背景；连续固定点和静态KKT均未支付此项。强要求mG≤W比half所需更强，应明确保留较弱充分门槛及背景查询信用，避免因强候选未闭合而误判原目标。

## 1. 已证通用关系及其来源

沿原实际路径B，在位置i强制A后沿原完整策略续行，删除当前槽得到V_i(A)。记

\[
d_i(A)=\sum_{x\in A}\frac1{1+c_x(V_i(A))}\le u_i,
\qquad
\lambda_x(A)=\frac1m\sum_i c_x(V_i(A)).
\]

原稿的列随机矩阵和查询函数为

\[
K_{TA}=\frac{\sum_i\#\{j\ne i:Z_i(A)_j=T\}}{m(m-1)},\quad
q(p)=Kp,\quad
\mu_x(p)=\sum_Ap_A\lambda_x(A),\quad
g_T(p)=\sum_{x\in T}\frac1{1+\mu_x(p)}.
\]

每列恰含m(m−1)个槽，所以K≥0且每列和为1，q确为合法主题分布。SC要求

\[
p_T>0\Longrightarrow g_T(p)=M(p):=\max_Ag_A(p),
\quad G(p):=\sum_Tp_Tg_T(p)=M(p)\quad(p\in\mathrm{SC}).
\]

原稿logit–Brouwer–零温极限证明正确：严格次优主题的概率指数趋零，极限即SC。SC集合由p_T[M(p)−g_T(p)]=0给出，是非空紧集。**这里完全没有使用SPE。** 因而存在性没有隐含付款、极小化或鞍点结论。

原IC加位置平均Jensen给每个确定A的全输入对角付款

\[
mg_A(e_A)\le\sum_i d_i(A)\le W.\tag{DIAG}
\]

它不能平均成mG(p)≤W，因为g_A(e_A)和g_A(p)的背景不同。以上均见[S1] §§1–3及[S4] §§1–3，与旧真实菜单去相关接口[S7] §5一致。

## 2. 自由分数值、真正安全值及SC的逻辑层级

空背景自由分数值为

\[
\delta_m=\min_{q\in\Delta\mathcal S}\max_T
\sum_{x\in T}\frac1{1+(m-1)q_x}.
\]

与不观察查询实现的整数竞争安全值v_m相比，已证方向只有

\[
\delta_m\le v_m,\qquad
\operatorname{OPT}_m\le(2m-1)\delta_m.\tag{STATIC}
\]

第一式由整数背景到其均值的Jensen得到；第二式不需要SPE。来源为[S6] §§1–2、[S7] §4及[S8]。

任何SC点仅给δ_m≤G(p)，一般并非自由分数鞍点：SC既不要求p=Kp，也不要求Kp极小化F(p,·)。甚至p↦G(p)的导数是

\[
\partial_{p_A}G(p)=g_A(p)
-\sum_x\frac{\alpha_x(p)\lambda_x(A)}{[1+\mu_x(p)]^2},
\qquad \alpha_x(p)=\sum_{T\ni x}p_T,
\]

故SC等值条件遗漏了响应背景随p改变的导数项，不能充当G极小化的KKT。相应地

\[
\delta_m\le\min_{p\in\Delta}M(p)
\le\min_{p\in\mathrm{SC}}G(p).
\]

这只是限制背景为K的像、再限制为SC所产生的弱化方向；不能倒推。**已付款SC只能证明自由分数δ聚合；不能由δ≤v反向宣称真正安全值v也被付款。** 分数均值cap不等于整数背景期望cap。

## 3. 真正OPEN付款，以及为half保留的较弱充分条件

[S1]的精确强候选是

\[
\forall(I,\sigma)\quad\exists p\in\mathrm{SC}(I,\sigma):\ mG(p)\le W.\tag{SC-STRONG?}
\]

这仍OPEN；本次没有证明它为真或为假。它若成立，STATIC给一般OPT_m≤(2−1/m)W，同一推导m=5给9W/5。不能把这个**条件**结论登记为新的五人界。

为half只需更弱的

\[
\exists p\in\mathrm{SC}:\ (m-\tfrac12)G(p)\le W,\tag{SC-HALF?}
\]

m=5是(9/2)G(p)≤W。更自由的根桥W≥(m−1/2)δ_m仍是既有OPEN充分条件；它不要求背景来自这个自洽池。强SC付款失败也不自动否定这些较弱条件，更不否定half。

还应保留静态证明中的背景查询信用。对任意q及其分数查询值g，置M=max_Tg_T、R=Σ_Tq_Tg_T；取最优m主题、其客户重数d_x，逐客户有

\[
\mathbf1_{d_x>0}\le\frac{d_x+(m-1)q_x}{1+(m-1)q_x}.
\]

求和得**不丢弃R的全输入关系**

\[
\operatorname{OPT}_m
\le\sum_{j=1}^m g(T_j)+(m-1)R
\le mM+(m-1)R.\tag{KEEP-q}
\]

在SC点，M=G且R≤G，所以

\[
\operatorname{OPT}_m\le mG(p)+(m-1)R(p)
=(2m-1)G(p)-(m-1)[G(p)-R(p)],
\quad R(p)=\sum_Tq_T(p)g_T(p).
\]

因此存在SC点满足mG+(m−1)R≤2W已足够；m=5的直接压力测试是5G+4R≤2W。它可比(9/2)G≤W更弱，因为保留G−R≥0信用。**这只是[S6] §2、[S7] §4的既有静态代数保留原项，不是新增福利定理，也不是另开调系数主线。** 真正新增承重内容仍必须是原树IC对右端的共同付款。

## 4. 未付项的精确形式：SC没有自动控制查询—后继相关性

令I均匀取实际位置、A∼p；α_x=1_{x∈A}、L_x=c_x(V_I(A))、μ_x=E L_x。真实IC支付

\[
D(p)=\mathbb E\sum_x\frac{\alpha_x}{1+L_x}\le W/m.
\]

精确倒数展开给

\[
D(p)-G(p)
=-\sum_x\frac{\operatorname{Cov}(\alpha_x,L_x)}{(1+\mu_x)^2}
+\sum_x\frac{\mathbb E[\alpha_x(L_x-\mu_x)^2/(1+L_x)]}{(1+\mu_x)^2}.
\tag{COV}
\]

证明只需使用

\[
\frac1{1+L}=\frac1{1+\mu}-\frac{L-\mu}{(1+\mu)^2}
+\frac{(L-\mu)^2}{(1+L)(1+\mu)^2}
\]

后乘α取期望。设真实IC松弛s=W/m−D≥0，C为COV的协方差总项，J为非负曲率总项，则

\[
W/m-G=s-C+J.
\]

所以强付款恰缺某个SC点上的C≤s+J。SC最佳查询等式目前没有导出这个不等式；需要真正使用别的完整历史IC。该公式是旧去相关余量的直接展开，不认领新颖性。capacity在固定策略锥、固定p=(e2+e5)/2下的20条IC精确组合[S4] §4确实付款，但只限该锥/该p，不能推广为全m机制。

## 5. 两个固定见证：纯点与all-p失败不触及混合付款

本次从单位客户定义独立重放两份指定策略，均检查43个有序节点、258条含自身IC及全部六列查询，不调用作者审计、规范SPE求解器或优化器。所有IC通过。可重跑代码与完整Fraction输出见本目录[self_consistent_fixed_witness_audit.py](self_consistent_fixed_witness_audit.py)、[JSON](self_consistent_fixed_witness_audit.json)。脚本记录635输入文件及SHA256，16客户输入逐项来自[S2] §2。

**16客户例。** m=3、实际(0,3,4)、利润(9/2,5,9/2)、W=14、OPT=16。全部六个纯查询的唯一最佳查询为(5,5,5,2,2,2)，严格改善差为(3/8,1/35,3/56,9/28,1/12,1/12)。因此普遍纯SC存在性确实为假；不是只发现一个小循环。[S2] §§4–6的全单纯形分类亦正确：唯一SC点为

\[
p=t e_2+(1-t)e_5,\qquad t=(27-\sqrt{537})/6.
\]

更强的准确区分是，全部36个纯列/查询值至多107/24<14/3。每个g_T对p凸，所以g_T(p)≤Σ_Ap_Ag_T(e_A)≤107/24，对**所有p**都已付款。该例根本没有混合付款缺陷。独立既有全单纯形解析审查见[S5]。

**635客户旧all-p例的补充核对。** 原坏p=(e2+e5)/2确有3G−W=40617/340340>0，但

\[
g_5(p)-g_2(p)=421947/170170>0,
\]

所以它不是SC。并且同一指定见证已有一个**已付款纯SC e1**：其q分子是(2,0,1,2,1,0)/6，六查询值依次为

\[
(36111/280,\ 5291/35,\ 35067/280,\ 31263/280,\ 4554/35,\ 5403/40).
\]

标签1唯一最大，g1=5291/35<154=W/3，付款余量W−3g1=297/35。故这个all-p反例不仅尚未反驳SC，实际上有明确的已付款SC。这里是固定旧见证的精确再核对，不是新反例、新half结果或普遍付款证据。

在旧坏p上D=154恰用尽真实IC，C−J=13539/340340>0，精确解释其all-p失败来自何处。它不支持继续围绕all-p不等式修补。

## 6. PB分数平台：只关闭任意合法背景的局部桥

[S3]的真正鞍点证明成立，关键是两个不同条件都已核验：q*下p*支持查询最优，且固定p*时背景负梯度满足H_R>H_D，q*支持全目录H最大主题；singleton查询和梯度亦都被严格压住。不能只靠查询等值证明鞍点。

参数沿用既有PB完整策略[S9]，L=7422/2063，δ_r(b)=Δ=d[f(1+L)+2g(1)]，前三人的真实利润u=3d f(3)<Δ。j=1,2,3的合法主题混合概率

\[
\theta_j=\frac{3(L-j)}{r-j-1}
\]

均在(0,1)，通过“一个hot+两个outside”与“三个outside”的混合逐客户保持分数总负载L；可行域嵌入给反向下界。因此四个连续节点的δ均为Δ，局部余额

\[
u+(R-1)\delta_{R-1}(b_{\mathrm{current}}+F)-R\delta_R(b_{\mathrm{current}})
=u-\Delta<0
\]

严格成立。本次Fraction重算15个查询/梯度/负载条件通过，完整SPE身份仍继承旧PB全部历史解析证明，未重新独立证明巨大策略树。

这里b由singleton重复形成且已覆盖全部客户，未证为根SPE实际前缀。因此只反驳**任意合法背景**FF-LEADER及逐步非负δ链；不反驳根逐人δ、根强/弱δ聚合、在轨受限桥或half，也不反驳SC付款。固定原PB实际尾的总剩余收益事实上满足

\[
\sum_{i=1}^r u_i
=d[9f(3)+1648f(1)+824f(2)+4944g(2472)]>r\Delta,
\]

已用Fraction核验；因此本例确实允许后段补偿前三步欠债，不能从三个负局部余额推断该剩余总量失付。独立既有平台审查来源为[S10]。

## 7. 给作者的具体沟通建议

1. 请把最新义务始终写成“存在某个已付款SC”或更弱的根/在轨共同付款，明确是mG、(m−1/2)G，还是保留R的mG+(m−1)R≤2W。三者不是已证结论，m=5目前均没有无条件付款。
2. 不再修补普遍纯SC存在性，也不继续all-p池化付款或任意合法背景逐步非负链。这三项已有各自准确反例；它们均没有反驳根half。635见证已经有e1付款，16见证全部p付款，不能再以二者作为混合SC缺陷的证据。
3. 下一份值得继续的一般推导应点名一条新承重关系：例如完整离轨IC如何支付COV的总相关项，或如何直接支付KEEP-q的比较覆盖。请明确使用哪些原树行、同一利润是否重复使用、量词是否包含所有完整历史平局。静态固定点、查询活跃条件与背景KKT不是该付款。
4. 将同一一般关系直接代入m=5：若只能得到“假设SC付款则9/5”，应据实写条件结果并讨论真正缺口；若保留R，则检查是否已无条件得到5G+4R≤2W。不要转成五人加行、锥扫描或系数优化。

## 来源索引

- [S1] `research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round4_general/root/self_consistent_pool.md`。
- [S2] 同actor `round4_general/direct/self_consistent_pure_shortcut.md`。
- [S3] 同actor `round4_general/security/pb_fractional_saddle_plateau.md`。
- [S4] 同actor `round4_general/capacity/self_consistent_pool_review.md`、`mixed_sc_dual_audit.json`。
- [S5] 同actor `round4_general/construction/review_no_pure_selfconsistent.md`。
- [S6] `research/workspaces/customer-attraction/R-077c0cacfba24288be91dee1acf6d484/security/free_fractional_security.md`。旧文FF-LEADER的OPEN状态被[S3]仅在任意背景版本上更新；不能照抄其旧接续建议。
- [S7] `research/current/customer_attraction/general_half_proof.md` §§4–5。
- [S8] `research/current/customer_attraction/oblivious_security.md`。
- [S9] `research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/menu/pair_attack.md` §§2–7。
- [S10] R-d3981c0168644971803a9c3380ed687c `round4_general/induction/independent_review_pb_fractional_plateau.md`。
- 固定635原始输入：R-d3981c0168644971803a9c3380ed687c `round4_general/security/pooled_mean_background_raw.json`；本次核算输出记录其SHA256，便于父方重跑。
