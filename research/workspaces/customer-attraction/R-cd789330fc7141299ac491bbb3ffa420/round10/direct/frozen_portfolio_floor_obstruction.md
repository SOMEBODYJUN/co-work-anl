# An arbitrary frozen portfolio does not supply a static response floor

2026-10-24. This note disposes of exactly one named auxiliary statement used
in an attempted adaptive-portfolio proof. **Q-CAG-HALF and the actual-SPE
minimum-profit net ROW remain OPEN.** No finite search was used. The example
below is not asserted to be an SPE outcome, and does not furnish a target
counterexample.

Tree10 independently reconstructed the exact static value and checked the
scope in [its internal review](../tree/direct_static_floor_review.md).
This is an internal check only, with no novelty or external-review claim.

## Candidate and its intended use

For a full legal profile q of m themes, put t(q)=min_i u_i(q), and let

\[
\theta_m=\min_{B\in\mathcal S^{m-1}}
          \max_{T\in\mathcal S}\sum_{x\in T}\frac1{1+c_x(B)}.
\]

The candidate was

\[
t(q)\le\theta_m\qquad\text{for every legal full portfolio }q.\tag{FLOOR}
\]

If true, it would allow an arbitrary frozen portfolio's minimum return to be
used as a frozen best-response floor at every history of the same total
population. It would still not justify an adaptive individual floor: later
players observe the current action. FLOOR itself is false, before that
second issue arises.

## An arbitrary-player obstruction, with exact static value

For every m>=3 let the unit customers be 0,1,...,m-1. The common catalog
contains all m singletons and the m-1 star edges

\[
L_j=\{j\}\quad(0\le j<m),\qquad
E_j=\{0,j\}\quad(1\le j<m).
\]

The frozen portfolio q=(L_0,...,L_(m-1)) has every payoff equal to 1. Thus
t(q)=1. Take B=(E_1,...,E_(m-1)). Its center load is m-1 and each leaf load
is one. A leaf singleton has insertion return 1/2, the center singleton has
return 1/m, and every edge has insertion return

\[
\frac12+\frac1m.
\]

Consequently theta_m<=1/2+1/m<1.

For completeness this background is minimizing. If any leaf is uncovered by
a competing (m-1)-tuple, the corresponding edge query returns at least 1,
already more than 1/2+1/m. Otherwise each of the m-1 leaves is covered. Each
legal theme touches at most one leaf, so the m-1 competing themes touch each
leaf exactly once. Their center load k is at most m-1. Every edge query then
returns 1/2+1/(k+1)>=1/2+1/m. Hence

\[
\boxed{\theta_m=\frac12+\frac1m,\qquad t(q)=1.}\tag{STAR}
\]

The ratio t(q)/theta_m=2m/(m+2) tends to 2. Thus this static interface is not
merely missing a small uniform slack. Empty themes can be added without
changing the calculation; all instances already use finite common
catalogs and unit customers. These assertions are static only.

## Exact limitation

The portfolio q is not required by FLOOR to be an equilibrium, and the proof
above makes no such assertion. In particular it does not refute

* a floor that uses the actual minimum profit of a complete SPE;
* the true-query net ROW at an actual minimum-profit position;
* any positive whole-tree payment or the HALF target.

The failed step in the direct attempt was moving from a collection of
on-profile utilities to a floor against an unrelated static background.
Common catalog symmetry alone does not permit that transfer. A valid next
step must exploit complete-tree rationality or retain and pay the change of
background explicitly.

At m=5 the same general family gives t(q)=1 and theta_5=7/10, so it also
fails the requested substitution pressure test as an auxiliary floor. This
is an exact substitution into a general family, not a five-player project
or evidence against HALF.
