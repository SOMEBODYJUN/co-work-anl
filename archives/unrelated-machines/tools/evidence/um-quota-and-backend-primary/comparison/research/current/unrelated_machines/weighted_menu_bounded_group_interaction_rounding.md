# 加权菜单的有限组交互：两次匹配给出实际次二界

读取目的：为近二困难性构造定位仍需保留的全局耦合。本结果不限制显式菜单的state数；额外使用的是**全部菜单并集上的组交互度**与资源跨组度。它在该结构类上输出完整实际调度，不从配置LP间隙推导困难性，也不解决一般UM-TARGET-v1。

## 1. 精确合同

**ID / Version：`UM-BOUNDED-GROUP-INTERACTION-WEIGHTED-MENU-v2`。** v1的较弱常数来源另冻保留；本v2使用完整块的精确尾项损失，参数及结论见下，不改旧ID的量词。

**Objects / Domain / Definitions。** 非空有限组集G；每组g有非空、显式列出的indexed states A_g。每个state s对应独立private机器M_gs及显式资源**集合**S_gs，同一state内资源标识互异；不同states可重复，同一resource可在一组的很多states出现。资源机器R_u与所有private机器互异。每个incidence给二进制非负有理数p_gsu，且W_gs=Σ_{u∈S_gs}p_gsu≤1。允许S_gs为空、p为零和未使用的资源机器。

完整原ordinary UM实例P恰含：每group一件selector J_g，只能到本组各M_gs，耗时均1；每(g,s,u)一件独立incidence job I_gsu，只能到M_gs耗时p_gsu或R_u耗时1；其余所有时间为∞。无其它jobs、预载、拒绝、共享private机器或side constraints。所有indexed states及全部原jobs均保留。结构标签是输入的一部分，不免费将一般P分解到此域。

记U_g=⋃_s S_gs。给定或计算有效整数上界Δ≥1、M≥0，使

\[
 \max_u |\{g:u\in U_g\}|\le\Delta,\qquad
 \max_g |\{h\ne g:U_g\cap U_h\ne\varnothing\}|\le M. \tag{1}
\]

空最大值取零，仍取Δ≥1。度数在**全部states并集**上计算，包含列出的零private权incidences，不以某个未知选态的交互图代替。有效上界可显式检查，可二进制输入而任意大。

**Quantifiers / Assumptions / Exact Statement / Conclusion。** 对每个满足上述域的显式输入及有效参数，令

\[
 \beta=\frac1{M+2\Delta-1},\qquad R=2-\beta. \tag{2}
\]

存在确定性总位多项式算法，不输入OPT、YES witness、最优选态、配置分布或未知可行分配，输出全部原jobs的具体合法σ，满足

\[
 C_{\max}(\sigma)\le R\,\mathrm{OPT}(P). \tag{3}
\]

菜单大小无界；固定M、Δ时才得到本结构类与规模无关的ε。G非空及selector1保证1≤OPT≤2，本域不含n=0/OPT=0实例。空G接口可另输出空调度并保留一台idle机器，不在本ID的非空组量词内。算法有两个准确分支：成功给绝对负载≤R；失败给实际OPT≥1+β并返回负载≤2。式(3)不声称每个输入都存在负载≤R。

**Dependencies / Scope。** 只用显式二分图匹配、下面自证的完整块分配不等式及保OPT归一化；不导入Santa Claus近似后端。它比原配置阈值T多用真实输入的交互度结构，不是相对CONFIG T的统一舍入合同。

## 2. 对所有states归一化，精确保留真实OPT

对每个W_gs<1的state加入一枚bonus job：在M_gs耗时1−W_gs，在只属该indexed state的新独占resource耗时1。每state至多加一job/机器。增广后所有state的private总量为1，旧jobs和时间逐一不动；新resource跨组度1，无新组间交互，原M和Δ仍有效。

删全部bonus及新机器把任意增广调度投影为P调度，不增负载。反过来，任意P调度峰C≥1都可保持所有原job，并将**每个state**的bonus分别导出独占新机，各新机负载1≤C，包括未选state的bonus。因此增广N(P)满足OPT(N(P))=OPT(P)。先在N(P)上运行下述算法，再投影即可。该论证同时处理原空state、W=0及零时间原jobs；没有按数值复制。

以下先设所有W_gs=1；资源/state均指当前归一化实例的真实对象，包含bonus，不能把“原资源”误读为仅限增广前P的资源。

## 3. 重资源匹配的失败给出真实下界

称一个state为分散态，若其所有private时间≤β。对存在分散态的每组，按输入顺序固定一个，形成组集L。其余组集H的**每一个**state都含某个p>β。

建二分图H与原资源：当且仅当某个原state满足p_gsu>β时连(g,u)，每边保存一个实际见证state。若此图无覆盖H的匹配，则

\[
 \mathrm{OPT}\ge1+\beta. \tag{4}
\]

证明：假设存在实际峰C<1+β的调度。每个H组的selector落到某个真实state；该state至少一枚p>β的job必须导出，否则private负载≥1+p>1+β。因为C<1+β≤2，每resource至多容纳一枚unit job。每H组选一枚这样的实际导出job，便给覆盖H的匹配，矛盾。

失败时将每selector置任意本组state、每incidence留在自己的private根，峰≤2。由0<β≤1及

\[
 (2-\beta)(1+\beta)-2=\beta(1-\beta)\ge0,
\]

该分支的真实近似比≤2/(1+β)≤R。它的下界来自实际所有调度，未假设有原最优见证。

## 4. 成功时先付出重资源的真实干扰

若匹配覆盖H，为每H组选其匹配边保存的state，只导出这枚p>β的job，保留所有其它jobs，预留这些互异resource。

