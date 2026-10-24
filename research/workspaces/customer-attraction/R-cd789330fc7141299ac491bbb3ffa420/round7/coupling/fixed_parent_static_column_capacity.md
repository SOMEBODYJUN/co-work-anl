# 同一 parent B 的静态分母第一列：跨不同孩子的联合容量

2026-10-24，coupling7。接续 [SD 独立重构](static_denominator_and_query_projection_review.md)。任意人数、一般有限共同目录、每份完整历史纯 SPE。下列是对任意两个合法完整叶 B,Z 成立的计数关系；它不证明任何全树实际钱包。**Q-CAG-HALF 仍 OPEN。** [root 从精确陈述独立重构](../parent/reverse_sd_and_joint_review.md)与 [independent7 独立审查](../independent/review_fixed_parent_first_positive.md)通过；global_budget7另给相同分母的精确密度展开。无外审或新颖性声明。

## 1. 同一个 B、任意 SD 行集合

固定实际叶 Z=(S_1,...,S_m) 与另一个完整合法叶 B。记 C=union_i S_i 为原实际覆盖。对每个角色 i、每个 x∈S_i，记

    z_x=c_Z(x)>=1,
    d_i(x)=c_B(x)+1−1_(x∈B_i)>=1.

SD 第一项的正边 i→l 为

    q^B_(i,l)=sum_(x∈S_i∩(B_l\S_l))1/[z_x d_i(x)]. (Q)

这里 i≠l 自动成立：x∈S_i 但 x不在S_l。其支持只在 parent B角色l选择、原实际至少一人选择、而原实际l未选择的客户 (C∩B_l)\S_l。

可只使用一部分行，或给每行任意非负系数 0<=theta_i<=L。未使用行设 theta_i=0。theta_i必须是这个固定B与角色i的全部来源合并后的总系数；若逐来源各自<=L但总和更大，不能重复使用实际coverer计数来获得同一列cap。不同i的真实 off-IC child W_i可以完全不同；本引理只使用同一个 B 和同一个 Z，不要求这些行共享 W。

## 2. 联合第一列容量

**STATIC-COLUMN。** 对每个 recipient l，

    sum_i theta_i q^B_(i,l)
      <=L sum_(x∈(C∩B_l)\S_l)1/c_B(x)
      =L u_l(B;(C∩B_l)\S_l)
      <=L u_l(B).                              (CAP)

证明：固定 x∈(C∩B_l)\S_l，此时 b=c_B(x)>=1、z=c_Z(x)>=1。x不在C时没有sender覆盖它，贡献为零，不定义1/z。对每个可能 sender i，d_i(x)>=b，而实际覆盖 x 的角色恰有 z 个，故

    sum_(i:x∈S_i) theta_i/[z d_i(x)]
       <=L z/(z b)=L/b.

对 x∈(C∩B_l)\S_l 求和即得 CAP。每个 l 同时成立，不把每个 sender 各领一份 parent利润。若该主题或差集为空，整列零，无除以零。L=0时亦为零。

## 3. 精确逐客户密度

global_budget7收到主合同后补充了下面的精确展开，本组再按 d_i 重构。对固定 x，令

    Z_x={i:x∈S_i},  B_x={i:x∈B_i},
    z=|Z_x|, b=|B_x|, r=|Z_x∩B_x|.

在 x∈(C∩B_l)\S_l（因此z>=1）的列中，i∈Z_x∩B_x 时 d_i=b；i∈Z_x\B_x 时 d_i=b+1。因此该列从全部行收到的 x 金额，除以它在 parent B 的份额1/b，恰为

    density_x(theta)
      =[sum_(i∈Z_x∩B_x)theta_i
          +(b/(b+1))sum_(i∈Z_x\B_x)theta_i]/z. (DENSITY)

它不依赖所选的新 B-recipient l（只要 l∈B_x\Z_x）。theta_i全等于1时，

    density_x(1)=1−(z−r)/[z(b+1)]<=1.           (EXACT)

这显示列容量的余量来自 B 相对 Z 丢失的实际coverer。CAP仅使用<=L，不需要优化局部常数；精确密度为后续 joint 退款保留客户口径。

## 4. 同一显式矩阵的实际 row 容量

固定 sender i。对每个 x∈S_i，正 recipient 的数目恰为

    n_x=|B_x\Z_x|,

所以该客户的正 row 出流总金额恰为 n_x/[z_x d_i(x)]。因为 i∈Z_x：若 i∈B_x，则 n_x<=c_B(x)−1=d_i(x)−1；否则 n_x<=c_B(x)=d_i(x)−1。因此

    sum_l q^B_(i,l)
      =sum_(x∈S_i)n_x/[z_x d_i(x)]
      <=sum_(x∈S_i)1/z_x=u_i(Z).               (ROW)

非空 S_i 时每个逐客户比例严格小于1，故 row总额<u_i(Z)；空主题row为零。此处x在B中无coverer时 n_x=0、d_i=1，仍合法。

所以 q^B 是一张同时受 original actual-row 钱包与固定parent B-column 钱包控制的非负显式运输矩阵。ROW与CAP必须取同一张q，而不是两张存在性证书；全体row/column容量同时由上面的闭式实现。若归一化为实际行利润的转移比例，单独这一层有严格行损失；但其 B终点若继续进入其它SD项/投影层，不能据此宣布整个扩展网络收缩或已支付。

## 5. 与其它联合接口的区别及限制

[单孩子 prefix 运输](joint_prefix_claim_transfer_blind_review.md)以同一个 W 的全部 prefix请求为输入，利用共同prefix负载 b_x<=c_W(x)控制未来列。STATIC-COLUMN 则以同一个 B 的不同当前i行、不同W_i为输入，利用静态实际分母 c_Z(x)与 actualcoverer总数控制所有角色列，允许合法 backward 目标。二者不能据此直接相加，它们可能请求同一 parent B利润。

本界只控制 SD 的第一类正边。它没有包含同一行的 theta_i v_i(B)直接项、第二类 W_i未来正边、已有parent请求，或其它parent B'送来的请求。尤其不能把“第一列<=L”与“直接项<=L”合成总系数<=L；若相加，必须按同一客户/整行实际库存重算。

支持 (C∩B_l)\S_l 与 l 的 off-IC（从 prescribed B_l 改实际 S_l）有潜在接点：它是放弃旧主题时消失的客户利润。但整条 off-IC slack还包括共同客户负载变化及 S_l\B_l 的新收入；本页不把这个 restricted profit直接当作可扣除的 ell_l，也不按客户重权该IC。

多个不同 parent B 的列容量各自属于不同叶钱包；不能自动视为同一个实际u_l。新关系实际接到 SD 第一类跨行借款的共同 parent容量这一步；从 parent到原actual的总支付、第二类child预算和循环仍待证明。
