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
  及父方独立代数核对。原正文已加有日期的撤回与替代，研究状态同步。不是新 half 机制。
