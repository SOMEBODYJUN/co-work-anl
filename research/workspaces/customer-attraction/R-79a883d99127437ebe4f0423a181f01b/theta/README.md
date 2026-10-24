# Dynamic Theta: independent witness cones and the remaining budget

Status (2026-10-24): **general representation lemma; no new covering
inequality; no counterexample to TB, TB-ANY, SM, or Q-CAG-HALF.** This is a
personal research backup, not a promotion of the main claim.

The exact model is the common finite catalogue, arbitrary provider count,
unit clients/providers, and every full ordered-history pure SPE. Empty topics
and repeated choices are allowed throughout.

## Precise definitions

At any fixed legal prefix `h`, the current player has one action left and
future providers play a complete local pure SPE. Put

```
L_h(A) = min_{z in SPE terminal outcomes after (h,A)} u_current(z),
Theta(h) = max_A L_h(A).
```

These are local subgame continuations, not continuations required to extend a
previously fixed ancestor strategy. All minima/maxima exist in the finite tree.

For an actual complete SPE `sigma`, let `a` be its actual ordered path,
`h_i=a[:i]`, and `W(a)` its final coverage. The proposed bridge remains

```
TB:     W(a) + sum_i Theta(h_i) >= OPT_m.
```

TB-ANY makes the same assertion for every legal path `a`, without requiring
that path to be SPE-realizable. Only TB would be used with
`sum_i Theta(h_i) <= W(a)` to prove the main half-coverage claim.

## General representation lemma: exact minimum leader payoff

Let `E(h)` be all complete local pure SPEs of the subgame at `h`. Then

```
Theta(h) = min_{tau in E(h)} u_current(outcome(tau)).              (1)
```

For the lower bound, a local SPE's chosen payoff is at least the payoff from
each alternative action followed by that SPE's continuation, and the latter
is at least `L_h(A)`. Thus every local-SPE leader payoff is at least `Theta(h)`.

For attainment, choose `A*` maximizing `L_h(A)`. At child `(h,A*)`, choose a
local SPE attaining its minimum payoff `L_h(A*)=Theta(h)`. At every other child
`(h,A)`, independently choose a local SPE attaining `L_h(A)<=Theta(h)`.
Prescribe `A*` at `h`. Its chosen payoff weakly dominates every alternative,
and all child continuations are themselves SPEs. This is a complete local
SPE attaining equality in (1). Equalities, empty topics and all-zero instances
cause no difficulty.

This lemma is already implicit in the exact set-valued Bellman recurrence.
It is a representation fact, not a lower bound involving OPT.

## Independent witnesses give an exact multi-cone formulation

Fix a legal ordered path `a`. For each `i`, independently choose a local SPE
`tau_i` at `h_i=a[:i]` and denote its leader payoff by `v_i`. Equation (1)
gives the exact equivalence

```
W(a)+sum_i Theta(h_i) >= OPT_m
 iff
W(a)+sum_i v_i >= OPT_m for every independent family (tau_i).   (2)
```

The forward direction uses `v_i>=Theta(h_i)`. For the reverse direction choose
one minimizing local SPE separately at each `h_i`. The witnesses need not
agree at nested histories. Requiring their strategies to glue into one full
SPE would shrink the family and invalidate the equivalence.

For a fixed actual complete strategy `sigma`, a fixed family `(tau_i)`, and
a fixed comparison tuple `T`, all relevant conditions are rational linear
inequalities in the nonnegative integer client-type multiplicities `r_B`:

* Every SPE comparison has the form
  `sum_B r_B (1_{a in B}/c_B(z)-1_{b in B}/c_B(z')) >= 0`.
* The proposed budget has the linear form
  `W(a)+sum_i v_i-coverage(T)`.

Thus a negative point in the intersection of the actual full-SPE cone and
all the independent local-witness SPE cones refutes TB. A comparison tuple
need not remain optimal under varying multiplicities: its coverage already
lower-bounds the new `OPT_m`. If the actual full-SPE cone is omitted, the
same argument attacks TB-ANY only.

