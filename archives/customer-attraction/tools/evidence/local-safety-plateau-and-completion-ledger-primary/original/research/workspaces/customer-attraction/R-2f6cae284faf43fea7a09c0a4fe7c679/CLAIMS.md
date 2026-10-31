# Boss21 精确命题与研究等级

本桌面身份 R-2f6cae284faf43fea7a09c0a4fe7c679；模型引用
`research/current/customer_attraction/model.md`。本页是个人研究登记，不自动替代共享
canonical 账本。除明确给出的辅助反例外，Q-CAG-HALF 仍 OPEN。

## B21-LOCAL-SAFETY-SLOPE-NO-v1

- **Exact statement / quantifiers：** 对每个整数 B≥3，存在五名单位客户、共同11主题目录、
  合法长度5B的有序历史及其后四人的完整纯SPE，使 V=v4(b)、V'=v3(b+1_A)
  满足 V'=V、u_current−V=−1/[2(B+2)(B+3)]<0。因此不存在任何有限实数α
  （即使依赖剩余人数r）令全部合法背景、全部完整纯SPE均满足
  `u+(r−1)V'−rV >= −α(V'−V)`。
- **Objects/domain/definitions：** 五客户x,y,p1,p2,p3；六主主题xp_j、yp_j，五singleton；
  背景由每singleton重复B次产生。静态安全值的竞争元组不观察查询抽样。
- **Scope / conclusion：** 排除按安全值增量有限倍付当步负债的通用局部桥；不保证该背景
  是根实际前缀，不反驳根half或实际总安全值桥。
- **Dependencies：** 倒数离散凸性、同一静态原始/对偶、统一严格收益排序、集合值BI及
  全离轨singleton子SPE拼合；祖先扩展仅用有限逆向归纳。
- **Evidence：** [自足符号证明](security/flat_security_increment_counterexample.md)、
  [完整子策略证书](security/flat_security_increment_certificate.json)、
  [独立审查](potential/review_background_security_plateau.md)。作者B3审计1464历史16104比较；
  独立实现B3/4/10各同数量比较。有限审计核对构造，全部B证明来自符号排序。
- **Counterevidence / objections：** 未发现fatal；已明确不作背景在轨可达性断言。
  实际四位总利润减4V严格为正，本例不攻击聚合。
- **Status：** 完整解析证明、独立内部审查；外审未记录，全球新颖性未认证。

## B21-ARBITRARY-OWNER-REPEAT-v1

- **Exact statement：** 任意m槽比较元组T，对每个x∈∪T固定任意合法owner o(x)
  （x∈T_o(x)）；令Y_i的前i槽恰为T_1,…,T_i，后缀任意。若a_x为T中覆盖x槽数，
  旧owner势UNIT误差满足 `sum_(i:x∈T_i)e_i(Y_i;x) <= H_(a_x)−1`。
- **Objects/domain/assumptions：** 任意有限单位客户、共同有限目录、任意m；允许重复与空主题；
  无需T最优或Y_i来自SPE。owner对整条推导固定，不能逐叶变化。
- **Conclusion/scope：** 旧first-owner假设可以撤去，信用不变；不支付跨叶漂移。
- **Dependencies / evidence：** 旧INSERT/UNIT身份；
  [正文](random_portfolio/arbitrary_owner_prefix_budget.md)与
  [独立审查](branch_budget/review_arbitrary_owner_harmonic_path.md)。
- **Objections：** 固定实际端点的owner平均不能搬到依赖随机排列的中间真实叶；
  owner端点优化可能被总有符号债务等量抵消。
- **Status / novelty：** 完整一般推论、独立内审；旧INSERT的直接量词推论，非新机制认领，
  无外审或新颖性认证。

## B21-OPTIMAL-COMPLETION-EXCHANGE-v1

- **Exact statement：** 任意完整纯SPE、任意真实有序历史h（长度i−1）、其当前规定主题S、
  任意最优r主题补全T、任意槽j，令P为旧覆盖，F_r(P)为总覆盖最优补全，
  O=P∪∪T、D_j=T_j\(P∪∪_(ell≠j)T_ell)、e=|S\O|、
  δ=F_r(P)−F_(r−1)(P∪S)。有 δ≤|D_j\S|−e；对每个合法A，
  `|A\O|<=|D_j\A|`，并有任意槽子集的联合替换版本。
