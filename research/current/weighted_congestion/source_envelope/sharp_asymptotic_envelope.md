# 文献两攻击公式：参数上确界的锐渐近证明

Reviewer: R3 internal agent `sharp_source`. Date: 2026-10-14 UTC.

Claim ID: `R3-SOURCE-SHARP-ASYMPTOTIC-v1`.

## Exact statement and scope

For every integer `d >= 2`, put

\[
F_d=\sup_{n,k,w,\beta}\min\{A,B\},\qquad
A=\frac{1+n\beta(1+w)^d}{(1+nw)^k+n\beta},\quad
B=\frac{(1+w)^k+\beta w^d}{(nw)^k+\beta(1+w)^d},
\]

where `n` is an integer at least one, `k` is an integer in `[1,d]`,
`0 < w <= 1`, and `0 <= beta <= 1`. Then

\[
\boxed{\quad F_d\sim\frac{2}{\sqrt e}\,
                  \frac{\sqrt{d\ln\ln d}}{\ln d}\quad}
\qquad(d\longrightarrow\infty\text{ through integers}).
\]

This optimizes precisely the two certified attack ratios of the source
construction. It does not assert that their minimum is the exact best
equilibrium factor of each game, that the source topology is optimal among
other constructions, or that the universal threshold `a_*(d)` has this order.
In particular, the upper bound below is on `F_d`, not on `a_*(d)`.

Status: complete independently reconstructed general proof, submitted for
parent-agent independent attack; not externally reviewed. Numerical evidence
is diagnostic only. No novelty or priority conclusion is claimed here.

Dependencies: elementary real inequalities, the source expression (3), and
the source proof that the two attack cases cover every pure strategy state.
No existing matching order upper bound is imported.

## Source verification

