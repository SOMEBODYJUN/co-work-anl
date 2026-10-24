# Empty-root PB checkpoint: the one-real contract and the missing credible amplification

2026-10-24. **Exploration note, not a general theorem or target counterexample.** This note fixes the original CAG-MODEL throughout: all customers and players have unit value/weight, topics may be repeated, and a proposed SPE must be optimal at every ordered history. It does not promote the background PB construction to an actual root path.

## A short calculation sufficient to leave the one-real contract

Use one segment of the old block catalogue. A real block has q distinct unit customers; a dummy block has Hq distinct unit customers, with integral multiplicities after a common scaling if necessary. A regular topic selects ell real blocks and the first k-ell dummy blocks, for 1<=ell<=k. The putative actual path is k copies of one k-real topic F, followed by n one-real/all-dummy topics, selecting distinct new real blocks. Let r=k+n and assume there are at least r+1 real blocks and at least 2k real blocks. Thus an extra fresh real block remains available at the actual last player's node, and the last copy player can query k wholly fresh real blocks.

The actual welfare per segment is q[r+(k-1)H], and each copy player's actual profit is q. The last player's one-real/all-dummy topic earns q+(k-1)Hq/n. Replacing one dummy by an extra fresh real block is a legal immediate last-player deviation. Therefore actual last-player optimality requires H>=n.

Now force the last copy player to choose k fresh real blocks. Impose the explicit extra contract that, in the resulting true continuation, each of the n remaining players uses at most one real block in this segment. This is a restriction on that branch, not a consequence of SPE. If c_a are the final loads on those k queried blocks, then sum_a c_a<=k+n. Reciprocal Jensen gives the deviator at least

    q sum_a 1/c_a >= q k^2/(k+n).

Its actual profit q can deter this deviation only if n>=k(k-1). Every r-topic comparator covers at most kr real blocks and all k-1 dummy blocks, so

    2W-OPT_r >= q[(2-k)r+(k-1)H]
                 >= q[n-k(k-2)]
                 >= q k > 0.

The same calculation sums over disjoint Cartesian segments when the stated assumptions hold segment by segment. It uses no old (G) condition and no frozen continuation. Its only role here is to show that the literal one-real punishment contract has already exhausted the available empty-root budget. We do not extend it to unlisted parameter ranges, arbitrary continuations, arbitrary catalogues, or arbitrary SPE.

## What a different construction would have to accomplish

Allowing several real blocks per punishment topic removes the Jensen hit-budget premise: one follower may hit as many as k queried blocks. That makes the simple counting obstruction disappear. However, it does not provide a credible punishment strategy. Every prescribed multi-real action must beat an alternative that replaces the already shared queried real blocks by currently fresh blocks, and the continuation after this alternative is a different, genuine ordered-history subtree.

There are two distinct cases. If fresh real blocks are available throughout every possible continuation and each topic admits arbitrary real-block exchanges, the eventual fresh alternatives make direct repeated targeting difficult. If punishment branches first cover a large fraction of the real-block universe, fresh outside options may disappear; this is the only concrete route in this geometry not already rejected by the above short calculation. Those extra real choices must themselves be optimal in their complete subgames, and the original copy player can also select every expansion/punishment topic from the common catalogue.

No all-history strategy achieving this saturation-and-targeting behavior has been found. The elementary coverage and payoff counts alone do not rule it out. They also do not constitute a candidate SPE.

## A useful all-input reformulation, with no claimed solution

For any hypothetical root SPE outcome, let C be its actual covered customers and U the customers omitted by that outcome. Every actual prescribed action lies inside C. In every actual prefix, every x in U has load zero. Thus the omitted part cannot obtain the flattening supplied by the legal high-load background in the PB counterexample. An empty-root construction must make U congested only after entry; it must simultaneously remove the last follower's other fresh U outside options, and it must control entry through every punishment/expansion topic itself.

This is a reformulation of the original obstacle, not a new inequality. In particular, no assertion is made that a method's failure implies half, that all omitted customers are private, or that all input catalogues satisfy an exchange property.
