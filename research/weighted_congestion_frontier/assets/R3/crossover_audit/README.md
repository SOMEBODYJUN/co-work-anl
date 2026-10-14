# R3 independent literal crossover audit

Audit date: 2026-10-14 UTC. No search implementation or reported floating point factor was used by the verifier. The audit independently rebuilt the game directly from the seven masks, positive rational weights, and fourteen resource latency functions supplied for review.

## Claim WCF-R3-CROSS32-AUDIT-v1

**Exact statement.** There exists a four-player weighted atomic congestion game in `G_32` with weights `(1,1/10,1/20,1/50)`, fourteen resources, and two strategies per player, such that for every pure state `s` there exists a player `i` whose other strategy has cost `D_i(s)` satisfying

`C_i(s) > (9/5) D_i(s)`.

In fact, writing `B(G)=min_s max(1,max_i C_i(s)/D_i(s))`, its exact rational value is in `degree32_certificate.json`, and its informational decimal is `1.800488032325864`. The minimizing states are `0110` and `1001`. Consequently this particular game has no alpha-PNE for every `1 <= alpha < B(G)`, including alpha `9/5`; it does have a `B(G)`-PNE at those minimizing states because the equilibrium definition uses the weak inequality.

**Objects and domain.** Player indices are `1,2,3,4` in this document and `0,1,2,3` in the code and JSON. A state bit is the selected action. Mask label `1` belongs to action `0`, label `2` belongs to action `1`, and label `0` is absent from both. Every representative has a separate complementary resource obtained by swapping labels `1` and `2`. Both resources of a pair have the same latency

`c_e(x)=t_j*(x/T_j)^k_j`, where `T_j=sum_{i:mask_i!=0} w_i`.

The representatives, coefficients, and powers are exactly:

| Representative | t | k |
| --- | ---: | ---: |
| 0101 | 127 | 32 |
| 0112 | 231 | 32 |
| 1022 | 145 | 32 |
| 1100 | 139 | 32 |
| 1120 | 28 | 32 |
| 1122 | 41 | 32 |
| 1211 | 289 | 2 |

All coefficients `t_j/T_j^k_j` are positive rationals. The game therefore belongs to the precise polynomial model, with degree at most 32 and costs unmultiplied by player weights. Each of the sixteen states and sixty-four unilateral flips is fully evaluated.

**Evidence.** The following table gives eight state representatives; complementing all bits preserves the entire vector of costs, so the remaining eight states have identical respective ratios and witnesses. Decimals are solely explanatory: the stored rational costs and margins establish strictness.

| State | Witness player | C/D | C-(9/5)D |
| --- | ---: | ---: | ---: |
| 0000 | 3 | 1.813014712427298 | 1.765323070119263 |
| 0001 | 3 | 2.107020753961129 | 67.57567389875082 |
| 0010 | 4 | 1.804472655414893 | 0.859217933684833 |
| 0011 | 1 | 1.803388370686756 | 1.059917173992566 |
| 0100 | 4 | 1.818241334879999 | 2.899398725081922 |
| 0101 | 3 | 1.811634034854311 | 1.793005779423444 |
| 0110 | 4 | 1.800488032325864 | 0.134396658607905 |
| 0111 | 2 | 1.802820892710630 | 0.605014336123469 |

**Boundary treatment.** A current positive cost with zero deviation cost is assigned infinite improvement; two zero costs impose no obstruction for alpha at least 1 and are assigned comparison value 1; zero current and positive deviation cost gives ratio 0. All actual current and deviation costs in this game are positive. Every player uses one resource of the last, quadratic, complementary pair, and its load is at least that player's positive weight. Thus the strict finite comparisons do not depend on dividing by zero. The verifier explicitly exercises all three zero-boundary conventions.

**Status and scope.** Two independent exact reconstructions of one finite game, with a complete all-state certificate. The independent reviewer reconstructed the costs before reading any prior calculation. The parent researcher's `main_check.py` then reconstructed explicit strategy sets, normalized polynomial coefficients, all resource loads, and all sixteen states and sixty-four deviations without importing this verifier; its exact costs match the frozen certificate. This provides internal independent cross-review of the finite degree-32 statement. The fixed-parameter failure certificates are exact computational results from this verifier; the parent researcher also reports independent verification of the failure conclusion. The parameterized extensions below are authored derivations by this reviewer and have not themselves undergone a second independent review. External peer review and priority certification have not occurred. This result is a finite-instance lower-bound asset; it proves neither a growing infinite lower bound nor the full-class sublinear upper bound required by `WC-TARGET v1`. Its embedding gives `a_*(d) >= B(G)` for every integer `d>=32`, because `G_32` is a subclass of `G_d`; this constant observation is not a new growth theorem.

## Fixed weights and coefficients do not preserve the 9/5 obstruction

**Claim WCF-R3-FIXED-DEGREE-FAIL-v1.** Hold the weights, masks, and coefficients above fixed, replace the first six powers by `d`, and leave the last pair quadratic. It is false that this family has no `9/5`-PNE for every integer `d>=32`.

The exact scan finds at `d=40` a state `0111` (and its complement `1000`) with maximum flip ratio approximately `1.7928163137054876 < 9/5`. The assertion of that strict comparison is rational, not rounded. The threshold at `d=33` is approximately `1.801040414281835`; this illustrates why checking only the nearest degree does not certify all degrees.

There is also a precise asymptotic failure. For a resource of one of the first six pairs, `0<=x/T<=1` and weights remain fixed, so its latency tends to `t` when all supported players use the resource and tends to zero otherwise. The quadratic pair stays exactly the same. All sixteen limiting current and deviation costs remain positive. Since each cost and each ratio converges and the state and player sets are finite,

`lim_{d->infinity} B(G_d) = 5235403/2930833 = 1.786319111324323... < 9/5`.

The limiting minimizers are `0111` and `1000`, and the complete rational limiting game certificate is stored separately. In particular there exists an integer `D` such that for every integer `d>=D`, this fixed-parameter family has a `9/5`-PNE. This says nothing against changing the weights or coefficients with degree.

## Reproduction and files

Run `python research/weighted_congestion_frontier/assets/R3/crossover_audit/verify_degree32.py` from the repository root. It uses only the Python standard library and exact `Fraction` arithmetic. The script recomputes every unilateral deviation from the literal resource definitions. Default execution verifies all assertions and compares recomputed evidence to the frozen JSON without changing it. `--generate NEW_DIRECTORY` generates evidence at a new destination and refuses an existing directory.

- `verify_degree32.py`: independent literal cost construction and boundary rules.
- `main_check.py`: second reconstruction by the parent researcher, using explicit strategy sets and coefficients rather than the mask cost routine; also verifies the separate source-bound leaf certificates.
- `degree32_certificate.json`: exact sixteen-state costs, all deviation costs and ratios, chosen witnesses, positive margins, and exact instance factor.
- `fixed_degree_scan.json`: degree-specific exact comparison results, with informational decimals.
- `degree40_failure_certificate.json`: exact all-state evidence including the strict sub-9/5 optimum at `0111`/`1000`.
- `fixed_weight_limit_certificate.json`: complete exact fixed-weight limiting state costs and ratios.
- `limit_family.md` and `verify_limit.py`: separate parameterized interface, with independent-review obligations expressly open.
