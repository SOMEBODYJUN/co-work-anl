# Seven maxima, seven or more providers: a joint customer-level half-union certificate

Scratch research report, 2026-10-10. Author derivation and standalone exact
coefficient audit are complete. Independent review is pending. This report
does not change the repository claim registry, does not assert novelty, and
does not solve the unrestricted arbitrary-maxima conjecture.

## Theorem

In the unit-provider sequential customer-attraction model, let the finite
common catalog have exactly seven distinct inclusion-maximal coverage sets.
Every complete ordered-history pure SPE, with arbitrary internal subthemes
and history-dependent ties, satisfies

\[
 U\le 2W\qquad(n\ge7).
\]

Since all seven maximal sets fit in an n-action comparison portfolio,
`OPT_n=U` in this range. The theorem therefore gives half optimal coverage.
Together with the established at-most-six-maxima theorem it covers at most
seven maxima for `n>=7`. It leaves exactly-seven-maxima `n=5,6` outside the
present report. No padding by fictitious catalog actions is used.

The proof has three branches: individual mixed-floor rational certificates for `n=7,8`;
a fixed rational dual checked on complete finite coefficient domains for
`n=9,...,12`; and an analytic coefficient proof for every `n>=13`.

## 1. Genuine customer types and final maximal action

Write the maximal coverages as `B_0,...,B_6`, relabeling so that the actual
final action has coverage `B_0`. That coverage must be maximal: a strict
legal superset preserves each old customer payment and adds a strictly
positive payment from each new customer, with no follower whose action can
change. Thus a nonmaximal final action contradicts best response.

For each catalog customer, let `I` be its nonempty incidence among the seven
maxima and `J` its true membership among actual provider actions. Set

\[
 f=1_{0\in I},\quad k=|I\setminus\{0\}|,\quad
 p=|J\cap\{0,\ldots,n-3\}|,\quad d=1_{n-2\in J}.
\]

The last true membership is exactly `f`. Hence `|J|=p+d+f` and the complete
compressed domain is

\[
 f,d\in\{0,1\},\quad0\le k\le6,\quad1\le f+k\le7,
 \quad0\le p\le n-2.
\tag{1}
\]

No route restriction is imposed on earlier true memberships. This enlarges
the genuine domain, so a certificate valid on (1) covers arbitrary actual
actions, including subthemes omitting core customers. Write `w_{I,J}` for
customer mass. Then

\[
 U=\sum w_{I,J},\quad W=\sum w_{I,J}1_{p+d+f>0},\quad
 u_t=\sum w_{I,J}\frac{1_{t\in J}}{|J|}.
\tag{2}
\]

A share with zero numerator is zero; positive numerators always have
positive denominators. The customers of incidence all seven maxima form
the core `C`, with mass `c`; singleton incidences have total mass `P`; all
remaining noncore incidences have total mass `V`.

## 2. Mixed floors retained as one joint budget

For seven maxima the established all-history mixed floor has raw sequences

\[
 A_t=\frac{n+t}{(t+1)(7n-5t)},\quad
 B_t=\frac2{7n-5t}\quad(0\le t\le n-2),
\]

\[
 A_{n-1}=\frac1{n+6},\qquad B_{n-1}=\frac{n+1}{n(n+6)}.
\tag{3}
\]

Let `alpha_t=min_{q>=t}A_q` and `beta_t=min_{q>=t}B_q`. Every actual provider
at prefix length `t`, at every legal ordered history, has final payoff at
least

\[
 c/n+\alpha_t P+\beta_t V.
\tag{4}
\]

For completeness, the mechanism behind (4) routes every catalog action into
one containing maximum. At a prefix with route counts `z_j`, remaining
count `r=n-t`, and `z_I=sum_{j in I}z_j`, put

\[
 F_j=\frac{w_{\{j\}}}{z_j+1}
 +\sum_{2\le|I|\le6,\,j\in I}\frac{w_I}{z_I+r}.
\]

If a deviation to the full `B_j` has no same-route follower, its private
customers have final load at most `z_j+1`; its shared customers have load
at most `z_I+r`. Weighted averaging with `y_j=z_j+r/2` gives a private
coefficient at least `(n+t)/(2(t+1))`, and shared coefficient at least one,
with total weight `(7n-5t)/2`. At `r=1`, use `y_j=z_j+1`; shared coefficient
is at least `1+1/n`. These are exactly (3). If a same-route follower exists,
its true action is a subset of the full deviating maximum, so the deviator
receives at least that follower's final payoff. Backward induction over all
ordered histories, using the nondecreasing suffix envelopes, proves (4).
This argument never freezes a follower after a deviation.

