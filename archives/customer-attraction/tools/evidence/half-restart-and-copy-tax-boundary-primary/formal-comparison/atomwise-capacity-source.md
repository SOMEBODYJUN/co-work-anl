---
id: "customer-attraction/atomwise-capacity-two-swap-row-teleport-and-query-debt"
kind: "lemma"
type_tag: "引理"
title: "逐原子容量二交换、行内再启动分布与换查询债"
status: "proved-conditional-signed-bounds-and-row-distribution; covariance-source-compatibility-unresolved"
summary: "恰五人raw域保signed价格/门槛边界，atomwise κ库存给κR/2；行内teleport控制行动到达与势漂移，但不推出原全端点容量，改行查询另付Qinput及旧中心校正。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/exchange/source_capacity_two_interface.md"
---

# 恰五人模型与一个给定raw对偶

采用[有限单位客户、有限非空共同目录、每份完整历史纯SPE模型](../定义/共同目录完整历史模型--定义.md)，本源接口专指m=5。保空主题、重复、零客户及任意离轨平局。固定实际前缀\(h_i\)，对每个完整raw有序终局允许任意进入标签和未来主题，包括原实际标签。令
\[
C_i(z)=d_i(z)+\sum_{k>i}[M(z_{<k})-u_k(z)],\quad
r_i(z)=\eta_i+\mu C_i(z)-a\cdot\ell_i(z)\ge0.
\]
\(\ell_i\)删除同一进入槽，\(a\ge0\)固定，\(\mu\ge0\)来自明示共同成本约束，η任意。M是当前人max-min可信门槛，非原σ任意选值；本页要求r对**每个允许raw终局**成立，不要求单点raw本身cap可行或为SPE。

# 保留边界的signed交换

令\(z=(h_i,A,B,Y)\)、\(z^s=(h_i,B,A,Y)\)，进入/第一后继收益为d、v。计数同构保深尾M，两人收益交换，\(\ell_i(z^s)-\ell_i(z)=\mathbf1_A-\mathbf1_B\)。设
\[
K_i(T)=M(h_i,T),\qquad P_i(T)=a\cdot\mathbf1_T+\mu K_i(T).
\]
净成本展开给
\[
r_i(z^s)-r_i(z)=2\mu(v-d)+P_i(B)-P_i(A).
\]
对任意非负源权\(\theta_{i,z}\)，由目标r非负，
\[
\boxed{\mu\sum\theta(d-v)\le\frac12\sum\theta r_i(z)
+\frac12\sum\theta a\cdot(\mathbf1_B-\mathbf1_A)
+\frac\mu2\sum\theta[K_i(B)-K_i(A)].}\tag{U}
\]
无需行动平衡，但两个边界是**有符号总和**，不能换为\((d-v)_+\)或边绝对值。μ=0照常，不作除法。

# 原端点原子的容量与一次R库存

给定一份特定原源库存\(p_{i,z}\)，每行质量一，令\(R=\sum_{i,z}p_{i,z}r_i(z)\)。若
\[
0\le\theta_{i,z}\le\kappa p_{i,z}\quad\text{对每个完整源原子 }(i,z),
\tag{CAP}
\]
则\(\sum\theta r/2\le\kappa R/2\)。κ=2恰至多用一份R，不是两份。每个个别包只跨一次层不保证CAP：不同来源可在同一原子合流。只限制进入行动边际也不足以限制同一行动内不同尾/见证原子的拥塞。

记\(\gamma_a=\max_Ta\cdot\mathbf1_T\)。若每行原库存的进入边际同为q，逐原子有\(a\cdot(B-A)\le\gamma_a-a\cdot A\)，右端非负，故可用CAP上界：
\[
\sum\theta a\cdot(B-A)\le5\kappa[\gamma_a-E_q(a\cdot A)].
\]
用不足五行时仍可取这五行上界。令\(\Delta_K=\sum\theta[K_i(B)-K_i(A)]\)，得到
\[
\mu\sum\theta(d-v)\le\kappa R/2
+(5\kappa/2)[\gamma_a-E_q(a\cdot A)]+\mu\Delta_K/2.
\]
q为某最优五元组均匀分布时，中项为\(\kappa P_{{\rm opt},a}/2\)，其中\(P_{{\rm opt},a}=5\gamma_a-\sum_j a\cdot T_j\)。通常a=ρt²，它不是静态[最优组合影价](最优组合影价松弛与正损失替换停界--引理.md)的t价Popt。换查询成该元组还改变源/KKT差额，不能保原已资助R。

完整槽另用\(r_i^+=\eta_i+\mu C_i-a\cdot c\)，交换保完整c，行动a价边界消失，界为\(\kappa R_+/2+\mu\Delta_K/2\)。须用其自身dual/库存，不能同时花删除槽R和完整槽R+。

# 行内再启动分布：行动到达支配与势漂移

固定同一行的有限第一后继Markov核\(T(A,B)\)，选r支持在\(P_i\)最大主题。存在唯一概率分布
\[
\boxed{p=\tfrac12(r+pT)=\sum_{k\ge0}2^{-k-1}rT^k.}\tag{TELEPORT}
\]
级数非负且权和一，代入得不动点；任意两解的\(\ell_1\)差经随机核至多缩为一半，故唯一。于是
\[
pT=2p-r\le2p,
\qquad E_{A\sim p,B\sim T(A,\cdot)}[P_i(B)-P_i(A)]
=E_pP_i-E_rP_i\le0.
\]
在**以这份p和T为源律**的行内流中，若每个完整原子只用一次，U给原半库存signed界而不需平稳性。\(pT\le2p\)是行动坐标的到达支配；它本身不证明任意多个起源、不同尾见证合流后的完整原子CAP。T若需提升为完整原子/真实Cov源，还须保其条件尾分布和原库存身份。

