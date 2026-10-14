# Explicit directed cohort family with asymptotic leading constant one

## Claim R1-COHORT-UNIFORM v2

**Exact Statement.** For every integer d≥ceil(e^8)=2981 there is the explicit finite weighted congestion game G_d below, with positive weights and positive monomial coefficients of degree at most d, such that every pure state admits a strict α_d-improvement, where

    α_d = d/(ln d+4 ln ln d).

Therefore G_d has no β-PNE for any 1≤β≤α_d, and a_*(d)≥α_d. In particular

    liminf_{d→∞} a_*(d)/(d/ln d) ≥ 1.

**Objects.** The same directed odd-ring hub/cohort architecture as R1-COHORT-UNIFORM v1, with the new parameters specified here. Every reset main resource can have many strategic users. The binary complementary pair-resource 2-PNE obstruction is consequently inapplicable.

**Domain / Quantifiers.** Every integer d≥2981; all pure states of the resulting finite game; real positive weights and coefficients; integer positive player counts. No fixed-player-count restriction is imposed.

**Assumptions.** Exact MODEL.md, including the cost convention without multiplication by player weight. No other game assumptions.

## Explicit parameters, weights, and resources

Write

    D=ln d,
    h=ln D,
    α=d/(D+4h),
    t=(D+2h)/d,
    m=the least odd integer ≥D^2,
    k=ceil(2D/h),
    x=t^{2m−1},
    n=floor(1/(kx)).

The reset has (n_0,k_0,x_0)=(n,k,x), and every buffer i=1,…,m−1 has (n_i,k_i,x_i)=(1,d,1/t). All indices are modulo m.

Hub weights and light weights are

    u_0=1,
    u_i=t^{2(m−i)}   (1≤i≤m−1),
    u_m=u_0,
    v_i=t u_{i+1}   (0≤i≤m−1).

Cohort i contains n_i light players of weight v_i. Thus v_i/u_i=x_i and v_i/u_{i+1}=t, with exact cyclic closure Π_i x_i=t^m.

Main resources A_i^0,A_i^1 each have cost a_i z^{k_i}. Light-specific side resources B_{i,j}^0,B_{i,j}^1 each have cost b_i z^d. Hub H_i with action h_i selects A_i^{h_i} and every B_{i−1,j}^{h_i}; light L_{i,j} with action l_{i,j} selects A_i^{l_{i,j}} and B_{i,j}^{1−l_{i,j}}. These are the players' complete strategy sets. The positive coefficient recipe is given below.

## Certificate interface and coefficient recipe

Define q_i=a_i u_i^{k_i}, p_i=b_i u_{i+1}^d and

    N_i=(1+x_i)^{k_i}−α(n_i x_i)^{k_i},
    M_i=α(1+n_i x_i)^{k_i}−1,
    Q=(1+t)^d−α,
    P=α(1+t)^d−t^d,
    F_i=n_i N_iQ/(M_iP),
    Z=Π_i F_i.

We prove N_i,M_i,Q,P>0 and Z>1. Then let

    R_i=n_i N_iQ/(P M_{i+1}),
    q_0=1,
    q_{i+1}/q_i=R_i/Z^{1/m},
    D_i=q_{i+1}M_{i+1}/(n_i Q),
    U_i=q_iN_i/P,
    p_i=sqrt(D_iU_i),
    a_i=q_i/u_i^{k_i},
    b_i=p_i/u_{i+1}^d.

The q-ratio product is one, so the cyclic construction is consistent. Since D_i<U_i, it gives the strict inequalities

    q_i N_i>p_iP,
    n_i p_iQ>q_{i+1}M_{i+1}.                              (CERT)

**All-state coverage.** If any light has l_{i,j}=h_i, switching its bit decreases its cost by a strict factor greater than α: its current cost minus α times deviation cost is at least q_iN_i−p_iP>0. This bound permits all cohort mixtures. If no such light exists, all lights in cohort i have bit 1−h_i. The odd ring has some h_i=h_{i+1}; H_{i+1}'s cost difference on flipping is exactly n_i p_iQ−q_{i+1}M_{i+1}>0. Hence every pure state is covered. Detailed resource-load derivations are in UNIFORM_COHORT_FAMILY.md and are unchanged by these parameters.

