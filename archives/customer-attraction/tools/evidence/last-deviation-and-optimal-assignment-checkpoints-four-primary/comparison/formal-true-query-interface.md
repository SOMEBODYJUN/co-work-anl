---
id: "customer-attraction/真实最优查询的冻结差额与可信修复接口"
kind: "resource"
type_tag: "资源"
title: "真实最优查询的冻结差额与可信修复接口"
status: "proved-accounting-and-historical-interface-boundaries"
summary: "V/F、裸遗漏/净差、signed Q与首次偏离min、比例中继失败及2R+D可信修复各保量词和历史有限scope。"
source_ids: ["7e27faf6c4cbc21b7ba8", "e177dc302942e7acf6de", "2dbdf5a83cd9c423d56b", "737d3cbea9d2ecff7ff6", "458d2e5f0e6c31f4dd8b"]
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_4/README.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_4/README.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_4/duplicate_action_quotient.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_4/duplicate_action_quotient.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_4/minimum_reply_commutation.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_4/minimum_reply_commutation.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/review_action_quotient.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/review_action_quotient.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/QUERY_INTERFACES.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/QUERY_INTERFACES.md"]
review_status: "五MD22861B全文及正式相关全文比较；完整22ids claim pushed/synced且本5owner/SHA核；0原codeJSON/0原或新数学程序，15客户全报价表为知情手工解析非新1024运行；逐源retained"
---

# 真实最优查询的冻结差额与可信修复接口

## 原索引是按需回读，不是新审查或付款

4536B QUERY_INTERFACES是父方按研究者问题回读原文的接续索引，自述不是新数学、独立完整审查或目标证明。本页把其独有基准、账目、失败桥和修复前提实质保全；引用到的每个原code/JSON/长稿不因此视为全文读或额外primary done。所有合同采用有限单位客户、共同有限非空目录、单位玩家和全部有序历史纯SPE，保任意平局。

实际有序路径S，覆盖C，W=|C|；T=(T₁,…,T_m)为达到OPT的索引元组，允许重复。V_ij是在**实际前缀**强制T_j后，同原σ按改变历史真实完成的当前收益；F_ij则冻结其他实际动作，若c_x为实际负载、a_i=1_Si，则F_ij=Σ_Tj1/(1+c_x−a_i)。只V_ij≤u_i可用真实IC，F不可用。

| 接口 | 精确现有范围 |
|---|---|
| 存在最优T和π，Σ_iV_iπ(i)≥|O\C| | 已被完整两人SPE否定：唯一最优支持下两匹配均41<42 |
| 存在最优T和π，Σ_iV_iπ(i)≥OPT−W | 本源当时OPEN充分桥；当前已读正式候选亦未关闭，41vs42例的净差仅1不能反驳 |
| 存在最优T和π，Σ_iF_iπ(i)≤W | 不同的冻结指派强桥，已有反例；不能用它代替真实V的净差接口 |

[41vs42完整证明](../障碍/最优组合真实偏离匹配不足--障碍.md)给W44、OPT45、唯一最优(B,D)、V矩阵两行(19,19)/(22,22)。本索引“按需检索未找到净差反例”不是穷尽全仓/文献声明；当前也不把再次陈述充分性当推进。

## signed差额与共同预算的准确层级

记H=O\C、I=O∩C、G=C\O，比较重数d_x，实际重数c_x。[完整非负信用恒等式](../引理/最优主题菜单的非负静态信用与带符号自适应恒等式--引理.md)已给显式L_i≥0，使

$$\sum_jF_{ij}=\operatorname{OPT}-W+u_i+L_i,\quad Q_i=\sum_j(F_{ij}-V_{ij}),$$
$$\sum_jV_{ij}=\operatorname{OPT}-W+u_i+L_i-Q_i.$$

