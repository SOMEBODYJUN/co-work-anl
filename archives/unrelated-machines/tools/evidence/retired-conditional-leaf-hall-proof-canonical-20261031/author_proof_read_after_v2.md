# Conditional leaf Hall: author-proof read-after review

Reviewer: /root/sol_literal_budget_attack, 2026-10-18.

Verdict: PASS for the mathematics stated in Exact v2. I found no fatal step in the complete author proof. This is a post-disclosure review; my earlier Exact-first reconstruction remains unchanged and retains its earlier independent identity.

## Actual identity and reading scope

Before this read, my independent Exact-first record was frozen as
/workspace/scratch/038d9dcc4cac/sol_conditional_leaf_hall_exact_first_review.md,
SHA-256 f5e2bbfc15066eff1969a8a91106d92c22103c1c245b80f65eda365e85518812.
Root reported actually reading that complete record before releasing the author proof.

I then checked the whole-file hash and actually read the complete header and §§A–F of
/workspace/scratch/038d9dcc4cac/sol_general_repair_conditional_hall_proof.md,
SHA-256 357c762c9481183dd3f0f5fdf9631beddad931bb80977e753287d6bf662d73e6,
in one untruncated 3252-token tool result.

I did not open the author checker named in §F, any sol_nsw draft, or another candidate author record. The author checker's reported executions and counts are therefore read assertions of the author, not executions independently certified by this review. My own previously reported finite audit was actually run independently.

## 1. The global-flow constructions differ only in slack placement

Write beta_i=sum_s z_(c_i,s,u), B_i=sum_(j<=i) beta_j, and delta=1-sum beta. My independent construction puts all unused hole probability on the last port, giving leaf i flows

\[
 (y_{i,u_i},y_{i,u_{i+1}})=(1-B_i,B_i).
\]

The author puts the slack on the first hole, giving

\[
 (y_{i,u_i},y_{i,u_{i+1}})
 =\left(\sum_{j>i}\beta_j,\ \delta+B_i\right).
\]

Both are nonnegative row-one flows. The first leaves global resource slack delta at the last port; the second leaves it at the first port. All other port columns are tight. On the specific family every old resource column is tight, so delta=0 and the constructions coincide exactly. This is an equivalent valid choice, not a discrepancy or a hidden restriction to z=lambda.

The conditional construction in §C agrees with my independent one: leave the original group's own port free on each path, even when only another indexed state of that group is positive on the old resource, and concatenate these per-resource matchings. Scale by the supplied lambda. It covers every added leaf and leaves the conditioned state's only possible positive z on the hole. This handles arbitrary fractional z, zero lambda, d=1, d=0, unused data, and explicit zero incidences without division by lambda. Summing all global path columns gives the reverse projection for the same original point.

## 2. The family value bounds are different and both valid

My Exact-first proof used the number of parking items: if M owns r positive home items in a row, all r displaced helpers need a distinct positive parking item, so r<=t whenever the minimum is positive. Therefore M's value is at most t/D=1/t.

The author instead uses the total normalized parking value. At common minimum v, M gives v<=r/D, while r displaced helpers together have parking value at most one, giving rv<=1. Hence v^2<=(r/D)v<=1/D. The r=0 case yields v=0 directly. This reasoning is valid for all allocations and does not presume an actual state distribution. The common attaining allocation with r=t proves equality. The path-value preservation then transfers the bound, and OPT=2-V transfers it to the full ordinary matrix.

## 3. Complete matrix, classification, and partition checks

Section A correctly retains every unselected indexed state's payload at its private root, with load one. The root carrying the original unit selector has load two minus its exported coefficient mass, while every incidence costs one at its resource endpoint. Thus T<2 implies disjoint decoded bundles. The trivial complete all-tail schedule gives OPT<=2 and covers the endpoint case. Zero jobs consume no private load and may simply stay private; deleting them is unnecessary.

The strict b<epsilon threshold characterization is exact. For the family, the full parking state leaves tail one even though a unit home coefficient is present, so helpers are correctly retained in C. The same holds at fixed epsilon when t>1/epsilon. New adjacent singleton leaves are in L for every positive epsilon.

Section C explicitly retains the designated partition precondition for the general theorem. Its example showing why automatic repartition can fail is correct: two old singleton groups on one resource have a basic epsilon=1/2 point lambda=1,z=1/2 each, but their path lift has the two original singleton groups and the new adjacent leaf as three unit-demand groups on two ports. Automatic all-leaf matching is infeasible. This example is outside the stated non-threshold-original-group precondition and therefore does not contradict the theorem.

The two directions in §D preserve actual menu value because all added leaves require one positive endpoint whenever the minimum is positive. They occupy d-1 distinct ports, leaving at most one positively valued old-core port per old resource. The proof does not identify old and new physical machines. The positive-support FSLP statement uses full support z=lambda and the same hole flow; it agrees with the explicit interpretation and proof in my independent record.

## 4. Size, bit length, and checker boundary

The counts in §F agree with my independent derivation: P_0=D^2(t+2), L_0=D^2+Dt(D-1), S_C=D+2D^2, I=P_0+2L_0. Each family port belongs positively to one core indexed state and at most two adjacent leaf states. The ordinary matrix counts include all selectors, all incidence jobs, and all private state roots. The rational extension uses sums of original point coordinates and multiplication by lambda, with no reciprocal-weight expansion, so the claimed explicit polynomial bit cost is sound.

The proof states that its checker checked t=2,3,4 and reduced parking allocations; I did not validate that code or those execution counts. My independent audit actually checked t=2's full 180-machine, 201-job matrix and all flow constraints, plus a separate partial-z/zero-lambda/d0/d1/d2/zero-incidence example. Neither finite checker is needed for the general proof.

My independently frozen script has no dependency on a scratch input path or author module. It uses only Python's standard library. Its main output is the relative path sol_conditional_leaf_hall_independent_audit.json in the current working directory. Thus running it from a repository working directory would create that result there. The current JSON key order can depend on set iteration, so the frozen output hash identifies the actual saved run rather than promising byte-identical reruns. A separately adapted persistent copy may sort keys or accept an output argument; the frozen independent record and its code/output hashes should not be rewritten.

The resulting claim remains an unconditional gap for this particular conditional-leaf relaxation and an exact preservation theorem under its stated partition. No hardness, stronger joint-core barrier, CONFIG/PSD hierarchy result, or main unrelated-machines theorem follows. No repository file was edited in this review.
