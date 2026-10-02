# Computing the arbitrary-k factor-two witness: two separated obligations

Version 1, 2026-10-02. The target is the **same** common-catalog, labeled-facility,
positive atomic-weight model and complete exact customer-NE continuation in
[MF-MODEL](model.md). The input for complexity statements is explicit binary
rational data and explicitly listed k. These results neither give a polynomial
factor-two location algorithm nor assert hardness of finding such a witness.

## MF-PURE-CAP-POLY: polynomial completion from a capped pure assignment

**Statement.** Fix any labeled layout, an explicit rational threshold B>0, and a
feasible pure customer assignment. Suppose each facility of load >B contains
exactly one customer of weight >B, and every other facility has load at most B.
There is an algorithm polynomial in the bit length of this input that returns
an exact pure customer NE, leaving those isolated heavy customers in place and
keeping every other facility at load at most B. In particular, an initially
ordinary distinguished facility remains at load at most B.

**Proof and precise theorem import.** Remove the isolated heavy customers and
their facilities temporarily. Every remaining customer is initially assigned
to an available remaining facility; restrict its allowed set to the remaining
facilities covering it. This is the restricted identical-parallel-links game:
each customer's job size is its weight, each machine's latency is its total
assigned weight, and each customer can select only its covering machines.
Gairing--Lücking--Mavronicolas--Monien, *Computing Nash Equilibria for Scheduling
on Restricted Parallel Links* (STOC 2004, Section 4), give an algorithm that,
from **any** feasible assignment with positive integer job sizes, produces a
pure NE without increasing the makespan. In particular, their Theorem 4.7
gives a polynomial bound in the number of jobs, links, allowed edges and the
logarithm of total integer weight. Apply it here: the ordinary makespan was at
most B, so its output makespan remains at most B.

Reinsert the heavy customers on their original facilities. Each heavy customer
already pays exactly its own weight, the minimum possible actual load at any
facility it might choose. Each ordinary customer pays at most B; moving to an
isolated heavy facility would cost more than B, since that facility contains a
customer of weight >B. Therefore the result is a pure NE of the **full**
customer game, including all the temporarily omitted choices. Empty facilities
and customers becoming unserved at a different layout cause no issue: only
customers served at this fixed layout are jobs, and a customer with no allowed
ordinary machine could not have had the stipulated initial assignment.

For binary rational weights w_i=u_i/v_i, scale all weights by
D=product_i v_i (and compare against DB). D has bit length at most the sum
of the denominator bit lengths, so the integer algorithm's log(total weight)
and every arithmetic operand have polynomial bit length. Scaling preserves
all comparisons and NE conditions. There is no pseudopolynomial loop in the
*value* of D here. The threshold B is not an input to the imported algorithm.

**Application to SC-K-2-E.** Sections 4--5 of [uniform_two.md](uniform_two.md)
construct such an initial assignment with B=2a for every actual deviation from
their selected on-path profile; the deviator is ordinary. Once that profile is
given, all k(|S|-1) off-path equilibria and their load certificates can therefore
be computed in polynomial total time. An arbitrary remaining labeled layout
also has a polynomial-time default pure NE: start with any feasible pure
assignment, apply the same restricted-link algorithm to all served customers
and facilities, and retain each customer's actual set of covering facilities.
A complete continuation can thus be represented by a polynomial-size rule with
polynomial-time evaluation at any queried layout. This is a **conditional**
construction: the proof's global choice of the on-path profile is unresolved.

**Evidence distinction.** The published algorithm and its makespan theorem are
paper facts; deleting and reinserting isolated heavy customers is the present
model-specific deduction. The old strict-improvement proof still establishes
existence, but its number of improvement steps was never proved polynomial.
No implementation of the imported scheduling algorithm is presently in this
repository, and no claim of tested running time is made.

## SC-K-LEXMAX-STRONG-HARD: the existing global selection oracle

**Decision problem.** Given an explicit positive-integer MF-MODEL instance,
integer k, and threshold T, decide whether the **first** coordinate (minimum
load) of the lexicographically maximum increasingly sorted facility-load
vector among *all feasible site-uniform profiles* is at least T. The profile
family is exactly that of [uniform_two.md](uniform_two.md), Section 1; a client
chooses one covered occupied site and then independently uniformly among the
facilities at that site. On-path NE is *not* a condition on candidates in this
selection problem.

**Statement.** This problem is strongly NP-complete even when the number of
sites equals k, every site has the same reach, and every site covers all but
the other sites' private customers. Thus computing the precise global lexmax
profile used in the existing existence proof is strongly NP-hard. This is a
barrier for that oracle, not for finding some factor-two SPE witness.

