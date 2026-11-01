# Dominated topics prevent reduction to a maximal subcatalog

Status: a new consequence of the previously proved collision-free family, with a
new all-SPE analysis of its maximal subcatalog. This is a bridge obstruction,
not a counterexample to Q-CAG-HALF. The proof below is symbolic for every number
of groups; the accompanying computation is only a finite independent check.

## Exact bridge and orientation

For a finite common catalog S let Max(S) be its inclusion-maximal topics. Write
L(S,m) for the minimum welfare among all complete-history pure SPE of the game
with catalog S and m players. A tempting proof-transfer bridge is

    L(S,m) >= L(Max(S),m).                                      (B)

Equivalently, every full-catalog SPE would have welfare at least that of some
maximal-only SPE. Because deleting dominated topics preserves OPT, this bridge
would allow a lower-welfare theorem for maximal-only catalogs to transfer back
to arbitrary catalogs.

The construction below refutes (B). It does **not** refute the opposite
monotonicity inequality L(S,m) <= L(Max(S),m). An initial exploratory message
misdescribed the orientation; all statements here use (B) explicitly.

## Uniform family and conclusion

Fix any integer k>=1 and m=k+1. For each i in {1,...,k}, let X_i be a two-customer
set and let a_i be another customer. Let b,d be two more customers, all distinct.
The full catalog consists of

    A_i = X_i union {a_i},   B_i = X_i union {b},
    C_i = X_i,              D = {b,d}.

The maximal subcatalog M contains exactly the A_i,B_i,D. Every customer is a
distinct unit customer, and every player has unit weight. Both catalogs have

    OPT_(k+1) = 3k+2,

as witnessed by A_1,...,A_k,D.

**Theorem.** For every k>=1:

1. The full catalog has a complete-history pure SPE whose ordered outcome is
   C_1,...,C_k,D and whose welfare is 2k+2.
2. Every complete-history pure SPE of M has welfare at least 3k+1.
3. M has a complete-history pure SPE of welfare exactly 3k+1. Therefore
   L(M,k+1)=3k+1.

In fact, its entire set of SPE terminal multisets is exactly

    {A_1,...,A_k,D} and {A_1,...,A_k,B_i} for i=1,...,k.          (T)

Thus there are exactly k+1 count outcomes, despite arbitrary ordered-history
continuation selection and ties.

For k>=2, the full SPE in item 1 is worse than **every** maximal-only SPE. For
k=2 this is already an eight-customer, three-player counterexample to (B):
full welfare 6 versus maximal-only minimum 7, while OPT=8 in both games.

The comparison is unbounded in the number of players and topics. If one instead
requires W(full SPE) >= c L(M,m) universally, then necessarily c<=2/3, since

    (2k+2)/(3k+1) -> 2/3.

Equivalently, a comparison L(M,m)<=K W(full SPE) needs K>=3/2. We do not claim
that 2k+2 is the full catalog's minimum for all k; the stated SPE suffices for
these necessary conditions.

## Full-catalog strategy: exact dependence

Item 1 is precisely the complete Q/B-state induction already proved in
`research/current/customer_attraction/collision_free_three_halves_family.md`,
Sections 2--4. That proof permits arbitrarily many old A's and fills every other
ordered-history subtree by a genuine pure SPE. Thus its all-history quantifier,
including arbitrary ties, is available here without strengthening it. Its
actual path is collision-free; its on-path players each receive 2.

The new work below proves items 2--3 without importing a canonical tie rule or
assuming that two equal-count histories have the same continuation.

## A forced fresh-A suffix lemma

Consider any fixed ordered history in M in which b has already been covered.
Suppose there are g untouched groups, each meaning that neither A_i nor B_i has
been chosen, and exactly g players remain. Every touched group already has a
chosen A_i. The history can additionally contain D or a B_i, but each group has
only its one A_i and, possibly, one B_i; no other repetitions are present.

Then **every** SPE continuation consists of the g fresh A's, each exactly once,
in some order, and each future player receives 3.

Proof by induction on g. The g=0 case is empty. For g>0, a player can choose any
fresh A_j. Its child history meets the same conditions with g-1 fresh groups and
g-1 players, so by induction every child SPE uses only the other fresh A's. The
current payoff is therefore 3. No topic has size more than 3, so every current
SPE choice must attain 3. Fresh B_j has payoff at most 2+1/2; a topic of a touched
group has payoff at most 2; D has payoff at most 2. Thus only a fresh A can attain
3. Induction applies to its actual child. This proves the assertion for every
possible tie resolution and every complete ordered-history SPE.

The bounds just used need not be sharp. They hold against every continuation:
b already has one old covering player; a touched group's X_i already has one
old covering player; any touched A_j's a_j is already covered. Future players
can only decrease these terminal shares.

## A forced one-extra-player suffix lemma

Now suppose the history has exactly one chosen B_i, has no A_i, and every other
touched group has exactly one A_j. No D and no other B has been chosen. Let g
groups be untouched and let g+1 players remain.

