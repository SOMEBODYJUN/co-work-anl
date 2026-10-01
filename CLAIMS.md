# Versioned claim registry

Curation checkpoint 2026-10-01. **Status terms:** `paper fact` means a cited paper actually states a claim at a specified location; `direct derivation` means a short displayed proof is recorded; `internally audited candidate` means a manuscript and internal attacks exist without independent external certification; `implemented/checked` is bounded software evidence. This registry fixes mathematical identity, not an AI confidence score. Definitions M1–M4 are in [`MODEL.md`](MODEL.md); joint-premise hyperedges are in [`research/graph.json`](research/graph.json).

## Shared-catalog branch

### `PF-IJCAI-LB` — published lower bound

- **Exact statement / quantifiers:** for every $\epsilon>0$, the weighted atomic two-facility model has an instance with no $(\phi-\epsilon)$-approximate SPE. Krogmann et al. state that tightness remains open. This is a universal-factor lower bound, not complexity hardness at $\phi$.
- **Objects/domain/assumptions:** the cited paper's host-graph game and exact customer NE; Theorem 5/Figure 7. Its shared-catalog reading and perturbation to rational weights are **additional manuscript interpretations**, not part of the bare published statement.
- **Dependencies/evidence/objections:** published paper in [`LITERATURE.md`](LITERATURE.md); common/rational mapping in `phi_n_manuscript/main.tex` §1 requires independent scope check.
- **Status/related files:** `paper fact` for published statement, `candidate interpretation` for shared/rational transfer; related `SC-PHI-SHARP`.

### `SC-PHI-E` — shared-catalog existence

- **Exact statement / quantifiers:** for **every** finite nonempty shared catalog $U_1=U_2=S$, finite explicit customer incidence family, and positive real atomic weights under M1–M3, **there exist** pure first-stage locations and a full selection of exact independently mixed customer NE at all labeled layouts such that no facility's unilateral gain exceeds $\phi=(1+\sqrt5)/2$.
- **Definitions/scope/conclusion:** existential continuation selection, co-location legal, arbitrarily many sites/customers/mixers. No claim for every selection or for the instance-optimal factor.
- **Joint dependencies:** P/E/T/C local witnesses, true uniqueness at two branches, full-catalog menu threats, arbitrary closed-cycle contradiction and S2 certificate completion. See [`math/SHARED_PHI.md`](math/SHARED_PHI.md) and manuscript §§2–13, Appendices A–B.
- **Evidence/counterevidence/status:** 25-page integrated proof, internal menu-membership audit and finite adversarial checks; no known fatal objection, no external line-by-line review. `internally audited candidate`. The old exact-$m$ existence proof is history, not a premise. Related files: `phi_n_manuscript/main.tex`, `asym_research/common_phi_menu_quantifier_audit.md`.

### `SC-PHI-A` — shared-catalog bit-polynomial construction

- **Exact statement / quantifiers:** for **every** `SC-PHI-E` input with positive **binary rational** weights and explicit incidence/shared catalog $S$, a deterministic algorithm constructs a $\phi$-SPE in $O(|S|^2(n+1)^4)$ exact rational operations with polynomial intermediate bit length. Output: rational on-path and at most $2|S|-2$ actual unilateral-deviation continuations plus a polynomial pure-NE default rule.
- **Assumptions/definitions/scope:** fixed menu $F(s,t)=P\cup E\cup T\cup C$, menu minima $u$, full-catalog threats $d_F$. $m(s,t)\le u(s,t)$, equality not asserted. Final scan chooses the best **within $F$**, not the instance's globally optimal $\alpha^*$.
- **Joint dependencies/evidence:** menu-cycle existence proof, `LOCAL-CHORD-POLY`, guarded repair, exact comparisons/bit bounds; manuscript §14, `common_phi_algorithm.py`, 753 complete seeded certificates and 10,206 local menu cases.
- **Objections/status:** existing complete-game tests chose no C on-path witness; independent checker and large-bit benchmarks pending. `internally audited candidate + research implementation`, not externally validated library.

### `SC-PHI-SHARP` — conditional matching threshold

- **Exact statement/quantifiers:** the optimal universal approximation factor in the shared-catalog positive-rational class is $\phi$.
- **Joint premises:** `SC-PHI-E` upper bound **and** `PF-IJCAI-LB`'s shared-catalog/rational interpretation. Neither alone establishes equality. The heterogeneous sharp-2 lower example is outside this class.
- **Evidence/objection/status:** manuscript §1's strict-inequality perturbation and published Theorem 5; `conditional candidate` pending independent upper and transfer reviews.

### `LOCAL-CHORD-IFF` and `LOCAL-CHORD-POLY`

