# Two-stage facility location with weighted atomic customers

Research checkpoint: 2026-09-30. This repository is a **research record**, not a claim of external peer review. Start with this map, then `RESEARCH_STATE.md`, `CLAIMS.md`, and `FAILED_ROUTES.md`. The main shared-catalog theorem and the heterogeneous-catalog theorem are internally audited manuscript claims; the exact code certificates can be checked independently of their universal proofs.

## Research goal

Determine the best universal approximation factor for a pure first-stage, exact-customer-Nash subgame-perfect outcome, and construct such an outcome in time polynomial in the *binary input length*. The primary problem has **two facilities with the same finite location catalog**. A separate, genuinely different problem gives each facility its own catalog. The shared-catalog target is the golden ratio `phi=(1+sqrt(5))/2`; the heterogeneous target is 2. Neither result says that a particular instance's optimal factor is computed by its fast constructor.

## Mathematical objects and definition map

Let `G` be a finite set of customers, `w_g>0` their weights, and `C_s subset G` the customers who can reach location `s`. The input explicitly lists locations and incidence sets. A covered customer must choose one of the facilities at a reachable location; uncovered customers abstain. Facility payoffs are expected served weight. Customers minimize the expected **realized** total weight at their chosen facility and may independently mix. The same customer must evaluate both options with the same linear cost rule. Locations may coincide and may cover no customers.

For a labeled layout `(s,t)`, put `A=w(C_s\C_t)`, `B=w(C_t\C_s)`, and list common weights `w_1,...,w_k` from `C_s intersection C_t`. If customer `i` chooses facility 1 with probability `p_i`, its expected loads are `x=A+sum_i w_i p_i`, `y=B+sum_i w_i(1-p_i)`. With `Delta=x-y`, an independent mixed customer NE satisfies

- `p_i=1 => Delta<=w_i`;
- `p_i=0 => Delta>=-w_i`;
- `0<p_i<1 => Delta=w_i(2p_i-1)`.

At each labeled layout one may choose an exact customer NE independently. The facilities' on-path choices `(s,t)` form an `alpha`-approximate pure-location SPE when no unilateral change of a permitted location raises that facility's continuation payoff by more than factor `alpha`. This is an **existential continuation-selection** definition, not robustness against all customer equilibria.

Definitions depend as follows:

```text
incidence + weights -> private/common loads -> exact local customer NE
                  -> labeled continuation selection -> facility deviation inequalities
                  -> alpha-SPE certificate
```

For the shared catalog `S`, `m(s,t)` is the *true* minimum payoff to the facility at `s` over all exact independent customer NE at `(s,t)`, and `d(t)=max_{s in S} m(s,t)`. The fast constructor instead uses a fixed finite menu `F(s,t)` and its own menu minima `u(s,t)`; **`u` and `m` are different quantities**. The proof's key obligation is that the response-cycle contradiction needs only witnesses from `F`, plus independently proved uniqueness at two special steps. `common_phi_algorithm.md` records the precise transfer. In the heterogeneous paper, a different four-seed *pure* menu supports factor 2; do not conflate the two menus.

## Claim map and real dependencies

| ID | Exact scope and current status | Principal dependencies |
| --- | --- | --- |
| `P-2024-LB` | **Paper fact:** Krogmann et al. prove that no universal factor below `phi` is possible for weighted two-facility instances; they leave tightness open. | IJCAI 2024, Theorems 5–6. |
| `SC-PHI-v2` | **Internally audited manuscript claim:** for a finite shared catalog and positive binary rational weights, construct an exact-customer-NE `phi`-SPE in bit-polynomial time, `O(N^2(n+1)^4)` rational operations. | Local guarded repair; two-mixer and strong-chord witnesses; static-menu quantifier audit; full response-cycle proof. |
| `LOCAL-HARD-v1` | **Proof manuscript:** computing a particular facility's *minimum* local NE payoff is weakly NP-hard, even with zero private loads. | 2-bounded subset-sum reduction and NP membership. It does not imply global construction hardness. |
| `HC-2-v1` | **Internally audited separate manuscript claim:** arbitrary finite, possibly unequal catalogs admit a bit-polynomial pure-continuation factor-2 construction; a positive-integer family approaches 2. | Four-seed guarded repair; legal cross-color chords; independent lower-family calculation. |
| `HC-RHO-v1` | **Internally audited separate manuscript claim:** if one catalog has at most two choices and every cross pair has at most one common customer, the sharp factor is `2 cos(pi/7)`. | Restricted response-core lift and six-customer lower family. |
| `QUAD-v1` | **Algebraic result, conditional application:** with two facilities and mandatory participation, each customer's same strictly increasing quadratic cost at both facilities preserves the full customer equilibrium correspondence; hence `SC-PHI-v2` transfers if its theorem is accepted. | Constant-sum counterfactual loads; see `astra_ext/results.md`. |

The exact statements, quantifiers, evidence, objections, and versions are in `CLAIMS.md`. The main chain is:

```text
local customer NE + guarded repair
    -> local strong-chord existence -> polynomial local exchange constructor
    -> fixed menu F + two uniqueness arguments
    -> arbitrary response-cycle contradiction -> shared-catalog phi theorem
    -> certificate generator + direct exact verifier
```

The heterogeneous four-seed/2 chain is separate. Its lower bound does **not** refute the shared-catalog `phi` claim. `LOCAL-HARD-v1` motivates bypassing full local minima, but is not a premise in either upper-bound proof.

## Research frontier and next actions

