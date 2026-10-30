# Correction: the old 15/7 layer did not impose complete pair coupling

2026-10-21. Root's independent attack identified a fatal scope error in the
round1 description. The underlying rational 15/7 primal/dual certificate is
valid for its selected constraints. Its preserved JSON layer name containing
`all-two-topic-coupling` and the old claim of complete pair consistency were
incorrect. Original certificate bytes are preserved; main prose and README
now explicitly retract that scope.

For distinct topics a,b and three providers write the six payoff data as
(A,B,X,Y,Z,W) for pure a, pure b, and the two actions in counts (2a,b), (a,2b).
The old rows were

\[
 Z-Y=3(A-B),\qquad X-W=\tfrac32(A-B).
\]

Their difference already implies same-support conservation
2X+Y=Z+2W. Thus they have rank two rather than the required rank three.
Checking a derived pair coverage range cannot repair the specified payoff
values. The missing independent row can be taken as

\[
 2X+2W=Z+3B.
\]

The three rows are independent: their minor on coordinates (Y,X,Z) has
determinant one. They annihilate each of the three actual pair-customer
columns (likes a only, b only, or both). Those columns are independent, so
the common signed pair payoff map is exactly their three-dimensional null
space. This establishes the corrected constraint scope without rank guesses.

`complete_pair_v2.py` adds this third row on every one of the 15 topic pairs,
while retaining the same 43-history full strategy, all 258 true incentive
comparisons, all 2520 sharp same-topic dilution rows, all same-support total
equalities, normalization at root {0,3,4}, and fixed comparison {1,2,4}.
The exact new labeled-closure optimum is **2**. The 15/7 obstruction therefore
does not survive complete pair coupling on this strategy/comparison.

`complete_pair_v2.json` stores rational primal and dual certificates.
`verify_complete_pair_v2.py` imports no optimizer or candidate generator. It
rebuilds every comparison and dual coordinate, then reconstructs the three
customer masses for each pair and directly checks all six payoff entries
(90 reconstructions). This independently verifies the intended pair scope
on the accepted vector. TC-DIL-1, E+BC, and the direct common-moment layers
are unaffected by this correction.

Reproduce from repository root:

```sh
python3 research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/tree_coupling/round2/complete_pair_v2.py
python3 research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/tree_coupling/round2/verify_complete_pair_v2.py
```
