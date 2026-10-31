---
id: "unrelated-machines/residual-throughput-occupation-final-review"
kind: review
type_tag: 审查
title: "残余通过量格结构与占位图表示最终独立审查"
status: integrated
truth_status: "fixed-residual-lattice-and-occupation-deficit-scopes-confirmed; dynamic-role-gap-retained"
review_level: "full-read-5532-byte-review-cross-archive-residual-occupation-comparison"
scope: "UM-RESIDUAL-THROUGHPUT-LATTICE-v1, UM-OCCUPATION-INDUCED-EDGE-DEFICIT-v1, fixed-sink occupation face, graph deficiency, finite audits and joint-recovery boundary"
summary: "8c89e756… 是 residual throughput/occupation 的最终独立审查记录。本文完整读取 5532 字节，核对固定残余 LP 的格次模、零边解释、占位缺口、动态角色失效、任意图独立集表示、finite LP/max-flow 证据、规模/位复杂度和一般恢复算法缺口；与 private-sink convex-hull、occupation face、Hall/price-cover、heavy matching 对象去重，不升级一般 UM。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/residual_throughput_occupation_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/residual_throughput_occupation_review.md"
  - "related-source:c8cdbf5ff2de274caf1b:research/current/unrelated_machines/residual_throughput_and_occupation_projection.md"
  - "related-source:37cf25f76e20361e1511:evidence/runs/unrelated_machines/occupation_base_face_independent_audit.json"
  - "related-source:bc9a4af396b1b13d8692:evidence/runs/unrelated_machines/occupation_induced_edge_deficit_release.json"
related_objects:
  - "凸包边际与残余通过量占位双源审查--审查.md"
  - "占位基面与残余边缺口有限审查--审查.md"
  - "固定汇点占位基面与未知OPT承诺的最终审查--审查.md"
  - "任意汇点价格覆盖与共同占位联合舍入最终审查--审查.md"
  - "重型匹配凸化与逃逸残余审计--审查.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/residual-throughput-occupation-20261031/original/residual_throughput_occupation_review.md"
source_sha256: "a8027c1fc83d01c83f1dc39ab3232539b23143e743be61a5936bc953901e8015"
source_size: 5532
---

# 1. 来源身份与独立阅读范围

本轮完整读取 8c89e7565baec0618625 的 review 源，5532 字节，SHA-256 为 a8027c1fc83d01c83f1dc39ab3232539b23143e743be61a5936bc953901e8015。对象覆盖 UM-RESIDUAL-THROUGHPUT-LATTICE-v1 和 UM-OCCUPATION-INDUCED-EDGE-DEFICIT-v1。

记录先由两位研究者独立处理：一条路线推导固定 R 的对偶格闭包，另一条构造严格次二占位的图缺口；随后图构造者攻击公式、允许牺牲 padding 并用实际最大流验证，主研究者再统一重写。之后独立攻击者完整读取最终正文与两份代码并复跑正式审计；不把旧共同容量背景或同一研究者重复执行计为新外审。

冻结来源和相关程序 hash 已在原 review 中固定：

- residual_throughput_and_occupation_projection.md：SHA-256 2c0c8001e0c2313bdcad7ca434e8a16688f10488aa050ff9390ab642fa9a295e；
- residual_throughput_lattice.py：SHA-256 66677a73831484233020020b89df6e21c18e71e9e1b3bd37d7d5e74d3830f12a；
- occupation_induced_edge_deficit.py：SHA-256 5d2b822bf18e0ea081a2627b755d248f855d2a003b169cb0818e80509bc6f966；
- residual throughput release JSON：SHA-256 faf7ac1bd3e95e2e4345466f31a128483d6023532c52046c4e7d884d51f3bff6；
- occupation release JSON：SHA-256 2070d39d86c82673779a6505ef0df6d0b92713af8bcb4d940822eca399df4d94。

本审查不是外部同行评审，也不认证全球新颖性。

# 2. 固定残余通过量的格次模合同

给有限机器 M、残余任务 R、资格边 E、非负有理时间 p_ij 和容量 c>=0，定义

F(c)=max Σ_(i,j) x_ij

其中每个任务分配总量<=1，每台机器负载 Σ_j p_ij x_ij<=c_i。对偶为

F(c)=min {Σ_j a_j + Σ_i c_i u_i : a_j+p_ij u_i>=1, a,u>=0}。

取两个最优对偶的 coordinatewise min/max 组合，可得 F 单调且满足格次模：

F(c)+F(d) >= F(c∨d)+F(c∧d)。

证明只需 p_ij>=0，允许任意异端处理时间。显式有理 LP 可在输入位长多项式内精确求 F 并返回 primal/dual 证书。F(c)=|R| 当且仅当所有残余任务存在共同分数路由。

若任务有零资格边，必须先把零时间/零资格任务按源合同剥离；物理删除机器的资格语义不能与零边免费预处理混淆。固定占位 I、容量 c_i(I)=C_i−a_i 1_{i∈I} 时，g(I)=F(c(I)) 是非增次模，缺口 D(I)=|R|−g(I) 是超模。这个固定残余性质本身不能推出联合占位选择，方向也不能误用次模最小化。

