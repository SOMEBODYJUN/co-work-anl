# Independent finite-menu audit for the common-catalog golden-ratio construction

Date: 2026-09-30. This audit concerns the **original common location set** model: two facilities use the same nonempty finite set S, may co-locate, and customers have positive rational atomic weights and independent mixed strategies. It does not import the heterogeneous factor-2 theorem or treat its lower bound as a common-catalog obstruction.

Audited sources: `phi_global_proof_candidate.md`, `strong_cross_chord_arbitrary_n_proof.md`, and `astra_local/local_chord_algorithm.md`. The phrase “uploaded Pro result” in `asym_research/meta.md` is not a premise of this audit.

## Verdict

The true-minimum oracle can be removed from the existing global golden-ratio proof. All its uses of an extremal customer equilibrium are witnessed by a single fixed polynomial menu at each unordered site pair. The proof needs only the minimum over that menu. In particular, its two claims of *uniqueness among all customer equilibria* follow from strict dominance proved using menu members, rather than from an unavailable global minimum.

This is a proof dependency audit, not a numerical substitution. The menu and each oracle use are specified below. The full global inequalities must still be included in a standalone theorem proof; the audit identifies exactly why their quantifiers remain valid after substitution.

## 1. A precise nonadaptive menu

Let a layout have private loads A,B and common customer weights w_1,...,w_k. Put R_A=A+sum w_i and R_B=B+sum w_i. Every menu member is retained only after its exact customer Nash inequalities are verified. All choices use a deterministic customer ordering and tie rule.

### P: guarded pure seeds

Enumerate both all-common-on-one-side assignments, and for each common customer h, both assignments putting exactly h on one side and all other common customers on the other side.

For each seed:

* If it is a pure NE, retain it.
* Otherwise identify its lower-load side with initial load Q and higher-load side with load P. Retain a repaired witness only if **every common customer initially on the lower side has weight at least P-Q**.
* For such a seed, repeatedly move a largest strictly improving common customer from the original higher side to the original lower side. Stop at no improvement or at the **first load-order reversal**. Retain that output.

A strict improving move has weight w<P'-Q'. Both resulting loads are inside the old load interval. Before reversal the gap decreases, so moved weights are nonincreasing. At reversal the new gap is smaller than the last moved weight. Thus every moved or originally lower-side customer is stable, and all remaining original higher-side customers are now on the lower-load side. The output is a pure NE, and the originally lower side retains load at least Q. At most k moves occur. If the seed was not already an NE, both final loads are strictly below the initial high load and strictly above the initial low load.

The all-common seeds guarantee a nonempty pure submenu: if the side holding all common customers is initially lower it is already an NE; otherwise the other side has no common customer and the guard is vacuous.

A generic improvement routine with no initial guard cannot replace this construction. Extra exact equilibria may be added to the menu, but the specified guarded outputs must be included.

### E: equal-reach splitting

When R_A=R_B, include the profile p_i(A)=1/2 for every common customer. Equal reaches imply A=B, so every common customer is indifferent and the two expected loads are equal. This includes every co-location.

### T: two designated mixers

For each distinct pair h,j, orient A as the lower-reach endpoint and B as the higher-reach endpoint, using both orientations when their reaches tie. Put every other common customer at B. Set W=sum_{i not in {h,j}} w_i and D=B-A+W>=0. Let

    p_h(A)=(1+D/w_h)/2,  p_j(A)=(1+D/w_j)/2.

Include the profile if D<=min(w_h,w_j), and verify all exact NE conditions. There are at most k(k-1) such profiles. With coordinates c_i=w_i(2p_i(A)-1), the gap is

    Delta=A-B+sum_i c_i = D,

and the two designated customers are indifferent. The remaining pure-B customers are stable because D>=0>=-w_i. Explicit verification covers boundary probabilities. The probabilities are then reflected back if A was the second physical endpoint.

For the global proof's same-large-pair application, A<=B and 0<=D<min(w_h,w_j); hence this required member is always retained. No unknown normalized cycle threshold is used to construct the menu.

### C: one fixed strong-chord witness

Let U=max(R_A,R_B), V=min(R_A,R_B), q=(sqrt(5)-1)/2 and a=q^2. If

    U>0,  V>U/(2q),  C=sum_i w_i<q V,
    max_i w_i<=a U,

include a deterministic output of the strong-chord constructor. It is an exact independently mixed NE satisfying loads

    L_U>=q V,  L_V>=q U.

The empty common list is allowed and has its forced pure profile. At equal reaches one may use E instead, since C<qU makes its equal loads larger than qU. For unequal reaches the larger-reach orientation is unambiguous. The algorithm of `astra_local/local_chord_algorithm.md` supplies the witness in O((k+1)^4) rational arithmetic operations. It does not compute a general minimum-equilibrium payoff.

