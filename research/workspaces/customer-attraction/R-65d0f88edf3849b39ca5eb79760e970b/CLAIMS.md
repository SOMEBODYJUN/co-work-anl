# 本轮精确命题与审查

## Q-CAG-HALF

对象、定义域、全部历史及平局量词均为 CAG-MODEL；欲证每个纯 SPE 有
2W≥OPT_m。状态 OPEN；本轮没有提升其真值状态。

## R22-ROUTE5A-INFERENCE-ERRATUM-v1

- **对象/定义：** 任意实际并集 U、最优并集 C；W=|U|、O=|C|、
  I=|C∩U|、L=|C\\U|、E=|U\\C|，及源稿合法排列付款 R。
- **假设/范围：** 源稿一般份额引理给 W≥R；拟附加条件 R≥L/2。
- **准确结论：** 仅凭这些账本可推出 O≤3W，所展示的推导不能推出 O≤2W。
  修正充分条件 R≥O-W=L-E 则和 W≥R 确实推出 half。
- **依赖：** 集合恒等式 W=I+E、O=I+L；源稿 L1--L3。
- **证据：** 自足算术证明，full_tree 发现，父方读原文重算，direct_exchange
  只见定义独立重构一致；标量反模型不是 CAG 或 SPE 反例。
- **异议/限制：** 不声称旧条件⇒half 在完整 SPE 类本身为假；原 half 仍 OPEN。
  L1--L4 数学身份未改变；没有新增一般半覆盖引理。
- **状态：** 内部解析审查完成，无外审/新颖性认证；源稿已修。
- **正文：** [勘误](full_tree/route5a_half_credit_gap.md)、
  [审查](parent/route5a_independent_review.md)。

## R22-PREFIX-CREDIBLE-EXIT-COMPILER-v1

- **对象/域：** CAG-MODEL 的任意 m≥2，任意 1≤j<m，原终局 z 及其长度 j
  实际前缀后实现尾部的一份完整纯 SPE。其余旧早期子树不必可信。
- **定义/量词：** ell_i(A) 是固定实际前缀 h_i、强制 A 后，在全部真正完整
  后继 SPE 中当前利润的最小值；M_i=max_A ell_i(A)，
  Delta=max(0,max_(i≤j)(M_i−u_i(z)))。A 包括原 A_i。
- **结论：** 对任意正有理 s≥Delta，存在同人数全历史纯 SPE 的 Cartesian
  保险编译，原坐标实际终局仍 z，新增实际福利 (m+j)s、新增最优 (2m−1)s，
  因而新 half 差额为 O−2W−(2j+1)s。同时复制原、新客户清分母。
- **依赖：** 任意强制动作的银行低菜单全历史构造、真实孩子 SPE 极小值、
  Cartesian 完整联合偏离相加与首次异常永久退出；j=1 复用旧常数三修复。
- **证据：** 自足全参数证明；root_regret 独立重构；父方先重构后对稿；
  security_aggregate 未读作者稿的势最大计数实现盲证明。
  25 单位客户回归核全 43 历史、258 项比较，验证含两个不可信旧早期节点的输入。
- **限制/异议：** 未知系数锐性、无外审/新颖性认证。Delta=0 以原路径可信拼合
  处理，不构造零银行。固定 (m,j) 的 robust 与固定 m 原 half 等价；跨全部 m
  需合法 j(m)，固定数值 j 不含 m≤j。尚无旧 gap>(2j+1)Delta 输入。
- **状态：** 完整内部证明，无已知 fatal objection；不是 half 闭合或新增已证范围。
- **文件：** [正文](credible_attack/prefix_credible_exit_compiler.md)、
  [父审](parent/prefix_compiler_review.md)、
  [银行盲证明](security_aggregate/bank_punishment_blind_proof.md)。

## R22-OPTIMAL-PREFIX-BILL-UP-NO-v1

- **精确被否定命题：** 对每个原完整 SPE，存在某个最优 m 元组及排列，
  强制其前 k 个主题后沿原策略所得真实叶 Z_k 的当前利润总和
  D=sum_k u_k(Z_k)≤原实际 W。
- **反证/域：** 既有 22 单位客户四人完整 SPE，唯一最优多重集四叶；
  全部 24 排列的 D 最小为 193/12>14=W。
- **证据：** 原自足 SPE 来源；作者及父方互不导入的 Fraction 实现重放
  259 历史、1554 比较并枚举全部最优元组/排列。父审输出存源文件 hash。
- **状态/限制：** 该一般支付桥 FALSE；这是旧完整证书的新定向后果，非新 SPE
  构造、非 half 反例。BILL-LOW 未判定，FTA/自由菜单状态不变，无外审/新颖性认证。
- **文件：** [正文](direct_exchange/optimal_prefix_bill_boundary.md)、
  [独立审计](parent/audit_forced_optimal_bill.py)。

## R22-BETA-CLONE-FIXED-STRATEGY-LIFT-NO-v1

- **精确被否定命题：** Beta-clone 吸收合法固定背景后，任意给定原完整 SPE
  的所有 fresh-clone 历史可保留原主题规定动作，再填重复 clone 孩子成为完整 SPE。
- **对象/反证：** 四类 85 原单位客户，36 singleton 主题实现 AC 客户背景一；
  合法 hA 两人子 SPE 当前收益 (24,22,22)。clone fresh A_1、末位 B 给 24，
  但重复 A_0 后所有末位 BR 为 fresh C，重复者获 25，无法可信补全。
