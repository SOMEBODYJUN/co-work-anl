# Dual LP route: branch-coverer decomposition (candidate / open)

Scope: general finite common directory, arbitrary `m`, all-history pure SPE. This is a personal research note, not a proved Q-CAG-HALF theorem.

## Fixed notation

Fix a complete pure SPE `sigma`, actual root topic `a0`, and a client type `B` with `B` disjoint from every topic on the actual root path (so its actual coverage coefficient is zero). For a root deviation to a topic `t in B`, write the resulting full `sigma` branch as `z(t)`. Let

`k_B(t) = |{j: z(t)_j in B}| >= 1`.

For every future history `h=(t,a_2,...,a_{i-1})` on this branch at which the prescribed action `a_i` lies in `B`, use the exact SPE row comparing `a_i` with the actual root topic `a0`:

`Gamma_{h,a0} = payoff(type, a_i on z(h)) - payoff(type, a0 on z(h,a0))`.

Because `a0 notin B`, the `B`-coordinate of the second term is zero. The `B`-coordinate of every selected row is `1/k_B(t)`. There are exactly `k_B(t)-1` selected future actions in `B`, hence

`sum_{h on branch t, a_i in B} Gamma_{h,a0}[B] = (k_B(t)-1)/k_B(t)`.

This is an exact coordinate identity; it uses only legal full-history SPE rows and does not freeze a continuation.

## Consequence for the target dual

The target coefficient for an uncovered type is `(2c-o)[B] = -1` whenever `B` occurs in the comparison optimum. The selected off-path rows leave a residual deficit exactly `1/k_B(t)` on `B` (if one instead also includes the root row `Gamma_{empty,t}`, its `B` coefficient is `-1/k_B(t)` and the deficit is `2/k_B(t)`). Thus the only unresolved payment is a branch-specific `1/k` (or `2/k` with the root row) for each optimal-uncovered type. For `k=1`, the root deviation row is the only available branch row and its positive coordinates on root-covered types must pay the deficit.

The rows' coordinates on other types can be negative, so summing this identity over client types is not automatically a dual certificate. A successful aggregation must choose root alternatives / fractional optimal cover weights so that the total negative spillover on root-covered types is at most their target budget `2c[B]`. This is the concrete remaining LP obstruction, rather than an undefined “future response” issue.

## Relation to existing conic dual

For fixed `sigma` and comparison union `J`, the exact cone is `D_sigma={r>=0:Gamma_sigma r>=0}`. Farkas says that proving `2 c - o >= 0` on `D_sigma` is equivalent to constructing nonnegative multipliers `lambda` with `2c-o = Gamma^T lambda + eta`, `eta>=0`. The branch-coverer rows above provide a canonical sparse family of candidate multipliers. No universal aggregation bound is proved here.

## Why this is useful

It isolates the dynamic part in a finite, auditable identity: every uncovered type's root deviation deficit is reduced from one unit to a residual reciprocal of the number of branch coverers by legal off-path IC rows. Any future proof can focus on bounding the cross-type spillover of these rows, and any counterexample to that aggregation can be searched as a linear certificate failure.
