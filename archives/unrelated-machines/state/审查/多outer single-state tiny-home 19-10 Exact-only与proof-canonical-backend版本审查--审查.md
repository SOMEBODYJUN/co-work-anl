---
id: "unrelated-machines/multi-outer-single-state-tiny-home-exact-v1-review"
kind: review
type_tag: 审查
title: "多 outer single-state tiny-home 19/10 Exact-only 与 proof/canonical/backend 版本审查"
status: integrated-exact-provenance
truth_status: "exact-only-scope-confirmed; author-proof-read-after-and-finite-backend-separated"
review_level: "full-read-exact-and-author-proof; canonical-independent-read-after-compared"
scope: "UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v1 exact-only candidate, author proof v1, independent/canonical read-after, and finite multi-outer backend"
summary: "8b0284… 的 Exact-only 源定义一个 k 可变、single-state outer、互异 tiny homes 和共享 fallback 资源的 typed 输入域，并只陈述确定性总位多项式 19/10 算法候选。本文完整读取 Exact 与作者 proof，回查已有 independent Exact-first、canonical/read-after 和 two-resource backend 归档；保留 Exact-only 身份、proof read-after 时序、全原 jobs 回填、finite backend 边界和 v1/v4/v5 去重，不把该对象推广为一般 unrelated-machines 算法。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_multiouter_single_state_tiny_home_19_10_exact_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_general_repair_multiouter_single_state_tiny_home_19_10_exact_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_multiouter_single_state_tiny_home_19_10_author_proof_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_general_repair_multiouter_single_state_tiny_home_19_10_author_proof_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_multi_outer_tiny_home_final_canonical_actual_read.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_multi_outer_tiny_home_final_canonical_actual_read.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_multiouter_single_state_tiny_home_19_10_author_read_after.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_multiouter_single_state_tiny_home_19_10_author_read_after.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_multiouter_single_state_tiny_home_19_10_independent_exact_first.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_multiouter_single_state_tiny_home_19_10_independent_exact_first.md"
  - "source:19575b9ed8447b7d0589:evidence/runs/unrelated_machines/multi_outer_request_winner_pair_backend_audit.json"
  - "source:3743fee56233f1e58188:evidence/runs/unrelated_machines/multi_outer_request_winner_pair_backend_root_replay_scope.json"
related_objects:
  - "多outer tiny-home作者证明v1读后与完整算法范围增量--审查.md"
  - "多outer双资源后端与tiny-home算法边界有限审查--审查.md"
  - "全局行基数过滤与多外层单态小home双源审查--审查.md"
  - "归一化菜单福利与CE后端有限审查--审查.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/multi-outer-tiny-home-exact-v1-20261031/original/sol_general_repair_multiouter_single_state_tiny_home_19_10_exact_v1.md"
  - "archives/unrelated-machines/tools/evidence/multi-outer-tiny-home-exact-v1-20261031/original/sol_general_repair_multiouter_single_state_tiny_home_19_10_author_proof_v1.md"
  - "archives/unrelated-machines/tools/evidence/multi-outer-backend-20261030/source-manifest.json"
  - "archives/unrelated-machines/tools/evidence/multi-outer-backend-20261030/backend-rerun.json"
source_sha256: "38c85ffed433edc9742f2e523ae39c820dc315454262a498ff8386b0b6cc001a"
source_size: 3714
---

# 1. 读取范围、身份和版本时序

本轮完整读取 8b0284f9d6749a028120 的 Exact-only 源，3714 字节，SHA-256 为 38c85ffed433edc9742f2e523ae39c820dc315454262a498ff8386b0b6cc001a。Exact 源明确说它只给输入模型和量词，不给作者证明、权重更新、随机实验、方差或去随机化算法；候选不是一般 UM-TARGET-v1，也不声称新颖性。

同一对象的作者 proof 已完整读取，17,024 字节，SHA-256 ce05c7d5fb99d78da44a802578ca33c5ba383b15f6fe0c3a64424ff088c00332。作者稿绑定 Exact 的 hash，并明确在 Exact-first 独立重构之前不提供给 reviewer；因此作者 proof 是 read-after，不应倒写为 statement-first 独立证明。

仓内已有完整审查对象记录了 independent Exact-first、final canonical actual-read 和 author read-after 三份来源；本页核对其 source ID、大小、SHA 与已归档数学摘要，并与本批直接读取的 Exact/author proof 对照。相关 source 元数据为：

