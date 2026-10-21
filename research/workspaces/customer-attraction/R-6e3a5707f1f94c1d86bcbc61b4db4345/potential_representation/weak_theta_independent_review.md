# Independent attack: disjoint copies of the 36-customer example

Status: the auxiliary counterexample survives this independent mathematical
attack. This is an internal review, with no external review or novelty claim.
Q-CAG-HALF is neither proved nor refuted.

I reconstructed the strategy and local arithmetic before reading the author's
`equilibrium_tree/weak_theta_replication.md`. The blind reconstruction used a
last-touched-block schedule; the author's fixed priority for blocks with two
entries, then one entry, also works. No direct-sum theorem for arbitrary SPEs
is being invoked.

## Object checked

Take k disjoint customer blocks, each with six topics X0,X1,X2,Y0,Y1,Y2.
There is one unit customer for every cross-group pair and three distinct unit
customers for each set consisting of two X topics and two Y topics. Thus each
block has 36 unit customers. The common catalogue contains the 6k block topics,
and there are m=3k sequential providers.

The claimed complete-history pure SPE has W=34k, while OPT_m=36k and theta_m=12.
It refutes only W >= (m-1/2) theta_m for k>=4, with signed gap
W-(m-1/2)theta_m=6-2k.

## Blind arithmetic and the dangerous deviation

For a block-local ordered prefix h, let J(h,a) be the joining player's utility
immediately after choosing a, before any later players enter that block. Since
later entry only increases denominators, J is an upper bound on that player's
eventual utility under every continuation.

Exact arithmetic, computed directly from the customer definition, gives:

| Prefix h | Joining values, by topic order X0,X1,X2,Y0,Y1,Y2 |
| --- | --- |
| empty | 21,21,21,21,21,21 |
| X0 | 21/2,33/2,33/2,29/2,29/2,29/2 |
| X0,X1 | 9,9,12,10,10,10 |
| X0,Y0 | 25/3,12,12,25/3,12,12 |
| X0,X1,X2 | 15/2,15/2,15/2,15/2,15/2,15/2 |
| X0,Y0,Y1 | 20/3,35/4,35/4,22/3,22/3,19/2 |

Group exchange, group-internal relabelling and player permutation cover all
prefix classes used here. A repeated two-entry prefix has best join 15.

The potentially fatal direct-sum deviation is entering a block already closed
with three distinct topics. Its joining utility is at most 19/2, strictly below
the intended opening payoff 10. This is why an untouched block cannot be
undercut by further entry into a closed block. The number 19/2, rather than a
generic disjointness argument, carries this part of the construction.

## All-history extension

Call a history good when every block has at most three local entries and those
entries use distinct topics. A first bad prefix stays bad forever. At each
minimal bad prefix, choose one arbitrary pure SPE of its remaining finite
subgame by backward induction. These are disjoint subtrees, so this defines a
single strategy on every bad history.

At good nonterminal histories, use the author's policy: first complete a block
with two entries; otherwise enter a block with one entry; otherwise open an
empty block. Fixed block ties are allowed. In a singleton block choose the
opposite group. In a two-entry block choose an unused topic from the second
entrant's group. Three-entry blocks are never selected by this policy.

Every policy continuation from a good history fills every block to three
distinct entries: all its moves preserve goodness, there are exactly 3k total
moves, and each block has capacity three. Consequently an empty-block entrant
eventually earns 10, a prescribed singleton-block entrant earns 12, and a
prescribed pair-block entrant earns 12. Delays while other blocks are completed
do not change these utilities.

All possible deviations at a good node fall into the following exhaustive
classes.

| Destination and action | Child status | Deviator's final utility bound |
| --- | --- | ---: |
| Empty block, any topic | Good | 10 |
| Singleton block, fresh topic | Good | 12 |
| Distinct-pair block, fresh topic | Good | 10 or 12 |
| Singleton block, repeated topic | Bad | at most 21/2 |
| Distinct-pair block, repeated topic | Bad | at most 9 |
| Closed block, any topic | Bad | at most 19/2 |

When a singleton or pair exists, prescribed utility is 12 and every displayed
bound is at most 12. When none exists, prescribed utility is 10; only empty and
closed blocks are possible destinations, and their bounds are at most 10.
Bad-subtree play cannot increase the displayed immediate-entry bounds.

Backward induction on the remaining depth therefore proves SPE optimality at
every good history, while the grafted backward-induction subgames prove it at
every bad history. This is a complete-history proof. It does not require that
same-count ordered histories have the same replies.

At the empty root, the rule completes each block as X0,Y0,Y1 before opening the
next, so welfare is 34 per block.

## theta and optimum, including arbitrary repeated prefixes

For every global prefix of length 3k-1, some block has at most two entries.
Its best joining utility is 21 for zero entries, 33/2 for one entry, 15 for two
repeated entries, and 12 for two distinct entries. Therefore theta_m >=12.

A witness prefix has X0,Y0,Y1 in k-1 blocks and X0,Y0 in the last block.
Its largest joining utility is max(19/2,12)=12, giving theta_m <=12.
This minimum ranges over all legal prefixes, not just strategy histories.

Choosing all three X topics in every block covers all 36k customers with 3k
topics; hence OPT_m=36k. The SPE's ratio is 18/17 throughout, so no main-target
counterexample is present.

## Review conclusion and limits

The proof survives the following attacks: global reassignment between blocks,
starting another block during an unfinished block, repeats, fourth entries,
arbitrary multiple unfinished blocks off path, and all histories after the
first bad move. The author strategy passes. A general theorem saying that
disjoint SPEs concatenate would be unjustified; the local entry gap here is
the essential extra fact.

The adjacent independent audit checks the exact entry table and every good
state for k=1 and k=2, evaluating fresh deviations by the complete good-state
policy and bad deviations by their continuation-independent entry bounds.
These finite checks support the implementation; the all-k result is proved by
the preceding induction.
