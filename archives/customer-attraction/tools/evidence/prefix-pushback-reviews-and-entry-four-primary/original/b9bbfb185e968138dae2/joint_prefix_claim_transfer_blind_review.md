# 同一孩子的全部 prefix 利润请求：联合列容量的独立盲重构

2026-10-24，coupling7。root 传来 credible7 的精确合同后，未读作者正文完成本页推导。研究对象仍是任意人数、一般有限共同目录、每份完整有序历史纯 SPE；本引理的代数实际对任意同前缀合法完整叶成立。**Q-CAG-HALF 仍 OPEN。** 只审单个孩子的联合 prefix 请求，不把分枝叠加或旧请求免费加入。

## 1. 精确合同

固定两个合法完整叶 B,W，角色数均m，且在某i以前前缀相同：

    W_j=B_j for every j<i.

通常 B 为一个父 prescribed 叶，W=finish(B_<i,d) 是在 i 强制合法行动 d 后的真实孩子；但下面的恒等式/容量只用两叶同前缀，不要求 W 是SPE或甚至真续局。

记 p_j^B=u_j(B)、p_j^W=u_j(W)。对每个 prefix 角色 j<i，定义

    q_jl=sum_(x∈B_j∩(B_l\W_l))1/[c_B(x)c_W(x)]  (l>=i),
    N_j=sum_(l>=i)sum_(x∈B_j∩(W_l\B_l))1/[c_B(x)c_W(x)].

每个分母都由 x∈B_j=W_j 保证为正。待审身份和联合容量是

    p_j^W=(p_j^B−N_j)+sum_(l>=i)q_jl,
    0<=p_j^B−N_j<=p_j^B,
    sum_(j<i)q_jl<=p_l^B for every l>=i.          (JOINT)

## 2. 逐客户重构

固定 j<i 和 x∈B_j=W_j。两叶当前 j 均覆盖 x，因此

    1/c_W−1/c_B=(c_B−c_W)/(c_B c_W).

同前缀使差只来自 suffix l>=i，而 c_B−c_W 等于 B_l\W_l 的新增旧 coverer 数减去 W_l\B_l 的新 coverer 数。按正负分别求和即得 JOINT 第一行。

对同一 x，把 B 中其它 coverer 集记 J_B、W中记 J_W。其负项份数为 |J_W\J_B|，所以

    1/c_B−|J_W\J_B|/(c_B c_W)
      =[1+|J_B∩J_W|]/(c_B c_W)>0.

对 x∈B_j 求和即 p_j^B−N_j>=0；上界来自 N_j>=0。空主题时三项均零。

## 3. 真正联合的未来列容量

定义每个客户的共享 prefix 负载

    b_x=sum_(j<i)1_(x∈B_j)=sum_(j<i)1_(x∈W_j).

固定 suffix角色l>=i。交换有限求和给精确式

    sum_(j<i)q_jl
      =sum_(x∈B_l\W_l:b_x>0) b_x/[c_B(x)c_W(x)].       (COLUMN)

零prefix负载 b_x=0 的客户不产生原 q_jl，故上式只求 b_x>0；这些客户均有 c_W(x)>0。因为 W 保留全部 prefix coverer，b_x<=c_W(x)。因此每个被求和客户的系数<=1/c_B(x)，从而

    sum_(j<i)q_jl
      <=sum_(x∈B_l\W_l)1/c_B(x)
      <=p_l^B.

这是**同一个 W 的全部 prefix 角色共同**只用一次的 B suffix利润容量。若把每个 j 的 q_jl<=p_l^B 分别加起来，会丢失这个机制；COLUMN 才是联合步骤。

## 4. 非负角色系数的 L-infinity 保持

取任意输入系数 0<=lambda_j<=L（j<i，L>=0）。乘 JOINT 并求和：

    sum_(j<i)lambda_j p_j^W
      =sum_(j<i)lambda_j(p_j^B−N_j)
         +sum_(l>=i)sum_(j<i)lambda_j q_jl.

定义 parent B 上的输出系数

    kappa_j=lambda_j(p_j^B−N_j)/p_j^B  (j<i),
    kappa_l=[sum_(j<i)lambda_j q_jl]/p_l^B  (l>=i),

零利润分母的系数取0。其分子也必为0：prefix空利润蕴含该主题空；suffix空利润蕴含没有正 q 的客户。因此分母约定不丢失正量。

由第2节 current 非负及第3节 COLUMN，

    0<=kappa_j<=L for every j,
    sum_(j<i)lambda_j p_j^W=sum_j kappa_j p_j^B. (PREFIX-OP)

所以该单孩子的**全部 prefix 请求**可一起送回 parent B，各 parent role 的利润系数不超过原输入共同上限L。此处当前项在原 j，suffix收到来自全部prefix的合计，却仍保持同一个L。

## 5. 域、限制与审查结论

PREFIX-OP 是非负精确利润运输，单个 W 层面的联合系数上界成立。不需要借用 W中过去玩家的 IC；其输出只是 B 叶的角色利润请求。B相应角色何时真 prescribed、强制 query 角色如何由 whole-IC 支付，需要在外部网络另核；不能因为得到 parent B 利润，就直接叫 actual 钱包。

若 B 上此前已有 suffix 请求，新的 kappa_l 要与旧系数相加；PREFIX-OP 不说明相加后仍<=L。若多个孩子 W^a 同时回 parent B，每个单独给的 kappa^a_l亦须求和；每个<=L不代表总和<=L。不同孩子的 COLUMN 客户池是各自的，不是同一份 parent容量被同时独立领取。叶为混合时，只有在相同 parent B 下用总权<=1的凸组合，才能直接保持该L界。

**盲重构结论：JOINT、COLUMN 和单孩子 PREFIX-OP 全部成立。** credible 作者对稿确认一致，并提醒 COLUMN 显示式显式略去 b_x=0 的客户以免形式0/0；已修正该分母口径，不改原 q 或容量。 它是比独立 synthetic-profit projection 更强的同孩子联合容量接口；未证明一般全树共同钱包、循环消除或 half。此次未做有限实例计算，通用结论由上述逐客户代数及有限求和证明承担。
