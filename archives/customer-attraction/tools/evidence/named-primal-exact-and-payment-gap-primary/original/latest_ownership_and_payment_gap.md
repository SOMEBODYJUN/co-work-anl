# 最后所有者、同一 query 退款与仍未付款的 ROLE

2026-10-24，payment9。对象为任意人数、任意有限共同目录及每份完整历史纯 SPE。Q-CAG-HALF 仍 **OPEN**。本文保存一般可变所有权的一个精确选择及尚未闭合的接点；没有新增福利下界或目标反例。

来源为 [可变所有权完整证明](roleobstruction/fractional_ownership_extension.md)、[第八轮共同 primal](../../round8/residual/linear_joint_payment_certificate.md)及其 GENERAL-DENSITY、[旧 uniform-reset 去重](../../round8/residual/common_action_reset_deduplication.md)。可变所有权由 payment9 与其实际子研究员 roleobstruction 同时独立推导，不认领外部新颖性。

R 的任意 owner partition 已见 [round3 §2](../../round3/credible/increasing_role_capture_flow.md) 和 [round5 §4 INIT](../../round5/credible/all_fresh_submarkov_elimination.md)。LAST 是旧允许选择中的一个确定规则，不把 R 所有权自由度本身称作本轮新机制；本轮扩张点是 full-O 坐标 H/r/qhat 的共同变量化。

## 1. 一个对全部输入都可初始化的选择

固定比较元组 T、实际叶 B，记 O=union(T)、C=union(B)、I=O intersect C、R=O minus C。对 I 保留原 canonical p_ix=1/c_T(x)。对每个 x in R 定义

    q(x)=max{i:x in T_i},
    p_ix=1_(i=q(x)).                              (LAST)

R 有 delta_ix=k_ix=1，故该选择属于可变所有权的已证区域 p_ix k_ix<=1；I 的 canonical 选择也属于该区域。因此同一 INIT、H 列及 I-PAY 都有合法点，无需 ROLE 假设。可以保留原 mandatory/optional-common 流，或在 R 上选择全部 common-future 取满的旧 uniform-reset 角点。

R 最大 future 初始化时，每个初始 query coverer 各获 p_ix/c_Wi(x)，current 也恰为该量。R 自然 uniform-reset 的 current 为 h_tx/c_A(x)。所有客户、origin、真实历史及 actual-prefix reset 保持原定义。

## 2. 最后所有者的嵌套支持

令 U_l=union_(j>=l)T_j，U_(m+1)=empty。任何到角色 l 的 natural 输入都来自 owner i<l。保持客户身份及 LAST 给

    h_tx>0, role(t)=l  =>  q(x)<l  =>  x in R minus U_l.

角色 l 的 initial current 只来自 q(x)=l，即 x in R intersect (T_l minus U_(l+1))。所以角色 l 的全部 R current 均支持

    R minus U_(l+1).                              (PREFIX-SUPPORT)

这个不变量不使用 SPE，不合并旧有序历史，也不要求每个 context 唯一父节点。

## 3. 同一 query 中可扣掉的部分

仅在全部 common-future 取满、R current=h/c_A 的旧 uniform-reset 角点，按同一角色 l、同一 action a 合并全部历史；若 a=T_l，把该 action 的 initial R current 同时合并。定义相应客户系数 mu_lax，使

    K_la=sum_(x in R intersect a) mu_lax/c_A_l(a)(x).

客户/角色反链与 initial owner 库存共同给 0<=mu_lax<=1。PREFIX-SUPPORT 给 q(x)>l 时 mu_lax=0。写 D_la=u_l(A_l(a))、e_la=u_l-D_la>=0，便有精确整行退款

    u_l-K_la
      = e_la
        +sum_(x in a minus R)1/c_A_l(a)(x)
        +sum_(x in a intersect R:q(x)>l)1/c_A_l(a)(x)
        +sum_(x in a intersect R:q(x)<=l)(1-mu_lax)/c_A_l(a)(x).

所有项非负。suffix-owned 的 R 客户确属这个 query 的未用利润；没有按客户加权使用 IC。

同 action 合并及 mu<=1 是旧 [round3 捕获流](../../round3/credible/increasing_role_capture_flow.md) 和 [round8 去重](../../round8/residual/common_action_reset_deduplication.md) 的已知机制，不称新聚合付款。LAST 指定了哪些 R 部分一定没有输入。

## 4. 准确断点与 m=5

ROLE 要支付同一 l 的 sum_a K_la，加上同一点的 d/H/J。上式只在每条自己的完整 query 中扣掉自己的未用利润。不同 action 的 e_la、C 收益与 suffix-owned 收益不能直接相加后从一份 u_l 扣除。同一未来 R 客户也不能让原始单位库存给多个 action 重复付款。

menu9 实际读到这个支持不变量后同意：目前没有可合法把不同 query 的未用 suffix 部分共同接入 ROLE 的不等式。若要接续，应证明真实 off-history IC 与 LAST 库存共同给出跨 action 的付款或交换，而不是再证明单 query 退款。

对一般推导直接取 m=5，PREFIX-SUPPORT、可变所有权、INIT、密度及上面的同 query 退款仍无条件成立；它们尚未推出任意目录/每份完整纯 SPE 的 OPT_5<=2W。只有进一步找到同一最优 T、同一所有权及全部 ROLE 的共同可行点，MASS 才条件性地给 OPT_5<=2W。

所有权自由度对 c_T(x)=1 的 R 客户完全没有作用；常数角色价格仍使总价恰为 |O|。因此本文没有解决一般总资金缺口，也不把 m=5 未闭合理解为候选已被反驳。
