---
id: "unrelated-machines/seven-state-star-global-quadratic-audit-scope-review"
kind: "review"
type_tag: "审查"
title: "七态星全局二次审计与root重放范围审查"
status: "historical-reviews-reconciled"
summary: "逐字段核对七态星12参数Fraction审计及root fresh-output范围，确认三组完整small矩阵、九组局部检查、作者/root字节一致性和明确未查软件；不把有限结果扩为任意维度定理或递归接线。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/seven_state_star_global_quadratic_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/seven_state_star_global_quadratic_root_replay_scope.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/seven_state_star_global_quadratic_and_extension_boundaries.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/seven_state_star_global_quadratic_and_extension_boundary_review.md"
---

# 七态星全局二次审计与 root 重放范围审查

本轮完整读取两个 claimed evidence/runs JSON，并对照全仓已有七态星主源及最终范围审查。两份 JSON 的 clean-show 原文哈希分别为：

- 审计输出 6210 字节，SHA256 9be19dec14e2abdb97377175372f63cbe47c08414e52516de5cc65cd74599335；
- root 重放范围 1985 字节，SHA256 365f4b15b962accb5a88626708136e0873a6012480c6d1dff1e7ca3d10357b07。

主源主 Claim 已另行限定为实际 OPT=1 的七态星局部核；本审查不把 evidence/runs 重新登记为主定理，也不把它们当作未读代码的替代品。

## 1. 审计字段与精确结果

第一份 JSON 的12组参数是
\[
(4,2),(8,2),(8,4),(16,2),(16,4),(16,8),
(64,2),(64,16),(64,32),(1000,2),(1000,100),(1000,500).
\]
各组使用 \(\eta=s/d\)、\(p=\eta^3/1000\)，并报告原星机器数 \(d+2\)、原 jobs 数 \(d+1\)、有限资格条目 \(2(d+1)\) 以及所有原 jobs 回到唯一 home 的 actual OPT=1 调度。

全部12组均有：

- row CFG first/pair exact；
- 5维 symmetric signed-slack rank=5、exact PSD；
- exact fractions.Fraction、Boolean monomial basis、无 pivot PSD 消元；
- 记录的 assignment states 与 degree≤6 true moments 字段。

仅前三组有完整 high-dimensional 矩阵：

| 参数 | full M3 | global q2 | assignment states | degree≤6 moments |
| --- | ---: | ---: | ---: | ---: |
| \((4,2)\) | 26维、秩18 | 16维、秩16 | 18 | 32 |
| \((8,2)\) | 130维、秩76 | 46维、秩46 | 90 | 466 |
| \((8,4)\) | 130维、秩116 | 46维、秩46 | 130 | 466 |

后九组只有5维 signed-slack、row CFG和home assignment等字段，不能把 JSON 中缺失的 full M3/global q2 当作已检查。

## 2. 与主源解析合同的逐点关系

七态主源解析合同对任意偶 \(d,s\) 讨论同一真实 assignment law、共同 M3、全部 global degree-two load localizers和逐行 CONFIG first/pair。审计有限结果与这些字段相容：

- 机器与原 jobs 的计数吻合 \(d+2\)、\(d+1\)；
- home assignment 给 actual OPT=1，坏样本质量 \(p\) 不改变该实际下界；
- signed-slack PSD 只记录有限矩阵的 exact PSD，不是新的 SDP finder；
- full M3/global q2 的三组秩值与主源所述 small 参数范围一致；
- row CFG first/pair 是逐行证书，不是把所有行拼成另一共同 assignment law。

主源另有稀疏 first/pair 支持、仿射 Boolean owner 和忠实 AND localizer 三个边界身份。审计 JSON 没有执行这些软件、没有测试新增 payload、shared owner 或 growing-depth 接线，因此相关解析边界仍以主源正文和既有审查的量词为准。

## 3. root 重放的准确可认证内容

第二份 JSON 给出代码路径、代码 SHA256
86d05b9013dda128a753f610eaeb9eec4146212c34fa9afcd2bbea3ccab382bd，
实际命令、exit_code=0、fresh output SHA256
9be19dec14e2abdb97377175372f63cbe47c08414e52516de5cc65cd74599335，
以及 author_output_byte_identical=true。

因此可认证的事件是：记录中的一次 fresh exact CLI 输出与作者输出逐字节相同，且精度配置是 Fraction、Boolean monomial basis、exact no-pivot PSD elimination。root 参数清单与审计 JSON 的12组一致。

这不认证：

- 任意未列 \((d,s)\) 的高维矩阵；
- 未附带的审计源码内容或运行环境；
- sparse-support、affine、AND、deep shared-owner 或 general scheduling 软件；
- SDP finder；
- 递归共同 law、near-two gap、hardness 或一般 UM 算法。

## 4. “有限反例”与“可推广结论”的分界

这两个 JSON 不是反例：每组都报告实际 home assignment 的 OPT=1，PSD/CFG 通过也没有给出峰值大于1的完整调度障碍。它们也不是新的全称定理：12个参数和3组完整矩阵不能代替主源对任意 \(d,s\) 的解析证明。

可以安全复用的有限结论只有：

- 指定12组参数上，exact PSD、row CFG和报告的 moment/assignment 字段通过；
- 指定前三组上，full M3和global q2矩阵维数、秩和PSD结果如表；
- root fresh output 与 author output 字节一致；
- 代码 hash、输出 hash、命令和未检查清单按 JSON 固定。

不应复用为：

- growing-depth shared-owner common law；
- 任意 child payload 或 merged machine 的局部负载成立；
- 将有限 signed-slack 结果解释为 relaxation integrality gap；
- 任何 NP/UGC/GapETH hardness；
- 一般 unrelated-machines 调度器或 SDP 求解器。

## 5. 全仓版本关系与历史读序

全仓 canonical 与审查记录把四个精确身份分开：全局 quadratic local、uniform cardinality pair-sparse support、affine Boolean owner boundary、忠实 AND localizer obstruction。历史 Exact-first、作者 Proof、最终正文 read-after 和 root 软件重放各有独立 scope；本轮只读取当前 claimed JSON 及既有 canonical/review 的可用范围摘要，不把历史执行者的独立性改写为本轮新盲审。

主源最终正文已明确：新增 payload 会消耗各行 slack；共享 owner、不同机器合并和 AND 接线需单独核全部 jobs、pair与共同 law。证据 JSON 不能覆盖这些接口，也不能把 root 的一次 fresh CLI 等同于完整软件实现。

## 6. 保留结论

本轮审查无数据字段冲突或 hash 不一致。两份 evidence/runs 可以作为七态星局部核的有限实现证据和 root 输出一致性记录；主源解析证明、边界条件、有限审计和未检查软件必须保持四层分离。当前仍开放任意 growing-depth 连接、共享 owner 的统一 law、全部机器共同低载 decoder、一般 UM 目标和任何 near-two hardness。
