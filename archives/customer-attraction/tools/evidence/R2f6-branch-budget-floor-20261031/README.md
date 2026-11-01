# R-2f6 branch-budget floor and background-plateau evidence

本证据包保存四份当前 clean 源的原件、隔离重放和独立字段检查。两份 `branch_budget` 源对五个既有完整策略输入做有限浮点 LP 诊断；两份 `potential` 源以标准库 `Fraction` 独立重建合法背景安全值平台的有限主树。

## 源哈希

| clean id | source | bytes | SHA-256 | 作用 |
|---|---|---:|---|---|
| `4d79ef69babc38ee7904` | `branch_budget/check_individual_coverage_floor.py` | 4725 | `9888c1b7f22e349680fac7274da3976560861029f05fb9c7114831fe55956ded` | 五个既有策略锥的 `(2m-1)u_i` 浮点 LP 诊断 |
| `37291033d6f0510c37ee` | `branch_budget/individual_coverage_floor_test.json` | 1217 | `d9eb4520ec98feb3b14e86f20175107950f1c8c3d553472110504ca92b4a6336` | 冻结五行 proposal 输出 |
| `80df6b7525e1720cf730` | `potential/audit_background_plateau.py` | 5086 | `5e5fce759be6f0cb34e1fdc21b02f78621074060374041bbcb51d98ffe83bcf5` | 五客户、11主题背景平台的独立 Fraction 重建 |
| `3283e346a685497dd57a` | `potential/background_plateau_independent_audit.json` | 133813 | `241b437bbae28f8a6c1f7be31f4acbae70d1c74ad31f5622845bc0ee5461bb33` | 冻结 B=3,4,10 全树审计输出 |

## branch-budget 有限 LP

脚本按原布局读取五个已保存的策略证书，枚举完整历史 SPE 行和大小至多 `m` 的比较主题，使用浮点 `linprog`。五个冻结结果为：

- `individual_security_failure` 与 `aggregate_theta_failure`：`m=3`，实际 `(0,3,4)`，目标 `(1,2,4)`，`lp_value=0.05263157894736836`；
- `root_tax_failure`：`m=4`，实际 `(0,0,0,5)`，目标 `(1,2,3,5)`，`lp_value=-1.6653345369377348e-16`；
- `portfolio_matching_failure`：`m=2`，实际 `(4,0)`，目标 `(3,4)`，`lp_value=-5.551115123125783e-17`；
- `global_decorrelation_failure`：`m=4`，实际 `(2,5,0,0)`，目标 `(0,2,3,4)`，`lp_value=-2.4980018054066022e-15`。

前两行严格为正，后三行的负值在双精度误差量级。脚本只在小于 `-1e-8` 时尝试构造整数计数和 Fraction 重核，本批没有触发该分支。因此这五行只能作为有限浮点 proposal 记录，不能算有理负证书，也不能推出 `(2m-1)u_i >= OPT_m` 的一般命题。

## 背景安全值平台

`audit_background_plateau.py` 不导入源 solver，显式构造五个单位客户、六个主主题和五个单例，按完整有序历史递归生成主树，再把单例接入所有离轨节点。源 JSON 与当前生成 JSON 逐字节相同，独立 verifier 返回 `PASS`。

三组背景均检查 `1464` 个有序历史和 `16104` 个含自身动作比较，最小 exact slack 为 0。精确结果为：

| `B` | 根 `u` | `v4=v3_after_0` | `v4-u` | `main_states` |
|---:|---:|---:|---:|---:|
| 3 | `11/30` | `23/60` | `1/60` | 210 |
| 4 | `13/42` | `9/28` | `1/84` | 210 |
| 10 | `25/156` | `17/104` | `1/312` | 210 |

这份独立有限证书支持既有全整数 `B>=3` 解析平台障碍的具体回放；它只给出 B=3、4、10 的运行记录，背景前缀可能离轨，不构成当前六人根 SPE 或六人 half 反例。

`replay/coverage-floor/` 保存成功的原布局和五个依赖输入；`replay/plateau/` 保存平台脚本运行。`verification.stdout.txt` 为 `PASS`，stderr 为空。