对每g∈L使用已固定的分散态，删去所有预留resource。任何删掉其正权项的H组都与g在完整并集交互图上相邻；每H组只取一resource，故最多删M项，每项≤β。剩余总private质量W'_g满足

\[
 W'_g\ge1-M\beta. \tag{5}
\]

零权项可同时删去但不改变该式。这里没有假设任意重匹配会保住某个原分数解；损失已经由输入交互度M逐项付清。

## 5. 一个共同完整块匹配保证所有轻组的导出质量

对每g∈L，把未预留的所选state资源按权重排序为β≥w_1≥⋯≥w_n≥0，m=⌊n/Δ⌋。前mΔ项分成连续的**完整Δ元块**，每块建一slot，邻接其中Δ个互异原resource；末尾不足Δ项不建slot。将所有L组的slots放进同一个二分图，右侧每resource只有一个节点。

每slot度恰Δ。一个resource在每组所选state内最多出现一次、只属该组一个块，又跨全部菜单至多Δ个groups，所以右侧度至多Δ。对任意slot子集A数边，Δ|A|≤Δ|N(A)|。Hall给同时覆盖**全部完整slots**的匹配，可确定性多项式求出；匹配不碰已预留重resource。

每组从第t块得到的资源权重至少w_{tΔ}。尾项的准确损失为

\[
 \Delta\sum_{t=1}^{m}w_{t\Delta}
 \ge W'_g-(\Delta-1)\beta. \tag{6}
\]

自足证明：前至多Δ−1项各≤β。其余位置从Δ到n，可分配给区间[tΔ,min(n,(t+1)Δ−1)]，t=1,…,m；每区间至多Δ项，均≤w_{tΔ}，这些区间恰覆盖余下所有项。n<Δ时余和为空、总质量≤(Δ−1)β，同式仍成立。这里用于**计账**的区间与实际完整匹配块不同，不要求最后计账区间完整。

因此每L组的匹配资源B_g满足

\[
 \sum_{u\in B_g}p_{g,s(g),u}
 \ge\frac{W'_g-(\Delta-1)\beta}{\Delta}
 \ge\frac{1-(M+\Delta-1)\beta}{\Delta}=\beta. \tag{7}
\]

最后等号使用式(2)。该正下界也排除实际L组n<Δ的情形。所有B_g互不相交；每H组则导出质量>β。

## 6. 还原全部原任务、端点和总位复杂度

将每selector置所选private state；只导出H的匹配job及L的完整块匹配jobs，**所有state**的其它incidence jobs均停在自己的private机器。每resource至多一unit；每未选state负载1；每已选state负载≤1+1−β=R。全部jobs各一次且端合法，成功分支实际峰≤R，而OPT≥1给比≤R。结合失败分支及§2投影，证明式(3)。

β=1恰对应Δ=1、M=0。所有归一化states都是分散态，H为空，slots是单resource，不同groups资源不交；所选state全部导出，峰与OPT均为1。零private jobs始终是真实原jobs，可留private0，不被当成resource0；同state资源标识互异为Hall计数的必要输入条件。

设原state数a、resource数u、group数g、incidence数l，输入机器a+u、jobs g+l；归一化至多再加a机器/a jobs，显式dense矩阵至多(a+u+a)(g+l+a)项，仍多项式。交互和跨组度从显式并集计算；重图每边存实际state，轻图每选中incidence最多贡献一边。Δ只用于对实际长度n做整数比较/整除和分块；不创建数值Δ份对象，Δ>n时直接无块。M只进阈值与度检查，不展开数值M。精确有理排序、加和、bonus和输出负载的编码位长均多项式；分母M+2Δ−1的位长O(log(M+Δ+1))。输出为所有原jobs的机器标识，亦总位多项式。

若同state允许两枚不同jobs指向同resource，Δ=1、M=0也可能有selector1与两枚private1/2/resource1的单state例，真实OPT=3/2。此例不在本域，只说明不能删掉“distinct resource set”后仍沿用本证明和OPT=1端点；不冒称排除了该扩大域的一切比1算法。

## 7. 坐标切片的交互预算与反面源的剩余义务

在带变量tag的[d]^Q grouped coordinate slices中，若每组**完整变量并集**最多q个，每变量跨组≤d且incidence index单射，则M≤q(d−1)。一个resource (x,z)可被一组用到，必须使该组的index等于z的某个坐标，故跨组度Δ≤min(d,Q)。因此任意显式菜单大小、任意各state cell权重总量≤1，都可代入本定理：固定q,d,Q给本结构类的统一次二算法。不能只按每个state的变量个数估M，若全部菜单的变量并集可增长，该估计未获支持。

严格unit承诺YES OPT≤1 / NO OPT>R，可用实际输出峰与R比较区分；中间情况不保证。故若要在同一源域得到任意接近2的实际困难性，不能同时保持M和Δ为全局常数（除非所用复杂度假设失败）。这只是必要结构边界；允许M增长并不自动提供NO解码。固定cube维数也未必控制M，见[三坐标精确表示](degree_three_weighted_menu_cube_embedding.md)。

**Evidence / Counterevidence / Objections / Status / Related Files。** 本文算法证明完整；Exact-first独立重构与实际作者Proof读后通过，最终本文实际读后另列[审查](../../reviews/unrelated_machines/weighted_menu_bounded_group_interaction_rounding_review.md)。v1/v2来源不原位覆盖，out-of-domain重复资源反例保留。无standing fatal，外审、新颖性、因子锐性未认证；无软件实现声明，独立18,018份排序数值核验只作辅助而非一般证明。与已存[degree2/固定K算法](degree_two_group_bounded_menu_joint_rounding.md)使用不同输入额外结构；既非一般UM算法，也非UM-TARGET-v1反面证明。
