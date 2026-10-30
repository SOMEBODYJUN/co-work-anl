# Finite m=6 search checkpoint

Status: **finite evidence only; Q-CAG-HALF remains OPEN**.

Using `customer_attraction.exact.ExactSPESolver` (terminal-count SPE outcome enumeration, with full strategy certificates available for each retained path), I ran two bounded searches:

- 4 themes, all nonempty customer-type subsets of size at most 6, unit multiplicity: 9,948 instances; no `OPT/minimum-SPE-welfare > 2`.
- 4 themes, 1,000 random instances with 1--8 customer types and multiplicities 1--8: worst observed ratio `7/6`, with `W=6`, `OPT=7`.

These scans do not prove the six-player theorem and did not produce a complete counterexample. They only rule out the searched finite families. The next proof task is to combine the exact identity

`W(P) = m*Phi(P) - sum_i Phi(P without player i)`

with full-history IC in a way that controls deletion-potential terms, rather than treating the harmonic-potential chain alone as a payment certificate.
