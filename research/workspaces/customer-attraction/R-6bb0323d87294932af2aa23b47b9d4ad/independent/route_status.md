# Independent attack status and duplicate checks

2026-10-24. General half target OPEN. This note records failed/unfinished reasoning accurately; it does not create a new obstacle theorem.

1. Reconstructed the obstruction independently: equilibrium root deviation comparisons keep the old prefix but all later actions may change. Summing static deviations or moving old-player payoffs between leaves is invalid.
2. Considered a fluid log benchmark: maximize sum_x log(1+(m-1)q_x) over topic distributions. Its KKT support equality yields OPT_m<=(2m-1)M, with M the largest reciprocal-price topic value at that optimizer. **Withdrawn assertion:** M<=v_m does not follow from Jensen. Jensen only lower-bounds v_m by the minimum over all fractional background caps, not by the cap at an arbitrarily chosen log optimizer.
3. Replacing the log optimizer with min_q max_A sum_(x in A)1/[1+(m-1)q_x] is exactly the existing free fractional safety t_m route, already proved as a static interface in R-077c0cacfba24288be91dee1acf6d484/security/free_fractional_security.md. Its leader/aggregate dynamic bridge remains open. The related pooled Jensen construction already appears in R-171cd7d518434f36a48cd50df29c9303/security/pooled_response_loads.md. These rediscoveries are not mathematical progress.
4. Outcome reduction to a count-Markov SPE cannot be used; an existing legal counterexample is recorded in R-d3981c0168644971803a9c3380ed687c/FAILED_ROUTES.md and the exact solver correctly retains sets of possible continuations.
5. The conditional minimal-leader-failure reduction in the companion note is the only completed derivation here. It supplies true branch expansion but no common cross-branch payment, so it does not close a target obligation.

No literature fact was newly imported, no finite sweep was used as evidence, and no target counterexample was claimed. A small floating computation on the already-known weak-iid family was merely a discarded diagnostic for the fluid log candidate; it was not a new instance search or a proof.
