# weighted-replay-entry 单源交付

认领提交 `aa3a89ff50291360dc1f905a1bf02cce54edcc58`；源 `ec418e2e53786e720520`，`tests/audits/weighted_congestion/replay.py`，4626字节，已完整实读/理解/比较。新增正式对象：

`archives/weighted-congestion/state/计算/历史加权拥塞审计的隔离重放入口--计算.md`

原码和完整历史注册表保存在 `archives/weighted-congestion/tools/evidence/weighted-replay-entry/original/` canonical原层级；`provenance.json`保两源各完整冻结commit/path/hash。fb658注册表194010字节只作比较依赖，不在本单源重复claim/done。源接口只使用classification/path，不读取表中历史source_files/branch版本来锁定数学。

实际必要核验仅未改原源码`--help`和`--list`各一次、exit0、stderr空；无数学审计子程序、无Git命令、未测试normal execute。47行list逐行精确匹配实际注册表；CLI命令、cwd、完整stdout/stderr/hash分别保存，`cli-manifest.json`说明核验范围。原入口正常execute会临时Git init/空commit且需要全部164个有path文件，本批不启动该分支、不重复已通过旧数学审计。

全部170条classification逐条解析、164条有path、6条无path、47条.py、50条evidence；无规范path别名碰撞。历史声明SHA与冻结inventory完整逐path比对，99同、65不同且全.md；47源码和50evidence均匹配。这只是元数据比较，不假称复审/执行164份数学来源。完整逐条结果在classification-review.json，原注册表未改。正文保留报告尾部截断12000/4000字符、缺件/超时异常、局部证据hash保全、两特例、目录恢复保持数学数据的条件，以及旧全类OPEN已被p/10全状态族否定的当前状态。

语义回执：`cleanup/workspaces/Boss4/weighted-replay-entry-next/semantic-receipts.json`。本代理未做Git/claim/checkpoint/done。下一批按Boss建议只接fb658 INTEGRATION主源，等待Boss正式claim后再做其独立完整处置，不现在领取其他来源。
