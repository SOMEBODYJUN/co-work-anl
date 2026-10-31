---
id: unrelated-machines/dobzinski-subadditive-nsw-configuration-lp-literature
kind: resource
type_tag: 资料
title: 子可加 NSW 文献与配置 LP 接口
status: full-pdf-and-compressed-text-read; paired-versions-identical
truth_status: literature-scope-and-interface-notes
review_level: full-23-page-pdf-text-read
summary: "完整读取 Dobzinski–Li–Rubinstein–Vondrák 2023 v1 的 PDF 与 gzip 文本两版本；登记 subadditive Nash social welfare 的配置LP reduction、迭代舍入、oracle和常数因子边界，不迁移成当前 unrelated-machines/SPE 定理。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/dobzinski_li_rubinstein_vondrak_2023_subadditive_nsw_v1.pdf
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/dobzinski_li_rubinstein_vondrak_2023_subadditive_nsw_v1_text.txt.gz
source_ids: [91a2e80713f7c416c7b0, 6fa74681357932f88c7b]
source_sha256:
  - 3ae5ff599f9c5cc367adc1923fdd571d342d967dc2d64e6ad5ff948f3905fc6d
  - 38f1ef5071d4a3440556c8caacbe1282690c5f30b0b0aeed5fed5b33809b13eb
source_sizes: [326593, 23711]
source_commits: [68fad804ec5946cb296f77dc5b336308a66abf12 (legacy-cleanup), aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c (main)]
evidence_manifest: ../../tools/evidence/retired-literature-subadditive-nsw-20261031/manifest.json
---

# 来源一致性与模型

两份来源是同一论文的 PDF 与 gzip 纯文本版本：PDF 23 页、源大小 326,593 字节；gzip 源大小 23,711 字节，解压原始文本 88,992 字节。PDF 经 `pdftotext -layout` 导出 1,391 行，与 gzip 解压文本逐字节一致。本资料因此按一个数学来源、两个版本入口记录，不把双版本计成两项独立结果。

论文模型是不可分物品集合 \(I\)、代理集合 \(A\) 和单调子可加 valuation \(v_i:2^I\to\mathbb R_{ge0}\)。目标是最大化

\[
\operatorname{NSW}(S)=\left(\prod_{i\in A}v_i(S_i)\right)^{1/|A|}
\]

的几何均值；近似因子 \(\alpha\) 表示输出至少 `OPT/alpha`。论文区分 value、demand、XOS 三种 oracle，并强调 subadditive/XOS 一般需要 demand 级访问，不能把 value oracle 自动当作同一模型。

## 1. 主要算法接口

### Configuration LP 与 Theorem 1 reduction

Configuration LP 对每个代理 i、配置 \(S\subseteq I\) 设 \(x_{i,S}\)，每个代理总质量为 1、每件物品总质量不超过 1，目标为加权 utilitarian welfare \(\sum_{i,S}v_i(S)x_{i,S}\)。论文 Theorem 1 给出 NSW reduction：若有一个 relaxation solver 产生满足额外“高值支持/匹配”性质的 configuration solution，并有一个对 utilitarian welfare 只损失常数的 rounding procedure，则可组合成 subadditive NSW 常数近似。

### Lemma 3：去除低值支持

论文先把每个代理的配置分布重整为只保留高值集合（除去价值主要集中于单件物品的代理）。操作是把低值配置质量拆到高值配置的子集，同时保持每件物品的总分配概率；这一步避免理想随机舍入产生大方差。证明只用 monotonicity/subadditivity 和配置 LP 约束，输出仍满足每代理质量和物品边际。

### 迭代舍入与浓度

对剩余代理递归：每一轮筛选一部分代理，用随机过滤确保物品仍足够，再把其配置分配出去。Lemma 4–7 给每轮满意代理比例、价值下界和失败概率；几何级数式的代理层级（约一半、四分之一、八分之一……）贡献一个约 1/4 的 NSW 乘积因子。子可加 concentration 用 Schechtman/Talagrand q-point control（Theorem 17、20）而非 submodular 的更强独立浓度。

### Feige welfare rounding 与 Theorem 10

对 subadditive valuations，论文调用 Feige 的 1/2 utilitarian welfare rounding（Theorem 11），而不是声称自己的随机舍入具有完全浓度。结合 Theorem 1、Eisenberg–Gale relaxation（Appendix A 的 Lemma 12–15）和 rematching Lemma 8–9，Theorem 10 得到：给定 demand oracles，可在多项式时间和多项式查询数内得到 subadditive NSW 常数近似。正文给出的保守总因子约为 `1/375000`（即输出至少 `OPT/375000`）；作者明确说各阶段常数较松，后续可能改善。

论文还说明：XOS 是子可加特例，使用 demand/XOS oracle 时流程更简单；submodular 情形的既有常数算法和这里的 subadditive 方案有不同 oracle/浓度边界，不能混称一个算法。

## 2. 表示、假设和限制

1. 配置 LP 变量按物品集合指数多，但 demand oracle 用于隐式求解；不提供显式配置列表时，算法接口依赖 oracle 模型。
2. valuation 要求单调、非负、子可加；文中 concentration 还对单件价值上界做归一化，再通过缩放恢复一般 \(\nu\)。
3. Theorem 10 是 NSW 公平分配，不是 unrelated-machines makespan、GAP 两容量、Santa Claus 或当前六提供者 SPE；其“agents/items”可与调度代理类比，但没有处理机器处理时间矩阵或客户续局。
4. 论文 v1 的常数是存在性/算法保证，不等于最优近似因子，也不认证任何新文献优先权之外的仓库结果。

## 与本仓库对象的关系

配置 LP、matching/rematching 和 matroid/Delta-matroid 资料可以作为第三阶段的算法背景：它们说明“先找高值 fractional support，再做结构化 rounding”是成熟接口。当前 unrelated-machines 的配置 LP 目标、vector-capacity 子模性反例和六提供者 SPE 有不同容量/客户语义，不能直接导入 Theorem 10 的常数。文献来源已按 PDF/gzip 双版本保全，全文一致性已核；本资料不宣称本仓库有新 subadditive NSW 定理。
