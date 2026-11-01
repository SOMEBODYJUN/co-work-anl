# Exact heterogeneous repair after genuine-child product transfer

2026-10-24. **Exploratory tool corollary, no target witness.** The input class throughout is the original CAG-MODEL: finite unit clients, m unit providers, one common finite catalogue, repeated topics allowed, and complete pure SPE on every ordered history. The argument is uniform in m and catalogue size. It does not establish general half or the reverse budget below.

## Sources and deduplication

The new repair theorem is `R-3bc48d936f044f12b0fa743482ff5eb0/credible/heterogeneous_prefix_repair.md`, independently reviewed at `../potential/heterogeneous_repair_independent_review.md`. For a target path with a genuine tail after position j<m, accurate credible deficits delta_i yield exact repaired half gap

    G_repaired = (OPT_m-2W) - [2 sum_(i<=j) delta_i + max_(i<=j) delta_i].

The genuine-child product transfer, signed per-position balances, arbitrary joint queries, and bounded grouping remainders already appear in `R-65d0f88edf3849b39ca5eb79760e970b/prefix_repair_next/product_threshold_prefix_attack.md`, which in turn attributes the transfer to `R-868a6ab8c81345f28335d75046b756b0/dynamic_matching/product_transfer_lemma.md`. They are not new discoveries here. This note changes only the final repair functional and keeps the existing true-child obligations intact.

## 1. Accurate floors; no arbitrary frozen continuations

Take finitely many components t with the same number m of providers and a common choice 1<=j<m. Component t has target ordered path z^t, a genuine complete SPE after its normal length-j prefix, actual target utility u_i^t, welfare W_t, and optimum O_t. All customer universes are disjoint in the product.

At its normal position i<=j and legal action A, let

    L_i^t(A) = min current utility among complete child SPEs after (h_i^t,A),
    M_i^t = max_A L_i^t(A).

These are genuine complete-history SPE minima, not minima over arbitrary suffix tuples. A product of independently attaining child SPEs is itself a complete child SPE, including every simultaneous coordinate deviation. Consequently the direct product P obeys

    L_i^P(B_1,...,B_K) <= sum_t L_i^t(B_t),
    M_i^P <= sum_t M_i^t.

No equality or converse is claimed: a general product SPE can correlate component continuation modes and need not decompose. In particular the signed balances M_i^t-u_i^t must be added before taking a positive part. Negative credible slack in one coordinate can help pay a different coordinate, because a deviation in that other coordinate may select a genuinely different low-payoff child SPE even while retaining this coordinate's current action.

For a usable sharper bound, the attributed product-transfer theorem defines a convexified genuine-child floor barL_i^t(A)<=L_i^t(A), with barM_i^t=max_A barL_i^t(A). More explicitly, let R_t(h_i^t,A,B) be the complete terminal set realizable by true remaining SPEs after the two forced actions. Put

    theta_i^t(A)=max_B min_(v in R_t(h_i^t,A,B)) u_(i+1)(v).

Over the finite menu of pairs (d_v,w_v)=(u_i(v),u_(i+1)(v)), for every legal B and v in that R set, minimize E[d_v] subject to E[w_v]>=theta_i^t(A). This rational LP defines barL. Its minimum is no larger than L because an L-attaining complete child SPE supplies a feasible menu leaf. If an optimal distribution has denominator D, put D replicas together and prescribe its menu leaves in their rational proportions. The next player obtains at least D theta; any other joint action can be continued through an independent product of true grandchild SPEs attaining each next-player minimum, whose total is at most D theta. Thus this block is a true complete child SPE and realizes total current payoff D barL. No mixed strategy is inserted into a single component.

Group all replicas by the current forced action A and use these denominator blocks; fewer than D replicas per action remain and use true L-attaining child SPEs. The total remainder loss at role i is bounded by

    C_i=sum_(t,A) (D_(t,i,A)-1)[L_i^t(A)-barL_i^t(A)].

This is independent of all replica numbers and every joint query. The block argument just reconstructed verifies the part of the attributed product transfer used here; the source's first author-only status is not silently changed for its other claims. Therefore finite products with n_t replicas have, uniformly over every joint query B,

    M_i^P <= sum_t n_t barM_i^t + C_i,

where C_i>=0 is a finite rational grouping-remainder constant independent of all n_t and of B. Each current-action group is partitioned into exact rational-denominator blocks and at most a fixed number of leftover replicas, which use attaining original L children. Every block and leftover has an actual complete child SPE. These are exactly the assumptions of the existing product theorem; this note does not derive a new barL or waive any grouping remainder.

