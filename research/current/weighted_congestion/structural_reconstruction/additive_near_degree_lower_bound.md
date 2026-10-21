# 接近次数的全状态门槛：显式加性平方对数余量

**ID/version:** `WC-ADDITIVE-NEAR-DEGREE-ALLSTATE-v1`.

**Status:** complete author proof, personally reconstructed by the lead;
final independent attack is pending. Finite audits verify the stated identities,
not the universal tail. The source construction is the
[fixed-c parameterized account](parameterized_allstate_family.md).

## 1. Exact target and the bottleneck before reading the family

Let (L=\lceil\log_2 d\rceil). The target is a standard finite weighted
congestion game with positive rational weights, positive rational monomial
latencies (a_ex^d), exactly two nonempty disjoint resource-set actions per
player, and

\[
 \forall s\ \exists i,t_i:\quad
 C_i(s)>(d-1200L^2)C_i(t_i,s_{-i}).
\]

Here (C_i(s)=\sum_{e\in s_i}\ell_e(\sum_{j:e\in s_j}w_j)). Every target
resource includes the deviator's own weight. Multiplying both costs of a
player by its fixed weight would not change the conclusion.

Before importing any proposed construction, the quantitative bottleneck is
clear: all losses from endpoint/area conversion, propagation, return defects,
and repair must fit a relative (O(L^2/d)) budget. A theorem for each fixed
(c<1), with a threshold depending on (c), cannot be substituted with a
varying (c(d)) unless that threshold is checked uniformly. In the supplied
family, the fixed-(n) threshold (d\ge(600n)^2) is too coarse for the desired
(n\asymp d/L^2). The actual necessary repair estimate is instead logarithmic:

\[
 d\log(3/2)>200n(\log d)^2.
\]

That estimate is compatible with the target. The other apparent obstruction,
the large endpoint (T\ge16nd), is much cheaper than its original cubic
binomial estimate suggests. The construction and the full replacement tail
are proved below, rather than applying the fixed-(n) theorem outside its
stated range.

## 2. Parameters and a uniform sufficient criterion

We first establish the family for integers (n\ge2,d\ge16) satisfying

\[
 d\ge8n,\qquad T=(1+1/(8n))^d\ge16nd,\qquad
 d\log(3/2)>200n(\log d)^2.                 \tag{A}
\]

All logarithms in the proof are natural unless their base is written. They
are analytic estimates, not irrational inputs to the game.

Define the rational/integer parameters

\[
 \delta=1/n,\quad \alpha=(1-\delta)d,\quad
 \theta=\delta/8,\quad \kappa=1+\theta,\quad b=1-\delta/2,
 \quad K=d^4,\quad R=8nd^4.
\]

Set

\[
 X=\sum_{r=1}^K(1+r/R)^d,\quad Y=\sum_{r=1}^K(r/R)^d,
 \quad H=T-\alpha,\quad J=\alpha X-Y,\quad S=\kappa J/H.
\]

The letter (J) denotes the quantity called (L) in the source family; it
avoids confusing that quantity with the binary logarithm (L) in the target.
Let (g\ge2) be the least integer for which

\[
 b^g\le(192d^2)^{-1},\qquad N=R^g/d,\qquad \varepsilon=R^{-g}.
\]

(N) is integral because (d\mid R). Put

\[
 W=(1+1/d)^d,\quad U=\sum_{r=1}^N(1+r\varepsilon)^d,
 \quad V=\sum_{r=1}^N(r\varepsilon)^d,\quad Z=U-\alpha V,
\]
\[
 A_a=S^a\ (0\le a<g),\qquad A_R=H/(4\alpha W).
\]

## 3. Endpoint, depth, and return estimates

The right Riemann sum for (f(t)=(1+t)^d) gives

\[
 R\frac{(1+\theta)T-1}{d+1}
 \le X\le R\frac{(1+\theta)T-1}{d+1}+T-1.       \tag{B}
\]

Assumption (A) implies (\alpha/T\le\delta/16), so

