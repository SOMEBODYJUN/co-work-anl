# 旧回复共同报价十四行：原作者审计器

正文：[旧回复共同报价十四行的系数审计器](../../../state/程序/旧回复共同报价十四行的系数审计器--程序.md)。主源 `53a6dd749f079ac1abc9` 的3019B未改原件共享于 [既有保全路径](../cross-source-graph-program/related/audit_cross_source_basic.py)，不重复存源；其SHA为 `5113ef5d4f46b5d2c40b6fc9dcb3c1788fa4d3ea6677bf89a462560d4a53275b`。冻结定位与比较来源见 [source-manifest.json](source-manifest.json)。

本目录补的是**原作者入口的当前真实复跑**。此前cross源清洗已另有独立新系数实现，本次不把原作者脚本再运行改称新的独立实现。

- [rerun/stdout.txt](rerun/stdout.txt)：未改原入口的386B完整输出，仅四字段，含43918系数比较、3137列和两条负余量。
- [rerun/stderr.txt](rerun/stderr.txt)：真实空输出；[execution.json](rerun/execution.json)记录exit0、环境、时间、输入前后SHA和实际命令。
- [comparison.json](rerun/comparison.json)：原负子集与此前独立审计的完整split14表对比，严格相等。原程序没有打印完整14表，此处不伪造。
- [replay_author_audit.py](replay_author_audit.py)：本次实际使用的进程组织代码，原作者代码与系数不变。
- [prepare_runtime.py](prepare_runtime.py)：后续重放用的目录恢复器，只按已保原件和SHA恢复文件，不运行任何原数学程序。本轮已在另一clone外目录恢复并核50文件，见 [preparation-check.json](preparation-check.json)。

原作者脚本在模块顶层执行；它导入cross后会替换sb.build并重置argv，因此使用独立进程。它仅生成14条新基本行，没有继承图build、priced/optimum行、LP或完整SPE验证。NumPy/SciPy仍是cross顶层导入所需依赖，本次为Python3.12.14、NumPy2.3.5、SciPy1.17.0；运行时开启assert。

本次续接保存的是2026-11-01T14:22:48Z已发生的唯一原入口事件，没有重新运行。原日志按字节保留；[selfcheck.json](selfcheck.json)另记录落地后的路径、SHA、JSON及Python语法检查，不把文件完整性自查计入数学审计。重放时须关闭 `PYTHONOPTIMIZE`，且不可加 `-O`/`-OO`；原代码的断言不能省略。

在结果仓库根目录，可用如下两步重放；输出置于新的隔离目录，不覆盖本次原日志：

```sh
python3 archives/customer-attraction/tools/evidence/cross-source-basic-author-audit/prepare_runtime.py --repository . --runtime ../cross-basic-runtime
python3 archives/customer-attraction/tools/evidence/cross-source-basic-author-audit/replay_author_audit.py --repository . --runtime ../cross-basic-runtime --out ../cross-basic-replay-output
```

恢复器复用 [联合图原件清单](../combined-branch-master-program/source-manifest.json)、[49份可用文件清单](../combined-branch-master-program/rerun/available-frozen-files-manifest.json)，加本审计器，按原repo相对路径恢复。清单中的两个大点从各自既有证据位置补路由；这为复现原共享环境，不宣称每个文件都被本审计加载、都经本任务逐条数学审查或都是最小依赖。work.py仅供原模块发现根目录，不执行、不需要凭据。

这里不重复历史LP、不重新验证原3945/4927/5108图。此前更广的独立行核验见 [cross审计报告](../cross-source-graph-program/audit-report.json) 与 [完整余量表](../cross-source-graph-program/added-row-slacks.json)，其中split_point的14行与本次同一输入。该点恰被两条实际末位报价切除；程序成功退出与旧点通过约束是不同结论。
