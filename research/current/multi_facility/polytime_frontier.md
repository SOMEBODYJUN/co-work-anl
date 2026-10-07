# Computing the arbitrary-k factor-two witness: two separated obligations

Version 1, 2026-10-02, with conditional construction and selection-rule
obstructions added 2026-10-03. The target is the **same** common-catalog, labeled-facility,
positive atomic-weight model and complete exact customer-NE continuation in
[MF-MODEL](model.md). The input for complexity statements is explicit binary
rational data and explicitly listed k. These results neither give a polynomial
factor-two location algorithm nor assert hardness of finding such a witness.

## 2026-10-07 update: greedy feasibility is closed, general bit-polynomial time is open

[SC-K-GREEDY-BOX-EXISTS](greedy_box_global_progress.md) proves that every canonical
greedy occupancy admits a full-box exact site-pure/within-site-uniform client NE,
with heavy and singleton-option customers frozen. Arbitrary strict improvements
from repaired box-and-`(H)` states, followed by the specified home-return repair,
strictly increase the interleaved threshold-clipped-load/count potential at every
microstep. There are at most `prod_i |A_i|-1` moves, and trace-free execution uses
polynomial space. This closes universal box feasibility and finite construction;
it does not bound the general running time by a polynomial in input bit length.

`SC-K-GREEDY-BOX-FINITE-2` combines that constructor with the existing
SC-K-GREEDY-BOX-TO-2 theorem. The latter's mathematical bit-polynomial off-path
proof remains unchanged. The connected executable instead uses the legacy finite
cap-preserving pure best responses for actual deviations and finite pure best responses for defaults, so its off-path software
is not the published polynomial scheduling algorithm.

`SC-K-BOX-STRUCTURED-POLY-2` is a new corollary, not a change to earlier IDs:
universal box feasibility plus either SC-K-INCIDENCE-BOX-DP or
SC-K-LOCAL-WEIGHT-BOX-DP, followed by BOX-TO-2, gives a full bit-polynomial
factor-two construction on the respective fixed-parameter class. The old
two-option/depth-two existence restrictions are unnecessary in this new version.
General bit-polynomial selection, not existence, is the remaining box obligation.
The old potential and untruncated lexmax counterexamples below are unchanged.

## MF-PURE-CAP-POLY: polynomial completion from a capped pure assignment

**Statement.** Fix any labeled layout, an explicit rational threshold B>0, and a
feasible pure customer assignment. Suppose each facility of load >B consists
of a single customer whose weight is >B (and contains no other customer), and
every other facility has load at most B.
There is an algorithm polynomial in the bit length of this input that returns
an exact pure customer NE, leaving those isolated heavy customers in place and
keeping every other facility at load at most B. In particular, an initially
ordinary distinguished facility remains at load at most B.

The isolation hypothesis is essential. Merely requiring exactly one customer
of weight >B on each overloaded facility would allow additional lighter
customers and is false. For B=2, let x have a forced weight-3 customer, y a
forced weight-2 customer, and a weight-2 customer have options {x,y}. The seed
assigning the flexible customer to x has loads (5,2), but that customer's
conditional costs are 5 at x and 4 at y. Every exact NE assigns it to y,
whose load becomes 4>B. The isolated-macro premise used in SC-K-2-E and in
the claim ledger already excludes this seed; this clarification does not
alter that theorem or its registered scope.

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

## SC-K-BOX-POTENTIAL-STRONG-HARD: exact boxed potential optimization

**Exact scope.** Given a positive-integer MF-MODEL input, run the specified
SC-K-GREEDY-BUDGET algorithm, freeze its occupied layout and multiplicities,
and consider site-pure assignments satisfying every full box
`q_s gamma <= W_s <= (q_s+1) gamma`. Deciding whether the minimum of the
exact site-uniform customer potential over these assignments is at most a
given rational threshold is strongly NP-complete, even when the greedy
layout has one facility at every site, every movable customer is lighter
than `gamma`, and every such customer can choose every occupied site.
This is the complexity of **exact global optimization of this selector**;
it says nothing about finding *some* boxed NE or a factor-two certificate.

**Proof.** Reuse the 3-PARTITION instance and the `m`-site construction in
SC-K-LEXMAX-STRONG-HARD above, with `X=mB` and private weight `P=X+1`
at each site. The first greedy placement scores `P+X=2X+1`; after that,
each unused site scores `P=X+1>(P+X)/2=X+1/2`, while adding a seat at any
opened site can only lower its score further. Hence all `m=k` sites open,
each with `q_s=1`, and the last score is `gamma=P`. All item weights
`a_i<gamma`. For any assignment of the items, writing `S_s` for the
total assigned to site `s`, `0<=S_s<=X` and
`W_s=P+S_s in [P,2P]`; thus *every* assignment lies in the full boxes.

The exact potential `Phi=sum_s (W_s^2-sum_{i at s} w_i^2)/2` differs from
`(sum_s S_s^2)/2` by the assignment-independent constant
`PX-(sum_i a_i^2)/2` (the private self-weight terms cancel).
Since `sum_s S_s=mB`, Cauchy--Schwarz gives
`sum_s S_s^2>=mB^2`, with equality exactly when all `S_s=B`.
Set the threshold `K=PX+(mB^2-sum_i a_i^2)/2`. Then
`min Phi<=K` iff the 3-PARTITION input is YES: the
`B/4<a_i<B/2` bounds force each equal-sum group to have three items.
The construction and threshold have polynomial encoding on the strongly
bounded source family. A site assignment is a polynomial certificate, so
the threshold problem is strongly NP-complete. Every global potential
minimizer is an exact customer NE because all assignments are boxed here;
nevertheless the same family already has an easily constructed exact
facility equilibrium, as shown above. Internal independent algebraic
review completed; no external review or novelty claim is made.

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

## SC-K-GREEDY-MAX-MULT: initial customers choose a maximal-multiplicity site

**Statement.** In the exact greedy *initial* site assignment, every served
customer is assigned to an occupied site of maximum final facility
multiplicity among all occupied sites covering that customer. This holds for
arbitrary positive weights, arbitrary k, and the deterministic or any other
tie breaking among equal greedy scores. It is an incidence fact about the
initial greedy assignment, not a property asserted after customer transfers.

**Proof.** Suppose customer i first becomes served when site s opens and is
assigned there. Any other eventually occupied site t covering i must open
*later*: an earlier opening would already have covered i. Let \(W_s^0\) and
\(W_t^0\) be the weights first assigned on opening s and t. Just before s
opens, all of the later set assigned to t are still uncovered, and i is
uncovered too but is not in that later set. Hence t's then-new-coverage
score is at least \(W_t^0+w_i>W_t^0\). Greedy chose s, so
\(W_s^0>W_t^0\). If the final counts had \(q_t>q_s\), then at the time
of t's **last** facility insertion, site s was already occupied and its
next-insertion score obeyed

\[
 \frac{W_s^0}{q_s^{\rm then}+1}
 \ge\frac{W_s^0}{q_s+1}
 >\frac{W_t^0}{q_s+1}
 \ge\frac{W_t^0}{q_t},                         \tag{12a}
\]

contradicting greedy's selection of t with score \(W_t^0/q_t\).
Thus \(q_t\le q_s\). The claim is vacuous for an unserved customer and
continues to allow later strict customer moves between different
multiplicities. No factor-two algorithm follows from this ordering alone.

## SC-K-GREEDY-UNOPENED-2: what survives on-path equilibration

**Statement.** Run SC-K-GREEDY-BUDGET on a positive-reach instance and let
\(\gamma>0\) be the score selected at its last insertion. Keep its facility
layout fixed. Starting with its site assignments, perform any sequence of
*strictly improving single-customer site transfers*, where each customer is
independently uniform among facilities at its chosen site. The process ends at
an exact customer NE after finitely many transfers. At every state reached, all
facility loads are at least \(\gamma\). If \(r\) is a site never opened by the
greedy run, its genuinely newly covered weight \(N_r\), determined only by the
fixed occupancy, is at most \(\gamma\). Consequently, for any reached state,
any source facility with load \(a\), and any such \(r\),

\[
 q_u\ge2:\quad N_r\le a;
 \qquad
 q_u=1:\quad N_r+w(J_u\cap C_r)\le 2a.             \tag{12}
\]

These statements include the reached exact NE. They apply to this *reachable*
NE, not to every equilibrium at the greedy layout. No polynomial bound on the
number of site transfers follows.

**Proof.** Each insertion can only decrease an occupied site's next-insertion
score, and opening a site can only decrease the still-uncovered weight scored
at each unopened site. Thus the successive chosen maxima are nonincreasing.
The final load at a site equals its score at its **last** insertion: assigned
customers never leave during the greedy run. Hence every initial facility load
is at least \(\gamma\). At the final insertion every unopened site's then-score
is at most \(\gamma\); that score is exactly \(N_r\) at the completed occupancy.

For a strict customer transfer from site \(t\) to site \(v\), write
\(b=W_v/q_v\). The strict actual-cost improvement is
\((W_t-w_i)/q_t>b\). After the transfer all \(q_t\) source coordinates still
exceed \(b\), and all \(q_v\) target coordinates increase from \(b\) to a
value above \(b\). Thus the increasingly sorted load vector improves
lexicographically, as in uniform_two.md (3). Its first coordinate cannot
decrease. The finite assignment space and this strict increase prove eventual
termination; at termination no customer has a profitable site change, and
uniform mixing within its chosen site is an exact individual NE. The first
coordinate is always at least \(\gamma\), so \(a\ge\gamma\). When \(q_u=1\),
\(w(J_u)=a\), whence \(w(J_u\cap C_r)\le a\), proving (12).

**Precisely what this repairs.** In the four-customer counterexample above,
the strong budget (8) becomes \(8>6\), but the needed *initial deviator cap*
at the unopened site is only \(8\le2\cdot6\). If stationary sites can also
be assigned to capped bins with isolated macro customers, the deviation proof
can start with the deviator at load at most \(2a\), rather than at most \(a\),
and MF-PURE-CAP-POLY then preserves the factor-two bound. This is a
**conditional interface**, not a proof that stationary packing always works:
customer transfers may change \(W_t\), so the original occupied-site budgets
(5) and (7) need not persist. If the source disappears, the assignment of
its old customers among surviving sites is an additional obligation. A
polynomial method to reach an appropriate exact on-path NE is also unproved;
the imported identical-link algorithm applies to pure fixed-facility jobs,
not automatically to these site-uniform transfers with differing \(q_t\).

## SC-K-EQUAL-MULT-GREEDY-2: a polynomial factor-two subclass

**Exact conditional statement.** On an explicit positive rational MF-MODEL
input, run SC-K-GREEDY-BUDGET. Suppose its resulting occupancy has the *same*
multiplicity \(q\ge2\) at every occupied physical site. This condition is
decidable from the greedy output in polynomial time and makes no assumption
about the number of occupied sites, the number of clients, or their overlaps.
There is then an input-bit-polynomial procedure outputting a pure labeled
facility layout, an exact independent-mixed on-path customer NE, and a
polynomial-size, polynomial-time evaluable complete exact continuation with
factor at most 2. The conclusion is conditional on this greedy **output**;
it does not assert the same for arbitrary multiplicities or give an algorithm
for every instance.

**Site-level Nashification and the imported invariant.** Write \(\gamma\)
for the last greedy insertion score. As above every initial facility load is
at least \(\gamma\). Choose a facility inserted at the last step: its site
has final load \(\gamma\). Applying its occupied-target budget (5), valid
since \(q\ge2\), gives every other occupied site's assigned weight at most
\((q+1)\gamma\); its own weight is \(q\gamma\). Thus initially

\[
              q\gamma\le W_t\le(q+1)\gamma
              \quad\hbox{for every occupied site }t.             \tag{13}
\]

Temporarily regard each occupied *site* as one identical parallel machine
with load \(W_t\), and each covered customer as an indivisible job of weight
\(w_i\), restricted to the occupied sites covering it. The 2004
Gairing--Lücking--Mavronicolas--Monien Nashification algorithm computes an
exact pure restricted-link NE in time polynomial in the numbers of jobs,
links, allowed edges and the logarithm of total integer weight. Its
Corollary 4.3 explicitly preserves both the global minimum load from below
and the maximum from above in each blocking-flow call; the full algorithm
changes assignments only through such calls, including calls on subsets of
links, so the full global extrema obey the same bounds. This last inference
from its described algorithm is part of the present theorem import and must
not be confused with the paper's more prominently stated makespan bound.
Multiply rational weights by the product of denominators to use its integer
algorithm; the multiplier has polynomial bit length. Equation (13) therefore
still holds in the returned site assignment.

Keep the greedy facility layout. For each customer assigned to site \(t\),
independently randomize uniformly among its \(q\) colocated facilities.
The customer's cost at its chosen site is
\(w_i+(W_t-w_i)/q\), while a facility at another accessible occupied site
\(v\) costs \(w_i+W_v/q\). Since all occupied sites have the *same* \(q\),
its exact no-deviation condition is precisely
\(W_t-w_i\le W_v\), the restricted identical-machine pure NE condition.
Uniformity among facilities at one site handles all within-site choices.
The resulting independent-mixed profile is an exact on-path client NE;
every facility has load \(a=W_t/q\ge\gamma>0\).