\[
 H\ge(1-\delta/16)T>T/2>0.
\]

Also (d/R\le\delta/32), and

\[
 \kappa(1-\delta)(1+\theta)
 =(1-\delta)(1+\delta/8)^2\le1-3\delta/4,
 \qquad \kappa(1-\delta)<1.
\]

Using (J\le\alpha X) in (B),

\[
 \frac SR\le
 \frac{\kappa(1-\delta)(1+\theta+d/R)}{1-\alpha/T}
 \le\frac{1-23\delta/32}{1-\delta/16}
 \le1-\delta/2=b<1.                           \tag{C}
\]

Termwise comparison gives

\[
 Y\le\rho X,\qquad
 \rho=\left(\frac\theta{1+\theta}\right)^d\le\theta^2.
\]

Since (\alpha\ge2), (J\ge\alpha X/2>0). The lower bound in (B)
is at least (KT/(d+1)); hence

\[
 \frac JH\ge\frac{\alpha K}{2(d+1)}\ge K/8>1,
 \qquad 1<S\le bR<R.                         \tag{D}
\]

Furthermore, (\theta\le1/16) implies

\[
 Y/J\le\theta^2/(2-\theta^2)\le\theta^2\le\theta/16,
 \quad \alpha X=J+Y\le2J,
 \quad \kappa J-\alpha X=\theta J-Y\ge\theta J/2. \tag{E}
\]

Because (-\log b\ge1/(2n)), for (d\ge4)

\[
 2\le g\le2n\log(192d^2)+1\le13n\log d.       \tag{F}
\]

Here the minimum with (g\ge2) causes no issue: the logarithmic upper
bound is already larger than 2. Since (W<3), (N\varepsilon=1/d), and

\[
 (1+r\varepsilon)^d-\alpha(r\varepsilon)^d
 \ge1-\alpha d^{-d}\ge1/2,
\]

we have (Z\ge N/2>0). Thus

\[
 \frac{A_RZ}{A_{g-1}J}
 =\frac{\kappa Z}{4\alpha W S^g}
 \ge\frac1{24d^2b^g}\ge8.                    \tag{G}
\]

For (g\ge2,R\ge2), the elementary induction
(R^{g-2}\ge2^{g-2}\ge g/2) yields

\[
 N\ge\frac{gR^2}{2d}\ge128gd^7
 \ge24(d+1)(gK+1)>gK.                         \tag{H}
\]

Consequently, for (0\le t\le gK),

\[
 (\alpha+1)(t+1)W\le3(d+1)(gK+1)\le N/8\le Z/4. \tag{I}
\]

## 4. A concrete standard game

There are players (P_{a,j}), (0\le a\le g), (j\in\mathbb Z/N\mathbb Z),
with weight (w_a=R^{-a}). Use representatives (j=0,\ldots,N-1) to define
(\operatorname{pos}(a,j)=j(g+1)+a).

For each adjacent pair (a,a+1), introduce a test ((a,a+1,K,-1)),
with amplitude (A_a). Introduce one return test ((0,g,N,+1)),
with amplitude (A_R). For a test ((a,b,k,o)), each anchor
(h=P_{a,j}) owns a new resource pair (e_{j,0},e_{j,1}).
The anchor selects side equal to its action bit. Its window users are
(u=P_{b,j+t\bmod N}), (t=0,\ldots,k-1). Such a user with action bit
(z_u) selects side

\[
 z_u\mathbin{\mathrm{xor}}
 1[\operatorname{pos}(u)>\operatorname{pos}(h)]
 \mathbin{\mathrm{xor}}1[o=-1].              \tag{J}
\]

Both sides of an adjacent-test pair have latency
((A_a/w_a^d)x^d). Both sides of a return pair have latency (A_Rx^d).
Every pair in every test is distinct. A player's action is the union of
the sides prescribed by its bit over all pairs in which it participates.
Thus there are exactly two actions, they are disjoint, and they are nonempty
because every player participates in at least one test. At this point there
are ((g+1)N) players and (2(g+1)N) resources. All weights and coefficients
are positive rationals.

