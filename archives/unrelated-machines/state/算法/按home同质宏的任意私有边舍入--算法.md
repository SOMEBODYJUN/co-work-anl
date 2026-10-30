---
id: "unrelated-machines/home-homogeneous-macro-arbitrary-private-edge-rounding"
kind: "algorithm"
type_tag: "算法"
title: "按home同质宏的任意私有边舍入"
status: "proved-structural-ST-application-no-end-to-end-software"
summary: "每home的宏时长与宏身份无关，使任意宏完美匹配保相同残余容量；任意私有资格与逐边小成本经LP/ST给1+δ及未知OPT承诺近似。"
legacy_ids:
  - "UM-HOMOGENEOUS-MACRO-PRIVATE-ST-v1"
  - "UM-HOMOGENEOUS-MACRO-PRIVATE-PROMISE-v1"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/questions/unrelated_machines/homogeneous_macro_private_edge_st_rounding_candidate.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/model_and_classical_barriers.md#3"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/heterogeneous_macro_uniform_residual_st_rounding.md"
---

# 按home同质宏的任意私有边舍入

机器为显式有限不交并H∪Z，至少一台；任务为宏B及其余私有任务J。宏只在home可用，|B|=|H|。宏资格图可任意交叠；对每个home h，所有有限宏边时间同为有理P_h，与宏身份无关。私有任务j的显式资格A_j⊆H∪Z任意，时间p_ij非负有理，可随任务和机器改变，不要求唯一home、组共同资格或等端时间。候选允许空A_j作为不可行接口输入而返回FAIL；未知OPT承诺版只对每任务至少一有限端、存在合法分配的输入谈有限OPT。

给有理T>0、0≤δ<1，假设全部P_h>T/2且全部有限私有边p_ij≤δT。有确定性总位多项式算法返回FAIL或实际完整调度；成功负载全机≤(1+δ)T，若原OPT≤T则必成功。FAIL不是T精确调度的充分必要判据；LP可接受没有T整数调度的实例。输入合同缺失与正确的域内FAIL应分开记录。

## 宏占位与残余容量

先检验宏资格图完美匹配。无则FAIL；若某P_h>T也FAIL。后者是原稿隐含于负容量LP的必要guard，应显式保留，即便没有私有任务或该home没有私有资格。取任意宏完美匹配M并固定它，每home恰放一宏，核心负载P_h。

令c_h=T−P_h，c_z=T。求显式有理LP

\[
\sum_{i\in A_j}x_{ij}=1\ (j\in J),\quad
\sum_jp_{ij}x_{ij}\le c_i\ (i\in H\cup Z),\quad x\ge0.
\]

私有资格空时该任务等式不可行。可按通常LST剪去p_ij>T端；固定T合同里δ<1已保证所有私有端≤T。LP不可行则FAIL，否则得到多项式位长有理解。

为何任意M都不丢完备性：真实T调度中的每个宏占用home，且每home至多一个宏，因P_h>T/2。宏数恰等于home数，故所有home恰占一宏。把其宏位置换成M，每home负载仍为P_h，原私有整数分配保持合法且满足同一c_i。因此真实T调度给LP可行点。该论证完全不需要私有任务有固定home身份。

## 槽舍入及全机保证

对每机i，将x_ij>0的任务按p_ij非增排序，在质量轴上连续放长x_ij的区间并切单位槽。每任务连到与自己区间有正交长的槽，交长是分数匹配；每任务质量恰1，每槽质量≤1。任意任务子集送出的总质量等于其大小，其邻槽至少这么多，故整数二分图匹配覆盖全部原私有任务；可确定性增广实现。

某机第r≥2槽匹配的任务处理时间不大于前一完整槽任何单位的处理时间，其成本可由该满槽分数费用支付；不同r收费到不同前槽。首槽另付正支撑最大件s_i=max{p_ij:x_ij>0}，空支撑取0。因此

\[
L_i^{private}\le\sum_jp_{ij}x_{ij}+s_i\le c_i+\delta T.
\]

加回home宏得P_h+c_h+δT=(1+δ)T；sink同样≤(1+δ)T。末槽不足1、未匹配槽、平局、零时间和空私有任务均保此论证。这是已有[支撑最大件定理](../定理/有序单位槽的支撑最大件舍入--定理.md)对非统一c_i的直接应用，未主张新ST原语。

