# R1 independent odd-ring asymptotic audit

Audit date: 2026-10-14. Reviewer: R1/ring_asymptotic_audit; a separate sub-review by `constant_attack` checked the original candidate's uniform constants. No Git mutation or board message was performed by this reviewer.

**Finding:** the original dyadic candidate is valid, and the recovered linear-reset construction proves the stronger model-wide lower bound `a_*(d) >= d/(ln d+2)` for every integer `d>=4`. No fatal algebraic or full-state objection was found. The same construction gives the strictly stronger explicit bound

\[
 E_d=\frac{d}{(d+1)d^{1/(d+1)}-d},\qquad a_*(d)\ge E_d\quad(d\ge2).
\]

Its achievable limiting envelope is within `2^(-d)` of `E_d`, and is

\[
 \frac{d}{\ln d+1}-\frac12+o(1).
\]

These are mathematical audit conclusions, not claims of first discovery. Literature and priority remain separate obligations.

## Claim identity, inputs, and scope

- **Claim IDs/version:** `R1-ODD-RING-AUDIT-v1`; derived refinement `OC-AMPLIFIER-ENVELOPE-v1`.
- **Objects/domain:** WC-TARGET v1, finite weighted atomic congestion games, arbitrary positive real player weights, arbitrary finite resource-subset strategies, nonnegative polynomial latencies of degree at most the integer `d`. Player cost is the sum of latencies, without multiplying by weight; each resource in this construction has a positive monomial latency.
- **Quantifiers/conclusion:** for every integer `d>=2`, there exists a finite game with no `E_d`-PNE. More generally, for every `0<t<1` and every `1<alpha<H_d(t)`, a finite game has no `alpha`-PNE, where `H_d(t)=((1+t)^d+t^(d+1))/(1+t(1+t)^d)`. Therefore `a_*(d)>=sup_{0<t<1}H_d(t)>E_d` as a numerical lower-bound inequality; no single game at the supremum is asserted.
- **Assumptions:** ring length odd and at least three; degrees `1<=k_i,D_i<=d`; all inequality margins strict. Player and resource counts may grow without bound as the requested factor approaches the envelope.
- **Dependencies:** MODEL.md, ACCEPTANCE.md, the independently reconstructed strict coefficient interface below, and elementary real inequalities. The source-family comparison in the last section depends only on the exact equation-(3) expression recorded in PRIOR_ASSETS.md.
- **Evidence:** a general derivation below, plus exact rational checks in `audit_checks.py` and `audit_checks.json`. Finite checks do not replace the general proof or enumerate all large-game states.
- **Counterevidence/objections:** none fatal found. The certificate barrier is a limitation of this sufficient interface, not a universal existence theorem. Novelty and priority are not decided here.
- **Status:** independently reconstructed and algebraically audited; source-literature review and coordinator integration remain distinct.
- **Related files:** `../odd_cycle/README.md`, `../odd_cycle/general_lower_bound.md`, `../odd_cycle/INTERFACE_BARRIER.md`, `audit_checks.py`, `audit_checks.json`, `literature_review.md`.

The first pass used MODEL.md, ACCEPTANCE.md, and the supplied general algebraic interface only. It reconstructed the bottleneck and checked the dyadic candidate before reading the recovered linear-reset proof. The stronger reset was then independently reconstructed from the interface before reading its frozen asset; that asset was subsequently checked against literal player costs.

## Independently reconstructed interface and state coverage

There are `m>=3` odd hubs `H_i` of weight `u_i` and, for each `i`, a cohort of `n_i>=1` independent players of weight `v_i`. Each player chooses a bit. Main resources `A_i^0,A_i^1` have latency `a_i z^(k_i)`. For each cohort member `j`, side resources `B_ij^0,B_ij^1` have latency `b_i z^(D_i)`. Hub `H_i` choosing bit `h` uses `A_i^h` and all incoming `B_(i-1),j^h`. Cohort member `(i,j)` choosing `l` uses `A_i^l` and `B_ij^(1-l)`.

Write

\[
 x_i=v_i/u_i,\quad t_i=v_i/u_{i+1},\quad
 q_i=a_iu_i^{k_i},\quad p_i=b_iu_{i+1}^{D_i},
\]
\[
 N_i=(1+x_i)^{k_i}-\alpha(n_ix_i)^{k_i},\quad
 M_i=\alpha(1+n_ix_i)^{k_i}-1,
\]
\[
 P_i=\alpha(1+t_i)^{D_i}-t_i^{D_i},\quad
 Q_i=(1+t_i)^{D_i}-\alpha.
\]

