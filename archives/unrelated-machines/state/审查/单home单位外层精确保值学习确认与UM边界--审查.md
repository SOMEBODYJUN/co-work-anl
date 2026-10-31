---
id: "unrelated-machines/unit-home-identity-learning-v1-scope-review"
kind: "review"
type_tag: "审查"
title: "单 home 单位外层恒等桥的 learning 确认与不相关机边界"
status: "integrated-learning-scope-confirmation"
truth_status: "existing-value-and-opt-identity-confirmed-no-new-claim"
review_level: "full-source-read-cross-object-comparison"
scope: "任意 normalized-flat Q 的 unit-home/unit-helper 外层恒等桥；仅作既有值桥复核，不扩展为一般 UM 算法或困难性"
summary: "来源完整读取并逐项核验 Q→Q⁺ 的构造、V 与普通 UM OPT 的精确相等、C<2/C≥2 两分支、显式规模和 m=0/空任务边界。该记录是 learning/确认材料，不登记新 Claim，不把 ν=1 外层当作免费邻近特例，也不声称一般 UM 算法或 hardness。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_unit_home_identity_learning_v1.md"
  - "clean:636a6d90d1ad2a91dc83"
related_objects:
  - "../资料/加权菜单Santa值桥与不相关机转换--资料.md"
  - "../定理/规范化平菜单的CONFIG与正支撑LP双向保持--定理.md"
  - "../审查/多outer双资源后端与tiny-home算法边界有限审查--审查.md"
  - "../审查/规范化平菜单Exact与Proof版本核验--审查.md"
  - "../定理/完整菜单的资源度三路径归约--定理.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/unit-home-identity-learning-v1/original/sol_general_repair_unit_home_identity_learning_v1.md"
---

# 对象身份、读取范围与处置

本页处理 clean 源 `636a6d90d1ad2a91dc83`，路径为 `history/source/notes/unrelated_machines/sol_general_repair_unit_home_identity_learning_v1.md`，冻结 blob 为 `b2c75c6db8a65df0af379e1ca64ab0d2c4b8599c`，源 SHA-256 为 `39b713119bfeb2a7894f17c6e6c9b61adac46b9a8a11639f200ae8070593eff9`，大小 4,623 B。原文已经逐字保存到本页 `evidence_paths` 所列目录。

来源标题是“Unit-home 外层的精确保值：learning 确认”。它主动声明：只确认一个直接重构，不登记新 Claim，不主张全球新颖性，不提供一般 unrelated-machines 算法或困难源。来源还说明 2026-10-18 的检索覆盖 `research/current/unrelated_machines` 的 `home/outer/helper/unit` 关键词、`research/unrelated_machines/CLAIMS.md` 的身份/保值关键词，并实际核对 normalized-flat 到 state-dummy Santa-Claus 的值桥以及 normalized 菜单 tree/resource path 的正文。该检索没有找到完整 unit-home 恒等桥，但这不是对仓库每一字节或外部文献的否定性认证；本页保留这个检索限度，不把“未搜到”写成新颖性证明。

本批的处置是 **integrated-learning-scope-confirmation**：把它整合为既有 normalized-flat 值桥和普通 UM 精确恒等的范围确认，保留唯一来源字节与版本 provenance；不另建定理、不给作者确认升级为独立外审，不把同一桥重复计为一般算法或 hardness 结果。

# 规范化输入与 Q→Q⁺ 构造

## 输入模型

令 Q 是任意完整显式 normalized-flat 菜单。共有 `m≥1` 个 groups，每组至少一个带索引的 state。每个 state 的非负二进制有理系数总和恰为 1；旧资源宇宙记为 `B`。零 incidence、重复 indexed states、inactive/unused resources 均保留，且同一 state 不重复列同一 resource。旧总 states、listed incidences、resources 数分别记为 `S`、`I`、`U`。

