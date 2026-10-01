> **Historical research note (superseded navigation).** Preserve the derivation below as provenance; use [the current mathematical map](README.md), [claim registry](CLAIMS.md) and [source-status guide](PROVENANCE.md) for current scope.

# Shared-catalog golden-ratio research handoff

Research checkpoint, 2026-09-30. The proof and algorithm below have undergone internal independent audits; they have not been externally refereed. This handoff concerns **two facilities with the same explicitly listed finite location set** and positive rational atomic customer weights. It does not assert the same factor for different facility-specific location sets.

## Main result under audit

The manuscript `phi_n_manuscript/main.tex` gives a proof candidate that a golden-ratio approximate pure-location SPE exists for every finite shared catalog. The added finite-menu theorem constructs one in polynomial bit time with exact independently mixed customer Nash continuations. The conservative arithmetic bound is `O(N^2 (n+1)^4)`, where `N` is the number of shared locations and `n` the number of customers. Rational on-path and unilateral-deviation continuations plus a polynomial default rule specify the full SPE.

The polynomial algorithm minimizes only over a fixed menu of explicitly generated exact customer equilibria at each pair: guarded pure all/single-client seeds, equal-reach half splitting, two designated mixers, and one reach-based strong-chord witness. It does not compute the minimum over **all** local customer equilibria. The step-by-step quantifier substitution and the two genuine uniqueness arguments are documented in `asym_research/common_phi_menu_quantifier_audit.md` and independently attacked in `asym_research/common_phi_counter_audit.md`.

`common_phi_algorithm.md` is the concise algorithm theorem and proof map. The full global cycle proof is in `phi_global_proof_candidate.md`; its arbitrary-common-customer mixed chord lemma is in `strong_cross_chord_arbitrary_n_proof.md`; the local polynomial construction and exchange proof are in `astra_local/local_chord_algorithm.md`. The final manuscript combines these arguments.

## Run and verify

From the archive root:

```bash
python3 common_phi_algorithm.py astra_ring/example.json --output my_phi_certificate.json
python3 test_common_phi_algorithm.py
python3 common_phi_counter_audit.py
```

`common_phi_algorithm.py` uses `asym_research/r_menu_solver.py` for guarded repair and `astra_local/construct.py` for the strong chord. Its certificate verifier checks original-weight individual Nash conditions and every actual unilateral facility deviation, independently of the menu minima. The first test suite recorded 753 complete certificates, including 750 random rational instances. A separate adversarial suite checked 10,206 local menus and 1,771 small full games. Finite checks do not replace the global proof.

The command-line reader preserves JSON decimal and exponent weights as exact
rationals; programmatic callers should pass integers or exact strings, not
Python floats. Certificate checks remain active under `python -O`. The current
constructor scans all location pairs after establishing the response-cycle
guarantee, so it may return a smaller factor within its fixed menu.

## Literature and boundaries

Krogmann et al., IJCAI 2024, already provide the golden-ratio lower bound and state a general `k` upper bound. Their paper leaves tightness of the golden-ratio lower bound open. The theorem here, if accepted after external review, matches that lower bound in the shared-catalog case and strengthens existence to a bit-polynomial exact-client-NE construction. The method is compatible with weak NP-hardness of computing a specified facility's **minimum payoff over all** local customer equilibria, proved in `astra_alg/hardness_proof.md`, because it never computes that minimum.

The earlier six-vertex sharp-2 lower bound uses **different** catalogs for the two facilities and does not contradict this theorem. The algorithm does not compute the instance's optimal approximation factor, solve arbitrary quota feasibility, or assert a golden-ratio guarantee for heterogeneous catalogs. Independent external novelty and mathematical review remain necessary before publication claims.
