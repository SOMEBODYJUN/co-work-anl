# Two conservative attacks: arbitrary polynomial costs give no larger threshold

## Claim identity

- **ID/version:** WC-R1-TWOATTACK-POLYNOMIAL-REDUCTION v1.
- **Exact statement:** Fix an integer `d >= 2` and a real `alpha > 1`. If a symmetric two-column gadget with one weight-1 player, `n >= 1` weight-`w > 0` players, and arbitrary nonnegative-coefficient polynomials `P,Q` of degree at most `d` satisfies both strict inequalities (H) and (L) below, then there is a gadget in the parameter domain of arXiv:2002.07466v3 equation (3), with main cost `x^k`, side cost `beta x^d`, `1 <= k <= d`, `0 < w' <= 1`, `0 < beta < 1`, and the same number of light players, satisfying both strict conservative attack inequalities at the same `alpha`. The output game need not equal the input game.
- **Objects/domain:** Finite games in WC-TARGET v1. The subclass has resources `a_0,...,a_n,b_0,...,b_n`; heavy strategies are the two whole columns; light player `i` has strategies `{a_0,b_i}` and `{b_0,a_i}`. Resources `a_0,b_0` use `P`; all side resources use `Q`. Costs do not multiply the player's weight.
- **Quantifiers:** For every `d,n,w,P,Q,alpha` in the preceding domain, existence of the two strict certificates implies existence of output parameters. This does not assert that every game without an `alpha`-PNE satisfies these certificates.
- **Assumptions/definitions:** Nonnegative coefficients, degree at most `d`; all player weights positive. A strict attack means current cost `> alpha` times deviation cost, including zero-cost boundary cases. The two tests are defined by their original inequalities, never by a quotient with a possibly zero denominator.
- **Scope:** Only the two state-independent lower estimates used in the source theorem. Other attacks, the exact full-state optimum, asymmetric weights, different side costs per player, and multiple layers are outside the conclusion.
- **Conclusion:** Allowing arbitrary symmetric polynomial `P,Q` does not improve equation (3) **through these two conservative certificates**. This is an obstruction to that proof interface, not an upper bound on `a_*(d)` or on this family's true full-state nonexistence factor.
- **Dependencies:** Elementary monotonicity of nonnegative-coefficient polynomials, convexity of a power function, and a finite weighted average. No universal equilibrium-existence theorem is invoked.
- **Evidence:** Complete proof below; exact rational regression in `verify.py` and frozen `verification.json`. The two contributors reconstructed the `P` and `Q` reductions separately, then composed them.
- **Counterevidence/objections:** The source estimates can be strictly weaker than the genuine full-state analysis. In particular the monomial game `d=2,n=3,k=1,w=1/5,beta=1/2` has a conservative minimum `61/66 < 1`; the main R1 conversation independently checks an exact full-state factor `157/156 > 1`. Thus this claim cannot eliminate improvement by full-state optimization. The `w=0` endpoint is excluded as a legal-game parameter, and no limiting ratio is substituted for a strict inequality.
- **Status:** DERIVED OBSTRUCTION; general proof reconstructed here; independent adversarial review pending. Truth is the stated interface theorem only; novelty versus prior literature is unverified; no WC-TARGET breakthrough claimed.
- **Related files:** `side_polynomial/Q_ENDPOINT_REDUCTION.md`, `verify.py`, `verification.json`, branch `MODEL.md`, `PRIOR_ASSETS.md`, `CLAIMS.md`.
- **Contributors:** R1 internal agents `lower_extension` (normalization, main-cost elimination, arbitrary-weight closure, composition) and `lower_extension/side_polynomial` (side-cost endpoint reduction). Actual inherited model configuration is not reported by the tool.

## Source and the two strict tests

Primary source checked independently: <https://arxiv.org/html/2002.07466v3>, Section 3, Theorem 1, equation (3), and its two-case proof. The source polynomial class and cost convention agree with WC-TARGET v1. The new reduction below is not attributed to that source.

