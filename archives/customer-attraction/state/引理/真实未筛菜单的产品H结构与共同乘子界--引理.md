---
id: "customer-attraction/unfiltered-true-grandchild-product-H-and-common-multiplier-bound"
kind: "lemma"
type_tag: "引理"
title: "真实未筛菜单的产品H结构与共同乘子界"
status: "proved-H-subadditivity-all-r-and-pointwise-additivity-r2-r3; no-half-payment"
summary: "完整Cartesian真grandchild菜单给H_P(τ)≤ΣH_t(τ)，r2/3逐τ等号；r2仅supH=M而非逐τ；r3真M整数池化与异质共同sup区别，r≥4不得由非负上界推符号。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/root/H_product_structure.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/aggregate/H_product_structure_review.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/aggregate/README.md"]
---

# 真正完整菜单及背景

有限个客户不交组件，单位客户和玩家、相同决策顺序、同r≥2名尚未行动者，完整Cartesian共同目录。各坐标固定合法有序前缀；允许任意非负整数背景作为辅助r人游戏，若应用回原游戏则必须角色对齐且前缀合法。空主题、同覆盖标签、重复、零客户、所有完整历史平局均保留，不把相同负载强制成同一续局。

3458B结构主稿与6640B审查全文整理。原审查**已收到完整statement和证明思路**，未读作者正文，是知情独立合同核查，非盲审或无提示发现。2476B入口另有一份joint-threshold盲核，它未读作者稿但已收到极点/舍入提示；二者先验不同，见[历史边界](../资源/前缀流真实分享与两类独审的历史边界--资源.md)。本页自足证明代数与可信拼合，未声称一般H(1)非负、Ψ/D付款或half。

当前角色i强制A，下一角色i+1再强制B。R(A,B)是**A,B之后**所有完整有序历史纯SPE的可实现完整终局，含过去和A,B。B并不先要求在其节点最优。r2时B后无决策，R就是该终端，包括非BR的B。有限逆向归纳保证菜单非空有限，保至少一个真正实现策略。置

\[
 d(z)=u_i(z),\quad v(z)=u_{i+1}(z),\quad
 \theta(A)=\max_B\min_{z\in R(A,B)}v(z),
\]
\[
 f(A,\tau)=\min_{B,z\in R(A,B)}[d(z)-\tau(v(z)-\theta(A))],
 \quad H(\tau)=\max_A f(A,\tau),\quad\tau\ge0.
\tag{H}
\]

θ是真实下一节点的max-min floor，非静态任意背景值；H全部组件与产品使用**同一个τ**，不允许每坐标独立优化后冒共同价格。

# 真M、H与Ψ的三层关系

一个菜单叶(B,z)能成为A后下一节点的完整SPE实际叶，当且仅当v(z)≥θ(A)。必要性：下一角色可选达到max_B min v的B，任何真实grandchild都付至少θ。充分性：在选定B孩子保z，对每个其它B′独立取使v达到最小的真实grandchild，偏离≤θ≤v；更深子树已SPE。选定B若有同标签其它实现者无须替换；不同完整有序孩子彼此独立。

所以

\[
 L(A)=\min_{B,z:v(z)\ge\theta(A)}d(z),\qquad M=\max_A L(A).
\tag{M}
\]

M亦等于完整节点SPE可实现的**最低当前利润**：任一完整SPE当前收益≥各A的L(A)，故≥M；各A贴最低孩子，再规定当前选最大者，达M。这不要求预先给定当前动作本身BR。

对任何可行v≥θ菜单叶，d−τ(v−θ)≤d。因此f(A,τ)≤L(A)、H(τ)≤M。H(0)≥0，故

\[
 0\le\Psi:=\sup_{\tau\ge0}H(\tau)\le M<\infty.
\tag{HM}
\]

没有由此得Ψ=M。H是有限条直线之min再max，不需凹；common sup不需达到。原单组件LP、纯SPE菜单和Ψ不能互换；[同一产品前缀凸化](同一产品前缀的可信凸化与有限舍入--引理.md)给真M上界，不称任意长suffix M可加。

# 全r的产品次可加

