# 同一完整花瓣策略的全p付款与分数minimax归约

身份：Boss2；任务 `boss2-wave4-repair-f4379d37833afc48`；内部词：Boss2 W4 花瓣已付minimax。

本次定向替代原 `ca-b7bf-petal-paid-pool-all-to-half`。源改为已证对象 `customer-attraction/pooled-response-load-jensen-credit-and-conditional-interface` 与已证花瓣付款 `M-a73c059007b34941839ba1683f0d4479`，共同按ALL使用。前者的真实分数背景构造及已经canonical的 `ca-b7bf-pool-ledger-to-conditional-minimax` 的完整归约在下文展开，后者支付本族同一策略的全部p前件。`M-9f2ee4fe4a7f454f83c30456b204b8f6` 保持原conditional对象和精确中间命题身份，不升proved，也不假设一般全p付款成立。

## 固定模型、策略与全p付款

固定整数m≥2、K≥2。取两客户核心A、与它不交的2(m−1)客户块B及互异私有客户c_j，目录标签为C=A、B、P_j=A∪{c_j}。固定一份原完整策略σ：根C，其余非末位B；末位查看整个有序历史，记非B行动数t。t=0选P_1；t=1且唯一非B为C时选B；t=1且唯一非B为P_j时选预先固定且不同于j的P_k；t≥2选B。这一预先固定映射在整个证明中不更换。

原策略证明对所有离轨历史及合法行动成立：末位在前缀t、P_j重数r_j下的收益分别为2(m−1)/(m−t)、2/(t+1)、2/(t+1)+1/(r_j+1)。按t=0、t=1唯一C、t=1唯一P_j、t≥2四类逐项比较即支持其规定动作。更早非根位置按当前前缀的t分类：t=0时，遵从B收益2，改C后末位B、改P_j后末位另一花瓣，偏离收益各恰2；t=1且唯一非B为C时，遵从B收益2，改非B后非B总数为2，C收益至多1、花瓣至多2；t=1且唯一非B为P_j时，遵从B后末位另一花瓣，B收益2(m−1)/(m−2)>2，改非B后的C/花瓣收益至多2（此非末位情形仅m≥3）；当前前缀t≥2时，遵从B收益2(m−1)/(m−t)>2，改非B令核心总重数至少3，C收益至多2/3、花瓣至多5/3。根C、改B、改P_j各得2。所有分母正，m=2时没有更早非根非末位位置。因此该规则给全部有序历史的完整纯SPE，actual为CB^{m−1}、每人收益2、W=2m；m=1、K=1不在本族。

对任意同一目录分布p，写p_C=a、p_B=b、p_{P_j}=s_j，其中a,b,s_j≥0且a+b+Σs_j=1。实际第i位置强制查询T∼p之后，严格沿同一σ续完并删除偏离者当前槽，保留固定过去。根查询C的删除背景是B^{m−1}；根查询B或P_j的删除背景是B^{m−2}加一个真实花瓣。其余每个actual位置，无论查询何标签，删除背景均为C,B^{m−2}。令ρ_j为根查询抽自p时产生花瓣P_j的概率；ρ_j≥0、Σρ_j=1−a。因此跨actual位置和查询平均后的真实负载为

\[
H_{A}=1-a/m,\qquad H_B=m-2+a/m,\qquad H_{c_j}=\rho_j/m.
\]

令t_x(p)=Pr_{T∼p}(x∈T)。池化查询值为

\[
P(p)=\sum_x\frac{t_x(p)}{1+H_x(p)}
=\frac{2(1-b)}{2-a/m}+\frac{2(m-1)b}{m-1+a/m}
+\sum_j\frac{s_j}{1+\rho_j/m}.
\]

因m≥2、0≤a≤1、ρ_j≥0，所有分母严格正，包含p的单纯形边界。第二项≤2b，末项≤Σs_j=1−a−b，第一项=(1−b)[1+a/(2m−a)]，故

\[
P(p)\le 2-a+\frac{a(1-b)}{2m-a}\le2=W/m.
\]

最后只用a≥0和1−b≤2m−a。该式对任意p成立，不必选定具体ρ分配，不更换σ或真实后继。这正是已证M-a73c…的全p付款，而不是开放的一般POOL强式。

## 合法分数背景与minimax的完整展开

