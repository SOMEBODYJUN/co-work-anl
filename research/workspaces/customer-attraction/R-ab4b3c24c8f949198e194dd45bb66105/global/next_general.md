# 新一轮一般付款尝试与根删除终端接口独立审查

2026-10-25。主 Q-CAG-HALF 仍 OPEN。原模型全输入、全有序历史及任意历史平局均保留。
本页的可靠新增工作是对同 actor `../deletion/next_general.md` 的独立解析核对，
不是一般 half 付款，也不认领 DR 退款或统一价格表示的新颖性。

## 1. 继续研究的对象与已核边界

已读 `../construction/uniform_signed_defect_prices.md`。本分支直接尝试全一价格，
即对任意末位为 BR 的目标路径证明

    OPT_m <= W(path)+sum_i M(h_i).                       (TB)

它是既有 TB-ANY 的末位 BR 限制，不是本轮新候选。
沿目标路径的静态覆盖机会损失 δ_i 之和是 `OPT_m−W`，
但 `δ_i<=M(h_i)` 的逐点推导已有旧真实 SPE 反例，不能用来完成跨位置求和。
目前没有得到支付这些机会损失的全范围新金额关系；未进行固定策略锥阴性扩样。

已核最新反例的准确范围：R-d398 的 `round5_general/security/global_extra_individual_counterfamily.md`
反驳真实零根个体 `OPT_m/(2m)` 保底；其余 padded-core 两稿反驳 LAST 聚合与保税助手。
它们没有直接反驳上述 TB。本页不重启个体保底、末位菜单或旧 FTA hybrid 恒等式。

## 2. 终端合同的盲核：末位 regret，不能换成跨删位收益增加

父方只发送合同后，本分支先按定义推导；随后读完整 `deletion/next_general.md` 作全文核对。
固定原真实强制根 T 的叶 `(T,H,A)`，中间负载为 b；A 在包含 T 的背景下为真正末位 BR。
删除 T，仍保留 H，令 B 是此时任意真正末位 BR。

令 `f_0(X)=sum_(x in X)1/(b_x+1)`，
`f_T(X)=sum_(x in X)1/(b_x+1+1_T(x))`，
`r_T(X)=f_0(X)−f_T(X)`。定义

    ell=f_0(B)−f_0(A) >= 0.                              (R1)

这是同一个删后末位节点的 regret：并非 `f_0(B)−f_T(A)`。
由原 BR `f_T(A)>=f_T(B)` 得

    ell <= r_T(B)−r_T(A)
         = sum_(x in T cap (B\A))1/[(b_x+1)(b_x+2)]
           −sum_(x in T cap (A\B))1/[(b_x+1)(b_x+2)]
         <= P_T,
    P_T=sum_(x in T\A)1/[(b_x+1)(b_x+2)].                (R2)

T\A 上原根份额的分母是 b+1，故逐客户 `2/(b+2)<=1` 给

    2ell <= 2P_T <= d_T.                                 (R3)

对于同一原完整 SPE 的全部真实根孩子，原根 IC 给每个 `d_T<=u_1`，
所以任意固定根分布 p 有 `2 E_p ell<=2 E_p P_T<=E_p d_T<=u_1`。
这是凸组合只用一次的钱包，不是无权求和。

此处 b 是末位之前已经固定的过去，末位没有后继；没有冻结一组未来响应。
如果后来更改 H 或其他孩子，就不能保留原 b 或把这份预算再次发放。

## 3. 独占信用及边界

原根利润按客户精确分成

    d_T = e_T+a_T+R_T,

其中 e_T 是仅由原根覆盖的单位客户数，a_T 是原根与旧末位 A 共有客户的根份额，
R_T 是 T\A 上至少有一个中间覆盖者的根份额。P_T 的 b=0 部分恰等于 e_T/2，
其 b>=1 部分满足 `2/(b+2)<=2/3`，故

    2P_T <= e_T+(2/3)R_T <= d_T.                         (R4)

稿件此分拆及 2/3 系数正确。m=2 时 H 为空、R_T=0，且 `2P_T=e_T`。
空主题、重复主题、零客户不改变证明；所有所用分母均正。
这属于已有 DR 同叶退款公式的末位推论及原根菜单付款，不是全树修复定理。

## 4. 统一价格 functional 的精确变化

令 n=m−1>=2，并明确以人数 n 的 HALF 为归纳假设。
统一价格等价表示给一份只依 n 的非负 lambda；它对**末位 BR 目标**成立，
不声称给出具体数值，也不声称可取全二。

在删后的零背景 n 人游戏中，设 q=(H,A)，q+=(H,B)。定义

    F_lambda(q)=2W(q)−OPT_n
                  +sum_(j<n)lambda_j[M_j(q_<j)−u_j(q)].

q 本身最后动作 A 可能不是 BR，故不能对 q 免费用 `F_lambda(q)>=0`；
q+ 的最后 B 才合法导入 `F_lambda(q+)>=0`。
每个 j<n 的精确有序前缀在 q、q+ 中相同，所以 M_j 完全相同。
若 `Delta_j=u_j(q+)−u_j(q)`，利润守恒给

    W(q+)−W(q)=ell+sum_(j<n)Delta_j.

因此

    F_lambda(q+)−F_lambda(q)
      =2ell+sum_(j<n)(2−lambda_j)Delta_j.                (R5)

稿件 (6) 的符号及 `Omega=sum(2−lambda)Delta` 正确。
用 `ell<=P_T` 后才得到其 (7)；Omega 保留符号且未被原根末位池支付。
全二价格会令 Omega 为零，但须额外证明该价格有效。

## 5. 原实际根、m=5 和准确剩余义务

对实际根，`W(q)=W−e_1`。由 (R4)、(R5) 和人数 n 的价格不等式，
稿件正确得到

    OPT_m−2W <= Delta_m−2e_1+sum lambda_j g_j+Omega+2P,

故所列充分付款

    Delta_m+sum lambda_j g_j+Omega+(2/3)R <= e_1

方向正确。它尚未证明，早期 g_j 使用的是删后真正子 SPE 重新优化后的 M，
不能以旧原含 T 叶的 actual regret 或一次退款替换。

m=5 时 n=4。已有四人 HALF 允许导入某份 PRICE(4)，但并不提供其坐标，
也不付 g 或 Omega。若另外假设未证的 MP_4，才有条件式

    OPT_5−2W <= Delta_5−e_1+2(g_1+g_2+g_3)+(2/3)R.

本次核对没有无条件通过五人 half 压力测试。m=2 不需要人数一的价格导入；
稿件第 3 节已明确限 n>=2，其前两节的终端推论仍适用 m=2。

审查结论：原稿 (1)—(9) 的明示关系、价格域导入条件和 m=5 条件范围通过独立解析核对。
本次未证明统一价格的全输入付款、未支付早期真实 M 的全树项，未取得一般 half 新界。
