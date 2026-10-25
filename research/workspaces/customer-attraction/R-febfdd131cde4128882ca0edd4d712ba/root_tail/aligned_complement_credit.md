# Five-player aligned root complements with retained four-tail credit

Date: 2026-10-25. Status: analytic consequence of the existing arbitrary-background four-remaining-profit certificate; exact finite coefficient reconstruction saved alongside. An independent branch reconstructed the raw fractional slack definitions and verified both `c=251/1500` and the aligned complement identity; its audit is `../independent/audit_four_profit_root_gain.py`. This is not a proof of five-player half coverage.

## Scope

Fix any finite common catalogue and any complete ordered-history pure SPE with five unit providers. Retain its prescribed actions at every history, including arbitrary ties. Let `O=OPT_5`, and fix an optimal indexed tuple `T_1,...,T_5`, allowing repetitions. For each index `i`, let the **true** root deviation branch be

`(T_i,A_i,B_i,C_i,D_i)`.

Write `z_i` for that branch's root payoff and `V_i` for the four followers' total payoff. The actual root payoff `u_1` satisfies `z_i<=u_1` for every `i`. When two `T_i` coincide the two histories and their continuations coincide; none of the derivation needs them to be distinct.

Set `alpha=1499/750` and `c=251/1500`.

## 1. A four-tail theorem stronger than its published ratio

The existing `research/current/customer_attraction/four_remaining_profit_bound.md`, equations (10)--(14), proves for every four-comparator tuple `Q` and every legal background `p` the identity

`alpha V-R_p(Q)=G+sum_x rho_{p_x}(a_x,b_x,c_x,d_x,q_x,r_x,s_x)`,

where `G>=0`. The auxiliary `q,r,s` are the true continuation after the first tail provider changes to the actual last tail topic. They need not be added to our state: define

`r_p(a,b,c,d)=min_{q,r,s in {0,1}}rho_p(a,b,c,d,q,r,s)`.

The table below gives every exact value at `p=0,1`. These are minima of all eight complete binary cases, not samples of games. In particular they remain valid with repeats, empty topics, and any consistency restrictions on the seven topic labels.

| Tail membership | r_0 | r_1 |
| --- | ---: | ---: |
| 0000 | 0 | 0 |
| 0001 | 0 | 133/750 |
| 0010 | 1/750 | 2003/12000 |
| 0011 | 1/1500 | 61853/180000 |
| 0100 | 1/1500 | 251/3000 |
| 0101 | 39/500 | 6331/22500 |
| 0110 | 1/1000 | 7363/36000 |
| 0111 | 623/3000 | 26047/60000 |
| 1000 | 2747/12000 | 239/1200 |
| 1001 | 691/6000 | 14579/45000 |
| 1010 | 47/1500 | 22183/90000 |
| 1011 | 1919/12000 | 5177/12000 |
| 1100 | 0 | 15767/90000 |
| 1101 | 77/750 | 63893/180000 |
| 1110 | 1/4000 | 43349/180000 |
| 1111 | 1169/6000 | 41143/90000 |

Consequently, when the background is one retained root topic `T`, for **every** comparator quartet,

`R_{1_T}(Q) <= alpha V-sum_x r_{1_T(x)}(a_x,b_x,c_x,d_x)`.   (F)

All `r_0` are nonnegative, and for `k=a+b+c+d` every row satisfies

`r_1(a,b,c,d) >= c*k/(1+k)`.   (C)

The constant in (C) is the largest uniform constant obtainable by minimizing this particular residual: equality occurs at tail membership `0100`. This is a coefficient statement about this certificate; it does not assert game sharpness.

Since the four followers' total payoff earned from customers of `T` is exactly `|T|-z`, (F) and (C) give the simple whole-profit form

`R_{1_T}(Q) <= alpha V-c(|T|-z)`.   (W)

This recovers value already present in the proof but discarded by the scalar ratio theorem. The credit is charged to the root topic's actual lost share, so it is not a free extra utility budget.

## 2. Aligned complements have an exact union identity

Apply (F) or (W) at root branch `i`, comparing the other four indexed optimal topics `T_-i`. For a customer covered by exactly `e>=1` optimal indices, its total contribution to the five left sides is exactly four:

* for each of the `e` indices whose root topic covers it, the other comparisons contribute `(e-1)/e`;
* for each of the other `5-e` indices, the other comparisons contribute one.

Thus `e*(e-1)/e+(5-e)=4`. The case `e=1` uses zero for the empty-comparison numerator; customers outside the optimal union contribute zero. Therefore

`sum_i R_{1_Ti}(T_-i)=4O`.   (A)

The analogous algebra identity holds for `m` indexed comparisons, with right side `(m-1)O`; only the four-tail certificate here specializes to five players.

Combining (F) and (A) gives the strongest row obtainable by retaining these tabulated minima:

`4O <= alpha sum_i V_i -sum_x sum_i r_{t_i(x)}(a_i(x),b_i(x),c_i(x),d_i(x))`.   (R)

It uses only the existing matched 32-type root histogram `(t,a,b,c,d)`. No auxiliary continuation label or independence assumption is introduced.

The simpler whole-profit version is

`4O <= alpha sum_i V_i-c sum_i |T_i|+c sum_i z_i`.   (S)

Writing `J=sum_i |T_i|`, root optimality and `J>=O` yield

`(4+c)O <= alpha sum_i V_i+5c u_1`.   (U)

Equation (R) dominates (S); equation (S) dominates the aligned scalar ratio `4O<=alpha sum_i V_i`. These are genuine SPE necessary inequalities, unlike an arbitrary assembly of unrelated scalar tails.

## 3. Remaining payment

The new row does not bound `sum_i V_i` by actual welfare. The five deviation branches are mutually exclusive; summing their follower profits without a further IC payment is not legal. In particular `V_i` is a background follower profit, never the root branch's full coverage. Also `sum_i(z_i+V_i)` is the sum of five branch coverages, not five times the actual coverage. The result is supplied to the parent full-root-histogram model so its existing actual-node and cross-menu comparisons can pay that remaining branch budget.

Exact reconstruction: `python3 research/workspaces/customer-attraction/R-febfdd131cde4128882ca0edd4d712ba/root_tail/audit_aligned_credit.py`.
