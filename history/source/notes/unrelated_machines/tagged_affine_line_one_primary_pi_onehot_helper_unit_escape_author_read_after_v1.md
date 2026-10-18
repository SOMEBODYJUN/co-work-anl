# Tagged affine LINE one-primary PI onehot escape — author-Proof read-after v1

Reviewer: general_query_response_review. Date: 2026-10-18.
Verdict: VALID. No fatal issue, standing objection, or requested correction.

## 1. Actual reading order and immutable hashes

This record was made only after the independent Exact-first proof had been frozen and actually read by root. I then received explicit release of and actually read the entire author Proof, Sections 1-7:

/workspace/scratch/038d9dcc4cac/tagged_affine_line_one_primary_pi_onehot_helper_unit_escape_proof_v1.md

SHA256: 2b4d738099afcc78a4d14c42a7142a08a6224f5b9e8fc6ae3a6f463c9e837c6b.

The proof corresponds to the frozen statement-only Exact:
- tagged_affine_line_one_primary_pi_onehot_helper_unit_escape_exact_v1.md;
- SHA256 59e71e7d7c496b9dda2a993af5d0253072601190b5e78a8599dd06093fb47bbd;
- source ID UM-TAGGED-AFFINE-LINE-ONE-PRIMARY-PI-ONEHOT-HELPER-UNIT-ESCAPE-v1.

My earlier independent reconstruction remains unchanged:
- tagged_affine_line_one_primary_pi_onehot_helper_unit_escape_exact_first_review_v1.md;
- SHA256 f535ef37960e5a8b30127127514db9035b69482c66c47f157eb26163c539a3a0.

No other new rainbow strategy, full-PI simplex candidate, or unrelated author's derivation was read. This is a new post-Proof record, not a retroactive claim that author content was available before the independent freeze. No old raw, Proof, Exact, repository, Work, or Git file was edited.

## 2. Comparison with the independent proof

The mathematical core is the same as my independent reconstruction:

1. Fix the arbitrary requested original main state and its primary labels t_u.
2. Condition each helper's original state distribution on its unique primary label being t_u, obtaining mu=R lambda on that event.
3. Primary-auxiliary pairwise marginals imply uniform conditional slope 1/R on each auxiliary separately.
4. Primary parallel-line separation and auxiliary pointwise capacity bounds give a fractional unit matching on the onehot positive cells.
5. Integral matching recovers actual whole original indexed states and distinct positive resource cells.
6. Directly schedule every original selector and every state-resource job, including unselected states and zero-time jobs, at makespan one.

No additional global source assignment, independently assembled label tuple, joint auxiliary independence, or disjointness of the full selected zero-weight supports is used.

One harmless implementation difference is that the author builds the helper-resource graph from edges of strictly positive conditional flow f. With explicit rational lambda, exact summation and positivity testing construct that graph in polynomial bit time. Every matched edge then has a positive-mu original state witness.

My independent construction may instead include every original state with the conditioned primary label, including lambda-zero states, storing a whole state witness per cell edge. The same fractional flow is supported in that larger graph, so its Hall condition also holds. This larger graph can be constructed without numerically computing lambda under a real-feasibility promise. The author uses the valid LP-first route supplied by the Exact for that case. These differences neither change the theorem nor require changing the earlier independent record.

## 3. Conditioning and primary-plane correctness

The primary marginal is exactly 1/R, so the conditioning event is nonempty and mu sums to one. For any auxiliary label a, multiplying the primary-auxiliary pair mass 1/R^2 by R gives conditional auxiliary mass 1/R. Auxiliary-auxiliary dependence is left unrestricted.

Each helper has exactly one primary, so there is only one such conditioning event per helper. This avoids any unsupported claim that several conditioned labels retain auxiliary uniformity.

On a primary plane, all relevant helpers and the requested main state now use the same slope t_u but their actual fixed intercepts remain pairwise distinct. Their complete primary lines are disjoint for every abscissa, even if the main intercept is nonzero. Thus helper primary positive cells avoid the entire main line and one another. Other primary planes have different tags, and main participates in no auxiliary plane. The proof does not change intercept numbering.

## 4. Auxiliary-plane capacity, arbitrary onehot choice, and Hall

For a fixed auxiliary cell (x,z,y) with z nonzero, a helper can select this positive cell only if its x label is the unique field slope (y-j_x(h))/z. Conditional slope uniformity makes the helper's flow to this cell at most 1/R. At most R helpers participate in x, so total incoming flow is at most one.

