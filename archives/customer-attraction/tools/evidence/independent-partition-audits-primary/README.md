# 最优分区冻结查询的独立原审计

自足程序对象：[最优分区冻结查询的独立原审计与双规模版本合同](../../../state/程序/最优分区冻结查询的独立原审计与双规模版本合同--程序.md)。它补旧反例页当时缺失的4684B独立原码、2811B大报告和2777B小报告，不重授发现，不重done已经清洗的作者输入或原review。

- `original/`保持三主源全部10272B原字节；`source-manifest.json`从冻结inventory绑定两commit/path/blob/size/SHA，另列全文实际比较的16文件。比较文件仅作已存在的依赖，不另申报主源完成。
- `replay_independent_fixed_inputs.py`只做新执行的隔离布局、记录与打包比较；原数学入口是未修改的`independent_partition_audit.py`。本次在clone外新目录执行默认14客户、`--large`127客户各一次，原作者exact审计/旧定义checker/发现器0次，LP0、canonical0。
- `replay/14/`和`replay/127/`各保真实execution-record、stdout、stderr及排他新建的generated-report。Python3.12.14、`-I -B`、assert开启，均exit0/stderr0；源和输入前后SHA未变。
- `replay-comparison.json`逐字段保存关键版本差异。小报告2777B逐字节同冻结；大报告2813B与冻结2811B仅`minimum_partition_excess_over_W`的JSON类型不同：历史数字9、当前字符串`"9"`，数值相同。当前`--large`另写`independent_partition_large_audit.json`，历史源名是`independent_partition_audit.json`；不推断旧argv或旧修改时序。
- `comparison-review.json`区分原码独立实现、同源输入、现有数学反例、52客户静态证书和有限阴性搜索；关系判断写入正式正文，第三阶段不造边。
- `repository-related-search.txt`是实际全仓关键词检索。命中不冒充全文阅读；全文阅读范围另记在manifest和comparison-review。
- `package-check.json`为只读封包自查：主源完整SHA、链接、JSON解析和运行记录一致性。它不新运行数学入口，不取代正文证明。

原独立程序只读客户类型和完整策略，按定义重算七个有序节点42比较、36个有序含重复比较组合、两最优顺序各两匹配的全部分区最小值。14点四项R均9>W8，127点均80>W71；half余量分别6、54。两主报告的所有payoff_rows及partition_minima均保全，并与作者输入的完整存储结果作包级比较。

程序不是通用输入验证器或全SPE枚举器；两固定合法输入完整策略通过，不证明一般六人half、客户数最小性、外部审稿或新增盲审。旧报告不含历史进程身份，本次新事件不倒填历史。请勿为封包重复运行；若未来确有新版本/新输入，使用新stage及新证据目录，保现有排他写入记录。
