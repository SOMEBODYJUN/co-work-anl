---
id: customer-attraction/deleted-current-self-consistent-pool-and-full-endpoint-cap-root-interface
kind: resource
type_tag: 资源
title: 删当前自洽池与完整端点cap回收的根稿接口
status: four-root-sources-accounted-for; existence-and-cap-proofs-separated-from-unpaid-budget
summary: 完整保第四轮CLAIMS、根稿及两入口的量词、真实推导和停点；删当前SC存在与对角付款为真，混合付款未闭，完整端点cap回收不能制造低值尾；保根银行反例属于另一矩阵。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round4_general/CLAIMS.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round4_general/MAIN_PROOF_WORKING.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round4_general/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round4_general/menu/README.md
source_ids: [ff00d43c470d7554d671, b04bb098f396085c8a53, 51aff72e309e5fbbcf35, b10c650bbe467c2b00c5]
review_status: full-frozen-source-reading-and-five-current-object-comparisons; no-new-general-proof-claim
---

# 同一模型下两类不同端点

固定有限单位客户、有限非空共同标签目录，m名单位提供者观察全部有序历史、每份完整纯SPE及其实际叶B。保空标签、同覆盖标签、重复、零客户和全部平局。记u_i为实际利润、W=Σ_i u_i，C为实际覆盖；最优m槽覆盖O分成I=O∩C、R=O\C、G=C\O。half等价于|R|≤|I|+2|G|。旧更强的|R|≤W不能重新作为前提。

四源是同一轮的根状态与导航，不是四份独立证明。其主要资产已由正式[SC资源](自洽池与多槽交换的审查合同及旧池化反例--资源.md)、[16客户纯点反例](../反例/六标签纯自洽查询失败与唯一混合支撑--反例.md)、[共享cap引理](../引理/共享实际前缀的cap回收与最坏福利提升--引理.md)及[cap原证据合同](菜单分离独审与cap极端点的原证据范围--资源.md)承接。本页保根稿各接口的共同前提、独有导航与历史状态，不把入口表的“核验通过”授予新的独立运行。

# 删当前的共同平均负载与存在性

m≥2时，在原实际位置i强制同一个合法标签A，再严格沿同一σ完成Z_i(A)；只删当前i槽得V_i(A)，恰m−1槽。对查询分布p定义

\[
q_T(p)=\frac1{m(m-1)}\sum_i\mathbb E_{A\sim p}\#\{j\ne i:Z_i(A)_j=T\},
\quad \mu_x(p)=(m-1)\sum_{T\ni x}q_T(p),
\]
\[
g_T(p)=\sum_{x\in T}\frac1{1+\mu_x(p)},\qquad G(p)=\sum_Tp_Tg_T(p).
\]

q质量为1，μ为竞争负载均值，不能丢掉m−1因子。SC条件是supp(p)⊆argmax_T g_T(p)，不是p=q。g连续，softmax(g/ε)为单纯形自映射，有不动点p^ε；取ε↓0收敛子列。若极限某标签严格非最佳，其softmax概率以固定正差指数趋零，故极限p为SC。此一般存在性不需要SPE，也不含付款；m=1另按单人最优处理，不写m−1分母。

固定确定A时，逐客户倒数凸性及原实际整行IC给

\[
g_A(e_A)\le\frac1m\sum_i d_i(A)\le W/m.
\]

若e_A还为SC便可付款，但不是每个输入有纯SC。混合时，查询A与它诱发的负载相关，不能把不同对角的不等式直接平均成同一个q(p)的G(p)≤W/m。

若**同一个SC**满足mG≤W，对最优m元组的客户重数d_x，有1_{d_x>0}≤(d_x+μ_x)/(1+μ_x)。求和并用所有g_T≤G，得OPT≤mG+(m−1)G=(2m−1)G≤(2−1/m)W。五人的9/5只是依赖这个强付款前提的条件常数。原稿“本轮未推出五人”是该路线的历史，不覆盖现行另证的[五人half](../定理/五人半覆盖--定理.md)，也没有付当前六人的预算。

# 两个旧辅助反例与一个不同矩阵