This is an upper bound by the line-membership event, so it remains valid when the onehot cell depends arbitrarily on the complete state and all other input data. The onehot cell need not have a fixed parking location or depend only on the x label.

At z=0, slope uniformity alone would not give that bound. The author correctly uses injective intercepts: at most one helper's line ever contains (x,0,y), and its total flow is at most one. This handles all cells, including the zero abscissa, and arbitrary auxiliary sharing between different primary blocks.

Every helper's outgoing onehot mass is one. The author explicitly proves Hall's inequality by summing the fractional unit rows over a helper subset and the unit column capacities over its neighborhood. Thus an integral matching covers all helpers. Every graph edge comes from an actual indexed state with the desired primary label and its own actual positive cell. Edge-state lookup therefore returns that entire input state, including its correlated auxiliary labels. No independent-coordinate state fabrication occurs.

The matched helper positive cells are distinct and avoid main positive cells. Main receives all its original positive cells, whose weights sum to one; each helper receives its single unit cell. This proves V=1 for every prescribed main state, with no restriction on the main's nonnegative norm-one weight pattern.

## 5. Full actual ordinary UM job audit

The author Proof supplies a direct original-job schedule, not only a partial-allocation assertion:

- each group selector goes to the private root of the selected original state;
- every selected state's positive incidence job goes to its own original resource machine;
- every selected state's zero-private-time incidence job remains on its own selected root;
- every incidence job of every unselected indexed state remains on that state's own root.

A selected root therefore has unit selector load plus zero job load; an unselected root has total private load exactly its original normalization sum one. Distinct selected positive cells ensure resource machines receive at most one actual unit job. Unused machines remain empty.

This covers all original selectors and every incidence identity exactly once, including states of zero lambda mass and all zero incidences. The complete original matrix is unchanged; there is no deleted baseline task, free export, virtual machine, or omitted unselected state.

At least the main selector exists, and all selector finite times are one, so any complete actual schedule has makespan at least one. The constructed complete schedule has makespan one. Hence OPT(P)=1 exactly.

Overlapping zero portions of selected full supports are permitted because those original jobs run privately, while the matching controls precisely the exported positive incidence jobs.

## 6. Rational certificates, bit complexity, and boundaries

With supplied rational lambda, mu only multiplies by integer R and f only aggregates explicit state masses. Rational numerator/denominator lengths remain polynomial in the total encoding length; probabilities are not unfolded into copies. The number of helper-resource edges is bounded by explicit onehot state occurrences, and deterministic bipartite matching plus a state-table scan is polynomial.

For the real-feasibility version, the author's explicit finite LP has one variable per original state, R primary marginal equations, R^2 pair equations per auxiliary incidence, normalization, and nonnegativity. Coefficients are zero/one with rational right sides of polynomial encoding length. Its variable and constraint counts are polynomial in the expanded state/plane input. Standard deterministic rational-LP feasibility can obtain a polynomial-bit rational certificate when real feasible; infeasibility is only failure of this additional distribution interface, not an ordinary UM infeasibility conclusion.

The schedule output scans all original incidences. The Exact's machine count S+(|P|+|A|)R^2 and job count n+I are correct; unused auxiliary planes remain present. No poly(log R)-only output bound is asserted for compact or oracle input. There is no 1/lambda, denominator-value, permutation, or hidden-configuration expansion.

The proof correctly covers H empty, A empty, unused auxiliary variables, R=2, arbitrary nonzero main intercept, zero state masses, and all zero private cells. Each helper state, including zero-probability indexed states, remains onehot and retains its full original identity.

## 7. Scope and final verdict

The author Proof uses exactly the structural restrictions in the frozen Exact: one primary per helper, no main auxiliary incidence, all-state onehot helper weights, injective fixed incidence intercepts, explicit state tables, and primary-auxiliary pairwise marginals. It does not assert that conditioning multiple primary labels preserves auxiliary uniformity, that diffuse helpers reduce to the same matching, or that all pairwise-independent tagged-line menus admit this escape.

No source-CSP solution, general identity-copying obstruction, Chan/LST hard-image identification, hardness, new matching backend, external review, software execution, or global originality is certified by this record.

The full author Proof agrees with the independently reconstructed theorem. No correction is requested and no standing objection remains. A future canonical text requires a separate actual reading and scope record. The different full-PI simplex candidate remains outside this review.