## 5. All front states have a preserving one-player exit

A front in one class is a bit string with at most one adjacent change.
Encode its (2N) possibilities by (x\in\mathbb Z/(2N)\mathbb Z):

\[
 B_x(j)=\begin{cases}1[j<x],&0\le x<N,\\
                      1[j\ge x-N],&N\le x<2N.
       \end{cases}                           \tag{K}
\]

Forward (x\to x+1) flips clone (x\bmod N); backward (x\to x-1)
flips clone ((x-1)\bmod N). These are actual single-player deviations.

Simultaneously send clone index (j\to j+1\bmod N) in all classes and
flip the bits of precisely the players crossing (N-1\to0). If the wrap
indicators are (e_h,e_u), the order predicate in (J) changes by
(e_h\mathbin{\mathrm{xor}}e_u). The light player's bit flip cancels
(e_u), leaving a common resource-side exchange by (e_h) for the whole
pair. Loads, costs, and costs after a specified one-player deviation are
therefore unchanged. In (K), all phases increase by one. We may normalize
the mover's class phase to zero, without normalizing the other classes.

For an adjacent test, normalize its heavy class to zero and put
(r=x_{a+1}-x_a\pmod{2N}). The heavy forward mover is clone 0; the number
of same-side light users is exactly

\[
 h(r)=\begin{cases}K-\min(r,K),&0\le r\le N,\\
                   \min(r-N,K),&N\le r<2N.
       \end{cases}
\]

Its old/new costs in this test are

\[
 A_a(1+h(r)/R)^d,\qquad A_a(1+(K-h(r))/R)^d. \tag{L}
\]

The backward costs are the reverse of (L) at (r+1\pmod{2N}).
If (r\notin[0,K]\cup[N,N+K]), choose backward for (K<r<N) and
forward for (N+K<r<2N). Its old/new cost is then exactly ((A_aT,A_a)).

We also need an incoming-test bound valid at every relative phase. Normalize
the light class to zero. Its forward mover is clone 0. In the (K) windows
containing it, index the anchors by (-k\bmod N), (0\le k<K). By (J),
the light population currently on its side has size (K-k), while its
target side after the deviation has size (k+1), including itself. For some
(e_k\in\{0,1\}), the old/new costs are therefore

\[
 A_a\sum_{k=0}^{K-1}((K-k)/R+e_k)^d,\qquad
 A_a\sum_{k=0}^{K-1}((k+1)/R+1-e_k)^d.       \tag{M}
\]

Each is at most (A_aX). Backward edges reverse a forward edge in a
different phase, so the same two-sided bound applies.

For a mismatched adjacent pair, the selected heavy mover in class 0 has
total old-minus-(\alpha)-new margin at least

\[
 H-\alpha A_RW=3H/4.
\]

A selected mover in class (1\le a<g) instead has margin at least

\[
 A_aH-\alpha A_{a-1}X
 =A_{a-1}(\kappa J-\alpha X)
 \ge(\theta/2)A_{a-1}J\ge\theta H/2.         \tag{N}
\]

If there is no such mismatch, each adjacent difference is

\[
 x_{a+1}-x_a=k_aN+t_a\pmod{2N},\quad
 k_a\in\{0,1\},\quad0\le t_a\le K.
\]

Hence (x_g-x_0=kN+t\pmod{2N}), where (k) is a parity and
(0\le t\le gK<N). Normalize the last class to zero and write
(r=x_0-x_g). In the return test, let (h_k=-k\bmod N),
(\sigma_0=1), (\sigma_k=0) for (k>0), and
(e_k(r)=1[B_r(h_k)=\sigma_k]). The last class's forward mover has
unscaled old/new return costs

\[
 O(r)=\sum_{k=0}^{N-1}((N-k)\varepsilon+e_k(r))^d,
 \quad Q(r)=\sum_{k=0}^{N-1}((k+1)\varepsilon+1-e_k(r))^d. \tag{O}
\]

