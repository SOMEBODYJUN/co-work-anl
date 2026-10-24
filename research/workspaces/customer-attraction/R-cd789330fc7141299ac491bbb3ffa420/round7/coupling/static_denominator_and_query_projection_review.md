# 静态分母 off-IC 分解：盲重构与 synthetic-profit 合法化接口

2026-10-24，coupling7。收到 global_budget7 的精确合同（对象、公式、支持域和 closure 异议）后，**未读其证明正文**完成下列重构。一般人数、一般有限共同目录、每个完整历史纯 SPE；Q-CAG-HALF 仍 OPEN。本文不声称新颖性，不把有符号身份或合法域表示当共同容量证明。

## 1. 收到的合同

实际终局为 Z=(S_1,...,S_m)，实际收益 u_i。natural context t=(g,i) 的规定叶为 B=finish(g)，当前规定主题 a，收益 v=u_i(B)。在同一个 g 强制改选实际主题 S_i 后完成真实叶

    W=finish(g,S_i),  z=u_i(W),  ell=v−z>=0.

对 x∈S_i，定义

    d_x=c_B(x)+1−1_(x∈a),
    theta=sum_(x∈S_i)1/d_x,
    T_B=sum_(x∈S_i,j≠i) [1_(x∈B_j)−1_(x∈Z_j)]/(c_Z(x)d_x),
    T_W=sum_(x∈S_i,j>i) [1_(x∈W_j)−1_(x∈B_j)]/(d_x c_W(x)).

合同恒等式为

    u_i=v−ell+T_B+T_W.                            (SD)

它保留原 off-history 整条 IC 的有利负号 −ell，而没有把 current prescribed a 与实际 S_i 的客户拆权比较。

## 2. 独立推导与逐边利润界

因为 x∈S_i，c_Z(x)>=1。d_x=1+sum_(j≠i)1_(x∈B_j)>=1 是把 B 当前行动换成 S_i、但暂时冻结 B 其它行动的静态分母；它不是新 SPE。

逐客户有

    1/c_Z−1/d = (d−c_Z)/(c_Z d),
    d−c_Z=sum_(j≠i)(1_Bj−1_Zj),

因此 u_i=theta+T_B。另一方面 W 与 B 保留同一个过去 g，current 在 d 中已经替换成 S_i，故

    c_W−d=sum_(j>i)(1_Wj−1_Bj),
    1/d−1/c_W=(c_W−d)/(d c_W),

即 theta=z+T_W。代入 z=v−ell 得 SD。

第一项的正 recipient j 具有 B_j 覆盖 x、Z_j 不覆盖 x。此时 c_B(x)>=1 且 d_x>=c_B(x)，故

    1/[c_Z(x)d_x] <=1/c_B(x).

把一条 j 边中所有相应 x 求和，第一类正边金额 q^B_j<=u_j(B)。第二类正 recipient j>i 具有 W_j 覆盖 x、B_j 不覆盖 x；因 d_x>=1，

    1/[d_x c_W(x)]<=1/c_W(x),

所以第二类 q^W_j<=u_j(W)。这些是整条边被该叶同角色完整利润支配的计数关系；不是该利润已在原实际钱包中有库存。

若 B=finish(Z_<k,A_k) 是一次 actual-prefix query 产生的单重置叶，则第一类 j<k 的差为零；j=k 是强制 query 角色，其分支利润受原 actual k 行 IC 支配；j>k 的 B_j 确为 B_<j 上的 prescribed 行动，B 是该 natural context 的 prescribed completion。所以第一类可有合法 backward natural 目标 k<j<i。第二类 j>i 是 W 的真 prescribed 后继，也合法。

但是进入 W 后，再对一个更晚 natural context 使用 SD，其规定叶可带两个旧强制动作。此前 j<i 的 W 利润未必是该 j 的真规定 completion；不能沿用一次重置域，直接把 q^B_j 当作 true IC 左边。这个直接 closure 异议成立。

## 3. 一般 synthetic profit 的 query-projection 接口

