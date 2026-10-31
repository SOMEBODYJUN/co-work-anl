# Provisional review: bounded-group weighted menu exact statement

Source ID: `588d9d1babe0d23e6a59`
Path: `history/source/notes/unrelated_machines/bounded_group_interaction_weighted_menu_exact.md`
SHA-256: `fbadf808733bbe9828c90d429ed79e6e94ec0bbbd06a72dbb6768ea1315c15d6`
Size: 10,368 bytes. Both frozen source commits point to the same blob.

## Full read and mathematical identity

The 10,368-byte statement-first scratch was read in full. It defines an explicit unrelated-machines instance with nonempty indexed state menus, one selector per group, private state machines, resource machines and incidence jobs. Private state mass is at most one; resource incidence across groups is bounded by `Delta`; the group interaction graph has maximum degree `M`; all values are binary rationals and all jobs remain in the original instance. It proposes `beta=1/(M+2 Delta)` and `R=2-beta`.

The proof sketch has the same two-branch mechanism as the later canonical weighted-menu review: normalize every state with a private bonus resource; classify groups with a diffuse state; use a heavy-group/resource matching or derive `OPT >= 1+beta`; in the success branch reserve one heavy resource per non-diffuse group, charge at most `M beta` stolen mass, and match complete blocks of `Delta` remaining resources for diffuse groups. The scratch explicitly keeps all unselected-state jobs, distinct resource identities, exact rational sorting, and polynomial explicit matching. It also gives a grouped-cube specialization with `M <= q(d-1)` and `Delta <= min(d,Q)`.

## Comparison with the canonical review

The current canonical review is `archives/unrelated-machines/state/审查/加权菜单组交互匹配双源续审查--审查.md`. It records the same source family as `UM-BOUNDED-GROUP-INTERACTION-WEIGHTED-MENU-v2`, but with the corrected denominator `beta=1/(M+2 Delta-1)`. The canonical review tightens the block tail accounting from the scratch's `W'_g/Delta-beta >= beta` presentation to

`[1-(M+Delta-1) beta]/Delta >= beta`.

Thus the scratch is neither a new general-UM theorem nor an unrelated duplicate. It is an earlier statement-only version of the same bounded-interaction algorithm, and its denominator is weaker by one in the additive term. The scratch has no independent proof, implementation, finite experiment, or sharpness claim. Its unique value is historical provenance for the first exact statement and the explicit boundaries (no OPT witness, no CONFIG backend, no hidden resource expansion, no SPE transfer).

## Recommended future disposition

When the write endpoint is available, register this source as `integrated`, targeting the canonical weighted-menu review, and retain its fingerprint and denominator-correction note. Do not create a second theorem object or treat the weaker `M+2 Delta` factor as the current sharp statement. No `claim`, `done`, or `push` was attempted in this provisional pass.
