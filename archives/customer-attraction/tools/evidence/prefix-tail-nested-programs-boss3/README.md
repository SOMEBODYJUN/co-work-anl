# 前缀、真实末三位和嵌套分支程序证据

本包清洗四个原来源：`prefix_floor_lp.py`、`last_three_lp.py`、`nested_branch_lp.py`、`lift_old_point.py`。完整原字节在 `original/` 中保留原相对路径；[source-manifest.json](source-manifest.json)绑定两冻结版本、blob、SHA-256、主源/仅依赖身份。

正式数学对象：

- [六人前缀保底证书的整数阈值与有理回代](../../../state/计算/六人前缀保底证书的整数阈值与有理回代--计算.md)
- [真实末三位分支的逐客户福利证书搜索](../../../state/程序/真实末三位分支的逐客户福利证书搜索--程序.md)
- [实际末主题嵌套偏离与旧边缘抬升](../../../state/程序/实际末主题嵌套偏离与旧边缘抬升--程序.md)

## 本次真实执行

`run_original_once.py` 核所有输入SHA，在clone外临时副本按原层次放置四程序及三依赖，再顺序执行四个原主入口各一次；均退出0、stderr空，原文件前后字节不变。Python 3.12.14、NumPy 2.3.5、SciPy 1.17.0；OpenBLAS及OpenMP线程数均固定1。完整实际argv、临时路径、时间和源哈希在 [runs/execution.json](runs/execution.json)，全部stdout/stderr逐入口保存。临时运行树已由上下文管理器删除，日志仍保留；不称后台继续计算。

| 入口 | 实际运行范围 | 证据强度 |
| --- | --- | --- |
| prefix_floor_lp | 阈值0、1、2、3、4 | 0/1/2只有浮点不可行；3/4有原Fraction完整余项核验 |
| last_three_lp | n=3、4、5、6 | 仅浮点β和打印活跃权；未调用可选NPZ保存 |
| nested_branch_lp | 默认六人、源实际3/4、query A、相邻四根JSON存在 | 80640约束/1484变量，float β=2.287018214699084；无有理权证书 |
| lift_old_point | 两query_kind各实际1/2/3/4源，plain=False、separate=False | 各第一源浮点可行，其余六个浮点不可行；未保存精确隐藏见证或Farkas证书 |

新增 `audit_prefix_certificate_and_old_marginal.py` 不导入上述原程序，用标准库从S/Z/V未消交集式核阈值3和4的完整系数域，3528/2856含交集类型全部非负。它另按已绑定旧点SHA核该调用真正消费的16hist、1K及8正边缘/W；没有重核旧1033行，也不把其194个new-reply记录冒作本轮已重新分析。完整输出为 [runs/independent-prefix-and-margin.json](runs/independent-prefix-and-margin.json)。

独立脚本是读取后编写的第二实现，不是盲审。完整条件证明由正式正文中的真行合法性、完整局部域及精确余项共同承担；浮点优化状态没有被升级成完整博弈事实。原脚本均未改动。运行包装器在本轮全四次成功执行后补了非零子进程退出码的转发，仅改善将来的失败报告；原执行记录仍是实际已完成这一轮，没有因此重跑。

## 可复现依赖与运行方法

三件直接依赖也保完整原字节：`max_branch_lp.py`、`root_lines_certificate_v2.json`、R-c4f旧1033点 `full_new_reply_closure_exact.json`。前两件位于与嵌套程序同目录，旧点在原R-c4f相对位置。旧点的SHA为 `24a2f9fa7e7a47e26e065b41ada98e1788a5b448251fb8c1e881557c1f7c9f11`；它与后来5108点或5692点不同。

在本目录运行 `python -B audit_prefix_certificate_and_old_marginal.py` 可重核已保存的有理输入，不需SciPy。要重新执行原发现器，复制本包到新的工作目录并先将既有 `runs/` 移到另一个记录目录，再运行 `python -B run_original_once.py`；包装器拒绝覆盖已经存在的 `runs/execution.json`。不要直接删除已归档日志。NumPy/SciPy仅用于四个原入口。

数学来源清单之外的临时路径只用于记录本轮事实，不是后人需要取得的依赖。source-manifest中的exported_path记录来源导出的历史位置，稳定复现使用evidence_path对应的本包原件。stage和本证据均不含仓库凭据。
