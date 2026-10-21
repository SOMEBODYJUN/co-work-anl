# Central optimizer deletion: preserved security, an exact bonus budget, and its sharp boundary

Research backup, 2026-10-21. These are exact general lemmas about the original
nonnegative unit-customer CAG potential. They do **not** establish aggregate
security or Q-CAG-HALF. Central suffix optimization differs from a true SPE
suffix; that difference remains a substantive unpaid incentive obligation.

## 1. Objects

For any topic multiset/count vector z define the harmonic potential

\[
\Phi(z)=\sum_x H_{z_x},\qquad H_0=0,
\]

where z_x is the number of chosen topics covering customer x. A provider's
payoff is the deletion marginal of this one common potential. For a fixed
number k≥0 of centrally optimized responders, define

\[
M_k(q)=\max_{B\in\mathcal S^k}\Phi(q+B).
\]

Repeated topics and empty topics remain legal. The maximum is finite and
attained. Prefix q may have repeated labels. No SPE or tie restriction is
used in the following central-optimizer lemmas.

## 2. A safety distribution survives central optimizer elimination

Let the original total provider count be m, let ℓ=m−k≥1, and fix an arbitrary
query distribution p. Write its original oblivious guaranteed value as

\[
s(p)=\min_{|B|=m-1}\mathbb E_{A\sim p}
[\Phi(B+A)-\Phi(B)].
\]

For every opponent prefix q of ℓ−1 topics,

\[
\boxed{\mathbb E_{A\sim p}[M_k(q+A)-M_k(q)]\ge s(p).}\tag{S}
\]

Indeed fix one optimizer B*(q) of M_k(q), independently of the realized query
A. Then

\[
M_k(q+A)-M_k(q)
\ge\Phi(q+B^*+A)-\Phi(q+B^*).
\]

The fixed multiset q+B* has m−1 competitors, so its p-expectation is at least
s(p). In particular an original safety-optimal p guarantees v_m in every
static marginal-potential game based on M_k with ℓ remaining active players.
This is a true nonadaptive comparison: B*(q) is chosen before A.

This result does not make the original earlier players an SPE of the reduced
M_k game. It also does not assert that M_k is submodular; §5 gives a genuine
four-customer failure of that tempting closure property.

## 3. Simultaneous k-responder deletion bonus budget

Fix any prefix q with labelled provider positions i=1,…,ℓ and a central
optimizer B* of k topics. Write q_x for the prefix customer load and b*_x for
the optimized response load. For each prefix provider i with chosen topic a_i,
define the reoptimization bonus on deleting i by

\[
\delta_i^*=M_k(q-e_{a_i})-\Phi(q-e_{a_i}+B^*)\ge0.
\]

Then

\[
\boxed{\sum_i\delta_i^*
\le\sum_{x:q_x>0}
\frac{q_x(k-b_x^*)}{(q_x+b_x^*)(q_x+k)}.}\tag{B}
\]

The denominators are positive. The bound concerns one simultaneous optimizer
of all k responders; it does not add k separate one-responder taxes.

**Proof.** For any candidate B of k topics, optimality at q gives
Φ(q+B)≤Φ(q+B*). Subtracting the two deletion marginals of prefix player i,

\[
\begin{aligned}
\Phi(q-e_{a_i}+B)-\Phi(q-e_{a_i}+B^*)
&\le u_i(q+B^*)-u_i(q+B)\\
&\le\sum_{x\in a_i}
\left[\frac1{q_x+b_x^*}-\frac1{q_x+k}\right].
\end{aligned}
\]

Here every B has customer load at most k. Maximize the left side over B,
then sum i. Each customer x belongs to exactly q_x prefix positions, yielding
(B). Nonnegative customer multiplicities are used in the componentwise bound;
integer multiplicities always represent distinct unit clients.

For k=1 and B*={L}, only x∉L contributes, and

\[
\sum_i\delta_i^*\le\sum_{x\in C(q)\setminus L}\frac1{q_x+1}.
\]

This recovers the root's last-best-response deletion tax. For k≥2 the tax can
be much larger than one-half of prefix payoff; the next section shows that
the coefficient k/(k+1) is sharp even in a very small structured catalog.

