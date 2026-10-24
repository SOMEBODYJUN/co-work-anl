# Incidence-LP dynamic budget for maximal-cover routing

**Status.** Candidate general lemma / reusable proof interface. It is a direct extension of the routed-prefix argument in `research/current/customer_attraction/dynamic_maxima_bound.md`; it does **not** prove Q-CAG-HALF for unrestricted incidence. No finite computation is used.

## Exact setup

Use CAG-MODEL with `n` providers and a finite common catalog. Let
`B_1,...,B_s` be the distinct inclusion-maximal coverage sets, and write
`C=intersection_j B_j`, `c=|C|`, `U=|union_j B_j|`. Route every catalog label to one containing maximal set. For each nonempty incidence `I subseteq [s]`, let

\[
X_I=\{x:\{j:x\in B_j\}=I\},\qquad w_I=|X_I|.
\]

At a legal prefix of length `t`, let `p_j` be the number of earlier actions routed to `j`; put `r=n-t` and `p_I=sum_{j in I}p_j`. Define

\[
f_j(p,r)=\frac{w_{\{j\}}}{p_j+1}+
 \sum_{\substack{I\ni j\\ |I|\ge2}}
 \frac{w_I}{p_I+r}.
\tag{1}
\]

The same deviation/subset-domination argument as in the dynamic-maxima proof gives, for a deviation to the whole `B_j`, a payoff at least `c/n+f_j(p,r)`. If a later action is routed to `j`, its whole theme is a subset of `B_j`, so the deviator's payoff dominates that follower's terminal payoff on the same branch; if no later action is routed to `j`, the displayed denominator bounds the final loads directly.

## Incidence LP

For each `r>=1`, define

\[
B(r)=\min\left\{\sum_{j=1}^s \beta_j:\;\beta_j\ge1\ \text{if }w_{\{j\}}>0,\quad
\sum_{j\in I}\beta_j\ge r\ \text{for every }I\text{ with }w_I>0,\ |I|\ge2,\quad \beta_j\ge0\right\}.
\tag{2}
\]

This is a finite rational covering LP. The private lower bound is needed only when the corresponding private block is nonempty. If `U-c>0`, then `B(r)>=1`; when `U-c=0` the welfare bound is trivial and the LP denominator can be omitted. Set

\[
D_t=t+B(n-t),
\qquad
E_t=\max_{q\in\{t,t+1,\ldots,n-1\}}D_q.
\tag{3}
\]

`E_t` is a nonincreasing suffix envelope even when `D_t` itself is not monotone.

## Prefix counting inequality

Choose an LP-feasible `beta` for `r` and set `y_j=p_j+beta_j`. For a private block `X_{\{j\}}`,

\[
\frac{y_j}{p_j+1}\ge1
\]

by `beta_j>=1`. For a nonprivate incidence `I`,

\[
\frac{\sum_{j\in I}y_j}{p_I+r}
=\frac{p_I+\sum_{j\in I}\beta_j}{p_I+r}\ge1
\]

by (2). Therefore

\[
U-c\le\sum_j y_j f_j(p,r)
\le (t+B(r))\max_j f_j(p,r)=D_t\max_j f_j(p,r).
\tag{4}
\]

Consequently some legal maximal deviation gives at least

\[
\frac cn+\frac{U-c}{D_t}\ge
\ell_t:=\frac cn+\frac{U-c}{E_t}.
\tag{5}
\]

## Backward-induction consequence

For every complete ordered-history pure SPE and every legal prefix of length `t`, the current provider's terminal payoff is at least `ell_t`.

Proof is by backward induction on `r`. At the current prefix deviate to a maximizing `B_j`. If no later action is routed to `j`, (4) gives (5). If a later action is routed to `j`, choose the first such follower at actual depth `q>=t+1`. The induction hypothesis gives that follower payoff at least `ell_q`; because `E_q<=E_t`, this is at least `ell_t`. The deviator chose all of `B_j`, hence contains the follower's theme and obtains at least the follower's terminal payoff on every customer in that theme. SPE optimality transfers this deviation lower bound to the prescribed action. The argument uses the original continuation after the forced action, all ordered histories, and arbitrary history-dependent ties.

Summing at the root gives the general incidence-LP bound

\[
\boxed{W\ge c+(U-c)\sum_{t=0}^{n-1}\frac1{E_t}.}
\tag{6}
\]

Since `OPT_n<=U`, the same coefficient bounds optimal coverage. If the coefficient in (6) is at least `1/2`, Q-CAG-HALF holds for this incidence class.

## Relation to existing bounds and exact limitation

Taking `beta_j=r/2` for every `j` (and at `r=1`, `beta_j=1`) recovers the existing scalar budget `t+s(n-t)/2` and `n+s-1`, after suffix enveloping. More generally (2) can be strictly smaller for sparse incidence systems or for maxima without private blocks, giving a data-dependent certificate. It also explains why a uniform factor cannot follow from this LP alone: with all pair incidences on `s` maxima and no private blocks, symmetry forces `B(r)=sr/2`, so the budget is linear in `s`. The missing general step is therefore a second mechanism for dense high-incidence systems (e.g. cross-customer load balancing or true continuation credit); this lemma does not claim that mechanism.

No claim is made that the LP coefficient is sharp for SPE welfare. Failure of the coefficient to reach `1/2` is only a certificate-template boundary, not a Q-CAG-HALF counterexample.

## A clean sufficient incidence condition

Let

\[
\tau_{\rm inc}=\min\left\{\sum_j\alpha_j:\;\alpha_j\ge1\ (w_{\{j\}}>0),\quad
\sum_{j\in I}\alpha_j\ge1\ (w_I>0, |I|\ge2),\quad \alpha_j\ge0\right\}.
\tag{7}
\]

This is a fractional cover number of the maximal-incidence hypergraph, with singleton edges retained. When `U-c>0`, `tau_inc>=1`. Taking `beta=r alpha` in (2) gives `B(r)≤r tau_inc`. Since `tau_inc>=1`, the comparison denominator `n+(tau_inc−1)r` is nonincreasing in prefix length and dominates the suffix envelope. Hence

\[
W\ge c+(U-c)\sum_{r=1}^n\frac1{n+(\tau_{\rm inc}-1)r}.
\tag{8}
\]

In particular, `tau_inc≤2` implies half coverage because

\[
\sum_{r=1}^n\frac1{n+(\tau_{\rm inc}-1)r}
\ge\sum_{r=1}^n\frac1{n+r}\ge\frac12
\]

(each denominator in the last sum is at most `2n`; the `n=1` endpoint is exactly `1/2`). This condition is a distinct, incidence-level certificate; it is not a bound on the original theme fractional cover `tau_C`. For all-shared incidence and `s≤4`, `alpha_j=1/2` recovers the known `s≤4` route. Sparse incidence can satisfy `tau_inc≤2` even when the number of maximal themes is larger. The condition is only sufficient: disjoint-maxima catalogs have large `tau_inc` but are handled by the separate singleton-load mechanism.
