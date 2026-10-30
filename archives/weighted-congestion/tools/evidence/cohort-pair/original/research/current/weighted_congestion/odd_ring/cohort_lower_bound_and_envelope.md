# 奇数环总证明：全状态非存在、精确包络与同次数构造

Authorship and provenance: the odd hub/cohort strategy construction was posted
by R1 in public-board message 42 (`aa0ccec68ec54eed9ce2e6b3c0e5c909`). R3 independently
reconstructed its full-state proof, then derived the scalar envelope and a
uniform-degree rational construction. Internal agents independently reconstructed
the coverage and attacked the parameter and envelope arguments; see the linked
reviews. This is unrefereed mathematical work. Global priority is not certified.

While this proof was being completed, R1 posted independently frozen message48
(`a3541c655682451584ef4a38c9b6c430`, commit `ba6fb27b6b5e1d5b00fe6fbb40178f1b5e334194`)
with a linear reset and the equivalent scalar function H_d(t). Substitution
R=1/t identifies sup H_d(t) with T_d exactly. Thus the d/ln d advancement is
a shared, independently reconstructed mechanism, not a claim that this R3
record alone originated that growth. Our additional exact upper bounds the
entire specified positive test system and our realizing construction uses only
degree-d monomials.

## 1. Exact claims and epistemic scope

**WC-R3-ODD-RING-CERTIFICATE-v1.** Fix integer d>=1, odd integer m>=3,
integers n_i>=1 and 1<=k_i<=d, positive real weights u_i,v_i, and alpha>1.
Indices are modulo m. Define x_i=v_i/u_i, t_i=v_i/u_(i+1), and

    N_i=(1+x_i)^k_i-alpha(n_i x_i)^k_i,
    M_i=alpha(1+n_i x_i)^k_i-1,
    P_i=alpha(1+t_i)^d-t_i^d,
    Q_i=(1+t_i)^d-alpha.

The two strict local tests in section 3 have positive resource coefficients
if and only if every N_i,Q_i is positive and

    G=product_i n_i N_i Q_i/(M_i P_i)>1.

These tests imply that the game in section 2 has no alpha-PNE. The iff describes
this sufficient test system, not all possible nonexistence proofs for the topology.

**WC-R3-ODD-RING-ENVELOPE-v1.** Put

    f_d(R)=[R(1+R)^d+1]/[(1+R)^d+R^(d+1)],
    T_d=sup_{R>1} f_d(R).

For fixed d>=2 and alpha>1, some finite odd ring can satisfy the above positive
test system if and only if alpha<T_d. The supremum is attained by the scalar
function, but the strict certificate does not attain alpha=T_d. Moreover,

    H_d<T_d<=H_d+1/(2^d+1),
    H_d=d/[(d+1)d^(1/(d+1))-d],
    T_d~d/ln d.

**WC-R3-ODD-RING-LOWER-v1.** For every integer d>=2 and every real
1<=alpha<T_d there is a finite game in MODEL's G_d, with positive rational
weights and coefficients and all latencies monomials of degree exactly d,
which has no alpha-PNE. Thus

    a_*(d)>=T_d,   liminf_{d->infinity} a_*(d) ln(d)/d>=1.

For each alpha a new finite game may be chosen. No one fixed finite game is
claimed to obstruct every alpha<T_d. This is a full-model lower bound, with
player count and resource support allowed to grow; no efficient input-size
construction or full-model upper bound is claimed.

Objects, domain, quantifiers, assumptions and definitions are exactly those
displayed here and in [MODEL](../../../weighted_congestion_frontier/MODEL.md). Conclusions concern weak
alpha-PNE inequalities; our witnesses strictly violate them. Dependencies are
elementary inequalities and the explicit construction, not an imported
existence theorem. General proofs establish the claims; finite computations
are supplementary evidence. The current proof and independent internal reviews
record no unresolved fatal objection in the stated scope. Novelty remains
unassessed globally. Value is the growing lower family and reusable certificate;
mechanism is odd parity plus multiplicative weight/coefficients feedback;
ambition is a lower-bound stage breakthrough, not resolution of WC-TARGET.

## 2. The actual game

Hub H_i has weight u_i. Cohort i contains n_i players L_ij of common weight v_i.
There are distinct resources A_i^b and B_ij^b for b in {0,1}, with fees

    c_(A_i^b)(z)=a_i z^k_i,
    c_(B_ij^b)(z)=b_i z^d,

where a_i,b_i>0 do not depend on the player using the resource or on b.
Hub H_i's action h uses A_i^h and every incoming B_(i-1),j^h.
Light L_ij's action l uses A_i^l and B_ij^(1-l).
Each player has exactly these two resource-subset strategies. Its weight is
the same on every resource; its cost is the sum of resource latencies, without
multiplying by weight. There are m+sum_i n_i players and 2m+2sum_i n_i resources.
All are finite. In particular this is neither a player-specific-cost game nor
a weighted-resource-demand model.

## 3. Coverage of every state and the coefficient cycle

If any light L_ij is aligned with its own hub, its current cost is at least

    a_i(u_i+v_i)^k_i+b_i v_i^d.

After flipping its action its cost is at most

    a_i(n_i v_i)^k_i+b_i(v_i+u_(i+1))^d.