| 版本 | ID | 字节数 | SHA-256 | 本页身份 |
|---|---|---:|---|---|
| Exact-only v1 | 8b0284f9d6749a028120 | 3714 | 38c85ffed433edc9742f2e523ae39c820dc315454262a498ff8386b0b6cc001a | 本轮直接完整读取 |
| author proof v1 | e15dcf3e8976443630af | 17024 | ce05c7d5fb99d78da44a802578ca33c5ba383b15f6fe0c3a64424ff088c00332 | 本轮直接完整读取 |
| independent Exact-first | fede89d2e822cbc5b149 | 16573 | c063799d1cfa38db6f05cd14f47bc728136dd6766856e4956f9cbe5570a2549a | 既有独立审查记录 |
| canonical actual read | 5e81cf15c24c42e46e75 | 10456 | 299a27d33a68522b78ee70e8779752df6961b90b0dd5a7c8b4ef8396cadb2d90 | 既有 canonical 读后记录 |
| author read-after | ec1508f77b58b8cf013d | 15209 | 567b9e1153ecfb15b2ff14013a14e52df73a5acefe7585fe2e5652fdfb7483d0 | 既有 proof/canonical 读后记录 |

现有 two-resource backend 的两个 JSON 也已对照其 manifest 和重放记录；它们只覆盖有限 moments/CE 后端，不能替代 Exact、Proof 或全算法证明。

# 2. Exact-only 的精确输入域

## 2.1 typed Q

输入有 k 个 outer groups，k 是显式输入变量，不能视为固定常数。每个 outer O_i 恰有一个 indexed state，其正 home 支持为 homes g_(i,j)，权重 w_(i,j)>0，满足每个 outer 权重和为 1，且最大 home 权重满足

max w_(i,j) <= 1/(4096 k^4)。

所有 home 在物理上互异。每个 home 有且只有一个 helper H_(i,j)，该 helper 的 own indexed state 是 home 上的 unit singleton；其他 indexed states 是共享资源集 B 上显式列出的 normalized 非负有理向量，状态内系数和为 1。helper 可以没有 fallback state，但 own state 始终保留。B 与 homes 不相交，fallback 支持可以跨 helper、跨 outer 任意重叠。

每个 indexed state/resource pair 至多列一个 incidence。零 incidences、重复 fallback state 索引、unused resources 都是输入的一部分并且不能删除；零 incidences 不改变正 home 支持。所有状态和资格都显式列出，没有 succinct state 编码，也不宣称任意菜单可免费归一化到 tiny-home 域。

## 2.2 完整普通 unrelated-machines 矩阵

每个 indexed state 建立独立 private machine，每个资源建立 resource machine。每个 outer 一个原 unit selector，只能在该 outer 的全部 state-private machines 执行；每个 listed incidence 是不可拆 job，在自己的 state-private machine 处理时间为原系数，在指定 resource machine 处理时间为 1，其他单元无穷。全部 selectors、未选 state payload、零 incidence jobs、重复 indexed states 和 unused resources 的 jobs 都要执行。

若 groups、states、listed incidences、resources 数为 G,S,I,U，则完整 P(Q) 有 S+U 台机器、G+I 个 jobs、S+2I 个有限资格单元。算法输入是完整 typed Q；不要求从任意普通 UM 矩阵识别或重构该类型。

## 2.3 Exact 的唯一算法声称

Exact-only 声称存在固定确定性总位多项式算法，仅接收 Q 本身，显式生成完整 P(Q)，输出每枚原 job 在原有限端点上的完整 assignment sigma，并满足

Cmax(sigma) <= (19/10) OPT(P(Q))。

多项式次数是绝对常数，不依赖 k、home 数、fallback 支持宽度、indexed states 数或输入分母的数值。算法不输入 OPT、feasible relaxation 点、actual allocation、联合 law、精度参数或调度 oracle，也不提供精确 SDP oracle。

Exact 允许标准确定性有理 LP 可行性算法。候选实现采用 common primitive-SA1：每个 indexed state 有 binary A，每个 listed incidence 有 binary Z；state partition、boxes、gates Z<=A、resource capacities、state perspective quality 行全部显式生成；每个原线性行与同一 A/Z primitive 及其补相乘，使用一个共同对称二阶数组和 binary diagonal。Exact 只给这一接口合同，不给可行点，也不在本源内证明 SA1、MW、方差或 CE。

# 3. 作者 proof 的实际承重链

