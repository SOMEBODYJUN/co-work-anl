# 资源局部窄权带：Shapley 存在界与跨带拼接障碍

Date: 2026-10-14. Model: WC-TARGET v1, specifically the unweighted player
cost `C_i = sum_e c_e(load_e)`, with positive real player weights, arbitrary
finite strategy families, empty strategies allowed, and nonnegative
polynomial coefficients. This is a self-contained independent reconstruction.
No universal `o(d)` claim is made. No novelty claim is made.

## Claim identities

| ID/version | Exact scope and conclusion | Status |
|---|---|---|
| WC-R3-DENSE-SHARE v1 | For a nonempty finite positive-weight user set S and `F(x)=x c(x)`, with c a nonnegative-coefficient polynomial, uniform Shapley shares satisfy `w_i <= w_j => phi_i <= phi_j` and `phi_i/w_i >= phi_j/w_j`; consequently `min(S) c(W) <= phi_i <= max(S) c(W)`. | Complete algebraic proof below; exact finite verification; external review absent. |
| WC-R3-DENSE-LOCAL v1 | For every WC-TARGET game and finite R>=1, if every resource's **potential** users have weight ratio at most R, the explicitly defined scaled Shapley potential has an R-PNE at every global minimum. No degree or player-count factor. | Complete proof from DENSE-SHARE; two independent proofs of the share envelope and exact finite audits complete; external review absent. |
| WC-R3-DENSE-POT-SHARP v1 | For every fixed R>1 there is a sequence of games of local weight ratio R in which the unique minimizer of the stated potential has best approximation factor tending to R. The games themselves have an exact PNE. | Complete asymptotic proof below. This is sharpness of this selection mechanism, not a threshold lower bound. |
| WC-R3-BAND-CURL v1 | Normalizing each player's standard Shapley marginal by its own band scale need not admit an ordinary exact set potential when a resource mixes bands; a two-user cubic total-cost identity witnesses the failed mixed-difference equation. | Exact obstruction; weighted potentials are not ruled out. |
| WC-R3-BAND-LINEAR v1 | The unmodified standard Shapley potential, also after resource-minimum scaling in the given family, can select a state with factor at least d/6 for every d>=7 even though the two weight bands are singletons. | Exact family and proof below; this is a potential-mechanism obstruction, not equilibrium nonexistence. |

Objects/quantifiers/assumptions are explicit in the respective sections below.
Dependencies: only the definitions of finite potential minimization, uniform
Shapley shares, the multinomial theorem, and positive weights. Evidence:
`verify.py` and `verification.json`. Counterevidence: cross-band claims below.
Related files: `../../../MODEL.md` is the model authority; this README and `verify.py` are
the frozen local assets. The code is not a substitute for the proofs.

## The resource set potential and its exact marginal

Write `W(S)=sum_{j in S} w_j`, `n=|S|`, `F(x)=x c(x)`. Thus F(0)=0, even
when c has a constant term. Set H(empty)=0 and, for nonempty S, define

\[
 H(S)=\sum_{\varnothing\ne T\subseteq S}
 \frac{(|T|-1)!(n-|T|)!}{n!}F(W(T)).
\]

For i in S define its standard uniform-permutation Shapley share

\[
 \phi_i(S)=\sum_{T\subseteq S\setminus\{i\}}
 \frac{|T|!(n-|T|-1)!}{n!}
 \bigl[F(W(T)+w_i)-F(W(T))\bigr].
\]

Direct subtraction of H(S minus i) from H(S) gives

\[
 H(S)-H(S\setminus\{i\})=\phi_i(S). \tag{1}
\]

For a nonempty T not containing i, with t=|T|, the coefficient difference
in that subtraction is `-t! (n-t-1)!/n!`; for T containing i the coefficient
is `(t-1)! (n-t)!/n!`. These are exactly the two terms in (1).
Efficiency is immediate by telescoping F along each permutation:

\[
 \sum_{i\in S}\phi_i(S)=F(W(S))=W(S)c(W(S)). \tag{2}
\]

## Exact positive-coefficient proof of the share ordering

By linearity it suffices to take `F(x)=x^q`, q an integer at least 1. Expand
`W(S)^q` into multinomial terms. A term with exponent vector gamma is
present in a coalition exactly when that coalition contains its support.
In a random ordering, each member of that support is last with equal
probability. Therefore

\[
 \phi_i(S)=\sum_{\substack{|\gamma|=q\\\gamma_i>0}}
 \frac{q!}{\prod_j\gamma_j!}
 \frac{\prod_j w_j^{\gamma_j}}{|\operatorname{supp}\gamma|}. \tag{3}
\]

Fix i,j with weights a<=b. Fix an exponent vector beta on the other users.
Let m be its support size and let h=q-sum(beta). Terms with h=0 do not
contribute. For h>=1 write

\[
 B=\frac{q!}{h!\prod_{\ell\ne i,j}\beta_\ell!}
       \prod_{\ell\ne i,j}w_\ell^{\beta_\ell}\ge0.
\]

