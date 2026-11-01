# R-2fc aggregate-security tail comparison notes

## Scope and source identity

The six source IDs are the frozen versions in `research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/`. Each was read through `clean show` and saved under `original/`. The inventory SHA-256 and sizes are recorded in `manifest.json`. The `legacy-cleanup` and `main` source commits are both registered for each path; `replay/compare_frozen_bytes.py` read both commits and found byte equality with the archived output for all six files (12 comparisons, exit 0).

## Per-source disposition

| ID | Source | Exact content read | Comparison with existing obstacle / `dr_boundary.md` | Disposition |
|---|---|---|---|---|
| `615b20e056941847ca2d` | `dr_groups_simple_query.json` | `k=6,n=3`, seed 22112, one trial, fixed groups policy/query, `best_objective=-0.0003226252477301038`; witness root `[0,3,4]`, 43 policy entries, 83 states | Base finite floating diagnostic summarized historically as the single DR row. Witness is diagnostic-only; no customer budget or exact reconstruction. | `integrated` |
| `29bbc735344948028c8b` | `dr_groups_simple_query_diag.json` | Same fixed query/seed/trial and witness skeleton, `harmonic_diagonals=true`, `best_objective=-0.00028658162935766944` | Matches the harmonic-diagonal floating row; adds exact JSON field values and finite witness metadata only. | `integrated` |
| `e66595d9da26cedb6334` | `dr_groups_third.json` | Same fixed query/seed/trial and witness skeleton, `third_positive=true`, `best_objective=-0.0002817921983817029` | Matches the third-order-positive floating row; adds exact JSON field values and finite witness metadata only. | `integrated` |
| `6c9d817c586d116a7ef2` | `dr_groups_repeats.json` | Same groups query/seed/trial, `harmonic_repeats=true`, `best_objective=0.0`, no witness | Matches the mixed-repeat harmonic zero row. Zero is a finite optimizer output and not a nonexistence proof. | `integrated` |
| `4b98a2950c56d94cfbf5` | `dr_n3k3.json` | `k=3,n=3`, seed 22101, 100 trials, `best_objective=0.0`, no witness | New finite parameter point not used by the exact obstacle; no exact witness, customer instance, or theorem. | `integrated` |
| `8cda73aa604b09b9b171` | `dr_n3k4.json` | `k=4,n=3`, seed 22102, 100 trials, `best_objective=0.0`, no witness | New finite parameter point of the same diagnostic family; no exact witness, customer instance, or theorem. | `integrated` |

“Integrated” means the source-specific metadata and evidence boundary are recorded in the state computation object and evidence packet. It does not mean that a floating objective becomes an exact mathematical result. The six raw JSON files remain retained under `evidence/.../original/` for byte-level audit.

## Mathematical boundary

The existing obstacle is an exact finite counterexample in a larger monotone DR marginal-potential game, explicitly outside CAG. It supplies the exact integer data and static-security calculation relied upon. These six files do not add support-invariant welfare, customer multiplicities, rational potential values, a full-SPE certificate, or a universal quantifier. The negative objectives are finite floating values under one fixed policy/query and one trial; the zero objectives are finite run summaries over one or 100 trials. No value is promoted to CAG evidence, a general theorem, or a new exact counterexample.

## Program evidence

- `replay/validate_tail.py` exit 0; validates all six source hashes, sizes, statuses, parameters, objectives, and witness shapes.
- `replay/compare_frozen_bytes.py` exit 0; 12/12 archived-vs-source comparisons are byte-identical and Git blob IDs match.
- Six `python3 -m json.tool` runs exit 0; every stderr is empty. Formatted stdout and exit markers are preserved in `replay/`.