这里的“完整”是普通 UM 转换的关键：所有旧 selector、所有 indexed-state payload 和所有 incidence job 都存在，不能因为其权重为零或 state 没被选就删除。indexed 身份也不能按内容合并；该边界与既有 CONFIG/FSLP 审查中的规范化域一致。

## 外层重构

对每个旧 group `g` 新建一个互异且不在 `B` 中的资源 `h_g`。旧 group 改名为 helper `H_g`，完整保留原 indexed states，并另添一个 own indexed state；这个 own state 唯一 incidence 是在 `h_g` 上的系数 1。再加入 outer `O_g`，它只有一个 indexed state，唯一 incidence 也是在 `h_g` 上的系数 1。除这些 helper 与 outer 外没有其它 groups。记新菜单为 `Q⁺`。

因此每个 outer 只有一个 home，`w_g=1`，`ν=1`；helper 的 fallback 仍是任意原 normalized 菜单，未被压成某个特殊 state。新 groups 数为 `2m`，新 states 数为 `S+2m`，新 incidences 数为 `I+2m`，新 resources 数为 `U+m`。这里的 unit own state/helper 是完整菜单的一部分，不是仅在目标解中临时添加的标记。

# 实际 normalized 菜单值：V(Q⁺)=V(Q)

令 `V(Q)` 表示在 pairwise disjoint resource bundles 上最大化的最小 normalized menu quality；同样定义 `V(Q⁺)`。来源给出严格恒等

\[
V(Q^+)=V(Q).
\]

## 旧解到新解

给定 Q 的任意旧 allocation。每个 helper `H_g` 使用原来的 state 和 bundle；每个 outer `O_g` 拿自己的新 home `h_g`。旧 bundles 互不相交，新 homes 彼此不同且不在 `B` 中，因此新 allocation 的最小质量不小于旧 allocation。取旧最优值的上确界即得 `V(Q⁺)≥V(Q)`；有限显式菜单下也可直接取 attaining states。

## 新解到旧解

考虑 Q⁺ 的任意 allocation，其最小质量记为 `b`。若 `b>0`，每个 unit outer 要达到正质量，必须得到自己的 `h_g`。由于 helper 的 own state 不能再使用同一 `h_g`，该 helper 只能使用原 `B` 上的某个 fallback state；其 fallback bundle 的质量至少为 `b`。删除所有 outer 及其 home，留下原 groups 在 `B` 上的 bundles，即得到 Q 的合法 allocation，故 `V(Q)≥b`。再对任意新 allocation 取最大值得 `V(Q)≥V(Q⁺)`。

若 `b=0`，反向不需要从每个 outer 推出 home：由 normalized 质量非负，`V(Q)≥0= b`。这一分支明确涵盖 `V=0`，不依赖正值 promise；`V=1` 也由同一双向构造覆盖。合并两边得到上述精确恒等，而不是仅一侧的近似不等式。

该值桥与《加权菜单 Santa 值桥与不相关机转换》中的既有 `OPT_UM=2−V` 资料对象相容，但本页的 outer/helper 构造本身没有把 state-dummy Santa 的所有额外断言重写成新定理。使用值桥时仍须满足每 state private 系数总量恰为 1、每 resource 是独立 unit machine、每 group 一个 selector 且全部 incidence jobs 保留等模型条件。

# 完整普通 UM 矩阵与 OPT 恒等

## 矩阵定义和新增端点

`P(Q)` 的普通矩阵按以下完整结构构造：每个 state 一台 private machine；每个 resource 一台 resource machine；每个 group 一个 selector，selector 可在该 group 任一 own private machine 的时间 1 端点上运行；每个 listed incidence 是一枚独立 job，在其 private machine 上运行时间为其 coefficient `p`，在对应 resource machine 上运行时间 1，另一端点为无穷；未选 state、零 jobs、unused resources 都保留。

Q⁺ 中每个旧 selector 多得到一个新的 helper-own private endpoint，因为 helper own state 已加入 group；因此这是对旧矩阵的结构化扩展，不能描述成只添加互不相交的固定任务。新增 outer selector 固定在其 outer private machine；新增 outer incidence 有自己的 private 端点和 `h_g` 的 resource 端点。