Terms involving both i and j cancel in `phi_i-phi_j`. The remaining
contribution is `B(a^h-b^h)/(m+1)<=0`. Hence `phi_i<=phi_j`.

The beta contribution to `phi_i/a-phi_j/b` is zero when h=1. For h>=2,
its exact value is

\[
 B(b-a)\sum_{r=0}^{h-2}
 \left[\frac{\binom h{r+1}}{m+2}-\frac1{m+1}\right]
 a^r b^{h-2-r}. \tag{4}
\]

To obtain (4), the i-only and j-only terms contribute
`B(a^(h-1)-b^(h-1))/(m+1)`. The terms involving both contribute
`B(b-a)/(m+2) sum_{r=1}^{h-1} binom(h,r) a^(r-1)b^(h-r-1)`.
Factoring the difference of powers gives (4).

Every coefficient in brackets is nonnegative, since

\[
 \binom h{r+1}\ge2,\qquad
 \frac2{m+2}-\frac1{m+1}
   =\frac{m}{(m+1)(m+2)}\ge0.
\]

This proves the inverse normalized ordering. A nonnegative linear
combination over q gives the stated result for `F=x c(x)`.

Choose a minimum-weight user u and a maximum-weight user v. By (2), c(W)
is the weight-weighted average of the numbers `phi_i/w_i`. Thus
`phi_u/w_u >= c(W) >= phi_v/w_v`. Combine this with the ordinary share
ordering to obtain

\[
 w_u c(W)\le\phi_u\le\phi_i\le\phi_v\le w_v c(W). \tag{5}
\]

No division by c(W) was used. If c is zero, every term is zero. If S has
one user, (5) is equality. For affine c, only q=1,2 occur and the normalized
ordering is equality: `phi_i=w_i c(W)`.

## Resource-local R-PNE lemma

For each resource e let

\[
 P_e=\{i:\text{some strategy in }S_i\text{ contains }e\}.
\]

Unused resources with empty P_e can be dropped. For the remaining resources
put `a_e=min_{i in P_e} w_i`, `b_e=max_{i in P_e} w_i`, and assume
`b_e/a_e<=R`. Define

\[
 \Phi(s)=\sum_e H_e(S_e(s))/a_e,
 \qquad
 D_i(s)=\sum_{e\in s_i}\phi_{i,e}(S_e(s))/a_e.
\]

All quantities are finite. By (1), for **every** unilateral deviation,

\[
 \Phi(t_i,s_{-i})-\Phi(s)=D_i(t_i,s_{-i})-D_i(s). \tag{6}
\]

Common resources are unchanged and cancel in this identity. By (5) and
`S_e(s) subset P_e`, resourcewise and therefore strategywise,

\[
 C_i(s)\le D_i(s)\le R C_i(s). \tag{7}
\]

At a global minimum s of the finite function Phi, (6) gives
`D_i(s)<=D_i(t_i,s_-i)`. Hence

\[
 C_i(s)\le D_i(s)\le D_i(t_i,s_{-i})
              \le R C_i(t_i,s_{-i}).
\]

This proves WC-R3-DENSE-LOCAL v1. Every strict R-improvement also strictly
decreases Phi, so all such improvement sequences terminate. No polynomial
time claim is implied; the displayed H has exponentially many subset terms.

The word potential in P_e is essential: a deviation can introduce a player
whose weight is absent from the current user set. An envelope based only on
the current users supplies no uniform scale for that deviation.

Boundary cases: empty strategies have D=C=0; zero-cost deviations force C=0
at a potential minimum; resources with zero polynomial costs contribute zero;
degree zero is covered. At R=1 this is an ordinary exact potential for the
original costs. In fact d<=1 has exact PNE without any ratio restriction,
using the unscaled H and the weighted-potential identity with multiplier w_i.

## Where bands can be glued without loss

One may have arbitrarily many weight bands, arbitrarily large global weight
ratio, and arbitrarily many users in every band. If each resource's potential
users are all contained in one band of ratio at most R, the lemma applies
directly. Resource scales can differ arbitrarily. This is the precise safe
band interface; no density hypothesis is needed.

If a resource mixes far-separated bands, the within-band ratio alone does
not supply the hypothesis. The two obstructions below explain why the
obvious Shapley gluing steps do not repair it.

## Sharpness for this particular potential selector

Fix any real R>1. For m positive, take m fixed players of weight R and one
moving player of weight 1. Every fixed player has only strategy {A}; the
moving player has strategies {A} and {B}. Set `d=m^2`, `W=mR+1`,
`c_A(x)=x^d/W^d`, and `c_B(x)=rho_m` constant. Define

\[
 \delta_m=\frac{1}{(m+1)W^d}
       \sum_{k=0}^m[(kR+1)^{d+1}-(kR)^{d+1}].
\]

This is the moving player's Shapley marginal on A. Its original A cost
is exactly 1. Since it is the minimum-weight user, ordinary share ordering
and efficiency imply the upper bound below. Its last-place marginal gives
the lower bound:

\[
 \frac W{m+1}\left[1-(1-1/W)^{d+1}\right]
 \le\delta_m\le\frac W{m+1}. \tag{8}
\]

