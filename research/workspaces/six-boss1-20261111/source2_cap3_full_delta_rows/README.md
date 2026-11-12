# Boss1：585条完整二维cap3端点原行

RUN `six-boss1-20261111`；实际 agentID `/root/source2_cap3_tradeoff`。本阶段仅向本隔离目录写入。

**已物化全部225个源物理顶点的585条原尺度记录，每条完整513列；独立逐列检查全部PASS。** 360条一般T、45条C-only、180条ordered，无筛删，无除25，无LP点或最优面读取，无优化器。

## 直接入口

- [exact_family.json](exact_family.json)：顶层`rows`，每条`row.a`为长度513的有理数字符串列表；全部真实IC/K/freeEC、参数、来源id与二维包SHA均在行内。
- [proof.md](proof.md)：完整物化说明、真实付款、列合同、旧族比较与结论范围。
- [source_binding.json](source_binding.json)：冻结二维包及旧186/δ180家族的准确SHA绑定。
- [vertex_registry.json](vertex_registry.json)：全部225原顶点完整metadata、原weak状态与cell/edge关联。
- [vertex_cost_tables.json](vertex_cost_tables.json)：从真实COST直接计算的74880个尾成本、全部弱态及全物理重数。
- [bound_row_recipe.json](bound_row_recipe.json)：冻结源recipe的逐字节副本。
- [literal_checker_output.json](literal_checker_output.json)：300105列、585条元数据及真实菜单检查全部PASS。
- [C_only_redundancy.json](C_only_redundancy.json)：45条C-only的明确底边绑定及非负余项，全部记录保留。
- [literal_coincidences.json](literal_coincidences.json)：与既有186重合174条，与旧δ180重合180条，两族并集命中297条；288条仅为字面未见。
- [old186_containment.json](old186_containment.json)：174个字面身份、12个非负二顶点身份，完整支付旧186家族，未增加或删除新行。

九份孤立弱最优记录均保留。全部585向量内部互异，但这是事后核验事实，不是去重规则。C-only的全二维冗余已证明，仍保留当前45条；一般T/ordered对所有已有约束的锥冗余没有在本阶段判断。

客户列依`(a1,…,a6,x,o,c)`字典序排列，第512号列为独立K。`numerical_divisor=25`仅为可选数值元数据，`divisor_applied=false`；真实IC取`real_budget.source_IC`，不可改为25。

冻结记录见`freeze_manifest.json`和`SHA256SUMS`。完成后停止写入，供Main独立接回并进行后续实际点与完整面检验。
