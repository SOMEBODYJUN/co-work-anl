# Boss3：人口交换八原件恢复与复用

主源8件49951B：[逐件定位/大小/指纹](source-manifest.json)。原件均在[original](original/)，文件名保持不变；双冻结commit保在manifest。本次没有额外claim/done。

完整数学判断、原算法正确性、输入校验范围和当前目标边界见[正式程序页](../../../state/程序/人口交换原证书与全参数严格审计的恢复核验--程序.md)。13/40/q的数学结论已由[既有反例正文](../../../state/反例/两人到三人的严格人口福利下降族--反例.md)自足证明；本次只补原实现/报告身份及完整对照，不重建另一套同内容数学计算。

## 原运行

在全新clone外runtime里复制8原件，原入口各一次，未改源码，均exit0、stderr空，JSON输出与冻结原件逐字节同。

| 入口 | 事件 | 保存输出 | 外部输入 |
|---|---|---|---|
| population_exchange_audit.py | [event](replay/population_exchange_audit/event.json) | [output](replay/population_exchange_audit/output.json) | 同目录13/40的m2/m3四certificate.json；实例重数仍由代码写死 |
| strict_population_family_audit.py | [event](replay/strict_population_family_audit/event.json) | [output](replay/strict_population_family_audit/output.json) | 无；BASE/OFFSET/P2/P3均代码内 |

每次stdout/stderr按原字节另保，event记录实际argv/cwd、依赖指纹、输出指纹和耗时。事件中的stage/runtime为本次真实绝对路径，非未来必须存在的依赖。将original八件复制到一个独立临时目录即可运行两py；它们按__file__定位并覆盖同名JSON，不在original归档目录直接运行。

## 只复用已完成的定义级证据

[旧独立审计](../maximal-population-and-ordered-compression-primary/new-definition-audit/output.json)已充分覆盖13版全部根SPE集合、40版完整严格表以及q族全部78条仿射行；它先误用40表失败、再按q22生成q表成功的两次事件不变。本次未执行旧入口，也没有另写效用/BI/LP计算。

[数据对应脚本](comparison/compare_original_and_definition.py)仅完整解析原件和旧output/input/event，用AST读原q常量，不import原代码。一次exit0，[event](comparison/event.json)、[stdout](comparison/stdout.txt)、[完整对应结果](comparison/output.json)保全：

- 四证书52个有序节点，instance/合法整数动作/完整键集/无重复全部核对。原入口并未读instance，本次不忽略该缺口。
- 13客户全部m2/m3根路径、计数、minW、OPT一致；不谎称旧轮已审此原选定的弱策略。
- 40版26节点全部104个四动作收益与旧独立表一致。
- q版P2/P3完整动作表与全部78条chosen/alpha/beta/q22一致。原阈值18/21和q22最小差4、1/3一致。
- 三个m3完整策略并不相同；所有差异保存。原tiny固定4题且D空，旧正式见证3题，本轮给合法4题解析延伸，没有再跑tiny BI。

未来可运行（仅覆盖comparison输出）`python comparison/compare_original_and_definition.py --repository-root /absolute/path/to/repository`。脚本读取仓内旧充分证据，完整读入依赖的真实SHA记录在output；不需旧程序执行环境。

本轮实际次数：原population1、原strict-q1、只读对应1；新定义效用/BI/LP入口0，无失败尝试。两个原入口自己的集合值BI/仿射IC计算属于原入口实际执行，不混作0。原/旧/新事件各自保身份。

所有结果仅否定人口无条件单调和原行动支持内删人的免费步骤。人数2/3、全部比率大于half，不是当前六人模型的half反例。关系判断见[relation-review](relation-review.json)，逐源receipt在cleanup工作区，不改索引或旧正文。
