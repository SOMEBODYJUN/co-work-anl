# R216 / forest boundary increment

This evidence bundle audits four locally available claimed source artifacts and keeps finite-search reports separate from general mathematics.

## Source IDs read in full

- `5c9a4ea8ec3529ce76cd`: R-21674 workspace README, 2,959 bytes.
- `f52629029fafc986e75a`: R-21674 `credible_search/README.md`, 3,095 bytes.
- `f64f9e0fe44cd4c5e9e8`: R-12bf6a96 `probe_forest_floor.py`, 3,678 bytes.
- `db8499cae5774325c959`: R-12bf6a96 `probe_forest_floor_cone.py`, 5,315 bytes.

The original local copies and frozen SHA-256 values are recorded in `replay/result.json`. The R-21674 gap JSONs and several direct-cover files remain in-progress but their blobs were not locally available when this review was performed; the review does not claim to have read those files.

## Reproducible run

```text
python archives/customer-attraction/tools/evidence/r216-forest-boundary-20261031/verify_batch.py
```

Exit code: 0. The script verifies all four source hashes, checks the 240-case exact forest report and 80-case cone report retain `counterexample=false` and `universal_claim_proved=false`, checks the four R216 branch/gap markers, and evaluates the root-support bound and sharp constant family with `Fraction` arithmetic. See `replay/stdout.json`, `replay/result.json`, and `replay/exit_code.txt`.

## Mathematical boundary

The companion formal review derives the leakage bound

`OPT_m <= (2 - 1/m) W + (1 - 1/m) |B|`,

where `B` is the union of root-omitted customers touched by true successors. The no-leak case gives the standard `(2 - 1/m)` bound; for six providers, a strict half violation would require `|B| > W/5`. A large-theme plus private-singletons family attains the no-leak constant. The forest threshold and R216 gap searches remain finite or conditional.