- **True-branch identity：** 强制T_j后沿同σ，当前利润d、Γ=u−d，尾部在D_j的利润L，
  当前T_j\D_j利润d_out，ε为drop-T_j/add-S的补全松弛，则
  `δ−u = L−d_out−|D_j∩S|−e−ε−Γ`。
- **Domain/scope：** 全部有限单位输入、任意人数/目录、全部历史平局；D_j仅比较元组私有，
  不要求全目录私有。交换无需SPE；最后一项Γ≥0使用当前真实SPE行。
- **Evidence/dependencies：** [自足正文](branch_budget/optimal_completion_exchange_debt.md)；
  两个研究线程从覆盖及同枝分享独立重构。
- **Objections/status：** 总和只是OPT−2W的精确重写，不构成共同付款。代数证明完整、
  内部重构；外审与相对全部旧资料的新颖性未认证。

## B21-STATE-FLOOR-RELAXATION-NO-v1

- **Exact statement：** 存在十单位客户、十共同三窗口主题、三人静态根菜单，全部根实际利润
  3/2，严格小于v4(0)=33/20，而每条菜单尾序列的每个位置j均满足
  `u_j >= v_(3−j+2)(root+prior_tail)`。可补全一份全部非根历史满足这些floor的
  形式策略且根全部行动平局，但没有完整SPE断言。
- **Definitions/scope：** 客户e_i，下标模10，A_i={e_(i−1),e_i,e_(i+1)}，菜单
  `(A_i,A_(i−1),A_(i+2))`。此为删除真实后继IC的辅助接口反例。
- **Evidence：** [证明](relay/state_dependent_floor_interface_counterexample.md)、
  [独立盲审](relay/stationary/state_floor_blind_review.md)及独立Fraction回归。
- **Objections / limitations：** 指定末位有严格盈利偏离，第二位也未认证IC；不能称SPE反例。
  更强逐背景extra-slot floor已有旧2475人完整反例，本项不认领首次排除该一般归纳路线。
- **Status：** 辅助静态反例完整、独立内审；无外审、新颖性未认证；不反驳half。

## B21-OPTIMAL-BRANCH-GAP-v1（本轮继续主攻）

- **Exact statement：** 沿上项任意h及最优槽j，Y_j为强制T_j后的真实尾主题并集，
  `ρ_j=F_r(P)−|P∪T_j∪Y_j|`，`t_j=|T_j\(P∪S∪Y_j)|`，
  `f_j=|S\(P∪T_j∪Y_j)|`。定义
  `ξ_j=F_(r−1)(P∪S)−|P∪S∪Y_j|>=0`，
  `η_j=r d_j−|D_j\S|−(r−1)t_j>=0`。
  则精确有
  `r(δ−u)=(r−1)ρ_j−ε_j−e−(r−1)f_j−(r−1)ξ_j−η_j−rΓ_j`。
- **Objects/domain/quantifiers：** 每个原模型输入、每份完整纯SPE、每个有序历史、每个最优r补全
  和每个比较槽；r≥1。重复/空主题和零客户包括。ρ_j正是强制孩子的机会损失，因
  `F_(r−1)(P∪T_j)=F_r(P)`。
- **Dependencies：** 同尾覆盖替换 `δ=ρ+t−f−ξ`、最优补全交换，以及逐客户
  `r d>=|D_j\S|+(r−1)t`；无冻结真实续局的SPE假设。
- **Evidence：** recurrence2和exchange2独立推导，父方重构；正文正保存。由η非负得到全范围
  折扣不等式。尚未以此证明跨树总支付。
- **Objections / frontier：** ξ只比较静态可行补全，不能当S孩子的真实损失。归纳若给
  `ρ_j<=偏离枝tail利润`，仍不能把该利润替换成actual tail。折扣小于一不自动产生共同预算。
- **Status：** 解析关系已重构，待完整审查与去重；一般half保持OPEN；无外审/新颖性认证。
