# 一般半覆盖：下一轮研究的接续材料

**Q-CAG-HALF / customer-attraction：OPEN。** 本页是短的工作上下文。它不新增定理或审查等级，不规定研究方法；需要使用某项关系时，读该行的唯一原文及实际审查，而非展开全部链接。盘点截止与实际核验见[清理记录](CURATION.md)。

## 固定对象，不在整理中换题

采用[模型](../current/customer_attraction/model.md)：有限单位客户集 N、有限非空共同目录 S⊆2^N、任意 m≥1 位单位权提供者依次各选一次主题，观察全部有序历史。允许重复、空主题、零客户及任意历史依赖平局。终局 z 的客户负载 cₓ 给收益 uᵢ(z)=Σₓ∈Sᵢ1/cₓ，福利 W(z)=Σuᵢ=|∪Sᵢ|；OPTₘ 是 m 个主题的最大并集大小。

固定**任意一份完整历史纯 SPE σ**，实际终局 z。每个有序历史 h、每个合法主题 T 都满足真实偏离比较

\[
u_i(z_h)\ge u_i(z_{h,T}).
\]

zₕ,ₜ 在 h 强制选 T 后继续沿原 σ；全部后继都可以响应 T。相同主题计数的两个历史可以有不同续局。计数缓存的可实现终局集合不等于只允许计数依赖策略。

对任意最优主题元组的并集 O，令 C 为实际并集，L=|O\C|、E=|C\O|。则

\[
\operatorname{OPT}_m-W=L-E,\qquad
2W\ge\operatorname{OPT}_m\ \Longleftrightarrow\ L-E\le W.
\]

不能丢掉 E 后将原任务偷换成 L≤W；后一加强已有完整反例。零福利实例直接用乘法不等式，不定义0/0。

## 已经可以调用的关系