记有限目录为𝒮，客户向量1_T保留原标签覆盖。自由分数背景域为

\[
\mathcal K_{m-1}=(m-1)\operatorname{conv}\{1_T:T\in\mathcal S\}.
\]

每个真实删除背景含恰m−1个合法目录标签。其负载和属于𝒦_{m−1}；平均i和T∼p后仍在这一紧凸域内。因此每个p各自构造出的H(p)∈𝒦_{m−1}。这里不是宣称一个共同H可同时封顶所有查询，也不是冻结后继或把计数历史合并。

令f_L(T)=Σ_{x∈T}1/(1+L_x)，F(p,L)=Σ_Tp_T f_L(T)=Σ_xt_x(p)/(1+L_x)，并令

\[
t_m=\min_{L\in\mathcal K_{m-1}}\max_{T\in\mathcal S}f_L(T).
\]

目录有限，查询单纯形及𝒦_{m−1}均紧凸；F对p线性，对L连续且凸（每一项是非负系数乘正分母的倒数）。凸minimax交换给

\[
t_m=\min_L\max_pF(p,L)=\max_p\min_LF(p,L).
\]

逐个p取合法L=H(p)，由上节同σ的全p付款得

\[
\forall p:\quad\min_LF(p,L)\le F(p,H(p))=P(p)\le W/m.
\]

对p取最大即t_m≤W/m。这完整支付了中间条件命题M-9f2…的显式前件。一般Jensen恒等式W−mP=Σe_i+Σκ_i+mJ中的κ_i仍有符号；本证明从未由e_i,J≥0推出一般付款。

## 静态覆盖系数与最终贡献

固定任意L∈𝒦_{m−1}，写L=(m−1)Σ_Tq_T1_T，q为目录分布；令M=max_Tf_L(T)。取同一实例任意最优m槽元组(T_1,…,T_m)，令d_x为其客户覆盖重数。逐客户有

\[
\mathbf1_{d_x>0}\le\frac{d_x+L_x}{1+L_x}.
\]

d_x=0时右侧非负；d_x≥1时d_x+L_x≥1+L_x。求和并展开L即

\[
\begin{aligned}
\operatorname{OPT}_m
&\le\sum_x\frac{d_x}{1+L_x}+\sum_x\frac{L_x}{1+L_x}\\
&=\sum_{i=1}^m f_L(T_i)+(m-1)\sum_Tq_Tf_L(T)\\
&\le mM+(m-1)M=(2m-1)M.
\end{aligned}
\]

对L取最小，结合已付t_m≤W/m，得

\[
\operatorname{OPT}_m\le(2m-1)t_m\le(2-1/m)W\le2W.
\]

这对每个m≥2、K≥2和每份预先固定不同花瓣映射的原完整σ成立，局部结论没有未付前提。两source在本ALL中各承担真实作用：pooled证明背景合法性及已canonical的minimax/静态覆盖归约；花瓣付款证明同一σ的∀p预算。M-9f2…保持中间条件命题，精确pin见新边intermediate_propositions。

Q-CAG-HALF仍要求任意有限共同目录及每份完整σ，本边只保contribution。635客户反例否一般全p付款，不能外推本族付款；也不能倒用t_m≤v_m而声称W≥mv_m。本族原精确OPT=2m+min(K,m−1)可给另一个更强直接界，但本边仅登记实际POOL归约推出的保证。

## 本轮读取与既有证据的界线

本轮直接实读共同模型、HALF主问题、pooled现行引理全文、原pooled_response_loads全文（尤其§3）、pool_structural_checks全文（尤其§2）、花瓣完整策略及阈值证明全文、旧八条边全文、旧收据全部21核心处置，以及独立3D报告中本范围的逐边/逐对象复核。对25对象的当前pin/正文SHA、8旧资产SHA作了精确比较，均与任务和独立3D报告一致。

其余七边、21核心中不受本次花瓣修正影响的比较和四共享比较，按同pin、同SHA及本轮独立3D既有全文数学复核保留；继承的“本轮重算”等措辞仍归原Boss1/b7bf-recovery-worker历史批，不移作本worker新执行。本轮没有重跑成熟科学证书、635审计、66430节点、65536型或原发现器。原包reading-ledger/finite-evidence-check保精确引用，完整独立3D报告另以相同字节保存供追溯。
