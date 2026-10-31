# 本轮精确身份与证据

2026-10-24。个人研究记录。原目标 `Q-CAG-HALF` 的对象、量词、假设与结论不变，
状态 **OPEN**。本页不自动登记 canonical 新结果；内部证明、内审、外审、新颖性分别记录。

## B16-DELETION-REGRET-ENVELOPE-v1

- **Objects / Domain / Quantifiers：** 任意有限单位客户、有限非空共同目录、n>=1，
  非负整数背景 b,d，原背景 b+d 的任意全部有序历史纯 SPE sigma。固定其实际尾元组 q；
  在背景 b 中保留 sigma 作为完整策略，R_j 为其原实际节点的最大真实单步正 regret。
- **Definitions / Exact Statement：** p_j 为原实际尾前缀负载，c 为 q 负载；
  K_j=max_T Σ_(x∈T)d_x/[(b_x+p_j(x)+1)(b_x+p_j(x)+d_x+1)]，
  E_d=Σ_(c_x>0)d_xc_x/[(b_x+c_x)(b_x+d_x+c_x)]。
  逐位置 `R_j<=K_j-delta_j(q)`，总计 `ΣR_j<=ΣK_j-E_d`；delta_j 定义见唯一正文。
- **Assumptions / Scope：** 全部零项按正文处理；重复、空主题、任意有序历史平局均允许。
  删除后的 sigma 不要求 SPE。只约束原实际节点的 regret，不将不同强制叶视为同一叶。
- **Conclusion / Dependencies：** 真实原 IC、删除收益差与单调分母；任意删除背景的激励误差
  上界，未给 ΣK_j 共同福利付款。单插入版本由同轮 harmonic_menu 先推得。
- **Evidence / Status：** [作者完整一般证明](parent/deletion_regret_envelope.md)、
  [仅见合同后的盲独立重构](independent_general/background_deletion_blind.md)均完成；
  独立有限精确回归只是实现检查。内部解析审查通过，无外审、新颖性未认证。
- **Objections：** 无已知致命异议；任意深度单例背景族使人数无关的原叶池付款失败，
  所以不能由本式免费进行删位 SPE 归纳。一般 half 未解。

## B16-OPTIMAL-STATIC-ASSIGNMENT-NO-v1

- **Refuted Statement：** 对每个原模型实例、每份完整历史纯 SPE 终局 z，存在一个达到
  OPT_m 的 m 元组 T 及索引排列 pi，使 `Σ_i u_i(T_pi(i),z_-i)<=W(z)`。
  这使用冻结终局的静态偏离，既不同于真实偏离匹配，也不同于全部比较元组的断言。
- **Exact Counterexample：** m=3，六个两两不同共同主题，1953名不同单位客户，63个
  正整数兴趣类型。完整43节点策略实际 z=(0,3,4)，收益
  (1733/3,1736/3,1736/3)，W=1735。全部216合法有序比较元组（含重复）中，
  OPT=1740、只有{1,2,5}这一无序最优支持，六种排列的最小静态和为1736>W。
- **Dependencies / Evidence：** [原始实例](dynamic_exchange/assignment_instance.json)、
  [全部有序动作表](dynamic_exchange/assignment_full_policy.json)、作者准确正文和回放；
  [独立双实现审计](terminal_query/independent_assignment_audit.py)、
  [父方单位客户整数审计](parent/audit_static_assignment.py)。三路均核全部43历史/258比较。
- **Scope / Counterevidence：** 只否定上述更强桥。`2W-OPT=1730>0`，不是 Q-CAG-HALF
  反例；一般目标、安全值、FTA/Mpath 都未被本例否定。
- **Status：** 有限实例的完整精确证明与独立内审完成；尚无外审或新颖性认证。
  后续冻结值和原始 hash 见各自 JSON；不以浮点求解输出充当证明。

## B16-ROUTE5A-HALF-INTERFACE-ERRATUM-v1

- **Original interface：** 旧 route5a §4 的半遗漏门槛只推 W>=|H|/2，不能推出 half；
  原 `W>=(OPT-W)/2 => 2W>=OPT` 是算术错误，只能得到 `3W>=OPT`。
- **Corrected distinct v2：** B=max_pi Σ_i |T_pi(i)\C|/(m-i+1)，若 `B>=OPT-W`
  则由已证 W>=B 得 half；更强 B>=|H| 也充分。门槛变化作为新版本，未证明一般成立。
