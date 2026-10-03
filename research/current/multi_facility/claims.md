# Exact claim identities: common catalog, arbitrary k

Claims added on 2026-10-02 are version 1 of that date; the new two-site
component and fixed-layout selection claims are version 1 dated 2026-10-03.
Status fields are separate:
source = new current work; current proof = complete; internal review = reverse
reconstruction, separate internal proof attacks, and exact independent-implementation
checks; external review = not recorded; novelty = not certified. A passing computation
is not the reason for any universal quantifier below. The repository's current
claim ledger and [audit](../../K_FACILITY_AUDIT_2026-10-02.md) record the integrated scope.

## SC-K-2-E -- uniform factor-two existence

**Objects/domain:** MF-MODEL; any finite number of clients, positive real atomic
weights, nonempty finite common catalog, arbitrary integer k>=2, labeled
facilities with co-location, linear realized-load cost, compulsory service when
covered, independent customer randomization.

**Exact quantifiers and conclusion:** for every k and every instance I there
exist s in S^k and one complete exact-NE continuation sigma such that
L_f(sigma(s[f<-r]))<=2L_f(sigma(s)) for every label f and every catalog site
r!=s_f. The on-path NE is site-pure/uniform-within-site; all off-path NE can be
pure. This is an existence upper bound, not instance optimality, sharpness,
robustness to every NE selection, or a polynomial-time algorithm.

**Dependencies:** SC-K-LEX-BUDGET, MF-PACK-2, MF-PURE-CAP, MF-CONT-COMPLETE and
MF-MODEL. No dependency on any two-facility theorem or previous hardness delivery.
**Evidence/proof:** `uniform_two.md`, Sections 1-8; two exact audit scripts and
frozen outputs. **Objections:** all source/target multiplicities, stranded
clients, atomic self-load, off-path compatibility, and input representation are
addressed in `reverse_review.md`; no surviving fatal objection identified.
**Implementation:** exact exhaustive constructor and full-rule evaluator,
`multi_facility_spe/two_exists.py`; no polynomial iteration bound.

## SC-K-LEX-BUDGET -- on-path equilibrium and complete transfer budgets

**Objects:** any lexicographic maximum of the sorted increasingly ordered
facility-load vector over all feasible site-uniform profiles and all layouts
of an MF-MODEL instance with positive maximum reach. Each customer is assigned
to one occupied site J_t and independently uniform among its q_t facilities.

**Statement:** every such maximum is an exact customer NE and all facility loads
are positive. For every facility f at u, let a=W_u/q_u and let N_r be the weight
covered by r but unserved before the move. If q_u>=2, then for all other occupied
t, W_t<=(q_t+1)a, and for every unoccupied r, N_r<=a. If q_u=1 and J=J_u, replace
these by W_t+w(J cap C_t)<=(q_t+1)a and N_r+w(J cap C_r)<=a.

**Dependencies/proof:** MF-MODEL, finite lexicographic maximization; Sections 1-3
of `uniform_two.md`. **Review:** independently checks all ties rather than one
chosen maximum. **Limit:** removing common catalog access or the orphan terms
invalidates the proof. **Implementation:** exhaustive search; second checker
independently enumerates all labeled maxima and rechecks each budget.

## MF-PACK-2 -- positive weights, bounded bins or isolated macros

**Statement:** for every a>0, integer h>=1 and finite list of positive real
weights totaling at most (h+1)a, there is a partition into at most h bins, each
of weight <=2a or containing exactly one weight >2a. A repeated feasible-pair
merge constructs it with at most n-1 merges and O(n^3) elementary operations.

**Objects/assumptions:** clients stay separate atoms; no coverage constraints
inside this scalar lemma; empty list permitted. **Dependencies/proof:** direct
pairwise-sum contradiction, `uniform_two.md` Section 4. **Boundary/counterevidence
to strengthening:** h+1 weights equal to a disprove the same statement with
both cap and macro cutoff ca for every 1<=c<2. This is not global SPE sharpness.
**Implementation:** `merge_pack`, exact Fraction arithmetic; 267 finite cases.

## MF-PURE-CAP -- a full-game invariant for exact pure equilibration

**Statement:** for any fixed layout, B>0 and a feasible pure customer assignment
in which every served customer of weight >B is alone on its facility and every
other facility has load <=B, there exists an exact pure customer NE with the
same heavy clients still isolated and every other facility still of load <=B.
In particular any distinguished initially ordinary facility stays below B.

