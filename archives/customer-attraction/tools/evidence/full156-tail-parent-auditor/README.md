# 完整156主题两人尾集合原审计器

正式对象：[完整156主题的两人尾集合审计器](../../../state/程序/完整156主题的两人尾集合审计器--程序.md)。完整数值逐字段解释见[配套报告](../../../state/计算/完整156主题固定前缀的两人尾报告--计算.md)。

`original/audit_full156_reply_set.py`是3920B原入口，SHA `6818a46135139c032f7a399ac9a75be908e0f921728f89a5887777375efd575d`，原字节不变。related中7510B作者kernel生成器及3253B审查稿全文实读，仅作数学比较，均不执行。`source-manifest.json`给7份来源完整ID/路径/字节/SHA与当前数据检查范围。

真正运行依赖仅3个JSON，保在相邻 `full156-tail-parent-report/original/research_5/`：旧point、F/G/U kernel、含前四题的总福利矩。临时运行前复制到空目录，保相对布局；结束即移除大副本。本包不持久重复约5.9MB数据。pair点不是本程序读取依赖，作者246个客户矩轨道未重构，原必要图5108字段也未重新验证。

本次用 `run_original_once.py`执行一次未改原入口，Python3.12.14、assert启用、无第三方依赖，exit0、stderr0B。输出 `rerun/audit_full156_reply_set.json` 与 `rerun/stdout.txt` 都是1349B且逐字节等冻结报告，SHA `99d94577b978d76a618781ba5274fee0297ccdeef087e90fba5d6ef52f827415`。`rerun/execution.json`保完整argv、临时cwd、时间及前后源哈希；临时目录已清除。

本轮实际调用命令为：

```sh
python3 archives/customer-attraction/tools/evidence/full156-tail-parent-auditor/run_original_once.py
```

包装器的rerun目录独占创建保护已生效，再次执行会在原入口运行前拒绝覆盖；未来新运行应另设独立空输出位置，保留本轮记录。不要直接在冻结original目录运行原入口，它会覆盖同目录同名JSON。

数学检查逐项解释在正文：全24336对核G对称及U=F−G，所有末位BR与全部平局参与M=max(min可信收益)判据，恰六个可实现两人SPE尾(Ci,Bi)，其最小总福利>1/2。旧A6确为BR但旧A5低于可信阈值；3δ5超过旧half坏差，只阻止该固定路径的已知异质修复，非所有修复器下界或全六人结果。

当前主Boss另写 `verify_report_fields.py`，全文读取并重建旧16字段及补核当前矩形状/尺度/福利对称；本包实读该脚本和 `field-audit.json`，不重复执行，不把它说成第二套客户矩生成器。程序、数据、已知尾判据及修复定理各自作用在正式正文解释，第三阶段再建边。
