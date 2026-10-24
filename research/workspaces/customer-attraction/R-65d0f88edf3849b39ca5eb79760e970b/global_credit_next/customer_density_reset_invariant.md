# fresh 客户不重采时的全图密度不变量（候选，待独审）

2026-10-24。任意有限共同目录、任意人数、任意完整有序历史纯 SPE；以下计数/流不变量实际上只需要固定的一份完整确定策略及 actual 叶，不使用其最优性。**Q-CAG-HALF、FRESH-RESIDUAL 均仍 OPEN。**

本稿接 `R-d398.../next_general/credible/clock_cycle/source_preserving_kernel_review.md` §3 的每客户 incoming 保留核。它改变分母，不是原 full-profit/fresh-profit 标量流的删边版本。本稿不声称那些会重采客户的旧标量流也有下述结论。

## 1. 定义及允许初始化

固定 actual 叶 `Z=(Z_1,...,Z_m)`，actual 覆盖 `C`。固定一个客户 `x` 不在 `C`。客户标签在全程保留；不同客户各自独立进行本节线性流，再用既有一次 max 系数完整 IC 付款接口统一计算每个 context 的 actual 整行费用。

在每个 source 角色 `k` 允许一个 actual-prefix 强制主题 `T_k`，真实完成叶为

`Y^k=finish_sigma(Z_<k,T_k)`。

给该 source 的客户库存 `rho_k(x)>=0`，只在 `x in T_k` 时可以正，满足

`sum_k rho_k(x) <= 1`。                                               (INV)

初始可向 `Y^k` 上每个 future coverer `j>k` 的真实 natural context

`s=(Y^k_<j,j)`

注入任意量

`b^k_s(x) <= rho_k(x)/c_{Y^k}(x)`；                                    (INIT)

非 coverer 不注入。每个 source 的所有初始注入总量不超过 `rho_k(x)`，其余可当前吸收或不使用。原 owner INIT、round7 坐标子边 `a_kjx<=p_kx/c_{Y^k}(x)`、以及对这些边的 further clipping 均在这个域内。若同角色允许多个不同 source action，应改为各自库存之和并保留 `(k,T)` 标签；以下证明不变，但为简洁正文只写单个 `T_k`。

## 2. 每客户不重采递推

一个有正 x incoming 的 natural context 为 `t=(g,i)`。规定动作 `a_t=sigma_i(g)` 必须覆盖 x；规定完成叶为 `B_t=finish_sigma(g)`，actual-reset 完成叶为

`A_t=finish_sigma(Z_<i,a_t)`。

记其合计 incoming 为 `h_t(x)`，并置

`v_t(x)=1/c_{B_t}(x)`，`beta_t(x)=h_t(x)/v_t(x)=h_t(x)c_{B_t}(x)`。

对一个 `j>i`，只有 `x in A_{t,j}` 且 `x notin B_{t,j}` 才有原正边；其原价为

`q_tj(x)=1/[c_{A_t}(x)c_{B_t}(x)]`。

因此沿该边发出的 x 流为

`beta_t(x) q_tj(x) = h_t(x)/c_{A_t}(x)`。                              (EDGE)

接收 context 是 `s=(A_t_<j,j)`，其规定完成叶恰为 `A_t`。为本稿的纯流不变量，允许删除或分数保留原正边；边实际流始终不超过 EDGE。逐客户同价正负取消后保留的边也包含在内。**任意删正边只在非增质量流意义下允许；不因此声称删边后余量仍有合法 whole-IC 付款。** 如需 actual 付款，必须用原客户保留核、同客正负取消核，或另经核验的合法 CLIP，并按该版本重算。

因 x 不在 C，reset 叶的 i 以前没有 x 覆盖者。令 `U={j>i:x in A_{t,j}}`、`V={j>i:x in B_{t,j}}`。所有 future 正边总流至多

`h_t(x) |U\V|/[1+|U|] < h_t(x)`。

未外送部分在当前角色非负吸收。fresh 无 past 正出口；角色严格增加；故对每个 source 的 x 质量，此图是有限非增质量流，没有复制。

## 3. 一般不变量

**候选定理（RESET-DENSITY）。** 在 (INV)--(EDGE) 的同一次客户保留流中，每个正生成 natural context `s` 同时满足

`0 <= h_s(x) <= 1/c_{B_s}(x)`，即 `0<=beta_s(x)<=1`。                  (DENSITY)

更精确地，令 `k` 是 s 的有序 history 与 actual history 首次不同的位置，则

