# Computing the arbitrary-k factor-two witness: two separated obligations

Version 1, 2026-10-02, with conditional construction and selection-rule
obstructions added 2026-10-03. The target is the **same** common-catalog, labeled-facility,
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
