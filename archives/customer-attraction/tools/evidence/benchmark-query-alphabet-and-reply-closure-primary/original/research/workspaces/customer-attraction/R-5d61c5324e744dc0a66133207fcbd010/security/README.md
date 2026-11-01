# Security / fixed-population catalog closure checkpoint

2026-10-23. Q-CAG-HALF, direct all-player `u_i>=OPT_m/(2m)`, true aggregate mixed safety, and mixed full-root menus remain **OPEN** here. This subagent wrote only this personal directory and performed no git or credential operations.

## General result

`safe_catalog_padding.md` proves a same-player-count closure lemma: any old complete pure SPE survives the addition of arbitrarily many disjoint new topics of size `t<=K/m`, where K is the old maximum theme size. The actual path and all its payoffs are preserved, and the enlarged optimum is exactly

    max_(1<=r<=m) [OPT_old,r+(m-r)t].

The full-history proof defines old-restricted BI after every new-theme history. It preserves arbitrary history-dependent old ties. For t0 no repeated empty themes are added; the formula reduces to the old optimum. The universal capK/m is sharp for preserving arbitrary old SPEs. A policy-dependent larger cap `min{L_sigma,K/(m−1)}` is also sufficient when m>=2, with L_sigma the minimum mover payoff over every old ordered history.

This yields a general primary-counterexample test, not just an auxiliary safety test: any strict inequality `OPT_old,r+(m-r)K/m>2W` immediately turns into a genuine half counterexample in a larger catalog with the same m and W. Likewise replace2W by2m u_i for the direct-floor route. No such violation is asserted.

The parent’s cleaner replayed the base audit and checked the proof, identifying the zero-cap duplicate-empty issue now repaired. The sharpness/refined cap/primary-target corollaries remain author-level derivations unless the parent separately reviews them. No external review or novelty certification.

## Reproduction

- `audit_safe_catalog_padding.py` / `.json`: independent standard-library Fraction implementation. Quotients equal-coverage old themes, constructs 36 enlarged complete policies at m1..4 and old catalog size1..3, checks15,849 exact ordered-history comparisons, and independently verifies the optimum convolution. The general theorem is proved analytically; the finite run checks the implementation.
- `direct_floor_probe.py`: candidate discovery by complete ordered-history policy cones. Exact integer backward induction samples history-dependent tie selections; the LP varies every nonempty customer type. Exact candidates would require rational feasibility and independent full-history replay.
- `direct_floor_probe_n4_k7_seed231026.json`:16 sampled policies generated from seven-cycle/perturbed-cycle inputs. No positive direct-floor separator observed. A total-catalog-union LP upper bound is used as a filter; only if this exceeds2m does the code enumerate m-topic portfolios. Float scope only.
- `direct_floor_probe_n5_k7_seed231027.json`:four further sampled policies, same limits. No positive separator observed.
- `safe_padding_probe.py` / `safe_padding_probe_n3_k6_seed231028.json`:eight complete three-player/six-topic policy cones, testing all potential maximum-size themes and all old portfolio sizesr2..3 against the padded direct floor. No positive separator observed. This is float discovery only, not a universal or exact fixed-cone certificate.

Do not continue increasing these batches merely to accumulate negatives. The new reusable object is the analytic catalog closure and its stronger linear separation test; a useful next step would target a policy with good coverage by substantially fewer than m old topics, or integrate the closure objective into another general construction. The fixed-cycle cones did not expose that structure.

## Mixed-menu lead passed to the counterexample agent

For k disjoint copies of the old16-customer four-player block, a hypothetical simultaneous root menu with one localq_T and all other blocksq0=AABC would be separated by uniform independent D queries whenever k>=4:

    min_root_column E_query insertion
      >=37/10−17/(12k)>13/4.

This is a conditional calculation only. The full simultaneous SPE scheduler is unproved; sequentially finishing blocks fails because a completedq0 offers insertionD=37/10, exceeding later proposed3.25 movers. The construction task was passed to the counterexample agent; no direct-sum theorem is assumed here.
