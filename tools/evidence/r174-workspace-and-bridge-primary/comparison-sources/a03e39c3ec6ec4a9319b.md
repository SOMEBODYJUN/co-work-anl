# Complete pair-incidence stress test for the routed incidence LP

**Status (2026-10-24):** rigorous obstruction to one specific proof interface; not a Q-CAG-HALF counterexample. It shows that the maximal-incidence LP / one-deviation budget cannot by itself close the general half bound, even when the comparison is made with `OPT_m` rather than the union of all maximal sets.

## Construction

Fix integers `s >= m >= 2`. Let the customers be one unit customer `x_{jk}` for each unordered pair `1 <= j < k <= s`. Let the common catalogue consist of the `s` maximal themes

\[
B_j=\{x_{jk}: k\ne j\},\qquad j=1,\ldots,s.
\]

There are no private customers and no other themes. The maximal-incidence hypergraph is the complete graph `K_s`; every customer has incidence exactly `{j,k}`. The maximum union of `m` catalogue themes is obtained by choosing `m` vertices and equals

\[
\operatorname{OPT}_m = {s\choose 2}-{s-m\choose 2}
 = m s - \frac{m(m+1)}2.
\tag{1}
\]

(For `m=s`, this is all `s(s-1)/2` customers.)

## Exact LP budget at the root

At the empty prefix the routed deviation lower bound used by the incidence-LP proof assigns `p_j=0` and `r=m`. For every maximal theme,

\[
f_j(0,m)=\sum_{k\ne j}\frac1m=\frac{s-1}{m}.
\tag{2}
\]

The incidence LP has one constraint `\beta_j+\beta_k\ge m` for every edge `{j,k}`. By summing all `s(s-1)/2` constraints,
`(s-1)\sum_j\beta_j\ge m s(s-1)/2`, so `\sum_j\beta_j\ge ms/2`; equality is attained by `\beta_j=m/2`. Thus

\[
B(m)=\frac{ms}{2},
\qquad D_0=B(m),
\qquad D_0\max_j f_j(0,m)=\frac{s(s-1)}2.
\tag{3}
\]

The last quantity is the union of all `s` maximal themes, so (3) is tight for the LP's root counting inequality. It does not exploit that only `m` themes are available in `OPT_m`.

## Why this is a genuine interface obstruction

To obtain a half bound from a root certificate of the form
`OPT_m <= 2 D_0 max_j f_j(0,m)`, (2) would give only

\[
2D_0\max_j f_j(0,m)=s(s-1),
\]

whereas (1) is `m s - m(m+1)/2`. For example, with `s=4m` the ratio of (1) to this doubled root credit tends to `7/32`, and with `s\gg m` it is asymptotic to `m/s`; more directly, the root LP credit is independent of the fact that the optimum can use only `m` vertices. If one instead asks the one-step form `OPT_m\le 2m\max_j f_j(0,m)`, its right side is `2(s-1)`, while (1) is order `ms`; this fails by an order-`m` factor whenever `s\gg m`.

Thus the failure is not a numerical weakness of a chosen feasible `\beta`: the complete-graph dual certificate forces `B(m)=ms/2`. Any proof that only (i) routes each action to one maximal theme, (ii) bounds a current deviation by `f_j`, and (iii) pays all uncovered comparison customers through a single nonnegative incidence-LP multiplier vector must introduce a second mechanism. Candidate mechanisms are cross-branch continuation credit, pair-edge load balancing, or a direct comparison that uses the `m`-theme cap in (1).

## Scope and non-claims

This catalogue is not asserted to have a low-welfare SPE; no complete SPE or target counterexample is constructed here. The calculation only rules out the stated one-deviation incidence-LP template as a stand-alone proof of Q-CAG-HALF. It complements the existing observation that the same LP has `B(r)=sr/2` on complete pair incidence. The obstruction survives replacing the global maximal union `U` by the exact `m`-theme optimum in the attempted root inequality.
