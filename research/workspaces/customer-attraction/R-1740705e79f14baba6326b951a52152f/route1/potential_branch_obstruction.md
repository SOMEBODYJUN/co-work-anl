# Harmonic potential: exact branch identity and a common-catalog monotonicity obstruction

**Status (2026-10-24):** reusable lemma plus a finite, fully checked obstruction to one natural proof route. This is not a counterexample to Q-CAG-HALF: the witness has `W=OPT_3=4`.

## Exact potential identity

For a terminal ordered profile `z=(S_1,...,S_m)`, write `c_x(z)` for the number of selected themes containing customer `x`, and
\[
\Phi(z)=\sum_x H_{c_x(z)},\qquad H_k=\sum_{q=1}^k1/q,\ H_0=0.
\]
For player `i`, let `z^{-i}` replace `S_i` by the empty theme while retaining every other theme in `z`. Then
\[
u_i(z)=\Phi(z)-\Phi(z^{-i}).
\]
This follows customer by customer: if `x\in S_i` and `c_x(z)=k`, the potential increment is `H_k-H_{k-1}=1/k`; otherwise both sides contribute zero.

At any SPE history `h` of player `i`, let `z_A` be the terminal outcome when `i` is forced to choose theme `A` and all later players follow the fixed SPE, and let `\bar z_A=z_A^{-i}`. The full-history SPE inequality is therefore exactly
\[
\Phi(z_{\sigma_i(h)})-\Phi(\bar z_{\sigma_i(h)})
\;\ge\;
\Phi(z_A)-\Phi(\bar z_A) \qquad(A\in\mathcal S).
\tag{P}
\]
Equivalently,
\[
\Phi(z_{\sigma_i(h)})-\Phi(z_A)
\;\ge\;
\Phi(\bar z_{\sigma_i(h)})-\Phi(\bar z_A).
\tag{P'}
\]
The right side is a branch-dependent deletion gap. It has no fixed sign, so (P) does not imply that the equilibrium continuation maximizes the terminal harmonic potential among current actions.

## Exact common-catalog witness

The six common themes are
\[
T_0=\{1,2\},\ T_1=\{2\},\ T_2=\{1,3\},\ T_3=\{0,1\},\ T_4=\{0,3\},\ T_5=\{3\},
\]
with four unit customers represented by interest signatures
\[
\{T_0,T_1\},\quad\{T_0,T_2,T_3\},\quad\{T_2,T_4,T_5\},\quad\{T_3,T_4\}.
\]
There are three players. The JSON file in this directory contains a full ordered-history certificate. Exact verification checks all `43` history nodes and `215` unilateral deviations.

One verified SPE path is `(T_1,T_3,T_4)`. At the root, forcing `T_0` under the same complete certificate leads to `(T_0,T_0,T_4)`. The root payoff is exactly `1` on both branches, so the deviation is SPE-admissible (a tie).

The terminal load vectors by customer are:

- actual `(T_1,T_3,T_4)`: `(2,1,1,1)`;
- forced root `(T_0,T_0,T_4)`: `(1,2,2,1)`.

Thus
\[
\Phi_{\rm actual}=H_2+3=9/2,
\qquad
\Phi_{T_0}=2H_2+2=5,
\]
so the equilibrium branch has **lower** harmonic potential by `1/2` despite the root being utility-optimal. After deleting the root action, the potentials are respectively `7/2` and `4`, and the deletion gap in (P') is also `-1/2`.

The witness has welfare `W=4` and `OPT_3=4`; it only blocks the implication `SPE ⇒ branchwise potential maximization`. It also shows why an induction that drops the deletion terms in (P') is invalid even for a common catalog and exact pure SPE with all off-path histories.

## Consequence for future routes

Any harmonic-potential proof must either (i) pay the signed deletion gaps across several histories so they telescope, or (ii) introduce a different state variable that controls these gaps. A proof that treats each current-action SPE comparison as `\Phi(z_{\sigma})\ge\Phi(z_A)` is false. The usual static exact-potential observation remains valid, but it cannot by itself turn full-history SPE into a potential local maximum.

This file does not alter the status of Q-CAG-HALF; it records a reusable exact identity and a checked mechanism boundary.

The local verifier `verify_potential_branch_obstruction.py` reruns the 43-history/215-deviation certificate check and exact Fraction arithmetic; its output records the two potential gaps as `-1/2`.
