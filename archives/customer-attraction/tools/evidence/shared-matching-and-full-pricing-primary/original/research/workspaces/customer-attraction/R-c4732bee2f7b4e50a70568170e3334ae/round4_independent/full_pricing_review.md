# Full 557-row pricing: independent mathematical and exact-computation review

2026-10-21. Reviewed the final 51-multiplier dual certificate in `round4_pricing/exact_dual_overlap1.json`, the factorization in `full_pricing.py`, and the definitions of the added terminal and retained-overlap pair rows. Independently reconstructed and priced every active dual row without importing the discovery `Universe`, `family_score`, `price`, any old-row evaluator, or the discovery optimizer.

## Result and precise scope

The independent exact full-universe dual check passes at

\[
\beta=\frac{178528430822287579296070598592537012737}
{87421565922360356032366460363114422206}
\approx2.042155490337931>2.
\]

The 51 rational multipliers are nonnegative. Their common denominator is `2010696016214288188744428588351631710738`; the scaled beta numerator is `4106153908912614323809623767628351292951`. This review validates an upper bound over the **entire stated 557-row histogram universe**, not just either old or newly generated support.

Since every genuine five-player full-history pure SPE supplies feasible client atoms and necessary aggregate rows, the dual gives the improved general-catalog five-player welfare bound `OPT_5<=beta W`, using the already established interpretation of the original 437 rows and the valid new comparisons. It remains above two. This does not prove arbitrary-player half coverage.

The matching 67-atom primal's full 557-row feasibility is not independently rechecked here. It is a separate contract needed to certify exact optimality of the relaxation. The discovery agent has recovered that point and the parent is separately reviewing its rows. A relaxation primal is not an SPE completion or an actual OPT certificate.

## Why conditional separation is complete

An atom has ten unrestricted fixed action-membership bits, three indexed branch histograms of total size five, and three reply-menu overlap pairs `(ell,h)`. The two third-position families have all compositions of five into eight binary cells, hence 792 histograms each; the second-position family has all compositions into 16 cells, hence 15,504 histograms. All 1,024 fixed masks are retained, including masks with zero actual coverage.

The first histogram coordinate is membership in the same five comparison topics. Its multiplicity d must agree across all three families. Conditional on the fixed mask and this common `d in {0,...,5}`, the stated relaxation imposes no further coupling between the three histograms. Retaining all histograms with that same d therefore includes every allowed column. Any extra global topic-incidence compatibility needed for an actual instance has been relaxed, which is safe for the upper bound.

Each new terminal offdiagonal row is computed from one family's history load and one of that family's indexed query lists. Each new two-query row likewise uses one family's background p_i and indexed membership pairs; it has no hidden term involving another family's histogram. The equality patterns of the branch and query indices only require that family's marginal binary-cell histogram, including its within-index query overlap. Thus the added rows preserve conditional separability. The active final dual uses only three of the 110 pair rows, all of type `query_equal`; unused pair rows have multiplier zero and cannot affect pricing.

The reply-menu constraints are exactly

\[
0\le h\le d,\qquad0\le\ell-h\le5-d.
\]

Writing `r=ell-h` identifies a rectangle `[0,d]x[0,5-d]`. Every active old-row dependence on these variables is affine. Therefore the maximum occurs at one of `(ell,h)=(0,0),(d,d),(5-d,0),(5,d)`. Repeated corners when d=0 or 5 are harmless. No omitted interior integer point can have a larger affine value. The independent check evaluates all four corners directly and sums the three separate menu maxima.

For each of the 1,024 masks and six common d values, the maximum weighted necessary-row score therefore equals the fixed old-row contribution plus the three histogram maxima plus the menu maxima. The residual is `120*(B*actual_covered-D*comparison_covered)-max_weighted_score`, where B,D are the exact beta numerator and common multiplier denominator. Its nonnegativity on all 6,144 conditional cases proves the dual coefficient inequality on every atom.

## Independent reconstruction details

`full_pricing_audit.py` implements the 18 active fixed-path old rows directly from the uniform-sharing definition. It reconstructs the local histogram rows and all active cross-menu count terms separately. For a retained-overlap query-equal row, with q=5, local query bits z_i,w_i, and totals B,C,K, it uses the excluded-own-index sum

\[
4\sum_i H_i-
\sum_i\left[a_i(B+C-z_i-w_i)-g_i(K-z_iw_i)\right],
\]

where `a_i=1/(p_i+1)` and `g_i=1/((p_i+1)(p_i+2))`. This is the literal `j=k != i` comparison sum expressed by that family's histogram; no family coupling is introduced. The terminal rows are independently reconstructed as `4*actual_last_share-query_count*sum_inverse_load+own_query_inverse_load`.

All small per-client coefficients are formed using Fraction and scaled by 120 only after checking integrality. Arrays holding these small coefficients use ordinary integers; multiplication by the large dual integers first converts to object arrays. All weighted sums and residuals therefore use unbounded exact integers. No floating tolerance selects the sign of the final residual.

The actual run in `full_pricing_audit.json` reports:

- all 1,024 masks, six common multiplicities, all 792/15,504 histograms and four menu corners retained;
- 126 distinct cached score contexts, matching the discovery program's context count;
- all 6,144 conditional residuals nonnegative;
- minimum scaled integer residual0, with 84 zero conditional cases;
- no negative case.

The source dual certificate SHA-256 is `6cc1849b3808d773a317efd64c6ed6df59ce89a589a06a303e9edc297f3d9d34`. The independent program ran in about 24 seconds and did not call an optimizer. It is a full-universe coefficient check, not a finite game search or a support-only dual check.

## Status boundary

The dual upper bound and its factorization pass this internal independent attack. The exact relaxation optimum additionally requires the separate 67-atom primal review. No external peer review, novelty certification, SPE completion of a relaxation point, or solution of `Q-CAG-HALF` is claimed.
