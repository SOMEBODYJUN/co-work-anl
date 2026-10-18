# Normalized-menu full-support LP preservation: actual author read-after (v1 and v3)

Reviewer: general_query_response_review. Date: 2026-10-18.
Status: VALID within the final v3 Exact contract. No fatal issue or standing mathematical objection found.

## Reading sequence and immutable provenance

This is a new author-Proof read-after record, not a replacement of a statement-first review. Before the author Proof was released, I froze:

- pre-Exact bounded-row SC research checkpoint, SHA256 b33a165fd22dd77b3ce8c93317a9754c52a60675a2d6366edbd9e99f0668d0f6;
- v1 Exact-only independent proof, SHA256 dff69ad05b38d92604c8aa7227009cd2a61bdbeeb60b5409471a39fca66f8c92;
- v3 Exact-only independent proof, SHA256 22acf36bac189365e4c4d5d85da30938f8623f8d383ca033d5e2fbf8e53950b7.

Only after the parent explicitly released them, I actually read the complete author Proof v3 (120 lines) and author Proof v1 (125 lines). I re-read both full texts before freezing this record and independently checked their byte hashes:

- normalized_menu_full_support_lp_preservation_proof_v3.md: fb652fd0a1fd71d01ec6297fd86dfb56bbaf06fa55b1acbb8440ca06e103c930;
- normalized_menu_full_support_lp_preservation_proof_v1.md: 7f8bd074a0f137dd4c75260fd7c8bd4023bcd24d5bd96042b56b46c552e47740.

I did not read the v2 Exact or an intermediate v2 Proof. The v3 Proof states that no separate v2 Proof was made. I certify the supplied mathematics rather than that historical assertion. All prior raw, checkpoint, independent-review, and manifest bytes remain unchanged.

The reviewed mature contract is v3 Exact SHA256 6a31b2699304f18847d1226305fa72c8f56998a2930f846a3467ca45309194bf. The v1 Exact SHA256 is 9fd644392d624431050d0d1489bea4464284a1594f7868bf4a3667641233a763. v1/v2 are process history, not separate mature claims being multiplied by this review.

## Comparison with the independent reconstructions

The author and I prove the same positive-support FSLP contract. Its resource coefficient is membership in P_gs={u:p_gsu>0}, not p_gsu and not all syntactic incidences. Zero private processing times remain actual UM jobs; omitting them from FSLP or from SC positive support does not delete them from the actual matrix.

There are two harmless proof-route differences:

1. For the tree reverse direction, the author sends one unit of flow from the root, with each child edge capped by the corresponding state probability. At a nonroot vertex, the own-resource capacity implies that total nonown probability is at least the incoming flow, so greedy splitting is legal. At a leaf, its original-state mass dominates the leaf flow. My independent reconstruction instead showed total original-leaf mass at least one and normalized those leaf masses downward. Both produce group mass one and componentwise no larger original-state weights, hence preserve every original resource inequality. Neither incorrectly asserts that all off-path activation has mass exactly one.
2. For several reverse LP bridges, the author greedily caps each group's nonnegative weights to total one; my reconstruction can divide by the group's total, which is at least one. Both only decrease weights and have rational bit-polynomial implementations.

No difference changes the object, quantifiers, or conclusion.

## Restricted flat machine CONFIG(1) bridge

The author's v3 Sections 1-2 are correct for the full original flat UM matrix.

Forward, on each private machine, the selector-plus-all-zero-incidences configuration has load one and weight lambda; the all-incidences configuration has load exactly one and weight one-minus-lambda. Thus every zero job has private coverage exactly one, every positive job has private coverage one-minus-lambda, and every original selector has total coverage one. Each positive incidence receives its remaining lambda coverage as a unit singleton on its own resource machine. The positive-support FSLP inequality is exactly the resource singleton probability bound. Empty configurations fill unused probability. This includes all original unselected-state jobs, unused resource machines, and indexed duplicate states.

Reverse, write alpha_gs for the private marginal of the actual selector. Each group has selector coverage sum_s alpha_gs at least one. A positive private incidence cannot coexist with that unit selector in any load-at-most-one private configuration, even if its time is arbitrarily small. Its private marginal is at most one-minus-alpha_gs, so its unique resource marginal is at least alpha_gs. Resource configurations contain at most one actual incidence because all resource endpoint times are one. Summing and then decreasing group weights to sum one proves FSLP. A zero private incidence supplies no such exclusion, exactly as required.

The optional finite certificate conversion from coverage-at-least-one to exact-one is also valid: deleting a single job from a configuration preserves machine feasibility and does not alter any other job's coverage. At most one split per processed job suffices; support increases by at most the number of jobs. This preserves machine probability totals. There is no denominator expansion.

This argument uses the restricted full flat structure and threshold one. It supplies no machine-CONFIG preservation theorem for arbitrary UM matrices or arbitrary thresholds.

## Tree, menu path, and state-dummy checks

The tree forward formulas normalize each new group and saturate fresh own-resource pairs. The reverse flow route above handles K=1 separately and permits arbitrary extra activation. The original positive-resource inequalities follow from leaf domination.

The menu-level path uses all syntactic group memberships, including zero entries, to form its port list. Its actual capacity accounting uses only positive-support state mass x_i. A hole distribution pi_i at least x_i with total one exists exactly when sum x_i at most one. The helper left-tail/right-prefix probabilities give helper use one-minus-pi_i at each port. Reverse summation subtracts exactly d-minus-one helper occupancy from d unit port capacities. This remains correct for zero-only memberships, d=0, d=1, unused resources, and indexed duplicate states.

