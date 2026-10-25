# Independent check of direct11's terminal/shared-saddle complement identity

2026-10-25, matching11. General input class unchanged; no new welfare bound
is proved. This reviews the exact interface sent by direct11, not a claimed
payment of its residual inequality.

Let b be the actual prefix load before the final player, P=supp b, S the
actual last action, and rho the query inclusion marginals. Actual final
profit u_m is sum_(x in S)1/(b_x+1). The true final-query value is
d_m(A)=sum_(x in A)1/(b_x+1). Therefore

    W-u_m=sum_(x in P)b_x/(b_x+1)
                +sum_(x in P minus S)1/(b_x+1),
    E|A|-E d_m(A)=sum_(x in P)rho_x b_x/(b_x+1).

With IC_m=u_m-E d_m(A)>=0, subtracting these gives exactly

    W-E|A|=IC_m+B,
    B=sum_(x in P)(1-rho_x)b_x/(b_x+1)
        +sum_(x in P minus S)1/(b_x+1)>=0.          (TERM)

No term on a query-covered but actually unserved customer is dropped: it
is present in E|A| and E d_m(A), hence cancels in their difference, and
its true last-query benefit is retained in IC_m.

At a global shared-load saddle put t_x=1/(1+L*_x), V=max_A sum_A t_x.
The background is total mass m-1 of legal topics, so

    Q=(m-1)V-sum_x L*_x t_x>=0.

This follows by integrating the valid pointwise bound sum_A t_x<=V against
that fractional topic mass; no pure-background assumption is used. Query
activity gives V=sum_x rho_x t_x, and then

    E|A|-V=sum_x rho_x L*_x t_x.

Combining with TERM yields the exact all-input interface

    W-mV=IC_m+B-Q-sum_x(1-rho_x)L*_x t_x.           (COMP)

Every displayed bank/demand term is nonnegative. COMP still needs
Q+sum(1-rho)L*t<=IC_m+B. It is an exact restatement of the requested cap
with a useful terminal bank, not a proof of that inequality. The last
IC is truly static because this is the actual terminal node; no earlier
player's continuation was frozen.

All signs/factors and all-customer boundaries check. Empty topics,
repeated topics, and m=1 cause no denominator problem. Direct substitution
m=5 gives W-5V=IC_5+B-Q-sum(1-rho)L*t; its mixed demand is still unpaid.
