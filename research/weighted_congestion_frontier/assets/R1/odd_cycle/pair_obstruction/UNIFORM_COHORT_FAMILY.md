# Explicit uniform directed cohort-ring family

## Claim R1-COHORT-UNIFORM v1

**Exact Statement.** For every integer d≥ceil(e^8)=2981, the finite weighted congestion game G_d explicitly constructed below belongs to the exact class in MODEL.md and has no α_d-PNE, where

    α_d = d/(8 ln d).

Every pure state admits a strict α_d-improvement. Consequently the same game has no β-PNE for any 1≤β≤α_d, and the universal threshold satisfies a_*(d)≥d/(8 ln d) for these d.

**Objects.** Binary hub players and binary light cohorts on a directed odd ring; two columns per main resource and per light-specific side resource.

**Domain / Quantifiers.** Every integer d≥2981; arbitrary positive real weights and positive real coefficients are legal in MODEL.md. The construction selects particular such weights and coefficients and permits player/resource counts to grow with d. The nonexistence statement quantifies over every pure state, rather than a selected improvement cycle.

**Assumptions.** Costs are sums of resource costs without a multiplier w_i. Every player has exactly the two strategies specified below. There are no other resources or players. Degree may vary by resource but is at most d.

**Definitions.** All logarithms are natural. Set

    r = ln d,
    α = d/(8r),
    L = ln α,
    m = the least odd integer ≥r,
    t = 2L/d,
    k = ceil(2L/ln L),
    x = t^(2m−1),
    n = floor(1/(kx)).

For the reset cohort i=0 put (n_0,k_0,x_0)=(n,k,x). For each buffer i=1,…,m−1 put

    (n_i,k_i,x_i)=(1,d,1/t).

Indices are modulo m. We prove below that L>3, 1≤k≤d, n≥1, and t∈(0,1).

## Weights and strategies

Hub H_0 has weight u_0=1. For 1≤i≤m−1 put

    u_i=t^{2(m−i)},
    u_m=u_0,
    v_i=t u_{i+1}  (0≤i≤m−1).

Cohort i contains n_i distinct players L_{i,j}, each of weight v_i. These formulas give v_i/u_i=x_i and v_i/u_{i+1}=t, including the reset. Thus

    Π_i x_i = t^m = Π_i(v_i/u_{i+1}),

and the weight closure is exact.

For each i there are main resources A_i^0,A_i^1 with identical cost a_i z^{k_i}. For each (i,j) there are side resources B_{i,j}^0,B_{i,j}^1 with identical cost b_i z^d. All a_i,b_i will be strictly positive.

Hub H_i with action h_i∈{0,1} selects A_i^{h_i} and all n_{i−1} side resources B_{i−1,j}^{h_i}. Light player L_{i,j} with action l_{i,j}∈{0,1} selects A_i^{l_{i,j}} and B_{i,j}^{1−l_{i,j}}.

There are m+Σ_i n_i players and 2m+2Σ_i n_i resources, all finite. Main A_0 resources have degree k≤d; all buffer mains and all side resources have degree d. Main resources may be used by more than two strategic players, so the pair-resource obstruction does not apply.

## Exact sufficient inequalities and all-state coverage

Scale coefficients by

    q_i=a_i u_i^{k_i},
    p_i=b_i u_{i+1}^d.

For each i define

    N_i=(1+x_i)^{k_i}−α(n_i x_i)^{k_i},
    M_i=α(1+n_i x_i)^{k_i}−1,
    Q=(1+t)^d−α,
    P=α(1+t)^d−t^d.

It suffices to choose q_i,p_i>0 such that for every i,

    q_i N_i > p_i P,                                      (LIGHT_i)
    n_i p_i Q > q_{i+1} M_{i+1}.                          (HUB_i)

Here is a complete coverage proof. If there is any light player whose bit l_{i,j}=h_i, let s≥1 be the number of cohort i players sharing h_i. Its current main cost is at least a_i(u_i+v_i)^{k_i}; after switching, its main resource contains at most n_i light weights and no hub. Its current side cost is at least b_i v_i^d; after switching, its side cost is at most b_i(u_{i+1}+v_i)^d. Therefore current cost minus α times deviation cost is at least

    q_i[(1+x_i)^{k_i}−α(n_i x_i)^{k_i}]
      −p_i[α(1+t)^d−t^d]
    = q_i N_i−p_i P > 0.

This bound allows arbitrary cohort mixtures and arbitrary h_{i+1}.

Otherwise every light has l_{i,j}=1−h_i. An odd binary ring has some index i with h_i=h_{i+1}. For that i, H_{i+1} collides with every light of cohort i on their side resources. Its current cost and deviation cost are exactly

    C = q_{i+1}+n_i p_i(1+t)^d,
    C' = q_{i+1}(1+n_{i+1}x_{i+1})^{k_{i+1}}+n_i p_i.

