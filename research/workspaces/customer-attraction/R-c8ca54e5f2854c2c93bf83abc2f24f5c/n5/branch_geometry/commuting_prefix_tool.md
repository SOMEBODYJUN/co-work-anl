# A permutation-robust continuation bound

Status: **TOOL ONLY**. Direct mathematical derivation; root independently reconstructed the unweighted inequality in this session. It does not exclude the historical 437-row obstruction, prove half coverage, or supply a genuine counterexample. The historical obstruction is used only as an exact negative test of the proposed added row. No claims about the newer 557/728 systems are inferred from that test.

## Statement

Fix one complete ordered-history pure SPE of CAG-MODEL. At a genuine node with three players remaining, let the background be `b_x`, and let the acting player's actual eventual profit be `v`. Fix a legal comparison theme `Q`, with bits `q_x`, and put `p_x=b_x+q_x`. Suppose a known genuine two-player SPE, possibly at a different ordered history with exactly this same background load `p`, has outcome `(R,S)` and profits `r,s`. Set

`H=r+s+sum_x 1_R(x)/((p_x+1)(p_x+2))`.

For every scalar `lambda>=0`,

`v+lambda H >= sum_x L_lambda(p_x,q_x)`,

where `L_lambda(p,0)=0`, and for `q=1` (so `p>=1`),

`L_lambda(p,1)=min{1/p, (1+2 lambda)/(p+2)}`.

This conclusion does not identify the policies at reordered histories. It transfers a bound on the *maximum attainable two-player total profit*, which depends only on background load and common catalog.

## Proof

If the first node deviates to `Q`, let `(P,Q')` be its original strategy's genuine subsequent two-player outcome. Its background is `p`. Write `c_x=1_P(x)+1_Q'(x)`. Node optimality gives `v>=U_Q(P,Q')`. The two-remaining tax theorem applied to the known outcome `(R,S)` gives `R_p(P,Q')<=H`, since `(P,Q')` is a legal comparison pair whether or not its ordered history agrees. Hence

`v+lambda H >= sum_x (q_x+lambda c_x)/(p_x+c_x)`.

For `q=1`, the displayed rational function is monotone in real `c>=0` with derivative having sign `lambda p-1`. Its minimum on `c in {0,1,2}` is therefore attained at `0` or `2`, giving exactly `L_lambda`. For `q=0`, all terms are nonnegative, including the `p=c=0` convention. This proves the theorem.

In particular, at `lambda=1`,

`v+H>=sum_x q_x/p_x`.

An equivalent pointwise proof of that case is

`q/(p+c)+c/(p+c)-q/p = c(p-q)/(p(p+c))>=0`

on `q=1`, with the zero-membership cases treated separately.

## Exact indexed application

Use the historical indexed notation. After `(A,T_i)`, the true third action is `H_i`, with profit `z_Hi`. The known pair after `(A,B,T_i)` is `(R_i^AB,S_i^AB)`. The former node may deviate to `B`, creating the ordered prefix `(A,T_i,B)`. Its load agrees with `(A,B,T_i)`, although its policy may differ. Thus, with `p=a+b+t_i`,

`z_Hi+lambda H_AB_i >= sum_x L_lambda(p_x,b_x)`.

Replacing `B,AB` by `E,AE` gives the second family. Summing over `i` is evaluable from the existing histograms: the `z_Hi` contribution uses only the second-position histogram, and `H_AB_i` and the right side use only the AB histogram. A common alignment beyond the shared `t_i` count is unnecessary for this particular sum.

The same argument at the true third node `(A,E)` using comparison `B` and the known pair `(X,Y)` at `(A,B,E)` gives

`z_U+lambda [z_X+z_Y+sum_x x/((a+b+e+1)(a+b+e+2))]`

`>=sum_x L_lambda(a+b+e,b)`.

For these applications, `p<=3` on the compared theme. The only nonzero lambda breakpoints are `1/3,1/2,1`; checking `0` and those three knots tests the piecewise-linear row family against a fixed point for all lambda>=0 (the slope is nonnegative after the final knot).

## Exact historical obstruction test

`audit_commuting_prefix.py` evaluates these legitimate rows against the 64-atom exact 437-row primal in `evidence/certificates/customer_attraction/five_player_indexed_bound.json`. All twelve knot checks have positive slack. At `lambda=1`, the AB sum is

`4900633767540477167953791168813860381023 / 1693447408906171136670830619783946211832 > 0`,

and the AE sum is

`3787456118199780686823224366053151620007 / 1693447408906171136670830619783946211832 > 0`.

Thus this theorem is valid response geometry but is too weak, in these direct applications, to remove even the old indexed obstruction. The positive finite checks are not evidence for the general half-coverage claim.
