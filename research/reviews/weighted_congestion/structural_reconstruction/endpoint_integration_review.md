# Endpoint–area integration review

**Status:** internally checked analytic interface; no blocking mathematical error found in the frozen endpoint source or its endpoint review. This review does not certify the all-state construction, priority, or external novelty. It checks the statements that an integrated structural article may import and the assumptions that must travel with them.

**Reviewer and scope:** independent endpoint/area reviewer in the current structural weighted-congestion session, 2026-10-21. The session explicitly overrides the repository's default customer-attraction topic. No git mutation, push, or external message was made. The integrated article was not yet present when this review was drafted; its endpoint section must be checked against the contracts below once available.

## 1. Frozen inputs

Repository HEAD at the start of this check: `32cda6fbe1900bb53312aa200c929fdd48ba8a2c`.

| Input | SHA-256 |
| --- | --- |
| `research/current/weighted_congestion/structural_reconstruction/endpoint_area_principle.md` | `6c56aeea7b91d0d16e4de83c5e3bf1b1b55c7a0f5d44b0b3eb99f4834041ba9c` |
| `research/reviews/weighted_congestion/structural_reconstruction/endpoint_review.md` | `9ae7fc6bf083f1d116688d8a4ae81e7ffae5b9fa4542e8c520a513e5a26a0e6e` |
| `tests/audits/weighted_congestion/structural_reconstruction/endpoint_certificate.py` | `ac7195f824cfa847c9d849d00d777926ed10fdec19e1b950e4c83578edc0fa0d` |
| `tests/audits/weighted_congestion/structural_reconstruction/raw_resource_audit.py` | `e75d0f1d3293d7c9b3a470a35223a7dee9505df99e17f56c10960a874ae38f8b` |
| `tests/audits/weighted_congestion/structural_reconstruction/near_degree_audit.py` | `39a1040ea037144dd41c4106e97a560049f1d0ca8746ffb0731859da9ca8f68c` |

Both endpoint documents and the three audit programs were read. The parameterized construction's model and local budget were also read for consistency; this is not an independent audit of its return parity, phase coverage, or same-degree repair proof.

## 2. Exact quadrature statements independently checked

Let `b=t_0<t_1<...<t_n=T`, `a_j=t_j-t_{j-1}`, `h=max a_j`, and `S_f=Σ_j a_j f(t_j)`. For every nondecreasing function for which the integrals exist,

\[
0\le S_f-\int_b^T f(t)\,dt
\le h\,[f(T)-f(b)]. \tag{E1}
\]

On each cell the error lies between zero and `a_j[f(t_j)-f(t_{j-1})]`; replacing `a_j` by `h` and telescoping proves the upper bound. Convexity is not needed for (E1).

If additionally `f∈C²`, `f'≥0`, and `f''≥0`, then

\[
0\le S_f-\int_b^T f
\le \frac h2[f(T)-f(b)]
 +\frac{h^2}{8}[f'(T)-f'(b)]. \tag{E2}
\]

Indeed the right sum minus the composite trapezoid sum is exactly `Σ_j a_j[f(t_j)-f(t_{j-1})]/2`. The trapezoid error is

\[
\frac12\sum_j\int_{t_{j-1}}^{t_j}
(t-t_{j-1})(t_j-t)f''(t)\,dt,
\]

whose nonnegative kernel is at most `h²/8`. This confirms the refined bound in the endpoint review. Its earlier omitted monotonicity assumption has already been corrected in the frozen version. Convexity by itself is insufficient: `f(t)=-t` has a negative right-sum error. The integrated article must retain `f'≥0`.

For `f(t)=t^d` and `u=w/T∈(0,1]`,

\[
\int_{T-w}^{T}t^d\,dt=wT^dK_d(u),\qquad
K_d(u)=\frac{1-(1-u)^{d+1}}{(d+1)u}
=\int_0^1(1-uv)^d\,dv. \tag{E3}
\]

