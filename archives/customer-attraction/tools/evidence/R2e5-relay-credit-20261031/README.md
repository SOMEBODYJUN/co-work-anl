# R-2e5 relay-credit full-depth ledger evidence

本证据包保存两个 relay_credit 数学源和同一工作区的 `workspace.json`。脚本与冻结 JSON 完整读取，并在隔离目录直接重放；workspace 仅含身份索引字段。

| clean id | source | bytes | SHA-256 | 处置 |
|---|---|---:|---|---|
| `4a0a90aa4d26e578c914` | `relay_credit/audit_full_depth_ledger.py` | 7229 | `dc30ee4ee359393b83f58cd702cc9f74521c6027d0a4464ed59c2f86e4fa877b` | Fraction 全深度有限复核 |
| `f9696dd81c9a59d41582` | `relay_credit/full_depth_ledger_audit.json` | 2211 | `7abe44353c7fe29cd963ad5016da7bd209950a43a6320085c271e36ef43c615f` | 冻结报告并逐字段比较 |
| `8439f635fa5fe23b9e98` | `workspace.json` | 150 | `c8c53ec643368ed68a036f7a35c978fc3c17a0e17b1b32884e6f5d4c12733205` | 仅工作区索引 |

`audit_full_depth_ledger.py --output generated.json` 返回码 0、stderr 为空，生成 JSON 与冻结 JSON 逐字节相同；独立 `verify_relay_credit.py` 返回 `PASS`。

冻结有限字段为：sharp family 的完整 SPE 检查覆盖 (m=2..6) 的 10,213 个有序历史和 60,276 项动作比较；(m=2..7) 的全部 5,912 个最优排列；变量公式核到 (m=80)，实际前缀风扇到 (m=10)；60 个任意策略代数样本、5,678 条边，其中 6 个零客户样本，明确 `SPE_claim=false`。示例调和 relay fee 为 (m(H_m-1))，从 (m=4) 起超过 (W=m)，但这只排除“用一条最优比较前缀并由共同实际 W 支付全部 relay 费”的特定模板；它不否定共同 source、全树流或六人 half。

`workspace.json` 的字段仅为 `schema/save/actor/instance`，没有客户、策略、收益、IC 或证书内容。它只作为 R-2e5 relay-credit 工作区的恢复路由。
