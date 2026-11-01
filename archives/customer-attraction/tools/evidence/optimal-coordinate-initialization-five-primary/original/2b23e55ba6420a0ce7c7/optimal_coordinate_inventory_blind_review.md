# 最优元组作 reference：逐客户源库存与受限未来输出的独立审查

2026-10-24，coupling7。root发送下述精确库存合同后，未读另文证明完成本页重构。一般人数、任意有限共同目录、每份完整有序历史纯SPE；**Q-CAG-HALF仍OPEN**。本页确认一个真正的逐客户非负初始化，而不是 full SD/half 证明。原命题与来源归 root，本组作独立合同审查。

## 1. 这里的 reference 与 actual 必须分开

固定原完整SPE，实际叶记 B=(B_1,...,B_m)，实际收益

    u_i=sum_(x∈B_i)1/c_B(x).

固定任意合法比较元组 T=(T_1,...,T_m)，并集 O。取最优元组时 |O|=OPT_m；下面库存引理本身不需要最优性。**将 SD 的 reference Z 取为 T，而不是策略实际叶。**

在原 actual-prefix B_<i 强制主题 T_i，随后跟随同一原 sigma，得到

    W_i=finish(B_<i,T_i),
    query_i=sum_(x∈T_i)1/c_(W_i)(x)<=u_i.        (WHOLE-IC)

WHOLE-IC 是实际 i 节点的一条完整合法比较；后继全部按原策略。没有把 T 当作 SPE，也不要求它的比较客户只有一个 owner。

每个 x∈T_i 的初始库存为

    p_ix=1/c_T(x),
    d_ix=c_B(x)+1−1_(x∈B_i).

因为 x∈T_i，c_T>=1；d_ix是将实际 B 的当前动作静态换成 T_i 的分母，故d>=1；W_i当前确含x，所以c_W>=1。x不在T_i时以下所有来源项记0，不定义无关零分母。

## 2. 四类有符号 coverer 金额与逐客户身份

对 x∈T_i，记

    P^B_ix=sum_(l≠i: x∈B_l\T_l)1/[c_T(x)d_ix],
    N^B_ix=sum_(l≠i: x∈T_l\B_l)1/[c_T(x)d_ix],
    q_ix=P^W_ix=sum_(j>i: x∈(W_i)_j\B_j)1/[d_ix c_(W_i)(x)],
    N^W_ix=sum_(j>i: x∈B_j\(W_i)_j)1/[d_ix c_(W_i)(x)],
    query_ix=1/c_(W_i)(x).

第一对比较 reference T 与静态 B-other 背景；第二对比较静态 B-other 与真实 W_i 后继。W_i与B在i以前一致，所以第二对只有未来 j>i。

两次 reciprocal identity 给

    1/c_T−1/d = P^B_ix−N^B_ix,
    1/d−query_ix = q_ix−N^W_ix,

即

    p_ix=query_ix+P^B_ix+q_ix−N^B_ix−N^W_ix.    (COORD-SD)

这是原 SD 在 reference=T 时、在 x∈T_i 上直接写出的版本；没有引入或逐客户拆用 off-IC slack ell。它的 whole-IC 接口只有第1节 query_i<=u_i。

## 3. pointwise ROW 保证库存非负

设 b=c_B(x)，a=1_(x∈B_i)，n=|cover_B(x)\cover_T(x)|。因 i是T-coverer，若a=1，则n<=b−1；若a=0，则n<=b。因此

    n<=b−a=d_ix−1,
    P^B_ix=n/[c_T(x)d_ix]<=p_ix.

所以可保留全部第一类正金额，并定义逐客户剩余库存

    r_ix=p_ix−P^B_ix>=0,
    r_i=sum_(x∈T_i)r_ix.

在非空来源客户上不等式甚至严格，但本构造只用非负性，不做局部常数优化。

由COORD-SD，

    r_ix−q_ix=query_ix−N^B_ix−N^W_ix<=query_ix,
    (r_ix−q_ix)_+<=query_ix.

最后一步合法，因为query_ix>=0。求和并只在此处用一次WHOLE-IC，得到

    sum_x (r_ix−q_ix)_+<=query_i<=u_i.           (DEFICIT)

