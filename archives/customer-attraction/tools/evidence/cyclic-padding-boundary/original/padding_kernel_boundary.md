# Exact HALF allowance for the on-path same-topic kernel interface

Status: analytic all-m construction and a sharp boundary for one explicitly
restricted payment interface. Finite complete-strategy members m=2,...,5 are
also independently replayed. This is not a HALF counterexample or a general
obstruction to weighted query transport. Independent review is pending.

## Family and intended scope

For every m>=2 start with the known 86-unit-client catalog (A,B,T,D,E) of the
two-player real-portfolio counterexample. Add m-2 topics Z_1,...,Z_(m-2), each
covering 22 new private unit clients and disjoint from every other topic. All
providers still share the whole catalog. There is a complete pure SPE with

    actual path (Z_1,...,Z_(m-2),E,A),
    every actual payoff 22, W=22m,
    unique optimal support {Z_1,...,Z_(m-2),B,D}, OPT=22m+1.

For this SPE, consider the restricted kernel interface in which each optimal
occurrence is matched to an actual topic a_j, and its real query must be taken
at an actual node choosing that same a_j. Every actual topic in this family
occurs only once, so this restriction fixes the query node once the matching
is selected. Among all such matchings, nonnegative contamination matrices and
weighted harmonic-kernel certificates, the least actual payoff budget is

    22(m+1) = (1+1/m)W.

Thus the entire allowance available for HALF can be necessary for this
interface, even in a high-welfare instance. The conclusion R<=W is not required
and is too strong for that restricted certificate family.

Crucially, the same instance **escapes the boundary** when query nodes may be
reused across different assigned actual topics. All actual payoffs equal 22,
so the last node can supply every query using total actual budget m*22=W.
A matching described below has zero contamination and proves strong R<=W.
The point of the construction is therefore to identify a restriction worth
removing, not to impose it on the main problem.

## Complete SPE construction

We first use a simple extension fact. Suppose an on-path continuation always
chooses an action attaining the largest immediate payoff at its prefix, and
later choices on that path do not decrease the selected player's payoff.
The path extends to a complete pure SPE: fill every off-path child with any
pure SPE by finite backward induction. At each path node the selected terminal
payoff equals the immediate maximum; every alternative terminal payoff is at
most its immediate payoff, so no chosen action can be improved. Induct from
the last node. This does not identify equal-count ordered histories.

At an actual prefix consisting only of distinct already used Z topics, let
L be the list of unused Z topics. If the current provider deviates to one old
topic S, prescribe the following continuation path:

| Old deviation S | Continuation path after S | Deviator's terminal payoff |
| --- | --- | ---: |
| A | B, followed by every topic in L once | 43/2 |
| B | every topic in L once, then T | 19 |
| T | every topic in L once, then B | 22 |
| D | T, followed by every topic in L once | 19 |
| E | every topic in L once, then A | 22 |

There are exactly |L|+1 remaining providers after the deviation. These paths
have the extension property above. The old-topic immediate maxima after lone
A,B,T,D,E are respectively 45/2,22,19,23,22. Unused Z topics pay 22, used Z
topics pay at most 11. After the first response B to A, every old-topic
immediate payoff is at most 22; after T to D, every old-topic immediate payoff
is at most 19. Thus B or T is a maximizing first response in the first/fourth
row, after which the unused Z choices are maximizing. In the other rows the
Z choices are maximizing until the final old response. All selected payoffs
are unchanged by later, disjoint Z choices.

Each old deviation therefore has a credible complete continuation giving its
deviator at most 22. A deviation to another unused Z topic has immediate
payoff 22, and a deviation to an already used Z topic has immediate payoff at
most 11, regardless of its continuation. Consequently every actual Z choice,
whose terminal payoff is 22, is optimal. After all Z topics have been used,
the same five responses give the original old two-player SPE (E,A), and every
used Z alternative pays at most 11. Glue these continuations at the distinct
actual-prefix query branches, and fill all unspecified subgames by backward
induction. This constructs a complete-history pure SPE for every m.

The specific query branches needed below are fixed by this construction:
deviating to B or D at any actual node before the last produces the old pair
(B,T) or (D,T), respectively, along with disjoint Z actions. At the last node
there is no follower. Thus the client type {B,T} has real query load 2 for an
early B query and load 1 for the last B query; type {D,T} does the same for D.
Both types are missed on the actual path.

## Optimality for every m

The old catalog's best union using at most k distinct old topics is

| k | 1 | 2 | 3 | 4 | 5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Old optimum | 26 | 45 | 66 | 86 | 86 |

The two-topic optimum is uniquely {B,D}. Each Z contributes 22 independently.
Replacing one Z in the proposed optimum by a third old topic gains at most
66-45=21<22; replacing two by a fourth gains at most 86-45=41<44; further old
topics do not help. Using only one old topic loses coverage as well. This
proves OPT=22(m-2)+45=22m+1, uniquely attained by all Z topics and {B,D}.
Every chosen topic has private comparison clients, and the comparison topics
are pairwise disjoint.

## Exact restricted-kernel lower and upper bounds

Use the customerwise contamination hypothesis and kernel normalization
K_lambda(J)>=1 from `cyclic_query_budget.md`. Since the optimal topics are
pairwise disjoint, every realized comparison-incidence set J is a singleton.
Hence every optimal occurrence j requires

    lambda_j >= 1+P_(j,j) >=1.

At most one of B,D can be matched to the last actual node. The other is queried
earlier, where its {B,T} or {D,T} client has actual load zero and real query
load two. The customerwise condition forces P_(j,j)>=1, so that occurrence
requires lambda_j>=2. All actual payoff budgets are 22. Therefore every
restricted routing costs at least 22(m+1). A general alpha normalization gives
the same conclusion after dividing all weights by alpha.

The bound is attained. Match each Z to its own actual node, B to the E node,
and D to the last A node. Take P diagonal, with P_(B,B)=1 and all other entries
zero. Take lambda_B=2 and every other lambda=1. The old B query is exactly the
two-player diagonal-contamination example; padding changes none of its old
client loads. All other queries satisfy zero contamination. Thus the kernel
condition holds and the budget is exactly 22(m+1).

## Explicit escape through cross-topic budget reuse

For m=2, match B to actual A and D to actual E. For m>=3, match B to A, D to
Z_1, Z_i to Z_(i+1) for i<m-2, and Z_(m-2) to E. No Z is assigned to its own
actual topic. Take every real query at the last actual A node. Each frozen
assigned query denominator then equals the corresponding last-node query
denominator on its comparison clients: B uses assigned A, D has no actual
cover, and every Z is assigned away from its unique actual cover.
Therefore P=0 and lambda=1 work. The query sum is

    22+22+11(m-2) <=22m=W,

and reusing the last SPE inequality m times spends exactly m*22=W. This query
node is not the actual topic assigned to most occurrences, so it lies outside
the lower-bound interface. It demonstrates why the main global search should
separate a query's frozen slot from the node supplying its budget.

## Reproduction and status

`padding_kernel_boundary.py` constructs complete policies for m=2,3,4,5,
using canonical BI only to fill unspecified subgames. Its separate direct
Fraction replay checks all ordered histories and all self/nonself comparisons:
6/30, 43/258, 400/2800 and 4681/37448, respectively. It checks optimality,
every relevant B/D query load, and the attaining kernel certificate. Complete
instances and policies are in `padding_kernel_boundary.json`.

The all-m conclusion rests on the extension and padding proof above, not on
those four finite computations. General existence of a cross-topic or
off-path routed budget <=(1+1/m)W remains unproved.
