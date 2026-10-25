# Definitions-first five-provider attack

2026-10-25. Scope: Q-CAG-HALF with exactly five unit providers, arbitrary finite common catalogue, uniform terminal shares, every complete-history pure SPE, arbitrary ties/repeats/empty themes. Latest user scope overrides the older root AGENTS general-only restriction. This note is an independent draft, not a half-coverage proof or counterexample.

## Blind derivation before reading the old five-provider proof

Fix the actual terminal union C and actual final payoffs u_1,...,u_5. Let T_1,...,T_5 be arbitrary optimum themes, and d_j=|T_j\C|. A deviation at actual position i gets at least d_j/(6-i), because these customers have zero fixed-prefix load and at most 6-i final competitors. Thus d_j <= (6-i)u_i for every i,j. Using only this security information gives sum_i u_i >= H_5 max_j d_j and missing optimal coverage <=5 max_j d_j, hence OPT_5 <=(1+5/H_5)W. It cannot approach two.

For the fourth player, after changing to T_j let L_j be the same original strategy's genuine last response. Write b_j=|(T_j\C)∩L_j|. Its deviation payoff is at least d_j-b_j/2. At the actual last node, L_j is a legal alternative and all its C-external customers would be exclusive, so b_j<=u_5. Therefore d_j<=u_4+u_5/2. The actual last player also gives d_j<=u_5. The critical issue is not merely bounded crowding: information about the real suffix's rational choice must pay for overlap and branch switching. Reading the old proof afterwards showed that these facts are subsumed by its stronger real reply menu interfaces.

The existing indexed proof gives approximately 2.0616947857207375 using 437 specified valid rows and also gives an exact relaxed feasible point above two. Consequently refining only a derivation already implied by those rows cannot establish the desired five-provider half bound. This note makes no claim that a richer full-tree argument is obstructed.

## A same-branch cardinality/coverage inequality

Let m>=1, let T be a largest catalogue theme with |T|=K>0, and force T at the empty root. For any arbitrary suffix tuple (rationality is unnecessary), write k_x for its load on customer x∈T, let d be this root player's terminal payoff, let Z be suffix coverage outside T, and let W_T=K+|Z| be this branch's total coverage. Since every suffix theme has size at most K,

    |Z| + sum_{x∈T} k_x <= (m-1)K.

Cauchy--Schwarz gives

    d = sum_{x∈T} 1/(1+k_x)
      >= K²/(K+sum_{x∈T}k_x)
      >= K²/(mK-|Z|).

Hence the exact valid inequality is

    W_T <= (m+1)K - K²/d.

For five providers, W_T<=6K-K²/d. If d<=u_1 by actual root SPE optimality, then W_T<=6K-K²/u_1. All denominators are positive for K>0. K=0 is the all-zero case. The inequality allows empty/repeated suffix themes and uses no tie assumptions.

Interpretation: a low payoff of a forced largest theme forces low welfare in that SAME genuine branch. It does not yet compare that branch with actual welfare. Applying a root theorem to the forced branch would be invalid because the forced root need not itself be optimal; only its suffix remains SPE. No valid cross-branch payment was derived.

## Next obligation

Either relate the full genuine forced-largest-theme branch to the actual path with a proved transfer budget, or bypass it. Any proposed relation must retain the original full strategy's actual responses, and may not declare the forced root to be an SPE. Parent is exploring complementary routes; this agent is available for independent attack of candidates.
