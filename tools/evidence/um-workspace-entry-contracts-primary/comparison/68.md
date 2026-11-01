---
id: "unrelated-machines/explicit-xos-nsw-final-review-proof-obligations"
kind: review
type_tag: 审查
title: "显式XOS分数NSW的确定化合同与真实审读链"
status: complete-primary-read-and-scoped-mathematical-reconstruction
summary: "全分数benchmark、固定lift纯有理progress、support CDF、先候选后label、shifted inverse/误差一DP和任意比较rematching；不继承旧generic tail错误或声称软件。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/explicit_xos_fractional_nsw_original_canonical_before_gamma_correction.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/explicit_xos_fractional_nsw_original_canonical_before_gamma_correction.md"
evidence_manifest: ../../../../tools/evidence/um-next-available-reviews/source-manifest.json
---

# 原模型、真实量词与来源

主源34a5b405d5ea02b46f89全文15036B/90行已读，含原审查、25条原来源表及2条纠错来源表、两份gamma纠错的语义合并。本文只承载A/B数学与审读链；[互补与REPAIR页](归一化菜单高低比例互补的实质纠错及修复边界--审查.md)承载C–F和纠错。当前canonical e7736babc411473bec2a全文765行已读；原651行608c39c70c3acf175aba的header/F/tail实际读，A–E与当前逐字节相同35234B，SHA02a7557526a4626f3e1f3c7e3780c425c3202dda6d8f56eab32b57a75b8d23d1，共同数学亦已读。

物品U有限，n≥1代理，真实allocation为原物品上两两不交bundles，可闲置物品。正分数benchmark y是有限有理配置族，行和1、每原物品列≤1、所有正质量配置v_i(S)>0，定义B_v(y)=exp((Σy ln v_i(S))/n)。重复配置不复制物品。后述算法只输出无权几何平均，未给weighted-agent结论。

UM-FRACTIONAL-BENCHMARK-REMATCHING-v1允许一般单调次可加v_i且v_i(∅)=0。给|H|=n、B=U\H、V_i≥0、A={V_i>0}，必须有i∉A⇒v_i(B)=0，并且对B上**每一可行分数配置族z**有Σ_(i∈A,T)z_iT v_i(T)/V_i≤cn。这个全称语义假设不是算法可验证oracle，也不能换成整数福利上界。则H上有双射π，使GM(V_i+v_i(π(i)))≥B_v(y)/(c+1)。

证明把配置质量送到其H中最大singleton；H-empty质量只来自A。以真实行列缺口运输补成双随机q，所有因子V_i+v_i(h)>0。次可加性将每耦合条目的ratio分给残余比值与|S∩H|，两项总和≤cn+n。Jensen给Σy ln v≤Σq ln(V+singleton)+n ln(c+1)，正支持permutation分解给一个π。零V、零singleton、空A/B不在零上取log。

# 显式XOS的全分数确定性规格

UM-EXPLICIT-XOS-DETERMINISTIC-FRACTIONAL-NSW-v1输入有限非空indexed clause表，v_i(T)=max_sΣ_(j∈T)p_isj，p为非负二进制有理数。允许零/重复clause、零总量、unused items，无全局normalization、数值网格或最小正系数假设。单个确定性输出同时对每个正y满足NSW≥B_v(y)/1125000；算法不输入y。它不是oracle-only XOS、一般subadditive后端或weighted NSW结论；数学规格无端到端软件。

1. 全U上找正singleton匹配。Hall失败时正实际allocation及正分数benchmark均不可能，返回空bundles，真实最优NSW=0。否则求全U真最大正product匹配τ，H=τ([n])，B余物品；只在固定H最优不足以支持后面的反事实换边。
2. 对A={v_i(B)>0}，以W_i=v_i(B)归一残余clause。固定lift有λ行和1、0≤z_isj≤λ_is、每物品Σz≤1。任何分数残余族用attaining clause lift进去；反向按z/λ排序的nested prefixes恢复至多|B|+1支撑，actual期望≥image utility。A空时省略后端。
3. a=|A|，b_i=1/a是可行image，ℓ=1/(4a)、h=1/(32a²)。在同一lift最大化M=Σu_i/x_i；M>2a时更新x←(1−h)x+h(b/4+3u/4)。x_i≥ℓ，log势每步增加>1/(128a)，而势从−a ln a到≤0，故<128a³次更新。a=1初始即停。lift矩阵0/±1、RHS0/1与objective无关，Cramer给固定顶点共同分母位界；每更新分母只增加多项式bits，避免递归放大。重算actual期望V_i≥W_ix_i，终点对所有分数族Σzv/V≤2a，给A的c=2。
4. 对恢复的支撑族各代理独立挑配置，以attaining clause系数/期望作为bid。每item阈值t的总请求s(t)≤1，1−Π(1−p_i(t))≥s(t)/2，所以期望normalized welfare≥q/2。有限bid levels的精确CDF式Σ_ℓ(t_ℓ−t_(ℓ−1))[1−ΠPr(bid<t_ℓ)]逐代理条件期望固定，给支撑内真实不交bundles。不枚举联合样本，tie用严格CDF。
5. 对A''={V_i≥6ν_i}（ν_i残余最大singleton）将高值配置分成原物品不交部分，价值在[V_i/3−ν_i,V_i]，继承质量≥1且物品边际不增。取d=5/2、δ_m=1/(7d)=2/35，反复福利舍入，每轮固定≥δ_m比例的满足者；至多|A''|轮。所有候选S_i、轮t_i及attaining clause先固定，之后才赋每原item唯一label，Pr(label=t)=δ_m(1−δ_m)^(t−1)。同轮候选不交、跨轮label互斥，最终物品不复用。