不能把右边u_i拆成客户利润，或把不同x各自当作一个SPE比较；这里只是逐客户代数求和后调用同一整条IC。

## 4. 未来输出可同时满足库存与原正边容量

记

    S_i=sum_x min(r_ix,q_ix)
       =r_i−sum_x(r_ix−q_ix)_+.

DEFICIT给 S_i>=r_i−u_i，且S_i>=0。因此欲输出的总质量

    b_i=(r_i−u_i)_+

满足 b_i<=S_i。一个明确合法选择为：若S_i>0，令

    b_ix=[b_i/S_i] min(r_ix,q_ix),

否则令全部b_ix=0。于是

    0<=b_ix<=min(r_ix,q_ix),
    sum_x b_ix=b_i,
    current_ix:=r_ix−b_ix>=0,
    sum_x current_ix=r_i−b_i=min(r_i,u_i).       (INVENTORY)

若q_ix>0，把b_ix按原future正边单价比例分到各j：

    out_(i,j,x)=b_ix q_(i,j,x)/q_ix,
    q_(i,j,x)=1_(j>i,x∈(W_i)_j\B_j)/[d_ix c_(W_i)(x)].

q_ix=0时b_ix=0，令out全零。由b_ix<=q_ix，每条out<=其原q边；由b_ix<=r_ix，单客户输出亦不超剩余库存。这是两组约束的**同一个**可行选择，不是分别存在而未经耦合。

所有原输入/利益数值为有限有理数；比例选择也有理，可在给定T和完整sigma后事先固定，不是根据抽样轨迹事后挑源。

## 5. 初始化的支付域与逐客户全局守恒

每个源坐标(i,x)有精确非负分解

    p_ix=P^B_ix+current_ix+sum_(j>i)out_(i,j,x).

第一类正边目标l满足x∈B_l，因此可作带标签(l,x)的actual利润券，不调用任何过去假IC。对全体i同时使用STATIC-COLUMN（reference=T），第一类正金额在每个actual l上联合满足

    sum_i q^B_(i,l)
       <=u_l(B;(O∩B_l)\T_l)<=u_l.

current总额=min(r_i,u_i)<=u_i，可按这个总额/u_i的**一个整行系数**使用actual i利润。current_ix只是来源标签的会计分拆，不声称这些x在actual B_i中，也不按x改权该IC。u_i=0时该current总额为0，系数定义0。

future输出到j>i的真实context (W_i,<j,j)：其规定完成叶确为W_i，且每个输出客户满足

    x∈(W_i)_j,  x不在B_j.                       (NEW-TO-ROLE)

因此来源客户对接收者的原actual主题是新的；它未必在整个actual覆盖外，不能叫全局fresh R客户。此属性只在本初始化输出处保证，后续整行重采若要保留它必须另证。

每个x∈O在所有T-coverer上的p_ix总和为1。因此所有客户总初始质量恰为|O|，本分解没有重复或丢失比较客户库存。future总质量为sum_i b_i；没有把它误算为已经由current或P^B支付。

边界：T_i为空时该来源全零；m=1时无两类recipient，r_i=|T_i|<=u_i、b_i=0；若u_i=0，WHOLE-IC迫使query_i=0，而正单位客户query必正，所以T_i为空，或直接由INVENTORY得current为零。所有实际除法都限于正分母/正S_i、q_ix。

## 6. 审查结论与下一承重

**独立审查通过：** COORD-SD符号、pointwise ROW、DEFICIT正部方向、同一份库存/边容量选择、合法future context及NEW-TO-ROLE支持、零端点与逐客户总守恒均成立。

这构造同时产生两类已知实际支付和一类未付future库存。第一类P^B与current各自受一份actual钱包控制；二者合并可给初始化coupon的cap2，但future尚在外，不得把此cap2称为完整half。后续若调用SAFE、SD或投影，须接收本页同一批固定out库存并合计所有旧实际负载；不能重新领取已经支付P^B或current所用的钱。尚未证明future可由剩余容量/合法退款共同吸收，也没有新的完整福利不等式。
