# Common-catalog arbitrary-k branch

## Research goal and current result

The newest [two-unequal-light-client parameter family](polytime_frontier.md#sc-k-two-light-lower-potential-no-lower-bounded-potential-can-overflow-with-two-weights) isolates a failed extension of the uniform-light flow proof. All lower greedy boxes remain feasible, and the initial assignment is a box NE, but their weighted-potential minimum uniquely exceeds an upper box. See the [integer input](../../../examples/multi_facility/greedy_two_light_potential.json) and [Fraction audit](../../../tests/audits/kfac_two_light_potential.py). This is a selection-rule obstruction, not a factor-two lower bound. The open task remains a polynomial box-NE selector for unequal light weights, or a different occupancy mechanism.

Extend the exact-customer-equilibrium, complete-continuation shared-catalog
model from two labeled facilities to arbitrary k. `SC-K-2-E` gives a complete
internal existence proof of a uniform factor 2 for EVERY k>=2. This answers the
constant-existence alternative; an unbounded optimum family cannot exist under
these exact hypotheses. The best uniform constant remains in [phi,2], using
the existing two-facility lower result only because k=2 is included. No
polynomial-time construction or sharp value is claimed.

The separate [mathematical and direction-value audit](../../K_FACILITY_AUDIT_2026-10-02.md)
records independent internal proof attacks and the remaining literature and
external-review obligations. Repository regression results and Git synchronization
are operational facts recorded at the time of integration, not proof premises.

## Objects and proof map

`MF-MODEL` -> finite global lexmax of site-pure, within-site independent-uniform
profiles -> `SC-K-LEX-BUDGET` (exact on-path NE plus orphan-aware transfer budgets).
Together with `MF-PACK-2` and `MF-PURE-CAP`, this yields a pure exact NE after
each actual deviation with deviator load <= twice its on-path load.
`MF-CONT-COMPLETE` then assembles one full continuation -> `SC-K-2-E`.

For the **algorithmic** question, [polytime_frontier.md](polytime_frontier.md)
strengthens the off-path step to `MF-PURE-CAP-POLY` using the published
restricted identical-link Nashification theorem. It proves
`SC-K-LEXMAX-STRONG-HARD` for the exact global selection oracle, while
`SC-K-LOCAL-PLS` shows a polynomial neighborhood local maximum is enough for
all on-path NE and transfer budgets. Neither is a polynomial algorithm for
finding that local maximum, nor hardness of finding some factor-two witness.
The separate `SC-K-GREEDY-BUDGET` procedure already constructs all budgets
in polynomial time, but a four-customer input proves that fixing its layout
and Nashifying on path can destroy those sufficient inequalities.
`SC-K-GREEDY-UNOPENED-2` sharpens this obstruction: along strict site-level
customer repair at the greedy layout, all loads remain above the last greedy
score, so an unopened deviation target always satisfies the actual factor-two
initial deviator cap. The unresolved part is packing the surviving occupied
sites and reaching the desired on-path exact NE in bit-polynomial time.
For the recognizable output subclass with equal occupied-site multiplicity
`q>=2`, the latter work *does* close: site-level restricted-identical-link
Nashification preserves both load extrema, and equal `q` makes its site NE
an exact original-game NE. All occupied and unopened budgets then hold and
the complete factor-two continuation is bit-polynomial
(`SC-K-EQUAL-MULT-GREEDY-2`). When greedy occupies k distinct sites, its
first maximum-reach site gives a persistent R/2 candidate score; the
range-preserving import gives a bit-polynomial **factor-two** continuation
(`SC-K-DISTINCT-GREEDY-2`), strengthening the older factor-three proof.
The more general `SC-K-COMPONENT-MULT-GREEDY-2` permits different
multiplicities in different customer-overlap components. Each component
must have constant multiplicity, and a multiplicity-one component must
be a single site. Independent site-level Nashification plus unchanged
singleton components preserve all four budgets and give polynomial factor two.
The newer `SC-K-RANGE-GREEDY-2` groups occupied sites by multiplicity and
checks an explicit bound on every client's incentive to cross to another
multiplicity class. Within each group, restricted identical-machine
Nashification retains its initial load range. For singleton sources, a
greedy customer-pool inequality controls a disappearing site, with the
deviator allowed initial load up to 2a at an unopened target. This removes
the old singleton-component restriction and admits some *light* cross-q
clients. `SC-K-LIGHT-COMPONENT-GREEDY-2` is a simpler sufficient test;
`SC-K-GREEDY-HEAVY-OVERLAP-2` needs no on-path repair at all.
The newer `SC-K-TWO-SITE-COMPONENT-GREEDY-2` also handles components with
two sites of *unequal* multiplicity. Shared clients start at the higher-q
site; one descending-weight pass transfers only strict improvements to the
lower-q site. A scalar load difference rules out all return moves, every
transfer preserves the greedy load box, and a pooled-orphan identity handles
the disappearing lower-q site. Constant-q components use the published
scheduler. This is bit-polynomial and admits some inputs that fail the range
certificate. The broader `SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2` permits
arbitrarily many mixed-q sites when each client has one occupied option or
the entire component. It inserts all-site shared clients in descending
weight at minimum current normalized load; private reserves and the greedy
load box close singleton-source deviations. It includes every two-site
component and a three-site q=(3,2,1) input failing RANGE.
`SC-K-NESTED-ANCHOR-GREEDY-2` further admits genuine partial overlaps:
the first-opened site covers all multi-option clients and, along a
nonincreasing-weight order, their occupied option sets expand by inclusion.
The restricted list rule then satisfies the last-job NE inequality, while
the common anchor alone preserves the greedy load box. Private reserves
close disappearing-singleton budgets. A strict three-site example separates
it from ALL-OR-ONE and RANGE; reversing two option sets makes the unrestricted
list rule fail NE but leaves another NE. The full mixed-q partial-overlap
problem remains open.
`SC-K-GREEDY-SINGLETON-RESET` gives a stronger off-path interface: after
departure from an originally singleton greedy site, reset old customers
to greedy's initial assignment and use its original q=1 pool bound. This
constructs a pure exact deviation NE with payoff at most 2 gamma when
the on-path facility earns at least gamma, regardless of the on-path
customer assignment. Hence **any supplied exact site-uniform on-path NE
in the full greedy load box** has a bit-polynomial factor-two continuation
(`SC-K-GREEDY-BOX-TO-2`), without singleton private reserves.
`SC-K-UNIFORM-LIGHT-FLOW-2` constructs such a box NE for arbitrary partial
overlaps and multiplicities when all multi-option customers lighter than
gamma have the same weight delta; other weights are arbitrary. A
lower-bounded integral convex-cost flow gives exact NE, and reversing a
path of equal-weight transfers proves the upper box. A strict three-site
H--M--L chain lies outside RANGE, ALL-OR-ONE and NESTED-ANCHOR. Finding
a box NE on general mixed-light-weight input remains open.
Outside those conditional classes, `SC-K-GREEDY-STATIC-PACK-NO` gives a
five-site integer instance where a reachable exact on-path NE leaves a
different surviving site too heavy for the old cap packing if customer site
assignments are frozen. The appropriate next interface must permit cross-site
customer reassignment or select a more robust on-path state; the example
does not preclude a factor-two continuation.
The related `SC-K-GREEDY-CAP-INFEASIBLE` instance adds an unopened target
with a forced private customer and proves **no** cross-site reassignment
can meet the old *global* ordinary cap for one deviation; nevertheless an
exact off-path NE gives the deviator less than twice its original load.
The next all-input method needs a deviator-specific bound that permits
safe overload elsewhere, or a different on-path mechanism.
The exact integer input is `examples/multi_facility/greedy_cap_obstruction.json`;
`python tests/audits/kfac_greedy_cap.py` independently rechecks greedy,
strict moves, on/off-path customer NE, and the forced cap obstruction.
This finite audit does not prove the conditional algorithmic theorems.
Two further integer witnesses (`greedy_repair_order_escape.json` and
`greedy_heaviest_escape.json`) show that arbitrary strict repair, and even
choosing the heaviest improving client at each step, may end at exact NEs
where a B-to-G deviation is **forced** above factor two in every mixed
off-path NE. Both layouts also have another reachable exact NE retaining
the four transfer budgets. Their scripts check finite arithmetic, not a
general theorem. Selection of a suitable NE on range-certificate-failing
mixed-q components of three or more sites with partial overlaps remains open.
`SC-K-DESCENT-ONLY-TRAP-NO` gives a six-client three-site chain where the
only maximal downward-q repair path stops before reaching customer NE;
one upward return completes it. This does not refute greedy occupancy.
In fact, the first
integer witness makes the fixed-greedy-layout site-uniform lexmax customer
assignment uniquely bad (`SC-K-GREEDY-FIXED-LEXMAX-NO`). A second integer
witness has exactly two site-uniform NEs and makes the bad one the unique
**global minimum of the exact customer improvement potential**
(`SC-K-GREEDY-FIXED-POTENTIAL-NO`), despite a good NE at the same layout.
These refute two specific on-path selection rules, not greedy occupancy.

The proof deliberately changes the type of continuation: on path it uses
independent mixing inside co-location groups; off path it isolates giant atoms
on stationary facilities and uses asymmetric pure equilibria. Requiring symmetry
on both sides can give unbounded apparent threats even for an instance with an
exact SPE (`SC-K-SYMMETRIC-MENU-OBSTRUCTION`).

## Claim and file map

| Path relative to this directory | Mathematical role and when to read |
|---|---|
| `model.md` | Complete arbitrary-k quantifiers, conditional actual costs and deterministic default continuation. Read before using any claim. |
| `claims.md` | Exact identities, dependencies, limits, and evidence of the current proof and obstruction claims. |
| `uniform_two.md` | Full theorem and all multiplicity cases; Sections 3.2 and 5.2 prevent lost clients when a singleton source disappears. Section 8 distinguishes finite construction from polynomial time. |
| `reverse_review.md` | Reverse reconstruction from the desired off-path cap; explicit objections and independent-implementation evidence, with no claim of external peer review. |
| `lexmax_boundary.md` | For every fixed k, the selected lexmax occupancy itself can need factor tending to 2 under all NE choices, while another layout has an exact SPE; a sub-two proof must permit different layouts. |
| `symmetric_menu_obstruction.md` | Explicit all-q family separating unbounded symmetric-menu threat from alpha^*=1 in the full model; read before proposing any menu-only lower bound. |
| `polytime_frontier.md` | Exact global lexmax hardness, local PLS neighborhood, greedy budgets, distinct-site and mixed-q conditional algorithms. Universal singleton reset completes any supplied box-constrained exact on-path NE; lower-bounded integral flow constructs one for arbitrary partial overlaps with equal light multi-option weights. Includes strict repair, fixed-layout selection, anchored-list and descending-only obstructions. Read before proposing a universal greedy-output customer selection rule. |

Implementation: `multi_facility_spe/two_exists.py` and `__main__.py`, a sibling
package rather than a silent modification of the two-facility API.
`tests/multi_facility/definition_check.py` recomputes conditional costs directly.
`tests/multi_facility/run_exact_audit.py` exercises the constructor and saved certificates;
`tests/multi_facility/run_reverse_audit.py` never imports that constructor and enumerates all
lexmax ties and all pure NE in its small audit domain. Frozen data are
`evidence/runs/kfac_two_exact.json` and `kfac_two_reverse.json`.

## Frontier and next decisive obligations

There are two genuine residual goals: sharpen the uniform factor in [phi,2],
and obtain a bit-polynomial construction on explicit rational input. The scalar
packing interface cannot simply replace 2 by a smaller constant: h+1 equal
weights saturate its bin count. That does not rule out a more informative
allocation invariant and a different layout-selection mechanism. In fact
`SC-K-LEXMAX-BARRIER` proves that keeping the same selected layout and changing
only its on-path NE or off-path selection cannot give a universal sub-two bound.
Exact global lexmax selection is strongly NP-hard, and strict-improvement
trajectory lengths have no polynomial bound proved here. Given the selected
on-path state, off-path capped Nashification can instead run in polynomial
time; the local-maximum search for a sufficient on-path state is in PLS, with
no polynomial-time solver proved.
The conditional range certificate now includes all-distinct output and
multi-site singleton components. The remaining algorithmic cases are
mixed-multiplicity inputs where some customer's cross-class incentive fails
the initial range check. The exact greedy-repair-order counterexamples
exclude two tempting choices of on-path NE, while explicitly retaining
another good NE at those same layouts; they do not establish greedy
occupancy failure or complexity hardness of the full search problem.

External peer review and priority against later literature, particularly the
unavailable 2025 dissertation, remain uncompleted. The existing two-facility
results and five-site complexity theorem retain their separate scope.