For any actual deviation, the source site survives because \(q\ge2\).
At its source, \(W_u=qa\). At every other occupied site \(t\), (13) gives
\(W_t\le(q+1)\gamma\le(q+1)a\), exactly budget (5). For any unoccupied
target \(r\), the occupancy has not changed, so its newly covered weight
still satisfies \(N_r\le\gamma\le a\), exactly (6). Thus the explicit
MF-PACK-2 construction of uniform_two.md Section 5.1 produces a feasible
pure assignment after each deviation with isolated clients heavier than
\(2a\), every ordinary facility at load at most \(2a\), and the deviator
ordinary. MF-PURE-CAP-POLY computes a pure exact customer NE preserving
that cap. Repeating for the \(k(|S|-1)\) actual deviations and using the
polynomial-time fixed-layout default NE procedure for any queried remaining
layout yields a compatible complete continuation. This proves the conditional
factor-two and bit-polynomial statement.

**Boundary.** If some occupied sites have multiplicity one, their departure
can erase a site and the orphan-aware budgets (7)--(8) must be recovered;
site-level NE at equal multiplicity one alone does not do this. If occupied
sites have unequal multiplicities, the site-choice cost inequalities are not
those of identical machines. The present argument makes no claim about either
case. It is an algorithmic theorem for a recognizable subclass of greedy
outputs, not a proof of the unrestricted target.

## SC-K-COMPONENT-MULT-GREEDY-2: polynomial factor two across components

**Exact conditional statement.** Run the same greedy algorithm, and form the
graph on *occupied physical sites* in which two sites are adjacent when some
customer covers both. Suppose (i) every connected component has constant
facility multiplicity \(q_t\), and (ii) each component of multiplicity one
consists of a single site. These conditions are polynomially checkable from
the greedy output. Then the same layout admits an input-bit-polynomial
factor-two complete exact continuation. This strictly generalizes the
equal-\(q\ge2\) sufficient condition above: disconnected occupied-site
components may have different multiplicities, and singleton components may
have \(q=1\). It does not cover a component with differing multiplicities or
a multi-site component with \(q=1\).

**Proof.** The greedy last score \(\gamma\) bounds each initial per-facility
load from below. Applied to a facility inserted last, budget (5) if its site
has multiplicity at least two, or budget (7) after dropping its nonnegative
overlap term otherwise, gives

\[
    q_t\gamma\le W_t\le(q_t+1)\gamma
    \quad(t\text{ occupied});\qquad N_r\le\gamma
    \quad(r\text{ unoccupied}).                         \tag{15}
\]

Each served customer's entire set of accessible occupied sites lies in one
graph component. Within each component with common \(q\ge2\), regard sites
as restricted identical machines and run the published range-preserving
Nashification as in the preceding theorem. It changes no customer to another
component and retains the interval in (15) for each site. Leave a singleton
\(q=1\) component untouched: every customer served there has that site as
its *only* occupied option. Site-uniform mixing after these independent
procedures is an exact customer NE, and every source facility has
\(a=W_u/q_u\ge\gamma\).

For a source with \(q_u\ge2\), all other occupied sites satisfy
\(W_t\le(q_t+1)\gamma\le(q_t+1)a\), and unopened sites satisfy
\(N_r\le\gamma\le a\). Thus (5)--(6) hold. For a singleton-component
source with \(q_u=1\), its assigned customer set \(J_u\) and weight
\(a=W_u\) are exactly those of the greedy profile, and no customer in
\(J_u\) covers any other occupied site. Therefore (7) follows from
\(W_t\le(q_t+1)\gamma\le(q_t+1)a\). The original greedy budget (8),
\(N_r+w(J_u\cap C_r)\le a\), is unchanged because both \(J_u\) and
the occupied-site set are unchanged. We have recovered *all four*
orphan-aware budgets for the exact on-path NE. Apply MF-PACK-2 and
MF-PURE-CAP-POLY to every deviation, then the polynomial default rule;
the complete factor-two certificate is bit-polynomial. Graph construction,
component decomposition and the finitely many scheduling calls also use
polynomial time. This conditional theorem does not imply that all greedy
outputs satisfy the component hypotheses.

## SC-K-DISTINCT-GREEDY-3: a weaker polynomial bound with no colocation

**Statement.** If the same greedy procedure occupies \(k\) distinct sites
with one facility apiece, then an exact on-path *pure* client NE and a
polynomial-time evaluable complete exact continuation of factor at most 3
can be computed in input-bit-polynomial time. This statement concerns only
instances whose greedy output has that property. The proof below alone does
not imply factor 2; the later SC-K-DISTINCT-GREEDY-2 now strengthens it.

**Proof.** The greedy last-insertion score \(\gamma>0\) bounds initial loads
below. Budget (7), applied to the last inserted singleton source and dropping
its nonnegative orphan term, bounds every other site load by \(2\gamma\);
its own load is \(\gamma\). With one facility at each occupied site, the
customer game is exactly restricted scheduling on identical machines. The
same range-preserving Nashification above returns a pure NE with every
facility load \(a_f\in[\gamma,2\gamma]\).

After any facility \(f\) of load \(a\) moves, keep all customers formerly
assigned outside its source where they were. Assign each of its old customers
that remains covered to any accessible facility at the new layout, and mark
the others unserved. Assign each genuinely new customer to \(f\) when the
target is previously unoccupied. The old source contributes total weight
\(a\), and the newly covered weight is at most \(\gamma\). Hence every
stationary facility has initial load at most \(2\gamma+a\), while \(f\)
has initial load at most \(a+\gamma\); both are at most
\(a+2\gamma\le3a\). Nashification on the *actual* deviation layout is
bit-polynomial, returns a pure exact customer NE, and does not increase
makespan. The deviator therefore earns at most \(3a\). The polynomial default
rule and labeled-layout argument of uniform_two.md Section 7 complete one
continuation. This older proof is retained to mark what its coarse load
summary can establish; the same greedy distinct-site layout has the stronger
factor-two property proved in the next section.

**Why the scalar summary alone stops at three.** For every integer \(M\ge1\),
consider two facilities, sites \(S,B,R\), and four customers with
weight/coverage pairs
\((M,\{S,B\}),(2M-1,\{B,R\}),(1,\{B\}),(M,\{R\})\).
The layout \((S,B)\) has a unique exact customer NE, of loads \((M,2M)\).
With \(\gamma=M\), these loads belong to \([\gamma,2\gamma]\) and the
unopened site's genuinely new reach is \(N_R=\gamma\). After the first
facility moves \(S\to R\), the site-exclusive weights at \(B,R\) are
\(M+1,M\), and the shared \(2M-1\) customer strictly prefers \(R\) in
every strategy of the others. The unique NE gives the deviator \(3M-1\),
a ratio \(3-1/M\). Thus the two scalar premises *alone* cannot imply any
factor below 3, even allowing mixed equilibria. This is **not** a
counterexample to the conditional greedy theorem: greedy first opens \(B\)
because its reach is \(3M\), then inserts the second facility at \(B\)
because \(3M/2>M\). Any improvement from 3 to 2 in the distinct-site
greedy subclass must exploit more of the greedy coverage incidence than
the scalar interval and new-reach bound.

## SC-K-DISTINCT-GREEDY-2: factor two for all-distinct greedy output

**Exact conditional statement.** Run SC-K-GREEDY-BUDGET on an explicit
positive rational common-catalog input. If all \(k\) greedy facilities occupy
different sites, an input-bit-polynomial procedure outputs the same labeled
layout, an exact **pure** on-path customer NE, and a polynomial-time evaluable
complete exact continuation with factor at most 2. No special customer
overlap, weight, or disconnectedness assumption is needed within this output
class. This strengthens SC-K-DISTINCT-GREEDY-3; it does not imply that greedy
always returns distinct sites.

**Proof.** Let \(R=\max_{s\in S}w(C_s)>0\). Greedy first opens a site \(s^*\)
with reach \(R\), assigning it *all* those customers. Under the stated
condition, it never inserts another facility at \(s^*\), and its assigned
weight stays \(R\). Before **every** later insertion, adding a facility at
\(s^*\) remains a legal occupied-site candidate of score \(R/2\). Greedy
chooses a greatest score, so in particular its last score obeys
\(\gamma\ge R/2\). Each final occupied site has load at least \(\gamma\),
by the monotonicity of selected scores proved above.

Since every occupied site has exactly one facility, the fixed-layout
customer game is restricted identical-machine scheduling. Apply the
published Gairing et al. polynomial Nashification to greedy's initial
assignment. Its global minimum-load preservation yields an exact pure
on-path NE in which every labeled facility earns
\(a_f\ge\gamma\ge R/2\). This does not require preserving the greedy
orphan-aware transfer budgets. After any unilateral deviation to a site
\(r\), that facility's payoff in **any** exact client NE is at most the
total weight of all customers covered by \(r\), namely
\(w(C_r)\le R\le2a_f\). Every fixed layout has a pure client NE computable
by the same published restricted identical-machine algorithm, so one can
select such a NE for every actual deviation and a default at all remaining
labeled layouts. All operations, fraction clearing and output certificates
have polynomial input-bit complexity. For \(R=0\), every payoff is zero.

The non-greedy example immediately before this section is compatible with
the theorem: there the greedy algorithm puts both facilities at B, so its
distinct-site premise fails. In particular a bound based only on the
interval \([\gamma,2\gamma]\) misses the first-site \(R/2\) comparison.

## SC-K-GREEDY-STATIC-PACK-NO: a surviving-site obstruction

The preceding unopened-target inequality does **not** make the original
MF-PACK-2 proof apply after arbitrary strict customer site repair. Here is
a positive-integer example where the source survives the deviation, but a
different stationary occupied site cannot be packed under that proof's cap
if its *current* site assignments are frozen.

There are \(k=8\) facilities and five common sites in tie-breaking order
\(A,E,B,C,D\). The customers are:

| weight | covered sites |
| ---: | :--- |
| 20 | A |
| 8 | A, B |
| 24 | B, E |
| 20 | B |
| 10 | A, C |
| 30 | C |
| 13 | B, D |
| 67 | D |
| 20 | E |

Greedy insertion with increasing site-order tie breaking is
\((D,80),(B,52),(C,40),(D,40),(D,80/3),(B,26),(A,20),(E,20)\),
so \(\gamma=20\). Initial multiplicities in site order are
\((1,1,2,1,3)\), with site weights \((20,20,52,40,80)\).
Transfer the customers of weights \(8,10,13,8,24\) in order along
\(B\to A,C\to A,D\to B,A\to B,B\to E\). Each move is a strict
conditional-cost improvement; its old and new costs are respectively

\[
 (30,28),\quad(40,38),\quad(106/3,35),\quad
 (38,73/2),\quad(89/2,44).                         \tag{14}
\]

The final assigned site weights are
\((W_A,W_E,W_B,W_C,W_D)=(30,44,41,30,67)\). This is an exact site-uniform
customer NE: the four customers who can choose between two occupied sites
have conditional cost comparisons
\(8+33/2\le8+30\) at B versus A,
\(24+20\le24+41/2\) at E versus B,
\(10+20\le10+30\) at A versus C, and
\(13+14\le13+67/3\) at B versus D. All other customers have only one
accessible occupied site. Uniform independent mixing within each site is
an exact choice among its colocated facilities.

Take either B facility as the deviator, of on-path load \(a=41/2\), and
move it, for example, to A; B still has one stationary facility. At E,
the one stationary facility retains customers of weights 20 and 24 if
all source-outside assignments are frozen. Their total is
\(44>2a=41\), while neither customer individually weighs more than 41.
Thus E cannot be represented by a \(\le2a\) bin or an isolated macro
under that *fixed site assignment*. This refutes the proposed interface
"repair customers on the greedy layout, then freeze their sites and apply
MF-PACK-2 separately at every surviving occupied site." It does **not**
refute a factor-two continuation: the 24 customer also covers B and may
be reassigned before off-path Nashification. It does not exclude a different
on-path NE or a different facility layout. The remaining proof obligation
is a cross-site reassignment or another invariant that handles such
surviving-site overloads in polynomial time.

## SC-K-GREEDY-CAP-INFEASIBLE: cross-site reassignment need not restore the cap

The preceding obstruction can be strengthened without claiming any failure
of factor-two stability. Add a sixth catalog site \(G\) **after** \(D\) in
the tie order. The weight-24 customer now covers \(\{B,E,G\}\), and add
one private weight-20 customer covering only \(G\); keep every other
customer and site of the preceding example. There are ten customers and
\(k=8\). Because \(G\) contributes only its private 20 of *new* weight
after B opens, the greedy insertion order and first nine customers'
assignments are unchanged, and G stays unoccupied. The five strict
transfers in (14) reach the same exact site-uniform NE, now with
\(W=(30,44,41,30,67,0)\) on \((A,E,B,C,D,G)\). The G-private client is
unserved until a facility moves there.

