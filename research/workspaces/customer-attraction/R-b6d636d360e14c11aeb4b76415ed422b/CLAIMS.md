# 本工作区的精确 Claim 与状态

原模型为仓库 CAG-MODEL：有限不同单位客户、有限非空共同目录、任意人数单位提供者、全部有序历史纯 SPE、任意历史依赖平局，允许重复/空主题及零客户。主目标 `Q-CAG-HALF` 的身份不变，仍 **OPEN**。本页只登记本轮个人资产，不自动正式入库，不声称全球新颖性或外审。

## B3-ACTUAL-OPTIMUM-PRUNING-NO-v1

- Objects / domain：对每个整数 m≥2，现行无拥挤族，m=k+1，主题 A_i=X_i∪{a_i}、B_i=X_i∪{b}、C_i=X_i、D={b,d}；|X_i|=2，所有客户不同。
- Exact statement / quantifiers：原目录存在完整 SPE 实际 C_1…C_k,D、W=2m；只保留实际支持与一个最优组合支持的并集后，OPT仍为3m−1，但**每个**剪枝后完整SPE均先选全部fresh A_i再D，W=OPT。最优支持实际上唯一，所以更换最优组合无效。
- Assumptions / scope：只否定“直接删除实际与所选最优外主题、仍保留某个不更高福利SPE”这一免费归约。没有证明任何复杂度/闭包大小下界，也不否定half。
- Dependencies：CAG-MODEL；原完整低福利族 `research/current/customer_attraction/collision_free_three_halves_family.md`；本轮的每个SPE归纳。
- Evidence：主代理及general_payment独立解析重构；规范与独立有序历史全集有限交叉核验m=2,3,4。
- Counterevidence / objections：未发现致命异议；不能把“原SPE存在”误写成“原最低SPE福利恰2m”。
- Status：一般解析方法障碍，内部独立检查通过；无外审/新颖性认证。
- Related files：`independent_frontier/comparison_catalogue_pruning_obstruction.md`、同名family脚本/JSON、`general_payment/pruning_independent_review.md`、`parent_review.md` §1。

## RI-NO-FIXED-LOCAL-STEP

- Objects / domain：合法固定前缀负载b、剩r人；F_r(b)=max_{r主题}Σc/(b+c)，零分子取零；当前真实收益u_A用同一终局分母。
- Exact statement / quantifiers：不存在有限实常数C，使所有该背景下完整SPE的实际首步都满足F_r(b)−F_(r−1)(b+1_A)≤C u_A。
- Assumptions / proof scope：空背景反例已足够。r=q²，大主题r客户、r−1个独立单例，全历史都选大主题，是完整SPE；u_A=1而指标跌落2q−1。
- Conclusion / limits：否定固定系数无储备局部台阶；不否定全背景利润半界或携带更强余额的递归。
- Dependencies：均分公式、已知大主题下界族及本轮F比较优化。
- Evidence：作者证明、未读作者稿的独立重构、root定义级重构、Fraction实现核验及r=1,2边界。
- Counterevidence：真实child余额2q−2确实足够，根half余量1；因此不能把大局部跌落当half反例。
- Status：一般解析障碍，内部独立检查通过。
- Related files：`recursive_invariant/background_profit_slack.md`、`independent_frontier/background_step_independent_review.md`、`parent_review.md` §2。

## CC-CARRIED-FLOOR-RECURSIVE-STEP-NO-v1

- Objects / domain：同上F_r(b)，h_r(b)=max_TΣ_(x∈T)1/(b_x+r)，当前首步A及其真实收益u_A。
- Refuted exact candidate：对每个合法b、r≥2、每个完整SPE，F_r(b)≤max{2r h_r(b),2u_A+max[F_(r−1)(b+1_A),2(r−1)h_(r−1)(b+1_A)]}。
- Counterexample：r=4,b=0；六主题69单位客户及完整策略；实际(0,0,0,5)、收益(10,10,10,18)、W48。F4=69,h4=15/2,F3(1_T0)=41,h3=15/2；候选右侧65，严格差4。
- Quantifiers / scope：一个完整SPE证书足以否定该全称台阶；不是放松LP点。未否定任何更弱一般支付或主half。
- Dependencies / evidence：完整JSON客户输入和259历史策略；作者独立单位实现及递归分支另一份独立逐单位实现核验1295真偏离；root核对标量反算与余额恒等式。
- Counterevidence / preserved facts：本例2W−OPT=27，真实child余额35；保底只能抽取4，而本步需要8。
- Status：候选 **FALSE**，精确完整SPE反例、内部独立核验通过；LP最优性非否定结论的前提。无外审/新颖性认证。
- Related files：`credible_construction/recursive_step_counterexample.md`、`recursive_step_attack.json`、`recursive_invariant/reserve_counterexample_review.md`、`parent_review.md` §4。

## B3-GLOBAL-TERMINAL-DEPTH-FLOOR-NO-v1

- Objects / domain：任意m≥2,1≤k<m；m个K客户不交大主题、m−k个K/(m−j+1)客户不交私有小主题，K=lcm(1,…,m)。
- Exact statement / quantifiers：存在完整形式策略，在原完整树**每个**深度≥m−k的有序历史上均为真实最佳回复，所有早期实际节点的全部鲁棒分母保底也成立，却有W=K[k+H_m−H_k]、OPT=mK；固定k时OPT/W无界。
- Assumptions / limits：只满足写明的弱化条件；早期实际偏离大主题真得K，原收益K/r，故不是SPE。
- Dependencies：不交主题均分、harmonic计数；旧实际固定前缀尾子树障碍按原范围保留。
- Evidence：作者证明与root独立重构正文§2—6；原完整树深层全部偏离的有限Fraction重放。
- Counterevidence / scope restriction：不能扩大为否定读取真实早期续局的全树方法；小模板附录另为作者推导，未包含于root独审。
- Status：一般弱化系统障碍，正文内部检查通过；无外审/新颖性认证。
- Related files：`common_catalog/global_terminal_depth_obstruction.md`、`audit_global_terminal_depth.py`、`parent_review.md` §3。

## 仍开的桥与未升级材料

- MG：OPT_m−W≤m min_i u_i。仍OPEN。有限指定策略锥未得反例不提升一般真值。
- ROW：固定实际位置i、最优m元组，OPT_m−W≤Σ_jV_ij，V是同节点真实偏离收益。比MG更强，正在一次明确固定锥攻击；见`general_payment/net_gap_handoff.md`。
- 真正W≥m v_m与较弱足够桥：仍OPEN。`security_aggregate/uniform_background_quadratic_interface.md`是不同外生高背景的辅助展开，不是空根模型支付证明；二次桥与提升条件均未解决。
- RI-SLACK-IDENTITY：E_r=E_child+2u_A−Δ为已证记账恒等式，不能独自支付总余额。全背景F_r≤2R_r仍比原根目标更强且未证。
