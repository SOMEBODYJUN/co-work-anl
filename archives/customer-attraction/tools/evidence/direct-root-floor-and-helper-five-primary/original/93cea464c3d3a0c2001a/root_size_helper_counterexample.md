# The root row cannot replace actual coverage by the largest theme

2026-10-24. Root supplied this named counterexample to one proposed
all-input helper. Direct10 independently reconstructed it without importing
root's implementation. **Actual net ROW and Q-CAG-HALF remain OPEN in
general and both hold on this instance.** This is no new fixed-population
positive result and no instance scan.

## Exact rejected statement

For a complete SPE's root and an m-slot comparison tuple T, let d_1(T_j) be
the true root payoff after forcing T_j and following the same original
strategy. The proposed stronger helper was

\[
\sum_{j=1}^m d_1(T_j)\ge
\left|\bigcup_{j=1}^m T_j\right|-K,
\qquad K=\max_{T\in\mathcal S}|T|.\tag{ROOT-K}
\]

This statement is **false**, including when T is an optimal tuple with all
m slots present. It must not be confused with the actual net ROW, which
has W in place of K.

## Unit instance and complete strategy definition

There are six providers, ten unit customers, and six pairwise disjoint
themes with sizes (3,3,1,1,1,1), labeled 0,...,5. This is a finite common
catalog and contains no provider or customer weights. Every unit customer
likes exactly one theme.

The following recursion defines the strategy at every ordered history. For
a count vector q of total at most six, let F(q) be the completed terminal
counts. At total six put F(q)=q. At smaller totals, calculate every completed
child F(q+e_a), then choose

\[
a(q)=\min\operatorname*{arg\,max}_{a\in\{0,\ldots,5\}}
\frac{w_a}{F(q+e_a)_a},
\qquad F(q)=F(q+e_{a(q)}),
\]

where w=(3,3,1,1,1,1). At an ordered history h use a(q(h)).

The recursion compares the current provider's final payoff under complete
continuations. It is **not** a myopic greedy rule. In particular replacing
this recursion by maximizing w_a/(q_a+1) would not justify all off-history
IC comparisons. The count-based strategy is one constructed legal strategy;
there is no restriction of the target's arbitrary-history quantifier.

Finite backward induction proves its complete SPE property. The independent
audit additionally expands every ordered decision history and checks every
alternative action exactly.

## Exact results and scope

The actual sequence is (0,0,0,1,1,1). Thus actual counts are (3,3,0,0,0,0),
W=6, OPT_6=10, and K=3. For each forced root action:

| Root action | Completed counts | Root payoff |
|---|---|---:|
| 0 | (3,3,0,0,0,0) | 1 |
| 1 | (3,3,0,0,0,0) | 1 |
| 2 | (3,2,1,0,0,0) | 1 |
| 3 | (3,2,0,1,0,0) | 1 |
| 4 | (3,2,0,0,1,0) | 1 |
| 5 | (3,2,0,0,0,1) | 1 |

Take T=(0,1,2,3,4,5), which covers all ten customers and is therefore
optimal. Its true root row sums to six. Consequently

\[
6<10-3=7\qquad\text{but}\qquad
6\ge10-6=4,\quad 10\le2\cdot6.
\]

The first comparison disproves ROOT-K. The latter two explicitly preserve
the original actual net ROW and HALF. In fact every actual provider has
payoff one, so the root is an actual minimum-profit position as well.

The independent checker
[audit_root_size_helper_counterexample.py](audit_root_size_helper_counterexample.py)
uses exact fractions and checks 462 count decision states / 2,772 count IC
comparisons, then all 9,331 ordered decision histories / 55,986 ordered IC
comparisons. Counts include the prescribed action. Its complete output is
[root_size_helper_independent_audit.json](root_size_helper_independent_audit.json).

Source attribution: the instance and intended full-BI completion are in
[root's primary note](../parent/root_standalone_row_helper_counterexample.md).
Root's [full-history audit implementation](../parent/audit_root_standalone_helper.py)
and [exact counterexample artifact](../parent/root_standalone_helper_exact_counterexample.json)
store the 9,331 ordered-history actions and 55,986 IC comparisons. This
directory supplies an independent implementation and exact scope check.
No external review or novelty is claimed.

The same instance also has W=6<OPT-K=7, so the proposed additive welfare
strengthening W>=OPT-K is false as well. This is another auxiliary
strengthening only; it does not change the original HALF or net ROW status.
