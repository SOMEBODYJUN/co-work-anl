# CA-UNIFORM-PORTFOLIO-TWO: a valid averaged cross-branch inequality

**Scope and status.** This is a self-contained, independently internally audited
proof in [CAG-MODEL](model.md),
at any fixed legal ordered prefix with exactly two players remaining. Customer
and provider weights are one; arbitrary integer customer multiplicities encode
distinct unit customers. The proof allows every history-dependent tie choice.
It does not prove the arbitrary-player half-coverage conjecture. The two-player
factor below was already known without background; the contribution here is an
averaged deviation interface and its cross-branch identity, with no novelty or
external-review claim.

Fix the prefix and write its customer load as $d_x\ge0$. Put

\[
U_d(X,Y)=\sum_{x\in X}\frac1{d_x+1+\mathbf1_{x\in Y}},\qquad
R_d(X,Y)=U_d(X,Y)+U_d(Y,X).
\]

Let $(A,B)$ be the actual two-player continuation. For arbitrary comparison
themes $T,S$ let $Q$ be the specified last player's reply after $T$, and let $R$
be that reply after $S$. These replies refer to the same complete SPE at the
same fixed ordered prefix. Define the four true deviation values

\[
V_{1,T}=U_d(T,Q),\quad V_{1,S}=U_d(S,R),\quad
V_{2,T}=U_d(T,A),\quad V_{2,S}=U_d(S,A).
\]

Then

\[
\boxed{2R_d(T,S)\le R_d(A,B)+V_{1,T}+V_{1,S}+V_{2,T}+V_{2,S}.}\tag{1}
\]

This statement averages both comparison themes over both actual players. It
requires less than first-player optimality: only last-player optimality at the
three histories ending in $A,T,S$ is used in (1).

## Four legal comparisons and an exact identity

The common catalog makes the following four slacks nonnegative:

\[
\begin{aligned}
D_{AQ}&=U_d(B,A)-U_d(Q,A),\\
D_{AR}&=U_d(B,A)-U_d(R,A),\\
D_{TR}&=U_d(Q,T)-U_d(R,T),\\
D_{SQ}&=U_d(R,S)-U_d(Q,S).
\end{aligned}\tag{2}
\]

The first two compare legal actions at the actual last node. The last two
compare the off-branch replies against one another at their own nodes. They do
not assert that a reply remains optimal when another predecessor is fixed.

For one customer write

\[
a=\mathbf1_A,\quad b=\mathbf1_B,\quad t=\mathbf1_T,\quad
s=\mathbf1_S,\quad q=\mathbf1_Q,\quad r=\mathbf1_R,
\]

and define the nonnegative integer polynomial

\[
\begin{aligned}
P(a,b,t,s,q,r)={}&6a+2b+2q+2r-4ab+12ts\\
&-2tq-2sr-3ta-3sa-aq-ar-tr-sq.
\end{aligned}\tag{3}
\]

The claimed nonnegativity is an elementary complete binary case check:

| $(t,s)$ | $a=0$ | $a=1$ |
| --- | --- | --- |
| $(0,0)$ | $2b+2q+2r$ | $6-2b+q+r$ |
| $(1,0)$ | $2b+r$ | $3-2b-q$ |
| $(0,1)$ | $2b+q$ | $3-2b-r$ |
| $(1,1)$ | $12+2b-q-r$ | $12-2b-2q-2r$ |

All eight entries are nonnegative for binary $b,q,r$.

Direct expansion of each customer's utility gives the exact identity

\[
\begin{aligned}
&R_d(A,B)+V_{1,T}+V_{1,S}+V_{2,T}+V_{2,S}-2R_d(T,S)\\
&\quad=\frac13(D_{AQ}+D_{AR}+D_{TR}+D_{SQ})\\
&\qquad+\sum_x
\frac{P(a_x,b_x,t_x,s_x,q_x,r_x)
      +d_x(3a_x+b_x+q_x+r_x)}
{3(d_x+1)(d_x+2)}.
\end{aligned}\tag{4}
\]

Every term on the right is nonnegative, proving (1). To reconstruct the
expansion, use

