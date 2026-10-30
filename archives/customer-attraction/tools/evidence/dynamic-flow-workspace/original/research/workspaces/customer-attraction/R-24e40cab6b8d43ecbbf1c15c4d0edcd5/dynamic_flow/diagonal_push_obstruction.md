# Exact finite obstruction to the universal diagonal push

**Status:** exact auxiliary-interface failure only; no claim about the main half theorem. This certificate tests the strengthening
\[
 p^{\mathsf T}Kp\le u\quad\text{for every distribution }p
\]
at a root node, where `K(T,A)` is the extra-slot query payoff after forcing root `A`, and `u` is the prescribed root payoff. It does **not** refute free mixed `Mfull`, `Mpath`, the weak aggregate `Σ_iG_i^+(p)≤W`, or Q-CAG-HALF.

## Input and complete SPE certificate

There are 3 providers and five topics `T0,...,T4`. The eight unit customer interest sets are
\[
\{3\},\{0,3,4\},\{0,1,3\},\{0,2\},\{2,4\},\{0,3\},\{0,2\},\{0,1,2,3\}.
\]
The exact solver's worst-welfare certificate has root path `(0,0,3)` and terminal counts `(2,0,0,1,0)`, with
\[
W=7,\qquad OPT_3=8,\qquad (u_1,u_2,u_3)=(7/3,7/3,7/3).
\]
`verify_certificate` checks all 31 ordered histories and 124 one-shot comparisons; it returns `valid=True`. The audit is reproducible with

```sh
PYTHONPATH=. python research/workspaces/customer-attraction/R-24e40cab6b8d43ecbbf1c15c4d0edcd5/dynamic_flow/diagonal_push_obstruction.py
```

For each forced root `A`, follow the same complete strategy to its terminal branch `Z(A)`. The exact extra-slot matrix (rows are query `T`, columns are forced root `A`) is
\[
K=\begin{pmatrix}
5/3&13/6&23/12&9/4&8/3\\
1/2&1/2&7/12&7/12&5/6\\
23/12&9/4&17/12&7/4&5/3\\
3/2&5/3&7/4&19/12&13/6\\
5/4&4/3&5/6&5/6&2/3
\end{pmatrix}.
\]
The forced-root current payoffs are
\[
D=(7/3,2/3,7/3,7/3,1),
\]
so every column's current root payoff is at most the actual `u=7/3`, as required by root SPE incentive comparison.

## Exact violating distribution

Take
\[
p=(10/287,\;157/287,\;0,\;0,\;120/287).
\]
Direct rational evaluation gives
\[
p^\mathsf{T}Kp=1501/1722,
\qquad p^\mathsf{T}D=248/287=1488/1722,
\]
so
\[
p^\mathsf{T}Kp-p^\mathsf{T}D=13/1722>0.
\]
The diagonal push fails even relative to the *average* forced-root payoff. Since `D_A≤u` for every column, this also gives `p^TKp>p^TD` but does not by itself imply `p^TKp>u`; in this certificate `p^TKp<7/3`. The exact conclusion is therefore a failure of the stronger local accounting claim, not a failure of a root cap.

## Dynamic-flow implication

This example shows that a proof cannot simply take the same source/query distribution `p`, replace each adaptive forced-root payoff by its independent extra-slot query payoff, and assert the quadratic push is nonpositive. The discrepancy is exactly the signed membership/downstream-response covariance in the RESET identity; a valid proof must either choose a different source distribution (free `Mfull`) or use nonlocal cross-branch credit. The example has `2W=14>OPT_3`, so it contributes no main-goal counterexample.

The script uses the repository's exact finite solver only for this explicitly stated finite candidate test; no finite search is promoted to a general theorem or impossibility claim. No external review or novelty certification is asserted.
