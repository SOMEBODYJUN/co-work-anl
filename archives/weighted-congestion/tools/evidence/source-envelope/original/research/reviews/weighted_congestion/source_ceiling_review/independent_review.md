# 文献两攻击公式统一上限：独立重构与反向审查

Review identity: **WC-ENVELOPE-INDEPENDENT-REVIEW v1**, 2026-10-14.
Reviewer: internal clean reconstruction agent under R1. This reconstruction was
completed before reading the candidate ceiling proof. Only the legal domain
`d >= 1`, `n >= 1`, `1 <= k <= d`, `0 < w <= 1`, `0 <= beta <= 1`
is considered. The asymptotic conclusion concerns `d -> infinity` through
integers.

## Exact object and source verification

Write

\[
F={1+n\beta(1+w)^d\over(1+nw)^k+n\beta},\qquad
G={(1+w)^k+\beta w^d\over(nw)^k+\beta(1+w)^d},\qquad R=\min(F,G).
\]

Both denominators are strictly positive on the legal positive-weight domain.
The object is the supremum `A_d = sup R` over these parameters. Theorem 1,
Eq. (3), and the two case proof on PDF pages 5-6 of
https://arxiv.org/pdf/2002.07466v3 were checked directly. The two ratios agree
exactly. The paper includes `w=0` in the optimization display although its
game model requires positive weights; no proposed witness here uses that
endpoint. The source proves an `Omega(sqrt(d)/log d)` lower bound for this
envelope, and its case analysis is a sufficient deviation cover.

An upper bound on `A_d` does **not** upper-bound the universal threshold
`a_*(d)`. Nor does it establish the actual best equilibrium factor of every
game with this topology. The stronger envelope lower bound does give a
stronger nonexistence lower bound through the already checked deviation
cover, for every strict target `alpha < A_d`.

## Autonomous order reconstruction

Set `x=nw`, `q=1+w`, and `T=beta*q^d`. Suppose `R >= 4`. Because
`beta*w^d <= 1 <= q^k`, the light inequality implies

\[
x^k+T\le {2q^k\over R}.
\]

The heavy inequality implies

\[
nT\ge R(1+x)^k-1\ge {R\over2}(1+x)^k.
\]

Therefore

\[
R^2\le 4n\left({q\over1+x}\right)^k,\quad n\ge R^2/4,
\quad x<q\le2.
\]

Also `F <= q^d`, hence `w >= log(R)/d`. Since `n>=2`,

\[
\log{1+x\over q}\ge {x\over6},\qquad
k\ge {\log(R/2)\over\log(q/x)}
\ge {\log R\over2\log(2/x)}.
\]

It follows that, with `t=log(R)/12`,

\[
R^2\le {4d\over\log R}\;
x\exp\left(-{t x\over\log(2/x)}\right).
\]

For `t>=2`, split at `x=1/t`. Below that point the scalar factor is at most
`1/t`; above it use `log(2/x) <= log(2t)` and maximize
`x*exp(-t*x/log(2t))`. This proves

\[
R^2=O\left({d\log\log R\over(\log R)^2}\right).
\]

The same preceding inequality with its scalar factor replaced by `x<2`
gives `R^2 <= 8d/log R`, preventing an exponentially large `R`. Splitting
at `R=d^(1/4)` now gives the required

\[
A_d=O\left({\sqrt{d\log\log d}\over\log d}\right).
\]

An independent legal lower family is obtained by putting `D=log d`,
`H=log D`, `w=D/d`,

\[
n=\left\lfloor {dH\over D^2}\right\rfloor,
\quad k=\left\lceil {D\over2\log(D/H)}\right\rceil,
\quad T=n^{-1/2},\quad \beta=T/(1+w)^d.
\]

For large integer `d`, all parameters are legal,
`x=nw <= H/D`, `x^k <= d^(-1/2)`, and `kx -> 1/2`. Consequently
`(1+x)^k` stays bounded, `n*beta -> 0`, and both ratios are
`Omega(sqrt(n)) = Omega(sqrt(dH)/D)`. This already matches the order of the
upper bound without any optimization or supremum attainment assumption.

## Line-by-line attack on the finite ceiling candidate

File reviewed: `../envelope_ceiling/README.md` as present on 2026-10-14.

The candidate's definitions `E=(1+w)^d`, `Q=beta*E`, `B=(1+w)^k`,
`A=(1+nw)^k`, `z=w/(1+w)`, `y=nz`, `h=log R` are correct. Its exact
light-player inequality is correct, since `(nw)^k=B*y^k` and
`beta*w^d=z^d*Q`. Its exact heavy-player inequality is also correct:
`RA-1 <= nQ(1-R/E)`.

The deductions `Q>0`, `E>R`, `0<y<1`, `y^k<=1/R`, and
`Q<=B/(R-1)` all follow when `R>1`. Combining the two inequalities gives

\[
nB/A\ge (R-1)(R-1/A)\ge(R-1)^2.
\]