**Assumptions:** positive weights and linear actual-load cost. Other customers
are served exactly when covered; no resource is removed. **Dependencies/proof:**
the three strict-improvement inequalities and finite weighted squared-load
potential in `uniform_two.md` Section 6. **Limit:** tie moves need not preserve
the invariant; the process chooses only strict improvements. No polynomial
termination bound is proved. **Implementation:** `pure_improve`, with invariant
and potential assertions at every move.

## MF-CONT-COMPLETE -- compatible full continuation

**Statement:** for a fixed labeled on-path layout, any selected exact customer
NE there and one selected exact NE for every actual unilateral deviation extend
to one complete exact continuation, because all these labeled deviation layouts
are distinct and every other fixed-layout customer game has a pure NE.

**Dependencies/proof:** MF-MODEL, coordinate-wise distinctness, finite weighted
squared-load potential, `uniform_two.md` Section 7 and `model.md`. **Limit:** this
does not claim facility stability at every off-path first-stage layout; that is
not the definition. **Implementation:** `evaluate_continuation` interprets the
on-path probabilities and listed pure exceptions, then uses a deterministic
pure-improvement default at every other layout.

## MF-PURE-CAP-POLY -- polynomial capped customer equilibration

**Statement:** for an explicit rational fixed-layout pure assignment satisfying
the exact isolated-macro and ordinary-cap B hypotheses of MF-PURE-CAP, an exact
pure NE with the same isolated macros and ordinary loads <=B can be computed in
input-bit-polynomial time. The k(|S|-1) actual deviations in SC-K-2-E therefore
admit polynomial completion **once its on-path profile is supplied**.

**Dependencies:** MF-MODEL, the already proved macro isolation, and the
makespan-nonincreasing polynomial Nashification theorem of Gairing et al.
(STOC 2004, Section 4) for restricted identical links; multiply denominators
to handle rational weights. Full import check, reduction to ordinary resources,
and reinstatement of omitted options: [polytime frontier](polytime_frontier.md).
**Status/limit:** conditional algorithmic lemma, internally checked; imported
theorem is published, present interface is not externally reviewed and not
implemented here. It does not construct the on-path layout.

## SC-K-LEXMAX-STRONG-HARD -- exact global selection barrier

**Statement:** given explicit positive integer clients, k, and T, deciding
whether some feasible site-uniform profile has minimum facility load >=T
(equivalently, the existing globally lexmax profile has first coordinate >=T)
is strongly NP-complete, even for k=|S| with equal site reaches. This is a
property of the **selection oracle** in uniform_two.md, not hardness of
finding a factor-two SPE.

**Dependencies/proof:** 3-PARTITION with one private client of weight
P=mB+1 at each of m sites, and the 3m source items common to all sites.
Duplicate occupancy forces one facility below P; with all sites occupied,
average load P+B forces exact 3-partition. Full quantifiers and encoding:
[polytime frontier](polytime_frontier.md). **Status:** direct internal proof
awaiting external review and novelty check; no code or numerical inference.

## SC-K-LOCAL-PLS -- a polynomial neighborhood sufficient for factor two

**Statement:** on explicit rational MF-MODEL input, local maxima of a
polynomially enumerable neighborhood of site-uniform profiles have exact
customer NE and all four transfer budgets. A polynomial-bit radix encoding of
the sorted load vector and an easily computed all-colocated initial state put
this sufficient-state search in PLS. Applying MF-PACK-2 and
MF-PURE-CAP-POLY to any such locally maximal state computes all actual
deviation certificates in polynomial time.

**Dependencies/proof:** the exact same strict lexicographic improvements used
to prove SC-K-LEX-BUDGET, now only for n(m-1)+k(m-1) specified neighbors;
factorial scaling gives an integer radix objective. Full neighbor rules,
vanishing-source cases, zero-reach and bit bounds are in
[polytime frontier](polytime_frontier.md). **Status/limit:** internal direct
derivation, external review unrecorded; PLS membership does not imply
polynomial convergence and does not establish PLS hardness of the target.

## SC-K-GREEDY-BUDGET -- polynomial construction of transfer budgets

**Statement:** for any positive-reach explicit rational MF-MODEL instance,
iteratively choose the occupied site score W_t/(q_t+1) or unoccupied site's
current new-coverage score, assign newly covered customers on opening a site,
and repeat until k facilities have been inserted. The resulting feasible
site-uniform profile has positive loads and satisfies all four transfer
inequalities (5)--(8). It need not be a client NE.

**Proof/dependencies:** at the last insertion to each source site, every
other occupied or unoccupied site's then-score is at most its final a.
When the source multiplicity is one, its assigned customers were then
uncovered; the two disjoint inclusion arguments yield the disappearing-site
terms. Full proof and a three-site four-customer fixed-layout NE obstruction:
[polytime frontier](polytime_frontier.md). **Status:** internally checked direct
proof; no implementation, external review, or factor-two algorithm claimed.

