---
id: customer-attraction/r-2fc-aggregate-security-mid-eight-source-ledger
kind: resource
type_tag: 资源
title: R-2fc 聚合安全中段八源诊断
status: eight-sources-read; enlarged-model-floating-diagnostics-retained; not-CAG
truth_status: finite source ledger only; no CAG certificate; no six-person half conclusion
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_n5k3.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_potential_probe.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/individual_groups_n3k6.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/individual_plateau_n3k4.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/monotone_n3k3.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/monotone_n4k4.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/monotone_policy_n3k5.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/monotone_policy_n4k4.json
related_objects:
  - ../资源/扩大DR聚合安全十源诊断清单--资源.md
  - ../计算/DR聚合安全六份浮点诊断--计算.md
  - ../障碍/单调递减边际势的强安全聚合障碍--障碍.md
evidence_packet: ../../tools/evidence/R-2fc-aggregate-security-mid-20261031/
---

# 读取范围与比较结果

这八个冻结路径来自同一个 `aggregate_security` 目录。`cleanup.py show` 逐项尝试过；当前 clone 的 promisor remote 无法连接 browser-proxy，八项均退出 1，stdout 为空，具体错误和 blob id 保存在证据包 `clean-show/`。随后逐一打开对应 GitHub raw URL 读取完整正文，并把字段、大小、blob 和 SHA-256 与冻结 inventory 对照。两个登记提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 对每条路径给出相同 blob；这是同一路径的版本副本，不改变本次八个 source version 的处置。

所有 JSON 顶层都写着 `floating diagnostic in an enlarged model, not CAG evidence`。脚本的模块说明也直接限定为一般 DR 边际势扩大模型，使用 numpy/scipy `linprog`，没有把输入宣称为 customer-attraction。既有精确锚点《单调递减边际势的强安全聚合障碍》仍是 `P=161`、`v=56`、路径 `[0,3,4]` 的扩大模型有理证书；其 support 预算冲突说明该锚点不具 CAG 客户实现。中段八源没有加入客户类型、均分预算、support 不变总收益、有理化势表、全策略量词或新的 CAG 证书。

# 八源读数与处置

| source | 原文读数 | 与已有对象的关系 | 处置 |
|---|---|---|---|
| `b5868d5b6d047171afcb` / `dr_n5k3.json` | `k=3,n=5,trials=500,seed=22103`，`best_objective=0.0`，`completed=500`。 | 只新增五人、三动作的有限随机汇总；没有 witness 或 exact table。 | `retained` |
| `d4f16fe38986277d7ce7` / `dr_potential_probe.py` | 7799 字节；一般 DR 潜势浮点 LP 入口，显式 `not` customer-attraction。精确源字节 SHA-256 `fa9b84b296ae2c80eb126b9e7ed06bcea2a3011e887816402c8b6bcc1a75015f`。 | 与旧十源/六源对象使用同一扩大入口，但本次把源码逐字节保存到 evidence 并实际运行有限命令，补足可复核入口。 | `integrated` 到中段计算对象 |
| `140e0efe501815fbb2df` / `individual_groups_n3k6.json` | `k=6,n=3,trials=1,seed=22112,policy=groups,first=1`；`best_objective=-0.002645502645502644`；root `[0,3,4]`；`p≈(0,.25,.25,.25,.25,0)`；`value_lower≈.0026455`、`welfare=0`。 | 与已有 `first=0` groups 诊断同 root 但预算只取首位；负值为固定策略/固定 query 的浮点近零，不是有理反例。 | `retained` |
| `f6c01a389ec2b00b8bd4` / `individual_plateau_n3k4.json` | `k=4,n=3,trials=200,seed=22111,no_dr=true,policy=plateau,first=1`；`best_objective=0.0`；`completed=200`。 | 与 groups/monotone 入口相同的有限程序，关闭 DR 且只看首位；没有 CAG 语义。 | `retained` |
| `438b38ee10dea3418acf` / `monotone_n3k3.json` | `k=3,n=3,trials=100,seed=22104,no_dr=true`；`best_objective=0.0`；`completed=100`。 | 仅随机/单调诊断摘要；零值不是全称安全性。 | `retained` |
| `7f861b14d37a2154f0a7` / `monotone_n4k4.json` | `k=4,n=4,trials=500,seed=22105,no_dr=true`；`best_objective=0.0`；`completed=500`。 | 与上项仅人数/动作不同；无精确策略树或客户预算。 | `retained` |
| `402c8867973f4b6e276e` / `monotone_policy_n3k5.json` | `k=5,n=3,trials=1000,seed=22107,no_dr=true,policy=monotone`；`best_objective=0.0`；`completed=1000`。 | policy 生成器和有限试验计数是新增元数据；不是 CAG 单调策略定理。 | `retained` |
| `9ae6d4ae302f52483a13` / `monotone_policy_n4k4.json` | `k=4,n=4,trials=100,seed=22106,no_dr=true,policy=monotone`；`best_objective=0.0`；`completed=100`。 | 与上项同入口但不同 n/k；没有额外 exact witness。 | `retained` |

# 必须保留的边界

`best_objective<0` 只代表固定 policy、fixed first budget、有限浮点 LP 的读数；`best_objective=0.0` 只说明给定 seed/trials 的运行未写出负值。它们都没有符号等式意义，不能升级为 CAG 反例，也不能升级为六人 half 结论。`no_dr=true`、`policy=plateau` 或 `policy=monotone` 只是程序开关；`first=1` 也不是全体玩家的聚合量词。任何后续复用都必须回到已有有理 `P=161,v=56` 扩大模型证书，并重新提供合法共同客户、support 预算和完整历史偏离证书。