不同actual-prefix的\(P_i\)及重启r可不同，该构造不保证各行有共同p，更不保证它们是福利鞍点原查询。原稿将此引理归于tree13提出、exchange13核符号；本页保这一来源身份，不把行内构造称为全树协方差流。

# 共同重选查询与新KKT中心的精确债

若行查询\(p_i\)与新参考域共同选取，令\(\rho_i(x)=\Pr_{p_i}[x\in A]\)、\(\rho=\frac15\sum_i\rho_i\)、\(t=(1+L)^{-1}\)、\(a=\rho t^2\)，\(\gamma=\max_Tg_t(T)\)。源为同一原σ的真实强制叶，记\(I=\sum_i(u_i-E_{p_i}d_i)\ge0\)，并定义
\[
Q_{\rm input}=5\gamma-\sum_iE_{p_i}g_t(A)\ge0,
\]
\[
C=\sum_iE_{p_i}\sum_{x\in A}t_x^2(\ell_i(A)_x-L_x),\quad
D=\sum_iE_{p_i}\sum_{x\in A}\frac{t_x^2(\ell_i(A)_x-L_x)^2}{1+\ell_i(A)_x},
\]
\[
\mathrm{Cov}=\sum_{i,x}E_{p_i}[(\mathbf1_{x\in A}-\rho_x)t_x^2\ell_i(A)_x],
\quad G=5a\cdot L-\sum_iE_{p_i}a\cdot\ell_i(A).
\]
若该L在**新同一shadow/可行域**下给相应非负KKT差G，直接倒数展开得\(C=\mathrm{Cov}-G\)，以及
\[
\boxed{W-5\gamma=I+G+D-\mathrm{Cov}-Q_{\rm input}.}\tag{QUERY-DEBT}
\]
原查询不在最大价格支持上就有整份Qinput成本，不能因teleport势漂移好而省略。

完整槽自身用G+，删除源对完整参考的账另加\(5\|\rho t\|^2\)。设\(\mathcal B=I+G^++D_0+5\|\rho t\|^2\)，完整静态信用\(Q^+=5\gamma-H_{\rm bg}\ge0\)，\(\mathrm{OPT}_5\le10\gamma-Q^+\)。足够金额为
\[
\mathrm{Cov}_0\le\mathcal B-Q_{\rm input}+Q^+/2.
\]
因\(Q^+=Q_{\rm input}+[\sum_iE_{p_i}g_t-H_{\rm bg}]\)，也可写\(\mathcal B-Q_{\rm input}/2+[\sum_iE_{p_i}g_t-H_{\rm bg}]/2\)。最后残差没有免费非负符号，需真实新静态比较而非改写。

# 保留旧shadow时须补足的完整中心项

为把原稿的旧中心警告写成可直接检查的恒等式，固定同一L、t及旧\(a_0=\rho_0t^2\)，令\(\xi_i=E_{p_i}\ell_i\)，并定义逐行中心协方差
\[
V=\sum_{i,x}t_x^2\operatorname{Cov}_{p_i}(\mathbf1_{x\in A},\ell_i(A)_x),
\quad G_0=5a_0\cdot L-\sum_i a_0\cdot\xi_i.
\]
对上面同一C展开，完整地有
\[
\boxed{C=V-G_0+\sum_{i,x}(\rho_i(x)-\rho_0(x))t_x^2(\xi_i(x)-L_x).}\tag{OLD-CENTER}
\]
原稿列\(\sum_i(\rho_i-\rho_0)t^2\xi_i\)作为非零端点项警告；若当作完整账，还须保\(-\sum_i(\rho_i-\rho_0)t^2L\)。只有\(\frac15\sum_i\rho_i=\rho_0\)时后一项为零，才只剩所列端点项。本式为本次按定义补全的中心差，不是原稿已有的付款。

即使保旧shadow，上式G0已经用新\(p_i\)的源均值；它也未必等于原旧查询下已资助的G。原先的R库存不会因保持向量a0就自动保持。这与QUERY-DEBT是不同约定，须先声明使用哪个中心，不能把新ρ替入旧银行。

# 剩余义务与当前状态

仍须将实际Cov表示成**同一**signed d−v需求，在原完整原子上证明CAP并支付规范门槛边界与输入价格债；没有这样的联合映射。行内pT边际支配、原子容量二条件及新/旧source是三项独立要求。零损失min-Q gate也未获得正损失金额，旧165/2不被这些代数消除。

主源5336字节及tree13相关交接全文实读，原件见[资源](../../tools/evidence/cross-role-capacity-primary/README.md)。本源无程序扫描；本批仅对另两固定实例运行cross-role原QA，不作容量/teleport实验。原五人OPEN是本条件路线未闭合，现行五人half另证成立；本页也不把系数5机械换成6充作六人定理。关系为raw SWAP→条件CAP界、有限核→行内分布、倒数展开→新查询债及旧中心差，超图留第三阶段。