The integral representation proves that `K_d` is nonincreasing in `u` and in `d`. Thus, for a grid with `η=max_j a_j/t_j`,

\[
I_d\le S_d\le I_d/K_d(\eta).
\]

The last bound may be crude when `b=0`, because the first relative cell size is then one. This does not weaken (E1).

For a nonnegative-coefficient polynomial `f(t)=Σ_{k=0}^d c_k t^k`, `f(T)>0`, the exact endpoint mass identity is

\[
\frac{\int_b^T f(t)dt}{Tf(T)}
=\sum_{k=0}^d\lambda_k\frac{1-(b/T)^{k+1}}{k+1},
\qquad \lambda_k=\frac{c_kT^k}{f(T)}. \tag{E4}
\]

The `λ_k` are a probability vector. This proves the polynomial extension and also its limitation: a degree bound alone does not imply degree-sized endpoint/area gain. Constant-term domination is a counterexample to that inference. The geometric error statements hold for arbitrary nondecreasing convex polynomials on the interval; the coefficientwise `K_d` comparison uses nonnegative coefficients.

## 3. Three scales and the finite local contract

Use consistent notation throughout the article: normalize the heavy player weight to one, let the light weight be `1/R`, let `K` be the integer window length, and let `m=K/R` be the total light mass. The endpoint source calls `m` by `q`, whereas the parameterized all-state source calls `1/R` by `q`; those two symbols must not be substituted into one another.

Put

\[
P=(1+m)^d,\quad
X=\sum_{j=1}^{K}(1+j/R)^d,\quad
Y=\sum_{j=1}^{K}(j/R)^d,
\]
\[
A=\frac{(1+m)^{d+1}-1}{d+1},\qquad
B=\frac{m^{d+1}}{d+1}.
\]

The sums `X,Y` are unweighted player costs. Multiplication by `1/R` produces the corresponding right-sum areas. The heavy mover's own weight is responsible for the positive baseline `1` in `P` and in `H=P−α`; omitting this baseline would change the actual deviation.

The exact finite bounds are

\[
A\le X/R\le A+\varepsilon_X,\quad
B\le Y/R\le B+m^d/R,
\]
\[
\varepsilon_X=\min\left\{
\frac{P-1}{R},\qquad
\frac{P-1}{2R}+\frac{d[(1+m)^{d-1}-1]}{8R^2}
\right\}. \tag{E5}
\]

For `α≥1`, `κ≥1`, define

\[
H=P-\alpha,\quad L=\alpha X-Y,\quad
\Gamma=\frac{L}{RH},\quad S=\frac{\kappa L}{H}.
\]

When `H>0`, local normalized contraction is `Γ<1`; a construction using an amplitude safety factor requires the stronger `S/R=κΓ<1`. The exact finite threshold for the latter is

\[
\alpha_{\mathrm{grid},\kappa}
=\frac{P+\kappa Y/R}{1+\kappa X/R}. \tag{E6}
\]

For any target `α≥1`, `α<α_grid,κ` implies `H>0`, because `Y<PX`, and it is equivalent to `κΓ<1`. A sufficient rationally checkable certificate is

\[
D_\kappa:=P-\alpha-\kappa(\alpha A-B)
>\kappa\alpha\varepsilon_X. \tag{E7}
\]

It gives

\[
1-\kappa\Gamma\ge
\frac{D_\kappa-\kappa\alpha\varepsilon_X}{H}>0. \tag{E8}
\]

All statements (E5)–(E8) are finite statements; no asymptotic approximation is used. For rational `m,α,κ`, integer `R` with `mR∈ℕ`, and integer `d`, all comparisons are rational.

The continuous threshold is

\[
\alpha_{\mathrm{area},\kappa}
=\frac{P+\kappa B}{1+\kappa A}. \tag{E9}
\]

