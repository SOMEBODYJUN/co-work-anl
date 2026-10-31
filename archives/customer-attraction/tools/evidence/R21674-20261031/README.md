# R-21674 2026-10-31 clean evidence

本证据目录对应 Boss3 实际领取并以 `clean show` 逐一读取的 20 个冻结源版本。原始源仍由 `cleanup/inventory.jsonl` 中的 ID、blob、SHA-256 和冻结 commit 定位；`source-manifest.json` 保留本批的精确绑定。`raw/` 与 `R21674_exec/` 仅为本地读取/导入适配缓存，不作为远端数学正文。

## 可重放运行

- `runs/audit_three_profit_opportunity.*`：逐 4096 状态、12288 系数的 Fraction 审计，退出 0。
- `runs/probe_branch_endpoint.*`：n=3,4,5,6,8,10 的有限 LP 均 infeasible，退出 0。
- `runs/certify_profit_endpoint.*`：在临时同目录导入依赖后，LP success=True；最大分母 10^6 重构时最小 slack=0、负 slack=0，退出 0。
- `runs/probe_opportunity_coeff.*`：cover C=2..3 均 infeasible；profit C=3 feasible，其余 C=2..2.75 infeasible，退出 0。
- `runs/probe_tax_endpoint.*`：n=3 feasible，n=4,5 infeasible，退出 0。
- `runs/probe_three_endpoint.*`：tau=1..2.5 feasible，tau>=3 的测试点 infeasible，退出 0。
- `runs/tail_three_price_probe.*`：k=3..100 的有限集合均 infeasible，退出 0。
- `runs/gram_probe.*`：18 次切面迭代，目标约 1.5；最后一次负核为 0，仍是数值/条件 Gram 探索，退出 0。

没有把上述有限 LP、MILP 超时、浮点候选或缺依赖运行当作全局定理、真实客户实例、SPE 反例或 Q-CAG-HALF 证明。完整的比较、边界和去向见 `comparison-notes.md` 与对应正式正文。
