---
id: customer-attraction/full18-seed-full-spe-terminal-set-exact-bi
kind: computation
type_tag: 计算
title: 十八主题种子的完整SPE终局集合精确归纳
status: finite-instance-exact-replay
truth_status: one-fixed-integer-customer-game
review_level: frozen-source-and-dependencies-read; original-implementation-replayed
source_ids: ["4487d9750c2c81ab3595", "268487a339c0df42447e", "71d8848d280b47450765"]
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_1/full18_exact_bi.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_1/full18_exact_bi.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_1/full18_vertex_recovery.json
---

## 固定实例与所求量

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)，本页仅检查一个给定六人游戏：18个标签U0至U17，114个会员类型，每类为非负整数个单位客户，总数56723525995500。源输入是research_6/seed_full18.json；其_scope明确是新实例，不继承旧必要点的比例或IC。完整114项原件和SHA保留在证据包，不能只凭本页总数重建游戏。

本页求该游戏**所有完整有序历史纯SPE的根终局计数集合**，并在其中求最小覆盖。算法按计数共用子问题的“可实现终局集合”，不要求一份策略在同计数的不同有序历史采用同一续局，因而并非只枚举计数选择器。空主题、重复选择和任意平局均由精确比较保留；本次固定目录不是一般目录的穷尽。

## 集合值归纳为什么保留全部完整历史策略

令q为已选标签的计数向量，E(q)为从该前缀出发可由某份完整纯SPE实现的终局计数。终局时E(q)={q}。在非终局，对每个合法动作a已有非空E(q+e_a)。令u_a(t)为当前提供者选择a且终局为t时的最终份额收益，定义

\[
F(q)=\max_a\min_{t\in E(q+e_a)}u_a(t).
\]

则精确递推为

\[
E(q)=\bigcup_a\{t\in E(q+e_a):u_a(t)\ge F(q)\}.
\]

必要性：任一完整SPE在每个动作分支都有某个后继SPE；当前选择的收益至少每个分支选定续局的收益，后者至少该分支的最小可实现收益，故至少F。充分性：给定通过阈值的a,t，在其他每个动作分支各选取达到最小收益的SPE；它们不超过F，故不超过u_a(t)，再在a分支选实现t的SPE即可。动作前缀不同是不同有序历史，允许分别选择续局，后续计数汇合不会施加额外策略相等限制。对剩余人数归纳得到充要性，所有相等情形均保留。

原程序以children中的终局索引数组实现该式，并用np.unique只去除重复终局索引；不会删除产生相同终局的合法平局策略。它输出终局集合而非全部策略列表，也没有导出一份具体完整策略证书。

## 整数运算与范围检查

六人份额分母整除60。Attack按所有计数构建会员负载和60/d整数系数；BI用int64客户重数乘该矩阵、与各标签会员指示相乘。输入客户数N满足

\[
60N=3403411559730000<2^{63}.
\]

所有点积项均非负，份额系数至多60；中间累加也受60N控制。计数/负载的int8值至多6，会员为0/1；终局索引用int32而本例仅100947项。这些界只保障本输入，不能将任意更大重数交给该入口而不重新检查。Attack另有归一化浮点initial与浮点发现方法，但本次BI没有消费initial或调用policy/optimize/linprog。

最优六主题覆盖从全部\(\binom{18}{6}=18564\)个六不同标签支持求最大；非负客户覆盖单调，任意含重复的六槽元组可以补成六不同标签而不降覆盖，所以此处等于允许重复的OPT6。全部计数状态数134596，其中深度6终局100947；它们不是134596份完整有序历史。

## 实际重放及完整报告

本次读取三个主源全部字段和源码、Attack全部实现及114项种子；原样运行一次BI，除stages.seconds外，全部字段与冻结JSON相等。没有重跑浮点锥搜索，不称第二套独立实现。

| 深度 | 状态数 | 各状态保留终局项数之和 | 最大集合 |
|---:|---:|---:|---:|
| 5 | 26334 | 35987 | 13 |
| 4 | 5985 | 12920 | 22 |
| 3 | 1140 | 7100 | 50 |
| 2 | 171 | 3361 | 95 |
| 1 | 18 | 1104 | 161 |
| 0 | 1 | 174 | 174 |

根有174个可实现终局。最小SPE覆盖W=42200434799400，OPT6=56723525995500，故

\[
\frac{\operatorname{OPT}_6}{W}
=\frac{189078419985}{140668115998}<2.
\]

原最坏终局非零标签为3、4、5、9、10、11，各选一次；原最优支持为6至11。该整数客户游戏满足half；它不认证旧必要点所指定的低覆盖路径，也不证明任意游戏的half。

## 88正类型恢复摘要的独立身份

第三主源full18_vertex_recovery.json共四字段：status明确“exact nonnegative rational new game, old-policy full IC not independently exact-audited”，max_float_error=4.220582217051572e-15，positive_types=88，largest_multiplicity_digits=60。本文件没有88项质量、方程或新游戏完整输入，不能从小浮点误差推出原策略的有理全IC，不能把88类型当本页114类型种子，也不能将其“60位重数”改称60bit。

[原运行及种子身份审查](../审查/四复制与末回复研究的原运行及种子身份--审查.md)曾记录另一新game根7终局和浮点控制器约1.55等历史作者报告；本页没有对应输入，仍保作者报告等级，不用当前174终局回放替它认证。该短摘要作为恢复历史资源保留，缺口是新实例、精确质量及完整策略IC的绑定证据。

## 用途与关系

原件、比较依赖、重放stdout、完整新报告及除时间外逐字段比较见[证据包](../../tools/evidence/full18-exact-set-valued-bi-boss6/README.md)与[源清单](../../tools/evidence/full18-exact-set-valued-bi-boss6/source-manifest.json)。本对象补足旧审查当时“未读程序/种子、未跑”的本固定114类型实例证据，不倒改旧阅读时点。

[整终局势与真倒二菜单联合停界](../障碍/整终局势与真倒二菜单联合停界--障碍.md)指出同源必要点有真实倒二严格盈利偏离；这里计算整个种子游戏的合法均衡终局，是不同量词的有限检查。二者都不提供六人目标反例。需要复用集合值方法时先保留上述任意历史续局的充要递推，再给定新游戏重新核整数界，不能只替换报告中的比例。