下面给一个可选的额外合法化层。它只处理上述 synthetic 叶利润的域，不声称 SD 新网络的总质量或容量已解。

**QUERY-PROJECTION（coverer 恒等式的一般用途）。** 固定任何合法完整行动叶 F，不要求沿原 sigma、SPE 或仅含一次强制动作。固定角色 j，写

    h=F_<j,  a=F_j,  v_F=u_j(F),
    R=finish(h,a),  d=u_j(R),
    B0=finish(h),  V=u_j(B0)>=d.                 (true IC)

R 是同一个原 sigma 在 h 下强制 a 的真 query 完成叶，B0 是 h 的真 prescribed 完成叶。对 x∈a，定义其它 coverer 集

    J_F(x)={l≠j:x∈F_l},  J_R(x)={l≠j:x∈R_l},
    q_l=sum_(x∈a:l∈J_R(x)\J_F(x))1/[c_F(x)c_R(x)],
    P=sum_l q_l,
    N=sum_(x∈a)|J_F(x)\J_R(x)|/[c_F(x)c_R(x)],
    J=sum_(x∈a)1/[c_F(x)c_R(x)],
    L=sum_(x∈a)|J_F(x)∩J_R(x)|/[c_F(x)c_R(x)].

F 与 R 的前缀 h 和当前 a 完全相同，因此 q_l>0 **只可能有 l>j**。逐客户 coverer 差给

    v_F=d+P−N,
    d−N=J+L>0 (a nonempty),
    v_F=(d−N)+sum_(l>j)q_l.                    (PROJECTION)

于是 v_F>0 时，单位 synthetic 利润质量可作一个守恒非负分裂：

    current amount (d−N)/v_F,
    future amount q_l/v_F to each l>j.

current 金额 d−N 可按系数

    alpha=(d−N)/V<=1

送入真正 prescribed natural context (h,j) 的完整利润 V。这里既没有把 F 当作该节点的 prescribed leaf，也没有把 a 当作规定行动；V>=d 是原 h 上“规定动作对 a”的**整条合法 IC**，其系数 alpha 是一个非负常数。future l 的目标为 (R_<l,l)，其 prescribed completion 确为 R，且 q_l<=u_l(R)。

若按利润质量实现路由，输入 w v_F 时，以 w(d−N) 注入真 current context，以 wq_l 注入真 future contexts；三种量都使用同一 w，质量恰守恒。相应 current 真利润系数是 w alpha<=w。若实际实现随后把这些自然输入交给 full-customer SAFE 图，必须将所有相同 context 输入相加后重算同一份 beta，不得为 projection 另领 actual 钱包。

a 为空时 v_F=d=P=N=J=L=0，接口为零；a非空则 d>0，SPE使 V>=d>0，所有分母合法。past 的 F/R coverer 完全相同，所以此额外层没有新 backward 边。对 forced 当前 a 也成立，因比较是在原合法历史 h 的真实 query 子枝上进行。

**这是域闭合，不是费用下降。** 将 v_F 形式改写成 alpha V+sum q 后，future 的利润系数 q_l/u_l(R) 可能同时出现多条，且它们后续又可能走 SD backward 边。此接口虽只向同角色/未来送，整个扩展网络仍可能有环，未证明可吸收、净质量非增、有限总 IC 系数或 actual cap。SD 的 signed T 项亦尚未成为一个守恒正 kernel。不能把 PROJECTION 的局部守恒说成整个 SD 递归已经守恒。

## 4. 与主线的准确连接

若后续 SD 网络确实只因“backward 目标含未来强制 query”而不合法，可以先把该叶同角色利润视为 synthetic 状态，再用 QUERY-PROJECTION 送回原 sigma 的真 current/future 规定 context。这样不会直接调用 forced-future 过去玩家的假 IC。

但整个网络还需同时解决原 SD 的正负总额、循环、共同实际支付和 off-history slack 的一致归属。本文没有给任何这些全局关系；仅确认 SD 恒等式、单重置 backward 域，以及一个可供后续审查的局部真 query 投影。

