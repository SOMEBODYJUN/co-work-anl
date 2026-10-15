# Heterogeneous endpoint forcing reduces to one light weight

Claim ID: **WC-R1-HET-ENDPOINT-REDUCTION v1**. Author: R1 internal cohort collaborator. Date: 2026-10-14.

Status: complete local proof; exact regression supplied; independent adversarial review passed (review.md). This is a restricted construction obstruction, not a universal existence theorem or an improved lower bound. No external theorem is used.

## Exact statement and scope

Fix an integer d≥0, an integer N≥1, positive weights w_1,...,w_N, and polynomials p,f_1,...,f_N of degree at most d with nonnegative coefficients. There are resources a_0,b_0,a_1,b_1,...,a_N,b_N. The paired core resources have cost p, and the paired resources a_i,b_i have cost f_i. A player of weight 1 chooses all a-resources or all b-resources. Light player i chooses {a_0,b_i} or {b_0,a_i}. Costs sum the resource costs, without multiplying by the player's weight, as in MODEL.md.

Write W=Σ_i w_i>0. Suppose α>1 and the following strict **endpoint forcing** inequalities hold:

(H) p(1)+Σ_i f_i(1+w_i) > α[p(1+W)+Σ_i f_i(1)].

(L_i) p(1+w_i)+f_i(w_i) > α[p(W)+f_i(1+w_i)] for every i.

Then there are an index i, an integer m≥1, and a same-degree homogeneous star with m light players, each of weight w_i and each satellite polynomial f_i, retaining the core polynomial p, such that every pure state has a strict improving deviation by factor greater than

    γ = 1 + (floor(n)/n)(α−1),       n=W/w_i.

In particular γ>1 and γ>α−1/(α−1). Thus the output has no γ-PNE. The statement concerns exactly the displayed endpoint forcing certificate; it does not assert that every heterogeneous star without an α-PNE satisfies that certificate.

Objects: finite games in the exact weighted congestion model. Domain: arbitrary positive real weights and nonnegative real polynomial coefficients; no rationality restriction. Quantifiers: for every input satisfying (H),(L_i), there exists an output index and integer multiplicity. Dependencies: polynomial monotonicity and convexity on nonnegative arguments. Evidence: the proof below and verify_endpoint_reduction.py. Objections: arbitrary full-state certificates are outside scope; no direct comparison with the published monomial envelope is claimed.

## Why these endpoints already cover every state

Fix the heavy player on its a-strategy. Let S be the lights choosing {a_0,b_i}, and T=Σ_{i∈S}w_i. If S is nonempty, any i∈S has current cost p(1+T)+f_i(w_i) and switching cost p(W−T+w_i)+f_i(1+w_i). Since T≥w_i,

    p(1+T)+f_i(w_i) ≥ p(1+w_i)+f_i(w_i)
                       > α[p(W)+f_i(1+w_i)]
                       ≥ α[p(W−T+w_i)+f_i(1+w_i)].

If S is empty, (H) is precisely the heavy player's strict improvement inequality. Exchanging a and b covers the other heavy strategy. This proves the input game's full-state nonexistence from the stated certificate, but not the converse.

## Proof of the reduction

The polynomial p cannot be identically zero: otherwise (L_i), nonnegativity, and f_i(w_i)≤f_i(1+w_i) give a contradiction. Consequently p(x)>0 for every x>0. All denominators used below are therefore positive. Zero satellite polynomials are allowed.

Define

    R = α p(1+W)−p(1) > 0,
    H_i = f_i(1+w_i)−α f_i(1).

Condition (H) says Σ_i H_i>R. Since Σ_i w_i=W, at least one i satisfies

    H_i/w_i > R/W.

Fix such an i, and abbreviate w=w_i, f=f_i, n=W/w≥1. Then

    p(1)+n f(1+w) > α[p(1+nw)+n f(1)],                 (1)
    p(1+w)+f(w) > α[p(nw)+f(1+w)].                   (2)

Here n is a positive real coefficient in two algebraic inequalities. We do not call it a player count or assert a game with nonintegral player count.

First, n is large whenever α is large. By (2), monotonicity of f, and p(nw)≥0,

    (α−1) f(1+w) < p(1+w).

Putting A=p(1)+n f(1+w) and B=p(1+nw)+n f(1), we have B≥p(1+nw)≥p(1+w)>0. Therefore (1) implies

    α < A/B
      < [p(1)+n p(1+w)/(α−1)] / p(1+nw)
      ≤ 1+n/(α−1).

Thus

    n > (α−1)^2.                                    (3)

Now put m=floor(n)≥1 and ρ=m/n∈(0,1]. The homogeneous integer star's two heavy endpoint costs are

    A_m=p(1)+m f(1+w)=ρ A+(1−ρ)p(1),
    B_m=p(1+mw)+m f(1).

A nonnegative-coefficient polynomial is convex on [0,∞). Since 1+mw=ρ(1+nw)+(1−ρ),

    B_m ≤ ρ B+(1−ρ)p(1).

Let γ=1+ρ(α−1). Using A>αB and B≥p(1),

    A_m−γ B_m
      > ρ(α−γ)B+(1−ρ)(1−γ)p(1)
      = ρ(1−ρ)(α−1)[B−p(1)]
      ≥ 0.

This remains strict when ρ=1 because the strictness comes from (1). For the light endpoint, m≤n and monotonicity give

    p(1+w)+f(w) > α[p(nw)+f(1+w)]
                 ≥ α[p(mw)+f(1+w)]
                 ≥ γ[p(mw)+f(1+w)].

Hence the integer star satisfies its endpoint inequalities strictly at γ. The preceding full-state argument applies to it.

Finally floor(n)>n−1, and (3) gives

    γ > α−(α−1)/n > α−1/(α−1).

Also γ>1 directly from ρ>0 and α>1. This completes the proof.

## Consequences that do not require literature assumptions

Let F_poly(d) be the supremum of the factors certified by endpoint forcing in homogeneous integer stars with arbitrary nonnegative-coefficient degree-at-most-d core and satellite polynomials. Every factor α>1 certified by heterogeneous endpoint forcing satisfies

    α−1/(α−1) < F_poly(d).

If F_poly(d) is finite, the corresponding non-strict convenient bound is

    α ≤ [F_poly(d)+1+sqrt((F_poly(d)−1)^2+4)]/2.

Thus heterogeneity changes this construction's optimum by at most an additive term tending to zero along any sequence where the certified factors grow. In particular it cannot change its asymptotic growth rate.

A comparison of F_poly(d) with the published monomial-star envelope needs a separate, independently checked polynomial reduction. This file intentionally does not import that external dependency.

## Exact validation and limitations

Run `python tests/audits/weighted_congestion/heterogeneous_endpoint/verify_endpoint_reduction.py`. It constructs a rational ten-light, two-weight instance at d=100 and α=12/5, uses rational arithmetic to check every endpoint, selects the density witness, and checks every state of both the heterogeneous input and homogeneous integer output. It also checks the integer-rounding branch and the degenerate zero-core impossibility on explicit test data. The finite tests verify the implementation and an example; the proof above establishes the arbitrary-real, arbitrary-finite-input statement.

The central unresolved escape is a heterogeneous star whose full-state coverage necessarily uses heavy deviations at some singleton-aligned states or opposite-light deviations, so that (L_i) fails. This result does not exclude that mechanism, asymmetric columns, or topologies beyond this star.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
