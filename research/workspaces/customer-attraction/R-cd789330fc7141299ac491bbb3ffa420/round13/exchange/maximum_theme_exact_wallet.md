# Exact maximum-theme wallet, usable at every actual position

2026-10-25. Original five-provider model, arbitrary finite unit customers,
arbitrary finite common nonempty catalog and every complete-history pure
SPE. **General HALF(5) remains OPEN.** This is an exact local payment and
a conditional root consequence, not a complete target proof. No external
review or novelty claim. **Source correction:** after deriving this, parent
identified the same arbitrary-position general-m BNS extension in
`R-acd974.../coverage_exchange/player_near_saturation_extension.md` (2026-10-21).
Its statement already yields both displayed coefficients at m=5. This is
an independent exact residual certificate/reconstruction of that OLD
mechanism, not a new mathematical improvement. The coefficient16 was also
suggested by parent13's floating local-envelope LP.

Let C be a largest catalog theme, L=|C|, and set

    F_C(T)=|T minus C|+|T intersection C|/5.

For every actual provider i with final payoff u_i and every legal T,

    F_C(T)<=16u_i-3L.                            (ALL-ROWS)

For the last actual provider there is the stronger bound

    F_C(T)<=11u_5-2L.                            (LAST)

These retain actual payoff caps. They do not compare a frozen suffix.

## Nonterminal actual positions

At any actual i<=4 force C and follow the original strategy. There are
five terminal themes: C, the genuine final response R_5, and three other
themes R_2,R_3,R_4. Those other themes may include past actual themes;
their numbering is only for this calculation. All have size at most L.
Write d for the forced C player's final payoff and v for the final
player's payoff. The actual-prefix IC gives d<=u_i. The final node gives
v>=U_5(T) in this SAME terminal prefix.

The exact inequality is

    16d-3L-F_C(T)
      =sum_(k=2)^4 [L-|R_k|]/2+[L-|R_5|]
         +[v-U_5(T)]+sum_x rho_x.                 (WALLET)

Every displayed slack is nonnegative. To verify rho pointwise, let a,t,l
be membership in C,T,R_5 and p the number of R_2,R_3,R_4 containing x.
Put c=a+p+l, and set zero-numerator fractions to zero. Direct expansion:

    rho=16a/c-11a/2+p/2+l-l/c
         +t/(a+p+1)-t(1-4a/5).

If a=0,l=0, rho=p/2+t/(p+1)-t>=0 for integer p=0,1,2,3.
If a=0,l=1, its minimum over t is p/2>=0.
If a=1, the coefficient of t is 1/(p+2)-1/5>=0. Its constant term is:

| l | p=0 | p=1 | p=2 | p=3 |
|---|---:|---:|---:|---:|
|0|21/2|3|5/6|0|
|1|3|1|1/4|0|

Thus rho>=0 for EVERY client type. WALLET and d<=u_i prove ALL-ROWS for
i<=4. No other branch player is assumed to maximize its payoff after a
forced earlier action; only the genuine last node is used.

## Last actual position

Let b_x be the load of the four actual prefix themes. The last player's
query to C is q_C=sum_(x in C)1/(b_x+1)<=u_5. Let

    E=sum_(x in C)(4-b_x).

For b=0,1,2,3,4,

    4-b<=20[1/(b+1)-1/5],

so E<=20(u_5-L/5). The four prefix themes each have size at most L;
therefore their total incidence OUTSIDE C is at most E. On C the terminal
query T earns at least 1/5 per interested client. Outside C, its discount
from a full unit is b/(b+1)<=b/2. Hence its true last-node utility satisfies

    U_5(T)>=F_C(T)-E/2.

The actual last-node IC gives U_5(T)<=u_5. This proves LAST. Also
u_5>=L/5, so 11u_5-2L<=16u_5-3L, establishing ALL-ROWS for i=5.

## Root-level amount and remaining range

For any optimal five-tuple T_1,...,T_5, clientwise coverage gives

    OPT_5<=sum_j F_C(T_j)+4L/5.

Together with ALL-ROWS this yields the unconditional amount relation

    OPT_5<=80 min_i u_i-71L/5<=16W-71L/5.

Consequently L>=70W/71 is a sufficient condition for HALF(5). If provider5
has minimum payoff, LAST instead gives OPT_5<=11W-46L/5, so L>=45W/46
suffices in that case. L=0 gives the zero-customer conclusion immediately.

The remaining L/W range is not controlled by these wallets. Neither a
finite LP optimum nor the displayed conditional consequence proves the
full five-player target. The useful additional information is that the
same maximum-theme query can be paid from EACH actual payoff separately,
including the last position, rather than only from the root payoff.
