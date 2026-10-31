---
id: "unrelated-machines/seven-state-and-gate-localizer-obstruction-exact-v1-review"
kind: "review"
type_tag: "审查"
title: "七态 AND 端点二次 localizer Exact 量词与障碍范围审查"
status: "integrated-exact-scope"
truth_status: "statement-only-scoped-faithful-and-obstruction"
review_level: "full-source-read-cross-object-comparison"
scope: "七态原星 faithful AND 新 endpoint、base≤5/共同 M3/次数六矩合同、q=Z(H−h) 负 load-localizer 与物理/算法边界"
summary: "完整读取 Exact-only 来源并和 7ccd 作者 read-after、既有七态全局二次审查及 affine owner 对象去重。Exact 只陈述在明确忠实 AND 与 base≤5 合同下 q=Z(H−h) 使 v 行局部化严格为负；不登记一般非仿射失败、算法、hardness 或 near-two gap。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_seven_state_and_gate_localizer_obstruction_exact_v1.md"
  - "clean:89318ccee567ab05e1cd"
  - "related-source:7ccd86160f25544a1e74:history/source/notes/unrelated_machines/sol_seven_state_and_gate_localizer_obstruction_author_read_after.md"
  - "related-source:35c3d73eecc8a450aedb:history/source/notes/unrelated_machines/sol_seven_state_and_gate_localizer_obstruction_author_proof_v1.md"
related_objects:
  - "七态AND端点二次localizer作者read-after审查--审查.md"
  - "七态原作业星GlobalQuadratic Exact与审计延拓边界审查--审查.md"
  - "七态星全局二次审计与root重放范围审查--审查.md"
  - "七态原星仿射Boolean所有者边界Exact与作者Proof版本审查--审查.md"
  - "鲁棒双端环与七态二次局部核双源审查--审查.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/seven-state-and-gate-localizer-exact-v1/original/sol_seven_state_and_gate_localizer_obstruction_exact_v1.md"
---

# 来源身份与 Exact-only 角色

本页处理 clean source `89318ccee567ab05e1cd`，原路径为 `history/source/notes/unrelated_machines/sol_seven_state_and_gate_localizer_obstruction_exact_v1.md`，冻结 blob 为 `d30eb76a6d73548036546fbb3ffb13fffbc6e45b`，源 SHA-256 为 `8ca3b942276658319808f3c32d5057b53611555d76bfbf6f4c5f94ea18e511ab`，大小 3,070 B。原字节已复制到 `evidence_paths`。

来源的 ClaimVersion 是 `UM-SEVEN-STATE-STAR-AND-GATE-LOCALIZER-OBSTRUCTION-v1`。它是 2026-10-18 的 scratch statement-only 候选，明确未独审、未登记，并强调它使用 `base≤5` 合同，与 affine owner 的 `base≤4` 分类对象分开。作者 Proof `35c3d73eecc8a450aedb` 和作者 read-after `7ccd86160f25544a1e74` 是独立来源；本页只处理 Exact 字节和其独有量词，不把未在本批导出的 Proof 先验改写成 Exact 的盲审或软件证据。

处置为 **integrated-exact-scope**：将该 statement-only 障碍接入已有 faithful-AND read-after 与七态全局二次对象的证据链，明确它是一个窄合同下的负 localizer，而非一般延拓不可能性定理。

# 1. 七态基础 law 与物理读法

取正偶数 `d,s`，满足 `2≤s≤d/2`，令

\[
\eta=s/d,\qquad h=s/2,\qquad T=1+\eta,
\qquad p=\eta^3/1000,
\]
\[
u_0=4p(1-\eta),\qquad e=4/5-p-u_0.
\]

于是 `0<η≤1/2`、`1≤h≤d/4`。`P` 在 `(C,H)` 七类上给出下表质量，类别内均匀选择 H 个不同索引令对应 `Y_j=1`：

| C | H | 质量 |
|---:|---:|---:|
| 1 | d | `p` |
| 1 | 0 | `1/20` |
| 1 | h | `1/20` |
| 0 | 0 | `1/20` |
| 0 | h | `1/20` |
| 0 | d/2 | `u0` |
| 0 | d | `e` |

所有七类质量为正。基础原星的 v 行负载为

\[
\mathrm{load}_v=C+H/d,
\qquad g=T-C-H/d.
\]

原 physical read 是：unit job `R` 可在 `u/v` 两端各用时间 1；原 jobs `j=1,…,d` 可在 `v` 用 `1/d` 或在不同 private `z_j` 用 1；`C,Y_j` 分别表示其在 v 上的原 endpoint。当前 Exact 只讨论新端点扩展时 v 的负载公式必须保持不变，不添加隐式逻辑约束到普通 UM eligibility。

