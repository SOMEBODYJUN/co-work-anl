---
id: "customer-attraction/r18-simplify-largest-incumbent-milp"
kind: "computation"
type_tag: "计算"
title: "R-18 最大 incumbent 简化 MILP 障碍"
status: "exact-integer-milp-replayed"
truth_status: "finite suffix-SPE and root-bridge obstruction; no full-SPE theorem"
review_level: "full-3058-byte-read-and-exit0-replay"
scope: "MILP simplification of one 3-player, 6-topic incumbent certificate"
source_refs:
  - "clean:14375a4d622e69252e13:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/global_proof/simplify_largest_incumbent.py"
  - "clean:ac0a7249b93d1961cb92:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/global_proof/largest_incumbent_small_counterexample.json"
  - "clean:663827506601922a81a3:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/global_proof/largest_incumbent_n3p6_best.json"
  - "local:archives/customer-attraction/state/障碍/R18最大主题强制根的非完整SPE障碍--障碍.md"
source_identity:
  inventory_blob: "cc8a83522dfe8648d41ee485c53b49bf63c876df"
  source_sha256: "b19cc54552cf80b79a6d9f9c6922b906e3afb8b6a13d504502a44773f8bfe643"
  source_size_bytes: 3058
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/original/simplify_largest_incumbent.py"
  - "archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/replay/simplify_largest_incumbent.stdout"
  - "archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/replay/simplify_largest_incumbent.json"
  - "archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/related/largest_incumbent_n3p6_best.json"
  - "archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/comparisons/14375a4d622e69252e13.md"

# R-18 最大 incumbent 简化 MILP 障碍

## 程序输入和目标

完整实读 3,058 字节 Python。程序读取同批三人六主题完整 incumbent best JSON 的策略动作和实例结构，沿原策略计算每个正深度历史的 suffix IC 行；为每个非空客户类型设置整数 multiplicity，增加“主题 0 保持最大裸大小”的条件，并通过 `scipy.optimize.milp` 强制根收益严格低于 `OPT/(2m-1)` 的线性不等式。它没有放宽 suffix IC，也没有把根强制动作误当成 SPE 行。

## 实际重放

复制 best JSON 与程序到临时目录后执行 exit 0，HiGHS 状态为 `Optimization terminated successfully. (HiGHS Status 7: Optimal)`。生成 JSON 的 SHA-256 为 `44ae1a0ecec9659c75eee622ed9990e216815ff17a150375dc19bd1b1cfd0986`，与冻结 `largest_incumbent_small_counterexample.json` 相同。

复跑摘要：实际 `(0,2,3)`，主题大小 `[13,12,13,13,13,13]`，强制 incumbent 收益 `13/2`，`OPT=33`，`W=26`，`OPT/u=66/13`，252 个 suffix comparisons，根偏离值 `[13/2,21/2,21/2,12,13/2,21/2]`。这证明 MILP 找到的确是一个有限 suffix-SPE/root-forced 障碍，而不是浮点候选。

## 证据边界

程序的 MILP 约束只保证正深度历史的 SPE 比较；根动作由搜索目标强制，所以输出明确不是 full SPE。它不证明最大基数主题在任意完整 SPE 中不能成为根最优动作，也不证明 `OPT>2W`。对象处置为 integrated 计算障碍，保留输入、stdout 和生成 JSON，不迁移到 unrelated-machines。
