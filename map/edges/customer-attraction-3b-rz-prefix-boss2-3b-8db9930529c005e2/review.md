# 3B review — RZ prefix/discount composition

Internal word: `SOLVER-3B-PREFIX`. The two core registrations and the newly added discount endpoint were read in full; all 33 declared reading files were read as contiguous UTF-8 spans and their declared SHA-256 values were recomputed. The large JSON certificates were parsed end-to-end, while the finite verification reports were checked for their recorded PASS status.

## Exact comparison

`M-63c` supplies the same-source prefix/tail bridge. For one complete pure SPE, one legal source `h`, `k >= 3`, fixed static legal menu and nonnegative customer-independent alpha/beta contracts, its first branch and the return branch share the actual terminal label `V`. The tail contract has `0 <= delta < 1`, `H_beta` defined for every legal current topic and every `s=0,...,k-2`, and the finite-directory maximum proof gives the tail bound for every legal `F`; only then may the bound be evaluated at the prefix's actual `V`. The displayed joint minimum keeps the same hidden `v` in both terms. Source, terminal-price, and capacity budgets add; if the combined source is normalized, `a_T+a_C+a_beta=1` must be paid. `delta=0` is a one-step tail, and beta nonzero does not imply delta positive.

`M-736` can consume that bridge on one fixed real R/Z edge only when the prefix's `V` is the same terminal identity used by the R/Z zero-budget terminal IC. With `P` the common prefix load, the added terminal row is `(q-z)/(P+r+1)`. The common four-state min is valid only under the per-customer inequalities

`alpha * DeltaA >= lambda*q/((P+1)(P+2))`,
`beta * DeltaB >= lambda/(P+1)`,

with nonnegative alpha, beta, lambda and fixed static query convex combinations. For the six-player instantiation the same actual fourth source, the same R^C/Z^C edge, and the same source/menu/seed are required. The exact contracts use `alpha=49`, `beta=10`, `lambda=17965`, with the two M-63c contracts scaled by 999 and 10000, producing 148951 u4 + 20391 u6 before income transfer. The complete 2560-type rational table and independent Main report establish minimum R margin 5/6 and minimum Z margin 0. The v-preserving map contributes 21669 a6/D; after cancellation, `20391-21669=-1278`, so the retained contract is `148951 u4 - 1278 u6 >= (10857/2) OPT6 - (88871/9) W`. The 30 ordered non-diagonal R^C/Z^C edges are averaged with common labels; one may not choose C_i independently per edge.

This is an accepted conditional composition step, with a concrete finite parameter instantiation. It does not promote the finite 49:10 certificate into a half-coverage theorem. The remaining payment is the actual fourth-source `148951 u4` obligation, equivalently the nonpositivity of the right side after rearrangement. The U/C signatures (`n=1`, old C query bits zero) show that the displayed per-customer compression cannot pay a single common positive `c`: `c <= 10857/2` on U but `c >= 16210369/108` on C. They do not refute the full SPE or all additional shared constraints.

## Validation

- Declared source hashes: all 33 recomputed and matched.
- `main_verify_prefix_tail_5752.json`: PASS.
- `main_verify_zero_capacity_v1.json`: PASS.
- `main_verify_strong_a6_transfer_v1.json`: PASS.
- Local `edge-bind --write`, `edge-check`, and exact asset/hash checks are run after this review is written.
