# Independent review: binary-background four-tail certificate

2026-10-25. This is an internal independent audit, not external peer review. It verifies a new valid ingredient for the five-provider target; it does not yet prove OPT_5<=2W.

## Audited exact statement

After a fixed genuine prefix with binary customer loads b_x∈{0,1}, let four remaining players follow an arbitrary complete-history pure SPE, with actual tail A,B,C,D and individual terminal utilities. Let V_out be their combined profit from customers b_x=0, and V_in their combined profit from customers b_x=1. For every four legal comparator themes Q_1,...,Q_4,

    R_b(Q_1,...,Q_4) <= 2 V_out + (5/3) V_in.

The comparator quartet need not maximize residual profit. Repeats and empty themes are legal, and history-dependent ties are preserved.

## Raw node legality

The off-path leaf is (D,Q,R,S), where Q,R,S are the original strategy's genuine replies after the tail root changes from A to D. It is not a fresh best-response choice. The first off-path action D is forced and never treated as optimal. The second and fourth off-path positions are genuine optimizing nodes, and all their required safety comparisons are legal because the catalogue is common.

The root-copy-D row is u_A(A,B,C,D)-u_D(D,Q,R,S)>=0. It follows from SPE at the tail root, with the original full continuation after the deviation. The actual second-player safety rows use final denominator at most b+a+3. The off-path second-player C safety row uses at most b+d+3. Actual and off-path last-player rows use their exact fixed-prefix denominators.

At either actual or off-path last-two node, write its fixed load p and its final two actions L,M. The already-proved same-background two-player tax lemma supplies

    H=u_L+u_M+sum_x 1_L(x)/[(p_x+1)(p_x+2)]
    >= R_p(Q_i,Q_j)

for each of the six different comparator INDEX pairs. Adding these six inequalities yields the audited pair-opt row. For a customer in e of the four comparison themes, the sum of the six comparison-pair profits is exactly

    e(4-e)/(p+1) + e(e-1)/(p+2).

This remains correct for repeated themes because the indexing, rather than theme distinctness, controls the count. The tax lemma uses the real strategy's appropriate replies, so no suffix is frozen. No binary-background aggregate correction is silently omitted: the certificate uses the raw residual target e/(b+e), not the older coarse aggregate approximation.

## Exact arithmetic audit

`audit_binary_tail_certificate.py` reads the submitted JSON's twelve rational multipliers and imports no author coefficient function. It recomputes every required row from the raw terminal shares, and recomputes all six comparator-pair terms individually. It checks all 2*128*16=4096 assignments of binary background, seven actual/off-path memberships, and four individually indexed comparator memberships. These have 1280 distinct background/seven-membership/comparator-count states. Every multiplier is nonnegative. The minimum exact residual is zero; precisely 17 compressed states have zero residual. This independently reproduces the author values.

Finite coverage here is complete coverage of every algebraic client type, not sampling of games or strategies. The exact pointwise identity plus the legal global slack inequalities therefore proves the statement for every size instance in the stated binary-background class.

## Five-root aligned consequence

Fix optimum themes T_1,...,T_5. For each i force T_i at the original empty root and keep the original strategy's genuine four-player SPE tail, with total tail profit V_i and forced root profit z_i. Its binary background is 1_{T_i}. Apply the audited statement to comparison quartet T_{-i}. The inside tail profit is |T_i|-z_i, so

    R_{1_Ti}(T_{-i}) <= 2V_i-(|T_i|-z_i)/3.

For a client appearing in e>=1 optimum indices, the sum across i of the left-side contribution is e*(e-1)/e+(5-e)=4. A client appearing in none contributes zero. Summing gives

    4OPT_5 +(1/3)sum_i|T_i| <= 2sum_i V_i +(1/3)sum_i z_i
                                 <= 2sum_i V_i +(5/3)u_1.

The final step is original root optimality z_i<=u_1. This is a valid new root-family inequality. It still requires a joint upper budget for the true off-path profits V_i before it can prove the five-provider target.

## Stronger retained certificate (same statement, outside coefficient 1999/1000)

The later, separate `parent/binary_tail_exact_1999.json` has thirteen nonnegative rational multipliers and establishes

    R_b(Q_1,...,Q_4) <= (1999/1000) V_out + (5/3) V_in.

The independent audit now accepts `--certificate`; it passes both files separately. For the stronger file it checks the same 4096 raw assignments/1280 compressed states, with exact minimum zero and 19 compressed zero states. The two newly relevant raw rows are the actual third tail node's denominator safety comparison with D, and the genuine off-path last node's exact comparison with B. Both are legal optimizing nodes; no forced off-path root optimality was added.

Writing c=1999/1000-5/3=997/3000 and J=sum_i|T_i| gives the full aligned root inequality

    12000OPT_5 +997J <=5997sum_i V_i +997sum_i z_i.

Using J>=OPT_5 and sum_i z_i<=5u_1 yields the weaker convenient form

    12997OPT_5 <=5997sum_i V_i +4985u_1.

The full-credit row retains more information and should be used before the convenient form when closing the five-provider proof. Neither displayed row yet supplies the missing common budget for the five genuine off-path tail profits.