1. Obtain an external, genuinely independent line-by-line proof review of the full shared-catalog cycle, static-menu substitutions, strong-chord exchange termination and bit complexity. An internally audited proof is a high-value **candidate**, not a refereed theorem.
2. Give the implementation a usable input contract, adversarial tests that make the global output use two-mixer/strong-chord cases, performance measurements at larger rational bit lengths, and a separate verification entry point. Present tests as implementation evidence only.
3. Check current related work and write a precise contribution comparison: the IJCAI paper already has the lower bound, a stated general `k` upper bound, pure local repair, and short continuation certificates. The new algorithmic claim is the static-menu bit-polynomial construction for the shared-catalog tight threshold.
4. For follow-on theory, study the one-common-customer heterogeneous case with both catalogs arbitrarily large, or seek a genuinely reusable abstract finite-menu theorem. The general heterogeneous factor 2 is already tight, so reducing it without an added assumption is impossible.

The current paper may be useful as a **research algorithm** for a matching incidence/weight model. It is not yet a validated general facility-location library or an implementation of instance-optimal `alpha`. See `USAGE.md` for exact input and certificate conditions.

## File map: shared-catalog core

Paths are repository-relative and complete. The final column says when to open the file.

| Path | Mathematical asset and reason to retain it | Read when |
| --- | --- | --- |
| `phi_n_manuscript/main.tex` | Current 25-page integrated proof of `SC-PHI-v2`: model, fixed menu, response-cycle analysis, arbitrary common-customer chord, local exchange algorithm, complexity. **Primary proof source.** | Auditing or revising the main theorem. |
| `phi_n_manuscript/main.pdf` | Rendered reading copy of the same draft; source above controls corrections. | Sharing a review copy. |
| `phi_n_manuscript/README.md`, `phi_n_manuscript/build_manuscript.py` | Build and prior compilation record; no mathematical authority beyond the source. | Rebuilding the PDF. |
| `phi_global_proof_candidate.md` | Earlier existence-oriented derivation and detailed cycle cases; Section 3.2's extremal selection is **not** an algorithmic premise. | Tracing the origin of a manuscript inequality. |
| `strong_cross_chord_arbitrary_n_proof.md` | Local two-position existence/iff with arbitrarily many common customers and three-mixer boundary. | Rechecking the difficult local lemma. |
| `common_phi_algorithm.md` | Exact finite-menu theorem, witness families, quantified `m` to `u` substitution, arithmetic and bit bound. | Checking why the code avoids an NP-hard oracle. |
| `common_phi_algorithm.py` | Exact-rational shared-catalog constructor and direct certificate verifier for `SC-PHI-v2`. | Running or auditing the algorithm. |
| `test_common_phi_algorithm.py`, `common_phi_algorithm_verification.json` | Seeded 753-game regression and observed menu-family counts; no universal proof. | Reproducing implementation checks. |
| `common_phi_counter_audit.py`, `asym_research/common_phi_counter_audit.md` | Independent conditional-cost enumeration and adversarial quantifier audit; identifies a necessary three-mixer local witness. | Attacking menu completeness or local NE checks. |
| `asym_research/common_phi_menu_quantifier_audit.md` | Line-by-line mapping of global proof witnesses to finite-menu members, including uniqueness steps. | Auditing the algorithmic transfer. |
| `astra_local/local_chord_algorithm.md`, `astra_local/construct.py`, `astra_local/verification.json` | Polynomial local exchange theorem, executable constructor and branch check record. | Checking the strong-chord call and bit-time claim. |
| `astra_alg/hardness_proof.md`, `astra_alg/hardness_enum.py` | Weak NP-hardness reduction for true local extremal NE load; small independent enumerator. | Understanding the precise computational obstruction. |
| `astra_alg/exact_algorithms.md`, `astra_alg/threshold_dp.py` | Integer-weight pseudo-polynomial spectrum algorithm and distinct-weight FPT reduction; exact oracle alternatives. | Working with restricted local weights. |
| `astra_ring/README.md`, `astra_ring/mitm_solver.py`, `astra_ring/run_lazy_ring.py` | Exponential exact local/global optimum solver and a sound but worst-case-exponential pruning variant. | Computing instance-optimal factors or independent small-case comparisons. |
| `astra_ring/example.json`, `astra_ring/example_optimal_certificate.json`, `astra_ring/example_ring_certificate.json` | Tiny reproducible instance and two exact certificates. | Testing output semantics. |
| `astra_ext/results.md`, `astra_ext/extension_report.md` | Precise quadratic-cost equivalence, its limits, and a historically separate heterogeneous lower example. | Extending customer costs without silently changing the model. |
| `common_phi_example_certificate.json`, `common_phi_iff_audit.py` | Example output and focused strong-chord audit. | Regression and debugging. |

## File map: heterogeneous companion

See the second block of `CLAIMS.md` and `asym_research/README_HANDOFF.md` before using these results. They concern different allowed sets and have their own manuscript, solver, lower-bound family, and exact overlap-parameter algorithm. Their individual paths and roles appear in that handoff and the companion table in `RESEARCH_STATE.md`. This is a companion line, not an unannounced strengthening of `SC-PHI-v2`.

## Working conventions

Keep exact theorem identity when changing catalog scope, participation, costs, quantifiers, or equilibrium concept: create a new claim version. Finite computations do not prove universal claims; a timeout is no mathematical evidence. Commit and push each meaningful checkpoint. Keep generated build intermediates and duplicate transfer ZIPs out of Git.
