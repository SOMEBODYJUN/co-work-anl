# A fixed polynomial witness menu for the shared-catalog golden-ratio theorem

Research result, 2026-09-30. This is an algorithmic proof transfer from
`history/proofs/shared/existence_candidate.md`, using the exact polynomial local constructor in
`math/proofs/local/chord_exchange.md`. It is independent of an oracle for a
facility's minimum load over every client equilibrium. The underlying global
proof remains an internally audited research draft, not externally reviewed.

## 1. The algorithmic theorem

There are finitely many explicitly listed clients with positive binary rational
weights, and a finite nonempty catalog S available to both facilities. Client
accessibility is explicitly specified. Clients independently minimize expected
realized total load at the facility they choose. Both facilities maximize their
expected client weight.

**Theorem.** An exact-client-NE, pure-facility-location phi-SPE can be constructed
in polynomial time in this input's bit length, where phi=(1+sqrt(5))/2. A
conservative bound is O(|S|^2(n+1)^4) rational arithmetic operations, with
polynomially bounded intermediate bit lengths. The output comprises rational
on-path probabilities, at most 2|S|-2 rational unilateral-deviation
continuations, and a polynomial default pure-NE procedure for every other
labeled location profile.

The theorem is about constructing one suitable continuation rule. It does not
optimize the global SPE factor, and does not compute exact local minimum loads.
All clients' continuation strategies are exact Nash equilibria for the original
weights. No weight rounding or approximate client equilibrium is used.

## 2. One static common menu for each physical pair

At a pair (s,t), let A,B be the exclusive client loads, let w_1,...,w_k be the
common client weights, and put W=sum w_i. The reaches are R_s=A+W and R_t=B+W.
Construct the following finite menu F(s,t), retaining individual independent
mixing probabilities. Use the same menu for on-path witnesses and both
orientations of punishment minima.

### P: all-on-one and every single-client seed, with guarded repair

Include each pure seed putting every common client on one side. Also, for each
common client h, include each seed putting only h on one side and all other
common clients on the other side. There are at most 2(k+1) seeds.

If a seed is already a pure NE, retain it. Otherwise retain a repaired output
only when **every common client on its initially lower-load side has weight at
least the initial load gap**. In that case, repeatedly move a largest strictly
improving client from the originally higher side, and stop at the first reversal
of load order or when no improvement exists. Fix ties by client index.

The repair lemma in the global proof makes this an exact pure NE and preserves
the original lower-side load as a lower bound. Each common client moves at most
once. Unqualified seeds are discarded. The all-on-one seeds make P nonempty.
The proof below needs these precise guarded outputs; arbitrary improvement
sequences are not substituted for them.

### H: equal-reach half splitting

When A=B, independently give every common client probability 1/2 at each side.
Both loads equal (A+B+W)/2, and each client is indifferent. In particular, at a
co-location (s,s), this supplies loads R_s/2,R_s/2.

### T: every designated pair of mixers

For every pair of distinct common clients h,j, put all other common clients at
the higher-reach location. Write U for the lower-reach location, V for the
higher-reach location, a<=b for their private loads, H=w_h, J=w_j, and

    Z = sum of all other common weights,
    D = b-a+Z.

If D<=min(H,J), give h and j probability (1+D/H)/2 and (1+D/J)/2 at U. The
remaining common clients use V purely. The expected gap L_U-L_V is D; the two
designated clients are indifferent and all other common clients use the lower
expected-load side. Thus this is an exact NE, with

    L_U = b+Z+(H+J)/2,
    L_V = a+(H+J)/2.

At equal reaches include both choices of U. There are at most 2 binom(k,2)
such outputs. Endpoints D=H or D=J are allowed; designated mixers need not be
genuinely mixed.

### C: one reach-based strong-chord witness

Order the reaches as R>=r. Whenever

    r > phi R/2,   W < r/phi,   max_i w_i <= (1-1/phi)R,

call the polynomial constructor `astra_local.construct.construct(R,r,weights)`
and include its output. For k=0 the maximum-weight condition is vacuous. The
strong-chord theorem guarantees an exact NE with

    L_R >= r/phi,   L_r >= R/phi.

Its choices depend only on the two reaches and the common weight list, not on
any response cycle, global threat, chosen heavy client, or quota generated later
in the global proof. At equal reaches include its reflection as well.