Move either B facility to G. Its on-path load is \(a=41/2\), so the
desired ordinary cap is \(2a=41\). In the actual deviation layout there
is **one** facility each at B, E and G. Three private weight-20 customers
are forced onto B, E and G respectively. The weight-24 customer covers
exactly those three sites, so every feasible pure customer assignment
puts it together with one of these forced weight-20 clients. That
facility's load is at least \(44>41\); neither of the two clients weighs
more than 41, so this overload cannot be isolated as a single macro
client. The separate D-private customer of weight 67 *can* be isolated
as a macro, but does not affect this three-site obstruction. Therefore
**no** initial pure customer assignment satisfies the global hypothesis
of MF-PURE-CAP-POLY with threshold 41 after this deviation, even when
cross-site customer reassignment is allowed.

Nonetheless the deviation game has a pure exact customer NE with
\(G\), the deviating facility, at load **20**. Assign the two A clients
of weights 20,10 to A; the E-private 20 and shared 24 to E; the B-private
20 and shared 8 to B; 30 to C; the D-private 67 and shared 13 to separate
D facilities, leaving the third D facility empty; and the G-private 20
to G. Loads in site order are
\(A:30,E:44,B:28,C:30,D:(67,13,0),G:20\). The weight-24 customer
at E pays 44, tying its alternative at G and strictly beating the B
alternative of 52. The weight-8 customer at B pays 28 versus 38 at A;
weight 10 at A pays 30 versus 40 at C; weight 13 at D pays 13 versus
41 at B and ties an empty D facility; weight 67 pays 67 and ties an
empty D facility. Thus nobody strictly improves. These comparisons
distinguish a pure off-path exact NE from the infeasible *global cap*
hypothesis. The example shows that merely allowing cross-site transfers
inside the old cap-preserving repair is insufficient; an unrestricted
algorithm must allow some stationary facility to exceed \(2a\) safely,
or use another on-path layout or continuation mechanism. It gives no
lower bound on the instance's best factor and no hardness result for
finding a factor-two certificate.
For this deviation the smallest feasible *ordinary* cap under the same
isolated-macro convention is exactly 44: the three-site argument gives
the lower bound, and the displayed pure NE isolates the weight-67 client
while every other facility has load at most 44.

## SC-K-RANGE-GREEDY-2: a multiplicity-class range certificate

**Exact conditional statement.** On any positive-reach explicit rational
MF-MODEL input, run SC-K-GREEDY-BUDGET. For each final occupied multiplicity
\(q\), use the *initial* greedy assigned site weights \(W_t^0\) to compute
\[
 \alpha_q=\min_{t:q_t=q}W_t^0/q,
 \qquad\beta_q=\max_{t:q_t=q}W_t^0/q.          \tag{16R}
\]
For each customer \(i\) initially assigned to site \(s\), set \(q_i=q_s\)
and check, for **every** other occupied site \(v\) covering \(i\) whose
multiplicity differs from \(q_i\),
\[
                \beta_{q_i}-w_i/q_i\le\alpha_{q_v}.   \tag{17R}
\]
If all these rational inequalities hold, an input-bit-polynomial procedure
constructs the same labeled layout, a site-uniform exact independent-mixed
on-path customer NE, and a complete exact factor-two continuation. This is
an efficiently recognizable **output subclass**, not an algorithm for all
inputs. Unlike the next light-client criterion, it can allow a customer
lighter than the final greedy score to span different multiplicities.

**Construction and on-path proof.** Group occupied sites by their final
multiplicity \(q\). Partition customers by the multiplicity of their
*initial assigned site*. For each group, treat its sites as restricted
identical machines and its assigned customers as unsplittable jobs allowed
at **all and only** their accessible occupied sites of that same
multiplicity. Their initial assignment is feasible. Apply the polynomial
Gairing et al. Nashification separately to each group. Its full algorithm
preserves the initial minimum and maximum machine load within that group,
so every final site \(t\) in the group obeys
\[
       \alpha_q\le W_t/q\le\beta_q,
       \qquad q\gamma\le W_t\le(q+1)\gamma.     \tag{18R}
\]
The second interval follows from the first and the initial greedy box
\(q\gamma\le W_t^0\le(q+1)\gamma\). Within its own group, every client
satisfies the machine NE comparison \(W_t-w_i\le W_v\), equivalent to its
site-uniform conditional cost comparison after division by common \(q\).
For a cross-group alternative \(v\), even if the algorithm moved client
\(i\) to another site within its original group, its current external
load is at most \(\beta_{q_i}-w_i/q_i\), while the other site's load is at
least \(\alpha_{q_v}\). Condition (17R) blocks that deviation. Uniform
independent mixing among facilities at the chosen site gives an exact
customer NE. Restricting a cross-group customer to its **original site**
would be insufficient here: it might still want to move to another site
with the same multiplicity; the algorithm retains all those same-group
options. All calls use integer weights after clearing rational denominators
with polynomial bit growth.

**All facility deviations, including singleton-source disappearance.** For
any source multiplicity at least two, the second interval in (18R) and
\(N_r\le\gamma\) restore the stationary-site budgets (5)--(6) with
\(a=W_u/q_u\ge\gamma\). For a singleton source, let \(K\) be the set of
all \(q=1\) occupied sites and \(P\) the clients initially assigned to K.
SC-K-GREEDY-MAX-MULT says every client's occupied options in \(P\) lie
inside K. When the first site \(s\in K\) opened, all of \(P\) was still
uncovered; for every \(t\in K\), greediness therefore gave
\[
       w(P\cap C_t)\le W_s^0\le2\gamma.           \tag{19R}
\]
The groupwise algorithm never moves clients between multiplicities, so
\(J_t\subseteq P\) for all \(t\in K\). For a singleton target \(t\ne u\),
\(W_t+w(J_u\cap C_t)\le w(P\cap C_t)\le2\gamma\le2a\): budget (7).
Against a higher-multiplicity occupied target \(t\), the overlap is zero
by MAX-MULT and (18R) gives budget (7). Against an unopened site \(r\),
\(N_r+w(J_u\cap C_r)\le\gamma+a\le2a\). This last bound replaces the
stronger old budget (8) only for the deviator: after the source disappears,
pack the customers of each *stationary* site by MF-PACK-2 using (7), and
start the deviator with at most \(2a\) rather than \(a\). It is still an
ordinary capped facility, so MF-PURE-CAP-POLY computes a pure full-game NE
without letting its load exceed \(2a\). Targets already occupied use the
same stationary packing with deviator initially empty. Assemble the
polynomially many deviation exceptions and a polynomial default pure NE
into one complete continuation, as in MF-CONT-COMPLETE. This is a bit-
polynomial **construction**, conditional on (17R).

The condition genuinely admits light cross-multiplicity clients: with
\(k=5\), sites \(A,B,C\), and customers
\((22,A),(2,AB),(5,AC),(24,B),(14,C)\), greedy selects
\((A,29),(B,24),(A,29/2),(C,14),(B,12)\). Thus
\(q=(2,2,1),\gamma=12,\alpha_2=12,\beta_2=29/2,\alpha_1=14\).
The weight-5 customer crosses \(q=2\) to \(q=1\) even though
\(5<\gamma\), yet \(\beta_2-5/2=12\le14=\alpha_1\). The weight-2 customer
has only same-\(q\) options and moves \(A\to B\); site weights become
\((27,26,14)\), an exact NE. The light-overlap condition below fails here,
while (17R) passes.

## SC-K-LIGHT-COMPONENT-GREEDY-2: repair only light-client components

**Exact conditional statement.** Run the greedy algorithm on a positive-reach,
explicit rational MF-MODEL instance, and let \(\gamma>0\) be its final
insertion score. Form a graph on its occupied sites, joining \(t,v\) if a
client of weight **strictly less** than \(\gamma\) covers both. Suppose each
connected component has constant facility multiplicity. Equivalently, no
light client covers occupied sites with different multiplicities. Then an
input-bit-polynomial algorithm
computes an exact site-uniform on-path customer NE, the same greedy labeled
facility layout, and a polynomial-size, evaluable complete exact factor-two
continuation. Heavy clients of weight \(\ge\gamma\) may connect sites with
different multiplicities, and light clients may move among multiple
multiplicity-one sites. This strictly includes both the earlier
full-overlap-component theorem and the immediately stable heavy-overlap
subclass below. It is also a corollary of the preceding range certificate:
every cross-multiplicity customer then has \(w_i\ge\gamma\), so
\(\beta_q-w_i/q\le\gamma\le\alpha_{q_v}\). The old all-distinct output class
automatically meets the hypothesis, though its direct proof above has a
stronger reach-based threat bound.

**Construction and proof.** The initial greedy assignment obeys, for every
occupied \(t\),
\[
       q_t\gamma\le W_t\le(q_t+1)\gamma.        \tag{16a}
\]
Fix every client with \(w_i\ge\gamma\) at its initial site. Within each graph
component of common multiplicity \(q\ge1\), regard its occupied sites as
identical restricted machines, its light clients as jobs allowed at **all**
their covered occupied sites, and its fixed heavy clients as jobs allowed
only at their initial site. The graph definition ensures that every allowed
site of a light client lies in this one component. Apply the published
Gairing--Lücking--Mavronicolas--Monien polynomial Nashification algorithm to
the initial assignment. It returns a pure machine NE and preserves both
global load extrema from below and above within that component. Thus (16a)
holds at termination. This applies just as well to multiple multiplicity-one
sites in a component. Multiplying rational weights by their
denominator product yields integer weights with polynomial bit length, so
these calls have input-bit-polynomial complexity.

Now independently randomize each client uniformly among the \(q_t\)
facilities at its assigned site. Each light customer's alternative occupied
sites have the same multiplicity \(q\); its conditional cost comparison is
\((W_t-w_i)/q\le W_v/q\), exactly the restricted identical-machine NE
condition after canceling the common \(w_i\). For a fixed heavy customer at
\(t\), (16a) and \(w_i\ge\gamma\) give
\[
          (W_t-w_i)/q_t\le\gamma\le W_v/q_v
\]
at every other accessible occupied \(v\), irrespective of its multiplicity.
Customers with one occupied option are automatic. Hence the full original
game has an exact independent-mixed on-path customer NE.

For any source \(u\) with \(q_u\ge2\), its load \(a=W_u/q_u\ge\gamma\);
all other sites satisfy \(W_t\le(q_t+1)\gamma\le(q_t+1)a\), and every unopened
site has \(N_r\le\gamma\le a\). These are budgets (5)--(6).

The multiplicity-one case uses a different, weaker budget. Let \(K\) be
**all** final occupied sites with \(q_t=1\), and \(P\) the clients initially
assigned by greedy to sites in \(K\). By SC-K-GREEDY-MAX-MULT, each client
of \(P\) has all its accessible occupied sites in \(K\). When the first
site \(s\in K\) opened, every client of \(P\) was still uncovered: any
previously opened site covering such a client would be an occupied option
outside \(K\), contrary to the maximal-multiplicity lemma. At that instant,
for every \(t\in K\), its unopened new-coverage score included every
client of \(P\cap C_t\), so greediness and the initial box imply
\[
               w(P\cap C_t)\le W_s^0\le2\gamma.     \tag{16b}
\]
For \(t=s\), its chosen opening score is \(W_s^0\) and the same inequality
holds. The componentwise Nashification neither sends a \(P\) client
outside \(K\) nor brings a client from outside \(P\) into \(K\). Hence
every resulting singleton-site assigned set \(J_t\) is contained in \(P\).

Fix a departing facility at singleton site \(u\), with \(a=W_u\ge\gamma\).
For another singleton target \(t\), the disjoint sets \(J_t\) and
\(J_u\cap C_t\) both lie in \(P\cap C_t\), and therefore
\(W_t+w(J_u\cap C_t)\le2\gamma\le2a=(q_t+1)a\): budget (7).
For an occupied target of multiplicity at least two, every client of
\(J_u\subseteq P\) is unable to access it by the maximal-multiplicity
lemma, so the overlap term is zero and (16a) proves (7). For an unopened
target \(r\), the original strong budget (8) need **not** survive: instead
\[
            N_r+w(J_u\cap C_r)\le\gamma+a\le2a.     \tag{16c}
\]
In the deviation construction of `uniform_two.md` Section 5.2, use the
unchanged stationary-site packing from (7), but give the deviator at most
the total in (16c), rather than the old stronger allowance \(a\). It is
still an ordinary facility of load at most \(2a\), so MF-PURE-CAP-POLY
preserves its cap while reaching a pure exact NE. For an already occupied
target the deviator initially gets zero, as before. Thus all labeled
deviations have factor-two pure exact continuations; a polynomial default
completes the rule. This proof does not infer a polynomial bound for
arbitrary customer-improvement paths.

The condition can require *real* repair while permitting unequal connected
full-overlap multiplicities. For \(k=5\), sites \(A,B,C\), take clients
\((17,A),(2,AB),(10,AC),(24,B),(10,C)\). Greedy selects
\((A,29),(B,24),(A,29/2),(B,12),(C,10)\), so \(q=(2,2,1)\) and
\(\gamma=10\). The weight-2 customer strictly moves \(A\to B\), taking
site weights from \((29,24,10)\) to \((27,26,10)\); this is an exact
site-uniform NE. The full overlap graph joins A to C through the heavy
weight-10 client, while the light graph has only the equal-multiplicity edge
A--B. Thus neither old full-component condition nor the all-heavy condition
below covers this example.

