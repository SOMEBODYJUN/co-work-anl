# Support — the exact point and its finite boundaries

## Core 58-customer construction

The core object fixes a labelled seven-topic catalogue with unit customer multiplicities

\[
x_{\{0\}}=9,\quad x_{\{1\}}=2,\quad x_{\{3\}}=2,\quad
x_{\{2,4\}}=34,\quad x_{\{5\}}=5,\quad x_{\{6\}}=6.
\]

Topics 2 and 4 cover the same 34-customer block; the other five blocks are pairwise disjoint with sizes 9, 2, 2, 5 and 6. The model keeps labels distinct even when their coverage is identical. Six providers act in order, all ordered histories are legal, and a forced action is followed by the same strategy on the changed history. The independent audit and the complete strategy file support the existence of a full-history pure SPE for this input. The exact static optimum is 58, while the complete SPE outcomes all have one provider on the 9-block and five providers on the 34-block, so `W=43`. Alias lifting keeps every root count vector

\[
(1,0,j,0,5-j,0,0),\quad j=0,\ldots,5,
\]

realizable without deleting the duplicate labels. This is an exact finite construction; it is not a general six-player half proof.

## Exact 11-unit equality point on the same σ

The same stored 19,608-node strategy is used with the distinct input

\[
x_{\{1\}}=1,\qquad x_{\{0,2\}}=6,qquad
x_{\{3\}}=x_{\{4\}}=x_{\{5\}}=x_{\{6\}}=1.
\]

The root and continuation path is `(0,2,2,2,2,2)`. The six customers of type `{0,2}` are covered once each, giving `W=6`; the five singleton customers are uncovered on this path. The six distinct labels `(0,1,3,4,5,6)` cover all 11 customers, so `OPT_6=11`. Thus the point has exact ratio `6/11` and gap `2W−OPT_6=1`.

The audit is dynamic: for each of the 19,608 ordered histories it compares the prescribed action with each of the seven forced actions and continues with the stored strategy after the forced history. There are 137,256 rows including self comparisons, all evaluated at payment scale 60, with minimum exact slack 0. The gzip evidence contains all 924 terminal count rows and all 19,608 ordered rows for this point and the separate 58-point input. Therefore the point is a feasible member of the same fixed-σ full SPE customer cone, and the 11-unit point independently supplies the attainment endpoint for the existing fixed-σ `min W/OPT_6=6/11` theorem.

## What the comparison does not pay

The point alone gives no lower bound for every nonnegative vector in the cone. The fixed-σ theorem's seven omitted-label normalizations and rational dual residuals supply that all-cone lower bound; this edge preserves that responsibility in the target and records only the independent attainable endpoint. The five branches whose certificates give `3/5` are lower bounds only, with no claim of separate attainment.

The 58-unit input and the 11-unit equality input are not scalar copies: they have different membership masks, different coverage quotient structure, and different welfare/optimum values. The 58-unit result quantifies all complete SPEs of one exact instance, while the 11-unit result concerns one fixed σ and a full cone of customer weights. Neither result quantifies over all six-player complete strategies or proves the universal `2W≥OPT_6` statement. Background remaining-profit quantities, static PNE, CCE and simultaneous facility models are outside the edge.
