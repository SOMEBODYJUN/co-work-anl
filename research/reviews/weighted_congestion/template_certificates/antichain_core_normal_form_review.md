# 空交反链核心规范形的独立重构与冻结攻击

Read only `research/weighted_congestion_frontier/MODEL.md` before this reconstruction. No author proof was consulted.

## Construction

Let G have finite resource set E, players N, positive real weights w_i, nonnegative-coefficient polynomials c_e of degree at most d, and finite nonempty strategy families S_i. For each i let M_i be the family of inclusion-minimal members of S_i, and set I_i = intersection of M_i. Every T in S_i contains some M in M_i, since S_i is finite. Write R = {i : |M_i| >= 2}.

If R is empty, choose for every player the unique member of M_i. This is an explicit exact PNE: that member is contained in every original strategy of player i, hence its deviation cost is weakly smaller with all other players fixed.

Otherwise form H on the same resource set E and players R, retaining w_i. Set

    K_e = sum_{i in N : e in I_i} w_i,
    h_e(x) = c_e(x + K_e),
    T_i = {M minus I_i : M in M_i}  (i in R).

All h_e remain degree-at-most-d polynomials with nonnegative coefficients, by the binomial formula. Each T_i has at least two distinct members, is an inclusion antichain, has empty total intersection, and all its members are nonempty: an empty residual would make its original member I_i a subset of every other member of M_i, contradicting minimality when |M_i| >= 2.

The fixed lift L is

    L(t)_i = I_i union t_i   if i in R,
    L(t)_i = I_i            if i not in R.

For i not in R, I_i is its unique inclusion-minimal original strategy.

## Uniform lift proof

At a lifted state, the load of resource e in G is K_e plus its optional load in H. This identity holds after every retained-player deviation to a member of M_i as well. For i in R put

    B_i(t_{-i}) = sum_{e in I_i} c_e(K_e + x_e^H(t)).

Because no residual strategy of player i contains e in I_i, B_i is independent of i's strategy. Hence current and minimal-deviation costs decompose as

    C_i^G(L(t)) = B_i + C_i^H(t),
    C_i^G(M, L(t)_{-i}) = B_i + C_i^H(M minus I_i, t_{-i}).

If t is an alpha-PNE for any real alpha >= 1, then B_i >= 0 gives

    C_i^G(L(t)) <= B_i + alpha C_i^H(M minus I_i, t_{-i})
                <= alpha C_i^G(M, L(t)_{-i}).

For any original deviation T choose M in M_i with M subset T. Its deviation cost is at least the cost of deviating to M: resource loads on M agree and the extra resources of T contribute nonnegative costs. Thus the alpha condition holds for T as well. A removed player is an exact best responder because its fixed I_i is contained in each original strategy, with equality of costs on common resources. Consequently every alpha-PNE of H lifts to an alpha-PNE of G, simultaneously for all real alpha >= 1. Construction and lift are alpha-independent.

This establishes the requested statement, including d=0, empty original strategies, zero costs, and singleton strategy families. No reverse lifting claim is used.

## Corollary plan using integer-monomial counterexample theorem

Given no-alpha-PNE G, first use the allowed integer-monomial counterexample theorem to obtain a no-alpha-PNE game K with positive integer weights and each resource cost x^j (0 <= j <= d). Apply the core reduction to K. The direct-PNE branch is impossible. Mandatory loads K_e are now nonnegative integers, so each shifted resource cost (x+K_e)^j has nonnegative integer coefficients and its leading coefficient is 1. Replace resource e with a disjoint block of b_{e,k} unit resources of cost x^k for each coefficient b_{e,k}; replace every occurrence of e in each strategy by its entire block. Every block is nonempty because the leading coefficient is 1. Thus nonemptiness, cardinality, antichain, and empty strategy intersection are preserved. Costs and pure states correspond exactly. The resulting integer-weight unit-monomial core game has no alpha-PNE. The converse follows from inclusion in the original class.

This plan requires from the external theorem only existence of a finite integer-weight unit-monomial no-alpha-PNE game at the fixed d and real alpha, not incidence-structure preservation.

## Allowed external theorem checked after reconstruction

After freezing the argument above, read the statement and §§1–3 of `research/current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md`. WC-INTEGER-MONOMIAL-COUNTEREXAMPLE-v1 has exactly the needed fixed-d, fixed-real-alpha scope. It may add mandatory private constants to make strategies nonempty; the core reduction simply removes these from strategic costs. No theorem strengthening or structure-preservation assumption is required by the corollary.

