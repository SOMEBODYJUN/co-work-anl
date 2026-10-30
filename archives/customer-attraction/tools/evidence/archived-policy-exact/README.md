# Archived policy exact-count evidence

This directory is the phase-two evidence package for the four archived-policy
drivers read in `cleanup/workspaces/Boss3/customer-structure/archived-policy-read/`.
The four frozen inputs are copied there byte-for-byte from the claimed source
objects.  The archived report is retained as an exploratory artifact: its
floating LP values are near zero, `best_float` is selected with a strict
`1e-8` improvement test, and `universal_result` is `false`.

`check_archived_policy_records.py` is an independent exact checker.  It does
not import the archived solver, `price_arrangement_attack.py`, the strategy
cone implementation, SciPy, or an LP package.  For each input it computes

\[
R(k)=\bigcup_a\{z\in R(k+e_a):u_a(z)\ge
\max_b\min_{y\in R(k+e_b)}u_b(y)\},
\]

where `k` is a prefix count vector and `z` ranges over terminal count vectors.
The induction is finite and exact over `Fraction`; it preserves every pure
continuation choice and therefore does not collapse histories into one
Markov policy.  The checker compares all 22 saved root records with the exact
root outcome sets and checks the 31-node selected coverage certificate at all
155 action comparisons (including the 124 genuine alternatives).

Run from the repository root:

```sh
python3 archives/customer-attraction/tools/evidence/archived-policy-exact/check_archived_policy_records.py
```

The saved output is `archived_policy_exact_check.json`.  It records the exact
SHA-256 values, count-state and terminal-state totals, all 22 roots, and the
selected certificate result.  The four root outcome counts are 8, 2, 7, and 5;
the count-state totals are 56, 35, 56, and 21.  These are finite-instance
facts, not a universal half-coverage theorem.

## Source map and limits

| object | stable source ID | role |
|---|---|---|
| `attack_archived_policies.py` | `42f15eb9d53f1a09437b` | archived-policy driver and report loop |
| `price_arrangement_attack.py` | `e4f16b49555f28d6421d` | exact export and policy-arrangement proposal |
| `archived_tstar_attack.json` | `692d7405644fa55a93b8` | 22 saved roots, selected point, and report metadata |
| source README | `42f15eb9d53f1a09437b` | source context and historical scope |

The imported iterative-search, cone, query-vertex, model, and certificate
files were read and compared against already archived objects; they are not
silently reclassified as new sources in this batch.  The checker certifies the
finite outcome-set recurrence and the selected tree only.  It does not recover
the 21 unsaved policies for any root, certify a floating LP upper bound, prove
that every attempted LP was feasible, or turn an early-stop proposal into a
counterexample.  The report's row counts remain provenance metadata.
