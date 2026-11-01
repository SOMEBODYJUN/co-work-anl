---
id: customer-attraction/dr-aggregate-security-pair-floating-diagnostics
kind: computation
type_tag: 计算
title: DR聚合安全配对浮点诊断
topic: customer-attraction
status: 有限浮点诊断；扩大模型；不是CAG证据
truth_status: finite floating diagnostics only; exact verifier is a separate enlarged-model certificate
review_level: raw-browser-read-and-independent-verifier-rerun
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/pair_groups_dr_n3k6.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/pair_groups_monotone_n3k6.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/pair_monotone_policy_n4k4.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/pair_plateau_n3k4.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/verify_dr_boundary.py
  - local:archives/customer-attraction/state/障碍/单调递减边际势的强安全聚合障碍--障碍.md
  - local:archives/customer-attraction/state/计算/DR聚合安全六份浮点诊断--计算.md
evidence_packet: archives/customer-attraction/tools/evidence/R-2fc-aggregate-security-pair-20261031/
---

# DR 聚合安全配对浮点诊断

这四份 JSON 与 `verify_dr_boundary.py` 属于同一 `R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security` 入口。四份 JSON 的顶层状态逐字都是 `floating diagnostic in an enlarged model, not CAG evidence`。它们只报告固定参数、固定随机种子和有限试验的浮点搜索；没有客户类型、support 不变的总收益预算、单位客户均分、合法 CAG 实例或全量有理证书。负的 `best_objective` 是该扩大模型一次浮点目标值，不能升级为 CAG 反例；`0.0` 是有限运行的结果，也不能解释为不存在负点。

## 四个源版本的实际读数

以下字段来自冻结提交的 raw 内容全文读取；ID、blob、字节数和 SHA-256 见本批证据包的 `sources-summary.json`。`first=2` 只按源文件中出现的字段登记，不推断程序对“pair”切片的内部实现。

| ID / 文件 | 参数（`k,n,trials,seed,no_dr,policy,first`） | `best_objective` | witness 读数 | 处置 |
|---|---|---:|---|---|
| `ab961a55539ea83079c6` / `pair_groups_dr_n3k6.json` | `6,3,1,22112,false,groups,2` | `-0.00028370513150265814` | `root=[0,3,4]`; `p=[0.12967744810799278,0.0036084041045110825,0.3962498071301828,0.15079275650002996,0,0.3196715841572832]`; `value_lower=0.002543230576404352`; `welfare=0.0048027560213060455`; `states=83`, `potential=83`, `policy=43` | integrated |
| `1245e6ccbc103168b87b` / `pair_groups_monotone_n3k6.json` | `6,3,1,22112,true,groups,2` | `-0.001265207200675137` | `root=[0,3,4]`; `p=[0.2290723250722263,0,0.30046333427046107,0.21884828102078246,0,0.2516160596365301]`; `value_lower=0.01134175339445241`; `welfare=0.021418299588229682`; `states=83`, `potential=83`, `policy=43` | integrated |
| `5683f1468fa9f737c779` / `pair_monotone_policy_n4k4.json` | `4,4,500,22109,true,monotone,2` | `0.0` | no witness field; `completed=500` | integrated |
| `ec8ea7d2aeb9864b6398` / `pair_plateau_n3k4.json` | `4,3,1000,22110,true,plateau,2` | `0.0` | no witness field; `completed=1000` | integrated |

The two `groups` witnesses have the same 83-state/43-policy shape as the earlier `first=0` six-action diagnostics, but their probability vectors are different floating values and the source JSON does not provide the earlier fixed rational query. Thus they extend the finite diagnostic ledger; they do not duplicate the earlier files byte-for-byte or supply a second exact certificate. The two zero-objective files add finite `n=4,k=4` monotone-policy and `n=3,k=4` plateau-policy parameter points. Neither source has a customer instance or a universal quantifier.

## Exact verifier and what it certifies

The raw verifier source is 3967 bytes and has SHA-256 `fe073ff8428f8c8a0428b2aa1edf4b7abd2d58a9e1cf64770c24da60041e791e`, matching the frozen inventory blob `9833007ab152f2c68eb3c92de78366eeecb12b3c`. A local byte-for-byte source snapshot was executed once with Python 3.12.14. It exited `0`; stdout is 1487 bytes and stderr is zero bytes. The captured files are `tools/evidence/R-2fc-aggregate-security-pair-20261031/replay/verify_dr_boundary.stdout` and `.stderr`, with the source snapshot under `original/verify_dr_boundary.py`.

The exact run checks the 84-value integer potential on six actions and three players, all 168 monotonicity inequalities, all 252 DR inequalities, 43 ordered histories and 258 deviation comparisons. It obtains path `(0,3,4)`, utilities `(0,105,56)`, total `W=161`, and static security value `v=56`; hence `3v-W=7` and `2v-(u_1+u_2)=7`, while `W-(5/2)v=21`. The fixed query is `(4/15,0,4/15,0,1/5,4/15)`, and the dual pure background is `03` with query values `(56,56,56,0,56,56)`. Nine negative third differences are also reported by the verifier.

This exact certificate belongs to the enlarged monotone DR marginal-potential game. The verifier explicitly records the non-CAG witness `Phi(11)=Phi(1)=161`, violating the CAG diagonal relation `2 Phi(11)=3 Phi(1)`. Equivalently, repeated actions change the aggregate potential/total-payoff budget (`P(1)=161` but `P(11)=0` in the established obstacle), whereas CAG welfare depends only on the support. The exact run therefore explains the failure mechanism and certifies the finite enlarged-model boundary; it does not prove or refute the original CAG strong/weak aggregation or half-coverage statements.

## Comparison with the preceding aggregate-security batches

The existing computation object `DR聚合安全六份浮点诊断--计算.md` records six `first=0` diagnostics. Its negative rows use the fixed rational query and the same enlarged-model status; its zero rows are also finite search summaries. The present `first=2` pair rows differ in source parameters and witness probabilities, so their only new content is finite search metadata and the two additional zero-objective parameter points. The exact integer obstruction and its CAG boundary remain the already integrated object `单调递减边际势的强安全聚合障碍--障碍.md`; this batch does not create a legal CAG customer counterexample or a general theorem.

## Read and runtime boundary

`clean show <id>` was attempted for all five IDs. The local promisor remote could not fetch the missing source blobs (`browser-proxy port 8889` connection failure), so the four JSON files were read through their public raw URLs in the frozen commit and the verifier source was reconstructed from that raw text; this limitation is recorded in the receipt. No credentials were printed or stored. The raw reads establish the source fields and exact hashes from the inventory, while the independent verifier run establishes only the finite exact enlarged-model checks listed above.
