# ZZ分裂必要点的原件绑定与核验

对应源02d0fd462e0a58600eb4，正式对象为[ZZ分裂必要系统的有理候选点](../../../state/计算/ZZ分裂必要系统的有理候选点--计算.md)。完整clean show导出与[已有112746B原件](../zz-threshold-closure-program/related/zz_split_exact.json)逐字节同，SHA312732da47c24fe39259c339cf669231162f1402c85a4036a8a351abaef7f51c，不额外复制。实际输入是[814800B split点](../split-basic-graph-program/related/split_basic_exact.json)，由原表source_sha256绑定。

|文件|实际职责|
|---|---|
|[review-record.json](review-record.json)|原件版本、全文阅读及相关比较、原运行与独立检查的边界|
|[rerun/execution.json](rerun/execution.json)、[stdout](rerun/stdout.txt)、[stderr](rerun/stderr.txt)|唯一新原CLI `zz_threshold_closure.py --split --verify`，4005行/275变量/min0，exit0，31.252秒|
|[rerun/runtime-manifest.json](rerun/runtime-manifest.json)|31份未改冻结文件及持久来源；前后SHA全同，是可用清单而非动态加载记录|
|[rerun/replay_split.py](rerun/replay_split.py)|实际启动记录用脚本，保当次绝对scratch路径；不把它改写成无包装shell执行|
|[materialize_runtime.py](materialize_runtime.py)|可移植复制/核SHA工具，重建独立树但不启动原程序|
|[materialization-report.json](materialization-report.json)|一次31文件复制与SHA复现测试，未再次启动原程序|
|[audit_split_point.py](audit_split_point.py)|标准库独立核275记录、43代表原子、全部1905恢复坐标及7931后继差异；不导入作者构图、不跑LP|
|[point-audit.json](point-audit.json)|全部16hist、22R层、43原子、275变量索引与质量、194组边缘、1905恢复坐标、255旧列差异及103后继变量差异|
|[self-check.json](self-check.json)|最终原字节、JSON/AST、正文链接、回执目标和运行身份自查|

原程序本身以直接子进程脚本方式执行，无runpy、trace、profile或函数替换；外层replay_split.py仅物化、启动和记录。assert启用，PYTHONOPTIMIZE移除，Python3.12.14、NumPy2.3.5、SciPy1.17.0。0新LP；原main实际只有一次。该事件补齐新Z处旧3945行，而既有[三表接口及180行审计](../zz-threshold-closure-program/interface-audit.json)的split60行复用，不重复扫描。原scope的3889字样按实际split模式校正为3945+60。

独立脚本本轮运行一次成功；43原子是有理质量的hist代表会员型，非43个单位客户或完整策略。共享阈值和必要IC均未认证全SPE、精确最优或全域不可行。后继7931点描述相同但103质量变，未在此重验其全图。

从仓库根仅复制冻结验证树：

    python archives/customer-attraction/tools/evidence/zz-split-exact-point/materialize_runtime.py --repo . --dest /tmp/zz-split-verification

原入口可在该树中按执行记录的原路径使用`--split --verify`；不要改成默认3949或pair7931入口。若只需重做本数据重构而不建原矩阵：

    python archives/customer-attraction/tools/evidence/zz-split-exact-point/audit_split_point.py --repo . --output /tmp/zz-split-point-audit.json

原点、输入、比较点及已有60行报告都保存在各自来源证据包，当前脚本逐SHA绑定它们。本页来源完成只针对02d0；不替其它输入或后继来源办理完成。
