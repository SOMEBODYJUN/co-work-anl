# R3 independent topology attack: versions 1–3

Claim reviewed: **WC-R3-FULL-TOPOLOGY-REDUCTION v3**. Reviewer: R3 topology
attack subagent. Review date: 2026-10-14. This is an internal mathematical
review, not an external review or a novelty certification.

The reviewer first read `MODEL.md`, `ACCEPTANCE.md`, and the applicable
`AGENTS.md` files, reconstructed the full state bottleneck independently,
and only then received the candidate proof interface and read
`../full_topology/proof.md`. All writes in this review are confined to this
directory. No Git mutation or public-board write was performed.

**Verdict:** the complete reduction is valid at the strengthened threshold
\(\rho=(1+\sqrt3)/2\), for every \(w>0\). No fatal objection remains in
the stated symmetric, identical-light-weight topology. The version history
must remain explicit:

* v1: full reduction for \(\alpha\ge2\), all \(w>0\).
* v2: full reduction for \(\alpha\ge\phi=(1+\sqrt5)/2\), all \(w>0\).
  The originally suggested \(w\le1\) restriction is unnecessary.
* v3: full reduction for \(\alpha\ge\rho\), all \(w>0\), by converting the
  remaining one-light right branch rather than excluding it.

The result is existential: it produces a new legal game with a source
certificate. It does not identify each original game's best factor with
the source certificate, nor imply an upper bound for the full MODEL.md class.

## Exact reviewed statement

For each integer \(d\ge1\), consider one weight-1 player choosing either
entire column \(a_0,\ldots,a_n\) or \(b_0,\ldots,b_n\), and \(n\ge1\)
weight-\(w>0\) players, where light player \(i\) chooses
\(\{a_0,b_i\}\) or \(\{b_0,a_i\}\). Both main costs are a common
nonnegative-coefficient polynomial \(F\), and all side costs are a common
such polynomial \(G\), each of degree at most \(d\).

For every \(\alpha\ge\rho\), if this game has no \(\alpha\)-PNE, there
exist an integer \(N\ge1\), \(0<\omega\le1\), \(1\le k\le d\), and
\(0<\beta<1\) such that

\[
1+N\beta(1+\omega)^d>
\alpha\bigl[(1+N\omega)^k+N\beta\bigr],
\]
\[
(1+\omega)^k+\beta\omega^d>
\alpha\bigl[(N\omega)^k+\beta(1+\omega)^d\bigr].
\]

The preliminary polynomial reduction retains the original \(w\) in its
left branch. The right one-light branch can replace it by \(1/w\).
Thus a statement requiring the same \(w\) throughout is proved at
\(\alpha\ge\phi\), but is not claimed by the v3 argument below.

## Independent reconstruction of all states

Fix the heavy player in column A, and let \(m\) light players use \(a_0\).
Write \(u=G(1),v=G(1+w),z=G(w)\). The heavy player's current and switched
costs are

\[
h_m=F(1+mw)+mu+(n-m)v,\qquad h_{n-m}.
\]

A light player using the heavy player's main resource has current cost
\(F(1+mw)+z\), and switched cost \(F((n-m+1)w)+v\). A light player on
the other main resource has current cost \(F((n-m)w)+v\), and switched
cost \(F(1+(m+1)w)+z\). The resource swap between columns covers every
state with the heavy player in B. No other unilateral deviations exist.

If \(F\not\equiv0\), define for \(1\le m\le n\)

\[
L_m=\frac{F(1+mw)+z}{F((n-m+1)w)+v}.
\]

Every denominator is positive. The numerator is nondecreasing and the
denominator is nonincreasing, so \(L_m\) is nondecreasing. Light stability
means \(L_m\le\alpha\) when \(m>0\), and
\(L_{m+1}\ge1/\alpha\) when \(m<n\). Consequently the light-stable
states form a nonempty integer interval \(I=[a,b]\).

One direct nonemptiness argument takes the smallest \(m\) with
\(L_{m+1}\ge1/\alpha\), or \(m=n\) if there is none. For \(m>0\),
the preceding ratio is \(<1/\alpha\le\alpha\), so this state also
satisfies its same-main-resource light test.

Under no-PNE, each \(m\in I\) must have \(h_m>\alpha h_{n-m}\).
If \(I\cap(n-I)\ne\varnothing\), both members of a reflected pair lie
in \(I\), demanding two incompatible reciprocal strict inequalities.
Therefore exactly one of \(2b<n\) and \(2a>n\) holds. The integer
endpoints matter: for even \(n\), the central state is automatically
heavy-stable; for odd \(n\), both adjacent central states being light-stable
already supplies a reflected pair.

## Left branch: translation is forced

