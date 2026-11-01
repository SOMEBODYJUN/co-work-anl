# 联合必要图原点的独立读取与精确审计

主源5e6ada29cce2eeda7f9e的816453B原件共用[已保存冻结文件](../full156-tail-parent-report/original/research_5/combined_branch_master_exact.json)，未修改、未再次复制。SHA为d1aeba67e20c8d8fc7ff38cd6566ac05c3771731f586584e5c6f1dfe233472a8。

[完整数学说明](../../../state/计算/索引主题与实际B分支的联合必要图有理点--计算.md)解释所有字段、轨道重数、R/Z历史、隐含00和后续Z重排边界。

从仓库根复现：

```sh
python3 archives/customer-attraction/tools/evidence/combined-branch-master-point/audit_point.py
```

[audit_point.py](audit_point.py)使用标准库Fraction读取全部1905条数据，不调用旧生成器或求解器，写出[current-point-audit.json](current-point-audit.json)。当前执行退出0，全部结构、194隐含00、2612交叠上界、六拆分R/Z容量、12实际B/C报价及归一化/福利通过。报告保原11字段（columns另由共享原件完整保存）、16行完整hist、六实际利润及全部18条聚合余量。

这不是全部5108行原入口重跑；更不证明精确最优值或完整历史SPE。原作者verified_rows/minimum_slack保报告身份。后继pair点改变Z，不能将本核验搬到新Z。无求解输出或随机种子被伪造为原作者运行。
