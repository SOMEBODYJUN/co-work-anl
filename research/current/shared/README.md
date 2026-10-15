# 共同目录双设施：黄金比尖锐阈值与实例复杂度

研究对象是两个带标签设施共享同一非空有限位置目录、允许同址、正权原子客户、被覆盖客户强制参与、线性实现负载费用及精确独立客户 NE。结论量词是存在一整套按有标签布局选择的精确续局，使在途位置为近似 SPE；不能改成每套续局均稳定。位多项式陈述另外要求显式可达关系与二进制正有理权重。

本分支的主成果是共同目录的普遍 **φ 上界、位多项式构造与匹配下界**。另有实例最优倍率的精确算法、弱 NP 完全性、四地点无 FPTAS，以及局部补全和原子误差工具。完整主稿及当前 Markdown 已有多轮内部审读；外部同行评审、新颖性与优先权没有由本次整理补成事实。

## 主要结论与证据状态

| 成果 | 精确范围与当前状态 | 首读正文 |
| --- | --- | --- |
| 黄金比存在与构造 | SC-PHI-E / SC-PHI-A；完整主稿、当前全分支证明及内部多轮审读；单实例证书只证明该实例达到所报倍率 | [分离陈述](theorems.md)、[全局证明](proof.md)、[算法规范](algorithm.md) |
| 黄金比尖锐下界 | SC-PHI-SHARP；六地点全布局与有理扰动证明，和上界共同给尖锐阈值 | [六地点下界](sharp_phi_lower.md) |
| 实例最优复杂度 | 同址正规形只缩减共同目录的异址交叠；三/五地点固定倍率困难性和四地点无 FPTAS 各自保留输入范围 | [参数边界](instance_complexity_barriers.md)、[五地点归约](five_site_exact_hardness.md) |
| 近平衡补全 | 固定重支持的局部精确 NE 工具已有完整分支与位长；通用实例最优 EPTAS 仍是候选任务 | [局部补全](near_band_completion.md)、[EPTAS 义务](../../questions/shared_alpha_eptas.md) |

## 按数学成果族阅读

1. 证明普遍上界：先读 [公共模型](../model.md)、[共同目录定义](model.md) 与 [定理分离](theorems.md)，再由 [全局证明](proof.md)进入重客户对、星心双锚、局部强弦，最后读算法。
2. 判断尖锐性与实例难度：先读六地点下界，再按地点数和输入倍率进入单交叠阶梯、三/五地点归约或四地点无 FPTAS。后者不否定 PTAS。
3. 接续新算法：精确实例最优问题先读同址正规形；拟做舍入或 EPTAS 先读原子粒度和近平衡补全。未来路线在 [ROADMAP](../../ROADMAP.md)，不是方法白名单。

## 全部分支数学正文

| 中文资产名 | 文件 | 数学内容与读取时机 |
| --- | --- | --- |
| [共同选址目录的模型、精确续局与菜单充分条件](model.md) | `model.md` | 固定共同目录、同址、强制参与和独立混合约定；引用黄金比结果前先核对对象与续局量词。 |
| [共同目录黄金比存在性、构造与证书的分离陈述](theorems.md) | `theorems.md` | 分别登记普遍存在性、位多项式构造、局部强弦和单实例证书，防止混用数学保证。 |
| [共同目录黄金比上界的全局证明主链](proof.md) | `proof.md` | 组织受保护修复、坏回应环、严格支配与双锚覆盖；由各分支页补齐具体推导。 |
| [重客户对的容量约束与三角回应环排除](heavy_pairs.md) | `heavy_pairs.md` | 展开 G1 的重客户对容量界、同对回应边矛盾和三角闭集严格下降。 |
| [星心与双锚覆盖的黄金比闭环证明](star_anchors.md) | `star_anchors.md` | 展开 G2/G3 的首边、星心、中心引理、锚点选择及两支终局。 |
| [配额精确均衡与局部强弦的完整构造](local_chord_full.md) | `local_chord_full.md` | 完整重建 L1/L2 的可行性分支、端点交换、多项式迭代和位长，补足主证明局部接口。 |
| [黄金比有限菜单搜索与完整续局证书规范](algorithm.md) | `algorithm.md` | 说明固定 P/E/T/C 菜单、搜索伪代码、验证语义、复杂度及实现边界。 |
| [黄金比尖锐性的六地点下界与有理扰动](sharp_phi_lower.md) | `sharp_phi_lower.md` | 给共同目录全布局偏离下界和统一有理化；与已登记上界合成尖锐阈值。 |
| [实例最优倍率的同址正规形与异址交叠参数](instance_complexity_barriers.md) | `instance_complexity_barriers.md` | 用共同目录正规形缩减精确支持枚举；分开两地点、等 reach、稀疏两 reach 与多交叠障碍。 |
| [共同目录单交叠的小地点数尖锐门槛](small_sparse_catalogs.md) | `small_sparse_catalogs.md` | 在不同地点单交叠条件下，分别给至多一、二、三、四、五地点的尖锐门槛 1、1、√2、∛4、φ，不能扩至多共有客户。 |
| [三地点固定倍率判定的弱 NP 完全性与守卫边界](three_site_exact_hardness.md) | `three_site_exact_hardness.md` | 对每个固定有理 1≤a<(1+√3)/2 给全布局弱 NP 完全性，并记录向更高倍率延伸的严格权重预算障碍。 |
| [五地点全部亚黄金比固定倍率的弱 NP 完全性](five_site_exact_hardness.md) | `five_site_exact_hardness.md` | 对每个固定有理 1<a<φ，以三态源、桥宏原子和全部带标签布局给弱 NP 完全性及位界；构造器与审计分开。 |
| [四共同地点实例最优倍率的无 FPTAS 间隙](four_site_no_fptas.md) | `four_site_no_fptas.md` | 在正整数权与所有实概率精确续局下建立全局 PARTITION 间隙；PTAS 问题仍开放。 |
| [原子粒度、可拆分对照与实例敏感近似续局](atomic_granularity.md) | `atomic_granularity.md` | 由原子局部误差构造完整近似续局，并识别固定坏倍率输入所需的宏原子。 |
| [固定重客户支持的近平衡精确均衡补全](near_band_completion.md) | `near_band_completion.md` | 给四个完整局部分支与位长；可作实例最优 EPTAS 候选的工具，不等于通用 EPTAS。 |

## 程序、审查与来源

规范程序属于 [facility_spe](../../../facility_spe)，固定菜单搜索的输出与普遍证明、最优性证书分别理解。[共同目录异址求解器](../../../facility_spe/exact/shared_offdiag.py)只枚举异址支持并输出完整精确续局；[独立比较测试](../../../tests/test_shared_offdiag.py)覆盖大同址交叠、零收益和平局。

五地点归约另有[独立构造器](../../../facility_spe/shared/five_site_hardness.py)、[构造审计](../../../tests/audits/five_site_hardness.py)及[边界审计](../../../tests/audits/five_site_hardness_edges.py)；冻结实例和完整续局证书与普遍归约证明分开。四地点的审计不宣称复现了原作者上传包。

精确命题与五轴状态见[全仓账本](../claims.md)和[审查登记](../../review_status.json)。[集成主稿](../../../history/source/manuscripts/shared_phi/main.tex)是来源；当前重写已将 G1–G3、L1–L2 全部分支放入上表的独立页。历史时间措辞不能推翻现行身份，也不能以当前证明的存在虚构外部认证。
