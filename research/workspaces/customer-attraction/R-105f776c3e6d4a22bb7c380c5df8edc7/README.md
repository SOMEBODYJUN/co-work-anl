# 一般顺序半覆盖：本轮研究桌面

2026-10-24。程序身份 `R-105f776c3e6d4a22bb7c380c5df8edc7`；main/customer-attraction/boss。
从附件恢复独立 clone，不覆盖旧对话身份。六名实际 `gpt-6.1-sol / ultra` 分支已完成本轮工作；
父方直接推导并完成两项一般删除误差关系。无后台常驻或无限运行承诺。

唯一主目标 [Q-CAG-HALF](../../../questions/customer_attraction_half_coverage.md)：任意有限单位客户、
有限非空共同目录、任意 m、每个完整有序历史纯 SPE 的 `2W>=OPT_m`。
**仍 OPEN：没有一般证明、目标反例或新增 half 已证范围。**

## 新增认识与准确等级

- [真实背景删除误差包络](parent/deletion_regret_envelope.md)：任意 b,d,n、保留同一完整策略，
  原实际节点的删除后 regret 总和不超过 `ΣK_j−E_d`。作者一般证明、盲独立重构与独立精确回归完成。
- [全部删位的后缀共同预算](parent/average_suffix_deletion.md)：任意 m、任意完整 SPE，
  `Σ_(i<j)R_ij+D/2<=Σ_(i<j)min{u_j,K_ij}`，从而 `ΣR_ij<=[(m−1)W−D]/2`。
  一般证明与先盲重构后读旧式比较完成。完整虚拟回放的较早实际节点另保留为(VR)；
  仍未控制离轨的退款重置，不能调用较小人数精确 SPE 归纳。
- [静态最优主题排列桥反例](dynamic_exchange/static_optimal_assignment_counterexample.md)：
  三人、六共同主题、1953单位客户，完整 SPE 的 W1735、OPT1740、每个最优排列静态和至少1736。
  作者、盲原始证书双实现、父方单位客户整数实现三路核全部43有序历史/258比较。
  只否定同行 seq242 的辅助桥，half 余量1730为正。
- [实际前缀关联预算](credible_attack/root_reachability_incidence_budget.md)：一般 lemma 排除高 dummy
  负载/低 real incidence 的实际根前缀；精确排除旧 PB 同目录同背景同剩余人数的任意实际实现。
  作者证明与父方读稿复核完成，不损害原合法离轨 child 反例，不排除其他编码。
- [route5a 算术勘误](global_payment/route5a_arithmetic_correction.md)：旧半遗漏付款推论只给3W界，
  修正需求门槛为 OPT−W。远端同期已有其他组独立纠错；已合并保留双方来源，L1–L4不变。

内部证明、审查、外审与新颖性分开：以上没有外部同行评审或新颖性认证；精确身份、依赖与异议
见 [CLAIMS.md](CLAIMS.md)。本区备份不自动等于共享 canonical 提升。

## 恢复与证据地图

| 路径 | 内容及读取时机 |
| --- | --- |
| [GENERAL_WORKING.md](GENERAL_WORKING.md)、[RESEARCH_STATE.md](RESEARCH_STATE.md) | 父方一般论证、实际停止点、竞争路线与下一 obligation；接续首先读。 |
| [CLAIMS.md](CLAIMS.md)、[FAILED_ROUTES.md](FAILED_ROUTES.md) | 精确量词、证明范围、已排除接口及为什么失败。 |
| [parent/deletion_regret_envelope.md](parent/deletion_regret_envelope.md)、[parent/average_suffix_deletion.md](parent/average_suffix_deletion.md) | 两项全输入删除误差组件、(ASD)/(VR)及不能跨真实分支调用归纳的边界。 |
| [independent_general/background_deletion_blind.md](independent_general/background_deletion_blind.md)、[后缀盲审](independent_general/suffix_deletion_corollary_blind.md) | 仅见合同重构，再比较旧虚拟回放；包含正 regret 取最大合法性和精确退款系数。 |
| [independent_general/audit_background_deletion_blind.py](independent_general/audit_background_deletion_blind.py)、[结果](independent_general/background_deletion_blind_audit.json) | 独立65例/469节点/1676原IC检查，9个正regret例；不承担一般证明。 |
| [parent/audit_suffix_deletion.py](parent/audit_suffix_deletion.py)、[结果](parent/suffix_deletion_audit.json) | 在冻结1953客户完整策略上按真实虚拟回放独立实现ASD/VR；不是新搜索。 |
| [dynamic_exchange/README.md](dynamic_exchange/README.md) | 静态最优排列反例的唯一正文、输入、完整动作表、发现与精确证明代码。 |
| [terminal_query/independent_assignment_audit.md](terminal_query/independent_assignment_audit.md)、[parent/audit_static_assignment.py](parent/audit_static_assignment.py) | 盲原始证书单位展开/Fraction双实现及父方独立整数实现；全部最优元组及排列，保留重复。 |
| [harmonic_menu/README.md](harmonic_menu/README.md) | 单插入真实目录误差上界、共同池与任意深度失真；是本轮任意d推广的前驱。 |
| [terminal_query/hybrid_ic_expansion.md](terminal_query/hybrid_ic_expansion.md) | 真正单步hybrid IC展开；剩余删位势差尚未获共同付款，只是探索稿。 |
| [credible_attack/README.md](credible_attack/README.md)、[父方复核](parent/root_reachability_review.md) | 一般root可达性lemma、PB参数原样应用和准确排除范围。 |
| [global_payment/README.md](global_payment/README.md) | 算术勘误及已弃驻留重置尝试；后者是旧边界的不同重构，不认领新机制。 |

## 保存与协作

用户已明确授权本题推送与本仓库协作交流。启动公屏seq247、与候选提出者私聊seq248、
静态反例定向发送seq252均已成功；发送不表示对方已读、接收或完成审查。
首次阶段保存已获 `status=pushed`，提交8b7ccc5d；并发勘误合并保留双方工作。
随后更新以最终 checkpoint 回执为准。接续本 clone 复用绑定与仓库根 work.py。

本轮在全树共同付款的实际数学缺口停止；没有以继续阴性扫描、重复恒等式或空轮询代替研究。
