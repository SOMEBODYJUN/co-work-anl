# 增加合法背景后最坏纯续局剩余利润上升

正式对象：[R51背景剩余利润非单调证书](../../../state/反例/R51背景剩余利润非单调证书--反例.md)。

主源 `e721cbff6868a74c7d64` 的1142字节JSON在`background_nonmonotone.json`原样保全。八兴趣类型共18名单位客户；固定余两人，合法过去从(0)改为(0,3)，总人数3改4，最小剩余利润9升11。两个终局计数都包含过去，非剩余行动计数；指标是剩余两人总利润，非完整覆盖或单人阈值。

`original/probe_background.py`是已全文读过的相关冻结生成器，2551字节未改。这里没有替该相关来源办理done。其`check`重建两种总人数并用规范纯SPE终局全集最小化剩余利润；`minimize`才产生与主JSON相同的返回格式。实际默认CLI、`minimize`、保存点`check`由本批另一任务记录于[生成器复现目录](../R51-background-probe/replay/replay-summary.json)，其中[minimize输出](../R51-background-probe/replay/minimize.stdout.txt)与本主源逐字节相同。当前复现不补造历史命令。

`verify_independent.py`是本任务新增的标准库Fraction实现。它不导入规范包或原生成器，不使用计数集合递归；直接展开18名客户，对每背景枚举全部4^5=1024份完整两人纯策略：一个首位动作和四个可能首动作后的末位回复。每个末节点须为真实最佳回复，首位须对其所用完整回复表最优。它保留所有平局，精确得到原背景三份SPE、新背景一份SPE，以及原JSON中的两个最小利润/计数见证。

复现命令（仓库根）：

```sh
python3 archives/customer-attraction/tools/evidence/R51-background-nonmonotone/verify_independent.py > archives/customer-attraction/tools/evidence/R51-background-nonmonotone/independent-replay.json
```

当前输出由该命令实际产生，exit0。输出保存全部32个有序终局的收益、两个背景全部四份完整子SPE及两张选定最小策略；各最小策略有五个决策节点，全部离轨节点已由穷尽条件核验。两背景全部SPE总覆盖都18；固定同一后缀的16项剩余利润均不升，所否定的是在改变后的可信策略集合上取最小值仍不升。

它不检查过去提供者的空根理性，未声称背景是某根SPE实际前缀；不研究混合SPE、最大单例阈值、静态混合查询值、六人实例、一般half或最少客户数。无随机发现、优化器、网络、盲审或外审。`manifest.json`列主源、相关读取、输出指纹和当前执行边界；`relations.json`记录逐项数学关系，正式图留第三阶段。

已实读比较：共同目录完整历史定义、终局全集算法、固定背景两人税界、合法背景纯/混合续局利润反例、52客户实际前缀反例。另全文读本批`background_welfare_nonmonotone.json`和`probe_monotone_welfare.py`作指标区分；其13客户/13→12覆盖下降不能替换本18客户/9→11利润上升。对应[福利对象](../../../state/反例/R51背景福利非单调证书--反例.md)单独处置其主源。
