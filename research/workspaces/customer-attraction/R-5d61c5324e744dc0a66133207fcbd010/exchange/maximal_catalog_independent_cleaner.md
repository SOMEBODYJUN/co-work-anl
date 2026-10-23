# Independent cleaner: the all-k maximal-only catalog boundary

2026-10-23. This is an internal independent mathematical check requested by the
parent, not external peer review. I reconstructed the mechanism from only the
statement and customer sets before reading
`../independent/maximal_catalog_boundary.md`. I found no fatal objection to its
all-k proof or exact outcome characterization. The original general half goal
remains OPEN.

## Object and quantified statement checked

For k>=1, each X_i has two distinct customers; a_i,b,d are all distinct from
these and each other. The common menu is A_i=X_i+{a_i}, B_i=X_i+{b}, D={b,d},
and m=k+1. Every ordered history and arbitrary pure SPE tie resolution is
included. The claimed terminal multisets are exactly all A_i plus D, and all
A_i plus one B_j. Their welfare is 3k+2 and 3k+1 respectively. Both menus,
including the larger menu with C_i=X_i, have OPT=3k+2.

## Independent reconstruction and stronger primitive

The following fresh-fill statement needs fewer prefix hypotheses than the
source uses. In **any** ordered prefix of the maximal-only game, suppose b has
already been covered, g groups are untouched (neither A_i nor B_i has appeared),
and exactly g players remain. Arbitrary repetitions in touched groups and
arbitrary old copies of D are allowed. Every SPE suffix uses the g fresh A_i,
once each, and each future player receives 3.

Induct on g. A fresh A_i leaves a child of this same form and therefore guarantees
3 against every child SPE. Any touched A_j has terminal payoff at most
2/2+1=2; any touched B_j has at most 2/2+1/2=3/2, because both X_j and b have old
coverage; a fresh B_j has at most 2+1/2=5/2; D has at most 2. Thus only a fresh
A_i can reach the guaranteed payoff 3. The same argument applies at every
ordered prefix separately; equal counts need not share selected continuations.

The second primitive is also sound. If exactly one old B_i and no old A_i is
present in its group, all other touched groups have a single A_j, and there are
g untouched groups and g+1 players left, every SPE fills fresh groups with A's
and finally chooses A_i. For g=0, A_i yields 2 while every other action yields
at most 3/2. For g>0 a fresh A_j guarantees 3 by the induction hypothesis, while
fresh B is at most5/2, old actions at most2, and D at most2. Hence only fresh A
is selected. This reasoning uses current players' actual child SPEs, never a
frozen suffix.

From a b-uncovered prefix of distinct A's, with g untouched groups and g+1
players left, deviation D enters the first primitive and yields exactly2.
An old A repeat yields at most 3/2 and is excluded. The remaining current
choices are fresh A (same state with g-1), fresh B (second primitive), old B
(first primitive), or D (first primitive). They exhaust the common menu.
Induction thus gives precisely the claimed list of terminal multisets as an
upper bound on possible outcomes.

## Attainment and the sensitive branch checked

The complete-SPE attainment construction is valid. At a b-uncovered prefix
containing an old A_i, one can designate old B_i as the next action, give it
payoff 2 using fresh-fill suffixes, and punish every **fresh A_j deviation** by
re-designating that newly inserted A_j and selecting old B_j next. This makes
the deviant A_j player's terminal payoff 2. The induction decreases g, and all
nonfresh-A deviation subtrees are either covered by the two primitives or may
be completed by any finite-game SPE when their immediate upper bound is at
most3/2. Crucially, the designated group must change from i to j on this
branch; the source explicitly does so.

At the root, B_1 followed by the one-extra suffix gives payoff 2. Root D gives2.
Each root A_i can be followed by the designated-B_i construction and also gives
2 to the root player. Hence root B_1 is optimal with every off-path subtree
SPE. Relabeling attains every all-A-plus-B_i multiset. The same root deviations
allow D as root and attain all-A-plus-D. This establishes equality of the
outcome set, not just its welfare bound.

## Bridge orientation and limits

The source uses the correct refuted orientation
L(full,m)>=L(maximal-only,m). For k>=2 its known full-catalog SPE W=2k+2 is
strictly below the maximal-only minimum 3k+1, while OPT remains3k+2. The ratio
necessary condition tends to2/3. The proof does not identify the full catalog's
minimum and does not refute the opposite monotonicity inequality. Keeping
maximal topics as accounting objects while retaining the original menu and
continuation tree remains legitimate.

The full-catalog C_1,...,C_k,D witness is imported from the existing collision-
free family; this cleaner checked the new maximal-only argument. The parent
already performed an independent finite exact audit and a separate symbolic
reading. No new finite computation is claimed here.