- **Scope / Evidence / Status：** L1–L4 不变；[精确纠错](global_payment/route5a_arithmetic_correction.md)
  及父方独立代数核对。原正文已加有日期的撤回与替代，研究状态同步。远端同期已有
  R-65d0组独立纠错，已安全合并两组来源，不认领首次；未构造旧条件本身的完整 SPE 反例。
  不是新 half 机制。

## B16-AVERAGED-SUFFIX-DELETION-v1

- **Objects / Domain / Quantifiers：** 任意原模型 m>=1 完整历史纯 SPE，实际 z、负载 c、
  原实际前缀 b_j。每个 i 后冻结真实前缀，将实际 S_i 作为固定虚拟行动回放后删去
  其负载；R_ij 是 j>i 的原实际后缀节点的最大真实单步 regret。
- **Definitions / Exact Statement：** D=#{x:c_x>=2}，
  K_ij=Σ_(x∈S_i)1/[b_j(x)(b_j(x)+1)]，
  A_ij=Σ_(x∈S_i∩S_j)1/[c_x(c_x−1)]。
  `Σ_(i<j)R_ij+D/2<=Σ_(i<j)min{u_j,K_ij}`，后者至多
  `min{Σ_j(j−1)u_j, Σ_jΣ_(b_j>0)1/(b_j+1)}`，故
  `ΣR_ij<=[(m−1)W−D]/2`。全部零项按正文处理。
- **Scope / Dependencies：** 固定每个删除的实际主题与后缀；完整根虚拟回放的较早
  实际节点另有正文(VR)，离轨节点没有免费全局预算。依赖本轮固定背景删除包络与
  已有虚拟回放的 `regret<=u_j−A_ij`，同叶退款/原 IC 是已有机制。
- **Evidence / Status：** [父方一般证明](parent/average_suffix_deletion.md)与
  [先盲重构后读旧式比较](independent_general/suffix_deletion_corollary_blind.md)完成。
  未用有限扫描承担证明；内部解析检查通过，未外审或认证新颖性。
- **Objections / Limitations：** 没有得到低损失精确 SPE 修复，不能应用较小人数 half
  归纳；实际节点误差为零也不保证离轨可信。一般福利范围没有提升。

## B16-REACHABLE-PREFIX-INCIDENCE-OBSTRUCTION-v1

- **Objects / Quantifiers / Assumptions：** 原模型任意目录，客户分为非空 R,D；每个主题
  为 D-singleton 或含至少 alpha>0 个 R 客户；每个触 D 的非 singleton 含至少 a>0
  个 R 客户；某合法主题含至少 q>0 个 R 客户。对任意合法前缀负载 b、剩余人数 r，
  令 I=Σ_R b、beta=max_R b、B=min_D b。
- **Exact Conclusion：** 若 B>I/a 且 qB>beta+floor(I/alpha)+r+1，则任何实现该 b
  的有序前缀都不能是完整根 SPE 的实际前缀。无论后来如何响应，最后一个 D-singleton
  都有严格盈利偏离。
- **Evidence / Status：** [自足一般证明与 PB 精确代入](credible_attack/root_reachability_incidence_budget.md)、
  [父方读稿解析复核](parent/root_reachability_review.md)。内部证明与读稿检查完成；无外审。
- **Scope / Objections：** 只排除同目录/同负载/同剩余人数的实际实现；PB 的合法离轨
  child 反例不受影响，不排除不同背景编码、更多主题或新的激励。不是 half 新福利界。

## B16-ALL-HISTORY-REGRET-STABILITY-NO-v1

- **Refuted exact contract：** 是否存在与人数、目录、客户无关的常数 C，使每个任意
  完整纯行动计划 tau 都有 `OPT_m<=2W(tau)+C B(tau)`，其中 B 为逐深度对**全部有序
  历史**最大真实单步 regret 的和。此处 tau 不要求 SPE；这是明确另立的稳定性桥。
- **Arbitrary-m family：** m 个主题各为 q 名共同核心客户加一名独有花瓣客户。根选首主题，
  中间位置重复前一主题，末位取一个尚未使用的主题；该规则在所有有序历史定义，末位
  处处最佳回复。精确 `W=q+2, OPT=q+m, B=H_(m−1)−1`。q=0 时
  `(OPT−2W)/B→∞`；q=floor(sqrt(m)) 时 `B/W→0` 而 `OPT/W→∞`。
