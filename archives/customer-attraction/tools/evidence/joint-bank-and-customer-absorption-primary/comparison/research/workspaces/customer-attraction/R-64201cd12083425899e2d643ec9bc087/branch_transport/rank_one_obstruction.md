# Individual full-history inequalities through one offpath departure do not give any constant welfare bound

Research checkpoint, 2026-10-21. This note gives a complete formal policy and
an exact obstruction to a specified *subset of the strategy-cone inequalities*.
The policy is **not an SPE**. This is not a counterexample to Q-CAG-HALF.
The proof is self-contained; the accompanying script checks arithmetic with
`Fraction` and does not call an optimizer or equilibrium solver. Independent
mathematical review has not yet been performed.

Version 1. The stronger arbitrary-cutoff version of the same construction is
in `fixed_rank_obstruction.md`; this file preserves the simpler rank-one proof.

## 1. Exact restriction being obstructed

Use the common-catalog, unit-customer, unit-provider sequential attraction
model. A complete formal pure policy `sigma` specifies an action at every
ordered history. It need not be an equilibrium. Define its departure rank by

\[
D_\sigma(h)=\#\{j:h_j\ne\sigma(h_1,\ldots,h_{j-1})\}.
\]

For each decision history `h` and every alternative `a`, let `Gamma[h,a]` be
the current player's payoff along the prescribed continuation minus its payoff
after choosing `a` and following the **same complete formal policy** thereafter.
Thus all rows keep the true continuation; no follower action is frozen.

The restriction studied here retains **every individual row** `Gamma[h,a]`
at every history with `D_sigma(h)<=1`. Each history and alternative may receive
its own arbitrary nonnegative multiplier. There is no node average, fixed
query distribution, fixed static kernel, or stationarity restriction.

**Theorem (rank-one strategy-cone obstruction).** For every `m>=1` there is a
finite disjoint common catalog, a finite unit-customer instance, and a complete
formal policy such that all these retained rows are nonnegative, while

\[
\frac{\operatorname{OPT}_m}{W}
=\frac{m}{\displaystyle\sum_{r=1}^m1/\lceil r/2\rceil}.
\tag{1}
\]

This ratio exceeds two exactly when `m>=9`, and tends to infinity. Consequently
there is no universal constant welfare bound derivable only from customer
nonnegativity and these rank-at-most-one incentive inequalities. In particular,
a universal half-coverage Farkas construction must, for some policies, use a
row at rank at least two, or introduce information beyond this row subsystem.

The quantifier is over formal policies and their restricted cones, not over
full SPE. The witness below violates an explicit omitted rank-two row.

## 2. Catalog and root path

Let

\[
L=\operatorname{lcm}(1,2,\ldots,\lceil m/2\rceil).
\]

Take `2m` pairwise disjoint themes `A_1,...,A_m,B_1,...,B_m`, with

\[
|A_i|=\frac{L}{\lceil(m-i+1)/2\rceil},\qquad |B_j|=L.
\tag{2}
\]

Every displayed size is an integer; every customer is a distinct unit customer
in exactly one theme. Every catalog theme has at most `L` customers. Selecting
the `m` big themes gives `OPT_m=mL`, and no `m` themes can cover more.

The actual path will be `A_1,...,A_m`. Therefore

\[
W=L\sum_{r=1}^m\frac1{\lceil r/2\rceil}.
\tag{3}
\]

Every theme size has the form `L/d` for a positive integer `d`.

## 3. Policy at every ordered history

Until a player departs from the root path, prescribe `A_i` to player `i`.
Suppose the first departure occurs at player `i`, choosing theme `T` of size
`L/d`. Set

\[
r=m-i+1,\qquad p=\#\{j<i:A_j=T\}\in\{0,1\},\qquad
q=\max\left\{p+1,\left\lfloor\frac{r+p+1}{d+1}\right\rfloor\right\}.
\tag{4}
\]

Prescribe another `q-p-1` consecutive copies of `T`, followed by distinct big
themes not previously selected, in increasing index order. This gives a
complete path after that first departure. There are enough fresh big themes:
the original prefix uses only reward themes and at most one big theme is the
first departure. Also `q-p-1<=r-1`, so the copying block fits.

If a second departure from this prescribed path ever occurs, prescribe the
last observed theme forever thereafter. Further departures merely change the
theme that subsequent players repeat. Equivalently: after the second departure,
`sigma(h)=h_last`. These rules define the policy at every ordered history,
including all histories of rank two or larger.

For any genuine alternative different from the prescribed action at a rank-one history with `s` players remaining, the
continuation after that alternative repeats it in every remaining position.
If its theme size is `z<=L` and its prefix count is `c`, the deviator's exact
payoff is therefore

\[
\frac{z}{c+s}\le\frac{L}{s}.
\tag{5}
\]

This is a property of the explicitly defined policy, not an assumption about
rational future behavior. Choosing the prescribed action instead gives the
identically zero incentive row and retains the rank-one continuation plan.

## 4. Every retained action inequality is valid

### Histories of rank zero