Writing the two right-sum errors as `e_X,e_Y`, monotonicity of `(1+t)^d−t^d` gives `0≤e_Y≤e_X`. Therefore `α_grid,κ≤α_area,κ` when `α_area,κ≥1`. If `α_area,κ<1`, the finite grid still cannot attain a target `α≥1`, since `κ(X−Y)/R>P−1`. A blanket ordering of the two thresholds outside the usable region is unnecessary and is not claimed here. For `κ=1`, the source correctly proves `α_area≥1` for every `m>0`.

The heavy endpoint needs a separate margin:

\[
\kappa L-\alpha X=(\kappa-1)L-Y>0. \tag{E10}
\]

It is not implied by bare `Γ<1`. One sufficient test is `κ−1>z/(α−z)`, where `z=[m/(1+m)]^d`, because `Y≤zX`. The article should display which of (E8) and (E10) each subsequent step spends.

## 4. Exactly what the degree asymptotics establish

For `κ=1`, the explicit lower envelope of (E9), obtained by dropping its favorable `m^{d+1}` term, has maximum

\[
d^{(d-1)/(d+1)}
=d\exp\left(-\frac{2\log d}{d+1}\right)
>d-2\log d
\]

at `1+m=d^{2/(d+1)}`. Strict slack and continuity permit a nearby rational `m`, after which (E7) gives a finite rational grid. This is an exact finite-degree local result. It is not an all-state no-equilibrium theorem with additive gap `2 log d`.

For `α=cd`, fixed `0<c<1`, the separate conditions

\[
m\to0,\qquad d/R\to0,\qquad P/(cd)\to\infty
\]

give `Γ→c`. They remove, respectively, total-mass loss, sampling loss, and the heavy mover's own-cost baseline. Merely requiring `dm→∞` is insufficient: `m=(log log d)/d` leaves `P` of order `log d`, so eventually `H<0`.

If instead `R/d→L₀∈(0,∞)`, `m→m₀≥0`, `K→∞`, and `P/(cd)→∞`, reversing the finite sum gives the exact lattice limit

\[
\Gamma\longrightarrow
\frac{c}{L_0[1-\exp\{-1/(L_0(1+m_0))\}]}.
\]

The geometric domination in the source is valid because `R(1+m)/d` remains bounded above and away from zero. For finite `L₀`, this is a genuine loss and cannot be replaced by `c`. In particular `K=d,R=L₀d` forces `m₀=1/L₀`.

Turning the local leading coefficient one into an all-state result requires independently proved amplitude closure, all-front exits, illegal-state repair, and actual resource degree `d`. The present review neither imports those conclusions from local contraction nor treats an improvement cycle as their substitute. The article may state an all-state theorem only on its separately checked construction proof.

## 5. Positive theorem from the same exact marginal

Consider a finite weighted congestion game with nonnegative-coefficient latencies of degree at most `d`. Fixed nonnegative background loads `b_e` may be included. For every movable player, every resource it may use, and every feasible profile in which it uses that resource, assume the **actual occupied share** satisfies

\[
w_i/L_e(s)\le\eta\le1.
\]

Set `k=K_d(η)>0` and

\[
\Phi(s)=\sum_e\int_{b_e}^{L_e(s)}\ell_e(t)dt.
\]

For a removed resource, (E3) applied coefficientwise gives a decrease of at least `w_i k ℓ_e(L_e(s))`. For an added resource, monotonicity gives an increase of at most `w_i ℓ_e(L_e(s'))`. Common resources have no load change. Adding their identical costs to both sides enlarges the resulting upper bound by `w_i(1−k)C_common≥0`, hence

\[
\Phi(s')-\Phi(s)\le w_i[C_i(s')-kC_i(s)]. \tag{E11}
\]

Every strict `1/k` improvement decreases the same finite-state potential. Thus every such path terminates and a `ρ_d(η)=1/K_d(η)` approximate PNE exists. This independently confirms the source proof, including the common-resource step.

