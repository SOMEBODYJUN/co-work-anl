# Depth-three greedy trees defeat the full-box potential selector

Current counterexample, 2026-10-04. Independently derived from a recursive-pool exchange attempt. Exact arithmetic independently reviewed by Sol Attack for the symmetric precursor; the strict version below removes all greedy ties. No external review or priority claim.

## `SC-K-DEPTH-THREE-BOX-POTENTIAL-NO`: exact scope and negative statement

Use the repository's MF-MODEL and canonical SC-K-GREEDY-BUDGET procedure. Freeze the clients with one occupied option and those of weight at least the last insertion score gamma. Among assignments of the remaining light clients, require every full greedy box

`q_s gamma <= W_s <= (q_s+1) gamma`.

The exact site-uniform customer potential is

`P = sum_s (W_s^2 - sum_{i assigned s} w_i^2)/(2q_s)`.

The following genuine positive-integer greedy input has a light-client graph that is a tree of opening-directed depth three, with exactly one light client per edge. Its unique global minimum of P over all full-box assignments is not a customer NE. The same greedy layout has a unique full-box NE, with strictly larger P.

This is a correctness obstruction to extending the height-two **full-box potential-minimum selector** beyond its stated domain. It is not an obstruction to boxed-NE existence, a hardness result for finding a boxed NE, a lower bound above factor two, or a proof that this greedy layout cannot support a factor-two continuation.

## Input

Sites, in deterministic tie-breaking order, are `A1,A2,B,C,D,R`; there are `k=15` facilities. Each row below is one atomic client.

| Client | Weight | Site options |
|---|---:|---|
| Private A1 | 4599 | A1 |
| Private A2 | 4598 | A2 |
| Private B | 3045 | B |
| Private C | 2000 | C |
| Private D | 1451 | D |
| Private R | 1000 | R |
| X1 | 400 | A1, B |
| X2 | 400 | A2, B |
| Y | 900 | B, C |
| Z | 150 | C, D |

The light graph is `A1 -> B <- A2`, followed by `B -> C -> D`. It has four edges, maximum undirected degree three, and longest directed path three. R is isolated. Its underlying graph is a tree; each light client has precisely two options.

## Strict greedy execution

For an occupied site, the next score is its original assigned pool divided by its current multiplicity plus one. For an unopened site, the score is the currently uncovered customer weight it can cover. The exact unique maximizing site and score at every insertion are:

| Step | Site | Score |
|---:|---|---:|
| 1 | A1 | 4999 |
| 2 | A2 | 4998 |
| 3 | B | 3945 |
| 4 | A1 | 4999/2 |
| 5 | A2 | 2499 |
| 6 | C | 2150 |
| 7 | B | 3945/2 |
| 8 | A1 | 4999/3 |
| 9 | A2 | 1666 |
| 10 | D | 1451 |
| 11 | B | 1315 |
| 12 | A1 | 4999/4 |
| 13 | A2 | 2499/2 |
| 14 | C | 1075 |
| 15 | R | 1000 |

Consequently

`q = (4,4,3,2,1,1)`, `gamma=1000`,

`W^0 = (4999,4998,3945,2150,1451,1000)`.

The four variable clients start at `(X1,X2,Y,Z)=(A1,A2,B,C)`. All have weights below gamma. Every private client has a single option and weight at least gamma, so no frozen client's possible deviation has been omitted. The exact audit checks uniqueness against **every** competing site at every step, not just descending scores in the displayed execution.

## All full-box assignments

There are 16 assignments of the four light clients. Exactly six satisfy all boxes. Write a state as the sites assigned to `(X1,X2,Y,Z)`.

If Y stays B, then B's load is `3945+400 h`, where h counts X clients sent to B. Its upper box is 4000, so h must be zero. Both choices of Z are boxed.

If Y moves to C, then Z cannot stay C: their joint load there would be `2000+900+150=3050>3000`. With Z at D, every one of the four X choices is boxed: B has load 3045, 3445 or 3845, and every source A_j retains at least 4598>4000. This proves that the following table is exhaustive.

| State | Totals `(A1,A2,B,C,D,R)` | Exact P | NE? |
|---|---|---:|---|
| `(B,B,C,D)` | `(4599,4598,3845,2900,1601,1000)` | `5948950/3` | No |
| `(A1,A2,B,C)` | `(4999,4998,3945,2150,1451,1000)` | `1983200` | Yes |
| `(B,A2,C,D)` | `(4599,4998,3445,2900,1601,1000)` | `1983450` | No |
| `(A1,B,C,D)` | `(4999,4598,3445,2900,1601,1000)` | `1983550` | No |
| `(A1,A2,C,D)` | `(4999,4998,3045,2900,1601,1000)` | `2037350` | No |
| `(A1,A2,B,D)` | `(4999,4998,3945,2000,1601,1000)` | `2050850` | No |

For a light client of weight w at s, NE means `(W_s-w)/q_s <= W_t/q_t` at its alternative t. The omitted own weight is the same additive w in the original conditional costs, so these inequalities are exactly equivalent to MF-MODEL best responses.

At the initial state, the four external-cost comparisons are

- X1: `4599/4 <= 3945/3 = 1315`;
- X2: `4598/4 = 2299/2 <= 1315`;
- Y: `3045/3 = 1015 <= 2150/2 = 1075`;
- Z: `2000/2 = 1000 <= 1451`.

Thus the initial state is an exact client NE. Every other boxed state has Z at D. When Y is at C, Z's external cost at D is 1451 while C's normalized load is 1450, so it strictly wants C. In the remaining state `(A1,A2,B,D)`, C's normalized load is 1000, so the same move is again strictly profitable. Therefore the initial state is the **unique** full-box NE.

## The unique minimizer is not NE

The displayed first potential is strictly below each of the other five. In particular,

`1983200 - 5948950/3 = 650/3 > 0`.

At its unique minimizing state, client Z would strictly improve by returning from D to C because

`(1601-150)/1 = 1451 > 2900/2 = 1450`.

The move is forbidden only by C's artificial upper box: its new total would be 3050, above 3000. The actual game has no such capacity restriction. Consequently, global optimality within the full boxes does not certify exact customer NE.

The feasible recursive whole-pool reversal sends Y from C back to B and both X clients from B back to their A sites, while returning Z to C. This restores the initial state and increases P by 650/3. Thus the recursive exchange's **feasibility** can be valid while its required potential-decrease assertion is false. Since the bad state is globally P-minimal among boxed assignments, no alternative simultaneous boxed exchange can strictly decrease P from it.

## Precise boundary established

The existing height-two theorem proves all boxed P-minimizers are NE when all light customers have two options and every opening-directed path has at most two edges. This counterexample shows that the directed-depth bound cannot simply be replaced by three, even on a tree with one light customer per edge. Branching matters here: the graph is not a consistently directed path, and the established path algorithm is unaffected. The input also lies within the bounded-treewidth/local-weight-diversity DP domain, which can select its actual boxed NE; that theorem is unaffected.

No universal existence question is closed negatively: this same input has a boxed NE, and BOX-TO-2 supplies its complete factor-two continuation. The construction's mathematical content is the failure of this particular optimization selector, separate from the already established computational hardness of optimizing it.

## Reproduction

`python3 tests/audits/kfac_depth_three_box.py`

The audit uses only exact Fraction arithmetic, exhaustively checks the 16 light assignments, verifies all greedy score comparisons, recomputes P from individual atomic clients, checks every customer's exact NE inequalities, and asserts all table entries and the gap 650/3. It is finite certification of this counterexample; it does not prove a universal boxed-existence theorem or any complexity lower bound.
