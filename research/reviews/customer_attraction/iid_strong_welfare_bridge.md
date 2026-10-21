# 强 iid 福利桥的既有反例推论：独立审查

审查对象：CA-IID-STRONG-WELFARE-NO，原CAG-MODEL的全部有序历史纯SPE；2026-10-21。
状态：内部独立重构通过；不是新的SPE实例，无外审或新颖性认证。

安全值研究分支与其独立研究员先发现现行强桥状态冲突，root另外读取静态iid完整定理、八客户完整策略和CCE原始证明，独立重建：

1. 静态凹势最大者q的n重乘积分布确为静态混合Nash，因而满足每个玩家每个固定行动的CCE约束。其覆盖期望正是Z_n，不是任意iid分布的最大覆盖。
2. 八客户结果量化同实例全部静态CCE，包括不对称/相关分布，故也包括该乘积分布；W6<544/87≤Z_3。SPE实例与均衡都不改变。十三客户证据也独立支持同一推论。
3. 显式t=(30−√669)/7解7t²−60t+33=0，q=(0,t,(1−t)/2,(1−t)/2)。纯查询1、2、3收益相等，查询0严格小；单位客户按原四主题逐项代入，Z_3=(4344−156√669)/49>6。核心推论不依赖此可选闭式计算。
4. 真正安全值44/23的minimax对象不同；W−3v_3=6/23>0。因此不能从本反例声称真正聚合安全失败，也不影响一般half或较弱iid桥的开放状态。

原有树平均分离向量不是SPE，其模板范围未扩大；这次真实SPE反例来自既有CCE正文。动态iid的五人特定实例强桥数值仍可未判定，一般强桥已被另一个三人实例否定，两句话并不冲突。

实际来源：[iid静态定理及推论](../../current/customer_attraction/iid_security_and_flow_barriers.md)、[八客户原证明](../../current/customer_attraction/eight_customer_cce_welfare_gap.md)、[十三客户原证明](../../current/customer_attraction/worst_cce_welfare_counterexample.md)。发现分支原稿在research/workspaces/customer-attraction/R-fc3359276dfd40798e003ae879bde525/security_game/independent/iid_strong_bridge_status_correction.md。

并发来源记录：远端ab8dc9fd也独立修正同一强iid开放状态；合并时保留其相同数学结论，与本页较完整显式计算及独立审查合并，未将此简单推论宣称为新实例或新颖结果。
