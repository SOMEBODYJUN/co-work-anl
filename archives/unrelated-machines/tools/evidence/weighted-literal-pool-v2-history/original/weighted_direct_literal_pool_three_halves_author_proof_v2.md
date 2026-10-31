# Weighted direct literal pools — author Proof v2

2026-10-18 root/boss11, scratch only. Exact SHA d3e958202875617bd2bf2f189fee6b98606ce346ab0342b46cd5c5632b3f743f. Root independently derived this pairing construction before routing the Exact, and wrote this file only after actually fully reading typed's frozen independent reconstruction SHA5aa835cabfe7bf94ef43c554692e132ad6d06e80f6e38707970d6b07e32265be. Typed's candidate-author/standard-slot familiarity remains disclosed; root is not a blind reviewer. The argument below is a different but equivalent sorted-slot realization.

For each variable/sign sort all of its actual occurrence identities by decreasing b, including zeros. If nonempty, put its first occurrence into a special slot shared with the first occurrence of the other sign of this same variable (if present). Pair the remaining occurrence list as (2,3),(4,5),... with a possible final singleton, giving each pair its own unit slot. No other pair/variable is merged. These are computational nodes, not physical machines.

Give each clause a node adjacent to the slots containing its actual occurrences. Sending mass1/k_c from that clause to each occurrence's slot gives a fractional matching of row sum1; every slot contains at most two occurrences, each mass<=1/2, so all column capacities1 hold. Coalesced multiple clause-slot edges keep an actual occurrence witness. Deterministic integral bipartite matching therefore covers every clause, and each chooses its matched original occurrence. No occurrence or clause is used twice.

For each variable at most one of its two first occurrences can be selected: they share one unit slot. Choose f_v's physical pool on a sign whose first occurrence was not selected; if a sign has no occurrences it is also suitable. For that sign no selected weight is w_1, and each remaining slot contributes at most its maximum. Thus its total selected query weight is at most

    w_2+w_4+... <= (w_1+w_2+w_3+...)/2 <=1/2.

The comparison pairs w_(2t) with w_(2t-1). It does not assume uniform occurrence weights or discard any zero. The other sign's actual selected queries are a subset of all its eligible occurrences, so its load is at most its full budget1.

Put each clause selector on its matched occurrence root and export exactly that original query to its own pool. Every other query stays at its own root with time1. Put each f_v on the selected false pool above. Every root then has one unit selector or one unit query; the f pool has at most1+1/2, the other at most1. All original jobs run exactly once on original finite endpoints. Empty formulas with unused variables directly choose a pool for each f; when there are no machines otherwise the specified idle branch has no jobs and load0.

The sorted lists, slots and witness graph have O(N+L+M) size; matching is deterministic polynomial, with comparisons and exact rational sums charged by original binary encodings. The fractional mass1/k merely proves feasibility; no expansion by a denominator, inverse b or unused finite time is performed. Repeated literals remain different roots/jobs. This proves the complete stated v2 schedule and per-pool strengthened bounds. It does not cover full eligible budgets greater than1, extra guards/endpoints, or general UM, and makes no sharpness/global novelty claim.
