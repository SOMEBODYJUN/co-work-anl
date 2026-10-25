# Full-slot cap and norm bank: independent algebra review

2026-10-25, tree12. Source read:
[`../aggregate/full_slot_cap_dual_norm_bank.md`](../aggregate/full_slot_cap_dual_norm_bank.md).
Arbitrary original m/catalog/complete ordered-history pure SPE. **HALF and
FPAY remain OPEN.** This internal review checks signs, domains and the all-m
calibration, without a covariance theorem or external review claim.

Let original deleted source load be ell_i(A), full source C_i(A)=ell_i(A)+1_A,
original entering payoff d_i(A), reference full load L^+, t=(1+L^+)^-1,
rho=Pr_p[x in A], and w=rho t^2. The cap stays on d_i, not on extra-query
payoff. The full cap dual with original feasible queries gives

    G^+=m w dot L^+-sum_i E_p[w dot C_i(A)]
       =sum_i mu_i I_i+sum_i E_pR_i^+(A)>=0.

Since E_p[w dot 1_A]=sum rho_x^2 t_x^2,

    sum_i E_p[w dot(ell_i(A)-L^+)]=-G^+-m||rho t||^2.

Therefore C_0=Cov_0-G^+-m||rho t||^2 and the original deleted-source Taylor
expansion around the SAME full reference gives

    W-m gamma=sum_i(1+mu_i)I_i+sum_i E_pR_i^+(A)
                        +D_0-Cov_0+m||rho t||^2.

The norm uses rho squared, not rho. Every source tail is still original.
Reference mass m does not change the reciprocal identity's source
denominator 1+ell; D_0 correctly retains it.

For an independent cancellation check, adding the queried provider's own
indicator to source load gives

    C_+-C_0=m sum rho t^2,
    Cov_+-Cov_0=m sum rho(1-rho)t^2,
    D_+-D_0=m sum rho t^2-Tax.

Hence Tax+D_+-Cov_+=D_0-Cov_0+m||rho t||^2. Full-source tax, variance and norm
are not independent banks. Full mass m and whole-theme price <=gamma give
Q^+=m gamma-sum L^+t>=0 and OPT_m<=2m gamma-Q^+. Thus FPAY with Q^+/2 has
the correct sufficient direction and coefficient.

In the old all-big family, the stated p and t give z_x=rho_x t_x=1/(2m) for
all 2m-1 clients. Row mixture p has full big-client load m-1+p_big and
singleton load p_single, yielding exactly those t values. Every legal theme
has the same shadow weight (2m-1)/(4m^2), so unrestricted and capped shadow
optima agree. Original deleted loads are B^(m-1) for every query, hence
Cov_0=I=R^+=Q^+=0. Direct substitution gives

    m||z||^2=(2m-1)/(4m)=gamma/2,
    D_0=1/(4m),
    W-m gamma=1/2=m||z||^2+D_0.

This verifies the all-m calibration, including m=5, without a policy scan.
It gives no arbitrary-catalog adaptive covariance bound. The full cap dual
also does not automatically price non-credible deviation/reset leaves.
