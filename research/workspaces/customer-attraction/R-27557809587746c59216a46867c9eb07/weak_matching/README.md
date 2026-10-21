# Weak optimal static matching: assignment identities and finite attacks

Q-CAG-HALF remains OPEN. This directory studies the sufficient auxiliary
claim that every complete-history pure SPE terminal profile admits an optimal
length-m topic portfolio and a matching whose frozen-opponent query sum Q is
at most (1+1/m)W. The stronger Q<=W bridge is false in the earlier Boss10
52-client example.

## Exact algebra; no equilibrium assumption

Fix a terminal profile S_1,...,S_m, client load c_x, and comparison portfolio
T_1,...,T_m with incidence k_x. For a permutation pi write

    A = sum_x k_x/(c_x+1),
    D = sum_{x:c_x=0} k_x,
    B(pi) = sum_i sum_{x in T_pi(i) intersect S_i} 1/[c_x(c_x+1)].

Then Q(pi)=A+B(pi). Uniformly random matching has

    E B = (A-D)/m,
    min_pi Q(pi) <= (1+1/m)A-D/m.

Proof: for c_x>0, removing position i changes the query share by
1/[c_x(c_x+1)] exactly when x belongs to S_i. Each comparison occurrence is
matched to one of the c_x covering positions with probability c_x/m. For
c_x=0 there is no correction. Sum the client contributions. The minimum is
at most the uniform average.

Thus the open optimal-portfolio adding-query bridge A<=W would imply the weak
matching bridge, with slack D/m. A strictly weaker sufficient condition is

    A <= W + D/(m+1).

This distinction can matter when many optimal comparison topics overlap on
clients missed by the actual outcome. It does not establish either condition
for SPE. The exact assignment optimization can additionally save the gap
between uniform matching and minimum matching.

For completeness the standard client accounting gives

    OPT <= Q(pi)+(1-1/m)W

for every optimal portfolio and every matching: each missed optimal client
contributes at least one to Q, and each covered optimal client contributes at
least 1/m. Consequently Q<=(1+1/m)W would suffice for OPT<=2W.

## Status and next test

Only the displayed identities and conditional implications are established
here. The weak matching bridge, its adding-query sufficient condition, and
Q-CAG-HALF all remain open. Planned finite attacks optimize the exact minimum
assignment in fixed complete-policy customer multiplicity cones. Every claimed
counterexample must be rechecked with exact arithmetic at all ordered histories
and over every optimal portfolio; floating LP output is only a locator.

The subsequent [partitioned frozen query candidate](partitioned_queries.md)
discards duplicate client charges among optimal topics. It has an exact
hypergeometric random-matching formula and would imply the sharp finite-m
bound if a general payment proof could be supplied. Its status remains OPEN.

The main reusable result is the [acyclic replacement lemma](acyclic_replacement_lemma.md):
a precise count-vector containment condition turns real full-strategy queries
into a once-charged frozen comparison, with exact total budget W. It supplies
a four-unit-row certificate for the earlier strong static-matching failure.
The condition is sufficient only; the known two-player real-portfolio failure
already disproves its universal existence.

Exact replay:

    python3 research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/weak_matching/acyclic_source_audit.py
    python3 research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/weak_matching/algebra_audit.py

`acyclic_source_audit.json` checks every ordered history of the original source
and all 63 type coefficients. `algebra_audit.json` checks the matching formula
for all 1302 incidence pairs through m=5 and reproduces the source charges.
The finite LP runs in `*seed*.json` are numerical searches, separately labeled.
