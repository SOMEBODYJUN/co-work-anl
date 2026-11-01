# 五个嵌套回复有理切面

主源509c4dd4cf7af167d84c，[2568B原件](original/nested_reply_cuts.json)SHA933a18540d8ea69058cf5e23f999c17b5c69bda7624c817a9e0034fca2f97295。全文五字段、五cut全部稀疏非零权及slack保原序，缺省权为0。[数学对象](../../../state/计算/嵌套回复的有理分离切面--计算.md)解释真IC、两种Y、权重与上包络。

仓库根复核：

```sh
python3 -B archives/customer-attraction/tools/evidence/nested-reply-projection-cut-data/audit_five_cuts.py
```

[新实现](audit_five_cuts.py)不导入原程序、无LP，按S/Z/V含交集式重构120个系数、5760隐藏状态，检查完整L与端点相等；逐六命名索引的30/6条边平均，五slack全精确等原负值。[完整结果](five-cut-definition-audit.json)保每cut16hist贡献、权重、SHA及两local表模板关系。

823005B输入与完整输入域检查共享[程序包](../nested-reply-projection-program/README.md)，不重复扫描或复制大点。原main仅由该任务执行一次6LP；新2494B输出和原件仅source路径不同，[replay-comparison.json](replay-comparison.json)保逐字段及路径替换后的精确字节恢复，不声称原文件字节全同。

五条均未使用middleB/单Y项，容量K系数也全0；G仍包含真实第五位T_i菜单IC。负值只切指定点，未给加cut后重优化结果或全称half。原source绝对路径是历史数据，复现使用包内冻结同SHA点。
