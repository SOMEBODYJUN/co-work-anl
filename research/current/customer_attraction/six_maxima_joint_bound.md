# CA-SIX-MAXIMA-HALF: arbitrary-provider half coverage with at most six maximal coverages

Version: 2026-10-10. Complete current proof, exact author coefficient audit, independent exact audit and independent mathematical reconstruction. External peer review and novelty have not been certified.

**Theorem.** In [CAG-MODEL](model.md), assume a finite nonempty common theme catalog, unit customers, unit providers moving once in order, and at most six distinct inclusion-maximal coverage sets. For every integer `n>=1` and every pure SPE defined on **all full ordered histories**,

\[
 \boxed{\operatorname{OPT}_n\le2W.}
\tag{J1}
\]

Let `U` be the union of the catalog. For every `n>=5` the proof gives the stronger union statement

\[
 \boxed{U\le2W.}
\tag{J2}
\]

When `n>=6`, `OPT_n=U`. For five providers and six maxima, that equality is not assumed. Arbitrary internal subthemes, omitted core customers, repeated or empty action labels, repeated choices, and every history-dependent tie are included. The new critical-case argument proves `U<=2W`; it does not claim the core-strengthened inequality `U<=2W-c` universally.

## 1. Exact use of the established mixed floor

The cases with at most five maxima follow from [CA-FIVE-MAXIMA-HALF](dynamic_maxima_bound.md). We therefore prove the remaining critical cases with exactly six distinct maximal coverage sets `B_0,...,B_5`. Each is the coverage of a legal theme. Set

\[
 C=\bigcap_{j=0}^5B_j,\qquad c=|C|.
\]

