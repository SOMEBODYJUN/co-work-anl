# 472客户强iid分离与根近饱和证据

六份冻结原字节文件在 `original/` 保留原路径；[source-manifest.json](source-manifest.json)记录全部源ID、完整双冻结commit、哈希与大小。原独审的默认路径仍可用。对应正文为[472客户有限反例](../../../state/反例/三人五主题对称独立收益分离--反例.md)、[完整历史与删标签核验](../../../state/计算/四百七十二客户独立收益分离的精确核验--计算.md)和[最大主题条件覆盖阈值](../../../state/推论/最大主题根近饱和的覆盖阈值--推论.md)。

在本目录运行：

```sh
python3 audit_472.py
```

该标准库程序不导入旧模型或审计函数，展开472名不同单位客户，检查两份完整有序策略及全部125/216终局、155/258比较、iid KKT、精确删标签投影和相关CCE完整策略的逐项相同。它还把原字节独审作为子进程真实运行两次，比较冻结五主题报告除 `source_witness` 本地路径之外的全部字段。原程序没有生成文件的副作用；本程序默认只打印结果。本轮保存的[完整输出](replay/exact.json)含每个节点的真实偏离收益、两原程序输出及映射。[verification.json](verification.json)绑定新源码/输出及相关已清洗CCE证书哈希。

原字节独审亦可单独运行：

```sh
python3 original/research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/strategy_geometry/cone_abstraction/strong_iid_independent.py
```

默认读取五主题完整JSON，也接受任意一个完整见证JSON路径作为唯一参数。冻结报告中的原绝对输入路径只是历史定位，不要求访问那个旧工作区。独审正文A/B分别是有限强iid分离与一般根饱和解析审查，数学对象在正式正文中分开；无新增外审。

本包未包含或冒称本批已清洗57202客户见证、`exact_iid.py`发现程序或 `root_saturation_audit.py`。根覆盖阈值具有全人数解析证明，有限代码不认证其普遍性。472两个版本均满足弱iid和half，真正安全值未计算；本包不给六人half或聚合安全值桥的证明/反例。
