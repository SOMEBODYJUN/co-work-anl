# exchange9 的两项独立定义级审查

2026-10-24。内部数学审查，无外审或新颖性认证；无新扫描或重新枚举。Q-CAG-HALF 仍 OPEN。

## global9 的最优组合交换曲线

已读 [optimal_exchange_curve.md](../global/optimal_exchange_curve.md)，独立检查 EX-t、EX-q、EX-H、EX-1，全部通过。

固定客户的 k 个最优覆盖槽与 c 个替换覆盖槽。随机槽双射下，前者的 k 个逆像是均匀 k 子集；它们避开 c 个实际覆盖槽的概率准确为 binom(m-c,k)/binom(m,k)。避开后，两组槽互不相交，iid 选择所需的 k 个选中及 c 个不选中事件概率是 t^k(1-t)^c。因此 EX-t 没有把一般事件误当独立；所需不相交已先显式条件化。

固定 q 时，选中的实际 q 子集与所替换的最优 q 子集确实独立均匀。损失概率是 P(全部 k 个最优槽被替换)×P(c 个实际覆盖槽均不被选)=binom(m-k,q-k)binom(m-c,q)/binom(m,q)^2，正是 EX-q。条件在总选中数 q 后，匹配实验具有这一分布，所以 EX-t 为其二项混合。

积分 dt/t 给左侧 H_c，右侧 Beta(k,c+1)；k>=1 消除了 t=0 的不可积风险。EX-1 一阶项仅来自 k=1，其系数是 (m-c)/m。t=1 得 |E|<=|R|。重复主题、空主题与任意叶均适用。作者正确标为静态最优性关系，没有使用 SPE 或支付遗漏，也没有推出一般/五人 HALF。

## credible9 的根菜单恒等式与背景域后果

已读 [root_covariance_and_background_domains.md](../credible/root_covariance_and_background_domains.md) §1、§3，并核对旧 [PB 构造](../../round5/menu/pair_attack.md) 的 r 槽静态安全定义及 UNIVERSAL-S 来源。未重审旧构造所有策略段或重跑数值；本审查只核本轮代数与量词推论，全部通过。

令 d_ax=b_x+1+k_ax。逐客户 1/(d_ax+alpha_ax)=1/d_ax-alpha_ax/[d_ax(d_ax+1)]。独立 t,a~p 给 C_x=p_x E_a(1/d_ax)-p_x E_a(alpha_ax/[d_ax(d_ax+1)])。从 D_x=E(alpha_ax/d_ax) 减去它，恰为稿中 covariance 加非负 self_refund。协方差为整行定义恒等式；根 IC 仅用于 u-D(p)>=0，没有客户重权 IC。ROOT 正确。

旧 PB 的查询 p 对每个静态 B in S^r 都有 E_p f_B>=s>u；真实首分支 Z(a) 也有恰好 r 个目录槽，因此对每列 a 同时有 E_p K(t,a)>=s。故 C(p)>=s>u>=D(p)，同时否定任意合法背景的 SELF 及弱 C(p)<=u。对任意列分布 Q，max_t E_QK>=E_pE_QK>=s，也确实否定该域自由 Mfull<=u。

槽数准确：K 为一个额外查询加完整 r 槽；没有误用 r-1 槽。背景由 singleton 合法前缀实现，但未证该前缀位于根 SPE 实际路径。因此推论不能扩为零背景根、实际前缀专用 Mfull 或 Mpath 的反例。稿中保留这些区别。

旧34数据算术相容：-9/100+19/600=-7/120，29/30-41/40=-7/120，29/3-29/30=87/10。这里只核相互代数一致性，不冒充重验旧完整证书。
