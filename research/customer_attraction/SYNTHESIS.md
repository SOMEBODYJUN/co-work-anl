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
| 同一实际末位对全目录报价，联合真源IC、同一K和分支末位IC | 任意尾长可合法投影隐藏回复；所有实际末价与K支出仍需共同支付。先保留共享主题身份再消元，不能逐枝独立花同一预算 | [共同报价与同菜单互查](../current/customer_attraction/priced_hidden_reply_projection.md)、[同源回复再查询](../current/customer_attraction/same_source_reply_requery.md) |

分数覆盖递推的准确结论是

\[
W\ge |O|\left[1-\prod_{r=1}^m\left(1-\frac1{r\tau}\right)\right].
\]

选取总重 τ≤m 的覆盖得一般弱界；直接代 m=5、τ=5 仅为 W≥(6049/15625)OPT₅。某个最优并集 τ≤7/2 时，m≥5由乘积界给half；m≤4另用已有一至四人一般定理。因此全人数的条件结论依赖两部分，不能说递推单独覆盖小人数；该条件仍不覆盖任意目录。弱界、条件推论和一般结论须分开。

已有三人锐5/3、四人1499/750<2、有限极大主题数及结构类定理，供引用，不从头重做。**恰五人已由[完整精确证书](../current/customer_attraction/five_player_half.md)证明半覆盖**（内部复核，未记录外审），保留原模型全部历史与退化情形；没有任意背景五人利润定理。旧437/557/728行二以上上界仅是各自指定模板的历史结果，不能据此继续将五人目标标作OPEN；其准确分数、独审和限制见[前沿](RESEARCH_STATE.md)。不把模板primal当成SPE，也不将零根五人结论套到六人后五位。

六人另有个人层已证条件：实际倒二主题A被前四中的**固定两名主题逐集合包含**时half，正文为[两早期包含证书](../workspaces/customer-attraction/subagent-f/m6_two_early_A_half.md)，独立重构见[3360系数状态审查](../workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/coordination.md)。这不等价于每个A客户的前四负载至少二。另有[遗漏最优重数递推](../workspaces/customer-attraction/R-5ba0899f8e71460dafad1ae1ac8c0bcf/subagent_2/omitted_optimal_multiplicity.md)和[根遗漏回复触及界](../workspaces/customer-attraction/R-3257c31784ff4b08ae3ea1cad3f95acb/notes/root_supported_reply_bound.md)，限制真正反例的不同必要结构；均未闭合一般六人，个人层状态与正式共享登记分开。

另一个个人层已证条件是[倒二主题逐客户三重早期覆盖](../workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_1/threefold_penultimate_half.md)：每个x∈A均被前四至少三名覆盖则half，与两固定主题包含条件不可比。[原始行独立重构](../workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/review_threefold.md)覆盖3528个含重叠的完整系数态。同一证书还给真实会员几何上的无条件缺陷余项，A内前四负载k=0,...,4的最坏360rho依次为`(-1079,-299,-93,2,42)`，A外rho非负；总rho自动非负尚未证，不能升级六人主目标。

至多六极大结果的条件是**整个目录**的极大覆盖数。任取最优六主题加实际末位只能得到至多七个关注主题；尚无保留全部历史SPE的任意目录→七极大归约。其他目录主题可能承载真实离轨回复；删主题或把早期行动替换成极大容器都不能自动保留原SPE。因此七极大六人的44轨道是结构子类缺口，不是已证等价的普适唯一缺口。

## 最容易再次误用的失败桥

| 精确误用 | 已有见证/纠错；留下的自由 |
| --- | --- |
| 把SPE终局冻结成静态Nash，或改用同实例最低静态CCE福利 | [静态福利分离](../current/customer_attraction/eight_customer_cce_welfare_gap.md)已有完整策略。真正静态安全值与CCE/iid福利不是同一对象 |
| 要求每个玩家有安全值/额外槽保底，或每个前缀余额非负 | [逐人反例](../current/customer_attraction/individual_security_counterexample.md)、[零根额外槽反族](../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round5_general/security/global_extra_individual_counterfamily.md)、[负前缀族](../current/customer_attraction/prefix_balance_family.md)。不否定尚未证明的真正聚合安全值桥 |
| 实际前缀冻结后，要求后继总收益 P 加新增覆盖 Δ 支付前缀外最优覆盖 | [52客户完整根SPE](../workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11/background/global_actual_prefix_counterexample.md)：P=17、Δ=0，前缀外两主题最优为18；甚至 P+λΔ 的任意固定λ也不能修复。它仍满足half |
| 只支付遗漏 L，或各角色只用自己的收益和退款支付 | [71客户唯一最优例](../workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/exchange/unique_optimum_omission_obstruction.md)有 L=36>W=35；[179客户逐角色反例](../workspaces/customer-attraction/R-b659ddeec819493bb10dc58441fa7b3d/refund/unique_optimum_refund_floor_counterexample.md)有倒二35<36。仍允许共同净差支付 |
| 强/弱iid福利替代真正vₘ，或固定实际负载缩放税桥 | [iid§1.2](../current/customer_attraction/iid_security_and_flow_barriers.md)、[精确税§5](../current/customer_attraction/fractional_actual_load_counterexample.md)已否。不能由此声称真正强/弱安全值聚合为假 |
| 将有限必要条件模板的二以上点称为目标反例 | 只否定那份模板足以证明half；仍需同目录客户实现、实际OPT及全部历史可信补全，见[五人障碍](../current/customer_attraction/five_player_indexed_obstruction.md) |

