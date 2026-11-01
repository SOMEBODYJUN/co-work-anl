---
id: customer-attraction/whole-profit-copy2-failure-and-prefix-request-cap2-quantifiers
kind: resource
type_tag: 资源
title: 复制全利润两倍失败与前缀请求cap2的精确量词
status: two-whole-profit-helpers-refuted; exact-PCAP-elimination-retained; nonterminal-common-payment-unproved
summary: 35客户完整SPE明确否定跨孩子COPY2及实际先后全利润两倍；独审先验与33→35加强保真。原PCAP按实际交集支持/逐源孩子利润预算，精确消元为Σu_j max(q+/childprofit)，全利润失败因q+=0不反cap2，固定单孩子列界不支付多枝。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round3_general/exchange/copy2_counterexample.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round3_general/exchange/copy2_independent_review.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round3_general/exchange/prefix_request_cap_checkpoint.md
---

# 两个已否辅助桥，原模型不变

有限单位客户、有限非空共同目录，单位提供者观察完整有序历史，每人选一次合法主题，终局客户在coverer间均分；完整纯SPE允许空/重复及任意离轨平局。对actual j<l，两个原加强分别是：

1. 在原l节点强制复制actual旧主题B_j、以后仍沿原σ真后继，复制者收益≥原actual u_j(B)/2（COPY2）；
2. 每份完整SPE的actual利润均有u_j(B)≤2u_l(B)。

4838B作者稿及4093B独审给同一35客户点反驳两式。它们没有否定下文带客户交集支持的PCAP，也不是half反例。其实际原报告8454B此前已全读，含31个有序节点、155个真偏离分数和逐名单位客户；本次按同SHA复用，不再show/读/执行该raw。

# 自足35客户构造，完整子SPE与根补全

六块两两不交：C6、P12、X8、Y₁2、Y₂2、Z5。目录
\[
 A=C\cup P,\ E=X,\ D=Y_1\cup Y_2\cup Z,
 \quad F_1=C\cup X\cup Y_1,\ F_2=C\cup X\cup Y_2,
\]
大小18、8、9、16、16，全部不同。根取A；固定A后的第二位取E，末位按第二位A/E/D/F₁/F₂分别选F₁/D/F₁/F₂/F₁。完整A孩子末位五候选表为

| prefix | A | E | D | F₁ | F₂ |
|---|---:|---:|---:|---:|---:|
| AA | 6 | 8 | 9 | 12 | 12 |
| AE | 9 | 4 | 9 | 9 | 9 |
| AD | 9 | 8 | 9/2 | 12 | 12 |
| AF₁ | 8 | 4 | 8 | 7 | 8 |
| AF₂ | 8 | 4 | 8 | 8 | 7 |

每个规定末位都最佳；在这些各自真实回复下，第二位五种选择最终收益全部8：复制A得C的2加P的6；E独享8；D得Y₁的1、Y₂的2、Z的5；F₁在F₂回复后得C2、X4、Y₁2，F₂对称。因此E是合法平局最佳回应，A孩子在全部六决策节点是完整子SPE。

其余四个首行动孩子各任选一份完整子SPE，有限逆向归纳保证存在且域互不相交。根A后的E/D不碰A，根得18；根其它合法主题的大小都≤16，所以任意真实回复下偏离收益≤16<18。故根A严格最优，任意上述孩子补全均给完整三人SPE。这是全历史补全论证，不靠冻结尾部或计数统一平局。

作者/独审另外选择最小标签BR将全部31节点显式补齐，根偏离向量(18,8,8,12,12)，第二位动作(E,A,A,A,A)。其完整表和原155项分数已在raw保，不把“其它孩子任取”与那一份具体完成字面混同。

Actual叶AED支付(18,8,9)。第二位在原A节点复制A后原真叶AAF₁，支付(8,8,12)，所以复制者8<原根18/2=9，且actual18>2·8=16。原叶三题不交覆盖所有35客户，W=OPT₃=35，不能升级成原half反例。

复制后前两位同题确实在**同叶**等收益，但不保护原叶根利润：C原来独享6，复制后被三位分享；P只被两个A分享。这明确说明跨孩子预算不是同叶相等的后果。共同复制所有块任意整数倍只等比放大相同旧例，不另认新机制或最优常数。

# 独审真正先验与33→35版本

4093B独审开头明确：只收到原始块、五主题和A孩子指定末位回复，审查前未看作者发现稿、主审计或代码；自行展开35不同客户、构造其余孩子，原称全31×5比较和125终局覆盖检查。它是知原构造输入/待核主张的独立内部实现，不是未知结论盲发现、外部同行审查或全球新颖性认证。本次只全文读该原审查，未取读/重跑其audit_copy2_review.py。

版本链也保留：最初P10是33客户，actual(16,8,9)、复制利润7，只否COPY2，因为7<16/2=8，而actual16=2·8没有否第二条全利润比。作者再要求P12加强，35客户actual18>16才同时否第二条。不能把33/35写成同份输入、把P12的第二项失败倒填首次审查，或删掉旧P10的独有历史。

作者稿还称root独立手算关键孩子、另一子agent不见发现源码/正文重构155项；这些原身份不冒作本批新执行。两MD与原raw同一35参数，但“存在任意合法孩子补全”的解析证明和最小标签具体表不同层次，均保清楚。

