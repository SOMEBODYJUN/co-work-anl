# Independent checks of the fixed-prefix and mean-cap shadow components

2026-10-25, matching12. Read aggregate12's
`../aggregate/fixed_prefix_shadow_component.md` and tree12's
`../tree/mean_cap_credible_shadow_working.md` in full. Both are general
components and expressly do not prove HALF or a new useful welfare bound.
No finite computation or policy scan was needed for these checks.

## Fixed actual-prefix inventory

Every deleted-current actual-prefix menu retains every prior actual action.
Consequently P=(1/m)sum_j(m-j)1_(B_j) and the selected genuine future load F
each have action mass(m-1)/2 and L=P+F. For j<i the coefficient
(m-j)/m is at least r_i/m, proving L_x>=P_x>=(r_i/m)b_i(x).

The ratio (b+r)/(1+rb/m) has derivative with sign1-r^2/m. Its endpoint
maximum over0<=b<=m-r is max{r,m^2/(m+mr-r^2)}. Combining with the true
one-step SPE floor proves the stated a_m(r), and direct substitution gives
B_5=1/5+1/4+1/3+11/25+9/25=19/12. The asymptotic B_m=(log m)/2+1/2+o(1)
also follows by splitting at sqrt(m). These signs and coefficients pass.

Qpast and Qfuture are exactly their weighted whole-theme price discounts,
so each is nonnegative and they sum to Qstat. This uses only
gamma=max_T g_t(T), not necessarily saddle KKT, hence is valid on the full
stated fixed-strategy shared domain. Their split is one wallet, not two.
The coarse consequence falls far short of the required9/2 at m=5.

## Mean-cap domains and dual cap-slack credit

The original, leafwise-truncated, per-action mean-cap, and global mean-cap
domain inclusions are correct. Actual-action endpoints are fixed. Every
allowed endpoint is a genuine tail-SPE endpoint at its own exact ordered
history; all averaged deleted-current loads have legal catalog mass m-1.
Mean-cap mixtures need not be original full SPEs, as the author states.

Finite LP duality gives Hi=eta_i+mu_i u_i, mu_i>=0, with
eta_i+mu_i d_i(A,e)>=w dot L_i(A,e) for every tagged endpoint. No sign on
eta is needed. Actual original source columns are among these endpoints,
so their reduced costs Ri(A)>=0 are legitimate. Substitution gives exactly

    G=sum_i[Hi-E_p w dot L_i^0(A)]
      =sum_i mu_i I_i+sum_i E_p Ri(A)>=0.

With the centered original-source covariance, C=Cov-G. Therefore

    W-m gamma=sum_i(1+mu_i)I_i+sum_i E_p Ri(A)+D-Cov.

All signs, the factor m, and the nonnegative banks check. The dual cap
price multiplies the original whole-query slack positively; it is not a
claim that mu_i u_i can be separately paid from W. G must not be spent
again after making this substitution.

For the per-action mean-cap source variant in section2, its I_i>=0 follows
from its conditional mean-cap definition, rather than a pure entering IC
for every selected endpoint. The note's distinction from a new SPE is
essential and adequate; sections3–5 instead use original source queries.

The residual covariance target and its Qstat half allowance are correct
conditional sufficient statements. No amount bound on Cov follows from
the domain/dual identities alone, and none is claimed. No fatal issue was
found in the stated components. External review and novelty are not
certified by this independent algebra/domain check.
