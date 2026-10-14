# 命题账本

本分支现有R3完整内部证明的源包络锐渐近和受限拓扑还原；没有全类o(d)上界或严格超源式sup的无限下界。下列文献条目是 Paper Fact，团队并未独立认证全文证明。不得把公屏 idea、数值证据或多人赞同升级为 Canonical Record。

## WC-TARGET v1 — OPEN

- Exact Statement / Conclusion：刻画 MODEL 中 a_*(d)，优先全类 o(d) 存在上界或严格提高核实过基线的无限非存在族下界。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：完全采用 MODEL.md；任意有限 E,N、多资源策略、任意正实权、非负系数次数至多 d，不限制人数。
- Dependencies：WC-LIT-UPPER-D、WC-LIT-LOWER、WC-LIT-N 是基线和约束，不是完成证明。
- Evidence：来源 §7 提出缩小缺口；本轮奇环下界已得a_*(d)≥T_d∼d/ln d，尚无匹配全类存在上界。
- Counterevidence / Objections：奇环成长下界有完整一般证明与独立内部攻击；全类存在上界仍线性，增长阶尚未确定。后续检索未认证全球优先权。
- Status：OPEN；Truth 未判定、Value 取决于贡献、Novelty 未认证、Mechanism 未发现、Ambition 保持全类。
- Related Files：MODEL.md、LITERATURE.md、PRIOR_ASSETS.md、ACCEPTANCE.md。

## WC-LIT-UPPER-D v1 — PAPER FACT

- Exact Statement：每个 d≥1、每个 G∈G_d 存在 d-PNE。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：MODEL 的全类，纯均衡，费用非负系数多项式。
- Conclusion：a_*(d)≤d，非多项式时间承诺，非最强有限 d 界宣称。
- Dependencies：Caragiannis–Fanelli 的近似势函数存在论证。
- Evidence：arXiv:1902.07173 摘要中 (d+δ) 存在保证，δ∈[0,1] 取零；核心下界论文引言及 §7 引述 d 上界。
- Counterevidence / Objections：还需选择性重建证明；社会成本保证的版本差异不影响本条仅记录存在性。
- Status：Paper Fact；未由团队独立证明；Novelty 无。
- Related Files：LITERATURE.md、PRIOR_ASSETS.md。

## WC-LIT-LOWER v1 — PAPER FACT

- Exact Statement：对每个 d≥2、每个 1≤α<α_lit(d)，核心来源定理1的族中存在一个合法游戏没有 α-PNE；游戏可依 α 变化。其式(3)给参数上确界，且 α_lit(d)=Ω(√d/log d)。不得把未取得的 sup 误写成一个固定参数游戏同时达到全部倍率。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：d≥2，多项式非负系数、重玩家与随 d 可增长的轻玩家；渐近结论是大 d，不是小 d 数值公式。
- Conclusion：a_*(d)≥α_lit(d)；不得将渐近常数下界写成精确门槛。
- Dependencies：全状态分两类的偏离比较及显式参数选择。
- Evidence：arXiv:2002.07466v3 §3、Theorem 1、式(3)及其证明。
- Counterevidence / Objections：sup 的端点不一定由一个参数实例取得；数值优化不替代参数全域证明。
- Status：Paper Fact；团队尚未完整重建；Novelty 无。
- Related Files：LITERATURE.md、PRIOR_ASSETS.md。

## WC-LIT-N v1 — PAPER FACT

- Exact Statement：每个有 n 个玩家、任意正权与非递减资源费用的有限加权原子拥塞博弈存在 n-PNE。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：资源独立玩家权、一般非递减费用；非 player-specific cost、非 resource-dependent weights。
- Conclusion：固定人数不能构造随 d 无界的非存在门槛。
- Dependencies：核心来源 §6、Theorem 4。
- Evidence：论文准确陈述；本轮未重建一般证明。
- Counterevidence / Objections：不得从存在性推导高效计算；人数固定的失败不反驳全类目标。
- Status：Paper Fact；Novelty 无。
- Related Files：LITERATURE.md、MODEL.md。

