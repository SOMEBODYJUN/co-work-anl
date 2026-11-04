---
id: customer-attraction/r3b6b-count-markov-outcome-reduction-probe
kind: computation
type_tag: 计算
title: R-3b6b 计数 Markov 终局集合有限降维探针
status: exact-saved-input-sets-rechecked
truth_status: count-reduction-not-universal; no-half-conclusion
review_level: exact-source-input-and-function-recheck; count-policy-versus-set-cache-separated
scope: abstract fresh-subset marginal-potential games and finite CAG count-dependent policy probes
summary: Exact finite outputs show that a count-dependent Markov selector can lose full ordered-history outcome certificates. The probes concern reduction validity only; they do not restrict the original Q-CAG-HALF model or produce a half counterexample.
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/structural_reduction/fresh_markov_gap.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/structural_reduction/fresh_markov_gap_reduced.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/structural_reduction/fresh_markov_probe.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/structural_reduction/markov_layers.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/structural_reduction/markov_probe.py
---
# 计数缓存与计数统一策略的分界

## 缓存什么，不等于统一选择什么

在[完整历史共同目录模型](../定义/共同目录完整历史模型--定义.md)中，终局收益只依赖各主题计数，所以从同一计数开始的**可实现终局全集**可以共享缓存。然而完整策略仍定义在有序历史上；两条同计数历史在不同分支可以选择不同可信续局。强迫它们共享一份下一动作/后继映射，是额外的计数策略约束。

在逆向归纳中，每个候选实际孩子先选一个可信终局；其余有序孩子分别选让当前玩家收益不超过该实际收益的可信终局。这是逐孩子的存在选择，不要求不同父历史对子计数使用相同选择。不能把集合值缓存的正确性换成统一策略净化的正确性。

## 抽象三步 fresh-subset 的精确分离

这里的动作是五个标签0,…,4，三名玩家每步只能选未用标签。终局是三元素**集合**，不是长度三的主题计数向量。固定集合势F，终局T中选择a的收益为

\[
 v_a(T)=F(T)-F(T\setminus\{a\}).
\]

令R(S)为从已选集合S出发所有完整有序历史策略能实现的终局集合。末层R(S)={S}；此前令

\[
 L(S)=\max_{a\notin S}\min_{T\in R(S\cup\{a\})}v_a(T),\qquad
 R(S)=\bigcup_{a\notin S}\{T\in R(S\cup\{a\}):v_a(T)\ge L(S)\}.
\]

必要性来自真实离轨收益不小于该孩子的最小可信收益；充分性则为每个离轨孩子独立选一个达到该下界的可信终局再拼接完整子树。计数统一选择额外要求每个两元素集合ab只有同一末回复d_ab，在比较所有单元素父节点前先固定整份d映射。

冻结`fresh_markov_gap_reduced.json`给出一个小势：空集和单元素取0，按字典序的十个二元素值为

\[
(1,0,0,2,0,2,3,1,0,0),
\]

十个三元素值为

\[
(0,0,5,4,0,0,5,0,5,0).
\]

这完整确定本三步游戏所需的26个势值。保存的原势与此缩小势各自得到相同两类根终局：

\[
\begin{aligned}
 R(\varnothing)&=\{014,023,123,134\},\\
 R_{\rm count}(\varnothing)&=\{014,123,134\},\\
 R(\varnothing)\setminus R_{\rm count}(\varnothing)&=\{023\}.
\end{aligned}
\]

其中014表示集合{0,1,4}。原页“计数子类保留前三个”的句子错误：前三个包含023，与所称差集矛盾。现按两份冻结JSON并分别调用原`outcomes`/`markov3`函数对保存的全部势值精确回算，改为上面明确的集合。原脚本main的随机生成规则不应当作这两份保存点的生成轨迹；本次核的是指定输入，未重跑随机搜索。

这只是抽象禁止重复动作的边际势游戏。尚未给它一个非负整数客户实现，不能由此称单位客户CAG反例。

## 客户实例与两个有限程序的准确范围

更强的[完整历史与计数统一策略严格分离](../反例/完整历史与计数统一策略的严格分离--反例.md)已有合法CAG客户构造：三人、五个互异覆盖主题、24831位单位客户。它先以统一正重数背景严格排除全部重复行动，再穷尽648种末层计数映射及130776种第二层选择；完整根终局7个，计数根终局6个，缺失023，最差福利分别22428与22429。其完整IC表、客户重数和最优覆盖22431均保留在该正式正文。不能只展示某一棵非计数策略，就宣称其根终局没有其它计数实现。

本页的另外两个程序须分开：

- `markov_probe.py`固定三主题、三玩家，遍历7种非空兴趣类型各取0/1/2的全部3^7个重数输入，比较完整终局与计数统一末层动作，遇到差异才输出；末层策略积超过cap时不作全枚举结论。
- `markov_layers.py`的保存main固定三主题、**四玩家**，最多3000个随机输入，按层固定一整份共同计数映射，cap=100000。返回`None`表示截断，不能记作两类终局相等，更不是上面三人穷举的另一实现。

探针没有普遍化有限阴性。要升级某个新发现，仍须合法单位客户、完整有序IC以及相应福利/最优覆盖；现有严格分离也只是否定计数净化，并不否定半覆盖。

## 来源与复用

五份原件的路径及SHA来自`cleanup/inventory.jsonl`：原势b948c6220684827efc2ea9f54c396bf210d819fbb48fdedd012803e9e4b955d1、缩小势a03fddff18e8070d3e203319df5f0d4da665c60146927e628bfcb26ec2d71f3f，均与实际Git blob核对。两份保存输入的集合差均已精确回算；客户反例的既有完整证明直接复用，不重复其穷举。未把抽象势、有限阴性、计数缓存及完整有序策略混为一物。
