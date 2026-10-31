# An action-marginal aligned credible-menu fixed point

2026-10-25, tree12. General original CAG input and arbitrary fixed original
complete pure SPE. **HALF and the payment at the fixed point below remain
OPEN.** This proves an existence component for a different analytical
coupling, not a shared minimax saddle theorem or new welfare bound.

Use conditional mean-cap lotteries from
[the mean-cap note](mean_cap_credible_shadow_working.md), retaining complete
pure tail-SPE witnesses and the original endpoint for every actual action.

## 1. Fixed feasible domain and existence

For each actual role i and forced A, let Q_iA be all lotteries over its
witnessed credible tail SPEs with expected entering payoff at most u_i.
For actual A=a_i this is the singleton original endpoint. The product
Q=product_(i,A)Q_iA is nonempty compact convex and independent of p.

For p in Delta(S), q in Q define

    L(p,q)=(1/m)sum_i sum_A p_A E_(e~q_iA)L_i(A,e),
    rho_x(p)=Pr_p[x in A],  t_x(p,q)=1/(1+L_x(p,q)),
    F_p(L)=sum_x rho_x(p)/(1+L_x),
    g_t(A)=sum_(x in A)t_x.

L(p,q) is a fractional legal catalog load of mass m-1. All these maps are
continuous. Consider the correspondence on Delta(S) cross Q,

    (p,q) -> P(p,q) cross M(p),
    P(p,q)=Delta(argmax_(A in S) g_t(A)),
    M(p)=argmin_(q' in Q) F_p(L(p,q')).

P has nonempty compact convex values and closed graph. For fixed p,
L(p,q') is affine in q' and F_p is convex, so M has nonempty compact convex
values. Its objective is continuous and its feasible compact Q is fixed;
Berge's theorem gives upper hemicontinuity and closed graph. Hence the
product correspondence meets Kakutani's hypotheses and has a fixed point
(p*,q*).

This is a mathematical fixed point. The p-response holds the already
produced load fixed; it is not claimed to maximize a payoff internalizing
the change of p inside L. No minimax interchange or mixed-SPE implementation
is invoked.

## 2. Price support and conditional shadow extremality

Write L*=L(p*,q*), t=(1+L*)^-1, rho=rho(p*) and
gamma=max_A g_t(A)=F_(p*)(L*). Every supported input action has price gamma;
every legal theme has price at most gamma. The q-minimization has derivative
shadow w_x=rho_x t_x^2. For p*_A>0, changing only q_iA has directional
derivative -p*_A/m times its shadow improvement. Thus every q*_iA with
p*_A>0 maximizes expected w dot L within its conditional Q_iA. APRICE from
the preceding note applies separately to each such mean-cap optimum.

The selected background action marginal is exactly the query p* at every
role. The shared minimax formulation instead permits background marginals
mu_i different from p*. Here gamma can be larger than that minimax value.
No small-gamma or uniqueness claim is made. The fixed-point set is compact,
so a point minimizing gamma among fixed points exists, but no bound on this
minimum is proved.

## 3. Exact source/background discount alignment

Draw the same conditional source query (A,e) from p*,q*_iA. Set

    I_i=u_i-E_(A,e)d_i(A,e)>=0,
    D=sum_i E_(A,e)sum_(x in A)
            t_x^2(L_i(A,e)_x-L*_x)^2/(1+L_i(A,e)_x),
    Cov=sum_(i,x)t_x^2 Cov_(A~p*)(1_(x in A),E_e L_i(A,e)_x).

The exact reciprocal expansion gives

    W-m gamma=sum_i I_i+D-Cov.                       (ALIGNED-BAL)

The decoupled linear term is zero because sum_i E_(A,e)L_i(A,e)=mL*.
Thus alignment trades the previous positive KKT gap for matching action
marginals; it does not retain both banks. I_i follows from the conditional
mean-cap definition, not from original IC at each cap-violating endpoint.
Every descendant IC still keeps its own genuine pure-SPE witness.

The fixed prefix/future split is L*=P+F, with

    P_x=(1/m)sum_j(m-j)1_(x in B_j),
    F_x=(1/m)sum_i E_(A,e)sum_(j>i)1_(x in Z_i(A,e)_j).

Both have mass (m-1)/2. Let

    Qpast=(1/m)sum_j(m-j)[gamma-g_t(B_j)]>=0,
    Qfuture=(1/m)sum_i E_(A,e)sum_(j>i)
                          [gamma-g_t(Z_i(A,e)_j)]>=0.

Then Qstat=(m-1)gamma-sum_x L*_x t_x=Qpast+Qfuture. The Qfuture here uses
exactly the source-query future leaves from ALIGNED-BAL. No replacement of
a distinct background action mixture by p is needed. This is a genuine
coupling relation, but it does not identify different witnesses' reset
leaves.

## 4. Weak target and actual stop

For any L* with the whole-theme price cap, standard static accounting gives
OPT_m<=(2m-1)gamma-Qstat. A sufficient amount at a favorable fixed point is

    Cov<=sum_i I_i+D+(gamma+Qpast+Qfuture)/2.          (ALIGN-PAY?)

No proof is supplied for every fixed point, or for existence of one that
satisfies ALIGN-PAY?. For m=5 this is W>=(9gamma-Qstat)/2 with the same unpaid
covariance. Thus the existence and alignment component does not give an
unconditional five-player or arbitrary-player HALF theorem.

A law-of-demand/variance proof can now try to spend source-future discounts
from the very leaves in its covariance expansion. It still must pay
standalone-error transfers and genuine off-branch resets with each bank
spent once. No finite scan was performed for this note.

## 5. Full-load variant

Replace the section 1 load map by the average FULL endpoint load
L^+(p,q)=L(p,q)+rho(p). For fixed p the q objective remains convex and the
conditional feasible domain is unchanged; the same Kakutani argument gives
a full-load fixed point with max-price support. Within an action A the own
load 1_A is fixed, so conditional shadow extremality is unchanged.

Keep the entering share payoffs d_i(A,e) and deleted source loads ell from
the SAME aligned conditional lotteries in Taylor, rather than extra-query
payoffs. These need not be the original sigma menus. Reference L^+ and
t=(1+L^+)^-1; the average deleted load is L^+-rho, so exactly

    W-m gamma=sum_i I_i+D_0-Cov_0+m||rho t||^2.

There is no G bank. This combines aggregate12's full-slot own-current term
with exact source/background action-marginal alignment. The current-action
price discount is zero because all supported A have g_t(A)=gamma. Thus
Q^+=Qpast+Qfuture, using precisely the source-query future expectation.
The sufficient amount is

    Cov_0<=sum I+D_0+m||rho t||^2+Q^+/2.

The full-slot signs and static implication are independently checked in
[the full-slot review](full_slot_norm_independent_review.md). This variant
does not inherit minimax-small gamma and does not prove the covariance
target. It does not count the absent G bank, or tax/norm variance twice.

Credible11 independently checked the fixed feasible product domain,
continuity/convexity, both response correspondences and Kakutani existence
from the exact contract. It also checked shadow maximality only on supported
actions, absence of a minimax claim, G=0, and exact Qfuture alignment.
This internal review covers the existence/alignment component, not either
unproved covariance amount or an original-game lottery implementation.
