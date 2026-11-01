# 固定背景收益切片审计表证据

主源c3bd87a3e8bc0d0b312e为38584B冻结JSON，SHA-256 f01662cb7c19ebd5725e8fd2b25d3d57bd8fec0668dccb855c2bc2dcec47db1b。完整数学解释见[数据正文](../../../state/计算/固定背景收益切片的有限秩与核基审计--计算.md)，一般解析证明见[固定背景回路定理](../../../state/定理/固定背景双主题收益切片的完整有理回路--定理.md)。

- [原表](original/fixed_background_audit.json)原字节保全；14个顶层字段、96基础/77聚合/14全单位记录，另165四槽和8六收益参数计数。
- [原审计程序](../fixed-background-circuit-audit-program/original/audit_fixed_background.py)与[数学原稿](../fixed-background-circuit-basis/original/fixed_background_circuit_basis.md)均全文实读；原件共享，不在此重复复制。
- [原main事件](../fixed-background-circuit-audit-program/replay/execution.json)、[外层记录](../fixed-background-circuit-audit-program/replay/process-capture.json)、[被动profile包装](../fixed-background-circuit-audit-program/replay_main.py)保唯一一次原函数运行，无替换helper。原main含旁观6.786694247秒，进程墙钟6.969239209秒，exit 0，断言开启。
- [重生表](../fixed-background-circuit-audit-program/replay/fixed_background_audit.json)与原表逐字相同；[旁观汇总](../fixed-background-circuit-audit-program/replay/observation-summary.json)与[完整捕获](../fixed-background-circuit-audit-program/replay/original-observations.json.gz)来自该同次原运行，不是另一次独立实现或旧JSON自带字段。
- [后续独审代码](../fixed-background-circuit-basis/related/check_fixed_background_rank.py)、[独审冻结表](../fixed-background-circuit-basis/related/fixed_background_rank_review.json)与[解析审查](../fixed-background-circuit-basis/related/fixed_background_rank_review.md)另有152基础/90聚合/8全单位、270四槽和406基向量，省略全零客户列；本包只读不重跑。
- [原目录README](../fixed-policy-circuit-flow/original/common_customer_README.md)保一般半覆盖未解、还需真实策略图中支付控制的范围。
- [来源清单](source-manifest.json)保存7份全文实读来源的冻结身份；[阅读比较记录](review-record.json)绑定真实比较对象和共享事件。
- [静态字段检查](schema-review.json)与[自查程序](check_package.py)只检查已有表字段、序列、捕获形状、Fraction字符串、字节和链接。自查结果另保存为self-check.json，不重新计算秩、核基、客户收益或任何SPE。

可从仓根执行python3 -I -B archives/customer-attraction/tools/evidence/fixed-background-circuit-audit-data/check_package.py，只刷新schema-review.json与self-check.json。没有导入任何数学源程序；原main、rank、基生成、LP与SPE新调用均为0。

完整基只相对于指定收益行族的全部形式客户列；它不表示枚举全部最小支撑回路，也不认证某个非负客户实例、共同完整策略或福利下界。全部有限计数不能替代任意背景和任意M的Cauchy/留数/根计数证明。
