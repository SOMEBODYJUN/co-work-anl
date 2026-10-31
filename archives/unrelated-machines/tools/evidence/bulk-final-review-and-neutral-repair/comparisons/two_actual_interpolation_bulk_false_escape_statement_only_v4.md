# 一般两actual见证插值与bulk全False逃逸：仅陈述 v4

ID: UM-TWO-ACTUAL-INTERPOLATION-BULK-FALSE-ESCAPE-v4。
作者typed_edge_gap，2026-10-18。仅scratch，完整Exact-only；无作者Proof/推导/测试。标准半整数排序槽/配对舍入的限域后果，不宣称新的舍入定理或全球新颖，不预登记重复资产。

版本关系：对应fee bulk committer族v3的范围扩展，合并一般插值机制与完整backbone特化。作者先仅读 `/workspace/scratch/038d9dcc4cac/unrelated_aux_heavy_readout_bulk_or_commit_split_statement_only_v3.md`，未读其Proof；独立特化Exact v1已冻结在 `/workspace/scratch/038d9dcc4cac/arbitrary_nonpool_committer_two_mode_false_escape_statement_only_v1.md`，SHA256 `4def1be309c85a6c2eec117ab892a70aef94cf6f6b9f83bff64e574368c1dc54`。之后root根据先行Statement独立闭合并建议一般域；本v4据此整理，不冒充blind单作者归属。所有旧字节保持。

## 0. 任意普通P的完整一般插值合同

给任意有限普通unrelated矩阵P，机器数m≥1、原jobs集Z可空；有限p_(i,z)为任意binary非负有理，其余∞。给T≥0 binary有理、两份同一P的完整actual assignments σ^0,σ^1，均覆盖全部Z恰一次、使用原finite资格、每台原machine load≤T。

另给任意distinguished原jobs子集F⊆Z，以及它们的一份指定actual legal目的地ν:F→[m]；ν可使用不同于两witness的原finite端，输出必须按ν执行这些F jobs。不假定ν自己的load≤T。对原machine i定义

- t_i=Σ_(z∈F:ν(z)=i) p_(i,z)；
- L_i^b=Σ_(z∈Z\F:σ^b(z)=i) p_(i,z)，b∈{0,1}；
- N_i=|{(b,z):b∈{0,1},z∈Z\F,σ^b(z)=i}|，按两份actual occurrence计数，即使同job两次同机也计两次；
- d_i=max{p_(i,z):z∈Z\F,σ^0(z)=i或σ^1(z)=i}，空max=0。

则存在det总位poly算法，输出P的一份全部原jobs完整actual τ，并同时满足：

(G1) 对每z∈F，τ(z)=ν(z)；对每z∈Z\F，τ(z)∈{σ^0(z),σ^1(z)}。全部原job各执行一次，不可拆分，无新machine/job/资格。

(G2) 对每machine i，非F实际job件数≤ceil(N_i/2)，且

  Σ_(z∈Z\F:τ(z)=i) p_(i,z) ≤ (L_i^0+L_i^1+d_i)/2。

故完整实际逐机load满足

  load_i(τ) ≤ t_i+(L_i^0+L_i^1+d_i)/2。

(G3) 所有界在同一份完整actual τ中同时成立。特别t_i=0时load_i≤3T/2；若t_i=T而一witness中该machine的F实际load为T，则load_i≤3T/2+d_i/2；若两witness的F实际load都为T，则L_i^0=L_i^1=d_i=0，load_i=t_i。

包括T=0、F或Z\F为空、actual零端、同job两witness同目的地、unused finite>T、ν不在旧supports的原finite端。所有输入条件应实际核验，不将未知σ存在性当免费调度算法。复杂度按显式P、两完整σ、F、ν、T与binary rationals合计位长收费，不按任何分母数值或1/tiny循环。

下面§1–5归一化T=1，精确给bulk backbone特化及必要pool逃逸；不把(G)当新source hardness或一般UM approximation算法。

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