## SC-K-GREEDY-HEAVY-OVERLAP-2: an immediately stable mixed-multiplicity subclass

**Exact conditional statement.** On an explicit positive rational MF-MODEL
instance of positive maximum reach, run SC-K-GREEDY-BUDGET with any fixed
polynomial tie rule and let \(\gamma>0\) be its final insertion score. Suppose
every customer covering **at least two distinct occupied sites** has weight
\(w_i\ge\gamma\). Then the unmodified greedy site-uniform profile is an exact
independent-mixed customer NE, and a factor-two complete exact continuation
can be constructed in input-bit-polynomial time. The condition is checked
*after* greedy placement; it permits different facility multiplicities at
sites in the same customer-overlap component. It is a conditional algorithm,
not the unrestricted all-input target.

**Proof.** The last insertion and SC-K-GREEDY-BUDGET give, for every occupied
site \(t\),
\[
 q_t\gamma\le W_t\le(q_t+1)\gamma.                 \tag{16}
\]
For a customer \(i\) initially assigned to \(t\) with an alternative occupied
site \(v\), its conditional cost at any facility at \(t\) is
\(w_i+(W_t-w_i)/q_t\). At \(v\) it would be \(w_i+W_v/q_v\). By the weight
assumption and (16),
\[
 \frac{W_t-w_i}{q_t}\le\gamma\le\frac{W_v}{q_v}.   \tag{17}
\]
Customers with only one occupied site have no cross-site move; independent
uniform mixing makes all facilities within their selected site indifferent.
Thus this is an exact customer NE even at equality \(w_i=\gamma\). Since no
assignment or occupancy changes, all four orphan-aware greedy transfer
budgets remain valid. The explicit packing construction of
`uniform_two.md` Sections 5--7, MF-PURE-CAP-POLY and the polynomial default
pure NE algorithm complete the exact continuation. Greedy scores, comparison
with \(\gamma\), the packing and all completion calls have polynomial input-bit
complexity. For zero maximum reach, the trivial zero-load certificate applies.

For a concrete mixed-multiplicity overlap, let \(k=3\), sites \(A,B\), and
three clients \((2,\{A\}),(2,\{A,B\}),(3/2,\{B\})\), with \(A\) first in
the tie order. Greedy chooses \(A,A,B\), with \(q_A=2,q_B=1,\gamma=3/2\).
The shared client weighs 2 and satisfies the condition. This example is not
covered by the earlier componentwise equal-multiplicity criterion.

## SC-K-TWO-SITE-COMPONENT-GREEDY-2: mixed multiplicities in a two-site component

**Exact conditional theorem.** Run the polynomial greedy procedure on an
explicit positive rational common-catalog instance with arbitrary (k\ge2)
and positive maximum site reach. Make the graph on occupied sites in which
two sites are adjacent if a client can use both. Suppose every component
either has a constant facility multiplicity, or consists of exactly two
sites (with potentially unequal multiplicities). This is a polynomially
checkable condition on the greedy **output**. Then, in input-bit-polynomial
time, the greedy labeled layout can be equipped with a site-uniform exact
independent-mixed on-path customer NE and a complete exact factor-two
continuation. The mixed two-site case does not require the cross-multiplicity
range condition (17R). Components of larger size and varying multiplicity
remain outside this theorem.

**Two-site customer repair.** Fix a two-site component (H,L) with
(Q=q_H>q=q_L\ge1). By SC-K-GREEDY-MAX-MULT, every customer able to use
both occupied sites starts at (H). All other served customers in this
component have exactly one occupied option. Scan the common customers in
**nonincreasing weight** order, each once. Transfer the currently scanned
customer (i) from (H) to (L) precisely when its current move is a
strict cost improvement. Write

\[
  \Delta=W_H/Q-W_L/q.
\]

A customer still at (H) of weight (w) strictly wants to move iff
(\Delta>w/Q). If it moves, (\Delta) decreases by
(w(1/Q+1/q)); thus a customer skipped at (H) can never begin to want
to move. Immediately after a moved weight (w), strict improvement gives
(\Delta>-w/q). If any moves occur, apply this to the **last** moved
weight (w_*). No subsequent moves change (\Delta), and every previously
moved weight is at least (w_*), so every customer now at (L) satisfies
(\Delta>-w_*/q\ge-w/q): none wants to return to (H). If no move
occurs, the skipped-customer argument already proves equilibrium. This is
an exact site-level NE in at most the number of common customers in that
component, including equality cases (ties are not transfers). Independent
uniform choice among facilities within the selected site turns it into an
exact customer NE of the original fixed-layout game.

**Load box invariant.** At the end of greedy, every occupied site obeys
(q_t\gamma\le W_t\le(q_t+1)\gamma), where (\gamma>0) is the
last insertion score. More generally, a strict transfer of weight (w)
from multiplicity (Q\ge q) to multiplicity (q), while this box holds,
has (w<\gamma): its old external load
((W_H-w)/Q\le\gamma+(\gamma-w)/Q) exceeds the target's old load
(W_L/q\ge\gamma). The new source load is (>\gamma). The strict
improvement inequality and the old upper box also give

\[
 W_L'/q < \gamma+\gamma/Q+w(1/q-1/Q)
          < \gamma+\gamma/q,
\]

where the last step uses (q\le Q) and (w<\gamma). All unaffected
sites keep their box. Thus every transfer in the descending scan preserves
the full box. For any component with constant (q), instead run the
published restricted identical-machine Nashification on its initial
customers and occupied sites; it preserves both load extrema, hence the
same box. Different components have no common reachable customer, so these
procedures combine into one exact customer NE. The denominator product has
polynomial bit length for rational weights; sorting, scans, and scheduling
calls are all bit-polynomial. An unserved customer has no occupied option
and is unaffected.

**Facility deviations.** Every on-path facility has load (a\ge\gamma),
and every unoccupied target has new coverage (N_r\le\gamma). For a
source with (q_u\ge2), the source survives, and the box yields
(W_t\le(q_t+1)\gamma\le(q_t+1)a) at each other occupied site;
the occupied and empty-target packing budgets (5)--(6) follow. If a
singleton source (u) is in an unequal two-site component, its partner
(H) has (Q>1). Every client now at (u) who can use an occupied site
other than (u) can use only (H), and the transferred common clients
started there. Hence
(W_H+w(J_u\cap C_H)=W_H^0\le(Q+1)\gamma\le(Q+1)a).
At other occupied sites the orphan overlap is zero and the box proves
(7). If instead the singleton source is in a constant-(q=1)
component, all customers assigned in such components were initially
assigned to (q=1) sites; the initial singleton-site customer pool
bound (19R) gives (7), including multi-site components. For an unopened
target in either singleton case, it suffices to put at most
(N_r+w(J_u\cap C_r)\le\gamma+a\le2a) on the deviator; the stronger
original budget (8) is not needed. Pack the surviving sites using (7),
isolate atoms above (2a), and apply MF-PURE-CAP-POLY to reach a pure
exact off-path NE without increasing the deviator above (2a).
The same construction covers an occupied target, starting the deviator
empty. MF-CONT-COMPLETE supplies the polynomial-size evaluable full rule.
This argument uses the customer pool only for untouched constant-(q=1)
components; the mixed-pair singleton may receive clients from the
higher-multiplicity partner and requires the displayed identity instead.

**Strict extension of the existing range condition.** Take (k=3), two
sites A,B and customers ((9,\{A\}),(1,\{A,B\}),(4,\{B\})).
Greedy inserts A with score 10, A with score 5, and B with score 4,
so (q_A=2,q_B=1,\gamma=4). Its shared weight-1 customer fails
(17R): (\beta_2-1/2=5-1/2>\alpha_1=4). The descending scan moves
this customer A\(\to\)B, producing weights ((9,5)) and exact NE:
its old external load is (9/2) while B's old load was 4, and at B
its external load is 4 while A's final load is (9/2). The load box
and all deviation cases above apply. This example separates output
classes, not the strength of their universal factor-two guarantees.

## SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2: arbitrarily many mixed-multiplicity sites

**Exact conditional theorem.** Run SC-K-GREEDY-BUDGET on any explicit
positive rational common-catalog input with arbitrary labeled (k\ge2)
and positive maximum reach. In each connected component of the graph on
occupied sites joined by a jointly accessible customer, suppose either
(i) all sites have the same final facility multiplicity, or (ii) each
served customer with an occupied option in this component can choose
**either precisely one occupied site or every site of this component**.
The condition is checked in polynomial time from the greedy output. Then
one can construct in input-bit-polynomial time the same labeled facility
layout, a site-uniform exact independently mixed on-path customer NE, and
a complete exact factor-two continuation. No upper bound on the number
of occupied sites or assumption of equal multiplicities is imposed in
(ii). Since every two-site component satisfies (ii), this output class
contains SC-K-TWO-SITE-COMPONENT-GREEDY-2; its constructive mechanism is
different. The general mixed-multiplicity component with partial
overlaps remains outside the theorem.

**Descending list assignment and on-path NE.** For a constant-multiplicity
component use the published restricted identical-machine Nashification,
as in SC-K-RANGE-GREEDY-2; it preserves the greedy load box. Consider a
component satisfying (ii) with nonconstant multiplicities. Write (F)
for customers eligible at **all** its occupied sites and (P_t) for
customers eligible at only (t), with weights denoted by the same letters.
There must be a shared customer; hence the component's first-opened site
(H) initially receives **every** customer of (F). All other sites
initially receive only their (P_t) customers. SC-K-GREEDY-MAX-MULT
implies (Q=q_H\ge q_t) for all sites in the component; as multiplicities
are not all equal, (Q\ge2). Initially

\[
 W_H^0=P_H+w(F),\qquad W_t^0=P_t\quad(t\ne H),\qquad
 q_t\gamma\le W_t^0\le(q_t+1)\gamma.             \tag{24}
\]

Remove the common customers from (H), keep all private customers fixed,
sort (F) by nonincreasing weight, and assign each in turn to a site
of minimum *current per-facility load* (W_t/q_t) among all sites in
the component (fix a site order for ties). This takes (O(n|S|))
rational comparisons after sorting. For any common customer (i) finally
at (s), let (j) be the **last** common customer assigned to (s).
Then (w_j\le w_i) and, immediately before assigning (j), site (s)
had minimum normalized load. As no later customer enters (s), for
every other occupied site (v) in the component,

\[
 \frac{W_s-w_i}{q_s}
 =\frac{W_s^{\mathrm{before}\ j}+w_j-w_i}{q_s}
 \le\frac{W_s^{\mathrm{before}\ j}}{q_s}
 \le\frac{W_v^{\mathrm{before}\ j}}{q_v}
 \le\frac{W_v}{q_v}.                              \tag{25}
\]

This is the exact customer no-deviation inequality after site-uniform
independent mixing. A private customer has no other occupied option,
and no customer can change to another component. Customers with no
occupied option remain unserved. Thus all fixed-layout customers are
at an exact NE, with equality allowed.

**Greedy load box survives list assignment.** After removing (F), all
sites (t\ne H) begin at (P_t=W_t^0\ge q_t\gamma); only (H)
may have normalized load below (\gamma). If it stayed below (\gamma)
throughout the assignment, every common customer would be sent to (H),
ending at (W_H^0/Q\ge\gamma), a contradiction. Hence (H) finishes
at least (\gamma), and never exceeds its original total (W_H^0),
so its box (Q\gamma\le W_H\le(Q+1)\gamma) holds.
Whenever another site (t) is chosen for a common customer of weight
(w), its current normalized load is at least (\gamma) and no larger
than (H)'s current load. The unassigned customer (w) was originally
in (H), so its current total there is at most (W_H^0-w). Thus

\[
 \gamma\le\frac{W_t}{q_t}
       \le\frac{W_H}{Q}
       \le\frac{W_H^0-w}{Q}
       \le\gamma+\frac{\gamma-w}{Q},
\]

which implies (w\le\gamma). Immediately after inserting it,

\[
 \frac{W_t+w}{q_t}
 \le\gamma+\frac{\gamma}{Q}
       +w\left(\frac1{q_t}-\frac1Q\right)
 \le\gamma+\frac{\gamma}{q_t},                    \tag{26}
\]

since (q_t\le Q). The lower box at (t) is permanent, while (H)
can only gain original common customers; (24)--(26) yield
(q_t\gamma\le W_t\le(q_t+1)\gamma) for all occupied sites at the end.
Rational sums, scaling for the constant-q scheduler, and tie comparisons
have polynomial bit length.

**All singleton-source and other facility deviations.** For (q_u\ge2),
the load box, (a=W_u/q_u\ge\gamma), and (N_r\le\gamma) give the
usual occupied-target and empty-target budgets (5)--(6). In a mixed
component satisfying (ii), a singleton source (u) cannot be (H)
because (Q\ge2). Its fixed private reserve is
(P_u=W_u^0\ge\gamma), and its final weight is
(a=P_u+w(F_u)), where (F_u\subseteq F) are common customers now at
(u). For every occupied target (v) **inside** the component,
exactly those (F_u) customers can follow the source. Using the box,

\[
 W_v+w(J_u\cap C_v)=W_v+w(F_u)
 \le(q_v+1)\gamma+a-P_u
 \le q_v\gamma+a\le(q_v+1)a.                      \tag{27}
\]

