> **Historical research note (superseded frontier statements).** Preserve the derivation below as provenance; use [the current mathematical map](../../../README.md), [claim registry](../../../CLAIMS.md) and [source-status guide](../../../PROVENANCE.md) for current scope.

# Exact MITM solver and lazy maximin-ring certificates

Research checkpoint, 2026-09-30. No third-party Python package is required. All strategic calculations use `fractions.Fraction`; the output contains exact rational probabilities and loads. This code does **not** rely on a floating-point MILP optimum or on limiting the number of mixers.

## What is delivered

- `mitm_solver.py`: exact two-location load optimization by threshold decomposition and meet-in-the-middle (MITM), plus full-game exact `m`, `d`, an identified maximin ring, and globally optimal approximation factor `alpha` over all layouts and continuation selections.
- `run_lazy_ring.py`: an exact branch-and-bound implementation that computes only the `d` values encountered while following a maximin response path, then searches its cycle. It returns the optimum **within that cycle**, not a claimed global optimum.
- `example.json`: a small incidence-model instance.
- `example_optimal_certificate.json`, `example_ring_certificate.json`: generated exact outputs, including on-path and unilateral-deviation equilibria.
- `benchmark_mitm.py`, `benchmark_results.json`: four reproducible timing/state-count observations. These are empirical illustrations, not average-case guarantees.

For the example, full optimization uses 45 pair-oracle calls. The lazy ring route uses 6 pair-oracle calls, visits 3 locations, and prunes 12 potential responses. Both produce an exact SPE (`alpha=1`). This improvement is instance-specific.

## Run

From the project root:

```bash
python -m facility_spe.exact.mitm --self-test
python -m facility_spe.exact.mitm examples/shared/tiny.json
python -m facility_spe.cli.lazy_ring examples/shared/tiny.json
```

Input format:

```json
{"weights":["1/3",2,5], "locations":[[0,1],[1,2],[0,2]]}
```

Each location lists the zero-based customer indices that can access it. Weights must be positive. Locations may have empty coverage. Both facilities have this same location set. Private loads are computed by set differences; common customers retain their separate atomic identities. JSON decimal numbers and fraction strings are interpreted as exact rationals.

For a two-location query alone use `{"A":2,"B":3,"weights":[5,7,11]}`. `A,B` are forced private loads and `weights` lists the common customers. This returns the minimum load of the first facility and a witnessing mixed customer NE.

## 1. Exact structural reduction

Let private loads be `A,B`, total common weight `W`, total covered weight `F=A+B+W`, and let `Delta=L_A-L_B`. For a common customer of weight `w` choosing A with probability `p`, the difference between its conditional A and B costs is

`Delta + w(1-2p)`.

Therefore pure A requires `Delta<=w`, pure B requires `Delta>=-w`, and a mixer has `p=(1+Delta/w)/2`. We allow a designated mixer to have probability 0 or 1 at an endpoint. Such designations duplicate genuine pure equilibria and never add an invalid equilibrium.

Sort common weights decreasingly. For each cutoff `h`, take the first `h` customers as heavy and the rest as light, of total weight `ell`. Restrict `|Delta|` to the interval between the largest light and smallest heavy weight. At cutoff 0 the upper endpoint is `F`; at cutoff n the lower endpoint is 0. The bound `|Delta|<=F` is valid because both loads are nonnegative.

Every light customer must choose the lower-load facility. Every heavy customer has one of three states A, B, M. Define `k=#M` and `z=sum(pure-A weights)-sum(pure-B weights)`. With `sign=sign(Delta)` the single equation is

`(1-k) Delta = A-B-sign*ell+z`.

All individual Nash inequalities have become the cutoff interval. Equal-weight boundaries and `Delta=0` are covered by closed intervals. The special case `k=1` is essential: numerator zero gives the **whole** interval, and nonzero gives no equilibrium.

## 2. MITM algorithm and its actual guarantee

Split the heavy customers into two balanced halves. A half-table stores one witness per pair `(k,z)` and is grouped by `k`, with `z` sorted. Histories with the same pair are interchangeable because eligibility depends only on the cutoff and gap.

For each pair of half-group mixer counts, the gap equation is linear in `z_left+z_right`. A legal gap interval gives an interval of legal right sums. Two binary searches locate it. At most the two right sums immediately around a target sum need be checked for a single-valley objective. For `k=1`, a binary search seeks the exact cancelling sum, then the desired target is clamped into the whole allowed gap interval.

