# 潜在用户密度填充：逐倍率保持均衡的投影与提升

Claim ID/version: **WC-R3-POTENTIAL-DENSITY-PADDING-v1**.

## Exact statement and model

Let G be any game in MODEL.md's class G_d, for any integer d>=0. For any
finite list of pairs (e,v), where e is an original resource and v>0, create
one new weight-v player per pair, with strategies empty and {e}. Leave all
original weights, strategies, and nonnegative-coefficient polynomials intact.
Call the resulting finite game G'.

For every finite real alpha>=1, projecting any alpha-PNE of G' onto the
original players yields an alpha-PNE of G. Original players' costs, including
all their unilateral deviation costs, agree under this projection. Every
alpha-PNE of G lifts to one of G' by putting all added players on empty.
Thus existence is equivalent, and the two games' best equilibrium factors
agree. There is no assumption that costs are strictly positive on all resources.

Quantifier order: for every G, every finite positive-weight padding list, and
every finite alpha>=1, both projection and lift properties hold. Padding does
not depend on alpha. The strategy and cost definitions are those of MODEL.md;
there is no player-specific latency or resource-dependent original weight.

## Proof

A nonzero nonnegative-coefficient polynomial c_e is strictly positive at
every x>0: at least one coefficient is positive, and each x^k is positive.
In any alpha-PNE of G', a new player using such an e would have current cost
c_e(x_e)>0 and the zero-cost deviation to empty. The inequality
c_e(x_e)<=alpha*0 is false for every finite alpha. Hence all added players
on nonzero resources choose empty.

Added players can remain on an identically zero resource. Their loads affect
no cost, both before and after any original player's deviation. The loads
on every nonzero resource therefore agree with the projected original state,
and all original current/deviation costs agree. All original approximate
equilibrium inequalities survive projection.

Conversely, an original alpha-PNE with all new players empty has exactly
the same original inequalities. Each new player has current cost zero and
nonnegative alternative cost, so its inequality holds. This proves the lift
and both implications, including zero games and empty original strategies.

## Consequence for minimum potential-user density

For a resource e, potential users are U_e={i: some original strategy contains e}.
Fix any integer L>=1. For each distinct weight v occurring in U_e, add enough
new (e,v) players to make its multiplicity among potential users of e at
least L. There are finitely many resources and weight values, so this is a
finite legal padding. A new player is a potential user even when it chooses
empty at every equilibrium.

For every real R>1 and every x>0, the resulting resource satisfies

    {i in U'_e: x<=w_i<Rx} nonempty
      => #{i in U'_e: x<=w_i<Rx} >= L.

The antecedent means an interval containing at least one potential user's
weight. It does not mean merely that the geometric interval is nonempty;
intervals beyond the finite weight spectrum have count zero. Every occupied
interval contains a whole weight class of multiplicity at least L. This
same padding works simultaneously for every R>1.

For fixed d,R,L, define D(d,R,L) to be the subset of G_d satisfying precisely
this occupied-interval minimum-count condition on each resource. The set of
finite factors guaranteed on every D(d,R,L) game equals the set guaranteed
on every G_d game: one inclusion is restriction to a subclass, and the other
applies any subclass guarantee to the padded version of any given G.
Consequently their universal thresholds, defined as infima, agree exactly.
No attainment of either infimum is assumed.

## What the reduction does and does not show

An upper bound based only on arbitrarily large **minimum potential-user
density** in occupied bands would already be a full-class upper bound.
This density condition does not isolate a simpler equilibrium-existence
class. It cannot supply active congestion without an additional argument.

This does not attack the sparse-spectrum condition that every interval
contains **at most** K potential users. Padding increases that K and respects
the distinction between upper and lower counts. It does not exclude methods
that preprocess dominated empty-choice players, use active loads, require
unavoidable participation, or impose a different substantive strategy condition.
The implication is a reduction, not a proof that a dense-class upper bound
is false. Exact Shapley-selector padding is a special application in
`../dense_bands/README.md`; this theorem preserves the whole equilibrium set
under projection rather than only a chosen potential minimizer.

The nonnegative polynomial assumption carries the strict-positivity step.
For general nondecreasing step latencies, cost-free positive load can mask an
original profitable deviation: one weight-1 player chooses a private cost 1/2
or a shared resource with c(x)=0 for x<=1 and c(x)=1 for x>1. Add a weight-1
empty/shared player. Original-private/new-shared is an exact equilibrium of
the augmented game, but its projection is not any finite-alpha equilibrium
of the original game. Thus the stronger projection assertion cannot be
silently imported to all nondecreasing costs.

## Status, evidence, and continuation

Dependencies: MODEL.md; strict positivity of a nonzero nonnegative polynomial;
the original cost inequality, including zero alternative costs. No external
theorem is imported. The step example is a boundary for the projection
assertion, not a counterexample to the polynomial result.

Evidence: [verify.py](../../../../tests/audits/weighted_congestion/density_padding/verify.py) checks exact costs, all unilateral deviations,
both projection/lift sets for several factors, zero resources, and degree-zero
and nonlinear inputs. [review.md](../../../reviews/weighted_congestion/density_padding/review.md) independently reconstructs the
proof; its separate checker supplies another implementation. Finite checks
are implementation evidence; the preceding proof carries all real-weight
and unbounded finite-size quantifiers.

Status: complete authored proof; independent review is tracked separately.
Truth: exact projection/lift reduction; value: a precise boundary on proposed
dense-band hypotheses; novelty: unassessed; mechanism: zero-cost escape and
strict polynomial positivity; ambition: full WC-TARGET remains OPEN.
Next obligation: identify an active-load or mandatory-participation condition
that a selection rule can maintain while controlling resources mixing scales.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