作者 proof 先定义互不相交资源 bundles 上各 group 的最大最小值 V，并证明完整普通 UM 的精确桥：

OPT(P(Q)) = 2 − V, 0 <= V <= 1, 1 <= OPT <= 2。

给每组值至少 v 的 disjoint bundles，选每组 attaining indexed state，把该 state 的正 incidence jobs 送到 exact resources，其余 payload、未选 states、zero jobs 和 selectors 留在各自 private machine，得到峰值至多 2−v。反向若完整调度 C<2，则每个 resource machine 至多承载一个 unit incidence，从每组 selector 所在 state 读取 disjoint bundle，值至少 2−C。有限输入保证最大值达到；V=0 时边界也成立。

作者 proof 固定 epsilon=15/16，生成显式 common primitive-SA1 有理 LP。base rows 是 state partitions、boxes、gates、resource capacities 以及每个 state 的 perspective quality sum pZ >= epsilon A；所有原行与同一 primitive 或其补的乘积均保留，X²=X。变量和行数关于显式输入多项式，标准有理 LP 给出不可行或多项式位长可行点。若 V>=epsilon，取达到阈值的真实 state/bundle 作 0/1 赋值，所有 lifted rows 成立，因此 LP 不可行推出 V<15/16。不可行分支的全-private baseline 峰值为 2，且 OPT>17/16，故 2/OPT<32/17<19/10。

可行点提取一阶 alpha、zeta。own singleton 的 gate/quality/box rows 给 E A_j0=E Z_j0；每个 helper 的 fallback mass f_j 至少覆盖其正 home claim x_j。保留正 fallback incidences 后：

- alpha_js >= 0，sum_s alpha_js = f_j <= 1；
- 0 <= zeta_jsu <= alpha_js；
- sum_u p_jsu zeta_jsu >= epsilon alpha_js；
- sum_{j,s} zeta_jsu <= 1。

alpha_js=0 时 gate 强制 zeta_jsu=0，不发生 0/0；丢弃原 zero incidences 只减少资源请求，不改变质量。

每个 helper 独立选择 fallback state 或 empty，选中 state 内的正 incidences 按 zeta/alpha 独立请求。给定 outer 权重 lambda，各资源只在实际请求者中按 lambda_i w_j p_jsu 排序，固定索引破平局；未请求但 state 已选中的 helper不能赢。阈值 CDF 和跨 helper 独立性给 winner oracle 的精确下界：

lambda · g(lambda) >= (5/8) epsilon² = 1125/2048。

候选 winner 的概率是 zeta_jsu 乘以其他 helper 中排在它之前的请求缺失概率；同一 helper 的其他 states 只经一次互斥求和，不被误当作独立 profile。

随后使用 theta=1/8、eta=1/32、N=1024k 的 floored rational multiplicative weights。每轮从 b_i 生成 p_i，再取 lambda=(7/8)p+1/(8k)，计算精确 g_i 并更新 b_i。对数不等式给每个 outer 的轮均值

mu_i >= 757/1792 > 2/5。

每个资源独立均匀选择保存的轮次；helper 的完整 state/request coins 作为一个独立块。条件于 helper profiles，资源 rule 独立，方差至多 delta k；替换一个 helper profile 对任一 outer 的影响至多 16k w_j，Efron–Stein 给整块方差上界。delta=1/(4096k^4) 时：

sum_i Var(W_i) <= 129 delta k^4 <= 129/4096 < 1/25。

固定中心平方势 Psi=sum_i(W_i−mu_i)^2。条件期望依次固定 helper states、正 incidence request coins、resource rounds；每步只在原条件概率为正的选项中选精确 conditional E Psi 最小者。单资源 winner events 与双资源 winner-pair events 足以计算一二阶矩；同一 helper 在两个资源上必须共享同一 selected state，不得独立重抽。所有计算使用显式 state/requester 数和有理公共分母，不列举指数 helper profiles。

最终 Psi<1/25，从而所有 W_i>1/5。取 Good={j:Q_j>=1/10}，由 W_i<=z_i+(1/10)(1−z_i) 得每个 outer 的 Good home weight z_i>1/10。Good helpers 的实际 fallback winner bundles 交给相应 outer，其余 helpers 回 own home；再按原有限端点回填所有 selectors、inactive/duplicate/zero payload 和未选 state jobs，得到 Cmax<=19/10。由于 OPT>=1，输出满足 19/10 相对比。

# 4. Exact、proof、independent/canonical/read-after 的关系

