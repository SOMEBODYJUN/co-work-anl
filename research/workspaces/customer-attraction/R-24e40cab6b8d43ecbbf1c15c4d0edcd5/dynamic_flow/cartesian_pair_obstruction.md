# Cartesian lift of the root-reset pair obstruction

**Status (2026-10-24):** exact reusable obstruction for a specified local proof interface; it is not a Q-CAG-HALF counterexample and does not refute free Mfull/Mpath. The base eight-player full-history SPE is the independently audited two-block DAG in `R-d22a706a03c5499d941a6a97f94128a8/counterexample/pure_menu_two_block_dag.json`; its root reset pair has `R_1(3,7)=9/10` with `e_1(3)=e_1(7)=J_1(3,7)=0`.

## Product construction

Let `G` be any CAG instance with `n` providers, catalog `S`, unit customer set `N`, and a complete pure SPE strategy `sigma`. For an integer `k>=1`, form the disjoint Cartesian product `G^{\\times k}` as follows. A product topic is a tuple `(A_1,...,A_k) in S^k`; the customer universe is the disjoint union of k copies `N_j`. Product topic `(A_1,...,A_k)` covers the copy-`j` customers in `A_j`. The product strategy chooses tuples coordinatewise according to `sigma` at the corresponding coordinate history. For every ordered history, the product continuation is the tuple of the component continuations.

A deviation to a product tuple changes each coordinate independently. Because the customer copies are disjoint, the deviating provider's payoff is the sum of the k component payoffs for the same deviation. Thus component SPE inequalities add, so the product strategy is a complete ordered-history pure SPE. This is the standard Cartesian-product closure, with no count-state or tie-rule identification.

## Root reset quantities add exactly

For a component root source `A_j` and query `T_j`, write `D_j(A_j)` for the current player's actual forced-root payoff, `u_j` for the prescribed root payoff, `K_j(T_j,A_j)` for the extra-slot query payoff, and `R_j(A_j,T_j),J_j(A_j,T_j)` for the signed-reset and common-customer tax terms. In the product instance, for source tuple `A=(A_1,...,A_k)` and query tuple `T=(T_1,...,T_k)`, disjointness gives

\[
D^{(k)}(A)=\sum_j D_j(A_j),\\qquad
\\nu^{(k)}=\sum_j u_j,\\qquad
K^{(k)}(T,A)=\sum_j K_j(T_j,A_j),
\]
\[
R^{(k)}(A,T)=\sum_jR_j(A_j,T_j),\\qquad
J^{(k)}(A,T)=\sum_jJ_j(A_j,T_j),\\qquad
 e^{(k)}(A)=\sum_j e_j(A_j).
\]
The four-membership proof of `RESET` therefore remains coordinatewise exact.

Applying the base pair `(A_j,T_j)=(3,7)` in every coordinate gives

\[
R^{(k)}(A,T)=\\frac{9k}{10}>0,
\\qquad e^{(k)}(A)=e^{(k)}(T)=J^{(k)}(A,T)=0.
\]
Hence the local requirement

\[
R(A,T)\\le e(A)+e(T)+J(A,T)
\]
(or its equivalent pairwise nonnegative-cap condition `K(T,A)+K(A,T)<=2u`) fails by `9k/10` for every k. The failure scales linearly while all ordered-history SPE inequalities remain exact.

## What this rules out and what it does not

This product family rules out any proposed general proof whose only payment for the signed root-reset term is a coordinatewise sum of current-player slacks and common-customer taxes. It also rules out a proof that first demands pairwise nonnegative two-query balances and then sums them. The obstruction is not a welfare counterexample: each base block has `W=OPT=32`, and the product has `W=OPT=32k`, so `2W>=OPT` with wide slack. It does not refute a free mixed Mfull/Mpath choice, a cross-coordinate nonlocal flow, or Q-CAG-HALF itself. A valid dynamic proof must use a genuinely cross-branch or nonlocal credit beyond these local terms.

No external peer-review or novelty claim is made. The source DAG and the base reset values are independently exact; the product identities are algebraic and preserve all histories.

## Tail-share interpretation of the signed term

For a fixed customer `x`, write `c_x=b_x+1` and `F_A(x)=n_A(x)/(c_x+n_A(x))`, the total share of the **later** providers covering `x` in the forced-`A` terminal (the forced current provider is included in `c_x`). Then the signed term has the exact customerwise form

\[
R_i(A,T)=\sum_{x\in A\\setminus T}\frac{F_A(x)-F_T(x)}{b_x+1}
       +\sum_{x\in T\\setminus A}\frac{F_T(x)-F_A(x)}{b_x+1}.
\]

Indeed `F_A-F_T=(b_x+1)(n_A-n_T)/((b_x+1+n_A)(b_x+1+n_T))`; the `T\\setminus A` case is symmetric. Thus positive reset is precisely a membership--downstream-tail-share covariance, discounted by the pre-root load. The local `e+J` terms do not see this covariance. Any successful nonlocal flow must route differences of later-tail shares between the two forced branches; treating `R` as an unstructured sign error loses this exact structure. The crude bound `R_+ <= V_A+V_T` (where `V_A,V_T` are later-tail welfare on the two branches) is immediate but is not a welfare proof because these are off-path branch quantities.
