---
id: "customer-attraction/direct-cover-readme-route"
kind: review
type_tag: "审查"
title: "customer-attraction 直接覆盖分支 README、义务分层与前缀障碍路由"
status: "retained-route-and-boundary"
truth_status: "workspace-route-document-not-proof"
review_level: "full-source-read-cross-archive-comparison"
scope: "direct-cover branch, weak-matching obligations, min-continuation compression, and incumbent-prefix obstruction routing"
source_refs:
  - "clean:5e1573a1c918d2e380f1:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/README.md"
  - "local:archives/unrelated-machines/tools/evidence/customer-attraction-direct-cover-readme-20261031/original/README.md"
  - "local:archives/unrelated-machines/tools/evidence/customer-attraction-direct-cover-readme-20261031/comparisons/comparison-notes.md"
related_objects:
  - "local:archives/unrelated-machines/tools/evidence/customer-attraction-lipschitz-failure-20261031/original/incumbent_actual_lipschitz_failure.json"
  - "local:archives/unrelated-machines/state/反例/customer-attraction实际前缀Lipschitz失败证书--反例.md"
---

# customer-attraction 直接覆盖分支 README、义务分层与前缀障碍路由

## 来源身份与处置

本对象完整实读 clean source `5e1573a1c918d2e380f1` 对应的 `research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/README.md`，源大小 4472 字节，SHA-256 `4834a61c0c032a1a522732a41389858c6b1cdd5a707159690c3d8bb093924dab`，inventory blob `90749a24c789ec7795b8fad3b75a6fe33715e30f`。原文保存在 [README evidence](../../tools/evidence/customer-attraction-direct-cover-readme-20261031/original/README.md)，比较记录在 [comparison-notes.md](../../tools/evidence/customer-attraction-direct-cover-readme-20261031/comparisons/comparison-notes.md)。

这是 customer-attraction 工作区的路线/状态说明，处置为 `retained` 审查资源。它没有给出新的 Q-CAG-HALF 半覆盖承重引理，也没有把有限诊断升级为一般结论；其独有价值在于准确分开三个匹配义务、记录最小续局压缩原则、定位失败的 incumbent Lipschitz 桥，并把后续脚本与证书的读取边界写清。

## 当前目标和三种义务

README 明确把一般 Q-CAG-HALF 目标保留为 `OPEN`。在一条固定完整纯 SPE 的实际有序路径和达到 OPT 的 m 元组 `T` 上，令 `V(i,T)` 表示位置 i 首次偏离到 `T` 后、沿同一策略的真实收益。三种强度不同的义务必须分别登记：

1. **弱匹配：** 存在一个最优元组和排列 `π`，满足 `Σ_i V(i,T_{π(i)}) ≥ OPT − W`；这是足以推出 half 的候选充分条件。
2. **弱平均：** `m OPT ≤ m W + Σ_{i,j} V(i,T_j)`；它更强，也足以推出 half。
3. **旧强平均：** `m OPT ≤ (m−1)W + Σ_{i,j} V(i,T_j)`；它更强，若成立可推出 `2−1/m`，但 README 只记录两人任意背景证明，未把任意人数写成已证。

README 同时提醒：已有 portfolio matching 反例只否定支付 `|O\C|`，没有否定弱匹配中的 `OPT−W=|O\C|−|C\O|`；全分布安全预算反例比较的是独立查询 `C_i`，不能直接替代真实偏离 `D_i`。有限计算也不能替代这些义务的证明。

## 最小续局压缩原则的状态

给定一条 SPE 可实现的实际有序路径，所有“首次偏离实际行动”的子树互不相交。README 说明可以分别替换这些子树的完整 SPE 续局而不改实际路径。令 `f_r(b,T)` 为固定前缀负载 `b`、首位已选 `T` 后，剩余 `r−1` 位所有合法完整纯 SPE 续局中该 T 入场者的最小收益；有限性使最小值存在。把每个首次偏离子树替换为达到最小值的续局不会提高实际节点的偏离收益，且子树内部仍为 SPE。

这给出一种规范 solver 可用的 min-continuation 证书思路：对实际行动保留 `u_i`，对非实际首次偏离写 `V(i,T)=f_r(b_i,T)`。README 没有把它宣称成新的均衡压缩定理；正式证明仍须读取其相邻对象并核对每个子树替换、有限性和路径保持条件。

## 失败的 incumbent Lipschitz 桥

较早尝试的桥为 `f_r(b,T) ≥ ((r−1)/r) f_{r−1}(b+A,T)`。README 记录该桥在五客户、三主题、任意正背景重数的统一族中失败，且额外固定动作未必是实际行动；随后又用实际限定的 61 客户输入把失败压缩到实际路径 `(B,A,A,F)`。其中真实偏离满足 `V_{1,A}=9 < (3/4)V_{2,A}=39/4`。因此限制额外行动为实际当前行动也不能修补单主题比例递推。

README 给出的机制解释是：后续跟随者收益从 P 转移到 B，说明只保留某个入场主题标量值、再按人数比例结算固定未来行动的影响是不够的。后续机制需要保留至少 B 的替代信用，或使用真实跨分支中继；继续调单个入场者比例没有证据基础。

## 诊断代码和边界

README 路由三个独立诊断：`check_weak_matching.py` 对既有规范证书做精确匹配检查但忽略若干嵌套 schema；`lp_weak_matching.py` 对固定完整策略锥做有限 LP 诊断，少量 `m=4,k=6` 与 `m=5,k=7` 未分离强平均，已停止同类随机扫描；`check_incumbent_lipschitz.py` 从 `dynamic_iid_local.json` 找到失败，再压缩成五客户族。它要求 root 后续分别读取这些文件，不能把 README 的指针当成已执行证据。

## 与当前任务和后续接续的关系

这是 customer-attraction 路线，不能迁移到 unrelated-machines 调度或六提供者有限单位客户 SPE。它可作为第三阶段关系证据：弱匹配、弱平均、旧强平均和实际偏离桥应有不同稳定 ID、不同证据类型和不同失败边界。后续读取 `actual_prefix_relay_obstruction.md`、`incumbent_lipschitz_obstruction.md`、三个脚本和 JSON 时，必须保留 `OPEN` 状态，区分候选、完整证明、有限实验和障碍。

本来源未执行任何代码、未核验兄弟文件、未发起新文献搜索。它不证明 Q-CAG-HALF，不否定真正聚合安全值，也不否定弱匹配/弱平均/旧强平均本身。
