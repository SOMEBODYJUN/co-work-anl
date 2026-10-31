---
id: "unrelated-machines/partial-minrep-linear-degree-sparsification"
kind: "bridge"
type_tag: "资料"
title: "partial-MinRep 线性 degree 删边源与外部边界"
status: "explicit-theorem-reviewed-with-conditional-source-and-physical-gap"
summary: "v2 对显式 D-regular total-projection game 给出随机删边、最大 degree Δ=1000μ、perfect completeness 和 cheap-list soundness≥0.9；固定参数的 PCP/parallel-repetition 来源、UM physical compiler 与 fee 实现仍是条件或开放接口。"
source_refs:
  - "clean:9375b56f128e3b90a223"
  - "clean:b927284288ac14421fc6"
  - "clean:ddc971c06663bd48e062"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/partial_minrep_linear_degree_exact_only_independent_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/partial_minrep_linear_degree_exact_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/partial_minrep_linear_degree_primary_comparison_source.md"
---

# 对象身份、来源分工与认证范围

本页合并三份同一 v2 对象的冻结来源：独立 Exact-only 重构、v2 精确陈述、以及与 Manurangsi 和 Minzer–Zheng 主要结果的定向比较。三份来源均完整读取，且全部原件由 `clean show` 导出并哈希复核。本页保存的是一个**显式投影游戏删边定理接口**，不是不相关机算法、不是实际 schedule 编译，也不是新颖性认证。

| clean ID | 原路径 | 源 SHA-256 | 大小 | 实读性质 | 本页处置 |
|---|---|---|---:|---|---|
| `9375b56f128e3b90a223` | `history/source/notes/unrelated_machines/partial_minrep_linear_degree_exact_only_independent_source.md` | `c04b2797441c761c7f452ceb86c05d3647a832975dd4ab3861dc4457922d4840` | 16,560 B | Exact-only 独立 blind review；重构完整概率、bit complexity、degree necessity、归一化和 conditional fee | 保存为独立数学核对与边界 |
| `b927284288ac14421fc6` | `history/source/notes/unrelated_machines/partial_minrep_linear_degree_exact_source.md` | `067ebfea168a2047d4b9a533c17430afdfefff78a14c0cb473f61a401b83c906` | 4,446 B | v2 精确陈述；不含作者证明 | 保存对象、量词和所有承诺 |
| `ddc971c06663bd48e062` | `history/source/notes/unrelated_machines/partial_minrep_linear_degree_primary_comparison_source.md` | `5fd85e6154703f9aa697711cba404e90da65f83c6917c432ced21c9ec4dda6df` | 4,441 B | 定向 primary 阅读与最近结果比较；新颖性未认证 | 保存外部前提、参数比较和物理缺口 |

证据原件位于 `archives/unrelated-machines/tools/evidence/partial-minrep-linear-degree-20261031/`，回执草稿在 `cleanup/workspaces/Boss2/partial-minrep-linear-degree-receipts-20261031.json`。

# 精确输入、参数与输出

输入是显式有限 D-regular 二部 projection game Π=(A,B,E,Σ,{π_e})，其中 |A|=|B|=n≥1、N=2n、D≥1、Q=|Σ|≥2。每条 π_e:Σ→Σ 是显式总映射；平行 constraint 边分别计数、分别采样和分别计 degree。边数 M=ND/2。单标签 value 是满足边比例。

multilabeling ψ 给每个顶点一个可为空的 Σ 子集，cost(ψ)=所有列表大小之和。边 e=(u,v) 被覆盖，当且仅当存在 a∈ψ(u)、b∈ψ(v) 使 π_e(a)=b。coverage 是覆盖边数除以总边数。

附加输入是二进制整数 g≥2 与二进制有理 0<ρ≤1。定义

- ℓ=floor(log2 g)，λ=1+ceil(log2 Q)；
- τ=ρ/(100 g²)；
- γ=ρ³/(10^9 g^8)；
- μ=ceil(1000 g λ/(ρ ℓ))；
- Δ=1000 μ。

