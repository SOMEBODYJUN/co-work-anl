# 比较客户的可变所有权：共同付款 primal 的一般扩张

2026-10-24，payment9/roleobstruction；与 payment9 同时独立得到同一推导。适用任意人数、任意有限共同目录和每份完整历史纯 SPE。本文是第八轮充分证书的有效扩张与解析核验，**不是新的福利不等式，不证明 ROLE 可满足，不认领外部新颖性**。Q-CAG-HALF 仍 OPEN。

主要来源：[固定所有权 primal](../../../round8/residual/linear_joint_payment_certificate.md)及其 GENERAL-DENSITY 合同、[初始化正部证明](../../../round8/inventory/source_preserving_density_envelope.md)。新自由度是把比较客户在不同比较角色之间的所有权也作为变量；证明仍使用原有真实 query、同客户流与一次 whole-IC。

## 1. 固定数据和可变份额

固定实例、完整 SPE sigma、实际叶 B、实际利润 u；固定比较元组 T，O=union(T)，I=O intersect union(B)，R=O minus union(B)。若 T 最优，才有 |O|=OPT_m。全部 query 完成叶 W_i=finish_sigma(B_<i,T_i)、R 自然图、reset 叶及分母保持第八轮原定义，不随本文变量变化。

对每个 x in O，以非负变量 p_ix 取代原来的 1/c_T(x)，要求

    p_ix=0 unless x in T_i,
    sum_i p_ix=1.                                  (OWN)

特别每个 p_ix<=1。对 x in T_i 定义固定整数

    d_ix=c_B(x)+1-1_(x in B_i),
    nB_x=|{l:x in B_l minus T_l}|,
    k_ix=d_ix-nB_x>=1.

这里 d_ix 是客户分母，不是整行 current d_i。由集合计数，若 x in B_i 则 k_ix=|B_x intersect T_x|；否则 k_ix=1+|B_x intersect T_x|。因此 k_ix<=c_T(x)。

重新定义线性量

    P_ix^B=p_ix nB_x/d_ix,
    r_ix=p_ix-P_ix^B=p_ix k_ix/d_ix,
    H_lx=1_(x in B_l minus T_l) sum_(i:x in T_i) p_ix/d_ix.

因为 l in B_l minus T_l 时该 l 不在求和的 T-coverer 中，以上恰是原 H 公式。由 k_ix>=1，r_ix>=0；由 d_ix>=c_B(x)，对每个实际 coverer l，

    H_lx<=sum_i p_ix/c_B(x)=1/c_B(x)=w_lx.

c_B(x)=0 时 H_lx=0，不使用零分母。故原 I 补余钱包容量 w_lx-H_lx 仍非负。

## 2. 线性扩张和充分性

在原 INIT 中把固定 p、r、H 换成上述变量，并用两条线性约束实现每条原加强边容量：

    a_ijx<=p_ix/c_Wi(x),
    a_ijx<=1/[d_ix c_Wi(x)].                       (OWN-CAP)

这等价于 a_ijx<=min(p_ix,1/d_ix)/c_Wi(x)。保留

    c_ix+sum_j a_ijx=r_ix,
    d_i=sum_x c_ix<=u_i,
    c_ix>=0, a_ijx>=0.

保留原 I-PAY、R-FLOW、ROLE，仅将 H、r 和入口量按同一点重新计算。全部系数仍固定有理，系统仍为有限 LP。

原合法性证明逐步继续成立：

1. OWN 给每客户一单位库存。INIT 给 a_ix<=r_ix<=p_ix；OWN-CAP 给逐入口密度 c_Wi a_ijx<=p_ix。因此 GENERAL-DENSITY 的 source 假设仍成立，得到全部非 actual context 的逐客户 f<=1。不同 origin 的可变 p 仍参加同一个 sum_i p_ix=1，未额外制造库存。
2. H 列界由上一节证明。每个 I 客户的总 future 为 1-sum_l H_lx-sum_i c_ix，仍不超过 sum_l(w_lx-H_lx)，所以忽略 ROLE 时可按同一补余实际份额分配 J。
3. R-FLOW 的固定图和 optional-common 家族不变；密度后的单 context whole-IC 与净 current 上界不变。
4. 初始每坐标 p=P^B+c+a；将 OWN 对同一客户求和，再加同一 I 现金出口及 R 守恒，得到原 MASS：

       |O|=sum_l[d_l+H_l+J_l+sum_(role(t)=l,x in R)L_tx].

   因此任意同时满足 ROLE 的点仍给 |O|<=2W。