- **Exact statements:** for one two-location customer game with reaches $U\ge V>\phi U/2$, common mass $C<qV$, $q=1/\phi$, maximum common weight $x$, an exact NE meeting $(L_U\ge qV,L_V\ge qU)$ exists **iff** $x\le U-qV$ or $C-x\ge U-V$. `LOCAL-CHORD-POLY` constructs such a witness when it exists in $O((k+1)^4)$ rational operations with polynomial bit length. Menu C uses only the sufficient extra condition $x\le(1-q)U$.
- **Objects/assumptions/scope:** distinct atomic common customers, independent NE, actual pair reaches; zero-common/equality conventions in manuscript Appendix A. This is local, not a global SPE assertion.
- **Dependencies/evidence/objections:** M2 equations, three-mixer branch, pure repair, pair-endpoint box-slice exchange and pivot/flip termination in manuscript Appendices A–B; `astra_local/construct.py` branch tests. `internally audited candidate`; pair-local optimum is not a global quadratic maximum. The 40/39 three-weight-20 instance refutes a two-mixer shortcut.

### `MENU-COVERAGE` and `CERT-SOUND`

- **`MENU-COVERAGE` exact obligation:** under failure of an $F$-quota witness and a full-catalog maximizing response cycle, **every equilibrium constructed for the cycle contradiction** belongs to the precomputed fixed menu, except two steps that establish actual all-NE uniqueness by strict dominance. It is **not** the assertion $u=m$. Source manuscript §§2–14 and `asym_research/common_phi_menu_quantifier_audit.md`; status central internally audited proof obligation, external reconstruction pending.
- **`CERT-SOUND` exact statement:** for a **particular valid input**, an on-path exact NE and exact NE after each actual unilateral deviation satisfying ratio $\alpha$ extend to a full $\alpha$-SPE by a prescribed deterministic pure-NE default. This direct criterion does not assume the universal theorem. `verify_phi_certificate.py` calls the same checker and ignores textual default metadata, so it is not an independent implementation or a checker of arbitrary supplied defaults. Status direct mathematical criterion with code-level checks; source `MODEL.md` M3 and `common_phi_algorithm.py:verify`.

## Heterogeneous-catalog branch

### `HC-2-UP`, `HC-2-LOW`, `HC-2-SHARP`

- **Upper exact statement:** for **every** finite nonempty $(U_1,U_2)$, possibly unequal/disjoint, positive rational atomic weights and arbitrary incidence under M1–M3, construct a pure-location factor-2 SPE with **pure exact customer NE at every continuation** in $O(|U_1||U_2|(n+1)^2)$ rational operations and polynomial bit lengths, using at most four guarded seeds per legal pair.
- **Lower exact statement:** for **every** $\alpha<2$, sufficiently large integer $M>4$ in the six-vertex graph H2 of [`math/HETEROGENEOUS.md`](math/HETEROGENEOUS.md) gives disjoint 2-by-2 catalogs, two common customers per legal pair and exact $\alpha^*(M)=(2M+10)/(M+14)>\alpha$. Every local NE/CE/CCE is uniquely pure, so mixing/correlation cannot evade it.
- **Sharp conclusion/dependencies:** unrestricted heterogeneous universal optimum equals 2 **jointly** from the upper and lower. Upper depends on full-catalog threats, four-seed completeness, legal opposite-color chords and both arbitrary-cycle branches; lower depends on pointwise dominance and an exact improvement matrix. Neither imports `SC-PHI-E`.
- **Evidence/objections/status:** `asym_research/paper/main.tex`, `tight_two_lower.md`, `r_menu_solver.py`, exact tests and internal attacks; no fatal mathematical issue found, external proof/priority review pending. Illegal-layout certificate bug corrected in commit `70026ad`. IJCAI Observation 4 already **states** a general $k$-approximation; first use of numeric 2 is not claimed. `internally audited candidates`.

### `HC-RHO`

- **Exact statement/quantifiers:** for **every** heterogeneous instance satisfying **both** $\min(|U_1|,|U_2|)\le2$ and $\kappa=\max_{s\in U_1,t\in U_2}|C_s\cap C_t|\le1$, the sharp universal factor is $\rho=2\cos(\pi/7)$, largest root of $z^3-z^2-2z+1$. A polynomial pure-continuation upper construction exists; for every smaller factor a positive-rational/integer six-customer family excludes it even with mixed customer NE.
- **Dependencies:** single-common payoff classification, 2-by-2 bad-cycle cubic, fixed tie rule, retention of one best column for each of at most two rows, strict lower family. The other catalog may be arbitrarily large; **both** arbitrary is open.
- **Evidence/objections/status:** manuscript §8, `asym_research/lower.md` §§1–10, exact lower instance and internal checks; `internally audited candidate`. That note's §11 is superseded; two common customers allow factor 2.

### `CORE-LIFT` and `HC-MONOTONE`

