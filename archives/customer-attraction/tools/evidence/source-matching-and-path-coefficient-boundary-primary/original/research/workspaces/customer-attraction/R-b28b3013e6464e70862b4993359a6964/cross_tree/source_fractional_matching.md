# Fractional source matching for the recursive capture flow

**Status:** exact construction / candidate interface; not a Q-CAG-HALF proof.  This note isolates a source-side improvement that is compatible with full ordered-history SPE rows and does not introduce a hidden mixed strategy.

Fix a complete pure SPE path and an optimal comparison tuple `T_1,...,T_m`, with `O=union T_j`, actual union `C`, omitted set `R=O\\C`. Choose an owner partition `Q_1\\dotcup...\\dotcup Q_m=O`, `Q_j subset T_j`. For a role permutation `pi`, initialize one unit of flow for each `x in Q_j\\cap R` at state `(pi(j), T_j, x)`, then use the legal increasing-role capture flow and the scalar payment `w_s=A_s/D_s` at every query state. Every source assignment uses a single actual-prefix forced query and the same original continuation policy; no player randomizes.

Instead of one fixed permutation, average these valid certificates uniformly over all `m!` permutations. Equivalently use the doubly stochastic source matrix `q_{s,j}=1/m`: each customer `x in Q_j` supplies mass `1/m` to each role `s` at the state `(s,T_j,x)`, and source mass remains exactly one after summing roles. The averaging is only a convex combination of proof certificates; it does not modify the game or assert a mixed SPE.

For a source state `(s,T_j,x)`, let `Z_s(T_j)` be the complete original-strategy rollout from the actual prefix before role `s` with `T_j` forced. Since `x in R`, no earlier actual player covers `x`; write `c_x=1+number{ell>s:x in Z_s(T_j)_ell}`. Let `D_s(T_j)` be role `s`'s total payoff in that rollout. Its contribution from all omitted customers in `T_j` is `sum_{y in T_j\\cap R} 1/c_y`, which includes the owner subset. Thus

```
A^src_{s,j} = (1/m) sum_{x in Q_j\\cap R} 1/c_x
             <= D_s(T_j)/m.
```

Consequently the one-row scalar source coefficient satisfies

```
w^src_{s,j}=A^src_{s,j}/D_s(T_j) <= 1/m,
```
with the zero denominator convention from the general flow note. For each role `s`, summing over all owner themes gives

```
L_s^src = sum_j w^src_{s,j} <= 1.
```

This improves the fixed-owner construction: every role has source load at most one simultaneously, while each source customer is still supplied exactly once. The proof uses only nonnegativity of the forced-row payoff and the owner partition, and survives duplicate/empty themes and arbitrary ties.

The result does **not** bound the incoming reset load `L_s^in`. After source averaging, a customer can enter several future rows through different forced leaves; the existing hit bound controls per-row probability but not the sum of `A/D` across distinct themes. Any completion must pay `L_s^in` from the same actual prefix IC budget; adding source and incoming budgets independently would double count.

A small exact enumeration (all size-3 directories over `n<=3` clients, `m=3`, all generated pure-SPE continuation trees, all optimal tuples) found no violation of the stronger numerical candidate `C_opt <= W+|C\\O|` when deterministic permutations and the nonuniform minimum-cost child routing were optimized. This is diagnostic only and is not evidence for the general claim.