For occupied targets outside the component, the orphan overlap is zero
and the box suffices. For a singleton source in a constant-(q=1)
component, use the first-opening customer-pool proof (19R), unchanged
by its within-component Nashification. At an unopened target (r),
any singleton source needs only
(N_r+w(J_u\cap C_r)\le\gamma+a\le2a)
as the deviator's initial cap; every stationary-site packing follows
from (27) or the constant-q pool. As before, isolate atoms above (2a),
pack stationary facilities, and call MF-PURE-CAP-POLY for a pure exact
NE preserving the deviator's cap. A polynomial default rule completes
the continuation. The conditional theorem relies on the actual greedy
output and does not infer a polynomial algorithm for every instance.

**Strictly beyond the preceding two output certificates.** With (k=6),
sites H,B,C and customers
((140,\{H\}),(10,\{H,B,C\}),(80,\{B\}),(41,\{C\})),
greedy strictly selects
((H,150),(B,80),(H,75),(H,50),(C,41),(B,40)).
Final (q=(3,2,1)), (\gamma=40), and initial site totals are
((150,80,41)). The sole shared customer fails (17R):
(\beta_3-10/3=140/3>\alpha_2=40); the occupied overlap component
has three sites, so the pair theorem also does not apply. Private
normalized loads are (140/3,40,41); the list algorithm assigns the
weight-10 customer to B, giving ((W_H,W_B,W_C)=(140,90,41)).
Its external load at B is 40, below the alternative loads (140/3)
and 41. The source C is singleton, so (27) also covers a genuinely
present source-multiplicity type even though no common client ends at C.

## SC-K-NESTED-ANCHOR-GREEDY-2: a partial-overlap mixed component

**Exact conditional theorem.** Run SC-K-GREEDY-BUDGET on explicit positive
rational MF-MODEL input. In every occupied-site overlap component, assume either
all multiplicities are equal, or the following two conditions hold. Let H be
the first site opened in that component. Every customer with at least two
occupied options in the component can use H. Moreover, these multi-option
customers admit an ordering i_1,...,i_m with nonincreasing weights and

\[
 A_{i_1}\subseteq A_{i_2}\subseteq\cdots\subseteq A_{i_m},
 \qquad A_i=\{t:q_t>0,\ i\in C_t\}.                 \tag{28N}
\]

The order and inclusion condition are polynomially recognizable, including
equal-weight ties (sort equal-weight option sets by size, then check each
adjacent inclusion). Under these conditions the **greedy layout itself** has
an input-bit-polynomial site-uniform exact independently mixed customer NE
and a complete exact factor-two continuation. A component may have arbitrarily
many sites and unequal multiplicities. This strictly extends the all-or-one
component output class, but does not solve partial overlaps with incomparable
or reverse-weight option sets. The claim is conditional on the actual greedy
output, not on an arbitrary prescribed occupancy.

**Construction and exact NE.** In a mixed component write F for its
multi-option customers and P_t for customers with just occupied option t.
As H opens before the other component sites and covers all of F, all of F
were initially assigned to H, while each other site initially holds precisely
its P_t. SC-K-GREEDY-MAX-MULT gives Q=q_H>=q_t; in a genuinely mixed
component Q>=2. Keep each P_t fixed. Remove F from H and, in order (28N),
place each i on a site of minimum current W_t/q_t **among A_i**, breaking
ties by a fixed site order. For a resulting customer i at s, let j be the
last member of F placed at s. Then j is no heavier than i and A_i is
contained in A_j. At the moment j was placed, every v in A_i was therefore
an eligible comparison site. With final weights,

\[
 \frac{W_s-w_i}{q_s}
 \le\frac{W_s-w_j}{q_s}
 =\frac{W_s^{\text{before }j}}{q_s}
 \le\frac{W_v^{\text{before }j}}{q_v}
 \le\frac{W_v}{q_v}\quad(v\in A_i\setminus\{s\}).       \tag{29N}
\]

This is exactly i's conditional-cost comparison when i independently
mixes uniformly among the q_s colocated facilities. Single-option customers
have no alternative occupied site; different components cannot share a
customer. Constant-q components use the published restricted identical-link
Nashification, as in the previous theorem. Hence the combined profile is
an exact customer NE, with no strictness assumption on ties.

**The box and all deviations.** Let gamma>0 be the final greedy insertion
score. Initially q_t gamma<=W_t^0<=(q_t+1)gamma for every occupied t,
and P_t=W_t^0>=q_t gamma for t!=H. Every i in F can choose H.
Consequently, if H were still below normalized load gamma whenever an
F-customer was placed, each such customer would choose H, contrary to
W_H^0/Q>=gamma at the end. H therefore finishes at least gamma and at
most W_H^0/Q<=gamma+gamma/Q. Before a weight w is assigned to some
t!=H, H contains at most W_H^0-w, and the minimum-choice rule gives

\[
 gamma\le W_t/q_t\le W_H/Q
 \le (W_H^0-w)/Q\le gamma+(gamma-w)/Q.
\]

Thus w<=gamma. On inserting it, the new load at t is at most
gamma+(gamma-w)/Q+w/q_t<=gamma+gamma/q_t, since q_t<=Q.
The lower bound at every non-H site is permanent. Therefore **every**
final site obeys q_t gamma<=W_t<=(q_t+1)gamma. This box argument only
needs the common anchor H, not the nesting condition; nesting is needed
for (29N).

For a deviator with source multiplicity q_u>=2, the box, a=W_u/q_u>=gamma,
and N_r<=gamma restore the occupied and unopened packing budgets as in
SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2. For q_u=1 in a mixed component,
u!=H and its fixed private reserve P_u=W_u^0>=gamma. Its remaining
weight a consists of P_u plus some customers of F. For every other
occupied site v, only members of F now at u can both follow u and use v;
their total weight is at most a-P_u. Hence

\[
 W_v+w(J_u\cap C_v)
 \le(q_v+1)gamma+a-P_u
 \le q_v gamma+a\le(q_v+1)a.                 \tag{30N}
\]

For v in another component the overlap is zero. Singleton sources in a
constant-q=1 component use the already proved first-opening pool bound
(19R). For an unoccupied target r, assign the deviator no more than
N_r+w(J_u\cap C_r)<=gamma+a<=2a; the stationary-site budgets just
proved permit isolated-macro packing. MF-PURE-CAP-POLY then gives a pure
exact off-path NE with deviator load at most 2a. The polynomial default
rule supplies the rest of the complete continuation. All comparisons,
fraction clearing, scheduling calls, and at most k(|S|-1) deviations are
polynomial in explicit input bit length; no exponential customer-improvement
path is invoked.

**Strict separation and a limit of the list rule.** Let k=6, site order
H,M,L, private weights (135,H),(80,M),(41,L), and two other customers
(5,HM),(3,HML). Greedy strictly selects H,M,H,H,L,M, with
(q_H,q_M,q_L)=(3,2,1), initial weights (143,80,41), and gamma=40.
The weight-5 option set HM is properly contained in the weight-3 option
set HML. The construction assigns 5 to M and then 3 to L, giving final
weights (135,85,44); (29N) verifies the NE. The old range condition
(17R) fails for weight 5 because 143/3-5/3=46>80/2=40, and the
all-or-one condition fails at HM. Thus this is a genuine partial-overlap
case beyond both previously recorded certificates.

Switch **only the two shared option sets**, to (5,HML),(3,HM), retaining
the same greedy sequence and initial weights. The same unrestricted
descending minimum-load list places both customers at M, giving
(135,88,41); the weight-5 customer's source external load is
(88-5)/2=83/2>41 at L. It is not an NE even though the load box survives.
Placing 5 at L and 3 at M instead gives an exact site-uniform NE with
weights (135,83,46). This example refutes an unconditional star-anchor
**list algorithm**, not the greedy layout or the factor-two target.

## SC-K-GREEDY-SINGLETON-RESET and SC-K-GREEDY-BOX-TO-2

**Reusable singleton-deviation lemma.** Fix the greedy layout of a
positive-reach explicit rational MF-MODEL instance, with last insertion
score gamma>0. Take a facility at an occupied site u with q_u=1 and
**any** exact on-path independent-mixed customer NE in which its expected
load a is at least gamma. For each deviation by this facility there is
an input-bit-polynomially constructible exact **pure** off-path customer
NE giving it at most 2gamma<=2a. In fact the off-path construction does
not use the on-path customer assignment at all; only the scalar a>=gamma
is needed for the factor comparison.

Let K be all sites with greedy final multiplicity one, and P the clients
*initially assigned by greedy* to sites of K. SC-K-GREEDY-MAX-MULT says
every P customer's occupied options lie in K. If s is the first site
of K opened, every P customer was then uncovered. For each t in K,
greedy's comparison at that opening (including t=s), and the final
second-seat candidate at s, give

\[
 w(P\cap C_t)\le W_s^0\le2\gamma.                 \tag{30C}
\]

After u disappears, **reset every old customer to its initial greedy
site**, except customers of its original greedy set J_u^0, whose old
site has vanished. Send each of these to any surviving occupied site
covering it, if one exists; by MAX-MULT that site lies in K. If none
exists and the deviator has opened an unoccupied site r that covers it,
send it to the deviator. Otherwise it is unserved. All genuinely newly
served customers N_r at an unopened target also go to the deviator.
Every surviving higher-multiplicity site retains its original assigned
weight W_t^0<=(q_t+1)gamma and has q_t stationary facilities. Every
surviving t in K holds a subset of P cap C_t, of weight at most 2gamma;
put all of it on its one stationary facility. At an occupied target the
deviator starts empty, whether its target originally had q_t=1 or more.
At an unopened target, the original greedy singleton budget (8) yields

\[
  N_r+w(J_u^0\cap C_r)\le W_u^0\le2\gamma.      \tag{30D}
\]

Thus the deviator is ordinary under cap 2gamma. Apply MF-PACK-2 with
parameter gamma to the original W_t^0 at each stationary q_t>=2 site,
isolating any customer above 2gamma. Other stationary facilities already
have loads <=2gamma. MF-PURE-CAP-POLY reaches an exact pure customer NE
without increasing the deviator above 2gamma; its macro-isolation check
includes previously stranded customers and the actual post-deviation
coverage. This is polynomial in input bit length. The reset can send
customers to different sites from the chosen on-path NE: continuation
states are independently selectable at different labeled layouts.

**Box-completion corollary (SC-K-GREEDY-BOX-TO-2).** Suppose an explicit
site-pure/uniform-within-site exact on-path customer NE at the greedy
layout has

\[
             q_t\gamma\le W_t\le(q_t+1)\gamma
             \quad\text{at every occupied }t.          \tag{30B}
\]

Then its same labeled layout has an input-bit-polynomial complete exact
factor-two continuation. At q_u=1, a=W_u>=gamma and the preceding reset
lemma applies, **without any private-reserve or orphan budget for the
selected NE**. At q_u>=2 the source survives; a=W_u/q_u>=gamma, the
stationary budgets follow from W_t<=(q_t+1)gamma<=(q_t+1)a at every
other occupied site. At the surviving source itself, W_u=q_u a is
exactly the (h+1)a packing budget for h=q_u-1 stationary facilities;
an occupied target keeps its original q_t stationary bins and starts
the deviator empty. Every unopened site's newly covered weight
N_r<=gamma<=a starts on the deviator. MF-PACK-2 and
MF-PURE-CAP-POLY complete these deviations. A polynomial default pure
NE rule supplies the other labeled layouts. This separates the task of
**finding** a box-constrained exact on-path NE from the now-complete
off-path algorithm. It does not assert such an NE exists at every greedy
occupancy, nor a polynomial method to find one on arbitrary input.

## SC-K-UNIFORM-LIGHT-FLOW-2: partial overlaps without a common anchor

**Exact conditional theorem.** Run SC-K-GREEDY-BUDGET on any explicit positive
binary rational MF-MODEL instance, with arbitrary labeled k>=2 and positive
maximum reach. Let gamma>0 be its last score and A_i the customer's set
of occupied sites. Suppose all customers with |A_i|>=2 and w_i<gamma
have **one common weight** delta (when this set is nonempty, 0<delta<gamma).
Customers with |A_i|=1 may have arbitrary weights, and multi-option customers
with w_i>=gamma may have arbitrary weights. **No condition on singleton
private reserves is imposed.** Then the **same greedy layout** has an
input-bit-polynomial site-uniform independently mixed exact customer NE
and a complete exact factor-two continuation. Arbitrary occupied-site
partial overlaps and mixed multiplicities are permitted. This claim neither
solves the general mixed-light-weight case nor asserts that every NE at
the greedy occupancy is safe.

**Fixed customers and lower-constrained potential.** Freeze each customer
with one occupied option at that site, and each multi-option customer of
weight at least gamma at its greedy initial site. All other served customers
are the N weight-delta *variable* customers. Let P_t be frozen weight at t,
n_t^0 the variable count initially at t, and n_t its count in a candidate
assignment. The initial greedy box is

\[
 q_t\gamma\le W_t^0=P_t+\delta n_t^0\le(q_t+1)\gamma.
\]

