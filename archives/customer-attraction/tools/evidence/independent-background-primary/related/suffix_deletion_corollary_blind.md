# Blind check of the averaged suffix-deletion regret corollary

2026-10-24. Status: **the stated corollary is proved analytically** from the background-deletion lemma. I checked the formula before reading the older virtual-replay note, then compared the scopes. No scans were run. This is an auxiliary stability budget, not a half-coverage induction.

## 1. Exact setup

Fix any empty-root m-provider complete ordered-history pure SPE sigma in CAG-MODEL, with actual path (S_1,...,S_m). Write c_x for final actual load, W for actual coverage, and

    b_j(x)=sum_(k<j) 1_(x in S_k).

For each i<m, freeze the actual prefix before i, regard actual S_i as one fixed additional background provider, and retain sigma's genuine suffix after the original history through i. Delete that single background provider, keeping the same complete suffix strategy.

For j>i, let R_ij be the positive one-deviation regret at original actual suffix node j in this deleted child. Its deviation is evaluated with the original prefix before i fixed, actual S_i absent, actual suffix actions before j fixed, current topic changed, and all later actions responding through the original suffix sigma. The deleted plan is not asserted to be SPE.

Let D=|{x:c_x>=2}|.

## 2. The pair envelope is an equality

In the background lemma for this child,

    b=load before i,
    d_x=1_(x in S_i),
    p_j=load of S_(i+1),...,S_(j-1).

Thus on x in S_i, b_x+p_j(x)+1=b_j(x), which is positive. Consequently

    K_ij=max_T sum_(x in T intersect S_i)
                      1/[b_j(x)(b_j(x)+1)]
         =sum_(x in S_i) 1/[b_j(x)(b_j(x)+1)].

The second equality follows because S_i itself is a legal common-catalog topic and covers every nonzero term. So no relaxation is needed at this step.

For each fixed j, summing over i<j counts b_j(x) copies of x and gives the exact identity

    sum_(i<j) K_ij
      =sum_(x:b_j(x)>0) 1/(b_j(x)+1).

No identification of ordered histories is used.

## 3. The total actual suffix refund is exactly D/2

Let A_ij be the removal gain on original actual provider j after deleting actual provider i. It is

    A_ij=sum_(x in S_i intersect S_j) 1/[c_x(c_x-1)].

This only involves c_x>=2, so its denominator is positive. For fixed deletion i, the background-deletion lemma subtracts

    E_i=sum_(j>i) A_ij.

For one customer x with c=c_x>=2 actual coverers, there are binom(c,2) ordered-position pairs i<j covering it, each contributing 1/[c(c-1)]. Therefore

    sum_(i<j) A_ij = D/2.

Equivalently, if i is the kth coverer, its suffix refund is (c-k)/[c(c-1)], and summing k=1,...,c-1 gives 1/2.

Summing the established nodewise bounds R_ij<=K_ij-A_ij proves

    sum_(i<j) R_ij
      <= sum_j sum_(x:b_j(x)>0) 1/(b_j(x)+1) - D/2.

For j>=2, every x with b_j(x)>0 is actually covered, and 1/(b_j(x)+1)<=1/2. The j=1 sum is zero. Hence

    sum_(i<j) R_ij <= [(m-1)W-D]/2.

The conclusions include m=1, empty topics, repeated actions, and zero-customer instances. In particular the right side is nonnegative, since D<=W and m>=2 in the only nontrivial case.

## 4. Comparison with the older virtual-replay budget

Only after this proof, I read:

    R-4ffa.../deletion/virtual_replay_regret.md

The old note already contains the exact deletion-gain-minus-original-IC identity, the common-leaf refund conservation, and the broad pointwise bound

    regret <= u_j(original) - A_ij

for a single removed provider. It also has a global-size envelope K_global/2 for the deviating removal gain. Those are not being rediscovered as new facts here.

The new suffix specialization retains an actual-prefix envelope K_ij. It is not identical to the displayed old u_j or global-size bounds. Since both proofs are valid, one may combine them pointwise as

    R_ij <= min{u_j(original),K_ij} - A_ij.

The exact prefix-dependent sum of K_ij and its D/2 rebate are the additional structure being used in the corollary. There is no claim of global novelty beyond the compared note.

For example, on the all-big actual path with m clients all covered by every provider, K_ij=m/[(j-1)j]. At late j this can be much smaller than the old u_j=1 bound. It can also be larger at early j, which is why neither unmixed pointwise envelope dominates in every position.

## 5. Why averaging these suffix errors does not yet supply a half induction

There are two distinct missing requirements.

**Earlier-provider recourse.** For i>1, the proved object is a suffix game with every provider before i frozen. A proposed (m-1)-provider root game would need the earlier providers j<i to remain strategic. If such a provider deviates, the deleted virtual provider at position i may choose a different topic under the original complete sigma. The deleted load is then branch-dependent rather than the fixed d=1_(S_i(actual)) used above. Their regrets are absent from the triangular sum sum_(i<j) R_ij.

The old causal virtual-replay construction does define a complete (m-1)-provider strategy for deleting i. Along its actual path, its regrets for j>i coincide with R_ij. For j<i it needs the other, branch-dependent refund comparisons from the old note. Averaging the triangular bound does not make those omitted terms disappear. Selecting i=1 avoids earlier-provider recourse, but then the averaging choice over i is lost.

**Off-path credibility.** Even for i=1, the displayed bound controls actual suffix-node regrets only. The background-deletion lemma applies separately at every history, but each history has its own prescribed continuation leaf and its own refund budget. A root count D and actual q do not automatically control those reset budgets. A smaller-player half theorem for exact SPE therefore cannot be invoked on the deleted prescribed strategy simply from this actual-path estimate.

In particular, zero actual-node regrets after deletion do not imply that the deleted strategy is SPE. Here is a direct analytical illustration for the more general background-deletion lemma: take disjoint topics A with two unit clients and B with three, b=0, and background d=1 on all five customers (realized by one old A provider and one old B provider). There are two tail providers. Prescribe first A and second B after either first action. With d retained, root A and B each give the root one; after A, B is the last best reply, and after B both A and B give the last provider one. Thus the original tail strategy is a complete SPE. After deleting d, its actual path remains (A,B), all actual-node regrets are zero, but after the off-path first choice B the last prescribed B gives 3/2 while A gives two. The deleted strategy is not SPE. This illustrates the logical credibility issue; it is not asserted to be a counterexample to the more specialized empty-root single-deletion corollary.

## 6. Optional whole-replay bookkeeping, still no closure

If tau_i denotes the older full virtual replay deleting i, let r_ij be the actual-node regret of surviving role j. Then r_ij=R_ij for j>i. For j<i, the old one-deletion bound gives

    r_ij <= u_j-A_ij.

Combining this with the new suffix envelope yields the valid general total estimate

    sum_i sum_(j!=i) r_ij
      <= sum_(i<j) min{u_j,K_ij}
          + sum_j (m-j)u_j - D.

The total actual refund over all directed distinct coverer pairs is D. This estimate is no worse than summing only the old pointwise bound, which gives (m-1)W-D, but it still carries all earlier-provider errors and only pays the original actual paths. It is not a robust full-tree induction theorem.

## Conclusion and exact status

The corollary and its D/2 coefficient are correct. The analytic prefix envelope is stronger information than the old coarse deletion bound in relevant positions. It does not yet produce a smaller exact SPE, a robust full-history welfare theorem, or a half-coverage induction. A further argument must pay earlier-player recourse and control the refund balance after genuine changes of branch.
