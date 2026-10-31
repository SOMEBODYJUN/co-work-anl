# Credible mean-cap shadow menus and cap-slack credit

2026-10-25, tree12. Arbitrary finite unit-client common catalog, arbitrary
unit providers, and an arbitrary given complete ordered-history pure SPE.
**General HALF, weak shared-cap payment and m=5 HALF remain OPEN.**

Root proposed offactual first-deviation SPE reselection under entering-payoff
caps. Credible11 independently derived the mean-cap analytical relaxation in
parallel with tree12. This note separates its domains and derives exact
cap-slack credit in the shared KKT bank. No auxiliary mean-cap lottery is
called a new original-game pure or mixed SPE.

## 1. Fixed outcome, credible witnesses, and three domains

Fix original sigma, actual tuple B, utilities u_i and coverage W. Put
h_i=B_<i, a_i=B_i. For A!=a_i let E_i(A) be all complete pure tail SPEs after
the exact ordered history (h_i,A), with their endpoint profiles. Distinct
policies sharing an endpoint can retain distinct witness labels. Write
d_i(A,e) for entering payoff and L_i(A,e) for deleted-entering-role load.
For A=a_i allow only the original actual endpoint: d_i=u_i and
L_i=c(B)-1_(a_i). No continuation leaf is identified across witnesses.

The leafwise-cap domain deletes each e with d_i(A,e)>u_i before convexifying.
It preserves genuine pure selectors on disjoint first-deviation children.
It does not automatically admit a supporting scalar cap multiplier at every
maximal surviving endpoint.

Two larger analytical domains must be distinguished:

    D_i^action(A)={E_q L_i(A,e): q over E_i(A), E_q d_i(A,e)<=u_i},
    K_action=(1/m)sum_i conv(union_A D_i^action(A));

    D_i^global={E_q L_i(A,e): q over tagged (A,e), E_q d_i(A,e)<=u_i},
    K_global=(1/m)sum_i D_i^global.

Actual-action endpoint columns remain fixed in both definitions. Original
sigma makes every cap feasible. These are compact convex polytopes, with

    K_original subset K_leafwise subset K_action subset K_global.

Every element is a fractional legal catalog load of total provider mass m-1.
Mean-cap lotteries can contain individual cap-violating endpoints; hence no
new pure-SPE completion or unaugmented mixed-SPE implementation is claimed.

They remain legal analytical proof domains: original B,u,W are fixed; each
component tail witness is a genuine original-game pure tail SPE; and its
whole ICs can be averaged nonnegatively. One must keep each IC's real
deviation leaf inside its own witness. Conditional query caps do not follow
from only the global mean cap.

## 2. Per-action cap prices and choice-dependent sources

For fixed nonnegative client shadow w, the finite mean-cap LP has exact dual

    max_(q:E_q d<=u_i) E_q[w dot L]
      =min_(lambda>=0)[lambda u_i+max_e(w dot L_e-lambda d_e)].

At an optimal lottery q and dual lambda,

    lambda(u_i-E_qd)=0,
    w dot(L_e-E_qL)<=lambda(d_e-E_qd)   for every credible e. (APRICE)

This is strong duality for the mean-cap LP, not the leafwise-truncated set.
APRICE does not bound lambda or fund lambda u_i from W.

At a saddle for K_action, let t=(1+L*)^-1 and w=rho t^2. In a realization of
L*, every positive-weight action component must maximize shadow within its
D_i^action(A). Retain those lotteries, preserving L*, and choose any such
maximizer for unused actions. Every source query now has an explicit
conditional lottery q_iA with E_e d_i(A,e)<=u_i. The reciprocal expansion,
including endpoint variance, is then exactly W-m gamma=sum I-C+D, with
I_i=u_i-E_(A,e)d_i(A,e)>=0. Reciprocal of mean load cannot replace mean
reciprocal in its I or D terms.

## 3. Global cap with original source queries

For K_global keep source queries from ORIGINAL sigma:

    L_i^0(A)=original forced-A deleted load,
    d_i^0(A)=original forced-A payoff<=u_i.

These source columns are feasible in D_i^global. Thus every source IC/reset
comparison still has one original complete tree. Only the independent static
background uses enlarged analytical menus.

