# Exact claim identities: common catalog, arbitrary k

All versions below are version 1, dated 2026-10-02. Status fields are separate:
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