The quantifier covers all relevant occupied states, not only a selected profile and not the total weight of players that could potentially use the resource. For `η=a/d` with fixed positive `a`, the guarantee tends to `a/(1−e^{-a})`; if `dη→0`, it tends to one. At `η=1` this potential gives `d+1`, without proving that this is the best general existence bound.

## 6. Executed exact audits

The following commands were run from the repository root with Python 3.12.14. Every command exited zero. No frozen evidence file was overwritten.

```text
python tests/audits/weighted_congestion/structural_reconstruction/endpoint_certificate.py
python tests/audits/weighted_congestion/structural_reconstruction/raw_resource_audit.py
python tests/audits/weighted_congestion/structural_reconstruction/near_degree_audit.py
```

The endpoint certificate reported `all_exact_checks_passed: true` for
`d=32, α=24, κ=101/100, m=1/4, R=256, K=64`. Its rational comparisons certify

\[
984/1000<S/R<985/1000,\qquad 1-S/R>3/200,
\]
\[
(D_\kappa-\kappa\alpha\varepsilon_X^{\rm refined})/H>3/200,
\qquad (\kappa L-\alpha X)/L>99/10000.
\]

Display-only values were `S/R=0.9844126223250914`, refined analytic contraction lower bound `0.01518547585258097`, coarse analytic lower bound `−0.031832376112681485`, continuous safety threshold `25.624199895655792`, and finite-grid safety threshold `24.372682380275943`. The true normalized heavy margin is slightly below `0.01`; the displayed floating-point value `0.01` must not be read as exact equality.

The actual-resource audit output was:

```json
{
  "status": "PASS",
  "phase_parameter_cases": 1358,
  "repair_bit_strings": 2046,
  "stable_set_instances": 168,
  "seed": null,
  "arithmetic": "fractions.Fraction, exact integers",
  "scope": "finite actual-resource identities only; not a universal proof"
}
```

The near-degree audit output was:

```json
{
  "status": "PASS",
  "checks": {
    "audit_heavy_and_light": 332,
    "audit_return": 225,
    "audit_twist": 560,
    "audit_clock": 2040,
    "audit_tail_rounding": 245
  },
  "total_exact_cases": 3402,
  "arithmetic": "Fraction and integer",
  "seed": null,
  "scope": "finite endpoint, parity, twist, repair and rounding audits only; universal tail has a separate analytic proof"
}
```

These programs evaluate prescribed resource sides and exact fractions. Their phase tables, finite repair strings, stable-set identities, and rounded tail parameters can detect transcription errors. None generates the enormous asymptotic witness or proves a universal no-equilibrium conclusion from samples.

## 7. Required integration wording and remaining limits

No change to the frozen endpoint mathematics was required. The integrated article should:

1. Carry `f'≥0` into the refined convex quadrature lemma, retain the coarse bound when it is smaller, and distinguish the coefficientwise polynomial extension from arbitrary convex functions.
2. Use different symbols for light atom weight and total window mass, always include the deviator's own load, and distinguish `Γ`, `κΓ`, and the heavy margin (E10).
3. Label (E6)–(E9) as the exact boundary of the stated scalar propagation contract. Preserve the usable-region qualification for the `κ` envelope.
4. State the small-atom assumption using actual occupied loads over all relevant states; keep its finite improvement and existence conclusions together with that assumption.
5. Separate the local `d−2 log d` envelope from the full same-degree construction and its independently funded repair budget. No local numerical certificate proves the latter.
6. Describe nonuniform optimal right sums as a numerical compression tool unless a new resource-incidence and repair implementation is supplied. Different cell widths cannot silently replace the equal-weight cyclic ranks.

The exact audits passed, and the independently rederived statements above support using this endpoint mechanism as a reusable analytic part of a structural article. All-state scope, publication priority, and general optimality remain separate claims.