Put \(\ell_t=\max\{0,\lceil(q_t\gamma-P_t)/\delta\rceil\}\). Minimize,
over assignments of variable customers to their own occupied option sets
with \(n_t\ge\ell_t\) at all sites, the separable potential divided by delta

\[
 F(n)=\sum_t\left(\frac{P_t n_t}{q_t}
       +\frac{\delta n_t(n_t-1)}{2q_t}\right).        \tag{31F}
\]

The greedy initial assignment makes these integer lower bounds feasible.
For completeness, a polynomial exact solver uses a unit-capacity edge from
the source to each variable customer, edges from that customer to each site
in A_i, and N unit site-to-sink slots at t, the jth with increasing cost
\(c_{tj}=(P_t+(j-1)\delta)/q_t\). Require the first \(\ell_t\) slots
at t to be filled. This is an integral minimum-cost flow with lower bounds
and O(N|S|+N) explicit edges.
One may avoid a lower-bound black box: set C=max_{t,j}c_{tj}, B=NC+1,
and subtract B from the first \(\ell_t\) slot costs. Since the initial
assignment fills all mandatory slots and every original full-flow cost is
between 0 and NC, an optimum of the rewarded network fills all of them.
Increasing original slot costs ensure that, given n_t customers at t,
the cheapest slots are precisely 1,...,n_t; thus the original cost is
(31F). Standard exact rational min-cost flow has polynomial input-bit
complexity (the source edges give N unit augmentations), and the output
is an integral client assignment. If N=0, retain the greedy assignment.

For a variable customer i at s, an alternative occupied v would strictly
improve its actual conditional cost exactly when

\[
          (W_s-\delta)/q_s>W_v/q_v.                  \tag{32F}
\]

If moving i leaves the lower constraints feasible, it decreases (31F)
by the exact potential difference, contradicting minimality. If the move
breaks the lower constraint at s, then \(W_s-\delta<q_s\gamma\), so
its left side is below gamma while \(W_v/q_v\ge\gamma\); (32F) is
impossible. Therefore every variable customer is at exact NE, without
requiring a bounded path of customer improvements.

**Upper box by a reverse transport path.** Draw one directed edge from
each variable customer's *initial* site to its final site, omitting
stationary loops. SC-K-GREEDY-MAX-MULT makes q nonincreasing along every
edge. If some final site t exceeded its greedy upper box, then
\(W_t>(q_t+1)\gamma\), hence \(n_t>n_t^0\). Flow decomposition of these
unit edges yields a simple directed path from a site s with
\(n_s<n_s^0\) to t; in particular \(q_s\ge q_t\). Along each edge of
the path return the corresponding customer from its final to its initial
site. Every move is allowed, intermediate site counts cancel, and only
s gains delta and t loses delta. The lower bound at t survives because
\(W_t-\delta>q_t\gamma+\gamma-\delta\ge q_t\gamma\);
all others are unchanged or increase. At s,
\(W_s\le W_s^0-\delta\le(q_s+1)\gamma-\delta\). Thus

\[
 \frac{W_s}{q_s}
 \le\gamma+\frac{\gamma-\delta}{q_s}
 \le\gamma+\frac{\gamma-\delta}{q_t}
 <\frac{W_t-\delta}{q_t}.                          \tag{33F}
\]

The return path strictly reduces (31F) by
\(W_s/q_s-(W_t-\delta)/q_t\), a contradiction. Hence all final sites
lie in \([q_t\gamma,(q_t+1)\gamma]\). Every frozen multi-option client
has w_i>=gamma, and its source external cost is at most
\(((q_s+1)\gamma-w_i)/q_s\le\gamma\), whereas every other occupied
site has load at least gamma. It therefore has no strict improvement.
The fixed one-option clients have no alternative occupied site. Uniform
independent choice within each assigned site is consequently a full
exact on-path customer NE.

**Off-path and bit complexity.** The full on-path box just proved meets
SC-K-GREEDY-BOX-TO-2, including its reset construction when a singleton
source disappears. Therefore every actual facility deviation admits an
input-bit-polynomial pure exact NE with deviator load at most twice its
on-path load. A polynomial default rule completes the continuation.
Rational denominator products,
the O(N) minimum-cost augmentations, the at most k(|S|-1) deviations,
and all calls to the published identical-link algorithm have polynomial
input bit length. The fixed-layout min-cost flow is **our reduction**;
the 2004 theorem is imported only for off-path exact Nashification.

**Strict new chain instance.** Take k=6, site order H,M,L, and clients
(140,H),(80,M),(41,L),(10,HM),(10,ML), with notation weight/options.
Greedy strictly selects H,M,H,H,M,L at scores
(150,90,75,50,45,41). The final counts are (3,2,1), gamma=41,
and initial totals (150,90,41). The two movable customers have common
weight delta=10. The minimum-cost
assignment puts HM at M and ML at L, giving totals (140,90,51).
Their source external loads are respectively 40 and 41, versus
alternative loads 140/3 and 45, so this is exact NE. The old range
certificate fails on the HM customer, since 150/3-10/3=140/3>90/2=45.
The overlap component is the H--M--L chain, so the all-or-one and
nested-anchor hypotheses fail; its singleton source is covered by the
general reset lemma. This finite instance separates the conditional
theorems, while the preceding argument proves the universal scope.

## SC-K-DESCENT-ONLY-TRAP-NO: three-site partial overlap needs an upward return

**Refuted selection assertion.** From the greedy initial customer assignment,
repeatedly make strict site-level customer improvements **only to sites of
weakly lower final facility multiplicity**. Every maximal such sequence
need not end at a full exact customer NE, even though every downward move
preserves the greedy load box. The following example makes the entire
downward path forced, so changing its order cannot repair the issue. This
does **not** refute the factor-two goal, the greedy occupancy, or the
all-or-one component theorem above.

Let (k=6), site order H,M,L, and take the six positive-integer customers

\[
 (64,H),\ (9,HM),\ (37,M),\ (5,ML),\ (2,ML),\ (20,L).    \tag{28}
\]

Greedy's strictly chosen site/score sequence is
((H,73),(M,44),(H,73/2),(H,73/3),(M,22),(L,20)).
There are no score ties. Final multiplicities are
((q_H,q_M,q_L)=(3,2,1)), last score (\gamma=20), and initial
weights ((73,44,20)). Name the shared clients Y=9 (H/M), Z=5
(M/L), and T=2 (M/L). At the initial state only T has a strict
downward improvement: its source external cost is
((44-2)/2=21>20), whereas Y has (64/3<22) and Z has
((44-5)/2=39/2<20). The subsequent path is forced:

| State weights ((W_H,W_M,W_L)) | Sole strict downward improvement |
| --- | --- |
| ((73,44,20)) | T: M\(\to\)L, (21>20) |
| ((73,42,22)) | Y: H\(\to\)M, (64/3>21); Z has (37/2<22) |
| ((64,51,22)) | Z: M\(\to\)L, (23>22) |
| ((64,46,27)) | None |

At the last state T is at L and has external cost (27-2=25),
whereas moving **upward** to M would cost its own weight plus M's
current per-facility load (46/2=23). It therefore strictly returns.
After T moves L\(\to\)M, the weights are ((64,48,25)), an exact NE:
Y at M has external cost (39/2<64/3), Z at L has external cost
20\(\le24\), and T at M has external cost 23\(\le25\);
the private customers have only their own site. The load box survives
even this particular upward return, but its preservation is not proved
for arbitrary upward moves. The graph is the three-site H--M--L chain:
no common customer covers all three, so it is correctly outside the
all-or-one subclass. A five-customer, four-facility star example with
clients ((40,H),(8,HA),(4,HB),(21,A),(19,B)) also defeats a
**fixed descending-weight one-pass** scan, but the six-customer example
is stronger because *every maximal downward-only order* has the same
upward-defective terminal state. Exact arithmetic and branch uniqueness
are checked independently in `tests/audits/kfac_descent_trap.py` from
`examples/multi_facility/greedy_descent_trap.json`; the displayed
inequalities prove the fixed-instance obstruction.

## SC-K-GREEDY-REPAIR-ORDER-NO: exact repair order can lose factor two

**Refuted assertion.** "Run greedy once and make *any* sequence of strict
site-level customer improvements to a site-uniform exact NE. Every terminal
NE of this kind admits a factor-two continuation at the fixed greedy layout."
The following positive-integer input refutes the universal quantifier over
strict improvement sequences. It does **not** say that every NE of the same
layout fails, or that the input lacks a factor-two witness elsewhere.

Take eight labeled facilities; the common site order is \(A,E,B,C,D,G\).
The ten atomic customers (weight, accessible sites) are
\[
 (80,A),(32,AB),(96,BEG),(81,B),(40,AC),
 (120,C),(52,BD),(268,D),(82,E),(80,G).             \tag{18}
\]
Greedy insertion is \((D,320),(B,209),(C,160),(D,160),
(D,320/3),(B,209/2),(E,82),(A,80)\), where each pair lists site and
chosen score. It leaves \((q_A,q_E,q_B,q_C,q_D,q_G)=(1,1,2,1,3,0)\),
site weights \((80,82,209,160,320,0)\), and \(\gamma=80\).

Now move weights \(32:B\to A\), \(40:C\to A\), \(52:D\to B\),
\(32:A\to B\), \(96:B\to E\). Each is a *strict* individual improvement;
the old and alternative conditional costs are respectively
\[
 (241/2,112),\quad(160,152),\quad(424/3,281/2),
 \quad(152,293/2),\quad(357/2,178).                 \tag{19}
\]
The final weights are \((120,178,165,120,268,0)\). This is an exact
site-uniform customer NE: the only clients with two occupied alternatives
have costs \(197/2\le152\) for the 32 client at B, \(178<357/2\) for the
96 client at E, \(120<160\) for the 40 client at A, and
\(217/2<424/3\) for the 52 client at B. The other clients have one
occupied site; within-site mixing is indifferent.

One B facility has on-path load \(a=165/2\). Move it to G; the other B
facility survives, and B, E, G now each have one facility. Private clients
of weights 81, 82, 80 are forced to B, E, G respectively. For the weight-96
client, the conditional cost of choosing G is **exactly** \(96+80=176\),
whereas B and E cost at least \(96+81=177\) and \(96+82=178\), regardless
of all other clients' independent mixing. It strictly chooses G in **every**
exact mixed NE of this deviation game. No other client has access to G.
The deviator therefore gets exactly \(176\) in every such NE, giving
\[
            \frac{176}{165/2}=\frac{32}{15}>2.     \tag{20}
\]
No off-path equilibrium selection can rescue this particular on-path NE.

The same greedy layout does have another good on-path NE: move only the
weight-40 client from C to A, a strict improvement, and stop. The loads
are \((120,82,209,120,320,0)\). The four shared clients (32,96,40,52)
respectively prefer B, B, A, D at conditional costs
\(241/2\le152\), \(305/2\le178\), \(120\le160\), and
\(424/3\le313/2\). The original four greedy transfer budgets also hold
for this exact NE (directly from the displayed weights and assignments),
so the existing packing and polynomial capped-completion argument gives
it a factor-two complete continuation. Thus the failure concerns **which
reachable NE is selected**, not greedy occupancy itself. The exact input
and independent arithmetic recheck are
`examples/multi_facility/greedy_repair_order_escape.json` and
`tests/audits/kfac_greedy_repair_order.py`. The script checks this finite
instance; it does not supply a polynomial way to choose the good NE on all
inputs.

**Even choosing the heaviest improving client first fails.** In (18), replace
only the weights 32 and 40 by 39 and 35. The same coverage, eight facilities
and site tie order give greedy insertion scores
\((D,320),(B,216),(D,160),(C,155),(B,108),(D,320/3),(E,82),(A,80)\).
The initial site weights are \((80,82,216,155,320,0)\) with the same
\(q=(1,1,2,1,3,0)\). At each step, select a strictly improving client of
**greatest weight** among all current alternatives. The unique greatest
choices, with old and new conditional costs, are
\[
 39:B\to A\ (255/2>119),\quad
 52:D\to B\ (424/3>281/2),\quad
 35:C\to A\ (155>154),\quad
 39:A\to B\ (154>307/2),\quad
 96:B\to E\ (182>178).                              \tag{21}
\]
The resulting exact on-path NE has weights \((115,178,172,120,268,0)\).
A B facility earns 86. Moving it to G again strictly forces the weight-96
client onto the deviator in **every** mixed NE, so its payoff is 176 and its
ratio is \(88/43>2\). This refutes that deterministic repair-order rule,
including its natural tie-free form. Moving just the weight-35 client
\(C\to A\) from the greedy initial state instead gives an exact NE with
weights \((115,82,216,120,320,0)\) and all four budgets. The exact variant
and audit are `examples/multi_facility/greedy_heaviest_escape.json` and
`tests/audits/kfac_greedy_heaviest.py`. It remains possible that a different
polynomial rule always selects a good NE or changes the greedy occupancy.

## SC-K-GREEDY-FIXED-LEXMAX-NO: the fixed-layout lexmax can select the bad NE