Then **every** SPE continuation chooses all fresh A's in some order, then A_i.
The fresh-A players each get 3, and the final player gets 2.

For g=0, A_i yields 2/2+1=2. Every other A_j has payoff 2/2+1/2=3/2;
every B_j has payoff at most 2/2+1/2=3/2; D gives 1/2+1=3/2.
Hence A_i is the unique best topic.

For g>0, choosing a fresh A_j leaves the same type of state with g-1 untouched
groups. By induction no future player touches this A_j, so the current payoff
is 3. Every fresh B_j is bounded above by 5/2 because b is already covered.
Every old topic or D is bounded above by 2. Therefore every SPE mover must pick
a fresh A, and the induction continues. Again no tie selector was imposed.

## Analysis before the first coverage of b

Consider a history containing only distinct A topics, with g untouched groups
and g+1 players remaining. This includes the empty initial history with g=k.

The current player can choose D. The resulting child is a forced fresh-A suffix
of the first lemma, so the D player gets exactly 2 in **every** child SPE.
Consequently every current SPE payoff is at least 2.

A repeated old A_j yields at most 2/2+1/2=3/2 against every continuation, so it
cannot be chosen. Each legal current action consequently has one of four forms:

* A fresh A_j: the child is another history of this same form, with g-1 fresh
  groups and g players remaining.
* A fresh B_i: the child meets the one-extra-player lemma. It fills the other
  fresh groups with A's and ends with A_i, so the final outcome contains every
  A_j and B_i, with welfare 3k+1.
* An old B_i: the child meets the fresh-A suffix lemma. It fills all remaining
  fresh groups, so again the final outcome contains every A_j and B_i, with
  welfare 3k+1.
* D: the child fills every fresh group with A's, giving all customers and welfare
  3k+2.

If g=0, the first case is absent and at least one old A exists because k>=1;
the remaining alternatives give the stated bound directly. Induction on g proves
that every initial SPE has welfare at least 3k+1.

## Attainment and full-tree completion

At the root choose B_1. Its child is the one-extra-player state, whose SPE
continuation is forced to be the fresh A's followed by A_1. The root B_1 player
therefore gets 2, and the final welfare is 3k+1.

For every alternative fresh B_i or D, the corresponding child lemmas yield root
payoff exactly 2. For an alternative A_i, choose this valid child SPE: next pick
the old B_i and then fill all other groups with fresh A's. We justify the
existence of this child SPE by the following strengthened induction.

At any b-uncovered history of distinct A's containing at least one old A_i,
there is a complete SPE that chooses this designated old B_i immediately and
then fills all fresh groups with A's. The current mover gets 2. With no fresh
groups this is an ordinary last-player best reply. With g>0 fresh groups,
attach the first lemma's forced suffix to the designated action B_i. After
each fresh-A_j deviation, apply the induction hypothesis at its child with the
**newly chosen A_j** as designated group: the next mover selects old B_j, which
reduces the deviant A_j player's payoff to 2. (Retaining the original designated
group i here would be incorrect: the fresh-A_j deviant would otherwise get 3.)
Fresh-B and D deviations have payoff 2 by the forced lemmas. Other old-B
deviations have payoff 2 by the first lemma. Repeated-A deviations have payoff
at most 3/2 under any child SPE. Hence the designated action B_i is optimal,
and every ordered-history child has been filled with a genuine SPE.

This strengthened induction supplies the required continuation after each root
A_i deviation. The original root A_i player finally gets 2/2+1=2. Thus every
root alternative is bounded by the selected root B_1 payoff 2. Unspecified
descendants inside a forced lemma may be filled by arbitrary SPE because each
lemma was proved for every continuation, including all ties.

This proves a complete pure SPE with root B_1 and supplies the attainment claim.
Relabeling the groups attains every all-A-plus-B_i multiset. Root D is optimal
with the same off-path punishments after A_i deviations, so all-A-plus-D is
also attained. The analysis before the first coverage of b already excludes
every other terminal multiset, proving (T).

## What this does and does not advance

The result identifies a concrete, scalable source of difficulty in an arbitrary
catalog: dominated interior topics can create welfare losses that disappear
after maximal-topic pruning, even though OPT and all maximal covers are kept.
In particular, a universal lower bound proved only for maximal-topic games
cannot be transferred by (B), even with arbitrary favorable maximal-game ties.

It neither disproves half coverage nor rules out a proof using maximal covers
as accounting objects while keeping the full original continuation tree.
Existing maximal-cover structural theorems do exactly the latter and are not
affected. It also does not settle the opposite catalog monotonicity inequality.

## Reproduction

Run `python3 research/workspaces/customer-attraction/R-5d61c5324e744dc0a66133207fcbd010/independent/check_maximal_catalog_boundary.py`.
It uses exact rational all-outcome backward induction and, at k<=3, expands and
independently verifies full ordered-history certificates. The mathematical
all-k result rests on the preceding induction, not the finite run.
