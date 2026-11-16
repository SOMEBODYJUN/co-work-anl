# 第三阶段收尾复核：数学依据、精确勘误与最终图谱

身份：Boss7。日期：2026-11-16。工作分支：`rebuild/research-v2`；公屏：`wcg/board-map-v2`。

## 当前交付状态

**全仓现役第三阶段构图任务、覆盖与整合已完成，原生最终检查和构建均通过。** 最新采用的正式整合为 `fe43decf02ac2d6090dc486d4f15eb7ff3b7435b`；两项最后交付 3313 与 7383 已按正式收据进入现行总图。Boss7 保留了同行所有有效审读，并把完整 m 槽纯门槛与已否的 m−1 槽门槛作了最小消歧。没有新增未领、执行中、阻塞或待整合的已知工作。

| 验收项 | 最终结果 |
| --- | ---: |
| 当前任务总记录 | 1,050 |
| 历史 done / withdrawn | 935 / 115 |
| 仍有效 done / 已整合批次 | 680 / 680 |
| available / claimed / blocked / handoff / pending integration | 全部 0 |
| 现役对象 / 登记材料 | 3,821 / 5,137 |
| 已连边 / 经比较保留孤立的覆盖 | 2,656 / 1,165 |
| 关系记录总数 | 2,673 |
| accepted / proposed / rejected | 2,667 / 5 / 1 |
| 最终图文件 | 21（根图及 20 个存档、子档投影） |
| 未登记材料 / 待定材料 | 0 / 0 |

935 个历史 done 中，255 个已由后继替代；最终有效集合为 680，未把历史重复计成新增成果。经比较保留孤立是完整的覆盖判定，不是未读或待决；相应理由仍在各对象 coverage。5 个 proposed 和 1 个 rejected 保留其记录及证据范围，发布图只收录 2,667 个 accepted 关系。开放数学命题保留自己的状态；图谱任务完成不意味着这些命题获得证明。

实际验收输出为 [final-check.json](final-check.json)、[final-build.json](final-build.json) 和 [final-map-status.json](final-map-status.json)；完整计数、全部 21 个投影路径及 SHA、canonical 指纹和范围说明见 [final-acceptance.json](final-acceptance.json)。最后两批的精确采用与文字消歧见 [final-delivery-adoption-review.json](final-delivery-adoption-review.json)。原生 build 输出的 `publication: local-not-pushed` 是生成动作当时的记录；随后 checkpoint 的实际 pushed 回执与公屏最终提交负责确认发布。

本目录其它审读报告保留各自的真实读取快照；其中当时的 claimed、尚待 canonical 等措辞属于该次审读时点，当前总状态以本节及最终验收文件为准。成熟旧成果按其原审读和当前精确资产继承，本轮没有冒称重新证明全部 3,821 个对象。

## 本轮实际完成的数学复核

| 问题 | 得到的结论与精确边界 | 完整审读记录 |
| --- | --- | --- |
| 静态补覆盖怎样迁移同动作合谋的全局势保证 | 补覆盖只给收益、费用和势差的恒等式。完整结论还要联合独立的 Shapley 同动作不等式。静态偏离的对应不能直接替代完整序贯策略的对应。 | [补覆盖与联合前提](wc-complement-review.md) |
| SUMmin 怎样支付六人 half | 对同一完整 SPE、同一个混合查询分布的共同预算若成立，则 `OPT_m ≤ 2m v_(m+1)(0) ≤ 2m M_path ≤ 2W`；取 m=6 得完整条件结论。共同预算本身仍开放。二元尾利润的聚合上界只是一项局部贡献，不提供 route5 的逐动作净需求下界。 | [SUMmin 与二元尾利润](cag-joint-review.md) |
| 裸 Cartesian 族怎样经过正规形迁移 | 对每个 t≥1，完整实际矩阵满足 `V=1−2^(−t)`、`OPT=1+2^(−t)`；联合已证的选择树和路径保值桥，得到三态、资源组度三的同值族。该后果不恢复裸乘积丢掉的 NO 间隙，也不产生一般 UM 困难源。 | [实际任务与正规形迁移](um-transfer-review.md) |
| 局部配对何时能给出原机器的实际调度 | 给定的全部 pair 若有同一个全机延拓，逐任务重数几乎处处为 0/1 且期望为 1，故每个原任务恰一次。反向只保证存在一份 Dirac 见证；可调度不保证任意指定配对可延拓。容量一星族的实际 `OPT=2−1/k` 排除 T=1 的全局延拓。 | [分组配置全局耦合](cross-glue-review.md) |

