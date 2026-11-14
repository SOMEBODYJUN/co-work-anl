# AC3D fresh support: finite-chain obstruction and scope boundaries

## Read scope and dependency additions

The assigned core is `M-2ca8a524bdb746d286d02ddb687f380d` (version 1, pin `8fd29778f8226eb9a67546881d083a404d11c6bf26f6acfb4325210207e36cca`). I read all nine declared references in order, verified each declared SHA-256, parsed all three original certificate JSON files and all three replay JSON files, and ran the optimizer-free rational audit. The task initially had no read-only endpoints. I used local `map read-add` to add:

* `customer-attraction/finite-reply-chain-protected-omission-relaxations` (pin `a9e042947b6349dc154108184c0e8d3655939979257ec26363573dd58d57cfd7`), the broader finite LP object whose section 3 pays the exact finite primal/dual values; and
* `customer-attraction/protected-omission-complete-two-player-search` (pin `d1c84a299c86d62fb1164252a90afd0864f5390a026f2311c399315ce7892264`), the complete two-player search object needed to prevent conflating the partial-chain d=1 point with the full p=6 search point.

No deferred candidate was promoted. The model endpoint is the declared common labelled-catalog definition; the two read-added objects are comparison endpoints, not substitutes for the assigned object.

## Core finite chain and exact certificate

The common model has a finite nonempty labelled catalogue (duplicate or equal-cover labels and repeated actions retained), unit clients and unit providers, sequential ordered actions, equal split of each covered client, and complete pure-SPE quantification over every ordered history. The obstruction object fixes a two-provider tail with labels `A=0,B=1,T=2,Q=3` and, for depth `d=1,2,3`, total labels `p=2d+4`. It fixes the partial last-player response map `r(0)=1` and `r(a)=a+2` for `2<=a<=p-3`; the first actions `B=1,p-2,p-1` are deliberately omitted. Background atom columns are `(mask m, b)` with `1<=m<2^p` and `b=0,...,4`. Protection mass is only the zero-background mass whose mask omits A and B and contains T or Q. The finite relaxation sets tail profit `P=U_0(0,1)+U_1(0,1)=1`, keeps all tail IC rows for the retained first actions and root rows against them, and maximizes `D`.

The original supports and dual rows were read as exact rational strings; `audit.py` reconstructs the share coefficient for every atom and every ordered tail, checks every saved support, every retained IC slack, every dual remainder, and the full best-reply matrix. It reports `exact-saved-certificate-verification-passed` and explicitly records that the historical floating LP search was not rerun. The exact finite outcomes are:

| d | p | atoms | retained rows | support types | u | v | P | D/P | nonzero dual rows |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 6 | 315 | 17 | 8 | 4/9 | 5/9 | 1 | 10/9 | 9 |
| 2 | 8 | 1275 | 39 | 19 | 38/83 | 45/83 | 1 | 90/83 | 19 |
| 3 | 10 | 5115 | 69 | 38 | 286/621 | 335/621 | 1 | 670/621 | 29 |

For d=1,2,3 the dual has respectively 315, 1275, and 5115 nonnegative exact atom remainders; the saved positive supports attain zero remainder. The corresponding unit scales are 9, 166, and 14283 (21, 346, and 38753 unit clients after multiplying the saved masses). These are exact values only for the displayed finite domains `b<=4` and the displayed partial response patterns.

## All-best-reply completion obstruction

For an omitted first action `a`, a full completion preserving actual `(A,B)` exists only if at least one true last-player best reply `t` satisfies the first player's payoff `U_a(a,t)<=u`, where `u=U_0(0,1)`. This tests every tie and follows the deviating history's real continuation; it does not freeze the on-path response.

The replay matrices give the following unavoidable strict root gains:

| d | omitted first action | all best replies | minimum first payoff against a best reply | strict gain over u |
|---:|---:|---|---:|---:|
| 1 | B=1 | {4,5} | 5/9 | 1/9 |
| 2 | B=1 | {6,7} | 45/83 | 7/83 |
| 3 | B=1 | {8,9} | 335/621 | 49/621 |
| 1 | 4 or 5 | {1} | 2/3 | 2/9 |
| 2 | 6 or 7 | {1} | 54/83 | 16/83 |
| 3 | 8 or 9 | {1} | 134/207 | 116/621 |

Thus no choice among best replies can preserve the actual root action for any of the three saved points. The result is a precise obstruction to extending these partial policies and is not a claim that the finite games lack other SPEs.

## Comparison with the broader finite-LP object

The read-added finite-LP object pays the same three exact primal/dual values and the retained-row relaxation. The assigned M object extracts the separate section-4 completion test and upgrades it to an exact all-best-reply route boundary. Therefore the useful relation is contextual: the finite-LP point with `D/P>1` is a relaxation candidate, while M certifies that its recorded `(A,B)` path cannot be completed. This does not form a logical implication from the LP object to a global half counterexample, and it does not enlarge the finite column domain or the response pattern.

## Comparison with the complete two-player search

The read-added complete-search object includes all `p^2-1` rows for each fixed response table, unlike M's retained subset. Its p=6 saved point has `P=1`, `D/P=14/13`, `u=6/13`, `v=7/13`, and all 35 nonself rows pass exactly, but the original six-label catalogue cannot generate its required positive background. Its p=4 and p=5 points have legal `AAA` backgrounds and ratio 1. M's d=1 point also has p=6, but it has only 17 retained rows, a different support, and `D/P=10/9`; matching p does not identify the objects. The comparison therefore only records a scope boundary: a complete-tail certificate is not repaired by, nor refuted by, the partial-chain obstruction, and the external-background caveat remains material.

## Open obligations and limits

* The dual and completion checks cover only `b=0,...,4`; no claim is made for `b>=5`.
* The d index is the length of a two-provider response pattern, not a game player count, and the d=1,2,3 domains are not asserted to be nested.
* Positive background masses in the d=1 and d=3 supports are external columns. They are not automatically a legal common-catalog prefix; a legalisation must add labels and rerun every newly available deviation.
* No six-provider/full-history IC, `OPT_6`, or global half implication is paid by these records.
* The complete-search comparison does not certify any finite-search global optimum; its historical floating enumeration was not rerun.

The exact next proof interface is to add the omitted first-action rows and a legal common-catalog background construction, then re-solve and re-audit the full ordered history. Until that is done, the route remains a finite relaxation boundary only.
