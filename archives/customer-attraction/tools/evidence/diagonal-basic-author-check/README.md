# 对角基本预算诊断的真实证据

主源 `ae3a69e8e041bfd1b8f5`；正文为[对角回复基本预算的拆分诊断程序](../../../state/程序/对角回复基本预算的拆分诊断程序--程序.md)。完整原码3061B；两份直接输入是旧1905列 `attractive_nested_exact.json` 与321变量的 `zz_threshold_exact.json`。主程序保旧K/历史/R边缘，用后者重新聚合Z/RZ，故诊断对象是3949阈值阶段的点，不是旧3889点原样或后3945点。

## 文件与事件

| 文件 | 作用 |
| --- | --- |
| `original/diagonal_basic_check.py` | 未改原入口；有顶层计算及覆盖status副作用，不能安全地把import当只读加载 |
| `related/zz_threshold_exact.json` | 完整136130B直接输入；本轮321条实际记录全核 |
| `related/zz_threshold_closure.py` | 全文实读的8353B生成器，解释slab、R位和作者3949行声明；本轮没有执行 |
| `source-manifest.json` | 冻结提交、ID、SHA、共享旧输入/模块路由、比较对象与范围 |
| `rerun/launch_once.py` | 当时在clone外使用的真实一次启动脚本，含该事件绝对路径；留作事件来源，不自动重跑 |
| `rerun/execution-event.json` | 原入口唯一执行：2026-11-01，Python3.12.14，0.963秒，exit0，stderr0；50库存文件前后相同，其中49冻结文件及1根标记 |
| `rerun/stdout.json` / `stderr.txt` | 938B实际stdout与0B实际stderr；原生成status与stdout字节相同 |
| `inspect_diagonal_input.py` | 新增全输入解码与当前点的逐客户四状态评价；不运行原构图或求解器 |
| `input-and-local-check.json` | 321完整描述符/界、25段、194组、56拆分余量、28合行和O/W |
| `hybrid-moment-ledger.json` | 194组旧Z/RZ、新Z/RZ及四状态质量，全量可接续 |
| `selfcheck.py` / `selfcheck.json` | 静态指纹、链接、回执、保存输出及账表一致性；不是新增原程序运行 |

旧816498B输入与相关模块共用 `../combined-branch-master-program/dependencies/` 的冻结原件。源清单给出真实旧路径；没有为了这份诊断复制全部大依赖。先前 `../split-basic-graph-program/verify_split_rows.py` 中 `literal()` 是已做过全域系数比较的独立收益定义。本轮只导入该新审计模块的定义，不调用其main，也不导入历史图构造；在当前10个正历史上做1440次四状态评价，与原程序输出的五负行严格一致。

所有56余量有5负、2零、49正；28合行全非负。五负分别是R异索引source、R异索引price、R同索引capacity、Z同索引source、Z同索引price。每个负值在另一索引部分恰好有相反正值；合账抵消正是本源独有的定位结果。

## 怎样复核而不混淆范围

静态复核可在仓库根运行：

```bash
python -B archives/customer-attraction/tools/evidence/diagonal-basic-author-check/selfcheck.py
```

局部数学核查脚本接受 `--repo`、`--threshold`、`--author-report`、`--output` 四个显式路径；将前三者指向本仓库、保存的阈值JSON和 `rerun/stdout.json`，输出另选新目录。它不会运行原入口；但本轮该局部核查已真实执行一次，无需为了重复计数再跑。

若以后确需复放原入口，先用共享 `../combined-branch-master-program/materialize_runtime.py` 创建全新绝对路径目录，再按清单的原研究路径放入本原码和阈值JSON。根 `work.py` 仅作定位标记。必须保持旧依赖路径，使用assert开启的Python；主源不解析 `--verify`，任何调用都会计算并写同目录status。原启动脚本保留的是已结束事件的路径，不能拿它的旧目录重复运行或把旧stdout当新输出。

作者3949行全图可行性、后3945/4005/7931新点、先前73728局部情况/106680矩阵系数完整审计，均是不同材料或既有事件。本轮没有新全图构造、LP、原阈值入口、split入口、SPE求解或重复完整系数审计。当前五负只排这一保存点；不排所有Z重排、固定支持或全游戏域，也不证明一般六人half。
