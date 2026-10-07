# 08 参考资料与继续阅读
讲义已经展开本项目的模型和主要证明。参考资料用于补一项明确的背景知识，或进入已经指明的研究分支。它们不替代正文中的关键推导，也不为本仓库的新结果自动提供审查背书。

## 1. 通用背景与本模型的关系

Easley--Kleinberg 的 [Networks, Crowds, and Markets](https://www.cs.cornell.edu/home/kleinber/networks-book/)第 6 章从博弈、最优反应和 Nash 均衡讲到混合策略；6.10 涉及动态博弈。它适合没有博弈论基础的读者。把这些概念用于本项目时，客户成本必须重新代入 $w_{i} + \sum_{j \neq i}w_{j}p_{jf}$，不能直接套书里其他游戏的收益表。

[MIT 6.042J Mathematics for Computer Science](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/)提供集合、逻辑量词、证明、增长阶和离散概率背景。读 00 时若卡在具体符号或证明方式，补对应主题即可；不需要先通读整课。

Gairing、Lücking、Mavronicolas、Monien 的 [Computing Nash Equilibria for Scheduling on Restricted Parallel Links](https://cgi.csc.liv.ac.uk/~gairing/publications/2004-stoc.pdf)，STOC 2004，是第 05 章导入的调度工具。论文 §4 的 Corollary 4.3 说明一次不可拆分阻塞流调用的极大负载不增、极小负载不减；Theorem 4.7 给出受限相同链的均衡算法。先看论文怎样定义允许集和链负载，再看本讲义怎样映射客户与带标签设施。混合站点重数的站内均匀客户模型有不同的不等式，第 06 章将直接给出公式反例；“链速度”一词不能使两个模型自动相同。

以上入口及对应章节已在本轮核对。背景资料用于补概念；外部调度定理用于一个明示条件下的步骤。两者均不能替代本项目主证明，也不表示本轮重做了整篇外部算法。

## 2. 双设施证明的继续点

共同目录黄金比例正文见 02。规范来源顺序是 [模型](../research/current/shared/model.md)、[完整证明](../research/current/shared/proof.md)、[局部弦](../research/current/shared/local_chord_full.md)、[重对](../research/current/shared/heavy_pairs.md)、[星心双锚](../research/current/shared/star_anchors.md)，最后看 [算法](../research/current/shared/algorithm.md)。讲义中的菜单与强弦在这些页有对应的精确编号。

φ 尖锐性的所有布局下界另读 [sharp_phi_lower](appendices/A01_phi_lower.md)。理解上界构造并不表示已完成下界：下界必须排除阈值以下的所有布局和所有允许续局。

一般异构 2 继续读 [核心提升](appendices/A07_hc_core.md)、[四种子](appendices/A08_hc_seeds.md)、[全目录环](appendices/A09_hc_cycle.md)、[匹配下界](appendices/A10_hc_lower.md)。账本仍保留内部候选状态；不得因为程序给出一个证书就改变这个状态。

任意长单交叠异构目录的 ρ 结果读 [全长直接证明](../research/current/heterogeneous/sparse_unbounded_rho.md)，下界和模型读 [restricted_rho](appendices/A06_rho.md)。关键是高低入口上的同一客户身份，以及三次式所对应的收益比；它不依赖一个尚未证明的短环缩约。

## 3. 任意设施数与计算前沿

因子 2 存在性完整来源是 [uniform_two](../research/current/multi_facility/uniform_two.md) 和 [reverse_review](../research/current/multi_facility/reverse_review.md)。第 03 讲已经给出连贯教学推导，原稿用于逐编号核对四预算、源站消失、装箱及宏原子边界。

算法工具来自 [polytime_frontier](../research/current/multi_facility/polytime_frontier.md)、[adaptive_reset_floor](../research/current/multi_facility/adaptive_reset_floor.md) 和 [frozen_overload_completion](../research/current/multi_facility/frozen_overload_completion.md)。先在 05 读懂基本接口，再根据 09 选择一条路线。前沿文件中的众多特殊类不是一般输入算法的拼接。

实例困难性继续读 [结构与算法边界](appendices/A02_barriers.md)、[三地点归约](appendices/A04_hard_three.md) 和 [五地点归约](appendices/A05_hard_five.md)。第 04 讲讲清判定问题与 YES/NO 方向；原稿给所有布局守卫的长证明，不能仅凭一个难布局推出整个实例困难。

## 4. 按研究方向选择的技术

| 方向 | 继续阅读 | 必须保留的范围 |
| --- | --- | --- |
| 小交叠与更小因子 | [A03](appendices/A03_sparse.md)、[原子粒度](../research/current/shared/atomic_granularity.md) | 目录大小、异址交叠和粒度条件；普遍界与实例最优分开 |
| 原子与可拆分负载 | [固定布局误差](../research/current/local_and_exact/atomic_wardrop_gap.md) | 固定布局和多选项客户最大原子权；该比较本身不给选址算法 |
| 类型压缩 | [参数算法](../research/current/multi_facility/type_compression.md) | 固定参数、输入位长、XP 与 FPT 分开 |
| 树结构上的盒均衡 | [关联图方法](../research/current/multi_facility/bounded_incidence_box.md)、[权种方法](../research/current/multi_facility/local_weight_box_dp.md) | 树宽、度或权种条件；否定只针对规定的盒选择器 |
| 浅层交叠的存在性 | [高度二证明](../research/current/multi_facility/height_two_box.md) | 每名轻客户两个选项、开启方向的深度；存在不自动给势最小化的高效算法 |

没有选这些方向时，先知道其准确范围即可。完整现行状态、命题编号和依赖见 [claims](../research/current/claims.md) 与 [review_status](../research/review_status.json)。历史手稿保留追溯用途，遇到符号或结论冲突时返回现行定义核对。
