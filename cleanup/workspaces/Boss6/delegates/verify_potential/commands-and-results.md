# Command log: `verify_potential_branch_obstruction.py`

All commands below were run from `/workspace/scratch/92f85f6f0437` on 2026-10-31 with Python 3.12.14. No Git writes, commits, pushes, fetches, or remote operations were performed. `git cat-file` was used read-only to materialize the frozen blobs into the delegate replay tree.

## Startup and source reads

```sh
cat co-work-anl-boss6/AGENTS.md
cat co-work-anl-boss6/cleanup/README.md
cat co-work-anl-boss6/cleanup/PROGRAM_CHECK.md
cat co-work-anl-boss6/cleanup/CHECKLIST.md
cat co-work-anl-boss6/cleanup/receipt-example.json
```

Read results: the cleanup rules require full-file and related-material reading, exact mathematical scope, and a receipt with `full_file_reviewed`, `related_material_checked`, `unique_content_accounted_for`, `read_note`, `comparison_note`, `decision_note`, `disposition`, and `targets`. The checklist entry for this source is `f3001ca6d7e2a9123d95`, currently `in-progress`, at `research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/route1/verify_potential_branch_obstruction.py`.

```sh
git -C co-work-anl-boss6 cat-file -p d299a5b2c7f6db319ab997b6c3bf621dd0f109eb > cleanup/workspaces/Boss6/delegates/verify_potential/source/research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/route1/verify_potential_branch_obstruction.py
git -C co-work-anl-boss6 cat-file -p 6621bc3007d8f583c44822b99c09b098ba7c2bc9 > cleanup/workspaces/Boss6/delegates/verify_potential/source/research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/route1/potential_branch_obstruction.json
git -C co-work-anl-boss6 cat-file -p 0d1bc6cffbf9ac26727729555859234fae4373b5 > cleanup/workspaces/Boss6/delegates/verify_potential/source/research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/route1/potential_branch_obstruction.md
cp -a tools/evidence/cag-coupled-seats-and-upload-audits/replay-tree/customer_attraction/. cleanup/workspaces/Boss6/delegates/verify_potential/source/customer_attraction/
```

Materialized source SHA-256 values:

```text
5055f6dbc9f582231f23279213b8e9e1004fa53a408f3453e8002372643a7779  .../verify_potential_branch_obstruction.py
6205c92730b8fdebb012b0562d3bca6f640dfca75e81c305a8daa3f263aad541  .../potential_branch_obstruction.json
db9d7f6ebb2acbc8f80e5c10a77c9e102cb9b47665d0117b2c421ef129baa3d7  .../potential_branch_obstruction.md
```

The frozen source blob IDs are respectively `d299a5b2c7f6db319ab997b6c3bf621dd0f109eb`, `6621bc3007d8f583c44822b99c09b098ba7c2bc9`, and `0d1bc6cffbf9ac26727729555859234fae4373b5`, present in both frozen commits `68fad804ec5946cb296f77dc5b336308a66abf12` and `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`.

## Primary verifier run

```sh
python3 cleanup/workspaces/Boss6/delegates/verify_potential/source/research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/route1/verify_potential_branch_obstruction.py
```

Exit status: `0`. Exact stdout:

```json
{"actual_history": [1, 3, 4], "claim": "CA-HARMONIC-BRANCH-DELETION-OBSTRUCTION-v1", "deletion_gap": "-1/2", "deviations": 215, "forced_root_history": [0, 0, 4], "histories": 43, "optimum": 4, "phi_actual": "9/2", "phi_deleted_actual": "7/2", "phi_deleted_forced": "4", "phi_forced": "5", "potential_gap": "-1/2", "scope": "branchwise harmonic-potential monotonicity fails; no main-claim counterexample", "status": "passed", "welfare": 4}
```

The same stdout and `exit_status=0` are saved in `run-output.txt`.

## Independent replay checks

```sh
python3 cleanup/workspaces/Boss6/delegates/verify_potential/independent_audit.py
```

Exit status: `0`. Exact stdout (also saved as `independent-audit-output.json`):

```json
{"actual": [[1, 3, 4], [0, 1, 0, 1, 1, 0]], "actual_phi": "9/2", "branch_checks_including_prescribed": 258, "certificate_valid": true, "checked_deviations": 215, "checked_histories": 43, "expected_histories": 43, "first_potential_lower_comparisons": [{"alternative": 0, "alternative_phi": "5", "chosen": 1, "chosen_phi": "9/2", "history": [], "payoff_alt": "1", "payoff_chosen": "1"}, {"alternative": 2, "alternative_phi": "5", "chosen": 1, "chosen_phi": "9/2", "history": [], "payoff_alt": "1", "payoff_chosen": "1"}, {"alternative": 3, "alternative_phi": "5", "chosen": 1, "chosen_phi": "9/2", "history": [], "payoff_alt": "1", "payoff_chosen": "1"}, {"alternative": 4, "alternative_phi": "5", "chosen": 1, "chosen_phi": "9/2", "history": [], "payoff_alt": "1", "payoff_chosen": "1"}], "forced_phi": "5", "forced_root": [[0, 0, 4], [2, 0, 0, 0, 1, 0]], "identity_failures": []}
```

This replay independently generated all 43 nonterminal ordered histories, evaluated all 258 prescribed/alternative branches, checked the potential marginal identity on every branch, and found zero identity failures. It found four root alternatives with lower prescribed-branch potential and tied root payoff; the source's required alternative `T0` is among them.

## Frozen source and runtime fingerprints

```sh
sha256sum cleanup/workspaces/Boss6/delegates/verify_potential/source/research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/route1/*
python3 --version
```

Results: source hashes are listed above; Python is `3.12.14`. Runtime package files copied from `tools/evidence/cag-coupled-seats-and-upload-audits/replay-tree/customer_attraction` had SHA-256 values:

```text
284282dfb35d5612734b979d691d57be9808c07a03857b533248eb2cbd5079ca  __init__.py
a269b532260b537e67879eba609ef23e046e8f7303458ecf11271c4673aecc45  certificate.py
a4c76d77fd6c8d18ac668ce2070a65f927d9dca6bbe3cdd36f467d1598b4a892  exact.py
ac28fc1a3837954ab9b8fc658701f53aecf0a1da059e316158aab7565dc5f6a8  model.py
3579b2eae0ad29e3a5b0c081f2c3833e9e55dc0dd740fbcafe0eb7239443c5f3  priced_hidden_reply.py
```
