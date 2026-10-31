# 任意非pool共享任务的两模式全False逃逸：仅陈述 v1

ID: UM-ARBITRARY-NONPOOL-COMMITTER-TWO-MODE-FALSE-ESCAPE-v1。
作者typed_edge_gap，2026-10-18。仅scratch。仅读fee v3 Exact（下列路径），未读其Proof。此页只冻结完整Statement/范围，不含作者Proof。它是标准排序槽舍入的限域推论候选，不宣称新舍入定理/全球新颖，不预登记成熟资产。

依赖对象定义来源：`/workspace/scratch/038d9dcc4cac/unrelated_aux_heavy_readout_bulk_or_commit_split_statement_only_v3.md`。保留其全部backbone、实际selector含义、显式输入与两actual一真witness；本页改变J资格域与输出合同，不能冒称fee v3已覆盖。

## 1. 全部原矩阵

给整数r≥2、偶数k≥2、binary rational 1/2<ρ<1。每变量a∈[r]有环i∈[2k]，正block i≤k（s_i=0）、负block i>k（s_i=1），后继i+按本变量模2k。

每a,i有不同原machines M_(a,i),C_(a,i)，每a另有A_(a,0),A_(a,1)。每a,i有q_(a,i),b_(a,i)，每a有f_a。只下表端有限，其余∞：

| 原job | 全部有限原端/真实时间 |
| --- | --- |
| q_(a,i) | M_(a,i):ρ；M_(a,i+):1；A_(a,s_i):1/k |
| b_(a,i)，i≤k | M_(a,i):ρ；C_(a,i):1 |
| b_(a,i)，i>k | M_(a,i+):ρ；C_(a,i):1 |
| f_a | A_(a,0):1；A_(a,1):1 |

另有任意有限原machines I（与backbone不交）、任意有限原jobs J（与backbone jobs不交）。J包含全部commit/guard/aux任务，每job至少一有限端。所有J有限时间为binary非负有理，可为zero，可有unused finite>1。J不受同机统一时间、row-span、tiny/medium、同机件数或branch归属限制。

机器共m=r(4k+2)+|I|，jobs共n=r(4k+1)+|J|。若J有E_J个finite entries，总finite为r(10k+2)+E_J；dense原P为mn项。全部原jobs只执行一次，不可拆分；zero仍为真实执行端。

实际label由f_a目的地定义：A_(a,1)表示True，A_(a,0)表示False。不给免费源标签关系。

## 2. 完整输入witness域

给不同u,v∈[r]和同一P的两份完整实际strict assignments σ^u,σ^v，均覆盖全部n原jobs、使用原资格、每台原machine实际load≤1。

σ^u仅x_u=True；σ^v仅x_v=True。其余q/b/J目的地、返回、exports、负C/ring/I归属、cohabitation均任意。零端、unused finite>1、空I/J、部分q exports均属于域。没有σ^u/v之外免费assignment。

## 3. 非pool域完整逃逸合同

假定J全部有限原端位于I或任意M/C，**不接任何A pool**。正/负C端及ring M端任意非负unrelated时间，允许同C strict共居多枚tiny J。

则可确定性总位多项式输出同一P的一份完整实际τ，使：

1. 所有f_a都在原正pool A_(a,0)，故实际label全False。
2. 每个非f原job z的实际目的地属于{σ^u(z),σ^v(z)}，全部原jobs各恰一次、资格合法。
3. 每个非pool原machine（全部I、M、正/负C）实际load≤3/2。
4. 正pool A_(u,0),A_(v,0)在固定f外各至多k/2枚q；其它正pool没有q。故每个正pool实际load≤3/2。
5. 负pool A_(u,1),A_(v,1)各至多k/2枚q，其它负pool至多k枚q，故负pool实际load≤1。
6. 完整实际Cmax(τ)≤3/2。

不主张M/C恰一原job、不主张负C恰b、不主张fee v3的K_a或逐branch J件数。这些加强对全False低峰反证不是必要条件，本页不免费沿用。

只有两份actual strict modes的存在而未给witness时，只承诺对应全False actual存在，不承诺求未知strict witness。

## 4. 任意pool资格的定量版本

进一步放开J可接任意A pool，其余全部输入/两actual witness保持。在给定两witness中，定义

d = max { p_(A_(a,0),z) : a∈{u,v}, z不是任何f,
          σ^u(z)=A_(a,0) 或 σ^v(z)=A_(a,0) }，

空集合max定义0；包括原q与J，zero也保留。由于输入strict，有0≤d≤1；unused原finite边不进入d。令P_used只指实际这两witness已用边，无新增资格。

则可确定性总位多项式输出完整allFalse实际τ，每个非f job仍只用其两witness原目的地，并满足：

- 全部非pool原machine实际load≤3/2；
- u,v正pool各load≤3/2+d/2；其余正pool load=1（可以共居实际zero J）；
- u,v负pool各load≤1，其余负pool load≤3/2；
- 完整Cmax(τ)≤3/2+d/2。

不保留第3节pool q计数界，因为J现在也可执行于pool。

对β=2−δ>3/2（即0<δ<1/2），d≤1−2δ给allFalse实际≤β；d<1−2δ给allFalse实际<β。应区别threshold等号，不把≤β冒充<β。

特别，若某候选声称“全部C<β实际调度都排除allFalse”，则必须d≥1−2δ；若声称排除全部C≤β，则必须d>1−2δ。在k满足1/k<1−2δ时，这个大d必来自一枚实际J job的原pool端，不能仅由q的1/k端提供。该J必须在相应一真witness真正执行于该正pool，并在另一witness离开（该处已有unit f，正d不容strict共居）。这是实际原任务/原目的地量词，不是仅有一条unused nearunit资格。

## 5. 位复杂度与范围

全部算法对显式原P、两份完整assignments和有理数编码的合计位长polynomial；不按1/tiny、denominator数值或1/(1−ρ)循环。没有实际slot/gate新machine或可拆分执行；输出逐原job给唯一原machine。

本页不认证普通UM的新近似算法，不声称新的source NO/NP-hardness/near2困难性；只有给定两actual模式的全False构造。第3节真正覆盖tiny正C、全部负C和ring接入，允许任意共享aux与实际medium共居；第4节保留pool近unit原任务这个逃逸义务。它仍不能提供可物理实现的高复用OR-commit机制。
