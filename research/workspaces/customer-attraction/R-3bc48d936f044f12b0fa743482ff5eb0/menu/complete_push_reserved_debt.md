# Complete-terminal push: exact discount, paid tail reserve, and stopping gap

2026-10-24. Personal general proof checkpoint. **Q-CAG-HALF remains OPEN.**
No general menu or security payment has been proved here. The statements below
quantify arbitrary finite common catalogues, arbitrary player counts, every
complete-history pure SPE, all ordered off-path histories, and every query
distribution. Empty topics, repeats, and zero customer sets are retained.

The explicit tail reserve is a quantitative combination of the existing
two-remaining-player push theorem and the actual last-player BR. It is not
claimed as a new independent tail theorem. Its purpose is to isolate the exact
early complete-terminal debt, including the extra own-action discount that is
absent from the already false all-p tail and Jensen budgets.

## 1. Full menus and the extra own-action discount

Fix the complete original SPE sigma, actual leaf z=(S_1,...,S_m), actual
profits u_i, and W=sum_i u_i. At actual prefix z_<i, force A and continue the
same original sigma to obtain Z_i(A). This retains all changing successors.
Delete only the forced role's action from this leaf to obtain B_i(A).

For an arbitrary common-catalogue distribution p, write

    q_x = Pr_(T~p)(x in T),
    d_i(A) = sum_(x in A) 1/c_x(Z_i(A)),
    D_i = E_(A~p) d_i(A),
    C_i = E_(A~p) sum_x q_x/[1+c_x(B_i(A))],
    P_i = E_(A~p) sum_x q_x/[1+c_x(Z_i(A))].

Thus P_i=p^T K_i p is the **complete-terminal** push, whereas C_i deletes
the forced action before querying. Original actual-prefix IC gives

    e_i := u_i-D_i >= 0.

Set kappa_i=D_i-C_i and

    R_i = E_(A~p) sum_(x in A)
             q_x/{c_x(Z_i(A))[c_x(Z_i(A))+1]} >= 0.

Every displayed denominator in R_i is positive because x is in A. Direct
subtraction gives the unconditional identities

    C_i-P_i=R_i,
    P_i-u_i= -e_i-kappa_i-R_i,
    W-sum_i P_i=sum_i(e_i+kappa_i+R_i).             (FULL-DISCOUNT)

In particular the failed all-p inequality sum_i C_i<=W does not refute the
different candidate

    sum_i P_i<=W for all p.                        (FULL-PUSH?)

Neither the sign of sum_i kappa_i nor Jensen credit alone proves FULL-PUSH.
The sum of the R_i is a genuine additional discount, but this page does not
bound the remaining negative covariance by that discount.

## 2. One explicit reserve paid by the actual last two roles