Define signed balances and target gaps

    a_i^t = barM_i^t-u_i^t,
    G_t = O_t-2W_t.

## 2. The heterogeneous sufficient criterion

For a vector v in R^j write

    F(v) = 2 sum_i (v_i)_+ + max_i (v_i)_+.

It is positively homogeneous, monotone coordinatewise, and subadditive. For nonnegative credible deficits it is precisely the heterogeneous repair cost.

Suppose there are rational nonnegative component weights lambda_t, not all zero, for which

    sum_t lambda_t G_t > F((sum_t lambda_t a_i^t)_(i<=j)).       (ATTACK)

Then a finite original-model counterexample to Q-CAG-HALF follows. This is a sufficient criterion, not an assertion that such components or weights exist.

Clear the lambda denominators, writing k_t for the resulting nonnegative integers. Set

    g = sum_t k_t G_t,
    a_i = sum_t k_t a_i^t,
    epsilon = g-F(a) > 0.

Use n_t=q k_t replicas, with q a positive integer. Target welfare and optimum are exactly additive because the catalogue is the full Cartesian product on disjoint clients: every component's optimal m-tuple can be paired positionwise. Hence the old product gap is qg. Its true credible deficits satisfy

    delta_i^P = (M_i^P-u_i^P)_+ <= (q a_i+C_i)_+.

Monotonicity and subadditivity yield

    2 sum_i delta_i^P + max_i delta_i^P
        <= F(q a+C)
        <= qF(a)+F(C).

Choose an integer q>F(C)/epsilon. If the actual product deficits are positive, apply the independently verified heterogeneous compiler at their exact values. It yields a complete pure SPE with gap at least

    qg-qF(a)-F(C) = q epsilon-F(C) > 0.

If all actual deficits vanish, the product target itself can be completed backwards to a full SPE using its accurate child floors, and its gap qg is already positive. Every quantity is rational; one final common integer scaling of old and added clients makes each multiplicity an integer while preserving all utilities, IC, coverage, and the strict gap proportionally. There remain exactly m unit providers.

This finite implementation retains all ordered histories and all simultaneous action-coordinate changes through the cited product-child construction and the heterogeneous compiler's permanent first-exit modes. It does not assume coordinatewise optimality suffices when a first joint deviation changes modes.

## 3. What this improves, and what it does not supply

The old uniform final sufficient condition was g>(2j+1) max_i(a_i)_+. Since

    F(a) <= (2j+1) max_i(a_i)_+,

(ATTACK) can be strictly easier when the remaining positive role balances are unequal. It also retains negative balances until after component summation. This is an attributed composition of two known tools, not a new welfare bound.

For example, if hypothetical components have one isolated credible deficit delta each, at distinct roles, the repair's maximum overhead can be shared: their total repair cost is bounded by 2K delta+delta instead of 3K delta. Thus a legal component with a positive gap greater than 2delta could potentially be useful even if it fails the individual 3delta threshold. This numerical observation is not a component construction. Moving a defect from one role to another is not free: changing the ordered prefix changes its true child floors, and padding with arbitrary earlier actions creates additional deficits. No role-rotation lemma or positive-gap seed is asserted.

Nor does summing signed component balances prove their reverse budget. If general half is true, (ATTACK) cannot occur. Taking one actual full SPE with all positive balances zero shows that proving this universal reverse condition would itself include the missing original half assertion.

## 4. General mechanism's m=5 pressure test

Put m=5 and j=4 in this same deduction. Its repair functional is

    F(a)=2[(a_1)_++(a_2)_++(a_3)_++(a_4)_+]
           +max_i(a_i)_+.

Four equal positive role balances D cost 9D; one isolated positive role balance D costs 3D. This confirms a strict improvement over the uniform 9D estimate for nonuniform data. It does **not** give OPT_5<=2W for an arbitrary catalogue and an actual complete SPE: no positive-gap seed satisfying (ATTACK), and no independent universal reverse budget, was obtained. The general mechanism therefore has not crossed the requested unconditional factor-two pressure test.

## 5. Construction route at the stopping point

No legal root-only or multirole bad plan beating this exact cost was found. Root-only positive target gap with a genuine complete suffix is already the old stronger FREE-ROOT open question; assuming such a seed would not be progress. Directly lifting the high-background PB subgame is still invalid because those backgrounds already cover the relevant clients. Identifying insurer clients with old covered clients could reduce nominal coverage cost, but it destroys the disjoint additive utility proof and requires new joint-history IC. No such overlapping-support construction is claimed.

No finite cone scan or fixed-number/structure theorem project was run. Failure to find an input is not a prevention theorem or evidence that Q-CAG-HALF is true.
