# 有限权类别三角排序混合势：知悉构造后的独立攻击

Reviewer: boss4 internal `stronger_lower` agent.
Claim: `WC-WEIGHT-CLASS-TRIANGULAR-POTENTIAL-v1`, including the fixed-background
and cluster-rounding corollaries and the class-count necessary condition.
Frozen preliminary source: `triangular_weight_class_potential.md`; canonical source: `research/current/weighted_congestion/weight_bands/finite_weight_class_potentials.md`.
SHA-256: `07df6b400b6fa54478caea600c447f31d5dd784bb5b9afac30e8793557defdc0`.

This is an **informed independent attack**. The reviewer independently
reconstructed the bottleneck of the earlier explicit `B` construction before
reading that earlier proof. The new triangular permutations and root equation
were then communicated by the boss before this manuscript was read. Thus this
record does not claim an independent discovery or a proof reconstruction made
without knowledge of the new central mechanism.

## Root and parameter quantifiers

For fixed integers `d>=2,k>=1`, define
`f_k(x)=sum_{j=0}^{k-1}((d-1)/x)^j-x` on `x>0`. Every summand with positive
degree is nonincreasing and `-x` is strictly decreasing, so `f_k` is strictly
decreasing even at `k=1`. It is continuous, `f_k(1)>=0`, and

    f_k(d)=sum_{j=0}^{k-1}(1-1/d)^j-d<0.

Thus there is exactly one root `A` in `[1,d)`. At `k=1` it equals one;
at `k>=2` it exceeds one. Increasing `k` adds a strictly positive term to
`f_k`, so `A_d,k` in fact increases strictly. The stated nondecreasing claim
is valid and supplies the at-most-`k` formulation.

Writing `q=d^(1/k)`, `B=sum_{j=0}^{k-1}q^j`, one has `(d-1)/B=q-1` and

    f_k(B)=sum_{j=0}^{k-1}(q-1)^j-sum_{j=0}^{k-1}q^j<=0.

Monotonicity gives `A<=B`. Fixed `k>=2` has the simple squeeze

    (d-1)^((k-1)/k)<=A<=sum_{j=0}^{k-1}d^(j/k),

so `A/d^(1-1/k)->1`. At `k=1`, both sides are exactly one. These claims
do not require a uniform asymptotic in growing `k`.

The scope observation `A_d,k -> d` at fixed `d` is also correct. Let its
monotone limit be `L<=d`. If `L<=d-1`, the defining sums cannot remain
bounded as `k` grows. Otherwise `(d-1)/L<1`, and taking the geometric-series
limit yields `L=1/[1-(d-1)/L]`, hence `L=d`. This confirms that the new
bound does not silently solve the unrestricted-class target.

## Arbitrary insertion bound and convex swapping

For a fixed old order, inserting a player of weight `w` after prefix `X`
adds exactly

    w c(X+w)+sum_j v_j[c(z_j)-c(z_j-w)].

All terms are nonnegative. For integer degree `1<=p<=d`, the derivative
bound and `u=(X+w)/Y` give

    Delta P<=wY^p[u^p+p(1-u)]<=p wY^p<=d wY^p.

The middle inequality uses `u^p<=u<=pu`. Constants contribute exactly
`w` times their constant coefficient; nonnegative mixtures and zero fees
are therefore included.

The adjacent heavy/light swap identity in the manuscript has the correct
sign. Convexity says that the average slope over the longer left interval
ending at `z` is smaller. After swapping only the mover with a neighbor,
deleting the mover leaves the identical old user order. Therefore total
potential comparisons yield the claimed *marginal* comparisons as well.
This is the important reason the swapping argument is legitimate.

If every suffix weight is at most `w`, moving the mover to the end increases
the total integral, yielding the marginal upper bound `w c(Y)`. If every
suffix weight is at least `w`, moving it to the end decreases the integral,
yielding the lower bound `w c(Y)`. Empty suffixes give equality. Equal-weight
swaps give equality, and inserting at the end of its current class is valid
because the resource integral depends only on class counts.

## Attack on the new triangular permutations

For `pi_r=(k,k-1,...,r+1,1,...,r)` and inserted class `i`:

* If `r<i`, class `i` lies in the initial light-to-heavy segment. Its later
  classes in that segment have smaller indices than `i`, as do *all* classes
  in the final segment `1,...,r`. Every suffix user is therefore heavier.
  The lower bound is `w c(Y)` and the arbitrary-order upper bound is
  `d w c(Y)`.
* If `r=i`, class `i` is last and its increment is exactly `w c(Y)`.
* If `r>i`, class `i` lies in the final heavy-to-light segment. Only
  `i+1,...,r` follow it, all lighter. The upper bound is `w c(Y)` and
  nonnegativity supplies the lower bound zero.

No hidden mixed-weight suffix remains. Missing classes simply contribute no
users; the inserted player ensures `Y>0`. Arbitrarily large cohorts are handled
by the same order and need no multiplicity bound.

## Mixture normalization, common multipliers, and arbitrary strategies

Put `t=(d-1)/A` and `lambda_r=t^(r-1)/A`. The root equation is exactly
`sum lambda_r=1`, with every coefficient strictly positive even when `t<1`.
With `S_i=sum_{r<=i}lambda_r`, the triangular bounds yield

    S_i w c(Y)<=Delta_i F_c<=[1+(d-1)S_(i-1)]w c(Y).