At a minimax saddle (p,L*), define rho_x=Pr_p[x in A], t_x=(1+L*_x)^-1,
w_x=rho_x t_x^2 and gamma=F_p(L*). All legal themes have t-price <=gamma,
and p-supported themes have equality. If L*=(1/m)sum_i bar L_i, every bar L_i
maximizes w dot L on D_i^global. Denote its value H_i. Then

    sum_i H_i=m w dot L*=m(gamma-sum_x rho_x t_x^2).

The role-i global LP has exact dual prices mu_i>=0 and eta_i in R:

    H_i=eta_i+mu_i u_i,
    eta_i+mu_i d_i(A,e)>=w dot L_i(A,e)  for all tagged endpoints. (GDUAL)

No sign eta_i>=0 is asserted. Actual-action tags are fixed original
endpoints. High-d offactual endpoints remain in this dual comparison because
the global cap constrains their mixture's entering payoff.

GDUAL compares child-SPE endpoint profiles only. A unilateral deviation leaf
inside a genuine witness need not itself be an endpoint of a complete SPE
after the entering history: its deviating role need not be best responding.
Therefore GDUAL cannot automatically be applied to every original reset leaf.
Such an application needs a separate credible-realizability argument or an
explicitly larger analytical raw-tail domain; neither is supplied here.

## 4. Nonnegative cap-slack credit in the KKT gap

For each original source query define

    R_i(A)=eta_i+mu_i d_i^0(A)-w dot L_i^0(A)>=0,
    I_i=u_i-E_p d_i^0(A)>=0.

The shared KKT gap against original source columns is

    G=sum_i[H_i-E_p(w dot L_i^0(A))]>=0.

Substituting GDUAL gives the exact relation

    G=sum_i mu_i I_i+sum_i E_p R_i(A)
      >=sum_i mu_i I_i.                              (CAP-SLACK)

Thus cap extremality contributes additional nonnegative credit from original
whole-query IC slack. It does not require or imply sum_i mu_i u_i<=W.
Large mu_i by itself is not a loss: here it multiplies I_i in a positive
bank. Reduced costs are nonnegative as well.

Using the ORIGINAL source queries, exact reciprocal expansion yields

    W-m gamma=sum I-C+D
             =sum_i(1+mu_i)I_i+sum_i E_pR_i(A)+D-Cov, (GBAL)

where

    C=sum_i E_p sum_(x in A)t_x^2(L_i^0(A)_x-L*_x),
    D=sum_i E_p sum_(x in A)
              t_x^2(L_i^0(A)_x-L*_x)^2/(1+L_i^0(A)_x),
    Cov=sum_(i,x)t_x^2 Cov_p(1_(x in A),L_i^0(A)_x).

Here C=Cov-G. Every selected background witness is a separate genuine tail
SPE; GBAL does not identify it with an original source leaf. CAP-SLACK is a
valid additional cap-frontier relation, not a proof its banks pay Cov.

## 5. Static slack and actual stopping point

Let Qstat=(m-1)gamma-sum_x L*_x t_x>=0, using fractional catalog legality
and the saddle whole-theme price bound. Standard static client accounting
gives OPT_m<=m gamma+sum L*t=(2m-1)gamma-Qstat. Therefore the precise
sufficient remaining payment is

    Cov<=sum_i(1+mu_i)I_i+sum_i E_pR_i(A)+D
                                    +(gamma+Qstat)/2.       (PAY?)

Equivalently W>=[(2m-1)gamma-Qstat]/2 suffices. At m=5 this is
W>=(9gamma-Qstat)/2, with every domain and CAP-SLACK unchanged. PAY? remains
unproved, so no unconditional five-player or arbitrary-player HALF follows.

No joint endpoint descent or covariance bound was found. An uncapped
credible endpoint improving shadow is priced by APRICE/GDUAL, not yet paid
by the actual wallet. The domains, dual and cap-slack relation are retained
without claiming a welfare improvement. No finite scan or fixed-player
positive project was performed in this round.

Credible11 independently reviewed sections 1 and 3--5, and matching11
independently checked sections 1--5. Both passed domain/dual/CAP-SLACK/GBAL
algebra and weak sufficiency, without any covariance amount. Credible11's
additional scope warning about non-credible deviation leaves is retained
above. These are internal checks, not external review or new welfare claims.