随机删边算法如下：若 D<2μ，原图原样输出；否则取最小 s 使 2^s μ≥D，令 p=2^-s，每条原边独立以概率 p 留下，得到中间图 H；随后只根据 H 中的 degree，一次性删除所有中间 degree>Δ 的顶点的全部关联边。不能改成迭代删边，也不能按最终 degree 反复判断。

结论的量词为：

1. 对每个随机种子，输出最大 degree≤Δ；
2. 若 val(Π)=1，则每个种子都保留 cost≤N 的 singleton multilabeling 覆盖全部剩余边；输出为空图时此完备性命题按真空解释；
3. 若 val(Π)≤γ，则以至少 0.9 的概率输出非空 Π′，并且**每一个** cost≤gN 的 multilabeling 在 Π′ 上覆盖严格少于 ρ 比例的边；
4. 运行时间、随机位数和输出长度关于显式 Π、g、ρ 的总二进制编码长为多项式，不按 g、1/ρ、μ 或 Δ 的数值做长循环。

固定参数 source 推论还需要外部 perfect-complete Label-Cover PCP、适当 biregularity 和 parallel repetition；本页将其作为条件，而不是已读已证的外部定理。

# 便宜列表 soundness 的完整概率账

假设 val(Π)≤γ。先在原图建立确定性覆盖上界。固定任意 cost≤gN 的 ψ，设其覆盖原边比例为 α。令列表大小大于 L=4g/τ 的顶点为 heavy。heavy 顶点数最多 gN/L；D-regular 性给出 incident heavy 边比例至多 2g/L=τ/2，即使一条边两端都 heavy 也只会在上界中重复计算。若 α≥τ，则至少 τM/2 条边既被覆盖又有两个 light endpoints。

从每个非空 light list 独立均匀抽取一个 label；空 list 不可能见证 covered edge，其余顶点任取。每条 covered light-light edge 至少有一对 witnessing labels，抽中该 pair 的概率至少 1/L²。因此存在一个 singleton labeling 覆盖原边比例至少

`τ/(2L²)=τ³/(32g²)=ρ³/(32·10^6 g^8)>γ`。

这与 val(Π)≤γ 矛盾。因此对所有 cost≤gN 的 ψ，同时有原图 coverage α<τ。该结论不需要枚举 multilabelings，只在分析中使用；空列表、任意 Q 和平行边均被包含。

在 D≥2μ 的分支，令 d=pD、A=pM=Nd/2。s 的最小性给出 μ/2<d≤μ，且 μN/4<A≤μN/2。对固定 ψ，删边前中间图中覆盖边数 X_ψ 的期望小于 τA。设 T=ρA/8，二项上尾给出

`Pr[X_ψ≥T] ≤ (8e/(100g²))^(ρA/8)`。

cost≤gN 的 multilabeling 数 K 可用 slots 计数：`K≤Q^(gN)(1+1/Q)^(NQ)≤exp(gNλ)`。又 `ln(100g²/(8e))≥ℓ`，故 union bound 得

`Pr[存在 cheap ψ: X_ψ≥ρA/8] ≤ exp(gNλ−ρμNℓ/32)<0.01`。

这里 rare-covered 上尾与共同的采样边数下界共同使用；不能仅把旧 soundness γ 替换成 g^-8 而跳过这两步。

再令 Y 为 H 的总边数。Chernoff 下尾给 `Pr[Y<A/2]≤exp(-A/8)<0.01`；输入参数保证 μ≥2000、N≥2，因而 A>1000。对每顶点，中间 degree Z_v~Bin(D,p)，均值 d≤μ。一次性 trimming 删除的边数 R 满足 size-biased identity

`E[Z_v·1{Z_v>Δ}] = d·Pr[Bin(D−1,p)≥Δ] ≤ d·(e/1000)^(1000μ)`。

因此写 β=(e/1000)^(1000μ)，有 E[R]≤Ndβ=2Aβ、`Pr[R>A/4]≤8β<0.01`。无需 high-vertex 事件独立；不允许把一次性规则换成迭代规则。