## Adversarial edge checks before author-proof comparison

- Resourcewise, mandatory loads include both retained and removed players; omitting retained players' common resources from K_e would be wrong.
- B_i may depend on other players' actions but not on i's current action or deviation, which is all the lift proof needs.
- The lift is from reduced alpha equilibria to original alpha equilibria only; original alpha equilibria can fail to descend after deleting B_i.
- For arbitrary supersets, the resource loads on the included minimal strategy are exactly equal in the two deviation profiles; only nonnegativity of the extra resource costs is needed here.
- There is no need to iterate minimization after shifting fees or deleting mandatory sets: set-inclusion comparisons are preserved by removing a common set.
- Keeping the entire original E ensures legal nonempty resources and, if “same degree” means actual maximal resource polynomial degree rather than the bound d, preserves that degree too.
- All-zero fees, original empty strategies, and d=0 cause no division, no 0/0, and no unsupported strictness claim.
- In the integer corollary, every shifted unit monomial has a nonzero leading coefficient 1; hence no resource block vanishes under coefficient expansion, and the expansion is injective on resource-subset strategies.

## Final frozen-proof adversarial review

## Freeze identity and chronology

The complete reconstruction at the start of this file was written and sent to root before the author proof was supplied. The allowed integer-monomial theorem was read only after that reconstruction. Then the author freeze `/workspace/scratch/ecf05625b47b/antichain_core_normal_form_frozen.md` was read. Its SHA256 was actually recomputed as

`0b7735af99dbd9657710fa5c5f94ed4af00649833bad3d60d1c1dd32caa4eb29`,

matching root's specified freeze. The pre-author-proof version of this independent file, including the independent theorem application plan and edge checks, had SHA256 `8cd50b99ac4888697af9bcd5e9133d690602185f4e204a4f00330a881d09cb29` immediately before this final appended review.

## Verdict

PASS for the exact stated structural reduction and fixed-(d, alpha) counterexample equivalence. No blocking mathematical error or missing model hypothesis was found. This is an independent internal review, not external review or a novelty certification. It does not establish the full-class asymptotic target.

## Detailed attack results

1. **Quantifiers and legal objects.** The construction has no alpha input. Retained weights are literally the original weights; retained players form J, a nonempty original subset in the H branch. Same E is used, so E remains nonempty even if some resources are unused. All transformed coefficients are nonnegative by the positive shift. The d=0 case needs no exception. If J is empty, the proof returns a genuine original exact PNE, rather than an illegal empty-player game.

2. **Minimality and arbitrary original deviations.** Every original strategy contains an inclusion-minimal strategy, by finiteness. For a subset deviation a subset t, the actual own-presence load on every e in a is identical in the two deviated profiles; the difference consists only of nonnegative charges on t minus a. Thus the domination step does not freeze old loads and does not need a hidden resource-monotonicity argument.

3. **Set structure.** Removing the common F_i preserves injectivity and all subset relations among the minimal strategies. With at least two members, an empty residual would imply one minimal strategy is contained in another, impossible. Intersection becomes exactly empty. The extra author observation F_i = intersection S_i is correct in both directions and causes no unstated assumption.

4. **Mandatory background accounting.** B_e includes mandatory weights of every original player, both retained and removed. This is necessary and correctly done. Optional load plus B_e is the original load resource by resource. For e in F_i, player i has no optional occurrence of e, so K_i depends on other players' optional choices only. Hence the same K_i occurs in current and every minimal-deviation cost. Shared mandatory resources and an e that is mandatory to one player but optional to another are both covered.

5. **All alpha simultaneously.** The key implication is precisely r <= alpha r' and K >= 0 implies r+K <= alpha(r'+K) for alpha >= 1. The proof applies this without division, so zero current costs, zero deviation costs, and alpha=1 are valid. Removed players are exact best responders against every lifted profile, not merely selected equilibria. Approximate equilibria need not project backward; the author explicitly disclaims that false converse.

6. **Integer unit-monomial corollary.** The allowed theorem is used before core reduction, so no unsupported claim that it preserves core structure is needed. After integer weights, every mandatory B_e is a nonnegative integer and every shift (x+B_e)^k has nonnegative integer coefficients. Its leading coefficient is 1, including k=0 in its constant interpretation. Therefore every old resource has a nonempty disjoint clone block. Such a block map preserves equality, subset relations, nonempty strategies, distinct strategy count and empty intersection. Each clone load is the old optional load and summed clone fees equal the shifted fee at every current/deviated profile. The equivalence is consequently valid for each fixed real alpha, with no rational-alpha assumption.