以下两组也已完成独立数学审读，并按各自实际范围接入本轮整合：

- **聚合末位保底反例与 SUMmin。** [36 客户固定策略](summin-36-budget-review.md) 对所有混合查询均有 `ΣR_i(p)≤57/2<34=W`。原 `K=6M+4`、`2n` 标签的[正编译输入族](summin-alln-budget-review.md) 对每个 `n≥3`、该输入的每份完整纯 SPE、每个混合查询分布都有 `ΣR_i(p)<W`。后一量词通过完整历史 fresh 编译桥支付；共同前提需要一条 ALL 关系。这两类对较强阈值的反例没有切断 SUMmin 路线，但都只是原候选的局部贡献。
- **NSW 的同一输出和实际 flat-UM 后果。** [现行 NSW 义务复核](nsw-current-obligation-review.md) 直接核了 B1–B6 及 C/D/E：显式无权 XOS 后端先固定实际输出，再对 H 上全部比较双射及所有正有限有理分数 benchmark 成立。原 norm1 显式菜单加正 support unit-FSLP 可行性，支付 almost-all 质量、准确共享 REPAIR promise 的 LP 判定与全部原 jobs 的 makespan≤2；它不支付任意 source 的保真正规化或全机器统一 `2−ε`。

这些审读分别核对了原陈述、模型、量词、必要证明、证据绑定及反例的否定对象。此前有效且没有变化的包仍按其原审读和精确资产 SHA 继承；本轮没有声称重新证明全仓所有对象。

## 两项最后交付的实际数学

### 全部完整 SPE 的联合局部预算

正式边 `boss5-all-spe-summin-budget-7383c8bf44f753cc` 由 **{`CA-AGGREGATE-LAST-FLOOR-NO`, `CA-MOBIUS-FULL-HISTORY-EMBED`}** 一条 ALL 支持，`accepted / unconditional / contribution`。原 \(K=6M+4\) 正编译输入的每份完整 SPE 都在全部有序重复历史上 fresh；较大 K 的参数桥用 \(K/2-2M=M+2>0\) 明确支付。任意 distinct 实际叶的 signed 福利至少 n−1，未用查询的 signed 价为 \(-F(Z)\)，已用查询严格较小，于是对每个同一 \(p\)

\[
\sum_iR_i(p)\le n[K\beta_n-F(Z)]\le nK\beta_n<W(\sigma),
\qquad W(\sigma)\ge KC+n-1.
\]

一般 \(\sigma\) 不沿用源展示策略的固定路径或福利等式。Boss3 d86 的指定策略结果及原资产完整保留。新关系只扩大同一明确输入族的策略量词，不解决一般 SUMmin 或一般六人 half。[实际正式边、两份证明和收据终审](all-spe-formal-delivery-review.md) 独立核了全部输入、证据、覆盖及三对象对处置。

### uniform 与 SUMmin 的完整双向身份

正式边 `boss3-uniform-summin-full-budget-equivalence-3313f41b4a46c9dc` 为 `accepted / equivalent_to / conditional / whole_result`。同一完整策略、actual 前缀、完整 m 槽和同一独立查询 \(p\) 下，每列有限求和给 \(\mathbb E_pK_i(T,A)=G_p(Z_i(A))\)，所以 \(R_i(p)=\psi_i(p)\)。两个完整全称预算双向等价；两端仍 open，未发生 \(\min\)/期望交换或候选真值升级。