Since `(d+1)/W` tends to infinity, both bounds tend to R. For all sufficiently
large m choose `rho_m=delta_m-1/m>1`. Both resource minimum-user scales are 1.
The unique minimizer of Phi places the moving player on B, because its two
incremental potential costs are rho_m and delta_m. That state's best
approximation factor is rho_m, tending to R. The state with the moving
player on A is an exact PNE. Thus this is a sharp **selector** example, not
a nonexistence construction and not a lower bound for a_*(d).

## Fatal mixed-difference obstruction to separate band normalization

Take one resource, two users of weights 1 and M>1, and `F(x)=x^3`.
There are two singleton weight bands; each has internal ratio 1. The mixed
set difference of H is

\[
 \kappa=H(\{i,j\})-H(\{i\})-H(\{j\})
 =\tfrac12[(M+1)^3-M^3-1]=\tfrac32 M(M+1)>0.
\]

Suppose one tries to define separately normalized marginals
`psi_i=phi_i/1` and `psi_j=phi_j/M`. An ordinary exact set potential Q
would require its mixed difference to equal both
`psi_i({i,j})-psi_i({i})=kappa` and
`psi_j({i,j})-psi_j({j})=kappa/M`. This is impossible.
One can recover a *weighted* potential with player multipliers 1 and M,
but the following example blocks a degree-independent guarantee from that
recovery. This objection does not rule out different potentials or a
nonpotential existence argument.

## Linear loss of the standard Shapley selector across singleton bands

For every integer d>=7 let M=d^2. A fixed player of weight M has only {A};
a player of weight 1 chooses {A} or {B}. Put

\[
 c_A(x)=\frac{x^d}{(M+1)^d},\qquad
 \delta_d=\frac{1+(M+1)^{d+1}-M^{d+1}}{2(M+1)^d},\qquad
 c_B(x)=\rho_d=\delta_d/2.
\]

The moving player's A cost is 1, whereas its standard Shapley marginal is
delta_d. Both potential resource scales are 1. Thus the unique minimizer
of Phi chooses B. Also the unscaled standard H chooses B; dividing shares
by each player's band weight and viewing H as a weighted potential has the
same minimizer, since the only moving player's weight is 1.

By the integral identity for a difference of powers and Bernoulli's
inequality,

\[
 \delta_d\ge\frac{d+1}{2}\left(\frac M{M+1}\right)^d
 \ge\frac{d+1}{2}(1-1/d)
 =\frac{d^2-1}{2d}\ge d/3.
\]

Consequently rho_d>=d/6>1. The selected state has best approximation factor
rho_d, although an exact PNE exists with the moving player on A. Every
band is exactly equal-weight, but the resource mixes bands. This blocks an
`o(d)` conclusion from **this selector and only this selector** merely by
replacing a global/resource ratio condition with arbitrary narrow bands.
For an arbitrarily large integer L, add L players of weight 1 and L players
of weight M, each with strategies `empty` and `{A}`. Both bands then have
at least L+1 **potential users of A**, with internal ratio exactly 1. At
every Phi minimum all new players choose empty: any new player on A can
leave, strictly decreasing H by its positive Shapley marginal. Their
presence therefore leaves the unique selected state and its rho_d loss
unchanged. This strengthens the obstruction to arbitrarily dense
potential-user bands on the very same resource. It does not apply to a
hypothesis guaranteeing many **active** users in each band at the selected
state and after deviations; preserving such a hypothesis is a separate
existence obligation.

## Limited literature check and remaining bridge

Primary sources read on 2026-10-14:

* Kollias and Roughgarden, *Restoring Pure Equilibria to Weighted Congestion
  Games*, author-hosted PDF, §§3.2--3.3, standard Shapley shares of `x c(x)`
  and their exact potential:
  <https://theory.stanford.edu/~kkollias/index_files/shapley.pdf>.
* Feldotto, Gairing, Kotsialou and Skopalik, *Computing Approximate Pure Nash
  Equilibria in Shapley Value Weighted Congestion Games*, arXiv v2, Lemma 6:
  `2 phi/(d+1) <= w_i c <= (d+3) phi/4`:
  <https://arxiv.org/pdf/1710.01634>.
* Ren, Wu, Xu and Yang, arXiv:2208.11309, abstract reports bounded-weight
  factor `2W(d+1)/(2W+d+1)` and algorithmic results:
  <https://arxiv.org/abs/2208.11309>.

These establish that the Shapley mechanism and bounded-weight research
direction are existing literature. The literature search was not exhaustive;
priority for the exact local R envelope, or an existing sharper bounded-weight
result, remains unchecked. The local theorem above is proven without importing
the papers' theorems. The new bridge needed for WC-TARGET is a method that
handles resources mixing separated bands with `o(d)` loss. Neither the ratio
lemma nor the failed separate normalizations establish that bridge.

Reproduction: `python tests/audits/weighted_congestion/weight_bands/verify.py` computes and compares the frozen record without changing it. `--generate NEW_PATH` refuses to overwrite existing evidence. Independent reconstruction is recorded in `../dense_band_review/independent_review.md`; selector obstructions retain separate scope.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
