# 最晚 NET 出口仍不自动给同角色总密度一

2026-10-24，credible8。此处检验一个明确的一般**结构候选**，不是研究固定人数正面命题，也不声称找到 Q-CAG-HALF 反例。候选如下：

> 一个 fresh 客户的一单位 source 在其初始 query 全体 coverer 间均分；以后保持客户标签，在每个 natural context 对同客户正负项作 NET，保留时间最晚的 (c_A−c_B)_+ 个新 reset-coverer。是否无需其它 IC，就有每个角色的全部 incoming 密度和<=1？

答案为否。失败只在任意策略/合法前缀几何层，不满足完整 SPE 已认证条件；它不排除真正 off-history IC、其它 NET 选择或其它共同支付能给一般 HALF。

## 1. 精确结构见证

角色采用 0,...,8 编号，一个 fresh 客户 x 在实际叶所有角色都不覆盖。原 source owner 为0。其初始强制 query 规定叶的 x-coverer 集为

    V0={0,1,8},  c_V0=3.

一单位 source 给 owner0、natural role1 和 natural role8 各 1/3。role8 的这一份 incoming 密度为 (1/3)·3=1。

role1 的原 profile 仍是 V0。它的 actual-prefix reset profile 的 x-coverer 集取为

    V1={1,2,3,4},  c_V1=4.

正新 coverer 为 {2,3,4}，负消失 coverer 为 {0,8}。同客户 NET 消掉两个正价，保留时间最晚的新 role4。于是它收到

    h_4=(1/3)/4=1/12.

role4 的原 profile 是 V1。其 actual-prefix reset profile 取为

    V2={4,5,6,7,8},  c_V2=5.

新 coverer 为 {5,6,7,8}，消失 coverer 为 {1,2,3}。NET 消掉三个正价，保留时间最晚的 role8，它收到

    h_8^extra=(1/12)/5=1/60.

新 role8 context 的负载为5，因此该条 incoming 密度为5/60=1/12。两个 role8 context 不同，合计

    sum_(t:role(t)=8)c_Bt(x)h_tx=1+1/12=13/12>1.

每条非终端客户路径的负载都严格增加 3→4→5；所有 query 的 actual 前缀均不覆盖 x，因此 prefix 兼容。初始未来 coverer1、8也均是 actual 主题未覆盖 x 的 new-to-role 支持。各步 outgoing 是原正边的 NET 子容量；没有新造 source，所有 source 质量保持守恒。

可以给不同规定动作使用不同目录标签以区分所需 query；本文只规定客户 x 的 coverer 几何，不补造使全部离轨选择最优的其它客户。因此**不是**一个完整 SPE 实例。不能从这里推出纯 SPE 的相同 density 候选失败，更不能推出 half 失败。

## 2. 精确计算的地位

[attack_latest_net.py](attack_latest_net.py) 用 Fraction 动态规划，针对上述一般候选，在允许任意 actual-reset coverer 集的结构松弛上最大化固定角色 incoming 密度。它不是 SPE solver，也不读写旧证书。每个状态 (V,i) 的 outgoing 仅取时间最晚的新 coverer，按 h/c_A 传递；目标 role 的边际值为 c_V h。给定 profile 后的所有分支都保留，非单路径抽样。

[latest_net_attack.json](latest_net_attack.json) 冻结这次精确分离。更小范围未分离只作搜索经过记录，不是任意规模正面证据；证明候选失败的是上节可直接手算的 13/12。

这个诊断指出：保留 source 客户标签、同角色 antichain 的金额库存、逐节点 density<=1、NET 的逐客户负载递增，连同最晚出口选择，仍不足以自动给同角色跨 context 的密度总和。需要真正使用可生成 SPE 的额外 IC 或更强路由选择。它没有否定存在其它合法共同路由。