When \(2b<n\), put \(N=n-2b\) and \(F'(x)=F(x+bw)\). Heavy instability
at \(m=b\) is

\[
F'(1)+Nv+b(u+v)>
\alpha\bigl[F'(1+Nw)+Nu+b(u+v)\bigr].
\]

Subtracting the common nonnegative term improves the strict margin by
\((\alpha-1)b(u+v)\), yielding the first requested conservative test.
Since \(b\) is the upper endpoint of the stable interval, the next state
fails only its same-main-resource light condition, so
\(L_{b+1}>\alpha\). Exactly, without an off-by-one approximation,

\[
F'(1+w)+z>\alpha\bigl[F'(Nw)+v\bigr].
\]

The binomial expansion of \(F(x+bw)\) has nonnegative coefficients and
degree at most \(d\). It can create a constant term; the model allows one.
This establishes the original same-weight translation interface whenever
the right branch is excluded.

## Right branch: the stronger obstruction and the remaining conversion

When \(2a>n\), put \(r=n-a\), \(N=2a-n\), and \(F'(x)=F(x+rw)\).
Let \(A=F'(1)\), \(B=F'(1+Nw)\), and \(C=F'(w)\). Heavy instability
at \(m=a\), with its common side term deleted, gives

\[
B+Nu>\alpha(A+Nv).
\tag{R1}
\]

At \(m=a-1\), the same-main-resource light condition holds when present:
\(L_{a-1}\le L_a\le\alpha\). Thus its failed condition is exactly
\(L_a<1/\alpha\), giving

\[
C+v>\alpha(B+z).
\tag{R2}
\]

All of \(A,B,C,u,v,z\) are nonnegative, \(A,B>0\), and \(u\le v\).
The following two cases cover every weight, including their common boundary.

If \(w\le1\), then \(C\le A\). From (R1) and (R2),

\[
B>\alpha A+N(\alpha-1)v,\qquad A+v>\alpha B,
\]

and therefore

\[
[1-N\alpha(\alpha-1)]v>(\alpha^2-1)A\ge0.
\tag{R3a}
\]

If \(w\ge1\), then \(z\ge u\), while \(C\le B\) because
\(w\le1+Nw\). Thus (R2) gives
\(v>(\alpha-1)B+\alpha u\). Substitution into (R1) yields

\[
[1-N\alpha(\alpha-1)]B>
\alpha A+N(\alpha^2-1)u\ge0.
\tag{R3b}
\]

Both cases force

\[
N\alpha(\alpha-1)<1.
\tag{R3}
\]

For \(\alpha\ge\phi\), (R3) rules out every integer \(N\ge1\).
This proves v2 for all weights, strengthening the original proposed
\(w\le1\) extension. At \(w=1\), both derivations apply and preserve
strictness; no equality exception exists.

For \(\alpha\ge\rho\), \(\alpha(\alpha-1)\ge1/2\), so (R3) forces
\(N=1\). Define

\[
\widetilde w=1/w,\qquad
\widetilde F(x)=F'(wx),\qquad
\widetilde G(x)=G(wx).
\]

The desired left heavy test is then exactly (R2), because its costs are
\(\widetilde F(1)=C\), \(\widetilde G(1+\widetilde w)=v\),
\(\widetilde F(1+\widetilde w)=B\), and \(\widetilde G(1)=z\).
The desired left light test is exactly (R1), because
\(\widetilde G(\widetilde w)=u\) and
\(\widetilde F(\widetilde w)=A\). Positive scaling preserves polynomial
degree and coefficient signs. Notice that **this conversion does not
exchange F and G**; their exchange belongs to the subsequent source
normalization for an already-left one-light certificate with weight above 1.

At the exact endpoint \(\alpha=\rho\), a hypothetical \(N=2\) makes
the left coefficient in (R3a)/(R3b) zero, contradicting a strict positive
right side. The endpoint is therefore included.

## Polynomial-to-source step

The two left tests alone, with \(\alpha>1\), imply
\(F(1+w)>F(nw)\), using \(z\le v\). Hence \((n-1)w<1\).
For \(n\ge2\), this forces \(w<1\). For \(n=1,w>1\), exchange the two
players and rescale weights: the tests exchange places under

\[
w''=1/w,\qquad F''(x)=G(wx),\qquad G''(x)=F(wx).
\]

Direct substitution checks both equations. Thus the source normalization
may assume \(0<w\le1\). The first left test makes \(G\equiv0\) impossible,
so \(G(1+w)>0\) and its normalization is legitimate.

For a monomial of degree \(j\), normalize its value at \(1+w\) to 1.
Its values at \(1,w\) are
\(U_j=(1+w)^{-j}\) and \(Z_j=(w/(1+w))^j=U_j^p\), with \(p\ge1\).
The endpoint chord of the convex function \(U^p\), on
\([(1+w)^{-d},1]\), dominates every degree-\(j\) point.
It produces a nonnegative mixture of constant and degree-\(d\) costs,
preserving \(G(1)\) and \(G(1+w)\), and increasing \(G(w)\).
The first test is unchanged and the second margin can only improve.

Delete the constant coefficient \(c\). The heavy and light strict margins
increase by \(n(\alpha-1)c\) and \((\alpha-1)c\), respectively. The
remaining degree-\(d\) coefficient is positive: if it vanished, the first
test would read \(F(1)>\alpha F(1+nw)\), which is impossible.

Writing the resulting side cost as \(\beta x^d\), set \(E=(1+w)^d\).
Its two bounds on \(\beta\) are

\[
\frac{\alpha F(1+nw)-F(1)}{n(E-\alpha)}
<\beta<
\frac{F(1+w)-\alpha F(nw)}{\alpha E-w^d}.
\]

The left numerator is positive, so \(E>\alpha\); both denominators are
strictly positive. Cross multiplication gives a strict linear functional
of the nonnegative coefficients of \(F\). At least one supported monomial
has a positive functional value. Degree zero has value
\((1-\alpha)[n(E-\alpha)+(\alpha E-w^d)]<0\), so the selected degree
lies in \(1,\ldots,d\).

Normalize that monomial to coefficient 1 and choose \(\beta\) between its
strict bounds. The lower endpoint is positive. The upper endpoint is below
1 since

\[
(1+w)^k+w^d\le(1+w)^d+(nw)^k
<\alpha\bigl[(1+w)^d+(nw)^k\bigr].
\]

This checks the source restrictions \(k\le d\), \(w\le1\), and
\(0<\beta<1\), without replacing arbitrary real coefficients by rational
coefficients in the theorem.

## Zero and equality boundaries

* \(F\equiv0\): \(m=n\) is an exact PNE, since each light has cost
  \(z\le v\) and the heavy has \(nu\le nv\). A nonzero constant F
  has the same conclusion.
* \(G\equiv0\): this is a weighted two-resource load-balancing game on
  the main resources. A strict cost improvement implies its old load
  exceeds the target load after the move, so it decreases the sum of the
  squares of the two main loads. A finite minimizer gives an exact PNE.
* \(F=G=0\): all costs are zero; every state is an exact PNE. No 0/0 ratio
  is used anywhere.
* \(d=0\): both costs are constant and an exact PNE exists. The source
  monomial conclusion is stated for \(d\ge1\); the no-PNE implication
  for \(d=0\) is vacuous.
* \(w=1\): the unit-weight potential
  \(\sum_e\sum_{j=1}^{x_e}c_e(j)\) changes by the moving player's cost
  difference, so a finite minimum is an exact PNE. Independently, both
  right-branch inequalities above apply at this boundary.
* Equality in a stability test is retained as stability. Failure is
  strictly greater, or strictly less for its reciprocal. Deleting common
  nonnegative costs preserves strictness, including when they are zero.
* \(b=0\) and \(a=n\) are allowed; no missing player's test is imposed.
  The translated residual size is always an integer at least 1.

## Supremum consequence and its precise limit

Define \(T_{\rm source}(d)\) as the supremum of the minimum of the two
source ratios over \(n\in\mathbb Z_{\ge1}\), \(0<w\le1\),
\(1\le k\le d\), \(0<\beta<1\). Define \(T_{\rm topology}(d)\) as
the supremum of finite-instance best \(\alpha\)-PNE factors for all games
of the topology reviewed here.

The source tests cover every state: \(m=0\) has the strict heavy deviation;
each \(m>0\) has a strict same-main-resource light deviation because its
current cost is at least the test's current cost and its deviation cost
is at most the test's deviation cost. Thus

\[
T_{\rm source}(d)\le T_{\rm topology}(d)
\le\max\{\rho,T_{\rm source}(d)\}.
\]

For the upper inequality, suppose an individual game had a best factor
strictly greater than that maximum. Choose a strictly intermediate real
\(\alpha\); the game has no \(\alpha\)-PNE, so the reviewed reduction
produces a source minimum strictly greater than \(\alpha\), contradicting
the defining supremum. This remains valid if a supremum is not attained.
In particular equality follows whenever \(T_{\rm source}(d)\ge\rho\).
The requested \(\max\{\phi,T_{\rm source}\}\) consequence is a weaker
immediate corollary.

This comparison relies on the stated parameter domain. If the external
formula-(3) uses a different domain, its equivalence must be separately
checked; this review proves the source-domain comparison written above,
not an unverified bibliographic identification or optimal asymptotic.

## Finite evidence

`check_review.py` independently constructs each player's literal resource
memberships, recomputes post-deviation loads, and compares every pure state's
costs with the compressed formulas. It checks the interval, reflected-pair
obstruction, left translation, right one-light conversion, chord replacement,
constant deletion, and monomial selection using `fractions.Fraction` only.
The suite contains zero/constant costs, degree zero, weights below/equal/above
1, fixed-seed mixed polynomials, and deliberate high-degree certificates for
both left and right branches. `review_results.json` records the actual run.
These finite checks validate the implementations in their recorded range;
the general proof above supplies the theorem's real-domain quantifiers.

No claim concerning novelty, external review, heterogeneous light weights,
asymmetric resource costs, or the universal \(a_*(d)\) is certified here.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
