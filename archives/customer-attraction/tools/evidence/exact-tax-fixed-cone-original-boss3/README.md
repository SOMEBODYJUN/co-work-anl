# 实际缩放精确税：三冻结源与新单点核验

正式正文：[实际缩放精确税的固定策略锥搜索](../../../state/计算/实际缩放精确税的固定策略锥搜索--计算.md)。

`original/scan.py`、`original/results.json`、`original/best.json` 是 Boss3 本批三个已认领冻结源的原字节。`original/customer_attraction_strategy_lp.py` 是已全文比较的直接依赖，只作相关来源，未在本批重新登记其done。完整SHA-256、字节数、双冻结提交、原路径及主/依赖角色在 `source-manifest.json`。

`audit_saved_records.py` 是本轮新写的独立标准库程序。它验证所有原件指纹、53条记录的全部273查询字段、最佳点全部127类型/2801历史，以及19607项真实偏离比较；输出为 `saved-data-audit.json`。这份输出是新数据核验，不是原浮点搜索复跑。其精确SPE认证只针对原best中全七标签共享一个客户的点。

从仓库根运行：

```sh
python3 archives/customer-attraction/tools/evidence/exact-tax-fixed-cone-original-boss3/audit_saved_records.py --out /tmp/new-exact-tax-audit.json
```

输出文件必须尚不存在，原冻结输出不会被覆盖。只需Python标准库。

原 `scan.py` 的运行布局需要原根 `customer_attraction/__init__.py`、该包及NumPy/SciPy、原 `tests/audits` 模块位置和全部当时输入文件。这里只保全原实现与明确接口，不声称已归集或重新跑完53个历史输入。程序导入的 `StrategyCone.optimize` 虽提供其他目标的精确对偶恢复，本扫描并未调用它，故本批没有273项精确上界证书。

原README入口所称53/273现已由实际记录核实。一般税桥的历史OPEN已由既有13人完整SPE反例纠正；本批没有把负搜索当一般证明或六人反例。
