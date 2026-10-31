---
id: "customer-attraction/R-171-count-markov-milp-candidate"
kind: computation
type_tag: 计算
title: "R-171 计数 Markov MILP 候选器"
status: "finite-candidate-generator-with-exact-small-replay"
truth_status: "count-Markov-subclass-only; no-full-history-bound"
review_level: "full-4932-byte-read-and-small-exact-replay"
scope: "R-171 credible/count_milp.py; count-state policy MILP expanded to ordered histories"
summary: "MILP 只生成按计数状态共享动作的候选策略。p=7 大型实例分别超时或 infeasible；p=2,path=(0,0) 的小重放以 15 个变量、38 条约束成功，浮点 LP value=3/2，Fraction/规范证书/独立全历史检查得到 W=2、OPT=3、ratio=3/2。它不是全历史 SPE 的 MILP 表示或一般下界。"
source_refs:
  - "clean:4b7ae57ed9a151791e7f:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/credible/count_milp.py"
  - "local:archives/customer-attraction/tools/evidence/R-171-credible-continuation-20261031/original/count_milp.py"
  - "local:archives/customer-attraction/tools/evidence/R-171-credible-continuation-20261031/replay/count-milp-small/stdout.txt"
  - "local:archives/customer-attraction/tools/evidence/R-171-credible-continuation-20261031/replay/count-milp-small/count_milp_small.json"
  - "local:archives/customer-attraction/state/审查/R-171可信低根接续与有限候选边界--审查.md"
  - "local:archives/customer-attraction/tools/evidence/R-171-credible-continuation-20261031/comparisons/comparison-notes.md"
source_identity:
  inventory_blob: "813a72aa6fedf70de170e7d9df875c6d4e26f2e6"
  source_sha256: "524ab41949a978705df1994dc155280e030bb9b3a17acc8ffe02badfdb172c42"
  source_size_bytes: 4932
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-171-credible-continuation-20261031/original/count_milp.py"
  - "archives/customer-attraction/tools/evidence/R-171-credible-continuation-20261031/replay/count-milp-small/stdout.txt"
  - "archives/customer-attraction/tools/evidence/R-171-credible-continuation-20261031/replay/count-milp-small/count_milp_small.json"
  - "archives/customer-attraction/tools/evidence/R-171-credible-continuation-20261031/comparisons/comparison-notes.md"
---

# R-171 计数 Markov MILP 候选器

## 1. 候选模型

源程序完整实读 4,932 B，SHA-256 `524ab41949a978705df1994dc155280e030bb9b3a17acc8ffe02badfdb172c42`，稳定 ID `4b7ae57ed9a151791e7f`，blob `813a72aa6fedf70de170e7d9df875c6d4e26f2e6`。给定主题数 (p)、根路径 `path` 和比较主题集合 (J)，程序先枚举深度小于玩家数的**计数状态** (k)，而不是所有有序历史。每个状态/动作有连续 `Ui` 变量和二元 `Zi` 动作变量，且每个状态恰选一个动作。

固定根路径的动作后，程序加入：根福利归一化、客户质量总和上界、根首动作的 payoff cap、根计数与路径一致、每个计数状态恰一动作、以及对每种客户类型和偏离动作的 payoff 差约束。MILP 目标以负的 coverage row 最小化，等价于在候选集合上最大化 (J) 的覆盖。SciPy `milp` 只产生浮点候选；若返回策略，程序再把计数状态动作展开到全部有序历史，构造 `StrategyCone`，并在 `cone.optimize` 后用 `integer_clones`、`verify_certificate` 和 `independently_verify` 做精确接受。

因此该对象只能谈“计数 Markov 子类中是否找到候选”。按计数状态共享动作会把不同顺序历史强行放入同一动作表；完整 CAG 模型允许这些历史有不同离轨平局，所以 MILP 的可行域不是所有完整策略的并集。程序 docstring 也明确它不声称 full-history 或 exact bound。

## 2. 实际重放和冻结摘要

在冻结依赖下用 `p=2,path=0,0,J=0,1,seconds=10,rootcap=1` 运行。HiGHS 返回 optimal，15 个变量、6 个 binary actions、38 条约束，浮点目标 1.5；`cone.optimize` 返回 exact primal、dual bound 和 dual optimal，value `3/2`。完整整数克隆为 `[2,1,0]`，策略根路径 `(0,0)` 的玩家 payoff 均为 1，最终 `W=2`、`OPT=3`、`ratio=3/2`。规范证书和独立全历史检查均通过，输出保存在 replay JSON。

冻结 `finite_attempt_summary.json` 另记录三个 p=7 运行：

| path / rootcap | HiGHS 状态 | 变量 / binary / constraints | 结果 |
|---|---|---:|---|
| `0,0,1,1,2` / 0.12 | time limit（60.34s） | 4747 / 2310 / 46540 | 无 primal objective |
| `0,1,1,1,1` / 0.15 | infeasible（2.42s） | 4747 / 2310 / 46540 | 无候选 |
| `0,0,1,1,2` / 0.19 | time limit（45.30s） | 4747 / 2310 / 46540 | 无 primal objective |

超时不是 infeasible，也不表示不存在候选；infeasible 只针对该 count-state、路径和 cap 组合。小 p=2 的 ratio 3/2 也低于 Q-CAG-HALF 反例所需的 2。

## 3. 与 R-171 credible 路线的关系

README 的低根路线要求完整有序策略、低根约束和逐历史精确偏离验证。`count_milp.py` 的后验展开/验证满足单个接受点的这一要求，但 MILP 生成阶段仍只搜索计数 Markov 子类；它不能支持“没有任何完整策略”或“所有 SPE 都有某比率”的结论。

与 `low_root_discovery.py` 相比，本程序用 MILP 同时选择计数策略和客户质量，但没有 credible continuation 的四种随机菜单递归；与 `minimum_root.py` 相比，它最大化指定覆盖集合的候选目标，而非在固定目标策略锥内最小化首位份额。三者的 `OPT/W`、root cap 和策略量词不可混用。

## 4. 处置

本对象作为 integrated 的候选器与小规模 exact replay 保存。它没有给出一般算法、MILP 对偶下界、全历史困难性、Q-CAG-HALF 反例或 unrelated-machines 结论；后续若扩展必须同时报告 count-state 假设、超时/infeasible 状态和完整有序历史证书。
