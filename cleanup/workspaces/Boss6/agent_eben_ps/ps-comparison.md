---
id: "cleanup/ebenlendr-krcal-sgall-ps-format-comparison"
kind: "resource-audit"
type_tag: "版本比较"
title: "Ebenlendr–Krčál–Sgall 2014 Graph Balancing PS 与 PDF 版本比较"
status: "read-and-compared-duplicate-format"
summary: "冻结 PostScript 与同论文 PDF 的数学文本逐字一致；PS 没有可登记的独有数学内容，建议 duplicate 指向 PDF 资源对象。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/ebenlendr_krcal_sgall_2014_graph_balancing_author.ps#pp1-20"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/ebenlendr_krcal_sgall_2014_graph_balancing_author.pdf#pp1-20"
source_ids:
  - "cf77d3613b18af8fa7bf"
  - "9244cba192cc71b62623"
source_sha256:
  ps: "3b4c2fcc89926d9e1fc6ee560b264a4b2fc13857c31759f81ec1d74d66a5706d"
  pdf: "a407bdbda09ea649f72454518f8dce526405fe7743a38abeb8ed499dee4918d5"
---

## 冻结身份与实际读取

- PS 源 ID `cf77d3613b18af8fa7bf`，路径 `history/source/literature/unrelated_machines/ebenlendr_krcal_sgall_2014_graph_balancing_author.ps`，大小 223535 字节，SHA-256 `3b4c2fcc...`（完整值见源清单）。头部是 DSC Level 2、`%%Pages: 20`、dvips 2012-05-23-1154。
- 同论文 PDF 源 ID `9244cba192cc71b62623`，路径 `.../ebenlendr_krcal_sgall_2014_graph_balancing_author.pdf`，大小 175030 字节，SHA-256 `a407bdbda09ea649f72454518f8dce526405fe7743a38abeb8ed499dee4918d5`。
- 使用 `work.py clean show ... --out` 分别导出；PS 以 `TMPDIR=$PWD/tmp_ps ps2pdf` 转换后，用 `pdftotext -layout` 读取。两份提取结果均 1015 行、9873 词、60327 字节；`cmp -s source.txt author.txt` 返回 0。20 个物理页（提取文件尾部换页符产生一个空尾页）均存在，章节/图表/定理编号一致。

## 数学内容核对

全文内容是 Ebenlendr–Krčál–Sgall, *Graph Balancing: A Special Case of Scheduling Unrelated Parallel Machines*：

1. 图平衡模型为带专属负载的加权多重图；边只能指向其两个端点，目标最小化最大顶点负载。等价于 restricted assignment 中每个任务至多两个等时可用端。
2. LP1（边守恒、顶点负载）配合 ROTATE 给 2-近似；LP1 的积分间隙可趋 2。
3. LP2 增加任意大边子树的 leaf-pair 约束；ROUND 按 Leaf Assignment、Tree Assignment、Rotation 交替，并用树约束维持 1.75 负载不变量。
4. LP3 以每顶点大边星约束替换为多项式规模；Theorem 2 证明 LP3 ⇒ LP2 且分数大边图是树/环并；LP-BALANCE + ROUND 给多项式 1.75-近似（GBapx 语义为 FAIL 或 ≤1.75 取向）。
5. LP2/LP3 的积分间隙均可达 1.75；三端超图的自然 LP3 扩展积分间隙为 2；配置 LP 对普通 graph balancing 至多 1.75，而一般不相关机及带速度 graph balancing 的配置 LP 间隙可趋 2（Theorem 4）。
6. 开放问题保留：图平衡的 1.5–1.75 区间、一般不相关机低于 2、异端权重的 unrelated graph balancing。

PS 本身只是同一冻结作者稿的排版格式。没有额外定理、证明、例子、勘误或独有图；所有数学内容由 PDF 版本承重，PS 只作为重复格式源。

## 全仓比较与处置建议

已检索 `archives/unrelated-machines/state`、`tools/evidence` 和 `research` 中 `Ebenlendr/Krčál/Sgall/Graph Balancing` 命中；未发现已有同论文专门对象。相邻资源为配置 LP、Svensson/Jansen–Rohwedder、Verschae–Wiese 与 Asahiro 等，但它们不吸收本论文的 LP3/ROUND 论证。建议由 PDF 源建立一个独立文献资源对象（例如 `archives/unrelated-machines/state/资源/Ebenlendr等--图平衡1.75近似与配置LP间隙--资源.md`），把本 PS 源登记为 `duplicate`，`targets` 指向该 PDF 对象；不要另造 PS 数学对象。

PS 版本已完整转换/读取，不能只以“同名”判重：判重证据是导出后全篇文本逐字节相等，并核对 20 页页数/DSC 头。该结论不把作者稿升级为外部当前最佳，也不把 graph balancing 结果迁移到六人 Q-CAG-HALF-6。
