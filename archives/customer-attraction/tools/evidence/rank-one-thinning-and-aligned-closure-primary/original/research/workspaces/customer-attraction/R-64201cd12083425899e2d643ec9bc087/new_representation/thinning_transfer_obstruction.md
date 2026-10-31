# Harmonic utilities do not transfer SPE to a thinning component

Status: self-contained candidate obstruction with exact independent arithmetic
below; no external review or novelty claim. This is not a counterexample to
Q-CAG-HALF. It blocks a particular transfer step in an integral representation.
The standard quadrature fact in Section 5 is included only as a boundary.

## 1. Exact model and representation

Let N be finite, S a finite nonempty common catalog of subsets of N, and m≥1.
Players choose once in order, observing all previous actions. For terminal
s=(S_1,...,S_m), let c_x=|{i:x∈S_i}| and

    u_i(s)=Σ_(x∈S_i) 1/c_x,       W(s)=|∪_i S_i|=Σ_i u_i(s).

A complete pure SPE specifies an action at every ordered history and maximizes
the current player's terminal utility against the specified successor strategy.
Histories with identical counts may have unrelated tie choices.

For t∈[0,1], define the component terminal utility

    K_i(t;s)=Σ_(x∈S_i) t^(c_x−1),       0^0:=1.

It is the expected number of i's customers surviving when each other provider
covering a customer is independently retained with probability 1−t: i receives
a customer's unit precisely if no other covering provider is retained.
Equivalently, choose independent provider priorities U_j uniform on [0,1].
Conditional on U_i=1−t, the probability that i precedes every other coverer is
t^(c_x−1). The same priorities may couple all customers; expectation is enough.

The pointwise payoff identity is

    u_i(s)=∫_0^1 K_i(t;s) dt.

For any specified strategy σ, a harmonic SPE constraint is therefore the
nonnegativity of the integral of its true deviation polynomial. It does not
assert that this polynomial is nonnegative at any fixed common t.

## 2. A 13-customer complete SPE with no common component parameter

There are three players and four themes A,B,C,D. Customer types and integer
multiplicities are:

| Accepted themes | Number of distinct unit customers |
|---|---:|
| A,B | 2 |
| C | 2 |
| A,C | 1 |
| A,B,C | 3 |
| D | 2 |
| B,D | 3 |

Thus |N|=13. The full strategy is the following. The table lists the current
player's four terminal harmonic payoffs when choosing A,B,C,D at that history
and then executing this same specified strategy. The designated action reaches
the row maximum in all 21 histories.

| History | Action | Choose A | Choose B | Choose C | Choose D |
|---|---|---:|---:|---:|---:|
| empty | B | 5/2 | 5 | 9/2 | 7/2 |
| A | B | 3 | 5 | 7/2 | 7/2 |
| B | C | 5/2 | 7/2 | 9/2 | 7/2 |
| C | B | 5/2 | 5 | 5/2 | 7/2 |
| D | B | 7/2 | 5 | 9/2 | 5/2 |
| AA | D | 2 | 14/3 | 10/3 | 5 |
| AB | C | 13/6 | 19/6 | 7/2 | 7/2 |
| AC | B | 7/3 | 5 | 7/3 | 5 |
| AD | B | 3 | 4 | 4 | 5/2 |
| BA | C | 13/6 | 19/6 | 7/2 | 7/2 |
| BB | C | 8/3 | 8/3 | 4 | 3 |
| BC | D | 5/2 | 7/2 | 5/2 | 7/2 |
| BD | C | 7/2 | 7/2 | 9/2 | 2 |
| CA | B | 7/3 | 5 | 7/3 | 5 |
| CB | D | 5/2 | 7/2 | 5/2 | 7/2 |
| CC | B | 10/3 | 6 | 2 | 5 |
| CD | B | 4 | 5 | 3 | 5/2 |
| DA | B | 3 | 4 | 4 | 5/2 |
| DB | C | 7/2 | 7/2 | 9/2 | 2 |
| DC | B | 4 | 5 | 3 | 5/2 |
| DD | C | 6 | 6 | 6 | 5/3 |

This verifies the complete harmonic SPE directly by backward induction.
Its root path is B,C,D, with payoffs (5,9/2,7/2), and W=OPT_3=13.
It satisfies half coverage with wide slack.

Now retain exactly this full strategy but evaluate component payoffs K(t).
Three actual last-node comparison slacks are:

| History | Chosen action vs deviation | Component slack |
|---|---|---|
| BA | C vs D | 3t²−2t |
| DA | B vs C | 4t−2 |
| DD | C vs B | 1−3t² |

