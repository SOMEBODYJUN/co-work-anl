# Independent review of aggregate-floor obstruction and hierarchical protection

This review uses the exact CAG model in `research/current/customer_attraction/model.md`:
one common finite catalog, individual unit customers, unit providers, sequential
actions, and pure SPE defined at every ordered history. It imports no repository
solver. No claim of external peer review or literature novelty is made.

## 1. Compact aggregate-floor obstruction: accepted

Partition six theme labels into X={0,1,2}, Y={3,4,5}. There is one distinct unit
customer for each of the nine cross pairs {x,y}, and three distinct unit customers
for each of the nine types consisting of two labels in X and two in Y. This gives
36 individual customers; each of the six themes contains exactly 21 customers.
Every provider has this same catalog.

The complete strategy is: player one chooses 0; player two chooses the smallest
label from the group opposite to the first choice; at every two-action history,
player three chooses the smallest unused label in the second action's group.
The last rule is defined after repeated histories as well. If the first two labels
are in the same group, it completes that group; otherwise it adds a second label
from the second player's group.

Directly expanding all 36 customers and evaluating their reciprocal congestion
shares verifies all 43 ordered decision histories and all 258 unilateral action
comparisons, including repeated and off-path histories. The minimum comparison
slack is zero. The root is (0,3,4), with payoffs (10,12,12) and coverage 34. All six
root deviations give the first player exactly 10. At every distinct two-action
prefix the best last response is 12, while at every repeated prefix it is 15.
Thus theta_3=12 and W=34<3 theta_3=36. OPT_3=36: choosing all three labels from
either group covers every customer. This refutes both a universal per-player
theta floor and the aggregate W>=n theta_n floor. It does not refute halfcoverage.

The direct arithmetic tables, ordered by label 0,...,5, include:

| History | Next player's deviation payoffs |
| --- | --- |
| (0) with the fixed subsequent rule | 9, 12, 12, 12, 12, 12 |
| (0,0) | 7, 15, 15, 37/3, 37/3, 37/3 |
| (0,1) | 9, 9, 12, 10, 10, 10 |
| (0,3) | 25/3, 12, 12, 25/3, 12, 12 |

The independent script is `review_compact_aggregate.py`; its frozen local output
is `compact_aggregate_review.json`. The earlier large positive Mobius witness
also passes independent exact replay, but is unnecessary for the compact result.

## 2. Hierarchical maximal incidence protection: accepted

Let B_1,...,B_s be the different maximal coverage sets of the catalog, with
duplicate coverage labels identified only for this structural definition. Set
I_x={j:x in B_j} for every coverable customer. Assume these nonempty incidence
sets are laminar. Assign each catalog action to some containing maximal B_j;
this assignment does not restrict or merge histories.

For each fixed j, the sets B_j intersect B_k are a chain under inclusion. To see
this from laminar incidence, all I_x containing j are mutually nested; the blocks
also containing any particular k form an upper part of that chain. Conversely,
two crossing incidence sets I_x,I_y would supply j in their intersection, k in
I_x minus I_y and l in I_y minus I_x, making B_j intersect B_k and B_j intersect
B_l incomparable. Thus the two structural descriptions are equivalent.

Fix any ordered history h with customer loads h_x, and choose a maximal B_j
maximizing f_h(B)=sum_{x in B}1/(h_x+1). It also maximizes over the entire catalog,
since every action is contained in a maximal set. Fix any nonempty arbitrary
ordered sequence A_1,...,A_r of subsequent actions, and route A_t into B_{k_t}.
Choose one t whose B_j intersect B_{k_t} is inclusion-largest, and write
I=B_j intersect B_{k_t}. By the chain property, every follower's overlap with
B_j lies in I. Consequently no follower covers B_j minus B_{k_t}; those leader
customers retain final shares exactly 1/(h_x+1).

Greedy optimality, with the common intersection canceled, gives

    sum_{x in B_j minus B_{k_t}}1/(h_x+1)
      >= sum_{x in B_{k_t} minus B_j}1/(h_x+1).

The selected follower's share on customers in I is no greater than the leader's
total share on I: both use the same final denominator on any commonly covered
customer, and the leader also covers every omitted customer of I. That follower's
remaining payoff is at most the right side above, because A_t is contained in
B_{k_t} and each covered customer's final congestion is at least h_x+1.
Adding proves that the leader's final payoff is at least this follower's final
payoff, hence at least the minimum final payoff among all followers.

This quantifies arbitrary follower actions, arbitrary legal or nonuniform
background loads, all greedy ties, empty subthemes, partial omissions of shared
blocks, and repeated labels. It proves domination of at least one follower; a
claim of domination of every follower would be false, even on disjoint maxima.

## 3. All-history induction and sharp welfare consequence: accepted

Fix total player count n, actual optimum O=OPT_n, and any history of length t.
Let M=max_T f_h(T), let d_x count an optimal n-action profile, and let h_x count
the t history actions. Every optimal-union customer satisfies
(d_x+h_x)/(h_x+1)>=1. Summing over all customers, including those outside that
union, gives

    O <= sum_{a=1}^n f_h(T_a) + sum_{a=1}^t f_h(H_a) <= (n+t)M.