## R3-SOURCE-SHARP-ASYMPTOTIC-v1 — INTERNAL PROOF

- Exact Statement / Conclusion：原式(3)源域全部参数sup F_d∼(2/√e)√(d ln ln d)/ln d。显式合法family在两类偏离均趋同常数，故a_*(d)≥(2/√e−o(1))同scale。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：d≥2整数，n≥1整数，k∈{1,…,d}，0<w≤1，0≤β≤1；F_d为两认证倍率min之sup，非单游戏exact threshold或全类上界。
- Dependencies：MODEL、源式(3)两个全状态attack（本轮已独立重构）；完整证明不导入既有matching O上界。
- Evidence：assets/R3/sharp_source_review/proof.md、review.md；Decimal验证仅诊断，未用来证明一般不等式。
- Counterevidence / Objections：未见fatal objection；极慢收敛不影响asymptotic，未认证后续文献全球优先权。源式sup本来已知，因此不称严格超过其基线。
- Status：完整一般证明与独立内部攻击；未外审。Truth有proof、Value给参数优化边界、Novelty未认证、Mechanism全局消元与局部化、Ambition为受限族。
- Related Files：assets/R3/sharp_source_review/、../current/weighted_congestion_frontier.md、根graph/review_status/assets。

## WC-R3-FULL-TOPOLOGY-REDUCTION v3 — INTERNAL PROOF

- Version history：v1 α≥2；v2 α≥φ、全部w>0；v3 α≥ρ=(1+√3)/2，右支单轻玩家允许w反演；每版范围明确，旧版为subcase。
- Exact Statement：对每个degree≤d对称同轻权两列F,G游戏和每个α≥ρ，若无α-PNE，则存在原式(3)域内monomial参数，其两test均strict通过同α。
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope：n≥1整数，w>0，F,G任意非负系数degree≤d同主/同副多项式；完整策略参proof；新游戏参数可改变。
- Conclusion：源包络F_d≤actual拓扑sup T_d≤max{ρ,F_d}；F_d≥ρ时T_d=F_d，所以该拓扑与源包络有同一sharp asymptotic。非a_*(d)上界。
- Dependencies：light稳定区间/反射、平移保持系数、右支n′α(α−1)<1和单轻反演、endpoint chord及系数线性消元。
- Evidence：assets/R3/full_topology/proof.md、verify.py/results.json；assets/R3/topology_attack/review.md及独立literal checker。
- Counterevidence / Objections：初版φ仅w≤1的解释已由w≥1时z≥u机制补齐；v3不能坚持整个还原保持原w。F≡0直接存在PNE，zero分母未除。未见fatal objection。
- Status：完整一般证明及独立攻击；未外审、未认证novelty。Truth有proof、Value封闭整个受限搜索、Mechanism为整数稳定区间、Ambition不涉及异权/交叉拓扑。
- Related Files：assets/R3/full_topology/、assets/R3/topology_attack/、../current/weighted_congestion_frontier.md。

## WC-R3-SOURCE32-178-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: For every original source parameter, min(H,L)<=89/50; all n,k and real w,beta are covered by analytic reduction plus exact negative interval certificates.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: exact identity in `research/weighted_congestion_frontier/assets/R3/source32_bound/PROOF.md`; MODEL cost and weak equilibrium conventions apply. No claim of a full-class upper bound.
- Dependencies: WC-SOURCE-FORMULA; all joint premises remain explicit.
- Evidence: research/weighted_congestion_frontier/assets/R3/source32_bound/certificate.json, research/weighted_congestion_frontier/assets/R3/source32_bound/verification.json, research/weighted_congestion_frontier/assets/R3/crossover_audit/main_check_results.json; separate independently authored verifier and direct reconstruction.
- Counterevidence / Objections: no remaining objection to the exact stated scope; fixed-degree improvement does not prove an unbounded family. External review and priority unverified.
- Status: complete exact statements with independent internal reconstruction; unrefereed. Truth: proved stated scope; Value: reusable separation/sign certificate/failure; Novelty: unassessed; Mechanism: explicit incidence and real-domain elimination; Ambition: WC-TARGET OPEN.
- Related Files: research/weighted_congestion_frontier/assets/R3/source32_bound/PROOF.md, research/weighted_congestion_frontier/assets/R3/source32_bound/verify.py, research/weighted_congestion_frontier/assets/R3/crossover_audit/main_check.py

