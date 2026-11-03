# ROW3: credible cross-query replies are a missing constraint

2026-10-25. Research task restricted by the current user to five providers,
arbitrary common finite catalog and arbitrary complete-history pure SPE.
This note does **not** prove OPT5 <= 2W and gives no counterexample to it.
It identifies an exact credibility failure in one relaxed ROW3 obstruction.

## Precise candidate and branch accounting

Fix any complete five-player pure SPE, its actual path z and W, and five
optimal comparison themes T_0,...,T_4. At the actual ordered history
h=(S_1,S_2), force player 3 to T_i and follow the original complete strategy.
Let the two real follower actions be R_i,S_i and define

    d_i = U_b(T_i;R_i,S_i),       ROW3 = sum_i d_i.

Here b is the actual two-player old load and
U_b(X;Y,Z)=sum_{x in X}1/(b_x+1_Y(x)+1_Z(x)+1).
The candidate is

    ROW3 >= OPT5-W.                                      (ROW3-v1, OPEN)

If it holds, and an actual minimum-payoff player is at position 3, then
ROW3 <= 5u_3 <= W proves half. The corresponding rows at positions 4 and 5
are already established elsewhere. This does not handle minima at positions
1 or 2.

All five d_i use actual successors of the same complete strategy. Let B be
the old players' actual final profit sum, V the actual last-two profit sum,
and u player 3's actual profit. In branch i, use B_i,V_i,d_i and
Gamma_i=u-d_i>=0. The exact relay is

    W_i-W = (V_i-V)+(B_i-B)-Gamma_i.                       (1)

The B_i-B term is mandatory at this nonroot history. At a true root there
are no old players and it vanishes. A lower bound on V_i from a three- or
four-player theorem does not upper-bound V_i-V or pay (1).

## Complete response IC omitted by the tested relaxation

For every pair i,j define the **real** last response after player 4 copies
S_j in the T_i child:

    K_ij = sigma_5(h,T_i,S_j).

For every i,j, complete SPE gives

    U_b(R_i;T_i,S_i) >= U_b(S_j;T_i,K_ij),                 (2)
    U_b(K_ij;T_i,S_j) >= U_b(Q;T_i,S_j)  for every Q.      (3)

The off-diagonal history (h,T_i,S_j) cannot be replaced by the original
history (h,T_j,R_j), nor can K_ij be selected independently of (3).
Equations (2)-(3) retain ordered histories and all ties. Repeated themes
simply make the corresponding ordered histories coincide.

Writing F_p(X)=sum_{x in X}1/(p_x+1), the same-background two-player identity
is

    U_b(S_j;T_i,K_ij)-U_b(K_ij;T_i,S_j)
      = F_(b+1_Ti)(S_j)-F_(b+1_Ti)(K_ij).

Together with (3), this gives the valid bound, for any legal Q,

    U_b(R_i;T_i,S_i)
      >= U_b(Q;T_i,S_j)
         +F_(b+1_Ti)(S_j)-F_(b+1_Ti)(K_ij).              (4)

The last potential difference has no established aggregate sign. Thus
(4) specifies a real additional obligation, not a closed proof of ROW3.
Equivalently, player 4's utility is at least the largest *credible* copy
value

    max_j min_{K in BR(b+1_Ti,S_j)} U_b(S_j;T_i,K),        (5)

which can be strictly larger than the denominator-only guarantee used
by the 77-row relaxation.

## Exact finite diagnostic

The parent supplied the 19,008-type, 77-row necessary-condition relaxation
with max (O-ROW3)/W about 1.51707147. Its 11 positive support types all have
b=0. I materialized each type's entire orbit under the five query-index
permutations, producing 18 legitimate catalog themes
C,D,E,T_0,...,T_4,R_0,...,R_4,S_0,...,S_4 and 185 positive client types.
Source orbit weights were rounded to 10^-8 and multiplied by 120*10^8;
therefore every resulting multiplicity is a positive integer. No claim
that rounding preserves all relaxed inequalities is needed here.

Exact all-outcome backward induction and a separate complete-strategy
verifier give:

* The proposed actual C,D,E leaf is not SPE: its C payoff is 2,791,921,400,
  whereas the root's exact guaranteed SPE payoff is 6,866,184,736.
* In every T_i child, the proposed R_i,S_i follower leaf is not SPE. R_i
  gets 4,632,856,876, but choosing S_j for any j != i is followed by the
  **unique** best reply R_j and gives 7,718,643,666. Its strict gain is
  3,085,786,790. This is precisely the off-diagonal (2)-(3) failure.
* The true minimum current payoff after forcing each T_i is 5,348,363,202.
  There are exactly 20 complete three-player SPE terminal count vectors.
  Across all such outcomes and all admissible first actions, the smallest
  possible true query-row slack ROW+W-O is 13,125,108,894 > 0.
* A full SPE certificate is included and independently checked at all
  343 ordered decision histories and all 5,831 nontrivial deviations.

This is a three-remaining-player credibility diagnostic with a five-theme
comparison union. It is **not** a complete five-player root example:
prepending two empty actions would not make those earlier actions optimal.
Its comparison union is not labeled OPT3. The conclusion is only that this
specific relaxed obstruction collapses when its real cross-query last
replies are enforced.

## Files and reproducibility

Run `python3` on `exact_materialized_relaxation.py` from the repository root.
It reads `frozen_row3_source_support.json` (the original 77-row support, frozen before later parent edits), reconstructs the integer catalog,
enumerates every pure-SPE outcome exactly using the existing faithful
outcome-set recursion, and separately verifies a full certificate.
The primary exact outputs are `exact_materialized_audit.json`,
`materialized_row3_catalog.json` and `materialized_row3_true_spe.json`.
The float materializer and policy-cone probes are discovery diagnostics only;
their absence of a counterexample does not prove ROW3 or half.