At the last player's every history, M>=O/(2n-1), so SPE gives that player this
floor. Induct backwards over the number of remaining players, with the fixed
global threshold L=O/(2n-1). At an earlier history, deviation to a greedy maximal
B_j invokes the given complete strategy's actual continuation. Every later player
in that continuation is at least L by the induction hypothesis, since that
hypothesis quantifies every longer ordered history. Protection above gives the
deviator at least the minimum of these actual follower payoffs, hence at least L.
SPE optimality transfers the guarantee to the actual current action. Therefore
every root player has payoff at least L, and

    W=sum_i u_i >= n O/(2n-1),  i.e.  O <= (2-1/n)W.

No future responses are frozen across deviations, no restricted greedy equilibrium
is presumed, and no anonymous tie rule is imposed. O=0 follows from nonnegativity;
n=1 follows from ordinary maximal coverage best response. A unique maximal theme
is structurally included and gives full coverage, as already known. The usual
disjoint singleton example with one theme of size n and n-1 unit themes attains
the constant: a complete SPE can have all n players choose the size-n theme.
Thus the constant is sharp in this structural class.

## 4. Finite implementation checks remain separate

`review_hierarchical.py` independently checks the incidence/chain equivalence on
all 128 three-label incidence supports, protection on 46,710 configurations, and
the immediate bound on 1,515 histories. Its five catalogs contain the complete
family of subthemes of their maxima, with nested overlaps, unequal private loads,
duplicate incidence customers, omitted common roots, empty actions, and greedy
ties. The direct checks use individual customer formulas and no solver imports.
These finite checks are supporting implementation evidence. Sections 2-3 are the
universal proof and the basis for accepting the exact stated theorem.

Literature attribution must be settled separately before any novelty claim. The
protection pattern may already occur in Groenland-Schäfer Theorem 20; this review
does not certify a new theorem beyond any literature hypotheses.

## 5. Final draft strengthenings: accepted

The canonical `laminar_incidence_bound.md` strengthens the induction threshold
to the exact global theta_n. This is valid: the last-player base follows directly
from its definition, and the same protection and all-history backwards induction
transfer that fixed threshold to every earlier player.

Let C be the intersection of the distinct maxima and c its customer count. For
every last prefix, maximizing immediate payoff over the catalog equals maximizing
over full maxima; hence the common C contribution factors even when subthemes
omit C. Each core customer has load at most n-1, so that term is at least c/n.
The stripped residual catalog has OPT_n equal to the original optimum minus c:
both original and residual optima can be expanded to maxima, and all maxima
contain C. Apply the universal immediate counting inequality to the actual
stripped history and residual optimal portfolio. This gives

    theta_n >= c/n + (OPT_n-c)/(2n-1),
    OPT_n <= c + (2-1/n)(W-c).

Both strengthenings retain arbitrary ordered off-path histories and core-omitting
subthemes. They cause no quantifier problem.

## 6. Arbitrary-n aggregate obstruction: accepted

Sections 3-4 of `aggregate_theta_counterexample.md` give, for every n>=3, a
2n-label partition construction. Its auxiliary fresh game has all marginal
payoffs in {0,1}. The specified policy gives each nonroot player payoff one at
every distinct history; every root deviation makes the root player its group's
sole final member, giving zero. Therefore the policy is an auxiliary complete
fresh SPE. The root signed welfare is n-1.

The repeated-prefix bias step was checked independently. For fresh current label
a, split one old multiplicity v>=2 across two other labels as (v-1,1). On every
fixed membership of the remaining labels with total background s, the four terms
give the following bias decrease upon splitting:

    2/(1+s) + 2/(1+s+v)
      - 1/(1+s) - 1/(2+s) - 1/(v+s) - 1/(v+1+s)
    = 1/((s+1)(s+2)) - 1/((s+v)(s+v+1)).

It is nonnegative and at s=0 is at least 1/3. Enough unused labels exist to split
all repetitions while retaining the current fresh label. Thus every repeated
prefix has fresh unit bias at least b+1/3, whereas every distinct prefix has b.
The signed term has absolute value at most M; K=6M+4 makes
K(b+1/3)-M strictly greater than Kb+1. The previously proved full-history Mobius
compiler applies because K>=4M+1, and its repeated-history filling leaves all
prescribed distinct histories unchanged. Consequently theta_n=Kb+1 exactly and
the legal root welfare is n theta_n-1. No failure found in this arbitrary-n
proof. Its positive-bias welfare remains above halfcoverage, as stated.

## 7. Ordered-tax boundary appendix: accepted

The added section 7 of `two_remaining_tax.md` constructs n>=4 SPE-attainable
static PNE counts but shows that a reordered last action can violate the tax
inequality. Its arithmetic, static comparisons, and stated SPE construction were
reviewed independently. At every prefix containing H, all-B continuation gives
each new B player at least v=2n-3, and any leaf or H deviation gets at most v.
At a B-only prefix, choosing H gives h=2(n-1); every leaf deviation is bounded
by its naked size h, and a B deviation gets v if a later H remains or b/n at the
last slot. Leaf/no-H histories can be filled by backwards maximization respecting
the already prescribed valid H-containing descendants. The author clarified
this filling procedure after review; the audit already implemented it.

The reordered sequence with H last cannot be SPE: after n-2 B actions, a leaf
deviation forces every best last response to a different leaf, giving the
deviator h>v. Thus the appendix correctly refutes only an order-insensitive
terminal-count relaxation, with gap (n-1)(n-3)/n. The valid H-first SPE has tax
slack one and does not refute the correctly ordered root-tax conjecture.