All three integrate to zero on [0,1], agreeing with the harmonic ties in the
full table. For a component SPE, the second comparison forces t≥1/2. The first
then forces t≥2/3. The third forces t≤1/√3. These are incompatible, since
(2/3)²=4/9>1/3. In particular no t∈[0,1] makes this σ a component SPE.
This excludes choosing a common component parameter even after seeing the
entire instance and full harmonic equilibrium.

The rows are true deviations at their own ordered histories. No successor
is frozen from a different branch, and no count histories are identified.

## 3. Unbounded-player version with a fixed five-theme catalog

For every m≥3, add the empty theme E=∅ to the same customer system. Consider the
legal ordered prefix h*=E^(m−3). It has zero customer loads and exactly three
players remaining. Graft the preceding three-player strategy into the subtree
below h* whenever subsequent actions belong to {A,B,C,D}. At any such node an
E deviation has payoff zero, while the table's selected payoff is positive.
Fill subtrees whose next action is E with arbitrary pure SPEs; finite backward
induction guarantees existence. This extends the displayed three-player SPE
to an SPE of the entire subgame below h*.

To extend it to the whole m-player game, keep that subgame fixed, fill every
other same-depth subtree with an arbitrary SPE, then work backward, choosing
an optimal action at every preceding node. Descendant SPE constraints do not
change when an ancestor action is selected. This produces a complete pure SPE
of the root game. Arbitrary history-dependent continuation choices are allowed
by the model, so another prefix with the same counts causes no restriction.

At the three histories h*BA, h*DA, h*DD, the same three polynomials occur.
Consequently this complete m-player harmonic SPE fails to be an SPE of every
component game K(t), for every t∈[0,1]. The obstruction applies to unbounded m
with only five catalog themes and 13 unit customers. No claim is made about the
root equilibrium path after this extension, or the worst welfare of the enlarged
game. These statements are unnecessary for the transfer obstruction.

## 4. A second, simple uniform-in-m boundary

Fix any finite set T⊂[0,1). For sufficiently large m, one full harmonic SPE can
fail component best response for every t∈T already at its root.

Take a big disjoint theme with m unit customers and m−1 additional disjoint
single-customer themes. Prescribe the big theme after every ordered history.
At a prefix with b previous big choices and r remaining players, choosing big
has harmonic utility m/(b+r)≥1. Any singleton deviation gives at most 1, even
when later players all choose big. Thus this is a complete pure harmonic SPE.
At the root, its component utility is m t^(m−1), versus 1 for a singleton.
For t_max=max T<1, m t_max^(m−1) tends to zero, proving the assertion. If T is
empty there is nothing to prove. This family has W=m and OPT_m=2m−1, so it
approaches, but never violates, the target factor two.

## 5. Positive quadrature boundary (standard moment argument)

Suppose an atomic nonnegative measure ν supported on L points of [0,1] obeys

    ∫ t^(c−1) dν(t)=1/c,       c=1,...,m.

Then L≥ceil(m/2). Indeed if 2L≤m−1, the polynomial P(t)=∏_(z∈supp ν)(t−z) has
P² of degree ≤m−1. Moment equality would give

    0=∫ P² dν=∫_0^1 P(t)² dt>0,

a contradiction. The bound concerns exact positive atomic representation of
all reciprocal shares up to load m, not arbitrary non-atomic decompositions.
It does not say a growing quadrature is unusable. Matching every c≥1 forces
ν to equal uniform Lebesgue measure, since polynomial moments determine a
finite measure on compact [0,1]. This last uniqueness is standard and follows
from polynomial density in continuous functions.

## 6. What is and is not ruled out

Ruled out: transferring a complete harmonic SPE to a single component game,
proving all component games' equilibrium bounds and applying them to that same
strategy without another argument, or representing all loads with a fixed-size
positive atomic quadrature independent of m.

Not ruled out: integrating signed component slacks before aggregating them,
using component parameters with different multipliers and exact compensation,
choosing different component equilibria, or a direct proof of Q-CAG-HALF.
The counterexample is an obstruction to an implication, not a theorem that
integral representations are useless.

Dependencies: elementary integral ∫_0^1t^kdt=1/(k+1), finite backward induction,
and the displayed unit-customer instance/strategy. Section 5 additionally uses
the standard polynomial moment argument and polynomial density. No literature
or repository theorem beyond the model is needed. Independent arithmetic audit:
`audit_thinning_obstruction.py`; exact input and strategy:
`kernel_no_common_parameter.json`.
