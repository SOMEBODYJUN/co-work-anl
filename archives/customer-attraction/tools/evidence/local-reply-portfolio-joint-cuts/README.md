# 嵌套回复、同源再查询与末位组合联合切面

主源 `80444e2ea783541f539e`，6533B，SHA256 `49aaf81f49aac3b544cf38ed97efdb6fa1849e1c810ff1705b7dd313052017a1`；两冻结提交68fad804…及aefc58ea…同字节。[完整正文](../../../state/计算/嵌套回复再查询与末位组合的联合切面--计算.md)保存三族18个模板的全部参数、真实策略身份、预算与推导。

| 文件 | 职责 |
|---|---|
| [original/joint_local_v2_cuts.json](original/joint_local_v2_cuts.json) | 未改原件；nested5、requery5、portfolio8；只有nested附历史slack。 |
| [audit_joint_cuts.py](audit_joint_cuts.py) | 本次独立字面requery/portfolio、具名索引平均及原AST row比较；不跑LP或完整程序入口。 |
| [exact-audit.json](exact-audit.json) | 一次独立审计的完整输出：全部18行SHA/余量/16hist贡献、基表和旧portfolio比较、全部输入SHA。 |
| [audit-execution.json](audit-execution.json) | 本次实际命令及工具观察退出结果；不伪装成原作者发现事件。 |
| [manifest.json](manifest.json) | 原件来源、共享实际依赖、阅读范围、运行分工与归档指纹。 |
| [self-check.json](self-check.json) | 正式文件SHA、JSON/Python语法、参数表、相对链接和回执目标检查。 |

本次仅新增一次独立数据审计。新P族1536个全actual二元域比较，缓存后12800次字面隐藏位求值，与原人数压缩及13/16零补齐相同。新R族24个唯一局部最小值、384个四隐藏位状态。N族完整继承上轮120系数/5760状态的独立定义核，未重新枚举其菜单；本次原nested row函数使用这个已核缓存，只比较行组装。全部18×1905=34290系数相同，18向量互异但不声称线性独立；代入共享5180点全部严格负。

现表与旧3121B基表逐字典及有理规范化键比较后，确认为旧nested5与requery4保持原序，新增requery第五条和portfolio8。旧29容量portfolio与旧8零容量portfolio均无与本8完全相同的模板。模板身份与行锥关系分开，未证明新增约束独立。

原嵌套发现器上轮唯一运行和定义级核验分别见[程序包](../nested-reply-projection-program/README.md)与[数据包](../nested-reply-projection-cut-data/README.md)。原再查询默认24LP由[程序任务](../early-reply-requery-program/README.md)本轮唯一执行；按完整模板匹配其5slack与当前独立重建全同，排序不同保留。本包新增原入口次数0，无5198全图构建、客户重优化或384查询搜索。

本次实际运行路径是clone外，保在audit-execution.json及exact-audit.json输入表。归档不改写这段历史路径；manifest提供它们的持久同SHA替代位置。程序需要四个显式路径，可在新的未占用输出路径上重放独立审计：

```sh
python -B archives/customer-attraction/tools/evidence/local-reply-portfolio-joint-cuts/audit_joint_cuts.py \
  /absolute/repo-root \
  /absolute/new-output.json \
  /absolute/repo-root/archives/customer-attraction/tools/evidence/local-reply-portfolio-joint-cuts/original/joint_local_v2_cuts.json \
  /absolute/repo-root/archives/customer-attraction/tools/evidence/early-reply-requery-program/replay/report.json
```

它拒绝覆盖已有审计报告以免静默重复；需要保留已共享的nested原点、独立结果、输入接口记录及三族原码。AST仅取指定纯函数作为被测端，未执行原顶层导入/发现/求解入口。输入全前后SHA不变。新P/R负值是当前诊断，原6533B表并未保存这些字段；其缺失发现历史不由重构补造。

空主题、重复选择、零客户、全历史弱平局与同一策略身份由解析证明保全。固定点被分离不等于后继系统无解、完整SPE反例或六人half。三族方向须区分：nested是非负真行的max上包络，requery/portfolio是预算右侧的min隐藏回复投影。
