# Eliminating a genuine final reply menu in any two-player tail

Status: exact necessary inequality, independently reconstructed by parent
from its three original SPE comparisons. This is an application of the
existing one-successor portfolio cancellation, not a new HALF(5) proof or
a claim of novelty. HALF(5) and unrestricted Q-CAG-HALF remain OPEN.

## Exact domain and statement

Use CAG-MODEL with an arbitrary finite unit-customer set, a finite nonempty
common catalogue, and any complete ordered-history pure SPE. Fix any
genuine history with exactly two players remaining. Let its old load be
`p_x`, its prescribed actions be `D,E`, and its two final payoffs be
`u_D,u_E`. Let `T_1,...,T_q` be any list of `q>=1` legal comparison themes,
allowing repetitions and empty themes. Put

    d_x=sum_j 1_(x in T_j),
    delta_x=1_(x in D), epsilon_x=1_(x in E),
    v_D(x)=delta_x/(p_x+delta_x+epsilon_x),
    v_E(x)=epsilon_x/(p_x+delta_x+epsilon_x).

Zero-numerator fractions are zero. For every real `t>=0`,

    sum_x [q v_D(x)+t v_E(x)-d_x/(p_x+1)
       +max(0,d_x/((p_x+1)(p_x+2))-t/(p_x+delta_x+1))] >=0.   (E_t)

This applies separately in the actual five-player path, in its true
maximum-theme root deviation, or in any other genuine history of the
same original complete strategy. It uses no anonymity or favorable
tie rule. The maximum-theme property is unnecessary for (E_t).

## Genuine comparisons and exact cancellation

For each index `j`, let `R_j` be the original strategy's actual final
response after the fixed old history followed by the forced action `T_j`.
Let

    U_p(X,Y)=sum_(x in X) 1/(p_x+1+1_(x in Y)),
    S=sum_j [u_D-U_p(T_j,R_j)] >=0,
    Z=sum_j [u_E-U_p(R_j,D)] >=0,
    V=sum_(j!=k) [U_p(R_j,T_j)-U_p(R_k,T_j)] >=0.

`S` is the first remaining player's true deviation IC. Every term of `Z`
is a final player's comparison in the prescribed `D` history. Every term
of `V` is a final player's comparison in the corresponding true `T_j`
history. Thus all three sums are nonnegative under the given original
strategy, including arbitrary ties.

Fix a customer and abbreviate

    p=p_x, D=delta_x, d=d_x,
    ell=sum_j 1_(x in R_j), h=sum_j 1_(x in T_j intersect R_j),
    K=(p+1)(p+2).

Then

    S_x=q v_D-d/(p+1)+h/K,
    Z_x=q v_E-ell/(p+D+1),
    V_x=(d ell-q h)/K.

Consequently `Q_t=S+(t/q)Z+V/q>=0` has the exact customer expansion

    (Q_t)_x=q v_D+t v_E-d/(p+1)
                +(ell/q)[d/K-t/(p+D+1)].

The overlap `h` cancels exactly. Because `0<=ell/q<=1`, its final term is
at most the positive part of the bracket. Therefore the left side of
`(E_t)` is at least `Q_t>=0`, proving `(E_t)`.

The five-provider row sent to parent uses `q=5,t=1/2`, equivalently
`Q=S+Z/10+V/5`. For `p in {0,1,2,3}` its per-customer coefficient is

    5v_D+v_E/2-d/(p+1)
           +[2d-p-2+D]_+/(2(p+1)(p+2)).

This eliminated form has no new menu state and can be priced from the
five true terminal membership bits and the comparison multiplicity `d`.

## Exact separation of one frozen template point

The frozen source is

    R-cd789330fc7141299ac491bbb3ffa420/round13/certificate/
    exact_max_menu_tuple_primal.json

Its SHA-256 is
`c0415208b932451f54646b4d49209876e8678e9da0d4a5297ee0207898af1feb`.
It is a 4007-row necessary-condition primal with W=1 and comparison cover
approximately 2.0125509122. It is not a complete SPE and is not a target
counterexample.

Evaluate `(E_(1/2))` in its recorded genuine maximum-branch bits and its
five-query comparison count, using the source's exact rational masses.
The result is exactly

    -1227955219406101921381370177982020110354542361259413533526
    /5875745307883226885488621846766048403041212632831848726505
      = -0.20898714206665983...

Thus this point cannot be extended to a full strategy satisfying the
genuine maximum-branch final reply comparisons. This is a separation of
one stated relaxation, not yet an improved universal welfare bound.

The independent disintegration feasibility test permitted every source
atom to split over all legal five-index `(T,R)` membership histograms,
preserving its old exact mass. A separating nonnegative combination is
`(10S+Z+2V)/13`. Its maximum over all per-atom reply histograms has exact
sum

    -2455910438812203842762740355964040220709084722518827067052
    /15276937800496389902270416801591725847907152845362806688913 <0.

Multiplying this value by `13/10` recovers the eliminated-row value.
The exact records are `max_penult_eliminated_exact_separation.json` and
`max_penult_menu_fixed_primal_extension.json` in this directory. The code
`max_penult_eliminated_pricing.py:newrow` gives a Fraction implementation.

## Remaining obligation

The local inequality is proved, and the source point is excluded. A
universal factor-two certificate still requires a full-domain pricing
argument and exact recovery, or a different direct global proof. No
floating restricted LP, finite instance test, or source-point separation
completes that obligation.