记坐标t的定义为R_t,θ_t,f_t,H_t，产品为P。固定联合A=(A_t)、B=(B_t)。逐坐标任选真实grandchild SPE，完整Cartesian策略积仍是全有序联合历史SPE：每次联合偏离的总收益差是合法各坐标偏离差之和。该积子集包含于全部R_P(A,B)，而R_P还允许真正跨坐标耦合。

因此先min的方向为

\[
 \min_{R_P(A,B)}v_P\le\sum_t\min_{R_t(A_t,B_t)}v_t.
\]

完整Cartesian B允许各坐标独立取max，故

\[
 \theta_P(A)\le\sum_t\theta_t(A_t).\tag{THETA}
\]

再固定A，将joint最小化限制到该product子集，并用τ≥0与**+τθ**符号：

\[
 \begin{aligned}
 f_P(A,\tau)
 &=\min_{B,z\in R_P}[d_P-\tau v_P]+\tau\theta_P(A)\\
 &\le\sum_t\min_{B_t,z_t\in R_t}[d_t-\tau v_t]
                   +\tau\sum_t\theta_t(A_t)
 =\sum_tf_t(A_t,\tau).
 \end{aligned}
\]

对完整Cartesian A取max，得

\[
 \boxed{H_P(\tau)\le\sum_tH_t(\tau)\quad(r\ge2,\ \tau\ge0).}\tag{SUB}
\]

不是假设每个joint SPE可分解，也非反向包含。若τ<0第二步方向不能照用；若行动域不完整Cartesian，max的逐坐标等式也不能照搬。

# 恰两人、三人的逐乘子等号

r2：强制A,B后已终端，joint叶恰为坐标终端组合，v、d可加；下一角色是末位，max利润亦可加，(THETA)及f两处均取等。

r3：A,B后仅一名末位。固定任一完整联合历史，其末位联合动作是BR iff每坐标动作均是该坐标BR。若某坐标不最优，只改该坐标就严格改善；全部坐标最优之积亦最大。全部平局BR集合精确Cartesian，因此R_P=×R_t，θ_P=Σθ_t，f_P=Σf_t，再max A可独立，故

\[
 \boxed{H_P(\tau)=\sum_tH_t(\tau)\quad(r=2\text{或}3).}\tag{ADD}
\]

固定背景不改变该集合等式。r≥4则B后至少两名决策者，真实耦合grandchild未必只在积子集，本页只保(SUB)。原主稿关于可能严格的机制不是这里已构造实例；审查明确没有严格例，不能宣称每个r≥4有负H或严格下降。

# r2未筛菜单的原单位例与sup平台

两个不交singleton主题X={x},Y={y}、零背景、两人。任意首强制A，末位复制A时d=v=1/2，选另主题时d=v=1。θ=1，所以

\[
 H(\tau)=\min\{(1+\tau)/2,1\},\qquad M=1.
\]

H(0)=1/2≠M；若提前删非BR B，就错误删掉第一条线。原例无需枚举程序。

一般r2，每个B的v≤θ(A)。各有限线d+τ(θ−v)非减；v=θ的线常数且至少一条，其余正斜率线足够大τ后不再取min。故f(A,τ)最终平台L(A)。有限A及有限组件可共用一个足够大τ，得到

\[
 \Psi_t=M_t,\quad M_P=\sum_tM_t,
 \quad\sup_\tau H_P(\tau)=\sum_t\sup_\tau H_t(\tau)
 \qquad(r=2).
\]

所以r2没有异质common sup严格收益，也没有真实M池化下降；不是逐τ H=M。r1本定义无next/θ，须单独按终端加法处理；可另约v=θ=0使式退化，不将它冒原r≥2定义。

# 共同sup、真实整数池化与统一舍入余量

对r≤3，同τ各分量H≥0则产品H≥0；若所有分量全τ非负，任何有限同型/异质产品也全τ非负。对r≥4，非负的**上界**ΣH不能推出H_P非负，同样不能仅靠上界断言负例。

r3令Ψ_t=sup H_t，(ADD)给

\[
 \Psi_P=\sup_{\tau\ge0}\sum_tH_t(\tau)
 \le\sum_t\Psi_t.
\]

