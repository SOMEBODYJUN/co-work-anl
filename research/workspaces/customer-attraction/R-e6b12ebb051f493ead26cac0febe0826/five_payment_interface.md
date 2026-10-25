# 五人一次末尾势缺陷：更弱的覆盖付款接口

## 身份与状态

原 CAG-MODEL，恰五名提供者，有限单位客户、任意有限非空共同目录；所有有序历史、任意历史依赖平局、重复主题、空主题和零客户均保留。固定任意完整纯 SPE 的实际终局 `(A,B,C,D,E)`。

记 `O=OPT_5`、`W` 为实际覆盖数、`u_i` 为实际最终收益，`P=u_1+u_2+u_3`。实际前三位负载为 `q`。调和势 `Phi(c)=sum_x H_(c_x)`，并令

    Gamma = max_(T,S in catalogue) Phi(q+1_T+1_S)
            - Phi(q+1_D+1_E).

本页的无条件结论只是下述旧组件的消元推论；不是五人 half 证明，也不认领底层机制新颖性。新的充分候选 `P+Gamma>=23O/72` 尚未证明。内部独立代数复核见 [payment_interface_review.md](five_potential/payment_interface_review.md)；没有外审或新颖性认证。

## 三份真实预算，保留同一实际末尾

1. [实际倒二真实查询行](../R-e05f01e191354b028004b433016ae1c9/penultimate_true_query_row.md)，对最优五主题组合给

       5u_4 >= O-W+t_q(D),
       t_q(D)=sum_(x in D) 1/((q_x+1)(q_x+2)).

2. [实际末两人势损失](../R-cd789330fc7141299ac491bbb3ffa420/round13/parent/two_tail_potential_review.md)给

       0 <= Gamma <= t_q(D\E) <= u_4/2.

   因而第一份预算还给 `5u_4>=O-W+Gamma`。这里没有把 `Gamma` 和 `t_q(D)` 相加；后者包含前者。

3. [真实前缀最终利润预算](../../../current/customer_attraction/fractional_cover_path_budget.md)取实际末位、最优并集的五主题覆盖，给

       O <= u_1+u_2+u_3+u_4+5u_5 = W+4u_5.

   可直接逐客户核对：在最优并集内，若客户被实际前四位覆盖 `b` 次且被末位覆盖 `e` 次，则前四位总收益贡献为 `b/(b+e)`；五个比较主题的末位查询之和至少给 `1/(b+1)`。若 `b=0`，查询已付一单位；若 `b>=1,e=0`，旧收益已付一单位；若 `b>=1,e=1`，两项和为一。并集外旧收益非负。每个查询都由同一实际末位的真实最佳回复上界为 `u_5`。

## 无条件消元

实际五主题是最优问题的可行解，因此 `h=O-W>=0`。令 `d=u_4,e=u_5`。上节给

    e >= h/4,
    Gamma <= min(d/2, 5d-h).

对所有 `d>=0`，有

    -d+min(d/2,5d-h) <= -h/9.

证明：`d<=2h/9` 时用 `4d-h<=-h/9`；`d>=2h/9` 时用 `-d/2<=-h/9`。故

    P+Gamma = W-d-e+Gamma
            <= W-h/4-h/9
            = (49W-13O)/36.                         (UPPER)

这是对每个给定完整 SPE 成立的上界，没有比较或拼合不同历史的钱包。

## 足够且较弱的未证付款

若能对所有上述五人实例及完整 SPE 证明

    P+Gamma >= 23O/72,                              (LOWER?, OPEN)

则 `(UPPER)` 立刻给 `98W>=49O`，即 `2W>=O`。

它比上一轮的 [ONE-GAP?](../R-cd789330fc7141299ac491bbb3ffa420/round13/security/two_tail_envelope_prefix_payment.md) 弱：旧候选为 `P+Gamma>=3v_5`，而已知静态比较 `O<=9v_5` 给 `3v_5>=O/3>23O/72`（`O>0`）。没有证明 `(LOWER?)`，也没有用已知 half 特例循环论证它。

在假设 `W=O/2` 时，`(UPPER)` 中的等号要求

    u_4=O/9, u_5=O/8, Gamma=O/18, P=19O/72.

这只是该消元上界的必要等号数据，不是 SPE 的可实现构造、最坏实例或锐性声明。

## 原候选与已失败加强不能混同

[两单点完整 SPE](../R-bfbfe64dd5f94fa09d36b75198633f2b/five_only/two_singletons_gamma_counterexample.md)否定的是 `P+Gamma>=3u_5`，其实际路径为 `(0,1,1,1,0)`。该例 `P=7/6,Gamma=0,O=2`，静态安全值 `v_5=1/3`：既不否定原 `3v_5` 候选，也不否定本页 `23O/72` 候选。

## 下一义务

用完整真实前三子博弈的激励，证明 `(LOWER?)`，或用全部有序历史可核验的五人 SPE 反驳它。即使反驳也只关闭该充分接口，不否定 HALF(5)。既有必要条件坏点或固定锥内未分离都不回答此义务。
