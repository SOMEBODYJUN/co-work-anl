---
id: "unrelated-machines/ebenlendr-krcal-sgall-graph-balancing-2014"
kind: "literature"
type_tag: "文献"
title: "Ebenlendr–Krčál–Sgall 图平衡的 1.75 近似"
status: "source-read-retained"
truth_status: "author-theorem-summary; not independently reproved"
review_level: "full-pdf-and-postscript-read; format-duplicate-checked"
summary: "作者稿证明每个作业至多两个等处理时间端点的 restricted-assignment 图平衡有 1.75 近似；核心是含树约束的 LP2、可多项式分离的 LP3 与叶分配/旋转舍入。PS 版本与 PDF 文本逐字节一致。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/ebenlendr_krcal_sgall_2014_graph_balancing_author.pdf#pages-1-20"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/ebenlendr_krcal_sgall_2014_graph_balancing_author.pdf#pages-1-20"
source_ids:
  - "9244cba192cc71b62623"
  - "cf77d3613b18af8fa7bf"
source_sha256_pdf: "a407bdbda09ea649f72454518f8dce526405fe7743a38abeb8ed499dee4918d5"
source_sha256_ps: "3b4c2fcc89926d9e1fc6ee560b264a4b2fc13857c31759f81ec1d74d66a5706d"
bibliographic:
  authors: "Tomáš Ebenlendr; Marek Krčál; Jiří Sgall"
  title: "Graph Balancing: A Special Case of Scheduling Unrelated Parallel Machines"
  pages: 20
  version: "author manuscript"
---

# 来源与对象

冻结作者稿共 20 页；PDF 为 175030 字节，PS 为 223535 字节。两份源分别导出为 1015 行、60327 字节的 `pdftotext -layout` 文本，`cmp` 结果相同，因此 PS 只保留为格式版本，不重复建立数学对象。本文研究无向多重图边定向：顶点是机器，边是作业；每条边只能定向到一个端点，目标最小化顶点入边权重之和的最大值。它等价于 restricted assignment 的特例：每作业至多两个可用机器，且两端处理时间相同。它不是一般 unrelated-machines，也不包含六人客户目录 SPE 的历史、策略或均分价值。

归一化决策版本给定顶点基载荷 `q_v` 和边权 `p_e`，判断是否存在定向使 `q_v+Σ_{e→v}p_e≤1`；若不存在，算法允许输出 `FAIL`，并要求存在所有定向都使某顶点负载超过 `1.75` 的证书。标准二分和缩放把该过程转为优化近似。

## LP1、旋转与增强约束

LP1 对每条边 `e={u,v}` 设 `x_{eu}+x_{ev}=1`，对每个顶点约束 `q_v+Σ_{e∋v}p_e x_{ev}≤1`。整数可行点与边定向一一对应。给定 LP1 分数解，沿其正支撑图的有向环执行 `ROTATE`：令环上某一端的质量增至 1、另一端减至 0，保持每条边总质量和各顶点分数负载不增。重复旋转消去分数环，得到整数定向，但直接使用 LP1 的积分间隙仍可达 2。

## LP2 与 1.75 舍入

令大边 `E_B={e:p_e>1/2}`。在任何负载至多 1 的定向中，大边在 `G_B` 中必须一一占用端点，因此 LP2 在 LP1 上加入每个 `G_B` 树 `T` 的树约束，限制树上边的分数负载与顶点剩余容量。树约束是指数多条，但其含义是排除大边森林中不可能同时整定向的局部过载。

`ROUND` 维护 LP2 可行分数解及以下不变量：顶点当前负载不超过 1.75；未定向边的支撑图无危险叶时可沿环旋转；出现叶时仅在叶端增载不超过 0.75 的条件下执行 `LeafAssignment`；大边所在连通分量的树约束始终保持。若所有边均已整数化，输出定向即给出 1.75 负载上界。Theorem 1 通过对 LeafAssignment、Rotation、树分量重排的逐案分析证明这些不变量。

## LP3 与多项式实现

LP3 用每个顶点的 `Star(v)` 多项式约束替代所有 `Tree(T)` 约束。Theorem 2 证明 LP3 的任意解满足 LP2 的全部树约束，并且大边分数支撑图的每个连通分量为树或含受控环；证明对树边约束求和并用 `x_{ev}≤1` 恢复任意树不等式。于是可以用普通多项式 LP 算法求 LP3，不需要指数分离 oracle。Algorithm `LP-BALANCE` 解 LP3 后运行 `ROUND`；Theorem 3 给出 GBapx 的正确性，因而得到图平衡的 1.75 近似。

## 间隙与适用边界

作者稿还给出三类限制：原 LP1 在长路径上有积分间隙 2；允许作业有三个端点时，含树约束的强化 LP 仍可有间隙 2；若两端处理时间不同（异速图平衡/一般 unrelated graph balancing），该定理不适用，配置 LP 也有趋近 2 的族。图平衡本身 NP-hard，作者及其引用给出低于 1.5 的困难性边界，但本 PDF 不重证外部归约；1.75 是特殊两端等速域的算法保证，不是一般模型的次二结果。

## 与现有正文的关系

本源补充图平衡的具体 LP2/LP3、树约束和 `ROUND` 证明机制；现有 Verschae–Wiese 配置 LP 资源对象承载的是异速两端的配置间隙与不同目标，不能把两者的 1.75 与趋二结果串成同一模型。后续 Jansen–Maack 的结构参数结果另有图/树宽和 restricted assignment 前提。第三阶段可将本源与配置 LP、受限图平衡审查建立“文献来源/模型特例”关系；不得将作者算法当作一般 `R||C_max` 或六人 SPE 的算法。

独立阅读证据、PS/PDF 格式比较及逐页文本保存在 `cleanup/workspaces/Boss6/agent_eben_pdf/` 与 `cleanup/workspaces/Boss6/agent_eben_ps/`。本文件未声称重新实现或独立重证作者算法。
