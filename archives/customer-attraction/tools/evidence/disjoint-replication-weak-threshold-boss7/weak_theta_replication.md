# Disjoint replication defeats the weakened last-player ceiling bridge

Status: candidate proof with exact local arithmetic audit; independent attack requested.
This concerns an auxiliary bridge only. Q-CAG-HALF remains open.

## Statement and base instance

For every integer k>=1 there is a CAG-MODEL instance with m=3k providers,
6k distinct topics and 36k unit customers, and a complete-history pure SPE
with welfare W=34k. Its global last-player worst-best-reply value is

    theta_m = min_{h in S^(m-1)} max_T sum_{x in T} 1/(1+c_x(h)) = 12.

Consequently W >= (m-1/2) theta_m fails for every k>=4: the signed gap is
34k-(3k-1/2)12 = 6-2k. At k=4 this gives m=12, W=136 and the proposed
right side 138. The actual optimum is 36k, so the construction does not
violate half coverage; its inefficiency is only 18/17.

Each of k blocks is a disjoint copy of the existing 36-customer example
in `research/current/customer_attraction/aggregate_theta_counterexample.md`.
In one block there are topic groups X={X0,X1,X2}, Y={Y0,Y1,Y2}:

* For each x in X, y in Y, one unit customer likes exactly {x,y}: 9 customers.
* For each two-element I subset X and J subset Y, three distinct unit
  customers like exactly I union J: 27 customers.

Customers from one block like no topic in another block. Every topic has
21 customers. Three distinct topics from one group cover all 36 customers.

## Exact local payoff facts

Here joining means adding one player to a local prefix and evaluating that
player before any further entrants. Further entries in this block can only
decrease this payoff.

| Local prefix | Joining action | Joining payoff |
| --- | --- | --- |
| One topic a | Repeat a | 21/2 |
| Two distinct same-group topics a,b | Repeat a or b | 9 |
| Two distinct same-group topics a,b | Third topic of their group | 12 |
| Two distinct same-group topics a,b | Any topic in the other group | 10 |
| Two distinct opposite-group topics a,b | Repeat a or b | 25/3 |
| Two distinct opposite-group topics a,b | Any unused topic | 12 |
| Three distinct same-group topics | Any topic | 15/2 |
| Mixed triple of distinct topics | The used minority topic | 20/3 |
| Mixed triple of distinct topics | A used majority topic | 22/3 |
| Mixed triple of distinct topics | An unused minority-group topic | 35/4 |
| Mixed triple of distinct topics | The unused majority-group topic | 19/2 |

In a distinct same-group triple each player earns 12 and its coverage is 36.
In a distinct mixed triple the minority-group player earns 10, each
majority-group player earns 12, and the coverage is 34. In particular the
maximum joining payoff after any distinct triple is at most 19/2 < 10.

## Nice histories and a complete strategy

For an ordered global history, retain the ordered local subsequence in
each block. Call the history *nice* if every local subsequence has length
at most three and contains no repeated topic. A block of length three is
closed. A nice nonterminal history always has an unclosed block, because
there are precisely 3k moves in total.

Fix all block and topic tie orders once. At any nice nonterminal history:

1. If some block has local length two, choose the first such block. For
   a same-group pair, select its group's unique unused topic. For an
   opposite-group ordered pair (a,b), select the first unused topic in
   b's group.
2. Otherwise, if some block has local length one, choose the first such
   block and select the first topic in the opposite group.
3. Otherwise start the first empty block with its topic X0.

After a non-nice history, use any pure backward-induction SPE of that
remaining finite subgame, with fixed lexicographic ties. A non-nice prefix
can never become nice again: a local repeat or a fourth local entry cannot
be removed. Thus the lexicographic subtree choices and the nice-history
rule are consistent and give one action at every ordered history. They
do not identify same-count histories or discard any off-path histories.

## Nice-state induction: all deviations are covered

Induct backward on the number of remaining players at every nice history.
Every nice child has the specified sub-SPE by induction. Every non-nice
child has the chosen ordinary backward-induction sub-SPE.

Under the nice rule, a block always closes on its third entry and is never
visited again. Every nice terminal history has exactly three entries in
every block: its 3k entries are distributed among k blocks with each local
count at most three. Thus every partial block does eventually close.
A first entrant to an empty block eventually gets 10:
the later second entrant chooses the other group, and the third entrant
joins the second entrant's group. A second entrant to a singleton block
gets 12, for both possible distinct-topic classes. A third entrant chosen
by rule 1 gets 12. The scheduling among blocks does not alter these local
terminal payoffs, since customers are disjoint between blocks.

