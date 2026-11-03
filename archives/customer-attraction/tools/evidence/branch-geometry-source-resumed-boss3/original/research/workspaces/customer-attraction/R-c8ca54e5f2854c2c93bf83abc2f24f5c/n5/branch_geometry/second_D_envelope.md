# Genuine second-to-penultimate response envelope

Status: direct necessary-condition theorem and **exact separation of the historical 437-row primal**. This is additional genuine ordered-history information. It is not a proof of five-player half coverage, a completed SPE, or a counterexample. The root has been sent the equation for independent review; no full mathematical review is claimed here.

## Exact game and branches

Use CAG-MODEL with five players, arbitrary finite common catalog and clients, and an arbitrary fixed complete ordered-history pure SPE. Its actual path is `(A,B,C,D,E)`, with actual second payoff `u2`. Fix five legal comparison topics `T_i`, allowing repetition. Use the indexed branches

* `(A,E,T_i,R_i^AE,S_i^AE)`, where the last two actions are the original strategy's genuine responses;
* `(A,T_i,H_i,I_i,J_i)`, likewise genuine responses.

Additionally expose the genuine second-position deviation to `D`:

`(A,D,R,S,T)`.

Only this last branch is new. Names `R,S,T` denote its three true successor topics; they do not identify any indexed topic.

The following seven aggregate slacks are nonnegative:

| Name | Slack | Justification |
|---|---|---|
| F | `u2-U_D(A,D,R,S,T)` | Exact second-position deviation with all genuine successors |
| E | `U_T(A,D,R,S,T)-sum_x e/(a+d+r+s+1)` | Genuine final player compares legal actual theme E |
| O | `5U_T(A,D,R,S,T)-sum_x j/(a+d+r+s+1)` | Sum of final comparisons with the five T_i |
| R | `sum_i U_RiAE(A,E,T_i,R_iAE,S_iAE)-sum_x r sum_i1/(a+e+t_i+2)` | Indexed fourth player compares new legal theme R; its final denominator is at most a+e+t_i+2 |
| S | Same preceding row with `s` replacing `r` | Indexed fourth player compares new legal theme S |
| H | `sum_i U_Hi(A,T_i,H_i,I_i,J_i)-sum_x t sum_i1/(a+t_i+3)` | Indexed third player compares new legal theme T, with at most three players remaining |
| I | `sum_i U_Ii(A,T_i,H_i,I_i,J_i)-sum_x t sum_i1/(a+t_i+h_i+2)` | Indexed fourth player compares new legal theme T, with at most two players remaining |

All bits in the table are client membership bits, `j=sum_i t_i`. Every row follows directly from SPE optimality at the written ordered history. Comparing a theme revealed at a different history is legal because the catalog is common. Only a denominator upper bound, rather than a frozen continuation, is used in the four floor rows. Empty themes, repeated actions, zero clients, and history-dependent ties remain allowed.

## Universal projected inequality

Choose any nonnegative weights `(alpha,beta,gamma,delta,epsilon,zeta,eta)` for the table rows. For a fixed original client state `z`, define

`K_AE=sum_i r_iAE/(a+e+t_i+r_iAE+s_iAE)`,

`C_AE=sum_i 1/(a+e+t_i+2)`,

`K_H=sum_i h_i/(a+t_i+h_i+i_i+j_i)`,

`K_I=sum_i i_i/(a+t_i+h_i+i_i+j_i)`,

`C_H=sum_i 1/(a+t_i+3)`,

`C_I=sum_i 1/(a+t_i+h_i+2)`.

Let

`M(z)=alpha*b/(a+b+c+d+e)+(delta+epsilon)*K_AE+zeta*K_H+eta*K_I`

`+max_{r,s,t in {0,1}} {(-alpha*d+(beta+5gamma)*t)/(a+d+r+s+t)`

`-(beta*e+gamma*j)/(a+d+r+s+1)-(delta*r+epsilon*s)*C_AE-t*(zeta*C_H+eta*C_I)}`.

A zero numerator is assigned value zero even when the denominator is zero. Every genuine nonzero term has a positive denominator. Then

`sum_x M(z_x)>=0`.                                              (1)

Indeed, the true new branch supplies one particular triple `(r_x,s_x,t_x)` for each client. The weighted sum of the seven original nonnegative aggregate slacks equals the sum of the corresponding expression before maximization. Maximization is pointwise, so the left side of (1) is at least that nonnegative weighted sum. This is a universal necessary inequality, not a claim that arbitrary locally maximizing triples can come from one strategy.

The state needed to evaluate (1) is already recorded by the historical indexed histograms: the AE histogram determines `K_AE,C_AE`; the second-position histogram determines `K_H,K_I,C_H,C_I`; both share the same comparison multiplicity `j`. No hidden matching is required. If `delta=epsilon`, the maximum depends on `r,s` only through `k=r+s in {0,1,2}`, so it has six states rather than eight.

## Exact old-primal separation

Use the following nonnegative weights, all with denominator one million:

| Row | Numerator |
|---|---:|
| F | 819936 |
| E | 80557 |
| O | 2110 |
| R | 26105 |
| S | 26105 |
| H | 15852 |
| I | 29336 |

For the exact 64-atom historical obstruction in `evidence/certificates/customer_attraction/five_player_indexed_bound.json`, direct Fraction evaluation gives

`sum_z mass(z) M(z)`

`=-336525906357864252494704662357779526105596687 / 24837228663957176671172182423497877773536000000`

`≈-0.013549253457823079 < 0`.

Thus the historical point violates a universal necessary row involving a genuinely missing second-to-D history. The computation enumerates only eight new client membership triples when evaluating an explicitly proved envelope; it does not search finite games and does not infer a positive general result from finite checks. `separate_second_D.py` reconstructs all seven exact per-client rows and verifies the rational weights and strict negative separation. Its numerical LP is only a source of convenient rounded weights; the final separation is checked exactly and does not depend on LP optimality.

## Earlier local diagnostic

`third_D_completion.py` considered a genuine third-to-D pair `(A,B,D,P,Q)` and its genuine fourth-to-`T_i` final response menu. Its 133-row necessary extension of the old point remained strictly feasible numerically. Adding the second-to-D branch in `two_D_completion.py` yielded an infeasible 283-row extension, whose seven active rows reduced to the envelope above. These local outcomes are diagnostics only. They do not prove any full extension feasible or infeasible beyond their precisely stated necessary rows.
