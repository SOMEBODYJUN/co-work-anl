# 唯一规范代码包

从仓库根目录使用 Python 模块入口，输入和输出示例在 [USAGE](../USAGE.md)。本包按数学任务组织：共同目录普遍构造、异构纯构造、局部引理、实例精确算法。旧 astra_*/asym_research 名称不再提供第二套入口；原始路径见[迁移表](../research/path_migration.json)。

| 路径 | 作用 | 新写的数学合同 |
| --- | --- | --- |
| [shared_phi.py](shared_phi.py) | 固定 P/E/T/C 菜单、全目录威胁、实例证书及检查 | [共同目录算法](../research/current/shared/algorithm.md) |
| [shared/four_site_fptas_hardness.py](shared/four_site_fptas_hardness.py) | 从 PARTITION 构造四地点正整数间隙实例，不求均衡或最优值 | [全局无 FPTAS 证明](../research/current/shared/four_site_no_fptas.md) |
| [heterogeneous_two.py](heterogeneous_two.py) | 四种子纯 NE 菜单及因子 2 证书 | [异构算法](../research/current/heterogeneous/four_seed_algorithm.md) |
| [local/pure.py](local/pure.py) | 两算法共享的受保护纯修复 | [局部引理](../research/current/local_and_exact/local_geometry_and_chord.md) |
| [local/strong_chord.py](local/strong_chord.py) | 有条件的强弦局部见证 | [强弦 iff](../research/current/local_and_exact/local_geometry_and_chord.md) |
| [exact/bounded_overlap.py](exact/bounded_overlap.py) | 枚举全部独立混合 NE 支持单元，算实例最优 | [EXACT-KAPPA](../research/current/local_and_exact/exact_algorithms_and_extensions.md) |
| [exact/single_overlap.py](exact/single_overlap.py) | 每跨对至多一人时的实例精确算法 | [受限 ρ 的区别](../research/current/heterogeneous/restricted_rho.md) |
| [exact/threshold_dp.py](exact/threshold_dp.py) | 正整数公共权重的局部伪多项式谱 | [DP-W](../research/current/local_and_exact/exact_algorithms_and_extensions.md) |
| [exact/mitm.py](exact/mitm.py) | 共同目录/局部的指数级精确比较 | [MITM](../research/current/local_and_exact/exact_algorithms_and_extensions.md) |

短证书检查实际输入的达到因子；普遍上界、复杂度、实例最优分别需要各自的数学论证。三个主要证书格式保持不同字段，不能按名称相似强行合并。新实现按[增长规则](../research/GROWTH.md)增加唯一模块、测试、证明和资产关系。
