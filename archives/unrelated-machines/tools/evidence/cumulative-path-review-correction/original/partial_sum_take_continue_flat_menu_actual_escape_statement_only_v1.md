# Take/continue 编译候选：独立陈述先行审查用文件

ID: UM-PARTIAL-SUM-TAKE-CONTINUE-FLAT-MENU-ACTUAL-ESCAPE-v1。
本文件只给精确对象、结论与范围，不附达界分配或下界证明。原名含Exact的完整来源已经含构造与证明，不能把读过该源的审查称为盲重构。

源SC：agents a=1,2,3，items u1,u2，每名agent对每item value=3/5。物品不可拆、最多一owner、允许不给某agent。

目标资源共11枚：共享u1,u2，及每a各互异x_a,y_a,z_a。对每a有三个真实groups r_a,m_a,l_a，其全部indexed states/private权表如下：
r_a: take1={u1:3/5,x_a:2/5}。
m_a: off={x_a:1}；take2={u2:2/5,y_a:3/5}。
l_a: off={y_a:1}；accept={z_a:1}。
每state一不同private机M；每资源一不同resource机R。每group一件selector1，仅可去该组所有state private。每state的每个resource一件不同incidence，只可去自己的M以表中private权执行，或该resource R以1执行。其它端∞，无其它job/预载/逻辑约束，全部未选state jobs也存在且须执行。共26machines、30jobs（9selectors/21incidences）。

V为每group选一个indexed state及该state任意resource subset，跨group子集全局不交、最大化最小private权之和。

Exact Claim：上述源SC真实max-min OPT=0；目标V精确2/5，目标完整普通UM真实OPT精确8/5。要求给全部原jobs的实际达界σ和任意完整σ下界，不能省未选states。于是此明确take/continue局部规则不可能有从任意目标positive δ partial allocation提取原全部agents Ω(δ)正效用的统一正常数decoder，即使可任意重排原items而非只解码已领取items。

候选规则的语义是把一条unit partial-sum path上每个take credit c∈(0,1)用normalized additive state {原item:c,下节点own:1−c}表示，下一节点可own/off，末节点fresh accept。上表是两个items path credits3/5、2/5的精确普通矩阵。结论只否此给定规则，不否所有DAG/source compilers或既有selector-tree正规形。常数显式对象，不作一般算法/源hardness/全球新颖性声明。
