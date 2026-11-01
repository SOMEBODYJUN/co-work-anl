# Exact local claim ledger

General Q-CAG-HALF remains OPEN with the shared model and full quantifiers.
All objects below are common-catalog unit games with full-history pure SPE.
No external review, novelty certification or half counterexample is claimed.

## B9-MAXIMAL-PRUNING-NO-v1

For every integer k>=1, take distinct customers X_i (two per i), a_i, b,d.
The maximal catalog consists of A_i=X_i+{a_i}, B_i=X_i+{b}, D={b,d}; with
k+1 players its minimum SPE welfare is exactly3k+1. Adding C_i=X_i gives a
catalog admitting complete SPE welfare2k+2. Both optimal coverages are3k+2.
For k>=2, L(full,m)>=L(maximal,m) is false; any reverse comparison needs
factor at least3/2 asymptotically. Opposite monotonicity is not settled.

Dependencies: CAG-MODEL, existing collision-free full-catalog strategy,
new all-SPE maximal-catalog suffix induction and attainment construction.
Evidence: `independent/maximal_catalog_boundary.md` and its finite exact
checks; parent reconstruction in `parent/maximal_catalog_review.md`.
Status: complete candidate proof with parent internal review; second
independent cleaner reconstruction reported no fatal objection and is saved
separately. No external review. This is a proof-transfer bridge boundary.

## B9-POPULATION-MONOTONICITY-NO-v1

Common catalog A,B,C,D, customer type counts AB9,C1,BC7,AD2,ABD11,CD10.
Unique full pure SPE at m2 has ordered path AC, welfare40, payoffs22,18;
at m3 it has path DBB, welfare39, payoffs47/3,35/3,35/3. Every node's
nonself comparison is strict. OPT2=OPT3=40. Minimum SPE welfare therefore
is not population-monotone. Scaling all counts by a positive integer
preserves comparisons and gives an arbitrarily large absolute drop; the
populations remain two and three.

Dependencies: definition-level finite backward induction, exact rational
full-tree comparisons. Evidence: author certificates/audit in `exchange/`;
independent parent all-outcome/replay oracle in
`parent/population_independent_audit.py`. Status: complete finite
counterexample with independent internal reconstruction, no fatal objection.
Does not refute half or induction with signed error.

Smaller type counts AB3,C1,BC2,AD1,ABD3,CD3 give W2=13,W3=12,OPT13;
this is a separate supporting version, not the strict version's statement.