The sequence `B_t` is itself nondecreasing, including its final step:
`(n+1)(n+5)-n(n+6)=5>0`. Define the early sums

\[
 F_P(n)=\sum_{t=0}^{n-3}\alpha_t,\qquad
 F_V(n)=\sum_{t=0}^{n-3}\beta_t
 =\sum_{r=3}^n\frac2{2n+5r}.
\tag{5}
\]

Let `M_t=u_t-c/n-alpha_t P-beta_t V>=0` for every `0<=t<=n-1`. The aggregate
of their first `n-2` rows has per-customer coefficient

\[
 \frac p{p+d+f}-F(m),\qquad m=f+k,
\]

where

\[
 F(m)=\begin{cases}
 F_P(n),&m=1,\\ F_V(n),&2\le m\le6,\\ (n-2)/n,&m=7.
 \end{cases}
\tag{6}
\]

The last expression preserves the real core contribution even when early
actual actions omit the core.

## 3. Final best responses and genuine last-two tax

For every `j=0,...,6`, the exact final-player best response gives

\[
 L_j=u_{n-1}-\sum w_{I,J}\frac{1_{j\in I}}{p+d+1}\ge0.
\tag{7}
\]

At the actual prefix of length `n-2`, the established genuine two-remaining
tax inequality gives, for every legal pair of maxima `B_j,B_l`,

\[
 T_{jl}=u_{n-2}+u_{n-1}
 +\sum w_{I,J}\frac d{(p+1)(p+2)}
 -\sum w_{I,J}\frac{1_{j\in I}+1_{l\in I}}
 {p+1_{j\in I}+1_{l\in I}}\ge0.
\tag{8}
\]

Zero comparison numerator means zero. The tax theorem uses the original
SPE's actual last reply after the first comparison deviation, that reply's
best response, and the actual final player's comparison to the same legal
reply. Thus (8) is a valid continuation inequality. It does not hold by
freezing the actual last action. Its direct two-player identity is
`R(actual)+g(actual first,actual first)-R(comparison)` equal to three true
SPE slacks plus `g(A,A)-g(A,Q)+g(T,S)>=0`, where
`g(X,Y)=sum_{x in X cap Y}1/((p_x+1)(p_x+2))`.

## 4. General compressed residual identity

For the `n>=9` branch assign multipliers `a,b,c_*,e` respectively to each early mixed slack,
each of the six `L_j`, each of the six `T_{0j}`, each of the fifteen
`T_{jl}` with `1<=j<l<=6`. All other row multipliers are zero. Put

\[
 q=6c_*+15e,
 \quad G_{f,k}(p)=\begin{cases}k/(p+1),&f=0,\\
 (6-k)/(p+1)+2k/(p+2),&f=1,
 \end{cases}
\]

\[
 K_k(p)=\frac{k(6-k)}{p+1}+\frac{k(k-1)}{p+2}.
\]

The residual lower bound for every genuine customer is

\[
\begin{aligned}
 r(f,k,p,d)={}&1_{p+d+f>0}-\frac12+aF(f+k)
 +\frac{bk}{p+d+1}+c_*G_{f,k}(p)+eK_k(p)\\
 &-\frac{ap+qd+(q+6b)f}{p+d+f}
 -\frac{qd}{(p+1)(p+2)}.
\end{aligned}
\tag{11}
\]

The share fraction is zero if its denominator is zero. Equation (11) is
the exact residual for these symmetric multipliers, and

\[
 W-U/2=\sum_{\text{used rows}}\lambda S
 +\sum w_{I,J}\,r(f,k,p,d).
\tag{12}
\]

All slacks and multipliers are nonnegative. Thus a nonnegative residual
on the complete domain (1) proves the theorem. No independently maximized
floors are added, and a customer's contribution to actual welfare is
exactly its real shares in (2).

For arbitrary `s`, the same derivation replaces `6` by `z=s-1`, `15` by
`binom(z,2)`, `G` by `(z-k)/(p+1)+2k/(p+2)` when `f=1`, and `K` by
`k(z-k)/(p+1)+k(k-1)/(p+2)`. Its mixed sequences are
`A_t=(n+t)/((t+1)(sn-(s-2)t))` and `B_t=2/(sn-(s-2)t)` with last values
`1/(n+s-1)` and `(n+1)/(n(n+s-1))`. This is a rigorous arbitrary-`s,n`
certificate interface, not an assertion that its residual is always
nonnegative.