Fix player `i` on the root path and set `r=m-i+1`. Its actual payoff is
`L/ceil(r/2)`. A departure to a theme of size `L/d` leads to final count `q`
from (4), hence payoff `L/(dq)`.

The elementary integer inequality

\[
d\max\left\{1,\left\lfloor\frac{r+1}{d+1}\right\rfloor\right\}
\ge\lceil r/2\rceil
\tag{6}
\]

holds for every `d,r>=1`. Indeed, writing the maximum as `k`, we have
`r+1<(k+1)(d+1)`, so integrality gives

\[
r\le dk+d+k-1\le2dk,
\]

where the second inequality is `(d-1)(k-1)>=0`.
The `q` in (4) is at least the maximum in (6), since `p>=0`. Thus
`L/(dq)<=L/ceil(r/2)`, proving every rank-zero comparison.
Choosing the prescribed action itself gives the zero row and needs no special
continuation reinterpretation.

### Histories of rank one, within the copying block

Such a player chooses `T` and receives `L/(dq)`. If at least one extra copy
is prescribed, then `q>p+1`, so `q=floor((r+p+1)/(d+1))` and

\[
(d+1)q\le r+p+1.
\tag{7}
\]

The last extra copy has `s=r-(q-p-1)=r-q+p+1` players remaining.
Equation (7) gives `dq<=s`. Earlier extra copies have at least as many players
remaining. Thus every player in the copying block receives at least `L/s`,
which dominates every alternative payoff by (5).

### Histories of rank one, after the copying block

The prescribed theme is a fresh big theme, and no later prescribed action
uses it. Its payoff is `L`, which also dominates all alternatives in (5).
This exhausts every history of rank zero or one: after its unique first
departure, a rank-one history follows the specified first-departure plan.

## 5. Small explicit instance and omitted violation

At `m=9`, take `L=60`. The reward sizes, in actual order, are

\[
(12,15,15,20,20,30,30,60,60),
\]

and the nine disjoint big themes each have size 60. There are 802 distinct
unit customers and 18 themes. The exact values are

\[
W=262,\quad\operatorname{OPT}_9=540,\quad
\operatorname{OPT}_9-2W=16,\quad
\frac{\operatorname{OPT}_9}{W}=\frac{270}{131}.
\tag{8}
\]

This policy is visibly **not an SPE**. After first choosing `B_1`, its specified
plan starts with five copies of `B_1`. At history `(B_1,B_2)`, player two has
made the second departure, so the policy prescribes `B_2` to player three and
all later players. Player three obtains `60/8=15/2`. Deviating to `B_3` makes
all remaining players repeat `B_3`, giving `60/7`. The omitted row is

\[
\Gamma_{(B_1,B_2),B_3}=-15/14<0.
\tag{9}
\]

The history has departure rank two. For general `m>=3`, the analogous violation
has payoff difference `L/(m-1)-L/(m-2)<0`.

## 6. Exact dual obstruction and asymptotics

Fix this complete policy, and let `G_<=1` consist of all its individual
incentive rows at histories of rank at most one, expressed over all nonempty
customer-incidence types. Let `c` be root coverage and `o` the coverage of
the `m` big comparison themes. The actual disjoint-theme customer vector `w`
has nonnegative integer singleton-type coordinates. Sections 3–4 prove
`G_<=1 w>=0`. For `m>=9`, `(2c-o)w<0`.

Consequently no nonnegative multipliers `lambda` and nonnegative customer
residual `rho` satisfy

\[
2c-o=G_{\le1}^{\mathsf T}\lambda+\rho.
\tag{10}
\]

This follows just by taking the scalar product with `w`; arbitrary separately
weighted rows, duplication of rows, and arbitrary support selection do not
help. The same argument excludes every fixed constant `C` in place of two
for sufficiently large `m`.

For `m=2s`, the denominator in (1) is `2H_s`; for `m=2s-1`, it is
`2H_{s-1}+1/s`. The summands in (3) are nonincreasing, so their average is
nonincreasing and the ratio in (1) is nondecreasing. Direct exact values at
eight and nine players are `48/25<2` and `270/131>2`; hence nine is the first
violating player count **within this family**, not a minimality theorem over
all possible restricted policies. Finally `H_s<=1+log s` proves divergence of
the ratio.

## 7. Reproduction and continuation

Run from the repository root:

```sh
python research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/branch_transport/rank_one_obstruction.py --through 12
```

`rank_one_obstruction.py` is an executable exact description of the complete
policy. It enumerates precisely the rank-at-most-one decision histories,
checks every legal alternative by executing the policy to a terminal outcome,
and checks the omitted rank-two violation. It avoids enumerating the enormous
unrestricted tree, but it does not omit any constrained history. The frozen
output is `rank_one_audit.json`.

Open extension: prove or disprove an analogous obstruction for every fixed
departure-rank cutoff `k`, with player count allowed to grow. The present note
establishes only cutoff one. A claim for arbitrary fixed `k` would need a new
recursive construction; it is not implied by the logarithmic root welfare
in this family.