The all-one (e)-vector gives ((U,V)), and the all-zero vector gives
((V,U)). Flipping one (e_k) changes each cost by at most (W).
If (k=0), use forward with (r=-t): at (t=0), only (e_0=0);
at (1\le t<N), precisely (e_0,\ldots,e_t=0). If (k=1), use backward,
whose costs are (Q(r+1),O(r+1)), with (r=N-t). At (t=0) its (e)-vector
is all zero; at (1\le t<N), it has exactly (t) ones. Thus the selected
return margin is at least

\[
 A_R\{Z-(\alpha+1)(t+1)W\}\ge3A_RZ/4.
\]

By (G), (E), and (M), including its incoming adjacent test gives margin

\[
 3A_RZ/4-\alpha A_{g-1}X
 \ge6A_{g-1}J-2A_{g-1}J
 =4A_{g-1}J>\theta H/2.                     \tag{P}
\]

This covers every vector of fronts. Consequently every such state has a
front-preserving real one-player deviation with margin at least

\[
 \eta=\theta H/4>0.                         \tag{Q}
\]

The proof does not replace coverage of all fronts by a sweep cycle.

## 6. A same-degree repair of every remaining state

For every pure state, not just front states, a valid upper bound on each
base-game cost is

\[
 B_*=(g+1)R^gT.
\]

Indeed adjacent resources have potential normalized load (1+\theta),
and a player's contribution from any test is at most (KA_aT). Their sum
is at most (gKS^{g-1}T\le gR^gT). The return contribution is at most
(NA_RW=NH/(4\alpha)\le R^gT). From (H>T/2),

\[
 B_*/\eta\le64n(g+1)R^g.                    \tag{R}
\]

Let (L_c=\binom{N-1}{2}\ge1), (M=2\alpha B_*). For each class and
each (1\le i<j<N), add a new pair of resources used only by clones
(0,i,j). Their chosen sides are their action bits xor ((0,1,0)), and
both resource latencies are

\[
 M\left(\frac{x}{3w_a}\right)^d.            \tag{S}
\]

This keeps the same players, weights, and two action labels. The three
players are all together precisely for local patterns 010 and 101; then
each pays (M). In every other pattern each costs at most (M\zeta),
where (\zeta=(2/3)^d). Each player participates in at most (L_c) pairs.
All pairs are untriggered precisely for front bit strings.

Suppose

\[
 \zeta\le\frac\eta{4\alpha^2B_*L_c}.        \tag{T}
\]

On a front state, the deviation from (Q) ends on a front. Its new clock
cost is at most (L_cM\zeta), so its full margin is at least
(\eta-\alpha L_cM\zeta\ge\eta/2>0).

On a nonfront class, let (b) be its first bit and (i>0) its earliest
different bit. Because the string is nonfront there is a later (j) with
bit (b), so clock ((0,i,j)) triggers. Flip only player (i) back to
(b). Its old clock cost is at least (M). In any clock containing it,
if it is the middle index it now equals the anchor; if it is the last index,
the middle index preceded (i) and already equaled the anchor. All its
new clocks are therefore untriggered. Its real new base cost is at most
(B_*). Its full margin is at least

\[
 M-\alpha B_*-\alpha L_cM\zeta
 \ge\alpha B_*-\eta/2\ge\eta/2>0.          \tag{U}
\]

This is a current single-player deviation, not a simultaneous repair.
The last inequality uses (B_*\ge T>\eta) and (\alpha\ge1).

It remains essential to check (T) with the actual degree (d). By (R),
(L_c\le N^2\le R^{2g}), and (\alpha\le d), it suffices to bound

\[
 \frac{4\alpha^2B_*L_c}{\eta}
 \le\Gamma:=256nd^2(g+1)R^{3g}.             \tag{V}
\]

The assumptions (n\le d/8), (d\ge16) imply

\[
 \log R\le5\log d,\quad g\le13n\log d,
 \quad g+1\le14n\log d\le14d\log d\le d^3.
\]

Consequently

\[
 \log\Gamma
 \le195n(\log d)^2+8\log d
 \le200n(\log d)^2<d\log(3/2),              \tag{W}
\]

