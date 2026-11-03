---
id: "customer-attraction/pb-background-full-history-review-scope"
kind: "review"
type_tag: "审查"
title: "PB背景反例的全历史审查、读序与版本范围"
status: "historical-reviews-integrated-and-mathematically-rechecked"
summary: "区分dynamic先陈述盲重构及后读稿、credible与原root非盲重构，保留水位的另一自足证明、两个真实尾人数方向、singleton分层及原待审标量回执的时间差。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/dynamic/review_pair_counterexample_blind.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/dynamic/review_pair_counterexample.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/credible/review_pair_counterexample.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/parent/review_pair_counterexample.md"
---

# PB背景反例的全历史审查、读序与版本范围

本对象保存[任意合法背景PB反例](../反例/任意合法背景的前两人额外槽安全值--反例.md)的四份原内部审查及其数学比较。本轮Boss3已读主稿和全部审查后重核，不称新的盲审；原四份记录逐字节保存在[证据目录](../../tools/evidence/pb-background/README.md)，各源ID、冻结版本和hash在[PROVENANCE](../../tools/evidence/pb-background/PROVENANCE.json)。

## 四份记录的实际读序和承诺

| 原记录 | 实际输入与读序 | 它自己确认的范围 |
|---|---|---|
| dynamic盲重构，b3762e387d95173ec9ad | 先读模型、参数、目录、策略和G/P/F陈述；尚未读作者§4–5 | 独立水位与三类激励重构，给定参数未见致命异议；当时尚待对照原证明 |
| dynamic对稿，9d4d49f22012ae5adfd3 | 冻结前一稿后才读取作者§4–5 | 全regular节点与singleton补齐通过；静态Jensen仍属于其他分工，不能由此单稿宣布PB整体已审 |
| credible，fe1e38e756d02adcde11 | 工具读取构造时同页返回§4–5，因此明确非盲 | 独立重建模式、水位、全部激励，并逐层核包括singleton竞争者的静态下界 |
| 原root，4612ee2f8f57c1cb3345 | 先读完整主稿，再重建证明 | 核真实续局和子树补齐，另核Jensen、计数与标量；合并其他分工而未宣称外审 |

四者都没有枚举48,495,120客户的巨大完整博弈树。其结论建立在解析全历史证明上，原自称独立Fraction数值重算是各自的历史记录；本轮真正运行的程序和输出另在[计算对象](../计算/PB背景反例的标量证据与实际前缀算术--计算.md)登记。

## 盲重构独有的最大水位表述

这给主正文的“补到c−1”证明一个可独立使用的等价形式。固定单段任意旧负载n_a≥0，当前及以后共N次最低负载增加。置

\[
 C(h)=\sum_a(h-n_a)_+,\quad
 h=\max\{z\in\mathbb Z:C(z)\le N\},\quad
 R=N-C(h).
\]

块数Q有限非零，C(z)随z最终趋于无穷，最大整数h存在。原当前选择的是最低块，它最终负载L属于{h,h+1}；若L=h+1则R≥1。原负载可以任意不平衡，不需旧历史按规定策略走。

当前若改选非空R块子集B，后继仍Greedy并对新偏离者所选块给第一平局优先。令a为B内原负载小于h的块数。若a=0，这些块当前加一后已至少h+1；若a≥1，补全段到h尚需C(h)−a≤N−1次，未来足够，所以每个所选块最终至少h≥L−1。

若|B|=1且原块低于h，当前先填一份缺额，未来补到h需C(h)−1次，余下R次。原L=h+1时R≥1，唯一新偏离者块优先再加一次，达到h+1；原L=h时无需这一步。原块本来至少h时当前自身已达到h+1。因此单块偏离最终负载至少L。

第二层“最近使用者”平局不用于这个单块加强；这里真正承重的是新偏离者**所选**块的第一优先。主稿“包含最近偏离者的块”应按此具体动作含义理解，不能理解为块本身包含某个玩家对象。后读稿审查确认两种水位证明等价。

## 模式切换和两条不同的尾人数界

审查逐项穷尽Greedy吸收情形：当前索引已超过3且此前无偏离；唯一早期偏离的全部处罚阈值已满足且以后不降；或者本来已有多个偏离/唯一偏离太晚。当前再regular偏离不会让Punish重新出现，所以水位比较确实针对两条真实Greedy续局。

