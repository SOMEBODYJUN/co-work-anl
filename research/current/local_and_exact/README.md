# 局部均衡、精确求解与条件扩展

本目录为重新推导和组织的研究说明，日期为 2026-10-01。对象是两设施、正权客户、覆盖后强制参与、客户独立随机选择可达设施的模型；默认客户最小化包含自身重量的预计负载，设施最大化预计承接重量。这里的“定理”指仓库内部证明陈述，不表示已经发表或外部审稿通过。

## 阅读顺序和逻辑边界

| 文档 | 问题 | 结论与依赖 |
| --- | --- | --- |
| [局部几何与强交叉弦](local_geometry_and_chord.md) | 固定布局有哪些精确 NE？何时存在两个指定配额的 NE？ | 支持单元完备性直接来自最优反应；strong-chord iff、全分支构造和位长已在[现行完整重建](../shared/local_chord_full.md)写出，对应共享主稿 Appendix A–B，均为内部证明。 |
| [精确算法与条件扩展](exact_algorithms_and_extensions.md) | 如何求局部极值和实例最优 SPE 倍率？何种费用扩展成立？ | DP、MITM、有界交叠最优化不依赖全局 φ 上界；将它们用于保证 φ 的搜索才依赖该上界。二次费用等价独立成立。 |

现行模型与状态以[规范模型](../model.md)和[现行命题](../claims.md)为准。原始来源为[共享主稿](../../../history/source/manuscripts/shared_phi/main.tex)，第一轮的[局部概览](../../../history/curation-2026-10-01/LOCAL_GAME.md)与[计算概览](../../../history/curation-2026-10-01/COMPUTATION_AND_EXTENSIONS.md)仅作可追溯的中间整理。有限测试是实现证据，不是任意规模证明。

## 本次来源核对发现

本轮另有严格的新参数界：[共同目录同址正规形](../shared/instance_complexity_barriers.md)使精确实例最优值及完整续局只需枚举**异址**交叠 $\kappa_{\ne}$ 的客户支持。实现和对照见 [shared_offdiag.py](../../../facility_spe/exact/shared_offdiag.py) 与 [test_shared_offdiag.py](../../../tests/test_shared_offdiag.py)。原 EXACT-KAPPA 的异构目录范围依旧以所有合法布局的交叠计；这个新证明用到了两家拥有相同目录。

1. 旧 exact-methods 笔记末段仍把“绕开精确局部极值的多项式 φ 算法”称作未来目标；当前主稿和[现行共享分支](../shared/README.md)已有有限菜单及 Appendix B 构造的全分支证明和内部审读。应保留旧探索的时间语境，并把当前内部证明与外部同行评审分开记录。
2. 旧来源使用 `mitm_solver.py`、`run_lazy_ring.py` 等历史文件名。实际入口为 [mitm.py](../../../facility_spe/exact/mitm.py) 与 [lazy_ring.py](../../../facility_spe/cli/lazy_ring.py)。DP 实现在 [facility_spe/exact/threshold_dp.py](../../../facility_spe/exact/threshold_dp.py)。本目录链接使用实际入口。
3. bounded-overlap 证明说短证书可直接验证，需要补充：它只证明**达到所报倍率**。全局最优性仍靠支持枚举及优化证明或重算；当前 `verify()` 用显式异常拒绝负的 `finite_factor_exists=False` 报告，且在 `python -O` 下仍执行检查。
4. strong-chord 的 `construct()` 文档字符串称失败“返回 None”，实际返回包含 `probabilities=None`、`branch='infeasible'` 和障碍数据的字典。应用程序应按实际接口判断。
5. [旧二次扩展笔记](../../../history/source/notes/extensions/quadratic.md)引用旧同目录 `extension_report.md`，该审阅记录现已保存为[cost_extensions.md](../../../history/source/audits/cost_extensions.md)；其“已核准”表示内部审阅。继承 φ 是对 SC-PHI-E 的条件应用，须同时保留该命题的输入范围与内部证明、外部评审状态。
6. 原 bounded-overlap 笔记记载 300 个跨一交叠实例和 100 个局部随机实例；当前该模块未提供这些计数对应的自测入口。本次不将历史计数写成新运行结果。DP 的 530 例与 MITM 的 435/12 例有可运行入口；MITM 另有[保存的运行记录](../../../evidence/runs/2026-09-30/mitm.json)。

本目录概览与全分支证明的覆盖度分别标注；实现和本轮运行事实见对应证据记录。未实现部分包括不同权值数参数 ILP 求解器、一般有理多面体 continuation LP 框架及其非线性交叠至多二的实例。
