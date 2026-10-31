# Weak matching partition-query finite reports

This package preserves three assigned partition-query reports from the weak-matching workspace and records two deterministic one-game replays plus an independent structural checker.

| source ID | source file | bytes | SHA-256 |
|---|---|---:|---|
| `acba20524372cf3f45ea` | `partition_examples_seed104216.json` | 62093 | `ef35c725d0996aa2c9c40ab82405452c5f46a06f186596221abba3a803804225` |
| `bc533ffdcb3a1e45d173` | `partition_p6m4_seed104213.json` | 207963 | `c19849a3127d73a8fa72ba985446d6e23a195a1973f49869fc938eb940d401ca` |
| `b04e4dc3e95e6066048a` | `partition_p7m5_seed104214.json` | 476792 | `fc4ddd68b1542d0ca342ccb66677c7c81c9a1af9d54b7ccf9ccaba1f3a14ea4e` |

All three reports use `query_mode=partition`, where the source probe's separator threshold is exactly 1. The examples report has 47 policy cones and 217 records (191 successful, 26 infeasible); its maximum saved value is `1.0000000000000002`. The p6 report has 196 cones and 588 records (575 successful, 13 infeasible); the p7 report has 99 cones and 297 records (268 successful, 29 infeasible). Their maximum saved values are also `1.0000000000000002`, within the source's `1e-7` floating early-stop tolerance, so none produced a partition separator.

The reports retain lower successful values as well: p6 reaches `0.3856891090488513`, examples `0.49999999999999994`, and p7 `0.34365903655728114`. These are feasible fixed-cone objective values below the threshold, not negative welfare gaps or SPE counterexamples. The p6 best metadata has a 6-topic/4-player instance, actual root `(2,2,2,2)`, target `(0,1,2,3)`, and 280 LP rows; p7 has a 7-topic/5-player instance, actual root `(0,0,0,0,0)`, target `(0,1,3,4,5)`, and 1260 rows. The examples batch uses canonical instances and its best is a 5-topic/2-player instance with target `(0,1)` and 21 rows.

The replay copies the previously audited probe implementation and canonical dependencies. One p6 partition run and one p7 partition run both exit 0 with empty stderr; their best values are `0.8139652647966064` and `0.7999822727070177`. `verify_partition_reports.py` checks all three source hashes, report counts, best fields, action counts, the partition threshold bound, and the replay outputs; it returns `PASS`.

The partition objective is a finite floating-point policy-cone diagnostic. It does not serialize every pre-LP term, provide an exact rational dual, reconstruct integer clients, or quantify over all complete pure SPE histories. The `success=false` records are infeasible fixed policy/target cones. The package therefore records a finite no-separator sample and does not claim a weak-matching theorem or a six-player half result.
