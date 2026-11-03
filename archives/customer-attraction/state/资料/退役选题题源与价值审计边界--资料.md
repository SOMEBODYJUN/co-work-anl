---
id: customer-attraction/retired-topic-source-authority-and-value-audit
kind: resource
type_tag: 资料
title: 退役选题题源与价值审计边界
status: historical-provenance-value-audit; no-math-certification
truth_status: source-classification-and-priority-judgment-only
review_level: full-source-read-cross-archive-comparison
scope: history/retired_topic_selection/multi_lane/research/topic_selection/notes/source_authority_audit.md; candidate provenance, author-source identity, value and completion boundaries
summary: "完整读取题源与价值审计：核对历史候选池的 A/B/C 来源标签、59 条记录与 exclude 边界，区分作者明确原题、作者建议方向和团队派生子题；保留 AP/公平分配/两容量 BMKP 等前排来源判断、作者身份核查和 FA09 等题源修正。该资料不认证候选仍开放、不证明新颖性或可完成性，也不把作者声望转移给团队子题。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/notes/source_authority_audit.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/notes/source_authority_audit.md
source_id: 331b5b18686559309e61
source_blob: 566ea0269bab5b3f3cf065686d7be0a4c0e945eb
source_sha256: 4500755bad6809313defe070c620607eead51c71f8624a2d4aaf2d4c713243b6
source_size_bytes: 13200
evidence_paths:
  - archives/customer-attraction/tools/evidence/retired-topic-selection-20261031/source_authority_audit.md
related_objects:
  - 退役选题索引与版本去重边界--资料.md
  - 同行选题比较与候选优先级边界--资料.md
  - 两套退役账本的逐命题来源分诊--资料.md
  - 仓库读取地图与退役双来源恢复--资料.md
---

# 来源身份与审计范围

冻结源 `331b5b18686559309e61` 是一份 2026-10-20 的题源与价值审计，路径为 `history/retired_topic_selection/multi_lane/research/topic_selection/notes/source_authority_audit.md`。`clean show` 导出的两份冻结定位内容相同，大小 13,200 字节，SHA-256 为 `4500755bad6809313defe070c620607eead51c71f8624a2d4aaf2d4c713243b6`；基线与旁读的 `research/topic-selection` 分支分别记录在原文中。

审计对象是候选题的来源身份、母工具和潜在价值，不是新数学定理，也不是全面文献查新或外部审稿。它明确把作者声望、母文质量、团队子题的独立贡献、当前正确性、可完成性和发表价值分成不同轴；同一卡片的母问题是作者题（A），不使后来附加限制的团队子题自动成为 A。

## 历史候选统计的准确含义

原文逐项读取 `candidate_pool.json` 并核对来源与状态小计：59 条历史记录中 A=12、B=2、C=45；其中 7 条为 exclude，非 exclude 的 52 条为 A=10、B=2、C=40。A 表示作者明确提出的原题，B 表示作者建议方向，C 表示团队派生精确问题。该统计沿用历史标签，不重新认证 12 条 A 题当前仍开放，也不把 exclude 一概解释为数学错误；合并、版本变化和已闭合子题都可能导致 exclude。

这些数字与 [退役选题索引与版本去重边界](退役选题索引与版本去重边界--资料.md) 的 59 条索引相互印证，但本源独有的是对“谁提出了什么、价值评价凭什么成立”的审计和修正。它们不是当前清洗分母、开放问题数量或完成来源数量。

## 来源较强的前排判断

审计把下列候选列作更符合“具体题源＋可形成成果”要求的前排。以下均只是研究判断；候选仍须独立查重、重建证明和核对真实输出。