where the last inequality is exactly (A). Hence
((2/3)^d<\Gamma^{-1}\le\eta/(4\alpha^2B_*L_c)), proving (T).
Every latency in the final game has degree exactly (d).

Thus assumptions (A) yield a finite rational game in which every pure state
has a strict (\alpha=(1-1/n)d) improvement. The total resource count is

\[
 2(g+1)N+2(g+1)\binom{N-1}{2}.
\]

The sizes are huge but finite; no polynomial encoding-size claim is made.

## 7. The uniform (d-1200\lceil\log_2d\rceil^2) tail

For every integer (d\ge d_0:=2^{20}), define

\[
 L=\lceil\log_2d\rceil,\qquad
 n=\left\lceil\frac{d}{1200L^2}\right\rceil. \tag{X}
\]

First (d>1200L^2) uniformly. At (d=2^{20}), this is the integer
comparison (2^{20}>1200\cdot20^2). For (L\ge21), use
(d>2^{L-1}) and (2^{20}>1200\cdot21^2). The latter inequality
propagates to every larger (L), because
(2(L/(L+1))^2\ge1) for (L\ge3). Thus (n\ge2), and rounding yields

\[
 \frac{d}{1200L^2}\le n
 \le\frac{d}{1200L^2}+1
 \le\frac{d}{600L^2}.                       \tag{Y}
\]

In particular (d\ge8n). The elementary inequality
(\log(1+x)\ge x/(1+x)), with (x=1/(8n)), gives

\[
 \log T\ge\frac{d}{8n+1}\ge\frac{d}{9n}
 \ge\frac{200}{3}L^2.
\]

Since (n\le d), (\log d\le L\log2<L), and (\log16<4),

\[
 \log(16nd)\le\log16+2\log d<4+2L
 <\frac{200}{3}L^2\le\log T.
\]

This proves (T>16nd), without a fixed-(n) asymptotic argument or a
condition (d\gg n^2).

Finally (Y) gives

\[
 200n(\log d)^2
 \le\frac d3\left(\frac{\log d}{L}\right)^2
 \le\frac d3(\log2)^2
 <d/3<d\log(3/2).                           \tag{Z}
\]

The last inequality follows from
(\log(3/2)=\int_1^{3/2}dt/t>\frac12\cdot\frac23=1/3).
All assumptions (A) therefore hold for every integer (d\ge2^{20}).
Moreover (X) implies

\[
 \alpha=d-d/n\ge d-1200L^2.
\]

The full game has margin (C_i(s)-\alpha C_i(t_i,s_{-i})\ge\eta/2>0)
for some real deviation at each pure state. Since target costs are
nonnegative, the same strict inequality holds with
(d-1200L^2\le\alpha). This establishes the exact requested quantifiers:

\[
 \forall d\in\mathbb Z_{\ge2^{20}}\ \exists G_d\ \forall s\ \exists i,t_i:
 \quad C_i(s)>(d-1200\lceil\log_2d\rceil^2)C_i(t_i,s_{-i}).
\]

Every (G_d) is standard, finite, rational, and pure monomial of degree (d).
Its two actions per player remain disjoint and nonempty after the clocks.
At the stated threshold the displayed approximation factor is positive.

## 8. What is and is not certified

The main new step is the uniform substitution (X) and the replacement of
the original (n^2) threshold by the actual conditions (A). Sections 2–6
also reproduce the construction and its all-state proof so that this note
can be reviewed without accepting an old theorem on trust.

The companion `audit.py` independently checks finite endpoint identities,
the wrap symmetry, the parity defect counts, and the earliest-error clock
repair from actual resource sides. It also checks integer rounding on large
example degrees. Those checks can catch transcription errors but do not
prove this infinite tail. The proof of the tail is (Y)–(Z), and the proof of
the all-state conclusion is the classification in Sections 5–6.

This note makes no novelty claim, does not assert an optimal finite-degree
constant, and does not infer nonexistence merely from a loop or a local
contraction.