## WCF-R3-CROSS32-AUDIT-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: One explicit rational four-player 14-resource game has strict >9/5 improvement at every pure state; its exact best factor is frozen. No growing lower-family implication.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: exact identity in `research/weighted_congestion_frontier/assets/R3/crossover_audit/README.md`; MODEL cost and weak equilibrium conventions apply. No claim of a full-class upper bound.
- Dependencies: WC-MODEL; all joint premises remain explicit.
- Evidence: research/weighted_congestion_frontier/assets/R3/crossover_audit/degree32_certificate.json, research/weighted_congestion_frontier/assets/R3/crossover_audit/main_check_results.json; separate independently authored verifier and direct reconstruction.
- Counterevidence / Objections: no remaining objection to the exact stated scope; fixed-degree improvement does not prove an unbounded family. External review and priority unverified.
- Status: complete exact statements with independent internal reconstruction; unrefereed. Truth: proved stated scope; Value: reusable separation/sign certificate/failure; Novelty: unassessed; Mechanism: explicit incidence and real-domain elimination; Ambition: WC-TARGET OPEN.
- Related Files: research/weighted_congestion_frontier/assets/R3/crossover_audit/README.md, research/weighted_congestion_frontier/assets/R3/crossover_audit/verify_degree32.py, research/weighted_congestion_frontier/assets/R3/crossover_audit/main_check.py

## WCF-R3-FIXED-DEGREE-FAIL-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: Keeping crossover weights/amplitudes and raising six degrees gives a 9/5-PNE at degree40; best factors converge to 5235403/2930833<9/5. Reweighting is not excluded.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: exact identity in `research/weighted_congestion_frontier/assets/R3/crossover_audit/README.md`; MODEL cost and weak equilibrium conventions apply. No claim of a full-class upper bound.
- Dependencies: WC-MODEL; all joint premises remain explicit.
- Evidence: research/weighted_congestion_frontier/assets/R3/crossover_audit/degree40_failure_certificate.json, research/weighted_congestion_frontier/assets/R3/crossover_audit/fixed_weight_limit_certificate.json, research/weighted_congestion_frontier/assets/R3/crossover_audit/fixed_degree_scan.json, research/weighted_congestion_frontier/assets/R3/crossover_audit/main_check_results.json; separate independently authored verifier and direct reconstruction.
- Counterevidence / Objections: no remaining objection to the exact stated scope; fixed-degree improvement does not prove an unbounded family. External review and priority unverified.
- Status: complete exact statements with independent internal reconstruction; unrefereed. Truth: proved stated scope; Value: reusable separation/sign certificate/failure; Novelty: unassessed; Mechanism: explicit incidence and real-domain elimination; Ambition: WC-TARGET OPEN.
- Related Files: research/weighted_congestion_frontier/assets/R3/crossover_audit/README.md, research/weighted_congestion_frontier/assets/R3/crossover_audit/verify_degree32.py, research/weighted_congestion_frontier/assets/R3/crossover_audit/main_check.py

