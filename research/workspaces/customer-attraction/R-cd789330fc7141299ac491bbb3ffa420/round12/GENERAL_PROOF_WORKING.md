# 第十二轮：真实端点重选与共同付款

Boss10同clone/actor接续，原Q-CAG-HALF仍OPEN，全部有序历史、任意平局、重复/空主题和零客户不变。六名指定gpt-6.1-sol ultra实际恢复，父方同步一般推导。

## 新反馈

已读公屏327对shared接口的独立审查。保留Hbg=ΣL*t和Qstat=(m−1)γ−Hbg≥0后，OPT≤(2m−1)γ−Qstat，half只需C≤I+D+(γ+Qstat)/2。它是既有静态余量，不是新钱。336/339多删身份池和reset范围已读，不重复调核或扩阴性。

## 当前全输入关系

固定原actual叶B及u_i。对每个actual-prefix强制A，取全部完整child SPE终局，A=B_i仅留原actual叶。逐叶d_i≤u_i的first-deviation子树可独立拼合成同一actual叶的纯SPE，复用旧可信接口。

进一步区分逐叶cap凸包、逐A均值cap与全row均值cap。后两者是分析域，不等于纯威胁重选；背景仍为合法m−1份目录负载，source始终可保留原σ。

[tree正文](tree/mean_cap_credible_shadow_working.md)及credible独立重构给全row均值cap的shadow LP对偶η_i、μ_i≥0。对每端点有w·ell≤η_i+μ_i d_i。shared最优负载与原source p下，KKT gap精确为

    G=Σ_i μ_i I_i+Σ_i E_p R_i(A),
    I_i=u_i−E_p d_i^orig(A)≥0,
    R_i(A)=η_i+μ_i d_i^orig(A)−w·ell_i^orig(A)≥0。

故G≥ΣμI。μu不是第二份actual利润，η可负；未付全Cov。余额为

    W−mγ=D−Cov+Σ(1+μ)I+ΣER。

仍需Cov≤D+Σ(1+μ)I+ΣER+(γ+Qstat)/2，或改变路线证明原目标。没有新无条件half界；m5同式仍待付款。

## 本轮推导状态

LP强对偶、扩大域、静态余项与有限未分离均不替代共同金额。各分支自由换路，成熟资产独立攻击，探索不等审批。当前原目标和充分候选均OPEN。

## 后续正文与检查

- [full-slot银行](aggregate/full_slot_cap_dual_norm_bank.md)与[独审](tree/full_slot_norm_independent_review.md)：插入税/曲率组合成m||ρt||²，低有效密度关联未付。
- [aligned fixedpoint](tree/aligned_credible_menu_fixedpoint.md)与[独审](credible/aligned_fixedpoint_review.md)：源/选中边际及future折扣一致；非minimax，不能同时免费领global版G。
- [floor域](tree/reset_floor_domain_independent_check.md)与[RESET](credible/mean_floor_reset_review.md)：raw reset价保全部祖先利润损失；释放actual tags仅为分析域。
- [净cap/BUBBLE](parent/net_cap_bubble_component.md)、[独审](credible/actual_prefix_bubble_review.md)、[QA](parent/netcap_bubble_exact_audit.json)：共同μ、保背景到下一actual行child SPE成立；下一行cap/原source库存未保证，finite只核实现。
- [swap/HALF-R](credible/uniform_copy_swap_component.md)、[独审](tree/uniform_swap_and_raw_flow_independent_review.md)：同row行动平衡及source容量下的signed缺额≤半份R，实际全树流未获这些条件。
- [真重放](tree/real_replay_covariance_flow.md)及[几何重放](geometry/conservative_raw_tail_replay.md)：正流/exact Q端点/一次signed银行成立，几何坐标边未必有Γ，仅总端点功可合用。
- [单query候选](geometry/one_query_convexification_candidate.md)、[条件信息](geometry/conditional_demand_and_information_budget.md)：Vp≤γ、martingale能量和末位transport正确；prefix multiplier未控制，Vp/2付款未证。
- [净cap对称](geometry/uniform_net_cross_history_symmetry.md)：交叉保持shadow，但cap变化是signed量，非自动可行。
- [正loss交换](matching/positive_loss_and_cap_domain_working.md)、[组件审查](matching/frontier_components_independent_review.md)：静态slack准确，没有可行shadow-improving孩子交换。

以上同一般m代m5仍全为条件付款。保留所有Popt/Rep/Out恰好重述原half，不算新钱。无新无条件福利界、目标反例、外审或新颖性认证。

## 实际停界

first-future强制actual主题再BUBBLE可兼容地转运下一child策略到末位，Γ/slack可消去；但多源堆积，arrival不是下一行原source。HALF-R有真1/2因子，却要求同row行动平衡与逐source容量，尚未接到真实Cov系数。

真重放与几何Doob可按相同逐label端点相等总功；这不控制任意target的同叶不同主题收益差、prefix multiplier或signed净cap转移。继续须构造该共同金额/平衡容量，或换路直接付OPT−W。当前具体推导在此停界；不以更多域/改名/阴性冒充进度，未声称所有一般方法不可能，无后台常驻承诺。

各候选的γ、μ/λ、source分布与reduced-cost库存依对应正文的域定义；deleted/full、原source/global-cap与aligned条件source是不同版本，不能把各自好项直接相加。HALF-R的差是经μ计价的signed差，不是未计价缺额或边正部。

[direct最后推导](direct/GENERAL_PROOF_WORKING.md)把足half的未证TAN-PAY集中到实际负载银行(m−1)/(2m)Σρt²c；KKT可限制该银行≤γ/2，但未将r_beta/reset真实映入它。它不是通用PSD/SPE定理，也不增加资金。[root按定义重构真流](parent/real_replay_definition_review.md)独立核查真实Γ、端点、一次source银行和坐标流区别；只核合法表示，未付乘子上界。

六名指定研究员与父方本次具体推导均已落盘交接。原目标仍OPEN，无新增一般福利界/目标反例；该运行窗口的可续结果是条件性HALF-R、保背景BUBBLE及明确的平衡容量/任意target余项，不以更多局部组件冒充一般目标推进。