Minimizing `Delta` gives `m(A,B)`. Maximizing it gives the minimum B load. More generally this solves any objective nonincreasing up to one given target gap and nondecreasing thereafter.

**Worst-case theorem:** a pair with `n` common customers is solved in `poly(n) 3^{ceil(n/2)}` exact arithmetic operations and `poly(n) 3^{ceil(n/2)}` space. The bit lengths of all rational operations are polynomial in the input bit length. The implementation stores full witness tuples, so no sharply optimized polynomial prefactor is claimed. The exponential improvement over `3^n` is rigorous, though MITM is classical machinery.

Let `kappa` be the maximum common-customer count of any queried location pair. Full exact optimization therefore costs

`N^2 poly(kappa) 3^{ceil(kappa/2)}`

arithmetic operations, plus polynomial incidence processing. Per-pair bounds can be summed instead of using a maximum. This is an FPT algorithm in overlap count `kappa`, with a still exponential dependence on that parameter.

The separate `astra_alg/` work provides an independently derived `O(n^2 W)` integer-weight DP and an FPT algorithm in the number of distinct common weights. Its weak NP-hardness proof for exact `m` explains why a general bit-polynomial exact `m` oracle should not be expected. I independently checked that reduction, the threshold DP, and the fixed-dimension ILP setup, including the `k=1` case.

## 3. Computing the true instance optimum alpha*

Compute all ordered minima `m(s,t)` and `d(t)=max_s m(s,t)`. At an ordered layout `(s,t)`, an equilibrium gap `Delta` has loads `(F+Delta)/2,(F-Delta)/2`, so its best enforceable factor is

`max{1, 2d(t)/(F+Delta), 2d(s)/(F-Delta)}`.

For positive total `d(s)+d(t)`, this is nonincreasing up to

`Delta_0=F (d(t)-d(s))/(d(t)+d(s))`

and nondecreasing thereafter. Searching the closest feasible gap on each side of `Delta_0` and taking the better objective value therefore suffices. A flat region from the floor at 1 causes no difficulty. A zero numerator over zero load is interpreted as zero; a positive numerator over zero load is infinite. All-zero coverage is handled with factor 1.

Run this query on every unordered layout, including co-location. The minimum is the exact global `alpha*`, **without assuming the golden-ratio theorem**. Its finite optimum is rational. A rational candidate `a>=1` satisfies `a<=phi` exactly iff `a*a-a-1<=0`; floating point is unnecessary.

The output's short deviation certificate proves the reported factor is attainable. It does **not** by itself prove global optimality: global optimality follows from the exhaustive-but-compressed MITM search and can be checked by rerunning it. Distinguish these two certificate claims.

## 4. A proved response-pruning bound and the lazy ring solver

For any particular customer NE `sigma` at `(s,t)`,

`m(s,t) <= U(s,t):=L_s(sigma) <= R_s`.

A cheap such equilibrium is obtained by inserting common customers in descending weight order into the currently lower-loaded facility, starting at the two private loads. This is a pure NE: on the final higher-load facility, its last inserted common customer bounds the final gap by its own weight; all earlier customers there have at least that weight. Customers on the lower side are automatically stable. If the higher side has no common customers there is nothing to check there.

For fixed opponent `t`, maintain a current exact best response value `D` and a location attaining it. If `U(s,t)<=D`, then `m(s,t)<=D`, so that response may be skipped **with an exact certificate**. Scan upper bounds in decreasing order, refine a bound by the exact MITM minimum only when necessary, and update `D`. At completion this gives exact `d(t)` and one valid `b(t)`; every pruned candidate retains a concrete punishment equilibrium with deviator load at most `d(t)`.

Start at any location and repeat only this `d(t),b(t)` computation until a visited location repeats. If the path visits `r` locations and its cycle has `k` locations, the worst-case pair-query count is `O(Nr+k^2)` rather than computing all columns eagerly. Since `r<=N`, the worst case remains quadratic in N. The branch-and-bound rule has **no proved nontrivial worst-case pruning fraction**.

Search layouts in this cycle using the exact local oracle and the full-game `d` values already computed. The ring corollary in the candidate proof guarantees a factor at most phi; that particular assertion remains conditional on the correctness of the main unreviewed proof. The output is nevertheless directly independently checkable as an approximate SPE of the full game, using the actual deviation equilibria.

The polynomial local strong-cross-chord constructor being developed in parallel can replace some on-path quota queries and can improve the concrete deviation upper bounds. Neither use removes the need to prove a bound on how often refinement is necessary.

## 5. Certificates and verification