## SC-K-GREEDY-MAX-MULT -- an initial incidence ordering

**Objects/domain:** any positive-reach common-catalog instance and the
initial site assignment output by SC-K-GREEDY-BUDGET; arbitrary k and
positive weights, any deterministic score tie rule. **Exact statement:**
each served customer is assigned to an occupied site with maximal *final*
facility multiplicity among all occupied sites it can use. **Proof:** a
later site t covering a customer first assigned at s had strictly smaller
opening weight W_t^0<W_s^0; if q_t>q_s, at t's last insertion the still
occupied s would have strictly larger next-insertion score, contradicting
greedy. [Full time-order argument](polytime_frontier.md).

**Scope:** the assertion concerns initial assignments, not arbitrary
customer NE reached after transfers; it does not control overloaded
stationary sites or imply a polynomial factor-two algorithm. Internally
checked as a direct invariant, external review and implementation not
recorded.

## SC-K-GREEDY-UNOPENED-2 -- an invariant after site-level customer repair

**Objects/domain:** the fixed occupancy output by SC-K-GREEDY-BUDGET for any
positive-reach common-catalog instance with positive rational weights and
arbitrary explicit k; customers remain independently uniform among the
facilities at their assigned site. Let gamma be the greedy last insertion
score. Quantify over every finite prefix of strict improving single-customer
site transfers starting from the greedy assignment, including any terminal NE.

**Exact statement:** every facility's load throughout these prefixes is at
least gamma; for each unoccupied site r, its newly coverable weight N_r is at
most gamma. Thus any facility of current load a departing for unoccupied r
has N_r<=a if its source survives, and N_r+w(J_u cap C_r)<=2a if it is the
source's sole occupant. Such a terminal exact on-path NE exists by finite
strict lexicographic ascent. This does **not** say that all NE at this layout
have these properties, or that the improvement path is bit-polynomial.

**Dependencies/evidence:** MF-MODEL and SC-K-GREEDY-BUDGET; the complete
sorted-load proof and the distinction from the stronger failed budget (8)
are in [polytime_frontier.md](polytime_frontier.md). Independently checked
algebraically; neither external review nor a software implementation is
recorded. **Remaining objection:** occupied stationary sites may lose the
packing budgets after these transfers, and the source's customers may require
new assignments when it disappears. No all-k polynomial factor-two
constructor follows from this lemma alone.

## SC-K-EQUAL-MULT-GREEDY-2 -- a conditional polynomial constructor

**Objects/domain:** positive-reach explicit rational common-catalog input
with arbitrary k; run the stated greedy procedure and require every occupied
site in its output to have the same multiplicity q>=2. This condition is
polynomially testable on the output, not an assumption that every instance
admits a suitable greedily selected layout.

**Exact statement:** on this subclass, an input-bit-polynomial algorithm
computes the greedy labeled layout, an exact independently mixed customer NE
uniform within each site, and an evaluable polynomial-size complete exact
continuation satisfying every unilateral facility deviation at factor 2.

**Dependencies/proof:** SC-K-GREEDY-BUDGET supplies gamma and the occupancy
budgets; the range-preserving restricted-identical-links Nashification in
Gairing et al. STOC 2004 (Corollary 4.3 and Theorem 4.7) produces a site-level
pure NE, which is an exact NE in this model only because every occupied site
has the same q. The retained interval q gamma <= W_t <= (q+1) gamma
restores (5)--(6) for each source. MF-PACK-2, MF-PURE-CAP-POLY and
MF-CONT-COMPLETE complete off-path certificates. Full [proof and import
audit](polytime_frontier.md); independent internal inverse check found no
fatal objection; no implementation, external review, or general-k all-input
claim. Unequal q and singleton sources are outside its scope.

## SC-K-DISTINCT-GREEDY-3 -- a conditional polynomial factor three

**Objects/domain:** the same input and greedy rule, conditional on all k
facilities occupying distinct sites. **Conclusion:** bit-polynomial exact
pure on-path customer NE and polynomial-time evaluable complete exact
continuation of factor at most 3. Nashification preserves initial site loads
in [gamma,2 gamma]; after each deviation a feasible pure assignment has
makespan at most a+2 gamma<=3a, and the same published theorem returns an
exact pure off-path NE without increasing that cap.