Suppose m>=2. Put j=m-1 and let b_x count the actual first m-2 actions.
At this exact ordered prefix, let rho(A) be sigma's genuine final action
after the forced penultimate action A. Let

    eta_x = Pr_(A~p)(x in A and x in rho(A)),
    w_x = 1/[(b_x+1)(b_x+2)],
    L = E_(A,A' iid p) [
          U_b(rho(A),A)-U_b(rho(A'),A)] >= 0,
    Q = sum_x 2 w_x q_x(q_x-eta_x)/(b_x+3) >= 0,
    V = sum_x q_x^2/[(b_x+2)(b_x+3)] >= 0.

U_b(X,Y)=sum_(x in X)1/[b_x+1+1_(x in Y)]. Each term defining L is a
true final-node BR comparison at the history ending in A. Here A' only
randomizes over other legal actions rho(A'); it does not transfer their
optimality from a different history. The known two-player push identity is

    D_j-P_j=L+V+Q.

Consequently,

    P_j-u_j= -e_j-L-V-Q.                           (PENULTIMATE)

For the last role, B_m(A) is the fixed actual past and does not depend on A.
Put b'_x=c_x(z_-m). Define the actual final BR slack, the pushed last-row
quadratic discount, and the actual complete-leaf discount by

    e_m=u_m-E_(T~p) sum_(x in T)
                   1/[1+c_x(z_-m)] >= 0,
    V_m=sum_x q_x^2/[(b'_x+1)(b'_x+2)] >= 0,
    R_m^actual=sum_(x in S_m)
                   q_x/{c_x(z)[c_x(z)+1]} >= 0.

The Bernoulli identity E_A[1/(b'+1+1_A)]=1/(b'+1)-q/[(b'+1)(b'+2)]
gives an exact last-push reserve:

    P_m=u_m-e_m-V_m.                               (LAST-PUSH)

The full actual column separately gives the pointwise subtraction

    g_p(z):=sum_x q_x/[1+c_x(z)]
           =u_m-e_m-R_m^actual.                    (LAST)

Every column of K_m is exactly the terminal consisting of the fixed past
and its forced A; hence P_m need not equal g_p(z). However the free final
menu can use the actual column. Define

    psi_i(p)=min_A sum_x q_x/[1+c_x(Z_i(A))],
    G_i=P_i-psi_i(p)>=0.

Then at the last position, choosing the actual column and also using the
pushed mixture gives

    psi_m(p)<=u_m-e_m-max(V_m,R_m^actual).          (LAST-MENU)

It is useful to reserve this last-column gain separately rather than
incorrectly setting P_m=g_p(z). The exact extra gain is

    J_m=P_m-g_p(z)=R_m^actual-V_m,

which can have either sign. Since G_m>=max(0,J_m), the available last-row
menu reserve V_m+G_m is at least max(V_m,R_m^actual). This does not let
one add V_m and R_m^actual as two independently paid discounts.

## 3. An unconditional aggregate menu relation

For i<=m-2 write H_i=P_i-u_i; these early full-push defects are not known
to have either sign. Combining PENULTIMATE with LAST-PUSH yields the
following exact relations for **every p**, with no hypothesis about an
optimal query, any stationary distribution, or a modified SPE:

    T(p)=e_(m-1)+L+V+Q+e_m+V_m >=0,
    sum_i P_i-W=sum_(i<=m-2) H_i-T(p),
    sum_i psi_i(p)-W
       =sum_(i<=m-2) H_i-T(p)-sum_i G_i.          (EXACT-TAIL)

The actual final column gives the companion paid bound

    sum_i psi_i(p)-W
      <= sum_(i<=m-2) H_i
         - [e_(m-1)+L+V+Q+e_m+R_m^actual]
         - sum_(i<m) G_i.                         (PAID-TAIL)

All terms in brackets, and all G_i, are nonnegative. The difference between
the right side and left side is G_m-J_m>=0. The exact version retains the
quadratic pushed last-row reserve V_m as well as its true mixture gain G_m;
the companion bound explicitly uses the actual full-leaf discount.

Proof: for every i, psi_i=P_i-G_i. For the penultimate row insert
P_(m-1)=u_(m-1)-e_(m-1)-L-V-Q; for the last row use LAST-PUSH. Summing
proves EXACT-TAIL. Replacing V_m+G_m by its lower bound R_m^actual proves
PAID-TAIL. All early H_i use original complete forced-action terminals.
No source is evaluated with a frozen successor.

In particular, if t=W/m and every actual-prefix free menu has psi_i(p)>t,
then necessarily

    sum_(i<=m-2) H_i
       > e_(m-1)+L+V+Q+e_m+R_m^actual
          +sum_(i<m)G_i.                         (EARLY-NECESSITY)

The statement is useful as a diagnostic: positive path-menu pressure must
survive both the full-leaf self discount and an explicitly paid two-role
reserve. It does not prove that such pressure is impossible.

PAID-TAIL is stronger than merely bounding the last two menu values by their
profits, but it is a corollary of existing true tail comparisons. It is not
a general early-debt payment, and is not reported as a new welfare theorem.

## 4. The exact unresolved sufficient payment, and m=5

One sufficient full-input payment would be, for every p,

    sum_(i<=m-2) H_i<=T(p)+sum_i G_i.              (EXACT-EARLY-PAY?)

A possibly stronger but explicitly actual-column version is

    sum_(i<=m-2) H_i
       <= e_(m-1)+L+V+Q+e_m+R_m^actual
          +sum_(i<m)G_i.                         (EARLY-PAY?)

This would imply sum_i psi_i(p)<=W for all p, hence

    Mpath=max_p min_i psi_i(p)<=W/m.

The known static inequality OPT_m<=2m v_(m+1)(0), together with
Mpath>=v_(m+1)(0), would then prove HALF. EARLY-PAY is unproved. It is a
stronger uniform-time sufficient route; no equivalence with HALF is claimed.

At m=5 the same formula, without adding five-player assumptions, asks for

    H_1+H_2+H_3
       <= e_4+L+V+Q+e_5+V_5+sum_(i=1)^5 G_i,
    V=sum_x q_x^2/[(b_x+2)(b_x+3)],
    V_5=sum_x q_x^2/[(b'_x+1)(b'_x+2)],
    b_x=sum_(i=1)^3 1_(x in S_i).

Here b'_x=b_x+1_(x in S_4). Replacing V_5+G_5 by R_5^actual gives the
slightly stronger actual-column sufficient version in EARLY-PAY.

If paid for every p, this would give Mpath<=W/5 and OPT_5<=10Mpath<=2W.
The present work has not bounded H_1+H_2+H_3 by this reserve. Therefore it
does **not** unconditionally pass the five-player pressure test. The missing
information is an early cross-history payment, not a numerical constant in
the proved tail identity.

## 5. Focused falsification diagnostic and stopping decision

The separate probe_complete_push.py tests FULL-PUSH? and the weaker
uniform-time free-column inequality on one fixed formal complete policy:
three players and six topic labels, root 0, second chooses the opposite
group's first label, last chooses the smallest unused label in the second
action's group. All 43 ordered decision histories and 258 IC comparisons
are kept. Variables are all 63 nonempty customer membership types.

Exactly two query distributions were used: p=(delta_2+delta_5)/2 and uniform
on six labels. The floating LP maxima for sum_i P_i-W, with total customer
mass one, were -1/8 and approximately -0.09104938. The analogous maxima for
sum_i psi_i-W were -1/8 and approximately -0.09722222. No strict proposal
was found. These are numerical diagnostics, not exact dual certificates,
not a proof of this policy cone, and not a proof of either general candidate.
The output is probe_complete_push.json. The labelled cone can collapse
different catalogue labels to the same customer set; this is another reason
not to promote its negative diagnostic to a theorem. No scan or new restart
was made.

The stopping point is EARLY-PAY, or a genuinely weaker direct Mpath payment.
No fatal issue with the actual-root Mpath definition was found. The known
arbitrary-background PB-extra counterexample must not be substituted for a
root-actual-position Mpath counterexample; reachability and the total root
slot count remain essential.

Sources used: current general_half_proof.md, model.md, the general state and
failed-route maps; R-e5367c3753db4149ba2d72950d8f1193/menu/
reservation_menu_budget_closure.md; R-d3981c0168644971803a9c3380ed687c/
round3_general/equilibrium/fractional_global_payment_boundary.md;
R-d22a706a03c5499d941a6a97f94128a8/induction/
two_player_full_terminal_pushforward.md; and the relevant round8 files of
R-cd789330fc7141299ac491bbb3ffa420. This checkpoint does not alter their
statuses or claim independent review of them.
