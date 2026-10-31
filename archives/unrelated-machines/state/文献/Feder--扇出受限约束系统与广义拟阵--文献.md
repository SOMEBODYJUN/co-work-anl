---
id: "unrelated-machines/feder-fanout-limitations-generalized-matroid-parity"
kind: "literature"
type_tag: "文献"
title: "Feder：扇出受限约束系统、广义拟阵奇偶与拟阵交"
status: "retained-literature-formalized"
truth_status: "source-theorems-transcribed-with-open-complexity-boundary"
review_status: "full-PS-read-after-pdf-conversion; cross-archive-comparison"
source_id: "d0fcf01aa8bd6952ea25"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/feder_fanout_limitations_author_original.ps"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/feder_fanout_limitations_author_original.ps"
evidence: "cleanup/workspaces/Boss7/agent_lit_batch/raw/d0fcf01aa8bd6952ea25-clean.txt"
---

# 对象与来源范围

本文是 Tomas Feder 的 Fanout Limitations on Constraint Systems。冻结对象是 d0fcf01aa8bd6952ea25，字节由 work.py clean show 取出；原始 PostScript 先用 Ghostscript 转成 PDF，再以 pdftotext -layout 读取 12 页。正文、定理、证明和结论均已读；源文件中的字体 OCR 字符有少量损坏（例如 ≤、重音符），本页按公式语义校正并保留原文边界。该来源讨论布尔约束复杂度，不是当前六人有限客户 SPE 或调度 payoff 模型。

## 定义域与量词

固定有限布尔模板（关系集合含常量关系）。普通 CSP 实例是有限变量—约束结构，要求存在同态到模板；图约束满足要求每个变量恰出现在两个关系中，约束作为图顶点、共享变量作为图边；二部约束满足再要求约束图二部着色，使每个变量恰连接两侧各一个约束。关系可由受限实例实现：保留只出现在一个约束的变量并投影掉两次出现的内部变量。

一个布尔关系 R⊆{0,1}^k 称为广义拟阵，若对 X,Y∈R，当二者在第 i 位不同、从 X 翻转第 i 位所得 X^i 不在 R 时，存在另一个 j≠i（也在 X,Y 的差异集）使翻转 i,j 后的 X^{ij}∈R。若 R 的所有向量有相同的 1 数，则该交换公理退化为拟阵独立集公理。共独立集是其补集为独立集的关系；子类包含子句、NAE 与模 2 线性关系。

## 主要结论

1. Schaefer 扩展（定理 3）。布尔图 CSP 若模板含常量且不属于 Horn/反 Horn、2-SAT、模 2 线性三类，则可在每变量至多两约束的模型中实现所有含正负文字的子句；二部模型中至少可实现所有单调子句。实现通过闭包失败依次构造二文字子句、三文字子句和归结：非线性闭包失败给 x∨y 或 x≠y，再结合多数/异或闭包失败得到任意子句。
2. 广义拟阵奇偶刻画（定理 4）。把实例中所有广义拟阵约束取不交并，匹配一对变量（要求其两次出现取同值）后，在剩余变量上得到的关系仍是广义拟阵。因此，图 CSP 中若出现非广义拟阵关系，要么落回 Schaefer 多项式类，要么可借助 x=y 或 x≤y=z 等复制关系制造 NP 完全性；剩余新问题正是广义拟阵奇偶。
3. 共独立集特例。把每次不匹配的变量对沿其所在约束改值，产生新的不匹配对；迭代后问题化为在约束图中找一条路径，只有路径末端约束的访问方式影响可行性，故该共独立集图 CSP 可多项式求解。
4. 二部广义拟阵交（定理 5）。若二部模板既不能实现 x=y 也不能实现 x≤y，则可通过补充位使 0/1 数相等，把广义拟阵交换结构嵌入普通拟阵；问题归约到拟阵交并可多项式求解。若能实现 x=y 或 x≤y，则二部性可被消去或复制回路制造 NP 完全性。来源结论只保证这些受限子类，未给出一般广义拟阵奇偶/交的全复杂度分类。

## 推导与失败机制

定理 4 的关键闭包步骤是：若 X,Y∈R 且 x_1=x_2，对另一坐标翻转若失败，广义拟阵公理给出辅助坐标翻转；若辅助坐标是已匹配的第一/第二位，则连续翻转两次仍回到可行关系，故投影关系保持广义拟阵。NP 完全性一侧从全零与全一向量构造最小集合 K；若翻转第一位必须同时翻转至少两位，则限制到三位得到 000、111 在而 100、110、101 不在的关系。A/B/C 三个中间向量的不同出现模式分别给 x=y=z、x≤y=z、x≤y≤z、x≤y,z 或 x=min(y,z)。前几种可与子句拼接复制；最后一种经辅助变量化为 x≤y,z，再用二部回路强迫任意扇出。

二部多项式性使用交换证明：若 X=0^k1^ℓ、Y=1^k0^ℓ（k≤ℓ）在广义拟阵中，且不能实现 x=y 或 x≤y，翻转首个 0 后必须能把某个 1 翻回 0；当 k<ℓ 时 Y 也能删去某个 1。补充哑位保持 0/1 数相同，即可应用拟阵基交换，构造两个拟阵并求交。

## 证据、比较与接续

证据文本为 cleanup/workspaces/Boss7/agent_lit_batch/raw/d0fcf01aa8bd6952ea25-clean.txt；来源 SHA/大小见 cleanup/inventory.jsonl 中该 ID。全仓比较命中 state/文献/稀疏CSP与平坦矩阵两篇文献整理--文献.md 与多份“扇出/匹配”审查；那些对象处理稀疏 CSP 或当前不相关机资源束，未重复本稿的广义拟阵定义和定理。可接续用途是把“每变量两次出现 + 闭包交换 + 路径/拟阵算法”作为有限约束结构的比较语言；不能把其 NP 完全性或拟阵交结论转写为客户目录覆盖或 SPE 存在性。

**状态与缺口**：来源定理及证明机制已保全；一般（固定模板、常数大小约束的）广义拟阵奇偶复杂度仍是原文开放问题，当前正文不扩大量词。
