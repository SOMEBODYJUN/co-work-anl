---
agent: Boss6/clean_seven_state_canonical_v1
source_id: "ee0deff479cc5c374543"
source_sha256: "691da049257e25486139214a923f4f4908a61df14ca6034caea0c3cbc86f3765"
source_path: "history/source/notes/unrelated_machines/sol_seven_state_star_global_quadratic_canonical_v1.md"
review_status: "full-source-read-and-related-material-checked"
recommended_disposition: "integrated"
---

# 来源 ee0deff479cc5c374543：七态原星 global quadratic canonical v1 处置草稿

## 1. 来源身份与实际阅读

通过 `clean show ee0deff479cc5c374543 --out ...` 导出并逐段实读冻结源 `sol_seven_state_star_global_quadratic_canonical_v1.md`，大小 7683 字节，SHA-256 `691da049257e25486139214a923f4f4908a61df14ca6034caea0c3cbc86f3765`；legacy-cleanup 与 main 两个冻结提交均指向同一 blob `da06360deac361c9e593f6307c7d3e72f516a079`。

来源自述为 2026-10-18 scratch 正文草稿，稳定 ClaimVersion 为 `UM-SEVEN-STATE-STAR-GLOBAL-QUADRATIC-LOCAL-v1`。它给出一个实际 OPT=1 的 d+2 台机器、d+1 个不可拆 job 的七态原星，构造同一真实完整 assignment law P，证明共同 M3、所有全局 degree≤2 负载平方 localizer、逐行合法 CONFIG first/pair；同时明确不声称递归接线、near-two gap、hardness 或一般调度算法。

## 2. 精确数学内容

参数为正偶数 `d,s` 且 `2≤s≤d/2`，`eta=s/d`、`h=s/2`、`T=1+eta`、`p=eta^3/1000`，机器 `u,v,z_1,...,z_d`，job `R,j_1,...,j_d`；R 在 u/v 端时间 1，每个 j_l 在 v 端时间 1/d、在 z_l 端时间 1。令 C 表示 R 在 v，Y_l 表示 j_l 在 v，H=ΣY_l。源给出七个 `(C,H)` 类别的精确质量，其中唯一超 T 的类别是 `(1,d)`，峰值为 2，真实 home assignment 给 OPT=1。

共同 assignment law P 的所有次数≤3 矩满足同一 M3 PSD、Boolean 和每个原 job one-hot；所有全局二次 q(X) 均通过对 home 标签置换平均化后写成 `P(H)+C(a+bH)`，以 active/inactive affine relation 和 Cauchy 控制唯一负 slack 类别，得到每台机器 `L[(T-load_i)q^2]≥0`。v 行的 alternate configuration distribution K_v 将 active bad 质量从 H=d 调至 H=s、由 inactive H=d/2 分流到 H=0,d，使 C,H,CH 和全部 first/pair 精确保留；u 与各 z_l 的 Bernoulli 行本身即为合法 CONFIG law。

源还给出外部背景合同：若所有原 assignment 指示都仿射写成 `Phi_b(C,Y)`，且 v 的可见 job 结构不变、没有新增 payload，则 v 行的局部化与 pair trade 可逐背景继承；其他行和新增 payload 必须另行核验。示例固定 payload `b0>eta` 在 z_l 立刻由 q=1-Y_l 造成负 localizer，说明不能免费递归扩展。

复杂度声明是显式二进制有理输入上的固定次数矩精确生成，未调用 SDP/优化 oracle。附带的 Fraction 审计只覆盖 12 参数组，前三组有完整 high-dimensional M3/global-q2，root fresh output 与作者输出逐字节一致；有限审计不代替任意 d,s 证明，也不检查 growing-depth 连接。

## 3. 与现有仓库对象比较

我核对了：

- `cleanup/workspaces/Boss6/CLAIMS.md` 的 `UM-SEVEN-STATE-STAR-GLOBAL-QUADRATIC-LOCAL-v2`、`UM-UNIFORM-CARDINALITY-PAIR-SPARSE-SUPPORT-v1`、`UM-SEVEN-STATE-STAR-AFFINE-BOOLEAN-BOUNDARY-v1` 和 `UM-SEVEN-STATE-STAR-AND-GATE-LOCALIZER-OBSTRUCTION-v1`；
- `archives/unrelated-machines/state/审查/七态星全局二次审计与root重放范围审查--审查.md`；
- `archives/unrelated-machines/state/计算/七态星全局二次审计与root重放边界--计算.md`；
- first/pair 独立对象与 affine/AND 分域审查。

当前 v2 ledger 是在 v1 原星合同上增加 first/pair 稀疏 support、版本边界及更完整的 extension wording；它没有否定 v1 的局部核。现有 finite-audit review 已把 v1/v2 的 12 组有限结果与任意参数解析合同分开，但此前没有把本 v1 canonical source 本身列入其 `source_refs`。本来源的独有去向是 v1 主证明的原始版本/参数合同与其“不免费接 payload / 不递归”的明确反例边界；不应另造 affine 或 AND 对象，也不应把有限审计升级为一般软件证明。

## 4. 建议正式对象与处置

建议 `integrated`，不标 duplicate：这是 global-quadratic stable ID 的 canonical v1 数学源，当前 archive 中已有审查/计算对象但缺少独立的定理正文落点。将源正文保留为：

- `archives/unrelated-machines/state/定理/七态原星全局二次负载局部核--定理.md`（v1 精确合同；frontmatter stable id `unrelated-machines/seven-state-star-global-quadratic-local`，legacy id `UM-SEVEN-STATE-STAR-GLOBAL-QUADRATIC-LOCAL-v1`）；
- 更新 `archives/unrelated-machines/state/审查/七态星全局二次审计与root重放范围审查--审查.md` 的 `source_refs`，加入两冻结提交下的 v1 source；
- 更新 `archives/unrelated-machines/state/计算/七态星全局二次审计与root重放边界--计算.md` 的 `source_refs`（审计证据仍是有限运行）；
- 保留现有 v2 Claim 与 sparse/affine/AND 分域边界，不把 v1 文件改写为 v2 全部结论。

建议 receipt：

```json
{
  "id": "ee0deff479cc5c374543",
  "full_file_reviewed": true,
  "related_material_checked": true,
  "unique_content_accounted_for": true,
  "read_note": "完整读取7683字节七态原星 global quadratic canonical v1；核对 d,s 量词、真实 assignment law、共同M3、global degree≤2负载localizer、逐行CONFIG first/pair、背景合同、payload反例和12组有限审计边界。",
  "comparison_note": "与现有 v2 CLAIM、first/pair sparse theorem、affine/AND 分域审查、七态有限审计及 root replay 逐项比较；v1 是主证明的原始 canonical 版本，v2 扩展边界但不改变 v1 局部核。",
  "decision_note": "将 v1 source 整合为独立定理正文并把其来源加入审查/计算对象；保留 actual OPT=1、有限 audit、无递归/无hardness/无一般UM算法边界，不把 v1/v2 或 affine/AND 合并成一个超范围结论。",
  "disposition": "integrated",
  "targets": [
    "archives/unrelated-machines/state/定理/七态原星全局二次负载局部核--定理.md",
    "archives/unrelated-machines/state/审查/七态星全局二次审计与root重放范围审查--审查.md",
    "archives/unrelated-machines/state/计算/七态星全局二次审计与root重放边界--计算.md"
  ]
}
```
