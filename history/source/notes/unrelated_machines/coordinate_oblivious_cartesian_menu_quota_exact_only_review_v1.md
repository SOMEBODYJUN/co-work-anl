# 逐坐标 oblivious Cartesian 菜单 quota：Exact-only 独立重构

审查者：general_query_response_review。2026-10-18。

本轮唯一数学输入为root消息内精确陈述UM-COORDINATE-OBLIVIOUS-CARTESIAN-MENU-QUOTA-v1。冻结前未读取root作者Proof、其它agent输出或其它相关论证文件；未作软件枚举，未改repo/Work/Git。

**独立判断：数学Claim有效，无fatal。对任意固定函数族(f_i)，受限最优恰floor((3/2)^t)/2^t；不受限同family的V恰1−2^(−t)。显式位多项式算法以完整展开instance的规模为计量；不能误读成对仅t及2t个函数位的succinct输入、仍显式输出全部bundles的poly(t)算法。**

## 1. 冻结对象与量词

t≥1为整数，D=2^t。Groups为g∈F_2^t，resources为(a,b)∈F_2^t×F_2^t。State ell∈F_2^t包含且仅包含满足所有坐标b_i+g_i a_i=ell_i的resources，每一项权1/D。因此每个state恰D项、总质量1。

逐坐标受限状态族是固定一组任意函数f_i:F_2→F_2，并令每个group g选择ell_i(g)=f_i(g_i)。固定state后，每group可以领取该state的任意资源子集；所有groups的所领子集全局不交，资源不可分。质量是子集基数/D。最优目标是最大化各group质量的最小值。

以下证明先对每一个固定(f_i)分别成立，因此允许先任意挑选(f_i)的受限最优也同值。结论并非ordinary UM的实际OPT，不声称有物理一致性gadget强迫f_i。

## 2. 全部函数族的全局资源同构

记u_i=f_i(0)、v_i=f_i(1)。对每个resource作同一坐标平移

a'_i=a_i+u_i+v_i，b'_i=b_i+u_i。

此为整个resource universe的双射，不依group。若g_i=0，则原选择条件b_i=u_i恰变成b'_i=0；若g_i=1，则原条件b_i+a_i=v_i恰变成b'_i+a'_i=0。因此所有受限state选择同时变为ell(g)=0。

该双射保每个group身份、全部incidences、每项1/D及子集disjoint性。故任意固定(f_i)的可行quota谱完全相同；之后只需证明canonical f_i≡0。

单坐标canonical两条支持是：

- g_i=0：{C,E_0}，其中C=(0,0)、E_0=(1,0)；
- g_i=1：{C,E_1}，其中E_1=(1,1)。

第四个坐标资源(0,1)不被任何group使用。故全部选定states的资源union恰为{C,E_0,E_1}^t，大小3^t。所有未用resources仍可存在，但不会提供quota。

## 3. 必要上界、floor与partial语义

任何可行allocation的每个group子集基数都是整数。令s为最小基数，则D个groups各至少领s个，且全局不交；全部可用资源恰3^t个，故Ds≤3^t。因此

s≤q:=floor(3^t/2^t)=floor((3/2)^t)，

从而最小质量≤q/D。该界适用于任意partial子集，未要求state全量导出，也未把资源作分数切割。floor来自不可分资源与共同整数quota，不能只报连续上界(3/4)^t。

## 4. 对全部group子集的Hall充分性

建二部图：左侧全部groups，右侧全部used resources，邻接正是固定state incidence。

对used resource r，令k(r)为其坐标中C的个数。它与恰2^k(r)个groups相邻：每个C坐标允许group bit任意，E_j坐标强制对应group bit为j。在每条邻边(g,r)上定义非负有理量

x_(g,r)=2^(−k(r))。

于是对每个resource r，其所有邻边量之和恰1。

对固定group g，它在每个坐标可选择C（对边量贡献因子1/2）或E_(g_i)（因子1）。所以其全部邻边量之和恰

sum_(r∈N(g)) x_(g,r)=(1+1/2)^t=(3/2)^t=:rho。

现在对任意group子集A，同时求和：

rho |A|=sum_(g∈A) sum_(r∈N(g)) x_(g,r)
       ≤sum_(r∈N(A)) 1
       =|N(A)|。

