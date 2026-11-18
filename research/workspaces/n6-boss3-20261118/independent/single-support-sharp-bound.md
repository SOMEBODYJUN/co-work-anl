# A sharp obstruction for a single realized coverage set

## Precise result

In the original six-person model, suppose the six on-path labels all have the same coverage set A. Labels themselves may be distinct. Then every full pure SPE with this realized path satisfies

    6 OPT_6 <= 11 W,    equivalently W/OPT_6 >= 6/11 when OPT_6>0.

The coefficient 11/6 is sharp, even for an SPE whose prescribed action is the same label at EVERY ordered history. Thus searching only all-identical-coverage realized paths cannot produce a counterexample to the target 2W>=OPT_6. It can reach ratio 6/11, so a proof relying on a larger margin for this case would be false.

## Proof of the bound

The final mover's realized payoff is |A|/6=W/6. For every catalogue label T, the true deviation has no successors and pays

    |T minus A| + |T intersect A|/6.

SPE at that actual final node therefore yields

    6 |T minus A| + |T intersect A| <= W.

Take an optimum tuple T_1,...,T_6, let B be its union, let a=|B minus A| and b=|B intersect A|. Summing these six final-node inequalities and using the union bound separately on the two disjoint client regions gives

    6a+b <= 6W.

Since b<=W,

    6 OPT_6 = 6a+6b <= 6W+5b <= 11W.

No static deviation comparison was substituted at an earlier player. The only comparison used is the actual last node, whose true continuation is empty. The conclusion also holds when W=0 and does not divide by zero.

## Sharp finite original-model construction

There are seven labels A,T_1,...,T_6. Make six disjoint core blocks C_1,...,C_6 of six unit clients each and six disjoint private blocks P_1,...,P_6 of five unit clients each. All twelve blocks are mutually disjoint. Set

    cov(A) = union_j C_j,
    cov(T_j) = C_j union P_j.

Prescribe A at every history, including every off-path history. The realized path is six copies of A, so W=36 and every realized utility is 6. The six labels T_1,...,T_6 cover all 66 clients, hence OPT_6=66. Therefore 6OPT_6=11W and W/OPT_6=6/11.

### Full-history optimality proof of the constant strategy

Fix any history h of length d<6, not necessarily on path. Let k be the number of prior T-label choices, and let q_j be the number equal to T_j, so sum_j q_j=k and 0<=k<=5. The remaining players follow the prescribed A strategy.

If the current player chooses A, the final load of every core block C_l is

    L_l = 6-k+q_l,    where 1<=L_l<=6.

Its utility is sum_l 6/L_l.

If instead the current player chooses T_j, the load of C_j is still L_j: exchanging this current A for T_j leaves C_j covered once by the current player. The private block P_j has load q_j+1, so its deviation utility is

    6/L_j + 5/(q_j+1).

The utility difference between prescribed A and T_j is exactly

    sum_{l != j} 6/L_l - 5/(q_j+1) >= 5-5 = 0.

Here each of the five core terms is at least 1 because L_l<=6, while 5/(q_j+1)<=5. This proves optimality at every ordered history, against every available label, under the single actual constant successor strategy. All ties are allowed. The complete constant strategy is therefore a pure SPE, without any path-only or frozen-inconsistent continuation argument.

## Reproducibility and independent replay

`tight_single_support.py` creates `tight-single-support.json` with integer atom weights and `tight-single-support-strategy.csv` with every ordered decision history. The common verifier `verify_spe_certificate.py` replays all seven-action histories and checks each node against each alternative's real recursively replayed terminal outcome. It does not use the attainable-outcome DP.

Commands, from the repository root:

    python research/workspaces/n6-boss3-20261118/independent/tight_single_support.py
    python research/workspaces/n6-boss3-20261118/independent/verify_spe_certificate.py research/workspaces/n6-boss3-20261118/independent/tight-single-support.json research/workspaces/n6-boss3-20261118/independent/tight-single-support-strategy.csv

The exact replay result is recorded in `tight-single-support-verification.json`.

## Remaining original problem

This result rules out a counterexample only when all six realized coverage sets coincide. It imposes no restriction on the catalogue's off-path labels and fully preserves all-history quantifiers. A half-coverage counterexample, if one exists, must use at least two distinct realized coverage sets. A useful next local case is exactly two realized coverage sets, where final-node charge weights are no longer uniform over the realized union; any extrapolation needs a new argument.
