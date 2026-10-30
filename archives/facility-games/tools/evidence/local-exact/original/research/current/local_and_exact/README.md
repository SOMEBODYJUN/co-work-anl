# 固定布局与实例最优：精确客户均衡、算法和费用扩展

默认对象为双设施、正权原子客户、覆盖后强制参与、独立客户随机化；客户最小化含自身重量的预计负载，设施最大化承接重量。原子—Wardrop 比较单独允许任意设施数，但只研究固定布局，不自动推出全局 SPE。

本专题提供**局部精确 NE 的几何描述、实例最优倍率的精确求解和有条件的费用迁移**。局部 DP、MITM、有界交叠最优化不依赖普遍 φ 上界；以它们搜索保证 φ 的证书时才依赖该定理。这里的证明和审读属于仓库内部记录，外部同行评审与优先权没有在本次整理中升级。

## 主要结论与证据状态

| 成果族 | 数学保证 | 证据或未解边界 |
| --- | --- | --- |
| 精确局部几何与强弦 | 支持单元完备性来自最佳回应；双配额精确 NE 与强弦构造有完整分支和位长 | 完整重建在[共同目录强弦页](../shared/local_chord_full.md)，对应主稿附录；内部交叉审读 |
| 精确支持枚举、整数 DP、MITM | 分开局部极值、全局实例最优倍率与实现合同 | 当前算法候选/软件身份逐项在账本记录；达到证书不等于全局最优性证书 |
| 费用扩展 | 二次费用局部等价直接成立；继承 φ 为依赖 SC-PHI-E 的条件应用 | 不能扩至任意凸费用；多面体续局框架及部分参数求解器未实现 |
| 原子—Wardrop 误差 | 固定布局任意设施数的每坐标尖锐误差 `(k−1)θ/2` 及链族取等 | 运输耦合的内部完整证明；不声称任意设施数 SPE，相关大规模拥塞文献新意另查 |

## 按数学成果族阅读

1. 研究某个布局的全部精确客户 NE 或配额：先读[公共模型](../model.md)，再读局部几何，具体构造转到完整强弦页。
2. 计算某个实例的最优倍率：先读精确算法合同；共同目录再读[同址正规形](../shared/instance_complexity_barriers.md)，只枚举异址交叠。异构 EXACT-KAPPA 仍计全部合法布局。
3. 改费用或近似原子客户：费用迁移查精确算法页的条件；可拆分对照查原子—Wardrop 页，避免把固定布局误差升级成选址存在定理。

## 全部分支数学正文

| 中文资产名 | 文件 | 数学内容与读取时机 |
| --- | --- | --- |
| [双设施固定布局的精确均衡谱与配额强弦](local_geometry_and_chord.md) | `local_geometry_and_chord.md` | 从客户最佳回应推导支持单元完备性，并连接双配额可行性与强弦构造的完整证明。 |
| [实例最优精确算法、局部困难性与费用扩展](exact_algorithms_and_extensions.md) | `exact_algorithms_and_extensions.md` | 统一支持枚举、整数 DP、MITM、参数算法及二次等价、多面体续局；分别标明已实现和未实现部分。 |
| [任意设施数原子均衡与 Wardrop 负载的尖锐误差](atomic_wardrop_gap.md) | `atomic_wardrop_gap.md` | 以运输耦合比较固定布局原子客户 NE 与可拆分负载；链族给坐标误差取等，不推出全局 SPE。 |

## 实现合同与来源差异

本轮另有严格的新参数界：[共同目录同址正规形](../shared/instance_complexity_barriers.md)使精确实例最优值及完整续局只需枚举**异址**交叠 $\kappa_{\ne}$ 的客户支持。实现和对照见 [shared_offdiag.py](../../../facility_spe/exact/shared_offdiag.py) 与 [test_shared_offdiag.py](../../../tests/test_shared_offdiag.py)。原 EXACT-KAPPA 的异构目录范围依旧以所有合法布局的交叠计；这个新证明用到了两家拥有相同目录。

1. 旧 exact-methods 笔记末段仍把“绕开精确局部极值的多项式 φ 算法”称作未来目标；当前主稿和[现行共享分支](../shared/README.md)已有有限菜单及 Appendix B 构造的全分支证明和内部审读。应保留旧探索的时间语境，并把当前内部证明与外部同行评审分开记录。
2. 旧来源使用 `mitm_solver.py`、`run_lazy_ring.py` 等历史文件名。实际入口为 [mitm.py](../../../facility_spe/exact/mitm.py) 与 [lazy_ring.py](../../../facility_spe/cli/lazy_ring.py)。DP 实现在 [facility_spe/exact/threshold_dp.py](../../../facility_spe/exact/threshold_dp.py)。本目录链接使用实际入口。
3. bounded-overlap 证明说短证书可直接验证，需要补充：它只证明**达到所报倍率**。全局最优性仍靠支持枚举及优化证明或重算；当前 `verify()` 用显式异常拒绝负的 `finite_factor_exists=False` 报告，且在 `python -O` 下仍执行检查。
4. strong-chord 的 `construct()` 文档字符串称失败“返回 None”，实际返回包含 `probabilities=None`、`branch='infeasible'` 和障碍数据的字典。应用程序应按实际接口判断。
5. [旧二次扩展笔记](../../../history/source/notes/extensions/quadratic.md)引用旧同目录 `extension_report.md`，该审阅记录现已保存为[cost_extensions.md](../../../history/source/audits/cost_extensions.md)；其“已核准”表示内部审阅。继承 φ 是对 SC-PHI-E 的条件应用，须同时保留该命题的输入范围与内部证明、外部评审状态。
6. 原 bounded-overlap 笔记记载 300 个跨一交叠实例和 100 个局部随机实例；当前该模块未提供这些计数对应的自测入口。本次不将历史计数写成新运行结果。DP 的 530 例与 MITM 的 435/12 例有可运行入口；MITM 另有[保存的运行记录](../../../evidence/runs/2026-09-30/mitm.json)。

本目录概览与全分支证明的覆盖度分别标注；实现和本轮运行事实见对应证据记录。未实现部分包括不同权值数参数 ILP 求解器、一般有理多面体 continuation LP 框架及其非线性交叠至多二的实例。

现行定义与状态以[规范模型](../model.md)、[现行命题](../claims.md)及[五轴审查](../../review_status.json)为准。[共享主稿](../../../history/source/manuscripts/shared_phi/main.tex)、[第一轮局部概览](https://github.com/SOMEBODYJUN/co-work-anl/blob/bd7798d5bbcc8086217ff54d7f91b445d0374b4f/history/curation-2026-10-01/LOCAL_GAME.md)和[计算概览](https://github.com/SOMEBODYJUN/co-work-anl/blob/bd7798d5bbcc8086217ff54d7f91b445d0374b4f/history/curation-2026-10-01/COMPUTATION_AND_EXTENSIONS.md)仅按来源身份追溯。
