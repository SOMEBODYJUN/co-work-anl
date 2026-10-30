# 任意玩家乘子势：有限多尺度边际夹逼障碍候选

Date: 2026-10-14. Originator: internal `attack_sandwich` agent, requested configuration `gpt-6.1-sol / ultra`; independent reconstruction by R1 upper-mechanism agent. This is an additional mechanism claim. It does not change the scope of `WC-R1-SANDWICH-BARRIER v1` in the frozen `proof.md`.

## Claim WC-R1-MULTIPLIER-BARRIER v1

**Exact Statement.** Fix an integer d≥2 and a real α≥1. If α<sup_{t>0}R_d(t), where

    R_d(t)=((d+1)(1+t)^d+t^(d+1))/(d+(1+t)^(d+1)),

then there is a finite positive weight vector w for which no set function F:2^[n]→R and no positive multipliers h_1,…,h_n satisfy

    h_i (w(S)+w_i)^d ≤ F(S∪{i})−F(S)
                      ≤ α h_i (w(S)+w_i)^d                  (M1)

for all S⊆[n] and i∉S. The h_i and F may depend arbitrarily on the entire finite vector w.

**Objects / Domain.** Finite positive real weights; one monomial resource c(x)=x^d; all player subsets; arbitrary positive player-specific scalar multipliers.

**Quantifiers.** For every d≥2 and every 1≤α<sup_tR_d(t), a finite vector exists which defeats every choice of the pair (F,h). The vector may depend on d,α. Neither infinitely many players nor infinitesimal weights are legal witnesses; only finite instances constructed below are used.

**Assumptions / Definitions.** Define κ*_d(w)=inf{α≥1: some F,h satisfy (M1)} and κ*_d=sup_w κ*_d(w). No attainment of the infimum in h is assumed or needed.

**Scope.** A uniform local marginal sandwich after any fixed positive rescaling of each player's cost. The same h_i must be used for that player on every resource when applying such a certificate to a game. This theorem already defeats the certificate on one resource. It does not exclude state-dependent rescalings, cross-resource cancellations, nonseparable potentials, or non-potential existence arguments. It is not an α-PNE nonexistence theorem.

**Conclusion.** κ*_d≥sup_tR_d(t)>d^((d−1)/(d+1)); the non-strict consequence κ*_d≥d^((d−1)/(d+1)) suffices here. Since choosing h_i=w_i and the known potential gives κ*_d≤d, κ*_d/d→1. The strict displayed inequality follows by choosing the t used in (5) of `proof.md`; it concerns the supremum κ*_d, not attainment by one fixed finite vector.

**Dependencies.** Within-class averaging; telescoping; finite Riemann-sum convergence; monotonicity of a linear fractional function. The lower proof below is self-contained. The bound d^((d−1)/(d+1)) and the elementary upper sandwich are reconstructed in `proof.md`.

**Evidence.** Full argument below; exact finite compressed certificates from `verify_multipliers.py`. The originating internal reviewer reconstructed the original mechanism before proposing this extension; R1 upper-mechanism then independently checked the multiscale argument. Parent and external review pending.

**Counterevidence / Objections.** One heavy/light block does not prove this result: arbitrary h can equalize its two paths. Multiple scales are essential to this proof. Averaging must permute both F and h before replacing h by class averages. All necessary clones must exist in the one finite weight vector. Endpoint α=supR_d(t) is not covered. No novelty claim has been verified.

**Status.** Self-contained candidate proof plus internal reconstruction and exact certificates; not canonical; external review pending.

**Related Files.** `proof.md`, `verify_multipliers.py`, `multiplier_evidence.json`.

## 1. Symmetrization within each equal-weight class

Suppose players are partitioned into finitely many classes, class j having weight a_j. Let G be the finite group of all permutations that preserve each class. Given (F,h) satisfying (M1), define

    Fbar(S)=|G|^(-1) Σ_{g∈G} F(gS),
    hbar_j=the arithmetic mean of h_i over class j.

For i in class j, w(gS)=w(S) and w_{g(i)}=a_j. Averaging (M1) for the pair (gS,g(i)) yields (M1) for Fbar and multiplier hbar_j. Thus it suffices to contradict classwise constant positive multipliers. Put β_j=hbar_j/a_j>0.

## 2. An exact two-class inequality

Select one player from a heavier class i and K players from a lighter class j. Write

    ε=a_j/a_i∈(0,1),  s=β_j/β_i>0,  u=Kε.

Apply the two orderings only to this selected subset, starting from the empty set. Normalize path sums by hbar_i a_i^d. The heavy-last and heavy-first sums are

    A_{ε,K}(s)=(1+u)^d+s ε Σ_{k=1}^K(kε)^d,
    B_{ε,K}(s)=1+s ε Σ_{k=1}^K(1+kε)^d.

