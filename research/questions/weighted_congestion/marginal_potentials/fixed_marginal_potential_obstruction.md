# 按玩家权重校准的边际势：线性障碍候选

Date: 2026-10-14. Author: R1 internal upper-mechanism agent (model inherited from parent; no model label inferred). Independent mathematical attack: internal `attack_sandwich`, requested `gpt-6.1-sol / ultra`; its returned checks are recorded separately. This document is a mechanism obstruction, not a lower bound on the universal equilibrium threshold.

## Claim WC-R1-SANDWICH-BARRIER v1

**Exact Statement.** Fix an integer d≥2. For every α<d^((d−1)/(d+1)), there is a finite positive real weight vector w such that no set function F:2^[n]→R satisfies, for every S⊆[n] and i∉S,

    w_i (w(S)+w_i)^d ≤ F(S∪{i})−F(S) ≤ α w_i (w(S)+w_i)^d.       (1)

The same obstruction applies to a sandwich with endpoints m and M, 0<m≤M, whenever M/m<d^((d−1)/(d+1)), by replacing F by F/m. The potential need not be anonymous, homogeneous, differentiable, polynomial, or independent of the complete finite weight vector.

**Objects / Domain.** Finite nonempty weight vectors with arbitrary positive real entries; all their subsets; one monomial resource c(x)=x^d. F may depend on the entire vector w and d.

**Quantifiers.** For every d≥2 and every α below the displayed threshold, there exists a finite vector w for which every set function F fails at least one inequality (1). This does not assert one fixed finite vector attains the limiting threshold.

**Assumptions / Definitions.** w(S)=Σ_{i∈S}w_i. A local increment is Δ_iF(S)=F(S∪{i})−F(S). A uniform weight-calibrated marginal certificate uses common m,M for every relevant resource, player, and subset; a resource coefficient multiplies both the marginal and the cost comparison. Define κ_d(w) as the minimum α admitting (1), and κ_d=sup_w κ_d(w).

**Scope.** An obstruction to certifying an approximate potential through the displayed local sandwich. It covers arbitrary resource set potentials satisfying this certificate, including dependence on player identities and all weight moments. It does not cover arbitrary player-specific multipliers in place of w_i, state-dependent certificates, cancellation across resources, nonseparable potentials, or proofs that establish existence without a potential. It does not show a game without an α-PNE. In particular, a one-resource game in which everyone may choose the empty strategy has an exact equilibrium even though its all-subsets marginal sandwich can be costly.

**Conclusion.** κ_d≥d^((d−1)/(d+1))=d−2 log d+O((log d)^2/d). Thus no o(d) existence bound can follow solely from a universal certificate of form (1). The lower barrier concerns the certificate's distortion, not a_*(d).

**Dependencies.** Telescoping of finite sums; convergence of right Riemann sums for x^d on compact intervals; elementary algebra. No imported equilibrium theorem is needed for the lower barrier. A reconstruction of the known upper sandwich, below, gives κ_d≤d.

**Evidence.** Complete proof below; exact rational finite witnesses from `verify.py`; internal independent attack confirms the two-order construction and quantifiers. Numerical values are not used in the proof.

**Counterevidence / Objections.** The all-subsets sandwich is a sufficient proof mechanism, not a necessary condition for an approximate potential or equilibrium existence. The n→∞ step must remain an existence-of-a-finite-witness argument for every strictly smaller target. Free player multipliers can balance this individual two-order cycle and are not excluded. The construction is plausibly related to known potential-method limitations; novelty is unverified.

**Status.** Self-contained proof; internal independent mathematical check; parent review pending. Not a canonical team theorem and not externally reviewed. Main target WC-TARGET v1 remains open.

**Related Files.** `verify.py`, `evidence.json`; source links at the end.

## Two-order proof

For any ordering π of the players, set S_k={π(1),…,π(k)} and define

    T_π(w)=Σ_{k=1}^n w_{π(k)} w(S_k)^d.

Summing (1) along the chain from ∅ to [n] gives

    T_π(w) ≤ F([n])−F(∅) ≤ α T_π(w).                            (2)

Therefore α≥T_π/T_σ for every pair of orderings π,σ.

Take one player of weight 1 and n players of common weight ε=t/n, where t>0. Let A_n(t) be the sum with all light players first and the heavy player last, and B_n(t) the sum with the heavy player first:

    A_n(t)=(1+t)^d + ε Σ_{j=1}^n (jε)^d,
    B_n(t)=1 + ε Σ_{j=1}^n (1+jε)^d.                            (3)

Each ε is strictly positive and the number of players is finite. Equation (2) yields α≥A_n/B_n. As n→∞ at fixed d,t,

    A_n→(1+t)^d+t^(d+1)/(d+1),
    B_n→1+((1+t)^(d+1)−1)/(d+1).

Consequently, if a proposed α works for every finite vector, then

    α ≥ R_d(t)
      := ((d+1)(1+t)^d+t^(d+1))/(d+(1+t)^(d+1))                (4)

for every t>0. Equivalently, whenever α<R_d(t), convergence provides some finite n with α<A_n/B_n, contradicting (2).

Put y=d^(2/(d+1)) and t=y−1>0. Since y^(d+1)=d²,

    R_d(t) > (d+1)y^d/(d+d²)
           = y^d/d
           = d^((d−1)/(d+1)).                                (5)

The strict inequality comes from t^(d+1)>0. This proves the stated strict-below-threshold obstruction. Finally,

    d^((d−1)/(d+1))=d exp(−2 log d/(d+1))
                   =d−2 log d+O((log d)^2/d).

No infinite-player game is asserted or used as a legal witness.

## Explicit finite error bound and a d+1-player witness