Positive weights exist exactly when `product x_i=product t_i`: set `u_0=1`, `u_(i+1)=u_i x_i/t_i`, and `v_i=u_i x_i`. This checks the dependence of the two ratio sequences rather than treating them as free.

If `N_i,Q_i>0`, then `M_i,P_i>0` for `alpha>=1`, and the strict local conditions

\[
 q_iN_i>p_iP_i,\qquad n_ip_iQ_i>q_{i+1}M_{i+1} \tag{1}
\]

are feasible exactly when

\[
 G:=\prod_i\frac{n_iN_iQ_i}{M_iP_i}>1. \tag{2}
\]

Indeed, define `K_i=n_iN_iQ_i/(P_iM_(i+1))`. Eliminating `p_i` gives `q_(i+1)<K_i q_i`, and multiplication gives necessity. For sufficiency choose rational `delta>1` with `delta^(m-1)<G`, set `q_0=1`, `q_(i+1)=K_i q_i/delta` for `0<=i<m-1`, and use the cyclic value `q_m=q_0`. The last strict bound follows from `G/delta^(m-1)>1`. Choose `p_i` as the midpoint between `q_(i+1)M_(i+1)/(n_iQ_i)` and `q_iN_i/P_i`, then recover positive `a_i,b_i`. For real inputs a suitable rational `delta` still exists by density; for rational inputs every resulting weight and coefficient is rational.

Every state is covered by (1). If a cohort player chooses the same bit as its own hub, its current main load is at least `u_i+v_i`, and its post-switch main load is at most `n_iv_i`, including the deviator. Its current side load is at least `v_i`, and its post-switch side load is at most `u_(i+1)+v_i`. The first inequality therefore makes its current cost strictly greater than `alpha` times its switching cost, independently of every other bit.

Otherwise every cohort chooses the opposite bit from its own hub. An odd cycle of binary hub bits has equal adjacent bits somewhere. At such an edge `i`, hub `H_(i+1)` shares all incoming side resources with cohort `i` and uses its own main resource alone. After switching, its incoming side resources are solo and its own main resource contains its full cohort. The exact current-minus-`alpha`-times-switching cost is `n_ip_iQ_i-q_(i+1)M_(i+1)>0`. This is a proof for every pure state, not merely a cycle of improvements. All chosen resources have positive load and positive coefficient, so no zero-cost quotient is used.

## Original dyadic candidate: uniform proof and finite checks

Take integer `s>=6`, `r=2^s`, `d=2sr`, `alpha=r/4`, and any odd `m>=s` (the least such odd integer suffices). Put `L=2m-1`, `t_i=1/r` for all `i`, and

\[
 x_0=r^{-L},\quad n_0=\lfloor r^L/s\rfloor,\quad k_0=s;
 \qquad x_i=r,\ n_i=1,\ k_i=d\quad(i\ge1).
\]

The closure identity is exact: `product x_i=r^(-L+m-1)=r^(-m)=product t_i`. The independent bottleneck reconstruction was the identity

\[
 F:=\frac QP=\frac{N_i}{M_i}\quad(i\ge1),\qquad
 G=\frac{n_0N_0}{M_0}F^L,
\]

where `Q=(1+1/r)^d-alpha`, `P=alpha(1+1/r)^d-r^(-d)`. The enormous reset cohort compensates for all small buffer factors; the ring-length condition is needed for the remaining amplification margin.

The following constants are uniform as `m` grows:

1. `A=r^L/s>2`, hence `n_0=floor A>A/2`. Also `n_0x_0<=1/s`.
2. `alpha/s^s=(1/4)(2/s)^s<=1/2916` for `s>=6`, so `N_0>=1-alpha/s^s>1/2`.
3. `(1+1/s)^s<3`, for example by comparing its binomial expansion with `sum 1/j!<3`. Thus `M_0<3alpha`, while `M_0>=alpha-1>0`.
4. Strict Bernoulli gives `(1+1/r)^r>2` because `r>=2`. Consequently `z=(1+1/r)^d>2^(2s)=r^2`, so `Q,P>0` and

\[
 F>\frac{z-\alpha}{\alpha z}
 =\frac4r-\frac1z>\frac4r-\frac1{r^2}>\frac2r.
\]

The regular `N_i,M_i` are `r^d Q,r^d P`, so all their signs are checked. Combining the bounds gives

\[
 G>\frac{r^{L-1}}{3s}\left(\frac2r\right)^L
 =\frac{2^L}{3sr}
 \ge\frac r{6s}>1.
\]

The last inequality follows from `2^s>6s` for every integer `s>=6`. No floor or growing-`m` flaw was found. The claimed bound is very conservative: the exact rational products below are much larger.

