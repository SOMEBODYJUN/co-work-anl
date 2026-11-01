# Raw read log — Boss2 R-2fc coverage representation

All six entries below were exported with `work.py clean show` and then read from byte 0 through EOF. The SHA-256 values are those of the exported files.

| Source ID | Bytes | SHA-256 | Full-read notes |
|---|---:|---|---|
| `237a9c14a68cbe08a526` | 11506 | `6a750484993f99a3893bc63306c50cce9c59400370bdbeea430194b39085db6a` | Read imports, exact Fraction helpers, rank, cover/payoff/potential, positive potential expansion, 22 space cases, 56 seeded strategies, exposure functional, disjoint SPE, last-layer obstruction, kernel sparsification, main/report fields. |
| `3bcc00f6fc8a8ac6756c` | 5238 | `f12d1fc0f9184ee597b12b3957b104ff8b519b35e8ee8e75f74e0561b14fe568` | Read Fraction target/model builders, r-loop full type enumeration, anchored/unanchored maximal proper restrictions, dual-column reconstruction, exact negative dual values, rational scale, main/report fields. |
| `10b27e972bf58a53c84e` | 13248 | `082fd97754bf5928ec971677054f49fe89975454a0e07e15cc4fd92a0cd655d6` | Read complete frozen geometry report, including identity/boundary text, all 22 space records, 7 strategy records, 7 exposure records, 4 disjoint-SPE records, 3 last-only records, and 5 sparse-support dictionaries. |
| `ae25ad82555f3e1b6d27` | 3779 | `3d82206e629fc5256bb91a1ddc1a08b6f64da666a269ce121b4894f5722f08a8` | Read complete frozen PM report, all six r cases, alpha/beta masses, type counts, local moment counts, negative dual values, integer scales and explicit finite limitations. |
| `b1ce857888be2dae3928` | 4654 | `a932d3a123ed5a30c2954b506b7d82dbd6e50d5ffe58ce5621abb1b246a721da` | Read complete frozen root report, all 20 (p,m) rank records, exposing pair total, m=1 exception and “no welfare theorem” scope. |
| `02ff2fdb8846b201e378` | 4905 | `a1212f6dff9d1f847e37d53635c1ca3ca55de12b287186aa6619b3ada7ecc5c3` | Read imports, compositions/rank/H, all p≤5,m≤4 rank loops, p≤8 exposing loops, m=1 exception assertion, report creation and CLI output. |

Related mathematical reading was completed for the coverage geometry and positive-moment locality manuscripts, aggregate-security DR boundary, harmonic-potential obstruction, CLAIMS/FAILED_ROUTES/RESEARCH_STATE, independent coverage review, and the existing theorem/obstruction/resource/computation objects named in `source-summary.json`.

The current batch’s replay artifacts are under `replay/`; no source, report, stdout or stderr was truncated. The finite checks and verifier outputs are recorded in `replay/execution.json`, `replay/related-ledger-verifier/execution.json`, and `replay/report-verifier/execution.json`.
