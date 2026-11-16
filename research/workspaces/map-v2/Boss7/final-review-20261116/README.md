# 第三阶段收尾复核：数学依据、精确勘误与最终图谱

身份：Boss7。日期：2026-11-16。工作分支：`rebuild/research-v2`；公屏：`wcg/board-map-v2`。

## 当前交付状态

本轮四个 Cartesian v3 定向替代包已全部 pushed、done，并按精确收据 pin 完成整合。当前继续跟进 Boss3 的 SUMmin 两项局部预算比较，以及 Boss5 对第四包冗余 input_pins 的定向元数据后继；它们完成并纳入最新图后再执行最终检查。本段将在原生 `map status`、`research check --final` 和 `research build --final` 的最新回执产生后更新。开放数学命题保留自己的状态；图谱任务的完成不意味着这些命题获得证明。

## 本轮实际完成的数学复核

| 问题 | 得到的结论与精确边界 | 完整审读记录 |
| --- | --- | --- |
| 静态补覆盖怎样迁移同动作合谋的全局势保证 | 补覆盖只给收益、费用和势差的恒等式。完整结论还要联合独立的 Shapley 同动作不等式。静态偏离的对应不能直接替代完整序贯策略的对应。 | [补覆盖与联合前提](wc-complement-review.md) |
| SUMmin 怎样支付六人 half | 对同一完整 SPE、同一个混合查询分布的共同预算若成立，则 `OPT_m ≤ 2m v_(m+1)(0) ≤ 2m M_path ≤ 2W`；取 m=6 得完整条件结论。共同预算本身仍开放。二元尾利润的聚合上界只是一项局部贡献，不提供 route5 的逐动作净需求下界。 | [SUMmin 与二元尾利润](cag-joint-review.md) |
| 裸 Cartesian 族怎样经过正规形迁移 | 对每个 t≥1，完整实际矩阵满足 `V=1−2^(−t)`、`OPT=1+2^(−t)`；联合已证的选择树和路径保值桥，得到三态、资源组度三的同值族。该后果不恢复裸乘积丢掉的 NO 间隙，也不产生一般 UM 困难源。 | [实际任务与正规形迁移](um-transfer-review.md) |
| 局部配对何时能给出原机器的实际调度 | 给定的全部 pair 若有同一个全机延拓，逐任务重数几乎处处为 0/1 且期望为 1，故每个原任务恰一次。反向只保证存在一份 Dirac 见证；可调度不保证任意指定配对可延拓。容量一星族的实际 `OPT=2−1/k` 排除 T=1 的全局延拓。 | [分组配置全局耦合](cross-glue-review.md) |

另两组当前比较也已完成独立数学审读，正式关系和整合由现有任务负责人承接：

- **聚合末位保底反例与 SUMmin。** [36 客户固定策略](summin-36-budget-review.md) 对所有混合查询均有 `ΣR_i(p)≤57/2<34=W`。原 `K=6M+4`、`2n` 标签的[正编译输入族](summin-alln-budget-review.md) 对每个 `n≥3`、该输入的每份完整纯 SPE、每个混合查询分布都有 `ΣR_i(p)<W`。后一量词通过完整历史 fresh 编译桥支付；共同前提需要一条 ALL 关系。这两类对较强阈值的反例没有切断 SUMmin 路线，但都只是原候选的局部贡献。
- **NSW 的同一输出和实际 flat-UM 后果。** [现行 NSW 义务复核](nsw-current-obligation-review.md) 直接核了 B1–B6 及 C/D/E：显式无权 XOS 后端先固定实际输出，再对 H 上全部比较双射及所有正有限有理分数 benchmark 成立。原 norm1 显式菜单加正 support unit-FSLP 可行性，支付 almost-all 质量、准确共享 REPAIR promise 的 LP 判定与全部原 jobs 的 makespan≤2；它不支付任意 source 的保真正规化或全机器统一 `2−ε`。

这些审读分别核对了原陈述、模型、量词、必要证明、证据绑定及反例的否定对象。此前有效且没有变化的包仍按其原审读和精确资产 SHA 继承；本轮没有声称重新证明全仓所有对象。

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

第四包 `b77` 的 task definition 和 source-delta 已用 v3，但冗余顶层 `input_pins` 漏保了旧 A 指纹。该记录矛盾已经确认，Boss5 的 `boss5-cartesian-receipt-repair-01720ef708fa6bdb` 正按定向替代流程修复，并保留五项已有资产的原 SHA。此处不将元数据遗漏隐去，也不撤回未变的数学。

## 有限计算的实际责任

- [CAG 精确检查](cag-joint-exact-check.json)：q=2,…,6 的 14,774 个重数向量，配三组参数，共 44,322 个参数/向量组合。核固定根尾利润的最大值和全部取等支持，没有枚举全部完整 SPE，也没有证明普遍 SUMmin。
- [UM 完整任务检查](um-transfer-finite-check.json)：从 16 份冻结 raw 文件重构 t=1,…,4 的全部任务、合法端、时间及见证负载，核 4,680 个补组交点；仅 t=1 穷举 1,024 份完整实际分配求最优值。t=2,3,4 是见证检查，一般最优值由解析证明承担。
- 全局耦合审读还用 exact Fraction 核容量一星族 k=2,3,4 的全部机器对。一般 `OPT=2−1/k` 由独立下上界证明承担，不由程序返回的公式字段承担。

相应可重放程序与原始输出均保存在本目录；没有把有限计算、程序绑定或最终结构检查提升为自动数学认证。

## 沿图继续研究

主入口是 [全图](../../../../../map/graph-v2.json)、[对象登记](../../../../../research/registry.json)、[覆盖判定](../../../../../map/coverage.json) 和 [跨包整合记录](../../../../../map/integration.json)。各存档及最深子档还有自身 `map/graph-v2.json` 投影，保留关系所需的外部端点。

从原题或候选对象 ID 出发，先读其完整陈述与 truth status，再读取相关边的 `source_ids`、`premises_mode`、`conditions` 和 `roles`。一条 ALL 边的全部前提需要同时满足；独立路线按不同边判断。`whole_result` 表示边支付的整条目标，`contribution.result/remaining` 分开记录已完成步骤与目标欠账；`relation_mode:conditional` 保留开放前提，`context` 不构成证明。反例应按实际否定目标使用，有限 checks 应按其参数域使用。

仍需继续研究的数学义务包括：同一完整 SPE 与同一混合查询分布的 SUMmin 共同预算、六人一般目录的普遍 half、route5 的逐动作净需求付款、普通矩阵内真正的一致性或困难源、由局部配置证书构造指定全局延拓的有效算法，以及其它对象已明确保留的开放前提。正规形保值、有限证书和局部比较均不替代这些证明。