The first bound allows all other cohort actions and either neighboring hub
action; the second includes the deviator and at most all n_i cohort members.
Consequently every aligned light has a strict alpha improvement if

    A_i N_i>B_i P_i,                       (L_i)

where A_i=a_i u_i^k_i and B_i=b_i u_(i+1)^d.

Otherwise all lights are anti-aligned with their own hubs. An odd binary ring
has an edge with h_(i-1)=h_i: if every adjacent pair differed, following all
m edges would flip the initial bit an odd number of times and not return it.
At this edge H_i has current and flipped costs exactly

    a_i u_i^k_i+n_(i-1)b_(i-1)(u_i+v_(i-1))^d,
    a_i(u_i+n_i v_i)^k_i+n_(i-1)b_(i-1)u_i^d.

It therefore strictly improves if

    n_(i-1) B_(i-1) Q_(i-1)>A_i M_i.       (H_i)

This proves all-state nonexistence from the local tests; it is stronger than
finding a cycle of improving states. All constructed current/deviation costs
are positive, so no 0/0 convention is used. Empty strategies and zero fees
permitted in MODEL do not impose additional obligations on this positive
subclass construction.

M_i,P_i are positive for alpha>1. Positive A_i,B_i satisfying (L_i),(H_i)
force N_i,Q_i>0 and

    B_i<R_i B_(i-1),
    R_i=n_(i-1)Q_(i-1)N_i/(M_i P_i).

Multiplication proves G=product_i R_i>1. Conversely suppose these signs and
G>1 hold. Let delta=(G-1)/(2mG). Set B_0=1 and, successively for i=1,...,m-1,

    B_i=(1-delta) R_i B_(i-1).

Bernoulli's inequality gives

    G(1-delta)^m >= G(1-m delta)=(G+1)/2>1.

It follows that the wrap edge also satisfies B_0<(1-delta)R_0 B_(m-1),
and hence all B_i<R_i B_(i-1). Choose A_i as the arithmetic midpoint between
B_i P_i/N_i and n_(i-1)B_(i-1)Q_(i-1)/M_i. Both tests are strict. Recover
a_i=A_i/u_i^k_i and b_i=B_i/u_(i+1)^d. All quantities are positive rationals
if weights, alpha and x_i,t_i are rational. This is a constructive coefficient
formula with no root extraction and no unspecified feasibility oracle.

## 4. The exact necessary envelope

Let y=n x and define, for alpha>1,

    F_(k,n)(x)=n x[(1+x)^k-alpha(n x)^k]/[alpha(1+n x)^k-1].

On a positive certificate edge,

    F_(k,n)(x)<=F_(k,1)(n x),
    Q/(tP)=F_(d,1)(1/t).

The first inequality uses 1+x<=1+n x and the common positive denominator.
The second is obtained by multiplying numerator and denominator by t^(-d).
Also, for every y>0,

    F_(k,1)(y)>1  iff  alpha<f_k(y).

For 0<y<=1, f_k(y)<=1: after multiplying out, this says
(1+y)^k>=sum_{j=0}^k y^j, which holds since every binomial coefficient is >=1.
For y>1, f_k(y) increases in k. To check this without an imported theorem,
write A=(1+y)^(-k), B=(y/(1+y))^k. The numerator of f_(k+1)-f_k, after
using the positive denominators, is

    [A y/(1+y)] [y^(k+1)-1-(y-1)B]>0.

Indeed y^(k+1)-1=(y-1)sum_{j=0}^k y^j>(y-1)B.
Therefore f_k(y)<=T_d for every k<=d,y>0.
If alpha>=T_d every F_(k,1)(y)<=1. Since

    product_i x_i=product_i t_i,
    G=product_i [x_i n_i N_i/M_i] [Q_i/(t_i P_i)],

the preceding inequalities imply G<=1, a contradiction. Thus every positive
certificate has alpha<T_d. This argument does not construct an alpha-PNE
when the certificate fails; it does not upper-bound the actual topology or a_*.

For d>=2, the binomial argument is strict when R>1, so f_d(R)>1 there.
At R=1 and as R tends to infinity its value tends to 1. Continuity therefore
puts the supremum at a finite interior R>1. For d=1 the function is identically 1.

## 5. Rational attaining families below the envelope

Fix integer d>=2 and a real 1<=alpha<T_d. Continuity and density of the
rationals allow rational a,R such that alpha<a<f_d(R), R>1. Write

    E=(1+1/R)^d,
    q=(E-a)/(aE-R^(-d)),
    B=ceil(4ad).

One has 0<q<1 and Rq>1. In fact a<f_d(R) is precisely Rq>1 after multiplying
by positive denominators. Also f_d(R)<E since R^(-d)<E^2, so E>a.
Choose an odd m>=3 such that, with ell=2m-1,

    (Rq)^ell>12Ba.                         (S)

Such m exists because Rq>1; this strict rational inequality is an effective
parameter-selection rule. Define

    u_0=R^ell, v_0=1,
    u_i=R^(2i-1), v_i=R^(2i)  (1<=i<m),
    n_0=floor(R^ell/B), n_i=1 (1<=i<m), k_i=d (all i).