原始量词、其他失败机制、回收信息和重试条件按需查[失败地图](FAILED_ROUTES.md)。历史稿中的OPEN、后来撤回的公式和研究指令不直接继承；先按其精确 Claim 检查现行状态。

## 还缺什么，怎样继续

现有预算路线都尚缺一条对**一般人数、一般目录、每份完整策略**有效的共同控制：把真实离轨后继改变行动带来的损失与旧收益返还放在同一份实际预算中，不重复使用 W。局部恒等式成立、形式表示等价或有限锥成功，都没有补上这一点。原目标也可通过完全不同的方法证明，不必先证明这些预算候选。

两项具体的开放接口供按需接续：真实查询行在更早位置的净差付款（[倒二已证行与限制](../workspaces/customer-attraction/R-e05f01e191354b028004b433016ae1c9/penultimate_true_query_row.md)）；真正安全值的弱充分桥 W≥(m−1/2)vₘ(0)（[安全值债务链](../current/customer_attraction/security_chain_and_local_boundary.md)）。后者及更强 W≥mvₘ 仍 **OPEN**：历史口头声称的聚合反例尚未恢复成可检查证书，不得当作反证。

另一个容易重新独立提出的旧候选是 **augmentation / FREE-ROOT**：r名完整SPE是否总满足 `OPT_(r+1)≤2W`；更强形式允许任意固定旧前缀并将其覆盖计入总W。它与任意背景剩余利润界是不同对象，均不能由零根五人证书直接推出。[原候选与all-big等号族](../workspaces/customer-attraction/R-2d91ff13b4b44effbe7e78a60470bcc7/independent/root_only_independent_checkpoint.md#3-一个更强非常紧的-root-only-候选)、[后续精确有限锥及终端基底](../workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/credible_attack/root_regret/README.md)已保存；候选仍OPEN，有限阴性不是新关系。原断点是不同真实孩子的福利与根利润极值不能从一份正深度理性预算共同支付，不是缺少r=1的基底。

该背景总覆盖接口的[恰两名剩余、三个比较主题版本](../workspaces/customer-attraction/R-07e7ddcae71544449ffaae7bdddcc1ab/research_1/two_remaining_three_comparison.md)另有自足个人层证明：四组真实菜单行以`(6S+Z+2V+5L)/11`共同付款，零背景256字面类型与全部正整数背景的解析尾部覆盖完整域。父方逐式阅读及作者实现复跑见[审查边界](../workspaces/customer-attraction/R-07e7ddcae71544449ffaae7bdddcc1ab/research_1/review_two_remaining_three_comparison.md)。它比较三个主题的并集与包含旧前缀的总覆盖，不是三主题背景利润定理，也不闭合五名剩余或六人；尚未完成全仓同结果查重及新颖性检查。

完整策略锥攻击可复用[非极小可信续局接口](../current/customer_attraction/credible_continuations.md)：按目标终局选择安全菜单，再在各有序孩子独立递归，已有完整支持的解析证明及规范采样器 `tests/audits/cone_attack_credible_variants.py`。按计数缓存终局集合或默认极小回复，分别不等于强制匿名策略或枚举全部形式策略。重写同一恢复算法、重跑既有紧族或继续没有明确判别对象的阴性扫描，不增加数学证据。

另两项容易被重新提出的既有表示应直接恢复：[同覆盖标签的全历史商定理](../workspaces/customer-attraction/R-84ce8a8709e34ea6af94f99991d3c2e3/duplicate_quotient/duplicate_coverage_quotient.md)（`B10-DUPLICATE-COVERAGE-QUOTIENT-v1`）用依历史lift保持SPE根覆盖序列/收益/OPT；[0/1信号统一可信重置](../workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/next_general/normal_form/reset_normal_form.md)在零信号历史保原整树，一信号按(count,action)重置最小可信尾。它们不是新福利支付，也不将原策略变成匿名策略。本轮另一实现和独立复核不另认新数学；真正未付的是规范化列之间的共同利润/覆盖预算。

六人的“实际最多两个覆盖主题”也已是旧结构结果的推论，不能重开成新目标：[末位频次筛选](../workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/credible_search/two_theme_terminal.md)在末位频次l≥2、k+l=6时全部满足`l(2k+1)≥k²−1`；l=1则是其重复首主题情形。另有[末两位不同的任意人数定理](../workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/terminal_pair/two_support_end_ab.md)。目录仍可任意大，条件只约束真实在轨支持，不是把目录删成两主题。

七极大六人还有可恢复的[dense系数证书](../workspaces/customer-attraction/R-d54cef1094414cc6a98575e671bd060e/dense_shared_seven_n6/dense_shared_seven_n6.md)：**每个可覆盖客户至少属于两个极大主题**时，3840列有理核验支持U≤2W。该原稿声称的“唯一singleton块”扩展存在未消除的致命范围异议，不能一并调用：正确静态最优是`OPT_6=U−min_j|X_{j}|`，原脚本却按遗漏唯一正私有块计目标。[范围审查及八客户覆盖等式反证](../workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/review_dense_seven_scope.md)明确只否该扩展的证明，不否扩展真值或六人目标。

下一轮先选一个精确一般义务，再读取其原文、真实反例和审查；写明新增哪条信息、推进哪一步。失败时记录准确范围和可复用机制。不要再用旧证书重放、同义改写、增加目录或多人赞同替代一般研究进展。
