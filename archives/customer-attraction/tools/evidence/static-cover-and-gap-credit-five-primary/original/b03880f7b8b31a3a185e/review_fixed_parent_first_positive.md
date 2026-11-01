# 固定 parent B 的第一正税整束列容量：独立审查

2026-10-24，independent7。收到 owner 精确合同后独立展开，再读取 SD 正文核对符号。**COLUMN 通过**。本稿只审 fixed-parent 第一类 B 正税；不是 full SD 容量审查，不能再给 direct v_i^B 或 W 税独立花一次 parent 利润。

## 1. 精确域

固定原实际叶 `Z=(S_1,...,S_m)` 与任意一个 parent 完整叶 `B=(B_1,...,B_m)`。负载分别为 c_Z,c_B。取任意角色集合 I subseteq {1,...,m}。对 i in I、l in {1,...,m}，定义

    q_il = sum_(x in S_i cap (B_l\S_l), i!=l)
             1/[c_Z(x)(c_B(x)+1-1_(x in B_i))]。

记 `d_i(x)=c_B(x)+1-1_(x in B_i)`。这正是 SD 的第一类正税；因为 `Z_l=S_l`，这里与 owner 写 B_l\Z_l 相同。不同 i 的返回真实分支 W_i 可以完全不同：q 不使用 W_i，其共同背景是**同一个 B 和同一个实际 Z**。

支持条件已解决零问题：q 的每项有 x in S_i，所以 c_Z>=1；又有 x in B_l，所以 c_B>=1，且 d_i>=c_B>=1。若 c_Z=0，不存在任何相关 S_i 输入项。若 p_l^B=0，则 B_l 为空客户集、该列恒零；输出比值定义0。

本证明不使用 SPE，也不要求不同 ordered history 的相同负载有相同续局。它只需要所有输入角色 S_i 来自同一实际 profile；若改成不同 context 的任意查询主题，覆盖者计数不再由 c_Z 支配，不能沿用此 cap。

## 2. 一行逐客户的共同列证明

固定 l 和 x in B_l\S_l。写 C=c_B(x)>=1、D=c_Z(x)。若 D=0，全部 q_il(x)=0。若 D>0，则每个有贡献的 i 有

    d_i(x)>=C,
    #{i in I:i!=l,x in S_i}<=D。

所以

    sum_(i in I)q_il(x)
      <=#{i in I:i!=l,x in S_i}/(DC)
      <=1/C。

对 x in B_l\S_l 求和，得到

    sum_(i in I)q_il
      <=sum_(x in B_l\S_l)1/c_B(x)
      <=p_l^B。                                    (COLUMN)

取任意 `0<=beta_i<=L`，同一整束输出系数

    kappa_l=[sum_i beta_i q_il]/p_l^B

满足 `0<=kappa_l<=L`。这里是全部 i 的真实联合预算，不是分别用 q_il<=p_l^B 后相加。

同一角色若在多个上下文重复出现，必须先把其固定 B 的系数合并，或已知 `sum_context beta_(i,context)<=L`。不能因每个 context 自己 beta<=L 就重复计算实际覆盖者 c_Z 次数。

## 3. 列的精确剩余，而非只知 <=

固定上面的 l,x，D>0。设

    k=#{i in I:i!=l,x in S_i},
    h=#{i in I:i!=l,x in S_i cap B_i}。

则精确有

    sum_i q_il(x)=h/(DC)+(k-h)/[D(C+1)],
    1/C-sum_i q_il(x)
      =(D-k)/(DC)+(k-h)/[DC(C+1)]>=0。             (COMP)

若 I 为全部角色，由 x notin S_l，排除 i=l 不减少实际覆盖者数，故 k=D，剩余恰为

    #{i:x in S_i\B_i}/[D C(C+1)]。

若 D=0，整份1/C仍剩余。若 x in B_l cap S_l，则没有第一正税，该客户的整份 parent 利润也剩余。

因此 COLUMN 和任何系数<=L的**保留自身客户部分**

    K_l=sum_(x in B_l cap S_l)1/c_B(x)

可共同放在同一 capL 中，因为正税只占 B_l\S_l。它只允许这份明确的 K_l，不允许把整份 direct v_l^B=p_l^B 再放进去。

## 4. 另一个有效边容量：actual 行也不超利润

固定实际角色 i。对 x in S_i，令

    R_x=#{l:x in B_l\S_l}。

因为 x in S_i，i 自己不是丢失 parent coverer，所以 i!=l 的排除不改变 R_x。若 a_i=1_(x in B_i)，则 `R_x<=c_B(x)-a_i`。因此

    sum_l q_il(x)=R_x/[c_Z(x)d_i(x)]
       <=[c_B(x)-a_i]/[c_Z(x)(c_B(x)+1-a_i)]
       <=1/c_Z(x)。

逐客户求和即

    sum_l q_il<=u_i(Z)。                            (ROW)

当 c_B=0 时 R=0、d_i=1，式子仍有效。因此第一正税矩阵同时有 actual 行利润和同一个 parent 列利润的双边质量容量。ROW 不说明 direct v_i^B 加正税的整行是 sub-Markov，也不支付 W_i 后继税。

## 5. 与完整 SD 的准确分界

按 `round7/global/static_denominator_off_ic.md`，每个真实自然 context 的完整式为

    u_i=v_i^B-ell_i+P_B+P_W-N_B-N_W。

本审查只共同支付 P_B。direct `v_i^B` 已经是一份 parent 当前角色的完整利润；P_W 又进入各自 W_i 的未来真实规定利润。把它们与 COLUMN 各自宣称“<=同一 parent 利润”后相加，会重复占用容量。不同 fixed-parent B、多个 child 与 query-projection 也须另有联合系数约束。

结论：fixed-parent 第一正税的全角色 COLUMN 正确，零 c_Z 不造成反例；COMP 和 ROW 可作为更细的同池容量信息。当前未证明 full SD 的共同支付、全图闭合或一般 half。
