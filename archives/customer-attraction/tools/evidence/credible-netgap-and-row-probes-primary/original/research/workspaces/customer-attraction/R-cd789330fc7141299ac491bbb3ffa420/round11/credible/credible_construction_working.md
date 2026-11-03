# Genuine bank punishment and the still unpaid minimum net gap

2026-10-25, credible11. This is an exploratory working note for the original
arbitrary-m Q-CAG-HALF. **The target remains OPEN.** No statement below
replaces the complete original game by independently chosen response menus.
The only new finite computation attacks an explicitly named all-input bridge
inside a policy which had already been verified in round10.

## 1. What has already been refuted, and what the current target is

The peer round5 insurance family gives original complete SPEs with

\[
W=2m,\quad \operatorname{OPT}_m=3m-2,\quad
u_1=1+\frac1{m-1}.
\]

Its exact source is
`R-d3981c0168644971803a9c3380ed687c/round5_general/security/global_extra_individual_counterfamily.md`,
including its source correction to R-44's Cartesian construction. We do not
claim this game, its m=3 seed, or its all-m controller as new. It refutes
several individual safety floors and, for m>=5, even
`u_i >= OPT_m/(2m)`. It does not refute

\[
\operatorname{OPT}_m-W\le m\min_i u_i.\tag{MIN-NET?}
\]

MIN-NET? is a genuine all-input sufficient bridge: its right side is at
most W because total actual utility is W. Its m=5 substitution would give
`OPT_5 <= 2W` without any extra hypothesis. We have not proved MIN-NET?.
The parent direct branch is separately investigating stronger true-query
row and assignment bridges. The bridge itself is not a new discovery.

## 2. Direct attempt to make insurance cross the target

Write a for the number of unit economic customers at each economic label
and b for the number in each bank block. This notation may be rational
during algebra, then integer-scaled; no provider weights are introduced.
In the peer's BASE/PUNISH/EXIT controller, the actual root gets

\[
u_1=\frac{a}{m-1}+\frac b2,
\]

and a middle player gets `a/(m-1)+b`. A middle player can change both
coordinates to a fresh economic label and a fresh bank. Under the exact
PUNISH continuation, its economic client is not selected by future fresh
economic labels; the last player copies precisely the deviator's bank.
Its deviation payoff is exactly `a+b/2`. Consequently genuine IC gives

\[
b+\frac a{m-1}\ge a+\frac b2,
\qquad
\frac b2+\frac a{m-1}\ge a.\tag{BANK}
\]

The second inequality is exactly `u_1>=a`. Actual economic coverage is
2a and its omitted optimum mass is `(m-2)a`. Hence this rescaling cannot
make MIN-NET? fail: the omission is below `m u_1`; actual banks only improve
the net coverage balance. It certainly does not produce a HALF
counterexample. This is an algebraic check on one proposed construction,
not a theorem about all bank games or all SPEs.

Nonuniform bank weights cannot simply be substituted into the old proof.
In its PUNISH last node every bank has exactly one previous user. Copying
the designated target bank is a genuine best reply only if that bank's
per-copy value is maximal. Arbitrarily assigning a cheap bank to each
deviator would therefore destroy the last player's incentive. No new
nonuniform full controller has been supplied here.

## 3. The common-catalog closure that a new construction must respect

A more ambitious idea is to let an early player change an economic and a
bank coordinate together. The deviation releases the bank customers in
its old action. A later action Q might then cover both the newly released
bank customers and the deviator T's new economic customers, compensating
the follower for herding T.

This alone does not define an SPE. Q is also a legal earlier action in the
same common catalog. The earlier player can select Q directly, potentially
retaining the bank whose release made Q attractive in the proposed
punishment branch. That different history needs its own genuine rational
continuation. Following this obligation creates action-to-follower cycles,
with different tails after different root choices; it does not create a
single freely selectable menu. The tree branch independently investigates
the cycle amounts. Here we have not proved a general cycle inequality or
constructed a target counterexample satisfying all those obligations.

The full Cartesian insurance example makes the problem particularly
visible: while fresh economic labels remain available, a future player
can combine the same bank with a fresh economic label. A purported
punishment which herds the economic coordinate loses against that legal
joint deviation. The real peer controller instead punishes the bank
coordinate, and (BANK) records its cost. This observation concerns the
construction and is not an impossibility result for all coupled catalogs.

## 4. Exact pressure on MIN-NET?, with no positive inference

`minimum_netgap_pressure.py` reuses the full policy in the round10
`repeated_upgrade_attempt_m5.json`. It does not enumerate new policies or
scan player counts. It permits all 255 nonempty client-interest types on
the same eight-topic catalog and enforces that root position 0 is an
actual minimum-payoff position. The fixed comparison is the already used
five-topic tuple `(2,3,4,6,7)`. With actual W normalized to one, the linear
objective is

\[
\left|\bigcup_j T_j\right|-W-5u_1.
\]

The exact accepted endpoint has

\[
\begin{aligned}
W&=11527673680,\\
\operatorname{OPT}_5&=16278494585,\\
u_1=\cdots=u_4&=2276882259,\\
u_5&=2420144644.
\end{aligned}
\]

The fixed comparison actually attains OPT at this point, and

\[
\operatorname{OPT}_5-W-5\min_i u_i=-6633590390<0.
\]

The exact integer endpoint and the full original ordered-history strategy
are frozen in the JSON. Canonical verification and a direct independent
Fraction comparison both pass all 4,681 histories and all 32,767 nonself
deviations. Floating LP output only proposes the point; exact feasibility
and the original game inequalities accept it. We did not recover or claim
an exact optimum certificate for this signed objective. Its negative gap
proves neither MIN-NET? nor HALF, even inside a different strategy cone.

## 5. Current remaining obligation

MIN-NET? still requires an all-input mechanism transferring the rents
created by each genuine punishment branch to one actual total budget.
Neither the bank rescaling algebra nor the one negative pressure endpoint
provides that transfer. A proof through punisher cycles would need an
amount relation controlling tail resets; merely closing the action graph
is insufficient. A counterexample would need a new original complete
strategy and all-history IC, together with `OPT>2W` to refute the main
target. This note stops at that precise unpaid obligation, with no new
restricted-input welfare project.
