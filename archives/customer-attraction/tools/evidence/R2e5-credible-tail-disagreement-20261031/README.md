# R-2e5 credible construction: tail disagreement exact audit

This evidence package preserves the complete claimed source files, one isolated replay, and an independent field checker. The source script is a definition-level `Fraction` audit. It does not import the canonical customer-attraction model, LP/BI solver, or SPE solver.

## Sources

- `source/audit_tail_disagreement.py`: source `3fb7ca48ac84287e7ed9`, SHA-256 `5261fc42d1cc935746f0580de12df21e57eb9cf97dcdf77fadefdec9f3fb83a8`, 4905 bytes.
- `source/tail_disagreement_audit.json`: source `82d97a54acf1258d02a6`, SHA-256 `b435864e4da03006ea88647f2c285b8752b4b478aaf92da4c07123a78cb142a1`, 810 bytes.
- The script's aggregate input is preserved by the earlier aggregate-security evidence package at `../aggregate-security/original/examples/customer_attraction/aggregate_theta_failure.json`; SHA-256 `be0e1a54d3a7ddfeba327c03ce1975932e8fd1018926147b9c555fe6af180aaf`.

## Replay

The script was copied into a temporary repository-shaped root and run with the preserved aggregate input at `examples/customer_attraction/aggregate_theta_failure.json`. The command exited `0`; `replay/audit.stderr.txt` is empty. The generated JSON is byte-identical to the frozen JSON (`cmp` exit `0`):

- `replay/audit.stdout.json`
- `replay/tail_disagreement_audit.generated.json`

The replay records 972 exact scalar checks, 13 triangle nodes/39 comparisons, and 43 aggregate nodes/258 comparisons. The two reported decompositions are `(1,1,0,0,0)` and `(10,12,0,1/2,5/2)` for `(root, tail_mean, g_drift, C, D)`.

## Scope

The exact identity and the two finite strategy audits are integrated. They do not establish an arbitrary-history SPE theorem, a common nonnegative customer representation across all local packets, an LP dual certificate, or the six-player half-coverage target. The aggregate case reuses an existing frozen input and strategy audit.