此 LP 的非 ROLE 部分非空，因为 p_ix=1/c_T(x) 恢复原有已证可行点。对某些其它 p，INIT 可能不满足 d_i<=u_i；本文不将任意 OWN 点都称为可行初始化。下一节给一个对所有输入均有效的充分所有权区域。

## 3. 对每个 tame 所有权均可初始化的解析区域

若额外有

    p_ix k_ix<=1                                  (TAME)

则该给定 p 一定满足原 INIT 正部论证。证明固定 (i,x)，缩写 p=p_ix、d=d_ix、k=k_ix、w=c_Wi(x)，n=原未来 positive coverer 数，nMinus=未来离开实际 coverer 数。固定计数恒等式 w=d+n-nMinus。此坐标 future 总容量为

    Q=n min(p,1/d)/w,
    r=pk/d.

要证明 (r-Q)_+<=1/w，只须证明

    pk w-n min(pd,1)<=d.

若 pd<=1，左边为

    pkd-pk nMinus+pn(k-d)<=pkd<=d,

因为 k<=d、pk<=1。若 pd>=1，左边为

    pkd-pk nMinus+n(pk-1)<=pkd<=d.

所以逐坐标正部不超过 1/w。先按 x 求和，之后只用 actual-prefix 对 T_i 的一条完整 IC，得

    sum_x(r_ix-Q_ix)_+<=u_i(W_i)<=u_i.

取每坐标 a_ix=min(r_ix,Q_ix)，c_ix=r_ix-a_ix，再按逐边容量比例拆分，就得到该 p 的合法 INIT。没有逐客户使用 IC。空 action 没有客户行；Q=0 时取 a=0。

原 canonical p=1/c_T(x) 属于此区域，因为 k_ix<=c_T(x)。尤其每个 R 客户有 d=1、nB=0、k=1，所以 **任意 R 上的 fractional ownership 都自动 TAME**。这不限制比较客户只能分给一个角色；任意分数分配均有效。全 O 的更大 OWN 区域作为充分 LP 同样合法，只是不给每个 OWN 点的先验初始化保证。

## 4. 真正严格的 payment 集扩张：一个完整 SPE 参数族

本节只检验精确一般候选“固定比较元组下，所有权变量是否真的扩大可行付款集合”，不作 finite no-counter 扫描，也不声称扩大了已知 HALF 实例类。

任取 m>=3。目录只有两个不交主题：B 含 m 个单位客户，E 含一个客户 e。完整策略在每个有序历史都规定 B。在一个历史中若已有 t 个 E，规定 B 的当前收益为 m/(m-t)，而改选 E 后后继仍全选 B，当前收益为 1/(t+1)。前者>=1>=后者；故这是一份完整历史纯 SPE。实际叶全 B，u_l=1，W=m。取固定最优比较元组

    T=(B,E,...,E),  O=B union E,  OPT_m=m+1.

其全部 initial future 边为空。对 B 客户只有角色 1 有所有权，H_1=0、H_l=1 (l>=2)，d_1=1。对 e 任取 p_2e,...,p_me>=0，sum_(l>=2)p_le=1；因为所有 query 中 e 都只被当前 owner 覆盖，d_l=p_le，没有 R-FLOW 或 J。因此总付款向量恰为

    F_1=1,  F_l=1+p_le (l>=2).

原 canonical 证书的唯一付款向量是 F=(1,1+1/(m-1),...,1+1/(m-1))。所有权变量的证书还包含例如 F=(1,2,1,...,1)，并且每个此类点都满足 ROLE 的 F_l<=2u_l=2。故固定 T 下付款可行点集合确实严格扩大；这个例子不声称原证书不可行，也不声称扩张已经解决一个旧证书失败实例。

## 5. m=5 压力代入与准确缺口

上述所有权扩张、TAME 正部界、密度、一次 whole-IC、MASS 和条件充分性对一般 m 已证，因此直接代入 m=5 仍无条件有效。第 4 节参数族在 m=5 给 canonical 付款 (1,5/4,5/4,5/4,5/4)，而可变所有权允许 (1,2,1,1,1)；这是解析例子，不是五人专门补行。

对于 **任意目录、每份完整历史纯 SPE 的五人目标**，本机制仍只给条件结论：若存在最优 T 及上述扩张 LP 的 ROLE 可行点，则 OPT_5<=2W。本文尚未证明这种 ROLE 点总存在，因此没有得到任意五人无条件 half，更没有证明一般 HALF。新增的可变库存分配不能被称作新增共同资金不等式。

下一步真正可推进的是用可变 p 对不同 query 的同角色压力作联合调整，或从真实 off-history IC 给这种调整的全局存在关系。单独每 context 的 f<=1、每个给定 TAME p 可初始化，均不能替代该关系。