## WC-R3-CROSS32-TOPOLOGY-SEPARATION-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: T32<=89/50<9/5<B(G), allowing all positive common light weights and arbitrary nonnegative principal/side polynomial coefficients in the symmetric topology.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: exact identity in `research/weighted_congestion_frontier/assets/R3/crossover_audit/separation.md`; MODEL cost and weak equilibrium conventions apply. No claim of a full-class upper bound.
- Dependencies: WC-R3-SOURCE32-178-v1, WCF-R3-CROSS32-AUDIT-v1, WC-R3-FULL-TOPOLOGY-REDUCTION-v3; all joint premises remain explicit.
- Evidence: research/weighted_congestion_frontier/assets/R3/crossover_audit/main_check_results.json; separate independently authored verifier and direct reconstruction.
- Counterevidence / Objections: no remaining objection to the exact stated scope; fixed-degree improvement does not prove an unbounded family. External review and priority unverified.
- Status: complete exact statements with independent internal reconstruction; unrefereed. Truth: proved stated scope; Value: reusable separation/sign certificate/failure; Novelty: unassessed; Mechanism: explicit incidence and real-domain elimination; Ambition: WC-TARGET OPEN.
- Related Files: research/weighted_congestion_frontier/assets/R3/crossover_audit/separation.md, research/weighted_congestion_frontier/assets/R3/crossover_audit/main_check.py

## WC-R3-DENSE-SHARE-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: For all positive real finite weight sets and nonnegative polynomial c, uniform Shapley shares of W*c(W) have increasing raw shares, decreasing shares per weight, and minw*c(W)<=phi_i<=maxw*c(W).
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/weighted_congestion_frontier/assets/R3/dense_bands/README.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/weighted_congestion_frontier/assets/R3/dense_band_review/independent_review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/weighted_congestion_frontier/assets/R3/dense_bands/README.md, research/weighted_congestion_frontier/assets/R3/dense_band_review/independent_review.md, research/weighted_congestion_frontier/assets/R3/dense_bands/verify.py, research/weighted_congestion_frontier/assets/R3/dense_band_review/independent_check.py, research/weighted_congestion_frontier/assets/R3/dense_bands/verification.json, research/weighted_congestion_frontier/assets/R3/dense_band_review/independent_verification.json

## WC-R3-DENSE-LOCAL-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: For every finite polynomial congestion game, resource potential-user weight ratio at most R>=1 ensures every stated scaled-potential minimizer is R-PNE, with no degree or cardinality factor. Empty strategies and zero costs included.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/weighted_congestion_frontier/assets/R3/dense_bands/README.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL, WC-R3-DENSE-SHARE-v1 and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/weighted_congestion_frontier/assets/R3/dense_band_review/independent_review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/weighted_congestion_frontier/assets/R3/dense_bands/README.md, research/weighted_congestion_frontier/assets/R3/dense_band_review/independent_review.md, research/weighted_congestion_frontier/assets/R3/dense_bands/verify.py, research/weighted_congestion_frontier/assets/R3/dense_band_review/independent_check.py, research/weighted_congestion_frontier/assets/R3/dense_bands/verification.json, research/weighted_congestion_frontier/assets/R3/dense_band_review/independent_verification.json

## WC-R3-DENSE-POT-SHARP-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: For every fixed R>1, an explicit finite-game sequence of local ratio R has unique stated-potential minimizers with factors tending to R, while each game has an exact PNE.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/weighted_congestion_frontier/assets/R3/dense_bands/README.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL, WC-R3-DENSE-SHARE-v1 and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/weighted_congestion_frontier/assets/R3/dense_band_review/independent_review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/weighted_congestion_frontier/assets/R3/dense_bands/README.md, research/weighted_congestion_frontier/assets/R3/dense_band_review/independent_review.md, research/weighted_congestion_frontier/assets/R3/dense_bands/verify.py, research/weighted_congestion_frontier/assets/R3/dense_bands/verification.json

## WC-R3-BAND-CURL-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: Two users of weights 1,M>1 with cubic total cost give incompatible mixed differences kappa versus kappa/M for separately normalized Shapley marginals. This does not rule out weighted or other potentials.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/weighted_congestion_frontier/assets/R3/dense_bands/README.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-R3-DENSE-SHARE-v1 and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/weighted_congestion_frontier/assets/R3/dense_band_review/independent_review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/weighted_congestion_frontier/assets/R3/dense_bands/README.md, research/weighted_congestion_frontier/assets/R3/dense_band_review/independent_review.md, research/weighted_congestion_frontier/assets/R3/dense_bands/verify.py, research/weighted_congestion_frontier/assets/R3/dense_bands/verification.json

