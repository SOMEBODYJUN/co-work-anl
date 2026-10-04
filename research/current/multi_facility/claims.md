# Exact claim identities: common catalog, arbitrary k

Claims added on 2026-10-02 are version 1 of that date; the new two-site,
all-or-one component and fixed-layout/repair obstruction claims are version 1
dated 2026-10-03.
Status fields are separate:
source = new current work; current proof = complete; internal review = reverse
reconstruction, separate internal proof attacks, and exact independent-implementation
checks; external review = not recorded; novelty = not certified. A passing computation
is not the reason for any universal quantifier below. The repository's current
claim ledger and [audit](../../K_FACILITY_AUDIT_2026-10-02.md) record the integrated scope.

## SC-K-INCIDENCE-BOX-DP and SC-K-HEIGHT-TWO-INCIDENCE-2 -- sparse boxed selection

**Objects/domain:** MF-MODEL with explicit positive binary rational input, common nonempty catalog, labeled `k>=2`, greedy positive-reach occupancy and score `gamma`; freeze clients of weight at least `gamma` and clients with one occupied option. In the remaining individually named light client–occupied site incidence graph, both sides have maximum degree `d` and treewidth `tau`, with `d,tau` fixed constants.

**Exact statements:** the first claim decides and constructs a boxed site-pure/within-site-uniform exact customer NE in input-bit-polynomial time, if one exists. It does not promise feasibility. The second additionally assumes every remaining client has exactly two occupied options and the opening-directed site graph has longest directed path at most two edges; for every such input it constructs a complete exact customer continuation and a factor-two labeled facility profile in input-bit-polynomial time.

**Dependencies/evidence:** local conditional-cost identity in MF-MODEL, greedy load box, finite-domain CSP and explicit treewidth conversion in [the new proof](bounded_incidence_box.md); SC-K-HEIGHT-TWO-BOX-EXISTS supplies feasibility for the second claim and SC-K-GREEDY-BOX-TO-2 supplies all off-path states. Fixed-width decomposition uses Bodlaender (1996) as an imported algorithm. One independent internal inverse review of the CSP argument; no external review or canonical software. Neither claim decides arbitrary mixed on-path strategies, nor yields a polynomial algorithm for varying `d,tau` or all inputs.

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

## SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2 -- arbitrary-size mixed multiplicities

**Objects/domain and quantifiers:** explicit positive rational MF-MODEL,
arbitrary labeled (k\ge2), positive maximum site reach, and the actual
occupancy of SC-K-GREEDY-BUDGET. Each occupied-site customer-overlap
component must either have constant final multiplicity, or have the
property that every customer eligible inside it can choose **one** site
or **all** its sites. Components in the latter class can have any size
and unequal multiplicities; the condition is checkable in polynomial
time. With no shared client the component is a singleton. This new ID
has a broader input domain than the preceding two-site theorem and does
not retroactively change that theorem's assumptions.

**Exact conclusion and construction:** the same greedy labeled layout has
an input-bit-polynomially constructible site-uniform independently mixed
exact customer NE and a complete exact factor-two continuation. Within
a mixed all-or-one component, the first-opened site H holds all shared
clients initially and has maximal final multiplicity Q. Keep customers
with a unique occupied option fixed; insert all shared clients in
nonincreasing weight at a current minimum normalized load (W_t/q_t).
The last shared client placed at any site proves every earlier client
there satisfies its full exact NE inequality. The greedy final load box
(q_t\gamma\le W_t\le(q_t+1)\gamma) survives: H receives a subset of its
initial clients, while a shared weight (w) sent elsewhere is at most
(\gamma), by comparing the chosen normalized load to H's remaining
load. Singleton sources outside H retain private weight (P_u\ge\gamma)
and obey (W_v+w(F_u)\le(q_v+1)\gamma+a-P_u\le(q_v+1)a).
Constant-q components use the published identical-link algorithm and
the existing singleton pool. MF-PACK-2, MF-PURE-CAP-POLY and the complete
continuation rule close every actual deviation, including empty targets.