三个 good events 同时发生时，最终 M′=Y−R≥A/4>0，而每个 cheap ψ 覆盖的最终边数小于 ρA/8，所以 coverage `<(ρA/8)/(A/4)=ρ/2<ρ`。union bound 成功率大于 0.97，故精确陈述中的 0.9 留有余量。输出最大 degree≤Δ 对每个 seed 都成立：被标记顶点的所有边都删去，未标记顶点的中间 degree≤Δ，后续删边不会增加 degree。

# Perfect completeness、随机位和总位复杂度

若 val(Π)=1，原图存在 cost=N 的 singleton satisfying labeling。随机删边和 trimming 只删除原 constraints，保留原 projection，因此同一 labeling 对所有 seeds 都满足剩余边。若输出空图，完备性声明仍为真空命题。

若 D≥2μ，s≤ceil(log2 D)。每条边用 s 个独立 fair bits，只有全零时保留，随机位总数至多 M·ceil(log2 D)，关于显式输入多项式。度数只需扫描存活 edge records，与二进制 Δ 比较；一次标记高点，再一次删关联边。不会进行 g、1/ρ、μ 或 Δ 次迭代。输出复制原 alphabet 与 projection，长度不超过输入多项式。

# 独立的线性 degree 必要性

该结论不需要 regularity 或随机删边。考虑任意非空 balanced total-projection game，左右各 N/2 个顶点，M 条边。任取每个左点一个 label，cost=N/2。对任意 t 条被选边，把其左端选定 label 的 projection 加入每条边右端的列表，总增量至多 t，并覆盖这 t 条边。令 K0=(g−1/2)N。若 ρM≤K0，取 t=ceil(ρM)≤K0，便得到 cost≤gN 的 multilabeling 覆盖至少 ρ 比例边，矛盾。因此

`ρM>K0`，即 `M>(g−1/2)N/ρ`。

最大 degree 至少为平均 degree 2M/N，所以 `Δ_max>(2g−1)/ρ`。ceil 与严格覆盖率给出严格不等式，而不是渐近版本。故固定 ρ 时，任何同类 source 的 degree 阶不能改为 o(g)。

# 两个精确归一化接口

## Biregular 到 balanced regular

若显式 bipartite projection game 左右正 degree 分别为 d_A、d_B，令 h=gcd(d_A,d_B)。把每个左点复制 d_A/h 次，每个右点复制 d_B/h 次；一条原边替换为对应复制对之间的完整二部边集，并保留原 projection。新两侧各有 M/h 个点，每个新点 degree=d_A d_B/h，输出边记录至多 M³，故显式多项式。

一致 copy labeling 给出原 labeling 的同值。反向从 copy labeling 随机均匀选每个原点一份 copy，原边满足概率恰等于对应完整 blowup 边的满足率；因此存在原 labeling 达到至少 copy labeling 的 value。最优 value 精确保持，perfect completeness 也保持。平行原边独立保留。

## 两个 alphabet 到一个共同 alphabet

若左、右 alphabet 不同，取 Q=max(2,|Σ_A|,|Σ_B|)，选 surjection f:[Q]→Σ_A 与 injection i:Σ_B→[Q]，替换每条 projection 为 `π′=i∘π∘f`，得到 total [Q]→[Q] 映射。原 assignment 可 lift 且值不降；新 assignment 中不在 i(Σ_B) image 内的右 label 不满足任何 incident edge，可改成 image 内任意 label 而不减满足数。再应用 f 与 i^-1 得到原 assignment 同值，故 optimum value 精确保持。顶点特定 alphabets 也可用局部 retraction/embedding，统一 alphabet 取最大值。这些构造本身不提供外部 PCP 定理。

# 外部 primary 比较、source 参数和新颖性边界

独立 comparison 实际读取了 Manurangsi arXiv:1807.00936v1 的 §3 全证明与 §4 讨论，Minzer–Zheng ECCC TR24-027 原版 §7.3.2、§7.4，以及 2026 Revision1 的主结果、定义、§7.3 bounded-degree 结果、§7.4 Lemma 7.12/Theorem 7.13。ECCC PDF 的 shell 下载曾超时，没有把失败请求当作取得字节，也没有虚构本地 SHA；Manurangsi 原始 PDF 保持其既有字节。

