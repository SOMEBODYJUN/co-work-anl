# A retained residual from the four-player profit certificate

Status: a proved strengthening of an existing **four-remaining-player necessary inequality**, not a five-player half-coverage proof. Exact arithmetic has been checked by `four_background_residual.py` in this directory. No independent review or external review is claimed. The present strengthening does not separate the old 727-row bad point and does not improve any stated five-player welfare constant.

## Exact domain and statement

Use the shared-catalog, unit-customer, unit-provider model with complete-history pure SPE, including all off-path histories, repeated and empty themes, and arbitrary ties. Fix a prefix with customer load `p_x in {0,1}` and four remaining players. Let their actual themes be `(A,B,C,D)`, their total profit be `V`, and put `b_x=(a_x,b_x,c_x,d_x) in {0,1}^4`. The reuse of the letter `b` for one membership bit is confined to the formulas below.

Let `beta=1499/750`. For any four legal comparison themes `T_1,...,T_4`, let

`O_4=sum_x e_x/(p_x+e_x)`, where `e_x=sum_j 1_{T_j}(x)` and zero numerators give zero contributions.

Then the existing four-player certificate gives the stronger inequality

\[
 O_4\le \beta V-\sum_x r_{p_x}(b_x),\tag{R4}
\]

where the following table specifies all values of the nonnegative rational function `r`.

| Actual membership ABCD | r_0 | r_1 |
|---|---:|---:|
| 0000 | 0 | 0 |
| 0001 | 0 | 133/750 |
| 0010 | 1/750 | 2003/12000 |
| 0011 | 1/1500 | 61853/180000 |
| 0100 | 1/1500 | 251/3000 |
| 0101 | 39/500 | 6331/22500 |
| 0110 | 1/1000 | 7363/36000 |
| 0111 | 623/3000 | 26047/60000 |
| 1000 | 2747/12000 | 239/1200 |
| 1001 | 691/6000 | 14579/45000 |
| 1010 | 47/1500 | 22183/90000 |
| 1011 | 1919/12000 | 5177/12000 |
| 1100 | 0 | 15767/90000 |
| 1101 | 77/750 | 63893/180000 |
| 1110 | 1/4000 | 43349/180000 |
| 1111 | 1169/6000 | 41143/90000 |

This is stronger than the bare ratio `O_4<=beta V`. It depends on the actual four-player order. It is not a license to change the given continuation or to transfer equilibrium status after deleting players.

## Certificate definition and proof

The dependency is `research/current/customer_attraction/four_remaining_profit_bound.md`, specifically its equations (3)--(12), with the same original complete strategy. Here is enough information to reconstruct this residual without reading another script.

The first remaining player may choose the actual last theme `D`; its true continuation is `(Q,R,S)`. For a customer write the seven membership bits as `(a,b,c,d,q,r,s)`, let `k=a+b+c+d`, `t=d+q+r+s`, and define actual shares `v_A=a/(p+k)`, ..., `v_D=d/(p+k)` and deviation shares `z_D=d/(p+t)`, ..., `z_S=s/(p+t)`. A zero numerator contributes zero.

Put `D_4=(p+1)(p+2)(p+3)(p+4)` and

\[
\begin{aligned}
\delta_2&=\frac1{p+1}-\frac1{p+a+b+1}
 +\mathbf1_{a+b=2}\frac{2p^2}{3D_4},\\
\delta_3&=\frac1{p+1}-\frac1{p+a+b+c+1}
 +\mathbf1_{a+b+c=3}\frac{p^2+p}{D_4}.
\end{aligned}
\]

For the per-customer row contributions **with the comparison-profit term removed**, use

\[
\begin{aligned}
K_\ell&=v_B-\frac\ell{p+a+3},\quad \ell\in\{c,d,q,r,s\},\\
P^0&=2\left(v_C+v_D+\frac c{(p+a+b+1)(p+a+b+2)}\right)+\delta_2,\\
E^0&=4v_D+\delta_3,\qquad F=v_A-z_D,\\
L_{QS}&=z_Q-\frac s{p+d+3},\\
L_{RC}&=z_R-\frac c{p+d+q+2},\\
L_{RS}&=z_R-\frac s{p+d+q+2},\\
L_{SB}&=z_S-\frac b{p+d+q+r+1}.
\end{aligned}
\]

Define

\[
\begin{aligned}
G_x^0=\frac1{1000}\bigl(&341K_c+302K_d+306K_q+302K_r+355K_s
 +354E^0+646P^0+1267F\\
&+24L_{QS}+8L_{RC}+17L_{RS}+108L_{SB}\bigr),\\
\rho_p(a,b,c,d,q,r,s)&=\beta\frac{k}{p+k}-G_x^0.
\end{aligned}
\]

The established four-player proof gives the exact identity

\[
 \beta V-O_4=G+\sum_x\rho_{p_x}(a_x,b_x,c_x,d_x,q_x,r_x,s_x),\qquad G\ge0.
\]

Every row used to form `G` is an actual-node SPE comparison or the established two-remaining-player tax comparison. The critical point is that `rho` does **not** depend on which four comparison themes were chosen. The only comparison quantity in the certificate is `-O_4`, with coefficient `(354+646)/1000=1`.

Set

\[
 r_p(a,b,c,d)=\min_{q,r,s\in\{0,1\}}\rho_p(a,b,c,d,q,r,s).
\]

This is a minimum over all eight binary incidence patterns, so includes the true off-path continuation without imposing a new selector or changing ties. The table evaluates these 256 rational expressions for `p=0,1`; every entry is nonnegative. Substituting `rho>=r` in the identity proves (R4). This finite incidence table is a complete per-customer coefficient verification, not a finite-instance SPE search.

## Five-player form and limitation

Fix any genuine five-player root SPE with actual path `(A_1,...,A_5)`, payoff vector `u`, and any five comparison themes with customer multiplicity `j_x`. Apply (R4) to the actual tail of four, whose background is `p_x=1_{A_1}(x)`, and sum over the five comparison-index subsets of size four. This gives

\[
\sum_x\sum_{h=1}^4
 \binom{j_x}{h}\binom{5-j_x}{4-h}\frac{h}{p_x+h}
 \le 5\beta(u_2+u_3+u_4+u_5)
       -5\sum_x r_{p_x}(1_{A_2},1_{A_3},1_{A_4},1_{A_5}).\tag{R5}
\]

Invalid binomial coefficients are zero. Repeated comparison themes cause no problem because these are index subsets. The same inequality applies in a true root-copy branch, replacing the four actual tail memberships and prefix accordingly.

On the frozen 727-row primal in `round5_pricing/exact_optimum_primal_terminal_cross.json`, the bare left-to-right slack is about `1.54341139577`; the retained correction is about `0.54777841646`, leaving positive slack about `0.99563297931`. Consequently (R5) does not exclude that point. The point itself is only a relaxation point, not a SPE.

The neighboring scratch experiments `root_branch_lp.py` and `last_ratio.py` are exploratory necessary-condition LPs. Their feasible points must not be described as full strategies, true SPE, or counterexamples to half coverage. No new five-player bound or arbitrary-player bound is established here.
