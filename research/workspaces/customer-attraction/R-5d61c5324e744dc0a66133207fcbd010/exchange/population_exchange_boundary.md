# Population deletion and replacement-chain boundary

Research backup, 2026-10-23. This disproves two possible exchange invariants,
not Q-CAG-HALF. The model is the common finite topic menu, unit customers, unit
players, all ordered histories, pure SPE with arbitrary history-dependent ties.

## 1. A 13-customer population decrease

The four topics are A,B,C,D. A customer row is its exact set of acceptable topic
labels; multiplicity means that many distinct unit customers.

| Customer type | AB | C | BC | AD | ABD | CD |
|---|---:|---:|---:|---:|---:|---:|
| Multiplicity | 3 | 1 | 2 | 1 | 3 | 3 |

For two players, the **only SPE terminal ordered path is AC**, covering all 13
customers. For three players there is a complete SPE with actual ordered path
DBB, covering 12. All three-player SPE terminal count vectors are ABC, BCD and
BBD, so the minimum SPE welfare is exactly 12. Both OPT_2 and OPT_3 are 13.

Consequently, minimum SPE welfare need not be nondecreasing with the number of
players, even on a fixed common menu and when the optimum stays constant.
Multiplying every multiplicity by any positive integer preserves all comparisons
and makes the absolute decrease arbitrarily large.

The full ordered certificates are `thirteen_m2_certificate.json` and
`thirteen_m3_certificate.json`. The complete comparison tables, all achievable
ordered paths and all terminal counts are in `population_exchange_audit.json`.

## 2. The failure persists with unique strict strategies

| Customer type | AB | C | BC | AD | ABD | CD |
|---|---:|---:|---:|---:|---:|---:|
| Multiplicity | 9 | 1 | 7 | 2 | 11 | 10 |

All two-player ordered nodes have unique maximizing actions; the unique complete
SPE has path AC, payoffs (22,18), welfare 40. The least strict comparison gap over
all nodes and nonself deviations is 1/2.

All three-player ordered nodes likewise have unique maximizing actions. The
unique complete SPE has path DBB, payoffs (47/3,35/3,35/3), welfare 39. The least
strict comparison gap is 1/6. Thus the population boundary does not rely on ties,
anonymous selectors or the ability to choose different continuations at equal
load histories. The optimum is 40 at both populations.

The two-player policy is root A and replies C,D,B,B after A,B,C,D. The
three-player policy is root D; second-player actions after A,B,C,D are B,D,B,B.
Its final reply table is:

| First/second | A | B | C | D |
|---|---|---|---|---|
| A | C | D | B | B |
| B | D | D | D | B |
| C | B | D | B | B |
| D | B | B | B | B |

Every entry is strict. Backward induction from this table gives uniqueness of
the full strategies, not just of the on-path welfare. The frozen certificates
and audit record all 5+21 ordered nodes and all 20+84 action comparisons.

## 3. A tiny support-preserving deletion failure

With types A=1, AC=2, BC=2, the two-player path BA is SPE. The unique one-player
SPE action is C. Deleting either actual BA player therefore cannot yield a
one-player SPE on the same menu. This refutes the stronger premise that every
SPE terminal profile has a deletion which is itself an equilibrium of the
smaller-population game. Allowing replacement is indispensable, but Section 1
shows that replacement cannot be assumed to preserve a welfare lower bound.

## 4. What remains

A useful deletion/insertion induction must retain an explicit continuation
state or an error budget; it cannot appeal to either raw population monotonicity
or support-preserving deletion. These examples do not exclude an induction
which changes actions and charges the resulting welfare drift jointly with
other true-branch inequalities. No such aggregate bridge is proved here.

`population_exchange_audit.py` expands the unit customers, replays the complete
certificates directly, and independently computes all ordered SPE terminal
histories by set-valued backward induction. It imports no project solver. Run:

```sh
python3 research/workspaces/customer-attraction/R-5d61c5324e744dc0a66133207fcbd010/exchange/population_exchange_audit.py
```

The parent independently reconstructed both examples from only the incidence
tables using a separate Fraction oracle and confirmed the claims. This is an
internal mathematical check, with no external review or novelty certification.
