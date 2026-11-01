# 旧查询网格行加入后的4971行有理必要点

正文：[旧查询网格切面加入后的有理必要点](../../../state/计算/旧查询网格切面加入后的有理必要点--计算.md)。唯一主源 `358135a42d98d3ff5129`，815911B，SHA256 `0c06316a0ad5b4079c54d36cf59255c36943af957644b0ffab1b34a249ee6f7c`；原件共享 [all_reply_query_cuts_exact.json](../continuous-old-query-cuts-program/related/all_reply_query_cuts_exact.json)，不复制大输入。两冻结提交、原路径/blob和实际比较来源见 [source-manifest.json](source-manifest.json)。

本包新增的是完整数据解码与有限局部精确核验，未重跑作者构图、4971行verify、网格/连续发现、LP或64割系数审计：

- [audit_point.py](audit_point.py)：标准库/Fraction独立读数器，逐字段检查全部1905列，字面六索引边重建group和全部列描述符，再计算194组四态、2612条交叠上界、36floor及8个强PAIR端点余量。
- [point-audit.json](point-audit.json)：全部12原字段、16hist精确质量、六收益、44行余量、完整189个储存overlap低于字面集合交Fréchet下界的例子，以及正overlap账本。这个189计数限制的是原样解释储存辅助量，不声称固定支持无法通过换交叠或会员实现。
- [joint-state-ledger.json](joint-state-ledger.json)：194组的旧/当前父列、边重数、00/01/10/11四态及R/Z边缘；含隐式00，非只读非零支持。
- [coordinate-delta.json](coordinate-delta.json)：同1905描述符下，前4963点到本点全部114个权变化（62joint、52overlap）。K和全部hist权未变，故相同W不意味着相同点。
- [execution.json](execution.json)、[stdout.txt](stdout.txt)、[stderr.txt](stderr.txt)：clone外新局部脚本执行信息与输出。开发时一次初始计算、收紧断言开关/摘要后一次最终运行，共两次自写脚本；新增作者入口次数为0。最终exit0、stderr空、约0.110秒。
- [selfcheck.json](selfcheck.json)：真实落地后的源SHA、输出/脚本SHA、JSON/语法、精确表格和相对链接检查；它不是另一次数学入口运行。

结果：16hist中10个正，194组四态上界全部通过；1306个辅助overlap均满足两个上界，1113个等于两R边缘的min、193个较小，其中189个若当字面集合交则不满足Fréchet下界。正文给0基列944的精确例证，并解释在原始行交叠系数非负的合同下，把全部R嵌套、保每组R/Z四态可共同向上抬升这层。该论证不自动认证其它新增约束或完整SPE。

44新增行直接回代：36floor为9零27正；8网格行是2零6正。整体4971可行性和最小余量0仍是原作者报告。本次按原SHA完整比对已有64割表与 [现存独立报告](../continuous-old-query-cuts-program/replay/local-row-audit.json)，确认64条仍针对本点、全部严格负；没有再次计算其121920个系数或180次发现LP。

从结果仓库根目录复核本包局部范围：

```sh
python3 -B archives/customer-attraction/tools/evidence/old-query-grid-necessary-point/audit_point.py --repository . --out ../old-query-point-local-check
```

选择新的输出目录以保现有记录。脚本拒绝优化禁用断言的解释器，不使用 `-O`/`-OO` 或 `PYTHONOPTIMIZE`。它按共享原件路径读取已保输入，不需旧完整运行目录、NumPy/SciPy或凭据；JSON输出没有全部4971行矩阵、精确对偶或完整策略。需要其它范围时，应明确新增的行/客户域/策略义务，而非从本局部PASS扩张认证。
