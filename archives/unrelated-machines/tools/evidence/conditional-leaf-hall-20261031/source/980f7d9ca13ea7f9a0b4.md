# Conditional leaf Hall v3: author-proof read-after

Reviewer: /root/sol_literal_budget_attack, 2026-10-18.

Verdict: PASS for the new §9 projection and gap claims. I found no fatal error in the author's transport proof. This is post-disclosure review of the new clause, not a fresh blind reconstruction of v2 or v3.

## Actual reading and preserved chronology

My new-clause-first record was frozen as
/workspace/scratch/038d9dcc4cac/sol_conditional_leaf_hall_consistent_marginals_exact_first_review.md,
SHA-256 783e27cbc45db0421164d2953d48c47ee66a8c0969210e399a9adb91fbf7e0cf.
Root reported actually reading that complete record before releasing the new author proof. The earlier v2 Exact-first and read-after records remain unchanged.

I then checked the whole-file hash and actually read the complete header and §§1–5 of
/workspace/scratch/038d9dcc4cac/conditional_leaf_hall_consistent_marginals_author_proof_v3.md,
SHA-256 730c5ef3af3861f123466d7e561111b363f5effb51c839efc0d6d284591d14c9,
in one untruncated 1472-token tool result. I did not open an author checker or another v3 author derivation.

## Transport construction: different valid completion

The author uses the same lower-bound transportation formulation as my independent reconstruction: table rows are the supplied state lambdas, columns are the single global hole law pi, and own-column entries must dominate that state's z. The lower fill z leaves nonnegative row residuals lambda_s-z_s, own-column residual pi_i-b_i, and other-column residuals pi_h. Both residual totals equal 1-b_i.

My independent formula filled those residuals proportionally, dividing by 1-b_i and branching when b_i=1. The author fills them by ordered greedy transport. Each nonzero fill empties a row or column, so O(number of states+d) fills suffice. This yields the same required row/column margins and own-port lower bounds, although generally a different valid table.

When b_i=1, all residual rows and columns are zero because z_s<=lambda_s and their totals are both one. Greedy transport therefore has nothing left to do. A lambda-zero state has z=0 and a zero residual row. Thus the author correctly avoids a reciprocal and needs no separate numerical limiting convention. States with coefficient zero on this resource but positive lambda retain their residual rows and are not omitted. If the core has no positive group port, the explicit product lambda_s*pi_h has the required margins.

The author's global slack is placed on the first hole, while my independent audit used the last hole. Both choices satisfy pi>=b; the family has zero slack, so they coincide there.

## Complete conditional matchings and the object shared by MC

For a fixed path, the author's conditional flow is the nonnegative sum of its full one-hole matchings with the transport row as weights. Its total mass is lambda_s, and the own-port hole mass dominates z_s. Consequently each conditional leaf row and every perspective column is correct.

Concatenating the disjoint path flows covers all leaves. If an explicit distribution over full matchings of all paths is desired, couple the path hole distributions by the common interval construction already proved in my new-clause-first record: union their cumulative rational endpoints in [0,lambda_s], and use each interval's fixed holes to form one full matching. This has polynomially many pieces and reproduces the concatenated flow. No exponential product list or division by lambda is needed.

Summing the author's conditional flows over the states of any one core gives the same global leaf-edge y^0, because each transport table has column marginal pi. The transports for distinct cores need not have the same joint correlations over paths or states. The proof correctly shares edge marginals and does not claim a common law of complete leaf matchings, a common state assignment, or simultaneous other-core usage in a conditional capacity.

The new proof does not upgrade v2's single-integral-matching witness. On a family parking path the helper home state necessarily mixes the other D-1 holes, as my independent record explicitly demonstrated. The author's weighted-mixture statement is consistent with that necessity.

## Projection, partition, and complexity

The reverse projection uses only the old global columns and complete leaf rows, so adding MC does not alter it. The deterministic actual-allocation witness has one positive-lambda state per core and automatically satisfies MC, proving necessity.

The designated partition remains all original groups as cores and exactly the new path groups as leaves. Automatic threshold elimination requires the same non-threshold-original-group precondition as v2; the author states it and does not silently change the partition. The d=1 empty-matching and d=0 retained-unused-resource cases are correct. Positive-neighbor D_+ does not add zero-only neighboring groups; retained zero jobs do not affect z, utility, or this argument.

All transportation residuals are rational sums/differences of supplied coordinates, and each greedy fill takes one rational minimum. Their encoding lengths and the complete explicit flow output are polynomial. The extra MC rows have coefficients 0/±1 and count at most |C|E_L. The claimed exact rational LP conclusion does not assume exact SDP feasibility.

The same old family point therefore extends while the original full ordinary matrix and its actual value remain unchanged. The fixed-epsilon classification and near-two unit-threshold gap follow from the already reviewed v2 proof. This remains a gap for R_cons, not a claim about actual-OPT approximation, joint-core constraints, full CONFIG/PSD liftings, or main unrelated-machines hardness.

No old record, author file, or repository file was modified during this read-after review. My independent v3 code and exact finite audit remain those already identified in the frozen new-clause-first record.
