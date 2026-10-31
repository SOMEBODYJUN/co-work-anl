---
id: "unrelated-machines/lst-k-dimensional-matching-hardness"
kind: "literature"
type_tag: "文献"
title: "Lee–Svensson–Thiery 的 k 维匹配与 k-集合打包渐近硬度"
status: "complete-source-read-integrated"
truth_status: "primary-theorem-read; external-literature-fact; not a theorem about R||Cmax"
review_level: "full-primary-read-with-definition-proof-and-boundary-comparison"
summary: "论文给出 R 度有界、字母表大小为 R 的 k-CSP 到 kR-维匹配的精确仿射线编译，并用随机稀疏化把 CSP gap 提升为大 k 的 k/(12+epsilon) 维匹配硬度；复杂度假设是 NP not-subset BPP。"
scope: "k-CSP, k-dimensional matching, k-set packing, k-matroid intersection; fixed CSP arity and sufficiently large prime alphabet"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/lee_svensson_thiery_2024_affine_line_set_packing_v1.pdf#全文"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/lee_svensson_thiery_2409_17831.pdf#全文"
source_ids:
  - "a5839014ba13020420d7"
  - "e12a6689b97c90389ca1"
source_sha256: "75c9acd3432958383ffb21b12dd4baf2dacec97e8a183962cde4460dd7884ee2"
source_version: "arXiv:2409.17831v1, 14 pages, 2024-09-26/27"
---

# Lee–Svensson–Thiery 的 k 维匹配硬度

## 来源与阅读范围

本对象由两个冻结路径构成：`lee_svensson_thiery_2024_affine_line_set_packing_v1.pdf` 与 `lee_svensson_thiery_2409_17831.pdf`。二者字节相同（SHA-256 `75c9acd3432958383ffb21b12dd4baf2dacec97e8a183962cde4460dd7884ee2`），均实际导出并通读了摘要、§1 技术概览、§2 Definition 2.1/2.3、§3 Theorem 3.1 与 Claim 3.3 的完整构造和证明、§4 Theorem 4.1/4.3 及附录 A–C。两个来源因此共享下述数学对象；第二份是相同冻结版本的路径重复，不能当作独立证明。

论文研究最大 k-维匹配（k-Dimensional Matching, k-DM），并把结果转移到 k-Set Packing、k-Matroid Intersection、k-Matchoid、k-Matroid Parity 等问题。它不研究不相关并行机 `R||C_max`，下文与本存档的关系只作为适用边界记录。

## 模型和精确主结论

一个 k-CSP 实例为
\[
\Pi=(G=(V,E),[R],\mathcal C),
\]
其中每条约束超边恰含 k 个变量，每个变量取 `R` 个标签之一，关系 `C_e` 是 `[R]^k` 的任意子集。赋值满足约束的比例记为 `val(Π)`。`d`-degree bounded 表示每个变量出现次数至多 d；`d`-regular 表示恰为 d。论文无损地把实例看作 k-partite。

k-Set Packing 是边大小至多 k 的超图最大匹配；k-DM 还要求超图 k-partite，因而每条边大小恰为 k。论文的 Theorem 3.1 在素数 R 下给出：对任意每变量度数至多 R、字母表大小为 R 的 k-CSP，有一个多项式时间的近似保持归约到 kR-Set Packing；若原 CSP k-partite，输出是 kR-DM，并且
\[
|M^*|=|\mathcal C(\psi^*)|,
\]
其中 `M*` 是输出最大匹配、`ψ*` 是原 CSP 最优赋值。归约还保留双向恢复：给定最大匹配可恢复最优赋值，给定最优赋值可构造同大小匹配。论文给出的运行时间按 `poly(|V|,|E|,R^k)` 计。

结合 Theorem 4.1：固定 `k≥4` 和任意常数 `ε>0`，对充分大的素数 R，除非 `NP ⊆ BPP`，不能把 R-度有界、字母表大小 R 的 k-CSP 区分为
\[
\operatorname{val}(\Pi)\ge 1-\varepsilon
\quad\text{或}\quad
\operatorname{val}(\Pi)\le
\frac{k(1+\varepsilon)}{(k-3)R}.
\]
取 k=6 并套用 Theorem 3.1，得到大参数 k-DM 的约 `k/(12+ε)` 近似硬度。附录 A 用素数密度选取 `p` 附近的 `kR`，再在每条边上添加独立 dummy 顶点，把只对 `kR` 维成立的结果扩展到所有充分大的 p；dummy 顶点各自只接一条边，匹配大小不变。复杂度假设仍是 `NP ⊆ BPP`，随机性来自 CSP 稀疏化，不能改写成只需 `P≠NP` 的确定性结论。

## 仿射线 gadget 和为什么匹配值相等

