---
id: "customer-attraction/all-position-pair-static-security-candidate-and-finite-cone-scope"
kind: "candidate"
type_tag: "候选"
title: "全位置成对安全值候选与有限锥判别范围"
status: "complete-source-scope-open-general-payment"
summary: "全位置pair≥2v仍候选，保有限minimax等价、末两已知范围、条件聚合比率与全部浮点表，不将阴性锥或当前五人half作pair证明。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-ab4b3c24c8f949198e194dd45bb66105/credible/README.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-ab4b3c24c8f949198e194dd45bb66105/credible/README.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-ab4b3c24c8f949198e194dd45bb66105/potential/README.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-ab4b3c24c8f949198e194dd45bb66105/potential/README.md"]
source_ids: ["11ac8952a5566d864f13", "5d6a7710f57a33aea786"]
truth_status: "general pair conjecture open; listed implications/certificate equivalence valid, historical finite LPs do not prove it"
review_status: "whole five primary and local related mathematics read; informed analytic reconstruction including one eight-client case; original finite/independent/nonblind scope retained; no new mathematical CLI"
---

# 全位置成对候选与真正静态值

使用[原单位客户共同目录模型](../定义/共同目录完整历史模型--定义.md)：m≥2，有限非空真实集合目录，单位提供者与客户，完整有序历史纯SPE，保空/重复/零客户/任意平局。固定实例真正不观察查询的整数静态安全值

v_m=max_p min_(B∈S^(m−1)) E_(T∼p) Σ_(x∈T)1/[1+c_x(B)]。

对同一完整SPE实际收益u₁,…,u_m，原4385B稿提出仍未付的候选：**任意不同位置i,j，u_i+u_j≥2v_m**。它弱于每人u_i≥v_m，强于单一聚合W≥mv_m；不能从逐人桥已假直接推pair假，也不能从聚合或half已证反推全部pair。

若全部无序pair成立，求和得(m−1)W≥m(m−1)v_m，W≥mv_m。结合[静态锐界](../定理/静态混合安全值的锐目录计数界--定理.md)OPT_m≤(2m−1)v_m，得**条件性**OPT_m≤(2−1/m)W。m5将给9W/5，但一般pair前提未证，本批不能宣称该更强五人界或一般half已闭合。当前[五人half](../定理/五人半覆盖--定理.md)另有证明，不自动支付此更强候选。

# 有限minimax的精确成对证书

对固定实例/策略/位置对，有限零和对偶使pair不等式等价于存在一个合法m−1槽**静态**背景分布Q_ij，令每个合法查询T同时满足

E_(B∼Q_ij)Σ_(x∈T)1/[1+c_x(B)]≤(u_i+u_j)/2。

Q可依实例、策略与pair；竞争行动可相关，Q不能观察当次查询。它不必是根真实菜单推送，更不要求背景自身为SPE。若拿真实菜单限制Q，会改变可行域；删其余玩家再调用二人SPE恒等式也不合法，因为背景、后继和IC一起改变，不能冻结中间行动。

末两位置的pair已由[末两人逐人保底](../定理/末两人逐人保底与全人数弱福利界--定理.md)得到：每人≥θ_m≥v_m，故sum≥2v_m。任意早期pair须另构造Q或用全树IC支付，不是已证范围。固定实际叶均匀删位背景的cap曾失败，不能把这一个Q免费作全部pair证书。

# 原有限浮点表的全部范围

原稿为识别反例，固定完整**形式策略**及查询p，客户类型质量作非负实变量；保全部类型和全有序IC，约束每个合法m−1槽背景下p收益至少1，最小化指定pair。只有浮点目标<2后还恢复不同单位客户并完整全树认证，才可能是pair反例。原列均未产生这种输出：

| 固定形式策略 | 固定p | pair从1编号 | 原浮点最小值 |
| --- | --- | --- | --- |
| 既有36/34六标签三人形式 | 六主题均匀；另(10,10,21,10,10,21)/82 | (1,2)、(1,3) | 均2 |
| d837bffdf7e0 / cascade | 七主题均匀 | (1,2) | 2 |
| 9715325c6b4e / returning_minority | 七主题均匀 | (1,2) | 2 |
| 3c29e8f9160e / delayed_reversal | 七主题均匀 | (1,2) | 2 |
| 上述cascade | 分别均匀零基{1,3}、{1,3,6}、{0,1,2,3} | (1,2) | 均2 |

原稿称复用attack_individual_defect.py的全策略行构建、scipy/HiGHS LP；未转精确对偶，没证明这些锥的pair定理，也未继续扩样。此表是列明条件的浮点有限历史，不是当前run次数、更不是全模型无反例。本批未读/导入/运行那个程序或策略压缩包，不捏造求解过程或证书；原Markdown逐字保全。

# 停点与已否定的额外加强

原稿已停止PI首位势边际、强弱iid桥、局部余额非负、纯势排序/高插入无环等旧失败路线，不新增这些障碍。其“最优全部遗漏≤W”也确实不是可用简化：[唯一最优遗漏族](../反例/唯一最优组合的全遗漏支付--反例.md)在两人k3有71客户，W35、OPT38、遗漏36>W，而最优外实际覆盖33，真正净差仅3，half余量32；客户重数k不是提供者数。本批全文比较既有全参数证明，不重跑或重done，避免丢掉实际最优外信用。

通用pair若成立，会接到[强聚合及累计M等价](../等价/强聚合安全的唯一价格与累计门槛的有限编译--等价.md)；但这项等价没有给pair的早期Q。原“m5同式未付”是本路线状态；真正待解决的是一般全树成对付款或明确完整SPE反例，不能把旧阴性锥扫描当成果。证据与完整scope见[说明](../../tools/evidence/exact-M-checkpoint-and-terminal-review-primary/README.md)。