The primary source is Christodoulou, Gairing, Giannakopoulos, Pocas, Waldmann,
*Existence and Complexity of Approximate Equilibria in Weighted Congestion
Games*, [arXiv:2002.07466v3](https://arxiv.org/html/2002.07466v3), dated
2022-03-27 on arXiv, Section 3, Theorem 1, equation (3).

I directly read the primary HTML on 2026-10-14. The source has the same
`n,k,beta` domains, with `w in [0,1]`. Its two cases are: the heavy player
alone on its principal resource; or at least one light player on that
resource. The first ratio is the exact improvement of the heavy player in
the first case. The second is a lower bound on a light player's improvement
in the second case. Its published exhibited asymptotic is
`Omega(sqrt(d)/ln d)`; the specific source choice has
`k=ceil(ln d/(2 ln ln d))`, which differs from the choice below.

We impose `w>0` for a legal positive-weight game. At `w=0`, the first ratio
is one, so that boundary cannot affect an asymptotic tending to infinity.
When `w>0`, both denominators are positive even at `beta=0`.

## Notation

For asymptotics write

\[
D=\ln d,\qquad H=\ln D,\qquad S=\frac{\sqrt{dH}}D,
\qquad c=\frac{\sqrt e}{2},\qquad J=H-\ln(2H).
\]

In the global upper-bound proof, use the different abbreviations

\[
x=nw,\quad E=(1+w)^d,\quad q=\beta E,\quad
p=(1+w)^k,\quad t=(1+x)^k,\quad r=x^k,
\quad \theta=\left(\frac{w}{1+w}\right)^d.
\]

Then `A=(1+nq)/(t+nq/E)` and `B=(p+q theta)/(r+q)`.

## Explicit attaining parameters and complete lower proof

For all sufficiently large integer `d`, choose

\[
w=\frac D{2d},\qquad
n=\left\lfloor\frac{4dH}{D^2}\right\rfloor,\qquad
k=\left\lceil\frac D{2J}\right\rceil,\qquad
q=\frac cS,\qquad \beta=\frac q{(1+w)^d}.
\tag{L1}
\]

All parameters are legal, for example whenever
`d >= ceil(exp(exp(4)))`: then `H>=4` and `J>0`; `w` and `q` are in `(0,1)`,
`0<beta<1`, `4dH/D^2>1`, and `D/(2J)+1<d`. One elementary justification of
the last inequality is `J>=J(4)>1` (because `J'=1-1/H>0` for `H>=4`), so
`k<=D/2+1<exp(D)=d`. The other inequalities follow immediately from
`D>=exp(4)` and exponential growth. This threshold is merely convenient,
not sharp.

Let `N=4dH/D^2`. Since `N->infinity`, rounding gives `n/N->1`. Consequently

\[
x=nw\sim\frac{2H}{D},\qquad
\frac{n}{S^2}\longrightarrow4.
\tag{L2}
\]

The ceil rounding gives `k=D/(2J)+O(1)` and `J/H->1`, hence

\[
kx\longrightarrow1,\qquad kx^2\longrightarrow0,
\qquad kw\longrightarrow0.
\]

It follows from `ln(1+u)=u+O(u^2)` as `u->0` that

\[
t=(1+x)^k\longrightarrow e,\qquad
p=(1+w)^k\longrightarrow1.
\tag{L3}
\]

Also `d w=D/2` and `d w^2=D^2/(4d)->0`, so

\[
E=(1+w)^d\sim\sqrt d.
\tag{L4}
\]

The lower-order term `r` is controlled by an exact one-sided estimate.
Since `n<=N`,

\[
x\le\frac{2H}{D}=e^{-J}<1,
\qquad
r=x^k\le(e^{-J})^{D/(2J)}=e^{-D/2}=d^{-1/2}.
\]

Therefore

\[
\frac rq\le\frac{\sqrt H}{cD}\longrightarrow0.
\tag{L5}
\]

The remaining terms satisfy

\[
\frac{nq}{S}=c\frac n{S^2}\longrightarrow4c,
\qquad
n\beta=\frac{nq}{E}\sim\frac{4c\sqrt H}D\longrightarrow0,
\qquad
\beta w^d\longrightarrow0.
\tag{L6}
\]

For the last assertion, `0<=beta<=1` and `0<w->0`; eventually `w<=1/2`,
so `beta w^d<=2^{-d}`. As `S->infinity`, (L3)--(L6) now give

\[
\frac AS=\frac{1/S+nq/S}{t+n\beta}\longrightarrow
\frac{4c}e=\frac2{\sqrt e},
\qquad
\frac BS=\frac{p+\beta w^d}{S(r+q)}\longrightarrow
\frac1c=\frac2{\sqrt e}.
\tag{L7}
\]

This proves `liminf F_d/S >= 2/sqrt(e)` and independently confirms the
candidate's leading constant with all integer rounding retained.

For each fixed sufficiently large `d` and every `alpha<min(A,B)`, the
source's two cases give a strict improving deviation from every pure state.
Thus these legal parameters also certify the corresponding nonexistence
lower bound in the exact model of `MODEL.md`. The supremum itself need not
be attained for this strict-interval interpretation.

## Exact inequalities for the global upper bound

Take any legal parameters and let `f=min(A,B)>1`. Since `t>=1` and `E>=1`,

\[
A=\frac{1+nq}{t+nq/E}\le E,
\qquad \ell:=\ln f\le d\ln(1+w)\le dw.
\tag{U1}
\]

In particular `w>=ell/d`. From `A>=f` and `B>=f`, respectively,

\[
ft-1\le nq(1-f/E)\le nq,
\qquad
fr+(f-\theta)q\le p.
\tag{U2}
\]

Here `0<=theta<=1`. Thus `q>0`, and multiplication gives

\[
(ft-1)(f-\theta)\le np.
\]

Because `t>=1`, `ft-1>=(f-1)t`; because `theta<=1`, `f-theta>=f-1`.
Therefore the following exact, uniform inequality holds:

\[
\boxed{\ (f-1)^2\le n\frac pt\ }.
\tag{U3}
\]

The second inequality in (U2) also gives `r<=p/f`, so

\[
\left(\frac{x}{1+w}\right)^k\le f^{-1}<1,
\qquad x<1+w\le2.
\tag{U4}
\]

Set

\[
a=\ln\frac{1+x}{1+w}\ge0,
\qquad b=\ln\frac{1+w}{x}>0.
\]

The inequality `a>=0` follows from `x=nw>=w`. Taking logarithms in
`r<=p/f` yields `k>=ell/b`, hence

\[
\boxed{\ (f-1)^2\le\frac xw\exp(-ka)
                    \le\frac xw\exp(-\ell a/b).\ }
\tag{U5}
\]

No relaxation of the integer constraints was needed to derive these
inequalities; using real values in the subsequent upper estimate only
enlarges their feasible range.

## Localization of every potentially maximizing sequence

Fix any constant `c_0>0`. Consider an arbitrary sequence of integer degrees
`d->infinity` and legal parameter quadruples such that

\[
f\ge c_0S.
\tag{U6}
\]

We now prove the required asymptotics along this arbitrary sequence.

As `p/t<=1`, (U3) gives `n>=(f-1)^2->infinity`. By (U4),
`w=x/n<2/n->0`. From (U1), (U4), and (U3),

\[
n=\frac xw\le\frac{2d}{\ell},\qquad
(f-1)^2\le\frac{2d}{\ell}.
\tag{U7}
\]

The lower bound (U6) gives
`ell>=D/2-H+(ln H)/2+ln c_0`, in particular `ell>=D/3` eventually.
Then (U7) gives `f=O(sqrt(d/D))`. Combining the upper and lower logarithmic
bounds,

\[
\ell=\frac D2+O(H),\qquad \ln\ell=H-\ln2+o(1).
\tag{U8}
\]

Next, `x->0`. If this failed, there would be a subsequence with
`x>=epsilon` for some fixed `epsilon in (0,1)`. Since `w->0`, eventually

\[
a\ge\tfrac12\ln(1+\epsilon),\qquad
0<b\le\ln(2/\epsilon).
\]

Writing `gamma_epsilon=ln(1+epsilon)/(2 ln(2/epsilon))>0`, (U5) and (U7)
would imply

\[
(f-1)^2\le\frac{2d}{\ell}\,f^{-\gamma_\epsilon}.
\tag{U9}
\]

This is incompatible with (U6): divided by `S^2=dH/D^2`, the right side is
`O((D/H) f^{-gamma_epsilon})=o(1)`, whereas the left side is bounded away
from zero. This proves `x->0` without presupposing a matching order bound.

Finally, `w/x=1/n->0`, so

\[
a=\ln(1+x)-\ln(1+w)\sim x,\qquad
b=\ln(1/x)+\ln(1+w)\sim\ln(1/x).
\tag{U10}
\]

Thus there exists `eta=eta_d->0`, with `0<=eta<1` eventually, for which
`a/b >= (1-eta)x/ln(1/x)`. With `lambda=(1-eta)ell->infinity`, (U1) and
(U5) give

\[
(f-1)^2\le\frac d\ell\,
 x\exp\left(-\frac{\lambda x}{\ln(1/x)}\right).
\tag{U11}
\]

## Elementary sharp one-dimensional bound

For `lambda->infinity`,

\[
M(\lambda):=\sup_{0<x<1}
 x\exp\left(-\frac{\lambda x}{\ln(1/x)}\right)
\sim\frac{\ln\lambda}{e\lambda}.
\tag{U12}
\]

Here is a full proof. If `x<=1/lambda`, the expression is at most
`1/lambda`. If `x>=1/lambda`, then `ln(1/x)<=ln lambda`, so it is at most

\[
x\exp\left(-\frac{\lambda x}{\ln\lambda}\right)
\le\frac{\ln\lambda}{e\lambda},
\]

the maximum of `u exp(-lambda u/ln lambda)` over `u>0`. When
`ln lambda>=e`, the first region has the same upper bound. Hence in fact
`M(lambda)<=ln lambda/(e lambda)` for all `lambda>=exp(e)`.
For a matching asymptotic lower bound choose `x=ln lambda/lambda`, whose
exponent equals

\[
\frac{\ln\lambda}{\ln\lambda-\ln\ln\lambda}\longrightarrow1.
\]

This proves (U12).

## Completion of the sharp upper bound

Apply (U12) to (U11). Since `lambda/ell->1` and `f->infinity`,

\[
f^2\le(1+o(1))\frac{d\ln\ell}{e\ell^2}.
\]

By (U8),

\[
\limsup\frac{f^2}{S^2}\le
\lim\frac{D^2\ln\ell}{eH\ell^2}=\frac4e.
\tag{U13}
\]

This holds along every sequence satisfying (U6). It implies the same upper
bound for `F_d`: if the claimed bound on its limsup failed, choose a
subsequence and a legal point with `min(A,B)` arbitrarily close to the
supremum on that subsequence. `F_d` is finite because `A<=E<=2^d`.
The lower proof ensures there are points of order `S`, and any point
witnessing a larger limsup satisfies (U6) for a fixed positive `c_0`.
Equation (U13) is a contradiction. Thus
`limsup F_d/S<=2/sqrt(e)`, and (L7) supplies the matching liminf.

## Review obligations and exclusions

The critical independent-attack targets are (U3), the `x->0` localization,
and the passage from arbitrary sequences to a supremum. All three are
proved above. No finite numerical search establishes any part of the upper
bound. The proof allows unbounded `n`, arbitrary real positive `w`, all
integer `k` in its source domain, and both coefficient endpoints. Parameters
with `beta=0` give `A<=1`, so cannot enter (U6). Parameters with `n=1` are
also automatically ruled out by (U3) when `f->infinity`.

The source's certified lower bound improves by a factor of order
`sqrt(ln ln d)` over its exhibited `sqrt(d)/ln d` scale, within precisely
the same parameterized construction. This file does not use the phrase
“new topology” or claim a new existence upper bound. A later-literature
priority search is still needed before any novelty language.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