Then x_0=R^(-ell), x_i=R for i>=1, and every t_i=1/R, including the wrap
edge. In particular product_i x_i=product_i t_i is exactly realized by the
actual resource-independent weights. At ordinary nodes N_i/M_i=q; at every
outgoing edge Q_i/P_i=q. Hence

    G=n_0 (N_0/M_0) q^ell.

Because q<1, (S) implies R^ell>12Ba>2B. Thus n_0>=R^ell/(2B)>=1. Moreover

    n_0 x_0<=1/B,
    N_0>=1-a/B^d>=1-a/B>=3/4>1/2,
    M_0<a(1+1/B)^d<=a exp(d/B)<e a.

The last inequality uses B>=4ad and a>1. It follows that

    G>(Rq)^ell/(4Bea)>3/e>1.

All N,Q,M,P are positive. Section 3 now constructs positive rational
coefficients and proves no a-PNE, and therefore no alpha-PNE, at every state.
Every latency has degree exactly d. The family need not have polynomial
size in d or in the precision of alpha; no such claim enters MODEL's threshold.

## 6. Growth and sharpness of this certificate's leading constant

Write

    f_d(R)=g_d(R)+1/[(1+R)^d+R^(d+1)],
    g_d(R)=R/[1+R(R/(1+R))^d].

For d>=2 differentiation gives the unique maximizer

    R*=1/[d^(1/(d+1))-1]>1,
    max_{R>0} g_d(R)=H_d=d/[(d+1)d^(1/(d+1))-d].

Indeed the derivative has the sign of 1-d(R/(1+R))^(d+1); it changes from
positive to negative at R*. For R>1 the extra term lies in (0,1/(2^d+1)),
giving H_d<T_d<=H_d+1/(2^d+1). Taylor expansion with z=ln d/(d+1)->0 gives

    (d+1)exp(z)-d=1+ln d+O((ln d)^2/d),

so T_d~d/ln d. This asymptotic is for all integer d, not just a sparse
subsequence. Section 5 gives a_*(d)>=T_d at every d>=2. Combined with the
verified literature upper bound a_*(d)<=d, a logarithmic gap remains.

An independent budget proof is useful for reuse. Set tau=alpha^(1/d)-1 and
y_i=n_i x_i. N_i>0 gives y_i<1/tau; Q_i>0 gives t_i>tau. Then

    x_i n_i N_i/M_i <1/[(alpha-1)tau],
    Q_i/(t_i P_i)  <1/[(alpha-1)tau].

Thus G>1 requires (alpha-1)(alpha^(1/d)-1)<1, which implies
(alpha-1)ln alpha<d. This confines the certificate to leading scale
(1+o(1))d/ln d, consistent with the exact envelope. It is not a full-model
existence result.

For d=1, f_1(R)=1 identically and no alpha>1 certificate is possible. For
d=0 the stated positive-degree input class is empty. Even rings do not supply
the parity step; the alternating all-anti profile evades this coverage proof.
Neither failing local tests nor a tool failure implies equilibrium existence.

## 7. Evidence, comparison, and remaining obligations