The upper coefficient equals
`1+t sum_{j=0}^{i-2}t^j=sum_{j=0}^{i-1}t^j=A S_i`. Thus the multiplier
`h_i=S_tau(i) w_i` is strictly positive and identical on every resource.
It does not depend on local class counts, local missing types, coefficients,
or any choice of strategy. Global class indexing is essential.

Deletion uses the same insertion estimate in reverse. After summing removed,
added, and retained resources, the exact claimed inequality follows:

    Delta Phi<=h_i[A C_i(s')-C_i(s)-(A-1)C_retained]
             <=h_i[A C_i(s')-C_i(s)].

Strict `A` improvements decrease the finite-state potential. A global minimum
exists and every single-player local minimum is a weak `A`-PNE. This covers
empty strategies, zero costs, a zero-cost deviation, and retained resources
without ratios. Arbitrary positive real weights and nonnegative real
coefficients create no existence obstruction because no computation of the
minimum or of the algebraic root is claimed.

At `d=0`, individual minimization of constant fees is exact. At `d=1`, the
given affine potential has insertion increment `w c(Y)` by
`[(X+w)^2-X^2+w^2]/2=w(X+w)`. These endpoints are handled separately;
the theorem's parameter definition remains `d>=2`.

## Three corollaries and their exact limitations

**Restricted target scale and necessary class count.** If `d>=16` and
`k<=ln d/ln ln d`, then `q>=ln d>2`, so
`A<=B<=d/(ln d-1)<=2d/ln d`. No instance parameter enters the constants,
but the global class-count premise remains indispensable.

If a degree-at-most-`d` game has no `alpha`-PNE (`alpha>=1`), then `B>alpha`;
otherwise the proven `A<=B` existence theorem contradicts nonexistence.
Rearranging positive quantities gives exactly

    k>ln d/ln(1+(d-1)/alpha).

The strict sign is correct, and the statement does not claim simultaneous
activation of these classes in any state. For fixed `C>0` and
`alpha=C d/ln d`, the right side is asymptotic to `ln d/ln ln d`.

**Fixed-background absorption.** Only players whose strategy family has
more than one distinct resource subset need be counted as mobile. Fixed
players produce resource-specific nonnegative loads `B_e`. The binomial
coefficients of `c_e(B_e+x)` are nonnegative and the degree does not increase.
Every mobile state and true deviation cost is preserved. Fixed players'
only deviation is to their same strategy, so their inequalities hold for
every `alpha>=1`. Fixed players may have arbitrary different positive weights
and arbitrary fixed resource subsets, including empty ones. When no mobile
player exists, the unique state is directly an exact PNE; no `k=0` formula
is invoked. The argument does not treat a merely strongly incentivized player
as fixed.

**Cluster rounding.** Given fixed labels with `v_tau(i)<=w_i<=R v_tau(i)`,
round *only* mobile players down to their representatives. For every state,
including every actual unilateral deviation state,

    x'=B_e+sum v_tau(i)<=x=B_e+sum w_i<=R x'.

The last inequality uses `B_e>=0` and `R>=1`. Nonnegative polynomial
coefficients imply `c(x')<=c(x)<=R^d c(x')`, including constants and
zero fees. If `x'=0`, then `x=0` and the comparison still holds. Summing
fees and applying the rounded game's equilibrium gives exactly the claimed
`R^d A_d,k` factor, with one distortion factor rather than its square.
Unused or repeated representatives reduce the actual class count and are
handled by monotonicity. Fixed players need not be rounded. If no mobile
player exists, exact equilibrium is immediate.

For `R=exp(1/d)`, `R^d=e`; combining the previous restricted-class
corollary therefore gives `2e d/ln d` with all original class-cover premises
retained. There is no claim that an arbitrary weight spectrum admits such a
cover by the permitted number of narrow clusters.

## Verdict and verification scope

No fatal objection found in the frozen triangular claim, its root properties,
the strict-improvement potential, or these corollaries. This is an informed
independent attack, not an uninformed reconstruction of the new mechanism.
The theorem is a structural subclass result; the unrestricted main target
remains open. External review and global novelty are unverified.

The independent Fraction audit tests literal ordered resources, arbitrary
class multiplicity and missing classes, global subset deviations, background
absorption, and one-sided rounding. Cases with integer `t` give exact rational
root parameters. Additional rational upper-root parameters test the `t<1`
region with normalized coefficients and a directly checked inequality;
they are not misreported as exact rational roots. Real/algebraic parameters
are covered by the proof above, not by the finite tests.

## Canonical paths and root replay

The canonical source hash is `81587ce089a0aba0aad278ac73e471aff174b9a8d2e7c2ac88205ecf061b2f60`. The root added canonical paths/status and two explicitly derived explanatory paragraphs (mobile-class necessary condition using the reviewed background corollary, and the already reviewed fixed-d root limit); the theorem identities, parameters and proofs are unchanged.

- Author audit: `tests/audits/weighted_congestion/weight_types/verify_triangular_classes.py`; result `evidence/runs/weighted_congestion/weight_types/triangular_classes.json`.
- Independent audit: `tests/audits/weighted_congestion/weight_types/independent_triangular_classes.py`; result `evidence/runs/weighted_congestion/weight_types/independent_triangular_classes.json`.

Both canonical replays exited 0. The latter record preserves the exact frozen proof hash it audited; code changes only route that hash to the canonical file. The proof of the real-root and all-real-input statements is analytic, not finite sampling.
