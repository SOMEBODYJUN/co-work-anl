# 首偏离源主题复制：真实 off-history 的严格未来迁移式

2026-10-24，round4_general/capacity。对象始终为任意人数、任意有限共同目录、每份完整有序历史纯 SPE，允许重复、空主题及任意历史平局。**Q-CAG-HALF 仍 OPEN；本稿没有新的共同实际钱包不等式。** 本稿保存的是与源兼容的一条真实比较及其精确可用范围，不把它称作新的福利定理或已认证新颖机制。

已读 round8 的 NEW-CAP、同客户全图密度、共同线性证书及 same-action uniform-reset 去重稿，并读本 actor 的坐标 I 补余接口。它们已经解决逐 context 的客户密度与 whole-IC 合法性；这里不再证明或认领那些结论。下面改用**同一旧历史内复制首偏离源主题**，不把 actual-return 的正 slack 换名作退款。

## 1. 每个非 actual context 有唯一的首偏离源行动

固定原策略 sigma 的实际叶 B。设被同客户流到达的非实际 context 为 t=(g,l)，令 k<l 是 g 与 B 首次不同的位置，a=g_k。其真实规定完成记

    A=finish_sigma(g),       b=sigma_l(g)=A_l.

只把 a 当作这个 context 的**首偏离源行动**；它一般不再是最初 OPT owner 的 T_i。密度稿的 parent-antichain 论证说明：任何 reset-future 父节点进入这个 t，父角色必为 k，父 reset 行动必为 a；直接初始化若进入 t，owner 亦为 k。多个父历史可以不同，不能称唯一父节点。

原正边或 optional-common 边均只发送父行动所覆盖的客户，因此 t 的每个正 incoming 客户都满足

    x in a cap b.                                      (SOURCE-SUPPORT)

这是这个选择的用处：源行动 a 确实在旧历史 g 的位置 k 已经选过。若改用最初 T_i，一般没有这个性质。

## 2. 一条真实复制 IC，不新增查询钱包

在同一真实历史 g，让当前角色 l 强制选 a，之后仍沿同一 sigma：

    Q=finish_sigma(g,a),
    ell^copy_t=u_l(A)-u_l(Q)>=0.                       (COPY-IC)

位置 k 与 l 在 Q 都选 a，所以同枝均分等式给

    u_l(Q)=u_k(Q).                                    (COPY-EQUALITY)

这里 u_k(Q) 含较晚强制动作，**不能**直接当位置 k 的 prescribed-profit 钱包；COPY-EQUALITY 本身也不给 u_k(Q)<=u_k(B)。若需要将其作为完整过去利润 claim 送回 parent，必须使用已有 joint-prefix-claim pushback，且其多子枝共同列 cap 仍须另证。

令

    J=a cap b,       P=a minus b,       M=b minus a.

写 J_A=sum_(x in J)1/c_A(x)，J_Q、P_Q、M_A 类似。整条真实 COPY-IC 精确写成

    ell^copy_t=J_A-J_Q+M_A-P_Q>=0.                   (ROW)

所有项都来自这两片真实叶；没有按客户独立使用 IC。

## 3. tracked 客户上的复制响应税严格落在未来

对 x in J，Q 与 A 在 l 以前相同，当前 l 在两叶也都覆盖 x。因此 c_Q-c_A 只由 j>l 的响应改变产生：

    1/c_A(x)-1/c_Q(x)
      =sum_(j>l) [1_(x in Q_j)-1_(x in A_j)]
                    /[c_A(x)c_Q(x)].                (STRICT-FUTURE)

故 ROW 给真正的整行关系

    sum_(x in J,j>l) [1_(x in Q_j)-1_(x in A_j)]
                       /[c_A(x)c_Q(x)]
      =P_Q-M_A+ell^copy_t.                          (MIGRATION)

它把“规定行动 b 放弃源行动 a 的哪些客户”与“同一源行动的共享客户在真尾部怎样变拥挤”联系起来。与返回 actual B_l 的比较不同，tracked 源客户既没有被当前行动删除，也没有在当前重新加入；所以该客户的税没有 past 或 current 出口。

