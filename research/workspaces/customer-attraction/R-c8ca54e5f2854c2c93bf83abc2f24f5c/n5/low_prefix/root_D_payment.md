# Root-to-penultimate feedback pays an early low-profit deficit

Status: new directly proved necessary row; exact independent coefficient audit
passes and it strictly excludes the historical 437-row primal. It is a missing
payment in that template, not a full five-provider half theorem. No complete SPE
counterexample or claim of exact optimality of a numerical relaxation is made.

Use CAG-MODEL: five providers, arbitrary finite unit clients and common finite
catalog, any fixed complete ordered-history pure SPE, arbitrary ties, empty and
repeated themes retained. The actual path is `(A,B,C,D,E)` and root utility is
`u1`. Fix any five legal query themes `T_i`, allowing repetitions. They may be
the optimal five, but optimality is not needed for this lemma.

Use two genuine indexed families from the same fixed strategy:

* `(A,E,T_i,R_i,S_i)` after second provider is forced to E and third to T_i;
* `(A,T_i,H_i,I_i,J_i)` after second provider is forced to T_i.

The optimizing nodes used below are fourth provider R_i in the first family
and third provider H_i in the second. At each client put

    K_AE = sum_i r_i/(a+e+t_i+r_i+s_i),
    C_AE = sum_i 1/(a+e+t_i+2),
    K_H  = sum_i h_i/(a+t_i+h_i+i_i+j_i),
    C_H  = sum_i 1/(a+t_i+3).

The subscripts i_i,j_i are membership in the genuine second-family replies,
not player indices or optimal multiplicity. A zero numerator is zero, including
zero denominators; every genuine nonzero profit denominator is positive.

## The newly exposed root branch

Force root to actual D and follow the original strategy, obtaining the genuine
branch `(D,F,G,H,Z)`. Its new membership bits are `(d,f,g,h,z)`; put
`n=f+g+h`. This root branch is different from the genuine second-to-D branch.
In particular, the root has no fixed A background here.

Five aggregate slacks are nonnegative:

| Aggregate | Per-client coefficient | Legal source |
| --- | --- | --- |
| Root IC | `u1_x-d/(d+n+z)` | Root chooses D and all four successors really change |
| Last BR | `z/(d+n+z)-e/(d+n+1)` | New genuine last provider compares actual E |
| Root floor | `u1_x-z/5` | Actual root compares legal new theme Z; all final loads at most 5 |
| AE floors | `3K_AE-n C_AE` | Sum of indexed fourth-provider comparisons with each F,G,H |
| Second floors | `K_H-z C_H` | Sum of indexed third-provider comparisons with Z |

The three middle successors F,G,H need only be legal catalog themes for this
argument; no extra best-response assumption is placed on them. Their true SPE
choices supply such legal themes. The last Z must be the real last best reply.
No same-load histories are assigned the same replies and no new reply is chosen
to optimize an analytic expression.

## A universal eight-state payment envelope

For any nonnegative weights `(alpha,gamma,beta,delta,epsilon)` define

    M_x = (alpha+beta)u1_x + 3delta K_AE + epsilon K_H
          + max_{n in {0,1,2,3}, z in {0,1}} {
               (-alpha*d+gamma*z)/(d+n+z)
               -gamma*e/(d+n+1) - delta*n*C_AE
               -(beta/5+epsilon*C_H)z }.

Then universally

    sum_x M_x >= 0.                                            (RD)

Proof: before the maximization, the expression at the true `(n_x,z_x)` is
exactly the weighted sum of the five displayed aggregate slacks. Their sum over
clients is nonnegative by the actual full SPE. Pointwise maximization can only
increase it. Reduction from sixteen `(f,g,h,z)` states to eight `(n,z)` states
is exact because all three intermediate floors have the same weight. This
does not assert that independently maximizing client states form legal themes.

Thus (RD) is additional root-level payment, expressly involving the credible
last reply of a new root branch and the shared legal catalog. It is not another
use of the three/four-remaining ratio interface.

## Exact historical-point separation

Take the simple rational weights

    (alpha,gamma,beta,delta,epsilon)
       = (79/100,1/20,13/100,2/125,3/200).

On the exact 64-atom historical necessary-condition point in
`evidence/certificates/customer_attraction/five_player_indexed_bound.json`,
the new valid row evaluates to

    sum_x M_x =
      -7925441818047196747641735646715598758647
       /564482469635390378890276873261315403944000
      = -0.014040191227136576... < 0.

This is a genuine missing payment in the old template: its certified primal
cannot be extended even to these five aggregate constraints from root-to-D.
It does not prove that every necessary point with ratio above two is excluded,
nor that an actual SPE falls in either previously proved high-prefix regime.
The low-prefix half obligation remains open.

`audit_root_D_payment.py` imports neither the discovery LP nor any SPE solver.
It reconstructs all old features from source memberships, checks all 1024 new
source membership cases, verifies the eight-state maximum equals the literal
sixteen-state maximum, and checks the symbolic affine identity in 384 basis
cases. Exact output is `audit_root_D_payment.json`. The universal proof is the
five genuine nonnegative rows above; finite coefficient checking only audits
the formula and exact exclusion arithmetic.

`root_D_envelope.py` is a discovery/diagnostic script with 181 necessary rows;
`--simple` retains the five aggregate rows above. Its optimizer output is not
used as a proof premise.