**Dependencies/evidence:** SC-K-GREEDY-BUDGET, range-preserving restricted
identical-link Nashification, MF-CONT-COMPLETE; direct proof in
[polytime_frontier.md](polytime_frontier.md), independent internal attack of
all source and target cases. This is not a factor-two algorithm, and no
implementation or external review is recorded. A load-only summary of the
initial interval and unopened coverage may require a ratio arbitrarily near
3 at a non-greedy fixed layout. This true but weaker claim is superseded
on its exact output class by SC-K-DISTINCT-GREEDY-2 below.

## SC-K-DISTINCT-GREEDY-2 -- full factor two on distinct-site output

**Objects/domain:** explicit positive rational MF-MODEL input, arbitrary
integer k>=2, conditional on the fixed greedy run putting all k labeled
facilities at distinct physical sites. No limitation on customer overlap.

**Exact statement:** construct in input-bit-polynomial time the same greedy
layout, an exact pure on-path customer NE, and a polynomial-time evaluable
complete exact continuation under which every unilateral facility deviation
has payoff at most twice its on-path payoff. In fact the deviation inequality
holds under *any* exact off-path NE once the specified on-path NE is selected.

**Proof/dependencies:** the first greedy site has maximum reach R and stays
single under the output condition. Its additional-facility candidate score
R/2 persists at every later insertion, so gamma>=R/2. Gairing et al.'s
restricted identical-link Nashification preserves the minimum initial
facility load gamma, and all distinct-site facility loads are thus >=R/2.
Every facility deviating to r can receive at most the full reach
w(C_r)<=R under any customer continuation. Complete [proof](polytime_frontier.md),
independently reverse-checked against labels, zero reach and all mixed
off-path strategies. Published customer algorithm is an imported theorem;
this deduction is an internally reviewed conditional theorem, not the
general all-input factor-two algorithm. External review and software
implementation are unrecorded.

## SC-K-COMPONENT-MULT-GREEDY-2 -- a wider conditional factor two

**Objects/domain:** arbitrary explicit positive rational common-catalog
instance with positive reach, after the fixed greedy rule. In the graph of
occupied sites joined when a customer covers both, require every connected
component to have constant facility multiplicity; any component with
multiplicity one must consist of one site. This condition is polynomially
testable on the greedy output and includes distinct components of different
facility counts.

**Exact statement:** a bit-polynomial exact on-path independent-mixed
customer NE and polynomial-size, polynomial-time evaluable complete exact
factor-two continuation exist and can be constructed. Components with
q>=2 are Nashified independently by published range-preserving identical-
link scheduling; q=1 singleton components remain unchanged. The global
greedy last score bounds each site's total in [q_t gamma,(q_t+1) gamma].
All q>=2 sources retain (5)--(6); singleton q=1 sources retain unchanged
J_u and (8), and their other occupied-site overlaps are zero in (7).

**Dependencies/proof:** SC-K-GREEDY-BUDGET, Corollary 4.3 and Theorem 4.7
of Gairing et al. for each component, MF-PACK-2, MF-PURE-CAP-POLY and
MF-CONT-COMPLETE. [Complete argument](polytime_frontier.md) independently
inverse-checked; no implementation or external review. This is a wider
conditional theorem than SC-K-EQUAL-MULT-GREEDY-2, not an all-input result:
mixed multiplicities in one customer-overlap component and multi-site
q=1 components remain outside its scope.

## SC-K-GREEDY-STATIC-PACK-NO -- fixed-site packing fails after repair

**Exact scope:** one positive-integer common-catalog instance with five
sites, eight labeled facilities, nine atomic customers, and the stated
increasing-site tie rule. At the greedy layout there is a five-move strictly
improving customer site-transfer sequence reaching a site-uniform exact NE.
For either of two facilities at B, source B survives its deviation, yet if
one freezes the current site assignments outside the source, stationary
site E cannot meet the isolated-macro-or-cap-2a hypothesis of MF-PACK-2:
its one facility has two clients of weights 20,24 totaling 44>2a=41.

**Evidence/proof:** the complete greedy score sequence, five exact cost
comparisons, final NE comparisons and failed bin condition appear in
[polytime_frontier.md](polytime_frontier.md); independently recomputed with
exact fractions, with no inference from finite search to a universal claim.
**Limit:** this refutes only a frozen-site off-path *proof interface* for
one reachable NE. Cross-site reassignment (the 24 customer can return to B),
another on-path NE or another layout may still give a 2-SPE. No lower bound
on the instance optimum or algorithmic hardness is claimed.

## SC-K-GREEDY-CAP-INFEASIBLE -- global cap repair can be infeasible