Q_i可正可负，末位Q_m=0。若在一个真正最优T证明Σ_iQ_i≤W+Σ_iL_i，则全位置相加得Σ_ijV_ij≥m(OPT−W)，再用ΣV≤mW推出half。更强ΣQ≤ΣL给OPT≤(2−1/m)W。它们都是未证共同付款，不是把Q按定义改非负即可成立。

对单个索引排列定义L_π=Σ_iF_iπ(i)−(OPT−W)、Q_π=Σ_i(F_iπ(i)−V_iπ(i))。H每客户冻价贡献d_x≥1，I冻价非负，G从净差中扣去一份，直接给L_π≥0。因此

$$\sum_iV_{i,\pi(i)}=\operatorname{OPT}-W+L_\pi-Q_\pi.$$

某π满足Q_π≤L_π就是净差真匹配接口。均匀排列平均在**固定有限V矩阵**上进行，每(i,j)概率1/m；没有交换真实玩家次序、随机化原树或把互斥枝利润共同领一次。静态最小F指派不替代这条预算，详见[净差候选](../候选/真实最优组合的净差匹配与共同付款--候选.md)。

## min压缩、比例中继与有限停止范围

原direct_cover已用actual路径首次偏离子树互不相交：在每个actual节点，把非actual动作孩子换成使刚入场者利润最小的完整子SPE；actual自行动孩子保原实现路径。孩子真SPE、替换后偏离收益不增，故可同时保持actual及完整IC。这**不**允许actual自行动孩子也无条件换成极小尾；[首回复前移严格间隙](../引理/极小可信续局首回复前移与严格间隙--引理.md)明确展示父IC可破。

[BAAF四人完整反例](../反例/实际前缀单主题比例中继的四人反例--反例.md)给f₄(空,A)=9，而actual首行动B后的f₃(B,A)=13，故9<3·13/4=39/4。附加的正是实际前缀动作也不能恢复f_r(b,T)≥(r−1)f_(r−1)(b+A,T)/r。该单主题/节点max反例没有否定跨主题净差匹配。

本源原报告global_coverage七份现成完整策略锥、66个指定最优支持的净匹配阴性重测并停止；两次浮点端点未通过有理恢复，其余未恢复全锥对偶。那不是当前新67次或一般最优证书，不应重新跑同批诊断记新信息。另有[四固定锥弱平均资料](../资料/真实偏离弱平均的最优元组合同与有限锥--资料.md)是不同四输入/含重复最优元组的浮点合同，不能把7/66与它合计成同一次全称检查。本批不读或跑这些原代码/JSON。

actual-only客户G在一个真实查询叶的未来份额，等于原后缀G份额+旧前缀G损失−新遗漏信用。此单叶恒等式不准丢旧前缀损失，也不允许每个互斥枝各领一份同一G。min压缩没有自动消除这一共同付款义务。

## 可信缺陷修复的实质前提

已读正式[统一/异质前缀修复](../定理/真实退出缺陷的统一与异质前缀修复--定理.md)保原索引的同人数完整Cartesian目录修复：输入目标前缀可不理性，但目标尾本来须为真正完整子SPE。每个前缀位置i，强制任意主题A后在**完整可信孩子**取极小利润ℓ_i(A)，M_i=max_Aℓ_i(A)，目标利润u_i，δ_i=(M_i−u_i)_+，R=Σδ_i、D=maxδ_i。真实修复后精确有

$$\operatorname{OPT}_{new}-2W_{new}=\operatorname{OPT}_{old}-2W_{old}-(2R+D).$$

首次任意联合异常后全部坐标永久进可信模式、完整Cartesian目录与共同缩放单位客户是承重条件。故只有旧正坏差>2R+D才给half反例；本索引未提供这样的输入。这不是actual-node冻结后悔付款；删客户后的实际后悔小，不控制真正可信child缺陷。旧末位本身非BR时，不能用保险修复掩盖输入不满足真尾合同。

本页未重造该已完构造或旧成功run。原接口索引回读记录、商编译测试和min局部例各是不同数学/证据，均未关闭一般六人half；后续研究方法不由这些历史路线预先限定。
