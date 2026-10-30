# 四份规范有理输入

本目录保存[四份输入与实际分支对象](../../../state/计算/四份回归输入与实际覆盖分支--计算.md)对应的完整JSON；它们原来位于 examples/multi_facility，均来自固定提交68fad804ec5946cb296f77dc5b336308a66abf12。

| 文件 | 来源ID | 原字节数 |
| --- | --- | ---: |
| growing-k-12.json | 16fd117d9d48831d4259 | 264 |
| heavy-three-sites.json | 0ce56760ec06047ba48c | 263 |
| orphan-overlap.json | e42f4bde538ceec88c95 | 352 |
| rational.json | f1ccb9efbe1ed5309542 | 351 |

四源共1230字节，原字节未改。[input_comparison.json](input_comparison.json)保存逐文件SHA-256、对应证书hash及全部输入与证书instance/冻结exact报告相等的实际比较结果，并列出所比较的历史布局、站点分配、排序收益、实际倍率及偏离记录数。

输入只含m、k、clients及每客户weight/sites；不含策略、NE证书或续局。weight为字符串，普通构造入口用Fraction精确解析。目录只是资源，不自行执行任何算法。

本批没有重跑构造器或均衡审计。可用[固定19文件重建入口](../factor-two-audit-suite/README.md)恢复默认lexmax CLI及这些输入的完整相对路径依赖，再在重建根目录运行，例如：

~~~sh
python3 -m multi_facility_spe examples/multi_facility/rational.json --output /tmp/facility_rational_fresh.json
~~~

输出须选不存在的新路径。此命令是复现方法，并非本批执行日志。新输入的实际验证范围与历史证书的具体数学差异均见正文；文件名不自动说明某个算法分支已被覆盖。对应四份证书在本批仅作相关比较材料，不替它们的清点来源申报done。
