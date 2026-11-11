# Source review: arbitrary two-action histories and the root72 append

Boss1; RUN `six-boss1-20261111`. New directory only; all completed root-C and requery packages stay frozen. This review is written before the newly released one-call root72 optimization.

## 1. Precise quantifier extension of the nine-budget cut

Fix ANY finite unit-client common-label-catalog instance and ANY complete ordered-history pure SPE sigma. Fix ANY ordered legal two-action history H=(L1,L2), whether or not reached by sigma from the root. Follow sigma's prescribed players 3,...,6 to obtain the genuine continuation (B3,B4,B5,B6). Let vi be player i's final share payoff in the leaf (L1,L2,B3,B4,B5,B6), for i=3,4,6. The first two actions are fixed background; neither of their incentive constraints is used.

Choose ANY ordered six legal query labels Q1,...,Q6, allowing repetitions, aliases and empty labels; let o be membership in their coverage union. For each k, at this same history H force Qk and follow sigma to the genuine R4_k,R5_k,R6_k. All nine budgets in the frozen cut remain valid:

* The source3 average IC is sigma's genuine player-3 IC at H against each Qk.
* The three old source4 SAFE budgets occur at the exact history (L1,L2,B3), use the genuine old v4, and query each legal Rj_k. Their own continuations are bounded by the two remaining successors, giving prefix load plus 3.
* The three old source6 SAFE budgets occur at (L1,L2,B3,B4,B5), use the genuine old v6, and query each Rj_k with no successors left.
* The new terminal Omean SAFE is a real terminal comparison at each (L1,L2,Qk,R4_k,R5_k).
* The new PAIR is paid at each four-action history (L1,L2,Qk,R4_k), by the same three true ICs and nonnegative self-overlap difference as before. Omean/Omean uses all 36 INNER query pairs at that history, followed by the OUTER six-branch average.

The queried Q role is its generating branch's own Qk, so its membership q remains in the true prefixes and source3 payoff. Old B3 is still the old continuation label, not Q. Full ordered histories remain intact even when labels alias or their coverage coincides.

No positive budget uses largest-label status, naked size K, actual root u, optimality of the six queries, a root deviation IC, or any old71 equality/slack. Tight old SAFE3 was only an interpretation of the excluded numerical point, never a premise of the universal projection. The averaged q moment still lies in [o/6,o] for arbitrary six legal labels. Therefore the exact all128 envelope certificate proves, for the stated arbitrary H and query menu,

    126000 v3 + 65719 v4 + 4962 v6 - sum_h m(h) w_h >= 0.

This is a quantified conditional-history claim; it does not identify histories with equal loads or choose favorable continuations.

## 2. Actual-path and 256-type mapping (informational only)

Taking H=(A1,A2) from the actual path makes the old continuation (A3,A4,A5,A6), hence vi=ui for i=3,4,6. Choosing an optimal six-label query menu is permitted but not required for validity.

The old128 bit order is (a1,...,a6,o). The global256 bit order is (a1,...,a6,x,o). If a is the integer represented by the first six bits, the exact map is

    old_index = 2*a + o,
    global_index = 4*a + 2*x + o,
    global_cut[global_index] = old_cut[old_index],   x=0,1.

The two x copies have identical coefficients. The K column is zero. Thus the arbitrary-history cut can enter the actual256 wallet without any X assumption. Main owns that separate insertion; the root72 system in this directory does NOT add actual-path joint rows or X columns.

## 3. The newly authorized root72 system

Use the old root-C construction unchanged: choose a genuine legal C with |C|=K, force it at the actual root, retain its true six-label branch and all128 types (p,y2,y3,y4,y5,z,o), plus actual root u. Keep all original 71 raw rows, including duplicates and zeros, with their original coefficients and their independent K/O right-side parameters.

Append only the one all128 requery cut, which applies because this root-C branch is a special case of section 1. It is stored in its ORIGINAL UNSCALED form. Its coefficient of u is zero, its coefficient of K is zero, and its right side is zero. No new column or equality is added.

The two equalities remain sum p*w=K and sum o*w=O. For the single new discovery call set

    K=1125421575458286230366665/6570307807568935468436467, O=1,

and minimize u over 129 nonnegative variables, 72 raw inequalities and two equalities. This reuses only Main's specified scalar K from the current global point; it does not reoptimize that global point.

## 4. Positive numerical scaling and exact dual recovery

Input rows use the convention A*x>=bK*K+bO*O. Keep the original71 numerical divisors equal to 1. For floating discovery only divide the appended large-coefficient cut by the positive integer 126000. Record this divisor in the exact input and solver output; no exact row is overwritten with its scaled version.

If the solver returns a nonnegative dual weight lambda_scaled for the divided row, the weight of the original row is

    lambda_original = lambda_scaled/126000.

More generally lambda_original=lambda_scaled/divisor. Exact recovery solves the original unscaled column equations, using these adjusted numerical values only as hints. The two equality multipliers pi_p,pi_o remain free.

For original unscaled row weights lambda>=0 and residual

    r=c-sum lambda*A-pi_p*E_p-pi_o*E_o >=0

on all129 columns, the universal root line is

    u >= a*K+b*O,
    a=pi_p+sum lambda*bK,  b=pi_o+sum lambda*bO.

The added cut has bK=bO=0 and no u coefficient, but its atom coefficients still affect residuals and the recovered supporting line. Preserve all five size-cap K contributions, the floor K/6 contribution if weighted, and the OPT union's O contribution if weighted. A numerical optimum at the fixed K is not itself a universal line; the complete all-column homogeneous identity is required.

## 5. Scope and stopping rule

Recover a matching exact primal and universal dual if possible, compare with the prior root line at this K, identify the positive mechanism, and verify every original unscaled row. This certifies only the stated finite necessary cone at the chosen K and a universal necessary root line. It does not certify a complete SPE, global root sharpness or half. One optimizer call is authorized for this new directory; further calls require a separate Main release.
