# 正深度付款下界四主源的原件、数据比较与当前回放

对应[正式审查正文](../../../archives/customer-attraction/state/审查/正深度付款下界游戏与冻结证书复核--审查.md)。这包证据只承担四人53单位固定实例的完整SPE/静态鞍点和载体身份，不给一般聚合桥或六人half结论。

## 冻结原件

`primary-source-manifest.json`按实际inventory保存全部两个commit来源、原路径、源ID、大小、SHA-256和当前保全路径。`original/`只有未修改原字节：

| 源ID | 文件 | 字节 |
| --- | --- | ---: |
| d250ec1aefa9ac03e914 | positive_depth_floor_game.json | 1549 |
| e0c5edd8647cbfbf42c0 | positive_depth_floor_certificate.json | 43258 |
| ee9f26f5886df39992b4 | positive_depth_floor_audit.json | 578 |
| acbfe5df47e41383b511 | audit_positive_depth_floor.py | 3533 |

四源已经完整实读，包括43258B内全部400动作和所有其余字段；不是仅凭输出PASS或摘要处置。原报告的18字段完整转写在正式正文。

## 数据身份比较

`comparison-source-manifest.json`与`related-original/`保全四件真实相关原件：canonical game、完整strategy、静态security、literal certificate。复用的原保存位置和实际inventory定位同时保留。它们仅作为related，本批不额外done。

在仓库根运行以下数据检查器：

```sh
python3 tools/evidence/positive-depth-floor-resume-primary/check-input-identity.py
```

它校验全部八件原件SHA、JSON无重复键或浮点值、实际输入类型/合法索引/动作全域，并逐字段比较整个策略对象、客户表及静态有理值，不运行IC、SPE、LP或福利枚举。输出`input-identity.json`以及`reading/all400-actions.txt`和`reading/all-non-action-fields.json`。可逆视图重新组回后与原证书完整JSON结构相同；原行序为先深度、后字典序。

数据比较结果：本cert.strategy与canonical完整JSON策略对象相同；game仅显示名B/P不同；静态p/Q仅有理约分格式不同。literal与本cert除construction_note及14个nice域末位动作外全部字段相同，14差原值完整保留。全文件SHA没有被误称相同。

`comparison-reading-manifest.json`列出本批真正全文读取的正式对象和必要原稿，记录路径、大小和当前SHA。关系解释在正文第5节；没有复制旧图或依赖检索命中作结论。

## 一次当前原入口回放

`replay/`内script/game/certificate是相应冻结原件的字节复制。程序依自身相邻路径读取输入，输出会覆盖相邻audit，因此从未对original内原报告执行它。一次真实执行后保存：

- `execution.json`：真实argv/cwd、解释器3.12.14、optimize0、exit0、时间、耗时和代码/报告SHA；
- `stdout.txt`、`stderr.txt`：本次输出与空错误流；
- `positive_depth_floor_audit.json`：本次生成的578B报告。

本次新报告与冻结原报告逐字节相同，stdout也与新报告逐字节相同。400节点×7=2800项含self偏离均通过；2400非self比较分2219严格、181平局；全部343有序静态三竞争背景通过精确匹配。实际利润、W/OPT、v4和所有差额见原报告及正式正文。

这是对未修改原实现的一次当前执行，不是另一份独立数学实现。原578B报告本身没有旧运行环境信息，本包没有把本次环境回填为旧环境。原入口没有main guard，import也会执行并覆盖输出；所有数学断言依赖非优化模式。可在独立可写副本中重放，保持相邻文件名；无需项目solver或外部库。

本批不重跑literal审计、一般提升证明或其它旧审计；完整53单位数学与静态域的已有对象得到真实数据身份对应。本包的有限成功不排除别的完整策略、目录或人数上的一般聚合障碍。
