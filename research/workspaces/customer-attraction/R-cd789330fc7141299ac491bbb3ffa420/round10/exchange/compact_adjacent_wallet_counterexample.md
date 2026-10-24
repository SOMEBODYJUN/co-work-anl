# A ten-customer full SPE defeats unrestricted adjacent-wallet funding

2026-10-24, exchange10. This is an exact attack on two stronger auxiliary
payment assertions proposed for arbitrary m/catalog/full-history pure SPE.
**It is not a HALF counterexample. The existential optimal-assignment
adjacent-wallet candidate remains OPEN.** Root and tree10 independently
reconstructed the instance and complete strategy; the author's definition
level replay passes all 21 ordered histories and 84 action comparisons.
[Tree10's independent audit](../tree/compact_strongA_review.md) imports no
author code and separately passes all 21 histories and 63 nonself IC rows.
External review and novelty are not claimed.

## Exact candidate identities

At an actual leaf Z=(S_1,...,S_m), put

    f_i(T)=u_i(T,Z_-i),
    C_j=sum_(x in S_j minus S_(j+1))1/[c_x(Z)(c_x(Z)+1)],
    C_sum=sum_(j<m)C_j.

The following universal assertions are false:

    sum_i [max_T f_i(T)-u_i] <= C_sum;                 (ROWMAX)
    for every optimal assigned tuple T,
             sum_i f_i(T_i)-W <= C_sum.               (OPT-ALL)

The same witness also refutes the common-query strengthening
`sum_i f_i(T)<=W+C_sum` for every legal T. These are distinct from the
weaker candidate that **some** optimal tuple and **some common assignment**
have `sum_i f_i(T_i)-W<=C_sum`. That existential candidate is not refuted.

## Ten distinct unit customers, four distinct common themes

There are m=3 providers. The common catalog is C,A,B,D; each table row
denotes the stated number of different unit customers.

| Themes covering the customer | Multiplicity |
| --- | ---: |
| C,A,B | 6 |
| A | 1 |
| B,D | 1 |
| D | 2 |

Thus |C|=6, |A|=|B|=7 and |D|=3, and all four themes are distinct. A and B
differ on their seventh customer. Since A union D covers all ten customers,
OPT_3=10; no static optimizer or special-size welfare theorem is needed.

## One complete history-dependent pure SPE

The root chooses C. The second provider's rule is

| First action | C | A | B | D |
| --- | --- | --- | --- | --- |
| Second action | C | A | B | A |

The last provider's complete rule is this table. Rows are the first action,
columns are the second action; the chosen theme is the cell entry.

| First / second | C | A | B | D |
| --- | --- | --- | --- | --- |
| C | D | B | A | A |
| A | B | B | B | B |
| B | A | A | A | A |
| D | A | B | A | A |

Every terminal entry is a best reply. The direct maximum terminal payoffs
at those histories, in the same row/column order, are

| First / second | C | A | B | D |
| --- | ---: | ---: | ---: | ---: |
| C | 3 | 3 | 3 | 4 |
| A | 3 | 3 | 5/2 | 7/2 |
| B | 3 | 5/2 | 3 | 4 |
| D | 4 | 7/2 | 4 | 7 |

These values follow immediately from the four customer types. For example,
after A,B the last actions A,B,D all pay 5/2, so prescribed B is legal;
after A,D, A and B both pay 7/2, so prescribed B is legal. No tie rule
is assumed beyond this explicitly supplied strategy.

Following that table, the second provider's true deviation payoffs are

| First / second choice | C | A | B | D |
| --- | ---: | ---: | ---: | ---: |
| C | 3 | 3 | 3 | 3 |
| A | 2 | 5/2 | 5/2 | 5/2 |
| B | 2 | 5/2 | 5/2 | 5/2 |
| D | 3 | 4 | 7/2 | 3/2 |

The prescribed second action is a maximizer in every row. The root's true
payoffs from C,A,B,D are respectively 3,5/2,5/2,5/2, so its prescribed C
is strictly optimal. This exhausts all 1+4+16=21 decision histories and
proves full-history pure SPE, not merely on-path stability.

## Exact violation and the surviving assignment quantifier

The actual leaf is (C,C,D), with profits (3,3,3) and W=9. The entire
frozen payoff matrix is

| Actual role / queried theme | C | A | B | D |
| --- | ---: | ---: | ---: | ---: |
| First C | 3 | 4 | 7/2 | 3/2 |
| Second C | 3 | 4 | 7/2 | 3/2 |
| Last D | 2 | 3 | 5/2 | 3 |

Hence the row maxima are (4,4,3), and their total static regret is 2.
The first adjacent wallet is zero because C=C. At the second transition
C to D, only the six core customers contribute, each at load two:

    C_sum=6/[2(2+1)]=1 < 2.

This refutes ROWMAX. The fixed query A gives `sum_i f_i(A)=11>9+1`,
refuting the common-query version as well. Finally (A,A,D) is an optimal
tuple because A union D covers the entire universe. Its displayed
assignment has Q=4+4+3=11, refuting OPT-ALL.

Every optimal multiset and its exact best permutation cost is as follows.
Any optimum must contain A for its private customer and D for D's private
customers, so this list is exhaustive.

| Optimal multiset | Best assigned tuple | Minimum Q |
| --- | --- | ---: |
| C,A,D | C,D,A | 15/2 |
| A,A,D | A,D,A | 17/2 |
| A,B,D | B,D,A | 8 |
| A,D,D | D,D,A | 6 |

Thus the best existential cost is 6, well below W+C_sum=10. Repeating the
profitable frozen query A at both early roles uses the same terminal exit
wallet twice; assigning an optimal D slot to an early role removes that
overload in this witness. This identifies the exact extra quantifier
needed by the surviving proposal, not a general funding proof.

The instance satisfies 2W=18>10=OPT_3. It also leaves the base-price bank
`J_base=sum_(c_x>0)1/(c_x+1)=6/3+3/2=7/2` unviolated. C_sum and J_base
must not be denoted by the same letter when interpreting this result.

## Reproducibility and limits

[audit_compact_adjacent_counterexample.py](audit_compact_adjacent_counterexample.py)
is a self-contained standard-library replay. It expands the ten unit
customers, reconstructs the explicit full strategy, checks every action at
every ordered history, and recomputes the frozen matrix, adjacent wallets,
OPT and all optimal multisets/assignment costs. It imports no discovery
code, optimizer or canonical game solver. Its exact output is
[compact_adjacent_counterexample_exact.json](compact_adjacent_counterexample_exact.json).

This single finite construction attacks the stated general candidates.
It is not a fixed-three-player positive research project, a no-counterexample
scan, a counterexample to the existential assignment proposal, or a new
unconditional welfare bound. The required general early-debt funding remains
unproved.
