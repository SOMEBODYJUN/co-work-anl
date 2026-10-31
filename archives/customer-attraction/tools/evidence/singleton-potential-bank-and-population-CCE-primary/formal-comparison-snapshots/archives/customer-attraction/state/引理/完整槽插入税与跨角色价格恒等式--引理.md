---
id: "customer-attraction/complete-slot-insertion-tax-cross-role-price-identities"
kind: "lemma"
type_tag: "引理"
title: "完整槽插入税与跨角色价格恒等式"
status: "proved-static-identities-and-lower-bound; specified-current-increment-bridge-refuted; common-payment-open"
summary: "一般整数过去与完整r槽的INS、角色总账、根后继税和平稳身份全部自足保留；真实全人数SPE给固定r当前增量无正统一付款系数。主题平稳不支付跨已揭示历史的相关性。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_audit/insertion_tax_and_column_correlation.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_audit/insertion_tax_and_column_correlation.md"
---

# 完整槽插入税与跨角色价格恒等式

## 对象、来源和结论级别

主源是[7390B完整原文](../../../../tools/evidence/first-saturation-and-insertion-credit-primary/original/37b0cc25eda54afa70b8/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_audit/insertion_tax_and_column_correlation.md)，两个冻结分支字节相同。本页保留其一般背景、所有完整槽、同列与独立重抽、全角色和根/后继两种总账、平稳核及跨深度断点；不以此前作为DD相关材料已读，冒充它此前已完成primary处置。来源自称独立机制接续，是2026-10-23的研究身份；本页没有外审或新颖性结论。

单位客户、有限非空共同主题目录，允许空主题、重复标签和零客户。固定一个合法有序过去，客户负载为非负整数b_x；还剩r≥1个真实槽。Q是有限概率分布，每列Z均含恰r个合法主题。以下静态代数不要求Q来自SPE，不能因使用“真实槽”就假设其列有激励兼容性。记n_x=c_x(Z)，n'_x为独立同分布副本，

\[
w_x=\mathbb E_Q\frac1{b_x+1+n_x},\qquad
v_Q(T)=\sum_{x\in T}w_x.
\]

分母的1属于一个独立额外查询。定义q_Q为先抽完整列、再从r槽均匀抽一个主题所得的**主题边际**，然后独立于竞争列重抽查询。因此

\[
v_Q(q_Q)=\frac1r\sum_x\mathbb E n_x\,
\mathbb E\frac1{b_x+1+n_x}.
\]

这不同于在同一列上抽槽后直接算价。当前原模型用全部有序历史纯SPE及任意平局；本页末段调用真实策略时保留这一完整身份，不把负载相同当成历史可合并。

## 插入税、负载分散和精确恒等式

原r名玩家的平均收益、同列插入税与负载分散分别为

\[
\bar U_Q=\frac1r\mathbb E\sum_x\frac{n_x}{b_x+n_x},\qquad
T_Q=\frac1r\mathbb E\sum_x
\frac{n_x}{(b_x+n_x)(b_x+1+n_x)},
\]
\[
\Gamma_Q=\frac1{2r}\sum_x\mathbb E
\frac{(n_x-n'_x)^2}{(b_x+1+n_x)(b_x+1+n'_x)}\ge0.
\]

n_x=0的两处项均定义为0；即使b_x=0也不产生0/0。有过去玩家时r Ubar只是剩余玩家总利润，不是全部覆盖福利，过去仍分享其覆盖的客户。

同一列内均匀抽槽再额外插入，其平均价恰为

\[
\frac1r\mathbb E\sum_x\frac{n_x}{b_x+1+n_x}
=\bar U_Q-T_Q.
\]

独立重抽竞争列的增量，逐客户用独立副本交换得

\[
\mathbb E n\,\mathbb E f(n)-\mathbb E[nf(n)]
=\frac12\mathbb E[(n-n')(f(n')-f(n))]
=\frac12\mathbb E\frac{(n-n')^2}{(b+1+n)(b+1+n')}.
\]

因此全输入准确成立

\[
\boxed{v_Q(q_Q)=\bar U_Q-T_Q+\Gamma_Q.}\tag{INS}
\]

Gamma=0当且仅当每一客户在Q的正概率支持中负载恒定；各槽的有序主题仍可不同。这是同一**完整r槽**背景上的恒等式，不通过删去当前槽得到r−1槽。

## 一个一般下界，不是价格封顶

n≥1时1/(b+n+1)≤1/(b+2)，故从同列价保留

