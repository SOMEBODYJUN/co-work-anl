---
id: "unrelated-machines/cartesian-tensor-reverse-root-reproduction-20261031"
kind: "review"
type_tag: "审查"
title: "裸 Cartesian 张量反向放大 root 代码重现与矩阵复核"
status: "retained-audit-only"
truth_status: "byte-identical-finite-reproduction-with-t1-exact-optimum"
review_level: "full-source-read-and-code-reproduction-boundary"
summary: "完整读取 root 实际代码与原矩阵复核记录。来源只报告 audit_only：在新 scratch 目录独立重现全套有限输出并逐字节对照，独立从稀疏 P 生成 expected finite qualification table，核对全部 4710 jobs 的实际 load；t=1 从真实 finite rows 穷举 1024 个 assignments 得 OPT=3/2。它没有实现受限 f 匹配、未知 OPT、一般 unrelated-machines 算法，也没有把有限重现提升为任意 t 结论。"
source_refs:
  - "source:741f30ac35aa85916669:history/source/notes/unrelated_machines/tensor_reverse_root_code_and_reproduction_review.md"
legacy_ids:
  - "UM-CARTESIAN-TENSOR-REVERSE-ROOT-REPRODUCTION-v1"
related_objects:
  - "unrelated-machines/cartesian-tensor-reverse-actual-audit"
  - "unrelated-machines/bare-cartesian-menu-reverse-amplification-counterexample"
---

# 1. 来源身份、实际读域与审计边界

`clean show` 导出的来源 `741f30ac35aa85916669` 位于
`history/source/notes/unrelated_machines/tensor_reverse_root_code_and_reproduction_review.md`，1,306 bytes，SHA-256 为
`55992aaef3d0a14353c28b10f1493cfab5adf9550d47459c9172261dbeabe325`。本页逐段读取原文，并将该冻结原文复制到
`archives/unrelated-machines/tools/evidence/tensor-reverse-root-reproduction-20261031/original/`。

来源的数学身份是对裸 Cartesian tensor 反向放大审计的 root 代码与重现实验记录，而不是新的作者证明。它明确把软件标成 `audit_only`：原程序没有实现受限 `f` 匹配，没有求未知的 `OPT`，没有构造一般 unrelated-machines 算法；本页只接受有限实例复核和代码身份信息。

# 2. 原代码与输入口径

记录给出实际被读取的 `audit_normalized_flat_cartesian_tensor_reverse_amplification.py` 的 SHA-256
`efa03ab9bc976f899e7a1b9bd7af6a96a68ef76c18decbbb7e31921eb18d262c`。程序使用 integer `D` 单位构造矩阵：从全资源筛选支持，建立完整 state 表、selector 和 incidence；固定给定的 cyclic witness
\(\ell_i(g)=g_{(i+1)}\)；独立 checker 回读真实 finite rows，并核对所有有序补组/state pairs 的交点为 1。它以 fresh `mkdir/openx` 方式写出，避免覆盖旧文件。

root 的重现是在全新 scratch 目录 `tensor_reverse_root_reproduction_v1` 中运行同一 repo 代码。记录明确说明没有 import 任何审计构造或校验器，而是从原 `t_sparse_P.json` 逐资源、逐组、逐 state 独立生成 expected finite 资格表，再同实际 sparse rows 比较。因此这部分复核检验的是 finite 输入表、程序输出和清单身份，而不是从输出反推出一个一般存在性命题。

# 3. 输出复现与全 job 读取

新目录生成的 15 个输出文件与 fee 冻结版本逐字节一致，包括 code hash 与 summary；原始输出仍保持 manifest 路径结构。另有 `root_original_matrix_verification.json` 记录独立矩阵核对。该复核逐一 load 全部 4,710 个 jobs 一次，并对真实 finite rows 进行资格回读；这里的“全部”是该冻结有限输入中的 jobs 总数，不是任意 `t` 的无限族。

这项事实与既有 sparse-P audit 的结论可以拼接为：root 代码重现没有改变原模型、processing-time 单位或 selector 语义；它增加了对代码/manifest/output 字节身份的独立证据，并对 expected finite qualification table 做了第二次生成。它没有替代作者数学 proof，也没有把 checker 当作算法正确性证明。

# 4. t=1 的完整优化与 t≥2 的界限

来源说 root 从实际 finite rows 再次枚举 `t=1` 的 1,024 个完整 assignments，得到峰值 `3/2`（以原单位表示）；这是具体 t=1 实例的 exact optimum 复核。此前的 sparse audit 只把 `t=2,3,4` 的循环 witness 和 all-jobs 合法性列出，没有给这些层做完整优化；本来源也没有补做它们的 optimum 搜索。

因此当前可安全使用的陈述是：冻结的 t=1 实例有二次独立枚举确认 `OPT=3/2`，并且 root 重现了全套 finite outputs、有限资格表和全部 jobs 的 load。不可使用的陈述包括“每个 t 都有 `OPT=3/2`”、“t≥2 的 witness 已经最优”、“该程序给出所有 t 的反向放大定理”或“由此得到一般 hardness/近二下界”。

# 5. 与相关来源的比较与可接续内容

与《裸 Cartesian 张量反向放大独立实际稀疏审计》相比，本源独有的是：代码 hash、fresh scratch 重现、15 个输出的逐字节相等、独立生成 expected finite qualification table、全 4,710 jobs 的逐次 load，以及从实际 finite rows 做的 t=1 第二次 1,024-assignment 穷举。与裸 Cartesian Exact/Proof 和 ternary palette tensor 系列相比，它不增加新的模型对象；后者的三叉 palette 障碍不能因共享 tensor/cartesian 名称而并入本源的二元有限复核。

后续接续应把本页作为“有限审计 → 可复现证据”边，保留 `OPT=3/2` 的 t=1 条件标签；若要声称 t≥2 最优、一般 `t` 递归或 source hardness，仍须另有完整优化或证明。软件输出应继续以 evidence manifest、代码 hash 和 frozen input hash 绑定，不能只凭字段检查推断数学正确性。

# 6. 处置

处置为 **retained**（语义上是 `retained-audit-only`）：保留原文、代码身份、逐字节输出和 finite matrix verification 证据；正文明确 t=1 exact、t≥2 未优化以及 audit_only 边界，不新建一般反向放大定理或 unrelated-machines hardness 结论。
