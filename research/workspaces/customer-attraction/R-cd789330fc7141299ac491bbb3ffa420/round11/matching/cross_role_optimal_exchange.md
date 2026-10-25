# Favorable optimal portfolios: exact cross-role replacement gate

2026-10-25, matching11. Arbitrary finite common catalogs, arbitrary player
count, unit customers/providers, all full-history pure SPE retained. **HALF
and WEAK-Q remain OPEN.** This is a static joint-selection relation. It
does not itself give a new welfare bound or pay any early true-response tax.
No novelty or external-review claim is made.

## Joint choice and exact copying refund

Fix an actual full leaf B=(B_1,...,B_m), loads c_x, final profits u_i and
W=sum_i u_i. It need not be an equilibrium for the statements below. Set

    f_i(A)=sum_(x in A) 1/[c_x+1-1_(x in B_i)].

Every denominator is positive on the indicated summation set. Among all
coverage-optimal legal m-tuples and all their assignments to actual rows,
choose a globally minimum frozen-cost pair, and relabel it T_1,...,T_m:

    O=union_i T_i,   Q=sum_i f_i(T_i)
      =min_(T optimal, pi) sum_i f_i(T_pi(i)).

Finiteness guarantees existence; repeated/empty themes are permitted.
For any two actual roles i,j, a legal copy of B_j into row i has the exact
cost

    f_i(B_j)=u_j-R_ij,
    R_ij=sum_(x in B_j minus B_i) 1/[c_x(c_x+1)]>=0.       (COPY)

Indeed on B_i intersection B_j the replacement preserves load c_x, and on
B_j minus B_i it raises load from c_x to c_x+1. In particular copying an
actual role never costs more than that role's original final payoff.
This is static copying into the actual background, not a true sequential
deviation and not an assertion about off-path old profits.

## Replacing a block of optimal tokens by other actual roles

Take arbitrary I,J subseteq [m], |I|=|J|. The indices I are removed
optimal tokens/rows; J are source actual roles, and need not equal I. Put

    O_notI=union_(i notin I) T_i,
    A_J=union_(j in J) B_j,
    L_IJ=(O minus O_notI) minus A_J,
    G_J=A_J minus O,
    delta_IJ=|L_IJ|-|G_J|.

Replacing T_I by B_J produces exactly m legal themes. Its coverage is
|O|-delta_IJ, so optimality gives delta_IJ>=0. Define the largest copying
refund in this cross-role block by

    Rstar_IJ=max_(bijections rho:I->J) sum_(i in I) R_(i,rho(i)),
    X_IJ=sum_(i in I) f_i(T_i)-sum_(j in J)u_j+Rstar_IJ.

For I=J=empty both quantities are zero. The all-input selection relation is

    delta_IJ=0  ==>  X_IJ<=0.                           (GATE)

Proof: when delta_IJ=0 the replacement portfolio remains optimal. Keep all
surviving T_i on their old rows, and place B_rho(i) on row i for a refund-
maximizing bijection rho. By (COPY) its total frozen cost is

    Q-sum_(i in I)f_i(T_i)+sum_(j in J)u_j-Rstar_IJ
      =Q-X_IJ.

The joint global minimality of Q forces X_IJ<=0. Thus any strictly positive
corrected cross-role cost excess forces a strictly positive net optimum
coverage loss. With integer unit customers it forces delta_IJ>=1. The
version without copying refund follows by discarding Rstar>=0.

For a single removed token i, its private-optimal block is
P_i=T_i minus union_(k!=i)T_k. A useful necessary consequence is

    f_i(T_i)>u_j  ==>  P_i minus B_j is nonempty.         (WITNESS)

More precisely, f_i(T_i)>u_j-R_ij implies
|P_i minus B_j|>|B_j minus O|. This uses delta=0 being impossible and
delta>=0; it does not assume P_i is private across the full catalog.

## Interface with source-token displacement

The source role set J can differ from the removed optimal-token set I.
Consequently (GATE) allows a future actual coverer to replace an optimal
source token, while returning the exact copying discount rather than
automatically spending both full payoffs. It is stronger than only using
same-role replacements I=J or only keeping optimal matching cycles.

What is missing is quantitative and dynamic. When delta_IJ>0, neither
coverage optimality nor min-Q selection bounds X_IJ by that lost customer
mass. The full-history SPE conditions must pay this positive-loss part.
In particular (GATE) gives no bound on Q-W in the full replacement I=J=[m]
when W<OPT, and no bound Q-W<=W/m. It is not legitimate to insert such an
amount bound after the implication.

The existing actual-prefix true-response identity remains

    Q-W=sum_i(E_i-e_i),
    e_i=u_i-d_i(T_i)>=0,
    E_i=f_i(T_i)-d_i(T_i),

where d_i(T_i) uses the same original complete strategy after the forced
actual-prefix query. (GATE) constrains permitted static token replacement;
it has not controlled sum_i E_i through those real response branches.

## Required m=5 substitution

The same general proof gives (COPY), (GATE), and (WITNESS) with arbitrary
I,J subseteq [5]. If the actual leaf is itself optimal, full replacement
gives Q<=W, already witnessed by assigning actual themes to themselves.
When it is suboptimal, the positive-loss term is still unpaid. Therefore
this mechanism alone does not establish OPT_5<=2W for arbitrary catalogs
and arbitrary complete-history pure SPE. No five-player coefficient tuning
or positive fixed-size project is inferred.

## Other precise candidate attack and status

`attack_weak_assignment.py` attacks the unchanged old WEAK-Q candidate in
one existing round10 complete m5/p8 policy cone, with one target support
(0,1,2,5,6), strict unique optimality, and all 120 frozen assignments.
`weak_assignment_attack.json` records a floating common margin -1/5 and no
positive candidate. It neither proves a cone upper bound (no exact dual
was recovered) nor raises the truth status of WEAK-Q or HALF. The attack
was stopped after this single bounded query; it is not the proof of any
displayed all-input relation above.

Existing static min-assignment decomposition and same-role zero-loss
selection are acknowledged rather than claimed as a solved payment.
The COPY refund and cross-role block gate were reconstructed directly from
the unit-customer formula here; deduplication and independent attack are
pending.
