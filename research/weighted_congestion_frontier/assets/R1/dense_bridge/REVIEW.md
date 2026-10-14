# Dense-bridge internal review, 2026-10-14

This directory contains three mechanism-boundary claims. None is a new
WC-TARGET existence upper bound or equilibrium nonexistence construction.
All reviews below are internal, informed reviews, not external referee
certification or a priority search.

## WC-R1-TOTAL-COST-POWER-OBSTRUCTION v1

Reviewer: `dense_bridge/local_curl`; author: `dense_bridge`.

The reviewer checked both general real-exponent arguments and reran the
literal finite-game verifier. The concave family has exactly two states,
cost vectors `(R,1/(2m),...,1/(2m))` and
`(1,1/m,...,1/m)`, and the stated integer-m condition strictly prefers
the bad state. The convex family has costs `(R,H+1/2)` and `(1,H+1)`;
the integral derivative bound holds for all real `q>1`. The existence of
finite integer parameters, degree-at-most-one coefficients, unit weights,
strict `R>alpha`, singleton families of the fixed players, and positive
costs were all checked. The good state is an exact PNE, so the claim must
retain its objective-only scope.

Actual command:

`python research/weighted_congestion_frontier/assets/R1/dense_bridge/verify_power_objective.py`

Actual result: `PASS: 9 literal finite-game exact checks`; arithmetic is
`Fraction` plus an exact positive-radical squaring comparison at `q=1/2`.
The frozen JSON records these nine cases. This run checks implementation
and instances; the general proof establishes the quantified theorem.

## WC-R1-ORDINAL-COPY-BRIDGE v1

Reviewer: `dense_bridge`; author: `dense_bridge/local_curl`.

The deletion-to-empty step gives strict positivity because every nonzero
nonnegative-coefficient polynomial is positive at a positive load. Both
old and new contexts can be simultaneously realized with finite copied
resources and fixed strategies; players in the intersection use both
bundles. The pairwise normalized inequality follows by approaching the
positive critical ratio from above with rational `m/n`. This is a
sequence of finite games using one fixed universal rule, rather than an
infinite-resource game. Pairwise comparability bounds the infimum away
from zero, so the unattained infimum still supplies a legal multiplier.

The every-global-minimizer implication is correct only because the rule
is invariant under restricting strategy families. It cannot be promoted
to a whole-game-specific rule. A some-global-minimizer statement gives
no such conclusion: constant objectives exhibit that boundary.

## WC-R1-GAME-SPECIFIC-SEPARABLE-ORDINAL-BARRIER v1

Reviewer: `dense_bridge`; author: `dense_bridge/local_curl`.

The finite witness game is chosen before considering any potential.
For `eta=(w_min/W)^d`, every same-player context ratio `B/A` lies in
`[eta,1/eta]`. Thus a fixed integer
`L>1/((R-alpha)eta)` and
`M=L+floor(alpha L/eta)+1` fit every required pair of bundles, and
`m=floor(alpha L B/A)+1` satisfies the strict two-sided ratio bound.
This verifies the potentially delicate quantifier order.

Resource permutations are actual automorphisms of the fixed full-subset
strategy game. Their finite average preserves strict decrease and turns
arbitrary game-specific `F_e` into one common `H`. All subset contexts
and bundle switches then occur inside that same game. Positive finite
normalized marginals and their attained minimum yield the forbidden
R-sandwich, with `alpha<R<rho_d` supplying the strict gap.

The example's all-empty exact PNE, and its unique incidence-count
minimizer, correctly show why this obstruction says nothing about
equilibrium nonexistence or arbitrary game-specific minimizer objectives.
No fatal objection remained after this internal check.

## Frozen dependency review

`dense_bridge/local_curl` independently reconstructed the finite
multiscale insertion-path argument and then read
`assets/R1/upper_mechanism/arbitrary_multipliers.md` from commit
`809b032`. It checked the class symmetrization of both potential and
multipliers, heavy-first/heavy-last insertion paths, finite Riemann sums,
strict `alpha<sup` range, finite clone counts, and rational separation
search. The dependency's actual asymptotic lower bound is
`rho_d/d -> 1`, consistent with the Caragiannis--Fanelli `d` potential.
An earlier informal `d+1-epsilon` summary was corrected before being used;
none of the claims here relies on that false stronger summary.

## Searches and remaining work

Primary documents opened were arXiv:2002.07466v3 and the ICALP 2019
Caragiannis--Fanelli paper. Additional web searches included
`weighted congestion games "d/log d" "existence"` and
`weighted congestion games "sublinear" approximate equilibria 2024 2025 2026`.
They did not identify a later full-class sublinear existence theorem in
the returned results. This is a limited search scope, not certification
that no such paper exists or that these mechanism claims are novel.

The outstanding research target remains a full-class sublinear existence
mechanism. The boundary established here makes nonseparability, selected
improvement edges, or genuinely global state selection the remaining
routes within the considered potential framework.