Let `r=nw`. If the heavy player is alone on its main resource, its exact current and deviation costs are `P(1)+nQ(1+w)` and `P(1+r)+nQ(1)`. If the heavy player shares its main resource, any sharing light player has current cost at least `P(1+w)+Q(w)` and deviation cost at most `P(r)+Q(1+w)`. Therefore the following two strict tests suffice to cover all states:

\[
\tag{H} P(1)+nQ(1+w)>\alpha[P(1+nw)+nQ(1)],
\]
\[
\tag{L} P(1+w)+Q(w)>\alpha[P(nw)+Q(1+w)].
\]

The theorem concerns simultaneous feasibility of exactly these tests. In a state where several light players share the main resource, their real deviation costs can be substantially smaller than the estimate in (L).

## 1. Reduce to `0 < w <= 1`

Suppose first `w>1` and `n>=2`. Then `nw>=1+w`; monotonicity gives `P(nw)>=P(1+w)` and `Q(1+w)>=Q(w)`. Consequently the left side of (L) is at most its bracketed right side, so (L) is impossible for `alpha>1`, even if some costs vanish.

For `n=1,w>1`, exchange the two players, divide all weights by `w`, exchange the roles of main and side resources, and set

\[
w'=1/w,\qquad P'(x)=Q(wx),\qquad Q'(x)=P(wx).
\]

These are still nonnegative-coefficient degree-at-most-`d` costs, and `0<w'<1`. The new (H) is exactly the old (L), and the new (L) is exactly the old (H):

\[
P'(1)+Q'(1+w')=Q(w)+P(1+w),
\]
\[
P'(1+w')+Q'(1)=Q(1+w)+P(w),
\]
\[
P'(1+w')+Q'(w')=Q(1+w)+P(1),
\]
\[
P'(w')+Q'(1+w')=Q(1)+P(1+w).
\]

A concrete resource relabeling is: new `a_0=old b_1`, new `a_1=old a_0`, new `b_0=old a_1`, new `b_1=old b_0`. The new heavy player is the old light player. The old heavy player's two strategies become the new light player's two cross-column strategies. Hence no strategic or cost-model change is hidden in the formula. All subsequent steps may assume `0<w<=1`.

## 2. Reduce the side polynomial to degree `d`

Write `a=1+w`, `A=a^d>1`, and `Q(x)=sum_{j=0}^d b_j x^j`, with `b_j>=0`. Define

\[
C=\sum_j b_j\frac{A-a^j}{A-1},\qquad
D=\sum_j b_j\frac{a^j-1}{A-1}.
\]

Both coefficients are nonnegative. The polynomial `Qtilde(x)=C+D x^d` satisfies

\[
\widetilde Q(1)=Q(1),\qquad \widetilde Q(a)=Q(a),\qquad
\widetilde Q(w)\ge Q(w).
\]

For the last assertion put `u_j=a^{-j}` and `v_j=(w/a)^j`. They satisfy `v_j=u_j^t`, where

\[
t=\frac{\log(a/w)}{\log a}\ge1 \qquad (0<w\le1).
\]

Convexity puts `(u_j,v_j)` below the chord joining the endpoints `j=0,d`. Multiplying this chord inequality by `a^j` gives

\[
\frac{A-a^j}{A-1}+\frac{a^j-1}{A-1}w^d\ge w^j.
\]

Summing with weights `b_j` proves the last comparison. At `w=1` the curve is linear, so equality is allowed; at `j=0,d` it is also equality. Thus there is no omitted endpoint.

Replacing `Q` by `Qtilde` leaves the strict margin of (H) unchanged and weakly increases the strict margin of (L). Now delete its constant term, taking `Qhat(x)=D x^d`. The (H) margin increases by `n(alpha-1)C`; the (L) margin increases by at least `(alpha-1)C`. Hence both strict inequalities survive. If `D=0`, (H) would say `P(1)>alpha P(1+nw)`, impossible by monotonicity; thus any feasible input yields `D>0`.