## WC-R3-BAND-LINEAR-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: For every integer d>=7 the specified unmodified/scaled Shapley selector has unique minima with factor at least d/6 although exact PNE exists. Optional empty-choice padding makes each potential band arbitrarily dense without rescuing this selector.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/weighted_congestion_frontier/assets/R3/dense_bands/README.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL, WC-R3-DENSE-SHARE-v1 and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/weighted_congestion_frontier/assets/R3/dense_band_review/independent_review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/weighted_congestion_frontier/assets/R3/dense_bands/README.md, research/weighted_congestion_frontier/assets/R3/dense_band_review/independent_review.md, research/weighted_congestion_frontier/assets/R3/dense_bands/verify.py, research/weighted_congestion_frontier/assets/R3/dense_bands/verification.json

## WCF-R3-SCALED-ORIGINAL-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: For weights (1,1/(10m),1/(20m),1/(50m)), six degrees32m^2 and original amplitudes, B(G_m)->65/34 and every m>=1 has no9/5-PNE. Any fixed alpha<65/34 is obstructed for all sufficiently large m.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_family.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/weighted_congestion_frontier/assets/R3/limit_review/review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_family.md, research/weighted_congestion_frontier/assets/R3/limit_review/review.md, research/weighted_congestion_frontier/assets/R3/crossover_audit/verify_limit.py, research/weighted_congestion_frontier/assets/R3/limit_review/check_independent.py, research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_evidence/finite_scans.json, research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_evidence/scaled_limits.json, research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_evidence/uniform_bounds.json, research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_evidence/retuned_m3_certificate.json, research/weighted_congestion_frontier/assets/R3/limit_review/independent_evidence.json

## WCF-R3-SCALED-RETUNED-v2 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: With exactly the displayed retuned rational amplitudes, every m>=20 and separately m=3 gives no2-PNE; m=1,2 have2-PNE; B(G_m)->100/49. Version1 m>=52 is a proved subcase, not silently rewritten.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_family.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/weighted_congestion_frontier/assets/R3/limit_review/review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_family.md, research/weighted_congestion_frontier/assets/R3/limit_review/review.md, research/weighted_congestion_frontier/assets/R3/crossover_audit/verify_limit.py, research/weighted_congestion_frontier/assets/R3/limit_review/check_independent.py, research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_evidence/finite_scans.json, research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_evidence/scaled_limits.json, research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_evidence/uniform_bounds.json, research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_evidence/retuned_m3_certificate.json, research/weighted_congestion_frontier/assets/R3/limit_review/independent_evidence.json

## WCF-R3-SCALED-TEMPLATE-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: For every real 1<=alpha<r, r>2 root of r^3-r^2-2r-1, fixed rational amplitudes and a finite M yield strict alpha improvement at every state for all m>=M. The selected-witness cone is infeasible at alpha>=r; full-topology optimality is unclaimed.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_family.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/weighted_congestion_frontier/assets/R3/limit_review/review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_family.md, research/weighted_congestion_frontier/assets/R3/limit_review/review.md, research/weighted_congestion_frontier/assets/R3/crossover_audit/verify_limit.py, research/weighted_congestion_frontier/assets/R3/limit_review/check_independent.py, research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_evidence/finite_scans.json, research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_evidence/scaled_limits.json, research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_evidence/uniform_bounds.json, research/weighted_congestion_frontier/assets/R3/crossover_audit/limit_evidence/retuned_m3_certificate.json, research/weighted_congestion_frontier/assets/R3/limit_review/independent_evidence.json

## WC-R3-POTENTIAL-DENSITY-PADDING-v1 — COMPLETE STATED SCOPE

