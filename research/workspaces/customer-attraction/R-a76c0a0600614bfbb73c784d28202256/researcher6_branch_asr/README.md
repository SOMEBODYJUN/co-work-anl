# Researcher 6: size ordered aggregate-seat branch (candidate)

Date: 2026-10-27. Target: Q-CAG-HALF-6, specifically the seven-maximal-cover n=6 missing-orbit mechanism.

## Exact scope

This is a **conditional branch certificate candidate**, not a six-player theorem. It tests the legal order-statistic aggregate-seat inequality against one missing route/target orbit:

- route `(0,0,0,0,1,0)`;
- target maximal-label mask `K=125` (binary `1111101`);
- 1631 literal customer columns from the existing seven-maxima route generator;
- all 1005 established base nonnegative slack rows (`M`, `L`, `T`, `worst`, `H`, `profit`), plus 42 ASR rows (one owner for each t=0,...,5) and linear order rows for the selected top-seat sets.

For a fixed prefix route and remaining `r=6-t`, define seat upper bounds
\[
 U_{j,k}=|B_j|/(p_j+k),\qquad 1\le k\le r,
\]
where `p_j` is the routed prefix count. If `H_t` is the set of `r-1` largest `U` seats, the order-statistic inequality
\[
 u_t\ge (\sum_{j,k}q_{j,k}-\sum_{h\in H_t}U_h)/(6r+1)
\]
is valid: the sum of the largest `r-1` actual seat values is at most the corresponding sum of the largest upper bounds, and all remaining `6r+1` seats are at most the r-th actual order statistic. The order rows enforce `U_h-U_l\ge0` for `h\in H_t,l\notin H_t`; they are aggregate nonnegative constraints in the customer masses. The ASR row itself is used with nonnegative multipliers.

The sampled size vector
`(23.8609321669,10.7601323143,0.4811564626,0.1085592917,1.1094273945,0.4166165803,13.6519395361)`
induces
```
H0=[(0,1),(6,1),(0,2),(1,1),(0,3)]
H1=[(6,1),(0,1),(1,1),(0,2)]
H2=[(6,1),(1,1),(0,1)]
H3=[(6,1),(1,1)]
H4=[(6,1)]
H5=[]
```
(`H_t` is stored in `exact_branch_audit.json`).

## Computation and evidence level

`branch_asr.py` computes the floating LP; `exact_branch_audit.py` reruns the same LP and rationalizes the 19 positive multipliers with denominator at most `10^9`, then checks all 1631 Fraction columns. It reports exact minimum residual
`18498863000606739639886045305171986828695633123297448847848950678586594650307 / 6762571796424872885022917111161933156201229619283339655506473064817216175091704`
(approximately 0.0027354775), at literal column `(I,J)=(6,16)`. Thus this **single order branch** has a positive rational coefficientwise residual after the order rows are paid.

The certificate is not yet independently reimplemented, and the LP's selected top-seat branch is only one of many possible size-order cells. It does not cover the other missing orbits, and it does not by itself imply a valid global half bound. The denominator-limited rationalization is a reproducible candidate requiring an independent exact audit before any claim upgrade.

Reproduction from repository root:

```sh
python3 research/workspaces/customer-attraction/R-a76c0a0600614bfbb73c784d28202256/researcher6_branch_asr/exact_branch_audit.py
```

(The script imports the frozen `scratch_extract_r5` helper; if that extraction path is absent in a fresh clone, copy the helper directory from `scratch_extract_r5` before replay.)
