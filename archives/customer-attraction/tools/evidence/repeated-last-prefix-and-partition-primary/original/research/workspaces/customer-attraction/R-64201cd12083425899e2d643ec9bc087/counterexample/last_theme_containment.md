# Counterexample reduction by containment of the final theme

Status: self-contained candidate theorem, derived 2026-10-21; independent
review by the sibling `independent_attack` found the maximality clarification
below and agreed with the algebra. This is a sufficient structural condition for Q-CAG-HALF,
not a solution of its unrestricted case. The argument uses only the existing
CAG model and the definition of a full-history pure SPE.

Let `(S_1,...,S_m)` be the actual ordered outcome of any such SPE. Write
`B=S_m`, `u=u_m`, `W=|union_i S_i|`, and let `k` be the number of indices
`i` for which `B subseteq S_i`. In particular `1<=k<=m`. Equality of labels
is not required. **Maximality clarification:** the last-player best response
`B` is necessarily an inclusion maximal customer set: at the fixed last
prefix, a strict superset gives the same contribution on `B` plus a
strictly positive contribution on its nonempty difference. Therefore every
catalog set containing `B` equals `B`; `k` in an actual SPE is precisely
the number of actual copies of the same covered customer set. The
containment wording is a valid proof interface but provides no enlargement
over counting copies in this model.

**Claim.** For every integer `m>=1`,

\[
\operatorname{OPT}_m\le W+(m-1)u,
\qquad
W\ge \frac{k(2m-k)}m\,u.
\tag{1}
\]

Consequently, if `W>0`,

\[
\frac{\operatorname{OPT}_m}{W}
\le 1+\frac{m(m-1)}{k(2m-k)}.
\tag{2}
\]

In particular `(m-k)^2<=m` implies `OPT_m<=2W`. Thus a five-player
counterexample must have at most two actual themes containing the last
theme; a six-player counterexample must have at most three. Counting exact
copies of the final theme gives a weaker immediate corollary.

## Last-node bound and the exact tax identity

Let `c_x` be the final load and `d_x=c_x-1[x in B]` the load immediately
before the last move. Define the last-node tax

\[
\tau=\sum_{x:d_x>0}\frac{d_x}{d_x+1}.
\]

For any `m` comparison themes `T_1,...,T_m`, last-player optimality gives
`u(T_j | S_1,...,S_{m-1})<=u` for every `j`. Customerwise, their union size
is at most the sum of those `m` deviation payoffs plus `tau`: if a customer
is in `t>=1` comparison themes, its contribution on the right is
`t/(d_x+1)+d_x/(d_x+1)>=1`; customers absent from their union have a
nonnegative contribution. Maximizing the comparison union therefore gives

\[
\operatorname{OPT}_m\le m u+\tau.
\tag{3}
\]

There is also the exact identity

\[
\tau
=W-u-\sum_{x\in(\cup_i S_i)\setminus B}\frac1{c_x+1}
\le W-u.
\tag{4}
\]

Indeed, on `B`, the tax is `(c_x-1)/c_x=1-1/c_x` (including zero when
`c_x=1`); off `B` but in the actual union it is
`c_x/(c_x+1)=1-1/(c_x+1)`. Equations (3)--(4) give the first inequality
in (1). This is the same genuine last-node comparison used in existing tax
arguments; no early-player tax bridge is asserted.

## Paying the final player's profit from actual profits

Every actual player has `u_i>=|B|/m`: at that player's actual history,
deviating to the common catalog theme `B` would yield at least `1/m` from
each customer of `B`, whatever the real followers do. SPE optimality at
that actual history establishes the stated bound; no continuation is
frozen.

For each of the `k` players choosing a theme containing `B`, its actual
payoff is at least `u`, because it receives the same `1/c_x` contribution
from every `x in B` plus nonnegative contributions from other customers.
Moreover `c_x>=k` on `B`, so

\[
u=\sum_{x\in B}\frac1{c_x}\le |B|/k.
\]

Summing the `k` containment-player bounds and the `m-k` remaining common
theme deviation bounds yields

\[
W=\sum_i u_i
\ge k u+(m-k)|B|/m
\ge k u+(m-k)k u/m,
\]

which is the second inequality of (1). The condition for (2) to be at most
two is exactly

\[
k(2m-k)\ge m(m-1)
\Longleftrightarrow (m-k)^2\le m.
\]

## Boundaries and scope

No division by `u` is needed. If `u=0`, (1) already gives `OPT_m<=W`.
If `W=0`, the first bound implies `OPT_m=0`, so half coverage holds without
forming a ratio. Empty `B` is allowed: then all actual themes contain it,
so `k=m` and `u=0`. For `m=1`, (1) gives `OPT_1=W` and (2) gives one.
For `k=m`, (2) gives `2-1/m`, including the familiar all-big construction.
The proof uses actual chosen sets and their inclusion, with the last
action already maximal. Arbitrary history-dependent off-path ties remain
allowed.

## Exact verification

`last_theme_containment_audit.py` checks the per-customer identities with
`Fraction`, the equivalence of the integer threshold, the `m=1`, zero and
all-containment boundaries, and checks all actual ordered SPE outcomes of
selected seven- and eight-theme cascade games with the canonical exact
solver. Its finite checks audit the algebra and implementation; the proof
above establishes the quantified statement.
