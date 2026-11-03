---
id: customer-attraction/r18-largest-incumbent-individual-bridge-probe
kind: computation
type_tag: 计算
title: R-18 最大 incumbent 个体桥策略锥探针
status: finite-relaxed-search-record;root-IC-omitted
truth_status: rational-recovery-checks-only-subgame-IC-and-size-cone; no-completeSPE-certification
review_level: old-full-read-and-20-step-replay-retained;later-root-omission-corrected
scope: m=5,p=7 incumbent individual OPT/(2m-1) probe; seed 68111
source_refs:
- clean:7e9097841e9839162c50:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/global_proof/largest_incumbent_probe.py
- local:archives/customer-attraction/state/计算/R18完整SPE策略锥walk有限候选--计算.md
- local:archives/customer-attraction/state/反例/R18最大incumbent个体桥有限反例--反例.md
- local:archives/customer-attraction/state/反例/三人调和势最优增量的完整策略证书--反例.md
- local:archives/customer-attraction/state/审查/最大incumbent候选的根激励遗漏与错误认证--审查.md
source_identity:
  inventory_blob: 8a4792f1686b2d333e35dd226fc7d9e466af2107
  source_sha256: 24ef0170b318beb6411bbeec2f988c38bdf57443fc48a361edeac464f97a16b0
  source_size_bytes: 5627
evidence_paths:
- archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/original/largest_incumbent_probe.py
- archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/replay/largest_incumbent_probe.stdout
- archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/replay/largest_incumbent_n5p7_run.json
- archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/replay/largest_incumbent_n5p7_best.json
- archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/comparisons/7e9097841e9839162c50.md
---

# R-18 最大 incumbent 个体桥策略锥探针

## 程序目标

完整实读 5,627 字节 Python。程序基于 `cone_walk.Engine`，对 `m=5,p=7` 的固定形式策略构造浮点 LP 提案，再用 Fraction 活跃行恢复客户整数重数。关键修正：程序随后自行重建 G 时跳过空历史根节点，只保后继 IC 和最大主题容量；虽然 import 了 `verify_canonical`，全文并未调用它，best 中 `verified:true` 直接硬编码。因此这不是完整 SPE 策略锥或定义级全树认证。目标值是一个动作 `a` 的 `OPT/u_a`；阈值为 `2n-1=9`，严格超过阈值也仅产生待完整根 IC 核验的候选；等号本身不违反桥。

搜索会固定若干 baseline/层化重叠 seed，并在有限步中从 LP endpoint 扩展；它不是全部客户质量、全部策略或全部支持的穷举。浮点 recovery 失败的提案只打印 `unrecovered`，不被当作反例。

## 实际重放

本次以 `--players 5 --topics 7 --steps 20 --seed 68111` 运行。第 0 步恢复一个 exact ratio `9`，之后到第 10 步仍未超过 9；run JSON 保存有限 records、cone 行数、portfolio 和 elapsed，best JSON 保存该 exact candidate。stdout 首行报告 `new_exact_best=9`，最终 finite best 为 9，恰等 `2n-1`，没有产生严格违反。

由于本次运行截取 20 steps，而源默认上限为 200，不能把“未超过 9”写成默认完整搜索结论。即使默认运行也只覆盖固定 seed/策略锥有限队列；它不会证明个体桥或 half。

对象处置为 integrated 的有限探针记录，与已撤回SPE认证的三人旧候选和 R-18 cone walk 互相比较；不迁移到 unrelated-machines。

后续实质纠错见[根激励遗漏审查](../审查/最大incumbent候选的根激励遗漏与错误认证--审查.md)：同源三人 best 恰有五个根盈利偏离。这里保过去20-step运行及原stdout/JSON，不重跑、不否定其数值记录，但这些松弛锥PASS/比9不能当完整SPE或普遍桥证据。
