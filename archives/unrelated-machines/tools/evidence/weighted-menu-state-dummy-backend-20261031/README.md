# Weighted-menu state-dummy backend evidence (2026-10-31)

This directory preserves the two frozen compressed source files and their extracted, runnable copies for the six `weighted_menu_` cleanup sources. The source SHA-256 values are:

- `initial.py.gz` (clean `8629950ab119d7e0bef2`, source SHA-256 `ae6706b743df06202e7b3799013eadb68df77931c244f122125a7d81300ec69d`)
- `initial_audit.py.gz` (clean `66c02ab103dfc9b7ba29`, source SHA-256 `c57f8cda7c13432942fea54c60c8584f37cfe2dff76f3f88700ae7023a11329e`)

The extracted backend is `source/degree_two_weighted_menu_backend.py`; the audit is `source/degree_two_weighted_menu_backend_audit.py`. Running the audit from `source/` with Python 3 produces `weighted_menu_backend_audit_results.json` and fixture outputs. It enumerates only the finite fixtures in the audit module; the core backend does not call enumeration, an optimum oracle, LP, recursion, or an external solver.

The implementation's declared scope is explicit degree-two group-resource support with nonnegative exact rational processing times and per-state private sum at most one. It must not be generalized to arbitrary weighted-menu or general unrelated-machines instances. The state-dummy value bridge is a separate exact normalized (per-state sum exactly one) theorem; these finite scripts are supporting evidence for backend mechanics and edge cases, not a proof of that theorem.
