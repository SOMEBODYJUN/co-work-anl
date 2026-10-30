# 共同幂混合全局最小点障碍：独立重构与逐区间攻击

Reviewer: boss4 internal `stronger_lower` agent. This review began by reconstructing
the two-independent-mobile cone problem before reading the candidate proof.
No public-board publication or Git write is performed by this reviewer.

Reviewed preliminary file: `power_mixture_minimizer_obstruction.md`; canonical account: `research/current/weighted_congestion/common_power_mixture_obstruction.md`.
Reviewed claim: `WC-COMMON-POWER-MIXTURE-MINIMIZER-OBSTRUCTION-v1`.
Frozen source SHA-256:
`ace6b4909ccd0a37ccea3cb9cdce0a16e2e545c64194675733c677f838a49ff7`.
该hash记录读稿时冻结字节；主研究者后来仅修状态、规范链接及复现合同，未改变数学陈述或公式。

## Independent bottleneck reconstruction before reading

Four players can consist of two independent mobile players and two background
players with singleton strategy families. An exact PNE is automatic if each
mobile's true two costs are constant and independent of the other mobile.
For a mobile of weight `w`, joining a background load `b` changes a power
objective by `a[(b+w)^p-b^p]`, not by its final resource fee. Therefore a power
objective can favor a true-cost-bad option.

However, defeating every single exponent separately is insufficient: positive
mixtures can combine two opposite weaknesses and select both true-good options.
For the two-block game a common positive linear separating combination of the
two objective-difference functions is the decisive proof obligation. It must
use coefficients independent of `p` and of the measure. This was communicated
to the boss before reading the frozen proof.

## Model and exact-cost audit

For every integer `d>=32`, the candidate parameters
`R=d/16`, `A=d^2+1`, `K=d(d+1)`, `W=K^(4d)` are positive rationals/integers
as stated. `W>1`, so both background weights `(A-1)W` and `W-1` are positive.
The two mobiles and two backgrounds give exactly four players; their four
resources are distinct. All coefficients are positive rational and independent
of `p`; every latency is a pure degree-`d` monomial.

The true mobile costs are exactly `R` and `1`, using post-deviation total
loads `W`, `AW`, `1`, and `W` respectively. The blocks are disjoint. The
state using both good options is the unique exact PNE. Background players
have no alternate strategy; their self-deviation inequalities hold for every
`alpha>=1`. Every other state admits an `R -> 1` deviation. Thus an objective
that excludes the good-good state at every global minimizer has the required
method failure, with strict non-equilibrium exactly for `alpha<R`.

## Power-difference and common-coefficient audit

Set `r=p-d`. Direct resource recomputation gives

    D_H(p)=R W^(p-d)-[(AW)^p-((A-1)W)^p]/(AW)^d
          =W^r[R-A^r delta_A(p)],
    D_L(p)=R[W^p-(W-1)^p]/W^d-1
          =R W^r delta_W(p)-1.

These are the objective changes for bad instead of good, including the fixed
background contribution. The original latency coefficients are held fixed
throughout; no hidden exponent-dependent coefficient substitution occurs.
The proposed

    kappa=1/[4R W^(1-1/(2d))]=4/[d K^(4d-2)]

is positive rational and independent of `p` and `mu`.

## Attack on all real-exponent ranges

All six preliminary estimates are valid at `d>=32`:

1. For `0<p<=1`, `(1-t)^p>=1-t` gives `delta_X(p)<=1/X`.
   For `p>=1`, Bernoulli gives `delta_X(p)<=p/X`.
2. `A=d^2+1<=4^d` holds already at `d=2`, and induction follows because
   `4(d^2+1)-((d+1)^2+1)=3d^2-2d+2>0`. Hence
   `A^(-1/(2d))>=1/2`.
3. For `1<=p<=A`, integrating `p(1-t)^(p-1)` over `[0,1/A]` gives
   `delta_A(p)>=p(1-1/A)^(p-1)/A`. Its last factor exceeds `1/4` by the
   displayed binomial/factorial bound, so `delta_A(p)>=p/(4A)`.
4. `delta_A(p)>=delta_A(A)>1/2` for `p>=A`. In fact
   `(A/(A-1))^A>1+A/(A-1)>2`, so its reciprocal is less than `1/2`.
5. `kappa W=K^2/(4R)>=16R` and `kappa<=1` follow directly; no estimate
   reverses after multiplication because all quantities are positive.