The published nonexistence baseline is Theorem 1 / formula (3) of
[Christodoulou et al., arXiv:2002.07466v3](https://arxiv.org/html/2002.07466v3),
explicitly exhibiting Omega(sqrt(d)/ln d). The recovered R3 proof of that
same formula's sharp envelope is (2/sqrt(e))sqrt(d ln ln d)/ln d. Both are
strictly smaller in order than T_d~d/ln d. The source-envelope improvement
is a separate joint dependency for comparison with its exact supremum; this
new lower proof does not depend on it.

The upper d and the finer finite-degree potential factor are checked in
[Caragiannis--Fanelli, arXiv:1902.07173v5, Theorem 2](https://arxiv.org/html/1902.07173v5).
The literature audit records later sources and scope; the search did not
discover a stronger same-model growing lower bound, but does not certify
global firstness. Arbitrary nondecreasing-cost step lower bounds, bounded
weight-ratio algorithms, and price-of-anarchy/stability bounds have different
quantifiers and cannot be substituted as this nonexistence baseline.

Reproducible exact tests are in `verify.py` / `verification.json`; clean
strategy reconstruction is in `../odd_ring_independent/verify_literal.py`.
Independent reviews are `../odd_ring_independent/REVIEW.md`, its separate
`EXACT_ENVELOPE_REVIEW.md`, and `../odd_ring_parameters/exact_envelope_review.md`.
Tests check rational inequalities and full states of small actual games;
they do not enumerate the huge growing family and do not replace this proof.

WC-TARGET remains OPEN: the next obligation is a full-class O(d/ln d)
existence bound or a stronger all-state mechanism exceeding this certificate
envelope. Raising ring length or tuning its monomial degrees cannot bypass
the proved positive-test-system envelope. Resources involving many players,
extreme rational scales and a low-total-weight large cohort are the present
amplification mechanism; minimum potential-user density alone was already
shown nonrestrictive by the separate padding theorem.

## 8. Nonnegative mixtures do not enlarge the certificate envelope

**WC-R3-ODD-RING-POLYNOMIAL-ENVELOPE-v1** is a new claim with a broader input
class, not an unannounced change of the monomial claims above. Let d>=2,
alpha>1, and retain the odd-ring strategies and common cohort weights. At
each group independently choose nonzero polynomials F_i,G_i of degree at most
d with nonnegative real coefficients. The two A action copies have shape F_i;
all B_ij action copies within group i have shape G_i. Costs are a_i F_i and
b_i G_i, with positive group amplitudes. No action-specific or clone-specific
shape extension is included.

Use the actual differences, without mixing their dimensions with section 1:

    N_i=F_i(u_i+v_i)-alpha F_i(n_i v_i),
    M_i=alpha F_i(u_i+n_i v_i)-F_i(u_i),
    P_i=alpha G_i(u_(i+1)+v_i)-G_i(v_i),
    Q_i=G_i(u_(i+1)+v_i)-alpha G_i(u_(i+1)).

The local tests are a_i N_i>b_i P_i and
n_(i-1)b_(i-1)Q_(i-1)>a_i M_i. The same monotone all-state proof and positive
coefficient-cycle proof apply. Some choice of shapes and parameters satisfies
this strict system if and only if alpha<T_d. In particular, for every fixed
choice satisfying the system, alpha<T_d is necessary. This does not assert
that every prescribed choice is feasible below T_d.

For necessity, write F_i(z)=sum c_k z^k and suppress i. M_k=alpha(1+n x)^k-1
is positive for every 0<=k<=d, including constants. Thus

    x n N/M=sum_k [c_k u^k M_k/M] F_(k,n)(x).

This is an exact convex combination: its displayed weights are nonnegative
and sum to one. Likewise write G_i(z)=sum e_k z^k, with
P_k=alpha(1+t)^k-t^k>0. Then

    Q/(tP)=sum_k [e_k u_(i+1)^k P_k/P] F_(k,1)(1/t).

Every individual monomial factor is <=1 at alpha>=T_d by section 4.
For k=0 the factors are respectively -n x and -1/t, also <=1. Individual
N_k,Q_k can be negative; that does not invalidate a convex upper bound.
The total N,Q must be positive in a certificate, so the normalized totals
are positive. Multiplying over i and using product x_i=product t_i gives
G<=1, contradicting strict feasibility. Sufficiency uses section 5's
degree-d monomial subclass.

Nonzero nonnegative shapes have M,P>0 at positive arguments. A zero F_i
cannot pass its strict light test; a zero G_i cannot pass the following hub
test. Pure constants have N<0 or Q<0; constants inside mixtures remain
covered. No 0/0 is evaluated. The same necessary argument at d=1 excludes
all alpha>1, since f_1=1. There is no division claim at alpha=1.

Dependencies are the exact certificate proof and scalar envelope, with the
new convex identities just proved. Independent attack and exact mixed-degree
checks are in `../odd_ring_parameters/polynomial_envelope_review.md` and its
companion Python/JSON. Truth: complete stated-scope proof; Value: closes the
mixed-polynomial tuning route; Novelty: unverified; Mechanism: positive
denominator-weighted combinations; Ambition: mechanism boundary, not a stronger
full-class lower or any full-class existence upper.

The actual-topology obligation, subsequently closed for this exact class in section 10, was: when these uniform tests
fail, must there be a real state with no alpha deviation? An all-anti state with
one equal hub edge has only one possibly improving hub, but some anti lights
can still prefer alignment. Partly aligned cohorts and these reverse light
deviations must be controlled; neither this proof nor infeasibility supplies
the needed state. Section 10 now supplies that state for every alpha>=T_d without assuming uniform forcing.

## 9. An actual-topology existence bound for singleton cohorts

**WC-R3-ODD-RING-SINGLETON-UPPER-v1.** For every odd m>=3, d>=2, and every
game of section 8 with n_i=1 at all groups, arbitrary positive real weights
and nonnegative degree-at-most-d shapes (zero fees now permitted), there is
a min{2,T_d}-PNE. In particular a T_d-PNE exists among the 2m single-conflict
states modulo global exchange of action bits. The min{2,T_d} equilibrium
need not be claimed to lie in that smaller set when 2<T_d. No sharpness or
general-cohort claim is made.

The internally derived [full proof](../../../reviews/weighted_congestion/odd_ring_parameters/SINGLETON_NOTE.md)
was then independently reconstructed by the root reviewer. Put the resource
positions around a cycle as A_0,B_0,A_1,B_1,... . An A position is conflicted
when its hub/light bits agree; a B position when light/next-hub bits differ.
Odd m makes a conflict-free assignment impossible. For any one chosen conflict
position, the other requirements uniquely fix the profile up to a global bit
flip. Costs are invariant under that flip because the resource copies have
identical fees. Thus there are 2m distinct single-conflict profiles modulo it.

Only the two players incident to the conflict can strictly improve. A different
player's flip turns both its solo loads into shared loads and cannot decrease
either latency. Each incident flip moves the conflict to an adjacent position.
The two directions on such an edge reverse the same player's before/after costs;
at alpha>=1 at most one direction strictly improves, even with zero costs.
If every single-conflict state had a strict alpha move, this 2m-vertex cycle
would have at least 2m arcs but at most one arc per edge. All its edges must
therefore be coherently oriented. Forward orientation supplies exactly the
two strict local tests, with n_i=1. At alpha>=T_d section 8 excludes this.

The reverse orientation must also be checked. Reverse the ring's indexing,
j corresponding to old i=-j modulo m, and exchange roles H'_j=L_i,L'_j=H_i,
weights u'_j=v_i,v'_j=u_i. Keep action bits, set A'_j^b=A_i^b and
B'_j^b=B_(i-1)^(1-b). The incoming resource of the new hub and the outgoing
resource of the new light are exactly their old resources. F'_j=F_i and
G'_j=G_(i-1) preserve nonnegative shapes and n'=1. New forward orientation
is the old reverse orientation, again impossible at alpha>=T_d. Zero shapes
cannot rescue a strict coherent cycle: its corresponding solo-to-shared move
cannot improve. Some single-conflict state is therefore an alpha-PNE, including
the weak endpoint alpha=T_d.

The factor 2 comes from a separate elementary support bound. In this subclass
every resource has at most two potential users. Take a global minimum of
Psi=sum_i C_i over all pure states. For a move of i, removing resources cannot
increase other users' costs; adding a resource creates at most one other cost
increase, at most the deviator's new latency there. Shared unchanged resources
retain the same loads. If C_common is the deviator's unchanged resource cost,

    Delta Psi <= 2 C_i(new)-C_i(old)-C_common.

Thus a strict factor-2 improvement would contradict minimality. This proves
2-PNE for arbitrary nonnegative nondecreasing fees with support at most two.
Combining the two independent existence bounds gives min{2,T_d}.

This reduces actual equilibrium existence to a small defect graph only for
n_i=1. When a common A resource carries multiple light players, a move can
alter a partially aligned cohort and this graph is no longer a simple cycle.
The general actual-topology gap remains. Truth: complete restricted existence
proof; Value: identifies where the single-conflict representation ceases to
apply; Novelty: unassessed; Mechanism: cycle arc counting and role reversal;
Ambition: subclass only. The companion exact graph audit checks all the stated
structural identities in small cases, including zero resources; it tests a
safe alpha=d and does not numerically pretend to verify the irrational endpoint.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。

## 10. 一般群组奇环实际阈值与正测试包络一致

ID/version：`WC-ODD-RING-GENERAL-COHORT-ACTUAL-UPPER-v2`。

版本关系：未入规范层的v1草案只给max{2,T_d}；本v2改变结论，使用奇数群组中央双标签和反向标量界得到T_d。旧有证书、下界和单成员Claim的身份均不改变。独立审查记录各冻结版本的hash及增强覆盖，不以旧版审查自动升级。

状态：完整一般子类证明；已独立重构并攻击，规范文件差异复核见配套审查。本文只处理下述奇环拓扑，不解决 WC-TARGET 全类命题。无外部定理导入，标量包络调用当前仓库已审的非负多项式正测试包络。

### 10.1 精确命题与范围

对每个整数 d≥2、奇整数 m≥3、正整数 n_i≥1、正实数 u_i,v_i，以及任意非负系数次数≤d 多项式 F_i,G_i（均允许零多项式），考虑以下有限游戏。指标模 m。Hub H_i 权 u_i，cohort i 有 n_i 名同权 v_i 的 light。互异资源为 A_i^b、B_ij^b，b∈{0,1}；两个 A 副本费用均为 F_i，同群全部 B 副本费用均为 G_i。Hub 的动作 h 使用 A_i^h 和每个 B_(i−1),j^h；light ij 的动作 l 使用 A_i^l 和 B_ij^(1−l)。成本不乘权重，真实偏离按 MODEL 重新负载。

定义当前奇环包络

    f_d(R) = [R(1+R)^d+1]/[(1+R)^d+R^(d+1)],
    T_d = sup_{R>1} f_d(R),
    A_d = T_d.

d≥2时第4节已证T_d>1，因此下面取α≥T_d时始终α>1。

**结论：每个上述游戏存在 T_d-PNE。** 更一般地每个 α≥T_d 均有 α-PNE。结合现有每个α<T_d的该拓扑严格反例，其实际拓扑最坏阈值恰为T_d（指有限实例最优倍率的上确界，不声称某个单独实例达到）。由于 T_d<d/ln d（第10.8节自足验证），此拓扑全体有 (d/ln d)-PNE，且其最坏阈值渐近为 d/ln d。没有声称所有实例最优因子相同，或全类有此上界。

对象、定义域、量词、假设、范围、结论均如本节；依赖为非负多项式单调性、有限整数稳定区间、本文单缺陷比较及已证正测试包络。Truth 为所写子类内部证明；Value 是闭合一般cohort实际拓扑缺口；Novelty 未认证；Mechanism 单缺陷取向与消去成对light；Ambition 仍为结构子类。

### 10.2 从真实资源导出的精确计数

令 k_i∈{0,…,n_i} 是与 H_i 同位的 light 数，z_i=h_i xor h_(i+1)。二进制 hub 配置恰要求 Σ_i z_i 偶；反之每个偶 parity z 有两个互补 hub 配置，它们成本相同。设

    q_i=G_i(v_i), V_i=G_i(v_i+u_(i+1)), D_i=V_i−q_i≥0.

固定 k_i,z_i，有 aligned light 时其当前和偏离成本为

    F_i(u_i+k_i v_i)+q_i+z_iD_i,
    F_i((n_i−k_i+1)v_i)+q_i+(1−z_i)D_i.

有 anti light 时其当前和偏离成本为

    F_i((n_i−k_i)v_i)+q_i+(1−z_i)D_i,
    F_i(u_i+(k_i+1)v_i)+q_i+z_iD_i.

因此固定 z 的 light α稳定计数集 I_i(z) 恰由这两式各自的 current≤α·deviation（在相应类型非空时）定义。

另记 W_i=G_i(u_(i+1))，Δ_i=V_i−W_i≥0，

    r_i=z_i k_i+(1−z_i)(n_i−k_i).

Hub i 当前及偏离成本恰为

    F_i(u_i+k_i v_i)+n_(i−1)W_(i−1)+r_(i−1)Δ_(i−1),
    F_i(u_i+(n_i−k_i)v_i)+n_(i−1)W_(i−1)+(n_(i−1)−r_(i−1))Δ_(i−1).

零费用全用乘法不等式，无成本商。

### 10.3 Light稳定区间与公共z=1代表

以下仅需 α≥1 和非负非减费用。省指标，写

    A_z(k)=F(u+kv)+q+zD,
    B_z(k)=F((n−k+1)v)+q+(1−z)D,  1≤k≤n.

A_z(k) 非减，B_z(k) 非增。计数 k 的 aligned 稳定条件是 A_z(k)≤αB_z(k)（k>0），anti 稳定条件是 B_z(k+1)≤αA_z(k+1)（k<n）。前者的可行集向下闭，后者向上闭。取最小满足 anti 条件的 k（n 自动满足），若 k>0，前一计数 anti 不稳给 B_z(k)>αA_z(k)，所以 A_z(k)<B_z(k)/α≤αB_z(k)。因此 I(z) 非空且是整数区间 [a_z,b_z]，含零费用情况。

z 从0变1时 anti 当前费用下降、偏离费用上升，所以最小稳定计数 a_1≤a_0。还总有 a_1≤floor(n/2)：在 k=floor(n/2) 时 n−k≤k+1，anti 在 α=1 已稳定。以后固定

    c_i=a_i(1)≤floor(n_i/2).

此 c_i 是 z_i=1 的 α-stable 计数。

若 I_i(0)=[a_i,b_i]，则 c_i≤a_i≤b_i。若 a_i>0，计数 a_i−1 的 aligned 条件由 a_i 的条件和单调性保证（a_i−1=0 时无需该条件），故它不稳只能由于 anti 严格改善：

    F_i((n_i−a_i+1)v_i)+V_i
       >α[F_i(u_i+a_i v_i)+q_i].                       (R-boundary)

若 a_i>n_i/2，记 r_i=n_i−a_i。把上式与单调性比较，z=1 在 k=r_i+1 的 aligned 条件严格失败：

    F_i(u_i+(r_i+1)v_i)+V_i
       >α[F_i(a_i v_i)+q_i].

因此 c_i≤r_i。若 b_i<n_i，类似地 b_i+1 只能因 aligned 严格改善而不稳：

    F_i(u_i+(b_i+1)v_i)+q_i
       >α[F_i((n_i−b_i)v_i)+V_i].                     (L-boundary)

### 10.4 单缺陷状态、偶中心与奇数群组双标签

对每个 i，让 z_i=0，其他 z_j=1。m 奇使 Σz=m−1 偶，故该状态合法。在非缺陷群 j≠i 取 k_j=c_j，在缺陷群选任意 k_i∈I_i(0)。全部light均 α稳定。

若群 j 的 z_j=1 且 k_j≤n_j/2，它使其下一hub收到的 shared B 数≤n_j/2；若自身 k_j≤n_j/2，则该hub的主资源当前费用≤偏离费用。因此在上述单缺陷状态，除 H_i 与 H_(i+1) 外全部hub逐主/侧项不增，exact稳定。缺陷 k_i≤n_i/2 时 H_i 也exact稳定，仅 H_(i+1) 可能不稳；k_i≥n_i/2 时 H_(i+1) 的incoming侧不增，其自身c_(i+1)≤half，所以仅 H_i 可能不稳。

若 n_i 偶且 n_i/2∈I_i(0)，两端均exact稳定，得到 α-PNE。

以下反设没有 α-PNE；取α≥T_d>1。每个 I_i(0)=[a_i,b_i] 作以下分类：

- 唯一 L：b_i<n_i/2，缺陷用真正最大端点 k_i=b_i，仅下一hub可能不稳；第10.3节给c_i≤b_i。
- 唯一 R：a_i>n_i/2，缺陷用真正最小端点 k_i=a_i，仅自身hub可能不稳；令r_i=n_i−a_i，第10.3节给c_i≤r_i。
- flexible：n_i奇，I_i(0)同时含floor(n_i/2)与ceil(n_i/2)。此群可任选L代表b=floor(n_i/2)或R代表a=ceil(n_i/2)，且c_i≤floor(n_i/2)=b=n_i−a，所以两种mixed比较的所需不等式均成立。代表可能不是真正端点，故此时不使用strict边界。

分类穷尽：稳定集合为整数区间；偶n跨中心会包含已处理的精确中心；奇n跨中心必同时包含相邻两个中央整数。singleton [0,1] 正是flexible，且c=0。这套处理对所有奇n一样，不使用(n+1)/(n−1)或任何实际成本商。

### 10.5 相邻L→R不可能：同一hub的双向严格改善矛盾

假设群 i 可取 L代表 b，群 i+1 可取 R代表 a。令 S 是缺陷 i、k_i=b 的单缺陷状态，T 是缺陷 i+1、k_(i+1)=a 的单缺陷状态。其余群均取固定 c。没有 α-PNE 迫使同一个 H=H_(i+1) 在 S 和 T 都严格 α改善。

写 n=n_i、c=c_i、v=v_(i+1)、u=u_(i+1)、N=n_(i+1)、C=c_(i+1)，以及 g0=G_i(u)、g1=G_i(u+v_i)。四个成本恰为

    H(S)       =F_(i+1)(u+C v)+(n−b)g1+b g0,
    H(Sflip)   =F_(i+1)(u+(N−C)v)+b g1+(n−b)g0,
    H(T)       =F_(i+1)(u+a v)+c g1+(n−c)g0,
    H(Tflip)   =F_(i+1)(u+(N−a)v)+(n−c)g1+c g0.

c≤b、C≤N−a、g1≥g0和 F 单调给

    H(T)≤H(Sflip),       H(S)≤H(Tflip).

若两状态都严格 α改善，则 H(S)>αH(T) 且 H(T)>αH(S)，与 α≥1及非负成本矛盾（也涵盖零成本）。

因此环上不可能有相邻 L→R。对每群任选一个可用标签，有限循环二字母串若两标签均出现必有 L→R，故只能全L或全R。若有flexible，先任意选标签所得串须常值，再仅翻转该flexible标签便成为非恒定串（m≥3），仍产生禁转折。因此没有flexible；全部群具有同一个唯一标签。

### 10.6 全L被现有非负多项式测试包络排除

每群都有真正最大稳定端点 b_i<n_i/2，并记

    n'_i=n_i−2b_i≥1,
    F'_i(x)=F_i(x+b_i v_i).

平移量非负，所以 F'_i 仍为次数≤d非负系数多项式。由 (L-boundary) 得

    F'_i(u_i+v_i)+G_i(v_i)
       >α[F'_i(n'_i v_i)+G_i(v_i+u_(i+1))].          (L')

缺陷 i 的状态只能由 H_(i+1) 严格改善。其自身 c_(i+1)≤b_(i+1)，可增大当前主费用到 F'_(i+1)(u_(i+1))，减小偏离主费用到 F'_(i+1)(u_(i+1)+n'_(i+1)v_(i+1))，仍保留strict。incoming B 两边均含非负共同项 b_i[G_i(u_(i+1))+G_i(u_(i+1)+v_i)]，α≥1允许删除，得到

    F'_(i+1)(u_(i+1))+n'_iG_i(u_(i+1)+v_i)
       >α[F'_(i+1)(u_(i+1)+n'_(i+1)v_(i+1))
             +n'_iG_i(u_(i+1))].                    (H')

(L'),(H')正是 `odd_ring/cohort_lower_bound_and_envelope.md`第8节测试（各amplitude取1），拥有奇数m、整数n'≥1、正实u,v、同费副本、非负degree≤d形状和strict α>1条件。F'≡0不能满足L'，G≡0不能满足随后H'，故该测试要求的非零形状也已推得。既有 `WC-R3-ODD-RING-POLYNOMIAL-ENVELOPE-v1` 证明其可行必有 α<T_d，与 α≥T_d 矛盾。没有把原游戏测试不可行直接当成PNE；是先由假设所有真实单缺陷态不稳重新导出新缩减游戏的完整strict测试。

### 10.7 全R也被相同标量包络排除

令 a_i=min I_i(0)>n_i/2、r_i=n_i−a_i、n'_i=2a_i−n_i≥1，以及F'_i(x)=F_i(x+r_i v_i)。定义

    NF_i=F'_i(u_i+n'_i v_i)−αF'_i(u_i),
    MF_i=αF'_i(u_i+n'_i v_i)−F'_i(v_i),
    NG_i=G_i(v_i+u_(i+1))−αG_i(v_i),
    MG_i=αG_i(v_i+u_(i+1))−G_i(u_(i+1)).