Exact-only 是候选输入合同，不含证明；作者 proof 是随后解封的完整算法证明，且 proof 自述其阅读顺序晚于 independent Exact-first。现有 independent Exact-first 记录从 Exact-only 量词独立重构 typed Q、OPT=2−V、SA1 threshold、winner oracle、MW、整块方差、CE 和 Good 回填；它没有把作者 proof 当作自己的独立依据。canonical actual-read 和 author read-after 记录进一步把 v1 证明接口与当前规范正文、v4/v5 版本和有限 backend 对照。

v1 的窄身份必须保留：

- single-state outer，不能把一个 outer 的多个 indexed states 当作同时可切换的更宽菜单；
- homes 全局物理互异，不能迁移到重合 home；
- 每个 home 必须有 own unit-singleton helper；
- fallback 只在共享 B 资源上，B 与 homes 不交；
- tiny-home 上界是 1/(4096 k^4)，k 是输入变量；
- 全部原 jobs 必须输出，不能只输出正 incidence winners；
- typed Q 显式列出所有状态和资格，不能把指数状态 profile 当作隐式接口。

canonical/read-after 资料还区分 v4 与 v5：v4 是独立新域，允许 B-only exact-threshold UD leaves，k=1 走 greedy，k>=2 的 home 上界改为约 1/(16384k²)；v5 再以 weighted matroid rank、分段 reciprocal 势和 prefix-flow 放宽到约 1/(1024k)。这些扩域不能回写为 v1 proof 的定理，也不表示 finite backend 覆盖了 v4/v5。

# 5. 现有 multiouter backend 的独有内容和有限边界

现有 two-resource backend 的 source-manifest 绑定两个 JSON：

- multi_outer_request_winner_pair_backend_audit.json，ID 19575b9ed8447b7d0589，SHA-256 e7433d8476ab2ae99218b4e0307198d0a586311fc84734b16ff3d6efb985c21d；
- multi_outer_request_winner_pair_backend_root_replay_scope.json，ID 3743fee56233f1e58188，SHA-256 683bf819197f513c428a14bb46ea63f804e96a600bfbebfe807ccf6d70bc03dc。

backend 只测试两个固定小例：3 helpers、2 outers、2 states/helper、2 resources、2 priority rules，精确枚举 2048 和 2916 个 outcomes，核对 moments、二阶 moments、11 步 conditional expectation、平方势不增和最终实际 winner values。重放记录给出第一例最终值 (3/8,1/3)，第二例 (1/8,0)。第二例有一个 outer 的最终值为 0，因为它没有 tiny-home 和 mu_i>2/5 前提；这不是 v1 算法反例。

backend 明确 whole_scheduling_algorithm_checked=false、small_weight_class_instantiated=false；没有运行 common-SA1 LP、N=1024k MW、tiny-home 大输入、完整 CE 复杂度或全部原 jobs 编译。root replay 的代码/输出 hash 和 exit code 只支持有限可复现性，不能视为独立数学证明、端到端实现或外部评审。

# 6. 去重、可用结论和未完成义务

与现有多outer作者 proof read-after 审查重复的内容是 OPT=2−V 桥、SA1 threshold、winner 质量下界、floored MW、整块方差、双资源 CE、Good threshold 和全 jobs 回填；本批不另造第二份算法定理。

本批 Exact-only 的独有记录是：candidate identity、完整 typed 输入量词、k 可变与 tiny-home 绝对界、所有原 job/finite endpoint 计数、SA1 只作为待求 LP 接口、无 OPT/actual oracle 输入、以及明确排除的多state outer、home 重叠、缺 own helper、auxiliary core、非 tiny 输入和一般 UM。

未完成义务包括：从 Q 实现并核验完整 SA1/MW/variance/CE/Good pipeline；在全参数 tiny-home 域证明每一步位复杂度；实现端到端 P(Q) job assignment；以及处理 v4/v5 扩域、多state outer、重合 homes、一般 non-UD 和一般 UM。没有 source hardness、P 不等于 NP、外部新颖性或一般 19/10 近似结论。

# 7. 处置

处置为 integrated-exact-provenance：Exact 原字节和作者 proof 原字节已复制到 evidence；正式正文保留 Exact-only 输入合同、author proof read-after 链、independent/canonical/read-after 版本关系和 finite backend 的有限范围。其正式算法身份仍限于 UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v1；不得把后续 v4/v5、有限 backend 或该 typed 合同外推为一般 unrelated-machines 算法。

