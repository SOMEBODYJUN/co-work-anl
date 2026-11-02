# 全策略锥CCE六源的增量来源合同

两正式对象：[程序合同](../../../state/程序/完整策略锥与静态粗相关对偶的交替接口--程序.md)、[四份计算记录](../../../state/计算/全策略锥CCE的二十八随机树与四个旧策略--计算.md)。旧[数值屏幕](../../../state/障碍/R-3b6b全策略锥CCE数值屏幕--障碍.md)及其全部原件继续保留。本包没有复制覆盖历史正文或给旧smoke补新独审身份。

六直接源按本次正常clean show的冻结元数据，与[既有六原件](../R-3b6b-security-global-20261031/source/)逐字节核同，所有226470B原字节仍在该已发表目录。四报告218982B全部32条case和660个attempt已逐字段实读，两个源码共7488B完整阅读。两个冻结提交内容相同，不作两次独立证据。

- `source-bindings.json`：六直接源及13项本地必要依赖，逐一保留完整提交、源路径、源ID、blob、SHA-256、字节数和实际已存原件地址。无需重复拷贝已有完整文件，也不登记或done这些依赖源。
- `lossless/*.json`：四报告的完整JSON值可逆排版。根字段全留；每case非attempt字段全留；每个attempt以(start,iteration,payload_id)按原顺序引用完整payload；message重复文字单独索引。解码后与原JSON结构逐项相等，浮点值不有理化。原字节哈希另验。
- `record-analysis.json`：全部case标量、每case完整网格/最小残差/归一化偏差、命名输入全部非零客户及实际路径。该文件声明的核验仅为数据、域和路径，不是SPE或CCE数学认证。
- `check_source_contracts.py`：只读绑定原件和本包视图的自查，不import作者程序，不调用求解器、LP或SPE验证器。传`--repo`指向结果仓库；输出JSON到stdout，不覆写输入。
- `relation-evidence.json`：参与对象、共同假设、关系种类、数学理由和证据定位，供父方阶段三逐边判断；不是直接写入正式图的边文件。

命名入口需要四模型、四完整策略；它们复用`pair-kernel-original-diagnostic-two-primary/original/`的冻结同SHA原件，四模型全部客户行已读，完整动作原件继承先前交付，只核精确历史域、标签和实际路径，不重跑已完成IC。随机入口所需的`cone_security_search.py`仍为旧包的5027B原件；规范包四模块复用`root-static-security-and-paired-lift-program-contracts/source-root/customer_attraction/`。该helper及规范exact/__init__本次实读，model/certificate按已建立模型/完整策略合同及同SHA原件复用，不另声称本轮全文审这两项。

NumPy/SciPy/HiGHS是外部运行依赖；历史报告没有版本、完整argv、全迭代解或完整运行绑定，本包不补造。`cone_cce_named.py`无main guard，import会跑LP且覆盖写死路径；不得在已发表目录import。`cone_cce_search.py`的main也覆盖`--output`，如未来确需复现应在隔离原目录布局中选新的输出路径。

本次作者程序执行、模块import、随机探索、LP、BI和新数学证书核验均0。旧包smoke仍为旧同实现的小规模运行，不重复为本次新证据。字段和字节自查均不能代数学理解；全部定义、式子、全兴趣删除论证、旧精确反例的后续状态及量词边界由正式正文承担。
