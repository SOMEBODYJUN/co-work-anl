---
id: "unrelated-machines/partial-sum-and-projected-vector-greedy-two-source-review"
kind: "review"
type_tag: "审查"
title: "Partial-sum 与投影向量贪心两源精读"
status: "restricted-escape-and-greedy-barrier-read"
summary: "两源分别确认 flat-menu partial-sum/take-continue 的实际八五逃逸反例（只否所列 AND 拆分规则）与 projected-vector max-norm greedy 的真实最优分布无界障碍（给定分布/顺序）。均保留真实有限任务、正有理与交换边界，不升级一般 UM hardness 或统一算法。"
source_refs:
  - "clean:638d79ce28896fd0ca4e"
  - "clean:cb4cd20a6abe5b669120"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/partial_sum_take_continue_actual_escape_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/projected_vector_greedy_review.md"
---

# 来源与范围

`638d79ce28896fd0ca4e`（SHA `db931ac5488f6a4b9cf453dff4c776e0dab90ce53642556fb2d67a8aa4ac8111`）审 partial-sum/take-continue flat-menu actual escape，并保留原 Exact 命名纠正；`cb4cd20a6abe5b669120`（SHA `f434d0a4eda6292bcb8879389c6a11185fb4f72fe4aa00e726a3769570c3cf74`）审 projected-vector greedy unbounded barrier。两源均 clean show 全文实读，证据与 manifest 在 `archives/unrelated-machines/tools/evidence/partial-projected-vector-20261031/`，receipt 草稿在 `cleanup/workspaces/Boss2/partial-projected-vector-receipts-20261031.json`。

# 1. Partial-sum/take-continue flat-menu escape

该 Claim 只否所列 AND 拆分规则，不否所有 DAG compiler、normalized leaf selector-tree 或一般 source hardness。当前认证范围为 §4–5，实际 Fraction 证书覆盖 30 jobs、26 loads、9 bundles；实现固定证书 audit-only，无 production algorithm。

核心量词是累计 take/continue 路径中一个八五式逃逸：原规则把 partial sums 分拆并持续选择，某些 flat menu 实例存在任意合法调度的下界，迫使路径规则无法保持目标。独立 statement-only 记录与作者 Proof 的读取顺序已纠正：原 misnamed Exact 含完整 Proof，不能充盲审；root另建真正 statement-only 记录后，先核 30-job certificate/任意调度 lower，再读作者源。最终 canonical whole SHA `f740…`，root/审查均核 source order 和唯一范围。

该反例不是最小性、一般 DAG 编译器不可能性或近二 hardness。矩阵由 root 逐57条资格/全部30 jobs/loads/bundles Fraction 核验，未做 E 优化枚举；已有 normalized selector-tree 与一般 UM-TARGET 仍开放。

# 2. Projected-vector greedy 无界障碍

对象 `UM-PROJECTED-VECTOR-GREEDY-UNBOUNDED-v1` 研究从真实最优调度分布 x 的有限任务指示空间构造 max-norm 投影向量并重复贪心。盲重构先锁定三个义务：最终全部任务指示必须在同一空间、投影更新要保持真实有限调度、严格多数必须与事件均值非零同时成立。压缩算子是实际条件化自伴正收缩 `A`，评分差 `〈ψ,(2A−I)ψ〉`；交换所有 A 两两可交换时，生成元子空间乘法封闭，更新等于真实交事件。

正文构造正有理 finite distribution：`Σ_s2^{-s}+kη=1`，所有条件概率在 `(0,1)`；路径 `H_t→C_t` 有严格多数，`C_t→H_{t+1}` 裕度至少 `3η/16`。通过有限复制得到三台机器、全部 finite 正处理时间、每个真实 atomic machine load≤1、unit task 给 OPT≥1，故 actual OPT=1。对于 k 与复制参数，最终向量规则把全部任务指示留在同一空间；输出路径严格选择却可有负载 `>k−1/2`，形成无界 max-norm 近似障碍。该结论只针对给定真实分布和固定 max-norm greedy 顺序，不是所有最优分布或所有算法。

交换边界的正面结论同样重要：若全部压缩算子两两交换，`(A_e²−A_e)1=0` 与生成元 span 给投影；`||(I−Π)M_ef||²=〈f,(A_e−A_e²)f〉=0` 使 V 对乘法封闭，非零状态最终对应一个真实支撑调度，Cmax≤T。该边界不限制重新耦合、换分布、自适应顺序或其它 repair。

有限 exact run 以 Fraction Gram–Schmidt 独立实现，核 12 atoms/323 tasks 的 3-machine 例、k=2…80 公式边界与正数提升恒等；另有 5-machine/120 order 后续汇集证据。有限测试不替代一般无界证明，不声称 k 的多项式输入规模或位多项式算法。

# 3. 关系、纠错和未解义务

两源共同说明“逐步 greedy/partial-sum 规则”可能被真实调度或任务空间的全局耦合击穿，但障碍对象不同：前者是 flat-menu take/continue 规则的局部 escape，后者是 projected-vector max-norm 重置在给定分布/顺序上的无界族。它们不合并成一般 UM hardness，也不否定 direct assignment、actual conditionalization 或其它算法。

本批未认证 production implementation、外部同行评审、全球新颖性或当前六人 SPE 目标。引用时必须保留：partial-sum 只否所列 AND 拆分；projected-vector 只对给定真实 optimal distribution/固定顺序；所有 finite/正有理/同一任务空间和交换假设。处置为 `restricted-escape-and-greedy-barrier-read`。
