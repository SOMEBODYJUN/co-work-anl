# Dynamic Theta: exhaustive multiplicity audit

Status: finite evidence only; this does not prove Q-CAG-HALF or the dynamic-Theta candidate.

## Exact scope

Using the repository's `ExactSPESolver` and `Fraction` arithmetic, I exhausted the 3-theme, 6-player class in which each of the seven nonempty customer signatures has multiplicity 0, 1, or 2. This is `3^7-1 = 2186` nonzero unit-customer inputs. For every input and every ordered path realizable by a complete history-dependent pure SPE, I computed

\[
  W + \sum_{i=1}^6 \Theta_i - \operatorname{OPT}_6,
\]

where the threshold at each path prefix is the exact Bellman value
\[
\Theta_i=\max_A\min_{z\in R(k+e_A)}u_A(z)
\]
from the complete pure-SPE outcome sets `R` cached by the solver. Thus this audit preserves off-path continuation choices and arbitrary ties; it is not a count-invariant strategy restriction.

## Result

The run inspected **2186 instances** and **at least 729 ordered pure-SPE paths per instance in the sparsest case**, with the exact aggregate path count recorded in `threshold_multiplicity_audit.json`; no negative slack occurred. The minimum observed slack was exactly **1**. A machine-readable witness and the reproducible script are next to this note.

This does not distinguish a universal proof from a counterexample outside the finite class. It does show that the 36-customer aggregate-floor obstruction does not transfer to the dynamic threshold: that obstruction has `W=34`, `OPT=36`, but its actual path thresholds are `(10,12,12)`, so the candidate slack is `34+34-36=32`.

## Reproducibility

From the repository root:

```sh
PYTHONPATH=. python3 research/workspaces/customer-attraction/boss20/independent_attack/threshold_multiplicity_audit.py
```

The output JSON records the exact instance/path totals and a minimum-slack witness. This computation is an audit artifact, not a general mathematical result.