- **Proof / Review：** [完整解析及全部历史公式](new_induction_repair/all_history_regret_and_reset.md)、
  [父方独立公式核对](parent/induction_repair_review.md)；定义级代码只作有限回归。
  无外审、新颖性未认证。
- **Scope：** 不是 Q-CAG-HALF 反例，也未嵌入真实 SPE 的删位回放；后者还具有全历史
  乘法近似及退款结构。本族不能排除利用那些额外信息的修复。

## B16-ROBUST-FRACTIONAL-PREFIX-v1

- **Objects：** 任意原模型有限实例、m≥1、全部有序历史完整纯计划 tau（无需 SPE），
  实际节点最大真实 regret rho_i，比较客户集大小 O 与分数主题覆盖总重 kappa≥1。
- **Exact statement：** 令 `r_i=m−i+1`、
  `F_m(kappa)=1−prod_(r=1)^m(1−1/(r kappa))`、
  `w_r=prod_(s=1)^(r−1)(1−1/(s kappa))`，则
  `W>=O F_m(kappa)−sum_i w_(r_i)rho_i`。
  特别 `OPT_m<=(W+B)/F_m(m)`，B 为上条全历史逐层最大 regret 和。
- **Dependency / Review：** 已有真实前缀分数覆盖利润计数，把 u_i 替换成 u_i+rho_i，
  后一项经过非负系数递推；[唯一作者推导](new_induction_repair/all_history_regret_and_reset.md)、
  [父方独立解析检查](parent/induction_repair_review.md)。新处是明确鲁棒形式，原产品界
  属既有资产；未外审或认证新颖性。
- **Limit：** 即使 rho=0，五人无条件因子 `1/F_5(5)=15625/6049>2`，因此不能以本式
  自动调用精确 SPE 归纳或推出一般 half。

## B16-FACTOR2-REGRET-COEFFICIENT-LOWER-v1

- **Candidate tested：** 对全历史乘法因子2近似纯计划，加上逐深度最大全历史加法 regret
  B，是否有 `OPT_m−2W<=C B` 的绝对常数 C？该不等式在 B=0 已含原目标，仍 OPEN。
- **Exact necessary condition：** 对每个 m 取两两不交的大主题 A（大小
  `L=ceil((m−1)/2)`）和 m−1 个单客户主题；前 m−1 位处处选 A，末位每一历史选
  真正 BR。此为全部有序历史因子2近似计划，并有 `W=L+1`、`OPT=L+m−1`、
  `B=m−1−L`、`OPT−2W=B−2`。故上述任何普适 C 必有 C≥1。
- **Evidence / Scope：** [作者全历史证明](new_induction_repair/factor_two_regret_attempt.md)、
  [父方独立解析检查](parent/induction_repair_review.md)。没有 C=1 的证明或反例，
  也未证明该计划来自某次完整 SPE 删位。不是一般 half 新范围；未外审、未认证新颖性。

## B16-BACKGROUND-ZERO-REGRET-REPAIR-NO-v1

- **Refuted exact bridge：** 对任意合法固定背景 b+d 的完整纯 SPE 后缀，删除 d 并
  保留原完整后缀策略。如果其**原实际后缀节点**删后 regret 总和为零，是否总存在
  删除后精确纯 SPE，福利至少为保留策略的实际投影福利？答案否；任意只依赖该 regret
  总量且在零处有限的绝对福利修复损失界也被等比例复制排除。
- **Exact witness：** 四主题 A,B,C,D；18名单位客户的八种兴趣类型及策略完整列于
  [自足正文](new_cross_branch/zero_regret_welfare_repair_obstruction.md)与[原始输入](new_cross_branch/zero_regret_repair_witness.json)。
  固定一份 A 背景时两位尾玩家完整 SPE 为 C,B、福利18（含背景）；删背景后保留
  策略实际 C,B 覆盖17，两个实际节点 regret 都零；新两人游戏的末位全部 BR 唯一，
  唯一精确 SPE 实际 D,B 覆盖16。
- **Evidence / Status：** 作者解析证明与独立代码、
  [父方原始重放及全部精确 SPE 枚举](parent/zero_repair_independent_review.md)完成，
  原始 SHA-256 在父方 audit JSON；内部核验，不是外审或新颖性认证。
- **Scope：** 背景 A 是合法固定背景，不要求是原三人 SPE 的实际根主题；所以不排除
  额外利用原战略根激励的删位定理，不是 Q-CAG-HALF 反例。原主命题仍 OPEN。
