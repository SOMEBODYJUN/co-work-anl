# Branch-cost LP dual for the mixed-owner budget (candidate interface)

2026-10-24. This note isolates the exact optimization problem left by the mixed-owner construction. It is a general-input representation, not a proof of Q-CAG-HALF.

Fix an actual root path of a complete pure SPE, an optimal comparison tuple, and the resulting sets `R=O\\C`, `C=I\\G`. For every player position `i` and legal topic `A`, let `z_{i,A}` be the terminal outcome after forcing `A` at the actual prefix and following the same complete strategy. Define

```
q_{i,A}
 = sum_{x in R intersect A} (c_{i,A}(x)-1)/c_{i,A}(x)
   - sum_{x in C intersect A} 1/c_{i,A}(x).
```

The first term is the response tax on root-uncovered optimal clients; the second is the common-client query credit. For a mixed owner plan `y`, rows satisfy `sum_A y_{i,A}=1`, and coverage requires `sum_{i,A:x in A} y_{i,A} >= 1` for each `x in R`. The sufficient condition from the mixed-owner derivation is

```
min_y sum_{i,A} q_{i,A} y_{i,A} <= |G|.
```

Indeed, `|R| <= |I|+|G| + Tax(y)-Q_C(y)`, so this inequality gives `|R| <= |I|+2|G|`.

## Exact dual

The primal is finite. Its dual is

```
maximize   sum_i alpha_i + sum_{x in R} beta_x
subject to alpha_i + sum_{x in R intersect A} beta_x <= q_{i,A}  for every (i,A),
           beta_x >= 0,
           alpha_i free.
```

Equivalently, after eliminating `alpha_i`, its value is

```
D = sup_{beta >= 0} [ sum_x beta_x
      + sum_i min_A ( q_{i,A} - sum_{x in R intersect A} beta_x ) ].
```

Thus the mixed-owner route closes exactly if every dual weight vector `beta` has `D <= |G|`. Any obstruction to the route must provide a valid `beta` and row-wise lower bounds on all branch costs; it is not enough to exhibit one expensive owner assignment or one fixed optimal tuple.

## What this dual adds

1. It separates the cross-tree difficulty from the already-proved customer accounting. `q` is the only branch object containing the real off-path continuations; `beta` prices simultaneous coverage of the same omitted client across independent deviations.
2. A putative proof via dynamic Farkas/flow must show that branch IC forces `D <= |G|`. A static max-flow certificate only proves primal feasibility and cannot control `q`.
3. A putative counterexample to this interface must make `D>|G|` for every selected optimal tuple and every complete SPE, while still respecting all off-path best responses. One row or one owner choice is insufficient.
4. If `G=0`, the criterion reduces to `D<=0`; negative query credits from actual-optimal intersection must pay all positive response tax. This makes clear why a root-only source bound cannot be iterated for free: a dual `beta` can price the same `R` client at several rows.

No general inequality `D<=|G|` has been proved here. The Q-CAG-HALF target remains OPEN.