\[
U_d(X,Y)=f_d(X)-g_d(X,Y),\quad
f_d(X)=\sum_{x\in X}\frac1{d_x+1},\quad
g_d(X,Y)=\sum_{x\in X\cap Y}\frac1{(d_x+1)(d_x+2)}.
\]

On converting to the denominator $(d+1)(d+2)$, each $f$ term gains the numerator
factor $d+2$. The $d=0$ remainder is $P/6$; increasing $d$ gives the
additional numerator $d(3a+b+q+r)$ in (4). Thus (4) proves every nonnegative
integer background, rather than extrapolating from tested backgrounds.

First-player and actual last-player optimality additionally give

\[
V_{1,T},V_{1,S}\le u_1,\qquad V_{2,T},V_{2,S}\le u_2.
\]

Consequently (1) implies $R_d(T,S)\le\tfrac32R_d(A,B)$ for every pair. At the
root, $R_0(X,Y)=|X\cup Y|$, recovering the known two-player $3/2$ coverage
bound. In nonzero background, $R_d$ still denotes only the remaining players'
profits; it is not total coverage.

Repeated themes, empty themes, $T=S$, $A=B$, and identical coverage under
different labels cause no problem. Their membership coordinates coincide in
the identity, and all deviations used in (2) remain legal.

For any $n\ge2$ comparison themes $T_1,\ldots,T_n$, define their two-player
deviation values using the same actual prefix as above. Averaging (1) over all
unordered index pairs gives the further valid interface

\[
2\sum_{x\in\cup_jT_j}\frac1{d_x+1}
\le\frac n2R_d(A,B)+\sum_{j=1}^n(V_{1,j}+V_{2,j}).\tag{5}
\]

Indeed, for each covered customer select one comparison index containing it.
Its $n-1$ pairs each contribute at least $1/(d_x+1)$ to $R_d$: if both themes
contain the customer, $2/(d_x+2)\ge1/(d_x+1)$. The pairwise right sides sum to
$\binom n2R_d(A,B)+(n-1)\sum_j(V_{1,j}+V_{2,j})$; divide by $n-1$.

## The precise arbitrary-player proof obligation

At the root of an $m$-player game, fix any actual SPE path and any comparison
tuple $(T_1,\ldots,T_m)$. Let $V_{i,j}$ be player $i$'s payoff after switching to
$T_j$ at the original actual prefix, with the specified full strategy then
executed. A possible generalization of (1) is

\[
m\left|\bigcup_jT_j\right|
\stackrel{?}{\le}(m-1)W+\sum_{i=1}^m\sum_{j=1}^mV_{i,j}.\tag{6}
\]

SPE supplies $V_{i,j}\le u_i$, so (6), if proved, would imply
$\operatorname{OPT}_m\le(2-1/m)W$. This is **an unproved stronger conjectural
interface** for $m\ge3$. The failed exact matching condition required a
permutation paying all omitted optimal customers; (6) instead permits a
uniform average and retains the actual coverage budget. Its two-player proof
shows why cross-off-branch comparisons matter. With more players, exchanging
an off-branch follower action changes later followers' actions, so the four
slacks in (2) cannot simply be replaced by comparisons of frozen follower
portfolios.

## Verification boundary

[An independent exact audit](../../../tests/audits/customer_attraction_uniform_portfolio.py)
imports neither the canonical model nor solver. It checks all $2^6$ membership
patterns, the complete eight-case table, and both coefficients of the affine
background numerator in (4). It also directly checks 576 `Fraction` identities
at backgrounds $0,1,2,7,101,10^6,1/2,4/3,1001/37$, and both root coverage
identities for every membership pattern. The symbolic expansion and eight-case
table above constitute the proof for all customers and all integer backgrounds.
No arbitrary-player claim follows from this finite calculation.

Run `python3 tests/audits/customer_attraction_uniform_portfolio.py` from the
repository root. An independent agent additionally reconstructed the identity
and checked all membership cases without importing this audit; no fatal flaw
was found.

冻结审计报告：[customer_attraction_uniform_portfolio.json](../../../evidence/runs/2026-10-09/customer_attraction_uniform_portfolio.json)。
