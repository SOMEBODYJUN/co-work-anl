# round8 密度组件后的共同付款接续：未闭合

2026-10-24，direct。任意有限单位客户、任意有限非空共同目录、任意人数及每份完整有序历史纯 SPE。**没有新增一般付款、福利界或反例；Q-CAG-HALF 仍 OPEN。** 本次未运行有限计算、固定人数诊断或策略锥攻击。

## 1. 实际读取的新资料与已解决范围

已读 peer round8 的：

- [source-preserving 全图密度](../../../R-cd789330fc7141299ac491bbb3ffa420/round8/inventory/source_preserving_density_envelope.md)；
- [固定比较元组共同付款线性证书](../../../R-cd789330fc7141299ac491bbb3ffa420/round8/residual/linear_joint_payment_certificate.md)；
- [共同边价格势](../../../R-cd789330fc7141299ac491bbb3ffa420/round8/residual/common_edge_price_potential.md)；
- [共同 query 压缩](../../../R-cd789330fc7141299ac491bbb3ffa420/round8/credible/joint_query_compression.md)；
- [同 action uniform-reset 去重](../../../R-cd789330fc7141299ac491bbb3ffa420/round8/residual/common_action_reset_deduplication.md)。

本轮承认并使用加强初始化、客户身份保持、非实际 context 的全图 `c_V(x)h_tx≤1`、一次 whole-IC 付款以及 optional-common 家族合法性；不重新证明或认领这些局部组件。首偏离位置固定所有 reset 父节点的角色、同角色质量反链控制真实多父合流，已解决的是支持与密度，不是实际角色的共同金额。

## 2. 价格 cut 没有给总资金

对固定原 σ、比较元组 T 和同一 P0，角色价格 λ 的精确问题是

    min_(v∈P0) Σ_l λ_l F_l(v) ≤ 2Σ_l λ_l u_l。

我尝试先用 ψ 的 mandatory/common 价格递推，再利用最优 T 交换行控制初始 source 的价格。递推只在合法流之间选择费用；`λ≡1` 时每个 ψ 恒为1，左边精确等于比较覆盖 `|O|`。这一 cut 已经是待证 `|O|≤2W`，不能从线性分离、价格最优或固定 T 的有限性获得资金。

最优主题交换可限制某个新行动在 O 外的覆盖与被删最优槽独有块，但自然 prescribed 行动可以完全位于 O 内而仍捕获 R 来源。该情形没有从交换最优性获得新的损失项。因此本次未构造一个把最优 T 交换行和全部真实 IC 合成为 PRICE-CUT 的非负组合。

## 3. 同 action 合并已去重，跨 action 仍无新约束

我曾尝试把 common 边全取满，使 R-current 精确成为 `h_tx/c_A(x)`，再将同一实际角色、同一规定动作的所有 contexts 合并。合并后逐客户输入仍有 antichain 总量界，且共享同一个 actual-prefix query 完成叶，故可共同调用该动作的一条 whole IC。

阅读后确认这正是 peer 的 `common_action_reset_deduplication.md`，并已定位为旧 round3 捕获流。这里不新增 kernel、表示或容量认领。

真正剩下的是不同动作可在不同来源客户上分别取大值。逐客户

    Σ_a H_(l,a,x)≤1

不推出不同动作的完整 query 共同系数总和≤1或≤剩余钱包。客户总量与每动作一次 whole IC 尚不能共同支付一个实际角色的所有 current。

## 4. 全历史 IC 的方向仍未接上共同钱包

固定自然 context `(g,l)`，规定动作为 a，记四个真实完成：

    V=finish_σ(g)，A=finish_σ(B_<l,a)，
    E=finish_σ(g,B_l)，B=原实际叶。

其第 l 位利润为 v,D,w,u_l。两条真实 IC 只有

    u_l−D=e≥0，v−w=ell≥0，
    v+u_l−D−w=e+ell≥0。

密度与 CLIENT-LOSS 已使每个 current 可由一次完整实际 query 付款；但上式没有把多个 prescribed contexts 的 v 共同压到同一个 u_l。反向 query `E` 的收益 w 是真实可比较量，`ell` 是 prescribed 优势，不能把它删去当免费退款。若把 w 的 C 客户份额解释成抵押，还必须证明这些互斥 return 叶对同一 actual C/G 库存共同只花一次。本轮没有这条关系。

## 5. 与 STATIC-2 的比较与停止线

STATIC-2 要求对一个真实实际位置的静态冻结收益 `F_i(T)` 有 `F_i(T)≤2u_i`；它仍未证明，不能作为这里共同角色金额的前提。即使某个单 query 的响应税获付，也未自动限制许多互斥 prescribed 动作的总 current。本次没有找到两者之间可闭合的付款转换。

可交接的具体未付式仍为同一次初始化和同一流的

    d_l+H_l+J_l+Σ_(t:role(t)=l,x∈R)L_tx≤2u_l

对所有 l 同时可满足，或一个真正足以支付 `|O|` 的更弱共同总额关系。当前既未证明，也未反驳。按 root 的收束指令停止重复 LP、单 action 表示或局部密度推导；不把读入新组件后仍未闭合的重述计作一般进展。
