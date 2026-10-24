# tree8 两份全树恒等式的独立方程审查

2026-10-24，independent8。完整读取 [兄弟 Hessian/RESET](../tree/sibling_hessian_and_reset.md)与 [固定被动查询税](../tree/passive_query_tree_tax.md)，从单位客户收益独立展开。**方程、符号及域通过；不包含共同 actual 钱包或一般 half。** 非外审或新颖性认证。

## 1. 兄弟分支与对称耦合

节点 (h,A_a) 上下一角色的真偏离尾是 C_ab，所以 γ_ab 是原完整 SPE 的整行 IC。Δ_ab 第二项采用 C_b，只是合法静态评估；原文正确保留区别。倒数差给 RCP 分子 c_b−c_ab，符号正确。

γ+Δ 中 C_ab 相消。对称 π 换 a,b 后，期望成为 Eπ[f_a(B_a,C_a)−f_b(B_a,C_a)]。固定 x，两分母是 s_ax+α_ax 与 s_ax+α_bx；二值 α 不同时，其乘积恰为 s_ax(s_ax+1)，所以差为 v_ax(α_bx−α_ax)。再次对称化得到原 HESS：

    Eπ(γ+Δ)=−½Σ_x Eπ[(α_ax−α_bx)(v_ax−v_bx)]。

因此 JOINT 确为 `½ΣE[(α_a−α_b)(v_a−v_b)]≤−EΔ`。iid 时 `½E[(X−X')(Y−Y')]=Cov(X,Y)`，COV 负号也正确。分支依赖的 c_a 留在 v_a 中；交换时保留整个 (B_a,C_a)，未错误冻结尾负载。

至少剩两人时所有尾长度一致。末位尾空则 Δ=0，curvature 只依背景，端点正确。重复主题、重复索引、空行动没有分母问题。π 须是同一非负对称耦合；不能每客户选择不同 π 后仍用一份整行 IC。

## 2. 被动负载、同叶税与边际势

对 x∈Z_i，c≥1，`1/c−1/(c+q)=q/[c(c+q)]` 给 τ≥0。代入同一原真 IC，恰有 `IC^q=Γ−τ(prescribed)+τ(deviation)>=−τ(prescribed)`；ROBUST 方向正确。

逐同叶客户求角色和，c 个原 coverer 抵消一个 c，得 Σ_iτ_i=Σ_(c>0)q/(c+q)。V_q 额外包含每个 c=0、q>0 客户的一单位，所以 POOL 减基数项正确。q=0、c=0 坐标按正文略去，没有0/0。q=1_T 时被动玩家解释属于代数插入，不声称原同人数 σ 仍为 SPE。固定独立主题分布时，期望税 ρ/[c(c+1)] 及求角色和后的 ρ/(c+1) 均正确。

追加 §3 的 Ξ_q 也通过：其每客户第 ell 个增量 `q/[ell(ell+q)]` 非负且非增，故离散凹；删除 i 仅在 x∈Z_i 降低一个负载，势差恰为 τ_i。q=1_T 时 Σ_(ell≤c)[1/ell−1/(ell+1)]=c/(c+1)，SAT 正确。固定 q 的无限增量和也有限（增量≤q/ell²），但这不支付跨叶 RESET。

叶钱包只支付同一个 prescribed 延续叶内的全部角色税。互斥节点产生不同叶时，POOL 不允许共同领一份 actual V_q；正文显式保留该断点。两份 notes 没有提供 RESET 的共同 actual 容量或被动查询全树修复预算，不能据方程通过提高 Q-CAG-HALF 状态。