**Exact obstruction.** In the first integer instance (18), fix the greedy
occupancy (q=(1,1,2,1,3,0)) in site order (A,E,B,C,D,G). Consider **all**
feasible site-pure customer assignments, each customer uniform among the
facilities at its selected occupied site, and maximize their increasingly
sorted vector of (k) per-facility loads lexicographically. There is a
**unique customer site assignment** attaining this maximum. It is the bad
exact on-path NE in (19), and its (B\to G) deviation earns (32/15>2)
times the old load in **every** exact independent-mixed off-path NE. Thus
even an exact fixed-layout site-uniform lexmax oracle cannot serve as the
missing customer-selection rule for this greedy layout. This is not a
claim about all possible on-path independent-mixed profiles, other facility
layouts, or the globally lexmax selection in SC-K-2-E.

**Proof of uniqueness over every feasible assignment, not just NEs.** Only
weights (32) (A/B), (96) (B/E), (40) (A/C), and (52) (B/D) have two
occupied options. The others are forced, while the weight-80 G-only customer
is unserved. If 96 chooses B, E has load 82, so the minimum facility load is
at most 82. If 96 chooses E, then a minimum **strictly greater than 82**
forces 32 to B: otherwise B's total is at most (81+52=133), giving each
of its two facilities at most (133/2). It also forces 52 to B: otherwise
B's total is at most (81+32=113), giving at most (113/2). Finally, it
forces 40 to A, because otherwise the sole A facility has load 80. These
choices determine the only remaining assignment, with site totals
((120,178,165,120,268)) and sorted minimum (165/2>82). Therefore it
uniquely maximizes even the **first** sorted coordinate; no tie rule on the
later coordinates can rescue lexmax. Its exact on-path NE inequalities and
the forced (96+80=176) deviation load are proved immediately above.
The distinct good exact NE at this very occupancy has E load 82 and the
four transfer budgets. An independent 16-assignment Fraction enumeration
checks the finite uniqueness claim in
`tests/audits/kfac_greedy_repair_order.py`; the displayed inequalities are
the proof.

## SC-K-GREEDY-FIXED-POTENTIAL-NO: global customer-potential minimum can also be bad

**Exact obstruction.** A second positive-integer input has eight labeled
facilities, common site order (A,E,B,C,D,G), and ten customers

\[
 (200,A),(128,AB),(231,BEG),(240,B),(68,AC),
 (330,C),(60,BD),(740,D),(200,E),(199,G).             \tag{22}
\]

Greedy scores in order are
((D,800),(B,599),(D,400),(C,398),(B,599/2),(D,800/3),
(A,200),(E,200)), including the stated tie order. Final multiplicities
are (q=(1,1,2,1,3,0)), last score (\gamma=200), and initially
assigned weights are ((200,200,599,398,800,0)). Name the four shared
customers (X=128) (A/B), (Y=231) (B/E/G), (Z=68) (A/C), and
(T=60) (B/D). At this **fixed** layout there are exactly two site-pure,
within-site-uniform exact customer NEs:

| NE | ((X,Y,Z,T)) | ((W_A,W_E,W_B,W_C,W_D)) | customer potential |
| --- | --- | --- | ---: |
| good | ((B,B,A,D)) | ((268,200,599,330,800)) | 86264 |
| bad | ((B,E,A,B)) | ((268,431,428,330,740)) | 86200 |

**Completeness of the two-NE classification.** If (Y=E), its external
load there is 200, so a customer NE requires (W_B/2\ge200). If (X=A),
then (W_B\le240+60=300); if (T=D), then (W_B\le240+128=368).
Consequently (X=T=B). With (Z=C), its source external load is 330
but the A option has load 200, so (Z=A). This uniquely gives the bad NE.
If (Y=B,X=B), the same (Z=C) choice strictly prefers A, so (Z=A).
Then (T=B) has external cost (599/2>740/3), forcing (T=D), the
good NE. Finally, if (Y=B,X=A), choosing (Z=C) gives the strict move
(330>328=W_A). With (Z=A), X has external cost 268 but its B option
has load at most (531/2<268) (and only (471/2) if T is at D),
again a strict move. Thus no other assignment is a customer NE. Direct
source-external versus target-load comparisons for the two displayed NEs
are, respectively, X: (471/2\le268), (150\le268); Y:
(184\le200), (200\le214); Z: (200\le330) in both; and T:
(740/3\le599/2), (184\le740/3). There are no hidden equality
cases or other occupied choices.

For a fixed occupancy, define the exact *weighted improvement potential*

\[
  P(J)=\sum_{t:q_t>0}
   \frac{W_t^2-\sum_{i\in J_t}w_i^2}{2q_t}.              \tag{23}
\]

A transfer (i:s\to v) changes it by
(w_i[W_v/q_v-(W_s-w_i)/q_s]), exactly (w_i) times the change in
that customer's conditional cost. Hence **every global minimum** over
feasible site-pure assignments is an exact customer NE. The two exact
potential values in the table and the complete NE classification show
that the bad NE is the **unique global minimum**. This conclusion is an
analytic consequence of the transfer identity and classification; the
independent 16-assignment Fraction audit is a check.

At the bad NE, a B facility has (a=428/2=214). After it migrates to G,
B, E and G each have one facility and respectively have compulsory
private loads 240, 200 and 199. The Y customer strictly prefers G:
its cost there is (231+199=430), whereas its cost at E is at least
(231+200=431) and at B at least (231+240=471), irrespective of
the other customers' independent mixing. No other customer can use G.
Thus **every exact independent-mixed off-path NE** gives the deviator 430,
or (215/107>2) times its old load.

The good NE at the same occupancy satisfies the four original budgets:
each site is within (q_t\gamma\le W_t\le(q_t+1)\gamma), every
facility earns at least (\gamma), the only empty site G has
(N_G=199), and the sole nonzero singleton-source orphan term is
from A to C, where (W_C+w(Z)=330+68=398\le2W_A=536).
The old packing and capped completion therefore give a factor-two full
continuation there. This counterexample rejects **global minimization of
the fixed-layout site-uniform customer potential** as a general safe
selection rule. It also has a unique fixed-layout site-uniform lexmax bad
state: if Y stays at B, E has load 200; if Y moves to E, a minimum above
200 forces X,T at B and Z at A, yielding minimum 214. The claim does not
concern lexmax across different facility layouts or arbitrary on-path
independent-mixed profiles. The integer input and independent audit are in
`examples/multi_facility/greedy_potential_escape.json` and
`tests/audits/kfac_greedy_potential.py`.

## SC-K-TWO-LIGHT-LOWER-POTENTIAL-NO: lower-bounded potential can overflow with two weights

**Exact scope.** This is a counterexample to the proposed extension of
SC-K-UNIFORM-LIGHT-FLOW-2 that freezes heavy customers and minimizes the
weighted customer potential subject only to the *lower* greedy boxes. It
does not refute the existence of a box NE or a factor-two continuation.
The earlier SC-K-GREEDY-FIXED-POTENTIAL-NO already shows that unconstrained
global potential minimization can pick a bad NE, which there also meets the
lower boxes. The point here is the much smaller **two variable customers
of unequal weights** instance and an explicit infinite integer family isolating the
failure of the equal-unit reverse path.

For every integer n>=45 divisible by 5, take k=7, common site order
R,H,M,L, four private clients of weights

\[
 R:n,\qquad H:16n/5-1,\qquad M:2n,\qquad L:n+2,
\]

and two multi-option clients X of weight 4n/5 with options H,M, and Y of
weight n-1 with options M,L. These are positive integers; both variable
weights are strictly below n and are distinct. Greedy opens

\[
 H,M,H,M,H,L,R
\quad\text{at strictly maximal scores}\quad
 4n-1,\ 3n-1,\ (4n-1)/2,\ (3n-1)/2,\ (4n-1)/3,\ n+2,\ n.
\]

For example, after opening L the still available H and M addition
scores are (4n-1)/4<n and (3n-1)/3<n, so R wins the last step without a
tie. The final multiplicities are (q_H,q_M,q_L,q_R)=(3,2,1,1), and
gamma=n. The initial assignment X=H,Y=M has totals
(4n-1,3n-1,n+2,n), hence lies in every greedy box. It is already an
exact client NE: X's source external cost is (16n/5-1)/3, below the
alternative (3n-1)/2; Y's source external cost is n, below n+2.

There are exactly four site-pure assignments of the variable clients.
Every one satisfies the lower bounds q_t n: the smallest H total is
16n/5-1>=3n, the smallest M total 2n, and the private L and R totals
are at least n. Evaluate the exact weighted improvement potential (23)
at the four states, writing P_ab for X=a,Y=b. The pairwise differences
from P_ML are

\[
 P_{HM}-P_{ML}=(4n^2-170n+150)/75>0,\qquad
 P_{HL}-P_{ML}=4n(n-5)/75>0,\qquad
 P_{MM}-P_{ML}=(n-1)(2n/5-2)>0.
\]

Thus the lower-constrained potential has the **unique global minimum**
X=M,Y=L. At that state the totals are
(16n/5-1,14n/5,2n+1,n): L violates its upper box 2n by one unit.
This state is also an exact client NE: X's source external cost is n,
at most (16n/5-1)/3 at H; Y's source external cost is n+2, at most
(14n/5)/2 at M. The initial HM state is in fact the only assignment
inside *all* upper boxes: each other state sends Y to L, or sends both
X and Y to M (whose total is 19n/5-1>3n). In particular, a good
box-constrained NE is present on exactly the same greedy layout.

At n=45 the six weights are H:143, M:90, L:47, R:45, X:36, Y:44;
the potentials (P_HM,P_HL,P_MM,P_ML) are (3696,3784,4392,3688).
The two-edge initial-to-final transport H->M->L replaces an incoming
weight 36 by an outgoing weight 44 at M. Reversing the path cannot cancel
the intermediate load as it does in (33F) for equal weights; the displayed
potential inequalities show that the return raises, rather than lowers,
the objective. The finite Fraction audit in
`tests/audits/kfac_two_light_potential.py` independently checks the
strict greedy run, four assignments, NE conditions, and selected family
members from `examples/multi_facility/greedy_two_light_potential.json`.
The general family conclusion follows from the displayed algebra, not
from the finite audit. Whether some *other* polynomial selection always
finds a box NE for unequal light weights remains open.

## SC-K-STAR-LIGHT-GREEDY-2: unequal light weights on anchored star edges

**Conditional polynomial theorem.** Run the greedy construction on a
positive-reach explicit rational MF-MODEL instance and let gamma>0 be its
last insertion score. Form a graph on occupied sites: two sites share an
edge if some customer of weight **strictly less than gamma** can choose
both; ignore customers with only one occupied option. Suppose every
nontrivial connected component of this *light overlap graph* satisfies
one of the following independently checkable conditions:

1. all its sites have the same final facility multiplicity; or
2. it is a star with center H, H opened before every other site in this
   component, and every light multi-option customer in the component has
   **exactly two** occupied options, H and one leaf.

Different components can have different multiplicities. Heavy customers
of weight at least gamma may cover arbitrary occupied sites across these
components; they are frozen at their original greedy sites. Then a
site-pure/within-site-uniform exact on-path customer NE within every
greedy box, and a complete exact factor-two continuation, are computable
in input-bit-polynomial time. The star condition permits arbitrarily many
leaves and arbitrary unequal light weights on every edge. This is an
output-recognizable sufficient class, not a claim for arbitrary partial
overlaps or a proof that the general greedy occupancy has a box NE.

**Construction.** Freeze every customer with a single occupied option
and every customer of weight at least gamma at its original greedy site.
At equal-multiplicity light components, use the restricted identical-link
Nashification algorithm already imported for SC-K-LIGHT-COMPONENT-GREEDY-2;
the frozen customers have singleton restricted lists. It preserves the
initial minimum and maximum site loads and gives exact customer NE within
that component, hence preserves its box. Light components are independent
for movable customers.

In a star component let Q=q_H. Since H opens before its leaves, every
variable light customer was first served at H. By
SC-K-GREEDY-MAX-MULT, Q>=q_t for each leaf t with a variable customer.
At each leaf sort its variable customers in **nonincreasing weight**,
breaking ties arbitrarily. Keep current totals W. Repeatedly remove from
the head of each queue every customer i whose move H->t is not strictly
improving, i.e. for which

\[
                  (W_H-w_i)/Q\le W_t/q_t.              \tag{34S}
\]

Such a customer stays at H permanently. If any heads remain, choose
among their leaves one with smallest current normalized load
beta=W_t/q_t (fixed site-index ties), move that head to its leaf,
and repeat. Every customer is skipped or moved exactly once. A direct
scan of the queues takes O(N|S|+N log N) rational comparisons per
component after sorting; combined with the greedy construction and the
imported scheduler this is polynomial in the explicit input and bit
length. All intermediate loads are sums of input rationals.

**Box invariant.** The initial greedy assignment satisfies
q_s gamma<=W_s<=(q_s+1)gamma at each site. Every performed move has
(W_H-w_i)/Q>W_t/q_t>=gamma, so the center after the move stays above
Q gamma; the leaf lower bound only increases. The center upper bound
only decreases. Moreover no weight w_i>=gamma can satisfy this strict
inequality from a box state. For w_i<gamma, if the leaf upper bound
were exceeded after a move, then

