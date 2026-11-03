---
id: "customer-attraction/r171-sparse-spe-rent-audit-output"
kind: "computation"
type_tag: "计算"
title: "R-171 稀疏 SPE 租金审计冻结输出"
status: "frozen-output-read-and-replayed"
truth_status: "finite-output-record; no general theorem"
review_level: "full-4406-byte-json-read-and-script-cross-check"
scope: "Frozen JSON report for independent sparse-rent audit"
source_refs:
  - "clean:211cb85bb67da5865528:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/independent/sparse_spe_rent_audit.json"
  - "clean:e7f3c5ef88b24e798b5b:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/independent/audit_sparse_spe_rent.py"
  - "local:archives/customer-attraction/state/计算/R171稀疏SPE租金独立Fraction审计--计算.md"
  - "local:archives/customer-attraction/state/引理/R-171稀疏槽clock租金与skip-premium分解--引理.md"
source_identity:
  inventory_blob: "c1aa68c90ed1434be81732356eaef45c1eb8f247"
  source_sha256: "8a1fb0e391a3d63840596ad4b9b9461888e5d80443ed280a0cefbecd7aa7394f"
  source_size_bytes: 4406
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/original/sparse_spe_rent_audit.json"
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/replay/sparse_spe_rent_audit.json"
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/comparisons/211cb85bb67da5865528.md"

# R-171 稀疏 SPE 租金审计冻结输出

## 输出身份

完整读取 4406 字节 JSON，源 blob `c1aa68c90ed1434be81732356eaef45c1eb8f247`、SHA-256 `8a1fb0e391a3d63840596ad4b9b9461888e5d80443ed280a0cefbecd7aa7394f`。顶层 `status` 为 `passed`，`scope` 明确限定为“有限精确检查；一般 SPE 和发散由配套正文证明”。JSON 与对应脚本均已实读；以复制脚本复跑生成的 replay JSON 与冻结文件逐字一致。

## 冻结统计

`ordered_history_audits` 包含 `q=2,3,4,5`，节点数分别为 15、63、255、1023，比较数分别为 30、126、510、2046，总计 2712。`all_tie_state_audits` 覆盖 `q=2,...,12`，状态数由 10 增至 300，`all_tie_checks` 总计 4048。`rent_audits` 覆盖 `q=2,...,30`，每行记录 `W=2`、`Gamma=1`、`weighted_rent=H_(q-1)/6` 的 Fraction 字符串；`q=30` 的冻结值为 `9227046511387/13974537376800`。

该 JSON 是脚本执行结果的稳定数据载体，独有于脚本的内容是每个 `q` 的逐项记录和最后的精确有理数序列。它与 `R171稀疏SPE租金独立Fraction审计` 互相引用，但不将输出记录误记为 companion note 的一般证明，也不把租金障碍变成 `2W<OPT`。对象处置为 integrated 计算输出，不迁移到 unrelated-machines。
