> **Historical research note (superseded frontier statements).** Preserve the derivation below as provenance; use [the current mathematical map](../../README.md), [claim registry](../../CLAIMS.md) and [source-status guide](../../PROVENANCE.md) for current scope.

# Handoff: two-stage facility location with atomic clients

Research checkpoint: 2026-09-30. The claims below have been independently cross-checked within this team, but the manuscript has not undergone external peer review. The model has two facilities with possibly different finite allowed location sets, positive rational client weights, and exact independent mixed customer Nash equilibria after each ordered facility layout.

## Closed results

1. **Sharp universal factor 2 for arbitrary catalogs.** Both facilities may have arbitrarily many different allowed locations. A 2-approximate pure-location SPE with exact **pure** customer continuations exists and can be constructed in polynomial bit time, with no bound on the number of common clients at a layout. A six-vertex undirected graph with positive integer weights gives a matching lower bound: for every factor below 2, a sufficiently large integer parameter makes every layout unstable even when *all* customer Nash equilibria, including mixed ones, are permitted. The lower example has exactly two common clients at every legal layout. See `universal_two.md` and `tight_two_lower.md`.

2. **A structural overlap threshold for one short catalog.** If one facility has at most two allowed locations and each legal cross pair shares at most one client, the sharp universal factor for that class is `rho = 2 cos(pi/7)`, about 1.8019377358. The other facility may have arbitrarily many allowed locations. The lower example has six clients, positive integer weights and unique customer equilibria. The upper proof handles reach ties and overlapping allowed location sets and gives a polynomial pure-continuation construction. See `lower.md` and the manuscript.

3. **Reusable closed-response-core lifting.** In any finite two-leader game with independent permitted equilibrium selection at each labeled action pair, a cycle of best responses to *minimum attainable deviation payoffs* preserves the full-game threats at every cycle vertex. Consequently a small balanced core theorem lifts to arbitrarily many actions on the other side. The lemma is not specific to location games. See `meta.md` Section 2A.

4. **Reusable computation.** A guarded repair menu with at most four seeds per layout suffices for the polynomial factor-2 algorithm: all common clients sent to either side, and the heaviest common client alone sent to either side. Its conservative bound is `O(|U1||U2|(n+1)^2)` rational operations. The supplied solver uses this compressed four-seed menu by default; `--all-singletons` selects the larger audit menu, and `--maximum-only` remains a compatibility alias for the default. Both modes have been checked independently. When at most `kappa` clients are shared at each pair, a separate exact algorithm finds the instance's optimal SPE factor by enumerating `3^kappa` local support patterns and balancing an attainable load interval; its running time is `O(|U1||U2|[n+kappa 3^kappa])` rational operations. This latter exact solver assumes linear expected-load customer costs. See `r_menu_solver.py`, `bounded_overlap.py`, and `bounded_overlap_theorem.md`.

The sharp universal factor-2 existence and lower bound persist when each client has its own strictly increasing realized-load cost function, provided that client's function is the same at both facilities. The proof and algorithm use only pure client equilibria; the lower instance is resolved by pointwise strict dominance. This does *not* assert that arbitrary mixed equilibrium sets are unchanged under nonlinear costs.

A separate proven note, `nonlinear_kappa_two_independent.md`, gives an exact linear-programming reduction whenever follower continuation payoffs have an explicit rational polyhedral representation. As one application, if each legal pair shares at most two clients, the instance-optimal factor remains computable in polynomial time for arbitrary client-, facility-, and location-specific realized-load costs with finite polynomial-bit rational evaluations. This extension has a proof but **no new solver implementation** and is not part of the manuscript.

## Literature boundary

Krogmann, Lenzner, Skopalik, Uetz and Vos, *Equilibria in Two-Stage Facility Location with Atomic Clients*, IJCAI 2024, introduces the model and states a general `k`-approximate SPE claim (Observation 4). Its displayed co-location argument does not directly establish that claim for disjoint allowed sets. Our work gives a self-contained polynomial pure-continuation construction and a matching heterogeneous lower bound; it is **not** the first statement of the number 2 in this literature. The previous paper's lower bound approaches the golden ratio for its unrestricted example; our asymmetric six-vertex lower bound approaches 2. Source: https://arxiv.org/html/2403.03114v2 . See `final_audit_and_value.md` for a careful comparison.

## Run the solvers

The six-vertex examples in this handoff use JSON keys `weights`, `locations`, `U1`, `U2`. Client and location IDs are zero-based. Each `locations[j]` lists the clients who can reach site `j`.

```bash
python3 r_menu_solver.py tight_two_M1000.json --output factor2_certificate.json
python3 r_menu_solver.py tight_two_M1000.json --all-singletons --output factor2_full_menu_certificate.json
python3 bounded_overlap.py tight_two_M1000.json --output exact_factor.json
python3 test_r_menu.py
python3 test_four_seed.py
python3 tight_two_family.py --M 10000 --output another_instance.json
```

Both solvers verify their returned on-path and deviation witnesses. The R-menu solver certifies a factor at most 2 and uses only pure customer equilibria. The bounded-overlap solver computes the **optimal factor** over all independent mixed customer Nash equilibria in the linear-cost model. `tight_two_M1000.json` has optimal factor `335/169`; the entire integer family has factor `(2M+10)/(M+14)`.

## Highest-value unresolved task

The general factor-2 guarantee is now tight, so refining its numerical constant has no value without additional assumptions. A meaningful next target is whether the single-common-client sharp constant `rho` survives when **both** catalogs have arbitrary size, or to prove a different tight threshold. Another is to extend the pure-menu/response-cycle method to three or more facilities, where deviation profiles may no longer admit the same two-player chord structure. Establish a genuinely new theorem before treating either as a follow-on paper. Negative numerical searches are not theorems.

## Files to keep

- `paper/main.tex` and `paper/main.pdf`: compiled 17-page manuscript draft with the universal theorem.
- `universal_two.md`, `lower.md`, `tight_two_lower.md`: full proofs and parameter families. `universal_two_independent_audit.md` and `adversarial_universal_two_20260930.md` record independent reviews. The historical four-cycle note `upper.md` is not required for this handoff.
- `meta.md`, `bounded_overlap_theorem.md`, `nonlinear_kappa_two_independent.md`, `final_audit_and_value.md`: abstract lifting, exact algorithms, and novelty and scope audit.
- `r_menu_solver.py`, `bounded_overlap.py`, `test_r_menu.py`, `test_four_seed.py`, `tight_two_family.py`: minimal reproducible implementation and tests.
- `tight_two_M1000.json`, `six_client_lower_instance.json`: matching examples on both sides of the overlap threshold.

Exploratory MILP runs, floating-point logs, unrelated nonlinear experiments and earlier attempts have been deliberately left out of the handoff.