**Exact scope:** six-site positive-integer common-catalog instance with
eight facilities and ten customers, obtained by adding an unopened G site,
one G-private customer and one new coverage edge to the preceding example.
The same greedy order and five strict customer improvements give an exact
on-path NE. At the B-to-G deviation, the deviator's on-path load is
41/2, and **no** feasible pure customer assignment satisfies the global
MF-PURE-CAP-POLY hypothesis for B=41, even after arbitrary cross-site
reassignment: private 20 customers force loads at B,E,G and shared 24
must join one of them, producing 44 with no isolated >41 client.

**Counterevidence to overreading:** the very same deviation layout has a
pure exact customer NE with deviator load 20, explicitly checked in
[polytime_frontier.md](polytime_frontier.md). Therefore this disproves
one proposed *global cap interface*, not the factor-two facility
certificate, a different on-path NE, or a full-input polynomial algorithm.
All exact greedy, strict-improvement and NE comparisons are in the proof;
independent fraction arithmetic in
`tests/audits/kfac_greedy_cap.py` confirms them from
`examples/multi_facility/greedy_cap_obstruction.json`. External review
unrecorded.

## SC-K-RANGE-GREEDY-2 -- multiplicity-class range certificate

**Objects/domain:** explicit positive binary rational MF-MODEL input,
arbitrary k>=2, positive maximum reach, and the fixed polynomial greedy
layout and initial assignments. For every final occupied multiplicity q,
define alpha_q and beta_q as the minimum and maximum *initial* per-facility
site loads of sites with this q. Each initially assigned customer i at a
site of multiplicity q_i must satisfy beta_q_i-w_i/q_i<=alpha_q_v for
every covered occupied site v of different multiplicity q_v. This is a
polynomially checkable condition, not an assertion that all inputs satisfy
it. The unchanged model has independent mixed exact client NE and complete
existential continuation.

**Exact conclusion:** an input-bit-polynomial procedure computes the
greedy layout, an exact site-uniform customer NE and a polynomial-size,
polynomial-time evaluable complete exact factor-two continuation. The
condition permits customers lighter than the final greedy score to cross
multiplicity classes; light-graph and all-distinct conditions are sufficient
special cases. No general-input constructor is claimed.

**Proof:** partition the initially assigned clients and occupied sites by
their source multiplicity q. In each q group, let **every** client choose
any of its accessible sites *within that same group*, and apply the
published range-preserving restricted identical-machine Nashification.
The machine NE is the original customer no-improvement comparison within
the group. Its retained range bounds every cross-group client's source
external load by beta_q-w_i/q and target load below by alpha_q_v; the
certificate inequality blocks all omitted choices. The original greedy
box q gamma<=W_t<=(q+1)gamma survives. For q>=2 departures it restores
budgets (5)--(6). For q=1 let P be all customers initially assigned to
singleton sites K. SC-K-GREEDY-MAX-MULT confines their occupied options
to K; when the first K site opened, the entire P pool was uncovered,
giving w(P cap C_t)<=2gamma for each t in K. The q-group repair preserves
P, so for singleton source u and singleton target t,
W_t+w(J_u cap C_t)<=2gamma<=2a; against q>=2 targets the overlap is zero.
For an unopened target the deviator starts with at most N_r+a<=2a,
while stationary sites are packed from the former inequality. MF-PACK-2,
MF-PURE-CAP-POLY and MF-CONT-COMPLETE finish every deviation. Full proof,
exact encoding and a strict-subclass example in
[polytime_frontier.md](polytime_frontier.md).

**Status/objections:** direct internal proof independently reverse-audited,
including the source-site-disappearance case and the requirement that
cross-group customers retain *all* same-group choices. Published
Nashification is an import; this deduction is not externally reviewed or
implemented as canonical software. The remaining mixed-multiplicity inputs
failing the certificate are genuinely outside its proved scope.

## SC-K-GREEDY-HEAVY-OVERLAP-2 -- mixed-multiplicity polynomial subclass

**Objects/domain:** explicit positive rational MF-MODEL input, arbitrary
integer k>=2, positive maximum reach, the fixed polynomial greedy rule with
final insertion score gamma>0. Every client that covers two or more of the
greedy occupied sites has weight at least gamma; clients having only one
occupied option have no additional restriction.

**Exact statement:** the *unmodified* greedy site-uniform assignment is an
exact independent-mixed customer NE. Its layout, on-path NE, and a
polynomial-size evaluable complete exact continuation satisfying every
labeled unilateral deviation at factor 2 are input-bit-polynomially
constructible. This allows unequal multiplicities in one overlap component,
unlike SC-K-COMPONENT-MULT-GREEDY-2; it is conditional on a polynomially
testable property of the greedy output, not a universal constructor.

