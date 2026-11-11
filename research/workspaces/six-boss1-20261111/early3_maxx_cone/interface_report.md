# 第三位常数 61/3 的 17 条同列接口

本行包在普遍数学证书单独冻结之后生成，并在任何 5b1b 点权重读取之前冻结。它引用 [普遍证明](../early3_maxx_cone.md) 的八份真实预算，不把旧任意锚 AP 当作常数 61/3 的证明。

## 结论

输出 [rows_17.json](rows_17.json)：**17 行、21021 既有列、1720 个非零系数、0 新列**。每行对应旧 `early_x_anchor_queries/rows_51.json` 中实际第三人的一个查询轨道，全部沿用同一个 actual 前四 f_P 最大标签 X。

每个查询轨道的平均必要行是

\[
\frac{61}{3}u_3-
\sum_h\frac{58x_h}{3(b_h+4)}
-\frac1{|\mathcal O|}\sum_{Q\in\mathcal O}\sum_h\frac{q_{h,Q}}{b_h+1}
+\frac1{|\mathcal O|}\sum_{Q\in\mathcal O}\sum_h
\frac{3y_{h,Q}}{(b_h+1)(b_h+4)}\ge0.
\]

这里 `b_h` 是原 actual 前二负载，`u3` 来自 raw `actual_bits` 第三位及实际六位总负载。`x_h` 是既有共同 X 质量列。对确定会员的 A/T/B/C 查询，真实 XQ 已由该会员位和 x_h 确定；对 R/Z/H 查询，`y_hQ` 使用原 420 个既有交叠上包络。

## 生成恒等式与独立核验

从 raw actual_bits 和 X 列重新生成

\[
\mathrm{SAFE}_3=u_3-\sum_h\frac{x_h}{b_h+4}.
\]

随后逐稀疏系数计算

\[
\mathrm{row}_{61/3}=\mathrm{row}_{23}-\frac83\mathrm{SAFE}_3.
\]

这是坐标生成恒等式。较强新行的有效性来自已冻结的普遍 61/3 证明；不能把“从一个已知非负行中减去另一非负量”当作独立的有效性推理。

[verify_interface.py](verify_interface.py) 不导入生成器，从另一路径直接重建新目标。它使用 raw A 会员、T/B/C 八词展开、R/Z joint-reply 三状态和 H 的 B4 两个真实角色位计算每个字面查询，再平均同一个轨道中的合法标签；没有把平均作为可行动的分数标签。原 raw SAFE3 与既有 symbolic lift 的第三位 SAFE 行逐分数一致。

核验结果见 [interface_verification.json](interface_verification.json)：

| 检查 | 精确结果 |
|---|---:|
| 既有列总数 | 21021 |
| raw hist 数及共同 X 质量列数 | 16 / 16 |
| 新行数 / 非零数 / 新列数 | 17 / 1720 / 0 |
| 全部 R/Z 原 joint 分组 | 194 |
| 从 raw 状态重建并比对的查询边缘 | 420 |
| 直接新公式 = 旧行 − (8/3) SAFE3 | 17 行逐系数通过 |
| 字面查询及 S6 轨道 | 158 / 17 |
| 字面 hist 查询检查 | 2528 |
| S6 代表图像与 hist 的等频检查 | 195840 |
| 原六个零质量 hist | 1,59,366,449,524,574，全部保留 |
| 优化器调用 / 点权重读取 | 0 / 0 |

每行保留全部 16 个 X 质量列，未按点的支持删除任何 hist。17 行总体中 420 个 y 列各出现一次，系数与原第三位 23 行完全相同且严格为正。因为每个真实交叠 `c_hQ≤y_hQ`，正系数替换只放宽目标行；原 `y=min(x,q)` 的规范化继续有效。该论证没有把 420 个上包络同时实现为一份真实客户交叠。

## 冻结及接口边界

旧 51 行、旧完整矩阵和 Main 的 23625 行准备均未修改。新行包只作为单独可追加的数学接口，是否合并由 Main 后续处理。它本身没有声称提高任何 LP 的最优值，也没有评价某个固定点。

普遍数学证书冻结清单：[math_freeze_manifest.json](math_freeze_manifest.json)。本行包另存 `interface_freeze_manifest.json`，后续若评价新 5b1b 点，结果与输入点 SHA 将单独保存，且不回写上述两个冻结包。

只复核现有输出时执行：

```sh
python -B research/workspaces/six-boss1-20261111/early3_maxx_cone/verify_interface.py
```

构造器拒绝覆盖已有输出。数学证明和行包都不需要重新运行任何优化器。
