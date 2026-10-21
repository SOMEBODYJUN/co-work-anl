# 安全值路线：精确实际税桥的完整SPE反例

2026-10-21，Boss8研究员个人资产。原目标Q-CAG-HALF以及真正聚合安全桥 `W≥m v_m` 均仍OPEN。

本目录的新发现是一个 **13名提供者、6个共同主题、36名单位客户** 的完整历史纯SPE，否定原来尚开放的精确实际分数税支付桥

`m max_T sum_(x in T) 1/(1+((m−1)/m)c_x) ≤ W + sum_(c_x>0) 1/(1+((m−1)/m)c_x)`。

- 自足数学说明：[refined_tax_counterexample.md](refined_tax_counterexample.md)。完整SPE由有限自动机给出：全部观察行动都有后继，允许等计数历史处于不同自动机节点。
- 输入、根路径、全部策略节点：[refined_tax_k10_packet.json.gz](refined_tax_k10_packet.json.gz)。27243自动机节点、18675决策节点，表示全部有序历史上的策略。
- 独立定义级核验：[audit_refined_tax_packet.py](audit_refined_tax_packet.py)，标准库、逐名单位客户、无需规范solver。112050项真实偏离比较精确通过；[冻结结果](refined_tax_k10_audit.json)。
- 构造器：[build_refined_tax_packet.py](build_refined_tax_packet.py)，使用规范集合值BI发现可实现终局，再构造有限自动机；审计器不导入它。
- 探索性前身：[padding_probe.py](padding_probe.py)。精确检查指定有限k，不是任意k证明。

数值均为精确有理数：实际路径 `P^10,A,A,B`，收益十二个 `5/2` 加一个 `3`，`W=33`、`OPT=36`。`M=3`、`G=708669/123025`，故 `13M−W−G=29481/123025>0`。更强逐人分数税候选亦失败，差为 `13999/246050>0`。

真正安全值不被否定：固定不观察查询的静态对手组合 `P^9,A,B,T` 使全部纯查询收益至多 `5/2`，因而 `v_13≤5/2`，本例满足 `W−13v_13≥1/2`。半覆盖余额是 `2W−OPT=30`。

root和credible的独立定义级复核均已通过（credible盲重建BI与完整续局）；对应脚本及结果见正文第6节。下一步：任意k的解析padding仍未证明。没有修改共享登记，没有git操作；由root统一保存。