\[
v_Q(q_Q)\ge\frac1r\sum_x\frac{b_x+1}{b_x+2}
\mathbb E\frac{n_x}{b_x+n_x}+\Gamma_Q
\ge\frac12\bar U_Q+\Gamma_Q.
\]

q_Q是合法主题分布，所以

\[
\boxed{\max_{A\in\mathcal S}v_Q(A)
\ge v_Q(q_Q)\ge\tfrac12\bar U_Q+\Gamma_Q.}\tag{LOW}
\]

空背景时r Ubar=E W，因子二下界完全不需要SPE。要证明某个根完整菜单存在价格上界M_full≤u，必须另构造一份便宜的Q；不能把LOW反读成它的上界。一般M_full的旧OPEN现已有[银行完整根菜单反例](../反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)，而本页静态恒等式保持成立。

## 全人数真实背景例：插入税并不由当前增量统一支付

主源引用的[6504B全人数重构](../../../../tools/evidence/first-saturation-and-insertion-credit-primary/related/ef21819792cb2a9aac5f/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_audit/meta_price_all_players_reconstruction.md)也实际完整读过，仅作本批相关来源、不额外done。它给每个m≥2、正整数L的一份完整SPE，而不只是任意大背景的形式例。目录只有不交主题A、B，大小分别mL、L。策略在全部有序历史规定：已经出现B则以后全选A；此前全A时，非末位选A，末位选B。

若历史已含h≥1次B，当前选A后A终数m−h，收益mL/(m−h)；选B后收益L/(h+1)，前者严格大。此前全A且不是末位时，选A得到mL/(m−1)>L，选B只得L；全A的末位两行动都得L，指定B合法。因此重复、离轨和平局全包含，得到完整SPE。实际覆盖W=OPT_m=(m+1)L，不是half反例。

固定实际前缀k次A，余r=m−k≥2。当前强制A或B的完整剩余列都含r−1个A和一个B；过去背景A负载k、B负载0。根真实收益

\[
d_A=\frac{mL}{m-1},\quad d_B=L,\quad u=d_A;
\qquad K=\begin{pmatrix}L&L\\L/2&L/2\end{pmatrix}.
\]

K列是当前强制A/B后的完整r槽，行是额外查询A/B，**保留当前槽**。唯一对称META-Nash为p=delta_A，C=p^TKp=L，D=d_A。完整槽/后继槽的主题边际分别为

\[
q_{full}=\frac{r-1}{r}A+\frac1rB,\qquad
q_{tail}=\frac{r-2}{r-1}A+\frac1{r-1}B,
\]
\[
v_Q(q_{full})=L\left(1-\frac1{2r}\right),\qquad
v_Q(q_{tail})=L\left(1-\frac1{2(r-1)}\right).
\]

所有列负载相同，Gamma=0。INS的另外两项精确为

\[
\bar U_Q=\frac{r-1}{r}\frac{mL}{m-1}+\frac Lr,
\qquad T_Q=\frac{(r-1)L}{r(m-1)}+\frac L{2r}.
\]

B槽插入税L/(2r)不会随实际过去k增大消失，但根真实收益增量D−C=L/(m−1)会消失。因此

\[
\frac{D-C}{C-v_Q(q_{full})}=\frac{2r}{m-1},\qquad
\frac{D-C}{C-v_Q(q_{tail})}=\frac{2(r-1)}{m-1}.\tag{RATIO}
\]

固定r、增大m的合法实际前缀使两比都趋0；不存在仅依赖固定r的正统一系数alpha，能在这类输入总令D−C≥alpha(C−v_Q(q_full))。若允许alpha依赖m,r，则全槽必要alpha≤2r/(m−1)，尾槽≤2(r−1)/(m−1)，不是充分性定理。特别alpha=1的旧2C≤D+v(q_tail)恰在m−1>2(r−1)失败，全槽对应m−1>2r；r=2即分别k≥2、k≥4。

这里最大完整查询恒为L<u；任意根行分布p的价格C≤L且D≥L，所以全p强推送、M_full以及half在**此族**都没有失败。失败的是要求当前增量支付整个槽边际插入亏损的特定桥。给任意Q和行分布p的一般剩余量只有

\[
C-v_Q(q_Q)=C-\bar U_Q+T_Q-\Gamma_Q,\qquad C=p^TKQ.
\]

代数不给C−Ubar符号。即使Q=p且p是K的对称Nash，只由v_Q(q_Q)≤C知道左边非负，也不推出D≥C。

## 同一列分布的全角色总账

对完整列中的角色j，定义