| 关系及准确范围 | 它给什么；还不给什么 | 唯一原文 |
| --- | --- | --- |
| 任意真实历史，旧负载 b、含当前尚余 r=m−i+1≥1 人：当前收益 ≥ maxₜΣₓ∈T1/(bₓ+r) | 对全部后继有效的分母下界；不把实际收益搬到另一分支 | [一般稿§2](../current/customer_attraction/general_half_proof.md#2-从真实行得到的无条件保证) |
| 任意非空比较集 O，以合法主题作总重 τ≥1 的分数覆盖；Pᵢ₋₁ 是同一实际终局早期收益和：|O|≤Pᵢ₋₁+(m−i+1)τuᵢ | 迭代得到下式；τ可随人数增长，无条件保证尚不到half | [分数覆盖前缀预算](../current/customer_attraction/fractional_cover_path_budget.md) |
| 真正静态安全值 vₘ(0)≥OPTₘ/(2m−1) | 对手的联合竞争主题不观察查询抽样；真实后继会观察，故不能直接推出 W≥mvₘ | [不观察查询的安全值](../current/customer_attraction/oblivious_security.md) |
| 实际遗漏私有席位谱及冻结前缀联合谱：uᵢ≥Λᵢ≥λᵢ、W≥ΣΛᵢ | 提供同一路径预算；私有遗漏为空时退回旧分母界，不自动支付共享遗漏 | [实际遗漏谱](../current/customer_attraction/uncovered_private_seat_spectrum.md)、[联合谱定义/审查](../current/customer_attraction/general_half_proof.md#31-冻结真实前缀的联合客户席位一般付款的精细加强) |
| 任意节点跨枝：ΔW=ΔV+ΔP旧−Γ，Γ≥0 | 非根必须保留旧玩家最终收益变化；根上 P旧=0。跨互斥子树仍无共同付款 | [修正后的节点式](../workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/representation/cross_branch_welfare_relay_identity.md) |
| 给定终局的软水位、共同信用和原规定路径税账 | 终局代数、条件可信接口各自有效；不能免费继承 SPE 或跨改枝重复花一份信用 | [软水位](../current/customer_attraction/fractional_tail_waterfill.md)、[条件接口恢复](../workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/credible/README.md) |

分数覆盖递推的准确结论是

\[
W\ge |O|\left[1-\prod_{r=1}^m\left(1-\frac1{r\tau}\right)\right].
\]

取 τ≤m 得一般弱界；直接代 m=5、τ=5 仅为 W≥(6049/15625)OPT₅。某个最优并集 τ≤7/2 时，m≥5由乘积界给half；m≤4另用已有一至四人一般定理。因此全人数的条件结论依赖两部分，不能说递推单独覆盖小人数；该条件仍不覆盖任意目录。弱界、条件推论和一般结论须分开。

已有三人锐5/3、四人1499/750<2、有限极大主题数及结构类定理，供引用，不从头重做。五人证据分为：共享正式437行上界约2.061695；个人557行**独立全域对偶已审上界**约2.04215549034；728行约2.04207898656仍为作者证书层。全都大于二。准确分数、独审和限制见[前沿](RESEARCH_STATE.md)。不把更强数值静默换进旧 Claim，也不把模板primal当成SPE。

## 最容易再次误用的失败桥

| 精确误用 | 已有见证/纠错；留下的自由 |
| --- | --- |
| 把SPE终局冻结成静态Nash，或改用同实例最低静态CCE福利 | [静态福利分离](../current/customer_attraction/eight_customer_cce_welfare_gap.md)已有完整策略。真正静态安全值与CCE/iid福利不是同一对象 |
| 要求每个玩家有安全值/额外槽保底，或每个前缀余额非负 | [逐人反例](../current/customer_attraction/individual_security_counterexample.md)、[零根额外槽反族](../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round5_general/security/global_extra_individual_counterfamily.md)、[负前缀族](../current/customer_attraction/prefix_balance_family.md)。不否定尚未证明的真正聚合安全值桥 |
| 实际前缀冻结后，要求后继总收益 P 加新增覆盖 Δ 支付前缀外最优覆盖 | [52客户完整根SPE](../workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11/background/global_actual_prefix_counterexample.md)：P=17、Δ=0，前缀外两主题最优为18；甚至 P+λΔ 的任意固定λ也不能修复。它仍满足half |
| 只支付遗漏 L，或各角色只用自己的收益和退款支付 | [71客户唯一最优例](../workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/exchange/unique_optimum_omission_obstruction.md)有 L=36>W=35；[179客户逐角色反例](../workspaces/customer-attraction/R-b659ddeec819493bb10dc58441fa7b3d/refund/unique_optimum_refund_floor_counterexample.md)有倒二35<36。仍允许共同净差支付 |
| 强/弱iid福利替代真正vₘ，或固定实际负载缩放税桥 | [iid§1.2](../current/customer_attraction/iid_security_and_flow_barriers.md)、[精确税§4](../current/customer_attraction/fractional_actual_load_counterexample.md)已否。不能由此声称真正强/弱安全值聚合为假 |
| 将有限必要条件模板的二以上点称为目标反例 | 只否定那份模板足以证明half；仍需同目录客户实现、实际OPT及全部历史可信补全，见[五人障碍](../current/customer_attraction/five_player_indexed_obstruction.md) |

原始量词、其他失败机制、回收信息和重试条件按需查[失败地图](FAILED_ROUTES.md)。历史稿中的OPEN、后来撤回的公式和研究指令不直接继承；先按其精确 Claim 检查现行状态。

## 还缺什么，怎样继续

现有预算路线都尚缺一条对**一般人数、一般目录、每份完整策略**有效的共同控制：把真实离轨后继改变行动带来的损失与旧收益返还放在同一份实际预算中，不重复使用 W。局部恒等式成立、形式表示等价或有限锥成功，都没有补上这一点。原目标也可通过完全不同的方法证明，不必先证明这些预算候选。

两项具体的开放接口供按需接续：真实查询行在更早位置的净差付款（[倒二已证行与限制](../workspaces/customer-attraction/R-e05f01e191354b028004b433016ae1c9/penultimate_true_query_row.md)）；真正安全值的弱充分桥 W≥(m−1/2)vₘ(0)（[安全值债务链](../current/customer_attraction/security_chain_and_local_boundary.md)）。后者及更强 W≥mvₘ 仍 **OPEN**：历史口头声称的聚合反例尚未恢复成可检查证书，不得当作反证。

下一轮先选一个精确一般义务，再读取其原文、真实反例和审查；写明新增哪条信息、推进哪一步。失败时记录准确范围和可复用机制。不要再用旧证书重放、同义改写、增加目录或多人赞同替代一般研究进展。
