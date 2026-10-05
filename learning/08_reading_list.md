# 08 必要资料与完整证明路线

资料分为基础补课、本项目讲义、核心完整证明三层。下面的顺序刻意避开历史日志。网页与论文信息核对日期为 2026-10-05；外部教材解释通用知识，不为仓库的新主张背书。

## 1. 只选两项基础资源

| 资料 | 具体读什么 | 什么时候需要 |
| --- | --- | --- |
| MIT OCW [6.042J Mathematics for Computer Science](https://www.ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/) | 定义与证明、逻辑量词、集合、归纳/不变量、图、增长阶、离散概率；从课程 Readings / Video Lectures 按主题选 | 第 00 讲练习不能独立完成时补对应主题，不通读整课 |
| Easley–Kleinberg [Networks, Crowds, and Markets](https://www.cs.cornell.edu/home/kleinber/networks-book/) | 第 6 章：6.1–6.4 博弈/最优反应/NE，6.7 混合策略；图陌生者补第 2 章 2.1–2.2；动态博弈概念可选 6.10 | 第 2–3 天前补概念。书中不同博弈实例不改变本项目的原子成本定义 |

最大流、整数费用流、NP 归约、树宽和整数规划无需全部先学。本课程先讲其具体合同，再在研究路线需要时补完整理论。两周学习不以读完一本教科书作为前提。

## 2. 主成果的完整证明，不只读摘要

| 成果 | 全员讲义 | 报告组完整阅读链 | 必须讲透的环节 |
| --- | --- | --- | --- |
| 共同目录双设施 φ 上界与构造 | [02](02_two_facility.md) | [模型](../research/current/shared/model.md) → [定理](../research/current/shared/theorems.md) → [完整证明](../research/current/shared/proof.md) 及其实际调用的 [局部弦](../research/current/shared/local_chord_full.md)、[星形锚](../research/current/shared/star_anchors.md)、[重对](../research/current/shared/heavy_pairs.md) → [算法](../research/current/shared/algorithm.md) | 菜单与精确局部极值的差别；C、G1–G3、L1–L2 的所有前提和分支；如何补全续局 |
| 同类 φ 尖锐性 | [02](02_two_facility.md) | [正有理下界与全布局证明](../research/current/shared/sharp_phi_lower.md) | 所有布局均被排除到阈值以下；连续参数的严格余量与有理化 |
| 一般异构双设施 2 | [02](02_two_facility.md) | [四种子构造](../research/current/heterogeneous/four_seed_algorithm.md) → [核心提升](../research/current/heterogeneous/core_lift_and_monotone.md) → [全目录环](../research/current/heterogeneous/full_catalog_cycle.md) → [下界](../research/current/heterogeneous/sharp_two_lower.md) | 共同目录中可用的弦未必合法；当前账本仍为内部候选，报告不能提升状态 |
| 任意长双侧单交叠目录尖锐 ρ | [02](02_two_facility.md) | [受限基础与下界](../research/current/heterogeneous/restricted_rho.md) → [高 reach 屏障](../research/current/heterogeneous/sparse_high_reach_barrier.md) → [全长直接证明](../research/current/heterogeneous/sparse_unbounded_rho.md) | 全目录回应、首个高到低入口、同一客户身份与三次式矛盾；不依赖尚未证明的短核心 |
| 固定 $1\le a<\phi$ 的共同目录实例判定 | [04](04_complexity.md) | [同址正规形与参数界](../research/current/shared/instance_complexity_barriers.md) → [三地点 a=1 及低区间](../research/current/shared/three_site_exact_hardness.md) → [五地点全部 $1<a<\phi$](../research/current/shared/five_site_exact_hardness.md) → [审查范围](../research/FIVE_SITE_AUDIT_2026-10-02.md) | YES/NO、宏原子强制、全布局守卫、固定倍率、弱 NP 与伪多项式的相容性 |
| 任意设施数共同目录因子 2 存在性 | [03](03_arbitrary_k.md) | [模型](../research/current/multi_facility/model.md) → [主证明](../research/current/multi_facility/uniform_two.md) → [逆审](../research/current/multi_facility/reverse_review.md) → [作用域审计](../research/K_FACILITY_AUDIT_2026-10-02.md) | 客户 NE、四类预算、源站消失、装箱、超重原子隔离、完整带标签规则；不声称高效或尖锐 |

两周报告优先按这些链走，历史 LaTeX 仅在现行页与原稿需要核对时查。现行页本身还留候选状态的部分，报告时说清证据等级。

## 3. 与当前算法目标直接相关的资料

必读主入口是 [计算前沿](../research/current/multi_facility/polytime_frontier.md)。文件很长，先依 [05](05_tools.md) 的索引读取贪心预算、SINGLETON-RESET、BOX-TO-2 与 RESET-PACK 的命题和证明；再看 [自适应重置](../research/current/multi_facility/adaptive_reset_floor.md) 和 [冻结安全超载](../research/current/multi_facility/frozen_overload_completion.md) 的完整合同。只学习其中确实要使用的结构子类。

合法导入的公开算法来源是 Gairing, Lücking, Mavronicolas, Monien, **Computing Nash Equilibria for Scheduling on Restricted Parallel Links**, STOC 2004，[作者提供的论文](https://cgi.csc.liv.ac.uk/~gairing/publications/2004-stoc.pdf)。重点读相同链部分 §4，尤其 Corollary 4.3 与 Theorem 4.7。单次 blocking-flow 的极值保持和整个 Nashification 的保持需分别核对；正有理缩放后仍须控制位长。不要把“论文里有调度算法”当成混合站点重数模型已被直接覆盖。

[混合重数接口边界](../research/current/multi_facility/restricted_related_link_boundary.md) 给出错误速度替换的准确反例。它排除的是这个文献导入方式，不证明一般算法困难。

## 4. 重要但不挤占核心证明的成果

下列成果卡是全员应知道的准确陈述，不展开其长证明。它们都是内部结果，尚无外部评审或完整新颖性核查；感兴趣的报告人再读全文。

| 成果卡 | 准确陈述与限制 |
| --- | --- |
| [单交叠小目录阶梯](../research/current/shared/small_sparse_catalogs.md) | 双设施共同目录、每个**不同地点**对至多一个公共客户、至多 N 个地点。尖锐普遍因子为 $N=1,2:1; N=3:\sqrt2; N=4:\sqrt[3]4; N\ge5:\phi$。这是结构类的普遍最坏倍率，不是实例判定复杂度。 |
| [原子粒度保证](../research/current/shared/atomic_granularity.md) | 双设施共同目录，$R=\max_t w(C_t)>0$，θ 是所有**异址公共客户**的最大原子权（不存在取 0）。若 $\theta<R$，可构造完整保证 $(R+\theta)/(R-\theta)$，并与 φ 保证取较小值。θ=0 得精确 SPE；保证值不声称实例最优，同址可有大原子。 |
| [原子—Wardrop 局部误差](../research/current/local_and_exact/atomic_wardrop_gap.md) | 固定任意 $K\ge2$ 布局，θ 是可达至少两家**设施**的客户最大权。任意精确原子 NE 与任意同布局可拆分 Wardrop 负载的每个坐标差至多 $(K-1)\theta/2$，常数可取等号。目录可异构；只比较固定布局的客户负载，不给设施阶段因子 2 构造。 |

[类型压缩](../research/current/multi_facility/type_compression.md)、[局部权种 DP](../research/current/multi_facility/local_weight_box_dp.md) 则是有明确固定参数限制的可算范围。具体参数和算法只在选定该研究路线时学习；不能把若干特殊类并列成一般输入算法。

**暂不布置：**全部树形变体、每个失败优先规则、整个历史仓库、所有证书、论文选刊讨论。第 06 讲已经提炼必须知道的机制，需要复用特定技术时再深入。