**Reduction.** Start with the standard strongly NP-complete 3-PARTITION input
of 3m positive integers a_i, sum_i a_i=mB, with B/4<a_i<B/2. Create m sites
s_1,...,s_m and k=m labeled facilities. At every site s_j put one private
customer of weight P=mB+1 covered **only** there. For each i add one common
customer of weight a_i covered at **every** site. Every site therefore has
identical reach P+mB. Set T=P+B. This construction is polynomial even on the
strongly bounded 3-PARTITION subfamily; all weights are positive integers.

If any site is occupied by q_j>=2 facilities, that site's total assigned
weight W_j is at most P+mB, and each of its facilities receives
W_j/q_j <=(P+mB)/2<P. Hence a profile with minimum load at least T>P must
occupy all m sites. Because k=m, there is then exactly one facility per site.
Each private customer is forced to its own site; the common customers form a
partition of the a_i. The m loads sum to mP+mB, so they all exceed or equal
P+B exactly when **all** equal P+B. This is equivalent to partitioning the
numbers into m groups summing to B. The bounds B/4<a_i<B/2 force each group
to contain exactly three numbers. Conversely a 3-partition produces precisely
those loads. A layout and site assignment certify the threshold in polynomial
time; therefore the decision problem is strongly NP-complete. The existence
theorem subsequently makes a global lexmax into a customer NE, but this
reduction needs no equilibrium computation.

**A stronger warning against misinterpretation.** Every instance in this
particular reduction family has an exact facility SPE that can be obtained in
polynomial time, even when the 3-PARTITION answer is NO. Occupy all m sites,
one facility at each, and use any pure customer NE on path (the published
restricted-link algorithm computes one); every facility then has load at least
P. If facility f leaves its site for another occupied site, the source-private
customer becomes unserved. Put all common customers (total weight mB=P-1) on
f, and leave each remaining private customer on its stationary facility. This
is a pure NE: each common customer's current cost is mB<P and any stationary
option costs at least P+w_i; a private customer at the target site pays P and
would pay P+mB upon joining f. All other private customers have no alternative.
The deviator earns mB<P, so its deviation does not improve. Every possible
deviation has this form, and the other layouts have polynomially computable
default pure NE. Thus hard exact lexmax selection is compatible with an easy
exact equilibrium on the very same inputs.

**Scope of the remaining frontier.** Find in bit-polynomial time an on-path
layout and exact client NE together with a suitable off-path packing or other
stability certificate. The four lexmax transfer inequalities in Sections
3.1--3.2 are sufficient, but need not be necessary. Optimizing their original
global lexmax potential exactly cannot serve as a polynomial algorithm unless
P=NP; the off-path Nashification step no longer accounts for that obstacle.

## SC-K-LOCAL-PLS: the four budgets need only local optimality

**Statement.** For explicit rational input, there is a polynomial-size state
space description, polynomially many polynomial-time neighbors per state,
a polynomial-bit integer objective and a polynomial-time initial state such
that **every locally maximal state** yields an exact on-path site-uniform
customer NE and all four transfer budgets of Section 3 in uniform_two.md.
Consequently the factor-two certificate search reduces to this explicit
polynomial local-search (PLS) problem, followed by MF-PURE-CAP-POLY.
Membership in PLS is an upper bound on *search complexity*, not a polynomial
time algorithm or a PLS-hardness result.

**States and neighbors.** A state consists of a labeled layout and, for each
served customer, a legal assigned occupied site. Unserved customers have the
forced marker bottom. The neighbors are (i) moving one customer to another
covered occupied site and (ii) moving one labeled facility to a different
catalog site. For a facility move, construct one canonical new assignment:

- If its old site still has a facility, keep all old site assignments; assign
  newly covered customers to the target site.
- If its old site disappears, assign its old customers covered at the target
  to that site, and the genuinely newly covered customers there too. For each
  remaining old-site customer that remains covered, choose the least indexed
  surviving site covering it; mark the others unserved. Keep assignments of
  customers outside the old site.

These rules make each neighbor legal in O(nm) elementary incidence checks.
There are at most n(m-1)+k(m-1) neighbors. If a customer violates the exact
conditional NE inequality, (W_t-w_i)/q_t>W_u/q_u, its transfer neighbor
strictly improves the sorted vector by uniform_two.md (3). The converse is
unneeded and can fail at a customer cost tie. Each violated facility budget (5)--(8) likewise makes
its corresponding canonical facility-move neighbor **strictly** improve the
sorted load vector, by the same coordinate argument as Sections 3.1--3.2;
the least-index redistribution only increases surviving loads. For (7), the
necessary check that the old target load was already above a follows from
w(J cap C_t)<=a. Hence a local maximum has both NE and every budget.

Start with all k facilities at a maximum-reach site and all its customers
assigned there. If maximum reach R>0, every load starts at R/k, and no
improving neighbor can reduce the lexicographically first load, so a reached
local maximum has all loads positive. R=0 has an immediate exact certificate.

