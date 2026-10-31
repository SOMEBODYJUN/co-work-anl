# R-24e40cab6b8d43ecbbf1c15c4d0edcd5 的个人研究工作区

研究存档：`customer-attraction`；发布身份：`R-24e40cab6b8d43ecbbf1c15c4d0edcd5`。

## 当前研究

目标是原量词不变的 `Q-CAG-HALF`：任意有限共同目录、任意人数、全部有序历史依赖纯 SPE，证明 `2W >= OPT_m`。本轮已确认主目标仍 OPEN。

我负责的直接一般表示见 [`direct/static_debt_reduction.md`](direct/static_debt_reduction.md)：对实际终局与任意最优元组，静态插入收益、真实续局收益和 retaliation debt 给出精确恒等式；半覆盖被归约为一条跨真实分支的总债务不等式。它不冻结后继，也不把辅助桥提升为定理。

并行研究的已推送材料：

- [`potential_dual/prefix_budget_lp_sharpness.md`](potential_dual/prefix_budget_lp_sharpness.md)：全部真实前缀预算行的 LP 尖锐界，说明仅重组 prefix rows 不能到达 1/2。
- [`shared_omission/target_union_incidence_budget.md`](shared_omission/target_union_incidence_budget.md)：把 incidence-LP 限制到单个最优并集的条件预算，以及任意共享 incidence 下固定驻留流的精确负余项。
- [`dynamic_flow/cartesian_pair_obstruction.md`](dynamic_flow/cartesian_pair_obstruction.md)：Cartesian 产品放大 root-reset signed-flow 障碍；只排除局部 slack/tax 或 pairwise cap，不是主目标反例。
- [`credible_counterexample/README.md`](credible_counterexample/README.md)：全历史有限扫描与 extra-one/真实菜单的精确障碍；仅为有限观察和辅助接口边界。

当前真正未付义务是：控制 `sum_i R_i(T_i)`，即各最优主题静态插入相对真实后继的反制债务；现有有限结果没有把它压到 harmonic insertion credit。

## 可访问材料

按需要在 notes/、experiments/、candidates/ 中保存有接续价值的材料，并在此链接。成熟资产沿既有规范入库，此处链接正文，不重复复制。

## 交流与状态

可以通过同一 work.py 私聊这个发布身份；其他人可访问已推送材料。本地草稿只有完成 checkpoint 并确认 pushed 后才对其他 clone 可见。
