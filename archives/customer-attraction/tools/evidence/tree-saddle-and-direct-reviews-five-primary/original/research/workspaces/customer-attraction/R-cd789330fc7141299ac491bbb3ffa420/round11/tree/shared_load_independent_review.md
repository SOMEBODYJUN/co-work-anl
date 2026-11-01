# Shared-load Bregman relation: independent algebra and full-tree tangent view

2026-10-25, tree11. General finite common catalog, arbitrary player count,
unit clients/providers, every complete ordered-history pure SPE; arbitrary
ties, repeated themes, empty themes and zero clients remain allowed.
**Q-CAG-HALF and shared-load aggregate payment remain OPEN.**

This is an internal independent algebra/domain review of
[`../parent/shared_load_bregman_working.md`](../parent/shared_load_bregman_working.md),
followed by a direct attempt. It is not a universal covariance bound or a
claim of external review/novelty. No numerical nonseparation is used here.

## 1. Compact convex domain and sufficient bound

At actual role i, let L_i(A) be the client load of its original forced-A
completion after deleting that current role. Past actual actions stay fixed;
the original strategy specifies every subsequent ordered history. Put

    K=(1/m) sum_i conv{L_i(B): B in S}.

K is a nonempty compact convex polytope. Its elements are fractional legal
catalog loads of total provider mass m-1: each deleted leaf is a legal
(m-1)-topic tuple, and convex combinations/averaging preserve that property.
Nothing says that such a load is itself a pure-SPE terminal profile.

For p in the catalog simplex, rho_x=Pr_p[x in A] and

    F_p(L)=sum_x rho_x/(1+L_x).

This is linear in p, continuous, and convex in L. Finite-dimensional convex
minimax therefore interchanges max_p min_L and min_L max_p. Thus the proposed
bound min_(L in K) F_p(L)<=W/m for every p does imply that one shared load has
every legal query payoff at most W/m. Because K is contained in the full
fractional (m-1)-provider domain, its minimax value is at least the true full
fractional static security value. This verifies the stated sufficient route;
it does not prove the proposed bound.

## 2. KKT support condition, including arbitrary realizations

Fix p and a minimizer L*. Set t_x=1/(1+L*_x), w_x=rho_x t_x^2.
For any realization

    L*=(1/m)sum_i sum_B q_i(B)L_i(B),

every B with q_i(B)>0 maximizes w dot L_i(B). Indeed the gradient of F at L*
is -w, and replacing this one supported column by another legal column is a
feasible one-sided direction. A smaller w dot supported column would give a
strictly negative directional derivative. This also covers nonunique
realizations and zero-rho coordinates; no division by rho is needed.

In particular the following gap is nonnegative:

    G_KKT=m w dot L* -sum_i E_(A~p)[w dot L_i(A)] >=0.       (KG)

This is the precise decoupled linear inequality. It does not weight a column
by its own query's membership indicator.

## 3. Exact residual and a nonnegative KKT bank

Write alpha_Ax=1[x in A], z_iAx=L_i(A)_x. Each query payoff is

    d_i(A)=sum_x alpha_Ax/(1+z_iAx).

The current role's actual-prefix IC gives
IC_i=u_i-E_p d_i(A)>=0, with one whole legal query per A. The elementary
reciprocal identity in the parent file gives exactly

    W-mF_p(L*)=sum_i IC_i-C+D,
    C=sum_i E_A sum_x alpha_Ax t_x^2(z_iAx-L*_x),
    D=sum_i E_A sum_x alpha_Ax t_x^2(z_iAx-L*_x)^2/(1+z_iAx)>=0.

All denominators are positive. For zero-rho coordinates alpha=0 almost
surely, so their terms vanish without exceptional conventions.

Subtracting the decoupled membership rho gives the more explicit exact form

    W-mF_p(L*)=sum_i IC_i+G_KKT+D-Cov,
    Cov=sum_(i,x)t_x^2 Cov_(A~p)(alpha_Ax,z_iAx).           (BUDGET)

KG is a genuine consequence of shared-load minimization. BUDGET still needs
Cov<=sum IC+G_KKT+D. It is not a proof that this inequality holds. No sign for
Cov follows from KG; replacing alpha_Ax by rho_x inside C discards exactly
this unpaid adaptive correlation. This is the specific full-tree obligation
left after the independently checked algebra.

## 4. A fixed quadratic tangent game on the original complete tree

For any fixed nonnegative t and every original terminal load c>=1,

    1/c=(2t-t^2 c)+(1-t c)^2/c.                           (TAN)

Thus define, only for algebraic evaluation of the original tree,

    v_i^t(Z)=sum_(x in Z_i)(2t_x-t_x^2 c_x(Z)),
    E_i^t(Z)=sum_(x in Z_i)(1-t_x c_x(Z))^2/c_x(Z)>=0.

Then u_i(Z)=v_i^t(Z)+E_i^t(Z), exactly. The tangent utility has a fixed
symmetric pairwise interaction kernel t_x^2:

    v_i^t(Z)=sum_(x in Z_i)(2t_x-t_x^2)
                  -sum_(j!=i)sum_(x in Z_i intersect Z_j)t_x^2.

For a genuine original node h and forced A completion Z_hA,

    v_i^t(Z_h)-v_i^t(Z_hA)
        =Gamma_hA-E_i^t(Z_h)+E_i^t(Z_hA)
        >=-E_i^t(Z_h).

This retains the two original real leaves and their exact signed error. It
does not assert that sigma is an SPE of the tangent game; tangent payoffs may
also be negative. Its symmetric quadratic potential is

    Phi_t(Z)=sum_x[2t_x c_x(Z)-t_x^2 c_x(Z)(c_x(Z)+1)/2],

whose formal one-role deletion marginal is v_i^t(Z). On one complete leaf,

    sum_i E_i^t(Z)=sum_(x:c_x(Z)>0)(1-t_x c_x(Z))^2.        (ONE-LEAF)

At t=(1+L*)^-1, the D in section 3 is exactly the p-average of these query
errors. The fixed pairwise kernel removes the tail-dependent reciprocal
Hessian from the comparison. This may be a useful representation for a new
coupling theorem, but no such theorem was proved here. ONE-LEAF cannot pay
errors taken from mutually exclusive complete leaves with one actual bank.
Likewise the exact potential does not make an earlier player's adaptive
deviation a potential difference: the other players' deletion profile also
changes.

## 5. Five-player pressure and actual stop

Substituting m=5 preserves all the above identities, KG, and the proposed
sufficiency min_K F_p<=W/5. BUDGET still contains the unpaid weighted Cov.
No unconditional OPT_5<=2W, general welfare improvement, or target
counterexample follows. This review verifies a correct common-load interface
and identifies its exact covariance/payment obligation; it does not count an
equivalent residual decomposition as closure or as new money.
