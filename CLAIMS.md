# Claim registry — exact identities, 2026-09-30

`Canonical record` here means the *statement and evidence are preserved accurately*; it does not mean the mathematical theorem has been externally certified. A change of quantifier, action set, cost rule, or conclusion requires a new version.

## `P-2024-LB` — external paper fact

- **Exact statement:** for every `epsilon>0` there is a weighted two-facility atomic-client instance without a `(phi-epsilon)`-approximate SPE, with `phi=(1+sqrt(5))/2`; the cited paper says tightness is open. The example uses a common location catalog (as checked in our manuscript); the rational-input transfer is justified by strict inequalities and small rational perturbations in `phi_n_manuscript/main.tex` Section 1.
- **Objects/domain/quantifiers:** finite two-stage facility game and continuation customer equilibria of Krogmann et al.; an existential hard instance for each positive epsilon. This is a *lower bound on universal approximation*, not a lower bound on one fixed instance or on exact computational complexity.
- **Dependencies/evidence:** Krogmann et al., IJCAI 2024, Theorems 5–6 and Figure 7; see `LITERATURE.md`.
- **Status:** paper fact for the published statement; the explicit common-catalog and rational perturbation interpretation remains part of our reviewed argument. **Related:** `SC-PHI-v2`, `HC-2-v1`.

## `SC-PHI-v2` — shared catalog, fixed-menu polynomial construction

- **Exact statement:** for every finite nonempty catalog `S` available to **both** facilities, every explicitly listed incidence family `C_s`, and all positive binary rational atomic weights `w_g`, one can deterministically output pure facility locations plus an exact *independently mixed* customer NE at every labeled layout, represented compactly by on-path and unilateral-neighbor probabilities and a polynomial default pure-NE rule. No permitted unilateral facility move yields more than `phi` times its on-path expected served weight. The algorithm uses `O(|S|^2(n+1)^4)` exact rational operations with polynomial intermediate bit lengths. All local customer equilibria are exact for original weights.
- **Assumptions/definitions:** mandatory participation for every covered customer; uncovered customers abstain; customer cost is expected realized load at the chosen facility; facility payoff is expected covered weight; mixed customers randomize independently. Same physical location can be chosen twice. `phi` is irrational but output probabilities and the certified instance factor are rational. The theorem constructs a *suitable* continuation selection; it does not claim every continuation selection works.
- **Dependencies:** guarded repair; half splitting at equal reaches; designated two-mixer template; `LOCAL-CHORD-v1` polynomial strong-chord construction; static menu `F(s,t)` and its menu-minimum response-cycle proof. It never computes the true local extremum `m(s,t)`. The imported lower bound `P-2024-LB` makes `phi` sharp conditional on this upper theorem.
- **Evidence:** integrated `phi_n_manuscript/main.tex` Sections 2–14 and Appendices A–B; `common_phi_algorithm.md` quantifier transfer; independent internal checks in `asym_research/common_phi_menu_quantifier_audit.md` and `asym_research/common_phi_counter_audit.md`; code and recorded exact tests.
- **Counterevidence/objections:** none known from current internal attacks. Still requires independent external reconstruction of the long global proof and stronger tests of difficult global branches. Small tests cannot justify the universal claim. The earlier existence-only draft is not independently a bit-polynomial construction.
- **Status:** internally audited **research theorem candidate**, implementation available, not peer reviewed or production qualified. **Related files:** `phi_n_manuscript/main.tex`, `common_phi_algorithm.py`, `test_common_phi_algorithm.py`, `README_MAIN_PHI.md`.

## `LOCAL-CHORD-v1` — polynomial local quota witness

- **Exact statement:** for a two-location customer game with reaches `R>=r`, common mass `W`, weights `w_i>0`, and the strong-chord hypotheses `r>phi R/2`, `W<r/phi`, `max_i w_i <= (1-1/phi)R`, an exact independent mixed customer NE can be constructed with loads at least `r/phi` at the `R` location and `R/phi` at the `r` location. A local exchange construction uses `O((k+1)^4)` rational operations and polynomial bit length for rational data.
- **Scope:** an auxiliary pair lemma, not a global SPE by itself; `k` may be arbitrary, including enough customers to require three genuine mixers. The equal-reach and zero-overlap branches follow the stated conventions in the manuscript.
- **Dependencies/evidence:** `strong_cross_chord_arbitrary_n_proof.md`, `astra_local/local_chord_algorithm.md`, `astra_local/construct.py`, `astra_local/verification.json`; internal review and branch tests.
- **Objections/status:** finite coverage and internal review only; the local exchange termination and sign inequalities require external audit. **Related:** `SC-PHI-v2`, `F3` in `FAILED_ROUTES.md`.

## `LOCAL-HARD-v1` — local extremal NE payoff hardness