Both paths have the same endpoints. Hence feasibility implies

    1/α ≤ r_{ε,K}(s):=A_{ε,K}(s)/B_{ε,K}(s) ≤ α.             (M2)

Let a=(1+u)^d, b=εΣ(kε)^d, c=εΣ(1+kε)^d. For K≥1, a>1 and 0<b<c. Therefore

    d[(a+sb)/(1+sc)]/ds=(b−ac)/(1+sc)^2<0.                  (M3)

For fixed t>0 set K=floor(t/ε), ensuring K≥1 once ε<t. As ε↓0, u→t and the sums are right Riemann sums. Thus

    r_{ε,floor(t/ε)}(s) → R_s(t)
      := ((d+1)(1+t)^d+s t^(d+1))
          /((d+1)+s((1+t)^(d+1)−1))                        (M4)

for every fixed positive s. R_1(t)=R_d(t).

## 3. Two constraints on relative multipliers

Choose t0>0 with R_1(t0)>α. By continuity in s, choose λ>1 with

    R_λ(t0)>α.                                              (M5)

Choose t1>0 so small that t1^(d+1)/((1+t1)^(d+1)−1)<1/α. This is possible since that fraction tends to zero as t1↓0. Then choose C>λ so large that

    R_C(t1)<1/α.                                            (M6)

By (M4), there exists δ>0, chosen also below min{1,t0,t1}, such that for all 0<ε<δ,

    r_{ε,floor(t0/ε)}(λ)>α,
    r_{ε,floor(t1/ε)}(C)<1/α.                               (M7)

By (M3), (M2) and the first inequality in (M7) force s>λ. The second forces s<C. These are strict inequalities. No convergence of F or h is involved.

## 4. One finite weight vector creates a contradiction

Choose an integer L≥1 with λ^L>C. Choose a fixed q∈(0,δ), and put a_j=q^j for j=0,…,L. Let T=max{t0,t1}. Give class j exactly

    N_j=ceil(T/a_j)+1

players. These are finite positive integers, and every player has strictly positive weight.

For each adjacent pair i,i+1, select one class-i player and floor(t0/q) class-(i+1) players. This many exist: a_i≤1 implies floor(t0 a_i/a_{i+1})≤T/a_{i+1}<N_{i+1}. Their ratio ε=q<δ makes the first constraint in (M7) apply. Consequently

    β_{i+1}/β_i>λ  (i=0,…,L−1),
    β_L/β_0>λ^L>C.                                         (M8)

Now select one class-0 player and floor(t1/q^L) class-L players, which again exist by the stated multiplicity. Their weight ratio is ε=q^L≤q<δ, so the second constraint forces

    β_L/β_0<C,                                              (M9)

contradicting (M8). Thus no F,h satisfying (M1) exist for this finite vector.

## 5. Rational finite construction and verification interface

For rational α,t0 with R_1(t0)>α, all parameters can be rational and finite. One direct selection is

    D0=α((1+t0)^(d+1)−1)−t0^(d+1)>0,
    λmax=(d+1)((1+t0)^d−α)/D0>1,
    λ=(1+λmax)/2.

Then (M5) follows by cross multiplication. Set t1=1/(α+1), which satisfies (M6)'s limiting requirement because

    t1^(d+1)/((1+t1)^(d+1)−1) ≤ t1^d/(d+1)<1/α.

Let D1=((1+t1)^(d+1)−1)−αt1^(d+1)>0 and choose

    C=λ+1+(d+1)(α(1+t1)^d−1)/D1.

Then C>λ and R_C(t1)<1/α. Find finite L with λ^L>C. Search integers Q≥2 until the two exact tests

    r_{1/Q,floor(Qt0)}(λ)>α,
    r_{Q^(−L),floor(Q^L t1)}(C)<1/α

both hold. Convergence guarantees termination. Taking q=1/Q gives the finite construction above. This search need only check adjacent and extreme class ratios, so it does not require explicit δ or uniform numerical sampling.

The test program computes the enormous but finite path sums through the exact recurrence

    S_0(K)=K,
    S_p(K)=((K+1)^(p+1)−1−Σ_{r=0}^{p−1}binom(p+1,r)S_r(K))/(p+1),

where S_p(K)=Σ_{k=1}^K k^p. The integer divisions are asserted exact. This provides compressed finite certificates even when expanding all clones would be impractical. The certificates witness failure of (M1) and do not enumerate pure game states or prove equilibrium nonexistence.

## Remaining research obligation

This removes fixed player-specific rescaling as an escape from the uniform local sandwich. A possible o(d) proof must use additional structure, for example correlations across a player's simultaneous resource changes, restrictions on the local inequalities needed only at a selected state, or a potential whose change cannot be certified resource by resource by fixed positive player multipliers. Establishing any such mechanism remains open.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
