---
id: "customer-attraction/r171-sparse-spe-rent-independent-audit"
kind: "computation"
type_tag: "计算"
title: "R-171 稀疏 SPE 租金独立 Fraction 审计"
status: "finite-exact-audit-passed"
truth_status: "finite-checks-only; companion proof carries general SPE/divergence claim"
review_level: "full-4148-byte-read-and-exit0-replay"
scope: "Two-customer complete SPE family; ordered histories q=2..5; all ties q=2..12; rent identities q=2..30"
source_refs:
  - "clean:e7f3c5ef88b24e798b5b:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/independent/audit_sparse_spe_rent.py"
  - "local:archives/customer-attraction/state/反例/R-171完整SPE稀疏槽租金障碍--反例.md"
  - "local:archives/customer-attraction/state/引理/R-171稀疏槽clock租金与skip-premium分解--引理.md"
source_identity:
  inventory_blob: "670f9a1d9ba20c06c284e85bfe6d652fb3f54eb9"
  source_sha256: "ef792c56df6c294d73b5c54066e92583768bf00d33abad6d7442fda4ad2d20e1"
  source_size_bytes: 4148
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/original/audit_sparse_spe_rent.py"
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/original/sparse_spe_rent_audit.json"
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/replay/audit_sparse_spe_rent.stdout"
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/replay/sparse_spe_rent_audit.json"
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/comparisons/e7f3c5ef88b24e798b5b.md"

# R-171 稀疏 SPE 租金独立 Fraction 审计

## 程序和实际执行

完整实读 4148 字节 Python 源，保留冻结 SHA-256 `ef792c56df6c294d73b5c54066e92583768bf00d33abad6d7442fda4ad2d20e1`、blob `670f9a1d9ba20c06c284e85bfe6d652fb3f54eb9`。为避免改写冻结原件，将程序复制到 `tmp/r171/run/` 后以 `python3` 执行一次；实际 exit 0，stdout 为 `status=passed`、`ordered_comparisons=2712`、`all_tie_checks=4048`。复跑 JSON 和 stdout 位于 evidence `replay/`，原冻结 JSON 位于 `original/`，二者 SHA-256 相同（JSON 稳定输出）。

程序定义两客户类型 0/1、容量阈值 `q` 的策略 `allowed/policy/finish`，终局收益是玩家所选类型的逆负载 `1/count`。当一类达到 `q` 后强制选择另一类，实际路径被固定为
\[
  (0),\;1^q,\;0^{q-1},
\]
终局计数为 `q/q`。`audit_histories(q)` 对 `q=2,3,4,5` 穷举每个有序历史，比较规定动作和两个固定动作沿真实后继的收益；`audit_all_ties(q)` 对 `q=2,\ldots,12` 的每个计数状态、允许平局和替代动作比较终局收益，并确认未满状态只通向 `(q,q)`。

## 租金恒等式和有限数据

`audit_rent(q)` 对 `q=2,\ldots,30` 逐客户以 `Fraction` 重算未来槽，验证每个被选单槽的值为 `1/6`、\(W=2\)、\(\Gamma=1\)，并核对加权租金
\[
  \sum_{j=1}^{q-1}\frac1j\frac16=\frac{H_{q-1}}6.
\]
冻结记录的最后一项（`q=30`）为 `9227046511387/13974537376800`。这与已归档的完整 SPE 障碍页中“稀疏未来槽可产生调和发散”及 clock/skip-premium 分解一致；独立脚本把定义级历史和租金检查拆开实现，因此是新 replay 证据而非把 companion note 当成程序输出。

## 证据边界

PASS 只认证列出的有限参数和精确 Fraction 比较。程序主输出明确写 `Finite exact checks; general SPE and divergence are proved in the companion note.` 因而不能单凭本文件声称对任意 `q` 的完整 SPE 证明，也不能证明原 Q-CAG-HALF 效率下界失败。`Gamma=1,W=2` 的租金发散属于支付桥的障碍；它没有给出跨全部真实历史的付款方案。与已有 clock 引理相同，reset 与 clock 的差额 skip-premium 仍需真实激励、抵销或其他信用支付。本对象不迁移到 unrelated-machines。
