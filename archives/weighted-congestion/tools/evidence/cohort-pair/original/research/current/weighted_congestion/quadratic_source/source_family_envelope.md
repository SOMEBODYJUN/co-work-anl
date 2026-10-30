# 文献两攻击公式：二次参数包络的有理上界

Claim ID: **WC-R1-SOURCE-D2-ENVELOPE v1**. Date: 2026-10-14 UTC.

Status: algebraic proof reconstructed independently, with exact-arithmetic
verification and internal independent review. The earlier `16/15` and
`17/16` exploration was version-zero work, never a canonical claim. This
first canonical statement freezes the `19/18` conclusion on the source's
integer-`n` domain. It is a ceiling for one source optimization formula,
not an existence theorem for all degree-two congestion games.

## Exact statement and scope

For every integer `n >= 1`, `k in {1,2}`, and `w,beta in [0,1]`, set

\[
q=1+w,\quad
N_1=1+n\beta q^2,\quad D_1=(1+nw)^k+n\beta,\quad
N_2=q^k+\beta w^2,\quad D_2=(nw)^k+\beta q^2.
\]

It is impossible to have both strict inequalities

\[
N_1>\frac{19}{18}D_1,
\qquad N_2>\frac{19}{18}D_2.               \tag{T}
\]

Consequently, whenever both denominators are positive,

\[
\min\{N_1/D_1,N_2/D_2\}\leq\frac{19}{18}
<\frac{53}{50}<\frac{17}{16}<\frac{16}{15}.
\]

In particular, the degree-two specialization of Christodoulou et al.,
arXiv:2002.07466v3, equation (3), has supremum at most `19/18`.

Objects and quantifiers: the four displayed polynomials, universally over
the specified parameter domain. Assumptions: no game existence theorem is
imported. Definitions: zero denominators are handled by (T), never by
evaluating `0/0`. Dependencies: elementary algebra and explicit nonnegative
square certificates. Scope/conclusion: a finite-degree source-formula
parameter ceiling. No optimality, new full-class threshold, or infinite-degree
breakthrough is asserted.

## Boundary cases and `k=2`

Always `D1 >= 1`. The second denominator vanishes exactly when
`w=beta=0`; there `N1=D1=1`, so the first strict inequality already fails.
When `w=0`, also `N1=D1=1+n beta`. When `beta=0`, the first quotient is
at most one.

For `k=2`,

\[
N_1-D_1
=n\beta(2w+w^2)-2nw-n^2w^2
\leq n(2w+w^2)-2nw-n^2w^2
=n(1-n)w^2\leq0.
\]

Thus the first quotient is at most one throughout this branch.

## Eliminate `beta` for `k=1`

Fix `t>1`, write `a=q^2`, and suppose `N1 > t D1` and `N2 > t D2`.
The first inequality becomes

\[
n\beta(a-t)>t(1+nw)-1>0.                  \tag{1}
\]

It forces `a>t`, `w>0`, and

\[
\beta>\frac{t(1+nw)-1}{n(a-t)}.
\]

The second inequality becomes

\[
q-tnw>\beta(ta-w^2),                     \tag{2}
\]

where `ta-w^2=t+2tw+(t-1)w^2>0`. Combining (1) and (2) gives

\[
F_t(n,w):=n(a-t)(q-tnw)
 -[t(1+nw)-1](ta-w^2)>0.                \tag{3}
\]

Every division has a verified positive divisor. This branch uses strict
cost inequalities and does not use `beta <= 1`.

As a polynomial in `n`,

\[
F_t(n,w)
=n[(a-t)q-tw(ta-w^2)]-tn^2w(a-t)
 -(t-1)(ta-w^2).                         \tag{4}
\]

## Two square certificates at `t=19/18`

Let `Q=tw(a-t)>0`. Since (4) is quadratic in `n` with leading coefficient
`-Q`, its exact finite-difference identity is

\[
F_t(n,w)=F_t(1,w)+(n-1)[F_t(2,w)-F_t(1,w)]
 -(n-1)(n-2)Q.                           \tag{5}
\]

For integer `n >= 1`, `(n-1)(n-2) >= 0`. At `t=19/18`,

\[
-1296F_t(1,w)
=148w^3+3(24w-7)^2+12w^2+8w+1>0,
\]

