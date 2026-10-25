# 自由共同背景直接优化覆盖对偶：候选与真实停点

2026-10-25，round2/sharedload。范围是任意有限单位客户、任意非空有限共同目录、任意人数、每份完整有序历史纯 SPE，含空主题、重复行动和任意平局。Q-CAG-HALF、SHARED 及其保留 Qstat 的 half 付款均仍 OPEN。本文没有新的无条件一般福利界。

本页不重算已经独立检查的共享 t²-KKT/Bregman 恒等式，也不将 Cov 政名后当成新增银行。它记录一个比“在 gamma 的极小背景付款”更自由的充分候选，并检查为什么它没有自动继承原非负曲率。

## 1. 真正改变优化目标的较弱充分条件

固定完整 SPE 的实际路径。沿原策略在实际位置 i 强制 B 后删当前槽的真实负载是 ell_i(B)，令

    K=(1/m) sum_i conv{ell_i(B):B in catalog}.

对任意 L in K 定义

    t_x(L)=1/(1+L_x),
    gamma(L)=max_(T in catalog) sum_(x in T)t_x(L),
    T(L)=sum_x L_x/(1+L_x),
    J_m(L)=m gamma(L)+T(L).

每个比较 m 元组 (T_1,...,T_m) 的并集 C 满足一般静态上界

    |C|=sum_(x in C)[t_x+L_x t_x]
       <=sum_j sum_(x in T_j)t_x+sum_x L_x t_x
       <=J_m(L).                                      (COVER)

因此下面是真正足够原 half 的全输入候选：

    min_(L in K) J_m(L) <= 2W.                         (COV-K?, OPEN)

它允许 gamma(L) 略增而 T(L) 减小；不要求 L 先最小化 gamma。该自由度不能通过在固定 gamma 极小点重选菜单分解获得，因为 J 取决于共同负载本身。

在任意背景设 Q(L)=(m-1)gamma(L)-T(L)>=0，则 J=(2m-1)gamma-Q。若父方 gamma 极小点 L* 已能支付

    2W >= (2m-1)gamma(L*)-Q(L*),

当然也支付 COV-K。反方向未证明；这里的“较弱”指允许更大的背景选择域，不宣称已经找到一个原模型 SPE 严格分开两者。COV-K 也不等价于原 half：COVER 本身可以有静态松弛。

## 2. 直接覆盖目标的变分权重变了

设 L 是 J 在 K 的局部极小点。令 p 是某个支撑于 gamma(L) 的活跃 whole themes 的分布，rho_x=Pr_p[x in A]。有限个光滑函数之 max 的一阶必要条件，可由方向锥分离写成存在这样的 p，使

    w_x=(m rho_x-1)t_x^2,
    w dot (Z-L)<=0 for all Z in K.                    (J-KKT)

从而实现 L 的每个菜单支持列 ell_i(B) 最大化 w dot ell_i(B)。这是必要条件，既不声称 J 全局凸，也不声称它足够保证全局极小。

与原 SHARED 的 rho t² 权重相比，这里额外减去 t²。客户 rho<1/m 的梯度权重可以为负；这些客户增加背景会增加覆盖对偶的 T 成本。因此不能直接拿原共享极小点的列支持作为 J 的最优支持，也不能将原 D 全部作为本目标的非负曲率。

对固定 p，令

    J_p(L)=m F_p(L)+T(L)
          =sum_x [1+(m rho_x-1)/(1+L_x)].

逐客户精确展开是

    J_p(Z)-J_p(L)
      =-sum_x (m rho_x-1)t_x²(Z_x-L_x)
       +sum_x (m rho_x-1)t_x²(Z_x-L_x)²/(1+Z_x).       (J-TAYLOR)

第二项有符号。使用 J-KKT 后免费删掉它，是无效的；只在全部承重客户 m rho_x>=1 时才有该固定 p 的全域凸性。后一个条件本身不由完整 SPE 或活跃查询等价关系推出。

这不只是表达式中看见一个负系数：在一般合法分数背景域上 J 确实可以严格凹。对每个 m>=2，取合法目录 A、B、空主题，其中 A、B 恰共一个客户，|A\B|=m+2、|B\A|=m+1。背景

    L_s=s 1_B+(m-1-s)1_empty,  0<=s<=m-1