精确金额对应为：SUMmin 的 \(L_i\) 是带查询边际的删槽折扣 \(\Delta_i\)，uniform 的 \(L_i\) 是重新选列收益 \(G_i\)，协方差自身税不带查询边际。桥是 \(D_i-C_i^{full}=\kappa_i+\Delta_i=\sum_x\operatorname{Cov}_i+\tau_i^{self}\)。既有末两位贡献据此重写，恰六人仍欠前四行共同债；末位两种储备只取 max，不重复计费。详见 [正式身份关系及尾路线终审](uniform-formal-delivery-review.md)。

[阈值前沿辨析](threshold-frontier-disambiguation.md) 还闭合了一个易误读的比较：已否的是 m−1 槽 \(W\ge m\theta_m\)，仍 open 的 `M-8f66f1abb0374762883f01d13235901c` 使用完整 m 槽 \(\theta_{m+1}\)。原正编译反族的每份完整 SPE 反而满足 \(n\theta_{n+1}\le n\max_aK(a,z)\le nK\beta_n<W\)。它是同列证明的直接后果，不另起重复任务或新边，也不求 \(\theta\) 的最优值。

## 一处证据记号的最小勘误

在独立实际稀疏审计的 §2，把任意完整状态的支持恢复为

\[
b_i+g_i a_i=\ell_i\pmod 2.
\]

冻结原文同处本来就是 `ell_i`。原清洗稿多出的 `(g_i)` 容易把任意完整状态误读成逐坐标选态约束。循环达界见证另取 `ell_i(g)=g_(i+1)`；它一般依赖别的组坐标。主文、一般证明、有限输出及数学真值都没有改变。

只有 `UM-NORMALIZED-FLAT-CARTESIAN-TENSOR-REVERSE-AMPLIFICATION-v1` 的附属证据登记从 v2 升至 v3；主文 SHA 保持不变。完整变动见 [最小勘误记录](tensor-audit-notation-erratum.json)。该记录的 `registered-local-not-pushed` 是创建时的历史状态；随后源码与登记已一并推送，提交为 `e0dd8c6e28a0ff3b30dcd695f5aed2620f059964`。旧 baseline 与冻结原件保留原字节。

首轮 [UM 迁移审读](um-transfer-review.md) 记录的是发现问题时的 v2 快照；下面四份正式替代收据负责现行 v3 输入，不回写历史审读以伪装成同一版本。

| 定向替代任务 | 实际作用 |
| --- | --- |
| `boss7-tensor-notation-repair-0bde5bd3570dc738` | 复核 free 值与逐坐标配额的联合修复障碍，以及裸族与正规形的 ALL 迁移；替代两条边，其余九项原资产保持。 |
| `boss7-tensor-notation-repair-eb8c557dc1ec6c43` | 复核全坐标单块特化和完整原任务审计；替代两条边，其余十八项原资产保持。 |
| `boss7-tensor-notation-repair-f484c80799f20359` | 比较裸菜单乘积与完整处理矩阵 Kronecker 积；十二项旧资产按原 SHA 保留，不新造逻辑边。 |
| `boss7-tensor-notation-repair-b77a4277b54f13f4` | 复核选择树及资源路径的真实任务双向合同，含 `OPT=2`、`V=0` 边界；四项旧资产按原 SHA 保留。 |

每包的新说明位于 `map/edges/<任务ID>/source-delta-review.md`，完整 coverage、输入版本和逐资产 supersession 位于 `map/receipts/<任务ID>.json`。

第四包 `b77` 的 task definition 和 source-delta 已用 v3，但冗余顶层 `input_pins` 漏保了旧 A 指纹。Boss5 的 `boss5-cartesian-receipt-repair-01720ef708fa6bdb` 已按定向替代流程修复、正式 done 并整合。新收据的 18 个输入全部 current；五项资产保持原 SHA，15 核心仍为 7 linked、8 isolated-after-review，coverage 与既有比较逐项不变。详见 [后继收据及数学实读](cartesian-receipt-successor-review.json) 与 [实际整合接入](cartesian-adoption-merge-review.json)。旧 b77 收据保留历史字节，未变的数学不撤回。

