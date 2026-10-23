# Parent reconstruction of the maximal-topic reduction boundary

Status: independent internal mathematical review, not external review or a
novelty claim. Q-CAG-HALF remains OPEN.

I reconstructed the two suffix arguments from the agent's exact statement and
then checked its proof. With b already covered and g fresh groups/g remaining
players, choosing a fresh A forces the same state with g−1, hence gives 3.
Every other action is bounded strictly below 3 by an existing cover. This
uses all possible SPE continuations, not a fixed tie selector. In the second
state there is one B group still missing A and one extra remaining player;
the final A of that group gives 2 while alternatives give at most 3/2.
The induction then forces fresh A's followed by this final A.

Before the first b-cover, a history of distinct A's has g+1 remaining players
and g untouched groups. Choosing D guarantees 2; repeating an old A gives at
most 3/2. Choosing a fresh B leads to the second suffix state, whereas choosing
an old B leads to the first. Both cover every A group and b, losing only d.
Repeated fresh-A decisions terminate after at most k steps. Thus every SPE
of the maximal-only catalog covers at least 3k+1 customers.

Attainment needs history-dependent completion: after a fresh A_j deviation
from the designated old-B state, the next designated old B must be B_j,
not the original B_i. The submitted proof explicitly makes this switch.
The deviating A_j then gets 2 and cannot gain. Root B_1, D, and any B_i
give 2, while an A_i root deviation is met by this old-B_i completion and
also gives 2. Arbitrary remaining subtrees can be filled with SPE because
the forced suffix lemmas quantify over every child equilibrium.

I found no fatal objection in these arguments, including k=1, old-B versus
fresh-B counts, or full ordered-history completion. The imported full-catalog
SPE is the existing collision-free family, and is not a new construction.
The all-k maximal-only welfare theorem is the new part. A second internal
cleaner review has been requested from the exchange agent and is recorded
separately when delivered.
