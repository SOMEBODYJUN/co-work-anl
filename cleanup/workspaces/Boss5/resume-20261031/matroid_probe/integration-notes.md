# Boss5串行整合交接

唯一认领源：`6ff9aa13dbf15bfbd72c`。本工作区只写草稿与证据，未改正式正文，未做Git写入、claim、checkpoint或done。

## 正式目标与映射

将 `semantic-draft.md` 作为完整正文写入：

`archives/matroid-structures/state/计算/五元以内拟阵公共基交换距离核验--计算.md`

保全四份证据，映射如下（正式目录已有，无需另建模型存档）：

| 本工作区文件 | 正式路径 |
|---|---|
| `evidence/matroid_exchange_diameter_independent.py` | `archives/matroid-structures/tools/evidence/retired-topic-selection-20261031/matroid_exchange_diameter_independent.py` |
| `evidence/matroid_exchange_diameter_independent_rerun.json` | `archives/matroid-structures/tools/evidence/retired-topic-selection-20261031/matroid_exchange_diameter_independent_rerun.json` |
| `evidence/independent_semantics_check.py` | `archives/matroid-structures/tools/evidence/retired-topic-selection-20261031/matroid_exchange_semantics_check.py` |
| `evidence/independent_semantics_check.json` | `archives/matroid-structures/tools/evidence/retired-topic-selection-20261031/matroid_exchange_semantics_check.json` |

独立脚本以祖先目录中的 `cleanup/OBJECTS.md` 找库根；源、rerun使用相邻文件，冻结结果保留原路径。默认新输出与脚本同名、扩展名改为 `.json`，所以按表重命名复制后可直接复现。输出使用独占创建，已有证据不覆盖。源程序5,412字节证据保持原样。

## fair-allocation两处准确替换

目标：`archives/fair-allocation/state/审查/退役三值家务FPO与拟阵交换结果三源复现--审查.md` 的第3节。无需改冻结JSON。

第一处，旧句：

> 来源 ID `4a4127c9a96303599be0`，大小 4,465 字节，SHA-256 `5a2549b3607a18588ad55940fa2e7d920f827f409c542e2f3d5ed84fe3a99c33`。JSON 明示 integer bitsets、无浮点、穷举，`max_n=5`。总计：498 个 labelled matroids、28,424 个 profiles、18,833 个 distinct exchange graphs、242,976 个 reachable basis pairs，全部 finite cases passed。

替换为：

> 来源 ID `4a4127c9a96303599be0`，大小 4,465 字节，SHA-256 `5a2549b3607a18588ad55940fa2e7d920f827f409c542e2f3d5ed84fe3a99c33`。JSON 明示 integer bitsets、无浮点、穷举，`max_n=5`。总计：498 个带标号抽象拟阵、28,424 个非空基支持、18,833 个按每个拟阵分别去重的交换有向图、242,976 个可达的不同地面元素有序对，全部 finite cases passed。图的顶点是地面元素，计数不指基对；支持重复产生同一图时只检查一次，不同拟阵产生同一图时仍分别计数。源码机制、独立交叉核验与复现见[五元以内拟阵公共基交换距离核验](../../../matroid-structures/state/计算/五元以内拟阵公共基交换距离核验--计算.md)。

第二处，旧句：

> strata 给出 n≤5、各 rank 的 matroid/profile/graph/pair 数。最长 witness 按 girth 分四类：

替换为：

> strata 给出 `n≤5`、各 rank 的 matroid/profile/graph/pair 数。`longest_witnesses` 的键为 `δ=rank−girth`，按这个差值分四类；每类保留一个达到该类有限最大距离的见证，未列全部达到者：

现有随后的四个项目数值均正确，无需改动。其“-1/0/1/2”是δ标签，不是girth。

## 现有matroid资料对象的准确增量

可在 `archives/matroid-structures/state/资料/交换距离与等长theta相关间隙的独立接口--资料.md` 第一节中“原全小抽象拟阵审计和GF(2)独立审计覆盖域不同，均不是全部拟阵证明替代。”之后增加：

> 抽象拟阵审计的源码、精确覆盖域和独立集/Floyd复现另见[五元以内拟阵公共基交换距离核验](../计算/五元以内拟阵公共基交换距离核验--计算.md)。其中28,424个profiles指非空基支持，18,833个图按拟阵内部去重，242,976个端点检查指图上的不同地面元素有序对，不能读成基对；结果键为 `δ=rank−girth`。

若Boss串行整合正文，无需改一般距离候选的量词、状态或PoA段落。README可增加本计算对象的入口。关系仅为来源/实现/有限验证/术语更正，不将有限审计变成一般证明。

## 已运行核验

原样运行：`python3 evidence/matroid_exchange_diameter_independent.py --max-n 5 --output evidence/matroid_exchange_diameter_independent_rerun.json`。

交叉核验：`python3 evidence/independent_semantics_check.py`。

前者四总数498/28424/18833/242976，和冻结JSON逐字段及字节SHA一致；后者对2,229个候选族以独立集增广对照基交换，逐图Floyd对照465,492个BFS距离条目，全部通过。没有重跑外部文献检索；一般组合证明仅为相关已读候选，不因运行升级。无缺源依赖。