## 已完成工作与真正开放义务的区分

[工作流历史核对](workflow-obligation-audit.json)、[CA 六组历史后继](ca-historical-workflow-audit.json) 及 [Wave20 精确复核](ca-wave20-workflow-tail-review.md) 追到现行正式收据和有效资产，再清理过时的“尚待交付”文字。撤销批按 withdrawn 记录，不伪写成 done。旧稿的待办句不覆盖现行证明与收据。

Wave20 的 T/35 证明适用于指定四人六标签完整策略的整个非负客户锥；root A 的同后继等锥与其他五根分开，mask49 的根 B 真实遗憾为 1/4。两份 230 分别优化 FREE 的 \(O_J\) 与付费的 \(O_J-3\Delta\)，不合并成一个目标。上述交付的完成不支付一般 full-tax、共同查询预算或序贯 half。

NSW 的 R50 已按现行 v6 收窄：先固定同一实际输出，再量化 H 上全部比较双射及所有正有限有理 benchmark 的保证已付；原 norm1 显式菜单的 C/D/E 后果已付。一般原输入的保真接口、例外根的共同容量修复及全机固定改善仍保留。

## 有限计算的实际责任

- [CAG 精确检查](cag-joint-exact-check.json)：q=2,…,6 的 14,774 个重数向量，配三组参数，共 44,322 个参数/向量组合。核固定根尾利润的最大值和全部取等支持，没有枚举全部完整 SPE，也没有证明普遍 SUMmin。
- [UM 完整任务检查](um-transfer-finite-check.json)：从 16 份冻结 raw 文件重构 t=1,…,4 的全部任务、合法端、时间及见证负载，核 4,680 个补组交点；仅 t=1 穷举 1,024 份完整实际分配求最优值。t=2,3,4 是见证检查，一般最优值由解析证明承担。
- 全局耦合审读还用 exact Fraction 核容量一星族 k=2,3,4 的全部机器对。一般 `OPT=2−1/k` 由独立下上界证明承担，不由程序返回的公式字段承担。

相应可重放程序与原始输出均保存在本目录；没有把有限计算、程序绑定或最终结构检查提升为自动数学认证。

## 沿图继续研究

主入口是 [全图](../../../../../map/graph-v2.json)、[对象登记](../../../../../research/registry.json)、[覆盖判定](../../../../../map/coverage.json) 和 [跨包整合记录](../../../../../map/integration.json)。各存档及最深子档还有自身 `map/graph-v2.json` 投影，保留关系所需的外部端点。

本轮另外整理了三份可直接供后续 Main / Solver 阅读的入口：[客户吸引](ca-research-entry.md)、[不相关机器](um-research-entry.md)、[静态补覆盖迁移](wc-research-entry.md)。入口把原题与定义、独立障碍、可复用成果、真实共同前提和下一项数学责任放在一起；不会启动旧研究系统，也不替后续研究者预先选定未证路线。

从原题或候选对象 ID 出发，先读其完整陈述与 truth status，再读取相关边的 `source_ids`、`premises_mode`、`conditions` 和 `roles`。一条 ALL 边的全部前提需要同时满足；独立路线按不同边判断。`whole_result` 表示边支付的整条目标，`contribution.result/remaining` 分开记录已完成步骤与目标欠账；`relation_mode:conditional` 保留开放前提，`context` 不构成证明。反例应按实际否定目标使用，有限 checks 应按其参数域使用。

仍需继续研究的数学义务包括：同一完整 SPE 与同一混合查询分布的 SUMmin 共同预算、六人一般目录的普遍 half、route5 的逐动作净需求付款、普通矩阵内真正的一致性或困难源、由局部配置证书构造指定全局延拓的有效算法，以及其它对象已明确保留的开放前提。正规形保值、有限证书和局部比较均不替代这些证明。