Every output lists an on-path exact customer equilibrium and at most `2(N-1)` labeled unilateral-deviation equilibria. At each deviation, the listed `prob_first` refers to the **deviating facility**; its opponent is explicitly recorded. The on-path first facility is the first entry of `layout`. Common-customer order is increasing input index.

The independent verifier checks probabilities in `[0,1]`, reconstructs the two exact expected loads, and checks the conditional-cost inequality or indifference for every common customer. It then checks every deviator's load against `alpha` times its on-path load. Private and uncovered customers require no extra strategic choice.

All other labeled facility profiles can use the deterministic descending-weight pure NE routine. Thus this is a compact description of a full continuation selection. The idea of storing only unilateral-neighbor continuations is already in IJCAI 2024 and is not a novelty claim here.

## 6. Validation evidence

- Built-in regression: 435 independent support-enumeration comparisons covering minimum, maximum, and interior target objectives; includes empty overlap, private domination, equal weights, one-mixer continua, and rational weights. Passed.
- Built-in complete-game checks: 12 random incidence instances, exact certificate verification and phi test. Passed. This is not a proof of the global theorem.
- An independent teammate compared 30 further MITM objectives against a separately implemented full-spectrum DP, including continuum/boundary cases, plus four degenerate full games. Passed.
- A separate lazy-vs-full check compares all computed `d` values and verifies the ring-restricted factor cannot beat the full optimum on 30 random games. Results are recorded in `lazy_check_results.json`.

Illustrative fixed-seed pair benchmarks:

| common customers | all ternary supports | half states over all cutoffs | seconds |
|---:|---:|---:|---:|
| 10 | 59,049 | 1,212 | 0.059 |
| 14 | 4,782,969 | 10,932 | 0.698 |
| 18 | 387,420,489 | 98,412 | 10.564 |
| 22 | 31,381,059,609 | 885,732 | 126.106 |

These use arbitrary large integer weights, not the small-total-weight regime in which DP is better. No brute-force runtime comparison is claimed; the support count is an exact combinatorial baseline.

## 7. Primary sources and novelty boundaries

1. Krogmann, Lenzner, Skopalik, Uetz, Vos, *Equilibria in Two-Stage Facility Location with Atomic Clients*, IJCAI 2024: [official proceedings](https://www.ijcai.org/proceedings/2024/0315.pdf), [full version](https://arxiv.org/html/2403.03114v2). Section 2 gives efficient construction of some pure client NE and polynomial verification. Their Theorem 6 hardness reduction uses `m+2` facilities and unequal facility location sets. It does **not** establish hardness of this project's two-facility/common-location-set optimum. Their partial continuation certificates already suffice for verification.
2. Horowitz and Sahni, *Computing Partitions with Applications to the Knapsack Problem*, JACM 21(2), 1974, 277–292: [author-hosted original](https://www.cise.ufl.edu/~sahni/papers/computingPartitions.pdf), [DOI](https://doi.org/10.1145/321812.321823). The square-root exponent improvement from MITM is established algorithmic machinery; the threshold and equilibrium-count reduction is the model-specific part here.
3. Lenstra, *Integer Programming with a Fixed Number of Variables*, MOR 8(4), 1983, 538–548: [original author copy](https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1983i/art.pdf), [DOI](https://doi.org/10.1287/moor.8.4.538). This supports the teammate's fixed-dimension ILP route after fixing the total mixer count; it is not a new ILP algorithm.

This was a targeted primary-source check, not an exhaustive novelty survey of extremal weighted two-link mixed Nash equilibria.

## 8. One high-value question for Pro

**Can an exact-client phi-SPE for two facilities sharing S be constructed in time polynomial in the full rational input bit length, without computing exact m?**

The concrete approach to attack is adaptive punishment-certificate refinement: keep explicit equilibria that upper-bound all deviation minima, construct on-path quota witnesses using the new local strong-chord algorithm, and refine only the inequalities that prevent certification. Pro must prove a polynomial bound on refinements or find a structural algorithm that avoids them. The current ring search lacks such a bound.

Already solved here: compressed exact pair optimization, integer-weight pseudopolynomial optimization, parameterized algorithms, correct ring restriction, and verifiable continuations. These are subroutines, not an answer to the high-value question. The pair-m NP-hardness blocks a naive exact-d oracle route, but does not rule out the phi-SPE construction problem. An FPTAS or a `(phi+epsilon)` guarantee would be a separate, weaker research target; rounding weights also risks losing **exact** customer equilibrium and cannot simply be asserted to preserve it.
