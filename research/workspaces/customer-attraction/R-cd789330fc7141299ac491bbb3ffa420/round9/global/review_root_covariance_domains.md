# Independent algebra and domain review of the root-menu note

2026-10-24, global9. Reviewed
`../credible/root_covariance_and_background_domains.md`, specifically its
§1 and §3, and read the cited `../../round5/menu/pair_attack.md` to check the
scope of the universal static-query lower bound. This is an internal review
of those deductions, not a new replay of the old full PB strategy proof.

## Covariance and ROOT

For one customer write `alpha=1[x in a]`,
`g=1/(b+1+k_a)`, and
`h=1/((b+1+k_a)(b+2+k_a))`. Binary `alpha` gives exactly

    1/(b+1+alpha+k_a) = g-alpha h.

Consequently its contribution to `D(p)-C(p)` is

    E[alpha g] - p_x E[g-alpha h]
      = Cov(alpha,g)+p_x E[alpha h].

Summing proves COV-REFUND, with the stated nonnegative refund. The refund is
not an IC term and the covariance need not be nonnegative. In a true root
SPE `u=max_a D_a`; hence `u-D(p)=sum_a p_a(u-D_a)` is a legal nonnegative
combination of whole root IC rows. Adding that quantity proves ROOT. No
customer-reweighted IC is being used. I find no error in these identities.

## PB implication and quantifiers

The original PB construction uses a legal singleton prefix `b`, remaining
population `r=2475`, root profit `u`, and a fixed legal query distribution
`p`. Its displayed (S) is a lower bound `s>u` against **every static tuple
of r legal themes**, including tuples containing singleton actions. This
is exactly the slot count needed by the full root menu: every complete
true root branch `Z(a)` is an r-tuple, and its independent extra query has
denominator `b+1+c(Z(a))`. Thus

    E_(t~p) K(t,a) >= s > u >= D_a

holds for every menu column `a`. The last inequality follows from the
complete SPE root IC and is not an extrapolation from the three on-path
Fill/Copy actions. Average over `a~p` to obtain `C(p)>D(p)` and `C(p)>u`.
Average instead over any column mixture `Q`, and use the fixed query `p`
as a lower bound on the maximum pure query, to obtain `Mfull>=s>u`.

Therefore all three arbitrary-legal-background statements listed in §3
are refuted by the cited old construction. The reduction does not need a
new parameter search or a new full-history strategy proof. It also does
not establish any failure at an empty root or at a root-SPE actual
prefix: the cited prefix covers all clients, and its being actually
reached in a root SPE has not been proved. The note preserves this
distinction correctly.

## Status

No fatal algebraic or domain issue found in §1 or §3. I have not independently
replayed the 34-client unit certificate in §2, the finite diagnostics in
§4, or the old PB strategy itself. No sign of ROOT or ROOT-AGG, and no
general half-coverage bound, follows from this review.