6. `4R/kappa=16R^2K^(4d-2)<=d^(12d-4)`, using `K<=d^3` and
   `16R^2=d^2/16<=d^2`. Also `A^(A-d)>=d^(2d^2-2d+2)`, and the latter
   exponent is at least `12d-4` at `d>=32` (indeed much earlier).

Now let `a=1-1/(2d)` and `b=1-1/(4d)`.

* If `r<=a`, then `p<d+1` and `r<=b`. Thus `D_L<=-15/16` and
  `kappa D_H<=1/4`, giving total at most `-11/16`.
* If `a<=r<=b`, then `d<p<A`. Estimates 2 and 3 give
  `z_A>=p A^(r-1)/4>=p/8`; since `p>d`, this implies
  `z_A-R>=p/16>0`. The same `D_L<=-15/16` estimate applies.
* If `r>=b` and `p<=A`, the preceding lower bound on `z_A-R` still holds:
  it used only `r>=a`, `p>=d`, `p<=A`. Hence the total is at most
  `W^r p[R/W-kappa/16]-1<=-1`.
* If `r>=b` and `p>=A`, then `z_A>=A^(A-d)/2>=2R/kappa`, and
  `z_A-R>=R/kappa` since `kappa<=1`. Bounding `delta_W<=1` gives total
  at most `-1`.

The overlap endpoints are consistent. Together they prove the stronger uniform
bound

    kappa D_H(p)+D_L(p)<=-11/16<0   for every p>0.

Thus there is no uncaught limit at `p->0` or `p->infinity`. The small-`p`
limit has `D_L -> -1`, and lies in the first interval; arbitrarily large
`p` lies in the fourth. No continuity argument at the excluded endpoints
is needed.

## Continuous measures, integrability, and minimizer ties

The finite-state assumption in fact forces `mu((0,infinity))<infinity`:
in a state where `L` uses `l_0`, that resource has load `1` and coefficient
`1`, so its contribution is `integral 1 dmu`. Since `mu` is nonzero, its
total mass is strictly positive. Finiteness of every state objective and
positivity of each original coefficient also gives finite integrals at all
positive loads occurring in `D_H,D_L`. Therefore the difference functions
are absolutely integrable, and linearity is legitimate.

Integrating the uniform bound directly gives

    kappa Delta_H+Delta_L <= -(11/16) mu((0,infinity)) <0.

This covers arbitrary atoms, non-atomic measures, infinite support, and measures
concentrated near either endpoint. `0^p=0` at `p>0` is consistent with every
empty resource and contributes no missing constant. The excluded zero measure
would make every state a minimizer and invalidate the claim, exactly as stated.

At least one integrated difference is strictly negative. Because the two mobile
choices are independent, that entire block's bad option is mandatory in every
global minimizer; a tie in the other block does not help. This handles the
quantifier *every global minimizer*, rather than merely finding one bad minimizer.

## Verdict and scope

No fatal objection found in the frozen stated claim. The proof closes the
nonnegative common-power-mixture minimizer obstruction, including dependent
choice of the measure, continuous measures, weak equilibrium endpoints, and
zero-resource-load conventions. It is still a narrow method limitation:
the very same game has an exact PNE, and nothing in this review promotes it
to the main target's nonexistence or existence theorem. External review and
novelty are unverified. An exact finite audit accompanies this review; it
checks arithmetic and selected actual powers, while the interval proof above
carries the real-exponent and continuous-measure quantifiers.

## Canonical account and actual replay

The final canonical proof SHA256 is `28789630c06bf8057bf6e13abe6abe78648b80b2cae49c5c832117be1cbfe22e`. The root compared it to the reviewed draft: only candidate/review labels and canonical audit links/contracts changed; the model, quantifiers, constants, formulas and interval proof are unchanged.

- `tests/audits/weighted_congestion/ordinal_potentials/verify_common_power_mixture.py`: SHA256 `8ea8601c7ad328517b47accaed7a4fad778776147969ab491d9439ffd0afac23`; root replay result `evidence/runs/weighted_congestion/common_power_mixture/author.json`, exit 0.
- `tests/audits/weighted_congestion/ordinal_potentials/independent_common_power_mixture.py`: SHA256 `d0f6e05956815340f291d1d74e8fa2f93b765a44af71b5f93899e976018ce066`; root replay result `evidence/runs/weighted_congestion/common_power_mixture/independent.json`, exit 0.