\[
D_j=\mathbb E\sum_{x\in Z_j}\frac1{b_x+n_x},\qquad
C_j=\sum_x\Pr(x\in Z_j)w_x.
\]

C_j把该角色主题按其**无条件边际**独立重抽，再查完整r槽；不是第j个实际子博弈可取得的续局收益。由sum_j Pr(x∈Z_j)=E n_x和INS直接得到

\[
\boxed{\sum_{j=1}^r(D_j-C_j)=r(T_Q-\Gamma_Q).}\tag{ROLE}
\]

此式可以同时核所有角色的总负债，不能把每个C_j重新认作其各自真实历史的IC右端。它没有控制根与其他角色之间如何分配总收益。

## 根/后继分离：另一协方差身份

现在固定原完整纯SPE，根源B按p随机强制，之后原策略确定。记a_x=1_B(x)，真实后继负载k_x**排除根B**，因此该列n_x=a_x+k_x。设

\[
v_x=\frac1{b_x+1+k_x},\quad
t_x=\frac{a_x}{(b_x+1+k_x)(b_x+2+k_x)},\quad p_x=\mathbb E a_x.
\]

独立完整列的额外查询价使用E(v_x−t_x)，真实根利润使用E(a_xv_x)，所以

\[
\boxed{D-C(p,p)=\sum_x\operatorname{Cov}(a_x,v_x)
+\sum_xp_x\mathbb E t_x.}\tag{ROOT}
\]

这不是把完整负载n直接代入v=1/(1+n)的旧SRC身份：ROOT先移走根自身，税项有p_x；[平均菜单](../候选/最优并集税与平均真实菜单的付款接口--候选.md)的完整源税是E[a_x/(n_x(1+n_x))]。两个精确坐标均可用，但不能只保一个“协方差”名称就交换其负载、税或抽样。

## 平稳主题边际不等于角色收益或META分布

定义source到随机完整槽的有限Markov核

\[
P^{full}_{BA}=\frac1r\#\{j:Z_j(B)=A\}.
\]

它总有平稳主题分布p：任取p_0，Cesaro平均q_N=N^{-1}sum_{k=0}^{N-1}p_0P^k在紧单纯形有收敛子列，且q_NP−q_N=(p_0P^N−p_0)/N趋0；极限即平稳。此为本页补全的有限存在性说明，不导入外部论文或算法复杂度。

r>1时，随机真实后继槽核P_tail满足

\[
P^{full}=\frac{I+(r-1)P^{tail}}r,
\]

所以二者平稳分布集合完全相同。r=1时P_full=I，尾核不存在，不使用除r−1的式子。平稳p使q_full=p，于是INS化成

\[
\boxed{D-C(p,p)=D-\bar U_p+T_p-\Gamma_p.}\tag{STAT}
\]

要由此支付stationary strong-push仍需真实SPE证明D−Ubar≥Gamma−T。平稳性没有该符号，也没有说这份p同时是矩阵K的对称Nash。不能把“存在平稳p”和“存在META p”拼为同一个分布。当前[36客户平稳收益见证](../反例/成员平稳但根收益不可交换的三人见证--反例.md)更具体给唯一平稳p下根收益10<34/3平均槽收益，说明单独D≥Ubar已失败；它没有直接决定带T/Gamma的STAT符号。其现存同SHA成功审计不重复运行，本页不将其报告冒称本次新证据。

## 已揭示历史之后不能直接望远镜

只有根源随机、之后完整纯策略确定时，任意非空真实有序历史已揭示其首行动B。给定该历史，后续以及根成员均确定，条件协方差与条件Gamma为0。但全协方差公式还保留

\[
\operatorname{Cov}(a,v)=
\mathbb E\operatorname{Cov}(a,v\mid H)
+\operatorname{Cov}(\mathbb E[a\mid H],\mathbb E[v\mid H]).
\]

第二项是不同根历史之间的相关性，并未因深层的第一项为0而消失。深层SPE只能比较各自已揭示历史下的真实行动和后继；将这些零条件量相加，不能领取跨根历史的新付款。

本页至此是精确代数、LOW下界、RATIO特定桥障碍和明确未付角色/跨历史义务。与[三八源界](../引理/整数完整负载的三八源去相关界--引理.md)接入时必须映射同一整数完整负载、同一指定源和同一分布；裸3/8系数不替代保负源税的完整INT。一般m/当前六人half、META共同付款、首次饱和B≤E+U都没有由这些恒等式闭合。本批无原数学程序、新策略复演或有限扫描运行。
