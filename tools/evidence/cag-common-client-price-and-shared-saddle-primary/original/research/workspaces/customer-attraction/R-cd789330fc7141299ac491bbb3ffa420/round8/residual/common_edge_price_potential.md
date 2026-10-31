# 可选 common-future 边的价格势：精确合同与未证 IC 付款

2026-10-24，residual8。root 提出在 inventory8 密度核与旧捕获核之间加入可选 common 边，本页从陈述独立推导其价格势。适用任意人数、一般有限共同目录及每份完整历史纯 SPE。**一般 HALF、角色共同容量仍 OPEN。** 本页不给新的共同容量不等式；价格递推不可充当付款证明。

## 1. 同一 R-only 图的局部选择

固定 actual B、R=O\union(B)，先将 I 按既有合法接口直接支付。保留 inventory8 的加强初始化和逐客户质量。一个 natural context t 当前角色 i、规定叶 V、动作 a，actual-prefix reset 叶为 A。对输入客户 x∈R∩a，置

    c=c_A(x), r=|cover_A(x) intersect cover_V(x)|,
    N=cover_A(x)\cover_V(x),
    M=(cover_A(x) intersect cover_V(x))\{i}.

R 无 actual past coverer，故 N、M 都只含未来角色，且 |N|+|M|+1=c、|M|+1=r。mandatory new 边 j∈N 各发 h_tx/c；common 边 j∈M 可以发 α_tjx h_tx/c，0<=α<=1。current 留下

    L_tx=h_tx[r-sum_(j in M)α_tjx]/c.

故 h_tx/c<=L_tx<=h_tx r/c。α=0 是 inventory 的 raw difference kernel；α=1 是 round3 uniform-reset 捕获流。客户、真实 future context 和严格角色 DAG 均保留；它不是原 full-profit SAFE/CLIP。

## 2. 任意选择仍有密度与一次完整 IC

同一非 actual 目标 t 的所有 reset 父节点仍在其首次 actual 差异角色 k。每条父贡献乘目标负载后不超过父 h_sx（mandatory 恰等于，optional 再乘 α<=1）。所以 inventory8 的同角色反链证明原样给

    c_Vt(x) h_tx<=p_kx+sum_(owner<k)a_owner,x<=1.

并且 current 不比 α=0 更大。用 f=c_Vh、D_x=1/c_A，r<=c_V 有

    sum_x L_tx<=sum_x f_tx D_x<=sum_xD_x=D_(i,a)<=u_i.

最后一步只调用一次原 actual-prefix 完整 IC；没有对 x 加权调用 IC。不同 context 同角色的 current 和仍未被这个单节点界控制。

## 3. 固定角色价格的最小费用势

给实际角色非负价格 λ_i。对每个 (t,x)，令 ψ_t(x) 是该同质线性流从此处出发的单位成本系数，即其最小最终实际角色价格；这不声称可向任意 context 独立注入一单位并保持 source/IC 密度合同。未来角色严格增加，反向递推唯一确定它。令 child(t,j) 为 A 中角色 j 的真实 prescribed context，则

    ψ_t(x)=[λ_i
            +sum_(j in N)ψ_child(t,j)(x)
            +sum_(j in M)min{λ_i,ψ_child(t,j)(x)}]/c.   (PRICE-DP)

证明：mandatory 边固定。每个 common 边增加 α/c 份未来价并减少同量 current 价，故在 ψ_child<λ_i 时取 α=1，在 ψ_child>λ_i 时取 α=0，平局任意。各边的选择独立，且 §2 的合法性对所有选择同时成立，所以可一起采用这些端点。current 的单独一份给 λ_i/c，其余 common 份选择 current 或 future。

对同一固定初始化，最小总代价为 sum_(initial t,x)b_tx ψ_t(x)。望远镜只使用该同一守恒 DAG；没有把不同 λ 的最优路由相加。角色容量可行性可用有限凸流集合的分离写成所有 λ>=0 的相应价格条件，但这只是等价优化接口。

特别，λ_i恒为1时 PRICE-DP 给 ψ_t(x)恒为1。于是价格条件恰为

    total unpaid source <= total actual residual budget.

与初始化合计后就是 OPT<=2W。**这说明价格递推没有自行证明总资金 inequality；不能将 λ=1 的待证条件隐藏在对偶中。** 本页也未证明任何来自真实 off-history IC 的新上界以支付一般 λ 的 source 势。

## 4. 真正需要新增的关系

反向 off-history query 是 finish_sigma(g,B_i)，与 actual-prefix reset finish_sigma(B_<i,a) 不同。其真实 IC 只给 prescribed profit>=return profit；rectangle 中的 off-slack 是非负优势，不能当作免费退款。若要从 PRICE-DP 推出共同 cap，必须把这些真实 return 叶的实际 C/G 抵押，与同一初始 source 和同一价格势共同付一次。

没有找到所需的一般 inequality。未进行新的有限扫描，也不因路由族更大或对偶更短提高 HALF 状态。
