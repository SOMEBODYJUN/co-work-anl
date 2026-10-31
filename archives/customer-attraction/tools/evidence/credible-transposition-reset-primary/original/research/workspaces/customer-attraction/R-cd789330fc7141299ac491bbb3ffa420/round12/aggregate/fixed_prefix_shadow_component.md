# The fixed-prefix part of every shared shadow load

2026-10-25. Original arbitrary-m/catalog/full-history HALF remains OPEN. This is an unconditional relation on the shared menu domain, with a deliberately coarse dynamic consequence. It does not improve the existing general welfare theorem. The coarse consequence fails the five-player value pressure and is not continued as a coefficient project.

Fix one original complete pure SPE sigma, actual path S_1,...,S_m and utility sum W. For each actual role i force B, execute the same sigma, delete current i, and let ell_i(B) be the competitor load. Choose any independent column mixtures q_i and set

    L=(1/m) sum_i E_(B~q_i) ell_i(B),
    t_x=1/(1+L_x),   g_t(A)=sum_(x in A)t_x,
    gamma=max_A g_t(A).

No minimizer or saddle assumption is needed in the next relation. Let b_i be the actual old-player customer load and r_i=m-i+1.

## 1. Exact past/future split

For every chosen L in the shared domain,

    L=P+F,
    P_x=(1/m)sum_(j=1)^m (m-j)1_(x in S_j),
    F_x=(1/m)sum_i E_B sum_(j>i)1_(x in Z_i(B)_j).

P is fixed by the actual path; F consists of genuine future actions in the selected actual-prefix branches. Both are fractional catalog loads of total action mass (m-1)/2. Therefore

    L_x >= P_x >= (r_i/m)b_i(x)                 (PREFIX)

for every actual i and client x: each of the r_i rows at or after i retains b_i in its past. This is not a prefix lower bound at arbitrary off-path histories.

For every chosen L above, the known static credit Qstat=(m-1)gamma-sum_x L_x t_x decomposes exactly into two separately nonnegative parts. No joint saddle or KKT assumption is needed, only gamma=max_A g_t(A):

    Qpast=(m-1)gamma/2-sum_x P_x t_x
         =(1/m)sum_j(m-j)[gamma-g_t(S_j)] >=0,
    Qfuture=(m-1)gamma/2-sum_x F_x t_x
         =(1/m)sum_i E_B sum_(j>i)[gamma-g_t(Z_i(B)_j)] >=0.

Thus the existing credit records explicit weighted price discounts of actual actions and of selected real future actions. This split does not produce a second copy of Qstat, nor does it control price discounts in different p-query branches. In particular q_i and the active query distribution p need not agree. The unresolved reset transport cannot silently replace q_i by p.

If Qstat=0, all actual S_j with j<m, and every future action occurring with positive q_i weight in these selected menus, have maximal shadow price gamma. This narrows the equality case of the old static comparison; it is not a separate restricted-instance research project or a proof of that case.

## 2. An unconditional, but weak, actual-profit floor

The ordinary true one-step SPE guarantee is

    u_i >= max_T sum_(x in T) 1/[b_i(x)+r_i].

By PREFIX, t_x<=1/[1+(r_i/m)b_i(x)]. Since 0<=b_i(x)<=m-r_i,

    t_x[b_i(x)+r_i]
      <= max{r_i, m^2/[m+m r_i-r_i^2]}.

The maximum follows by differentiating the fractional linear function (b+r)/(1+rb/m), or by comparing its two endpoints. Thus, using a legal maximizer of g_t,

    u_i >= gamma a_m(r_i),
    a_m(r)=min{1/r, (m+mr-r^2)/m^2}.

Summing yields the all-input relation

    W >= gamma B_m,
    B_m=sum_(r=1)^m a_m(r).                     (COARSE)

It holds for every L in the fixed strategy's shared domain, hence in particular for its minimax gamma. Empty themes and zero clients are covered without division by gamma; m=1 gives a_1(1)=B_1=1. The inequality uses the true actual-prefix one-step guarantee, so full-history SPE is not weakened to a fixed follower profile. It does not require guessing mixed actions a player can secretly commit to.

For r>=sqrt(m), a_m(r)=1/r. For r<=sqrt(m), it is the quadratic expression. Consequently B_m=(log m)/2+1/2+o(1). This is far smaller than the needed m-1/2.

## 3. Value pressure and honest stop

The same formula gives

    B_5 = 1/5+1/4+1/3+11/25+9/25 = 19/12.

It only proves W>=(19/12)gamma, whereas the stronger HALF-SHARED sufficiency asks W>=(9/2)gamma. Even combining COARSE with OPT_5<=9gamma gives a weak constant 108/19, worse than already proved five-player bounds. This is an unconditional shared-domain relation, not a new useful five-player welfare result.

The formula uses no actual successor optimality beyond the ordinary one-step guarantee. Its inability to close is therefore unsurprising: real off-path successor IC must provide the missing common money. Continuing to optimize this one-variable endpoint estimate would not address that gap.

The possible remaining use is the exact split of Qstat into actual and selected-future price discounts, so a future real reset proof can specify which terms it spends. No such map has been constructed here. The original weak target is still

    C<=D+I+(gamma+Qstat)/2.

This note does not pay it and does not turn VAR, the existing static credit or the prefix load bound into additional independent funds.

## 4. Independent internal check

Matching11 independently checked the domain, the coefficient inequality (m-j)/m>=r_i/m for every j<i, the fractional-linear endpoint derivative 1-r^2/m, both action masses, both discount identities and B5=19/12. The review also noted and corrected an unnecessarily narrow saddle assumption on Qpast/Qfuture: nonnegativity holds for any chosen L with gamma=max_A g_t(A). This is internal algebra review, not a new full-tree audit, external review or novelty certification.