# PCAP原逐源预算与实际交集支持

固定完整σ的actual叶B=(B₁,…,B_m)、actual利润u_j(B)。每个分支α从actual有序前缀在切点i_α强制合法T_α后沿同一σ完成，得W^α。切点允许i_α=l，也可同切点多个孩子；只有j<i_α的固定旧角色作为源，目标l满足i_α≤l。

记c_B/c_α为完整m槽负载，定义
\[
 q^+_{\alpha j,l}
 =\sum_{x\in B_j\cap(B_l\setminus W_l^\alpha)}
                 \frac1{c_B(x)c_\alpha(x)}.
\]
j固定旧角色使x在两叶都覆盖，分母正；这里保actual B_j与actual目标B_l的交集，不能换成源完整利润。非负请求只要求**每个源j单独**满足
\[
 \sum_{\alpha:j<i_\alpha}\lambda_{\alpha j}u_j(W^\alpha)
                         \le u_j(B).\tag{SRC}
\]
原PCAP?请求每个目标l都有Σ_(α,j<iα≤l) λ_(αj)q^+_(αj,l)≤2u_l(B)。源码检查点明确没有证明此一般式，也未证明它足够half；末位cap2与逼近2反族仅转述peer材料，本分支未重证/独审，真正原停点是l<m多尾。

# 请求变量的准确消元，不是付款证明

对j<l设
\[
 \rho_{jl}=\max_{\alpha:j<i_\alpha\le l}
                   \frac{q^+_{\alpha j,l}}{u_j(W^\alpha)}.
\]
空集合最大0。若分母0，固定旧B_j必无正价值客户，q+=0，比值定义0合法。则SRC下目标左边最大值精确为
\[
 \boxed{L_l=\sum_{j<l}u_j(B)\rho_{jl}.}\tag{TEST}
\]
上界逐源用q+≤ρ·childprofit。反向每个正预算源独立选达到最大比的一个有限孩子，放λ=u_j(B)/u_j(child)，其它请求0；无正比或零预算源取0。不同源没有共同分支容量约束，故可同时达到所有源最大。iα>l请求不贡献目标，置0即可。因此PCAP等价L_l≤2u_l(B)，只是一个有限线性优化消元，未新增实际钱。

逐客户c_B≥2（actual j/l都覆盖），故q+≤u_j(child)/2，得到ρ≤1/2及L_l≤(1/2)Σ_(j<l)u_j(B)。这只是前缀总利润的粗上界；没有由2u_l(B)支付该前缀利润。原目标l的IC确给全部合法主题的真实当前收益≤u_l(B)，复制B_j还使旧j与当前l在该复制完成叶等收益；但TEST分母来自许多更早分叉的不同W^α，不能把它们替成同一次复制完成中的源利润。

35例actual A与E不交，目标l2只有源j1，q+原每项0，故L₂=0。它否全利润COPY2与实际比例，却没有违反PCAP。没有把相同“cap2”标签下的不同来源/客户支持/预算定义合并。

# 后续局部正面组件与旧11输入记录

已实际全文比较后来的[固定单孩子共同prefix回推](../引理/前缀请求回推的单调价格与祖先规范化--引理.md)和[固定父共同列/反向分裂](../引理/共同列容量与保正价的反向分裂--引理.md)。它们给同一B/W的一组prefix共同列界和合法域处理，不能把不同孩子各自的cap相加后宣布TEST被付清。辅助双边客户矩阵、H-overlap余量也各有角色/支持限制；在本4稿中没有将它们与SRC合成一个已证PCAP。

4350B原检查点只记一份probe_prefix_request_cap.py旧定点检查：11份指定旧证书，root-tax、fractional-actual-load、prefix-balance、global-decorrelation、individual-security、worst-PNE、worst-CCE、eight-CCE、aggregate-theta、collision-free和上传四人十二主题auxiliary。原称用Fraction重放全部真实有序IC后计算TEST、保每源最大孩子及饱和λ，未见违反，root要求停扩输入后已停。

本次没有取得其实际代码/JSON/11输入，不因原叙述冒逐行已读或新原run。11个有限未分离不证明一般PCAP、不推出cap1、不是新小人数正面结果，也没有购买half。源码检查点本身是探索记录，不是完成付款定理。

# 与本轮817边界和历史时态

[同批817全p边界](../反例/八百十七单位客户的逐角色均值分数全查询付款失败--反例.md)否指定逐角色p均值的FG-all-p，PCAP则是带原交集支持和逐源利润归一的另一合同；两者未在此证明等价。作者末段的“弱FOMA”只作旧目标名称导航，本4没有完整定义，不凭名称新登记一个候选或移借真值。原稿2026-10-24的一般/五人OPEN保历史，现五人half他证不补PCAP或COPY2；一般/六人目标未由这组材料解决。

本页完整保4838/4093/4350三个原数学MD及其确切先验，0程序导入、Fraction/LP/BI/IC/菜单或新数学运行。原件指纹/真实取得/primary时点/前置发布与逐源receipt见[本批证据](../../tools/evidence/fractional-global-copy2-and-cap-author-four-primary/README.md)；未取源的代码或其它独审不凭导航补成已读。