The constructor is called using only actual reaches and the common-customer list. It is not called with d-values or adaptive quota parameters. Therefore a single output per pair covers all its uses in the global proof.

### Symmetry

Define one menu F({s,t}) of labeled assignments for each unordered site pair. Reversing the facility labels reverses every member of this same menu. Do not build independently chosen menus for the two orientations. P includes both seed orientations; T uses the lower-reach orientation and both orientations in ties; E and C are canonical by reaches. At equal reaches, any additional asymmetric C output is included together with its reflection (or C is replaced by the sufficient half-split E).

## 2. The correct replacement for the true-m criterion

Define

    u(s,t)=min_{sigma in F({s,t})} L_s(sigma),
    d(t)=max_{s in S} u(s,t).

These are finite rational minima and maxima. If a menu member at (s,t) satisfies

    L_s>=q d(t),  L_t>=q d(s),                         (Q)

then selecting menu-minimizing punishments after each actual unilateral deviation produces a phi-SPE. The two families of off-path unilateral deviations from a labeled on-path layout are disjoint. A default all-common guarded witness fills all remaining layouts.

This is a **sufficient** criterion for the unrestricted customer-continuation game. It need not be necessary for the existence of some SPE using equilibria outside the menus, and the constructive proof does not require necessity.

Assume no menu member satisfies (Q). Select b(t) attaining d(t), take any directed b-cycle, and normalize its maximum d to one. Co-location E implies

    d(s)>phi R_s/2,  R_s<2q.

For every menu member on a selected edge s->t,

    responder load P>=d(s),  incumbent load Q<q d(t)<=q.  (E)

Replace “every customer equilibrium on this edge” by “every menu member on this edge” wherever (E) is used. The pure submenu is nonempty, so a pure menu member can always be selected for atomic arguments. Every subsequently constructed blocking witness is listed in Section 3 below and belongs to the same menu.

Adding any additional exact equilibria to all menus preserves the proved guarantee: it retains the old witnesses and can only decrease u and d. This observation does not excuse omitting a required P, E, T or C witness.

## 3. Exhaustive witness audit against the global proof

| Source section | Apparent full-equilibrium/extremum use | Fixed-menu replacement and guard |
| --- | --- | --- |
| 2 | Compactness, exact m, response edges, co-location | Finite menu minima; sufficient criterion; E gives co-location. (E) is asserted only for menu members. |
| 3.1 | Pure repair | Exactly guarded P, stopping at first reversal. |
| 3.2 | Pure equilibrium maximizing the smaller reach | **Delete this background section. It is unused downstream.** No leveling extremum is computed. |
| 3.3 | If d(s)>R_s then uniqueness/return | All-common-at-s P gives responder load <=R_s whenever its private weight is <=R_s. Remaining case gives actual strict dominance; see Section 4. |
| 4 | H>=q propagation and heavy singleton witness | Propagation uses any pure P member. The displayed singleton seed is already an NE, hence is retained by P. |
| 5.1 | Two forwarded large customers / three large customers | Select any pure P member; (E) and ordinary pure Nash inequalities suffice. E is available if equal-reach equality is explicitly excluded. |
| 5.2 | Avoiding a large pair | All-common-at-t P. If repair is needed, initially lower s has no common customer, so the guard is vacuous. |
| 5.3 | Chord retaining one member of a large pair | Singleton-h P. If repair is needed, lower s contains only h and V-U<H, exactly the guard. |
| 6 | Capacity of a large-pair location | Select pure P; modified profile forwards only H. If not already NE its lower side contains only H and Q0-P0<H. This is the specified P repair. |
| 7 | Same-large-pair two-mixer contradiction | T with the two large customers, every remaining common customer on the higher-reach side. Capacity gives 0<=D<min(H,J), and the profile is an exact NE. |
| 8 | Triangle exclusion and closed pair subset | Reuses 5.2/5.3 P witnesses and 7 T; no new witness. |
| 9.1 | Bound u(t,s)<=R_t-H on upward h-chord | Singleton-h P. If repair is needed, its sole lower-side common customer H exceeds V-U<=R-2H<H. |
| 9.2 | Unique h-transport on a response edge | Select pure P; if sigma>=reach gap the reverse singleton seed is an exact P equilibrium, contradiction. Thereafter strict dominance proves true uniqueness; see Section 4. |
| 9.3 | Two-anchor covering: constructing both anchor chords | Each chord is singleton-h P. In the repair branch sole lower-side h satisfies V-U<=R-2H<H. Both target lower bounds are preserved by the fixed repair. |
| 10.1 | Abstract center theorem | The only new equilibrium call is singleton-h P, with the same R<3H guard. The return rule is 3.3; all other steps use inequalities/finite descent. |
| 10.2 | Nondegenerate-star center | Uses the pure P first edge from 12.1; no new local optimization. |
| 11 | Strong cross-chord with arbitrary number of mixers | C, constructed once from reaches. The output may have more than two mixers. |
| 12.1 | Maximum-reach first edge and uniqueness | E excludes equal reach; select pure P; reverse singleton exact P excludes sigma>=reach drop, then actual strict dominance. |
| 12.2 | h-only anchor | Purely structural consequences of preceding lemmas. |
| 12.3 | No-h chord when H>=R/2 | C. The proof verifies V>phi U/2, C<qV, maxcommon<=aU from actual reaches, independent of d. |
| 12.4 | Consecutive anchors if the next location is paired | C on (A0,A2) when A2 lacks h; otherwise uses 9.2. |
| 13 | No-h reach cap and final cycle closure | C on (Y,t). The rest is 9.1's P reach descent and 9.3's P covering contradiction. |