Construct each unordered physical pair once and define the reversed ordered
menu by exchanging the facility labels. At diagonal pairs the menu is explicitly
closed under that exchange. This ensures a single symmetric correspondence and
avoids inconsistent orientation-specific menus.

## 3. Menu minima and the correct edge quantifier

Define, for these menus only,

    u(s,t) = min { L_s(e) : e in F(s,t) },
    d(t)   = max { u(s,t) : s in S }.

Each minimum is attained by a listed witness. Choose b(t) attaining the maximum,
and select a directed cycle T of the map b. Threat values d retain their maxima
over the full original catalog S throughout.

If a menu witness at (s,t) has loads x>=d(t)/phi and y>=d(s)/phi, it gives a
phi-SPE: choose a minimizing menu witness separately after each actual
unilateral deviation. The two off-path deviation families are disjoint labeled
profiles, so these choices do not conflict. Other profiles use any exact pure
NE. This criterion is sufficient for a full-game SPE; it is not asserted to be
necessary for the unrestricted collection of all true equilibria.

Assume for contradiction that no such menu witness exists. On a selected edge
s->t=b(s), **every menu member**, rather than every true NE, satisfies

    responder load P >= d(s),
    incumbent load Q < d(t)/phi.

The first inequality is the definition of a menu minimum. The responder already
meets its required quota, so absence of a good menu witness forces the second.
Every use of an edge's universal load bound in the global proof can be restricted
to this precise quantifier.

## 4. Proof transfer: every needed witness belongs to this menu

Set q=1/phi and use the global proof's normalization max_{s in T} d(s)=1.
The following dependency audit identifies all equilibrium-producing operations.
All subsequent reach, overlap, and cycle inequalities remain identical because
they concern only a chosen menu member or a listed witness.

| Global proof part | Witness or information used | Why the menu suffices |
|---|---|---|
| Section 2 | Co-location R_s/2 on both sides | H includes every diagonal half split |
| Section 3.3 | All common clients at the incumbent, with repair | P includes exactly this seed and its guarded output |
| Section 4 | A specified heavy client alone at the incumbent | P contains every singleton, including this client |
| Section 5.1 | Any pure edge NE | P is nonempty at every edge |
| Section 5.2 | All common clients at the other endpoint | P includes the required all-on-one seed and output |
| Section 5.3 | A shared member of a large pair alone at one endpoint | P; the proof establishes the repair guard |
| Section 6 | Reassign only one specified heavy client forward | P; if repair is needed its lower side has only that heavy client and the displayed gap is smaller than its weight |
| Section 7 | Two specified large clients mix, all others at the higher-reach site | T contains this exact template; the proof establishes D<min(H,J) |
| Section 8 | Reuses pair avoidance and single-heavy chords | Already P and H |
| Section 9.1 | A specified common h alone at the lower-reach side | P; its guard follows from R<3H |
| Section 9.2 | Some pure edge NE, then the reverse singleton seed | Both in P; subsequent uniqueness is proved by strict dominance |
| Section 9.3 | For each of two anchors, put h alone at the queried site | P; if V>U, V-U<=R-2H<H, so the guard holds |
| Section 10 | Same common-h singleton chords and return rule | P and the strict-dominance arguments already covered |
| Section 12.1 | Some pure edge NE, then its reverse singleton seed | P; resulting unique transport is again a dominance conclusion |
| Sections 12.3,12.4,13 | A strong chord with reach-based quotas | C supplies exactly those quotas with no d-dependent choice |

### The apparent extremal calls do not survive this audit

Section 3.2's leveling selection maximizes one facility's pure-equilibrium load.
That subsection supplies background and is not used by the final proof; delete
it in the menu-based proof. None of the rows above needs this optimization.

In Section 3.3, the contradiction with a small P witness forces the responder's
exclusive mass E>R_s. This implies genuine strict dominance for every shared
client, so the actual NE is unique and every menu has the same payoff. Therefore
the return rule and equality d(s)=E remain valid for the menu minimum.

In Sections 9.2 and 12.1, choose any pure P witness. The edge inequalities imply
that precisely h is sent forward. The reverse singleton P witness rules out
sigma>=R_s-R_t. Once sigma<R_s-R_t, h strictly prefers the responder for every
profile of other clients; after h's action is fixed every other common client
strictly prefers the incumbent. This proves uniqueness among **all independent
mixed NE**, rather than assuming it from the definition of d. Consequently
d(s)=R_t-sigma is valid for the restricted menu as well.