| 候选 | 可核来源与身份 | 审计保留的数学差额与边界 |
| --- | --- | --- |
| AP-02 非对称拟阵拥塞纯 perfect equilibrium | 母文 `The Complexity of Equilibrium Refinements in Potential Games` v2 §6 明确去对称方向；affine 非对称子题仍是团队 C | 机制上从 Nash 提升到扰动稳健选择，需核最近邻、真实算法输出和位复杂度；不能称作者点名该 affine 子题 |
| FG01 四人 laminar EF1 与 K8/K12 | Cookson–Shah 论文 §5/Appendix B 明确四人方向 | 两个 key 的连续估值量词若闭合可直接推进母问题；有限物品数或随机样本不替代全估值证明 |
| FG02 copies SD-EF1 | Cookson–Ebadian–Shah AAAI 2025 §3.3.2 保留的 Open Question | copies 的 identical-copy 结构与一般 partition 负例不同；三人有限枚举只是证据，不是任意类型数定理 |
| GA-03 两容量 BMKP | Chen 等 ICALP 2026 §7 明确询问常数容量种类扩展 | 两容量联合 critical、全局供给和总损失若闭合会直接推进近紧近似；当前仍是 C，不能把作者来源转给团队候选 |

审计同时保留重边参数/去 shared weight、Group GAP、非线性 cloning、有限权重势和 Hao–Michini 拟阵 PoA 等题的真实价值或来源修正，但不把来源强度当数学真值。它提醒：FA01/FA02 等自然题即使来自职业早期作者，也不能因“非大佬”而降低其数学价值；反过来，成熟作者的工具引用也不认证团队 C 子题。

## 题源修正与模型分离

原文修正了 FA09 的直接题源，应引用 Jin–Tao WINE 2025 的原始问题，而不是把 He–Tao 后续转述当作首发；这只修正 provenance，不改变 EFX+普通 PO 与 EFX+fPO 的数学区分。原文还区分：

- 设施、GAP、BMKP、公平分配、原子拥塞、Nash 精炼和拟阵题属于不同模型；共同出现在候选池不产生数学依赖。
- 综述或母工具的作者声望只能支持“值得查阅”的来源判断，不能证明当前版本仍 OPEN、团队修改保持了原量词、或者所得子题新颖。
- 有限程序、随机样本、内部检索阴性和官方接收/主页信息分别是证据、背景或 provenance；它们不替代完整证明和文献查重。
- `AP-02`、FG01、FG02、两容量 BMKP 可共同进入来源优先级比较，但不能把这种排序当成功率、发表概率或跨模型主线。

原文还列出作者与论文入口（EC2026、Cookson–Shah、AAAI copies、ICALP BMKP、ESA Group GAP、cloning、HKS/HKM、Hao–Michini 等）及其核查边界。这些 URL/主页是来源定位线索；本次清洗保留源文件的记录，不把网页入口当作本对象已独立完成的外部审稿或新颖性认证。

## 与既有资料的关系

[退役选题索引与版本去重边界](退役选题索引与版本去重边界--资料.md)保存 59 条卡片、四条研究线和去重/闭合状态；[同行选题比较与候选优先级边界](同行选题比较与候选优先级边界--资料.md)保存另一份 boss17 的优先级地图；[两套退役账本的逐命题来源分诊](两套退役账本的逐命题来源分诊--资料.md)把账本中的来源拆到各自数学对象。本源不复制这些对象的数学证明或有限审计，而是补充“作者明确题／作者建议方向／团队派生子题”的身份审计、作者与论文身份澄清、前排判断依据及 FA09 等 provenance 修正。

第三阶段如建立关系，只能使用来源、版本、更正、候选优先级或模型对照语义；不得由作者身份建立 `derives`/`proves` 边，不得把“第一梯队”变成数学结论。

## 处置结论

处置为 `integrated` 资料资源。正式保全的是题源分类、59/52 统计的历史语义、前排候选的来源与首个承重义务、作者身份与题源纠错、以及“名作者不认证子题、有限查新不认证开放”的边界。它没有证明任何候选仍开放、没有认证新颖性、没有给出一般算法或均衡定理，也没有把历史统计写成全仓当前进度。
