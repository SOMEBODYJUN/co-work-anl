# Boss6：可信完整策略、完整分数查询与反例攻击

主目标 Q-CAG-HALF 仍 OPEN；早期 `OPT_m−W≤m u_i`、`B(u_i)≤W` 及既有更强
分数 floor 均未在本分支一般解决。没有真正半覆盖反例，没有将规范最差续局当成
全部 SPE。所有候选策略逐有序历史定义，正式精确例证覆盖全部离轨偏离。

## 本轮可复用成果

| 文件 | 准确用途与范围 |
| --- | --- |
| [完整查询归约正文](fractional_price_query_reduction.md) | PRICE-QUERY-VERTICES-v1：任意非负价格、任意非负客户重数的完整分数价格势，由只依 p 的有限精确顶点全表实现；证明所有边界与固定完整 σ 锥的 Farkas 接口。不是一般福利结论。 |
| [精确顶点生成器](fractional_query_vertices.py) | 整数 Bareiss+Fraction，不用浮点判断奇异或正性；全部正支撑行子集及坐标嵌入。 |
| [五目录完整顶点](query_vertices_p5_exact.json) | 全部 260 个标号顶点、27 排序型、171315 个行组合的精确枚举统计。理论合同有独立盲重构，p≤4 有第二算法全集核对；p5 尚未第二实现全枚举。 |
| [固定完整策略证书器](fixed_policy_price_certificate.py) | build 用 LP 提案后精确验证；verify 不调用 LP，独立重建全部有序历史 Γ 并逐坐标核对所有有理 Farkas 证书、所有查询及根占用主题。 |
| [非PNE固定策略分数floor证书](nonPNE_fixed_policy_tstar_exact.json) | 一份16客户福利比较失败来源的完整 σ，根 (0,3,3)，39 行 Γ；其**整个非负重数锥**的 2 主题×30 查询共60份精确证书，证明该锥 B(u_a)≤(m−1)u_a。 |
| [同策略更强价格证书](nonPNE_fixed_policy_price_plus_u_exact.json) | 同 σ 的60份精确证书，证明该锥 B(u_a)+u_a≤W。只此 σ，不扩为其他 SPE。 |
| [旧查询集合补核](query_enumeration_audit.json) | 最初浮点提案的查询集确与精确表相同；不认证旧浮点 LP 的上界。 |

独立理论/实现审查在同级 `../independent/`。主代理统一保存；本分支不单独 git、
推送或对外交流，也不修改共享数学状态。

## 探索与失败身份

- `price_arrangement_attack.py`：现只导入精确枚举器。`price_m3p5_discount1.json`、
  `price_m4p5_discount1.json` 保留最初8/20策略的浮点提案记录，未证明相应全锥上界。
- `attack_archived_policies.py`、`archived_tstar_attack.json`：对已有非PNE/匹配机制的
  固定策略锥攻击既有分数 floor；未分离。只有上表两份已逐项有理复验的证书有
  所写固定 σ 全锥结论，其余阴性不是一般证据。

下一步：提炼跨不限定 σ 的解析机制，或设计新的可信非PNE子树；停止增加同类
阴性 seed。完整 z 查询的量词已精确化，完整策略 σ 的一般量词仍承重。
