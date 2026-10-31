---
id: matroid-structures/exchange-distance-independent-review-source-boundary
kind: review
type_tag: 审查
title: 公共基交换有向图围长距离独立审查源的处置边界
status: integrated-into-existing-exchange-distance-object
truth_status: internal-proof-reconstruction-preserved; novelty-and-application-pending
review_level: full-source-read-and-cross-archive-comparison
summary: "完整读取 3394 字节的独立重建稿。其 P(S) 稳定引理与 dist_D(u,v)≤k−g+3 证明已由现有 matroid-structures 资料对象逐段承接；本源新增的是独立审查 provenance、边界枚举和不依赖表示性的明确声明，不应另造重复定理。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/notes/matroid_exchange_distance_independent_review.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/notes/matroid_exchange_distance_independent_review.md
source_id: f93fec4373a3bb09191d
source_blob: 199ea65c131b64d13d102028f419c992704fe4ef
source_sha256: 3f9f1984a7e6de9e44614968c3aa2af67b313efe616c1151bbdec9b27937c689
source_size_bytes: 3394
evidence_path: archives/matroid-structures/tools/evidence/retired-topic-claims-20261031/matroid_exchange_distance_independent_review.md
related_objects:
  - archives/matroid-structures/state/资料/交换距离与等长theta相关间隙的独立接口--资料.md
  - archives/matroid-structures/state/审查/成本保留Chernoff舍入标准推论审查--审查.md
  - archives/weighted-congestion/state/资料/有限双权近似势与非对称精炼目标的不同合同--资料.md
---

# 阅读与来源身份

`clean show f93fec4373a3bb09191d` 导出的冻结文件为 3394 字节，SHA-256 为 `3f9f1984a7e6de9e44614968c3aa2af67b313efe616c1151bbdec9b27937c689`；`legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 内容相同。全文逐段读取，没有把标题或摘要当作证明。

稿件声明它是对公共基族诱导交换有向图的独立反向重建，研究有限拟阵 `M=(E,I)`、rank `k`、最小 circuit 大小 `g`，以及任意非空（允许重复）基族 `𝓑`。在有弧 `r→s` 当且仅当某个 `B∈𝓑` 满足 `r∈B,s∉B,B-r+s` 为基的图 `D` 中，合同结论是任意可达不同顶点满足

`dist_D(u,v) ≤ k − g + 3`。

稿件逐步给出 `P(S)=S∪{r: ∃s∈S, r→s}` 的稳定引理：若 `rk(P(S))=rk(S)`，则 `P(P(S))=P(S)`。证明使用基本 circuit、closure 和 `B∩cl(S)` 的基性质，随后从终点首个基本 circuit 的 rank 至少 `g−1` 以及之后每一层严格增秩推出距离界。它明确说明不依赖 GF(2)、表示性、可定向性、graphic matroid 或原子博弈假设。

# 与现有对象的比较

现有 `archives/matroid-structures/state/资料/交换距离与等长theta相关间隙的独立接口--资料.md` 已完整承接同一距离合同、前向层证明、该 `P(S)` 稳定引理、反向层推导及 loops/coloops/平行元/不连通/free matroid 边界；该对象还保留候选 PoA 应用的独立量词和未闭合的新颖性/函数域义务。本次 source 不提供新的应用定理，也不把有限 GF(2) 枚举提升为全拟阵证明。

本源相对既有对象的独有 provenance 是：审查日期和“未先读 atomic_games 证明草案”的独立阅读声明、独立重建的完整短稿、以及对 `𝓑` 可重复、可为单基、loop/coloop/free/disconnected 边界的集中列举。其数学内容应作为现有对象的独立来源证据，而不是第二个同名定理。与 `weighted-congestion` 的原子拥塞、与 `unrelated-machines` 的高 girth 配置源只存在模型类比；不能把拟阵交换图距离界外推成机器实例 gap 或均衡结论。

# 处置与接续边界

处置建议为 `integrated`，目标是现有交换距离资料对象和本源原字节证据副本。第三阶段可建立“独立重建来源 → 交换距离候选”及“来源 → 证明接口”关系；不建立“来源 → 已证外部文献/新颖性”或“来源 → 高 girth 机器 gap”关系。若将来升级为定理，仍需独立核对文献新颖性、PoA 应用的完整域（零成本、端点和实际 PNE）及是否存在更紧锐界；本源自身不完成这些义务。
