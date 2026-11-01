---
id: "customer-attraction/Ra0-background-rows-fixed-support-script"
kind: "review"
type_tag: "审查"
title: "Ra0 固定支持背景行脚本"
status: "finite-exact-LP-diagnostic"
truth_status: "restricted-support-diagnostic; no-game-counterexample"
summary: "脚本把冻结的437行约束扩展为若干背景行，但只在64个原子支持上做线性规划和有理恢复；新点精确满足写入行，旧点在一条S3 indexed background行上违反，不能外推为全域定理或SPE反例。"
source_refs:
  - "clean:ac5bc2bdfb7f895f6d57:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_rows_fixed_support.py"
  - "local:archives/customer-attraction/tools/evidence/Ra0-rows-agent/background_rows_fixed_support.json"
  - "local:archives/customer-attraction/tools/evidence/Ra0-rows-agent/manifest.json"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/Ra0-rows-agent/background_rows_fixed_support.json"
  - "archives/customer-attraction/tools/evidence/Ra0-rows-agent/manifest.json"
---

主源是冻结的 `background_rows_fixed_support.py`，5,964 字节，SHA-256 为 `f7ec8d413ac359319be9ff1c2e5760a480a4d54a010fe63bde2c773ff4cc060e`。脚本读取已有五人索引审计的437行和64个原子支持，先把原行转成有理数矩阵，再追加三类诊断约束：任意背景对 `(i,C,D)` 行、两条固定真实后缀族的背景行，以及 AB/AE/S3/S4 的 indexed background 汇总行。它没有枚举所有允许的客户原子或完整策略。

扩展后总行数为 `437+1430`。SciPy 浮点 LP 在 `w·x=1` 下最大化覆盖型目标，随后脚本用活跃行和 Fraction 高斯消元恢复一个有理点，并检查所有新增行的非负松弛。报告中的 `exact_primal_verified=true` 只说明这个受限线性系统的有理点通过了矩阵检查；它不说明该点对应真实客户实例、完整历史纯 SPE 或福利结论。

结果报告的浮点目标为 `2.0391979934373885`，有理目标为
`301904989188813053163805000409977755377 / 148050846538890923800466562791232658950`。旧冻结点在新增背景行上最小松弛为负，最违反行是 `S3_indexed_background:C6:D7`；这说明旧点不能直接承受这组附加约束。报告同时明确 `game_SPE_witness=false`、`universal_bound=false`、`full_domain_dual_certificate=false`。

可复用内容是“在已冻结有限支持上追加背景行、先浮点找点再有理恢复”的诊断流程，以及旧点被新行排除的具体坐标。边界是支持仍只有64个原子，原437行和新增背景行来自既有固定模型；没有把所有客户类型、所有历史偏离、整数重数、SPE策略或六人半覆盖量词纳入。后续若要升级，必须先证明支持完备，再把矩阵约束与真实游戏收益和完整有序历史逐项对应，最后才可讨论主问题。