比较结果必须分层：

- Manurangsi 的 displayed Theorem 1 给随机归约下 Min-Rep gap g、degree O(g log g)、alphabet O(g^4 log²g)；其 generic Lemma 7 的 cheap-list 门槛是常数倍 N/√γ，未给 v2 所需的 g^-8 rare-upper-tail 组合，也不是 singleton perfect source。
- Minzer–Zheng 2026 Revision1 的 Lemma 7.12 仍导入 Manurangsi Lemma 7，Theorem 7.13 给 bounded-degree 结果 degree O(g log g)、alphabet O(g^(2+ε′))（固定 ε′>0、充分大 g）。它改善 alphabet-to-soundness 起点，但仍没有 v2 的 linear-degree partial-MinRep 命题，也没有 singleton perfect PCP 证明。
- bounded-degree Max2-CSP 的 near d/2 困难性是不同对象：它针对 single-label maximum satisfaction。把单标签 NO value 直接随机舍入成 cost-gN lists 会损失平均 list 长度，不能未经新证明替换 v2 的 cheap-list 声明。

因此 ddc971c 的安全新颖性结论是“在定向 primary 阅读范围内尚未定位同一较差 polynomial alphabet 换取 linear degree 的定理”，不是全球新颖性或不存在性证明。v2 的显式删边正确性与新颖性独立。

固定参数 source 推论的代数如下：若外部 perfect-complete Label-Cover PCP 与 repetition 让 Q≤poly_ρ(g)，则 λ/ℓ 只依赖固定 ρ，Δ=1000μ=O_ρ(g)。repetition length O(log g+log(1/ρ))，但 SAT 归约的多项式指数可以依赖事先固定的 g、ρ；不把随 SAT 输入增长的二进制 g 送入一个统一 PCP 链。对任意显式 Q 的删边算法本身仍有总位多项式保证，只是 Δ 可能更大。

随机归约的复杂度假设也须准确：若目标 promise 有确定性多项式算法，YES 每 seed 保留，NO 以至少 0.9 概率满足 cheap-list 禁令，便得到 SAT 的有界错误算法。因此 `NP not contained in BPP` 是充分的排除条件；不能仅用 P≠NP 推出随机归约困难性。

# 物理 fee 接口与未完成义务

若另有 actual UM compiler，把任意所需弱 schedule σ 转为 lists，满足覆盖至少 ρM 条真实 source 边、`cost≤N+B(σ)/F` 且 `B(σ)≤cM`，则 M≤NΔ/2，故

`cost≤N+cNΔ/(2F)`。

若 F≥cΔ/[2(g−1)]，则 cost≤gN，与 good NO source 的 strict cheap-list ban 矛盾。固定 ρ 且 Δ=O_ρ(g) 时，若 c 也由 compiler 固定控制，足够大的**固定 fee**即可；不能把 fee 自动写成 1，也不能声称 physical implementation 已存在。v2 明确没有构造 partial-trigger、projection/fee interface、实际 UM 矩阵或 schedule path。

# 最终边界与接续

三源共同支持：显式 D-regular total-projection game 上的随机删边定理、每 seed 完美完备性、以至少 0.9 概率的全 cheap-list NO、严格线性 degree 必要性、精确 biregular/common-alphabet normalization，以及条件 fee 代数。它们不支持：

- 一般不相关机实际编译或主 near-two 结论；
- v2 所需 PCP/parallel-repetition 外部 source 的本轮独立认证；
- 随机 source promise 的 P≠NP 困难性（需要 NP⊄BPP 之类假设）；
- fee=1、partial-trigger 机制或任何已实现 physical schedule；
- 全球新颖性或“此前不存在”证明。

本轮已完整实读、比较所有定义、量词、概率事件、退化分支、输入位复杂度、外部 primary 边界和 physical fee 缺口；无脚本或有限实验需要运行。数学正文归档为 unrelated-machines/state/资料，原件和 manifest 在 evidence 目录，回执草稿单列，等待 Boss checkpoint/done。