**Dependencies/evidence/limits:** MF-MODEL, SC-K-GREEDY-BUDGET,
SC-K-GREEDY-MAX-MULT, MF-PACK-2, MF-PURE-CAP-POLY, MF-CONT-COMPLETE and
the complete greedy-list proof in
[polytime_frontier.md](polytime_frontier.md). A strict six-facility,
three-site (q=(3,2,1)) integer example there fails the range condition
and the pair-component condition yet is covered. The two-site theorem is
subsumed as an output class (each pair's shared clients cover both sites),
but its independent one-pass repair proof remains a separate method.
General multi-site partial-overlap components are unhandled. Internal
independent reverse audit found no fatal objection; external review,
novelty certification and canonical implementation are unrecorded.

## SC-K-NESTED-ANCHOR-GREEDY-2 -- ordered partial overlaps around one anchor

**Objects/domain/quantifiers:** explicit positive binary rational MF-MODEL
input, arbitrary explicit k>=2, positive maximum site reach, and the actual
greedy occupancy. Each occupied overlap component has constant q, or its
first-opened H belongs to the occupied option set of every multi-option
customer and these customers can be ordered by nonincreasing weight with
nested, nondecreasing occupied option sets. Equal weights may be ordered to
satisfy inclusion. The condition is polynomially decidable. No condition is
imposed on a customer's coverage of *unoccupied* sites.

**Conclusion:** on this output subclass, the same labeled greedy layout has
an input-bit-polynomially constructible site-uniform independently mixed exact
client NE and a complete exact factor-two continuation. Remove multi-option
customers from H, retain one-option private reserves, then list-assign the
former in the stated order to an eligible site of minimum current W_t/q_t.
For an earlier customer i and the last later customer j assigned to its final
site, w_j<=w_i and A_i subset A_j imply the exact external-load NE condition.
The common anchor H and q_H>=q_t preserve every greedy load box, even before
the nesting condition is used. At a singleton source u!=H, its unchanged
private reserve P_u>=gamma bounds all occupied-target orphan overlap by
a-P_u; unopened-target weight is at most a+gamma<=2a. Existing packing,
polynomial capped Nashification and default continuation close every layout.

**Dependencies/evidence/objections/status:** MF-MODEL, SC-K-GREEDY-BUDGET,
SC-K-GREEDY-MAX-MULT, MF-PACK-2, MF-PURE-CAP-POLY, MF-CONT-COMPLETE and the
complete proof in [polytime_frontier.md](polytime_frontier.md). A strict
three-site q=(3,2,1) integer instance there lies outside both ALL-OR-ONE
and RANGE, while exchanging its two shared option sets makes the same
unrestricted list rule fail NE despite an alternative exact NE. Exact
arithmetic is independently checked by `tests/audits/kfac_nested_anchor.py`;
the check does not establish the universal theorem. Internal reverse audit
found no fatal objection; no external peer review, novelty certification or
canonical software implementation. This condition does **not** include
general three-site partial overlaps or prove the all-input polynomial target.

## SC-K-GREEDY-SINGLETON-RESET -- universal singleton off-path repair

**Objects/quantifiers:** positive-reach explicit rational MF-MODEL input,
arbitrary k>=2, the exact greedy layout with final score gamma>0, any
singleton-source facility f at an occupied site u with q_u=1, and any
on-path customer profile (including independent mixing) giving f expected
load a>=gamma. For every actual move of f, there exists an exact *pure*
off-path customer NE with its payoff at most 2gamma<=2a, constructible in
input-bit-polynomial time. On-path customer optimality is not needed for
the off-path construction; it is required when using the lemma in an SPE.

**Proof/objections:** P is the customers initially greedy-assigned to any
q=1 site. MAX-MULT prevents them from using an original q>1 site and the
first singleton opening proves w(P cap C_t)<=2gamma for all original q=1
sites. Reset all old customers to their original greedy sites except those
in the disappearing site's **original** J_u^0; redirect those to surviving
q=1 sites, or to a newly opened target when no stationary option remains.
The original strong greedy budget (8) puts at most W_u^0<=2gamma on an
unopened deviator target including genuinely new customers. Original q>1
sites survive, hold W_t^0<=(q_t+1)gamma and pack into their q_t stationary
facilities under cap 2gamma. Original q=1 sites each hold a subset of
P cap C_t of weight <=2gamma; occupied-target deviator begins empty.
MF-PURE-CAP-POLY completes exact customer NE preserving its cap. All
disappearing-site and occupied-target cases are explicit in
[polytime_frontier.md](polytime_frontier.md). Internal independent inverse
review found no fatal issue; no canonical implementation or external review.
This is an off-path lemma, not an algorithm for selecting the on-path NE.

## SC-K-GREEDY-BOX-TO-2 -- a sufficient on-path certificate

**Exact statement:** at the greedily chosen labeled occupancy, suppose an
explicit site-pure/uniform-within-site exact on-path customer NE satisfies
q_t gamma<=W_t<=(q_t+1)gamma at every occupied site. Then an exact
complete factor-two continuation for this same on-path state is computable
in input-bit-polynomial time. For q=1 sources use
SC-K-GREEDY-SINGLETON-RESET; for q>=2 the box gives occupied-target
stationary budgets, and greedy's N_r<=gamma gives unopened budgets.
MF-PACK-2, MF-PURE-CAP-POLY and MF-CONT-COMPLETE finish all layouts.

**Scope/limit:** no assumption on overlaps, site counts, weight diversity,
repair path, or singleton private reserves. The box and on-path NE must
both be supplied: their universal existence at the greedy occupancy and
input-bit-polynomial selection remain open. A bad NE outside the box does
not refute this conditional statement. Direct proof and reverse reset
check in [polytime_frontier.md](polytime_frontier.md); no external review.

## SC-K-UNIFORM-LIGHT-FLOW-2 -- equal light weights, arbitrary partial overlap

**Objects/quantifiers:** positive-reach explicit positive binary rational
MF-MODEL, arbitrary explicit k>=2, actual greedy occupancy and gamma>0.
Every multi-option customer (at least two occupied options) of weight below
gamma has one common weight delta with 0<delta<gamma, unless there are
no such customers. Single-option clients and multi-option clients of
weight >=gamma may have unrestricted positive weights. No restriction on
occupied overlap graph, multiplicities or singleton private reserves.

**Conclusion/construction:** the same greedy labeled layout has an
input-bit-polynomially constructible site-uniform independently mixed exact
on-path customer NE obeying every greedy box and a complete exact
factor-two continuation. Freeze single-option customers and multi-option
weights >=gamma at their greedy sites. Assign the delta clients by an
integral convex-cost flow minimizing the exact weighted client potential,
subject to W_t>=q_t gamma. A strictly improving client move cannot break
the lower bound. If a site t exceeds (q_t+1)gamma, decompose initial-to-final
client arcs into a path from a net-losing s to t; MAX-MULT gives q_s>=q_t.
Returning one delta client along every path arc is feasible and strictly
reduces the potential, a contradiction. The box also keeps all frozen
heavy clients at NE. SC-K-GREEDY-BOX-TO-2 supplies all off-path equilibria.

**Evidence/limits:** [full flow network, inequalities and strict chain
instance](polytime_frontier.md),
`examples/multi_facility/greedy_uniform_light_flow.json`, independent
`tests/audits/kfac_uniform_light_flow.py`. The three-site (3,2,1)
H--M--L instance lies outside RANGE, ALL-OR-ONE and NESTED-ANCHOR.
The finite script checks that instance only. The universal proof passed
independent inverse attack, but no external review, novelty certification
or canonical software implementation is recorded. Two or more different
light multi-option weights invalidate the equal-unit path argument as
stated; the all-input polynomial target remains open.

## SC-K-STAR-LIGHT-GREEDY-2 -- anchored star edges with unequal light weights

**Objects/domain:** positive-reach explicit rational common-catalog MF-MODEL;
arbitrary labeled k, greedy occupancy, gamma>0. In the graph joining
occupied sites that share a customer of weight below gamma with multiple
occupied options, every nontrivial component either has constant facility
multiplicity or is a star. In each star, its center H opened before its
leaves, and every light multi-option customer has precisely the two
occupied options H and one leaf. Frozen heavy customers may cross
components and have arbitrary incidence. Conditions are checked from
greedy output; no bounded number of sites or weight types is assumed.

**Exact conclusion:** in input-bit-polynomial time, find a site-uniform
independently mixed exact client NE in all boxes
q_t gamma<=W_t<=(q_t+1)gamma, then complete a factor-two continuation
with exact pure client NEs at every actual deviation. In star components,
per-leaf descending-weight queues move a customer H->leaf only on strict
improvement; choose the smallest normalized leaf load among eligible
heads. Every customer is processed once; q_H>=q_leaf and the strict
inequality preserve the full box. Nondecreasing selected leaf loads plus
the last-arrival weight order exclude all leaf->H returns. Constant-q
components use the already imported restricted identical-link scheduler;
frozen heavy clients are stable by the box. BOX-TO-2 completes off path.

**Evidence/limits:** [full proof and strict separating example](polytime_frontier.md),
`examples/multi_facility/greedy_star_edges.json`, independent
`tests/audits/kfac_star_edges.py`. The example has q=(3,2,1), two
unequal light weights and incomparable HM/HL options; RANGE,
ALL-OR-ONE, NESTED-ANCHOR and UNIFORM-LIGHT hypotheses all fail.
Those algorithms are not claimed to fail on this input. Internal
independent reverse reconstruction, no external review or canonical
software implementation. General light overlap graphs remain open.

## SC-K-TWO-LIGHT-LOWER-POTENTIAL-NO -- unequal light weights defeat the flow extension

**Objects/domain:** MF-MODEL with the greedy algorithm's seven-facility
occupancy and last score gamma=n, for every integer n>=45 divisible by 5.
Four occupied sites have multiplicities (3,2,1,1). The only multi-option
customers have different positive weights 4n/5 and n-1, both below gamma;
all other customers are private and frozen. All weights are integers.

**Conclusion:** minimizing the exact weighted customer improvement potential
over assignments satisfying *all* site lower boxes W_t>=q_t gamma has a
unique minimizer violating L's upper box by one. The same layout has a
box-constrained exact customer NE (indeed the initial greedy assignment),
so this only refutes that potential-selection extension of
SC-K-UNIFORM-LIGHT-FLOW-2. It gives neither a factor-two counterexample
nor hardness of box-NE search.

**Dependencies/evidence/objections:** MF-MODEL, SC-K-GREEDY-BUDGET, potential
identity (23), exact four-state comparison and all greedy scores in
[polytime_frontier.md](polytime_frontier.md); integer input
`examples/multi_facility/greedy_two_light_potential.json` and independent
`tests/audits/kfac_two_light_potential.py`. The earlier
SC-K-GREEDY-FIXED-POTENTIAL-NO is a stronger failure of a different
selection goal, including an actual forced off-path gain above two; the
present family isolates the equal-weight assumption with only two variable
clients. Internally independently checked, no external review.

## SC-K-DESCENT-ONLY-TRAP-NO -- forced upward return in a partial-overlap chain

**Exact objects/domain:** the six-client, three-site, six-facility positive
integer input (28), common site order H,M,L. Greedy has a strict site
choice at every insertion, final multiplicities ((3,2,1)), and load
box parameter (\gamma=20). Start from its assigned customer sites and
allow only strict improvements to sites of weakly lower final multiplicity.

**Conclusion:** every maximal sequence of such downward moves is the
unique three-step path T2: M→L, Y9: H→M, Z5: M→L. Its final site weights
((64,46,27)) have no downward improvement but T2 strictly prefers the
**upward** return L→M, external cost 25 versus alternative load 23.
After that return ((64,48,25)) is a true exact customer NE. Thus a
downward-only repair rule cannot universally complete the customer game,
even though the downward steps preserve the greedy box. This is **not** a
bad factor-two continuation or failure of the all-or-one theorem: the
component has partial H/M and M/L overlaps, no all-site common customer.

**Proof/evidence:** every greedy score, forced move and return inequality
are given in [polytime_frontier.md](polytime_frontier.md); integer input
`examples/multi_facility/greedy_descent_trap.json` and independent exact
`tests/audits/kfac_descent_trap.py` enumerate all currently allowed
downward moves after each step. Fixed-instance analytic obstruction,
internally audited; no external review.

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

## 2026-10-03: reset packing, path edges and type compression

`SC-K-RESET-PACK-INTERFACE` accepts any exact on-path customer NE with every individual facility earning at least the last greedy score, provided each original pool has a checked deletion packing. `SC-K-DOUBLE-LPT-GREEDY-2` supplies a deterministic polynomial recognition and construction test using two LPT passes and the imported minimum-load-preserving scheduler. Its exact triangle example selects a pure NE with a site total above the greedy upper box; neither theorem asserts acceptance on all inputs.

`SC-K-PATH-EDGE-LIGHT-GREEDY-2` handles directed opening-order light paths whose edges are internally equal-weight but may differ across edges. One improving forward move per client preserves boxes; no moved client wants to return. It includes unequal-weight P4 overlaps outside the prior anchored-star class.

`SC-K-BOX-NE-FPT-TYPES` decides the fixed-occupancy site-pure/uniform boxed-NE problem in FPT time parameterized by occupied sites and distinct multi-option weights. `SC-K-FROZEN-LIGHT-FPT` is a restricted component decomposition with frozen heavy clients. `SC-K-CATALOG-WEIGHT-XP-2` gives an unconditional complete factor-two constructor when the **entire** catalog size and distinct-weight count are fixed; its uniform parameter dependence is XP, not FPT. [Exact type encoding and proofs](type_compression.md). All are internally reviewed mathematical algorithms, without canonical implementation, external peer review or literature priority verification. The unrestricted arbitrary-parameter polynomial factor-two goal remains open.

## SC-K-THREE-SITE-CHAIN-BOX-EXISTS -- three-site chains with arbitrary unequal edge weights

For opening order H,M,L and light occupied-option graph H--M--L, arbitrary positive light weights on both edges still admit an exact full-box site-uniform customer NE. Every constrained exact-potential minimizer is NE: the only possible blocked move is an ML return L->M; return the **entire** HM pool currently at M to H simultaneously and bring the ML client to M. The exchange stays in all three boxes and strictly lowers potential, contradiction. [Full proof](three_site_chain_box.md). This is existence and an exact finite selection principle, not a polynomial algorithm to optimize the potential. Heavy customers are frozen; longer paths and branching remain open. Internal independent reverse audit, no external review or canonical implementation.

## SC-K-CONVERGING-PATH-BOX-2 -- a three-client converging light path

At four occupied sites D--B--A--C, exactly one movable light client on each edge starts respectively at D,B,C; q_D>=q_B>=q_A=q_C, and W_A^0=q_A gamma. A three-branch, at-most-seven-strict-move constructor stays in all greedy boxes and reaches exact client NE. BOX-TO-2 completes every facility deviation in polynomial input-bit time. [Full exact case analysis](converging_path_box.md), [finite rational state audit](../../../tests/audits/kfac_converging_path.py). Heavy multi-option clients remain frozen by the box inequalities. This theorem does not cover arbitrary trees, multiple clients per edge or a slack initial A. Internally reverse-audited; external review and canonical constructor implementation unrecorded.

## SC-K-HEIGHT-TWO-BOX-EXISTS -- shallow directed light graphs

Every variable light customer has exactly two occupied sites, and the orientation from earlier-opened to later-opened site has no directed path with more than two edges. Arbitrary branching, merging, differing multiplicities and unequal edge weights are permitted. Any full-box constrained minimum of the exact customer potential is an exact site-uniform client NE. A blocked backward improvement at u requires excess delta; all incoming neighbors of u are sources, so each entire incoming customer pool has weight at most gamma. Return a first-crossing prefix of these pools, together with the blocked client; all boxes remain valid and the exact potential falls strictly. [Complete proof](height_two_box.md). This subsumes the three-site-chain existence claim but does not find the minimizer in polynomial time or resolve paths longer than two edges. Two independent internal reverse audits; no external review, literature priority or canonical software.

## SC-K-CONVERGING-PATH-4MOVE-2 -- strengthened converging algorithm

Exactly three light clients occupy the D--B--A--C edges and start at D,B,C respectively. Greedy opening gives q_D>=q_B>=q_A and q_C>=q_A. Unlike SC-K-CONVERGING-PATH-BOX-2, no tight initial A or equality q_A=q_C is required. Check Z:C->A, T:D->B, X:B->A, a newly activated T:D->B, and Z:A->C in that order; at most four actual strict moves. Each move stays in the full box and the final state is exact customer NE, so BOX-TO-2 provides polynomial factor two. [Full proof](converging_four_moves.md), [finite exact audit](../../../tests/audits/kfac_converging_four_moves.py). The old seven-step claim is a strict special case and retains its independent case proof. Internal inverse review, no external review or canonical full implementation.