## Uniform parameter and degree checks

Throughout D≥8 and h=ln D>2. The ceiling implies

    k≤2D/h+1≤3D/h≤3D≤d.

As in v1, max_{z>0}(ln z)/z^{1/4}=4/e<2 gives h<2D^{1/4}. Therefore

    k≥D^{3/4},
    k ln k≥(2D/h)(3h/4)=3D/2,
    α/k^k≤(d/D)e^{−3D/2}=e^{−D/2}/D<1/2.              (1)

The elementary inequality 2ln D≤D holds for D≥8. Consequently

    0<t≤2D/d≤d^{−1/2}<1.

Because m≥D^2≥64, we have 2m−1≥15, and

    kx≤d^{−13/2}<1/2,
    n≥1/(2kx),
    nx≤1/k.                                               (2)

Thus n is a positive integer, weights are positive, and all resource degrees are at most d.

## Product bound

Put y=(1+t)^d and c=1−2/D^3. The logarithmic lower bound yields

    ln y≥dt−dt^2/2
         =D+2h−(D+2h)^2/(2d)
         ≥D+2h−2D^2/e^D.

For D≥8, 2D^2/e^D≤128/e^8<1/2<ln2. Hence

    y>dD^2/2,
    α/y<2/D^3,
    Q/P=(y−α)/(αy−t^d)>c/α.                              (3)

In particular Q,P>0 and c>0.

For every buffer, N_i=t^{−d}Q, M_i=t^{−d}P, and thus F_i=(Q/P)^2>c^2/α^2.

For the reset, (1)–(2) imply

    N_0≥1−α/k^k>1/2,
    M_0≤α(1+1/k)^k≤eα,
    F_0>n c/(2eα^2)≥c/(4e kxα^2).

Combining the reset and m−1 buffers gives

    Z>c^{2m−1}/(4e k t^{2m−1}α^{2m})
      =t/(4e k c) · [c/(αt)]^{2m}.                       (4)

We now give a robust explicit lower bound on the logarithm of the bracket. Since 2h≤D and D^2h≥24,

    ln[c/(αt)]
      =ln(1−2/D^3)+ln[(D+4h)/(D+2h)]
      ≥−4/D^3+2h/(D+4h)
      ≥−4/D^3+2h/(3D)
      ≥h/(2D).                                            (5)

The first inequality uses ln(1−z)≥−z/(1−z), z=2/D^3≤1/2, and ln(1+z)≥z/(1+z). These are valid with strict slack for D≥8.

Finally t≥D/d and k≤3D/h give t/k≥h/(3d). From m≥D^2, c<1, and (4)–(5),

    Z> [h/(12e)] exp[D(h−1)].                             (6)

Since D≥8 and h=ln D≥ln8>2, the right side exceeds e^7/6>1. Thus Z>1 uniformly over every integer d≥2981, proving (CERT) and the claimed all-state nonexistence.

## Claim metadata

**Scope / Conclusion.** Explicit infinite family with a lower-bound leading constant one relative to d/ln d. The stronger denominator ln d+4lnln d replaces v1's constant 8ln d. This note does not assert novelty, an improvement over known results, or an upper bound.

**Dependencies.** MODEL.md; common architecture and all-state load derivations in UNIFORM_COHORT_FAMILY.md; elementary real inequalities and odd binary ring parity.

**Evidence.** Explicit weights/counts/degrees, positive coefficients, strict certificate inequalities, uniform Z>1, and exhaustive state coverage.

**Counterevidence/Objections.** The number of hubs and lights grows with d; main resource degrees are heterogeneous; real weights and coefficients are used. All three are expressly permitted in MODEL.md. No claim is made about exact optimality of the interface or all games on this architecture. External literature comparison remains necessary before calling the result new.

**Status.** PROVED by the displayed inequalities; independently audited from the parent candidate. Novelty NOT CHECKED.

**Related Files.** ../../../../MODEL.md; UNIFORM_COHORT_FAMILY.md; PAIR_OBSTRUCTION.md.