\[
-324[F_t(2,w)-F_t(1,w)]
=721w^3+(42w-4)^2+38w^2+10w+2>0
\]

for every `w >= 0`. Each term in (5) is nonpositive, and the first is
strictly negative. Hence `F_t(n,w)<0`, contradicting (3), and proving (T).
No split into `w` intervals is needed. The `k=1` argument does not use
`w <= 1` either.

The integer condition is material to this proof: `(n-1)(n-2)` has the
opposite sign when `1 < n < 2`. We do not claim the `19/18` result on that
additional interval from this certificate.

## Optional weaker certificates for real `n >= 1`

Under `a>t`, (4) is strictly concave in `n`. For real `n >= 1`, it therefore
suffices to show `F_t(1,w)<0` and `partial_n F_t(1,w)<0` for `w >= 0`.

At `t=17/16`,

\[
256F_t(1,w)=-33+190w-355w^2-33w^3<0,
\]

because the quadratic `33-190w+355w^2` has discriminant `-10760`.
Also

\[
256\partial_nF_t(1,w)=-16+241w-898w^2-305w^3.
\]

For `w <= 1/16`, this is at most `-15/16<0`. For `w >= 1/16`, it is
at most `-16+241w-(14673/16)w^2`, whose discriminant is `-611` and whose
leading coefficient is negative. Thus both tests hold.

At `t=16/15`, let `m=n-1 >= 0`. A still shorter certificate is

\[
\begin{split}
225F_t(n,w)
={}&-(31-163w+318w^2+31w^3)\\
 &-m(15-211w+797w^2+271w^3)\\
 &-16m^2w(15w^2+30w-1).
\end{split}
\]

The last term is nonpositive because `15w^2+30w-1=15(a-t)>0`.
The first two brackets are strictly positive, as

\[
31-163w+318w^2=((636w-163)^2+12863)/1272,
\]

\[
15-211w+797w^2=((1594w-211)^2+3299)/3188.
\]

These weaker lemmas also cover `k=2` by its earlier elementary argument.
Their wider real-`n` domain is only an algebraic extension, with no
fractional-player game interpretation.

## Value, source relationship, and limitations

Truth: the proof closes the universal obligation on the source parameter
domain. Value/mechanism: eliminate one parameter, separate `k=2`, and certify
a concave quadratic using its first two integer values. Ambition: a
finite-degree formula-envelope asset. Novelty: no priority claim. The source
reports an approximate optimized value `1.054` for degree two. The proof
does not identify that optimum or prove that `n=1` is optimal. The ceiling
`19/18` sharpens the public-screen team's reported `53/50` safe ceiling.

The parent's separately frozen degree-two game certificate has value
`286/267`, which exceeds `19/18` by exactly `25/1602` (cross-product
difference `75`). That game's certificate lies outside this asset and has
not been re-audited by these subagents. Conditional on that separate
certificate, it strictly exceeds the source formula's entire parameter
envelope. The present proof yields no new all-game threshold certification
by itself.

Evidence/related files: `verify.py` verifies the displayed identities over
the rationals and performs explicitly finite numerical exploration;
`verification.json` records the actual run; `source_audit.md` records the live
primary-source check. Numerical exploration supports, and does not replace,
the universal proof.

Counterevidence/objections: no fatal algebraic objection found in the
independent reconstruction. Division signs, integer dependence, `k=2`, and
zero denominators are addressed above. No exhaustive later-literature or
priority audit has been performed. Internal review is distinct from external
peer review.

Contributors: parent R1 delegated the exact obligation. Subagent
`/root/quadratic_envelope` independently derived `k=2`, parameter elimination,
the `16/15` certificate, and the `17/16` refinement. Subagent
`/root/quadratic_envelope/polynomial_certificate` independently derived the
same `16/15` certificate before reading that derivation, then independently
found the `19/18` finite-difference square certificates. The first subagent
independently expanded and checked the latter certificates. Requested child
configuration: `gpt-6-astra / ultra`, authorized by the repository's
`prompts/MODELS.md`.

Parent `/root` additionally checked both `19/18` square certificates and the
quadratic finite-difference identity with independent Fraction polynomial
code; all passed. This check was reported to this subagent on 2026-10-14.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