For state-dummy SC, real row value is exactly one. Forward real-support probability lambda and singleton dummy probabilities (1-lambda)/(K-1) give every agent probability one, each group dummy occupancy one, and real occupancy equal to FSLP. K=1 is separate and needs no division by zero. Reverse configuration trimming is valid: a configuration without a positive own dummy and of value at least one must contain the entire positive real support. The K agents versus K-minus-one unit dummy capacities imply at least one total unit of real-support probability, which can be capped to FSLP. Foreign dummy and zero-value items can be deleted.

Any target strictly above one forces every agent configuration to contain an own dummy, contradicting that same group capacity count. Thus SC CONFIG's highest threshold is at most one. The independently established actual state-dummy value identity remains an actual-allocation argument; it is not inferred from LP feasibility.

## SC-layer path: actual and CONFIG domains

The v3 Sections 6-8 correctly distinguish their threshold domains.

Actual forward is valid for 0<v<=1: reserve an old-assignment hole per original item, give each old agent its own positive copy, and match all adjacent helper agents to the other copies. Their value is one, at least v. Actual reverse is valid for every v>0: each helper must hold at least one of its two positive copies. The d-minus-one helpers consume at least d-minus-one distinct copies, leaving at most one positive copy of the original item for old agents. A helper may hold both copies; this only strengthens the counting bound. After deleting zero-value items, each old agent has only its own positive copy, so merging cannot duplicate an old item. All old utilities are preserved. Therefore exact actual optimum preservation requires the stated old-OPT-at-most-one promise, and includes old OPT=0 by the positive-threshold reverse contradiction.

CONFIG forward is valid for 0<t<=1. Old-agent configurations retain weights and values after relabeling their positive items to their own copies. Per-item marginals x determine a dominating hole distribution; two singleton configurations per helper implement its prefix/tail probabilities without denominator expansion.

CONFIG reverse is valid for every t>0. After deleting zero-value entries, each helper configuration is nonempty, so its expected positive-copy count is at least one. It may be two, including when t>1. Summing copy capacities bounds old-agent total marginal by one. Since each old agent has at most one positive copy of each original item, relabeling back preserves each configuration's exact value without duplicating that item. This yields a finite old CONFIG(t) certificate.

Threshold zero is not justified by helper nonemptiness. The proof correctly supplies empty CONFIG(0) certificates independently and uses positive-threshold reverse implications for a zero optimum. Finite instances have finitely many configuration values, so the stated highest-threshold preservation under old-highest-at-most-one is sound, including attainment and the endpoints zero and one.

The construction does not inspect an optimal allocation, any unknown positive threshold, or an exponential configuration table. It applies to the finite certificate actually provided. Empty original item sets, zero rows, all-zero unused items, d=0, and d=1 do not create exceptions. Old-agent row totals are unchanged, new helper row totals are two, and each new positive copy is valued by one old agent and at most two helpers.

## Composition and Q_D

For J(Q)=P_SC(SC(N(Q))), normalization and K<=3 imply old SC row total at most three and both actual and CONFIG values at most one. The SC-path promise is therefore met. The final item positive degree is at most three, which is stronger than the intermediate degree-nine estimate. This correctly respects the order: normalized menu normal form first, state-dummy next, SC item path last. It does not assert that degree reduction normalizes arbitrary SC row totals.

The Q_D family gives a self-contained obstruction. Its displayed FSLP assigns main-state probabilities 1/D and each helper its g choice with probability 1-1/D, A choice with probability 1/D; every g and every A has occupancy one. In an actual positive allocation, if the main group takes r resources from row a, their r distinct helpers must all use the same A_a, so r<=1. The main value is at most 1/D. The displayed assignment attains it and satisfies all helper groups. This lower bound uses all helper groups and arbitrary partial bundles; it is not an enumeration result.

Accordingly the final SC image has CONFIG highest threshold one and actual optimum 1/D, with positive values only one and 1/D, row total at most three, and item degree at most three. The flat normalized machine image has machine CONFIG(1) feasible and actual UM optimum 2-1/D via the already established actual value bridge. The parameter D is measured by the explicit O(D^2)-size source family, not by log D.

This family refutes obtaining a constant actual guarantee from CONFIG(1) feasibility alone on the stated bounded-row class. Its actual values are below one, so it does not refute a constant finder under the different actual-OPT-at-least-one promise. No such promise algorithm is supplied or ruled out here.

## Bit complexity, dependencies, and review limits

Every displayed transformation uses finite rational sums, comparisons, downward capping or greedy flow, trimming, and relabeling. Output counts are polynomial in the explicit instance and the supplied finite certificate support. Rational numerator/denominator lengths grow at most polynomially under these operations; there is no expansion by a denominator, 1/p, or an implicit numerical D. The flat forward certificate has O(S+I+|U|) support; the SC path adds at most two singleton configurations per helper; exact-coverage pruning adds at most one split per original job.

The old actual normal-form and state-dummy contracts are prior checked mathematical dependencies. Their actual preservation is not inferred from the new FSLP equivalence. Q_D removes any dependence of the gap argument on an unread general Santa Claus CONFIG-gap proof. My pre-Exact research checkpoint accurately recorded the limit of its external-primary reading and remains unchanged.

BCG attribution and the authors' claimed personal reading are context, not new originality or external-review certifications from me. I previously read the indicated BCG primary section as recorded in the pre-Exact checkpoint, but that attribution is not needed to establish the self-contained SC path proofs just checked. No generic LP oracle implementation, new software, finite audit, NP-hardness, near-two source result, or actual-promise algorithm is certified by this read-after.

Conclusion: v1's mathematical core is valid and is correctly restated and extended in v3. The author's two newly added v3 branches agree with the independent v3 reconstruction. No correction is requested and no standing objection remains. A later canonical text requires its own actual reading and scope record.
