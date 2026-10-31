---
id: "unrelated-machines/one-outer-13-8-and-primitive-sa1"
kind: "algorithm-review"
type_tag: "资料"
title: "one-outer 13/8 与 primitive-SA1 同点后端"
status: "proved-under-explicit-single-outer-scope"
summary: "两份 Exact-first 记录分别给单 outer normalized-flat primitive-SA1 的 13/8 全有理 LP/grid/CDF-max 算法，以及 full primitive-SA1 下 ε²/4 welfare 后端与完整 jobs 回填；均严格限单 outer、独立 helper homes 和显式状态，未扩 multi-outer/general UM。"
source_refs:
  - "clean:04b3653d65dbfd764651"
  - "clean:1152906268a5a586771b"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_one_outer_primitive_sa1_exact_first_reconstruction.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_one_outer_13_8_exact_first_reconstruction.md"
---

# 来源身份与范围

本页合并两份相邻但不同身份的 Exact-first 记录：primitive-SA1 给定点 backend，以及 one-outer 13/8 新 Exact。两者共享“一个 outer、所有 helper 独立 own home、B-only fallback、显式 normalized-flat”域，但 welfare 常数和 LP/grid 输入不同；未把它们合并成一个更强 theorem。

| clean ID | 原路径 | SHA-256 | 大小 | 实读性质 |
|---|---|---|---:|---|
| `04b3653d65dbfd764651` | `history/source/notes/unrelated_machines/sol_one_outer_primitive_sa1_exact_first_reconstruction.md` | `419df2115facfc2b8cbd976d7f3a3a94fed2dc707ab915f34be10f5d19c8ca94` | 10,911 B | full primitive-SA1 给定点的 ε²/4 welfare reconstruction |
| `1152906268a5a586771b` | `history/source/notes/unrelated_machines/sol_one_outer_13_8_exact_first_reconstruction.md` | `399c6b29f54b1c0f49ee21e3ef64552edc1fec21fe09579a4dd91eecb5fe710f` | 11,188 B | 13/8 新 Exact 的 LP grid、5/8 CDF-max 与全 jobs 回填 |

证据原件和 manifest 位于 `archives/unrelated-machines/tools/evidence/one-outer-exact-20261031/`，回执草稿在 `cleanup/workspaces/Boss2/one-outer-exact-receipts-20261031.json`。

# 1. primitive-SA1 给定点：ε²/4 后端

在 full primitive-SA1 合同下，原 primitives A_s、Z_e 有共同一/二阶数组 Y；box、gate、resource、state value rows 及补乘子全在同一点。Singleton helper own-state 先用 gate/value rows 和补乘子推出 `μ_h=μ_z=Y_hz`，再乘任意 primitive/complement 得 `Y_rh=Y_rz`。这一步只用二阶，不调用 triples。

选任一 outer state a、正 marginal ρ，条件在 r=A_M,a。定义 outer home claims u_j、helper fallback masses α_js、claims ζ_jsu、fallback mass τ_j。共同 Y 给

`sum_j w_j u_j ≥ ε`，
`τ_j≥u_j`，
`sum_u p_jsu ζ_jsu ≥ ε α_js`，
`sum_{j,s} ζ_jsu≤1`。

由同一 r 行得到 fractional welfare benchmark `W_frac≥ε²`。再用独立 helper virtual state experiment、有限 score levels 和 Bonferroni `Pr[max score≥d]≥q(d)/2`，通过 exact conditional expectation 固定每个 helper state；最后每个 resource 给 chosen clause score 最大 helper，得到不交 B bundles 且 weighted welfare≥ε²/2。令 Good helpers quality≥η=ε²/4，weight lower bound≥η；outer 取 Good homes，其他所有 groups 回 own homes，完整 ordinary P 回填 selected incidences，得到 Cmax≤2−ε²/4。

后端只需显式 states、rational Y、有限 sums/division，未调用 general XOS/CONFIG/SDP oracle；域仍为 single outer 和独立 helper homes。多 outer、共享辅助 core、degree-four PSD 不在范围。

# 2. one-outer 13/8：固定 LP grid 和 5/8 welfare

给定显式 Q，生成完整 ordinary P（S+U machines、G+I jobs、含 zero incidences/duplicate states/unused resources）。`OPT(P)=2−v`，v 是菜单最小 value；selected-state bundle 回填给上界，C<2 反向给 bundle value≥2−C。

枚举 ε=k/128、k=1,…,128。原 primitives A_gs、Z_gsu 建 shared symmetric second-order Y，加入 state partitions、boxes、Z≤A、resource capacity、state value rows；每基行及每 primitive 的 positive/complement multiplier 线性化为 LP 行。LP variable O(N²)、rows O(N(N+U))，所有 coefficients rational。若 ε≤v，取 actual attaining states/0-1 claims 得 LP 可行；保留最大 feasible grid ε_hat。若无正 grid feasible，输出 all-private C≤2；若 v≥1/128，则 ε_hat≥v−1/128。

对给定点先条件一次正 outer state r。与 primitive-SA1 相同的 singleton identity、helper masses、fallback claims 和 resource columns 给 `W_frac≥ε_hat²`。新 welfare backend 用有限 CDF-max：对每 resource/score level，helper exceedance probabilities β_j 总和 q≤1；AM-GM 和二项式下界给

`Pr[max score≥d]≥(5/8)q`。

固定 helper states 前用 exact conditional expectation，选取有限 rational candidate；最终按 chosen clause score 最大资源归属输出不交 bundles，得到 `S=sum w_j q_j ≥(5/8) ε_hat²`。所有 operations 是 finite rational arithmetic，不计算 e、sqrt 或 unknown v。

将输出 q_j 做 threshold scan：对每 distinct t，R_t={j:q_j≥t}、W_t=sum weights、Q_t=min(t,W_t)，取最大 Q_t。若 `S≥h(2−h)`，则某 threshold set weight≥h；算法不需要知道 h。若 v≤10/13，C≤2 已满足 13/8 ratio；若 v>10/13，令 h=(13v−10)/8，恒等式

`(5/8)v²−h(2−h)≥1/64`

和 ε grid δ=1/128 给 S≥h(2−h)+3/512，故 output quality≥h，C≤2−h=(13/8)(2−v)=(13/8)OPT。

# 3. 完整 jobs、位复杂度和限制

两份记录都要求：selected selector 放原 selected state root；仅导出 selected-state 正 incidences；所有 unselected states、zero jobs、duplicate states 和其余 payload 留原 private roots；resources 至多一 unit job。LP 数、CDF candidates、threshold scan、matrix dense output 和 all-job回填均按显式 Q 的总 bit length 多项式，不按权重倒数、1/ε 或 state combination 数展开。

primitive-SA1 记录只在给定 full primitive-SA1 point 上论证 ε²/4；13/8 记录新增 128-grid LP 生成和 5/8 backend。二者都不证明：

- 多 outer、重合 homes、无 home 的 auxiliary groups 或一般 non-UD extras；
- general UM approximation、source hardness、native canonical-C2 或 all-machine near-two；
- 任意 rational SDP/CONFIG point 的自动寻找以外的外部 oracle；
- 作者程序、软件端到端执行或全球新颖性。

# 本轮实际处置

两源均完整 clean show 实读，比较了给定点 ε²/4 与新 13/8 的 LP/grid、CDF-max、threshold、complete matrix 和 scope。没有运行代码；原件和 manifest 在 evidence，正文归档为资料，回执草稿单列。
