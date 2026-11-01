# 同前缀单孩子 pushback：独立重构与精确共同容量

2026-10-24，independent7。先按 owner 给出的命题盲重构，未读 credible 作者正文。结论：**所述单孩子 prefix pushback 成立**，包括非负性和整组 prefix 的 cap；须明确零分母约定。另给一个保留精确余量的 H 分解，以及允许改换过去角色标签时的共同客户耦合。它们均为全输入终局代数，不使用 SPE；不自动允许叠加其他孩子或已有 parent future claim，不证明 half。

## 1. 对象与零约定

任意 m>=1，任意 i in {1,...,m}。令 B=(B_1,...,B_m)、W=(W_1,...,W_m) 为两个原模型合法完整叶，且

    B_j=W_j  (j<i)。

因此它们可以是同一完整策略中的 parent finish(g) 与单个 forced-current child finish(g,d)，但以下只用共同前缀。记

    c_B(x)=#{l:x in B_l}, c_W(x)=#{l:x in W_l},
    b_x=#{j<i:x in B_j},
    p_l^B=sum_(x in B_l)1/c_B(x),
    p_l^W=sum_(x in W_l)1/c_W(x)。

定义每个客户的新增/丢失 future coverer 数

    A_x=#{l>=i:x in W_l\B_l},
    R_x=#{l>=i:x in B_l\W_l}。

则 `c_B-c_W=R-A`，并且 `A_x<=c_W(x)-b_x`。

对 j<i、l>=i，定义

    q_jl=sum_(x in B_j cap (B_l\W_l))1/(c_B c_W),
    N_j=sum_(x in B_j) A_x/(c_B c_W)。

这些原始定义的分母均正：x in B_j 且 B_j=W_j，故 c_B,c_W>=1。将 q 按 j 汇总后的式子必须写为

    Q_l:=sum_(j<i)q_jl
        =sum_(x in B_l\W_l, c_W>0)b_x/(c_B c_W)。 (Q)

被省略的 c_W=0 客户有 b_x=0，其贡献定义为零。不能原样写 0/0。任何 p_l^B=0 的主题为空客户集，相关 q,N,H 均零；所有除以 p_l^B 的输出系数在此情形定义为0。

## 2. 当前角色保留项确实非负

对每个 j<i，由同叶收益差的客户恒等式，精确有

    p_j^W=p_j^B-N_j+sum_(l>=i)q_jl。              (ID)

非负保留项并非从 ID 右端各项总和非负推出；须另证。由新增数上界，逐客户有

    A_x/(c_B c_W) <= (1/c_B)(1-b_x/c_W)。

因此

    0<=N_j<=p_j^B-sum_(x in B_j)b_x/(c_B c_W)
             <=p_j^B。                            (RET)

若 B_j 非空，最后那个保留和严格正；若 B_j 为空，全部为零。这证明 `(p_j^B-N_j)` 可合法作为同角色非负 parent 利润块，而不是把新增 coverer 差的符号丢掉。

## 3. 整组 prefix 的列 cap

共同前缀给 c_W>=b。由 Q，逐客户 `b_x/(c_B c_W)<=1/c_B`，故

    0<=Q_l<=sum_(x in B_l\W_l)1/c_B<=p_l^B。      (COL)

取任意 L>=0 和 prefix 系数 0<=lambda_j<=L。定义 parent 全角色系数

    kappa_j=lambda_j(p_j^B-N_j)/p_j^B    (j<i),
    kappa_l=[sum_(j<i)lambda_j q_jl]/p_l^B (l>=i)。

按 §1 处理 p=0，则 RET、COL 给所有角色 `0<=kappa_l<=L`，且 ID 给精确值等式

    sum_(j<i)lambda_j p_j^W = sum_(l=1)^m kappa_l p_l^B。 (PUSH)

这是一个正线性、无穷范数不增的**单孩子 prefix 系数算子**。它同时处理全部 prefix claim；不需要按 j 分别用一次 parent future cap。

边界 i=1 时 incoming 为空；i=m 时只有一个 future 列；m=1、空主题、全零客户、原策略任意历史平局均不影响证明。只有一个 child 的所有 prefix 系数共享 capL，并非每个输入 claim 各有一份 capL。

## 4. future parent 容量的精确余量分解

对每个 l>=i 定义三个非负对象

    K_l=sum_(x in B_l cap W_l)1/c_B,
    Z_l=sum_(x in B_l\W_l, c_W=0)1/c_B,
    H_kl=sum_(x in (B_l\W_l) cap W_k)1/(c_B c_W)  (k>=i)。

H 每项分母正。按每个 B_l 客户在 W 是否保留、是否消失分类，精确有

    p_l^B = Q_l+K_l+Z_l+sum_(k>=i)H_kl。          (COMP)

