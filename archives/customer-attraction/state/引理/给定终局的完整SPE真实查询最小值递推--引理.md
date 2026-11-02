---
id: "customer-attraction/conditional-terminal-full-spe-real-query-minima-recurrence"
kind: "lemma"
type_tag: "引理"
title: "给定终局的完整SPE真实查询最小值递推"
status: "complete finite-instance recurrence and attainability proof; no all-input query-payment lower bound"
source_ids: ["48e207d8758ea09895d1", "4b2099a3e3a474019580", "9dd751cd47469f03aa53"]
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d5b468f0c01140e79be5afef669bc0e5/solo_query_payment/working.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d5b468f0c01140e79be5afef669bc0e5/solo_query_payment/working.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d5b468f0c01140e79be5afef669bc0e5/solo_query_payment/query_envelope.py", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d5b468f0c01140e79be5afef669bc0e5/solo_query_payment/query_envelope.py", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d5b468f0c01140e79be5afef669bc0e5/README.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d5b468f0c01140e79be5afef669bc0e5/README.md"]
review_scope: "whole primary sources read, all mathematical quantifiers reconstructed; current execution scope explicitly stated"
---

# 对象与量词

有限单位客户、有限非空共同**标签**目录\(\mathcal A\)，m≥1名单位提供者按全部有序历史行动，客户终值在覆盖者之间均分。允许空主题、同覆盖异标签、重复、零客户以及任意历史依赖弱平局。固定一个有限实例和非负有理查询权\(w_a\)；权可以全零，不必和为1，也不必为比较元组重数。

本页给出此固定输入上**全部完整纯SPE**的两个精确极值：条件于规定终局，实际路径的真实查询总额最小值，以及其中某一实际行的最小值。它们可由不同策略达到。不是把策略限制成计数政策，也不据算法存在证明一般半覆盖付款。

# 复用的终局全集与真实最低孩子

令k为已选动作的计数，\(E(k)\)是从该精确有序前缀可由某份完整子SPE实现的终局计数集合。值集只依赖k；同计数的不同有序历史仍可各选不同子策略。对\(|k|<m\)及合法a定义
\[
 g_a(k)=\min_{z\in E(k+e_a)}U_a(z),\qquad M(k)=\max_a g_a(k).
\]
U_a(z)是一个选择a的玩家在终局z中的最终收益；在此a已出现，零覆盖客户不产生零分母。

既有[可信续局菜单与完整策略重构](../算法/可信续局菜单与完整策略重构--算法.md)证明：给定z和当前规定动作a，可以实现为完整子SPE当且仅当
\[
 z\in E(k+e_a),\qquad U_a(z)\ge M(k).\tag{A}
\]
必要性由每个偏离孩子的收益不低于其最小值；充分性给规定孩子一份实现z的子SPE，其余孩子分别取达到g_b(k)的子SPE。它们是互不相交的有序子树，可同时拼合。终局E(k)={k}，非终局全集按(A)并集，极值有限达到；零客户也有非空可达集。

本页不把这个旧集合值恢复接口认作新结果。尤其“每个终局可由最低威胁恢复”不等于最低威胁树枚举了每一份完整策略。

# 一行真实查询的精确最小额

条件于终局z、当前规定动作a满足(A)。对每个合法查询b，强制当前选择b后必须沿同一完整策略的真实后继完成；其当前收益记V_b。若b=a，这个查询孩子就是规定孩子，故\(V_a=U_a(z)\)，不能再把它另换成g_a(k)。若b≠a，则V_b≥g_b(k)，各自最小值可以独立达到。因此当前查询行的精确最小额为
\[
 \boxed{q_w(k,a,z)=\sum_bw_bg_b(k)+w_a[U_a(z)-g_a(k)].}\tag{Q}
\]
权非负是下界方向的承重条件。括号非负，因为z属于该孩子全集。缺掉第二项会得到较弱下界，不能将该较弱值的负付款余量冒充某份可实现SPE的违例。

# 条件总额K与单行H

令K_w(k,z)为实现z的全部完整子SPE中，剩余实际路径各行查询额之和的最小值。终局K=0；非终局
\[
 \boxed{K_w(k,z)=\min_{a\text{ 满足(A)}}
 [q_w(k,a,z)+K_w(k+e_a,z)].}\tag{K}
\]

**下界。** 任一实现z的子SPE，其当前动作满足(A)，当前行≥q，实际孩子剩余总额≥对应K，故总额至少右端。