- **Exact statement:** with positive integer common customer weights and nonnegative integer private loads, deciding if some independent mixed customer NE has signed load gap `Delta<=-Q` is NP-complete; the reduction can be made with both private loads zero. Therefore finding one designated facility's **minimum payoff over all local NEs** is weakly NP-hard under binary encoding. A pseudo-polynomial integer-weight DP remains possible.
- **Quantifiers/scope:** the decision threshold is part of the input, and the claim is about *one fixed two-location client game*. It neither establishes hardness of the global `phi` constructor nor proves strong NP-hardness.
- **Dependencies/evidence:** explicit 2-bounded subset-sum reduction and support-certificate membership in `astra_alg/hardness_proof.md`; `astra_alg/hardness_enum.py` sanity checks; compatible DP in `astra_alg/exact_algorithms.md` and `astra_alg/threshold_dp.py`.
- **Objections/status:** internally audited mathematical proof, external review pending. **Related:** finite-menu bypass in `SC-PHI-v2`, `F1` in `FAILED_ROUTES.md`.

## `HC-2-v1` — heterogeneous catalogs, sharp factor 2

- **Exact statement:** for all finite nonempty, possibly different facility catalogs `U1,U2`, all explicit incidence families, and positive rational weights under the same linear customer-cost and mandatory-participation model, there is a bit-polynomial construction of a pure first-stage factor-2 SPE with **pure exact customer NEs at all continuations**. The four guarded seeds per layout give `O(|U1||U2|(n+1)^2)` rational operations with polynomial bit lengths. For every `alpha<2` a positive-integer six-vertex instance with `U1 != U2` has no `alpha`-SPE even allowing mixed customer NEs. In the displayed family the exact optimal ratio is `(2M+10)/(M+14)` for `M>4`.
- **Dependencies/evidence:** arbitrary-length legal cross-color chord argument in `asym_research/universal_two.md`, independent audits, `asym_research/r_menu_solver.py` and tests, and uniqueness/lower proof in `asym_research/tight_two_lower.md`. The earlier IJCAI paper already *states* a general `k` upper bound; our claim is constructive coverage and a matching heterogeneous lower bound, not first use of the number 2.
- **Objections/status:** internally audited separate manuscript, external proof and priority review pending. **Related files:** `asym_research/paper/main.tex`, `asym_research/README_HANDOFF.md`, `asym_research/final_audit_and_value.md`.

## `HC-RHO-v1` — restricted heterogeneous sharp factor

- **Exact statement:** when `min(|U1|,|U2|)<=2` and every legal cross-facility location pair shares **at most one** customer, the universal factor is exactly `rho=2 cos(pi/7)`. There is a polynomial pure-continuation construction; a six-customer family rules out every smaller factor. The other catalog may have arbitrary finite size.
- **Dependencies/evidence:** `asym_research/lower.md`, `asym_research/paper/main.tex`, the response-core lift in `asym_research/meta.md`, and `asym_research/six_client_lower_instance.json`.
- **Objections/status:** internally audited; **open** whether the same rho holds when both catalogs have arbitrary size. It is false if the overlap bound is relaxed to two common customers, by `HC-2-v1`'s lower family. Do not silently extend its quantifiers.

## `QUAD-v1` — algebraic equivalence and conditional application

- **Exact statement:** for exactly two facilities, mandatory participation and the same per-customer quadratic `f_i(z)=a_i z^2+b_i z+c_i` at either facility, with `a_i,b_i>=0`, `a_i+b_i>0`, the best-response differences are a strictly positive scalar multiple of those under linear realized-load cost. Consequently pure NE, independent mixed NE, CE and CCE sets agree layout by layout. Facilities still maximize expected covered weight.
- **Dependencies/evidence:** for the two counterfactual loads `X+Y=W+w_i`, so `f_i(X)-f_i(Y)=[a_i(W+w_i)+b_i](X-Y)` pointwise. `astra_ext/results.md` gives the proof and a cubic counterexample.
- **Status:** direct internally checked algebraic lemma. Transferring the global shared-catalog `phi` theorem is **conditional on `SC-PHI-v2`**. No claim for three facilities, optional participation, or arbitrary convex costs.

## `EXACT-OVERLAP-v1` — instance-optimal factor under bounded overlap

- **Exact statement:** for the linear-cost two-facility game with explicit catalogs and `kappa` the maximum number of common customers at any legal pair, complete ternary support enumeration determines the **instance's optimal** continuation-selection SPE factor and an exact rational certificate in `O(|U1||U2|[n+kappa 3^kappa])` rational operations (with standard input-incidence processing and polynomial bit operations per arithmetic step).
- **Dependencies/evidence:** `asym_research/bounded_overlap_theorem.md` and `asym_research/bounded_overlap.py`; unlike the fast universal constructors, this does search the entire local equilibrium spectrum. The separate rational-polyhedral extension in `asym_research/nonlinear_kappa_two_independent.md` is mathematical only and has no solver implementation.
- **Status:** internally audited companion result; exponential in `kappa`, so not a bit-polynomial algorithm for unrestricted overlap.