对每个变量 v，取资源点集 `X_v=F_R×F_R`。若 v 的出现次数为 `d_v≤R`，给包含 v 的每条有序约束一个不同的截距编号 `b∈F_R`，并对标签/斜率 `a∈F_R` 定义
\[
e_{a,b}=\{(x,ax+b):x\in F_R\}.
\]
同一斜率的不同截距两两不交；不同斜率在素数域中由
\((a-a')x=b'-b\) 有唯一解，因而恰交一个点。于是任一匹配在同一变量 gadget 内只能使用一个斜率颜色，最多取 `d_v` 条边；颜色即变量赋值，截距即约束发生次序。

对约束 `C=(v_1,\ldots,v_k)` 和其允许赋值 `a=(a_1,\ldots,a_k)∈C_C`，输出一条 kR-集合
\[
e(C,a)=e_{v_1,C,a_1}\cup\cdots\cup e_{v_k,C,a_k}.
\]
每个局部线恰含 R 个点，所以输出集合恰含 kR 个点。若原实例 k-partite，把每个变量 gadget 按第一坐标 x 分成 R 个列，再和 CSP 的 k 个分区组合，得到 kR 个点分区；每条输出边每个分区恰一个点。

同一变量中匹配边只能选一个颜色，因此任意输出匹配给每个变量确定一个标签，并且匹配边对应的约束必被该标签赋值满足。反向地，任意赋值把每个满足约束送入对应边；同一颜色的线平行不交，故这些边构成匹配。两方向给出最大匹配数等于最大满足约束数的精确等式。这里的“完整集合匹配”是论文证明的对象；它没有论证把每个集合只保留一小部分资源后的值仍反映 CSP 值。

## 度数稀疏化的承重步骤

Theorem 4.3 从 d-正则 CSP（字母表仍为 R）随机独立保留每条约束，概率
\[
p=(1-\lambda)R/d,
\]
再删去每个变量超过 R 的多余边，得到 R-度有界实例。对充分大的 R，以高概率同时成立：

- 完备性：`val(Π') ≥ val(Π)-3λ`；
- 若原 `val(Π)≤CR^{-γ}`、`γ≥2`，则
  \[
  \operatorname{val}(\Pi')
  \le
  \frac{k(1+\lambda)}{(\gamma-1)(1-\lambda)^2R}.
  \]

证明把采样边数视作独立 Bernoulli 和：对固定赋值用 Cantelli/方差界控制满足边数；用 Markov 控制超度删除量；用 Chebyshev 控制总边数；soundness 对全部 `R^{|V|}` 赋值作 Chernoff 上界和 union bound。Theorem 4.2 引入 Chan 的 d-正则 k-CSP gap，再令 λ 足够小得到 Theorem 4.1。故随机稀疏化的成功概率、`R` 充分大、k 固定等条件都是承重假设。

## 量词、边界和没有声称的内容

论文的 YES 是 `1-ε` 而非完美满足；只有在给定一个真正全满足赋值时，仿射 gadget 才能取每个变量同一斜率、不同约束不同截距，从而得到完整互不交集合。不能把“近完美”自动提升为这个 witness。论文也不处理空关系在后续编译中是否需保留 selector、非素数域、非均匀权、把多个允许 tuple 当独立 group、额外调度任务或任意 `R||C_max` 解码。

Theorem 1.1 的 `k/(12+ε)` 是渐近、大维度、近似比的复杂度事实，不是一个固定小 k 的有限反例，也不是普通调度 `OPT` 的上下界。附录 dummy 扩展保持匹配大小，但没有提供调度语义、机器负载或时间表。

## 与现有不相关机正文的关系

仓库已有仿射线 uniform compiler 的独立 Exact/Proof 审查，使用本论文的局部 affine-line 几何，但其对象是另一个“每组任取一个 state，再由 Hall 流分配半数资源并回填普通 UM jobs”的条件合同；它允许局部 labels 不来自一个全局 CSP 赋值，并明确给出 `C_max≤3/2` 的实际时间表。该合同不能反向升级为本论文的近似困难性，也不能把论文的完整集合匹配结论套到 tuple-as-group/dummy 或非均匀 compiler。两者共同使用斜率/截距线相交事实，但量词、任务身份和目标不同。

已有 `三维匹配与高维配额部分障碍双源审查` 把本论文只作为高维匹配 Paper Fact，并说明完整 K 层匹配不足以控制部分配额层；本对象补足了论文原文的精确 CSP 定义、仿射线等式、稀疏化概率和 `NP⊆BPP` 边界。后续若要把 LST 接到 `R||C_max`，必须另证所有部分层的 soundness、可计算 decoder 及实际负载与 source 值的对应。

## 证据、处置与接续

两份冻结 PDF 均已完整阅读；a583 与 e12 的 SHA 与字节完全相同，数学内容合一，第二份保留为重复来源。独有信息去向为本对象：定理/定义/证明位置、精确量词、随机化复杂度和与现有调度合同的边界。没有执行论文外部代码，也没有把有限审计当一般证明。适合第三阶段作为“来源”节点连接到仿射线编译审查与高维配额障碍；不应连接为 `UM-TARGET-v1` 的无条件否定。
