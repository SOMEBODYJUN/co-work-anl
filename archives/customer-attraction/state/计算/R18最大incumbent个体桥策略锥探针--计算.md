---
id: "customer-attraction/r18-largest-incumbent-individual-bridge-probe"
kind: "computation"
type_tag: "计算"
title: "R-18 最大 incumbent 个体桥策略锥探针"
status: "finite-search-run-record"
truth_status: "finite cone search; no universal bridge conclusion"
review_level: "full-5627-byte-read-and-20-step-replay"
scope: "m=5,p=7 incumbent individual OPT/(2m-1) probe; seed 68111"
source_refs:
  - "clean:7e9097841e9839162c50:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/global_proof/largest_incumbent_probe.py"
  - "local:archives/customer-attraction/state/计算/R18完整SPE策略锥walk有限候选--计算.md"
  - "local:archives/customer-attraction/state/反例/R18最大incumbent个体桥有限反例--反例.md"
  - "local:archives/customer-attraction/state/反例/三人调和势最优增量的完整策略证书--反例.md"
source_identity:
  inventory_blob: "8a4792f1686b2d333e35dd226fc7d9e466af2107"
  source_sha256: "24ef0170b318beb6411bbeec2f988c38bdf57443fc48a361edeac464f97a16b0"
  source_size_bytes: 5627
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/original/largest_incumbent_probe.py"
  - "archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/replay/largest_incumbent_probe.stdout"
  - "archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/replay/largest_incumbent_n5p7_run.json"
  - "archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/replay/largest_incumbent_n5p7_best.json"
  - "archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/comparisons/7e9097841e9839162c50.md"

# R-18 最大 incumbent 个体桥策略锥探针

## 程序目标

完整实读 5,627 字节 Python。程序基于 `cone_walk.Engine`，对 `m=5,p=7` 的完整有序历史 SPE 策略锥构造浮点 LP 提案，再用 Fraction 活跃行恢复客户整数重数并调用 `verify_canonical`。目标值是一个动作 `a` 的 `OPT/u_a`；阈值为 `2n-1=9`，达到或超过阈值才可能触发个体桥障碍。

搜索会固定若干 baseline/层化重叠 seed，并在有限步中从 LP endpoint 扩展；它不是全部客户质量、全部策略或全部支持的穷举。浮点 recovery 失败的提案只打印 `unrecovered`，不被当作反例。

## 实际重放

本次以 `--players 5 --topics 7 --steps 20 --seed 68111` 运行。第 0 步恢复一个 exact ratio `9`，之后到第 10 步仍未超过 9；run JSON 保存有限 records、cone 行数、portfolio 和 elapsed，best JSON 保存该 exact candidate。stdout 首行报告 `new_exact_best=9`，最终 finite best 为 9，恰等 `2n-1`，没有产生严格违反。

由于本次运行截取 20 steps，而源默认上限为 200，不能把“未超过 9”写成默认完整搜索结论。即使默认运行也只覆盖固定 seed/策略锥有限队列；它不会证明个体桥或 half。

对象处置为 integrated 的有限探针记录，与三人精确反例和 R-18 cone walk 互相比较；不迁移到 unrelated-machines。
