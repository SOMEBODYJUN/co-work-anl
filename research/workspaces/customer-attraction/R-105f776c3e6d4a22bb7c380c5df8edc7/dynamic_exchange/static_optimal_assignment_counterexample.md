# 静态最优主题排列预算的完整 SPE 反例

2026-10-24. Personal research checkpoint for **Q-CAG-HALF**. The general half
coverage question remains **OPEN**. This note disproves only the exact static
assignment interface described below. It does not give a half counterexample,
and it does not disprove matching that uses true changing continuations.

Status: author-level exact construction and complete definition-level replay.
The parent has requested an independent raw-certificate audit; that audit is
not claimed here. The raw instance and full policy below are frozen. No
external review or novelty certification is asserted.

## 1. Exact candidate that fails

Use the arbitrary finite unit-customer common-catalog
[CAG-MODEL](../../../../current/customer_attraction/model.md), with every
ordered-history pure SPE and arbitrary ties allowed. For a full SPE terminal
path z=(S_1,...,S_m), define its static replacement query

\[
 f_i(T;z)=\sum_{x\in T}\frac1{1+c_x(z)-\mathbf1_{x\in S_i}}.
\]

The false statement is:

> For every instance and every complete pure SPE terminal z, there exist an
> optimal m-topic tuple (T_1,...,T_m) and a permutation pi such that
> sum_i f_i(T_pi(i);z) <= W(z).

This statement would suffice for half coverage by the usual static coverage
charging inequality. It differs from the already failed true-deviation
matching of omitted customers: here the query background is frozen at z with
one original player removed, and the proposed upper budget is the whole W.

The construction below has m=3, six different legal topics, a **unique**
optimal support {1,2,5}, and

\[
 W=1735,\quad OPT_3=1740,\quad
 \min_\pi\sum_i f_i(T_{\pi(i)};z)=1736>1735.
\]

The actual and optimal topic labels are disjoint. All 63 nonempty customer
interest types have positive integer multiplicity. Thus neither changing the
optimal tuple nor avoiding duplicate comparison topics repairs this interface.

## 2. Explicit integer unit-customer input

Let P={0,1,2,3,4,5}. Define the integer subset function F by the following
nonzero values and set F(S)=0 for every other subset S of P:

| S | F(S) | S | F(S) |
| --- | ---: | --- | ---: |
| {0,2} | 2 | {0,5} | 2 |
| {2,3} | -1 | {2,5} | -1 |
| {3,4} | 1 | {0,1,2} | 1 |
| {0,1,4} | 1 | {0,2,5} | 1 |
| {0,4,5} | 1 | {1,2,5} | 1 |
| {1,3,4} | 1 | {1,3,5} | 1 |
| {3,4,5} | 1 | | |

For each nonempty B subset of P define integers, using ordinary subset sums,

\[
 c_A=\sum_{T\subseteq A}(-1)^{|A|-|T|}F(T),\quad
 z_A=(-1)^{|A|+1}|A|c_A,\quad
 x_B=\sum_{A\supseteq B}(-1)^{|A|-|B|}z_A,\qquad r_B=x_B+31.
\]

Create r_B distinct unit customers who like exactly the topics in B. This is
the M1 Boolean potential transform from the internally audited
[Möbius compiler](../../../../current/customer_attraction/mobius_compiler.md),
not a signed-customer model. Direct integer calculation gives

\[
 \min_B x_B=-30,\quad \max_Bx_B=30,\quad
 \sum_Bx_B=0,\quad\sum_B|x_B|=456.
\]

Consequently every r_B is an integer in [1,61], and the instance has
63*31=1953 distinct unit customers. The complete raw multiplicities are
[assignment_instance.json](assignment_instance.json).

For any terminal using three different topics, every selected player receives
the same uniform-bias contribution

\[
 \beta=31(2^6-2^3)/3=1736/3
\]

plus the signed potential marginal F(S)-F(S\{a}). The uniform-bias total
coverage is 3 beta=1736.

## 3. Complete ordered-history policy

The root selects 0. After the first topic a, the second player selects the
following topic:

| a | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Second action | 3 | 2 | 4 | 0 | 5 | 0 |

The last player's action after every ordered pair (a,b) is in the table. The
diagonal entries explicitly complete all repeated off-path histories.

| a \ b | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 2 | 2 | 5 | 4 | 5 | 2 |
| 1 | 2 | 0 | 0 | 5 | 3 | 3 |
| 2 | 1 | 0 | 0 | 1 | 3 | 0 |
| 3 | 2 | 5 | 1 | 4 | 1 | 1 |
| 4 | 5 | 3 | 3 | 1 | 3 | 0 |
| 5 | 2 | 3 | 0 | 1 | 0 | 0 |

All 43 prescribed actions appear separately in
[assignment_full_policy.json](assignment_full_policy.json).

The actual path is (0,3,4). Since F(034)=F(03)=F(04)=0 and F(34)=1,

\[
 (u_1,u_2,u_3)=(\beta-1,\beta,\beta)
 =(1733/3,1736/3,1736/3),\qquad W=1735.
\]

### Direct verification of the fresh-action subtrees

At a distinct pair (a,b), every fresh last action c has signed payoff
F(abc)-F(ab). The displayed last action always maximizes F(abc), so it is
optimal among all fresh actions. Following the displayed last actions, the
second player's signed payoff from each fresh alternative is:

| a \ second alternative | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | — | -1 | -1 | 0 | -1 | -1 |
| 1 | 1 | — | 1 | 1 | 1 | 1 |
| 2 | 1 | -1 | — | 0 | 1 | -1 |
| 3 | 1 | 1 | 0 | — | 1 | 1 |
| 4 | 1 | 0 | -1 | 1 | — | 1 |
| 5 | 2 | 1 | -1 | 1 | -1 | — |