解释只属代数：Q 使用 child 过去 coverer 份额；K 为原 l 自己保留的客户；Z 为 W 完全失去的客户；H 使用 child future 对丢失 B_l 客户的份额。四块只分同一份 parent 利润一次。

另有一个真正的行容量：

    sum_(l>=i)H_kl
      =sum_(x in W_k,c_B>0)R_x/(c_B c_W)
      <=sum_(x in W_k)1/c_W=p_k^W。               (HROW)

因为 R_x<=c_B(x)。于是若除 prefix lambda 外，还带有 0<=theta_k<=L 的 **H-overlap-only** child future claim，则它们可共同输出

    eta_l=[sum_j lambda_j q_jl+sum_k theta_k H_kl]/p_l^B
          <=L(Q_l+sum_k H_kl)/p_l^B<=L。

共同剩余至少是 `K_l+Z_l`。这是对 COL 的精确 complement 扩展，非仅逐行各自 cap。

限制不能删除：HROW 只是说明被分给 H 的 child future 质量不超过它的利润；它不把整份 p_k^W 等同于 sum_l H_kl。新 W 客户、保留的 B future 关联等 child future 质量没有由 H 付款。故不能借该扩展把全部 child future claim 免费塞入 complement。

## 5. 可选的共同客户耦合：若允许混合过去角色标签

这是不同的代数输出，不默认符合 owner 的 actual(j,x) 标签合同。对全部 child k、parent l，置

    M_kl=sum_(x in W_k cap B_l)1/(c_W c_B)。

每项均有正分母，且

    sum_l M_kl=sum_(x in W_k, c_B>0)1/c_W<=p_k^W,
    sum_k M_kl=sum_(x in B_l, c_W>0)1/c_B<=p_l^B。 (MARG)

若 k<i，W_k=B_k 的全部客户都被 B 覆盖，所以该行和恰等于 p_k^W。因此任意 prefix lambda in [0,L] 可用

    tilde_kappa_l=sum_(k<i)lambda_k M_kl/p_l^B

精确 pushback 整份 prefix claim，所有输出仍<=L。更一般地，全部 child 系数<=L 的**共享客户部分**可同时 pushback 到 parent capL；不被 B 覆盖的新 W 客户的利润显式留在外面。

与 §3 的区别：M 可以把一个过去角色的信用交给另一个过去角色，并占用保留的 future coverer；§3 保留各过去角色 diagonal 标签并只向丢失 future coverer 传输。若后续必须保留 old actual(j,x) 身份，不能用 MARG 无证替换该要求。

## 6. 不能叠加的边界是实质性的

**已有 parent future claim。** 两人，目录含 X={x} 与空主题。完整 SPE 在每个节点选 X；考察 h=(X) 的最后玩家。parent B=(X,X)，forced child W=(X,empty)。有 p^B=(1/2,1/2)、p_1^W=1、q_12=1/2、N_1=0。lambda_1=L=1 时 PUSH 输出 (1,1)。再叠加一个原已存在、系数1的 parent future claim，会令第二角色系数2；总价值为3/2>W(B)=1，任何全 parent cap1 表示都不可能。这不是选择更巧 pushback 即可修复的问题。

**多个 child。** 两人，大主题 X 含两个单位客户，另有互不交单客户主题 Y、Z。全历史都选 X 是完整 SPE：X 最终收益至少1，任何 singleton 偏离至多1。parent B=(X,X)，两个 forced children (X,Y)、(X,Z)。每个 child 的 prefix 角色收益均2，单独 PUSH 恰占满 parent 两角色 cap1；两份相加价值4>W(B)=2，不能共享一份 cap1。必须对多个 child 的 incoming 系数另有联合预算。

**零分母。** 一人 parent B_1={x}、forced child W_1=empty，prefix为空。Q_l=0，但未限制支持的写法 b_x/(c_B c_W) 为0/0。采用 §1 约定后全部恒等式成立；不采用约定则公式未定义。

## 7. 独立审查结论与主目标接入

单孩子 prefix PUSH、非负 RET 和 joint COL 的原断言通过解析独立重构；未发现实质反例。COMP/HROW 是可选的精确 complement 工具；MARG 是不保留过去 owner 标签的另一种共同客户表示。

这些关系是真实终局间的利润转换，不是 SPE IC。它们可支付已经合法汇聚成**一个 child、整组 prefix 系数在同一盒 [0,L]**的 incoming claim。仍须证明：整棵证明树如何使不同 child、已有 parent future claim、新 W 客户及原 actual coupon 的联合 incoming 保持同一容量。上述边界显示该问题不能省略。Q-CAG-HALF 仍 OPEN，不把本审查升级成全图 cap 或福利结论。