| s | m | d | alpha | Exact product, shown approximately | Claimed lower |
|---|---:|---:|---:|---:|---:|
| 6 | 7 | 768 | 16 | 283772.184978975 | 16/9 |
| 7 | 7 | 1792 | 32 | 119062.571159144 | 64/21 |
| 8 | 9 | 4096 | 64 | 13156065.59862943 | 16/3 |

The script evaluates the relevant expressions as `fractions.Fraction` and asserts the strict bounds, rather than deciding them from the displayed decimals. Both installed Python interpreters lacked `mpmath`; Decimal was used for numerical summaries. Additional initial Decimal checks at `s=10,12,16,24,32,64` were only numerical exploration and are not exact-arithmetic evidence.

For the originally requested monotone extension, take the largest `s>=6` with `d_s=2s2^s<=d`. The same game belongs to `G_d`; since `d<d_(s+1)=4(s+1)2^s` and `s+1<=log_2 d`,

\[
 a_*(d)\ge2^{s-2}>\frac{d}{16\log_2 d}
 =\frac{\ln2}{16}\frac d{\ln d}\qquad(d\ge768).
\]

This secondary dyadic bound is superseded by the all-degree linear-reset bound below.

## Linear reset: exact amplification, finite size, and rational realization

Fix integer `d>=2`, `0<t<1`, and `1<alpha<H_d(t)`. Put

\[
 z=(1+t)^d,\quad Q=z-\alpha,\quad P=\alpha z-t^d,
 \quad B=Q/P.
\]

Since `P>0`, the exact equivalence is

\[
 B>t\quad\Longleftrightarrow\quad
 \alpha<\frac{z+t^{d+1}}{1+tz}=H_d(t). \tag{3}
\]

In particular `Q>tP>0`. Choose a finite integer `R>=5`, `R congruent to 1 mod 4`, such that

\[
 t^R<\frac1{4\alpha},\qquad (B/t)^R>8\alpha^2. \tag{4}
\]

Starting at `R=5` and increasing by four terminates because `t<1` and `B/t>1`. This avoids any ambiguity from rounding logarithmic thresholds. Set `m=(R+1)/2`, `x=t^R`, `n=floor(1/(2alpha x))`, and use a degree-one reset at `i=0`; the other `m-1` positions have `x_i=1/t,n_i=1,k_i=d`. All side degrees are `d`.

The explicit weights are

\[
 u_0=1,\quad u_i=t^{2(m-i)}\ (1\le i<m),
 \qquad v_0=t^R,\quad v_i=t^{2(m-i)-1}\ (1\le i<m).
\]

They have exactly the required ratios, including the final cyclic edge. All weights are positive; no ordering relative to their own hub is assumed.

Condition (4) gives `1/(2alpha x)>2`, hence

\[
 \frac1{4\alpha x}<n\le\frac1{2\alpha x},\quad
 N_0=1+x-\alpha nx>\frac12,\quad
 0<M_0=\alpha(1+nx)-1\le\alpha-\frac12<\alpha.
\]

Thus `A_0=nN_0/M_0>1/(8alpha^2 x)`. Each buffer obeys `N_i=t^(-d)Q`, `M_i=t^(-d)P`. Therefore its full factor in (2) is `B^2`, while the reset factor is `A_0 B`. Consequently

\[
 G=A_0B^R>\frac{(B/t)^R}{8\alpha^2}>1.
\]

The midpoint coefficient recipe and the full-state argument now construct a finite game with no `alpha`-PNE. The number of players can be enormous but is finite, and every individual strategy is finite. If `alpha,t` are rational then the weights and coefficients are rational. For arbitrary real target `alpha<H_d(t)`, continuity permits a nearby rational `t'` and rational `beta` with `alpha<beta<H_d(t')`; constructing at `beta` gives an all-rational game which also has no `alpha`-PNE. Rationality is therefore available if desired, but WC-TARGET permits the original direct real construction.

At `d=2`, `H_2(t)>1` throughout `0<t<1`, since its numerator minus denominator is `t-t^2`. More generally, the difference `(1-t)(1+t)^d-1+t^(d+1)` has positive one-step increment `t(1-t)((1+t)^d-t^d)`, so `H_d(t)>1` throughout that interval for every `d>=2`. At `d=1`, `H_1(t)=1`; this mechanism supplies no factor above one. It is not legitimate to invoke the `alpha>1` construction there.

Useful exact small-degree endpoints are

\[
 H_2(1/3)=49/43,\qquad H_3(1/3)=193/145.
\]

