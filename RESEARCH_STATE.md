# Research state — 2026-09-30

## Active goal and current status

Primary goal: establish and make independently reviewable `SC-PHI-v2`, the sharp shared-catalog golden-ratio guarantee with a bit-polynomial construction and exact customer Nash continuations. An integrated 25-page LaTeX draft, exact-rational implementation, short deviation certificates, internal adversarial audit and reproducible tests exist. **Status is internally audited research manuscript, not externally accepted theorem.** The IJCAI 2024 lower bound is an external paper fact; the matching upper bound is our candidate.

The companion heterogeneous line `HC-2-v1` has a separate 17-page draft and exact pure-continuation constructor. Its tight factor 2 must not be substituted for the shared-catalog target. General 2 is already tight for heterogeneous catalogs. The sparse `HC-RHO-v1` result has the additional one-common-customer and short-catalog conditions.

## Frontier / proof obligations

1. **Static-menu global transfer:** rederive the arbitrary-length response-cycle contradiction using menu minima `u`, checking every edge's `forall e in F(s,t)` statement and the two points where a true unique NE is invoked. Read `phi_n_manuscript/main.tex` Sections 2–14 with `asym_research/common_phi_menu_quantifier_audit.md`. A single fatal counterexample blocks promotion.
2. **Strong chord and local exchange:** independently check all branch inequalities, degenerate weights and the polynomial pivot count in Appendix B and `astra_local/local_chord_algorithm.md`. A local three-mixer example makes any unproved two-mixer restriction invalid.
3. **Artifact readiness:** the CLI verifies its own output exactly, but the seeded full-game run has 662 pure, 88 half, 3 designated-two-mixer and **0 strong-chord on-path** outcomes. Build targeted global cases and independent verifier coverage of altered or missing certificates. Test runtime with large rational bit lengths and document actual resource usage. This is engineering evidence, not a way to prove the theorem.
4. **Publication positioning:** the original IJCAI paper states a `k` approximate upper bound and gives the `phi` lower bound. Verify the exact scope of that statement and later papers; distinguish earlier pure-repair ideas from the finite witness and bit-polynomial result. Related work in the draft is still short.

## Reliable current evidence and limits

- `common_phi_algorithm.py` checks conditional customer costs and all actual unilateral facility deviations using rational arithmetic. Its verifier does not rely on the global theorem; a valid certificate establishes the factor **for that instance**. The universal runtime/existence conclusion still depends on the full mathematical proof.
- `test_common_phi_algorithm.py` records 753 complete certificates with seed `2026093001`; `common_phi_counter_audit.py` checks 10,206 small local menus and 1,771 small full games. The three-mixer pair example is local, not a global hard-case witness.
- `astra_alg/hardness_proof.md` establishes a separate weak NP-hardness candidate for computing true local minimum NE payoff; it does not imply that our global constructive problem is NP-hard.
- `asym_research/tight_two_lower.md` gives an exact positive-integer family with optimum `2-18/(M+14)` for differing catalogs. It has no bearing on the shared-catalog `phi` lower bound.

## Next actions, in order

1. Invite an external proof auditor who first reconstructs the model, menu quantifiers and strong-chord obligation independently; record exact objections or approval scope.
2. Improve the user-facing algorithm artifact: document JSON schema, provide a standalone independent verification path, add difficult global examples and realistic bit-length benchmarks. A valid certificate is already useful even before the universal theorem is accepted.
3. Consolidate the shared and heterogeneous manuscripts into one paper only after checking both main proofs and the contribution/priority relationship; retain the separate claim identities and scopes.
4. If the first two stages hold, investigate a reusable abstract menu/response-cycle theorem. Otherwise salvage exact barriers, counterexamples or restricted cases rather than proclaiming a general breakthrough.

## Companion file map

| Exact path | Purpose and relevant claim |
| --- | --- |
| `asym_research/paper/main.tex`, `asym_research/paper/main.pdf` | Primary 17-page source and rendered draft of `HC-2-v1`, `HC-RHO-v1`, response-core lemma and bounded-overlap appendix. |
| `asym_research/README_HANDOFF.md`, `asym_research/paper/README.md` | Detailed independent entry points and manuscript build information. |
| `asym_research/universal_two.md`, `asym_research/universal_two_independent_audit.md`, `asym_research/adversarial_universal_two_20260930.md` | Arbitrary alternating-cycle proof and two independent internal attacks on general factor 2. |
| `asym_research/tight_two_lower.md`, `asym_research/tight_two_family.py`, `asym_research/tight_two_M1000.json` | Six-vertex positive-integer lower family, generator and reproducible instance for sharp 2. |
| `asym_research/lower.md`, `asym_research/six_client_lower_instance.json` | Restricted single-common sharp `rho` upper/lower analysis and explicit six-customer witness. |
| `asym_research/meta.md`, `asym_research/bounded_overlap_theorem.md` | Reusable closed-response-core lift and exact overlap-parameter solver theorem. |
| `asym_research/r_menu_solver.py`, `asym_research/test_r_menu.py`, `asym_research/test_four_seed.py`, `asym_research/four_seed_verification.json` | Four-seed pure algorithm and regression suite for `HC-2-v1`. The shared-catalog program imports its guarded-repair routine. |
| `asym_research/bounded_overlap.py`, `asym_research/nonlinear_kappa_two_independent.md` | Exact optimal-factor support enumeration for linear costs; separate unimplemented rational-polyhedral extension. |
| `asym_research/final_audit_and_value.md`, `asym_research/three_by_three_search_status.md` | Literature/scope/novelty audit and bounded exploratory search with explicitly inconclusive timeouts. |