- **Core-lift exact statement:** in a finite two-leader game with nonnegative payoffs, nonempty independently selectable continuation sets at each labeled pair and attained coordinate minima, a simple cycle of the full-game minimizing-payoff response map induces a balanced core preserving **full-game** threats; a stable core selection lifts to all actions. It is an existence reduction, not automatically efficient because true minima may be hard. Source heterogeneous manuscript §3 and `meta.md` §2A; `internally audited candidate`.
- **Monotone-cost statement:** the `HC-2-UP` and `HC-RHO` *pure* upper constructions and their strict lower families persist for each customer's same-at-both-facilities strictly increasing realized-load cost under mandatory participation. It does **not** preserve arbitrary mixed-NE sets. Source heterogeneous manuscript; `conditional extension`.

## Local computation and cost extensions

### `LOCAL-HARD`

- **Exact statement:** for one fixed pair with positive integer common weights, deciding if **some** exact independent mixed customer NE gives a designated facility load at most an input threshold is NP-complete, even with zero private loads. Exact local minimum computation is weakly NP-hard under binary input; no hardness of global $\phi$/2 construction follows.
- **Dependencies/evidence/status:** 2-bounded subset-sum reduction and support-cell NP certificate in `astra_alg/hardness_proof.md`; `internally audited proof candidate`, compatible with pseudo-polynomial `DP-W`.

### `DP-W`, `FPT-D`, `MITM-EXACT`, `EXACT-KAPPA`

| Claim | Exact domain, quantifier and conclusion | Evidence, status, objection |
| --- | --- | --- |
| `DP-W` | Every local pair with positive **integer** common weights totaling $W$, rational private loads: full equilibrium gap spectrum, extrema and quota witness in $O(n^2W+n\log n)$ exact operations. | `astra_alg/exact_algorithms.md` §§1–2, `threshold_dp.py`, 530 small exact checks; internally audited, **pseudo-polynomial**. |
| `FPT-D` | Explicit local rational-weight customers with $d$ distinct weights: local extrema/quotas in $2^{O(d^3)}\mathrm{poly}(n,L)$ using fixed-dimension ILP. | Same note §3; mathematical reduction, no implementation, binary multiplicities excluded. |
| `MITM-EXACT` | Every local rational-weight pair: exact single-valley gap objective in $\mathrm{poly}(n)3^{\lceil n/2\rceil}$ time/space; all-pair use computes global $\alpha^*$. | `astra_ring/README.md`, `mitm_solver.py`, 435 pair/12 full checks; implemented, exponential; short certificate alone proves attainment, not optimum. |
| `EXACT-KAPPA` | Every linear-cost two-facility game with arbitrary catalogs and max overlap $\kappa$: instance-optimal $\alpha^*$ over all independent mixed NE continuations and rational attaining certificate in $O(|U_1||U_2|[n+\kappa3^\kappa])$ exact operations plus incidence processing. | `asym_research/bounded_overlap_theorem.md`, `bounded_overlap.py`; internally audited, exponential in $\kappa$. |

Their common dependency is M2's complete ternary support representation, including the **one-mixer interval**. None depends on either universal upper-bound proof. Details: [`math/COMPUTATION_AND_EXTENSIONS.md`](math/COMPUTATION_AND_EXTENSIONS.md).

### `POLY-CONT`, `QUAD-EQ`, `QUAD-PHI`

- **`POLY-CONT`:** for finite two-leader games with **nonnegative leader payoffs** and independently selectable continuations at each labeled action pair, if each attainable continuation-payoff set is an **explicit polynomial-size union of rational polytopes** with polynomial-bit coordinates, rational linear optimization calculates coordinate minima and the optimal first-stage factor. Producing a full continuation witness additionally requires an effective payoff-to-customer-continuation realization procedure; its runtime is counted separately. The note also treats some nonlinear, facility/location-dependent costs with $\kappa\le2$ and rational polynomial-bit realized-load evaluations. Source `asym_research/nonlinear_kappa_two_independent.md`; `internally derived, unimplemented`, no general arbitrary-nonlinear solver claim.
- **`QUAD-EQ`:** for exactly two facilities and mandatory patronage, customer (i)'s *same at either facility* $a_i z^2+b_i z+c_i$, $(a_i,b_i\ge0, a_i+b_i>0)$, gives identical pure, independent mixed, CE and CCE customer equilibrium sets to linear realized-load cost at every layout. The pointwise counterfactual difference equals $(a_i(V+w_i)+b_i)(X-Y)$. `direct derivation`, source `astra_ext/results.md`.
- **`QUAD-PHI`:** the global shared-catalog $\phi$ statement transfers under `QUAD-EQ` **only if `SC-PHI-E` holds**. Cubic counterexample in [`FAILED_ROUTES.md`](FAILED_ROUTES.md) blocks generic convex-cost correspondence transfer.

## Version and evidence rule

Changing catalog quantifiers, cost symmetry, customer equilibrium concept, participation, input encoding or complexity creates a new claim version. Finite tests remain bounded observations. Internal agent reviews are evidence annotations with scope, not votes or proof premises. See [`EVIDENCE.md`](EVIDENCE.md).
