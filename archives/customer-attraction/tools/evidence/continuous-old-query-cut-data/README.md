# 64个有理旧查询cut的完整数据及三点核验

主源0e0463f4cf45c16d0c84的[15013B原件](original/continuous_old_query_cuts.json)保全部五字段、64八元组及精确负余量。两冻结提交同SHA e9ce9c66ea5598038ad7f5aa19cfab44d5156c8e35b3081665481153a968c4fa。

[数学正文](../../../state/计算/旧查询回复的六十四个有理分离切面--计算.md)说明适用模型、量词、非负参数、隐含后继最小化、轨道重数、发现范围与重复方向。后续[32条列表](related/continuous_refinement_cuts.json)只作跨版本比较，不在本源回执冒称该源done。

仓库根运行：

```sh
python3 archives/customer-attraction/tools/evidence/continuous-old-query-cut-data/audit_cuts.py
```

[audit_cuts.py](audit_cuts.py)不导入旧生成器、不求LP，从数学计数投影积分全部64行，在4971旧点、5108联合点及换Z的pair点各重算一次；实际退出0，[全部结果](three-stage-cut-audit.json)保每条三点精确余量及全输入SHA。旧点64负且逐一匹配原保存值，联合点5零59正，pair点3零61正。不是全旧5108行在新Z处复核。

旧815911B点共享[代码来源证据](../continuous-old-query-cuts-program/related/all_reply_query_cuts_exact.json)；联合点和pair点共享此前已推原件。一次原180LP发现重放及121920列系数独立核由[代码包](../continuous-old-query-cuts-program/README.md)保存，本数据任务不重复运行。未声称连续族闭包、最优值或完整SPE。
