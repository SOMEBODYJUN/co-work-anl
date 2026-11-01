# 完整156主题福利矩：共享原件与独立客户重建

正式正文：[完整156主题固定前缀的福利矩数据](../../../state/计算/完整156主题固定前缀的福利矩数据--计算.md)。本目录处理主源`303cdd613c09a5fa5f7c`，相关大原件复用已保全文件，不重复持久1.7MB福利矩。

## 文件与执行

- [冻结福利矩](../full156-tail-parent-report/original/research_5/full156_tail2_welfare_10344.json)：1685067B，SHA256 `fe8fb09f7527f8f4cd26ad67f6e43be5bc84cb5d9c47fea39fd0661bab0e5256`。
- `verify_welfare_atoms.py`：本轮新增标准库实现，不导入或执行原生成器；从全部六索引排列和slab端点构成整数客户类型，再直接累计未覆盖人数。
- `welfare-audit.json`：全部24336格检查、1590类型摘要、10hist明细、156行摘要、所有九字段身份及固定范围结论。
- `source_manifest.json`：主源与四个必要来源的指纹、路由、阅读范围和未认证事项。

在仓库根运行：

```sh
python3 archives/customer-attraction/tools/evidence/full156-welfare-kernel-data/verify_welfare_atoms.py
```

脚本需要共享`full156-tail-parent-report/original/research_5/`下的point、kernel、welfare，及`full156-pair-master-point/original/pair_master_exact.json`；先核四件原字节SHA。不会覆盖它们，也不输出第二份大矩。

## 独立重构的完整性

原生成器使用至多四个命名索引的矩缓存；新实现全枚举每个hist的六索引不同词排列，按pair提供的每个R固定slab及所有Z阈值切成正质量小区间。每个小区间乘原尺度、除排列数均为整数，得到1590个不同156位客户类型，总人数等于尺度S。全部156主题覆盖不同。

固定前四覆盖的客户直接计入总福利；对其余客户，只有两个尾主题均不覆盖时才扣除。因此整数覆盖式重建全部156²格。报告逐行保存最小/最大整数福利、half计数和用逗号连接156个十进制整数得到的SHA，以便定位差异；原始完整矩仍是共享冻结文件。

类型摘要格式为`json.dumps([[hex(mask),str(multiplicity)] for mask,multiplicity in sorted(atoms.items())],separators=(',',':'))`的UTF-8字节。SHA为`87d207363bf7e9401b47c7a8be10cb8e7b23227fcd0a8cfbd2198893c21abccd`；它与同批收益矩Solver独立物化摘要一致。备用十进制`mask:count\n`格式SHA为`9b03b66a0cb669b17c635ee359a1314a51a80715e721852948e1fc43c8ec2c7f`。摘要不代替1590类型的实际重构与24336格逐项比对。

## 真实阅读与复跑区别

主源九字段和全部24336值、7510B生成器、point全部1905列、pair全部364变量及研究₅README均已实读/解析，按字段在生成中的实际作用检查。point的K及1306个overlap列不参与该生成器物化，不能因此声称其必要图全部行通过。16个hist旧索引映射全保；525项`hist_column_old`不是当前列位置，首次只读试算按旧索引直接取列时报错，正式算法已按当前块身份核对修正。

原入口由[生成器任务](../full156-kernel-generator/rerun/execution.json)负责唯一默认及福利复跑，本任务没有重复运行。已实读其[比较报告](../full156-kernel-generator/rerun/comparison.json)：数学字段全同；kernel的运行时长改变其哈希，福利输出相应只改变`kernel_sha256`。本页不宣称原输出逐字节重现。

总福利含前四位，与两位剩余利润不同；规范化福利除S，收益除60S。7188个低于half的行动对不等于SPE反例；全域矩、给定前缀两人尾SPE及六人完整根SPE分开。既有两人尾报告和固定前缀资源已全文比较，来源/实现/有限验证关系写入正文，三级超图留第三阶段。
