# round6 credible：actual coupon 非负净化

2026-10-24。复用同 actor，接续 round5 全 fresh / 全客户消元。只攻任意 m、任意目录、全部有序历史纯 SPE 的一般 HALF，仍 OPEN。不 Git，不改 round4/5 或共享文件。

[安全退券与利润差剪枝](safe_coupon_netting.md)：root 独立重构与shared独审均通过；past正券保留实际标签。正recipient可剪到(v−u_i)_+，当前净支付min(v,u_i)。该选择局部最少传播，新正券负载逐点不大于原gross负载；不比较旧net，不称cap1/cap2。亦可接relay仅fresh利润分母，所有退款来自同一actual整行。无外审或新颖性认证。

真正未付是净券共同容量，不是负项如何假配给旧角色。root 的 O 全 owner 源 cap2 与仅 fresh 分母路线可并行；不得把任何正表示升级为 HALF。

正文§6另补 root 独立重构的 role pooling：past 标签验证 actual 域后，正金额可在同角色按原实际份额比例分配，不调用过去 IC。全 O 初始化及净化的角色总额 A_j 若满足 A_j≤2u_j，即足以证明 HALF；固定客户券 cap 是过强接口。该 role cap2 仍未证明，负 q 仍须原地 SAFE 处理。
