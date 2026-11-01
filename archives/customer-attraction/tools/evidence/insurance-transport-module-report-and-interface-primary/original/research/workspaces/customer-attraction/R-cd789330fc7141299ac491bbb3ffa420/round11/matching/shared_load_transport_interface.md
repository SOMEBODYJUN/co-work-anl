# Shared-load KKT interface with genuine query-role transport

2026-10-25, matching11 continuation. This is an exact interface, not a paid
aggregate inequality. The arbitrary-player/common-catalog/full-history pure
SPE target and its m=5 substitution remain OPEN. No further policy-cone
scan was run.

Use the parent's `../parent/shared_load_bregman_working.md` notation:
L_i(A) is the true forced-A leaf's competitor load after deleting current
role i, and d_i(A)=sum_(x in A)1/[1+L_i(A)_x]. Every original whole IC is
d_i(A)<=u_i. The shared convex domain is

    K=(1/m) sum_i conv{L_i(B):B in S}.

Fix p, rho_x=Pr_p[x in A], any L* in K, and t_x=1/(1+L*_x). The following
freedom does not change the requested query marginal: choose arbitrary row
distributions p_i satisfying

    sum_A p_i(A)=1,
    sum_i p_i(A)=m p(A).                              (TRANSPORT)

Thus each actual role spends one whole IC coefficient, while the total
query mass of each theme stays fixed. Define

    C(p_i)=sum_i E_(A~p_i) sum_(x in A) t_x^2[L_i(A)_x-L*_x],
    D(p_i)=sum_i E_(A~p_i) sum_(x in A)
             t_x^2[L_i(A)_x-L*_x]^2/[1+L_i(A)_x],
    IC_i(p_i)=u_i-E_(A~p_i)d_i(A)>=0.

The same reciprocal expansion as in the parent gives exactly

    sum_i E_(p_i)d_i(A)=m F_p(L*)-C(p_i)+D(p_i),
    W-m F_p(L*)=sum_i IC_i(p_i)-C(p_i)+D(p_i).       (T-BREGMAN)

The constant term is correct because sum_i Pr_(p_i)[x in A]=m rho_x.
This permits an actual role/query transportation, not independent changes
to customer weights inside a whole IC. For p uniform on m labeled
comparison slots, the transport maximum is a maximum true-payoff perfect
assignment (with repeated theme slots still separately indexed).

The strongest transported true-payoff bank is

    H(p)=max_(TRANSPORT) sum_i E_(p_i)d_i(A)
        =min_(alpha_i+beta_A>=d_i(A))
                [sum_i alpha_i + m sum_A p(A) beta_A]. (T-DUAL)

The transport problem is finite; alpha,beta are unrestricted in sign.
Always H(p)<=W by the original actual-prefix ICs. A sufficient but
unproved relation would be m min_(L in K)F_p(L)<=H(p). This is stronger
than the shared-load cap itself, so it is not adopted as a required new
goal or claimed as progress. Merely optimizing the transport in
(T-BREGMAN) does not improve its full right side: the source IC slack
changes by exactly the same amount as the net curvature debt. That
cancellation must be retained.

For a pure p concentrated on A, the transported marginals force p_i=A.
Then the explicit feasible load L=(1/m)sum_i L_i(A) and Jensen give

    min_(K)F_A <= F_A(L) <= (1/m)sum_i d_i(A) <= W/m.

This proof does not extend to a mixed p by averaging the separate
minimizers, because the independently queried theme and selected load
must have the same common mixture. That mixed correlation is the unpaid
part of the parent's problem.

## Why the optimal-portfolio exchange gate is not an automatic payment

The earlier cross-role GATE selected an unweighted coverage-optimal
m-tuple minimizing frozen assignment cost. In contrast p here can be any
query distribution. At a minimizing shared load, menu weights q_i select
columns maximizing sum_x rho_x t_x^2 L_i(B)_x. This is a weighted repeated
load objective, not unweighted optimum coverage preservation. Thus GATE
cannot be applied to those q_i without a separate valid optimum-preserving
replacement construction. Neither fractional safety-optimal p nor a
KKT support column automatically supplies such a construction.

At m=5, (TRANSPORT) has row mass1 and column mass5p(A), and every displayed
identity still holds with the factor5. The mixed-query numerical payment
remains unproved; this is not an arbitrary-catalog five-player half proof.

## Last analytical attempt: active-query prices and the PSD tangent game

At a genuine shared minimax saddle, write M for the cap. Every active
query A has g_A(t)=M and every legal B satisfies g_B(t)<=M. Thus there is
an exact nonnegative price slack for a prospective token replacement:

    sum_(x in A minus B)t_x-sum_(x in B minus A)t_x
      =M-g_B(t)>=0.                                (ACTIVE-EXCHANGE)

This uses weighted query activity, rather than unweighted coverage
optimality, so it does apply to arbitrary saddle p. It gives no numerical
comparison between original payoff and this t-price by itself.

Fix the same t for every history. Put

    k_t(A,B)=sum_(x in A intersection B)t_x^2,
    v_t(A)=sum_(x in A)(2t_x-t_x^2).

At any full leaf with competitor load z for role i, reciprocal expansion
gives exactly

    u_i=v_t(A_i)-sum_(j!=i)k_t(A_i,A_j)+D_i(leaf),
    D_i(leaf)=sum_(x in A_i)
         t_x^2[z_x-L*_x]^2/(1+z_x)>=0.              (TANGENT)

The overlap kernel is a positive-semidefinite Gram kernel on the common
theme features t_x 1_(x in A). A possible strategy was to prove a robust
joint-payment inequality for the symmetric pairwise tangent game and then
retain all exact D defects. This was not accomplished. Original whole IC
at a real history only implies

    tangent_i(actual)-tangent_i(deviation)
      >=D_i(deviation)-D_i(actual).

The tangent game therefore does not inherit SPE. Applying a tangent-game
theorem for free would drop a branch-dependent curvature difference, and
paying many off-history comparisons from the same D_i(actual) would reuse
the bank. ACTIVE-EXCHANGE, the optimal-portfolio zero-loss GATE, and this
PSD representation have not supplied a joint one-IC-per-actual-role
payment. The present derivation stops at C<=D+sum IC, which remains open.