Punish节点则只能由早期唯一偏离及连续规定处罚到达。不存在先进入Greedy再返回Punish的同一历史。总处罚≤180、当前索引≤183、每段已用块≤186，分别支撑动作可行性与人数界。

- **遵循Punish一侧**：阶段末零块≥1877，后续Greedy≤2474<2·1877。新Greedy一块的最近使用者晚于旧处罚者；最近偏离者旧低块的优先处理也不会消耗旧处罚者自己的零块。因此其非热点块保持负载1，热点最终为t=10。
- **当前Punish玩家偏离一侧**：它成为第二偏离者，后继全Greedy，至少2292人。主稿用Q+k=2066作为把其所选块全部补到2的充分步数；dynamic独立重构指出其实Q步已经足够，因为当前新占块减少了待填零块数。两种上界都被2292严格超过，较松原界仍正确。

不能把遵循侧的Greedy上界用于偏离侧的证明，或反过来以偏离侧下界描述原实际尾部。两边dummy分别用g(r)下界和g(1)上界，正是P比较所需方向。该局部玩家IC也不是多位处罚者的联合最优性。

## G如何同时提供三个模式所需的辅助比较

G为g(r)>2f(1)−f(2)。由于f严格递减而g(1)≥g(r)，它已经蕴含

\[
 g(1)\ge g(r)>2f(1)-f(2)>f(1)>f(2).
\]

因此Punish偏离上界在每段选一个R块时最大，以及Fill/Copy偏离上界在保留最多D块时最大，都不是漏加的数值假设。

对ℓ=2，real增益受2f(z)−f(z+1)的递减控制；ℓ=3时再用

\[
 3f(z)-f(z+1)\le2[2f(z)-f(z+1)]
\]

（差为f(z)−f(z+1)≥0），每多一块real的收益上界由失去一个dummy的g(r)支付。L=1的端点另用所选块至少负载1。各段可加覆盖任意Cartesian多段偏离，不能只检查一个段便省略这个求和理由。

## singleton、静态槽数及合法背景的界限

singleton偏离收益≤1/(M+1)，regular在任何后继下收益≥dq/(M+r+1)。这个统一严格比较允许在首次singleton后的每个子树任选纯SPE，不要求以后整块f、g仍适用。各首次singleton子树不相交，可按真实有序前缀逐个拼合。

静态PB值的对手有r个竞争主题并不观察查询。credible和原root均按q个客户层分开用Jensen：regular每层每槽最多覆盖k块，singleton只覆盖一个客户，也满足界。不能把singleton错误提升成整块负载，亦不能把不观察查询的对手改成查询后自适应回复。dynamic分工只重算所给s公式的数值，没有独立证明这部分；本轮保留该区别。

合法singleton前缀实现b，仅保证其是一条合法历史。固定子SPE后再向祖先逆向归纳，可以嵌进一份原全游戏完整SPE；祖先选择最佳动作可能使这一历史离轨。四审查都没有证明它在根路径发生。后来[最后D-singleton障碍](../障碍/PB大背景的最后单例偏离--障碍.md)恰说明同原参数、精确背景及regular尾的直接在轨实现不可能，与这些审查不冲突。

## 原报告的待审文字与后续证明状态

原标量程序和JSON仍写“analytical full-history proof awaiting independent review”。这是该程序冻结时点的状态字符串；它只认证G/P/F等标量，不随后来文稿更新。本轮保全原字节，不把字符串改写成完成，也不因这个旧字符串忽略随后确实存在的dynamic、credible与原root审查。

主稿最终所称“完整解析分离、已完成分工内部审查”需要上述范围共同支撑。它不意味着外部同行评审、新颖性认证或一般half已解。原root提及的独立参数脚本、dynamic独立标量脚本和它们的输出保留为原件内导航；本批未把这些独立程序列为新运行或已清洗来源。当前可复现依赖是已经原样保存并重放的作者标量程序，它只承担自己的有限算术职责。

第三阶段关系应分开：两种水位证明等价；三模式真实IC与singleton补齐支持完整子SPE；静态层Jensen给同一查询的r槽保证；正标量差闭合PB-extra反例；合法历史到实际根前缀不是这条链的一环，而是另有真实障碍的迁移问题。