`beta_s(x) <= sum_{q<=k} rho_q(x) <= 1`。                              (PREFIX-DENSITY)

注意 k 严格早于 s 的当前角色。实际 context 没有 x 覆盖者/正 x incoming，故不需给其指定 k。

### 证明第一步：receiver 的首偏离唯一决定所有 parent 的角色和 reset 动作

设 s 的当前角色为 j，且一条正 x 边从 t=(g,i) 进入 s。由 EDGE，a_t 覆盖 x；而 x 不在 C，actual 动作 Z_i 不覆盖 x，所以 `a_t != Z_i`。reset 叶 A_t 在 i 以前恰等于 actual，在 i 取 a_t。因此 receiver history `A_t_<j` 首次偏离 actual 的位置恰为 i。

于是对同一个 s，所有 natural parents 的角色都必须等于该唯一首偏离位置 k；所有 parents 当前动作都必须等于 s 历史中的第 k 个动作，且它们的 reset 叶都是同一个 `B_s`。不存在一个早于/晚于 k 的 parent 同时向 s 送正 x 流。

同理，若 s 直接接受 source q 的正初始 x 注入，则 T_q 覆盖 x、`T_q != Z_q`，故 s 首偏离位置恰为 q；所以只有 source k 能直接注入 s。

### 证明第二步：角色 k 的 input 总质量和 source k 库存共同至多前缀库存

保持 source 标签。来自 source q 的每条 natural 轨迹角色严格增加，因此在某个固定角色 k 的全部 natural contexts 上，它的 incoming 总和至多其原库存 `rho_q(x)`。并且只有 q<k 的 source 能在角色 k 的 natural contexts 出现；q>=k 的 source 尚未发出严格 future 注入。

更直接地，可在角色 k 前切开整个递增 DAG：每个 source q<k 的总在途质量不超过 `rho_q(x)`，其中进入角色 k 的部分至多这一数量。于是

`sum_{t:role(t)=k} h_t(x) <= sum_{q<k}rho_q(x)`。                      (LAYER)

此式是质量不复制和严格角色次序的 cut 不等式；不使用任何 IC。

### 证明第三步：同一 receiver 的分母共同，故合流后仍受控

由第一步及 EDGE，receiver s 的全部输入可用同一分母估计：

`h_s(x) <= [rho_k(x) + sum_{t:role(t)=k, reset(t)=B_s}h_t(x)]
                /c_{B_s}(x)`。

使用 LAYER 后即得 PREFIX-DENSITY，再由 INV 得 DENSITY。该论证处理同一真实 context 的全部初始/递归来源，未将合流前的逐来源上界相加成错误的单位 cap。证毕。

## 4. 接到 whole-IC 的准确结果及停止处

同时对全部 fresh x 运行该流。每个 context 先合计各 x，既有客户保留核使用

`beta_*t=max_{x in a_t\C} beta_t(x)`

乘该角色的一条完整 actual-prefix IC；退款后留下非负 current amount `L_t`。本候选给

`beta_*t <= 1`，从而 `L_t <= u_{role(t)}`。

这里 `L_t<=u_role(t)` 只对原客户保留核、同客正负取消后重算的核，或确有同一 whole-IC 退款证明的合法 CLIP 断言；§2 单纯允许的任意删正边不能免费附带这项 actual 付款结论。

这是比“仅初始 fresh injection 的 beta<=1”更强的全图客户密度控制。其证明实质就是**每客户总质量守恒/非增，加上同一 receiver 的唯一首偏离和局部共同入边因子 `1/c_receiver`**；不将这个直接推论包装成新的共同 actual 容量机制。它**没有**证明同一个 actual 角色的所有 contexts 满足

`sum_{t:role(t)=l} beta_*t <= 1`

或

`sum_{t:role(t)=l} L_t <= 2u_l-d_l-H_l-J_l`。

不同 histories 的 max 可由不同 fresh 客户实现；DENSITY 不能把它们自动合成一条 actual IC。以上一般不变量不等于 FRESH-RESIDUAL 或 HALF，也不能混入会在不同客户之间重采的标量 nu 流来领取其更低 whole-IC 系数。

## 5. 核查范围

本稿未生成有限实例或扫描。候选证明只用真实 reset completion 的 history 域、每客户保留、source 库存和非增质量流；仍待 root 从精确陈述独立攻击。若成立，其数学新增仅是全图 DENSITY/PREFIX-DENSITY，不作新颖性认证。真正下一步仍须支付同 actual 角色的多 context 合账，不能停在 beta_*t<=1 后宣称实际钱包 cap。
