# Boss1 mathematical review: seven distinct topics and the frozen five-player policy

The core is the v2 fixed 215899-unit-customer instance with nine positive interest types and a complete 2801-node policy. Its default action is 0 with nine specified exceptions; all prescribed actions lie in {0,2,3}. Boss1 read the complete core page, the complete ordered-offpath-mutation program page, and the static simultaneous-NE half-coverage theorem. Full evidence reading and lossless JSONL views are the worker's separately recorded responsibility.

## Fixed actual leaf and static comparison

The actual leaf is (3,0,0,0,0). The first player's utility is 119580/5+300/5+20=23996; each of the four other players receives 119580/5+300/5+100/4=24001. Their sum is W=120000.

Holding the other four actual actions fixed, the seven alternative payoffs for the first player are (23996,23996,23996,23996,23991,23996,23996). For any one of the four players originally choosing 0, they are (24001,24001,24001,23986,23996,23986,24001). These formulas directly verify static PNE. They are not a consequence of generic sequential IC: here the relevant true continuations can additionally be checked to agree with the fixed-other-action leaves. The worker confirmed these two vectors against the full mature JSONL reading.

Apply M-3a55169b86b64a7a99a13e612a389688 only after this point-specific static PNE premise is paid. With the five optimal comparison labels, static deviations give W≥Σ_x k_x/(1+c_x), and the pointwise union bound gives OPT_5≤2W. This derives the half-coverage subclaim for this leaf, not its complete-history SPE, distinctness, exact ratio, or a universal sequential guarantee. No target-core assertion should be recycled as a self-loop premise.

## Exact optimal support and geometric restriction

The positive private types for labels 1,2,4,5,6 force all five labels if all customers are covered. Their support indeed covers every one of the nine types, so it is the unique optimal five-label support and OPT_5=215899. Hence OPT_5/W=9/5−101/120000 and 2W−OPT_5=24101.

Labels 0 and 3 differ on the 100 customers of {0,1,2,4,6} and the 20 customers of {3,5}, so their symmetric difference is 120. The complete pair comparison certifies this as the minimum. Thus the frozen d=1000 separation inequality is tight for this pair. It is a constraint of this particular saved instance, not a uniform sharp constant for all distinct-topic games.

The offpath mutation invariant protects ordered actual prefixes. It explains how one run can preserve an ordered leaf while changing offpath policies and customer weights. It does not certify a frozen policy as SPE without its full real-continuation inequalities, does not establish minimum-SPE welfare, and does not establish exhaustive search over leaves.

## Optional analytic extension, outside the original core

Adding t nonnegative integer copies of the nine-customer game with five customers interested in {0,2,3} and one private customer for each of 1,4,5,6 preserves this same policy's SPE. On each added copy every prescribed action is a big label, giving 5/(ν+r)≥1 at any history; deviating to a private label gives at most 1. Fixed-policy IC is additive over disjoint customer copies. The combined game therefore has W=120000+5t and unique optimal support 12456 with OPT_5=215899+9t. The minimum symmetric difference remains 120, so d=1000 holds only at t=0; the ratio is 9/5−101/(120000+5t). This observation clarifies the quantifier boundary and does not replace the core's finite claim or warrant an unrelated new node merely for connectivity.