## 3. Normalize the main polynomial and eliminate the side coefficient

Feasibility of (L) also implies `P` is not identically zero: otherwise `Q(w)<=Q(1+w)` makes (L) impossible. Thus `P(1)>0`. Divide all costs by this positive number. Write

\[
P(x)=\sum_{k=0}^d p_kx^k,\qquad p_k\ge0,\qquad \sum_kp_k=1,
\]

and `Q(x)=beta x^d`, with `beta>0`. Keep `r=nw`, and put

\[
A=(1+w)^d,\qquad \rho=\left(\frac{w}{1+w}\right)^d,\qquad b=\beta A.
\]

The two original strict margins become

\[
\tag{H'} n(1-\alpha/A)b>\alpha P(1+r)-1,
\]
\[
\tag{L'} (\alpha-\rho)b<P(1+w)-\alpha P(r).
\]

Since `P(1+r)>=1` and `alpha>1`, the right side of (H') is positive. Thus `A>alpha`, so every division below has a strictly positive denominator. Also `alpha-rho>0`, since `0<rho<1`. Feasibility is exactly the existence of `b` in the open interval

\[
\frac{\alpha P(1+r)-1}{n(1-\alpha/A)}
<b<
\frac{P(1+w)-\alpha P(r)}{\alpha-\rho}.
\]

Eliminating `b` gives

\[
\sum_{k=0}^d p_k F_k>0,
\]

where

\[
F_k=n(1-\alpha/A)[(1+w)^k-\alpha r^k]
 -(\alpha-\rho)[\alpha(1+r)^k-1].
\]

A positive weighted average has a positive term. Moreover,

\[
F_0=-(\alpha-1)[n(1-\alpha/A)+\alpha-\rho]<0.
\]

Choose some `1<=k<=d` with `F_k>0`. Define

\[
b_- =\frac{\alpha(1+r)^k-1}{n(1-\alpha/A)},\qquad
b_+ =\frac{(1+w)^k-\alpha r^k}{\alpha-\rho},
\]

and take `b*=(b_-+b_+)/2`, `beta*=b*/A`. The inequality `F_k>0` gives `0<b_-<b_+`, so the output `P*(x)=x^k`, `Q*(x)=beta* x^d` satisfies both strict tests at the original `alpha`.

## 4. The source restriction `beta <= 1` is automatic

For every positive `w` the differences `(1+w)^j-w^j` strictly increase with the integer `j>=0`, since their successive difference is

\[
w(1+w)^j-(w-1)w^j>0.
\]

Since `r>=w`, the chosen `k` obeys

\[
(1+w)^k-\alpha r^k
 <(1+w)^k-w^k
 \le A-w^d.
\]

Consequently

\[
\frac{b_+}{A}
=\frac{(1+w)^k-\alpha r^k}{\alpha A-w^d}
<\frac{A-w^d}{\alpha A-w^d}<1.
\]

Therefore `0<beta*<1`. This closes the full parameter-domain obligation rather than treating the source's coefficient cap as harmless by assumption.

## Boundaries and reusable interface

All input and output weights are strictly positive. No quotient is used until its denominator has been proved positive. Identically zero `P`, identically zero `Q`, or a purely constant side polynomial cannot satisfy the two strict tests for `alpha>1`; this follows directly from the original margins. The proof allows constant terms in either input polynomial and allows zero coefficients at every other degree. It does not rely on `w -> 0` or a supremum being attained.

The reusable procedure is constructive: close `w>1` as in step 1, perform the endpoint replacement of `Q`, normalize, evaluate the finite list `F_1,...,F_d`, choose a positive entry, and select an interior `beta`. The finite rational verifier executes this procedure exactly on rational inputs. Its runs check algebra and boundary behavior; the general real-parameter theorem is proved by the displayed argument, not by the runs.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