For `R>=exp(2)`, the stated last bound `(R-1)^2>=R^2/2` is valid. Since
`B/A<=1`, it legitimately implies `n>=R^2/2` and then `z<1/8`.
The bounds `z>=h/(2d)`, `n<=2dy/h`,
`A/B=(1+(n-1)z)^k >= (1+y/2)^k`,
`k>=h/log(1/y)`, and `log(1+y/2)>=y/4` are all in the correct direction.
Their combination yields the candidate's equation (4) exactly.

The scalar split at `y=1/h` is valid for `h>=2`:
the first branch uses `1<=2log h`; the second branch maximizes a function
over all positive `y`, an admissible upper relaxation. Thus the finite claim

\[
R\ge e^2\implies R^2\le {8d\log\log R\over(\log R)^2}
\]

survives this review. The conversion to `sqrt(128)*sqrt(dH)/D` for `D>=16`
also survives. `log h/h^2` is decreasing on the stated range. The two small
`R` branches are correct; for completeness the sentence `R<e^2 => R<S`
can be supported by noting that `S(D)=exp(D/2)*sqrt(log D)/D` is increasing
on `D>=16` and `S(16)>e^2`.

No mathematical defect was found. At the instant of review,
`envelope_ceiling/verify.py` and `verification.json` were not yet present;
the README's future verification references were therefore not executable.
This is an evidence bookkeeping issue, not a objection to the proof.

## Dangerous boundaries and quantifiers

- `beta=0`: the heavy ratio is `(1+nw)^(-k)<=1`; this cannot be part of a
  growing envelope sequence.
- `n=1`: the autonomous product bound (whose product step is valid already
  for `R>=2`) gives `R<=2`; therefore any growing
  near-optimal sequence must have unbounded `n`.
- Large `w`: the autonomous necessary conditions give `w=x/n<=8/R^2`.
  Thus a sequence with `R->infinity` automatically has `w->0`; this is a
  deduction, not a permission to set a player's weight equal to zero.
- Fixed-parameter `w=0`: the heavy ratio is one. At `(w,beta)=(0,0)` the
  other displayed ratio has zero denominator, so avoid assigning it an
  unqualified value. Legal sequences with simultaneous `n->infinity` and
  `w->0` are covered by the uniform inequalities.
- All floors and ceilings in the explicit lower family contribute vanishing
  relative errors; `n->infinity`, `k<=d` eventually, and a ceiling preserves
  the useful inequality `x^k<=d^(-1/2)`.
- The upper proof bounds every legal parameter tuple. Taking a supremum
  therefore needs no compactness, continuity, or attainment assertion.
- A nonexistence conclusion uses strict `alpha<R`. Given `alpha<A_d`, the
  defining property of a supremum supplies a legal tuple with `R>alpha`;
  no claim of nonexistence at the endpoint `alpha=A_d` follows.

## Sharp constant: independent reconstruction awaiting candidate review

The same bottleneck predicts the sharper constant `2/sqrt(e)`. In the
candidate coordinates `y=nw/(1+w)`, any sequence with
`R>=c*sqrt(dH)/D` for fixed `c>0` has `h~D/2`, `n->infinity`, and `y->0`.
The first fact follows from the finite ceiling and the lower size assumption;
the last follows by applying the attenuation bound to any subsequence with
`y>=epsilon>0`. Then

\[
R^2\le(1+o(1)){d\over h}\,
y\exp\left(-{(1-o(1))hy\over\log(1/y)}\right).
\]

The scalar supremum obeys

\[
\sup_{0<y<1}y\exp\left(-{t y\over\log(1/y)}\right)
\sim {\log t\over et}.
\]

For the upper half, split at `y=1/t`; above that point
`log(1/y)<=log t` gives the exact exponential maximization, and below it
the contribution is `O(1/t)=o(log t/t)`. For the lower half take
`y=log t/t`. This gives `R^2<=(4/e+o(1))*dH/D^2` along every such sequence.
The `o(1)` terms must be justified along an arbitrary sequence, or uniformly
on the stated region, before transferring this to the envelope supremum.

A balancing lower family has `w=D/(2d)`, `n~4dH/D^2`,
`k~D/[2(H-log(2H))]`, and `Q~sqrt(e)/(2S)`, where `S=sqrt(dH)/D`.
Then `(1+nw)^k->e`, `(1+w)^k->1`, `(nw)^k<=d^(-1/2)`,
`(1+w)^d~sqrt d`, and both ratios are `(2/sqrt(e)+o(1))*S`.
This predicts the same sharp constant as the subsequently communicated
candidate. The forthcoming candidate file still needs its own quantifier
and boundary audit.

## Status

Independent reconstruction establishes the proposed `Theta` order and finds
no flaw in the finite ceiling argument. The sharp constant has a complete
independent route, but this file does not yet record a review of the sharp
candidate itself. Internal review only; external peer review and novelty
search have not been performed. No shared claim map or publication state
has been changed by this review.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