For every factor strictly below either endpoint and above one, the corresponding finite construction applies. No game at either endpoint is claimed by this strict limiting argument.

The exact rational script reconstructs all weights, chooses `delta`, and checks both strict local inequalities at every ring position for these instances:

| d | t | alpha | R | m | Exact product, shown approximately |
|---:|---|---|---:|---:|---:|
| 2 | 1/3 | 113/100 | 101 | 51 | 3.85493688035 |
| 3 | 1/3 | 13/10 | 49 | 25 | 3.27433707981 |
| 4 | 1/3 | 3/2 | 57 | 29 | 3.25537002106 |
| 10 | 1/4 | 5/2 | 25 | 13 | 2.56027275967 |

This is exact coefficient evidence, not enumeration of all states; the general state-cover proof is the reason all states fail.

## Uniform d/(ln d+2) theorem

For integer `d>=4`, set `L=ln d` and `t=L/d`, which lies in `(0,1)`. The inequality `ln(1+s)>s-s^2/2` for `s>0` gives

\[
 z=(1+t)^d>\exp(L-L^2/(2d)).
\]

Differentiation gives `L^2/(2d)<=2/e^2<ln2`, hence `z>d/2`. Therefore

\[
 H_d(t)>\frac1{t+1/z}>\frac d{\ln d+2}.
\]

The proposed factor exceeds one for all `d>=4`, because `d-ln d-2` is increasing after one and positive at four. The finite construction thus works at that exact factor. Strictness at the factor belongs to this particular game; the conclusion about `a_*` does not presume that its universal infimum is attained.

## Improved explicit envelope and its asymptotics

Decompose the exact threshold as

\[
 H_d(t)=\frac1{t+(1+t)^{-d}}+
 \frac{t^{d+1}}{1+t(1+t)^d}. \tag{5}
\]

The denominator `f_d(t)=t+(1+t)^(-d)` has derivative `1-d(1+t)^(-d-1)` and positive second derivative. For `d>=2` its unique minimizer in `(0,1)` is

\[
 t_d=d^{1/(d+1)}-1.
\]

(The inequality `d<2^(d+1)` ensures `t_d<1`.) At the minimizer,

\[
 E_d=\frac1{f_d(t_d)}
 =\frac d{(d+1)d^{1/(d+1)}-d}>1.
\]

The last inequality also follows directly from `f_d(0)=1` and `f'_d(0)=1-d<0`. The second term in (5) is strictly positive, so `H_d(t_d)>E_d`; the finite construction therefore yields **one game with no `E_d`-PNE**, rather than merely factors tending to `E_d` from below.

For all `0<t<1`, that second term is bounded by

\[
 0<\frac{t^{d+1}}{1+t(1+t)^d}
 <\left(\frac t{1+t}\right)^d<2^{-d}.
\]

Thus the exact amplifier envelope `U_d=sup H_d(t)` obeys

\[
 E_d<U_d\le E_d+2^{-d}. \tag{6}
\]

In fact the upper inequality can be made strict: `H_d` extends continuously to `[0,1]`, both endpoint values equal one, and its maximum exceeds one, so it occurs at an interior point where the displayed error bound is strict.

For `d>=4`, `E_d>d/(ln d+2)`. One elementary verification writes `w=L/(d+1)` and uses `e^w-1-w<=w^2 e^w/2`. Since `L<sqrt d`, `w<1/2`, and `e^w<2`,

\[
 (d+1)(e^w-1)+1-L-1
 \le\frac{L^2e^w}{2(d+1)}<1.
\]

Therefore the denominator of `E_d/d` is strictly below `L+2`. The inequality `L<sqrt d` for `d>=4` follows from the positive value at four and the derivative of `sqrt d-ln d`; `w<1/2` also follows from `ln d/d<=1/e<1/2`.

Expansion of the exact denominator gives

\[
 (d+1)d^{1/(d+1)}-d
 =L+1+\frac{L^2}{2(d+1)}+O(L^3/d^2),
\]

and hence

\[
 E_d=\frac d{L+1}-\frac12+o(1),\qquad
 U_d=\frac d{L+1}-\frac12+o(1).
\]

In particular both have leading asymptotic constant one relative to `d/ln d`. This is a complete general asymptotic derivation of the achievable envelope, not an empirical optimization claim.

## Interface barrier: correct scope and audit

The recovered obstruction is correct for its stated interface. Fix `alpha>1`, integer `d>=1`, positive ratios with the closure identity, and `1<=k_i,D_i<=d`. Put `z=alpha^(1/d)`, `L=z-1`. From `N_i>0`,

\[
 n_ix_i<(1+x_i)/z,\qquad x_i<1/L;
\]