有合法总质量 m-1。A 始终是唯一活跃查询，因此

    gamma(L_s)=m+2+1/(1+s),
    J_m(L_s)=m(m+2)+(m+2)-2/(1+s),
    d²J_m(L_s)/ds²=-4/(1+s)^3<0.

这是只针对“直接 J 目标自动凸”的全人数解析反证；这些背景没有声称是同一个原 SPE 的 K。因此它不反驳 COV-K，也不反驳在真正菜单域上可能存在的额外曲率关系。

## 3. 保留最优并集的全部静态信用

在任意 L（包括原 gamma 极小点）固定一个最优比较元组，令 n_x 是该元组覆盖 x 的次数、C 是其并集。四项静态松弛均非负：

    Q=(m-1)gamma-sum_x L_x t_x,
    P=sum_j[gamma-sum_(x in T_j)t_x],
    O=sum_(x in C)(n_x-1)t_x,
    E=sum_(x notin C)L_x t_x.

并有精确式

    OPT_m=(2m-1)gamma-Q-P-O-E.                         (OPT-EXACT)

因此父方 Cov 总账若保留其 KKT 银行 G，则准确的较弱充分付款可写为

    Cov <= I+G+D+(gamma+Q+P+O+E)/2.                   (OPT-PAY?, OPEN)

若使用已把 G 吸收到 C 的父稿记号，则同式为 C<=I+D+(gamma+Q+P+O+E)/2。这里 P、O、E 是 COVER 的真实静态松弛；本式没有证明任何 Cov 金额界，不能当作新增全树付款。对不同最优元组可重选这些静态松弛，但其和由 OPT-EXACT 固定，单独换最优元组不会增加总信用。

## 4. 一个真实但较弱的实际末位界

下面只需要 K 含实际删槽列及真实末位 BR，因而对全部原模型输入成立。它不是 half 闭合。

对原 gamma 极小背景的 saddle (p*,L*)，设 c 是实际负载，S_m 是实际末位主题，alpha=(m-1)/m。实际删槽列平均给 alpha c in K，因此 m>=2 时

    gamma=F_p*(L*) <= F_p*(alpha c)
        <=m/(m-1) d_m(p*) <=m/(m-1) u_m.            (LAST)

第二步逐客户使用

    1+alpha c >= alpha(1+c-1_(S_m)).

准确保留差额可写为

    gamma <= m/(m-1)u_m-B_last,

    B_last=sum_x rho_x *
      m[1+(m-1)1_(x in S_m)] /
      [(m-1)(c_x+1-1_(x in S_m))(m+(m-1)c_x)] >=0.

仅当 rho_x>0 才需该分式；此时若 x in S_m，则 c_x>=1，分母正。rho=0 的项按零计。末位 whole IC 的松弛还可以一并保留：精确关系用 m/(m-1)d_m(p*) 替代 u_m。这里没有按客户重加权 IC。

LAST 的局限是 u_m 不一定是实际最小利润，不能将 u_m 替换为 W/m。B_last 是同一个实际末位 whole-query 上界的减项，不能在已经使用该上界之后再重复花费。

## 5. 五人代入和执行停点

同一一般候选在 m=5 直接是

    min_(L in K)[5 gamma(L)+T(L)]<=2W.

原 gamma 极小点版本是 2W>=9gamma-Q；保留固定最优元组的全静态松弛则为 2W>=9gamma-Q-P-O-E。没有这些未证的金额付款，不产生任意目录的无条件 OPT_5<=2W。

当前真正未付内容没有变化：原 t² 下后继 law-of-demand 留下的 r_beta 漂移与不同真实后继重置，尚未由一份实际 W、IC 或静态松弛共同控制。改成直接 J 目标时，新增可选背景的同时失去非负 Bregman 曲率，故没有得到一个已证的更便宜付款。

本次未作有限负例扩样、外发、git 或共享正文修改。没有宣称新颖性、独立审查、一般半覆盖证明或目标反例。