## 旧调度到新调度

给定 Q 的任意合法调度 `σ`，保留全部旧 job/machine assignment。每个 helper-own incidence 留在其新增 private machine；每个 outer selector 留在 outer private machine；每个 outer incidence 送到 `h_g` 的 resource machine。所有新机器的负载恰为 1。旧 selector 在其 private machine 上贡献时间 1，所以旧调度的 makespan `C(σ)≥1`；新调度没有增大峰值，且有新增 unit 机器达到 1，故

\[
C(σ^+)=C(σ).
\]

这一步保留旧零 job、旧未选 state job、重复 indexed state 的身份，不能通过删掉它们来获得等式。

## 新调度到旧调度：严格 C<2 分支

取 Q⁺ 的任意新调度 `σ⁺`，makespan 为 `C`。若 `C<2`，outer selector 的唯一可行 private machine 被迫使用；outer incidence 若不送其唯一的 `h_g` 端点会超出对应 private/资源选择，因而必须送到 `h_g`。此时 `h_g` 已经承载一枚 unit outer incidence，helper-own incidence 不可能再使用 `h_g`，只能留在它自己的 helper private machine；该 private machine 已有 unit helper-own incidence，于是 helper selector 必须改在一个旧 fallback private machine 上运行。把全部旧 jobs/machines 限制回来，就得到 Q 的合法旧调度，且负载不增：`C(σ)≤C(σ⁺)`。

这是一条“正余量”反向证明。它不把 `C=2` 时的 unit 独占性偷用到等边界，也不删除旧任务。若当前最佳新 makespan小于 2，就直接推出 `OPT(P(Q))≤C`。

## C≥2 退化分支与精确 OPT

若新调度 `C≥2`，可以输出旧矩阵的 full-private baseline：每个 incidence 留在自己的 old private machine，每个 selector 任取本组一个 old state private machine。每台 private machine 至多承担该 state 的 payload 总和 1 加 selector 的 1，故峰值至多 2；资源机器为空或只承担不超过 unit 的任务。于是旧 `OPT≤2≤C`。

将 `C<2` 的反向限制和 `C≥2` 的 full-private baseline 合并，得 `OPT(P(Q))≤OPT(P(Q⁺))`；旧调度到新调度的正向恒等给 `OPT(P(Q⁺))≤OPT(P(Q))`。因此

\[
\operatorname{OPT}_{UM}(P(Q^+))=\operatorname{OPT}_{UM}(P(Q)).
\]

这个证明覆盖 `OPT=2` 边界，不假设 optimum 恰好等于 2，也不把 `C=2` 误写成 resource unit 的严格互斥情形。通过前一节值桥，在 normalized 域还可写成两边都等于 `2−V(Q)`，但只在上述完整矩阵模型下有效。

# 规模、位复杂度与边界

Q⁺ 的计数为

| 对象 | Q | Q⁺ |
|---|---:|---:|
| groups | `m` | `2m` |
| states | `S` | `S+2m` |
| incidences | `I` | `I+2m` |
| resources | `U` | `U+m` |
| ordinary UM machines | — | `S+U+3m` |
| ordinary UM jobs | — | `I+4m` |
| finite endpoints | — | `S+2I+6m` |

只复制原有理数并添加 `0/1/∞` 端点，转换是确定性总位多项式；不调用 `OPT`、allocation oracle 或未知目标。零 jobs、unused resources、inactive states 与重复 indexed states 原样保留。稠密表示的规模也按输入位长多项式增长。

`m=0` 的空实例不属于本非空 normalized-flat 值定义。若其 UM 侧没有 jobs，则单独输出空调度、`OPT=0`，不能套用 `2−V` 的非空表达式。该来源也没有把任意外部 UM 矩阵转换成 normalized-flat Q；因此不提供从一般 UM 到该菜单模型的识别、嵌入或 hardness 归约。

# 与全仓对象的比较和证据边界

