# 可见最大 C 联合 v4：1586 行求解骨架待释放

Boss1；RUN six-boss1-20261111。状态：**WAITING_INPUT_AND_MAIN_RELEASE**。

本项只完成求解骨架，**当前优化授权 0、实际优化调用 0**。尚无已释放的 input SHA，也没有 main_release.json、消费标记或数值结果。开始时一次性确认新输入目录尚未出现；未轮询，未选择任何旧输入替代。

## 已落盘接口

| 文件 | 职责 |
|---|---|
| contract.py | 1586 raw／513 非负列／2 等式；精确 SHA、预检和明确 Main 授权门禁 |
| solve_once.py | 未来唯一 highs-ds 调用；60 秒、presolve=False、先排他消费记录 |
| recover_exact.py | 一次返回支持上的有理线性代数；全部原尺度付款和仿射 rhs；失败保留障碍 |
| verify_certificate.py | 独立标准库 Fraction 全行、全列、自由等式与互补核验 |
| analyze_optimal_face.py | 全部零对偶余量列上的完整最优面、全部 1586 条参数条件 |
| main_release.template.json | 空授权模板，不是调用许可 |
| expected_outputs.json | 未来实际结果、证书、诊断与最终冻结的输出合同 |

完整数学说明见 [source_review.md](visible_maximum_joint_v4_solve/source_review.md)。

## 保持的严格边界

未来模型完整保留 1050 个上游 raw 行和新 536 行、全部 512 九位客户类型与独立 K 列、原目标、两条自由等式以及 rhs=−1 的仿射上帽。所有零/重复行保留。没有 fixed K、支持限制、旧点补全或第二优化器路径。

新 536 行的真实 source weight 可以不同；其准备数值除数仍逐条为 25。精确恢复使用原系数，按 \(y_i=-\mathrm{SciPyMarginal}_i/d_i\) 归还原尺度。

完整面从所有零对偶余量列出发，不局限于返回点支持。任何旧等号排除都必须等新正付款与自己的真实来源确认后才使用；不预设 NS5 正付款，也不预设某个 \(u_2-K/5\) 结论。

Main 尚需释放准确 1586 输入 SHA、准备/尺度/来源/预检指纹及明确一次 LP 授权。静态骨架检查不代替新 536 行的来源审查和全系数预检。当前没有产生新福利界或 SPE，原六人半覆盖仍 OPEN。
