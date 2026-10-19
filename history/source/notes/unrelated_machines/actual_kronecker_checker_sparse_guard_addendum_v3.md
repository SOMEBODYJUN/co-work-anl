# 规范检查器严格稀疏记录门槛的v3补充读后

本补充只复查v2后新增的严格finite_edges序列化guard；不重做此前九类证书变异。此前v1异议与v2读后原字节保留，不倒改旧版曾接受重复同端记录的事实。

## 实际读取、差分与版本

已读旧clone最终规范checker新增guard及上下文，代码SHA256：

`8e95e8c4b00654b2e85efbd37e294837796755ce189e7e933e5200752abebbb3`。

与独立冻结的v2代码逐字差分确认，唯一变化是在原完整matrix mapping比较前增加六行guard：finite_edges总row数100；每row恰4条；每个原ID为exact int且0..63；每row四ID唯一。差分冻结为 `canonical_checker_guard_v2_to_v3.diff`。其后仍完整比对400个原有限端的真实时间与资格，故新guard只收紧原始列表表达，不改变数学实例或已审的调度/LP验证作用。

随后实际读取新clone同路径checker字节并核hash：

- `co-work-anl-boss11/tests/audits/unrelated_machines/actual_kronecker_product.py`
- `co-work-anl-boss11-negative/tests/audits/unrelated_machines/actual_kronecker_product.py`

两者hash均为上述8e95e8c4...，复制完全同字节。本审查没有修改这两个clone。

## 本轮实际五项拒绝

独立scratch副本 `checker_sparse_fixture_v3/` 中，脚本 `review_sparse_guard_v3.py` 实际执行以下变异，全部返回非零且未创建成功输出：

1. 原row追加同一finite端，形成第五项；由len(row)==4拒。
2. 在row长度仍4时，用已有端覆盖另一个不同端；由四ID唯一拒。
3. 把ID0写成JSON false；由type(i) is int拒，不能借False==0混入。
4. 原row增加第五条不同端；由len(row)==4拒。
5. finite_edges追加第101个job row；由总row数100拒。

结果、拒绝位置及代码hash完整冻结于 `checker_sparse_guard_review_v3.json`。本轮未修改共享输入、证书或既存输出，未覆盖任何旧审查记录。

## 裁定与边界

v2保留的重复同端归并接受行为在v3已经关闭；strict100×4原记录合同通过本次指定范围的代码读后与实际变异。ID类型/范围/唯一性都先于dict转换，因此不会被字典去重掩盖。

与v2相比没有其他代码变化，既有正确证书、15件同时改派、有限四次幂和原位覆盖拒绝审查继续适用；parent的正确v3运行是另一个实际事件，本补充不冒称重跑了所有旧case。无standing fatal，未宣称一般LP solver、全输入调度算法或hardness实现。
