# Dynamic query-debt identity for the free complete path menu

**Status (2026-10-24).** Exact algebraic identity for every finite common-menu instance and every complete history-dependent pure strategy. It is not a proof of Q-CAG-HALF and it does not assert that the free path-menu bridge is true. The identity isolates precisely the term created when a forced action changes its continuation.

## Setup

Fix a position `i`, an actual prefix, and a complete pure strategy. For every legal forced action `A`, let `Z_i(A)` be the complete terminal obtained by forcing `A` and then following the same strategy. Write

\[
c_A(x)=c_x(Z_i(A)),\qquad h_A(x)=c_A(x)-\mathbf 1_{x\in A}.
\]
Thus `h_A(x)` is the load supplied by all other positions in that forced terminal, and `h_A(x)\ge0`; if `x\notin A`, then `c_A(x)=h_A(x)` and if `x\in A`, then `c_A(x)=h_A(x)+1`.

Let `p` be any query distribution on the common menu and `q_x=\Pr_{T\sim p}[x\in T]`. Define

\[
D_i(p)=\mathbb E_A\sum_{x\in A}\frac1{c_A(x)},\qquad
C_i(p)=\mathbb E_A\sum_x\frac{q_x}{1+c_A(x)},
\]
where `A\sim p` in both expectations. `D_i` is the forced current-player payoff under the same query distribution; `C_i` is the same-query push-forward price. The free menu quantity satisfies
\[
\psi_i(p)=\min_A\mathbb E_T\sum_{x\in T}\frac1{1+c_A(x)}\le C_i(p).
\]

For each customer with `0<q_x<1`, define conditional reciprocal loads
\[
H^0_{i,x}=\mathbb E\!\left[\frac1{h_A(x)+1}\,\middle|\,x\notin A\right],\quad
H^1_{i,x}=\mathbb E\!\left[\frac1{h_A(x)+1}\,\middle|\,x\in A\right],
\]
and
\[
J^1_{i,x}=\mathbb E\!\left[\frac1{(h_A(x)+1)(h_A(x)+2)}\,\middle|\,x\in A\right].
\]
The conditional terms are only needed when their conditioning event has positive probability; their coefficients below vanish at `q_x=0` or `1`.

## Exact identity

For every `i` and `p`,
\[
\boxed{
C_i(p)-D_i(p)
=\sum_x \left[q_x(1-q_x)(H^0_{i,x}-H^1_{i,x})-q_x^2J^1_{i,x}\right].
}\tag{DI}
\]

Proof is pointwise in `x`. If `I=\mathbf1_{x\in A}` and `h=h_A(x)`, the query contribution is `q_x/(h+I+1)` and the current contribution is `I/(h+1)`. Conditioning on `I=0` and `I=1` gives
\[
\begin{aligned}
\mathbb E\left[\frac{q_x}{h+I+1}-\frac{I}{h+1}\right]
&=(1-q_x)q_xH^0_{i,x}+q_x\left(q_x\mathbb E[\frac1{h+2}\mid I=1]-H^1_{i,x}\right)\\
&=q_x(1-q_x)(H^0_{i,x}-H^1_{i,x})
-q_x^2J^1_{i,x},
\end{aligned}
\]
using `1/(h+1)-1/(h+2)=1/((h+1)(h+2))`. Summing over `x` proves (DI). No equilibrium assumption, tie convention, or count-invariance is used.

## Interpretation and exact boundary

The second term is always nonpositive. The only possible positive push-forward debt is
\[
q_x(1-q_x)(H^0_{i,x}-H^1_{i,x}),
\]
which is a continuation covariance: forcing a query action that **omits** `x` must, on average, leave a larger reciprocal residual load on `x` than forcing an action that contains `x`. In a fixed-suffix (history-independent) continuation, `h_A(x)` has the same value after conditioning on `x\in A` or `x\notin A` up to the direct action indicator, so `H^0=H^1` and the debt is strictly nonpositive. Dynamic continuation is the only source of a positive term.

For the global free path menu, the exact accounting is
\[
\sum_i\psi_i(p)-W
\le \sum_{i,x}q_x(1-q_x)(H^0_{i,x}-H^1_{i,x})
-\sum_{i,x}q_x^2J^1_{i,x}
-\sum_i e_i-\sum_i L_i,
\]
where `e_i=u_i-D_i(p)\ge0` is the actual IC slack and `L_i=C_i-psi_i(p)\ge0` is the gain from choosing the best defensive column rather than pushing the same `p`. Thus a proof of the uniform path candidate `\sum_i\psi_i(p)\le W` must pay the positive continuation-covariance sum with the collision discounts, IC slacks, or a genuinely cross-history continuation inequality. A static max-flow or a terminal welfare identity does not pay this term.

This also gives a clean diagnostic for a putative counterexample to the free path-menu bridge: it must have nonzero query mixing and a positive aggregate `H^0-H^1` large enough to dominate both `J^1`, `e_i`, and `L_i`. Pure queries (`q_x\in\{0,1\}` for all `x`) have no positive covariance term and obey the menu bound directly from SPE.

## Fixed-suffix corollary

If every forced action only replaces the `i`-th action while all other actions remain fixed, let `c_x` be the actual terminal load and `r_i(x)=\mathbf1_{x\in A_i}`. Then the conditional residual load is fixed at `h_x=c_x-r_i(x)` and (DI) gives
\[
C_i(p)-D_i(p)=
-\sum_{x:r_i(x)=0}\frac{q_x^2}{(h_x+1)(h_x+2)}
-\sum_{x:r_i(x)=1}\frac{q_x^2}{(h_x+1)(h_x+2)}\le0.
\]
Hence for a static Nash profile (or any fixed-suffix SPE root), `\sum_i\psi_i(p)\le W` for every `p`, and therefore the free complete path menu satisfies `M_{path}\le W/m`. This corollary is deliberately limited: it does not allow continuation actions to change after a forced deviation.

## What remains open

The original Q-CAG-HALF and the unrestricted free complete path-menu bridge remain OPEN. The identity does not transfer a continuation term between mutually exclusive children; any such transfer must be proved from actual later-player IC at the corresponding history. It is unsafe to reuse one terminal's `H^0-H^1` credit in another branch.
