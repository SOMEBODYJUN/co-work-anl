# Residual optimal-portfolio budget fails with two providers

Status: explicit exact counterexample to a **stronger auxiliary conjecture**,
not to Q-CAG-HALF. This note is self-contained; no claim of minimality or novelty.

The attempted direct strengthening was: if a pure SPE covers union C, then the
maximum number of customers outside C that m themes can cover is at most |C|.
Unlike the previously refuted m times maximum residual-theme inequality, this
uses a non-double-counted residual portfolio. It is still false.

There are two providers and six common themes A,B,T,S,Q,R. The following ten
blocks are distinct unit customers, with each row's multiplicity as shown.

| Themes containing the customer | Multiplicity |
|---|---:|
| A | 4 |
| A,Q,R | 2 |
| B | 5 |
| B,Q,R | 2 |
| T | 3 |
| T,Q | 2 |
| T,R | 2 |
| S | 3 |
| S,Q | 2 |
| S,R | 2 |

The first provider selects A. The complete second-provider strategy is
A→B, B→Q, T→Q, S→R, Q→R, R→Q.

The full matrix below gives the second provider's payoff. Rows specify the
first action and columns the possible second action.

| First action | A | B | T | S | Q | R | Chosen reply | First payoff |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| A | 3 | 7 | 7 | 7 | 7 | 7 | B | 6 |
| B | 6 | 7/2 | 7 | 7 | 7 | 7 | Q | 6 |
| T | 6 | 7 | 7/2 | 7 | 7 | 7 | Q | 6 |
| S | 6 | 7 | 7 | 7/2 | 7 | 7 | R | 6 |
| Q | 5 | 6 | 6 | 6 | 4 | 6 | R | 6 |
| R | 5 | 6 | 6 | 6 | 6 | 4 | Q | 6 |

Every specified reply maximizes its row, and every root action gives the first
provider exactly 6. Thus this is a full ordered-history pure SPE, including all
off-path nodes. The actual outcome (A,B) has disjoint themes of sizes 6 and 7,
so payoffs are (6,7), C=A∪B, and W=13.

Themes T and S are disjoint from C and from each other, each with size 7.
Therefore the residual two-theme optimum is 14>13. Enumerating all theme pairs
also gives original OPT_2=14, so the actual coverage ratio is 14/13 and the main
half-coverage conjecture is satisfied with substantial slack.

The mechanism is a mutually credible Q↔R reply cycle. Each of Q,R contains two
customers from A and two from B plus two customers of each residual theme.
The internal overlap simultaneously keeps these replies competitive at the
actual last node and limits their first-player payoffs after deviation. Purely
disjoint residual benchmarks do not remove the cross-branch obstacle.

`audit_residual_obstruction.py` reconstructs every one of the 7 decision nodes
and 42 action comparisons in Fraction arithmetic, and enumerates all theme
pairs for both optima. Its finite audit checks this explicit counterexample;
the table above is the proof.

Discovery scripts: `residual_two_lp.py` exposes the insufficient two-branch
relaxation; `residual_two_full.py` adds all last-node and all true root
comparisons for each candidate complete response map. Their LP outputs are
exploratory and are not used as proof premises.
