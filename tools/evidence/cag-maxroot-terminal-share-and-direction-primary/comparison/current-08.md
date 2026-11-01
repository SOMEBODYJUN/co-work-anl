---
id: "customer-attraction/fixed-entering-role-real-replay-and-once-only-potential-budget"
kind: "algorithm"
type_tag: "算法"
title: "固定进入槽的真实后继重放与一次有符号势预算"
status: "proved-flow-and-telescoping; quantitative-covariance-payment-open"
summary: "对同一完整纯SPE的真实源枝及所选raw终点分布给p_AQ_i(y)非负守恒路径；未来边有原有序历史IC，最后换进入标签的删除负载功为零；固定势只使用原源质量一次。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/tree/real_replay_covariance_flow.md#1-4"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/tree/uniform_swap_and_raw_flow_independent_review.md#3-4"
---

# 固定进入槽的真实后继重放与一次有符号势预算

## 模型、规范门槛与分析端点

采用[有限单位客户与完整历史纯SPE模型](../定义/共同目录完整历史模型--定义.md)：共同目录\(\mathcal S\)有限非空，m≥1名单位提供者依次观察全部有序历史，各选一次目录主题；终局客户价值在覆盖者间均分。保空主题、重复选择、零客户和全部离轨历史依赖平局。固定**同一份**完整纯SPE σ、实际路径s及收益u_i，W=Σ_i u_i。

对任意合法历史h，令\(\mathcal R(h,A)\)为当前人强制选A后，孩子子博弈可由某份完整纯SPE实现的有序终局全集。当前角色k=|h|+1的规范门槛为
\[
M(h)=\max_{A\in\mathcal S}\min_{z\in\mathcal R(h,A)}u_k(z).
\tag{M}
\]
有限树逆向归纳保证集合非空、最值达到。任意子SPE中的当前收益≥M(h)：每个真实备选孩子给它的收益至少该孩子全集中的最小值，再用当前IC取max。反向取达到max的行动A*，在该孩子选择达到其min的完整子SPE，其他行动孩子各选达到自身min的完整子SPE；不同有序孩子子树可独立拼接，于h选A*便得到当前收益恰为M(h)的完整纯SPE。因此M(h)也等于该历史全部完整纯SPE中当前角色k收益的最小值。此等价使用的正是原当前角色的收益坐标和全部孩子SPE集合；M不能替换成一份固定σ自行选择的续局收益。其全集与拼接逻辑已经由[终局全集算法](完整历史纯SPE终局全集--算法.md)保留。

固定实际行i及其原实际前缀h_i=s_{<i}。对每个合法A，令z_A=finish_σ(h_i,A)，即进入角色i被强制后沿原σ完成的**完整m人终局**。任意同前缀的合法raw终局z可有任何进入行动z_i和任何未来动作，不要求它是SPE。定义
\[
c_x(z)=\sum_{k=1}^m\mathbf1_{x\in z_k},\quad
\ell_i(z)=c(z)-\mathbf1_{z_i},\quad d_i(z)=u_i(z).
\]
删除的始终是同一个角色i；不根据查询主题在后面另找一人删除。角色i已被强制，后文只用k>i的子SPE门槛，不给该强制进入者另施M(h_i)下界。取所选目标概率律Q_i，支持在这些raw终局中。Q_i只是分析背景分布，不声称为可执行纯/混合SPE。域必须放行所有进入标签，包括原实际行动；否则以下混合端点和势不等式可能落在域外。

固定目录分布p和一个全程不变的实向量t∈\(\mathbb R^N\)。置
\[
a_A(x)=\mathbf1_{x\in A},\quad\rho_x=E_p a_A(x),
\quad w_A(x)=a_A(x)t_x^2,\quad w(x)=\rho_xt_x^2,
\]
\[
\mathrm{Cov}_i=E_{A\sim p}[(w_A-w)\cdot\ell_i(z_A)].
\]
p、Q_i可为有限单纯形上的任意实概率，零概率边保为零；此处不要求t来自某个最优背景或鞍点，流恒等式只需它固定。A是分析中保留的源标签，没有给原玩家新信号或隐藏随机承诺。

