# 四份显式续局证书及直接检查

本目录服务于[四份证书对象](../../../state/计算/四份保存证书的显式续局与默认补全--计算.md)。四个原JSON共34266字节，完整来源ID、原路径和SHA-256见[certificate_sources.json](certificate_sources.json)，全部来自固定提交68fad804ec5946cb296f77dc5b336308a66abf12，原字节未修改。

| 原JSON | 实际偏离条数 | 本批检查的实际倍率 |
| --- | ---: | --- |
| growing-k-12.json | 24 | 1 |
| heavy-three-sites.json | 10 | 1 |
| orphan-overlap.json | 6 | 1 |
| rational.json | 8 | 65/63 |

本批已实际运行[check_saved_certificates.py](check_saved_certificates.py)，结果保存在[certificate_checks.json](certificate_checks.json)。它调用已保留、hash核对过的[原定义检查器](../factor-two-reverse-review/definition_check.py)，只对四在轨NE和48个显式偏离纯NE作精确原子条件成本检查；另核布局/分配/概率字段、全部终态负载、源目标元数据、40次重原子独占及普通设施帽。

脚本没有运行构造器、全局字典序枚举、未列子博弈穷举或实际默认续局求值；原记录的13步改善及124个初始静止箱没有轨迹可供本批重放。输出逐条标明已核量和仅保留的原统计。完整默认续局的数学依据及531740个未列布局的范围在正文说明。

从结果仓库根，选一个尚不存在的输出路径：

~~~sh
python3 archives/facility-games/subarchives/common-many/tools/evidence/factor-two-saved-certificates/check_saved_certificates.py --output /tmp/facility_certificate_checks_fresh.json
~~~

使用普通Python3.10以上模式，勿以 -O 关闭断言。脚本拒绝覆盖已有输出，并核对相邻目录的固定定义检查器hash。此依赖已作为先前清洗资源保存；无需导入构造器或额外包。

若需真正运行完整续局求值器或原构造/交付套件，已有[19文件核心快照重建入口](../factor-two-audit-suite/README.md)恢复原相对路径。那是另外的执行范围，不能把本目录52项直接NE检查称为完整delivery重跑。