No step requires selecting an equilibrium outside F that minimizes a payoff over all customer NE. In particular, a pure NE may be taken from P in each atomic-load argument without imposing any unsupported purity on a menu minimizer.

## 4. The two places where true uniqueness survives

### 4.1 Return rule (global Section 3.3)

Suppose s->t has u(t,s)>R_s. Let E be the responder's exclusive weight. If E<=R_s, put all common customers at s. If already stable it gives responder load E<=R_s. Otherwise the original low side t has no common customer; its P repair keeps the responder strictly below initial high load R_s. Both contradict u(t,s)>R_s. Hence E>R_s.

Every common customer then strictly prefers s regardless of everyone else's choices: its cost at s is at most R_s, while its cost at t is at least E+w_i>R_s. The actual customer game therefore has one equilibrium; every menu member is that equilibrium, so u(t,s)=E exactly. The source load is R_s and (E) gives d(t)>phi R_s. This proves the return rule using finite-menu values.

### 4.2 Common-h transport (global Sections 9.2 and 12.1)

The pure-menu and reverse-singleton arguments establish:

    R_s>R_t,  sigma<R_s-R_t,
    source load R_s-H<=K<q,
    responder load R_t-sigma>=d(s)>q.

Here sigma is the total weight of common customers other than h. Customer h's smallest possible cost at s is R_s-sigma, strictly larger than its largest possible cost R_t at t. Thus h strictly chooses t in every actual NE.

Conditional on h choosing t, every other common customer strictly chooses s: its cost at s is at most R_s-H<q; choosing t costs strictly more than the base load R_t-sigma>q. Consequently the actual NE is unique, and the finite-menu minimum equals its responder load R_t-sigma. The equality needed by the two-anchor algebra is therefore valid; no full m oracle is hiding in it.

## 5. Arithmetic, complexity, and exact checks

For n customers and N common sites:

* P has at most 2(n+1) members; each guarded repair uses O((n+1)^2) rational operations.
* E has one member.
* T has O((n+1)^2) members; constructing and directly verifying every one costs O((n+1)^3) rational operations.
* C costs O((n+1)^4) rational operations using the exchange construction, including finite pure repairs.

Thus all pair menus and their minima take O(N^2(n+1)^4) rational arithmetic operations. Finding d and scanning all witnesses is lower order. Storing every explicit probability vector takes O(N^2(n+1)^3) rational entries; recording only minima, a selected witness, and deterministic provenance can reduce storage, but is not needed for polynomiality.

The output certificate consists of one on-path mixed NE and at most 2(N-1) actual unilateral-deviation NE, plus a polynomial default pure-equilibrium routine. Each stored NE is checked directly using

    Delta=A-B+sum_i w_i(2p_i(A)-1),
    p_i=1 => Delta<=w_i,
    p_i=0 => Delta>=-w_i,
    0<p_i<1 => Delta=w_i(2p_i-1).

All probabilities are rational. Exchange coordinates are input-weight signed sums; mixer gaps divide such sums by integers at most n, and probabilities divide by an input weight. Pure repair only adds/subtracts input weights. Their encoding lengths are polynomial in the original binary input length.

Golden-ratio comparisons are exact: to compare a nonnegative rational z to q, compare z^2+z-1 to zero, and handle negative z directly. Other displayed comparisons reduce to rational comparisons with q using q^2=1-q. There is no floating tolerance in acceptance of a customer NE or a facility improvement inequality.

## 6. Remaining work boundaries

The fixed-menu closure removes the local-minimum oracle obstruction for the original common-catalog phi construction. It does not solve arbitrary quota feasibility or exact minimization over all mixed customer NE, and therefore is compatible with the separate NP-hardness theorem for m. It also does not imply a phi guarantee for arbitrary facility-specific catalogs; the co-location and all common-catalog chords used above must be legal.

Implementation testing checks that generated probabilities and certificates agree with these definitions. It cannot replace the global cycle contradiction or justify a generic repair algorithm whose output is missing the proved load bounds.
