# 规范完整矩阵证书检查器的初版输入拒绝异议

审查对象：`co-work-anl-boss11/tests/audits/unrelated_machines/actual_kronecker_product.py`，首次全文读取SHA256 `bf559a00581730d68684ddf28e8a331975ca86f5cdc5246c89506d2df0fd3f62`。

审查者实际执行了该版正确输入，结果保存到 `canonical_checker_baseline_run_v1.json`，1024份seed、两证书、400有限端、15件结构改派、四次幂10000jobs/4096machines均通过。此正确运行不证明错误输入会被拒。

代码全文审查得到三项问题：

1. `verify_square` 未检查扁平machine ID的整数类型与0..63范围。对任何正确证书的每一项v同时改为v−64，Python有 `divmod(v−64,8)=(i−8,h)`，M[i−8]正好别名M[i]，loads[v−64]正好别名loads[v]；因此原算法会把这些错误负ID解释成合法旧端并保留全部负载。bool False也会别名机器0。该异议由确定的Python索引语义推导，未伪称已对旧版实际运行变异。
2. dict-schema分支只遍历前100个row，未先检查raw的总长度，追加第101row会被忽略。该分支生成的ass仍100长，因此后面的len(ass)==100不能检查原记录数。
3. 输出字段叫seed primal-dual value，但该版只显式核dual权和/目标，没有回算half-half primal的八个行负载。数学上半半primal已在正文证明，问题是代码验证报告的作用需对齐。

三项已立即报告parent，parent修复共享代码，审查者未改。首次准备scratch副本变异时，代码hash已变为bb7d555...，保护断言立即中止，因此没有对已变版本冒称这是旧版实验，也没有覆盖v1运行记录。

修复版明确增加每个raw的len100检查、每个扁平ID的exact int与0..63检查，以及half-half八行负载全1的精确验证。对应修复读后与实际变异另存v2及之后记录。此处保留原始异议，不回写成旧版已安全。
