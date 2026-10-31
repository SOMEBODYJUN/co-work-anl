---
id: customer-attraction/last-payoff-not-uniformly-shared-disjoint-family
kind: counterexample
type_tag: 反例
title: 末位收益不可按人数均摊的全历史不交族
status: complete-analytic-full-history-SPE-family
truth_status: refutes-named-auxiliary-cap-only; actual-coverage-is-optimal
review_level: independently-reconstructed-and-definition-level-exact-finite-check
scope: 每个m≥2的有限单位客户、共同m主题目录；构造一份全部有序历史纯SPE；m≥4违反辅助cap
summary: 两客户大主题加m−1个不交单例，前末位取未用单例、末位按过去大主题计数选真最佳回复，实际收益为1,…,1,2、W=OPT=m+1，故辅助式(m−1)u_m≤W在m≥4失败。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/credible_attack/README.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/credible_attack/README.md
---

原README记录末位收益猜想 `(m−1)u_m≤W` 已被完整SPE不交负载均衡例否定，但未在该1395B源内给旧见证。本页给本轮独立重构的一个足够自足族，不声称恢复未交付旧见证的相同字节，也不主张新颖性。它是原模型中的真实SPE，反驳的是上述辅助不等式；**不是**当前六人half反例。

## 共同目录与全部有序历史策略

固定m≥2。有两名单位客户构成A；另m−1名不同客户各构成单例B₁,…,Bₘ₋₁，所有主题彼此不交。目录恰为这m个主题，所有玩家均可选全部主题。零客户/空主题并非该实例的必需成分；同一主题重复行动及任意离轨有序历史全保留。

对每个长度小于m的历史h定义σ：

- 当前还不是末位：选择标签最小、在h中尚未被选择的B主题。
- 当前是末位且过去A计数至多1：选A。
- 当前是末位且过去A计数至少2：选标签最小、尚未使用的B主题。

每个前末位历史长度至多m−2，故至少有一个未用B。末位在A已有至少2次时，历史至多用了m−3个B标签，也有未用B。策略在全部m进制有序历史上定义，包括不由自身规定动作到达的重复历史。

## 完整SPE证明

末位：若A过去0次，选A收益2，任何B至多1；若A过去1次，选A收益1，与任何未用B平局、优于已用B；若A过去至少2次，选A收益至多2/3，未用B收益1。因此规定末位动作总为真实最佳回复。

固定任一前末位历史。规定未用B以后不再被任何前末位规定玩家选中；末位或选A，或另一个未用B。因此当前规定收益恰1。改变当前行动时，全部后来动作仍依上述σ重新响应：

- 改选另一未用B也得1；改选过去已有r≥1次的B则得至多1/(r+1)≤1/2。
- 改选A：若过去A为0次，末位再选A，当前最终得2/2=1；若过去A为1次，末位选未用B，当前仍得2/2=1；若过去A至少2次，末位选未用B，当前至多2/3。

当前无严格有利偏离。这个论证对每个离轨历史逐节点成立；每位只动一次，因而σ是一份完整有序历史纯SPE。平局按已规定规则选，未加泛型扰动或删掉平局。

实际路径为(B₁,…,Bₘ₋₁,A)，每位前末位收益1，末位收益2，所有m+1客户均被覆盖。目录全部m主题恰能覆盖同一宇宙，故
\[
W=OPT_m=m+1,\qquad (m-1)u_m-W=2(m-1)-(m+1)=m-3.
\]
m=2时该差−1、m=3等号，m≥4严格反驳cap。当前六人实例W=OPT₆=7、u₆=2，cap左侧10>7，而half当然成立。不能把此辅助失败改称福利反例。

## 新定义级核验与接续

本轮另写标准库Fraction检查，独立展开m=2,…,6全部有序历史，沿规定/真实强制行动完成同一σ，逐节点比较收益。新入口仅执行一次（非历史原程序复跑）：合计10213决定节点、60276条含自身激励比较，最小松弛0，五个cap差依次−1,0,1,2,3；Python3.12.14/assert、exit0/stderr0。代码、原stdout、JSON和真实元数据在[证据入口](../../tools/evidence/root-following-source-batch/README.md)。普遍m结论由上面解析证明承担，有限五例不代替它。

这落实原README“不得以末位收益按人数均摊”的边界；没有否定所有末位安全值或税诊断。例如[末位收益税诊断](../引理/末位收益税诊断--引理.md)按具体客户负载收费，不能用本页被否的cap替换其合同。对任意背景子游戏向原根游戏迁移，仍须[实际前缀关联预算](../审查/实际前缀的关联预算与PB背景可达性复核--审查.md)及全已覆盖福利账，不得删掉过去客户支持。