# 局部网格、逆矩与任意比较匹配

只对候选辅助权取Q=210|B|、a_ij=floor(Q w_ij/V_i)/Q、β_i=ν_i/V_i。总损失<1/210=δ_m/12，Σa≥δ_m/12、Σa≤1、各a≤β_i。此floor不改原valuation、物品或物理处理时间。

独立Bernoulli、0≤a_j≤β、M=Σa_jp_j>0时，令Y=Σ(a_j/β)X_j。凸性弦界t^d≤1−d+dt给E t^Y≤exp(−(M/β)(1−t))；积分得E[1/(β+ΣaX)]≤(1−e^(−M/β))/M<1/M，再以log的Jensen得E[−ln(β+ΣaX)]≤ln(1/M)。只承载单候选内独立加性weights，不能直接套一般subadditive或相关mask。

势Φ=Σ_(i∈A'')−ln(β_i+Σa_ij1[label_j=t_i])。整数权Qa总和≤Q，所以每行剩余分布用Q+1格卷积，概率分母位长按输入分母bits相加。log表每项绝对误差1/(2|A''||B|)；逐item选近似最小条件势，每步损失≤1/|B|，总损失≤1。无需除tiny prefix概率，也无1/β个状态。rank计数与ln(a!)≥a ln a−a给GM(V_i/(ν_i+v_i(T_i)))<10000d²。所有i∉A''明确T_i=∅；这包括A''非空的情形，是最终102B补句的真实内容。

对任意比较π:[n]→H，τ全U最优给rematching：在singleton successor图中，每个偏好残余ν的顶点都删除outgoing边，包含cycles的图拆成止于该顶点的不交路径。逐路径反事实用残余item替换，τ最优给product比较；不同路径可分别使用同一残余maximizer作反事实，未同时分配它。由此存在ρ使Πmax{b_i,a_iρ(i)}≥Πmax{b_i,a_iπ(i),ν_i}。零比较product空泛、零outside因子由正b保护，均有分支。

最后在H上以原v_i(T_i∪{h})求真最大product。A''内ratio付2V/(ν+b)，A\A''付6，outside付1，sum-to-max再付3，得到对所有π同时NSW≥GM(V+singleton)/(60000d²)。A的c+1再付3，60000·3·(5/2)²=1125000。旧generic-SA链漏掉的三因子和不适用的tail估计并未被这条显式XOS替代证明“追认正确”。

有理最大product由不同乘积log间隔≥2^(−2nL−1)和每边误差G/(4n)的有理最大权匹配精确实现。log用binary scaling及atanh级数，精度bits多项式；不比较任意超越数benchmark。以上LP、支撑、CDF、轮数、Q格和匹配均按显式总位长多项式，不按系数倒数或原分母数值展开。

# 实际审读链与外部先验

v1/v2/v3 statement-only及rank Exact-only保留旧数值反驳；v4/v5 coauthor记录是熟悉工具者的验证/提案来源，没有可追认的旧v4完整NSW作者Proof。独立6.1-sol只获冻结Exact v5（解压原hash3160d7…），先冻结a90086…；root读完后才释放已冻结作者Proof v5（298935…）。作者事先读过Exact-first/工具，是informed author。独立read-after d70dcc…、最终canonical ba2e84…不是新盲审。原651行2365f5…曾按1–220/221–440/441–651实际重读，102B补句被差分核实。

主源25行原来源表（另2行纠错表）逐项保留于原件：v1–3 Exact/rank，v4/v5 gzip Exact与coauthor，v5作者/Exact-first/read-after/final，shifted inverse四源，grid-DP四源，primary-scope audit及DLRV PDF/text。container与解压hash分列；本轮只核inventory可绑定者，不把表中链接阅读扩大为全部原件已读。standalone inverse/DP的PASS不自动认证完整NSW常数。

历史root对DLRV arXiv:2309.04656v1仅针对性读§2.1–2.5/Appendix B及相关Thm17/19/20，渲染看PDF12/13；英文作者读供给文本全篇而非PDF，独立审者只读文本splitlines229–768、1212–1346。文本1391换行+23formfeeds=1414 splitlines；23页326593B原PDF的arXiv页眉2023-09-09与内文2023-09-12分开。matching/splitting/iteration/rematching继承模板；本轮未重读外部PDF或新做新颖性检索，不导入文献的integral-OPT theorem为fractional结论。

既有《分数重匹配与归一化XOS稳健缺口边界》保留早期条件成熟度，《显式XOS与福利舍入三源边界》保留文献/内部规格分层；本页不改它们，而写清本5源审查实际覆盖和上面的重构。内部数学与未实现软件、外部发表、外审和全球新颖性继续分开；当前没有代码审计或运行来认证完整算法。
