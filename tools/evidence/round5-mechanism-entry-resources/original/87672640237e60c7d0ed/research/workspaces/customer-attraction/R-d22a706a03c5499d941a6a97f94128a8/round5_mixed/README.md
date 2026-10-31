# 第五轮：完整根菜单的混合阻断

主目标 Q-CAG-HALF 与一般 Mfull 均未在本目录宣布解决。本文档不改共享账本。

| 文件 | 精确范围与用途 |
| --- | --- |
| [replicated_menu_minimax.md](replicated_menu_minimax.md) | **条件性解析结果。** 若 n 块根菜单可由完整 SPE 实现，则 n≥3 时精确混合值为 `37/10−17/(12n)`；n=4 首次严格超过根收益 `13/4`。后继可实现性由同轮 credible_family 单独研究，不能把条件菜单当成完整反例。 |
| [verify_replicated_menu_minimax.py](verify_replicated_menu_minimax.py) | 独立从五类单位客户计算单块矩阵、根自身收益、原始/对偶匹配及自由背景cap；不用规范 solver 或已有审计矩阵。 |
| [three_block_last_low_witness.md](three_block_last_low_witness.md)、[独立局部核验器](verify_last_low_witness.py) | **局部解析阻断。** 在 `ACD | AAB | AAB` 前缀余三人时，当前人可保证 `37/10>13/4`；仅用最后两人的直接最佳回复分析。它只验证一个障碍节点，不覆盖全部目标排序。 |

同轮 credible_family 的精确集合 BI 已发现 **n=3 的四类指定根列全部不可实现**，故不能把本条件矩阵当真实反例，亦不能再盲用两块直和。其诊断见 `../round5_credible/block_menu_n3_probe.json`；本目录没有将该大 BI 独立重跑。若某个 n≥4 真能实现，条件矩阵资产将否定 Mfull 及弱完整终局推送，不否定自由选择竞争背景的 extra-one 门槛或半覆盖；此时需要单独证明完整可实现性。

一次替代诊断也失败：固定 `p=uniform(D0,D1,D2)`、根自身收益限制 `≤13/4`，真实 n=3 子树中每类根行动所能取的最大 p 插入值为 `(101/30,283/90,197/60,551/180)`；B、D 类没有超过根收益。因此没有继续在此固定实例调参。最大值及可实现性来自同一 credible_family 探针；本目录只独立重算相应展示 profile 的有理插入值。
