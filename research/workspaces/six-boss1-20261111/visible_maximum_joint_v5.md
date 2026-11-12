# 全可见真实最大标签联合层 v5：3056 行冻结准备

**状态：PREPARED_NO_OPTIMIZER。完整 3056 条 raw 不等式、513 个非负列、2 条自由等式；优化器调用 0。**
独立完整准备检查通过；准备冻结不授权数值调用，最终准入由 Boss1/Main 对准确冻结身份再预检。
原六人 half 问题仍 OPEN，必要锥点不被解释为 SPE。

## 精确输入与准入身份

- 输入：`visible_maximum_joint_v5/exact_input.json`。
- 输入 SHA256：`12f456dfbc789a5c1826d248e4851b84f66b428554d181b7ba12cbfdb920f3ac`。
- Main 完整组装释放 SHA256：`653e43d66feda8874fef8230fe95d689aa00378bca327284ddee43fcf300f821`。
- 冻结身份：`visible_maximum_joint_v5/freeze_manifest.json`；逐件摘要：`SHA256SUMS`。

Main 的最终 release 和 source review 字节保持不变。Main 后续明确授权“记录失败、适配、检查并冻结”的任务另存于
`preparation_freeze_authorization.json`；它没有授予优化权限。新 λ230 族不进入此输入。

## 完整原行顺序与尺度

| 0 起始 raw 区间 | 行数 | 来源 | 原 K 付款 |
| --- | ---: | --- | --- |
| 0–1585 | 1586 | `visible_maximum_joint_v4` | 原系数字典和全部旧尺度逐字继承 |
| 1586–1766 | 181 | `all_source_ordered_menu_cells` | 原 `c_i` |
| 1767–1794 | 28 | `source2_cap_coupled_internal_safe` | 已使用 C 等式后的 `s/5` |
| 1795–1822 | 28 | `source2_minimal_cap_safe` | 已使用 C 等式后的 `s/5` |
| 1823–2918 | 1096 | `all_source_minimal_cap_safe` | 原 `S=1+sum(beta)` |
| 2919–3055 | 137 | `ordered_minimal_cap` | 原 `S=1+sum(beta)` |

全部 512 个 `(a1,a2,a3,a4,a5,a6,x,o,c)` 型与独立 K 列 512 保留，全部 513 列非负。
原目标、`sum(o*z)=1`、`sum(c*z)-K=0`、原字典序与两份列路由文件均保持原样。
所有新增行的末 BR 均值原权为 1，数值除数统一为正字符串 25；源 IC 的真实权可不同。
所有原尺度字符串、稀疏零、显式零、重复行和元数据均保留。

原 30 条 `rhs=-1` 行、1 条零行与总 123 条准确重复 raw 行均未删除。
2932 条不同非零仿射行只作完整输出后的诊断统计，没有用于选行或压列。
一般 minimal 的源 2 八目标各 28 行，共 224 行；其 C 目标仍保持消等式前的真实 S 成本。
一般 H 使用 `t/min(D,5)`，没有改成统一 K/5。C-only 包的 `-11/20` 自由等式乘子完整保留，且没有二次消元。

## 实际失败及修复

Main 首次实际 build 在旧代码第 203 行发生 `KeyError: K_column`，当时未写任何完整输入。
真实失败与当时源码分别保留于 `build_attempt1_failure.json`、`build_attempt1_source.py`。
唯一异形来源是 `ordered_minimal_cap`：它使用 `columns[0..511]={column,bits,type_string}` 和
`columns[512]={column:512,kind:independent_K}`，没有 `K_column`、`atom_columns` 或 `schema` 坐标字段。

生成器和独立 checker 分别实现显式字段适配，逐原位置检查全部 513 列并匹配 v4 的完整原子字典，
没有排序掩盖置换，也没有修改来源字节。其余四个来源继续逐字比较原坐标结构。
修复后的第二次实际 build 成功，第一次完整 checker 通过；执行记录分别在
`build_attempt2_execution.json`、`assembled_check_attempt1_execution.json`。

## 完整独立检查

| 检查范围 | 精确数量 | 结果 |
| --- | ---: | --- |
| v4 全列位置、原目标与两等式、旧尺度 | 813618 个列位置／1586 个尺度字符串 | 保持原样 |
| ordered cells 全列公式 | 92853 | 全部一致 |
| coupled C-only 全列公式 | 14364 | 全部一致 |
| minimal C-only 全列公式 | 14364 | 全部一致 |
| 一般 minimal 五源八目标全列公式 | 562248 | 全部一致 |
| ordered minimal 五源全列公式 | 70281 | 全部一致 |
| 新增公式合计 | 754110 | 全部准确相等 |
| 全系统列位置合计 | 1567728 | 全部核对 |
| 一般源 2 C 行与 C-only 的有符号等式身份 | 28 对／14364 列 | 全部零残差，全部行保留 |

`literal_check_result.json` 为 **PASS_COMPLETE_LITERAL_PREPARATION**。
完整 source 字典、原顺序、全部非行 metadata、各族原 K 成本、系数字符串和数值尺度均分别比较。
Main 已完成所有最终来源的完整几何、真实隐藏成本和弱平局证明；准备 checker 另外独立重建所有新增公式系数，
未导入 builder 或来源项目代码，全部程序只有 Python 标准库。

只读子席另核五族坐标、所有新增行尺度和 20 件批准源文件首尾身份，报告在 `independent_coordinate_review.json`。
完整实读、修复和审查说明见 `preparation_review.md`；Main 准入审查仍为原 `source_review.md`。

## 当前文件与后续权限

当前完整状态是 `final_preparation_state.json`；最终源顺序是 `final_release.json`，冻结身份以 `freeze_manifest.json` 为准。
`stage1_*`、初始 `preparation_contract.json`、模板和初始 pending 记录保留阶段一事实，不是当前待付列表。

manifest 明确给出 `raw_rows=3056`、`columns=513`、`equalities=2`，`artifacts` 仅用包内 basename 和 SHA256 字符串。
没有优化调用、旧点读取或支持限制，没有固定 K，没有 SPE 构造或新最优值声明。
Boss1/Main 将对这份准确冻结输入做全 3056 concat、目标、等式和尺度预检后，另行决定是否释放一次数值调用。