- Exact Statement / Conclusion: Arbitrary finite empty/{e} positive-weight padding preserves all finite-alpha equilibrium projection/lift and original deviation costs. Every occupied potential-weight interval can have minimum count L, yet that subclass and the full G_d have identical successful-factor sets and thresholds.
- Objects / Domain / Quantifiers / Assumptions / Definitions / Scope: full exact identity in `research/weighted_congestion_frontier/assets/R3/potential_padding/proof.md`; arbitrary positive real weights where universally quantified, specified rational amplitudes for constructive families, MODEL weak cost inequalities.
- Dependencies: WC-MODEL and the direct proof in the linked account. No unproved migration between models.
- Evidence: authored general proof, independently reconstructed review `research/weighted_congestion_frontier/assets/R3/potential_padding/review.md`, and actual exact code/records listed below. Finite sampling remains separate from proof.
- Counterevidence / Objections: selector failures do not prove nonexistence; occupied interval is not every geometric interval; retuned m1,m2 fail; cubic boundary is only for prescribed witnesses. No unresolved fatal objection within stated scope.
- Status: complete stated-scope proofs with independent internal reconstruction; unrefereed. Truth: stated scope proved; Value: reusable interface/obstruction/reduction; Novelty: unassessed; Mechanism: explicit linked derivation; Ambition: full WC-TARGET remains OPEN.
- Related Files: research/weighted_congestion_frontier/assets/R3/potential_padding/proof.md, research/weighted_congestion_frontier/assets/R3/potential_padding/review.md, research/weighted_congestion_frontier/assets/R3/potential_padding/verify.py, research/weighted_congestion_frontier/assets/R3/potential_padding/independent_check.py, research/weighted_congestion_frontier/assets/R3/potential_padding/verification.json, research/weighted_congestion_frontier/assets/R3/potential_padding/independent_verification.json

## WC-R3-ODD-RING-CERTIFICATE-v1 — COMPLETE GENERAL PROOF / INTERNAL REVIEW

- Exact Statement / Conclusion: For odd m>=3, n_i>=1, positive u_i,v_i, 1<=k_i<=d and alpha>1, the specified two strict local tests have positive coefficients iff all N_i,Q_i>0 and product n_i N_i Q_i/(M_i P_i)>1. They exclude alpha-PNE at every state.
- Objects / Domain / Quantifiers / Assumptions / Definitions: full exact identity in `assets/R3/odd_ring_sharp/PROOF.md`, sections 1–6; costs and weak alpha-PNE use MODEL.md. Positive rational construction is a subclass of arbitrary positive-real-weight G_d.
- Scope: Fixed exact positive local-test system; iff is coefficient feasibility, not all possible ring nonexistence.
- Dependencies: WC-MODEL; explicit elementary proofs, no imported nonexistence theorem.
- Evidence: complete general proof, independent reconstruction before reading the initial route, two envelope attacks, Fraction full-state small game and separate exact growing-certificate checks.
- Counterevidence / Objections: no unresolved fatal objection in the stated scope; finite tests do not prove generality. Later-literature search is not exhaustive; global priority unverified.
- Status: canonical stated-scope internal mathematical result, unrefereed. Truth: proved scope; Value: growing lower/usable mechanism boundary; Novelty: unverified; Mechanism: odd parity and weight-cycle amplification; Ambition: lower stage breakthrough, WC-TARGET OPEN.
- Related Files: `research/current/weighted_congestion_frontier.md`, `assets/R3/odd_ring_sharp/PROOF.md`, `assets/R3/odd_ring_sharp/verify.py`, `assets/R3/odd_ring_sharp/verification.json`, `assets/R3/odd_ring_independent/REVIEW.md`, `assets/R3/odd_ring_independent/EXACT_ENVELOPE_REVIEW.md`, `assets/R3/odd_ring_parameters/exact_envelope_review.md`, `assets/R3/odd_ring_literature/notes.md`.

## WC-R3-ODD-RING-ENVELOPE-v1 — COMPLETE GENERAL PROOF / INTERNAL REVIEW