For a nondecreasing continuous f, its right Riemann sum on [a,a+t] with mesh ε=t/n is at most its integral plus ε(f(a+t)−f(a)). Therefore (3) gives

    A_n ≥ (1+t)^d,
    B_n ≤ 1+((1+t)^(d+1)−1)/(d+1)
             +(t/n)((1+t)^d−1).                              (6)

At y=d^(2/(d+1)), t=y−1, the first two terms in B_n sum to d. Thus

    A_n/B_n ≥ (d/y)/(1+(t/n)(d/y−1/d)).                       (7)

Taking n=d gives

    A_d/B_d ≥ d/(y+t−ty/d²) ≥ d/(1+2t)
             = d/(2d^(2/(d+1))−1)
             = d−4 log d+O((log d)^2/d).                     (8)

Hence an explicit family with exactly d+1 players already produces an asymptotically linear certificate obstruction. Irrationality of t is allowed by MODEL.md. The verification script separately uses rational t and exact arithmetic; it does not approximate (8) and present it as exact.

## Reconstructing the known upper sandwich (not a new existence result)

For d≥1 define

    H_d(S) = (w(S)^(d+1)+d Σ_{i∈S}w_i^(d+1))/(d+1).

For absent i, put x=w(S)/w_i. Dividing its increment by w_i^(d+1) gives

    Q_d(x)=((1+x)^(d+1)−x^(d+1)+d)/(d+1)
          =1+Σ_{k=1}^d binom(d,k) x^k/(d+1−k).

Since 1/d≤1/(d+1−k)≤1 for 1≤k≤d, and the constant term is 1,

    (1+x)^d/d ≤ Q_d(x) ≤ (1+x)^d.

Thus w_i(w(S)+w_i)^d/d≤Δ_iH_d(S)≤w_i(w(S)+w_i)^d. The function dH_d satisfies (1) with α=d; hence κ_d≤d. Combining this with (5) yields κ_d/d→1.

This is the γ=1 potential in Caragiannis–Fanelli, reconstructed algebraically rather than imported without checking. Constant costs (degree zero) have the exact resource potential H_0(S)=w(S). For nonnegative polynomial coefficients, add the monomial potentials coefficientwise; choose the degree-d lower endpoint 1/d for every positive degree≤d, with constants satisfying the same bound. For a unilateral move, shared resources cancel in the potential; the nonnegative costs of shared resources preserve the needed comparison. Therefore the usual argument covers empty strategies and zero coefficients too. This reconstructs a sufficient upper certificate only; it does not strengthen the literature d bound.

## Claim WC-R1-CYCLE-RATIO v1: a finite exact certificate interface

**Exact Statement.** For each fixed finite positive weight vector w and integer d≥0, form the graph whose vertices are subsets S. For every i∉S put A(S,i)=w_i(w(S)+w_i)^d>0. Add an upward arc S→S∪{i} and a downward reverse arc. For a directed cycle C let U(C) be the sum of A over upward arcs and D(C) the sum over downward arcs. Then

    κ_d(w)=max_C D(C)/U(C),                                   (9)

where the maximum may be restricted to simple directed cycles. In particular κ_d(w) is attained by a set function F.

**Objects / Domain / Quantifiers.** Every fixed finite positive vector w; every integer d≥0; every directed cycle in its finite subset graph. This concerns (1), not all approximate potentials.

**Assumptions / Definitions / Scope / Conclusion.** A directed cycle has both up and down arcs, so U(C)>0. κ_d(w) is as defined above. Formula (9) is an exact finite characterization of the local sandwich optimization.

**Dependencies / Evidence.** Finite difference constraints; proof follows. Internal independent attack confirmed both directions, including nonmonotone cycles. No numerical optimizer is needed.

**Counterevidence / Objections / Status.** Considering only two monotone orderings need not exhaust (9); no assertion of their sufficiency is made. This is a generic difference-constraints representation, so novelty is not asserted. Self-contained proof, internal check, parent review pending.

**Related Files.** This document; `verify.py` uses a two-path exact certificate only and does not compute the maximum in (9).

To prove (9), rewrite (1) as

    F(S∪{i}) ≤ F(S)+αA(S,i),
    F(S) ≤ F(S∪{i})−A(S,i).

Assign arc length αA to an up arc and −A to a down arc. Summing these constraints around a directed cycle gives αU(C)−D(C)≥0, proving necessity. Conversely, if all cycles have nonnegative length, distances from a new source joined to every vertex by zero-length arcs are finite and satisfy every arc constraint. These distances provide F. Every closed walk decomposes into simple cycles; its D/U is a U-weighted mean of their ratios, so a finite simple-cycle maximum suffices. At that maximum there is no negative cycle and the same construction gives an attaining F. A two-edge cycle gives ratio 1, ensuring κ_d(w)≥1.

## Literature checks and interpretation

- Caragiannis–Fanelli, arXiv:1902.07173v5, §2 Lemma 1, Definition 1 and Theorem 2: https://arxiv.org/pdf/1902.07173 . The relevant mechanism is precisely a common multiplicative comparison between a resource-set marginal and w_i times latency. Their γ=1 formula is H_d above. The paper also distinguishes convergence of all sufficiently improving paths from bare equilibrium existence.
- Christodoulou et al., arXiv:2002.07466v3, §7: https://arxiv.org/html/2002.07466v3#S7 . It identifies the Ω(√d/log d) versus d gap and points to potential-based upper arguments. This section does not itself prove a barrier for all potential arguments; neither does the present document.
- Next obligation: to seek o(d), one must leave the common w_i marginal sandwich, e.g. justify compatible player-specific multipliers or use a statewise argument. Such an escape needs new inequalities; neither this obstruction nor the finite cycle representation supplies them.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