## 与 normalized-flat/state-dummy 值桥

《加权菜单 Santa 值桥与不相关机转换》已经保存 normalized-flat state/private/resource 的 Santa 值桥和 `OPT_UM=2−V` 条件恒等。本来源独有的是：在每个旧 group 外层再加一个 unit outer、一个 unit home 与一个 helper-own state，并证明 Q 与 Q⁺ 的实际值直接相等以及完整 UM OPT 直接相等。它没有重新证明 state-dummy 的 dummy 容量、SC threshold-1 CONFIG、或一般值桥以外的 hardness；引用这些性质时应回到既有资料对象并保留其模型边界。

## 与 CONFIG/FSLP 双向保持

《规范化平菜单的 CONFIG 与正支撑 FSLP 双向保持》和 Exact/Proof 版本核验都要求 state total=1、正支撑或完整 job 身份、阈值一与有限 indexed states。当前 unit-home 桥没有改变 FSLP/CONFIG 证书；它只是在实际 allocation 与完整 UM schedule 上增加一层 exact identity。不能用 Q↔Q⁺ 的实际值等式自动推出 FSLP 的新可行性、任意 threshold 的 CONFIG 定理或近二算法。

## 与 tiny-home / 多 outer 后端

《多outer双资源后端与 tiny-home 算法边界有限审查》处理的是另一对象：多 outer、互异 homes、共享 fallback、`k⁴` tiny-home 权重，以及有限 winner-moment/conditional-expectation 后端。其算法需要 tiny-home 假设、具体 LP/MW/CDF/方差链和完整 jobs 回填；本页 Q⁺ 让每个 outer 的 home 权恰为 1，正好是该 tiny-home 条件的反例边界，且本页没有给多 outer welfare rounding 算法。因而不能把 Q↔Q⁺ 恒等桥改写成 tiny-home approximation，也不能把 tiny-home backend 的 19/10 结论套到任意 Q⁺。

## 与已有 one-outer 近似审查

既有 one-outer normalized-flat 13/8 审查只覆盖 typed 单 outer、互异 home、shared fallback 且需要完整 primitive-SA1/LP、CDF rounding 和固定 margin；当前来源不提供这些算法所需的 supplied point、LP certificate、CDF backend 或调度输出。两者都保留 zero/duplicate/unused jobs，但数学合同不同，不能因都写 `normalized-flat` 而合并。

## 资料/审查/障碍分类

本来源是 **审查/学习确认**：

- **已确认**：Q→Q⁺ 的构造；`V(Q⁺)=V(Q)`；完整普通 UM `OPT(P(Q⁺))=OPT(P(Q))`；`C<2` 强制与 `C≥2` baseline 两分支；显式规模和位复杂度。
- **不是本来源证明**：一般 normalized-flat 或一般 UM 的算法、近二近似、NP-hardness、外部文献新颖性；state-dummy Santa 的全部 CONFIG/FSLP 合同；tiny-home/multi-outer rounding。
- **审查边界**：检索未搜到不能作为全库否定；m=0、OPT=0、V=0 需按来源的单独分支处理；C=2 不可套 C<2 的 unit 资源强制。

# 结论

在其明示的完整 normalized-flat 域中，给任意 Q 添加每组一个 unit home、一个 unit outer 和一个 own-unit helper state，得到 Q⁺，确实保持实际 menu value 与完整普通 UM makespan optimum。该事实说明：即便每个 outer 只有一个 unit home（`ν=1`），其 helper fallback 仍可携带任意原 normalized-flat 菜单；不能把这一扩域视为“免费相邻特例”。

本页仅作为既有值桥的条件性 source interface 和 provenance 记录。它没有新 Claim、没有代码执行或有限实验、没有一般 UM 归约、没有 hardness 结论，也没有解决任意 normalized-flat/ordinary UM 的算法问题。后续引用必须同时写出 nonempty `m≥1`、state total=1、完整 job 保留、`C<2` 反向条件、`C≥2` baseline 与 `m=0` 空任务边界。
