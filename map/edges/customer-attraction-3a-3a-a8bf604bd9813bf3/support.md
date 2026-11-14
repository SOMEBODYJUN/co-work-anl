# Support — two exact inputs for the same strategy

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

The audit is dynamic: for each of the 19,608 ordered histories it compares the prescribed action with each of the seven forced actions and continues with the stored strategy after the forced history. Each input has 137,256 comparisons including self comparisons, all evaluated at payment scale 60, with minimum exact slack 0. The gzip evidence contains 924 terminal count rows and 19,608 ordered rows per input. The point named `lp_integer` independently supplies the attainment witness for the existing fixed-σ theorem. The point named `random` independently places the 58-customer vector in the same cone at `43/58>6/11`.

## Registered statements and proof scope

The 58-customer construction is the full scope of `M-c5e460641b3e47729159aa9e7cb6a175`. The 11-customer witness belongs to the scope of `cag-r70-six-player-seven-topic-fixed-complete-strategy-lp`, whose evidence references the “LP十一点：大块锐例与相同固定策略” section and the fixed-cone certificate. The new contextual check compares these two registered statements against the shared frozen evidence. The all-cone lower bound follows from the fixed-σ theorem's seven rational dual certificates and its six-slot optimum identity. The five certificates with value `3/5` are branch lower bounds.

The two inputs have different positive membership masks, with duplicate labels 2 and 4 for 58 customers and 0 and 2 for 11 customers. Thus even a common scalar rescaling cannot identify these vectors. The 58-customer result quantifies all complete SPEs of a single instance. The fixed-cone theorem quantifies over all admissible nonzero customer-type vectors for the specified σ. The universal six-player `2W≥OPT_6` question is outside both results.
