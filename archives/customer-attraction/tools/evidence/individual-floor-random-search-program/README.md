# 三人六主题固定策略的逐人覆盖比探针证据

主源`75e5e8d6444d274ec58d`为1385字节`individual_floor_search.py`，实际是固定`group_policy(6,3)`的一次确定性浮点LP循环，没有RNG或seed。目录名`individual-floor-random-search-program`仅保留既定路径。自足数学合同见[正式正文](../../../state/程序/三人六主题固定策略的逐人覆盖比线性探针--程序.md)。

| 文件 | 身份 |
|---|---|
| [original/individual_floor_search.py](original/individual_floor_search.py) | 完整冻结源，不改写 |
| [source-manifest.json](source-manifest.json) | 主源、原锥辅助模块、四个规范模块及原README的7份完整原文身份；相关源不代办done |
| [replay_once.py](replay_once.py) | 本轮实际用过的仓外一次性观察脚本，字节保留；硬编码原工作路径，不是通用CLI |
| [replay/execution.json](replay/execution.json) | 原顶层调用、6输入前后SHA、版本、函数次数、事件范围 |
| [replay/process-capture.json](replay/process-capture.json) | 外层`python3 -I -B`实际argv、退出码及墙钟 |
| [replay/stdout.txt](replay/stdout.txt)、[replay/stderr.txt](replay/stderr.txt) | 原3行输出147字节，stderr为0字节 |
| [replay/original-model.json](replay/original-model.json) | 原构造43动作、259历史终局查询、185×63有理行及浮点矩阵，348330字节 |
| [replay/original-lp-results.json.gz](replay/original-lp-results.json.gz) | 123份原完整OptimizeResult及目标/归一化行；94642字节，解压1060816字节 |
| [replay/capture-summary.json](replay/capture-summary.json) | 仅整理同一次原返回的状态及三项best，不新增求解 |
| [review-record.json](review-record.json) | 实读比较、未覆盖分支及成熟结果复用边界 |
| [check_package.py](check_package.py)、[self-check.json](self-check.json) | 静态身份、JSON结构、支持枚举顺序、已存模型形状和链接检查；0数学重跑 |

唯一新增数学入口在2026-11-01完成：`runpy.run_path`调用原顶层一次，`sys.setprofile`只观察原函数返回值和现成模型，不替换函数、不更改输入。123次原LP全部`success=True,status=0`，外层exit0、2.072814641011064秒。未调用BI、规范证书、整数克隆、独立IC核验、精确顶点/对偶恢复，没有另求LP。六份输入前后SHA相同。

原三项输出依次为`4.205623901581722 / (1,2,5)`、`4.125 / (1,2,4)`、`4.714285714285714 / (1,2,4)`，玩家编号0、1、2分别对应实际标签0、3、4。这是本轮观察，不冒充未保存的历史stdout；浮点状态与原浮点边际都不等于精确最优证书。三个玩家分别归一化，返回点不必相同。

原返回的无穷上界残差按观察脚本的Python `json.dumps`默认行为保存为`Infinity`，共123×63=7749项，全部位于`result.upper.residual`。因此压缩内容使用Python JSON允许的非有限数扩展，严格RFC JSON读取器须先处理该标记；它表示变量没有有限上界，不是目标值无界或求解失败。没有NaN或其他位置的无穷值。本包不改写原事件字节以迁就另一解析器。

`replay_once.py`先建全新runtime/replay目录，在原目录深度放入完整源文件，再从已保原件复制辅助模块和规范模块。正式包保留原事件路径字符串作为历史事实，不把它们改成新argv。若以后确需复现，须在新的工作目录准备相同输入及导入深度，明确记录新事件；不要原地重跑这份一次性脚本，也不要以封包检查名义触发原入口。

原辅助模块共享[customer_attraction_strategy_lp.py](../strategy-cones/original/tests/audits/customer_attraction_strategy_lp.py)，四规范输入共享[可信填充程序依赖](../credible-padding-program/README.md)，原背景记录共享[global_proof/README.md](../global-floor-research-entry/original/README.md)。其精确建模能力不意味着本源调用了辅助模块的有理认证方法。[固定锥定理](../../../state/定理/固定完整策略的客户重数锥--定理.md)证明建模合同；[银行反族](../../../state/反例/笛卡尔银行目录的逐人分数门槛反族--反例.md)提供后来全称逐人门槛的真实SPE纠正。两种证据没有混并。

静态检查命令是`python3 -I -B archives/customer-attraction/tools/evidence/individual-floor-random-search-program/check_package.py`，只读已存结果并重写本包`self-check.json`，不导入原源、辅助模块或SciPy。当前没有任何有理最优值或本策略整数反例交付。