**Dependencies/evidence:** SC-K-GREEDY-BUDGET provides q_t gamma<=W_t<=
(q_t+1)gamma and all four budgets. For a shared client of weight at least
gamma, its conditional external load at its assigned site is at most gamma,
whereas any alternative site's current load is at least gamma. MF-PACK-2,
MF-PURE-CAP-POLY and MF-CONT-COMPLETE give polynomial completion. Complete
proof and a mixed-q example: [polytime_frontier.md](polytime_frontier.md).
Direct algebra independently reversed; external review and software
implementation are unrecorded. Equality at gamma is allowed.

## SC-K-LIGHT-COMPONENT-GREEDY-2 -- light-overlap conditional constructor

**Objects/domain:** arbitrary integer k>=2, common finite catalog and
positive binary rational atomic weights in MF-MODEL, positive maximum
reach, and the polynomial greedy output with final score gamma>0. Join
occupied sites only when a customer of weight *strictly less than gamma*
covers both. Each resulting graph component must have constant facility
multiplicity. A multiplicity-one component may contain arbitrarily many
sites and light clients.

**Exact statement:** in input-bit-polynomial time construct an exact
independent-mixed site-uniform on-path customer NE and one complete exact
factor-two continuation for the greedy labeled layout. Fixed heavy clients
may cross multiplicity classes; light customers can really move within
equal-q components. The hypothesis is recognized from the deterministic
greedy output; it is not a theorem for all input instances.

**Proof/dependencies:** SC-K-GREEDY-BUDGET gives the initial box
q_t gamma<=W_t<=(q_t+1)gamma. Restrict each weight>=gamma customer to
its initial site, and use the published range-preserving identical-link
Nashification within each equal-q light component. The returned light
client machine NE is the exact original site-choice condition; a heavy
client cannot improve because its source other-client load is <=gamma and
every alternative site load is >=gamma. For q>=2, the box restores (5)--(6).
For q=1, put all originally assigned singleton-site clients into one pool
P. SC-K-GREEDY-MAX-MULT confines every member's occupied options to
singleton sites. At the first singleton opening, every member of P was
uncovered, so for each singleton site t the total weight of P covering
t is at most the first site's opening weight, itself at most 2 gamma.
Repair stays within multiplicity classes; hence for a singleton source u
and singleton target t, W_t+w(J_u cap C_t)<=2 gamma<=2a, retaining
budget (7). Against q>=2 targets the overlap is zero and the box proves
(7). For an unopened target, replace original (8) by
N_r+w(J_u cap C_r)<=gamma+a<=2a: stationary sites can still be packed,
and the deviator starts as an ordinary <=2a facility. MF-PACK-2,
MF-PURE-CAP-POLY and MF-CONT-COMPLETE construct all exact off-path
witnesses. Full proof,
encoding and a five-customer instance outside both previous subclasses:
[polytime_frontier.md](polytime_frontier.md).

**Status and limits:** complete direct internal proof with independent
adversarial reconstruction; imported 2004
Nashification is published, this deduction has no external review,
novelty certification or canonical implementation. Mixed-q overlap through
light customers remains outside this criterion; all-distinct greedy output
is included and also has an independent reach-based factor-two proof.

## SC-K-TWO-SITE-COMPONENT-GREEDY-2 -- polynomial mixed-multiplicity pair repair

**Objects/domain and quantifiers:** explicit positive rational MF-MODEL,
arbitrary labeled (k\ge2), positive maximum reach, and the occupancy of
SC-K-GREEDY-BUDGET. In its graph joining occupied sites with a common
reachable client, every component must either have constant multiplicity or
at most two sites. The condition is decidable in polynomial time after
greedy; it is not a claim that every instance has such an output.

**Conclusion:** a deterministic input-bit-polynomial construction gives the
same greedy facility layout, site-uniform independent-mixed exact on-path
client NE, and a polynomial-size, polynomial-time evaluable complete exact
continuation with every single-facility gain at most two. For an unequal
two-site component (Q>q), sort shared clients by decreasing weight and
transfer from the (Q)-site to the (q)-site iff strictly improving; a
single pass is exact NE and preserves the greedy load box. Constant-q
components use published identical-link Nashification. A singleton source
in a mixed pair satisfies the orphan budget by the identity
(W_H+w(J_L\cap C_H)=W_H^0); singleton sources in constant-q components
use the initial client-pool bound. All empty-target deviators start at
load at most (2a), and MF-PURE-CAP-POLY closes the off-path games.

