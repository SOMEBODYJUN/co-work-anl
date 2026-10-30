# uniform NET-cap 下交叉尾部对称化的准确代价

2026-10-25。任意人数、共同目录、完整历史；HALF OPEN。
保存 raw uniform NET-cap 的局部一般关系，没有新的全局付款。

## 1. canonical M 的计数不变性

同计数有序历史的未来游戏同构：过去行动固定，未来效用只依赖过去计数。
因此 canonical threshold M(h)=M(b_h)。这不要求原 sigma 在这些历史选择同尾，
也不把旧对偶的 lambda_h 误作相同。

## 2. 交叉记录及对称混合

固定根角色 i、前缀 h、同一有序中间序列 z、主题 A,A'，取

    y1=(h,A,z,A',tau1),       y2=(h,A',z,A,tau2).

记根/当前利润为 r1,c1 和 r2,c2。两处都以一半权重用 tau1、一半用 tau2，
新的根利润和与当前利润和均为 (r1+r2+c1+c2)/2。
完整负载的两处合计分布不变，deleted-root shadow 总和也不变。
允许 tau1,tau2 为任意 raw 尾部，不声称混合是纯 SPE。

## 3. 净 cap 的变化

令 B_i=d_i+sum_(k>i)[M(z_<k)-u_k]。
混合不改变中间及当前的 M 项；当前之后两前缀计数相同，任一给定尾部的
descendant M 项相同，故混合后的 descendant M 总和准确保持。
固定中间角色与尾部角色的合计利润也保持。
根利润增加半差额、当前利润减少同一半差额，故

    Delta[sum_pair B_i]=c1+c2-r1-r2.                  (NET-TRANSFER)

它是旧进入根 cap 半差额的两倍。全部 raw 域消除了 child-SPE 可实现性门，
但没有免费满足全局 NET-cap；这个带符号变化仍须明确付款。

若 tau1,tau2 是原 sigma 的真实 cross-child 尾部，当前原规定利润为 v1,v2，
则 current IC 给 c1<=v1、c2<=v2，从而真上界为

    Delta[sum_pair B_i]<=v1+v2-r1-r2.                (NET-IC)

跨根 v1,v2 不能换成实际路径 u_j，也不能逐对取正部后重复源银行。

## 4. 统一 dual 定价与未付项

若 r_i=eta_i+mu B_i-w·ell_i>=0，mu>=0，则概率和 shadow 保持给

    Delta[sum_pair r_i]=mu(c1+c2-r1-r2).

这是同一 multiplier 的合法定价，不是新银行。
若原 pair 在 selected Q 正支持，原 reduced costs 为零，则 mu>0 时该 cap 变化
必须非负；这是 extremality 的限制，不是付款。
若变化<=0，修改不增 global cap 并保持 shadow，因而可行；一般没有该符号。

未完成的是把一组保守 pair 操作接入真实 P_i→Q_i replay，
使 NET-TRANSFER 的全部有符号变化进入同一个源 cap telescope，
并让对角 work 下降到单查询 variance/2。这里没有该联合下降。

## 5. 五人压力

m=5 不改公式；尚无总 covariance 金额或 W>=(9gamma-Qstat)/2。
没有更多域扩张、固定规模计算或目录限制。
