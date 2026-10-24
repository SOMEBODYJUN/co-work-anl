# ALL-FUTURE primary: full postread audit

2026-10-24, menu9. Object read in full: `../parent/all_future_coverer_payment_family.md`, identity B10-ALL-FUTURE-COVERER-PAYMENT-v1. The preceding contract reconstruction is in `net_all_reset_kernel_review.md`; this note is a subsequent full postread audit, not a claim of blind review of the primary text.

**Verdict:** sections 1-5 check as a general legal-family and conditional-certificate theorem. No fatal objection found. Common ROLE feasibility, an improvement of the welfare bound, and Q-CAG-HALF remain unproved. No finite tests or new instances were used.

## Domain, density, and payment

For R-only input, every reset x-coverer is current or genuinely future. There are a-1 future recipients, so 0<=z_j<=h/a gives L>=h/a automatically. Together with the explicit L<=vh/a, the exact range is h/a<=L<=min(h,vh/a). The full-uniform point is nonempty for every h>=0.

The density proof uses only the unchanged source inventory/edge contract, true reset targets, internal z<=h/c_A, nonnegative current, and increasing roles. ALL-FUTURE retains all of them. First-deviation parents may be numerous but have one role, so the antichain bound applies. No mandatory-new equality or parent uniqueness is needed.

The source current bound L_tx<=f_tx/c_A(x), followed by f_tx<=1, upper-bounds its complete amount by the complete query D_t<=u_i. The displayed refund expands to u_i-sum_xL_tx exactly; each displayed term is nonnegative. The same role's multiple contexts are still not jointly bounded.

## Old-source and strictness check

The primary correctly attributes same-client positive/negative cancellation to old round5 NET and the peer source-preserving review section 4. In the latter, source identity is explicitly retained, so the primary correctly avoids calling clientwise cancellation or maximal current new.

The extra recipient freedom is real: after cancellation, necessary mass need not remain among the original new coverers. This is independent of latest/fractional ownership, which changes initial labels and capacities rather than this local recipient freedom.

For utmost literal precision, the sentence "strictly contains the restricted recipient family" means that inclusion is general and can be strict for admissible local count data, as in the following example. It does not mean strictness for every fixed instance/context, nor an already exhibited strict enlargement of ROLE-feasible full SPEs. The primary already states the latter limitation explicitly. One could replace the phrase by "contains, and the inclusion can be strict at the local-polytope level" to remove any possible ambiguity.

## Price example: 5/4, 1, 3/4 all check

Use the primary's counts a=4,v=3: current plus one common future plus two new futures in A, and one lost past coverer in V. Set H=h/4. Current price is 1, common continuation price is 0, and each new continuation price is 2.

**Old fixed-new plus optional common.** The two new edges each carry H. If the common edge carries t in [0,H], current is 2H-t. Price is

    (2H-t)+2H+2H=6H-t,

minimized at t=H, giving 5H=5h/4. Thus the primary's 5/4 is the old round8 optional-common minimum, not the raw common-zero value. The raw common-zero price would be 3/2.

**Old same-client NET plus optional common.** At most one new edge-unit H can be canceled by the one lost coverer. At the maximum cancellation, total new outflow is H. If common outflow is t in [0,H], current is 3H-t. Price is

    (3H-t)+2H=5H-t,

minimized at t=H, giving 4H=h. Partial or zero cancellation has weakly larger price, so 1 is the true minimum of that restricted family.

**ALL-FUTURE.** The required outflow is only (a-v)H=H and may all go to the zero-price common coverer. Both new edges are zero and current is 3H. Price is 3H=3h/4. Since the common edge has cap H, this is also the local minimum. Taking h<=1/3 ensures f=3h<=1. These are legitimate local polytope comparisons; no full SPE realization or target counterexample is asserted.

## Price recursion and its exact boundary

For the per-client ALL-FUTURE family, d=(a-v)_+ is an integer in [0,a-1]. After sorting successor unit costs, a fixed total of k edge-units uses the k cheapest targets. The constraints 0<=beta_j<=1 and sum beta_j>=d admit an integral optimum for this linear objective, giving exactly the primary's minimum over k=d,...,a-1. Ties can also have fractional minimizers. With lambda all one, backward induction gives every successor unit cost one and hence every candidate cost one.

**Critical extension boundary:** this per-client price recursion does not remain the price recursion after the whole-row pooling extension in my preceding review section 7. Replacing individual L_tx<=v_tx h_tx/a_tx by sum_xL_tx<=u_i couples distinct clients at one context. Each client's routing can no longer be minimized independently: cancellation/current choices share one aggregate u_i constraint, and context inputs may mix multiple origins. A joint context allocation or the larger finite LP is required. The primary's recursion is correct because the primary presently states the per-client family only.

## Conditional synthesis and pressure test

Replacing R-FLOW by ALL-FUTURE keeps exact mass conservation. H, initial current, and I complement payments must belong to the same point; fractional ownership changes require recomputation, as stated. Any common ROLE-feasible point still implies |O|<=2W. Canonical ownership and uniform routing keep the non-ROLE region nonempty.

At m=5 the primary provides that same conditional implication only. No unconditional OPT_5<=2W follows from the enlargement or the local price example. Novelty, external review, and original general welfare status are accurately limited in the primary text.