| 对象 | 原稿精确身份与当前比较 |
|---|---|
| 16单位客户、三人六标签 | 全43有序决策历史、258含自身IC，actual034，u=(9/2,5,9/2)、W14、OPT16。六纯点的唯一最佳标签依次555222，故纯SC普遍存在为假；本例全部p却有G≤107/24<14/3。现行全文还解析给唯一混合支撑{2,5}及t=(27−√537)/6。纯点失败不是混合付款失败。 |
| 635单位客户、同三层规则 | u=(154,154,154)、W462、OPT558；p=(e₂+e₅)/2有3G−W=40617/340340>0，否全p删当前池化付款。该坏p非SC，固定背景(0,2)已给最大查询154。不能否“存在某个paid SC”。 |
| 后续保根银行矩阵 | [银行全文](../反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)用K_{T,A}=Σ_{x∈T}1/(b_x+1+c_x(Z(A)))，Z含根共r槽。它否低值对称Nash/完整根菜单混合；四人完整菜单值59/36>u=4/3。这不是此处删当前、跨全部实际位置平均的非线性g(p)，不能据其名称同为SC把本页paid-SC状态改为FALSE。 |

本批只读这些既成证据和证明，不重跑其原审计，不将两份旧内部检查泛称外审或盲审。CLAIMS中“construction独立展开”及capacity补审各有自己的来源时序，不能合并为本批新258项验证。

# 完整端点并集的cap回收与提升

另一接口固定实际h_k，强制A后取**任一完整尾SPE**的有序完整终局y∈R(h_k,A)，而非只用σ的孩子。D_{k,A}={y:v_k(y)≤u_k}，D为对全部k,A的并；A=S_k也含全部cap合格替代尾。

对有序节点h，令\ell_T(h)为强制T后的真完整尾SPE中当前者的最小终局收益，M(h)=max_T\ell_T(h)。有限性给极值。指定孩子y能被理性化当且仅当当前收益≥M(h)：保选中孩子，其余动作各贴达到\ell_T的真完整后继即可。**旁枝不附加祖先cap**。

若前k位有某j满足v_j(y)≤u_j，取最大这样的j。j=k直接入D；否则每个j<l≤k都有v_l(y)>u_l≥M(h_l)。由k向j+1退推，先理性化强制A，再理性化中间实际动作；不同有序分歧的旁枝独立粘接，终局仍是同一有序y。最终y∈D_{j,S_j}，可能改变落格，不保证仍入原D_{k,A}。

因此前k总利润不增足够，任意非零非负加权前缀总利润不增亦足够。若前k全部严格改善，同一拼合可继续到根，得到另一完整根SPE。对先最小化W、同W再最大化u₁的规范化原SPE，任何W(y)≤W的此类尾必入D：否则提升后W相等且u₁更大，矛盾。此规范化不是任意指定σ的性质。

若还能找到一个这样的真实y，既有完整m槽额外插入值G_p(y)≤W/m，又有某前缀角色不改善（或规范化下W(y)≤W），本引理才将低值候选回收成cap合法端点。**本引理没有生产满足两条件的y**。原menu入口的末两位上界min_D G_p≤min(u_{m−1},u_m)，在两者均大于W/m时仍不付款。

# 其余独有根账与来源导航

MAIN_PROOF_WORKING保NEW-CAP逐客户全图密度及单context whole-IC合法性，但不同action必须由同一次选择共同满足2u−d−H−J；同action可合并是旧组件，不能再次授予新预算。PB自由分数鞍点三步平台否任意合法背景的逐人δ链；该背景已覆盖所有客户且未证在轨，不反根聚合或half。

背景聚合候选M_r^new(b)≤W_new(actual)+U_suffix(actual)在空根对应half，其递推仍留机会损失δ−u，改叫reserve不使其非正。README另导航因果批量删位的同叶退款守恒、源行动复制比较及外支持探索；这四个根来源只给入口和所需共同预算边界，本批未把尚未完整读到的原稿当新primary done。CLAIMS原清单的六个状态分别保留存在、未付、纯点否定、cap回收、PB背景障碍及全p否定，不压成一个“方法失败”。

这些根源的准确用途是把已证域关系和表示送往仍缺的低值/共同付款接口。第三阶段可记录“SC存在+paid-SC前提⇒条件福利界”“不改善前缀+真实尾⇒ADM成员”“保根银行反例不能迁移删当前矩阵”等有条件关系；不导入旧图、不造已付边。本批两保存点的新有理核只属于[ADM有限菜单程序](../程序/ADM探针的完整终局菜单与两保存点精确证书--程序.md)。

六原件、五份逐字节比较快照及manifest见[证据说明](../../tools/evidence/adm-saved-points-20261102/README.md)。正文与依赖目前仅本地checkpoint；逐源处置JSON是待发布草稿，没有pushed或done确认。
