# 全可见真实最大标签联合层 v5：第一阶段准备接口

**状态：STAGE1_PREPARATION_INTERFACE_ONLY。优化器调用 0；完整输入尚未生成或冻结；最终总行数待 Main。**

本席 `visible_joint_v5_prepare` 已读取 v4 的实际准备器、完整字面检查器及来源审查，两个已核定新族的完整证明、源矩阵、坐标和尺度合同，并绑定 Main 的来源复核记录。Main 后续又明确允许读取已冻 `source2_minimal_cap_safe`；其 28 条 C-only 行已作来源/格式复核，但 Main 最终审查仍待付。写入范围仅为 `visible_maximum_joint_v5/` 与本说明。没有读取活跃的一般 minimal 或适应帽 ordered 族目录，也没有打开任何 LP 候选或 primal/dual 点文件。

## 已核定且必须完整保留的前缀

| 顺序 | 来源 | raw 数 | 0 起始索引 | 原尺度/数值尺度 |
| --- | --- | ---: | --- | --- |
| 1 | v4 完整输入 | 1586 | 0–1585 | 全部旧正尺度字符串原样保留 |
| 2 | `all_source_ordered_menu_cells` | 181 | 1586–1766 | 末 BR 均值权 1；数值除数 25；K=`c_i` |
| 3 | `source2_cap_coupled_internal_safe` | 28 | 1767–1794 | 末 BR 均值权 1；数值除数 25；已用 C 等式，K=`s/5` |

**1795 只是当前已核定前缀小计。** 已冻 source2 minimal 的 28 行不触发 1823 行中间输入。一般 minimal 的完整行数、各族追加顺序以及第三个适应帽 ordered 族是否纳入，均待 Main。

完整位序保持 `(a1,a2,a3,a4,a5,a6,x,o,c)`；全部 512 原子和独立 K，共 513 个非负列。原目标和两条自由等式不变。所有旧零行、稀疏零、显式零、重复行及 30 条 `rhs=-1` 行完整保留；新行也全行追加，不做去重或提前消元。

## 已建接口

- [`preparation_contract.json`](visible_maximum_joint_v5/preparation_contract.json)：固定 v4 与已批准来源的完整身份、具体行字段、前缀顺序、尺度和 35 个直接批准文件哈希；`final_raw_count=null`。
- [`source_review.md`](visible_maximum_joint_v5/source_review.md)：实际已读准确来源、完整模型量词、两族付款与 K 路由、未完成的来源列表。
- [`build_input.py`](visible_maximum_joint_v5/build_input.py)：只能在 Main 的完整释放后逐字组装；本阶段不执行组装。不存在求解或冻结入口。
- [`check_preparation.py`](visible_maximum_joint_v5/check_preparation.py)：标准库/Fraction 独立字面检查；阶段一只查明确批准的冻结包，并区分 Main 来源复核状态。
- [`pending_sources.json`](visible_maximum_joint_v5/pending_sources.json)：两个必需 minimal 族与可选适应帽 ordered 族所缺最终输入和全局释放要求。
- [`pending_source2_frozen_descriptor.json`](visible_maximum_joint_v5/pending_source2_frozen_descriptor.json)：已允许读取的 28 条 C-only 源格式、原行序与冻结身份；Main 最终复核字段仍为空。
- [`final_release.template.json`](visible_maximum_joint_v5/final_release.template.json)：不可执行的待填模板；本阶段不存在 `final_release.json`。

源格式存在已处理的差异：v4 的 `raw_rows` 是列表；ordered 使用 `rows` 列表与 `raw_row_count`；coupled 的 `raw_rows=28` 是整数，其列表仍为 `rows`，bit_order 必须读取该包的坐标合同。生成器使用每族明确的字段路径，不通过通用 fallback 猜行列表。

阶段一复核命令：

```bash
python research/workspaces/six-boss1-20261111/visible_maximum_joint_v5/check_preparation.py --stage1
```

结果在 `visible_maximum_joint_v5/stage1_known_source_check.json`；其范围仅是已批准冻结来源与公式路由。Main 已独立完成 ordered/coupled 两族全几何、真付款和全列复核，source2 minimal 的最终 Main 复核待付；本阶段不重跑来源项目程序。source2 minimal 的负自由等式乘子（包括 `-11/20`）必须保留，不能误作非负付款限制。

本阶段实际检查通过：v4 全 813,618 个列位置，ordered 全 92,853 个公式系数，coupled 全 14,364 个公式系数，以及 source2 minimal 全 14,364 个公式系数均核对完成。`stage1_gate_check.json` 记录语法检查及缺少 Main 最终释放时生成器的预期拒绝；没有生成输入、数值尺度合并表或冻结 manifest。全部代码仅导入 Python 标准库。

## Main 下一轮须交付

所有纳入族的最终 manifest、完整 family、proof、coordinate 合同及 SHA；准确完整 raw 行数和原行序哈希；Main 最终来源复核记录及 SHA；各族的最终追加先后和整个 v5 的准确总行数。source2 C-only 的冻结身份及 28 行已收到，其 Main 最终审查未收到。一般 minimal 将有五源，含源 2 的通用八标签 224 行，仍保 C 等式之前的真实 K 成本；它与 C-only 包不能混称。可选的 q=1/5 适应帽 ordered 族须显式决定纳入与否，再给最终包名和完整身份。

收到完整最终信息后，再实读最终证明、适配源格式及真预算检查、更新 source review，随后按 Main 的显式完整组装指令生成一次完整准备输入。不会冻结 1795 或 1823 行中间输入。

现有准备接口的释放只针对组装；`optimizer_authorized=false`、`freeze_authorized=false`。Boss1/Main 串行负责最终发布。原模型仍允许空覆盖、重复和别名、全弱平局；必要锥点不被解释为 SPE，half 仍 OPEN。