from `Q_i>0`, `t_i>L`. Multiplication and closure give `product n_i<L^(-2m)`. Furthermore

\[
 M_i\ge(\alpha-1)(1+x_i)^{k_i},\quad
 N_i<(1+x_i)^{k_i},
\]

and, writing `y=(1+t_i)^(D_i)`, `r=t_i^(D_i)`,

\[
 P_i-(\alpha-1)Q_i=y-r+\alpha(\alpha-1)>0.
\]

Consequently

\[
 \prod F_i<[(\alpha-1)(\alpha^{1/d}-1)]^{-2m}.
\]

A product greater than one requires `(alpha-1)(alpha^(1/d)-1)<1`. Since `exp(s)-1>=s`, this implies `(alpha-1)ln alpha<d`, whose positive boundary is asymptotic to `d/ln d`. The linear reset attains that leading constant within this sufficient certificate.

This does **not** upper-bound `a_*(d)`, nor prove existence for every game having the same resources outside the interface's simultaneous local inequalities. Its scope is the coefficient certificate (1)-(2).

## Self-contained coarse ceiling for the source equation-(3) family

This section audits the coordinating R1 suggestion independently; it compares the full exact source optimization domain without assuming the separately recovered sharper R3 theorem. The source expression in PRIOR_ASSETS.md is the minimum of

\[
 A=\frac{1+n\beta(1+w)^d}{(1+nw)^k+n\beta},\qquad
 B=\frac{(1+w)^k+\beta w^d}{(nw)^k+\beta(1+w)^d},
\]

with integer `n>=1`, `1<=k<=d`, and `0<=w,beta<=1`. Let `F_d` be its supremum, interpreting degenerate cases by the original inequalities rather than `0/0`. The proof below actually allows arbitrary finite nonnegative `w,beta`.

Suppose `f=min(A,B)>1`. Then `w,beta>0`: at `w=0`, `A=1`; at `beta=0`, `A<=1`. Write

\[
 E=(1+w)^d,\quad p=(1+w)^k,\quad T=(1+nw)^k,
 \quad r=(nw)^k,\quad q=\beta E,\quad
 \theta=(w/(1+w))^d\le1.
\]

Now `A=(1+nq)/(T+nq/E)` and `B=(p+theta q)/(r+q)`. From `A>=f`, `fT-1<=nq`; from `B>=f`, `(f-theta)q<=p-fr<p`. Since `fT-1>=(f-1)T` and `f-theta>=f-1`, multiplication yields

\[
 (f-1)^2\le\frac{np}{T}\le n.
\]

Also `fr<p` implies `nw<1+w`, so `(n-1)w<1`. Finally `A<=E` follows from `1<=ET`, giving `ln f<=dw`.

If `f>=4`, then `n-1>=(f-1)^2-1=f(f-2)`, so

\[
 f(f-2)\ln f<d.
\]

Because `f(f-2)>=f^2/2` and `ln f>1`, this implies `f<sqrt(2d)`. The remaining case has `f<4`. Taking the exact supremum gives

\[
 F_d\le\max\{4,\sqrt{2d}\}=O(\sqrt d).
\]

Thus the ring result strictly exceeds the **entire source equation-(3) supremum**, not only the source's published coarse asymptotic lower estimate, for all sufficiently large degrees. A safe explicit range is every integer `d>=256`: the function `sqrt(d/2)-ln d-2` increases for `d>8` and is positive at 256, so `d/(ln d+2)>sqrt(2d)>=4`. As `E_d` is still larger, the refined ring bound also exceeds `F_d` there.

This ceiling is an algebraic bound on one source construction. It is not a universal existence theorem, is not claimed as a separate valuable new result, and by itself does not establish worldwide priority for the ring lower bound.

## Evidence execution and remaining limits

Command run from the repository root:

```text
python research/weighted_congestion_frontier/assets/R1/odd_ring_audit/audit_checks.py
```

Result: all three exact dyadic instances and all four exact linear-reset coefficient constructions passed; seven Decimal envelope checks at `d=2,3,4,10,100,1000,1000000` passed at precision 100. The positive correction `H_d(t_d)-E_d` eventually rounds to zero or underflows in finite Decimal arithmetic; the script only checks a nonnegative numerical correction and the strict correction is established analytically by (5). A rounded equality is not evidence against its strict positivity.

Remaining work outside this review: primary-source priority audit beyond the source family, reconciliation of claim/asset registries and provenance, and independent research on a model-wide upper bound. The interface barrier cannot supply that last result. No world-novelty, optimal universal threshold, or matched upper-and-lower claim is made.
