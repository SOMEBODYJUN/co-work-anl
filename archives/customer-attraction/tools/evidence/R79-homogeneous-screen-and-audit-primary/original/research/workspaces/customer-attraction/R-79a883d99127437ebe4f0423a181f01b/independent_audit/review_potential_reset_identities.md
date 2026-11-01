# Independent algebra audit of POT and RESET

2026-10-24. Reviewed the parent's `../GENERAL_PROOF_WORKING.md` after
independently auditing the tiny covariance example. Verdict: the displayed
POT and RESET identities are correct, with the scope and missing inequality
stated below. This review establishes no general welfare closure.

## Potential insertion and the independent-query term

For any nonnegative integer background b and any unit-action tuple Q,
write Phi_b(Q)=sum_x [H_(b_x+c_x(Q))-H_(b_x)]. The marginal contribution of
inserting one action T into Q is exactly

    Phi_b(T,Q)-Phi_b(Q)=sum_(x in T) 1/(b_x+c_x(Q)+1).

This identity also holds when Q is empty, or T is empty. All denominators
used in the marginal are positive.

Fix any complete pure strategy and one genuine history. Let B(A) denote
its genuine continuation after forced current action A; no equilibrium
property is needed yet. For independent A,T drawn from the same distribution
p, let

    D=E sum_(x in A) 1/(b_x+1+c_x(B(A))),
    Cminus=E sum_(x in T) 1/(b_x+1+c_x(B(A))),
    C=E sum_(x in T) 1/(b_x+1+1_(x in A)+c_x(B(A))).

Insertion gives D-Cminus as the expectation of
Phi_b(A,B(A))-Phi_b(T,B(A)). Swapping iid A and T in the second term is
valid, and gives precisely R=E[Phi_b(A,B(A))-Phi_b(A,B(T))].

For Cminus-C, a client contributes zero unless it belongs to both A and T.
When it belongs to both, its contribution is

    1/[(b_x+c_x(B(A))+1)(b_x+c_x(B(A))+2)].

Thus D-C=R+J is exact. No actual continuation was replaced by a static or
off-model equilibrium. The iid assumption is essential to this exact form
of R; arbitrary unrelated query and forced-action distributions require a
different expression.

## Exposing genuine unilateral comparisons

For fixed A,T, use t=B(T) as a legal sequence of forced actions. At each
successive genuine history beginning with A and the already forced prefix
of t, define Z_(j-1) to follow the prescribed action and Z_j to force the
next t_j before following the same original strategy. Both are real
continuation outcomes from that history, so the moving player's terminal
payoff difference Gamma_j is nonnegative under full-history SPE.

The marginal identity gives the exact terminal decomposition

    Phi_b(Z_(j-1))-Phi_b(Z_j)
      = Gamma_j + Phi_b(Z_(j-1)\j)-Phi_b(Z_j\j).

Here deleting slot j is terminal algebra only. Summing over j telescopes
the undeleted potentials to R. At the final slot there are no later
actions, and deletion leaves identical tuples on the two sides; hence
E_n=0. This independently confirms RESET, including its n-1 endpoint.

For n=0, R=0. For n=1, both tuples in the R difference retain the same
current action A and differ in only the last player's action. Insertion
therefore turns the potential difference into that player's genuine
best-response comparison, yielding R>=0. For n>=2, B(T) is a legal tuple
but cannot be substituted as a single follower action. No sign for R or
the earlier reset terms follows from SPE alone.

## Required quantifier for the proposed global payment

The path identity

    sum_i C_i-W = -sum_i(e_i+R_i+J_i),  e_i=u_i-D_i>=0,

is correct when the same p is used in each definition. To infer the stated
extra-slot security lower bound, it suffices to prove nonnegative total
payment for a common p maximizing v_(m+1)(0); then each C_i(p) is at least
v_(m+1)(0), because every menu column is a legal m-slot background and the
query is independent of that column. Proving payment for every p would be
a stronger sufficient assertion. The working draft should state which
quantifier is being investigated; the algebra by itself proves neither.

No fatal algebraic objection was found. The unsupported step remains the
general joint budget paying negative reset terms, or a weaker free-menu
budget. This review does not treat an equivalent representation as a new
inequality or as evidence that the general claim is solved.
