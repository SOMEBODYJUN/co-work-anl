---
id: "unrelated-machines/research-entry-and-um-target-boundary"
kind: "resource"
type_tag: "资源"
title: "不相关并行机研究入口与 UM-TARGET-v1 边界"
status: "retained-navigation-and-scope"
summary: "冻结的研究入口页。它把不相关并行机 R||Cmax 的目标、当前暂停状态、路线正文、证据与审查入口串起来，并逐项保留各路线的量词和适用范围；它不是一份新的统一近似定理，也不关闭 UM-TARGET-v1。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/unrelated_machines/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/unrelated_machines/README.md"
  - "source:0cc2d00f55ebae08d785b76e8956b9402222f3d1:research/unrelated_machines/README.md#sha256=3f500dbd1f48aa31778b5fa3e59603b29708d79c0ffb2032fbcb3c6550fd803d"
related_objects:
  - "unrelated-machines/um-target-v1"
  - "unrelated-machines/configuration-lp-gap-boundary"
  - "unrelated-machines/heavy-matching-residual-and-escape"
  - "unrelated-machines/joint-matching-completion-and-block-cuts"
  - "unrelated-machines/cyclic-batch-repair-and-fork-obstruction"
---

# 处置说明

本源是 `research/unrelated_machines/README.md` 的冻结入口页，两个来源提交 `68fad804ec5946cb296f77dc5b336308a66abf12`（legacy-cleanup）和 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`（main）定位到同一路径；当前冻结 blob 为 `0cc2d00f55ebae08d785b76e8956b9402222f3d1`，SHA-256 为 `3f500dbd1f48aa31778b5fa3e59603b29708d79c0ffb2032fbcb3c6550fd803d`，大小 72,477 字节、424 行。本次逐段读取了标题、目标身份、路线表、长期资产表、模型边界、审查入口以及结尾的保存协议。它不是一个单独的作者证明或程序报告，而是把大量已经存在的 canonical 正文、审查和证据链接按研究义务重新组织。因此保留为资源对象，不把整页复制为定理；每项数学结论仍以所链接正文和审查为准。

页首明确当前全仓主攻是 `Q-CAG-HALF`，本页仅在显式选择 `unrelated-machines` 存档时作为入口。该路由决定不能当数学证据。它同时声明不相关并行机题的主身份为 `UM-TARGET-v1`：非负二进制有理输入的 R||Cmax，是否存在统一常数 `ε>0` 和确定性位多项式算法，对所有输入输出实际 makespan `≤(2−ε)OPT`。近二困难性是另一侧目标，原目标和一般反面均保持 OPEN。

# 页面实际提供的模型边界

页面重复强调以下边界，后续引用入口页时必须保留。

* 配置 LP 的 gap=2 只否定相应比较合同，不能被改写为原题 NP-hardness、统一近二下界或一般算法不存在。
* 任何“反面”路线都要给出固定 `ε` 的真实 OPT gap、完整 YES/NO 输入族、绝对阈值 decoder 和总位复杂度；复杂度假设逐条写明。有限矩阵、局部配置、静态福利或一个失败的舍入合同都不能替代这些量词。
* 源页的“当前用户决定研究否定”只是路线选择；不能把方向选择当作已证反面。
* 模型必须保留零值/空任务、禁边回译、边的有限性、机器与任务的总位长度、普通完整调度与部分配置 LP 的区别。
* 同一目录中把正面结构接口、条件算法、有限审计、候选反例和文献入口并列展示；它们的状态和承重范围不能由导航页合并。

页中给出的基本存档定位与现行 `archives/unrelated-machines/问题--问题.md` 相符：研究对象是 R||Cmax 非负二进制有理处理时间矩阵；一般统一 `2−ε` 目标和一般困难性都未关闭。入口页不是阶段三超图，旧地图或路线链接也不能自动生成数学边。

# 入口页逐项保留的数学路线状态

下面按源页实际分组摘要。每一项都保留原页的限定词，方便后续清洗者跳到 canonical 正文和冻结审查。

## 1. 正权菜单、部分激活与经典边界

`resource_distortion_flat_menu_rounding.md` 只在显式菜单数/资源度、`W≤1` 和固定同资源正权比 `κ` 的范围内给 `C≤2−(2−OPT)/(ακ)`（固定 `α>4`）；该结构推论没有完整后端实现，也不承载任意近二源。`partial_minrep_linear_degree_source_and_fee_bridge.md` 的条件复杂度结论是：若已有随机源有总多项式判别器，则 `NP=coNP`；若拒绝概率逆多项式，还得到 `NP=RP=coRP=coNP`。源页明确仍缺真实 compiler、完整输出 decoder，因此不能宣称一般反面。

`explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary.md` 的 F2 只是显式 norm1/共同支撑 LP 下的福利筛选（页中写作 `H_{3/8}>2q/5`）；它排除的是特定高组源，不是 R||Cmax 的普遍困难性。

## 2. 配置、匹配和共享逃逸路线

`heavy_matching_residual_and_escape.md` 给出三个限范围身份：安全位多项式 heavy matching 过滤、简单支撑配置 gap 和共享小端容量逃逸族。它们分别有正文、独立审查和双路代码/证据，但页中明确“主目标仍 OPEN、新颖性未认证”。

`joint_matching_completion_and_block_cuts.md` 分开三项：给定 `H,x` 的 `(3/2+δ)T` 条件构造；固定有理 `δ<1/3` 的精确选择 NP 完全（包含空 `N` 和每 job 唯一 small 的子情形）；以及随 `B` 变化的末簇切面。半单位扩展把承诺窗口推到固定 `δ<1/2` 的不可能性，但不涉及 `δ=1/2` 或其他舍入合同。入口页要求把三者分别引用，并保留审查和三份代码的证据定位。

`row_count_escape_gap.md` 的全局单行基数过滤和 compact shared escape 说明：即便每个单机配置可延伸到完整配置 LP，仍可能 `OPT=2−1/k`；完整条件矩和共同相关性仍缺。`joint_slot_prefix_rounding.md` 的正面接口只适用于删去零任务后每行正时间跨度 `≤2` 的条件，给一次前缀计数 LP 加全任务槽匹配的 `3/2` 构造。

## 3. 长链、循环和森林接口

`cyclic_batch_repair_and_fork_obstruction.md` 把局部优化器、固定单机迁出数的真实 OPT 障碍、以及需要多目的地分流的 padding 族严格分开。`UM-OPT-HULL-LONG-CHAIN-LOCAL-GAP-v1` 的精确族中，mincost 槽输出 `2−1/k`，严格 lex 改善需要 `d+1` 个任务和 `d+2` 台机器；这不是一般局部算法的近似界。

`rooted_dag_degree_token_bridge.md` 给出有向需求树的任务桥梁与精确 OPT 恒等式；两层需求树另有半比例贪心。二者都只是可复用的结构接口，不能外推到一般多层/多边界输入。

`forest_boundary_contraction.md` 的 `UM-FOREST-BOUNDARY-AUGMENT-v1` 只在唯一 boundary、内部无外接的森林上给 knapsack 父包界和逐机消元；双边界菜单版本同样需要后续共同选择机制。源页明确一般多边界、有环核心仍缺可计算共同选择。

## 4. 固定槽、边际与容量外包

`optimal_convex_fixed_slot_gap.md` 展示固定槽 matching 可以趋近 2，即使 `x` 有显式全局最优凸分解；这一族有实际证据和双路审查，但不是一般算法下界。`optimal_hull_marginal_rounding_barrier.md` 进一步给真实 OPT 凸包上固定 row/count 的 sup 2、pair-NC 负相关尾界、以及宏任务冻结后的迁移前沿；高阶成功概率只针对指定负相关族。

`minimal_star_contraction_and_capacity_gap.md` 分开多拟阵容量外包损失 `max(1,2−p/k)`、最小总处理量面的 near-2 断点、以及原地拟阵外包需要指数多个输入位长的局部结论。这些都是具体外包或支撑保持边界，不能升级为一般调度困难性。

`bounded_configuration_cardinality_slot_margin.md` 在固定配置任务数 `K` 的承诺下给 `(2−K^{-(K−1)})T`，其中 `K=2,3` 的 `3T/2`、`11T/6` 为锐界；当 `K` 增长，余量消失，未给无承诺全输入算法。

## 5. 菜单、标签和仿射源边界

源页保留了多组只针对特定菜单/标签接口的正面或反面：三坐标正规形、Cartesian 菜单 recoupling、block coherence rank、affine-line tuple groups、normalized menu configuration preservation、single-outer selector、raw K2、multi-outer tiny-home、gated menu welfare、tagged affine line gap、wide rectangle escape、bulk OR/commit、pairwise-independence boundary 等。共同规则是：每项正文给出明确机器/任务、权重、状态和 decoder 范围；独立审查和冻结输入用于有限验证；缺少全局物理 coherence 或低负载 NO decoder 时，不得改写为 UM-TARGET-v1 的一般反面。

页面还特别标明：许多“actual≤1.5”或固定 `3/2` 合同只覆盖局部模板，许多 `OPT→2` 反例只覆盖特定共享背景、固定矩、单外层或 clone 结构；即使合同被排除，也不自动排除其它算法。对 `source value 1/R`、`CONFIG(1)`、`M1/M2`、`D_+` 等接口，必须回到 canonical 正文核对同一对象是否仍保留原任务身份。

## 6. 复制、周期、正规形与位复杂度

`private_graft_and_resource_repetition.md` 的 complete-clone 多重周期结论仅针对每个机器/任务复制 `q` 份、全 `q²` 克隆边；最优周期由可行 `q` 的 gcd 决定，不能泛化到任意精选接线。`model_and_classical_barriers.md` 的常量正规形只把算法存在性缩到有限正整数边和 `O(log² n)` 种权值；它不提供近二困难性。

页中反复要求把 bit complexity、阈值精度、空菜单/零任务和禁止边回译写入定理。`succinct_prefix_atomic_decoding_bridge.md` 的有限精度桥只在精确守恒 law、带噪 max-mass 和有理网格的限定下恢复阈值；绝对误差的 `N` 倍稀释仍需保留完整原子空间。

# 证据、审查和后续使用

README 的长期资产表列出 canonical `research/current/unrelated_machines/`、题目账本 `research/unrelated_machines/`、候选 `research/questions/unrelated_machines/`、审查 `research/reviews/unrelated_machines/`、历史文献、`tests/audits`、`evidence/certificates` 和 `evidence/runs`。这些路径描述了复现链：先读定义和精确正文，再读冻结审查，最后读程序和输入；程序输出是有限证据，不替代理论量词。

源页的保存协议也有数学含义：每个 Claim 要同步登记正文、review 状态和 assets；新对象保持稳定 ID；源正文、审查、代码、输入和运行报告分开保存。阶段二完成后才能建立阶段三有解释的超图，旧图不能直接导入。该协议与当前清洗规则一致，故把本源留作导航资源。

# 与现有存档的关系和限制

* 本对象补充 `archives/unrelated-machines/README.md` 的一句话存档定位，提供路线级入口和准确量词索引；不复制档内已有定理正文。
* 由于源页的主要内容是链接和研究状态，未将其拆成若干定理文件；各条数学路线的独有证明和实验应继续由对应 canonical 文件承载。
* 入口页没有关闭 `UM-TARGET-v1`，也没有把任何有限实验、局部障碍或条件复杂度桥升级为一般反面。若后续正文与本页状态冲突，以同一冻结版本的自足正文/审查为准，并在对象中记录新版本差异。
* `weighted-congestion` 的源与本页只通过历史路线和工具接口相邻；本对象不把拥塞均衡、正占用核或其它存档的结论迁移到不相关并行机模型。
