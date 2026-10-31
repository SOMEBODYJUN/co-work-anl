# 配置、固定激活与有限程序的五主源证据

父级确认本批正式claim已pushed b74e98a4ffe5b9b460553510c8acaf32405f8993且synced。五主源共18,335B/283行全文实读；原件SHA、长度和两冻结路线见[source-manifest](source-manifest.json)，[逐节去向](source-section-map.json)35块连续覆盖1..末行，不用程序字段替代阅读。

本批七个正式对象、一个新档README：

- [三项目合并失败的精确验证输入与输出--计算.md](../../../archives/budget-games/state/计算/三项目合并失败的精确验证输入与输出--计算.md)
- [等启用成本的自然预算LP与整数截断缺口--反例.md](../../../archives/configuration-assignment/state/反例/等启用成本的自然预算LP与整数截断缺口--反例.md)
- [隐式配置定价与梯度背景的算法合同--审查.md](../../../archives/configuration-assignment/state/审查/隐式配置定价与梯度背景的算法合同--审查.md)
- [下闭配置指派与最大值覆盖的整数等价--等价.md](../../../archives/configuration-assignment/state/等价/下闭配置指派与最大值覆盖的整数等价--等价.md)
- [给定稀疏配置的确定性预算舍入--算法.md](../../../archives/configuration-assignment/state/算法/给定稀疏配置的确定性预算舍入--算法.md)
- [固定激活背包的类内统一权与拆分障碍--反例.md](../../../archives/contention-resolution/state/反例/固定激活背包的类内统一权与拆分障碍--反例.md)
- [有限双权边际势的自由尺度浮点搜索--计算.md](../../../archives/weighted-congestion/state/计算/有限双权边际势的自由尺度浮点搜索--计算.md)

- [configuration-assignment真实模型入口](../../../archives/configuration-assignment/README.md)。

配置源不能并入BMKP max-min、UM makespan或CAG历史载体。其已知整数覆盖等价、任意成本给定支持半损失舍入、隐式pricing/梯度合同分别保存；新发现原第一轮等成本“任意自然LP点”遗漏floor，新增两bin精确反例及修复后的x/L合同。前批root review仅用一般成本半损失，不受此缺口影响。

两份主源脚本各原字节隔离运行一次，exit0：coNP toy输出与267B主源JSON字节一致；finite grid得到七个网格的完整55,735B数值结果。为固定x反例，另新增支持脚本和报告全文读取，支持脚本隔离运行一次并复现612B冻结输出；支持源只作比较，不额外done，且配对报告现属Boss3领取，本worker无写入。

[runs](run-manifest.json)保每次命令、环境/依赖版本、开始结束/时长、程序/输出SHA和stdout/stderr；[run-analysis](run-analysis.json)保完整有限输出结构及字面二进制float转Fraction后的全部7360约束检查。小正违反、分母猜测和HiGHS success都不升精确可行证书/有限最优/全人数定理。旧finite结果冻结源现属Boss2；本次生成SHA与其库存SHA相同，仍不额外done。

[支持原件](supporting-source-manifest.json)、[实际全文比较范围](comparison-manifest.json)、[阅读日志](reading-log.json)、[结构验证](validation.json)分开记录。外部论文仅保主源的历史版本化报告；本批不声称所有被链论文、探索LP、round2 manifest或代码已读。源码保持原字节，不修通用helper或原浮点算法；正文准确说明trusted输入和缺口。

五条[semantic-receipts](../../../cleanup/workspaces/Boss4/r3-retired-config-certificates/semantic-receipts.json)、[实质自查](../../../cleanup/workspaces/Boss4/r3-retired-config-certificates/semantic-review.md)、[关系证据](../../../cleanup/workspaces/Boss4/r3-retired-config-certificates/relations.json)、[copy-files](../../../cleanup/workspaces/Boss4/r3-retired-config-certificates/copy-files.json)、[下一五候选](../../../cleanup/workspaces/Boss4/r3-retired-config-certificates/next-candidates.json)独立交付。父级串行保存后done；本worker无Git、claim/done或图写入，根总树由Boss衔接。