## 5. Seven and eight providers: exact individual-floor certificates

For these two player counts retain all `n` individual mixed rows, rather
than their symmetric early aggregate. The complete row order is
`M_0,...,M_(n-1)`, followed by `L_0,...,L_6`, followed by all 28 `T_jl`
with `0<=j<=l<=6` in lexicographic order, including repeated pairs.

The following table completely specifies every multiplier. Each displayed
integer is divided by `10000`; any row not listed has multiplier zero.

| n | M-row numerator vector, in position order | Each L_j, j=1,...,6 | Each T_0j, j=1,...,6 | Each T_jl, 1<=j<l<=6 |
|---|---|---:|---:|---:|
| 7 | (7225,7244,7281,7394,7936,2727,0) | 1196 | 615 | 51 |
| 8 | (7113,7124,7144,7184,7283,7775,2401,0) | 1179 | 641 | 55 |

In particular `L_0`, every repeated tax pair, and the last mixed row have
zero weight. These certificates were supplied by the parallel joint-budget
search agent and independently reconstructed in this report's audit.

For every nonempty incidence `I subset {0,...,6}` and every earlier true
membership `E subset {0,...,n-2}`, set
`J=E union {n-1}` if `0 in I`, and `J=E` otherwise. This is the complete
enlarged literal domain; it has `127*2^(n-1)` columns. Evaluate the actual
share `1_(t in J)/|J|`, subtract the appropriate private/shared/core floor
in each `M_t`, and evaluate (7),(8) from these same true memberships.

For the listed nonnegative row multipliers define
`r(I,J)=1_(J nonempty)-1/2-sum lambda_q s_q(I,J)`. The exact identity is
again (12), now with individual rather than symmetric mixed rows. The
standalone audit checks every literal customer column and obtains

\[
 \min r_7=\frac{344541}{320450000}>0
 \quad\text{over 8128 columns},
\]

\[
 \min r_8=\frac{15483}{775000}>0
 \quad\text{over 16256 columns}.
\tag{13}
\]

These finite, complete coefficient checks are rational proof data. They
cover arbitrary customer masses and arbitrary earlier subthemes; they are
not SPE enumeration or sampled game testing.

## 6. Nine through twelve providers: one fixed rational dual

Set

\[
 a=\frac34,\quad b=\frac2{19},\quad c_*=\frac{11}{133},
 \quad e=\frac6{665}.
\tag{14}
\]

For `n=9,...,12`, the exact audit checks all `26(n-1)` compressed cases,
using the literal suffix-minimum private floor from (3). The minima are

| n | Complete cases | Minimum residual |
|---|---:|---:|
| 9 | 208 | 13083575/3480880788 |
| 10 | 234 | 288689/22822800 |
| 11 | 260 | 17649416027/867723576720 |
| 12 | 286 | 866272417771/32017930648704 |

Every minimum is positive. These finite coefficient domains cover arbitrary
customer masses and every genuine SPE type, so they are complete rational
proof data rather than finite game searches.

## 7. Every n at least thirteen: analytic floor estimates

First, for every `n>=7`, all raw private coefficients in (3) are at least
`1/(2n)`. For an interior index `t`, the required inequality is

\[
 2n(n+t)-(t+1)(7n-5t)
 =5t^2+(5-5n)t+2n^2-7n
\]

\[
 =5\left(t-\frac{n-1}{2}\right)^2+
 \frac{3n^2-18n-5}{4}\ge0.
\tag{15}
\]

The final expression is positive at n=7 and increasing thereafter. The
last private coefficient obeys `1/(n+6)>=1/(2n)` for `n>=6`. Therefore the
whole suffix envelope obeys the same bound, and

\[
 F_P(n)\ge\frac{n-2}{2n}.
\tag{16}
\]

Second, the function `x -> 2/(2n+5x)` is decreasing, so

\[
 F_V(n)=\sum_{r=3}^n\frac2{2n+5r}
 \ge\int_3^{n+1}\frac2{2n+5x}\,dx
 =\frac25\log\frac{7n+5}{2n+15}.
\tag{17}
\]

For n>=13, `3(7n+5)>=7(2n+15)`, hence the log argument is at least `7/3`.
The convergent positive series for `log((1+z)/(1-z))`, at `z=2/5`, gives

\[
 \log(7/3)>2\left(\frac25+\frac{(2/5)^3}{3}\right)
 =\frac{316}{375}>\frac56.
\]