- **证据：** 自足利润表及积分、三 clone 有理兴趣 pattern×2520 的有限单位客户
  实现；父方手算和另一研究员独立有理 pattern/单位客户局部全行动审计。
- **限制：** 原局部子 SPE 可 BI 向上扩充，但未证 hA 在轨。没有否定重新选择
  fresh 子策略、只保实际根终局的 lift、静态份额表示或原 half。
- **状态：** 此固定策略接口 FALSE，内部解析核查完成；无外审/新颖性/最小性认证。
- **文件：** [正文](full_tree/beta_clone_fixed_strategy_lift_failure.md)、
  [父审与独立计算范围](parent/beta_clone_review.md)。

## R22-FRESH-RESET-DENSITY-v1

- **对象/域：** 任意完整确定策略及实际并集外客户 x；固定 source 标签、
  全部有序 natural contexts。这里不需要策略最优性。
- **完整假设：** 库存 INV 总和≤1；初始单边≤rho_k/c_receiver 且总注入≤rho_k；
  只送严格未来 coverer；EDGE 每条≤h_parent/c_receiver；同客户不重采；
  natural 总外流≤incoming、角色严格上升。不能删去这些 kernel 合同。
- **结论：** 对每个正生成 natural context s，其与 actual 首偏离角色为 k，
  beta_s(x)=h_s(x)c_Bs(x)≤sum_(q≤k)rho_q(x)≤1。
- **依赖/证据：** receiver首偏离唯一确定所有parent的角色及reset叶；
  source保留的递增DAG质量cut。作者及父方从精确合同解析重构；未新增有限扫描。
- **状态/限制：** 纯流引理内部检查通过，无已知致命异议，未外审/新颖性认证。
  whole-IC付款只援引已有合法核，本轮没有独立升级那些核。
  没有给同一actual角色的多contexts总费用上界，不是half承重闭合。
- **文件：** [正文](global_credit_next/customer_density_reset_invariant.md)、
  [父审](parent/reset_density_review.md)。

## R22-BETA-TERMINAL-COLLISION-DEBT-v1

- **对象/域：** 任意合法整数背景、任意目录、任意有限 clone 终局；Beta表示、
  统一分母、同集合标签商的口径严格沿自足正文。无 SPE 假设。
- **定义：** U^c 为 clone 收益、U^b 为原背景同一投影叶收益；S为标签仅出现
  一次的玩家、R为重复者，D为投影剩余利润减clone覆盖，G为S总增益。
- **结论：** 逐客户有 U_i^c≥U_i^b(i∈S)，且 sum_R(U_i^b−U_i^c)=D+G≥0。
  任意按完整clone使用次数定义的上尾，clone总收益≤原背景投影总收益。
- **依赖/证据：** n·Bernoulli 与 Binomial 的凸序弦线比较；总覆盖 d/(b+d)；
  两标签每用户份额按复用次数排序。作者、父方分别推导前两式，父方对稿核上尾。
- **状态/限制：** 同一终局代数内部检查通过，非 SPE lift。没有比较不同真实
  后继叶；24→25反例仍成立。无外审/新颖性认证。
- **文件：** [正文](background_salvage_next/clone_collision_debt_and_credible_gap.md)、
  [父审](parent/static_accounts_review.md)。

## R22-EXACT-M-PATH-HALF-v1

- **对象/域：** 任意原实例，任意完整有序路径 z（甚至无需理性尾部）。
  M(h)为h后全部完整纯SPE当前利润的最小值，按真正孩子全集定义。
- **候选结论：** sum_i M(h_i)≥OPT_m/2，等价于精确递推
  F(h)=M(h)+min_A F(h,A)、F(terminal)=0 的 F(empty)≥OPT_m/2。
- **已证接口：** 可信实际后缀输入有 W+sum_(i≤j)(M_i−u_i)_+≥sum_iM_i≥F(empty)。
  因而若候选成立，则旧 O−2W≤2sum缺陷≤2jDelta，并闭合原 half。
- **证据/异议：** 接口为定义级不等式；核心候选未证。有限未分离不支持真值。
  “取各M极小孩子可拼成同福利SPE”的捷径已有精确反例，不能作为证明。
- **状态：** OPEN，较强充分候选；不是原 half 的等价重写，不认领新颖性。
- **文件：** [精确定义、来源与停点](robust_prefix_next/threshold_path.md)。

## R22-PRODUCT-PREFIX-ATTACK-v1

- **对象/域：** 同人数m、同合法j的有限组件族，各有同一目标路径及可信j后缀；
  barL严格限旧product_transfer_lemma的下一角色菜单LP，保留全部联合退出。
- **候选解析组合：** 若有有理lambda≥0使 G(lambda)>(2j+1)D(lambda)，
  G=sum lambda(OPT−2W)，D=max(0,max_i sum lambda(barM_i−u_i))，
  则足够大有限整数产品、统一余数误差和已审前缀编译可构造原half真反例。
- **证据/限制：** 作者重构旧工具组合、同一产品正常叶及有限舍入；父方尚未完成
  独立审查此组合。没有严格条件见证；barL<L本身不保证barM<M或正G。
- **状态：** 解析组合待独审、攻击条件无见证，不提升原目标，也不称新一般付款。
- **文件：** [组合稿](prefix_repair_next/product_threshold_prefix_attack.md)。
