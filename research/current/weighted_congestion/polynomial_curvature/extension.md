# Exact three-load tradeoff for nonnegative-coefficient polynomials

Claim ID: **WC-R1-THREELOAD-ENVELOPE v1**. Contribution: R1 independent
curvature reviewer. Objects, domain, quantifiers, assumptions, definitions and
conclusion are precisely those of the theorem below. Scope: exact optimization
of three positive load values, not a game-equilibrium threshold. Dependencies:
the self-contained discrete convex-envelope proof below. Evidence:
extension_verify.py and its exact output; root reconstructed and checked the
argument after the independent reviewer supplied it. Objections: unrestricted
nonnegative coefficients, finite degree and positive load ordering are essential;
negative coefficients are not covered. Status: complete basic-tool proof,
informed internal review, no external review or novelty certification. Related
files: proof.md, review.md and extension_verify.py. The tool's value is a sharp
reusable interpolation constraint; its mechanism is adjacent-grid support; its
ambition is deliberately local.

This is a self-contained strengthening of the analytic tool in proof.md.
It is a standard convexity/linear-programming consequence, with no novelty
claim and no claim about an approximate-equilibrium threshold.

## Theorem

Fix real numbers 0<L<H<U and 0<epsilon<1. Set

    r=L/H in (0,1), s=U/H>1,
    gamma=log(s)/log(1/r)>0.

Choose an integer n>=0 with r^(n+1)<=epsilon<=r^n, and define

    theta=(epsilon-r^(n+1))/(r^n-r^(n+1)) in [0,1],
    M(epsilon)=theta*s^n+(1-theta)*s^(n+1).

At a shared endpoint either possible choice of n gives the same value.
Among every finite nonzero polynomial p with nonnegative coefficients
satisfying p(L)<=epsilon p(H), the exact minimum of p(U)/p(H) is
M(epsilon). It is attained by

    p_*(x)=theta*(x/H)^n+(1-theta)*(x/H)^(n+1).

Every minimizer is a positive scalar multiple of p_*. Thus at an endpoint
the minimizer is a monomial; otherwise it has exactly these two adjacent
nonzero monomials.

The minimum feasible degree, with degree understood as an integer, is

    d_min=ceil[log(1/epsilon)/log(H/L)].

For every degree budget D>=d_min the same optimum M(epsilon) is achieved;
for D<d_min no feasible polynomial exists. Finally,

    M(epsilon)>=epsilon^(-gamma),

with equality exactly when epsilon=r^k for an integer k>=1. Consequently
gamma is the largest exponent c for which the bound
p(U)/p(H)>=epsilon^(-c) holds for all epsilon and all admitted p.

## Proof

Write p(x)=sum_k a_k x^k, and normalize by

    q_k=a_k H^k/p(H).

The q_k are nonnegative, have finite support, and sum to one. The two
ratios of interest are therefore

    z=sum_k q_k r^k=p(L)/p(H)<=epsilon,
    y=sum_k q_k s^k=p(U)/p(H).

Let f(x)=x^(-gamma) on x>0. Then f is strictly convex and decreasing,
and f(r^k)=s^k. Let ell_n be the affine line through the two points
(r^n,s^n) and (r^(n+1),s^(n+1)); its slope is negative.

For a convex function, a chord extended outside its endpoint interval
lies below the function. Every grid point r^k lies outside the open
interval (r^(n+1),r^n) or is an endpoint. Hence

    ell_n(r^k)<=f(r^k)=s^k

for every integer k>=0, with equality only for k=n,n+1 by strict
convexity. Taking the q-weighted sum and using the negative slope gives

    y>=sum_k q_k ell_n(r^k)=ell_n(z)
      >=ell_n(epsilon)=M(epsilon).

The advertised polynomial p_* has p_*(H)=1, p_*(L)=epsilon, and
p_*(U)=M(epsilon), proving attainability. Equality requires z=epsilon
and q supported on n,n+1, uniquely fixing the weights to theta,1-theta.
This also proves uniqueness up to scaling, including the endpoint cases.

If p has degree at most D then r^k>=r^D for every occupied k, so
z>=r^D. Feasibility thus requires r^D<=epsilon, equivalently
D>=d_min. The polynomial p_* has degree d_min after zero coefficients
are omitted, so this condition is sufficient as well.

Jensen's inequality gives y>=f(z)>=f(epsilon)=epsilon^(-gamma).
For the minimizing p_*, Jensen is strict when 0<theta<1 and is an
equality at the monomial endpoints. Choosing epsilon=r^k and
p(x)=(x/H)^k also shows that an exponent greater than gamma cannot
hold uniformly over epsilon. This proves every assertion.

## Specialization to the prefix loads

For L=3/2-2^(-m), H=3/2, U=2-2^(-m), the exact exponent is

    gamma_m=log((2-2^(-m))/(3/2))
              /log((3/2)/(3/2-2^(-m))).

For m>=3 this exceeds 2^(m-2), as proof.md establishes. The exact
piecewise-affine function M is the sharp leakage/overshoot tradeoff on
these three loads, even when arbitrarily large polynomial degrees are
allowed. In particular increasing the degree budget beyond d_min cannot
improve the optimum for this specified leakage constraint.

The regression extension_verify.py checks the affine minorants and
attaining polynomials using exact rational arithmetic on a finite sample;
the argument above is the universal proof.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
