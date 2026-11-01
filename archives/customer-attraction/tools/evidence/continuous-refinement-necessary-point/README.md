# 连续精化有理点的完整数据审计

主源 `50795a04991d5196f95f`，正式对象为[连续旧查询精化图的有理可行点](../../../state/计算/连续旧查询精化图的有理可行点--计算.md)。[816661B原件](../continuous-query-refinement-program/related/continuous_refinement_exact.json)共用已保存文件，SHA-256为 `abac45f78980d02f2bd056758a96653aa0bc0d8b87571820a5742397dc490246`。

`audit_point.py` 由前批已归档独立结构审计适配，逐字段、逐列读取12顶层字段及1905列。检查194隐含00、2612交叠上界、六分轨道容量、十二实际旧回复安全报价及三十六实际R/Z报价，并重算O、W、坏差、六实际利润及正权分布。全部使用Fraction，不导入原图或优化器。

`point-audit.json` 另保存原overlap的具体解释边界：165项违反真实交叠Fréchet下界，173项小于共同阈值min。保存列992提供两R边缘均为整块质量而v=0的短见证。该诊断不否定原有限必要图可行，也不否定改写辅助量后的会员实现；正文给出准确量词和证明。

本次执行记录为 `execution.json`、`stdout.txt`、`stderr.txt`，退出0。它只运行当前数据审计。此前唯一原5075图verify事件继续引用[程序事件](../continuous-query-refinement-program/rerun/execution.json)，本任务未重复原CLI、LP或32切面积分。

复现本数据审计可在仓库根运行：

```sh
python3 -I archives/customer-attraction/tools/evidence/continuous-refinement-necessary-point/audit_point.py --source archives/customer-attraction/tools/evidence/continuous-query-refinement-program/related/continuous_refinement_exact.json --output /absolute/new-point-audit.json
```

`source-manifest.json` 绑定主源、共享原件和实际比较证据；`package-check.json` 记录本包SHA、JSON、Python语法、链接及receipt目标检查。当前审计不覆盖其余5075行，不认证连续闭包、精确最优、完整共同目录策略或six-half反例。
