---
id: "customer-attraction/R275-padded-residual-dag"
kind: "review"
type_tag: "审查"
title: "R275 填充残差 DAG 与六人辅助边界"
status: "finite-exact-dag-replayed"
truth_status: "finite-auxiliary-counterexample-certificate; not-Q-CAG-HALF"
summary: "冻结 padded_residual_dag.py 用 ExactSPESolver 构造一个 m=6、9主题、10类客户的完整历史目标 DAG；5440个节点全部通过独立阈值/纯SPE结果集核验，代码声明其作用域只针对 common-query regret ≤ minimum provider payoff，不针对 Q-CAG-HALF。"
source_refs:
  - "clean:91b39137ab91a8bc9d3f:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/direct_global/padded_residual_dag.py"
  - "clean:ee53fbf96073c13bf5c0:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/direct_global/padded_residual_m6_dag.json"
  - "local:archives/customer-attraction/tools/evidence/R275-padded-dag-agent/manifest.json"
  - "local:archives/customer-attraction/tools/evidence/R275-padded-dag-agent/verify_dag.stdout"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R275-padded-dag-agent/padded_residual_dag.py"
  - "archives/customer-attraction/tools/evidence/R275-padded-dag-agent/padded_residual_m6_dag.json"
  - "archives/customer-attraction/tools/evidence/R275-padded-dag-agent/replay.stdout"
  - "archives/customer-attraction/tools/evidence/R275-padded-dag-agent/verify_dag.py"
  - "archives/customer-attraction/tools/evidence/R275-padded-dag-agent/verify_dag.stdout"
  - "archives/customer-attraction/tools/evidence/R275-padded-dag-agent/customer_attraction/model.py"
  - "archives/customer-attraction/tools/evidence/R275-padded-dag-agent/customer_attraction/exact.py"
  - "archives/customer-attraction/tools/evidence/R275-padded-dag-agent/customer_attraction/certificate.py"
---

# 来源身份与模型

主源 `91b39137ab91a8bc9d3f` 是 2,277 字节的 `padded_residual_dag.py`，冻结 SHA-256 为 `c73bba2397cdcca85f8f1a214a04ab94cca52be217977f595da7a1b7071bb07c`。它导入 `Instance` 与 `ExactSPESolver`，脚本文件头明确写着这是 discovery/certificate builder，本身不是普遍证明。

`instance(m)` 建立五个固定客户类型和 `m−2` 个 padding 主题。对 `m=6`，主题为 `A,B,T,D,E,P0,P1,P2,P3`，客户类型及重数为：`{A,D}:2`、`{A,E}:2`、`{B}:3`、`{B,D,E}:2`、`{T}:3`、`{T,D,E}:2`，以及四个 padding 单主题客户 `{Pi}:4`。玩家数为 6，客户在所选主题间均分，纯 SPE 结果由精确计数求解器给出。

# DAG 构造

脚本固定目标路径

`h=(P0,P1,P2,P3,A,B)=(5,6,7,8,0,1)`。

其目标终局计数为 `(1,1,0,0,0,1,1,1,1)`。递归状态是 `(k,c)`：`k` 为当前前缀主题计数，`c` 为一个目标终局计数。对每个动作 `a`，脚本只保留满足两项条件的动作：`c` 属于 `ExactSPESolver.outcomes(k+e_a)`，且该动作在 `k` 的主题收益不低于 `ExactSPESolver.threshold(k)`。沿指定路径且仍可行时保留路径动作；其他位置取第一个可行动作。

对于每个可行动作，所有偏离动作 `b` 都递归到一个目标：遵循动作沿用 `c`，偏离动作选择该子状态中按 `(topic_payoff(b,z),z)` 字典序最小的纯 SPE 终局。这会把每个有限历史的偏离后继也显式放进 DAG，而不是只保存实际路径。

# 复现与独立核验

直接以保存的精确模型重放 `m=6`：

```text
PYTHONPATH=archives/customer-attraction/tools/evidence/exact-spe \
python3 padded_residual_dag.py 6
```

退出码为 0，输出 `nodes=5440`；生成的 DAG SHA-256 为 `555d309040dc76222624776a71c6d49b54804880cf38da12d2597abed2129efc`，与冻结的 m6 JSON 一致。独立 `verify_dag.py` 重新实例化同一 ExactSPESolver，逐节点检查终端计数、每个保留动作的目标是否属于相应 SPE outcome 集、阈值收益是否满足，并检查所有替代动作的子节点目标；共核验 2,437 个非终端节点，结果为 PASS。

# 代码报告的有限数值与作用域

冻结 JSON 的 `expected` 字段报告：实际路径的提供者收益为 `[4,4,4,4,4,5]`，`W=25`，实例最优福利 `OPT=26`，`query=2`，`query_uncovered=5`，`F=30`，最小收益为 4，`bridge_slack=5−m=−1`。这些字段是该构造针对辅助 common-query regret 边界的诊断量；它们不能被重写成六人半覆盖结论。

JSON 的 `scope` 明确限定为“只针对 common-query regret ≤ minimum provider payoff 的反例，不针对 Q-CAG-HALF”。因此本对象可作为一个有限、可复核的辅助边界构造：它展示了指定 padding 客户和完整离轨 DAG 下的收益/查询缺口，但没有证明任意客户目录、任意历史或六人目标的下界失败。

# 可复用内容与缺口

可复用的是一种把“目标终局 + 每个偏离动作的阈值可行后继”编码为共享 DAG 的方法；它适合在小人数实例中检验辅助 regret 或查询收费命题，并且保留所有离轨动作的纯 SPE 结果集合。

仍需把 `W=25`、`OPT=26`、`query=2` 与实际辅助命题的精确定义逐项接上，并与 Q-CAG-HALF 的客户覆盖量词分离。DAG 核验只证明本实例的有限证书结构和求解器合同，不能替代任意输入的理论证明，也不能把代码注释中的“counterexample”扩展为主问题反例。
