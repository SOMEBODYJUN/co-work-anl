# WC-R1-TOTAL-COST-POWER-OBSTRUCTION v1

## Exact statement and identity

For every real exponent `q>0`, `q!=1`, and every finite `alpha>=1`,
there is a finite WC-TARGET v1 game of degree at most **one**, with all
weights equal to one and only one player having more than one strategy,
such that the unique global minimizer of

`J_q(s) = sum_i w_i C_i(s)^q`

is not an `alpha`-PNE. In fact, its mobile player has a deviation with an
arbitrarily prescribed improvement ratio `R>alpha`.

- **Objects / domain:** finite atomic congestion games, arbitrary finite
  multi-resource strategies, the unmultiplied latency-sum cost convention
  of MODEL.md; nonnegative affine and constant latencies are sufficient.
- **Quantifiers:** a separate game can be chosen for each `q,alpha,R`.
  The number of players and resources can grow with `R` when `0<q<1`.
- **Definitions:** a fixed player has a singleton strategy family; this
  does not mean its strategy contains a single resource. A unique global
  minimizer is also a strict local minimizer here because there are just
  two pure states.
- **Conclusion / scope:** this disproves degree-only approximation
  guarantees obtained by minimizing this specified nonlinear objective.
  It does not assert that the games lack approximate equilibria. They have
  an exact PNE at the other state. It does not rule out other nonseparable
  objectives or game-dependent state-selection procedures.
- **Dependencies:** only the WC-TARGET definitions and elementary powers.
- **Status:** complete elementary proof, literal exact-arithmetic checks
  for `q=1/2` and `q=2`; internal informed review passed by
  `dense_bridge/local_curl` (see `REVIEW.md`). No external review or
  novelty claim.
- **Source / contributors:** reconstructed by the R1 `dense_bridge`
  subagent on 2026-10-14; neither an external-paper theorem nor a result
  copied from the previous local-potential obstruction.
- **Related files:** `verify_power_objective.py`,
  `power_objective_exact_checks.json`, `universal_additive_ordinal_bridge.md`.

## Why this route was tested

Taking a power of each player's total cost is a natural nonseparable
escape from resource-wise marginal sandwiches. One might hope that
concavity lowers the effective polynomial degree, or that convexity makes
an individual improvement more valuable. Arbitrary multi-resource
strategies and unrelated private baseline costs invalidate these two
heuristics respectively. The constructions below isolate those failures
already in unweighted affine games.

## Concave powers: `0<q<1`

Fix `R>alpha`, and choose a positive integer `m` so large that

`(1-2^(-q)) m^(1-q) > R^q-1`.                         (1)

There are `m+1` unit-weight players and resources `a,e_1,...,e_m`.
The only mobile player, player 0, chooses either `{a}` or
`{e_1,...,e_m}`. Fixed player `j` uses only `{e_j}`. The latencies are

`c_a(x)=R`,     `c_{e_j}(x)=x/(2m)`.

At the bad state `s`, player 0 uses `{a}`. Its cost is `R`, and every fixed
player has cost `1/(2m)`. At the good state `t`, player 0 uses all the
`e_j`; every shared load is 2, player 0's cost is 1, and every fixed
player's cost is `1/m`. Therefore

`J_q(s)=R^q+2^(-q)m^(1-q)`,

`J_q(t)=1+m^(1-q)`.

Condition (1) gives `J_q(s)<J_q(t)`. Since these are the only states, `s`
is the unique minimizer. Yet `C_0(s)=R>alpha C_0(t)`, proving the claim.
The finite integer `m` exists because `1-q>0` and `1-2^(-q)>0`.

All game data can be rational by taking rational `R` and integer `m`;
the objective exponent itself need not be rational.

## Convex powers: `q>1`

Fix `R>alpha`, and choose a nonnegative integer `H` so large that

`(q/2) H^(q-1) > R^q-1`.                            (2)

There are two unit-weight players and three resources `a,b,e`.
Player 0 chooses `{a}` or `{e}`. The fixed player uses `{b,e}`. Set

`c_a(x)=R`,     `c_b(x)=H`,     `c_e(x)=x/2`.

At `s`, player 0 uses `{a}` and the costs are `(R,H+1/2)`.
At `t`, player 0 uses `{e}` and the costs are `(1,H+1)`.
Consequently

`J_q(t)-J_q(s)=1-R^q+(H+1)^q-(H+1/2)^q`.

By integrating the derivative `q x^(q-1)` over `[H+1/2,H+1]`,

`(H+1)^q-(H+1/2)^q >= (q/2) H^(q-1) > R^q-1`.

Hence again `J_q(s)<J_q(t)`, while player 0 improves from `R` to 1.
Existence of finite integer `H` follows from `q-1>0`. Rational game data
are again sufficient.

## Boundary and legality audit

Both families have finite nonempty player/resource sets, positive
resource-independent weights, nonempty finite strategy families, and
nonnegative coefficients of degree at most 1. Constants are permitted
by WC-TARGET. All occupied-resource costs and both mobile-player costs
are positive. Thus neither a quotient by zero nor a limiting definition
of equilibrium is used. The failure is strict: choose `R>alpha`, rather
than equality, and choose strict inequalities (1) or (2).

The good state is an exact PNE: the mobile player would otherwise
increase its cost from 1 to `R>1`, and every other player has no
alternative. Thus objective failure must not be confused with a
nonexistence lower bound. Because degree-at-most-one games belong to
every `G_d` with `d>=1`, this objective family cannot certify any finite
universal factor as a function of `d` alone.

## Literal exact checks and their scope

`verify_power_objective.py` constructs the actual finite strategies and
latencies using `fractions.Fraction`, recomputes every resource load in
both states, and verifies the player's strict improvement and all fixed
costs. It does not merely compare supplied cost vectors.

For `q=1/2`, take `R=r^2` and `m=18(r-1)^2`, integer `r>=2`.
The objectives simplify exactly to

`J_bad=4r-3`,     `J_good=1+3(r-1)sqrt(2)`.

The strict objective comparison is certified by squaring positive terms:
`[4(r-1)]^2 < 2[3(r-1)]^2`, i.e. `16<18`.
The script checks `r=2,3,5,10`, reaching 1459 players/resources.

For `q=2`, take integer `R>=2` and `H=R^2`. The objective gap is exactly
`J_good-J_bad=7/4>0`. The script checks `R=2,3,10,100,1000`.

These computations are finite implementation checks. The two general
proofs above, rather than numerical sampling, establish the quantified
claim for all real `q>0`, `q!=1`, and all requested finite ratios.

## Literature check

The primary sources checked for the surrounding model and existing
potential arguments were Christodoulou et al.,
[arXiv:2002.07466v3](https://arxiv.org/html/2002.07466v3), especially its
model and Theorem 4, and Caragiannis--Fanelli,
[ICALP 2019, article 133](https://drops.dagstuhl.de/storage/00lipics/lipics-vol132-icalp2019/LIPIcs.ICALP.2019.133/LIPIcs.ICALP.2019.133.pdf).
The present two-state objective obstruction is an independent elementary
derivation; the search was not a priority review for this claim.

## Remaining obligations / retry condition

Internal independent attack should check the exact quantified scope and
literal constructions. The main `o(d)` existence goal is untouched.
A retry of a nonlinear total-cost objective needs additional structure
that prevents arbitrary splitting of an alternative across resources or
unrelated large private baseline costs, or a different global objective
that couples these effects rather than applying a fixed power playerwise.