对正 incoming 客户还知 k 与 l 都覆盖 x，故 c_A(x)>=2。任一正 future 项不超过 Q 中该角色同客户利润的 1/2：

    1/[c_A(x)c_Q(x)] <= (1/2)/c_Q(x).                (HALF-COLUMN)

这**只**是逐 recipient 的同叶客户份额比较，不是全部未来角色合计的 1/2 收缩，也不是 actual u_j 的容量。正 recipient 在 Q 的 prescribed 尾部，域合法；不同 t 的 Q 仍是互斥叶。

## 4. 输入权重不能逐客户偷用 ROW

设任意 incoming h_tx>=0，只支持 J，令 f_tx=c_A(x)h_tx；NEW-CAP 全图密度给 f_tx<=1。对于任意一个整行标量 theta_t>=0，在 J 外把 f 补零，定义

    R_t(f,theta)=sum_(x in J) [f_tx-theta_t]
                         [1/c_A(x)-1/c_Q(x)].

则精确有

    sum_(x in J) f_tx[1/c_A(x)-1/c_Q(x)]
      =theta_t(P_Q-M_A+ell^copy_t)+R_t(f,theta).       (WEIGHTED)

theta_t 乘的是一次完整 COPY-IC，R 是权重与真尾重置的有符号余项。f<=1 不固定 R 的符号，也不给 sum_t theta_t<=1。

因此不能把 STRICT-FUTURE 对 tracked x 的符号，直接提升为 ROW 在输入权重 f 下的符号；也不能为每个正 x 各用一份 COPY-IC。此处的权重余项与旧 rank 水位协方差是同一类问题，未认领为新的已付信用。

## 5. 共同账与实际停止点

这一比较的新增选择是**首偏离源行动**：它保留同客户流的实际来源见证，并保证 tracked 复制税严格未来；不复述同 action 的 actual-prefix reset 合并。可以把各 t 的完整 COPY-IC 非负加权共同使用，但右侧包含：

1. 同一真实 A 中的 M_A，以及同一真实 Q 中的 P_Q；它们不是 actual C/G 库存。
2. 加权余项 R_t。
3. 来自不同源 a、不同历史的未来 Q 利润 claim。

本稿没有证明这些项与同一次初始化的 d,H,J 共同落在 actual 两份钱包内。若把 M_A 当作 actual 的空位收益，或者把互斥 Q 各领一份 actual 库存，就重复了原缺口。上述关系因此不能给 ROLE、FRESH-RESIDUAL 或 OPT<=2W。

## 6. m=5 压力测试

把**同一推导**代入 m=5，不加五人专用假设：

- l=5 时没有 future，故 J_A=J_Q，ROW 精确退化为 M_A-P_Q=ell^copy_t>=0，WEIGHTED 的 tracked 差与 R 都为0。这说明末位 b 的源外收益足够支付其放弃的源行动收益，但它仍发生在各自旧历史，未合成 actual 第5人钱包。
- l=4 时，STRICT-FUTURE 只有角色5；l=3 时有角色4、5；l=2 时有角色3、4、5。每个正 recipient 有 HALF-COLUMN，但不能把三份逐 recipient 界误加成整体收缩。
- 将所有节点相加后，尚未付的仍是跨源 M_A/P_Q 与 R_t 的共同 actual 余额。因此本推导**没有推出**任意共同目录及每个完整 SPE 的 OPT_5<=2W；也没有形成新的无条件五人常数。

`audit_source_copy_identity.py` 以 Fraction 穷举 m=5 所有合法 k<l、共享客户的前缀/尾部 incidence，检查 STRICT-FUTURE、tracked c_A>=2、HALF-COLUMN，以及末位恒零；它只审计逐客户算术，不生成或认证新 SPE。一般式由第2—4节代数证明，不由有限检查承担。

## 7. 交接

本轮没有取得新的跨 action 共同容量。可继续的准确问题是：能否用首偏离源行动的真实 COPY-IC，在**同一份源库存**下联立控制 M_A/P_Q、R_t 及未来 Q claims，使其共同消耗已有 actual 余券；或者改变初始化使这些项在生成前已经平衡。此前已知 NEW-CAP、每 context cap1、same-action uniform-reset 与常价格对偶都不足以替代这一步。
