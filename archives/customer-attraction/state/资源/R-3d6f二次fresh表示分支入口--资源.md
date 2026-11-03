---
id: "customer-attraction/r3d6f-quadratic-fresh-representation-entry"
kind: "resource"
type_tag: "资源"
title: "R-3d6f 二次 fresh 表示分支入口"
status: "historical-workspace-navigation"
truth_status: "navigation-only; Q-CAG-HALF-open"
summary: "R-3d6f new_representation README 记录 quadratic graph compiler、精确回归和高偏置安全边界候选；不含一般证明、完整 SPE 证书或 half 反例。"
source_refs:
  - "clean:2edcc94fedb77163b934"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/new_representation/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/new_representation/README.md"
source_sha256: "ff75394098264c6a6c699d5e64aede55eedea8a23467185921dcca5e3d66edc7"
related_objects:
  - "customer-attraction/auxiliary-symmetric-quadratic-fresh-individual-static-floor-candidate"
  - "customer-attraction/r3d6f-fractional-weak-bridge-and-witness-dag-review"
---

## 载体身份与入口内容

来源 `2edcc94fedb77163b934` 是 R-3d6f 工作区 `new_representation/README.md`，772B，SHA-256 为 `ff75394098264c6a6c699d5e64aede55eedea8a23467185921dcca5e3d66edc7`。README 列出三个分支文件：`quadratic_graph_compiler.md`（全历史双向编译、θ等式、高偏置安全边界候选）、`quadratic_graph_compiler.py`（有理系数到整数单位客户编译与精确回归）和 `quadratic_graph_audit.json`（实际回归输出）。

README 明确 Q-CAG-HALF 仍 OPEN；高偏置编译只给安全边界，不能用来反复搜索 half 坏点。审计 JSON 是有限精确回归输出，不是一般福利证据。

## 数学边界与接续

该 README 是导航和状态记录，不承载编译证明、客户实例、完整有序历史策略、SPE 偏离核验或审计输出本体。相关二次辅助候选、R-3d6f 分数负载弱桥和 witness-DAG 审查均保持独立量词；后续若读取分支文件，须用各自 clean source、SHA 和完整证据另行登记。

本对象只保存入口、现状和接续边界，不创建定理、反例或一般半覆盖结论。
