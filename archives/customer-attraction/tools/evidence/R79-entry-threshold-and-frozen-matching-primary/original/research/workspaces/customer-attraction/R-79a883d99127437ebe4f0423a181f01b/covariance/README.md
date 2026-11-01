# 续局协方差的逐客户边界

当前目标仍为一般 Q-CAG-HALF，状态 OPEN。

- `customerwise_covariance_boundary.md`：四客户完整 SPE 严格否定逐客户残余负载单调与逐客户额外槽债务非正；同时给全部决策严格的七客户版本。它们不反驳一般 half 或 aggregate/full-menu 候选。
- `audit_customerwise_covariance.py`：不导入求解器的 Fraction 定义级核验，检查全部历史和精确协方差。
- `test_pushforward_cone.py`：根提出的全 p 额外槽推送总额候选的两个既有完整策略锥测试，无违反证书，不作一般结论。

下一步仍需真实多后继 IC 的跨客户总支付；一后继恰由最后玩家 BR slack 与碰撞折扣支付，不能逐客户分开或将整组后继冒充一个可行动者。
