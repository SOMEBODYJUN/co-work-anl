# 净券与可变归属四主源：实读、比较及解析核验

## 范围与实际操作

Boss4本批四个正式主源ID为2fb6ffdfbbe602e419f4、63cabeef464802659aec、2ea839a33cc204211265、14f7ebe916c389d33536，总28190字节。2026-10-30，本代理从既存external缓存恢复副本，逐份全文读取四主源及六旁读，不将父批“已读”记录代替本次阅读。保存副本与冻结清单的SHA-256和字节数逐份匹配；没有重新调用clean show，没有Git、claim、done、checkpoint或认证。

本批四主源全为Markdown，没有程序来源。所做数学核验是下述解析推导和完整参数证明；新数学程序执行数为0。只另做文件指纹、JSON和相对链接完整性检查，不把这种机械检查称数学证明。曾尝试委派独立复核，但并发线程已满，未产生第二代理审查；本次为同一代理的原文重构与自查，不冒称独立盲审、外审或新颖性认证。

## 完整实读登记

| 来源 | 字节 | 本次实际阅读与独有内容去向 |
| --- | ---: | --- |
| safe_coupon_netting.md | 7448 | §1—6全文；whole-IC signed ledger，同context SAFE退N/e，NET-LOAD，最大标量CLIP、重算beta/gross而非net单调、局部最小传播，fresh分母，同角色pooling与full-O ROLE-CAP2 → 安全净券定理。 |
| global_role_coupon_hitting.md | 4675 | §1—5全文；同一full/fresh固定核PRICE、跨所有context逆序归纳、全源HIT与合法INIT、终点量而非访问数 → 角色命中定理。 |
| fresh_source_order_and_suffix_hits.md | 7542 | §1—5全文；任意有限源量与多query，reset标记，past合法域、零收益、fresh SOURCE-ORDER、后缀HIT/前缀割/一般与单调价格、full-O例外 → 同一角色命中定理后半。 |
| fractional_ownership_extension.md | 8525 | §1—5全文；可变full-O的p/H/r/入口，原同客户密度与I补余，TAME两段代数，R旧owner自由，全部m≥3完整SPE付款向量严格扩张，m5及ROLE未证 → 可变归属候选。 |

六旁读源均全文实读并存related：fresh_profit_normalization.md、role_price_envelope.md、review_role_price_envelope.md、review_coupon_pruning_blind.md、source_time_coupling_review.md、source_order_reconstruction.md，共26049字节。它们尚未由本代理提交逐源完成。其证据作用分别是fresh重归一化闭合域、uniform-subset凸包及层积分、按稿逐式复核、SAFE/CLIP的真实审查范围、源时间盲重构与随后对稿、收到命题后的源时间重构。

历史审查身份保持区别：review_coupon_pruning_blind.md自身说明先收到关键公式/提示，不能因文件名blind称严格盲审；source_time_coupling_review.md说明§1—5在未读作者正文时重构，§6随后对稿；source_order_reconstruction.md是收到精确命题后重构。这里记载原件事实，不声称本次重新实施这些审查。

## 全仓比较及范围

在当前结果仓库对全部Markdown检索SAFE、CLIP、净券、分数归属、可变归属、whole-IC、来源保持、共同钱包，以及四个源文件名；正文比较排除tools/evidence中的旧副本和cleanup/checklists生成清单，随后全文实读全部六个直接匹配的正式对象。检索仅发现相关线索，本身不算全文阅读。额外全文读模型、半因子勘误、唯一最优遗漏反例与六人分数覆盖条件定理；五人定理只核对精确命题、结论段和当前定位，不声称本批重读其全部53行/附录或重跑其程序。

| 当前正式对象 | 已核区别与兼容关系 |
| --- | --- |
| state/候选/固定比较元组的线性共同付款证书--候选.md（全文） | 固定canonical p，full-O坐标H/r及I-PAY、同客户optional-common R流。新可变p LP包含它，TAME给每个给定点的初始化充分域；最终仍是同一次ROLE。 |
| state/定理/同客户来源保持流的加强初始化与节点密度--定理.md（全文） | 广义source合同只需共同客户库存、每入口密度和严格future。可变p继续满足合同；节点f≤1不控制同角色多个context。该核保持客户且可增加common边，一般不是SAFE/CLIP删正边子核。 |
| state/候选/分数归属与实际净券的共同钱包--候选.md（全文） | 先固定SAFE/CLIP净列P，再联合Hall取消和实际I路由，残源需求总量为|R|−|G|、钱包总量W。与本full-O H/r +2u坐标LP不同，不能混领优化点或预算。SAFE/HIT提供其列合同，不能替它证明OWNER-NET。 |
| state/算法/固定来源路由的最大回撤与价格分离--算法.md（全文） | 输入是固定同客户流点，按来源缩放回留原角色；可使d′>u，超出原INIT。不是可变p或CLIP的同一自由，不证明任意ROLE总成功。 |
| state/计算/来源回撤原程序与有序策略的精确重放--计算.md（全文） | 已有六固定case的真实历史执行属于前批；本批未重跑、未将其计为四Markdown主源的程序证据，失败cut分支该历史执行未触发。 |
| state/引理/固定最优前缀链的归属端点抵消--引理.md（全文） | 全局固定归属的势端点与signed债等量抵消；分数归属允许需求重分配，不制造新资金，不允许不同p沿同链望远镜。 |
| state/障碍/遗漏份额支付的半因子勘误--障碍.md；state/反例/唯一最优组合的全遗漏支付--反例.md（均全文） | half需要净需求|R|−|G|而非半额或全遗漏。两人完整SPE的全遗漏桥反例并不反驳本批full-O +2u充分系统，也不反驳六人half。 |
| state/定理/五人半覆盖--定理.md（仅精确命题与当前定位）；state/定理/六人分数覆盖条件半覆盖--定理.md（全文） | 独立五人定理已成立，不受旧“本机制未证明五人”历史句覆盖。六人τ≤9/2有条件已证；本批无条件ROLE仍开放，不能把条件范围或付款向量例升格无条件六人half。 |