## 真实重放的非负系数与所选终点

独立抽A∼p、y∼Q_i。起点z^i=z_A。对j=i+1,…,m依次定义
\[
g_j=(h_i,A,y_{i+1},\ldots,y_{j-1}),
\quad z^{j-1}=finish_\sigma(g_j),\quad
z^j=finish_\sigma(g_j,y_j).
\tag{REPLAY}
\]
前一步的终点恰是下一步的规定叶；故每条未来边是原σ在**精确有序历史**g_j上当前角色j强制改为y_j的真实偏离，后面继续同一σ。完整SPE给整名玩家的IC
\[
\Gamma_j(A,y)=u_j(z^{j-1})-u_j(z^j)\ge0.
\tag{IC}
\]
没有对客户份额逐项加权后声称仍是IC。较早已强制的目标动作可以偏离σ，其形成的前缀仍是合法有序历史，σ的完整性正是在这里承重。

给每个带(A,y)标签的j边质量
\[
f_i(A,y,j)=p_AQ_i(y)\ge0.
\]
同一路径所有层保该质量；逐层聚合时每个内部状态入流等于出流、每层总质量一。加入阶段j便是有限有向无环流，即使两个完整profile相同或保留自环也不成循环。每个原源标签A的初始总质量准确为Σ_y p_AQ_i(y)=p_A。

所有未来动作替换后，z^m=(h_i,A,y_{>i})。最后将进入行动A静态改为y_i并**冻结已经置入的目标尾**，终点就是y。此最后边没有角色i的真实IC，但
\[
\ell_i(h_i,A,y_{>i})=\ell_i(y)
\]
逐点成立，删除负载的任何线性功均为零。最后带源标签的分布为p_AQ_i(y)，所以终点边际确为原先选定的Q_i，且终点独立于被动源标签A。i=m时没有未来边，Cov_i=0，只剩此零删除功的标签边。

## 协方差总功与固定势的同流望远镜

终端混合叶的删除负载只依赖y，独立于A，故其中心化源权期望为零。逐路径相减得到
\[
\boxed{\mathrm{Cov}_i=-\sum_{A,y}\sum_{j>i}
p_AQ_i(y)(w_A-w)\cdot[\ell_i(z^j)-\ell_i(z^{j-1})].}
\tag{FLOW}
\]
这是明确非负保守流对目标协方差的精确展开，不是仅声称存在某种流；它尚未估计右侧金额。构造以已经给定的Q_i为输入，没有给出所选Q_i的搜索器、概率位编码或一般位多项式时间保证。

任意**同一行全程固定**的终局函数Φ_i，在包括最后静态标签边的同一路径上有
\[
\sum_{\mathrm{flow}}f\,\Delta\Phi_i
=E_{Q_i}\Phi_i-E_{A\sim p}\Phi_i(z_A).
\tag{TELE}
\]
全部中间值按入流/出流相消；即便某中间profile等于另一个原源profile，也不凭此产生第二份原源质量。不能将ΔΦ逐边改为正部再引用(TELE)。这一源容量结论只针对这些固定有符号势，不自动限制各条\(\Gamma_j\)正部的重复总额。

较早mean-floor域可取固定非负乘子λ_ih及
\[
\Delta_{ih}(z)=\mathbf1_{z\text{延伸}h}[M(h)-u_{|h|+1}(z)],
\quad F_i(z)=\sum_{h\text{为严格未来历史}}\lambda_{ih}\Delta_{ih}(z).
\]
原源未来沿σ，故F_i(z_A)≤0。若目标域**确实另要求**E_Q d_i≤u_i以及每个E_QΔ_ih≤0，则E_QF_i≤0；(TELE)给\(\sum f\Delta F_i\le-E_pF_i(z_A)\)，不要求各中间raw叶F_i≤0。

## 最新单一净cap与同一份源银行