## 5. 投影 PRICE、源时间与不能自动继承的 HIT

root 从精确陈述独立重构后指出：PROJECTION 的 current 金额 J+L 逐客户为

    [1+past_common+future_common]/(c_F c_R),

所以每个 future q_l<=J<=J+L。以 v_F 归一化，synthetic→(current natural/future natural) 这一层仍在“包含 current j 的 uniform-subset 行”凸包中；这是角色层 PRICE，没有 contraction/cap 推论。

若 synthetic F 保持 F_<k=Z_<k 且其待投影角色 j>=k，则 true prescribed current h=F_<j 仍在 k 前匹配 actual；R也保留该前缀，所有 projection future 角色大于j。因此它保持 fresh 源的时间下界。SD 的第一类正边亦不可能到 j<k（那里 B_j=Z_j），第二类只到未来。故这些局部支持变换均保留“最终实际角色不会早于源 k”的候选不变量；但要谈最终角色仍须先得到一个真正守恒可吸收的整体网络。

旧 GLOBAL-HIT 不能仅凭每个新增层也有 PRICE 便套用。原 SAFE 行的 current 输出是实际终端；对目标集 K 外的 current，该项的 K 命中值为0。这里 current 输出进入同角色的另一个 natural context，其后续命中值可能只是已知<=h，代替0会使原归纳不闭合。抽象地，先以1/2落同角色继续、1/2送某目标，再在同角色续层以1/2终止、1/2送同目标，最终目标质量为3/4；两个局部层各自都满足二元 uniform-subset 合同。真实 coverer 约束是否禁止某些这样的合成，须另证；仅有 PRICE 不足。

## 6. 保留第一类正边的 SD 反向非负 kernel：root合同独立核查

root收到 STATIC-COLUMN 的 ROW 后提出下面的精确合同；本节从公式独立核查，不读取另文证明。对同一SD行，设 P_B,N_B 是 T_B 的正负总额，P_W,N_W 是 T_W 的正负总额，则

    u_i=v+P_B+P_W−F,
    F=ell+N_B+N_W>=0.

ROW 已证 P_B<=u_i。故定义 r=u_i−P_B>=0，得到

    r=v+P_W−F.                                  (REVERSE)

只在第二类 W未来正边中删除总金额 c=min(P_W,F)；其余正子边可以任意固定选择，所需总额总能由原正容量实现。相应退款由 F 变为 F−c，当前 prescribed B利润净金额为

    v−F+c=min(v,r)>=0,
    P_W−c=(r−v)_+.

因此得到精确非负金额分裂

    u_i=P_B+min(v,r)+(r−v)_+.                    (REVERSE-KERNEL)

- 第一类正边 P_B原封保留，仍享有固定parent B的 STATIC-COLUMN / ROW共同容量；
- current金额 min(v,r)送入真 prescribed B-context，其完整利润系数 min(v,r)/v<=1（零量按零）；
- 第二类 W未来正边只保留原容量的子集，总额(r−v)_+，其目标仍为W中的真实规定后继；
- 第一类若处于多次强制历史导致synthetic目标，仍需第3节QUERY-PROJECTION或其它联合prefix接口，不能直接叫真natural。

核查分两例即可：若r>=v，则 F<=P_W，删F、当前留v；若r<=v，则 F>=P_W，删全部W正边、当前留r。不要求F<=v；这正是先用 ROW 预留P_B后再取消W正边的作用。所有负项与ell只参与同一行F一次，不能随后再另领退款。

**正性/域结论通过，付款方向仍须保持。** 这是以原实际利润u_i为输入、将质量送往off-history利润的反向kernel。它没有把off-history客户源送回原actual钱包，所以仅有此分裂并未证明fresh源已付或half。current输出是另一natural节点，既不是实际终端也未证明全图PRICE/HIT；合并projection及SD递归可形成同角色/反向循环。没有一般吸收、有限累计IC系数、cap或福利结论。