# 3. 动态角色变化会失效

当宏边选择 H 同时改变残余任务 R(H) 与扣减 h_i(H)，冻结 R 的格次模性不能直接继承。原矩阵 `P=[[1,1/2],[1/2,1]]` 给出 V(empty)=2、V({e})=V({f})=1、V({e,f})=2，非单调且非次模；其实际 `OPT=1/2`，由两件任务分别走交叉 light 端同时达到，而每任务所有有限端至少 1/2 给下界。它是范围负控，不是 promise 算法反例；不要与另一任意图占位构造的 OPT=1 混同。

即使固定 R，F(c) 接近 |R| 也不保证每个任务均完成；一个只剩 1−eta 容量的任务即可使 F<1。故“通过量接近全任务数”不能替代实际全局调度。

该动态角色缺口是 residual-throughput 对象的主要开放义务：若一般算法需要同时选择 H、R(H) 和容量扣减，必须另行证明共同可求的恢复、联合匹配和固定误差，不可将固定-R格性质静默延伸。

# 4. 任意图占位诱导边缺口

UM-OCCUPATION-INDUCED-EDGE-DEFICIT-v1 固定有理 alpha∈[1,2)、delta>0，对任意显式简单图 G=(V,E) 构造：

- 每顶点一台图机和一台辅助机；
- 每顶点一件宏任务，可在所有机器上时间 1；
- 每顶点 r 件只可在自身图机上的 tiny；
- 每条图边一件只可在两个端点图机上的 tiny；
- tiny 时间 h=1/q<=delta，r=q(alpha−1) 为整数；
- q 是 alpha、delta、最大度 Delta 的显式整数倍，满足 Delta h<=2−alpha。

宏任务放辅助机、专属 tiny 放图机、边 tiny 任意定向给出峰值 1 的完整调度，单位宏下界给 OPT=1。对占位集合 I，图机容量是 I 内 alpha−1、I 外 alpha。固定残余通过量缺口恰为

D(I)=|R|−F(c(I))=|E(G[I])|。

上界按 I 内专属 tiny 加内部边 tiny 的容量计数；不假定 LP 先安排 padding。下界保留专属 tiny、丢内部边 tiny、把其余边定向到未占位端，负载逐台合法。因此完整占位可行集合恰是 G 的独立集族，显示该系统可实现任意图结构，不能自动视为固定数量拟阵或 p-extendible。

星图 K_{1,s} 已足以说明叶集可行、加入中心需移除所有叶；该表示是集合系统障碍，不是 makespan hardness，因为实例本身总有 OPT=1 的辅助机调度。alpha/delta 固定时构造规模多项式；若二进制参数极小，tiny 件数和位复杂度需单独收费。

# 5. 有限证据与审计边界

occupation base-face 有限审计覆盖小型 transversal presentations 和 20,760 个 faces，核验暴露面仿射维数及 changing coordinates=2*dimension；不测试私有 DP、heavy-home 枚举、sink budget LP 或实际 scheduler。它是有限面证据，不替代一般 occupation face lemma。

occupation-induced edge-deficit release JSON 对 15 个 K1/K2/P3/K3/K1,4 及 alpha∈{1,3/2,199/100} cases 生成实际矩阵、完整宏/私有/edge tiny jobs，验证 OPT=1、全部占位子集的独立集 iff 和整数最大流 deficiency=内部边数。无随机抽样，Fraction/整数，Python 3.12。它不覆盖任意图全枚举、任意 alpha/delta、统一 scheduler 或一般 hardness。

# 6. 与相关对象去重

与 private-sink convex-hull/negative-correlation 障碍：前者固定真实凸包点、要求集中迁移，后者固定残余/占位并研究 F 格性质；两者共同说明局部边际证书不能直接承担动态全局恢复，但量词不同。

与 fixed-sink occupation face：面维数与 2K 混合 home 结论是 occupation 模式的固定-T 结构；本 review 的任意图缺口和 F 格次模是动态残余/图集合系统，不能互相替代。与 Hall/price-cover/heavy matching：这些是共同资源池、价格覆盖或匹配合同；本对象的任务身份和容量扣减可随占位变化，不能免费套用。

与 CAG/SPE：宏/占位/容量模型无客户目录、终局均分或完整历史纯 SPE，保持 unrelated-machines 隔离。

# 7. 处置与未闭义务

处置为 integrated：原 review 已复制到 evidence；正文保存 F 的 LP 对偶/格次模、零边解释、动态角色失效、任意图独立集缺口、面/最大流有限证据和参数位复杂度边界。

仍未闭合：

- 一般 H 同时改变 R(H) 与容量时的共同恢复/舍入；
- 固定误差下的真实联合调度和全局容量控制；
- 任意图占位系统之外的结构识别；
- 一般 UM 近似算法、UM-TARGET-v1、外部新颖性和 hardness。

本对象没有把 finite scripts 或有限图族升级为一般定理。