Conversely, every TB counterexample has such a finite multi-cone witness:
take its actual full SPE, independent minimizers from (1), and an optimal
comparison tuple. This is an exact reformulation, not a Farkas proof. A
single fixed strategy cone cannot replace the independent witness cones.

The analogous SM test fixes a forced comparison action at each `h_i` and
uses only a local SPE below that forced-action child. It must retain the
whole forced player's payoff. For a test of SM-opt-exists, a negative result
for one permutation is insufficient; all optimal assignments must fail.

## Rational witness reduction

The same formulation permits real nonnegative type masses as a search
relaxation without losing strict counterexamples. For fixed strategy
witnesses the SPE constraints are homogeneous rational weak inequalities,
and a strict negative budget is a rational strict inequality. A nonempty
rational polyhedron with a strict feasible inequality contains a rational
feasible point. Scaling a rational point by a common denominator gives
nonnegative integer client-type multiplicities and preserves every SPE
comparison and the strict violation. This preserves unit clients; it does
not introduce weighted providers. The argument also preserves tie faces
because they remain explicit linear constraints.

This is a completeness statement for a fixed finite witness architecture,
not an efficient algorithm and not a finite bound on arbitrary `m` or the
catalogue size.

## Analytic POP consequence and failed local inference

Write `Theta_r(empty)` for the minimum first-player payoff in the `r`-provider
game on the same nonempty catalogue. Adding the empty topic does not change
this value when some client is coverable: choosing the empty topic gives
zero, while any nonempty topic guarantees positive payoff. If no client is
coverable, all quantities are zero. Consequently TB-ANY, applied to the path
of `m` empty choices, would imply

```
POP: sum_{r=1}^m Theta_r(empty) >= OPT_m.                         (3)
```

POP uses dynamic local-SPE leader values. Replacing them by static
nonobserving-query security values changes the assertion. For example,
`A={1,2}`, `C={3,4}`, `B={1,3}` has static values summing to `7/2` for one
and two providers, while `OPT_2=4`; the dynamic two-provider leader minimum
is 2, giving dynamic sum 4. This example is an explanation of the dynamic
distinction, not a new fixed-size research project.

The known `root_tax_failure.json` has dynamic root values
`(30,15,13,9)` for horizons 1--4 and optimal values `(30,41,51,61)`.
The last local marginal fails (`9 < 61-51`), while the cumulative dynamic
sum is `67 >= 61`. Thus POP/TB-ANY cannot be proved by asserting each
dynamic root value pays its own optimal marginal.

## What was attempted and what remains unproved

The scripts below implement explicit attacks on the stated bridges. They
did not produce a negative exact witness. Their finite nonnegative outputs
are not mathematical assets establishing any universal inequality; no
sample count is used as evidence for the general claim.

* `attack_tb_any.py`: exact Bellman minimization of `W+sum Theta` over
  unrestricted paths, using the full set-valued local-SPE recurrence.
* `multicone_attack.py`: joint strategy-cone LP attack, with separate
  independent local-SPE witnesses. Its result carries an explicit `TB` or
  `TB-ANY` mode. A negative float proposal is not reported as a counterexample
  until rational reconstruction, all exact cone checks, recomputed dynamic
  thresholds, and (in TB mode) actual-path SPE membership pass.
* `population_cones.py`: the necessary POP consequence, using independent
  minimum-leader SPE witnesses for each horizon. A directed test of the
  known root-tax witness cone also gave no negative exact point.

The genuine missing step is an inequality linking these independent local
SPE witnesses to a single actual coverage budget. The local SPE inequalities
justify each witness but do not identify different witness terminal leaves,
equate their inventories, or allow their follower utilities to be charged
to actual `W` more than once. Neither (1), (2), the rational reduction, nor
the absence of a proposed negative point proves this missing inequality.

The main target remains **OPEN**. TB, TB-ANY, POP, and the SM sufficient
bridges remain unproved and unrefuted in this note.
