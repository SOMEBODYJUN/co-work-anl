# R-aba0b2b728764e70a75058d600afe6b6 的个人研究工作区

研究存档：`unrelated-machines`；发布身份：`R-aba0b2b728764e70a75058d600afe6b6`。

## 当前研究

本阶段按用户指示转向 UM-TARGET-v1 的反面：寻找在明确复杂度假设下、对每个固定 ε 都有实际整数 OPT 间隙 (1) 对 (2-ε) 的位多项式归约。公屏协作确认现有 LST 3/2-hard、配置/SA gap 和 Santa Claus 方向都不足以给出该结论。

已冻结的本阶段障碍是 [三维匹配需求树的低比例地板与反面归约障碍](../../../current/unrelated_machines/three_dimensional_matching_demand_floor_obstruction.md)：标准 (D_K(A)) 的精确 (b^*) 同时含一资源匹配 (mu) 与三维匹配 (
u)，完美 YES 值为 (2/K)。这排除了“提高三元组需求来压低 NO、同时保留 YES=1”的直接接口。公共 Hall 资源族给出可趋零的目标形状，但尚无 NP 编码。

## 可访问材料

- [精确障碍正文](../../../current/unrelated_machines/three_dimensional_matching_demand_floor_obstruction.md)
- [Fraction 审计代码](../../../../../../tests/audits/unrelated_machines/three_dimensional_matching_demand_floor.py)
- [冻结审计记录](../../../../../../evidence/runs/unrelated_machines/three_dimensional_matching_demand_floor_audit.json)
- [反面路线账本](../../../unrelated_machines/CLAIMS.md)

下一步是攻击共享标签/高距离一致性候选：完整 YES 需 (b^*=1)，而每个 (bge ε/2) 的实际树必须解码源问题；同时先在公共 Hall 资源小族上检查任何复制或 tensor 方案是否把分数池整数化。

## 交流与状态

已在公屏征集各单位的重合路线和最小一致性 gadget，并收到 boss1/2/3/4/10/11/12 反馈。未完成的想法仍标注为候选，不把消息或有限实验升级成一般硬度。其他人可访问已推送材料；本地草稿只有完成 checkpoint 并确认 pushed 后对其他 clone 可见。
