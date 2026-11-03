# 早期机会计数与价格交替：完整保存证据

对应[正式计算对象](../../../state/计算/早期机会计数与价格交替样本--计算.md)。五主源均经`work.py clean show ID`完整取得，原size、SHA256、blob、两个冻结来源和实际归档路径在[manifest.json](manifest.json)。JSON以确定性gzip保存，解压逐字节等于冻结源；压缩不删字段或动作。程序原件不改导入路径。

| 源ID | 原文件 | 原字节数 | 保存记录 |
|---|---|---:|---:|
| 58bfc248ddc2d0abee5a | count_m5k6.json | 3570381 | 100 |
| ecbe744c2db70e4e73a8 | count_m7k7.json | 29761031 | 95 |
| 25a236da78c9e5356f6c | price_alternating.py | 2309 | 程序 |
| e4050b94e166805f313d | price_m5k7.json | 6070283 | 100 |
| cd59a8a92f99832a3bba | strong_count_m5k6.json | 3568705 | 100 |

`related/`完整保留已读依赖`count_policy_attack.py`（源ID10955b59b31ac70b0664）、原九输入审计`scope_audit.py`（5554201fc7e7d2752cf5）及目录README（d25e74338c5333894669）。它们是比较依赖，不在本五源回执中重复done。原发现器依赖NumPy/SciPy及原research相对目录，本文没有运行其main、原LP、BI、RNG或旧九文件main。

新标准库程序[audit_saved_tables.py](audit_saved_tables.py)读取所有四JSON、递归遍历全部字段，核完整计数键集并重放每个真实分支，以整数缩放逐表精确核IC；结果是[saved-table-audit.json](saved-table-audit.json)，保395条在两种输入下的全部资格、质量和/收益归一误差、目标重算、负IC条数和最差具体偏离见证。输入合同是`Fraction(str(v))`与再`limit_denominator(10^6)`两种，均不冒充原二进浮点solver完整向量。

实际执行一次：

```sh
python3 archives/customer-attraction/tools/evidence/boss5-early-prices/audit_saved_tables.py
```

退出0。每种输入执行238020计数状态/1386120非自身IC，逻辑涵盖13630515个有序决策历史；分别146/323表通过。源码的minimum以自身恒等零为基线，执行次数仅数非自身比较。失败表完整保留，未把逐坐标恢复当可行性保持操作。重运行该命令只复核固定保存输入，不调用优化器；输出也不认证任何LP精确最优值、固定锥上界、一般逐人候选或六人half。

原件源SHA按manifest可核：`gzip.decompress`所得字节的SHA256须相同。`saved-table-audit.json`每文件另含解压SHA和整树类型/字段计数，便于发现尾部、动作或质量被截断。正文准确交代95/100保存前缀、strong系数4、价格局部best与成熟大块家族的边界。

收尾复核见[final-review.json](final-review.json)：再核五主源原哈希、所有JSON字段及逐表报告汇总、正文链接、计数资格逻辑和具名端点算术；未再运行IC大审计或原发现器。五源最终语义处置在[cleanup-receipts.json](cleanup-receipts.json)，由协调方在正文已推送后统一登记；回执不代替数学证明。