- Exact Statement / Conclusion: For each d>=2 and alpha>1, some finite odd ring satisfies the positive monomial local-test system iff alpha<T_d=sup_R>1 [R(1+R)^d+1]/[(1+R)^d+R^(d+1)]. H_d<T_d<=H_d+1/(2^d+1), H_d=d/[(d+1)d^(1/(d+1))-d], hence T_d~d/ln d.
- Objects / Domain / Quantifiers / Assumptions / Definitions: full exact identity in `assets/R3/odd_ring_sharp/PROOF.md`, sections 1–6; costs and weak alpha-PNE use MODEL.md. Positive rational construction is a subclass of arbitrary positive-real-weight G_d.
- Scope: Certificate envelope only; failure does not imply an equilibrium. Strict endpoint alpha=T_d is infeasible for these tests.
- Dependencies: WC-MODEL, WC-R3-ODD-RING-CERTIFICATE-v1; explicit elementary proofs, no imported nonexistence theorem.
- Evidence: complete general proof, independent reconstruction before reading the initial route, two envelope attacks, Fraction full-state small game and separate exact growing-certificate checks.
- Counterevidence / Objections: no unresolved fatal objection in the stated scope; finite tests do not prove generality. Later-literature search is not exhaustive; global priority unverified.
- Status: canonical stated-scope internal mathematical result, unrefereed. Truth: proved scope; Value: growing lower/usable mechanism boundary; Novelty: unverified; Mechanism: odd parity and weight-cycle amplification; Ambition: lower stage breakthrough, WC-TARGET OPEN.
- Related Files: `research/current/weighted_congestion_frontier.md`, `assets/R3/odd_ring_sharp/PROOF.md`, `assets/R3/odd_ring_sharp/verify.py`, `assets/R3/odd_ring_sharp/verification.json`, `assets/R3/odd_ring_independent/REVIEW.md`, `assets/R3/odd_ring_independent/EXACT_ENVELOPE_REVIEW.md`, `assets/R3/odd_ring_parameters/exact_envelope_review.md`, `assets/R3/odd_ring_literature/notes.md`.

## WC-R3-ODD-RING-LOWER-v1 — COMPLETE GENERAL PROOF / INTERNAL REVIEW

- Exact Statement / Conclusion: For every integer d>=2 and real 1<=alpha<T_d, a finite rational-weight/coefficient congestion game, all resource latencies positive monomials of degree exactly d, has no alpha-PNE. Therefore a_*(d)>=T_d~d/ln d and liminf a_*(d)ln(d)/d>=1.
- Objects / Domain / Quantifiers / Assumptions / Definitions: full exact identity in `assets/R3/odd_ring_sharp/PROOF.md`, sections 1–6; costs and weak alpha-PNE use MODEL.md. Positive rational construction is a subclass of arbitrary positive-real-weight G_d.
- Scope: Game may depend on alpha; unbounded player count/support and huge input size allowed. No endpoint game, polynomial-time construction, full-class upper, matched growth, or global priority claim.
- Dependencies: WC-MODEL, WC-R3-ODD-RING-CERTIFICATE-v1, WC-R3-ODD-RING-ENVELOPE-v1; explicit elementary proofs, no imported nonexistence theorem.
- Evidence: complete general proof, independent reconstruction before reading the initial route, two envelope attacks, Fraction full-state small game and separate exact growing-certificate checks.
- Counterevidence / Objections: no unresolved fatal objection in the stated scope; finite tests do not prove generality. Later-literature search is not exhaustive; global priority unverified.
- Status: canonical stated-scope internal mathematical result, unrefereed. Truth: proved scope; Value: growing lower/usable mechanism boundary; Novelty: unverified; Mechanism: odd parity and weight-cycle amplification; Ambition: lower stage breakthrough, WC-TARGET OPEN.
- Related Files: `research/current/weighted_congestion_frontier.md`, `assets/R3/odd_ring_sharp/PROOF.md`, `assets/R3/odd_ring_sharp/verify.py`, `assets/R3/odd_ring_sharp/verification.json`, `assets/R3/odd_ring_independent/REVIEW.md`, `assets/R3/odd_ring_independent/EXACT_ENVELOPE_REVIEW.md`, `assets/R3/odd_ring_parameters/exact_envelope_review.md`, `assets/R3/odd_ring_literature/notes.md`.

