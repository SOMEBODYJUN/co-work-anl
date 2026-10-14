# Independent internal review of the endpoint reduction

Claim: **WC-R1-HET-ENDPOINT-REDUCTION v1**. Date: 2026-10-14.

Reviewed objects: `endpoint_reduction.md`, `verify_endpoint_reduction.py`, and
`verification.json` in this directory. Reviewer: independent endpoint-attack
agent. **Verdict: the stated restricted reduction is proved. No mathematical
gap or counterexample was found.** This is internal review, not external peer
review, and does not establish a universal equilibrium theorem or identify the
optimal homogeneous polynomial-star envelope.

## Independence and scope

Before opening the candidate proof, the reviewer received only the exact model,
the two endpoint hypotheses, and the proposed conclusion. The reviewer
independently reconstructed the density selection, the bound
`n > (alpha - 1)^2`, and the convex rounding argument, and reported them to the
coordinator before receiving the proof path. The subsequent review compared the
frozen proof with that reconstruction. No shared claim catalog or public board
was edited for this review.

The claim uses arbitrary positive real weights and nonnegative real polynomial
coefficients, with degree at most the same fixed `d` before and after reduction.
The game remains finite because the chosen multiplicity is `floor(W / w_i)`.
The number `W / w_i` is used algebraically before rounding; no fractional-player
game is assumed.

## Independent proof reconstruction

Write `a = alpha - 1 > 0`, `Q = p(1)`, and `P = p(1 + W)`. The heavy endpoint
hypothesis gives

    sum_i [f_i(1 + w_i) - alpha f_i(1)] > alpha P - Q.

Weighted averaging with the positive weights `w_i` therefore selects an index
such that, for `w = w_i`, `f = f_i`, and `n = W / w`,

    Q + n f(1 + w) > alpha [P + n f(1)].

The original light hypothesis still holds for that same selected index. Put
`F = f(1 + w)` and `G = f(1)`. Monotonicity and nonnegativity give the particularly
short bottleneck calculation

    n F > alpha P - Q + alpha n G >= a P,
    P + F >= p(1 + w) + f(w) > alpha [p(W) + F] >= alpha F.

Consequently `F > 0`, `P > a F`, and `n F > a^2 F`, so `n > a^2`. This argument
does not compare `w` or `W` with 1 and therefore covers weights larger than 1 as
well as weights smaller than 1.

Let `m = floor(n) >= 1`, `rho = m / n > 0`, and `gamma = 1 + rho a`. Scaling the
strict fractional heavy inequality yields

    Q + m F > (1 - rho) Q + rho alpha P + alpha m G.

Convexity gives

    p(1 + m w) <= (1 - rho) Q + rho P.

The exact identity

    [(1 - rho) Q + rho alpha P]
      - gamma [(1 - rho) Q + rho P]
    = rho (1 - rho) a (P - Q) >= 0

and `alpha m G >= gamma m G` prove the homogeneous heavy endpoint strictly.
For the light endpoint, `m w <= W` and `gamma <= alpha` immediately give

    p(1 + w) + f(w)
      > alpha [p(W) + F]
      >= gamma [p(m w) + F].

Finally `floor(n) > n - 1` and `n > a^2` imply

    gamma > alpha - a / n > alpha - 1 / a,

while `rho a > 0` gives `gamma > 1` separately. Thus the maximum of the two
requested lower bounds is exceeded strictly.

The candidate's proof is equivalent to this argument. Its use of the combined
denominator `B = p(1 + W) + n f(1)` in the convexity calculation is correct and
absorbs the nonnegative satellite term into the same inequality.

## Boundary cases and full-state interpretation

- An identically zero core is incompatible with any strict light hypothesis:
  `f_i(w_i) <= f_i(1 + w_i) <= alpha f_i(1 + w_i)`. A nonzero polynomial with
  nonnegative coefficients is positive at every positive argument, so the
  candidate's divisions are justified.
- An identically zero satellite is allowed in the input, but cannot be the
  selected positive-density witness. The selected `F` is positive by the heavy
  inequality; no division by an arbitrary satellite cost is required.
- Positive constant terms cause no difficulty in monotonicity or convexity. If
  the entire core is constant, the light hypothesis itself is impossible,
  since its satellite cost weakly increases on switching. In particular the
  degree-zero case is vacuous, not an omitted exceptional construction.
