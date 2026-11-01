# Blind reconstruction of heterogeneous prefix insurance repair

2026-10-24, before reading the author draft. Original general Q-CAG-HALF remains OPEN.

## Algebra and product construction reconstructed independently

Let z=(S_1,...,S_m) be an arbitrary old terminal, with the old last action a best reply.
For each old actual prefix h_i and action A, let ell_i(A) be the minimum current
payoff over complete SPEs of the true successor subgame. Define
D_i=max_A ell_i(A), delta_i=(D_i-u_i(z))_+ for i<m, and delta_m=0.
The continuation minimum is attained because the game tree and pure SPE set are finite.

Sort the positive distinct delta levels. A layer of thickness s>0 has marked set
I={i<m:delta_i>=the upper endpoint}; write k=|I| and q=m-k>=1.
The insurance instance has k disjoint banks of size 2s, one disjoint Y of size qs,
and q-1 disjoint leaves of size s. The specified insurance terminal assigns each
marked player its own bank and every unmarked player Y. Its utilities are 2s
at marked positions and s otherwise. Its welfare is (m+k)s. Its entire catalog
union is (2m-1)s, and m actions cover it (k banks, Y, and q-1 leaves).

Consequently summing layers gives W_ins=m delta_max+sum delta_i,
OPT_ins=(2m-1)delta_max, and each position's planned insurance payoff is
baseline delta_max plus delta_i. The half-gap loss is therefore
2 sum delta_i+delta_max. Rational layer sizes can be made integer by a common
copy scale; a theorem for literal integer clients must state that scale explicitly.

The exact missing insurance lemma is: after every proper prefix of the specified
insurance terminal, and after every possible current insurance action, there
exists a complete SPE of all remaining insurance players giving the fixed current
player payoff at most s. If this holds, an arbitrary joint old/insurance deviation
can be punished by a product of (i) an old continuation attaining ell_i(A), and
(ii) independently selected insurance continuations with the cap in every layer.
The deviation gives at most u_i+delta_i+delta_max, exactly the planned payoff.
Every deviation branch uses complete component SPEs, so the Cartesian product
is a complete SPE; distinct full histories may use different threat products.
The intended joint action retains the intended old terminal, whose successor
need not itself be an old SPE; this is paid recursively by later insurance layers.

The last joint player is a best responder: all banks already selected once give
entry payoff s, Y has q-1 old copies and gives s, and each leaf gives s; the old
last action is a best reply by hypothesis.

## Threshold invariant exposed by the cap lemma

Scale s=1. At a normal prefix let a banks have appeared and b copies of Y.
Before the current position i, a+b=i-1, b<=q-1, and the number of high marginal
seats above 1 is
Q=(k-a)+(q-1-b)=m-i.
If the current action is an already occupied bank, a leaf, or already saturated Y,
its own payoff is already <=1 and cannot increase. If it is a fresh bank or an
unsaturated Y, the high-seat count drops to Q-1 while m-i successors remain.
There is one extra successor beyond filling all high seats, which can be used
to copy the chosen fresh bank or complete Y to q copies.

This establishes feasibility of a desired final occupancy but not yet its full
SPE implementation. The natural candidate punishment terminal fills other fresh
banks once and Y to q-1 copies, and places one final player on the selected bank;
for a selected Y, it fills all fresh banks and completes Y to q copies. These
terminals are follower static NE and all follower utilities are >=1. A static NE
alone does not prove a sequential SPE. A naive myopic maximum-entry-payoff rule
is not a universal solution: values (3,2), three players give greedy A,B,A with
root utility 3/2, but root B followed by A,A gives root 2.

This blind reconstruction therefore establishes the repair theorem conditional
on the stated cap lemma, isolates the exact all-history obligation, and does not
promote the theorem before that obligation is independently proved.