7. **Scope.** The result removes fixed players, containments and mandatory backgrounds from possible counterexamples but supplies no uniform bound on players, strategies, resources or weights. Section 5's application must be understood only at d, alpha values for which alpha is defined and at least 1 (as already required by the exact statement). No asymptotic upper bound, improving lower-bound family or solution of the main target follows from this reduction.

## Independent literal audit

Wrote `/workspace/scratch/ecf05625b47b/core_normal_form_independent_audit.py` using only Python's standard library, `Fraction`, and its own literal current/deviation cost evaluator. It imports no repository proof or verification code. Executed successfully; output is `/workspace/scratch/ecf05625b47b/core_normal_form_independent_audit.json`.

Audit scope: six explicit finite fixtures whose original games have 98 profiles in total; the cost/lift audit exhausts their 16 total core profiles, at six rational multipliers 1, 4/3, 3/2, 2, 5, 100. Across the core fixtures it checks 56 exact minimal-deviation cost decompositions, 92 literal superset-deviation cost comparisons and 48 nonvacuous equilibrium-lift cases. The integer fixture verifies the literal mandatory/optional-overlap expansion (x+2)^2 = x^2+4x+4, builds 13 unit-monomial clones, and checks 24 exact current/deviation costs. Fixture coverage includes original empty strategies, zero fees with active players, inclusion-dominated strategies, shared mandatory loads, a resource mandatory to one player and optional to another, all-player deletion, d=0, positive rational weights, and the one-way-only nature of approximate lifting. In the latter fixture, original costs 110 and 101 make the first action a 2-PNE, while corresponding core costs 10 and 1 make its projection fail 2-PNE.

All audit assertions passed. These are finite exact-arithmetic checks and do not constitute the proof of the universal statements; the general proof is reviewed above.

Audit script SHA256: `85011180247de835d30a8ab9170ecaa14e908d8f05ac56897f58a9f250204467`.

Audit output SHA256: `2468dd1215d011cb1b8d4543f9904f3fdadfeddbb345f6f7635ed8b533b3e345`.

No repository files were changed by this reviewer; no Git write or external message was performed.

## 入库版本与规范命令

当前正文追加于[整数规范形、空交核心与端点](../../../current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md)第7节；旧两个Claim及第1–6节不由本审查替代。新增部分与上述冻结稿数学内容相同，只调整标题编号、路径和独立审查状态。

独立源码迁入`tests/audits/weighted_congestion/template_certificates/independent_antichain_core.py`。主研究者仅删除启动时读取暂存冻结正文并核对hash的环境依赖，保留所审hash作结果元数据；所有literal输入、成本评价、归约及断言不变。规范运行`python3 tests/audits/weighted_congestion/template_certificates/independent_antichain_core.py`，新路径运行结果及源码hash保存在`evidence/runs/weighted_congestion/template_certificates/independent_antichain_core.json`；本报告前述旧hash明确标识审查原freeze，不要求下一位研究者具备会话暂存路径。作者代码及结果为`tests/audits/weighted_congestion/template_certificates/verify_antichain_core.py`与`evidence/runs/weighted_congestion/template_certificates/antichain_core.json`。

## Canonical integration read-only recheck

Compared the appended section 7 in canonical `research/current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md` against the reviewed freeze, with an exact normalization assertion: only the declared heading/numbering, status text, and section 7.5's explicit d>=2/C>=1 qualification differ. All theorem, construction, cost identities and inequalities are unchanged. Section 8 identifies the review and finite audits without elevating them to the general proof. Thus the preceding PASS applies to the canonical claim.

Compared canonical `tests/audits/weighted_congestion/template_certificates/independent_antichain_core.py` byte-for-byte to the scratch audit after deleting exactly the FROZEN scratch-path assignment and the startup assertion that reads that scratch file. No fixture, arithmetic or mathematical assertion changed. Canonical script SHA256 is `d8b4a06e75ac9d0b0360452a19d7d41473f4e59633b9704f588d9d6c863e3b44`. The canonical evidence wrapper records this exact source SHA and status passed; its nested result is JSON-equal to the original scratch audit output. This check did not modify the repository or rerun already-passing tests.

Minor navigation-only observation: the retained wording “第一节给” in canonical section 7.3 refers to local section 7.1, inherited from the freeze's local numbering; it does not change or obstruct the argument.
