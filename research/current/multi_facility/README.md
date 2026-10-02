# Common-catalog arbitrary-k branch

## Research goal and current result

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

The proof deliberately changes the type of continuation: on path it uses
independent mixing inside co-location groups; off path it isolates giant atoms
on stationary facilities and uses asymmetric pure equilibria. Requiring symmetry
on both sides can give unbounded apparent threats even for an instance with an
exact SPE (`SC-K-SYMMETRIC-MENU-OBSTRUCTION`).

## Claim and file map

| Path relative to this directory | Mathematical role and when to read |
|---|---|
| `model.md` | Complete arbitrary-k quantifiers, conditional actual costs and deterministic default continuation. Read before using any claim. |
| `claims.md` | Exact identities, dependencies, limits, and evidence of all seven proof/obstruction claims. |
| `uniform_two.md` | Full theorem and all multiplicity cases; Sections 3.2 and 5.2 prevent lost clients when a singleton source disappears. Section 8 distinguishes finite construction from polynomial time. |
| `reverse_review.md` | Reverse reconstruction from the desired off-path cap; explicit objections and independent-implementation evidence, with no claim of external peer review. |
| `lexmax_boundary.md` | For every fixed k, the selected lexmax occupancy itself can need factor tending to 2 under all NE choices, while another layout has an exact SPE; a sub-two proof must permit different layouts. |
| `symmetric_menu_obstruction.md` | Explicit all-q family separating unbounded symmetric-menu threat from alpha^*=1 in the full model; read before proposing any menu-only lower bound. |

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
Global lexmax enumeration and strict-improvement trajectory lengths
are not known to be polynomial here.

External peer review and priority against later literature, particularly the
unavailable 2025 dissertation, remain uncompleted. The existing two-facility
results and five-site complexity theorem retain their separate scope.