定义固定净成本
\[
B_i(z)=d_i(z)+\sum_{k>i}[M(z_{<k})-u_k(z)]
=d_i(z)-S_i(z).
\]
原源z_A对所有严格未来角色都沿σ，故S_i(z_A)≥0，且d_i(z_A)≤u_i。最新分析域只约束
\[
\sum_iE_{Q_i}B_i\le W,
\tag{NET-CAP}
\]
每行Q_i各归一。它不蕴含每行E_Qd_i≤u_i或E_QF_i≤0；不能继续拆用较早的两个端点银行。

令
\[
I_{\rm total}=W-\sum_iE_pd_i(z_A)\ge0,\qquad
S_{\rm total}=\sum_iE_pS_i(z_A)\ge0.
\]
在**同一组**已选Q_i上相加(TELE)便给
\[
\boxed{\sum_{\text{全部行流}}f\,\Delta B_i
\le I_{\rm total}+S_{\rm total}.}
\tag{NET-TELE}
\]
最后标签边的ΔB_i一般非零，虽其删除shadow功为零，仍必须保留来使终点准确到Q_i。

为明确银行身份，考虑固定w下在(NET-CAP)域最大化Σ_iE_Q(w⋅ell_i)的有限LP。原源分布可行，域有限凸紧。其对偶可取同一个μ≥0和各行归一乘子η_i，使
\[
r_i(z)=\eta_i+\mu B_i(z)-w\cdot\ell_i(z)\ge0
\quad\text{对所有允许raw叶}.
\]
单一μ来自**显式的一条总cap**，不是将原先历史相关λ或不同行μ_i无代价归一化。原源对偶差有精确分解
\[
G=\sum_i\eta_i+\mu W-\sum_iE_p(w\cdot\ell_i(z_A))
=\mu I_{\rm total}+\mu S_{\rm total}+R,
\quad R=\sum_iE_pr_i(z_A)\ge0.
\]
这三项只是同一份G的分拆。若所选Q_i为该LP的原/对偶最优解，互补性使目标端松弛相消；否则同一有符号common-shadow工作只得到相应上界。二者均不额外支付(FLOW)的自适应权\(w_A-w\)。

## 真实流与raw坐标流的关系及审查身份

raw坐标流保留源未来动作，逐格改为y的未来动作，然后同样最后改进入标签。它与(REPLAY)对每个(A,y)有相同起点、混合终点和最终y。对固定A的线性shadow及固定Φ_i，总有符号功只取决于端点，故两种流的总功逐路径相同。raw中间叶通常不是新前缀后的σ规定叶，不能给每个坐标边\(\Gamma_j\ge0\)，也不能逐边互借银行。

若把整个进入分支先改为finish_σ(h_i,y_i)再重放，后续状态不再依赖原A，平均自适应未来功为零，原债务集中在这条无相应未来IC的分支替换上。单纯先静态换进入标签而冻结原源尾则仍依赖A，也失去(REPLAY)的“每步前是σ规定叶”性质；这两种操作不可混称同一种enter-first流。

本次两主源共13533字节均全文实读，另实读八份相关定义/修订稿，原件与双冻结指纹在[证据](../../tools/evidence/real-replay-covariance-history/README.md)。原`uniform_swap_and_raw_flow_independent_review.md`是2026-10-25的内部检查，开头列明已读uniform-copy与raw-tail稿，正文再比较真流；其文字没有声明本批盲审。本次是在读过原稿后实质重构，不新增独立审稿人、外审或有限运行纪录。源中未给本流执行程序，本轮也未重跑别的旧审计。

定量缺口见[真实重放的协方差付款问题](../问题/真实重放协方差的定量付款--问题.md)，条件交换工具见[行动平衡交换半库存引理](../引理/同前缀行动平衡交换的半份约化成本界--引理.md)。本对象只完成显式流、真实IC和一次固定势望远镜，m=5同式成立也未推出无条件half；恰六人每份完整SPE目标不由本构造解决。关系已解释，超图留第三阶段。
