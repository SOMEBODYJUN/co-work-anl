---
id: "unrelated-machines/cartesian-tensor-reverse-actual-audit-20261031"
kind: "review"
type_tag: "审查"
title: "裸 Cartesian 张量反向放大独立实际稀疏审计"
status: "retained-finite-audit"
truth_status: "finite-t1-exact-and-t1-to-t4-sparse-witness-only"
review_level: "full-source-read-and-finite-audit-scope-comparison"
summary: "完整阅读 Cartesian tensor 反向放大的独立 actual sparse-P audit 记录。它核对 t=1..4 的完整原 jobs、稀疏资源交点、互补 pair、规模和 schedule；仅 t=1 直接枚举 1024 个完整 assignments 得 OPT=3/2，t≥2 只核给定 witness，不优化。该证据不能升级为任意 t 的一般反向放大定理、源硬度或一般 unrelated-machines 结论。"
source_refs:
  - "source:f6b0d365e20cb43d93c1:history/source/notes/unrelated_machines/tensor_reverse_actual_audit_review.md"
legacy_ids:
  - "UM-CARTESIAN-TENSOR-REVERSE-ACTUAL-AUDIT-v1"
related_objects:
  - "unrelated-machines/bare-cartesian-menu-reverse-amplification-counterexample"
  - "unrelated-machines/ternary-palette-v2-source-review"
---

# 1. 来源、代码身份与审计级别

`clean show` 导出的来源 `f6b0d365e20cb43d93c1` 为
`history/source/notes/unrelated_machines/tensor_reverse_actual_audit_review.md`，5,377 bytes，SHA-256 `55041afcaa86bf12918f76085449b881a08bad0814cbcd1ba4173069f62508f4`。本页逐段阅读并将原文保存到
`archives/unrelated-machines/tools/evidence/tensor-reverse-actual-audit-20261031/original/`。

来源明确分类为 `audit_only`：未读取作者 Proof，只使用 root 授权的循环 witness `ell_i(g)=g_(i+1)`，不冒称独立发现见证；有限运行不能替代任意 `t` 的一般证明，也不认证其它 tensor/source/compiler。

# 2. 稀疏普通 UM 输入与完整 jobs 口径

对 `t=1,2,3,4`，令 `D=2^t`，独立枚举全部资源 tuples `U^t`，由真实检查

\[
b_i+g_i a_i=\ell_i(g_i)\pmod 2
\]

筛出支持。输出保留全部 resource/private machines、selectors、每个 indexed state 的全部 incidence jobs 及全部有限 processing entries；未选 state 的 incidence jobs 仍留在 private，未使用资源也保留。时间统一为整数单位 `1/D`：private incidence 为 1 unit，selector/resource 为 `D` units；审计禁止 float。

每个资源 tuple 只对应一个全局 resource ID，不把同一资源按 incidence 私有化。`t=1` 的四个 base supports 另与 Exact 硬编码集合对照。all-jobs schedule JSON 逐 job 核对唯一目的机、原 processing time、整数 start/end、不重叠、全机峰和总 job 计数。

# 3. 有限运行结果与精确计数

审计给出的有限统计为：

| `t` | groups | state/private | resources | jobs | finite entries | `D` | witness peak (units) | ordered complementary pairs |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 4 | 4 | 10 | 20 | 2 | 3 | 8 |
| 2 | 4 | 16 | 16 | 68 | 144 | 4 | 5 | 64 |
| 3 | 8 | 64 | 64 | 520 | 1088 | 8 | 9 | 512 |
| 4 | 16 | 256 | 256 | 4112 | 8448 | 16 | 17 | 4096 |

逐组 exports 为 `1,3,7,15`，使用资源数为 `2,12,56,240`，unused 资源数为 `2,4,8,16`。规模恒等式为 groups `D`、states/private/resource machines `D²`、incidences `D³`、selectors `D`、finite entries `2D³+D²`；dense 物化项分别为 `80,2176,66560,2105344`，审计使用 sparse 表，不把未写项计作 finite。

选中 state 恰留一个 all-ones incidence，故 witness 峰为 `D+1` units；未选 state 的 `D` 枚 incidence 各自 private，使用 resource 各承载一枚 unit。所有原 selectors 与 payload 真实执行。

# 4. 互补交点与 t=1 的完整实际优化

`tN_all_complementary_intersections.json` 枚举全部有序 `g, complement(g), ell, ell'`，共 `D³` 项，反向 unordered pair 也保留；每条交点从实际 P 支持取集合，要求恰一个真实资源，并与独立坐标解核对。

仅 `t=1` 调用 `exhaustive_t1_actual_opt`：从完整 ordinary P 的每 job 全有限端取 Cartesian product，共 1024 个完整 assignments，逐机累加原 processing times，得到 exact `OPT=3` units，即 `3/2`。函数对 `t≠1` 明确拒绝；`t=2,3,4` 没有 brute-force optimum，只核给定 all-jobs witness、互补 pair 和 schedule 合法性。

因此可以确认的数学内容是：四个具体 sparse-P 实例的 all-jobs witness、资源/资格/交点/规模检查通过，且 t=1 有独立完整优化值 `3/2`。不能把 witness mass `(D−1)/D` 与 peak `(D+1)/D` 的有限模式写成所有整数 `t` 的定理。

# 5. 与旧对象的关系与未完成范围

《裸菜单读后与保值降度及调色板障碍》以及《裸 Cartesian 菜单乘积的精确反向放大》已承载原 Exact/Proof 与一般对象范围；本源独有的是一次实际 sparse-P audit 的全 job 输出、t=1 完整 optimum 枚举、t=2..4 witness-only 明示、代码/manifest/summary hash 和稀疏规模表。三叉 palette tensor v2 是不同模型，不能因都写 tensor/cartesian 就合并为“所有张量失败”。

本源没有作者 Proof 读取、没有任意 t 的一般 compiler、没有 t≥2 optimum 搜索、没有 polynomial-in-t claim（输出按显式矩阵规模计费）、没有源 hardness、NP/UGC、新颖性或一般 unrelated-machines 算法。后续若接入障碍图，必须把边标成“有限 audit → bare Cartesian reverse object”，不能将 t=1 的 `3/2` 自动提升为递归或一般下界。

# 6. 处置

处置为 **retained-finite-audit**：原文证据、代码与运行 hash 指针保全为审计范围记录；正式正文只写实际读取、有限结果、独有内容和不可外推边界，不新建一般数学主定理。