**Dependencies/evidence:** SC-K-GREEDY-BUDGET, SC-K-GREEDY-MAX-MULT,
MF-PACK-2, MF-PURE-CAP-POLY, MF-CONT-COMPLETE and the exact descending-scan
and load-box proof in [polytime_frontier.md](polytime_frontier.md). The
three-customer ((9,A),(1,AB),(4,B)) input fails (17R) but satisfies
this claim, so the output class is strictly wider in that direction.
The proof is internally reconstructed and exact arithmetic checked;
external review, literature priority and canonical implementation are
unrecorded. Larger mixed-multiplicity components and the full-input
polynomial factor-two target remain open; neither a finite instance nor a
published scheduler alone proves this new conditional theorem.

## SC-K-GREEDY-FIXED-LEXMAX-NO -- fixed-layout lexmax can be the unique bad NE

**Exact objects/domain:** the eight-facility, six-site, ten-positive-integer
client instance of SC-K-GREEDY-REPAIR-ORDER-NO and its specific greedy
occupancy. Maximize the increasingly sorted per-facility load vector over
**all site-pure, within-site-uniform customer assignments at this fixed
occupancy**, whether client NEs or not.

**Conclusion and proof:** the unique maximizer is the bad exact on-path NE
with site totals ((120,178,165,120,268)) and minimum load (165/2).
If the shared weight 96 stays at B, E gives minimum at most 82. If it
goes to E, minimum above 82 forces weight 32 at B, weight 52 at B and
weight 40 at A, uniquely determining this assignment. A B facility then
gets 176 from B-to-G in every exact independent-mixed off-path NE,
gain (32/15>2). At the same greedy occupancy another exact on-path NE
retains a complete factor-two continuation.

**Evidence/scope:** the full inequality proof in
[polytime_frontier.md](polytime_frontier.md), the fixed integer input and
16-assignment independent Fraction enumeration in
`tests/audits/kfac_greedy_repair_order.py`. This rejects **only** the
fixed-greedy-layout site-uniform lexmax selection rule; it says nothing
about other layouts, all on-path independent-mixed profiles, or the global
lexmax used in the existence theorem. Internally audited fixed-instance
counterexample; external review not recorded.

## SC-K-GREEDY-FIXED-POTENTIAL-NO -- global site-uniform potential can prefer the bad NE

**Exact objects/domain:** eight labeled facilities, six common sites and
the ten positive integer customers in (22) of
[polytime_frontier.md](polytime_frontier.md). Greedy has the specified site
tie order and occupancy ((1,1,2,1,3,0)). Only **site-pure customer
assignments, independent uniform within the chosen site**, are candidates
in the fixed-layout global potential minimization. This is a different
selection claim from SC-K-GREEDY-FIXED-LEXMAX-NO, even though this new
input also has a unique bad fixed-layout lexmax.

**Exact statement and proof:** the customer potential
(P=\sum_t(W_t^2-\sum_{i\in J_t}w_i^2)/(2q_t)) changes under (s\to v)
by (w_i[W_v/q_v-(W_s-w_i)/q_s]). Global minima are therefore exact
customer NEs. Algebraic case analysis leaves exactly two site-uniform NEs,
with potential 86264 for the good one and 86200 for the bad one. Thus the
bad NE is the unique global potential minimum. In it, a B facility earns
214 and moving to G earns 430 in **every** exact independent-mixed
off-path NE, gain (215/107>2), because the 231 client strictly prefers
private-base 199 at G to 200 at E or 240 at B. At the same occupancy
the other customer NE retains all four sufficient transfer budgets.

**Dependencies/evidence/limits:** MF-MODEL, SC-K-GREEDY-BUDGET, the exact
transfer potential identity and exhaustive analytic two-NE classification
in [polytime_frontier.md](polytime_frontier.md). The raw integer input is
`examples/multi_facility/greedy_potential_escape.json`, independently
enumerated with Fraction arithmetic in `tests/audits/kfac_greedy_potential.py`.
This is a fixed-layout selection-rule counterexample, not a failure of
the greedy layout, global lexmax over layouts, or full-input factor-two
existence. It is internally reviewed; external review is unrecorded.

## SC-K-GREEDY-REPAIR-ORDER-NO -- a reachable bad exact NE

**Exact scope:** eight labeled facilities, six common sites, ten positive
integer customers, and the displayed greedy tie order. A specified five-step
strict site-level customer-improvement path from the greedy initial assignment
ends in a genuine site-uniform exact customer NE. At this particular on-path
NE, a B facility with payoff 165/2 moving to G gets payoff 176 in **every**
independent-mixed off-path customer NE, giving ratio 32/15>2. The G-private
80 and B/E-private 81/82 force the shared 96 client strictly to G.