No other step in the global proof minimizes over all true equilibria. In
particular, every strong-chord application uses only the same two-sided
reach-based quotas supplied by C, and then compares those quotas to the full
menu threats via Section 3.3.

With these substitutions, Sections 4--13 of the global proof exclude the same
large-pair families, establish the same common-heavy-client transport, and close
the arbitrary-length response cycle. All witnesses invoked for a contradiction
are members of F. Thus the assumption of no good menu witness is impossible.
The construction of Section 3 gives the asserted phi-SPE.

This is a transfer of the supplied full proof, including its heavy-pair and
two-anchor arguments. It does not infer an algorithm merely from the bare
existence statement of that theorem.

## 5. Runtime, exactness, and output

For k common clients, P has O(k) outputs, each found in O((k+1)^2) rational
operations. T has O(k^2) outputs, with O(k) time to materialize and verify each.
H takes O(k). C takes O((k+1)^4) rational operations. Consequently every pair
menu has O((k+1)^2) entries and is built in O((k+1)^4) operations.

Compute all ordered minima, full d-values, and one response cycle. Scan every
menu entry on S x S; the theorem guarantees a qualifying entry already on
T x T. For its rational loads x,y compute

    alpha = max(1, d(t)/x, d(s)/y),

using the convention that a positive threat divided by zero is infeasible and
0/0 contributes zero. The theorem supplies an entry with alpha<=phi. For
rational alpha>=1, this comparison is exactly alpha^2-alpha-1<=0. There is no
floating-point golden-ratio test.

The full-catalog scan is within the same asymptotic time bound and may improve
the certified factor for a given instance. It optimizes only among witnesses
in the fixed menus, not among all possible continuations.

All seed and repair coordinates are signed sums of input weights. Pair-template
probabilities divide such sums by an input weight. The strong-chord constructor
has polynomial bit complexity. Hence all stored numbers and rational
comparisons have polynomial bit lengths. The output factor and probabilities
can all be rational; an irrational golden-ratio probability is unnecessary.

Only the selected on-path continuation and its actual unilateral neighbors
need be retained in the final certificate. At any other pair use guarded repair
of an all-on-one seed, which is always qualified or already an equilibrium.
This specifies an exact NE after every labeled location profile in polynomial
space.

## 6. Implementation and independent checks

`facility_spe/shared_phi.py` implements the static menu, full threat computation,
cycle selection, witness scan, and compact continuation certificate. It imports
the previously verified guarded repair and polynomial strong-chord routine.
Its `verify` function recomputes individual conditional client cost differences,
all facility payoffs, and every permitted unilateral deviation. It never reads
menu minima or assumes the theorem while verifying a supplied certificate.

Example:

```bash
python3 -m facility_spe.shared_phi examples/shared/tiny.json --output certificate.json
python3 -m tests.test_shared_phi
```

The test script includes zero coverage, a single physical site, the old
heterogeneous near-2 family with the four sites now shared, rational random
instances, serialized certificate round trips, and a chord whose requested
quotas require three genuinely mixed clients. The last pair has private loads
40,39 and common weights 20,20,20; the constructed loads are 277/4,279/4.
The recorded run verifies **753 complete exact certificates**: 750 seeded
rational random games and the three directed global instances. The largest
observed menu factor is 2013/1508. The separate three-mixer pair check passes.
Test counts and observed factors are recorded in
`evidence/runs/2026-09-30/shared_phi.json`. The existing eight-client, five-site
example in `examples/shared/tiny.json` additionally produces an exact factor-1
certificate in `evidence/certificates/shared/tiny_phi.json`.
These checks validate the executable;
the static-menu proof above supplies the universal guarantee.

Two independent agents inspected the menu formulas, guarded repair, every
minimum-load quantifier substitution, and the mandatory three-mixer example.
The separate audit is
`evidence/audits/shared_menu_quantifiers.md`. The new contribution here is
the static finite-menu transfer and complete global certificate construction.
The original existence proof, polynomial strong-chord routine, and guarded
pure repair are existing ingredients from the preceding research rounds.

## 7. Why local NP-hardness is unaffected

The construction uses realizable upper bounds u(s,t)>=m(s,t), certified by
specific menu equilibria. It does not assert equality, approximate m to arbitrary
precision, or decide arbitrary quota feasibility. The global proof closes the
response cycle for this specially chosen finite witness correspondence. Thus
the weak NP-completeness of optimizing a designated facility's load over all
client NE is consistent with this polynomial global existence construction.
