# 3056 完整准备：实际失败、显式坐标适配与独立复核

本次固定准入是 Main 已释放的完整 3056 行。`final_release.json` 的 SHA256 保持
`653e43d66feda8874fef8230fe95d689aa00378bca327284ddee43fcf300f821`，Main 写入的
`source_review.md` 也保持原字节。λ230 新族不在本输入内。全部工作只发生于本包和相邻说明；优化器调用为零。

## 1. 第一轮真实失败及修复

Main 首次实际运行 builder，在旧代码第 203 行逐字段检查坐标合同时发生 `KeyError: K_column`。
接手时完整输出均不存在。`build_attempt1_failure.json` 记录 Main 的真实报告和接手时状态；
`build_attempt1_source.py` 保存当时源码字节。没有把这次失败改写为首跑成功，也没有为了生成日志重跑同一已知失败。

缺字段发生于最后一个冻结包 `ordered_minimal_cap`。前四个包仍使用完整
`variables/K_column/bit_order/atom_columns` 结构。新 ordered 包的坐标结构是：

- `columns[0..511]` 各含原位置 `column`、九位 `bits`、九字符 `type_string`；
- `columns[512]` 准确等于 `{"column":512,"kind":"independent_K"}`；
- `all_512_types_lexicographic=true`、`K_is_independent=true`、`uses_C_equality=false`；
- 坐标文件没有 `K_column`、`atom_columns` 或 `schema` 字段；family 顶层仍明确给出 `K_column=512`。

builder 按明确包名及已固定文件 SHA 分派适配，逐原位置比较全部 513 列，不排序、不猜字段、不改变来源。
独立 checker 另行用九位大端展开解码，再与 v4 完整原子字典比较，不导入 builder。
前四包原子字典继续逐字比较；存在的 C 等式按完整 513 列核对，缺少可选 `nonnegative_columns` 不人为补写来源。
最终非负列全集仍逐字继承 v4。

修复后的第二次实际 build 成功，记录于 `build_attempt2_execution.json`。
生成输入 SHA256 为 `12f456dfbc789a5c1826d248e4851b84f66b428554d181b7ba12cbfdb920f3ac`。

## 2. 最终来源及完整顺序

| 0 起始 raw 区间 | 行数 | 完整来源 | 原 K 列 |
| --- | ---: | --- | --- |
| 0–1585 | 1586 | v4 原完整输入 | 原字典逐字保留 |
| 1586–1766 | 181 | `all_source_ordered_menu_cells` | 原 `c_i` |
| 1767–1794 | 28 | `source2_cap_coupled_internal_safe` | 已用 C 等式后的 `s/5` |
| 1795–1822 | 28 | `source2_minimal_cap_safe` | 已用 C 等式后的 `s/5` |
| 1823–2918 | 1096 | `all_source_minimal_cap_safe` | 原 `S=1+sum(beta)` |
| 2919–3055 | 137 | `ordered_minimal_cap` | 原 `S=1+sum(beta)` |

新增全 1470 行均以末 BR 均值权 1 的原尺度存储，数值除数为正字符串 `25`；源 IC 的真实权可变化。
原 1586 的正尺度字符串、稀疏零和显式零、元数据与行序全部保留。30 条 `rhs=-1` 原行、1 条零行和
123 条准确重复 raw 行均保留；2932 条不同非零仿射行只是诊断数字，不参与删除或选行。

一般 minimal 包的源 2 保留全部八个目标各 28 行，共 224 行。其 C 目标行仍保消等式前的真实 K 帽成本。
独立 checker 对全部 28 对核出
`R_general = R_C_only - (S-s/5)(|C|-K)`，全 14364 个系数准确零残差，两套完整行均保留。
`tau=0,s=9` 的自由等式乘子 `-11/20` 原样保留，不误当成非负预算权。

## 3. 准确来源阅读与复核分工

本席已实读新两族准确冻结版的完整证明：一般 minimal 的 SHA
`30e2f3add32ec4d49192325dbe706e9d1c7e958722df0402d4699991fd9f69b6`；ordered minimal 的 SHA
`db6dd7c970ff5a525ad8b86f23640025ec5f66b250eccc85ad48f522e9fe401d`。
根六个双缺面、全五源、全部八目标、坐标最小帽、同六菜单内排同索引、原尺度和 K 成本均保持来源陈述。

一般行保留

\[
a u_i+S K-\sum_x\left[S t_x+\frac{24t_x}{D_x}
-\frac{s t_x}{\min(D_x,5)}+\frac{o_x}{6[p_x+1+(6-i)t_x]}
+\sum_{j>i}\frac{\tau_jo_x}{6[p_x+(j-i)t_x+7-j]}\right]\ge0.
\]

ordered 行使用其新 `1/10` 常数帽和 `1/[5(7-j)(8-j)]` 交叉系数，以及无损仿射 G。
没有把新域套成旧固定帽域，也没有把一般 `H_i(T)` 改成统一 `|T|/5` 或 K/5。

Main 的已固定来源报告承担完整域、全部几何、真实隐藏成本和弱平局最小值证明。
本席的独立准备检查另从各族已读公式重建所有新增系数，并按完整源字典核装配，不重跑旧项目程序或任何优化器。
五族新增公式重建计数分别为 92853、14364、14364、562248、70281，总 **754110**；
加原 1586 行全部列位置，总 **1567728**。目标、两等式、完整 513 非负列和原列路由均通过。

`coordinate_contract_audit` 子席另外进行了独立只读坐标／尺度审查，完整核五族 20 件来源文件首尾 SHA、
全部原子、1470 条新增行与旧尺度；返回 PASS，未写文件、未执行来源程序、零优化。报告由本席按其真实返回记录。
实现独立不被宣称为外部盲审。

## 4. 检查与冻结边界

第一次完整 `check_preparation.py --assembled` 通过，真实执行记录在
`assembled_check_attempt1_execution.json`，结果在 `literal_check_result.json`。
冻结只使用 Main 后续明确要求“修复、检查并冻结”的授权，记录于 `preparation_freeze_authorization.json`；
原 `final_release.json` 的组装权限字段继续原样保留。这个准备冻结不授权数值优化。

`freeze_manifest.json` 的 `artifacts` 仅使用本包 basename 作为键、SHA256 字符串作为值，避免下游读者二次拼接仓库路径。
显式计数字段是 `raw_rows=3056`、`columns=513`、`equalities=2`。相邻说明的 SHA 单列，不写入 basename 工件表。
阶段一说明和 pending 工件是历史；当前准入和身份由最终 release、完整 input 与 freeze manifest 确定。

原模型仍是有限单位客户、有限非空共同标签目录、完整有序历史纯 SPE，允许空覆盖、重复、覆盖别名与全部弱平局。
这里仅得到完整必要行输入；不声称锥点可实现为 SPE、任何新最优值或 half 结论。half 仍 OPEN。