Every catalog customer belongs to a nonempty maximal incidence
`I subset {0,...,5}`. Let `P` be the total mass of singleton incidences and `V=U-c-P` the mass of incidences of size two through five. The proven [CA-DYNAMIC-MAXIMA-MIXED](dynamic_maxima_bound.md#5-mixed-privateshared-refinement) floor uses

\[
 A_t=\frac{n+t}{2(t+1)(3n-2t)}\ (t<n-1),\qquad A_{n-1}=\frac1{n+5},
\]

and their suffix minima, together with the nondecreasing sequence

\[
 b_t=\frac1{3n-2t}\ (t<n-1),\qquad
 b_{n-1}=\frac{n+1}{n(n+5)}.
\tag{J3}
\]

For every `n>=5` the private suffix envelope is at least `1/(2n)`. Indeed

\[
 n(n+t)-(t+1)(3n-2t)
 =2\left(t-\frac{n-1}{2}\right)^2+\frac{n^2-4n-1}{2}\ge0,
\]

and `1/(n+5)>=1/(2n)`. The shared last-step comparison is
`(n+1)(n+4)-n(n+5)=4`, so (J3) is nondecreasing. Thus every actual root-path provider has the valid necessary inequality

\[
 u_t\ge\frac cn+\frac P{2n}+b_tV.
\tag{J4}
\]

This is a coarsening of the previously proved full-history mixed floor. Its proof allows actions that omit core and residual customers. The true action of an earlier provider need not equal its chosen maximal container.

## 2. The final action is a whole maximal coverage

**Last-action lemma.** At every legal prefix of length `n-1`, the action selected by any pure SPE has inclusion-maximal coverage.

If its coverage `A` were strictly contained in a legal theme's coverage `B`, changing to `B` would preserve every payment from `A`. Each added customer `x in B\A` would pay the strictly positive amount `1/(h_x+1)`, where `h_x` is its actual earlier load. There are no followers whose actions can change. This is a strict profitable deviation, contradicting final-player optimality. Hence the chosen coverage equals one of the distinct `B_j`. Duplicate theme labels do not affect this argument, and every final-player tie still obeys it.

Route each root action into any maximal coverage containing it, choosing arbitrary containers for internal subthemes. Write its route string as `a=(a_0,...,a_{n-1})`. The last-action lemma implies that the **true final coverage equals** `B_{a_{n-1}}`.

For each customer, let `J subset {0,...,n-1}` be the set of providers whose **true root actions** cover it. Its maximal incidence `I` and actual membership `J` satisfy

\[
 J\subseteq\{t:a_t\in I\},\qquad
 1_{n-1\in J}=1_{a_{n-1}\in I}.
\tag{J5}
\]

Only the second equality uses the final maximal action; no earlier container is treated as actual coverage. Let `w_{I,J}` count customers of each type. Then the exact, nonduplicating decomposition is

\[
 U=\sum_{I,J}w_{I,J},\quad
 W=\sum_{I,J}w_{I,J}1_{J\ne\varnothing},\quad
 u_t=\sum_{I,J}w_{I,J}\frac{1_{t\in J}}{|J|},\quad
 \sum_tu_t=W.
\tag{J6}
\]

All fractions with zero numerator are defined as zero. A nonzero numerator always has positive denominator. Core customers are the incidence `I={0,...,5}`, even if earlier true actions omit them; the final action covers all of them.

## 3. A complete linear budget of genuine SPE inequalities

We use three families of **nonnegative** slacks, each valid for the given full SPE.

1. The `n` mixed slacks `M_t=u_t-c/n-P/(2n)-b_t V`, from (J4).
2. The six exact final-player best-response slacks

\[
 L_j=u_{n-1}-\sum_{I,J}w_{I,J}
 \frac{1_{j\in I}}{|J\cap\{0,...,n-2\}|+1}\ge0.
\tag{J7}
\]

The deviation is the legal full maximal theme `B_j`, holding the genuine earlier actions fixed.

3. For each of the 21 unordered index pairs `0<=j<=k<=5`, including repetitions, use the established [CA-TWO-REMAINING-TAX](two_remaining_tax.md) at the actual prefix of length `n-2`. For a type set

\[
 p=|J\cap\{0,...,n-3\}|,\qquad d=1_{n-2\in J},\qquad
 m_{jk}=1_{j\in I}+1_{k\in I}.
\]

The valid pair slack is

\[
 T_{jk}=u_{n-2}+u_{n-1}
 +\sum_{I,J}w_{I,J}\frac d{(p+1)(p+2)}
 -\sum_{I,J}w_{I,J}\frac{m_{jk}}{p+m_{jk}}\ge0.
\tag{J8}
\]

Its comparison is the remaining profit of the legal theme pair `(B_j,B_k)` under the **actual** preceding load `p`. Its tax uses the true penultimate action. The tax theorem proves (J8) from the original strategy's true response after the first comparison deviation, that response's last-player optimality, and the actual final player's comparison to the same response. It never freezes the actual follower after a deviation. Repeated pairs are legal under the common catalog.

Let `S_q` list these nonnegative slacks, and let `s_q(I,J)` be their raw per-customer coefficients. For any nonnegative multipliers `lambda_q`, define

\[
 r(I,J)=1_{J\ne\varnothing}-\frac12
 -\sum_q\lambda_qs_q(I,J).
\tag{J9}
\]

There is then an exact accounting identity

\[
 \boxed{W-\frac U2=\sum_q\lambda_q S_q+
 \sum_{I,J}w_{I,J}r(I,J).}
\tag{J10}
\]

Thus nonnegative **customer-level** residuals prove half coverage. No separately maximized floors are added, and covered customers are charged only through their real shares in (J6).

## 4. Five providers: all 52 complete routing classes

With five positions a route uses at most five of the six labels. Rename labels in order of first appearance. The resulting restricted-growth string obeys

\[
 a_0=0,\qquad 0\le a_t\le1+\max_{q<t}a_q.
\tag{J11}
\]

There are exactly 52 such strings of length five. These are **complete routes**, including the position and identity of the last maximal action. The 15 strings of length four classify only prefixes and are insufficient by themselves for (J5). Unused labels may be ordered arbitrarily; every maximal incidence is still enumerated.

The [frozen rational certificate](../../../evidence/certificates/customer_attraction/six_maxima_joint_bound.json) contains one explicit 32-coordinate nonnegative multiplier vector for every string (J11). The row order is

- `mixed:0,...,mixed:4`;
- `lastBR:0,...,lastBR:5`;
- `twoTax:00,01,...,05,11,...,55`, with pairs in lexicographic order.

Every coordinate is the stored nonnegative integer divided by **10000**. No LP solver or optimality statement is part of the certificate.

For each of the 52 routes, enumerate every nonempty `I subset {0,...,5}` and **every** `J` satisfying (J5). Direct Fraction substitution in (J9) proves all **20,080** customer inequalities nonnegative; the minimum is exactly zero. This finite enumeration is complete: the type of every actual customer appears, and their integer masses can be arbitrary. Applying (J10) proves `U<=2W` for every five-player SPE with exactly six maxima. It does not assume a realization for every auxiliary type, since admitting extra types only strengthens the coefficient requirement.

## 5. Six, seven or eight providers: one path-free small-fraction dual

For these three player counts, route enumeration is unnecessary. Relabel the true final maximal action `B_0` and enlarge the type domain: every earlier true membership bit is unrestricted, while the last bit is exactly `1_{0 in I}`. This broader domain contains every genuine route and actual action profile.

Use the **same** nonzero multipliers at each of these player counts:

| Nonnegative slack family | Multiplier |
| --- | ---: |
| `M_t`, `0<=t<=n-3` | `35/48` |
| `L_j`, `1<=j<=5` | `1/8` |
| `T_{0j}`, `1<=j<=5` | `5/48` |
| `T_{jk}`, `1<=j<k<=5` | `1/96` |

All other multipliers are zero. They are nonnegative and use precisely the valid inequalities §3.

For transparency, the residual depends only on four small integers. Write

\[
 f=1_{0\in I},\quad k=|I\setminus\{0\}|,\quad
 p=|J\cap\{0,...,n-3\}|,\quad d=1_{n-2\in J}.
\]

Here `f,d in {0,1}`, `0<=k<=5`, `1<=k+f<=6`, and `0<=p<=n-2`. Put

\[
 F_n(m)=\begin{cases}
 (n-2)/(2n),&m=1,\\
 \sum_{t=0}^{n-3}1/(3n-2t),&2\le m\le5,\\
 (n-2)/n,&m=6,
 \end{cases}
\]

\[
 g_{f,k}(p)=\begin{cases}k/(p+1),&f=0,\\
 (5-k)/(p+1)+2k/(p+2),&f=1,\end{cases}
\quad
 h_k(p)=\frac{k(5-k)}{p+1}+\frac{k(k-1)}{p+2}.
\]

Expanding (J9), including every actual share and the true tax, gives

\[
\begin{aligned}
 r_n(k,f,p,d)={}&1_{p+d+f>0}-\frac12+\frac{35}{48}F_n(k+f)
 +\frac{k}{8(p+d+1)}\\
 &+\frac5{48}g_{f,k}(p)+\frac1{96}h_k(p)
 -\frac{35p+30d+60f}{48(p+d+f)}
 -\frac{5d}{8(p+1)(p+2)}.
\end{aligned}
\tag{J12}
\]

The share term is zero when its denominator is zero. The `k(5-k)` and `k(k-1)` terms count respectively one and two memberships in the ten distinct pairs among the other five maxima. These formulas retain true earlier coverage only through its count, rather than replacing earlier actions by containers.

The complete finite ranges in (J12) have respectively 110, 132 and 154 cases. Fraction substitution gives:

| `n` | All literal `(I,J)` columns | Minimum residual | Resulting lower fraction `W/U` |
| --- | ---: | ---: | ---: |
| 6 | 2016 | `1/72` | `37/72` |
| 7 | 4032 | `1/32` | `17/32` |
| 8 | 8064 | `23393/532224` | `289505/532224` |

The exact audit independently evaluates both the raw slacks and (J12) on **every** literal column and verifies their equality. Thus the 396 compressed cases cover the entire enlarged domain, not a sampled ordering region. All three minimum residuals are positive, so (J10) proves the claimed half bound with the displayed margins. No seat sorting, fractional seat selection or route classification enters this branch.

## 6. All remaining cases and precise scope

For `n=1`, the only provider chooses maximum coverage, so `W=OPT_1`. For `n=2`, the zero-background [two-remaining tax theorem](two_remaining_tax.md#3-无背景时重构两人已发表界) gives `OPT_2<=3W/2`. The established [sharp three-player theorem](three_player_sharp.md) gives `OPT_3<=5W/3`, and [CA-FOUR-UPPER-1499-750](four_player_bound.md) gives `OPT_4<=1499W/750<2W`. These are universal catalog bounds, so they cover six maxima as well. They compare to `OPT_n`, and do not substitute the full union for small player counts.

For `n>=9`, [CA-SIX-MAXIMA-NINE-PLUS-HALF](six_maxima_no_private.md#5-nine-or-more-providers-unrestricted-six-maxima) already proves `OPT_n=U<=2W-c` with arbitrary private/shared incidence and internal subthemes. The proof is analytic for all `n>=9` and independently audited; a finite scan of player counts is not used as its universal justification.

For fewer than six maxima, the previously proved [CA-FIVE-MAXIMA-HALF](dynamic_maxima_bound.md) supplies all player counts, and `U=OPT_n` for `n>=5`. Hence no fictitious theme, padded action, or modified classification of private customers is needed. The zero-union case has `W=OPT_n=0` immediately. Repeated theme labels, empty internal actions and arbitrary ties were retained by the mixed-floor and tax premises and by the last-action lemma. Nothing in the proof assumes the SPE terminal is a simultaneous PNE.

The theorem closes the unrestricted **at-most-six-maxima** class. Catalogs with seven or more distinct maximal coverages and at least five providers remain outside this theorem. The earlier [dynamic-seat path obstructions](six_maxima_seat_obstructions.md) remain valid obstructions to that specified aggregate mechanism; they are not SPE welfare counterexamples, and the present joint accounting uses additional true-membership and final-response information.

## 7. Exact audit and review obligations

The [standard-library coefficient audit](../../../tests/audits/customer_attraction_six_maxima_joint.py) imports no model, SPE solver, discovery LP or earlier audit. It reconstructs the nonnegative aggregate slacks from raw per-customer equal-sharing coefficients, verifies the 52-route certificate completeness, checks all 20,080 five-player columns, and evaluates the common dual on all 14,112 enlarged-domain columns for six through eight players. It also checks all 396 compressed identities and minima. The finite check of the private envelope for `n=5,...,100` is a regression; the displayed algebra in §1 is its universal proof.

Replay:

```sh
python tests/audits/customer_attraction_six_maxima_joint.py
```

The frozen author record is [here](../../../evidence/runs/2026-10-10/customer_attraction_six_maxima_joint_final.json). The complete exact certificates are proof data and have been audited independently of their numeric discovery. The [independent exact audit](../../../tests/audits/customer_attraction_six_maxima_joint_independent.py) separately reconstructs all raw slacks and checks the same finite domains; its [frozen record](../../../evidence/runs/2026-10-10/customer_attraction_six_maxima_joint_independent.json) records the exact results. The [independent mathematical review](../../../evidence/runs/2026-10-10/customer_attraction_six_maxima_joint_math_review.json) reconstructs the SPE legality, final-action lemma, route completeness, enlarged domains and exact dual. Both internal reviews passed. External peer review, novelty and factor sharpness are not asserted.