Consequently

\[
 F_V(n)>\frac13\qquad(n\ge13).
\tag{18}
\]

The core value `(n-2)/n` is also at least `1/3` in this range. Since the
multiplier `a` is positive, substitute the lower bounds (16),(18) into
(11). It remains to prove those coarser residuals nonnegative.

## 8. Complete analytic residual proof for the fixed dual

Under (14), set

\[
 q=12/19=6b,\qquad \delta=b+c_*+5e=31/133,
 \qquad D_n=1/8-3/(4n).
\]

For private types, `f+k=1`. If they are uncovered, necessarily
`f=d=p=0,k=1`, and the residual is at least

\[
 L_n=\frac{115}{1064}-\frac3{4n}.
\tag{19}
\]

For covered private types the four possibilities have these lower bounds:

| f,d | Lower residual |
|---|---|
| 0,0 (p>0) | `D_n+delta/(p+1)` |
| 0,1 | `D_n+(187p-18)/(532(p+1)(p+2))` |
| 1,0 | `D_n-9/(532(p+1))` |
| 1,1 | `D_n+(27p-9)/(266(p+1)(p+2))` |

Each is at least `D_n-9/532=L_n`: positive-slope numerators permit their
negative constants to be bounded using `(p+1)(p+2)>=2`; the other negative
term uses `p+1>=1`. At n=7, `L_7=1/1064`; it increases with n. Thus all
private residuals are positive for every n>=7.

An uncovered shared type has `f=d=p=0,2<=k<=6`. Here
`K_k(0)=k(11-k)/2>=0`. Dropping that nonnegative internal-pair term, its
residual is at least

\[
 -1/4+(b+c_*)k\ge-1/4+2(b+c_*)=67/532>0.
\tag{20}
\]

Consider now every covered shared or core type, using `F>=1/3`.

* If `f=d=0`, then `p>0` and the residual is at least
  `(b+c_*)k/(p+1)+eK_k(p)>=0`.
* If `f=0,d=1`, then `k>=2`. Dropping `eK>=0` and using `k>=2` bounds the
  residual below by `(263p+78)/(532(p+1)(p+2))>0`.
* If `f=1,d=0`, write the residual lower bound as
  `C_1(k)/(p+1)+C_2(k)/(p+2)`, where

\[
 C_1(k)=a-2q+bk+c_*(6-k)+ek(6-k),\quad
 C_2(k)=2c_*k+ek(k-1).
\]

  `C_2(k)>=0`. The quadratic `C_1` is concave on `1<=k<=6`, so its minimum
  on that interval is at an endpoint. The endpoints are
  `C_1(1)=27/532>0` and `C_1(6)=9/76>0`.
* If `f=d=1`, the residual lower bound is

\[
 \frac{p(27/266+\delta k)+E(k)}{(p+1)(p+2)},\qquad
 E(k)=27/266+\delta k+(6-k)(c_*+ek)-q.
\]

  Its p coefficient is positive. The quadratic `E` is concave on
  `1<=k<=6`, and its endpoints are `E(1)=43/266>0`, `E(6)=33/38>0`.

These cases are exhaustive for (1). They establish nonnegative residuals
for every n>=13, without a finite scan of larger player counts. Combining
this with Sections 5--6 and the accounting identity (12) proves the theorem.

## 9. Exact audit files and scope

`seven_tail_audit.py` imports only `Fraction`, `json`, `Path`, and `hashlib`; it reconstructs
the raw floor sequences, the true equal-share coefficients, all four old
slack families, and all 24,384 literal columns for n=7,8 plus all 988
compressed coefficients for n=9,...,12. The small-player full multiplier
vectors are `n7_n8_exact_duals.json`, copied from the parallel joint search
agent's certificate and independently checked here. Its frozen combined
output is `seven_tail_audit.json`.

The arbitrary-s interface following (12) is valid, but is not uniformly
nonnegative. In particular, the stronger union target is impossible for
unrestricted `s`: with s disjoint unit themes and n<s providers, every SPE
can choose distinct themes, giving `W=n,U=s`; if `s>2n`, then `U>2W`.
This is a real SPE obstruction to the union statement, while `OPT_n=n=W`
and the original half-optimal-coverage conjecture remains true in that
example. General arbitrary-s work must track `OPT_n` rather than silently
substitute the full union. No general SPE counterexample is supplied here.

The numerical discovery scripts are exploratory only. The exact small
certificates and the analytic proof above carry the claims in this report.
