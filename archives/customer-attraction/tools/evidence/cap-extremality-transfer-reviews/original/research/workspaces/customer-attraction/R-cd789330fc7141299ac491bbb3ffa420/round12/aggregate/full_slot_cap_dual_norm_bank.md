# Full-slot cap dual and the self-overlap norm bank

2026-10-25, continuation after the coarse prefix estimate failed value pressure. General HALF remains OPEN. This combines the current mean-cap dual with full-slot static backgrounds, keeping every source query in the ORIGINAL complete SPE. There is an explicit nonnegative term, but no bound on the remaining covariance and no new welfare theorem.

Tree12/credible12 developed the deleted global mean-cap domain and CAP-SLACK; see `../tree/mean_cap_credible_shadow_working.md`. Full-slot insertion discounts/terminal payments already appear in peer R-d3981c0168644971803a9c3380ed687c/round6_general/convex/terminal_pooled_full_payment.md and R-e7c3c9a51d38458aa551eec469e04cf2/global/README.md. Those mechanisms are not claimed new. Here the combined full-slot cap-dual is expanded directly against ORIGINAL deleted source loads, retaining m||rho t||^2.

## 1. Full analytical domain, original sources

Fix the actual tuple B, utilities u_i and complete ordered-history pure SPE sigma. At actual prefix h_i, each endpoint e after forcing A has a genuine complete pure tail-SPE witness. The actual-action tag keeps only the original actual endpoint. Write d_i(A,e) for entering utility, ell_i(A,e) for deleted-entering-role load and C_i(A,e)=ell_i(A,e)+1_A for complete load. Define

    D_i^+={E_q C_i(A,e): E_q d_i(A,e)<=u_i},
    K^+=(1/m)sum_i D_i^+.

These are analytical convex background domains, not executable SPE lotteries. Every background is a fractional legal catalog load of mass m. Sources remain ell_i^0(A),d_i^0(A)<=u_i from ORIGINAL sigma; selected endpoints do not replace them.

At a joint saddle let L^+ be its full background, t=(1+L^+)^-1, rho_x=Pr_p[x in A], w=rho t^2 and gamma=F_p(L^+). All whole-theme t-prices are <=gamma; supported queries have equality. For H_i^+=max_(D_i^+) w dot C, the finite cap dual gives mu_i>=0,eta_i with

    H_i^+=eta_i+mu_i u_i,
    eta_i+mu_i d_i(A,e)>=w dot C_i(A,e).

With ORIGINAL quantities

    I_i=u_i-E_p d_i^0(A)>=0,
    R_i^+(A)=eta_i+mu_i d_i^0(A)-w dot C_i^0(A)>=0,

one obtains exactly

    G^+=sum_i[H_i^+-E_p(w dot C_i^0(A))]
       =sum_i mu_i I_i+sum_i E_pR_i^+(A).        (FCAP)

## 2. Deleted source around a full background

Use the ORIGINAL deleted ell_i^0 in Taylor, always around the SAME full L^+:

    Cov_0=sum_(i,x)t_x^2 Cov_p(1_(x in A),ell_i^0(A)_x),
    D_0=sum_i E_A sum_(x in A)
       t_x^2[ell_i^0(A)_x-L_x^+]^2/[1+ell_i^0(A)_x]>=0.

The current source indicator has mean overlap

    sum_i E_p[w dot 1_A]=m sum_x rho_x^2 t_x^2.

Consequently exact reciprocal Taylor expansion gives

    W-m gamma
      =sum_i(1+mu_i)I_i+sum_i E_pR_i^+(A)
                 +D_0-Cov_0+m||rho t||_2^2.     (FNORM)

This is an all-input identity, not a covariance estimate. Whole ICs remain original; no customer-wise IC weighting is used.

For an independent sign check, define Cov_+,D_+ with full source loads but the same reference L^+. Let Tax=sum_i E_A sum_(x in A)1/[(1+ell_i^0(A)_x)(2+ell_i^0(A)_x)]. Then

    Cov_+=Cov_0+m sum_x rho_x(1-rho_x)t_x^2,
    D_+=D_0+m sum_x rho_x t_x^2-Tax,
    Tax+D_+-Cov_+=D_0-Cov_0+m||rho t||_2^2.

Tax, Bregman differences and self-overlap norm are therefore not independent credits. FNORM is their combined balance after exact cancellation.

## 3. Only the full-slot HALF requirement

The old static comparison, with slack retained, is

    Q^+=m gamma-sum_x L_x^+t_x>=0,
    OPT_m<=m gamma+sum_x L_x^+t_x=2m gamma-Q^+.

It suffices to prove

    Cov_0<=sum_i(1+mu_i)I_i+sum_i E_pR_i^+(A)
                     +D_0+m||rho t||_2^2+Q^+/2. (FPAY?, OPEN)

This does not require W>=m gamma when Q^+>0. Uniform role mass is retained; no comparison to free-position Mpath is made. For corresponding deleted/full endpoint domains one has gamma^+<=gamma^- by adding current action load to the SAME endpoint lottery, but their different static coefficients remain.

For m=5, FPAY? would give OPT_5<=10gamma-Q^+<=2W. The amount inequality is still unproved; no arbitrary five-player theorem follows.

## 4. Effective density and the standard tight family

Set z_x=rho_x t_x, so gamma=sum_x z_x. On coordinates z_x>=1/(2m), the already identified norm bank pays half that query price: m z_x^2>=z_x/2. The low-z deficit is sum(z_x/2-mz_x^2). Low z does not imply private clients, independent seats or a shared payment. No low-z theorem is asserted.

For calibration use the old all-m big-theme/singletons family: one theme contains m clients, the other m-1 disjoint themes each one client, actual SPE all-big. The unrestricted full fractional saddle, also feasible in this full mean-cap domain, is

    gamma=(2m-1)/(2m),
    p_big=m/(2m-1), p_single=1/(2m-1),
    t_big=(2m-1)/(2m^2), t_single=(2m-1)/(2m).

Forcing a singleton has a credible all-big tail and entering utility one; the actual all-big entering utility is also one. The same row mixture p realizes the stated full load. Its gradient values for big and singleton background actions are equal, certifying the unrestricted convex saddle and, by feasibility, this domain's saddle.

Every client has z_x=1/(2m). ORIGINAL deleted source backgrounds are always B^(m-1), so Cov_0=I=R^+=Q^+=0 and

    m||z||^2=gamma/2,
    D_0=1/(4m),
    W-m gamma=1/2=m||z||^2+D_0.

At m=5 this gives gamma9/10, norm9/20, D_0=1/20 and OPT_5=9=10gamma. This is one general-family calibration, not arbitrary five-player HALF.

## 5. Exact remaining obstruction and review

The cap dual controls common weight rho t^2 against whole credible endpoint loads. Cov_0 uses conditional indicator1_A at each original query. Neither FCAP nor the high-z elementary estimate bounds its low-z adaptive part. Successor IC must couple that amount to the SAME original-source D_0/I or SAME chosen endpoint dual reserve R^+. I have not derived that transfer.

Tree12 and credible12 independently checked FNORM, the coefficient m sum rho^2 t^2 (rather than m sum rho t^2), the ORIGINAL cap/source distinction, Q^+ signs and the exact static/payment implication. Their checks do not certify FPAY? or external novelty. No finite scan was run for this continuation. This is further work after the coarse prefix bound, not an endpoint refinement or a new general welfare result.
