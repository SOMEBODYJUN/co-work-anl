# 归一化菜单最小状态数的精确组合表示：作者 Proof v2

对应 UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION-v2。冻结Exact SHA256 6208afa100822520502e368c1cf3814d6d5bd520e3fdaec363efc33961eb2d3d。此Proof另冻，仅在Exact-first审查冻结后转交；无实现/有限测试声明。

## 1. 每条clause的support下界

令h为一条clause的正support大小。归一化与非负给h≥1。若d=0，已足够给h≥k=1。

若d≥1，则h≤d会使B等于该support时clause值1>η，违反low条件，所以h>d。把h个正权降序为w1≥⋯≥wh>0，总和1。前d项的平均至少全部h项平均1/h，故前d项和≥d/h。low条件对这d个资源成立，所以d/h≤η，h≥d/η，整数h≥ceil(d/η)=k。

此处不假设单项≤1/t，也不假设uniform；零系数不在support内，重复clauses不影响。

## 2. Unit覆盖与uniform k-subset正规化

任意t-subset T满足f(T)=1。有限最大值必由某条clause取得，而非负总量恰1意味着该clause在T上达1当且仅当它的完整正support包含于T。

对每条原clause，从其正support中任选k项F_s（步骤1保证足够），把该clause换为在F_s上均匀的1/k，余项0。原来被此clause覆盖的每个T都含其全support，从而也含F_s，仍在新clause上得1。于是全部t-subsets仍unit；新所有clause总量1，故新f(T)不超过1。

对任意|B|≤d，新clause在B上的值≤d/k。d0时此值为0；d>0时k≥d/η给d/k≤η。所以所有新clauses及它们的最大值满足low条件。变换不增indexed clause数，去重还可减少。每个F_s是同一U的k子集，没有辅助资源、玩家或隐藏约束。

因此任何原合法K菜单产生一个大小≤K的family F，每个t集含某个k集。反过来，任意这样的family以均匀k-clause实现，unit和low同上成立。两向给

K_min=Θ(2t,t,k)。

这是精确最小规模的数学等价，不是poly求这个覆盖family的算法。它的方向是每个大的t集含一个指定小k集。

## 3. 一般覆盖计数及两个锐端点

每个固定k集恰被C(2t−k,t−k)个t集包含；所有C(2t,t)个t集都需覆盖。故K乘前者至少后者，得到Exact第2项；重叠覆盖与重复indexed clauses只会浪费，不能降低下界。

若d0，k1。至多t个选中singletons会留下至少t个未选资源，组成无覆盖的T；而任选t+1个singletons，未选仅t−1项，每个T必含一个。因此Θ(2t,t,1)=t+1，uniform singleton菜单达到。

若ηt为正整数，d=ηt且k=t。一个t集仅能包含它自身这个大小为t的指定集，故family必须是全部C(2t,t)个t集；它们的均匀clause满足low，因为d/t=η。因此K_min=C(2t,t)，锐且达到。固定约分η=A/B，取任意t=Bz,z≥1便满足该端点。

## 4. 固定η的普遍增长与bit复杂度

d≥1时k=ceil(d/η)。写θ=ηt−d∈[0,1)，则

t−k=floor(θ/η)，

所以0≤t−k≤ceil(1/η)−1=c。令l=t−k，由k≥1还有l≤t−1。因此

C(2t−k,t−k)=C(t+l,l)≤(2t)^l≤(2t)^c。

二项展开所有2t+1项之和4^t，central项最大，故C(2t,t)≥4^t/(2t+1)。代入一般覆盖计数即Exact第5项。

源是一名additive玩家的2t个不同资源、各值1/t，只需O(t log(t+1))位列举；unit/tiny条件确为它各集合原阈值。固定η意味着c固定，以上K下界超过该显式源长度的任意固定次幂；即使每state仅用一个记录，输出也已超多项式。没有把此增长写成2^{Ω(源总位长)}，没有声称η变化时c仍常数。

选择k-subset和均匀化本身对已给的完整菜单是多项式变换；然而其输入可能已指数大，它不提供一个从原additive行多项式输出全部这些clauses的算法。即使指数多clauses共享相同数值1/k，indexed supports仍须显式列出；用隐式family换表示将改变合同。

## 5. 可满足性及限制

例如列出全部t-subsets、各自均匀权1/t，总能满足域。于是最小规模不是对空约束集的陈述；Exact只在两个端点及通过Θ定义给精确答案，不称一般binomial比值始终达到，也不声称能poly计算Θ。

所有结论只限同一U上的逐玩家非负norm1 explicitXOS、对全部unit/tiny子集同时保真。全局辅助归约、其它表示、unit损失、只对可达分配保真等不被排除。没有近2源NO、一般Santa Claus无常数困难性或UM-TARGET反面结论。