The prescribed second action maximizes every row. Root signed payoffs after
the prescribed continuations of root actions 0,...,5 are
(-1,-1,-1,-2,-1,-1), so root action 0 is optimal.

### Repeated histories and repeated deviations are checked too

The sufficient general M2 bias would be 4*456+1=1825. Here the smaller bias
31 is verified directly, rather than assumed to inherit M2's conclusion.
For this fixed complete policy, each of the 258 exact SPE comparisons is
affine a+K b in a uniform bias K. Direct substitution into all 63 customer
types gives:

| Bias slope b | Number of comparisons | Minimum signed intercept a |
| --- | ---: | ---: |
| 0 | 186 | 0 |
| 16/3 | 66 | -5/3 |
| 32/3 | 6 | 0 |

The first row includes every comparison that ends in two fresh terminal
profiles, as well as the fresh comparisons at repeated last histories. The
other rows include all repeated-action deviations. Hence K=31 makes every
comparison nonnegative; in fact the largest IC threshold from positive-slope
rows is only 5/16. Positivity of the actual customer types requires K>=31.

[audit_assignment_witness.py](audit_assignment_witness.py) independently
reconstructs all these quantities using only integer arithmetic and Fraction.
It imports no optimization package, canonical SPE solver, model, or verifier.
It directly replays all 43 histories and all 258 comparisons in the legal
compiled game. The frozen exact output is
[assignment_exact_audit.json](assignment_exact_audit.json).

## 4. Unique optimum and unavoidable assignment excess

Because every singleton customer type has positive multiplicity, adding any
previously unused topic strictly increases coverage. Thus an optimal
three-topic tuple uses three different topics. For a three-element support S,

\[
 W(S)=1736+3F(S)-\sum_{a\in S}F(S\setminus\{a\}).
\]

The signed welfare values over all 20 supports are:

| Support | Signed welfare | Support | Signed welfare |
| --- | ---: | --- | ---: |
| 012 | 1 | 013 | 0 |
| 014 | 3 | 015 | -2 |
| 023 | -1 | 024 | -2 |
| 025 | 0 | 034 | -1 |
| 035 | -2 | 045 | 1 |
| 123 | 1 | 124 | 0 |
| 125 | **4** | 134 | 2 |
| 135 | 3 | 145 | 0 |
| 234 | 0 | 235 | 2 |
| 245 | 1 | 345 | 2 |

Thus {1,2,5} is the unique optimal support and OPT_3=1736+4=1740.

Every static replacement of an actual topic by a target topic uses three
different labels, because {0,3,4} and {1,2,5} are disjoint. Consequently all
such static queries receive the same beta bias, and their signed matrix is

| Actual player | T=1 | T=2 | T=5 |
| --- | ---: | ---: | ---: |
| 1, removing 0 | 0 | -1 | 0 |
| 2, removing 3 | 1 | 0 | 1 |
| 3, removing 4 | 0 | 0 | 0 |

The minimum assignment sum of this matrix is zero. If player 2 gets topic 2,
its entry and the other entries are zero; if player 1 uses its only negative
entry at topic 2, player 2 necessarily pays one on topic 1 or 5. Therefore

\[
 \min_\pi\sum_i f_i(T_{\pi(i)};z)=3\beta=1736=W+1.
\]

Every optimal ordered tuple is a permutation of the unique support, so the
existential choice of an optimal tuple cannot avoid this strict failure.

## 5. Mechanism and exact boundary

Static topic 1 or 5 against the actual root's frozen suffix (3,4) gives signed
root payoff zero. The true SPE continuation after either deviation changes
the suffix to (2,0) or (0,2), giving signed root payoff -1. At the second
actual node, static topics 1 and 5 have a signed premium one, while their true
continuations have signed payoff -1. The favorable discount at player 1,
topic 2 cannot be used without paying a premium at player 2. This forces a
positive frozen-follower assignment total despite every true incentive row
being nonnegative.

The construction exploits the exact common-bias cancellation on distinct
terminal labels, which is the mechanism isolated in the
[Möbius compiler](../../../../current/customer_attraction/mobius_compiler.md).
It does not transport the frozen costs back into true SPE deviations.

This is a genuine counterexample only to the static assignment interface.
It leaves the true same-node ROW net-gap candidate, the aggregate static
security bridge, and Q-CAG-HALF unresolved. In this instance
2W-OPT_3=1730>0. A future proof may use true branches, several nodes, or the
actual-only coverage credit; none of those are ruled out here.

## 6. Sources, discovery, and frozen reproduction

The exact candidate was relayed by the parent from peer seq242. The discovery
MILP [probe_disjoint_assignment.py](probe_disjoint_assignment.py) attacked
only this named all-input candidate, fixing disjoint actual/optimal supports;
it was not a search for a primary half counterexample. The saved discovery
output is [probe_disjoint_assignment.json](probe_disjoint_assignment.json).
[simplify_assignment_witness.py](simplify_assignment_witness.py) then reduced
the discovered integer table with its complete fresh policy held fixed.
[assignment_witness.json](assignment_witness.json) contains the 13 nonzero
integer F values and the fresh policy. The exact proof above and the raw full
certificate do not rely on the MILP solver's status.

From the repository root, the author audit command is:

```
python research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/audit_assignment_witness.py
```

The script recreates the frozen files deterministically; do not run it while
another agent is auditing those raw files. No general positive theorem is
claimed from this finite computation.
