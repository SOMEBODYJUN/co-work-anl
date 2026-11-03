---
id: fair-goods/copies-sd-ef1-exhaustive-result-v1
kind: review
type_tag: 审查
title: 退役公平商品 goods-with-copies SD-EF1 穷举结果处置
status: finite-exhaustive-evidence-open-universal-question
truth_status: finite-computational-evidence; no-formal-proof; universal-existence-open
review_level: full-frozen-result-read-cross-archive-comparison
summary: "完整读取 copies_exhaustive_results.json；保留三代理、至多四个非全体类型、重数1/2的9216 profile穷举、最坏排序和最少证人数值，明确这不是任意人数/类型数的 SD-EF1 定理。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/evidence/runs/topic_selection/fair_goods/copies_exhaustive_results.json
source_ids: [7ead041568d237b20080]
source_sha256: [6698e99b16641989d53412fd86a3ad1da67160868e262e0d7baedb0e269059b8]
source_blobs: [5d1d2d935807bc06f09fd450db8a247669a9cff8]
source_commits: [68fad804ec5946cb296f77dc5b336308a66abf12 (legacy-cleanup), aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c (main)]
evidence_manifest: ../../tools/evidence/retired-fair-goods-copies-results-20261031/manifest.json
---

# 模型、冻结范围与阅读记录

`copies_exhaustive_results.json` 属于独立的 `fair_goods` goods-with-copies 模型，不是 weighted-congestion、fair_chores、unrelated-machines 或 customer-attraction。一个类型 (g) 有 (c_g) 个等值副本；每个 agent 每类型至多拿一件；agent (i) 对类型/副本按自己的严格排序观察。对所有观察者 (i)、比较者 (j) 和 (i) 的排序前缀 (P)，SD-EF1 的计数形式是

[
|A_i\cap P|\ge |A_j\cap P|-1,
]

等价于从 (j) 的 bundle 删除对 (i) 最优的一件后，(A_i) 至少随机占优。类型副本等值是关键条件；一般 partition matroid 中同类元素可被 agent 区分的反例不能直接移植。

本源 source ID 为 `7ead041568d237b20080`，冻结路径 `history/retired_topic_selection/independent_review/evidence/runs/topic_selection/fair_goods/copies_exhaustive_results.json`，blob `5d1d2d935807bc06f09fd450db8a247669a9cff8`，SHA-256 `6698e99b16641989d53412fd86a3ad1da67160868e262e0d7baedb0e269059b8`，大小 693 bytes。完整 JSON、manifest 与字段验证在 [retired-fair-goods-copies-results-20261031](../../tools/evidence/retired-fair-goods-copies-results-20261031/)。

# 1. 精确有限域

`scope` 字段给出：3 agents；至多 4 个非全体类型；每类重数为 1 或 2；严格 rankings；按 simultaneous type renaming 识别。`profiles_checked=9216`，正好是固定 agent 1 的类型顺序后，对另外两人的 4-type 严格排序 (24^2) 与每个类型 multiplicity pattern (2^4=16) 的乘积：

[
16\times24^2=9216.
]

“非全体类型”是指不出现 (c_g=3) 的类型；全体副本在每个 bundle 比较中同量出现，可以从前缀差中抵消。每个 profile 的 checker 还要遍历全部满足列和与每人每型至多一件的 allocations；JSON 没有单独列出每 profile 的 allocation 数，但它的 `all_instances_have_sd_ef1=true` 是对这 9216 个 profile 的聚合断言。

`minimum_witness_count=9` 表示在这些 profile 中，找到的 SD-EF1 witness allocation 数量的最小值为 9；它不是“每个 profile 只有 9 个 witness”，也不是一般下界。`worst` 保存了达到该最小值的一个 profile：

- multiplicities `[1,1,2,2]`；
- agent 1 ranking `[0,1,2,3]`；
- agents 2、3 ranking 均为 `[0,2,1,3]`；
- `count=9`。

因此最坏实例仍有 9 个通过 SD-EF1 的完整分配，说明有限域内没有以“证人稀缺”直接暴露的失败；但它没有说明任意更多类型、不同重数或更多 agent 仍有证人。

# 2. 结果的数学状态

`all_instances_have_sd_ef1=true` 是有限穷举输出，`boundary` 明确写着“finite theorem verified by exhaustive Python, no independent formal proof; universal copies cancel pairwise counts; weak orders follow by refining ties”。这句话应分解为三个层次：

1. 在所声明的 9216 个严格排序 profile 上，程序找到了 SD-EF1 allocation；
2. “全体副本两两抵消”是该有限编码的结构观察，支持把注意力收缩到 (c_g=1,2) 的非全体类型；
3. ties 可先任意细化再回到弱序，是候选报告提出的处理路线，但 JSON 没有独立形式化证明其对所有弱序及所有后缀/前缀量词的闭合。

因此本源支持把 n=3、最多四个非全体类型的前缀修复问题作为可行研究入口，但不证明“任意 goods-with-copies 总有 SD-EF1”。候选报告的首个承重义务仍是三人混合 multiplicity prefix-repair lemma：保持每一列和，在最早坏前缀上做 alternating exchange，并证明已修复的更早前缀不会循环破坏。普通平均舍入只能给成对误差 2，不能替代 SD-EF1 所需的误差 1。

# 3. 与同档 fair_goods 材料的比较

先前的候选报告与候选清单还记录了更大的随机样本和独立标量核验；那些来源是不同 source ID，本页不把其字节或运行冒充为本源。当前源的独有内容是：精确 scope 字符串、9216 的 profile 计数、`minimum_witness_count=9` 以及最坏的 `[1,1,2,2]`/双排序 profile。它与已有候选正文的关系是“把有限 FG02 检查的聚合结果从候选地图拆成可引用证据”，不是重新声称一个定理。

模型边界必须保持：

- 对任意人数的 goods-with-copies，当前仍是开放问题；三人四非全体类型只是一个有限截面。
- (c_g=3) 的全体类型可以在有限 profile 的 pairwise prefix 差中抵消，但不能据此删除任意类型后声称一般 (c_g\le n) 已解决。
- 严格排序的同时重命名归一化不处理所有 agent 的 ties；弱序回退需要单独证明。
- SD-EF1 是序数前缀目标，不能由普通 numeric EF1、1/2-EF1 或 constrained MNW 的近似保证替代。

# 4. 处置与接续

本源处置为 `integrated-finite-evidence`：原 JSON 复制到 evidence，保留 SHA/blob/大小、有限 scope、最坏 profile 和 9 witness 数值，并在本页明确“无独立形式化证明、普遍问题开放”。第三阶段可建立“有限穷举支撑→三人 copies 前缀修复候选”的启发/有限验证关系，但不得建立“有限穷举→任意 goods-with-copies SD-EF1 定理”边。

验证脚本只检查哈希、693 bytes、9216、9、worst profile 和 boundary 标记；它不能证明 checker 的实现正确性或论文级普遍量词。对应生成脚本是另一个来源，若后续要正式复现，须单独 clean claim、读取并在独立目录运行。
