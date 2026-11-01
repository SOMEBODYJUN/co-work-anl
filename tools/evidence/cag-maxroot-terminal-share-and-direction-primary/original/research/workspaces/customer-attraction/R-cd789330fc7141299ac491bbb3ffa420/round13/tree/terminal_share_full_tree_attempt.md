# Terminal-share budget: scope, exact obstruction and handoff

2026-10-25, tree13. Original HALF5 remains **OPEN**. No statement below is
an original-game counterexample to HALF5 or a new unconditional upper bound.

## 1. The candidate and the restored prior failure

For actual payoff vector `(u_1,...,u_m)` and `W=sum_i u_i`, the aggregate
candidate was

    C2: 2W >= (m+1) u_m; for m=5, W >= 3u_5.

It was subsequently located as an already OPEN candidate in
`R-18e993ca519949aba29e030d3d7b15b3/counterexample/mechanism_scan/harmonic_payoff_cap.md`.
The stronger C1, `2u_i>=u_m` for every early i, is already FALSE:
`R-18e993ca519949aba29e030d3d7b15b3/next_boss/terminal_clone_counterexample.md`
has a three-player four-theme seven-unit-client complete SPE with payoff
`(3/2,2,7/2)`. It violates C1 and attains equality in C2. That prior exact
counterexample supersedes this branch's earlier unsuccessful small cone QA.
Neither candidate should be promoted on the basis of that QA.

A possible implication of C2, conditional on proving it, is this: if every
actually omitted client in one optimal five-tuple belongs to at least two
of its five themes, actual last-player IC gives `5u_5>=2D`, where D is the
number omitted. C2 would give `D<=5W/6` and hence HALF5 for that class. This
is only a conditional use of an unproved candidate, not a theorem obtained
here. It does not handle the general mixed incidence class.

## 2. A precisely specified two-path necessary relaxation

Write the actual path as `(A_0,...,A_(m-1))`. Keep one genuine-root-deviation
name tuple

    z=(A_(m-1),Q_1,...,Q_(m-1)).

There are `2m-1` formal theme names. For each nonempty membership type B of
these names introduce nonnegative client mass r_B. Normalize actual welfare
to one. Include all of the following valid necessary rows:

1. At every actual role i and for every named theme T, actual payoff is at
   least `sum_(x in T) 1/(b_actual_i(x)+m-i)`.
2. At every future role i>=1 of z and for every named T, the source role's
   terminal payoff is at least the analogous conservative denominator sum.
3. Actual root payoff is at least the entering payoff in the exact z tuple.

For real complete SPEs these rows are necessary, irrespective of coincidences
among names or full-history ties. They do not impose all source child-SPE
conditions. `terminal_share_symbolic.py` constructs every row coefficient
for all `2^(2m-1)-1` customer membership types. Maximizing actual final-player
share over this relaxation is therefore an all-atom algebraic-template test,
not a catalog-instance census and not a full-tree SPE optimization.

## 3. Exact five-provider relaxation witness

The exact feasible point in `root_source_relaxation_exact.json` has normalized
actual payoffs

    (610818,701391,935188,1402782,2805564) / 6455743.

Thus every named necessary row is nonnegative, actual welfare equals one,
but

    6u_5-2W = 3921898/6455743 > 0.

This proves only that the named rows cannot imply C2. It does not refute C2.
The record includes a nonnegative integer-unit-customer instance obtained by
clearing denominators; no signed or non-unit provider weights are used.

The stronger full-tree information kills this point already at local
last-two tails. With the integer multiplicities in the record:

| Candidate local tail | Current payoff | Exact M at its prefix |
| --- | ---: | ---: |
| actual prefix (0,1,2), proposed next action 3 | 1,402,782 | 1,593,822 |
| source prefix (4,5,6), proposed next action 7 | 818,178 | 1,338,882 |

Both proposed tail endpoints fail the required current payoff >= M.
The M values use the exact all-SPE endpoint characterization; only these
two-player local tails are computed. This is enough to reject the proposed
local continuations and is not a global search or a target counterexample
certification. A three-player analogue is retained in the same JSON for
simple inspection: W=253, actual payoff `(49,68,136)`, source payoff
`(49,52,65)`, and the two actual/source thresholds are 79>68 and 84>52.

`audit_root_source_relaxation.py` recovers an exact rational feasible vertex,
checks every nonnegative row with Fraction, clears denominators, and
recomputes the two local thresholds. Floating optimality is not needed for
the claimed failure: one exact violating feasible point is sufficient.

## 4. Actual stop

A single root source with robust denominator IC misses even last-two
credible-tail constraints; it cannot close the terminal aggregate route.
The existing indexed five-player frontier already uses substantially
stronger genuine tail information, so the witness above is not advertised
as a cut against the 437/557/728 bad points. The attempt did not establish
C2, exclude a genuine bad HALF5 endpoint, or produce a feasible bad endpoint.

For cross-query capacity, a teleportation law was proposed to exchange13:
`p=(r+pT)/2`, with r maximizing the appropriate row potential. It supplies
arrival domination by `2p` and a favorable signed potential drift, but
requires a query law compatible with the actual same shadow/source bank.
The exact drift lemma and its limitations are maintained in exchange13's
`source_capacity_two_interface.md`. Replacing the common query by rowwise
laws introduces input-price debt and, if the old shadow center is retained,
a nonzero endpoint-centering term. Neither term is free money. No common
Cov-to-HALF-R source-capacity construction was completed here.
