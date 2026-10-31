# R-2e5 varying-baselines code-bank suffix probe

本证据包保存当前领取的两个 varying-baselines 源、精确求解器依赖、原脚本重放输出和独立字段检查。该批是已有“二进制全码银行的加载者真实偏离”障碍的四点有限报告复核；解析的任意 \(d\ge2\)、任意共享遗漏证明仍由既有障碍正文承担。

## 源

| clean id | source path | bytes | SHA-256 |
|---|---|---:|---|
| `b099cfb45b42ccda7e71` | `.../credible_construction/varying_baselines/code_bank_suffix_probe.json` | 10545 | `829cc98c9244e4c0999a6e77a08d96893b15aa89449a7cb8ae847ca9ca294a1b` |
| `86b62e461fb25274692c` | `.../credible_construction/varying_baselines/inspect_code_bank.py` | 4834 | `e9d908fd848b6d5cf2f7eede9fe454fbf65578f7256848a20ca8ea71539e584c` |

`inspect_code_bank.py` 依赖 `customer_attraction.model.Instance` 和 `customer_attraction.exact.ExactSPESolver`。`replay/layout/customer_attraction/` 保存实际使用的完整依赖副本；为满足源脚本的固定 `parents[6]` 路径，脚本在 `replay/layout/a/b/c/d/e/f/` 中按原相对布局运行。

## 重放结果

原脚本 exit 0、stderr 为空；重放生成的 `code_bank_suffix_probe.json` 与冻结源 JSON 逐字节相同。独立 `verify_code_bank_probe.py` 返回 `PASS`，并核对源哈希、四行参数、状态布尔值、每行状态计数和所有 B/C/A/L 动作的严格关系。

| (d,h,x,y) | 共享遗漏 | loader payoff | true threshold | `B_j` continuations checked | states / terminal / retained |
|---|:---:|---:|---:|---:|---:|
| (2,18,1,1) | 否 | 18 | 39/2 | 1 | 165 / 120 / 165 |
| (3,18,1,1) | 否 | 27 | 57/2 | 3 | 969 / 816 / 1005 |
| (3,36,2,3) | 是 | 54 | 58 | 4 | 969 / 816 / 1005 |
| (4,18,1,1) | 是 | 36 | 75/2 | 12 | 6545 / 5984 / 6996 |

全部四行都记录 `desired_in_outcomes=false`，末位真行和冻结加载者行通过，所有 B_j 续局的 bank-balanced 审计通过。所有 B_j 动作的 `minimum_SPE_payoff` 严格高于 desired loader payoff；C/A/L 动作没有超过。报告中的 165、969、6545 等是计数态、终局态和保留 outcomes 的有限求解器统计，不是完整任意历史定理的证明规模。

## 数学边界

有限报告重现了 \(L_i,B_i,B_i\) 指定顺序在四个参数点不在 outcomes 的事实，并支持既有解析障碍中“真实 \(B_j\) 偏离后的任意两人 SPE 平衡银行并释放 \(X_j\)”的同方向证据。它没有检查同计数的另外两个后缀排列能否实现，也没有把四点报告升级为 \(d\) 的全称或六人 half 反例。源脚本的精确 solver 依赖和 stdout/stderr 都被保全，便于第三阶段复核。