**Dependency/evidence:** [full arithmetic and proof](polytime_frontier.md),
`examples/multi_facility/greedy_repair_order_escape.json` and independent
`tests/audits/kfac_greedy_repair_order.py`. A *different* single strict
improvement at the same greedy layout already reaches another exact on-path
NE with all four original transfer budgets, hence with a factor-two complete
continuation. The counterexample refutes **every terminal NE reached by any
strict-repair order is safe**; it neither refutes existence of a good NE at
greedy occupancy nor a general factor-two algorithm. Finite exact arithmetic
checks the fixed witness but does not prove a universal bound. Internal
independent inverse check completed; external review unrecorded.

## SC-K-GREEDY-HEAVIEST-NO -- largest-weight strict repair is unsafe

**Exact scope:** the ten-customer instance in
`examples/multi_facility/greedy_heaviest_escape.json`, with eight labeled
facilities, six common sites and the displayed site tie order. Greedy outputs
multiplicities (1,1,2,1,3,0). From its initial assignment, repeatedly choosing
the *largest-weight* client with a strict cross-site improvement (with no
largest-weight ties) leads through the five specified moves to an exact
site-uniform customer NE of site weights (115,178,172,120,268,0). A B
facility has payoff 86 but moving to G yields 176 in every off-path
independent-mixed exact NE, ratio 88/43>2. The private B/E/G clients force
the shared 96 client to G. Another one-step reachable exact NE at the same
layout retains all four sufficient budgets.

**Proof/evidence:** exact moves and universal mixed-NE forcing argument in
[polytime_frontier.md](polytime_frontier.md); independent arithmetic,
max-weight selection at *every* step and good-NE budget comparison in
`tests/audits/kfac_greedy_heaviest.py`. Status: fixed-instance counterexample
internally audited; no conclusion about the existence of some suitable NE
at the greedy layout, the unrestricted polynomial algorithm, or global
factor-two existence. External review unrecorded.

## SC-K-SYMMETRIC-MENU-OBSTRUCTION -- bad menus are not lower bounds

**Statement:** for every integer q>=3, the explicit three-site/three-client
instance with k=q+1, weights (q^2,1,q-1/4), and client site sets ({A,T},{A},{B})
has a site-uniform lexicographic-maximizing on-path NE with q facilities at A
and one at B. At the deviation B->T EVERY co-location-symmetric exact NE gives
the deviator q^2, an improvement ratio q^2/(q-1/4)>k-1. Nevertheless the SAME
on-path state extends to an exact SPE using pure asymmetric off-path NE with
zero deviator load at every actual deviation; alpha^*(I,k)=1.

**Dependencies/proof:** MF-MODEL and MF-CONT-COMPLETE; complete scalable proof in
`symmetric_menu_obstruction.md`. **Input:** three explicit positive rational
atoms, or integer weights (4q^2,4,4q-1), common three-site catalog and k explicit
labels. **Limit:** excludes one proposed continuation restriction for the given
on-path lexmax, not every possible layout under every symmetric rule.
**Implementation/evidence:** `tests/multi_facility/run_reverse_audit.py`, seven values through
k=64 and all 274 corresponding actual deviations. These finite checks are not
the scalable proof.

## SC-K-LEXMAX-BARRIER -- exact boundary of the selected facility layout

**Statement:** for every integer k>=2 and h>=2, the explicit k-site, k-client
common-catalog family with weights h,1,3(h+1)/4,...,3(h+1)/4 and cover sets
{A,T},{A},{Z_2},...,{Z_(k-1)} has a unique site-uniform lexmax occupancy, up to
labels: two facilities at A and one at each anchor. The optimal factor at
ANY such occupancy, permitting ALL on-path and off-path exact independent
mixed NE, is exactly 2h/(h+1). The full instance nevertheless has alpha^*=1,
attained with one facility at T, one at A, and one at each anchor.

**Objects/encoding:** explicit k labeled facilities, k positive rational atoms,
common k-site catalog; scaling by 4 gives strictly positive integers.
**Dependencies/proof:** MF-MODEL, MF-CONT-COMPLETE and the explicit family;
`lexmax_boundary.md`. No two-facility lower theorem is imported. **Scope/limit:**
for every fixed k, the same global lexmax layout rule cannot establish any
universal factor below 2 by changing only customer equilibria. This is NOT a
global factor-two lower bound; the instances are exactly stable elsewhere.
**Review/evidence:** a low A facility has unavoidable gain h because e forces
H strictly to T in every deviation NE; all remaining deviations are explicitly
completed. Twenty parameter pairs, 1552 actual deviation witnesses and six
independent labeled lexmax enumerations are checked by
`tests/multi_facility/run_lexmax_barrier_audit.py`. General quantifiers are proved
algebraically, not by these tests. External review and priority unverified.
