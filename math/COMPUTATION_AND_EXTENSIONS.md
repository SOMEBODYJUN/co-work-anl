# Exact computation, complexity boundary, and cost extensions

These results are mathematically distinct from the universal finite-menu construction. See [`MODEL.md`](../MODEL.md) and [`LOCAL_GAME.md`](LOCAL_GAME.md) for the exact customer game. “Internally derived” below does not mean externally refereed.

## C1. True local extrema are weakly NP-hard

Let $m_1(A,B;w)$ minimize facility 1's expected load over **all** independent mixed customer NE of one fixed pair. [`astra_alg/hardness_proof.md`](../astra_alg/hardness_proof.md) gives an explicit chain from SUBSET SUM to 2-bounded subset sum, then to deciding whether some NE has gap $\Delta\le-Q$, using variable customers of weights $Q+a_i$ and $n+1$ anchor customers of weight $Q$. The reduction excludes $\Delta<-Q$, while at $\Delta=-Q$ the variable statuses pure-1 / mixer / pure-2 encode coefficients $0/1/2$. A complement-and-extra-common-customer step makes both private loads zero. The support-cell description L1 supplies polynomial-size rational certificates, including the one-mixer interval. Thus the threshold decision is NP-complete and exact $m_1$ is **weakly** NP-hard in binary input.

This is a barrier only to a direct general exact-$m$ oracle; it proves **nothing** about hardness of finding one global $\phi$-SPE. The candidate finite-menu algorithm avoids $m$ entirely. It is coherent for the exact-$m$ DP below to be pseudo-polynomial.

## C2. Three exact ways to compute local equilibria

| Method and exact scope | Mechanism / complexity | Deliverable and limit |
| --- | --- | --- |
| **Integer-weight threshold DP:** common $w_i\in\mathbb Z_{>0}$, $W=\sum_iw_i$; private $A,B$ may be rational. | Sort weights, choose gap sign and cutoff; propagate states `(number of mixers, signed pure weight)`. $O(n^2W+n\log n)$ rational operations, $O(n^2W)$ witness memory as implemented. | Full gap spectrum, local minimum, quota witness. Pseudo-polynomial in $W$, not binary-length polynomial. [`astra_alg/exact_algorithms.md`](../astra_alg/exact_algorithms.md) §§1–2 and [`threshold_dp.py`](../astra_alg/threshold_dp.py). |
| **Distinct-weight FPT reduction:** $d$ different positive rational common weights, explicitly listed customers. | Fix sign, cutoff and mixer count; use at most (2d) integer class-count variables in fixed-dimensional ILP. Claimed $2^{O(d^3)}\operatorname{poly}(n,L)$ time. | Mathematical reduction, **no implementation**. Binary-encoded multiplicities are outside its stated input model. Same proof note §3. |
| **Meet-in-the-middle (MITM):** arbitrary positive rational common weights. | Split ternary support states in halves and search sorted signed-sum tables around a single-valley load objective. $\operatorname{poly}(n)3^{\lceil n/2\rceil}$ time/space per pair. | Exact local minima and an exponential full-game *instance optimum* solver in [`astra_ring/mitm_solver.py`](../astra_ring/mitm_solver.py); lazy ring pruning in [`run_lazy_ring.py`](../astra_ring/run_lazy_ring.py) has no polynomial worst-case oracle bound. |

The bounded-overlap solver uses the direct $3^k$ L1 support enumeration rather than the MITM optimization. Let $\kappa=\max_{s\in U_1,t\in U_2}|C_s\cap C_t|$. It computes **the actual optimal factor** $\alpha^*$ over all pure facility layouts and all independent mixed customer NE continuation selections in

$$
 O(|U_1||U_2|[n+\kappa3^\kappa])
$$

exact rational operations, up to ordinary incidence processing. At every pair the $3^k$ support cells are rational points or intervals. Their extrema give the true threats $(D_1(t),D_2(s))$. On any attainable first-load interval ([a,b]), the objective

$$
 \max\{1,D_1(t)/x,D_2(s)/(V-x)\}
$$