未找到同名正式SAFE、GLOBAL-HIT或变量p对象；现有钱包只旁引原稿。因此三篇正文是对象化主证明，而不是为已存在同一数学对象重复换名。所有比较均限本仓当前快照；没有把检索无命中称整个历史库不存在。

## 解析自查的具体承重项

1. LOSS逐客户：两叶负载a,b，消失coverer数r，D−N=(b−r)/(ab)>0，因为当前角色总是共同coverer。故N≤D≤u和F=N+e≤u；原beta整行IC系数未改，退款是其标量资金分解。
2. CLIP：v=u+P−F；删c≤min(P,F)后current=u−F+c、out=P−c。最大c给out=(v−u)+、current=min(v,u)。只对固定原注入与选定子边重新递推beta′；beta′≤beta，但current增加，故仅保旧gross逐券上界，不保旧net单调。
3. fresh核：nu−P=D_F−N=u−Y−N−e；仅nu>0节点定义beta=h/nu，正fresh边见证后继nu>0。无past出口，只收fresh来源，不能拼full-O来源或旧beta。
4. 行凸包：q_j≤sum_x1/(c_Ac_B)≤D−N，故非current概率≤current。阈值混合的总质量及各边际精确；逆序归纳对K内current仅用≤1，未假定一到K就吸收。past边仅终点，非终端future严格递增，故HIT覆盖全部contexts与跨客户重采。
5. 价格：置lambda_(l+1)=基线，对前s高价集用s/(s+1)，价格差层积分望远镜得基线/(l+1)+sum lambda_(s)/(s(s+1))。全图与fresh后缀各用自己的同一来源/核，常数价格只给M≤M。
6. SOURCE-ORDER：每源alpha的reset标记q满足k≤q<i且history在q前与actual相同。future更新q′=i；正past需x∈Z_j且x∉g_j，因此j≥q≥k。两人一客户唯一主题的full-O owner2一半付款给past1，明确阻止越域。
7. 变量p：H列界只用OWN及delta≥c_B；p=P_B+r，OWN按客户合计给I未来量能由同一点w−H补余付清。R图/分母不变，入口满足共同库存与逐边密度合同；源反链给首差异s处f≤p_sx+sum_(i<s)a_ix≤1。全文显式写R-FLOW与ROLE，避免“保留原约束”遗漏系统。
8. TAME：对pd≤1和pd≥1两段分别展开pkw−n min(pd,1)，用k≤d及pk≤1得≤d；逐客户正部求和后只调用一条完整主题IC。canonical总属TAME，R的k=1使所有合法分数归属自动满足；不声称所有仅OWN点均可先验初始化，也不声称TAME必要。
9. 严格扩张：任意m≥3的每一有序history，已有t个E时选B收益m/(m−t)≥1、选E收益1/(t+1)≤1，故完整SPE。固定最优T=(B,E,…,E)无future边，F=(1,1+p_2e,…,1+p_me)，确有至少两个不同付款向量。仅固定T付款向量集合扩大，旧canonical本来可行，不宣称新half实例或普遍ROLE。

## 尚未支付的命题与接续

SAFE/CLIP保证非负合法表示和局部受限最少传播；HIT/SOURCE-ORDER保证同一图的终点运输约束；变量p/TAME保证有限线性扩张、给定区域初始化及一个严格付款向量例。它们共同没有证明最终同角色多context和来自多query的共同容量。完整原树更多off-history IC是否足够排除正价格缺口，仍需新的普遍论证。

三篇正文的关系判断另见[关系说明](../../../../../cleanup/workspaces/Boss4/net-coupon-primary-next/relation-note.md)。当前阶段二不自动改写draft-scaffold三级超图，不为连通造边；阶段三可据这里的多前提、条件和出处逐边登记。