\[
 \frac{W_t}{q_t}>\gamma+\frac{\gamma-w_i}{q_t}
 \ge\gamma+\frac{\gamma-w_i}{Q}
 \ge\frac{W_H-w_i}{Q},                                  \tag{35S}
\]

contrary to (34S). Thus every step preserves every box. A skipped
customer cannot become improving later: W_H only decreases and its
leaf's W_t only increases.

**Exact NE at termination.** Before choosing a move, all currently
nonimproving heads are skipped, revealing further heads until each
remaining head is improving. Let beta_1,beta_2,... be the normalized
leaf loads *before* successive moves, across the component. This
sequence is nondecreasing. A nonchosen leaf has unchanged beta and a
decreasing center can only remove an eligible head; the chosen leaf's
new beta is larger than its old beta, and its new head is revealed only
after this increase. Skipped heads never reenter. If there was a last
move j, its strict improvement leaves final W_H/Q>beta_last.

At any leaf t that received customers, let j be its last arrival, with
prearrival load beta_j. Earlier arriving customers i on that edge have
w_i>=w_j by the queue order. Hence their final external cost at t is

\[
       (W_t-w_i)/q_t\le (W_t-w_j)/q_t
          =\beta_j\le\beta_{last}<W_H/Q.                \tag{36S}
\]

So no moved customer wants to return to H. A skipped customer remains
at H and cannot improve by the monotonicity just proved. Customers
frozen for having one occupied option have no site deviation. For a
frozen multi-option customer with w_i>=gamma, the final box gives its
source external cost at most gamma, whereas every alternative site's
current normalized load is at least gamma. Components processed by the
same-multiplicity scheduler are independent of star transfers because
no *light* movable customer joins them; their equilibria remain valid.
Thus the complete site-uniform profile is an exact independent-mixed
customer NE. SC-K-GREEDY-BOX-TO-2 gives all polynomial off-path pure
NE choices and the complete factor-two continuation.

**Strict separation from prior sufficient classes.** Let k=6, sites
H,M,L, with private clients H:100, M:95, L:47 and shared clients
X:(36,HM), Y:(44,HL). Greedy strictly inserts
H,M,H,H,M,L at scores 180,95,90,60,95/2,47; q=(3,2,1), gamma=47.
Initially totals are (180,95,47). Y stays at H, while X moves H->M
because (180-36)/3=48>95/2; the terminal totals (144,131,47)
satisfy every box and all exact NE inequalities. The old RANGE check
fails for X, and the two unequal light weights prevent UNIFORM-LIGHT.
The HM and HL option sets are incomparable in inclusion order, so
NESTED-ANCHOR does not apply; each has only two of three sites, so
ALL-OR-ONE does not apply either. This is a separation of *sufficient
classes*, not evidence that those other algorithms fail on the input.
The exact input and independent finite arithmetic check are
`examples/multi_facility/greedy_star_edges.json` and
`tests/audits/kfac_star_edges.py`. The universal conclusion rests on
the proof above, not on that finite example. No canonical software
implementation of the general constructor or external review is claimed.

## Sources and review status

- Gairing, Lücking, Mavronicolas, Monien, STOC 2004, Section 4, especially
  Corollary 4.3 (both load extrema per blocking-flow call), the construction
  of the full algorithm, and Theorem 4.7 (exact NE and polynomial time):
  https://cgi.csc.liv.ac.uk/~gairing/publications/2004-stoc.pdf .
- 3-PARTITION is used only as a standard strongly NP-complete source problem.
  The reduction above is self-contained after that source fact.
- The heavy-client interface and lexmax profile family are the existing
  [uniform-two proof](uniform_two.md). The new deduction and reduction have
  been independently rechecked internally; external review and literature
  priority for this particular reduction are unrecorded.
- The distinct-site 2-bound, multiplicity-class range certificate,
  singleton-source pool argument and both repair-order counterexamples were
  independently reverse-reconstructed in this round. The two new scripts
  check exact fixed-instance arithmetic; they do not certify the universal
  conditional algorithms. The present conditional theorems and their
  novelty have not had external peer review, and no canonical software
  implementation of the imported scheduler or new constructors is claimed.
- The two-site mixed-multiplicity scan was independently rederived from the
  one-dimensional load difference, its box invariant and both singleton-source
  cases. The fixed-layout lexmax and potential-minimum obstructions were
  independently attacked by analytic assignment classification and exact
  Fraction enumeration. These are internal checks; no external peer review
  or complete literature-priority finding is recorded. In particular, the
  second example's global potential minimum follows from the transfer
  identity and complete NE classification, not from a finite search alone.
- The arbitrary-size all-or-one component construction was independently
  reversed through its last-assigned-job NE inequality, lower and upper
  greedy boxes, and the private-reserve singleton budget. Its three-site
  strict-range-failure example was recomputed with exact rational arithmetic.
  The partial-overlap downward trap has an exact unique path proof and an
  independent Fraction branch audit; it limits one repair rule only.

## SC-K-RESET-PACK-INTERFACE: reset-based off-path completion beyond the box

Fix the positive-reach greedy layout and its last score `gamma>0`. Write
`J_t^0` for its original customer pool at occupied site `t`, and `q_t` for
its facility multiplicity. Suppose we are supplied **an explicitly encoded exact on-path
independent-mixed customer NE**, whose individual facility payoffs satisfy
`a_f>=gamma`. For each site `u` with `q_u>=2`, also supply a partition of
`J_u^0` into `q_u-1` bins. Every bin either has total weight at most
`2gamma`, or consists of one isolated customer of weight above `2gamma`.
The latter is a macro bin and has no other customer. These are explicit,
polynomially checkable conditions. Under them the greedy layout admits an
input-bit-polynomial complete exact factor-two continuation.

For an actual deviation by `f` from a source `u` with `q_u>=2`, discard the
on-path assignment and reset every previously served customer to its original
greedy site. The source survives and its `q_u-1` stationary facilities take
the supplied bins. Every other occupied site `t` has all of its original
pool and `q_t` stationary facilities. Greedy gives
`W_t^0<= (q_t+1)gamma`; `MF-PACK-2` packs this pool into ordinary bins of
load at most `2gamma` and isolated macros. At an occupied target the moving
facility starts empty. At a newly opened target `r` only genuinely newly
covered customers join the mover, with total `N_r<=gamma`. Thus **all**
stationary ordinary loads and the mover start at most `2gamma`, and macros
remain isolated. `MF-PURE-CAP-POLY` returns an exact pure customer NE while
keeping the moving facility at most `2gamma<=2a_f`. Its client-restriction
and isolation checks apply to the actual deviated layout, including newly
served clients. For `q_u=1`, use `SC-K-GREEDY-SINGLETON-RESET`, which needs
only `a_f>=gamma` and likewise ignores the supplied on-path assignment.
Use the existing polynomial pure-NE default at every other labeled layout.
The partitions, reset, at most `k(|S|-1)` actual deviations, scheduling
calls, and rational comparisons have polynomial input-bit complexity. This
interface makes no claim that arbitrary inputs admit the required on-path
state or deletion partitions; a partition is checked, not found by an
unbounded bin-packing search.

## SC-K-DOUBLE-LPT-GREEDY-2: two checkable greedy-pool packings

There is a deterministic subclass test and constructor satisfying the
preceding interface. For each greedy pool `J_t^0`, sort clients by
nonincreasing weight (breaking ties by input index) and repeatedly place
the next client in a least-loaded one of its `q_t` co-located facilities.
Check that **every** resulting facility load is at least `gamma`. If any
check fails, this particular certificate returns *unknown*. Greedy already
gives `W_t^0<= (q_t+1)gamma`; hence each bin is at most `2gamma`, since
all its other `q_t-1` bins have at least `gamma` (also true for `q_t=1`).

Independently, for every `q_t>=2`, run the same deterministic descending
least-load rule on **the original pool again**, now with `q_t-1` bins.
Check that each deletion bin is at most `2gamma`. If all checks pass, apply
the published polynomial restricted-identical-link Nashification to the
first complete pure facility assignment. Each client is eligible for all
facilities at its covered sites; the algorithm returns an exact pure client
NE without lowering the initial **global minimum** facility load, so every
resulting `a_f>=gamma`. The final site totals need not satisfy a greedy
upper box. `SC-K-RESET-PACK-INTERFACE` supplies all actual deviations.
The LPT checks, published scheduler, and continuations are polynomial in
the explicit client, facility and rational input encoding. The use of LPT
is a sufficient certificate, not an assertion that LPT decides all feasible
partitions. This construction permits arbitrary occupied-option overlap
graphs and arbitrary unequal client weights.

**Strict separation from the box and light-path interfaces.** Let `k=8`,
sites `H,M,L`, private weights `H:110,110,110,60,54`, `M:140,100,80`,
`L:100`, and clients `X:(50,{H,M})`, `Y:(60,{M,L})`, `Z:(5,{H,L})`.
Greedy's strict scores are
`499,380,499/2,190,499/3,380/3,499/4,100`, so the final multiplicities
are `(4,3,1)` and `gamma=100`. The original pools total `(499,380,100)`.
One deterministic tie order gives first packings
`H:(160,115,110,114)`, `M:(140,100,140)`, `L:(100)`; deletion packings
are `H:(170,164,165)`, `M:(200,180)`. All checks pass. First move Z from
its H bin of 115 to L, then X from its H bin of 160 to the M bin of 100.
The facility loads become `H:(110,110,110,114)`, `M:(140,150,140)`,
`L:(105)`. Every client's exact facility NE inequality
holds, but M's site total is `430> (3+1)gamma=400`. Thus the double-LPT
certificate genuinely accepts an on-path equilibrium outside the box
required by `SC-K-GREEDY-BOX-TO-2`; it does not claim no alternative boxed
NE exists. The light-overlap graph is a triangle with three unequal edge
weights, so it is neither an anchored star nor a directed path; RANGE fails
for Y because `(380-60)/3>100`.

These are internally reconstructed conditional proofs; an exact example
audit verifies only the displayed finite instance. Neither the general
constructor nor its priority over the literature has external review.

## SC-K-PATH-EDGE-LIGHT-GREEDY-2: directed light paths

At the positive-reach greedy layout freeze every customer with one occupied
option and every customer of weight at least `gamma` at its original site.
Form the graph of the remaining multi-option light clients. Each nontrivial
component may have constant multiplicity (the existing restricted-identical
scheduler case), or satisfy: every light client has exactly two occupied
options; each edge is oriented from the endpoint greedy opened earlier to
the one opened later; each vertex has indegree and outdegree at most one;
and all clients on an edge have the same weight `delta_e<gamma`. Different
edges may have **different** weights. Thus such a component is a directed
opening-order path. These conditions are checkable in polynomial time.

Start from greedy's assignment. In a directed path, repeatedly choose an
unmoved light client at its original endpoint `u` with edge `u->v` whose
move is strictly improving:

`(W_u-delta_e)/q_u > W_v/q_v`.                         (P1)

Move the client once and stop when none remains. `SC-K-GREEDY-MAX-MULT`
gives `q_u>=q_v` on each edge, since the client was uncovered before `u`
opened and `v` opened later. Source lower box follows from (P1) and
`W_v/q_v>=gamma`. An upper-box overflow at v would give
`W_v>(q_v+1)gamma-delta_e`, and therefore
`W_v/q_v>gamma+(gamma-delta_e)/q_v >=
 gamma+(gamma-delta_e)/q_u >=(W_u-delta_e)/q_u`, a contradiction.
All other box directions are immediate.

After a move on edge `u->v`, every customer already moved on that edge has
source external cost `(W_v^new-delta_e)/q_v=W_v^old/q_v`, strictly less
than its alternative cost `W_u^new/q_u` by (P1). Between moves on that edge,
the preceding path edge can only add load to u and the succeeding edge can
only remove load from v. Later moves on the same edge restore the same
strict comparison simultaneously for all of its equal-weight customers.
Thus no moved customer ever wants to return. Every unmoved customer is
stable at termination; each client moves at most once. Frozen heavy clients
are stable from the boxes:
`(W_s-w_i)/q_s<=gamma<=W_t/q_t` for each alternative t.
Constant-q components use the already imported range-preserving scheduler.
We obtain a site-pure, uniform-within-site exact NE in the full greedy box;
`SC-K-GREEDY-BOX-TO-2` gives the complete factor-two continuation in
polynomial input-bit time. This is a conditional constructor, not a theorem
for arbitrary light overlap graphs.

For a strict four-site witness take `k=10`, private weights
`H:184,M:140,N:89,L:41` and clients `X:(14,{H,M})`,
`Y:(10,{M,N})`, `Z:(6,{N,L})`. Greedy strictly opens/adds
`H,M,H,N,M,H,M,H,N,L`, with scores
`198,150,99,95,75,66,50,99/2,95/2,41` and final
`q=(4,3,2,1)`, `gamma=41`. Only Z first improves `N->L`;
then Y improves `M->N`. Final site loads `(198,140,99,47)` are in
their boxes and form an exact customer NE. The unequal-weight P4 light
component lacks an anchored-star center and a common anchor; Z fails RANGE
because `89/2>41`. The [exact rational audit](../../../tests/audits/kfac_path_edges.py)
checks the instance, not the general theorem. Internal reverse review found
no remaining flaw; external review and literature priority are unrecorded.