is minimized at $x=\operatorname{clamp}_{[a,b]}(VD_1/(D_1+D_2))$ when $D_1+D_2>0$, with explicit zero conventions. Enumerate all cells and layouts; choosing attaining punishments yields a compact certificate. This is `EXACT-KAPPA` in [`asym_research/bounded_overlap_theorem.md`](../asym_research/bounded_overlap_theorem.md) and [`bounded_overlap.py`](../asym_research/bounded_overlap.py). It is polynomial if $\kappa\le2$, but generally exponential in $\kappa$. A short certificate proves attainment; exact *optimality* also needs the exhaustive support argument.

## C3. Abstract rational-polyhedral continuation selection

[`asym_research/nonlinear_kappa_two_independent.md`](../asym_research/nonlinear_kappa_two_independent.md) gives a separate **unimplemented** theorem: for finite two-leader games with nonnegative leader payoffs and independently selectable continuations, if the attainable continuation payoff set at every labeled action pair is explicitly presented as a polynomial-size union of rational polytopes, rational linear programming computes coordinate minima and the optimal first-stage stability factor by minimizing the maximum of two payoff ratios on each polytope. Producing a customer-continuation witness additionally needs an effective realization routine, with its running time counted separately. It also works through an application with $\kappa\le2$ for certain facility- and location-dependent nonlinear customer costs whose finite realized-load evaluations are rational with polynomial bit length. Treat the explicit polyhedral representation and representation-size proof as indispensable hypotheses. This result is not a general polynomial solver for arbitrary nonlinear games or arbitrary overlap. The reviewed document is a proof note, not tested software.

## C4. Quadratic equilibrium equivalence

For exactly two facilities and mandatory participation, customer (i) may use its own cost $f_i(z)=a_i z^2+b_i z+c_i$, with $(a_i,b_i\ge0)$, $a_i+b_i>0$, **provided it uses the same $f_i$ at both facilities**. Conditional on the other customers' realized actions, its two counterfactual loads $(X,Y)$ obey $X+Y=V+w_i$. Hence

$$
 f_i(X)-f_i(Y)=(a_i(V+w_i)+b_i)(X-Y),
$$

where the multiplier is strictly positive and independent of others' actions/recommendations. Therefore all pure NE, independent mixed NE, CE and CCE constraints are identical to the linear model at each layout. This **algebraic lemma** is independent of the global theorem; a global $\phi$ consequence remains conditional on `SC-PHI-E`, and a heterogeneous factor-2 consequence on `HC-2-UP`. See [`astra_ext/results.md`](../astra_ext/results.md).

The equivalence does **not** follow for arbitrary convex costs: private weight $1$ at the first facility and two common weights $(2,3)$ have a linear mixed NE at probabilities $(1/4,1/3)$, but with cubic cost the weight-2 customer's conditional costs are $90$ versus $86$. This refutes mixed-equilibrium preservation, not a global cubic approximation theorem. Three facilities, exit, and facility-specific functions also break the two-option constant-sum argument.

The heterogeneous **pure** upper and strict lower bounds admit a different extension to each customer's strictly increasing realized-load function, same at either facility: pure action comparisons preserve their order pointwise. This does not assert preservation of *mixed* equilibrium sets. It is described in the heterogeneous manuscript and should remain a different claim from the quadratic full-correspondence equivalence.

## C5. Reproducibility and limits

`threshold_dp.py` reproduced 530 full-spectrum small cases against ternary enumeration; `mitm_solver.py --self-test` reproduced 435 pair objectives and 12 full games. `asym_research/test_r_menu.py`, `test_four_seed.py` and `common_phi_counter_audit.py` exercise different constructs and were rerun in this curation pass. These are finite code checks, never proof premises. The DP helper formerly accepted a truncated probability vector; commit `70026ad` corrected its length check. `bounded_overlap.verify()` checks finite attainment certificates but does not certify its negative `finite_factor_exists=False` reports independently; in the valid two-facility linear model the candidate universal factor-2 theorem would make that branch unreachable.

The old MITM README mentions absent benchmark files, and some older notes still call the global polynomial $\phi$ construction open. Their mathematics can remain provenance, but their dated frontier text is superseded by the current **candidate**, not by an externally accepted theorem. See [`PROVENANCE.md`](../PROVENANCE.md).
