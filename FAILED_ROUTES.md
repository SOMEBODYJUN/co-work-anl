# Failed routes and sharp obstructions — 2026-09-30

Each entry distinguishes a false statement from an unproved or expensive method. Never infer mathematical failure from a timeout.

## F1. Use the exact minimum over all local customer equilibria as a polynomial oracle

- **Attempt:** compute `m(s,t)` exactly at every layout, form `d(t)=max_s m(s,t)`, then follow the response cycle.
- **Mechanism and obstruction:** `astra_alg/hardness_proof.md` reduces 2-bounded subset sum to existence of a local NE below a specified load, even with zero private loads. Integer-weight `threshold_dp.py` uses `O(n^2 W)` operations; `astra_ring/mitm_solver.py` remains exponential in overlap. Thus the direct exact-`m` implementation has no established bit-polynomial bound, unless P=NP under the reduction.
- **Salvage:** these routines compute exact instance optima on manageable inputs and provide independent checks. The fixed finite menu `F(s,t)` bypasses the need to calculate `m`; local hardness says nothing about the complexity of finding one `phi`-SPE.
- **Revisit if:** a structural input restriction bounds total weight, common-customer count or the number of distinct weights.

## F2. Replace a true minimum with arbitrary punishment upper bounds without changing the proof

- **Attempt:** retain a few feasible customer equilibria and use their payoffs as upper bounds for `m` while copying the original maximin cycle argument.
- **Failure:** the edge implication needs *all* witnesses in the chosen set to satisfy a responder-load bound. Arbitrary retained equilibria do not imply the relevant quantifier for another on-path equilibrium. Unbounded lazy refinements are not a polynomial algorithm.
- **Salvage:** `common_phi_algorithm.md` proves a particular *fixed* menu is complete for every witness invoked by the global contradiction; the `u`-based argument is a new proof obligation, not a formal substitution `m=u`. `astra_ring/run_lazy_ring.py` retains sound pruning and useful exponential exact certificates.

## F3. Restrict strong-chord witnesses to at most two genuinely mixing customers

- **False statement:** all relevant local two-position quota witnesses need at most two mixers.
- **Counterexample:** private loads `40,39`, three common customers each of weight `20`, reaches `100,99`. Exact support enumeration leaves only the three-mixer load pair `(277/4,279/4)` meeting both strong-chord quotas; its probabilities are `(39/80,39/80,39/80)` for facility 1. Pure and two-mixer load pairs fail. See `asym_research/common_phi_counter_audit.md` and `strong_cross_chord_arbitrary_n_proof.md`.
- **Salvage:** `astra_local/construct.py` handles arbitrarily many common customers; do not trim its mixed-support branch for an unproved speedup.

## F4. Apply the shared-catalog `phi` theorem to unequal catalogs

- **False scope extension:** `SC-PHI-v2` implies a universal `phi` guarantee when `U1 != U2`.
- **Counterevidence:** `asym_research/tight_two_lower.md` supplies a six-vertex positive-integer family with optimum `(2M+10)/(M+14) -> 2` for a 2-by-2 heterogeneous catalog; all local equilibria are uniquely resolved. Its scope excludes a common catalog and so does not contradict `SC-PHI-v2`.
- **Salvage:** `HC-2-v1` has a separate factor-2 construction and matching lower family. One-common-customer and a short catalog allow the more precise `rho` theorem.

## F5. Generalize quadratic-cost equivalence to all convex congestion costs

- **False statement:** any strictly increasing convex realized-load function preserves the linear model's mixed customer NE.
- **Counterexample:** `astra_ext/results.md` gives a three-customer cubic-cost example whose linear mixed equilibrium ceases to be an equilibrium. The quadratic proof uses the exact two-facility constant-sum identity; it also fails to cover exit options, customer-specific facility functions or three facilities.
- **Salvage:** the precise customer-specific quadratic equivalence is a useful conditional extension under mandatory participation.

## F6. Treat small searches or MILP timeouts as theorem evidence

- **Attempt:** infer a factor bound for arbitrary 3-by-3 catalogs from the absence of a counterexample in a bounded strict-uniqueness MILP class.
- **Failure type:** `asym_research/three_by_three_search_status.md` records time limits with no incumbent, not infeasibility certificates; the encoded family does not cover multiple customer equilibria. Numerical near-ties can be solver artifacts.
- **Salvage:** any candidate must be rechecked with exact rational full-equilibrium enumeration. The general heterogeneous factor 2 has a separate proof; the sparse arbitrary-by-arbitrary `rho` question remains open.
