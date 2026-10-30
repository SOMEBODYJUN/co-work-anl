# Independent skeptical review of the all-n prefix-balance family

Reviewer: `/root/prefix_balance/family_skeptical_review`, independent of the construction author.

Reviewed [canonical proof](../../../research/current/customer_attraction/prefix_balance_family.md)
against `customer_attraction/model.md`, the repository-wide `model.md`, and
`co-work-anl/AGENTS.md` on 2026-10-10. No repository files were edited.

**Verdict:** I found no gap in the universal counterexample or complete-history
SPE construction. The conclusion follows from the displayed algebra for every
integer n ≥ 4; finite checking is supplementary. There is one small ambiguity in
the last-player table: its first row lists the action selected by the tie rule,
rather than the complete set of best replies.

## Denominators and inequalities

For a last-player prefix, a+b+Σℓ_k=n−1. Thus every payoff denominator lies in
[1,n]. In (4), the Jensen denominator is
D=(n−2)b+2(n−1)−a−ℓ_j>0, and b≤n−1−a−ℓ_j gives
D≤(n−1)(n−a−ℓ_j). The latter factor satisfies n−a−ℓ_j≥1.
Consequently both Jensen and the second reciprocal comparison have the claimed
direction. When a=ℓ_j=0 and Σℓ_k≥2, b≤n−3 yields
D≤n²−3n+4; the numerator excess in (6) is n−3>0.

All four ordinary-leaf cases in (7) exhaust the possibilities. The delicate
case (8) has exactly the claimed cleared numerator
(n−1)²(n−4)≥0. For n=4 this lower-bound equality does not create an omitted
tie: equality in Jensen would require distributing two leaf actions equally
among three other leaves, which is impossible for integer counts. In (9), the
a≥1 comparison has strictly positive cleared difference n²−2n−1. For a=0,
the denominator in (10) is n²−(n−1)Σℓ_k≥2n−1>0, and the final cleared
difference n²−4n+2 is positive for n≥4. No zero, negative, or reversed
denominator was found.

## Complete strategy and ties

The strategy assigns an action at every ordered history. At last-player
prefixes with a≥1 or at least two leaf actions, B beats A and every ordinary
leaf strictly. B also beats L_n strictly except at
(a,b,ℓ)=(1,n−2,0), where (5) gives an exact B/L_n tie. B-first priority
selects B there. Therefore the table should either be captioned “selected
action under the specified priority” or annotate this tie. This is a wording
issue, not an equilibrium failure.

With no A and exactly one ordinary-leaf action, precisely the other n−1
leaves tie for maximum; A, B, and the repeated leaf are strictly worse by
(12). At least one other ordinary leaf exists, so the stated priority selects
the earliest such leaf. All-B and single-special-leaf prefixes have the unique
best reply A by (11) and (13).

I rederived each actual continuation in §3. All-B deviations lead respectively
to A+B^(n−1), two distinct ordinary leaves+B^(n−2), or
A+L_n+B^(n−2), with the payoffs claimed. Prefixes already containing A or
two leaf actions retain that condition after every deviation, so all following
actions really are B; the reduction to an appended-B comparison background is
legitimate because payoffs depend on terminal counts. Both single-leaf history
classes have the claimed continuation counts and positive margins in (15)–(16).
Some earlier B/L_n comparisons are weak ties inherited from the terminal tie;
weak optimality is sufficient for the model's SPE definition. These cases
exhaust every legal ordered history, including length n−2.

## Coverage, quantifiers, and finite diagnostics

The n disjoint leaves cover all customers, and their positive private groups
force any full-coverage n-action support to contain every leaf. After A, the
two completion cases, with or without B, both give the same attainable bound
2(n−1)(n−2). Hence (18)–(20) follow, including B₁=4−n−1/n<0.
For 0≤α<2, choosing n≥4 with n>4/(2−α) makes
(α−2)n+4−α/n<0; for α<0, n=4 already works. This proves the full fixed-real-α
quantifier, not merely a limit heuristic.

As a separate diagnostic, an independently written unit-customer expansion
used exact `Fraction` arithmetic and checked every count prefix and every
true-continuation action comparison for n=4,5,6: respectively 84/504,
330/2310, and 1,287/10,296 states/comparisons. All passed, and the only tie in
the table's B rows was the B/L_n tie identified above. These finite results do
not establish the universal claim; the preceding denominator analysis and
complete-history case exhaustion do. External peer review and novelty were
not assessed.
