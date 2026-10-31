---
id: fair-allocation/personalized-bivalued-efx-monotone-completion-obstruction
kind: review
type_tag: 审查
title: 个性化双值 EFX 效用单调补全障碍
status: integrated-method-obstruction; finite-audit-referenced; general-efx-po-open
truth_status: proof-scope-obstruction-only
review_level: full-source-read-cross-archive-comparison
summary: "完整读取三人五物个性化双值 goods 的参数族笔记。该族严格否定‘任意 EFX 起点都能沿逐人效用不降路径补成 EFX+普通 PO’这一更强路线；它不否定每个实例存在 EFX+PO，也不解决 Jin--Tao 的一般兼容性问题。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/notes/personalized_bivalued_monotone_completion_obstruction.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/notes/personalized_bivalued_monotone_completion_obstruction.md
source_id: ad497e4442a9f23a486d
source_sha256: b26727ff28d2552b3b41a176f5f9f0183acdb9bc15891d13f38784807330d6c8
source_size_bytes: 5063
source_evidence: archives/fair-allocation/tools/evidence/retired-topic-selection-20261031/personalized_bivalued_monotone_completion_obstruction.md
related_objects:
  - ../资料/可加公平与副本前缀目标的候选反例分层--资料.md
  - 三值家务EFX反例与公平fPO边界三源处置--审查.md
  - ../资料/图定向残差与两平行类秩成本的独立合同--资料.md
---

# 来源身份与模型

冻结源 `ad497e4442a9f23a486d` 是一份 5063 字节的研究笔记，`legacy-cleanup` 与 `main` 两冻结提交内容相同，SHA-256 为 `b26727ff28d2552b3b41a176f5f9f0183acdb9bc15891d13f38784807330d6c8`。它不是 Jin--Tao 原论文，也不是一般兼容性定理；它专门攻击一条更强的证明路线：先取任意 EFX 分配，再只允许每个代理效用不下降，试图走到仍为 EFX 的普通 Pareto 最优整数分配。

模型是三名代理、五件不可分 goods、严格正的个性化可加估值。代理 1 的五件价值为 `(1,1,1,a,a)`，代理 2 为 `(1,1,b,1,1)`，代理 3 为 `(1,1,c,c,c)`。参数为有理数
`3/2<a≤2`、`b≥2`、`c>2`，并且 `a<2` 或 `b>2`。完整分配的普通 PO 只比较整数分配；EFX 按任意代理、任意比较代理和比较包中的任意单件删除定义。

取
`X_1={4,5}`, `X_2={1,2}`, `X_3={3}`，效用为 `(2a,2,c)`。每个比较包至多两件：代理 1 删除一件后对方包价值至多 1，代理 2 同样至多 1，代理 3 看代理 1 删除后剩余一件高值物为 `c`、看代理 2 删除后至多为 1，故 X 是 EFX。由于代理 1 的包仍可被改进，X 不是 PO。

# 逐点不降的支配者穷尽

设 Y 弱 Pareto 支配 X 且至少一人严格改进。每个代理必须拿到非空包，所以代理 1 至多拿三件，并且其效用至少为 `2a`。

若代理 1 只拿两件，因 `a>1`，达到 `2a` 的唯一两件集合是 `{4,5}`。代理 3 为达到 `c>2` 必须从 `{1,2,3}` 中拿物品 3；代理 2 为达到 2 只能拿物品 1、2，于是 Y=X，不可能严格改进。

因此任何严格支配者都让代理 1 拿三件、其余两人各拿一件。代理 2 达到目标 2 只能拿物品 3；代理 3 为达到 `c` 必须拿 4 或 5；于是唯一两种候选是
`({1,2,4},{3},{5})` 与交换 4、5。二者效用均为 `(a+2,b,c)`，在 `a≤2,b≥2` 且 `a<2` 或 `b>2` 时严格支配 X。但代理 3 看代理 1 的三件包，删去低值物品 1 或 2 后仍见 `c+1>c`，所以两个候选都违反 EFX。由此不存在 EFX 且严格逐点支配 X 的整数分配。

这是一个完整的参数族证明草案，承重条件正是 `3/2<a≤2`（排除代理 1 以三件低值物品达到目标）、`c>2`（强制代理 3 取高值物品）和 `a<2` 或 `b>2`（保证严格改进）。等号或空/零值边界不属于该结论。

# 独立核验与严格范围

笔记记录基例 `(a,b,c)=(2,3,4)` 的独立 Fraction 穷举：243 个完整分配、2 个严格支配者均违反 EFX；该实例有 21 个 EFX 与 13 个 EFX+PO 分配。这个结果只能支持指定输入和该方法边界；它不是“无 EFX+PO”反例，也不是多代理一般性证书。笔记另称参数网格、等号边界和空/零输入已检查，但本次未将其另行冻结的程序与 JSON 源纳入独立 `clean show`，因此不把那些未领源的运行细节当作本批重跑结果。

全仓比较确认，`archives/fair-allocation/state/资料/可加公平与副本前缀目标的候选反例分层--资料.md` 已保存同一参数族的简要证明和量词边界；`三值家务EFX反例与公平fPO边界三源处置--审查.md` 则保存另一模型的 chores 与两代理 goods/fPO 边界。后者的已知 EFX/fPO 分数不兼容不等同于本源的普通 PO 或逐效用补全障碍。`图定向残差与两平行类秩成本的独立合同--资料.md` 也明确 rank chores 与本 goods 模型不同。

# 处置与接续

处置为 `integrated`，因为本源独有的是完整参数族的“强路线失败”证明、严格参数作用和两候选支配者穷尽；正式对象不把它提升为 EFX+PO 不存在定理。第三阶段只宜建立“方法障碍/已知反例/模型对照”关系到上述可加公平资料对象。真正的一般问题仍需分别处理：是否存在某个 EFX+普通 PO 分配、个性化比率下的结构界，以及允许效用回退或改变起点的算法。