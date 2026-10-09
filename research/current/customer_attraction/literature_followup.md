# 顺序半覆盖目标：追加的一手文献量词核查

核查日期：2026-10-09。对象始终是 [CAG-MODEL](model.md) 的共同有限目录、
单位客户和单位提供者，且量化全部完整历史依赖纯 SPE。本文补充
[已有审查](literature.md)，不登记一般半覆盖定理。

## 1. 原论文的当前版本与两人证明范围

**Paper Fact。** [Deng 等的 arXiv 记录](https://arxiv.org/abs/2307.07174)
在此次核查时列出 v1（2023-07-14）和 v2（2024-10-10）。
[v2 §6](https://arxiv.org/html/2307.07174v2#S6) 仍将超过两名提供者时的
sPoA 上界 2 写为猜想。

**Paper Fact。** v2 Theorem 5.2 的两人假设用 “i.e.” 列出玩家数为二及
两玩家单位权；证明取 $T\in\mathcal S_1$、$S\in\mathcal S_2$，定义真实回复
$Q=\sigma_2(T)\in\mathcal S_2$。式 (18)--(20) 的三个合法比较分别是：
观察 $T$ 后次人选择 $Q$ 优于 $S$；首人实际收益优于偏离 $T$ 后的收益；
观察实际首主题后次人实际行动优于 $Q$。

**Interpretation。** 这段两人证明没有使用 $\mathcal S_1=\mathcal S_2$。
因此 “symmetric agents” 在该定理句中的表述不能被机械地当作证明所必需的
共同目录假设。这也说明 [固定背景两人税界](two_remaining_tax.md) 的三比较机制
并不是更多人数的目录对称性论证；任意人数仍需新的续局控制。

**检索事实，非不存在证明。** 本次以论文全名、customer attraction、
sequential symmetric market sharing、valid utility、Shapley coverage 等组合，
并针对最近两年定向检索，没有找到已解决本页精确任意人数量词的后续论文。
arXiv 当前版本仍提出猜想，只说明该版本未解决，不能据此证明全世界没有新结果。

## 2. 不能导入的顺序 set packing 定理

**Paper Fact。** de Jong、Uetz，
[*The quality of equilibria for set packing and throughput scheduling games*](https://link.springer.com/article/10.1007/s00182-019-00693-1)，
International Journal of Game Theory，2019 在线发表、2020 年第 49 卷，
§3 要求各玩家目录 downward-closed，
并规定与任何其他已选集合交叠时个人收益为 $-\infty$，否则为自己集合的总价值。
Theorem 6 对任意行动顺序和每个 $\alpha$-近似 SPE 给出对应行动终局为
$\alpha$-近似 PNE；Theorem 5 的顺序 PoA 为 $\alpha+1$。
Theorem 7 / Corollary 1 在共同目录、精确 SPE 时给出 $e/(e-1)$。

**Interpretation。** 这里后继玩家的合法选择必须避免先人已占资源，故先人的收益
不会被理性后继者稀释；Theorem 6 的证明明确用这个性质。
CAG 允许共同覆盖，后继者会降低先人的客户份额，且任意主题目录不必向下闭合。
把主题剩余部分当成可选行动会改变目录，把交叠收益改成均分会改变游戏。
该论文的 §1 related work 也明确区分 set packing 和 uniform-sharing covering。
因此搜索结果中的“顺序 PoA 为 2”及“对称顺序 PoA 为 1.58”不是本目标的文献解答。

## 3. 新近 submodular best-response 结果的时间模型

**Paper Fact。** Konda、Chandan、Grimsman、Marden，
[*Best Response Sequences and Tradeoffs in Submodular Resource Allocation Games*](https://arxiv.org/html/2406.17791v1)，
arXiv:2406.17791，2024，§II 式 (5) 和 Algorithm 1 的 $k$-round walk
从所有玩家空行动开始，每步一名玩家相对固定的其他玩家当前行动做静态最优反应；
后续轮次可再次行动。

**Interpretation。** $k=1$ 也没有把后继玩家的条件策略放入当前行动者的目标。
它控制的是 myopic 更新轨迹，不是一次依次行动、预见真实离轨续局的纯 SPE。
因此其有限轮福利结果不能通过令 $k=1$ 导入本目标。

## 核查结论

以上新检查没有提供可直接使用的任意人数 $\operatorname{OPT}_m\le2W$ 定理。
也没有产生目标反例。本页不修改 [Q-CAG-HALF](../../questions/customer_attraction_half_coverage.md)
的开放状态；首步机会成本桥的数学反例另见 [CA-TAX-BRIDGE-NO](tax_bridge_counterexample.md)，不把文献未检得升级成新颖性结论。
