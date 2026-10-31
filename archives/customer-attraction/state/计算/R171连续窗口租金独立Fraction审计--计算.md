---
id: "customer-attraction/r171-continuous-window-rent-independent-audit"
kind: "computation"
type_tag: "计算"
title: "R-171 连续窗口租金独立 Fraction 审计"
status: "finite-exact-audit-passed"
truth_status: "finite interval identity and sparse-boundary checks; universal proof remains in review"
review_level: "full-3382-byte-read-and-exit0-replay"
scope: "Binary paths; exhaustive interval choices m<=6; 500 seeded random cases; sparse future-window boundary"
source_refs:
  - "clean:6f3b610d73444dbb7e17:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/parent/audit_interval_independent.py"
  - "local:archives/customer-attraction/state/引理/R-171连续窗口与固定人口pair误差预算--引理.md"
  - "local:archives/customer-attraction/state/引理/R-171稀疏槽clock租金与skip-premium分解--引理.md"
  - "local:archives/customer-attraction/state/反例/R-171完整SPE稀疏槽租金障碍--反例.md"
source_identity:
  inventory_blob: "ea1495b0346963ac524c145d7725a289a9fdcbc8"
  source_sha256: "66b4fdd70998e104956e828b9535941c142419c6df4bff614c43b26f9ecd0ea1"
  source_size_bytes: 3382
evidence_paths:
  - "archives/customer-attraction/tools/evidence/interval-rent-independent-20261031/original/audit_interval_independent.py"
  - "archives/customer-attraction/tools/evidence/interval-rent-independent-20261031/replay/audit_interval_independent.stdout"
  - "archives/customer-attraction/tools/evidence/interval-rent-independent-20261031/replay/interval_independent_audit.json"
  - "archives/customer-attraction/tools/evidence/interval-rent-independent-20261031/comparisons/6f3b610d73444dbb7e17.md"

# R-171 连续窗口租金独立 Fraction 审计

## 定义级核验

完整实读 3,382 字节脚本，SHA-256 `66b4fdd70998e104956e828b9535941c142419c6df4bff614c43b26f9ecd0ea1`，blob `ea1495b0346963ac524c145d7725a289a9fdcbc8`。`verify` 对二值客户命中路径 `bits`、第 `j` 行长度 `length`、权重 `theta` 和 reserve `rho` 同时计算窗口原式与按客户真实 hit rank 分配的式子，精确核对 `raw == allocated`，并检查
\[
 0\le raw\le cap=\Gamma\left(\frac1{\rho+1}-\frac1{\rho+ c}\right)
 \le \frac{\Gamma\,1_{c>0}}{\rho+1}.
\]
这里 `Gamma` 是窗口槽位拥塞 `max_t sum_{j:t in I_j} j theta_j`，不是事后按客户调整的常数。

程序先穷举 `m=1..6` 的全部二值路径、所有区间长度、`rho=1/3,1,5/2`，奇数行取 `theta_j=1/j`、偶数行取 `2/(3j)`；再用固定 seed `171021` 生成 500 个 `m=2..44` 随机路径/区间/有理权重/reserve。实际复跑 exit 0，输出 `cases=151586`（包含 exhaustive 与 random），JSON 和 stdout 保留在 evidence `replay/`。

## 稀疏未来边界

脚本额外构造 `bits=[1,0^{q-1},1^q]`，`q=1,2,3,8,64`，每个未来槽只使用一次，核对实际 raw cost 为 `H_q/6`，而连续窗口 cap 为 `1/2-1/(q+2)`。差值分别为：`q=1,2` 为 0，`q=3` 为 `1/180`，`q=8` 为 `89/1680`，`q=64` 为
\[
 \frac{241024808065020614604384539}{788177922735214845007574400}>0.
\]
另用相邻窗口 `bits=[1,0,1,0]`、`lengths=[2,2,0]`、`theta=[1,1/2,0]`、`rho=1` 核对 `raw=1/4`、`cap=1/3`，说明 rank-2 的直觉加强不能直接成立。

## 边界和关系

这份程序支持连续窗口租金恒等式的定义级有限证据，并把稀疏未来单槽违反连续窗口 cap 的方向展示为 exact Fraction 反例。它不替代 `R-171连续窗口与固定人口pair误差预算` 中的普遍按 hit-rank 证明；同样也不构成完整 SPE 全树运输。与 `R-171稀疏槽clock租金与skip-premium分解` 合看，连续窗口可以收费，跳过实际 hit 的 reset premium 不能自动删除；本脚本只审计旧群体租金的窗口/分配恒等式。

对象处置为 integrated 计算记录。有限结果不能升级为一般 payment bridge、Q-CAG-HALF 或 unrelated-machines 结论。