有理LP求解、宏完美匹配及槽匹配均多项式；每x_ij≤1故每区间至多跨两槽，每机槽数≤|J|。任务、机器、全部资格和分子分母位数计入输入；不按T、P_h或分母数值循环。这里给出数学算法，未交付新的通用LP、未知阈值搜索或端到端ST软件，也没有把量子流的有限运行算作本LP实现。

## 不给OPT的承诺版本

保持静态分层、|B|=|H|及每home的P_h与宏身份无关。承诺在真实OPT>0处全部P_h>OPT/2、全部有限私有边p_ij≤δOPT，固定δ≤δ̄<1。不输入OPT；不要求给其证书，也不声称一般输入能识别这份承诺。

先逐任务检查零端。全部有则给零调度，精确处理OPT=0及空任务。否则令Q为全部原处理时间分母之积；log Q受输入分母位长总和控制。任选完整合法原分配，其全部任务时间和U≥OPT且QU为整数。在t=k/Q上测试：t≥max_hP_h；宏资格图有完美匹配；剪去私有p_ij>t后，上述home容量t−P_h、sink容量t的LP可行。

该谓词单调：核心固定、容量随t增大、资格只增加，旧分数点仍可用。**不检查P_h>t/2，也不要求p_ij≤δt。** 后两项不能用于整段二分；私有小尺度来自关于OPT的承诺。真实OPT可行且其全部端≤OPT，因此测试接受OPT，进而接受U。整数二分首个接受网格点t*≤OPT，用O(log(QU+1))次测试，并取最后的LP见证。

在t*舍入时支撑最大件仍≤δOPT，即使不满足≤δt*。加回核心后

\[
C_{max}\le t^*+\delta OPT\le(1+\delta)OPT\le(1+\bar\delta)OPT.
\]

最小接受网格点不必等于原OPT或精确LP最优值。固定δ̄才有统一ε=1−δ̄>0；δ随实例趋1不提供统一改善。若U都未接受，可报告承诺不适用，不能据此称一般合法输入没有调度。

## 同质性失效的确切机制与后续

若宏时间依赖身份，任意宏匹配不保持残余容量。具体T=1、H={0,1}、B={a,b}，宏矩阵为p_0a=p_1b=3/5、p_0b=p_1a=9/10。另两件私有任务只在home0可用，各耗时1/5，δ=1/5。对角宏匹配加两私有给峰1；反对角匹配使home0残余仅1/10，私有总量2/5的LP不可行。它反驳“任意身份相关宏匹配后用精确残余容量”这一步，不反驳别的联合算法。

后续原稿`heterogeneous_macro_uniform_residual_st_rounding.md`已完整比较：仍要求|B|=|H|、宏只home且全部>T/2，但允许宏时间依赖身份。任意合法宏匹配后将home私有容量统一放宽为T/2，原OPT私有分配仍给LP点，ST使home≤(3/2+δ)T、sink≤(1+δ)T，δ<1/2。未知OPT搜索保留全部私有边，误差按δOPT支付。它以较弱3/2+δ界去掉同质性，不否定本页更强1+δ界。后续稿另以3-PARTITION说明任意小但异质任务的精确容量不能免费流化；本页只导入其实际证明关系，外部复杂度前提不在这里另认证。

与[共同资格加权组算法](共同资格组的加权出口联合槽--算法.md)相比，本页允许任意跨home私有资格和逐边成本，但强制宏全占用且按home同质，两者不是同一输入域。与[共同量子精确应用](全占用同宏下任意资格量子的精确调度--算法.md)相比，本页放宽私有尺寸换取δ加性余量。宏数改变、宏可去sink或私有边不小都破坏当前完备性或误差链，未据此声称一般困难性。

T=0另走零端检查，不把严格正宏合同强行归一化；H空则B空，任意剩余私有任务只可在Z，LP/ST仍适用；零时间私有边保留。原稿为候选，现按所列全部条件知情重构其证明；没有独立冻结审查、外审或新颖性认证。一般矩阵如何提供该分层与宏占位结构仍开放，UM-TARGET-v1未由此解决。
