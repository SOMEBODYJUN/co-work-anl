# 固定旧回复边缘的末回复阈值闭包程序证据

本目录对应原源 `9c82a1b1090372077fec`，正式正文为[固定旧回复边缘的末回复阈值闭包程序](../../../state/程序/固定旧回复边缘的末回复阈值闭包程序--程序.md)。主源码8353B、SHA `959d52f297152b1f2ae5e07834c56ed94f87a5cef0cf252acf2a2d0071a0b7eb`，复用[已保存原件](../full156-pair-master-point/related/zz_threshold_closure.py)；全文由clean show读取，未修改原码。

## 文件及准确范围

| 文件 | 身份与范围 |
| --- | --- |
| source-manifest.json | 主源、三冻结输出、三个旧输入及28件静态默认运行树的路径/字节/SHA；不把祖先文件全部重新清洗。 |
| related/zz_threshold_exact.json | 冻结原输出，136130B；321变量。 |
| related/zz_split_exact.json | 冻结原输出，112746B；275变量。 |
| related/zz_cross_exact.json | 冻结原输出，124405B；302变量，对应priced+optimum合同。 |
| rerun/execution.json、stdout.txt、stderr.txt | 一次未改默认原CLI的实际事件；3949行、321变量、min0、exit0。 |
| rerun/available-frozen-files-manifest.json | 原事件前后SHA核同的51件可用文件；不是动态加载记录。 |
| audit_interfaces.py、interface-audit.json | stdlib独立读取三张完整变量表，绑定旧输入，重算分层/描述/质量/O/W及所有180个新增ZZ有理余量。 |
| interface-execution.json | 正式保存后独立审计的运行记录；与先前草稿报告字节相同；不调用原构图或LP。 |
| materialize_runtime.py、materialization-report.json | 28件默认依赖树只复制和核SHA；本轮不再执行该树。 |
| self-check.json | 正文、来源路径、原件/日志、报告及回执的静态自查。 |

三个旧输入均全部解析1905列、16hist和194组三态/隐含00；output全部十字段及898个变量记录均读取。原输出scope三者都保旧3889字样，故按源点/旗标辨版本。三张表的每个变量描述、source_sha、边界和O/W经独立核对；所有新增ZZ余量非负。split/cross旧3945/4927行没有由该独立脚本生成，因此这里只认证接口与新60行。全图原验证只新增default3949这一事件。

## 唯一默认原事件

实际调用在仓外共享树进行，命令、时间与环境见execution.json。Python3.12.14、NumPy2.3.5、SciPy1.17.0，assert启用，40.3297秒；stdout152B、SHA `df353c475aef36f72b8310feb53d81960b18a2f4fafacd720f3969d3e2739a01`，stderr空。报告为3949行、321变量、min0，W直接由旧源打印。没有runpy、函数替换、被动profile或优化器调用；原源码直接作为脚本运行。根work.py仅是注释定位标记，从未执行。最初把该标记误纳入源SHA预检的尝试在原程序启动前断言失败，随后排除标记；原入口实际执行仍只有一次，详见preflight_note。

原verify按数组位置取weight，不核输出的描述或元数据；本次独立接口核补当前三表绑定。原图构建会精确代入新Z，故默认3949通过包含改Z后的旧3889，不是只核新增60行。原日志未保存全部旧行余量，不能编造它们的分布或声称第二独立旧矩阵。

另一清洗员的[pair-master原事件](../pair-threshold-closure-program/run-report.json)是不同点的10344行，其中改Z旧5108均非负；引用该事件、不复制/重跑。它不认证任何独立zz_master输出，也不补split/cross全图重放。主程序cross若不给priced和optimum，只建4019总行；给全旗标才4987，verify不核旧rows字段因此不会据此拒绝弱模式。

## 可复现入口

独立核只读冻结数据，可另选仓外输出：

    python -I archives/customer-attraction/tools/evidence/zz-threshold-closure-program/audit_interfaces.py --repo . --saved-dir archives/customer-attraction/tools/evidence/zz-threshold-closure-program/related --output /tmp/zz-interface-audit.json

只物化默认树、不运行原入口：

    python -I archives/customer-attraction/tools/evidence/zz-threshold-closure-program/materialize_runtime.py --dest /tmp/new-zz-default-runtime

物化器拒绝已有目标，先核全部原件再写，根标记仅供路径发现。选取28件1453136B来自旧完整依赖清单的默认链，加主码及default精确输出；这是静态裁剪与复制测试，不宣称已在该新树重复执行。未来需原验证时按其打印argv在有NumPy/SciPy且assert开启的解释器中执行。此次真正验证过的共享树51件可用文件另有原记录，二者身份不混写。

数学复用限固定hist/R共同阈值域：旧Z和旧交叠会变，必须重验旧行；条件独立Z给共同会员实现而非完整策略。60名义槽中18空槽，不是60个独立约束。浮点发现、精确有理回代、局部独立审计、目录会员实现和全部历史纯SPE是不同层次。本目录没有新LP、一般域不可行、最优对偶、唯一性或六人half真值结论。
