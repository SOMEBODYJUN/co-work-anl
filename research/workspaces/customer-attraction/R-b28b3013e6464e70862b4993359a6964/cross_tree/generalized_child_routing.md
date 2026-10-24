# Arbitrary-child routing and the query-cover LP

**Status:** exact payment certificate interface, not a proof of Q-CAG-HALF. This note records a broadening of the increasing-role flow that is legal for the scalar IC accounting; it separates the true remaining row-load problem from an artificial restriction to old-branch coverers.

Fix an actual-prefix query state `s=(i,a,x)`, where `x` is an omitted comparison customer and `x in a`. Let `Z_i(a)` be the complete original-policy rollout after forcing `a`, and set

```
r_s(x) = 1 / (1 + |{ell>i : x in Z_i(a)_ell}|),
D_s = u_i(Z_i(a)),
```

so `r_s(x)` is exactly the x-contribution to the legal forced-query payoff `D_s`. If `f_s` units of pending x-flow arrive, absorb `f_s r_s(x)` and pass the remaining `f_s(1-r_s(x))` to **any** later state `(ell,b,x)` with `ell>i` and `b in S` containing x. The child need not be an action of a player that covered x in `Z_i(a)`. This is a valid scalar certificate: every state is still a real one-shot deviation from its own actual prefix, all indices strictly increase, and each customer’s source unit is absorbed exactly once by finite conservation. The child is a fresh legal query and its own coefficient is evaluated from its own rollout; no old continuation is transplanted as an equilibrium.

For nonuniform routing, define `rho_s=u_i/D_s`. The least cost per pending unit obeys the larger DAG dynamic program

```
V_s = rho_s*r_s(x) + (1-r_s(x)) min_{ell>i, b contains x} V_(ell,b,x),
```

with terminal rows automatically having `r_s=1`. This dominates the restricted recursion that only minimizes over old-branch future coverers. Choosing the minimum child is a proof-side routing decision, not an action or hidden mixed commitment by a player.

Equivalently, forgetting the flow decomposition gives a finite query-cover LP. For each legal actual-prefix query row `(i,a)` let `r_{i,a,x}` be the above coefficient and choose `w_{i,a}>=0`. If

```
Σ_(i,a: x in a) w_(i,a) r_(i,a,x) >= 1       for every x in R,
```

then summing the omitted-customer coordinates gives

```
|R| <= Σ_(i,a) w_(i,a) D_i(a) <= Σ_i (Σ_a w_(i,a)) u_i.
```

The flow is one constructive way to satisfy the covering inequalities without reusing a row; arbitrary-child routing shows that old-branch coverer edges are not logically needed for the scalar LP. The remaining general obligation is to choose the cover weights so that the row-load excess `Σ_i(L_i-1)u_i` is paid by the actual-only set `G` (or another already-accounted common budget). The source-fractional matching note gives `L_i^src<=1` for its initialization portion, but does not bound the incoming portion.

This broadening must not be confused with a stronger game claim. It does not freeze any continuation, does not assert that a route is a SPE, and does not provide a per-type Farkas certificate simultaneously for all customer multiplicities. It only enlarges the legal collection of one-shot IC rows used in a fixed-instance scalar cover.