# 2. Exact 精确量词与共同矩合同

固定任意 `i∈[d]`。`Z` 必须是新增原 endpoint 的 degree-one 指示变量，或明确声明的新增 Boolean 坐标；已有 degree-two 多项式 `CY_i` 不能只改名后按 degree one 计数。

`Lhat` 是所有相关变量次数≤6 多项式上的同一个实线性泛函，并要求：

1. `Lhat(1)=1`，次数≤3 monomial 组成的共同 `M3(Lhat)` 为 PSD；
2. 对只含 `C,Y` 且次数≤5 的多项式 `r`，`Lhat(r)=E_P[r]`；
3. `Z` 和所有原 endpoint 的 Boolean 等式、原 jobs one-hot 等式支付到总次数 6，特别 `Z²=Z` 的乘子等式支付到次数 5；
4. 忠实 AND 的二次 Gram 等式
   \[
   Lhat[(Z-CY_i)^2]=0.
   \]

对全局原变量二次多项式

\[
q=Z(H-h),
\]

Exact 的严格断言为

\[
Lhat[gq^2]=-p(1-\eta)(d-h)^2<0.
\]

因为 `deg(q)=2`、`deg(g)=1`，所以 `gq²` 的总次数为 5，落在 `Lhat` 的次数≤6 定义域中。该严格负值与“v 行对全部 `deg(q)≤2` 的负载局部化均非负”直接冲突；不需要额外假设原行 CONFIG first/pair，加入这些约束也无法消除已经出现的负 localizer。

# 3. 独立精算：Gram AND 到负 localizer

令

\[
D=Z-CY_i,
\qquad B=g(H-h)^2.
\]

`D` 是 degree 2 的共同 M3 null vector。由 PSD 的 Gram-null 正交性，`Lhat(DR)=0` 对任意 `deg(R)≤3` 成立。`B` 的次数为 3，因此可取 `R=B`。另一方面，`Z` 的 Boolean 乘子等式允许在总次数 5 内把 `Z²` 替换为 `Z`：

\[
Lhat[gZ^2(H-h)^2]=Lhat[gZ(H-h)^2].
\]

用 `R=B` 的 null 正交性，再将 `Z` 替为 `CY_i`，得到

\[
Lhat[gZ(H-h)^2]=Lhat[gCY_i(H-h)^2].
\]

右侧只含 `C,Y` 且次数≤5，因而由 base≤5 匹配合同等于 `E_P[gCY_i(H-h)^2]`。在真实七态 law 中，C=0 的类别被 C 因子消去；C=1 的 H=0 类因 `Y_i=0` 消去，H=h 类因 `(H-h)^2=0` 消去，只有 `(C,H)=(1,d)` 类留下。此处 `Y_i=1`、`g=η−1`，所以

\[
E_P[gCY_i(H-h)^2]
= -p(1-\eta)(d-h)^2<0.
\]

这是精确有理值，不依赖渐近、索引平均、浮点 SDP 或原 CONFIG 分布。`d=4,s=2,h=1` 也满足同一负值公式；不要求 `h≥2`。

本证明只使用 degree-two Gram null 对 degree-three multiplier 的正交、`Z²=Z` 的第五次乘子等式和只含 `C,Y` 的 base≤5 匹配。它没有把 base≤5 偷换为 affine owner 的 base≤4，也没有声称 base≤5 是最弱必要条件。

# 4. 普通原 job 的 faithful-AND 读法

该 Exact 允许把 `Z` 实际实现为新增 unit job `K` 的两个不同 private unit endpoints：候选 assignment law 中按 `CY_i` 选择第一端，按 `1−CY_i` 选择第二端。每个 sample 中 `K` 恰执行一次，新增两行各自负载不超过 1，且 `K` 不在原 v 上收费；所有原 jobs 仍完整执行。

这提供了一个真实 faithful assignment law 的读法：其自身可以有任意阶 PSD、Boolean/one-hot 关系和 faithful Gram=0，但只要保留本节的共同 `Lhat`、base≤5、原 v 负载与二次 localizer 合同，`q=Z(H-h)` 仍使 v 行局部化为负。该读法不把 ordinary UM 的 eligibility 逻辑偷换成一个外加 AND 侧约束；AND 只是候选 assignment law 中的相关性。

# 5. 与既有 7ccd read-after、全局 quadratic 与 affine owner 去重

## 5.1 与 7ccd 作者 read-after

