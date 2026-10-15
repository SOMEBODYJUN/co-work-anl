# Full symmetric two-column topology: exact high-factor reduction

Claim ID: **WC-R3-FULL-TOPOLOGY-REDUCTION v3**.

Version history: v1 required α≥2; v2 broadened the factor range to α≥φ
for every w>0; v3 broadens it further to α≥ρ=(1+√3)/2. The earlier
statements remain proved subcases. Here φ=(1+√5)/2, and ρ is the
positive root of 2α(α−1)=1.

## Exact identity

Objects/domain: one weight-1 player and n≥1 players of the same weight w>0;
resources a_0,…,a_n,b_0,…,b_n. The heavy player chooses one entire column;
light player i chooses {a_0,b_i} or {b_0,a_i}. Main resources have the same
nonnegative-coefficient polynomial F, side resources the same such polynomial G,
each of degree at most the integer d≥1. Costs and α-PNE use MODEL.md.

Quantifiers/conclusion: for every such game and every real α≥ρ, if the game
has no α-PNE, there are an integer n′≥1, a weight 0<w′≤1, an integer
1≤k≤d, and 0<β<1 such that the source two-test certificate

    1+n′β(1+w′)^d > α[(1+n′w′)^k+n′β],
    (1+w′)^k+β(w′)^d > α[(n′w′)^k+β(1+w′)^d]

holds. The resulting source game can differ from the input game. This is an
existential reduction, not a claim that their finite-instance thresholds agree.
The translation and coefficient-elimination steps both retain all w>0.
This corrects the earlier interpretation that φ required w≤1.