## WC-R3-ODD-RING-POLYNOMIAL-ENVELOPE-v1 — COMPLETE STATED-SCOPE PROOF

- Exact Statement / Conclusion: For d>=2 and alpha>1, allowing each odd-ring group independent nonnegative degree-at-most-d shapes F_i,G_i, common across its action copies/cohort, does not change positive two-local-test feasibility: some finite certificate exists iff alpha<T_d. Constants in mixtures and arbitrary positive real weights are covered; zero shapes cannot satisfy the strict tests.
- Objects / Domain / Quantifiers / Assumptions / Definitions: PROOF.md section8, d>=2, alpha>1, finite odd ring, n_i>=1, nonnegative shapes degree<=d, resource-independent positive weights, shared action/cohort shapes and positive group amplitudes. Feasibility is existential over shapes/parameters.
- Scope: This is a certificate ceiling, not full-class or actual-topology equilibrium existence. Action-specific and clone-specific shape asymmetries are excluded. Sufficiency existential over chosen shapes, not for every prescribed shape.
- Dependencies: WC-R3-ODD-RING-CERTIFICATE-v1 and ENVELOPE-v1, plus exact denominator-weighted convex identities, including degree0 negative factors.
- Evidence: general proof independently attacked; actual Fraction mixed-degree checks with constants, zero-shape exclusions and signed individual differences.
- Counterevidence / Objections: no unresolved fatal within scope; infeasibility does not supply a pure stable profile. General partially aligned cohort and reverse light deviations remain an actual-topology gap.
- Status: stated-scope internally proved, unrefereed. Truth: proved; Value: closes mixed-shape tuning; Novelty: unassessed; Mechanism: convexity with positive denominators; Ambition: boundary, WC-TARGET OPEN.
- Related Files: assets/R3/odd_ring_sharp/PROOF.md section8; assets/R3/odd_ring_parameters/polynomial_envelope_review.md; check_polynomial_envelope.py; polynomial_envelope_verification.json.

## WC-R3-ODD-RING-SINGLETON-UPPER-v1 — COMPLETE RESTRICTED EXISTENCE PROOF

- Exact Statement / Conclusion: Every odd m>=3 ring with n_i=1 at every group, arbitrary positive real weights, symmetric action copies and nonnegative polynomial fees of degree at most d>=2 (zero fees permitted), has a min{2,T_d}-PNE. A T_d-PNE exists among the 2m single-conflict profiles modulo global action exchange.
- Objects / Domain / Quantifiers / Assumptions / Definitions: every finite odd m>=3, all n_i=1, positive real u_i,v_i, same group fee shape on both action copies, nonnegative degree<=d, d>=2; zero resources allowed. Uses MODEL's weak alpha-PNE, exact pure costs.
- Scope: Restricted actual-topology existence, not sharpness and not a general-cohort or full-model upper. The smaller factor-2 equilibrium is not claimed to be single-conflict when 2<T_d.
- Dependencies: WC-R3-ODD-RING-POLYNOMIAL-ENVELOPE-v1; exact defect-state cycle, correct reversed ring/role map, direct total-cost support-two inequality in PROOF.md section9.
- Evidence: internal independent defect-graph derivation, root reconstruction and exact small graph checks including zero fees and reverse resource/player map. Finite code uses safe alpha=d; endpoint T_d is established by the general proof.
- Counterevidence / Objections: more than one light per group destroys the simple defect-cycle representation; cannot promote this to arbitrary cohorts. No unresolved fatal within stated scope.
- Status: internally proved, unrefereed. Truth: stated subclass proved; Value: actual-topology boundary and representation; Novelty: unverified; Mechanism: arc counting/reversed roles/support; Ambition: structural subcase, WC-TARGET OPEN.
- Related Files: assets/R3/odd_ring_sharp/PROOF.md section9; assets/R3/odd_ring_parameters/SINGLETON_NOTE.md; check_singleton_graph.py; singleton_graph_verification.json.
