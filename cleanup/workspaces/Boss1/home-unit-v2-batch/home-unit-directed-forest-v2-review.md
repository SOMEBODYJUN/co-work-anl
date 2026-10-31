---
id: "unrelated-machines/home-unit-directed-forest-v2-extension-review"
kind: "review"
type_tag: "审查"
title: "单 home 去环、unit 根森林与一般有向需求桥 v2 增量审查"
status: "integrated-as-separate-v2-extension"
truth_status: "proof-consistent-with-explicit-scope; no-general-UM-algorithm"
summary: "冻结 v2 源在既有 home-unit-cycle / directed-token 对象上扩展输入域：任意负载下逐简单环逐机不增、C<2 下保留 U 根的可达森林正规化，以及任意显式有向图的需求树双向恒等 OPT=2-b*。三项保持独立对象，不把环境环、树选择或有限审计升级为一般 UM 算法。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/home_unit_directed_forest_exact_internal_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/home_unit_directed_forest_exact_internal_source.md"
related_objects:
  - "archives/unrelated-machines/state/审查/根树流环正规化与有向需求桥冻结审查--审查.md"
  - "archives/unrelated-machines/tools/evidence/rooted-dag-home-cycle-20261030/home_unit_cycle_elimination_and_directed_token_bridge.md"
  - "archives/unrelated-machines/state/定理/单home级联的完整查询族与可加费用--定理.md"
source_ids: ["e0965328b2194975c31c"]
source_sha256:
  - "5de9dff0b3467dfc2105e93945d7e5e0e4dda534dbf73cf73f9bc097fd8468a3"
---

# 来源身份与相邻对象

`e0965328b2194975c31c` 是冻结的 v2 精确陈述，源路径为 `history/source/notes/unrelated_machines/home_unit_directed_forest_exact_internal_source.md`，大小 4,626 字节、SHA-256 `5de9dff0…fd8468a3`；同一路径在 legacy-cleanup 与 main 两冻结提交字节相同，只计一次。它明确写出 v2 尚非现行 Claim，不能覆盖 v1 字节。本文把它作为独立增量审查：A/B 是给定实际调度的 home/unit 去环和根森林正规化，C 是不同任务构造上的一般有向需求树桥。它与单home查询立方体定理共享 home 语言，但没有把两份完整调度见证或查询费用引入 C。

既有《根树流、环正规化与有向需求桥冻结审查》已核对 v1 对象：任意负载逐简单环消除、`C<2` 的 U-rooted forest、环境有向图 token 恒等及有限审计。本 v2 源的独有内容是扩大 A 的输入描述、把 B 的根集合/预算边界写成精确量词，并把 C 改为任意简单有向图（允许根入边与环境环、正需求死端和巨大二进制需求）的完整双向构造。

# A. 任意负载逐简单环去环

机器集 `M` 有不交任务 `U,J`。每个 `U` 作业所有有限端处理时间为 1；每个 `J` 指定 home `h(j)`，home 时间 `a_j∈[0,1]`，其他有限端均为 1（`a_j=1` 只是参考端）。给定任意完整合法实际调度 `σ`，对每枚离开 home 的 J 作业画带原任务标签弧 `h(j)→σ(j)`；U 和留 home 的 J 不画弧。

若当前转移图有有向环，选一条**简单**环；将环上每条弧对应的 J 同时退回自己的 home。设环点 i 的唯一出弧任务为 j_i，则该机负载变化为 `a_{j_i}−1≤0`；环外机器和其余任务不变。逐轮删除至少一条弧，最多 `|J|` 轮后得到完整调度 `τ_DAG`，转移图无环且每台机器负载逐机不增，U 的实际位置和每枚 J 的任务身份/资格保留。

边界不可省略：在一般负载下不能把“环上全部弧一次性退 home”替换成按所有环点做同一批操作以外的变换，因为环可能有重复入边/外来 unit，逐机负载的变化不再是唯一 `a_j−1`。A 只声称实际调度之间的逐机比较，不给单件迁移路径或其逆路径，也不声称保持某个全局阈值外的额外性质。

# B. C<2 下保留 U 根的可达森林正规化

再给 `C<2` 且 `C_max(σ)≤C`。令每枚 U 的实际目的地为 `r(u)=σ(u)`；令 `R` 为从所有 `r(u)` 沿转移弧前向可达的机器集合（包含根）。令 `b_i=Σ_{j:h(j)=i} a_j`。构造 `τ_U`：U 位置保持；若 J 的 home 属于 R，保留其原 σ 位置；若 home 不在 R，将其退回 home。

因为 C<2，每台机器至多接收一个时间 1 的外来 J/U unit；R 中的外送弧因每点最多一个外来 unit 而形成互不相交、以 U 实际目的地为根的朝外树（允许单点树）。τ_U 的精确性质：

