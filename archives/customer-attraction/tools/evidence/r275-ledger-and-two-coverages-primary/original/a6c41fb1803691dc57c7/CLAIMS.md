# 本轮精确命题与证据入口

所有命题采用所链接正文的精确版本；这里是本工作区恢复索引，不自动成为共享 canonical 账本。一般目标 **Q-CAG-HALF 仍 OPEN**，没有完整一般证明或真正违反半覆盖的 SPE。

| 身份 | 精确范围、结论、状态与依赖 |
| --- | --- |
| B10-TWO-SUPPORT-END-AB-v1 | 任意 CAG-MODEL 完整 SPE，实际覆盖仅为两个不同集合 A,B，频次 k,l≥1，末两位依次 A,B，则 OPT≤[2−min(δ_(k,l),1/m)]W，δ 在正文显式严格正。此前顺序与整个目录复杂度任意。解析证明及另一研究员独立重建通过；依赖既有末两人三比较。见 [正文](terminal_pair/two_support_end_ab.md)、[独审](terminal_pair/independent_review.md)、[逐客户审计](terminal_pair/audit.json)。 |
| 近饱和改进 root-v1 / any-player-v2 | K=max主题大小，m≥3，任意实际玩家 i、任意大小 K 的 C、任意 D：m|D\C|+|D∩C|≤K+c_m(m u_i−K)，c_m=(m−1)²−m²(m−3)²/[2(3m²−7m+2)]。root 与任意实际玩家分版本，证明和独审入口见 [background_exchange](background_exchange/README.md)、[root复核](background_exchange/root_review.md)。仍缺全局误差支付。 |
| 改进交换投影的锐性与非充分性 | 六组单位客户投影在全部末两人 floors、终端 BR、保留重叠税行下取等 c_m；不是真 SPE。另一个五人有理投影满足全部所列实际节点必要行而比较覆盖超过二。见同目录对应正文、正式多项式和精确审计；不得称为主目标反例。 |
| Common Shapley E+BC | 全部大小≤m 的收益数组由同一有符号客户表示，当且仅当存在小计数扩展满足效率和 balanced contributions。只给线性空间，不给非负客户锥。正积分与 Möbius 反演自足证明见 [共同耦合](tree_coupling/common_shapley_coupling.md)。 |
| TC-DIL-1：递减 Shapley 边际的锋利稀释界 | 任意有限标签、非负递减 g、q_a,r_a>0 的非负实速率，L_a(q;g)≤κ L_a(r;g)，κ=max_(T含a)r(T)/q(T)，且锐。指数时钟耦合证明；适用于截断单调次模共同矩，无需非负客户实现。root及另一研究员独立重建通过。见 [稀释耦合](tree_coupling/submodular_dilution_coupling.md)、[独审](credible_search/submodular_dilution_independent_review.md)。 |
| 指定完整树的耦合层次（实质纠错） | 固定旧三人六主题完整形式策略与固定比较支持：图+稀释+同支持守恒仍9/4；加入**所选两主题收益差式**后仍15/7。旧稿把该差式误称为全部两主题耦合，现已撤回：该点违反第三条独立共同客户关系。补全全部两主题关系后新v2精确最优值为2；原共同有符号矩空间8/5不受影响。旧冻结JSON保留，按修正正文解释，见 [共同耦合](tree_coupling/common_shapley_coupling.md)及其round2/v2证书。 |
| Acyclic replacement 条件引理 | 若最优主题（或任意比较组合）的真实查询分支计数满足正文逐坐标的先前比较替换条件，且复用实际节点的行动预算重数恰为实际终局，则一次收费查询≤W，从而比较并集≤(2−1/m)W。一般存在性已经被旧两人反例否定；不得称为普遍证明。见 [条件引理](weak_matching/acyclic_replacement_lemma.md)。 |
| 输入对称下的终局见证商 | 固定对称客户输入及群不动根目标，联合取 (前缀,终局,标记动作) 轨道的存在性系统精确保存任意完整历史纯 SPE 的目标可实现性。不要求确定性策略等变，不对任意输入作对称化。见 [见证商](credible_search/outcome_orbit_quotient.md)；有限证书是实现核验，不是福利定理。 |
| CQ-min-NO（有限完整反例） | CAG-MODEL 六人、九个不同主题、三十单位客户，完整历史纯 SPE 有 W=25、OPT₆=26、最小收益4、一个完全遗漏主题 T 的共同冻结查询 F(T)=30。因此普遍桥 F(T)≤W+min_i u_i 为假。仅此辅助桥失败；完整 DAG 和独立展开客户审计见 [正文](direct_global/common_query_regret_counterexample.md)、[独审](security_global/padded_residual_m6_review.md)。 |
| Padded-residual-floor-4 | 对每个 k≥0，以十四客户 residual core 加 k 个互不交四客户主题，人数 m=k+2，每个合法历史、每个完整纯 SPE 续局的当前提供者收益均≥4。解析全历史逆向归纳，root独立重建通过。见 [正文](direct_global/padded_residual_uniform_floor.md)。不证明指定终局路径对每个 k 可实现；该路径只对已审六人证书作可靠记录。 |

本轮未闭合候选与正在核验的辅助桥反例分别在 `direct_global/`、`security_global/` 的 README 中标明。不得把浮点优化、固定策略锥无分离或多名研究员赞同，升级成普遍事实。