**Bit complexity of the objective.** Let D be the product of all input
weight denominators, z_i=D w_i be integers, Q=sum_i z_i, H=k!, and M=HQ.
For a state, each facility at t has integer scaled load
X_t=H(sum_{i in J_t}z_i)/q_t. Sort all k coordinates as
X_(1)<=...<=X_(k), put b=M+1, and evaluate

    V = sum_{j=1}^k X_(j) b^(k-j).

Every digit is between 0 and M, so comparing V is exactly comparing sorted
load vectors lexicographically. All numbers, including V, have polynomial
bit length because log D is bounded by the input denominator bits,
log H=O(k log k), and log V=O(k log(M+1)). The initial state, neighborhood
scan and objective comparison meet the usual PLS conditions. They do not
bound the number of improving transitions; using this search naively might
take exponentially many iterations.

## SC-K-GREEDY-BUDGET: polynomial transfer budgets alone

**Statement.** A deterministic polynomial-time greedy procedure constructs a
site-uniform *feasible* profile with positive loads and all four transfer
inequalities (5)--(8) of uniform_two.md, for every positive-reach instance.
It does **not** generally produce an exact on-path customer NE. Neither this
claim nor the counterexample below is a factor-two algorithm.

**Procedure.** Initially there are no facilities and no assigned customers.
At each of k iterations give an already occupied site t the score
W_t/(q_t+1); give an unoccupied site r the score equal to the weight of its
currently uncovered customers. Choose a site with greatest score, breaking
ties by site index. If it was unoccupied, assign to it every previously
uncovered customer it covers. If it was occupied, keep all assignments.
Insert one labeled facility there. All comparisons are rational sums and
quotients with polynomial bit length; a direct implementation takes
O(kmn) elementary incidence/arithmetic operations. With positive maximum
reach, every selected score is positive (after the first insertion, its
occupied site itself always has a positive score), hence every final
facility load is positive.

**Proof of every budget.** Fix a final source facility f at site u, and
look at the instant just *before the last facility was inserted at u*.
The score chosen at that instant was exactly its final load a=W_u/q_u:
the site's assigned customer set never changes after it first opens.

For a different final occupied site t already occupied at that instant,
its assigned weight was its final W_t and its score was
W_t/(q_t^{old}+1)<=a. Since its multiplicity can only grow,
W_t<=(q_t+1)a. If q_u=1, the customers J_u were all uncovered just before
u first opened, whereas every customer covered by t was then already
covered, so J_u cap C_t is empty. This also proves the stronger (7).

For a final occupied t that was unoccupied at that instant, its earlier
new-coverage score R_t^{old} was at most a. Its final assigned customers J_t
were then all uncovered, so W_t<=R_t^{old}<=a. When q_u=1, the additionally
relevant J_u cap C_t were also then uncovered and are disjoint from J_t;
therefore W_t+w(J_u cap C_t)<=R_t^{old}<=a<=(q_t+1)a.

Finally, any site r unoccupied at the end was unoccupied at that instant.
Its then-uncovered customers contain the final genuinely newly coverable
customers counted by N_r; if q_u=1, they also contain the disjoint set
J_u cap C_r. Thus its score at that instant gives respectively
N_r<=a or N_r+w(J_u cap C_r)<=a. These are (6) and (8).

**Fixed-layout interface counterexample.** Take k=2, sites A,B,C and four
customers of weights (6,3,5,2) with respective covered site sets
({A,C},{A,B},{B},{C}). The site reaches are (9,8,8). Greedy first opens A;
the next scores are 9/2 for A, 5 for B, and 2 for C, so it opens B and
assigns customers (6,3) to A and 5 to B. Loads are (9,5) and every budget
above holds. The customer of weight 3 has conditional cost 9 at A but 8 at B;
it strictly moves to B. The fixed-layout customer NE is unique, with loads
(6,8). For the facility at A, the now-required empty-target C budget is
N_C+w(J_A cap C_C)=2+6=8>6=a. The actual deviation earns 8<=2a,
so this only refutes preservation of the *sufficient budget* at that layout.
It does not refute factor two for the instance.

## Sources and review status

- Gairing, Lücking, Mavronicolas, Monien, STOC 2004, Section 4, especially
  Theorem 4.7 and the makespan preservation stated in the abstract/introduction:
  https://cgi.csc.liv.ac.uk/~gairing/publications/2004-stoc.pdf .
- 3-PARTITION is used only as a standard strongly NP-complete source problem.
  The reduction above is self-contained after that source fact.
- The heavy-client interface and lexmax profile family are the existing
  [uniform-two proof](uniform_two.md). The new deduction and reduction have
  been independently rechecked internally; external review and literature
  priority for this particular reduction are unrecorded.