1. 对 i∈R，`L_i(τ_U)=L_i(σ)`；对 i∉R，`L_i(τ_U)=b_i`。
2. τ_U 的全部转移弧都在 R；R 是以各 `r(u)` 为根的 `|U|` 棵互不相交朝外树。
3. 若 R 外所有 `b_i≤C`，则 makespan 仍不超过 C；全局 `b_i≤1` 是一个简单足够条件。

该构造不要求先执行 A。`a_j=1` 时 R 外可以有留在指定 home 的 unit J，但只声称转移弧森林的根来自 U；不声称 R 外逐机负载相对 σ 不增。阈值 C=2 时外来 unit 可以在同一机器共存，以上森林/预算论证不自动延伸。

# C. 任意简单有向图的需求树桥

输入显式有限简单无自环有向图 `D=(V,E)`、任意根 `r`（允许入边和环境环）、每顶点二进制非负整数需求 `k_v`。`k_v=0` 时要求出度为 0；正需求可大于出度或为死端。定义有限根树 H 为 D 中包含 r、从 r 朝外可达且除 r 外每点单父的树。令

`b(H)=min({1} ∪ {deg_H^+(v)/k_v : v∈H, k_v>0})`,  `b*=max_H b(H)`.

构造 unrelated-machines 实例 `P(D,k)`：每台机器一枚只在 r 以 1 处理的 U 根任务；对每个正需求 v，令 `d_v=outdeg_D(v)`, `q_v=min(k_v,d_v)`，建 q_v 个互异 J 子任务，每件在 home v 处理时间 `1/k_v`、每个原孩子端处理时间 1；若 q_v<k_v，再建一枚仅能在 v 处理、时间 `1−q_v/k_v` 的 filler；零需求不建 J。任务数至多 `1+|E|+|V|`，不按二进制需求展开。

**从调度解码 H。** 给定完整实际调度峰值 `C<2`，根任务位置为 r 的起点。每台机器至多收到一个时间 1 外来 J/U unit；从根起沿实际外送 J 的目的端读取，得到一棵合法根树 H（若某正需求点成为叶也保留其需求）。若 v 外送 s_v 个 child token，则其负载恰为

`1 + (q_v−s_v)/k_v + (1−q_v/k_v) = 2−s_v/k_v`.

故 `s_v≤deg_H^+(v)` 且 `s_v≤k_v`，从而 `C≥2−b(H)`，即 `b(H)≥2−C`，并得 `OPT(P(D,k))≥2−b*`。

**从 H 构造调度。** 给定任意 H，逐点把至多 `min(k_v,deg_H^+(v))` 个 J tokens 送到其 H children（具体 token 可任取），把其余 q_v tokens 和 filler 留在 home，沿 D 非 H 端不处理；叶节点仍留其 demand mass。根 U 留在 r。根机器含 U 根任务，负载为 `2−deg_H^+(r)/k_r`（若根需求为零则按定义没有该项）；非根机器的 home 质量为 `1−deg_H^+(v)/k_v`，不超过 1，树外机器也不超过 1。因此整体峰值≤`2−b(H)`，得到 `OPT≤2−b*`。

组合两向即 `OPT(P(D,k))=2−b*`。这是一条给定 D,k 后关于最优树值的精确恒等，不是寻找 H 的算法：在一般 D 上求 b* 的复杂度/近似性未给出。也不调用 LP gap、NP-hardness 或外部定理。

# 关系和适用边界

- 与既有 v1 home-cycle/token review 的关系：A/B 保留 v1 的 tagged-arcs、逐简单环和 C<2 unit 排斥，但 v2 明确允许任意负载的输入、a_j=1 参考 home、U 空、根入边、不可达环境环以及巨大二进制需求；不改写 v1。
- 与 `单home级联的完整查询族与可加费用` 的关系：共享“每 J 唯一 home”语言，但查询立方体要求同一普通矩阵上的两份峰值≤1 调度和不交支持；C 的 `P(D,k)` 没有第二见证、query 子集或费用合同，因此不能互换结论。
- 与 rooted DAG token bridge 的关系：C 的环境从 DAG 扩至任意简单有向图；树 H 仍是输出对象，环境环只影响候选集，不改变双向负载恒等。
- 与有限审计的关系：既有 cycle-path/HS-greedy 运行可作为边界证据，但本源未附新程序或新运行；不能把有限枚举称作一般图选择器。

# 缺口和处置

本源是 v2 扩展陈述，未提供一般图中高质量 H 的多项式寻找算法，也未给一般 UM-TARGET-v1 近二算法、NP-hardness 或外部新颖性。A/B/C 需保持独立稳定 ID；第三阶段可建立“v1→v2 扩域/纠错”和“home 语言共享但无推导”的关系，不能把它并入 single-home query theorem。

建议处置：`integrated` 到新的 `home-unit-directed-forest-v2` 增量审查对象（或既有 rooted home-cycle review 的 v2 段落），并保存本页作为 source-specific provenance；不覆盖旧 v1 正文。