因此每一个A都满足|N(A)|≥rho|A|≥q|A|，不是仅核总union，也不是只核子立方体形A。空A亦平凡成立。

该q-Hall条件充分且必要：给每个group建q个同邻接副本，普通Hall条件成立，因为任意副本子集涉及的原groups为A，其副本数至多q|A|≤|N(A)|。所以存在匹配使每个原group得到q个互异resources，且跨groups不交。等价地可用整数容量flow：source到group容量q，group到其邻resource容量1，resource到sink容量1；上述Hall条件保证满流qD，整数最大流给实际子集而非分数allocation。

所得每group质量恰q/D，结合上一节上界：

V_obl(t)=floor((3/2)^t)/2^t。

Hall证据也说明连续fractional graph有共同quota rho；但本结论的整数matching才保证不可分partial资源下的floor值。

## 5. t1与显式算法/位数

t=1时D=2、rho=3/2、q=1。两个支持各2资源、恰共享C，各另有自己的E_0/E_1；每group取自己的E_bit即质量1/2。若两者都取2项会冲突，所以V_obl(1)=1/2。任意(f_1)由上述平移等价；不存在奇偶或floor边界例外。

一般t，显式生成全部D groups及3^t used resources，列每group的D条邻边，边总数D^2=4^t；也可保全部4^t资源并让unused端孤立。q用整数3^t除2^t向下取整即可，数值位长O(t)，无浮点取整。

上述整数网络可用固定输入顺序选增广路的确定性最大流算法。每次增广至少1，总流qD≤3^t≤4^t，所以即使用朴素扫描增广也对展开图大小位多项式；所有容量及标签位长O(t)，算法不需构造高精度实数rho或枚举allocations。匹配完以逆平移返回原(f_i)资源labels，得到全部真实quota bundles。输出至多qD个labels，每label2t位，亦在展开规模内多项式。

“显式bit-poly”必须以展开的explicit-menu/graph instance为输入长度计，或允许总时间对这一展开规模多项式。若只有t（即使unary编码）和函数表2t位作为succinct输入，却要求显式列出D个groups的全部非空bundles，输出本身已有指数长度；当前证明与Claim不能被扩张为poly(t)总时间。这里没有这样的succinct算法声明。

## 6. 不受限同family的值：单独证明

现在去掉ell_i(g)=f_i(g_i)限制，允许每个group独立选择任意ell(g)。

上界：任取某g与其bitwise complement h=g+1。对于任意选择ell(g)、ell(h)，其两个完整state总有唯一交资源，因为每坐标的两式相减给

a_i=ell_i(g)+ell_i(h)，
b_i=ell_i(g)+g_i a_i。

所以全部groups不可能都领取自己的完整D项。最小基数仍为整数，因此其值至多(D−1)/D。此仅需一个complement pair的不可避免交点，不假定其它state之间交点数量。

下界：循环标号坐标，令ell_i(g)=g_(i+1)，下标t+1=1。给group g领取它state中所有a≠1^t的resources，b由

b_i=g_(i+1)+a_i g_i

唯一确定。每group恰得到D−1项。

这些bundles全局不交。若同一(a,b)同时属于g及h，写d=g+h，则对每坐标d_(i+1)=a_i d_i。因a≠1^t，存在a_j=0，故d_(j+1)=0；沿循环逐步推出所有d_i=0，即g=h。故每个所领resource至多归一group，完成合法partial allocation。

这给V≥(D−1)/D；与上界合并，

V=1−2^(−t)。

t1时循环选择ell_1(g)=g_1，保留a=0给两group各一资源，同样成立。该下界使用跨坐标选择（t≥2时），不混同coordinate-oblivious限制；t1两类恰同值也无矛盾。

## 7. 冻结结论与范围

精确数学式、每一个固定函数族同值、所有Hall子集、floor/不可分partial、t1及不受限对照值均已独立闭合。全过程只针对明确受限state-choice allocation语义；没有证明、假定或模拟ordinary UM物理一致性。总位多项式只按明确展开instance计，不按succinct参数t计。

**Exact-only独立通过，无数学fatal；未读作者Proof或其它agent输出。**