Hence the prescribed current mover gets 12 whenever a partial block of
length one or two exists, and otherwise gets 10. Evaluate each alternative:

* Entering an empty block keeps the history nice and makes the mover its
  first entrant, with terminal payoff 10.
* Entering a singleton block with a fresh topic keeps the history nice.
  The eventual third entrant is selected by rule 1. If the pair is in one
  group, all three earn 12; if it is mixed, the third entrant joins the
  second entrant's group. The deviator therefore gets 12 in either case.
* Entering a distinct pair with a fresh topic closes a distinct triple,
  keeps the history nice, and gives the deviator either 10 or 12.
* Repeating the singleton topic makes a non-nice child. The deviator's
  immediate payoff is 21/2, and any later entry only decreases it.
* Repeating either topic of a distinct pair makes a non-nice child. The
  immediate payoff is 9 or 25/3, again an upper bound on the final payoff.
* Entering a closed block makes a non-nice child. Its immediate payoff is
  at most 19/2 and bounds the final payoff from above.

The only non-nice deviation above with immediate payoff above 10 is a
singleton repeat. Such a singleton exists only when the current nice-rule
payoff is 12, so 21/2 < 12 suffices. A fresh entry to a singleton also
arises only at a state whose prescribed payoff is 12. At a state with
current payoff 10 there are only empty and closed blocks. Thus every
alternative payoff is at most the prescribed current payoff in every
case. This completes the induction and proves the complete strategy is
a pure SPE, including arbitrary off-path histories.

At the root the rule completes each block as (X0,Y0,Y1) before starting
the next, so W=34k.

## The global theta value and optimum

Take any global prefix of 3k-1 moves, allowing arbitrary repetition. Some
block has at most two entries. For zero entries its best joining payoff
is 21; for one entry it is 33/2; for two repeated entries it is 15; for
two distinct entries it is 12. Hence its best joining payoff is at least
12 and theta_m>=12.

Conversely, put (X0,Y0,Y1) in k-1 blocks and (X0,Y0) in the last block.
This is a legal global prefix of 3k-1 moves. Closed-block best joins are
19/2 and the final pair's best join is 12. Therefore theta_m<=12.

Choosing all three X topics in every block uses 3k topics and covers every
customer, so OPT_m=36k.

The file `weak_theta_replication_audit.py` independently expands the base
36 unit customers and verifies every local arithmetic class used above.
Its arithmetic is exact. The all-k conclusion follows from the induction,
not from a finite search of complete strategy trees.

## Why the genuine oblivious-security bridge survives

For this family the actual oblivious value is exactly

    v_(3k)(0) = 15/2 + 5/(2k).

Indeed all 6k topics form a single orbit under block permutations,
permutations inside each X/Y group and exchanges of the two groups.
The query guarantee V(p)=min_B E_(a~p) f_B(a) is concave in p (a minimum
of linear functions). It is invariant under these automorphisms, since
they also permute the legal opponent tuples. Averaging any optimal p over
the automorphism group therefore gives the uniform query distribution
without reducing V. This argument concerns a static comparison game and
does not constrain any equilibrium strategies to symmetric ties.

For t local opponents, let g(t) be the minimum uniform-six-topic query
payoff in one block. Exact enumeration of local counts gives the table:

| t | g(t) | One minimizing local count vector, in X then Y order |
| --- | --- | --- |
| 0 | 21 | (0,0,0,0,0,0) |
| 1 | 29/2 | (0,0,0,0,0,1) |
| 2 | 10 | (0,0,0,0,1,1) |
| 3 | 15/2 | (0,0,0,1,1,1) |
| 4 | 19/3 | (0,0,0,1,1,2) |
| 5 | 161/30 | (0,0,0,1,2,2) |

The adjacent exact arithmetic audit exhausts all 462 nonnegative six-topic
count vectors of total at most five. This is a finite proof of the stated
local inequality, with no numerical tolerance:

    g(t) >= 15-(5/2)t   for every integer t>=0.

For t=0,...,5 this follows from the table; for t>=6 its right side is
nonpositive and every query payoff is nonnegative. Thus no finite
extrapolation is used.

Any global opponent tuple has local counts t_1,...,t_k summing to 3k-1.
Its uniform-global-query payoff is at least

    (1/k) sum_j [15-(5/2)t_j] = 15/2+5/(2k).

Put three distinct same-group opponents in k-1 blocks and two distinct
same-group opponents in the last block. The same uniform query then
earns exactly [(k-1)(15/2)+10]/k = 15/2+5/(2k), giving equality.
Therefore

    W - m v_m(0) = (23k-15)/2 > 0.

The replicated theta obstruction consequently refutes neither the strong
nor weak genuine oblivious-security aggregate bridge.