Scope: only this symmetric topology and identical light weights. No all-game
upper bound is implied. Dependencies: direct state computations, monotonicity,
binomial translation preserving nonnegative coefficients, and a convex chord
inequality proved below. The topology is the one in Christodoulou et al.,
[arXiv:2002.07466v3, §3, Theorem 1 and (3)](https://arxiv.org/html/2002.07466v3).
The reduction is a team reconstruction of the mechanism discussed on the board;
global novelty is not asserted.

Status: complete proof; independent attack and exact finite checks are recorded
in `../topology_attack/` and `results.json` when complete. External review and
global priority are not recorded. Truth, value, novelty, mechanism, ambition:
the stated reduction has a general proof; it closes a restricted search space;
novelty is unassessed; the mechanism is a stable interval followed by coefficient
elimination; the universal target remains open.

## 1. All states and the stable interval

Fix the heavy player's column A and let m∈{0,…,n} light players use a_0.
Set u=G(1), v=G(1+w), z=G(w). Its current cost is

    h_m=F(1+mw)+(n−m)v+mu.

After its switch the cost is h_(n−m). A same-column light player's current
and switched costs are F(1+mw)+z and F((n−m+1)w)+v. A different-column
light player's current and switched costs are F((n−m)w)+v and
F(1+(m+1)w)+z. This lists all deviations; complement symmetry covers
the other heavy-player column.

If F≡0, m=n is α-PNE for every α≥1: light current cost z≤v, heavy current
cost nu≤nv. Thus nonexistence implies F≢0. Every F at a positive input is
then positive, so all quotients below have positive denominators even if G≡0.

For 1≤m≤n put

    L_m=[F(1+mw)+z]/[F((n−m+1)w)+v].

This sequence is nondecreasing. Light players are all α-stable at m precisely
when L_m≤α (if m>0) and L_(m+1)≥1/α (if m<n). These conditions form a
nonempty integer interval I=[a,b]: choose the smallest m with
L_(m+1)≥1/α, or m=n if there is none; its preceding L_m<1/α≤α when m>0.

At every m∈I nonexistence forces h_m>αh_(n−m). The intervals I and n−I
cannot intersect: otherwise a pair m,n−m would require both reciprocal
strict inequalities. Consequently exactly one of 2b<n and 2a>n holds.

## 2. The left interval gives the two tests

Suppose 2b<n. Let n′=n−2b and F′(x)=F(x+bw). At m=b heavy instability is

    F′(1)+n′v+b(u+v) > α[F′(1+n′w)+n′u+b(u+v)].

Deleting the same nonnegative term b(u+v) from both sides preserves strict
improvement because α≥1. Since b is the last light-stable state, b+1≤n has
L_(b+1)>α. This is exactly

    F′(1+w)+z > α[F′(n′w)+v].

Thus the two polynomial tests hold for (n′,w,F′,G). Translation preserves
degree and nonnegative coefficients, including constant terms.

## 3. The right interval reduces or is bounded by ρ

Suppose 2a>n. Put r=n−a, n′=2a−n and F′(x)=F(x+rw). Define
A=F′(1), B=F′(1+n′w), C=F′(w). Heavy instability at m=a, after deleting
r(u+v), gives

    B+n′u > α(A+n′v).

Because a−1 is not light-stable, its only failed condition is L_a<1/α
(the condition L_(a−1)≤α still holds when present). Its different-column
light player therefore has

    C+v > α(B+z).

Here 0≤u≤v, C≤B, z≥0 and B>0. Hence

    B > n′(α−1)v,        v > (α−1)B.

They imply the preliminary bound n′(α−1)²<1, hence α<2. To reach the
stronger bound n′α(α−1)<1, split only on w. For w≤1 also C≤A, so
αB<A+v and B>αA+n′(α−1)v imply

    (α²−1)A < [1−αn′(α−1)]v,

which forces n′α(α−1)<1, since A>0 and α>1. For w≥1 instead z≥u. Since C≤B,
the light inequality gives v>(α−1)B+αu. Substitution into the heavy
inequality yields

    [1−αn′(α−1)]B > αA+n′(α²−1)u ≥ 0.

Since B>0 and A>0, this again forces n′α(α−1)<1. These two cases
include w=1 and cover every positive w. For α≥ρ, the inequality
forces n′=1. This residual right branch itself converts to the left
tests: set w̃=1/w, F̃(x)=F′(wx), G̃(x)=G(wx). Its heavy test is exactly
C+v>α(B+z), and its light test is exactly B+u>α(A+v). Thus every right
branch either has α<ρ or supplies the required polynomial two-test
certificate. No right-branch nonexistence has been discarded without proof.

## 4. Reduce polynomial tests to source parameters

Write n for n′ and F for F′ in this section. Assume the two strict tests
with arbitrary α>1. The second test and G(w)≤G(1+w) imply
F(1+w)>F(nw). Thus (n−1)w<1. If n≥2 then w<1. The only case w>1
is n=1: exchange the two players and rescale all weights by 1/w. The two
tests exchange places for

    w″=1/w, F″(x)=G(wx), G″(x)=F(wx).

This can be checked by substitution, so we may assume 0<w≤1.

Let E=(1+w)^d. For a nonzero G normalize its coefficients by G(1+w).
For degree j the normalized values at 1,w are

    U_j=(1+w)^(−j), Z_j=(w/(1+w))^j=U_j^p,
    p=log(w/(1+w))/log(1/(1+w))≥1.

The function U↦U^p is convex on [E^(−1),1]. Its endpoint chord lies
above every (U_j,Z_j). Replacing G by a nonnegative combination of
1 and x^d with the same values at 1 and 1+w can therefore only increase
G(w). Both tests remain strict. Deleting its constant coefficient increases
both strict margins by (α−1) times that coefficient (times n in the heavy
test). We obtain G(x)=βx^d with β>0: β=0 could not pass the heavy test.

The tests now read

    β > [αF(1+nw)−F(1)]/[n(E−α)],
    β < [F(1+w)−αF(nw)]/[αE−w^d].

The first numerator is positive, so E>α; the other denominator is also
positive. Eliminating β gives a strict linear functional of the coefficients
of F. Some monomial x^k has positive value for that functional. The constant
monomial has value

    (1−α)[n(E−α)+(αE−w^d)]<0,

so 1≤k≤d. With that monomial the displayed lower and upper endpoints
leave a nonempty interval for β. Its lower endpoint is positive and its
upper endpoint is less than 1: for 0<w≤1 and k≤d,

    (1+w)^k+w^d ≤ E+(nw)^k < α[E+(nw)^k].

Choosing any β in the open interval proves the claim.

## 5. Consequence for the entire topology

Let T_source(d) be the source formula-(3) supremum of the minimum of its two
certificate ratios, with positive w and the stated source parameter domain.
Let T_topology(d) be the supremum, over all games of the topology above,
of their finite-instance best α-PNE factor. The source tests cover all pure
states, so

    T_source(d) ≤ T_topology(d) ≤ max{ρ,T_source(d)}.

For the upper inequality, if a finite-instance factor were greater than that
maximum, choose a strictly intermediate α. The reduction produces a source
certificate strictly larger than α, contradicting the definition of the
supremum. Endpoints of suprema need not be attained. In particular,
T_topology(d)=T_source(d) whenever T_source(d)≥ρ. A sharp asymptotic for
the source certificate therefore also controls this whole symmetric topology;
it is still not an upper bound for the universal a_*(d).

## Evidence, objections and continuation

The companion verifier calculates costs from literal resource memberships,
including both heavy-player actions, and checks the interval and translation
interface with rational arithmetic. It also exercises polynomial reduction,
zero costs, w>1/player exchange, integer endpoints and strict boundaries.
Finite checks support the implementation only. The proof above carries the
general quantifiers. Independent reviewer objections and their resolutions
must be retained in the separate review file; a fatal objection blocks promotion.

Next action: build a nonsymmetric high-support topology or allow heterogeneous
light weights with full-state coverage. The present obstruction does not address
either case. Contributions: R3 main reconstructed the proof and implementation;
the independent R3 topology reviewer attacked the exact statement before seeing
the proof. Board discussions of 2026-10-14 are antecedent research, not a
priority certification.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