**达到。** 取达到右端的a，在规定孩子取达到其K的完整子SPE；所有其他孩子分别取达到g_b(k)的完整子SPE。(A)保证当前规定动作仍最优，且每个孩子都可信。当前行恰q，实际孩子恰K。末端倒归纳证明整个公式和达到性。

若H_w(k,z)表示剩余实际位置中**最小一行**的极小值，末端记“没有决策行”（代码为None），则
\[
 H_w(k,z)=\min_{a\text{ 满足(A)}}
 \min\{q_w(k,a,z),H_w(k+e_a,z)\}.\tag{H}
\]
末端的第二项忽略。其证明同样用下界和互斥子树拼合；若最小来自孩子，选择达到孩子H的策略，若来自当前行，任一兼容可信规定孩子即可。K与H的最优策略可以不同，不能将两个分别最小值作为同一完整策略的联合得分。

# 恢复达到K的完整有序策略

原实现记录每个(k,z)的K最小动作。沿唯一规定实际路径使用这个动作，规定孩子保持目标z。每个非规定孩子b则选择使当前角色收益最小的终局
\[
 z_b\in\arg\min_{y\in E(k+e_b)}U_b(y),
\]
并独立递归恢复一份实现z_b的完整子SPE。在这些已经离开全局实际路径的子树，无须继续最小化全局查询目标，可任选满足(A)的规定动作。

写出动作的键始终为原有序历史，包含全部长度0至m−1节点。count缓存只共享值集和数值，不强迫不同顺序共用选择器。输出动作数为\(\sum_{t=0}^{m-1}|\mathcal A|^t\)，故没有位多项式规模承诺。代码只提供K的显式策略恢复，不应虚称另有保存的H最优策略。

# 对旧ROW、SUM两类候选的有限输入等价

取任意最优m元组，w为其标签重数，O=OPT_m，W(z)为实际福利。原查询付款候选是：

|候选|同一完整策略的原式|此有限输入的精确判别|
|---|---|---|
|ROW|每位置i有Σ_jV_ij≥O−W|对每个可实现z，H_w(0,z)+W(z)≥O|
|SUM-HALF|Σ_ijV_ij≥m(O−W)|对每个z，K_w(0,z)+mW(z)≥mO|
|SUM-SHARP|Σ_ijV_ij≥mO−(m−1)W|对每个z，K_w(0,z)+(m−1)W(z)≥mO|

每条真实IC给V_ij≤u_i，因而Σ_ijV_ij≤mW；SUM-HALF若普遍成立才推出half。ROW比它强，SUM-SHARP又是另一个更强付款要求。K递推没有提供控制不同孩子g的普遍下界，三者不能凭精确表示即标为已证。[倒二真实查询行](../定理/倒二真实查询行及三人返还边界--定理.md)已支付末两位的相应行；三人余局的有符号删除返还仍不能免费去掉。

# 根非理性计划的附带精确极值

只要求所有正深度子树为完整SPE，允许根规定a不最优。固定其规定终局\(z\in E(e_a)\)，其余孩子取最低威胁后，最小可能根后悔为
\[
 \Delta_{\min}(a,z)=[M(0)-U_a(z)]_+.
\]
若使M最大的孩子恰为a，则U_a(z)≥g_a=M，公式自动给0；因此把a也纳入M不会高估最小后悔。

对该固定实例，所有这类完整计划的最大坏差额精确为
\[
 \boxed{\max_{a,z\in E(e_a)}
 [\mathrm{OPT}_m-2W(z)-3(M(0)-U_a(z))_+].}\tag{R}
\]
[m≥2的三倍根修复](../定理/多主题独立保险的三倍根修复与半覆盖等价--定理.md)可以把严格正种子编译成同人数单位客户half反例，需完整恢复和核验后使用；m=1时这里只计算一个有限表达式，不调用该编译。非正值只排此固定输入，既不证明一般付款，也不是另一个根修复常数。

# 当前资格与边界

原稿标为单人推导、尚未另一研究者数学审查。本清洗已从定义完整重构(Q)–(R)及达到性，复用成熟全集恢复与根编译，给可复用的完整有限输入论证；不是新的外部盲审、新颖性或福利发现。原八个小输入全策略枚举及三份旧实例报告见[程序合同](../程序/真实查询下包络的全策略小例核对与三份保存诊断--程序.md)，本轮相关数学程序0执行。

同覆盖标签在当前模型本来合法；原稿将此说成“规范程序较宽边界、以后必须去重”的句子属于额外distinct-set变体，不限制本页或用户本轮模型。五人half已有后续证明，六人主目标仍独立开放，主目标已证也不能反推每一条曾经足够的查询加强。