Consequently C−αC'=n_i p_iQ−q_{i+1}M_{i+1}>0. These two cases exhaust all pure states.

## Exact coefficient construction

Suppose N_i,Q,P,M_i are positive and put

    F_i = n_i N_i Q/(M_i P),
    R_i = n_i N_i Q/(P M_{i+1}),
    Z = Π_i F_i = Π_i R_i.

If Z>1, set q_0=1 and recursively

    q_{i+1}/q_i = R_i/Z^{1/m}.

The product of these ratios is one, so this cyclic definition is consistent. Define the strict lower/upper bounds

    D_i = q_{i+1}M_{i+1}/(n_i Q),
    U_i = q_i N_i/P.

The ratio construction gives D_i<U_i. Set

    p_i = sqrt(D_i U_i),
    a_i = q_i/u_i^{k_i},
    b_i = p_i/u_{i+1}^d.

Then all coefficients are positive and both (LIGHT_i) and (HUB_i) hold strictly. This construction is algebraic in the displayed parameters; no search or unstated coefficient choice is required.

## Uniform proof that Z>1

We use only elementary inequalities, keeping explicit constants.

Since r≥8, the increasing function r−ln(8r) gives

    L≥8−ln64>3.

Thus α>e^3>4 and ln L>1. The ceiling gives

    k≤2L/ln L+1≤3L/ln L≤3r≤d.

To bound k^k, the elementary maximum of (ln z)/z^{1/4} is 4/e<2. Hence ln L<2L^{1/4} and

    k≥2L/ln L≥L^{3/4},
    k ln k≥(2L/ln L)(3 ln L/4)=3L/2,
    α/k^k≤α^{−1/2}<1/2.                                  (1)

Also 2r≤e^{r/2} for r≥8, so

    0<t≤2r/d≤d^{−1/2}<1.

As m≥r≥8, we have 2m−1≥15, and therefore

    kx≤d·d^{−15/2}=d^{−13/2}<1/2,
    n=floor(1/(kx))≥1/(2kx),
    nx≤1/k.                                               (2)

For y=(1+t)^d, using ln(1+t)≥t−t^2/2 gives

    ln y≥2L−2L^2/d.

The function r^2 e^{−r} decreases for r≥8, so

    2L^2/d≤2r^2e^{−r}≤128/e^8<1/2<ln2.

Thus

    y>α^2/2>2α,
    Q=y−α>y/2,
    0<P=αy−t^d<αy,
    Q/P>1/(2α).                                          (3)

For every buffer, the identities are exact:

    N_i=t^{−d}Q,
    M_i=t^{−d}P,
    F_i=(Q/P)^2>1/(4α^2).                                (4)

For the reset, (1) and (2) give

    N_0=(1+x)^k−α(nx)^k≥1−α/k^k>1/2,
    M_0≤α(1+1/k)^k≤eα,
    F_0=n N_0Q/(M_0P)>n/(4eα^2)
        ≥1/(8e kxα^2).                                   (5)

Equations (4)–(5), with x=t^{2m−1}, imply

    Z > [1/(8e k t^{2m−1}α^2)] [1/(4α^2)]^{m−1}
      = [t/(2e k)] [1/(4α^2t^2)]^m.

But αt=L/(4r)<1/4, hence 1/(4α^2t^2)>4. Furthermore k≤3L/ln L≤3L, so t/k≥2/(3d). Since m≥ln d,

    Z > d^{ln4−1}/(3e)>1.                                (6)

The last inequality holds already for d≥e^8: it is equivalent at d=e^8 to 4^8>3e^9, which follows from e<3 and 4^8=65536>3^{10}=59049. This proves the coefficient feasibility and the all-state nonexistence claim for every stated d.

## Claim metadata

**Scope / Conclusion.** An explicit infinite-family lower bound of order d/ln d in the exact nonnegative polynomial weighted congestion model. Strict inequalities establish failure even at α_d itself. This note proves the construction; it does not claim novelty or an improvement over any external lower bound.

**Dependencies.** MODEL.md; the directed cohort-ring architecture supplied by the parent branch; elementary finite binary odd-cycle parity and elementary real inequalities.

**Evidence.** Explicit weights, integer multiplicities, degree check, positive coefficient recipe, uniform product bound, and exhaustive two-case state coverage are all supplied above.

**Counterevidence/Objections.** The reset main has many strategic users, so the pure pair-resource 2-PNE theorem is inapplicable. The main degree k is heterogeneous, but k≤d was proved; the model permits heterogeneous resource degrees. Player count grows rapidly with d, which the model permits. Weights and coefficients need not be rational; the model explicitly permits all positive real weights and nonnegative real coefficients. Comparison against existing literature remains open and is required before labeling this a new lower bound.

**Status.** PROVED by the above algebra; independent branch review found no local-cost, closure, degree, integrality, or all-state coverage error. Novelty NOT CHECKED.

**Related Files.** ../../../../MODEL.md; PAIR_OBSTRUCTION.md.