## 4. Sharp family: no uniform one-half multi-optimizer bonus bound

For every integer k≥1 choose positive integers a,t with

\[
t=\frac a k(H_{k+1}-1).
\]

They exist, e.g. a=k(k+1)!. Choose an integer g>2kt. The catalog has
A, B_1,…,B_k, D_1,…,D_k. The distinct unit clients are:

- a clients liking exactly {A,D_1,…,D_k};
- t private clients for each B_i;
- g clients liking exactly {B_i,D_j} for each ordered pair (i,j).

Take the single fixed prefix q={A}. Let B*=(B_1,…,B_k). Then B* and
D*=(D_1,…,D_k) both centrally maximize Φ(q+B), and

\[
M_k(A)=k^2g+aH_{k+1}.
\]

After removing A the unique maximizing group is D*, with

\[
M_k(0)=k^2g+aH_k,\qquad \Phi(B^*)=k^2g+kt.
\]

Consequently

\[
\boxed{\delta_A^*=\frac{k}{k+1}a,\quad
u_A(A+B^*)=a,\quad
M_k(A)-M_k(0)=\frac a{k+1}.}
\]

Thus (B) is attained. In particular a bound δ≤(1/2)u_A independent of k is
false for every k≥2, even though B* is a genuine global potential optimizer.

**Why no other response multiset wins.** For k response topics, grid clients
have total incidence at most k², and H_d≤d. Equality of their potential to
k²g holds only for all k distinct B topics or all k distinct D topics. Any
other multiset either uses A and loses at least kg of grid incidence, or has
a grid client of load at least two and loses at least g/2 because
2−H_2=1/2. Its extra non-grid potential is at most aH_{k+1}+kt with prefix A,
and aH_k+kt without it. Since g/2>kt, it cannot beat the better pure group.
The two pure groups tie with prefix A by the choice of t. Without A, D*
beats B* by a[H_k−(H_{k+1}−1)]=ak/(k+1)>0.

A smaller exact k=2 instance already attains the bound with a=12,t=5,g=3;
its 15 possible two-topic response multisets are checked independently by
`verify_optimizer_deletion.py`. The general proof above uses the sufficient
larger g>2kt; it makes no minimality claim.

This family is a central-optimization obstruction. The fixed prefix need not
be played by an SPE at the root. It is not a counterexample to any aggregate
SPE bridge or half coverage.

## 5. The reduced envelope is not submodular

Four distinct unit clients x1,x2,y,z and four topics suffice:
A={x1,x2}, B={y,z}, C={y}, D={z}. Let M=M_1. At the fixed prefix q=A+D,

\[
M(q)=9/2,\quad M(q+C)=5,\quad
M(q+D)=29/6,\quad M(q+C+D)=11/2.
\]

Hence

\[
M(q+C)+M(q+D)=59/6<10=M(q)+M(q+C+D).
\]

The maximizer changes from B to A; the submodularity deficit is 1/6.
The original Φ is a genuine positive CAG harmonic potential. Thus preservation
of the safety distribution in (S) does not permit direct recursion through
the common-monotone-submodular conjecture.

## 6. The exact remaining credibility gap

For a **true SPE** suffix B_actual, define Γ=M_k(q)−Φ(q+B_actual)≥0 and
δ_i^actual=M_k(q−e_ai)−Φ(q−e_ai+B_actual)≥0. The exact payoff identity is

\[
u_i(q+B_{actual})=[M_k(q)-M_k(q-e_{a_i})]
+\delta_i^{actual}-\Gamma.
\]

The same Γ enters every prefix player's payoff, but it varies across true
deviation branches. One cannot discard −Γ. A further aggregate coverage
rearrangement can cancel Γ algebraically, but that rearrangement collapses
to conservation of covered prefix clients and provides no new incentive
budget by itself. We do not claim otherwise.

To turn (S) and (B) into a global security proof requires a genuinely new
comparison paying the branch-dependent Γ/δ debt from true successor
optimality. This note proves the static preservation and central deletion
budget, and gives exact limits on two naive ways of completing that step.