- At an integer `n`, `rho = 1` and `gamma = alpha`; the heavy endpoint remains
  strict because its strictness comes from the selected heavy inequality.
  At values immediately below an integer, the floor may lose almost one whole
  light player, but `1 - rho < 1 / n < 1 / a^2` still proves the strict bound.
  Values immediately above an integer are covered by the same exact argument.
- The branch `m = 1` is valid. All multiplicities satisfy `m >= 1` because the
  selected weight is one term of the positive sum `W`, so `n >= 1`.
- For a fixed heavy strategy, every nonempty set of aligned lights contains a
  light whose current core load is at least `1 + w_i` and whose post-switch
  core load is at most `W`. Its strict endpoint inequality therefore supplies
  a deviation. When the aligned set is empty the heavy endpoint supplies the
  deviation. Paired-resource symmetry covers the other heavy strategy. This
  verifies the candidate's all-state consequence for input and output.

Only the core requires convexity in the rounding proof; satellite
nonnegativity and monotonicity suffice. Nonnegative-coefficient polynomials
meet all these conditions. This observation does not expand the registered
claim's scope.

## Exact checks performed

The existing regression was rerun successfully:

    python research/weighted_congestion_frontier/assets/R1/cohort_growth/verify_endpoint_reduction.py

Its output agrees with the frozen `verification.json`: input factor `12/5`,
selected real multiplicity `235/23`, integer multiplicity 10, and output factor
`557/235`. It checks 1,024 subsets with the heavy player fixed to one strategy
for each of the input and output games; symmetry covers the other heavy
strategy. Its integer-rounding and zero-core checks also pass. Decisions use
exact `Fraction` arithmetic; the reported decimal ratios are display values.

Additional independent checks were run in a transient Python process using the
regression's polynomial evaluator and endpoint assertion, without changing the
frozen proof or evidence files:

| Effective multiplicity `n` | Output multiplicity | Exact output factor |
| --- | ---: | --- |
| `10 - 10^-12` | 9 | `2511111111111/1111111111111` |
| `10` | 10 | `12/5` |
| `10 + 10^-12` | 10 | `24000000000001/10000000000001` |

These are actual feasible endpoint fixtures, not only checks of the rounding
formula. For reproducibility, each uses `alpha = 12/5`, selected weight
`w = 23/1000`, nine other weights `(n - 1) w / 9`, core
`p(x) = x^2 + 1/10000`, and satellites

    f_i(x) = 1/100000 + b_i x^100,
    b_i = (99/100)
          [p(1 + w_i) - alpha p(W) - (alpha - 1)/100000]
          / [alpha (1 + w_i)^100 - w_i^100].

The checks verify all input endpoint inequalities, selection of the first
light by the density inequality, the bound on `n`, both strict lower bounds on
`gamma`, and both output endpoint inequalities. This explicitly exercises
positive constant terms and both sides of the floor discontinuity.

A separate feasible input uses ten lights of weight `23/1000`, one extra light
of weight `10^-6` with identically zero satellite, core `p(x) = x^2`, and the
same coefficient formula with zero constant terms for the ten nonzero
satellites. Every input endpoint and the ten-copy output endpoint pass; the
zero satellite correctly fails the density-witness test.

Finally, 62 exact rounding checks pass for `n = k, k - 10^-12, k + 10^-12`,
`k` in `{1, 2, 3, 10, 100}`, and `alpha` in
`{1.000001, 1.5, 2, 2.4, 3, 10}`, retaining the cases satisfying `n >= 1` and
`n > (alpha - 1)^2`. These finite checks support implementation and boundary
handling; the inequalities above establish the arbitrary-real claim.

## Consequence and limits

The displayed comparison with the supremum `F_poly(d)` follows: the constructed
factor `gamma` belongs to the homogeneous certified family, so
`alpha - 1/(alpha - 1) < gamma <= F_poly(d)`. Solving this inequality yields
the candidate's stated convenient non-strict bound whenever the supremum is
finite. Inclusion of homogeneous stars in heterogeneous stars supports its
asymptotic interpretation for growing certified factors.

The review does not prove that every heterogeneous star lacking an
`alpha`-PNE satisfies these endpoint hypotheses. It does not reduce arbitrary
polynomial satellites and core costs to a published monomial family. Full-state
certificates using other deviations, asymmetric paired resources, and other
topologies remain outside the result. No external source was needed for this
elementary local proof.
