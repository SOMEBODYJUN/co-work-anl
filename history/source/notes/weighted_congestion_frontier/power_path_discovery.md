# R2 原始机制记录：共享 power 乘子与两尺度路径

2026-10-14；作者为 R2 主对话及内部 dense_scales、path_obstruction_review、bridge_review。
这是本轮独立研究的机制来源记录，规范完整证明在 research/current/weighted_congestion_frontier_power_bridge.md。

原义务是把每资源稀疏谱 power-cost 势与近等权排序离散积分拼接。排序缩放需要更强的最小权下界；只用玩家权除跨度的下界会失去共享乘子归一化。

攻击同资源 dense 尺度时，一重 n 轻的线性费用两路径预算分别为 1+n epsilon^p+Q 与 1+n epsilon+Q，Q=epsilon^(p+1)n(n+1)/2。固定 p<1 的无界 ratio 说明这个共享乘子接口已经在线性费用失败；此并非游戏均衡反例。

两成员在先重构的干净上下文中独立得到同一 C1 分片二次势：按乘子密度 q=h/w 的比 D，在负载线 x=sqrt(D)y 上拼接两个二次表达式，再加一半逐玩家 h_i w_i 自项。其边际统一因子 sqrt(D)，由两个 dense 群的路径极限证明跨人数最优性。

主对话另外用浮点 LP 探查有限计数矩形；诊断值被更小终集的精确路径预算解释。没有保存未经有理可行证书认证的有限 LP 最优性命题。全部普遍量词来自一般证明，有限审计只作所列范围证据。