异质最优乘子不一致可使抽象菜单严格；本组三稿不提供原CAG可实现严格例。主稿说其它同轮真实例已核是来源导航，审查精确范围不认证那些未读例。相同类型N≥1复制则Ψ_(t^N)=NΨ_t，无common price额外严格收益；该齐次性此处只由r2/3等号推出，不能延伸到r≥4。

真实整数M不同：r3后两角色能以总v≥Σθ补偿，某坐标v<θ的投影不是子SPE，却可被另一坐标盈余支持。[任意背景两尾FILTER](../定理/任意背景两尾产品门槛与可信叶过滤--定理.md)的五客户输入在强制B时有四行(d,v)=(3/2,3/2),(1,1),(3/2,2),(2,3/2)，θ3/2、L(B)3/2、barL(B)5/4；两副本强制BB最低L=5/2<3。这里是固定A的L非可加，不能自动说max_A的M下降。另[保险菜单对象](保险根菜单的有效幅度与调和后继保底--引理.md)已有真正M严格例，但不把该例的M数字或独立M_ind当H(1)数字。

为说明Ψ与M的可用关系，完整保留入口所引20452B三相关稿中joint-threshold合同的解析接口（context主读，不额外done/原run）：类型k有n_k≥0副本。对**每个联合当前A**按(k,A)分组，用其全部真(B,z)菜单，质量n_g，解有限LP

\[
 \min\sum_{g,o}X_{go}d_{go},\quad
 \sum_oX_{go}=n_g,\quad\sum_{g,o}X_{go}(v_{go}-\theta_g)\ge0,
 \quad X\ge0.
\]

每组取达到max_B min v的B即可整数可行；可行域紧。若G个正组，极点正变量至多G+1：更多则G个质量等式加一个总v等式有双向扰动；总约束不活跃时至多G。因此只有一组可能混两项。将较高v项质量向上取整，组总质量整数不变且非负，总v只升，至多改一副本。统一

\[
 D=\max_{k:n_k>0,A}\{\max_{B,z}d-\min_{B,z}d\}
\]

覆盖全部正类型/全部当前A，不可只取actual或最优A的范围；空产品D0。舍入成本增≤D。总v≥Σθ的选定联合B后贴积SPE，其它联合B′各坐标贴最小v的真grandchild。即使B′某坐标未改变，也能在**不同完整联合历史**重新选该坐标续局；偏离总值≤Σθ，选定孩子≥Σθ，所以真child SPE成立。

有限LP对偶给value=sup_(τ≥0)Σ_g n_g f_g(τ)，符号是−τ(v−θ)。对任意联合A再max，与sup同向可交换，不需凹或达到；完整Cartesian使max分解为Σn_kH_k。于是任意r≥2有

\[
 M_P\le\sup_{\tau\ge0}\sum_kn_kH_k(\tau)+D.\tag{ROUND}
\]

这是存在低利润完整节点SPE的上界，不约束每份给定策略当前收入；没有支付右端。它也不同于按每(t,i,A)分母分块的旧余数C_i：这里一条总v约束只留一混合组，D是利润范围，无需所有主题组整除。r2可直接无舍入D0；零客户/零副本均Ψ=M=D0，零组删除，平局保真实实现者。

在r3的同型N副本，由(HM)、(ADD)、(ROUND)得NΨ≤M_N≤NΨ+D，因此M_N/N→Ψ；这是本页基于已列合同的直接解析推论，并非原单组件M=Ψ。r2更精确M_N=NM。r≥4没有NΨ≤M_N的上述证据，不能抄该极限。

# 当前用途与未付处

m5初始r5、继r4可能利用额外joint grandchildren，末三人以内单靠产品化不能由全τ非负H种子造负H。m6同理将r6/5/4与末三人区分。这没有证明所有组件H非负，也没有构造真正深层负菜单，不能拿三人M节省冒H(1)节省，更没付half所需的B+C/Ψ/D。本组五主源均为MD，不含程序源码，当前原entry/独立数学entry/LP/扫描全部0；代数证明与历史有限核声明分开见[证据](../../tools/evidence/insurance-source-and-H-product-primary/README.md)。
