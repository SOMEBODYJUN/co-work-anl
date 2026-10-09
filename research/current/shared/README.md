# 共享选址集合的黄金比构造

研究问题：两个设施可以选择同一有限位置集合时，能否以可计算的精确顾客续局选择，将设施单边改善控制在黄金比 φ 以内？

完整的[集成主稿](../../../history/source/manuscripts/shared_phi/main.tex)已给出普遍定理、局部工具、全局关闭和证书算法，且经过多轮内部审读；尚未经过外部同行评审。本组 Markdown 按数学对象重新写成，并将最初省略的 G1–G3、L1–L2 分支展开成独立证明页。内部逐式交叉核对记录不等于外部同行评审。

| 文件 | 应读内容 |
|---|---|
| [four_site_no_fptas.md](four_site_no_fptas.md) | 两设施共同四地点的全局 PARTITION 间隙；正整数权、所有实概率精确 NE/完整续局的下界与位复杂度；无 FPTAS、PTAS 仍开放。审计不是原作者包复现。 |
| [model.md](model.md) | 共享目录模型、精确 NE 方程、续局量词、菜单充分条件 |
| [theorems.md](theorems.md) | 存在性、位多项式构造、局部 C、单实例证书的分离陈述 |
| [proof.md](proof.md) | 受保护修复、坏环、严格支配、双锚覆盖及分支接口 |
| [heavy_pairs.md](heavy_pairs.md) | G1：大顾客对容量界、同对 T 矛盾、三角闭集严格下降 |
| [star_anchors.md](star_anchors.md) | G2/G3：首边、星心、中心引理、锚点选择与两支终局 |
| [local_chord_full.md](local_chord_full.md) | L1/L2：局部强弦的分支、端点交换与多项式迭代 |
| [sharp_phi_lower.md](sharp_phi_lower.md) | SC-PHI-SHARP：共同目录的六地点下界、全布局偏离与统一有理扰动 |
| [algorithm.md](algorithm.md) | 固定 P/E/T/C 菜单、搜索伪代码、验证语义、复杂度和实现边界 |
| [instance_complexity_barriers.md](instance_complexity_barriers.md) | 同址正规形与异址交叠参数精确求解；两地点、等 reach 及稀疏两 reach 精确 SPE |
| [small_sparse_catalogs.md](small_sparse_catalogs.md) | 不同地点单交叠时，最多 1/2/3/4/5 地点的尖锐阈值 $1,1,\sqrt2,\sqrt[3]4,\phi$ |
| [three_site_exact_hardness.md](three_site_exact_hardness.md) | 三地点共同目录的全布局弱 NP 完全性：每个固定有理 $1\le a<(1+\sqrt3)/2$，以及再往上该守卫的严格权重预算障碍 |
| [five_site_exact_hardness.md](five_site_exact_hardness.md) | 每个固定有理 $1<a<\phi$ 的恰五地点全局弱 NP 完全性；三态源、桥宏原子双向引理、全部 25 带标签布局与位复杂度。独立构造器 `facility_spe/shared/five_site_hardness.py`、审查 `tests/audits/five_site_hardness*.py`、冻结实例和完整续局证书与数学证明分开。 |
| [atomic_granularity.md](atomic_granularity.md) | 两设施可拆分对照与原子局部误差给出实例敏感的完整近似续局；宏原子是固定 $a>1$ NO 输入的必要条件 |

统一研究入口使用 [公共模型](../model.md) 和 [主张登记](../claims.md)。本分支固定目录相同、允许同址、强制顾客参与、顾客独立混合等假设；异质目录下界或任意凸成本扩展必须另外立项。

各编号分支已在对应页面按前提、实际不等式、固定菜单成员及边界分支逐项重写；[proof.md](proof.md)保留证明接口与阅读顺序。新的数学主攻方向见[下一阶段路线](../../ROADMAP.md)。单实例证书的有效性可独立核验，但不能代替普遍证明。

[共同目录实例最优求解器](../../../facility_spe/exact/shared_offdiag.py)只枚举异址客户支持，给出完整精确续局证书；[独立比较测试](../../../tests/test_shared_offdiag.py)覆盖大同址交叠、零收益和平局。新增证明与计算经过内部交叉审查，外部评审及文献优先权仍待核定。
