# 剩余利润机会边界的来源与精确复现

主对象为[发散系数与线性欠债](../../../state/障碍/R-18动态利润机会与非局部势边界--障碍.md)，执行范围由[计算资源](../../../state/计算/剩余利润机会公式与完整历史的精确核验--计算.md)说明。此目录原件、比较材料、重生成输出与本次新增核验分开保存；本次没有Git、网络或clean写入，不以本地文件声称已checkpoint或done。

- `original/`：父Boss clean show导出的本批3源，逐字节保全。
- `comparison/`：已整理R-18证据中的完整full-tree审计、两个JSON输入、原4641B输出及原README；只作比较依赖，不替原来源再done。
- `replay/reviewer/`：原944B复核脚本一次执行；输出282B、SHA与原件相同。
- `replay/full-tree/`：原完整历史审计一次执行；输出4641B、SHA与冻结报告相同。
- `supplemental/`：本次定义级单位客户核验代码及363条真实节点/行动比较、全部25个背景计数值。
- `replay-report.json`：两个原程序实际命令位置、Python版本、退出码、stdout/stderr和hash对账。
- `source-manifest.json`：本批完整冻结来源、比较文件hash、语义阅读范围和产物指纹。

`profit_opportunity_review_boss5.py`在模块顶层写相邻同名JSON，复现时先复制到新的临时目录，以免覆盖历史报告。它不读其他文件。`profit_opportunity_audit.py`除标准库外，只读取同目录的`background_step_instance.json`和`background_step_certificate.json`。新增补核脚本按相对路径只读`comparison/`两个JSON，写`supplemental/background-unit-check.json`。

全部一般数学结论由对象正文的解析证明给出；有限公式点不承担任意人数证明。历史reviewer字段仅保存来源事实，当前Boss5身份不作任何迁移。