已有 `7ccd86160f25544a1e74` read-after 页完整记录作者 Proof 的独立推导：令 `D=Z−CY_i`，先用 degree-three multiplier `Q=g(H-h)^2` 支付 Boolean 约化，再在真实 P 上得到同一个负值 `−p(1−η)(d−h)^2`。它还确认这是 faithful-AND、base≤5、原 v load 和 global quadratic 合同同时保留时的窄障碍，不是一般非线性 owner 定理。

本 Exact 的独有内容是： statement-only 的精确输入量词、`Z` 必须是 degree-one 新 endpoint、`Z²=Z` 需支付到次数五、`gq²` 的次数为五、无需 CONFIG first/pair、以及普通 UM faithful job 的两 private endpoints 读法。作者 Proof/Read-after 是后续证据身份，不能反向把本 Exact 写成已独审。

## 5.2 与七态原作业星 Global Quadratic Exact

已有 Global Quadratic Exact 与审计范围页记录另一合同：同一真实完整 assignment law `P` 同时满足共同 M3、所有 global degree-two load localizer、逐行 CONFIG first/pair，并有实际 OPT=1。当前 Exact 不是对该正向局部核的重复，也不否定其原 law；它说明在加入忠实 AND 新 endpoint、保留 base≤5 和原 v load 的情况下，额外二次 localizer 合同会出现负值。

因此不能把两个对象合并成“七态所有延拓均失败”：Global Quadratic 是未添加 faithful AND 的正向核，当前 AND obstruction 是在额外扩展合同下的窄负证据。

## 5.3 与 affine Boolean owner

Affine owner 对象使用 `base≤4`、affine candidates `f(C,Y)` 和共同 M3 Gram-null，分类支持上的 Boolean literals，并在 `B<2` pair-zero 条件下限制 affine-covered 正 owners。当前 AND Exact 明确使用 base≤5、忠实 `Z=CY_i`、degree-5 localizer；它不修改 affine classification，也不把 `CY_i` 伪装成 degree-one endpoint。两个对象的矩层级、端点类型和结论都必须分开。

# 6. 负值的真实范围与未完成义务

**可以安全使用的结论：** 对任意正偶 `d,s` 满足 `2≤s≤d/2`，在上述七类正概率 law、共同 M3、base≤5、原 endpoint Boolean/one-hot、忠实新增 degree-one `Z`、`Lhat[(Z−CY_i)^2]=0` 和不变的原 v load 下，`q=Z(H−h)` 给出严格负的 v-row localizer。因此这些条件不能同时与“v 行全部全局次数二 localizer 非负”共存。

**本 Exact 不证明：**

- 任意非仿射 extension 都失败；
- 任何其它 AND 实现、近似 AND 或改变基础矩的延拓；
- base≤5 是最弱必要条件；
- 不改变 v load 以外的接线一定失败；
- actual near-two gap、source decoder、一般 scheduling algorithm、SDP finder、NP/UGC hardness 或外部新颖性。

若 `Z` 不是新增 degree-one endpoint/Boolean 坐标，若只有一阶边际，若改变基础第五次矩、Gram 等式、原 v load 或 localizer 的次数，以上负值不能直接套用。其它非仿真依赖、跨背景路由和更深 shared-owner common law 必须重新列出全部 joint moments、jobs 和负载。

# 7. 证据级别与处置

本来源是 statement-only candidate；本页没有运行软件，没有读取作者 Proof 的源字节，也没有把 7ccd read-after 的作者结论回填成 Exact 的独立证明。已有 7ccd read-after 页属于后续作者证据，已有 global audit/root replay 只认证有限参数的 PSD/秩/assignment 字段和输出字节一致性；它们不能替代当前 Exact 的任意参数代数合同，也不能将其变成程序验证。

处置为 **integrated**：原文 evidence 已保留，正式页接入 faithful-AND 窄障碍链，明确与 affine owner、Global Quadratic 正向核、有限审计和一般 UM 目标隔离。

# 8. 结论

`89318ccee567ab05e1cd` 给出一个精确但范围很窄的 statement-only 障碍：在七态正支持 law 上，新增真实 degree-one endpoint `Z` 并忠实满足 `Z=CY_i`，若同时要求共同 M3、base≤5 的原基础矩、Boolean/one-hot、`Z²=Z` 第五次支付、原 v load 不变和全部二次负载 localizer 非负，则 `q=Z(H−h)` 产生

\[
Lhat[(T-C-H/d)q^2]=-p(1-\eta)(d-h)^2<0.
\]

它排除的是这一 faithful-AND 合同，不能外推到所有非仿射接线、一般 UM 算法、near-two gap 或 hardness。后续引用必须同时携带 `degree-one Z`、`base≤5`、`Lhat[(Z−CY_i)^2]=0`、原 v load 和 localizer 量词。