(R-boundary)给NG_i>MF_i。缺陷 i 只能由H_i严格改善；其前群的z=1代表c_(i−1)≤r_(i−1)。把当前side shared数从c增到r、把偏离shared数从n−c减到n−r后保留strict，再删除两边共同的非负成对side项，给

    NF_i>n'_(i−1)MG_(i−1).                           (RH)

α>1及单调性给MF_i,MG_i≥0。F'_i≡0会令NF_i=0，矛盾RH；G_i≡0会令NG_i=0，矛盾NG_i>MF_i。因此F'_i,G_i非零，在正输入严格正，故MF_i,MG_i>0，进而NF_i,NG_i>0。将两组strict测试相乘可得

    product_i [NF_i NG_i/(n'_i MF_i MG_i)]>1.          (RP)

当前奇环标量包络给α≥T_d时任意非负次数≤d多项式P及正x,y满足

    x[P(x+y)−αP(x)]≤y[αP(x+y)−P(y)].                (S)

为自足核对：对单项式P(t)=t^k，除以y^(k+1)后、R=x/y，(S)恰等价于α≥f_k(R)。当R≤1，二项式系数逐项比较给f_k(R)≤1；当R>1，f_k(R)随k非减且f_k(R)≤T_d。k=0亦给f_0=1；逐项非负相加即得(S)。

对F'_i用x=u_i、y=n'_iv_i，再用F'_i(v_i)≤F'_i(n'_iv_i)，得到

    u_i NF_i
      ≤ n'_iv_i[αF'_i(u_i+n'_iv_i)−F'_i(n'_iv_i)]
      ≤ n'_iv_i MF_i,
    NF_i/MF_i≤n'_iv_i/u_i.

对G_i用x=v_i、y=u_(i+1)，得到

    NG_i/MG_i≤u_(i+1)/v_i.

将这些正数界相乘，(RP)左边≤product_i u_(i+1)/u_i=1，矛盾。

第10.4至10.7节排除反设，证明α≥T_d存在α-PNE。所有代表来自有限集合，未要求连续极小值；所有反设用strict改善，与弱α-PNE端点完全相容。

### 10.8 显式 (d/ln d) 子类上界

既有标量证明给

    T_d≤H_d+1/(2^d+1),
    H_d=d/[(d+1)d^(1/(d+1))−d].

e^x≥1+x给 H_d≤d/(1+ln d)。又 ln d≤d−1、1+ln d≤d，故

    d/[ln d(1+ln d)]≥1/(d−1)>1/(2^d+1).

所以 T_d<d/ln d，因此此拓扑可核验的绝对常数为 C=1、d0=2。**这是上述拓扑结论，不是原题全类C=1结论。**

### 10.9 边界、潜在反驳与证据合同

- 允许任意正实u,v，n任意增长，F/G常数、零和混合次数；正文始终只用非负单调性、非负平移和包络已覆盖的形状。
- z=1代表与其他群无关，因为各light只见自身hub与next hub；cohort同权、同side费用承重。换异权light、同B多hub、不同动作费用、本环外资源后不能直接使用。
- 单缺陷仅m奇时成立；偶m取全z1与每群α=1稳定c≤half即给exactPNE，但这不是本文ID的必要部分。
- 任意奇n跨中心稳定区间（含singleton [0,1]）统一按双标签处理，绝不套用中心侧成本比例或成本商。
- 当前证明独立于文献源拓扑还原；后者只启发成对light平移，未未经核查调用其不同模型。
- 需要独立审查者重点攻击：I(z)非空的零成本边界、c≤r推导、mixed四成本的side方向、奇n跨中心双标签与flex环取向、全L平移形状与删除共同项、全R的strict正性与标量(S)适用。

审查：[先自主重构与冻结攻击](../../../reviews/weighted_congestion/odd_ring_parameters/general_cohort_actual_upper_review.md)。

可复现命令（在仓库根运行，均默认输出stdout，不覆盖冻结结果）：

```bash
python3 tests/audits/weighted_congestion/odd_ring_parameters/check_general_cohort_actual_upper.py
python3 tests/audits/weighted_congestion/odd_ring_parameters/independent_general_cohort_actual_upper.py
```

代码分别为[作者逐资源审计](../../../../tests/audits/weighted_congestion/odd_ring_parameters/check_general_cohort_actual_upper.py)和[独立资源策略重算](../../../../tests/audits/weighted_congestion/odd_ring_parameters/independent_general_cohort_actual_upper.py)，输入内嵌、seed及解释器/源码hash记录于输出。[作者冻结记录](../../../../evidence/runs/weighted_congestion/odd_ring_parameters/general_cohort_actual_upper.json)与[独立冻结记录](../../../../evidence/runs/weighted_congestion/odd_ring_parameters/independent_general_cohort_actual_upper.json)说明实际有限覆盖。两代码不互相导入；全部算术采用Fraction，未用浮点决定稳定性或strict边界。作者输入另含正/反向严格非存在小例，检验两种缩减分支，并不声称这些小例给增长下界。一般实参数证明来自上文而非有限枚举。

**证明给出的有限选态过程。** 固定α≥T_d，算每群I_i(0)=[a_i,b_i]与c_i=min I_i(1)。对于每个缺陷i，若a_i≤floor(n_i/2)，列出k_i=min{b_i,floor(n_i/2)}；若b_i≥ceil(n_i/2)，列出k_i=max{a_i,ceil(n_i/2)}，其余k_j=c_j。重复者只列一次，至多2m个计数状态；按固定次序令每群前k_j名light aligned，即给真实合法状态。上面的反设证明表明其中至少一个是α-PNE，故可直接逐状态验证后选择，不必枚举所有hub配置与cohort计数。没有声称任意实数输入的算法实现或位复杂度；有限池是所证存在机制的显式读取方式。

主目标仍为MODEL全类匹配上界判定；本定理只闭合同权cohort、同费副本奇环的实际阈值，不能将该拓扑当全类规范形。下一步若沿此族寻更强下界，必须改变cohort同权、动作副本费用或资源关联等承重合同，并重新证明全状态覆盖。
