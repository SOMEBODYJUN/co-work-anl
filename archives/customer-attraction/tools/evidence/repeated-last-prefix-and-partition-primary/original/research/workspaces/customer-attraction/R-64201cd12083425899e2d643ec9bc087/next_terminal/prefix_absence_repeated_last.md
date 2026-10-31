# Prefix absence strengthens the repeated final-theme reduction

Exact local identifier: **B2-REPEATED-LAST-ABSENCE-v1**.

Status: self-contained personal candidate result, 2026-10-21. Author proof
plus the root's independent algebraic reconstruction of the principal
inequality, polynomial condition, and uniform asymptotic expansion. This has
not been promoted to a shared repository claim or externally reviewed. It is
not a solution of unrestricted Q-CAG-HALF. All
statements concern the unchanged common-catalog, unit-customer, unit-player
model and every complete ordered-history pure SPE. The main gain is to retain
customers' absences from the actual prefix when taking a continuation-robust
deviation guarantee.

## 1. Independent review of the previous residual criterion

Fix an actual ordered SPE outcome of m players, final theme B, final-player
payoff u, and k actual copies of the customer set B. Set d=m-k, S=|B|,
V=W-S, and R=sum_{x in actual union outside B}1/(c_x+1).

At the last node, a strict catalog superset of B would be a strictly better
reply. Thus B is inclusion maximal, and counting actual sets containing B
is the same as counting customer-set copies of B. Distinct labels with the
same coverage count as copies.

Here is a self-contained proof of the last-node comparison. Let b_x be
the actual load before the last move and a_x the number of a fixed optimal
comparison tuple's m themes covering x. Customerwise,

    1_{a_x>0} <= (a_x+b_x)/(b_x+1).

For a_x>0 this follows from a_x>=1, and for a_x=0 the right side is
nonnegative. Summing, the a_x term is the sum of the m individual legal
last-player deviation payoffs, each at most u. Thus

    OPT_m <= m u+tau,  tau=sum_x b_x/(b_x+1).

On B we have b_x=c_x-1 and the tax is 1-1/c_x. Outside B but in the actual
union, b_x=c_x and the tax is 1-1/(c_x+1). Outside the actual union the tax
is zero. Therefore tau=W-u-R exactly. These two facts give

    OPT_m <= W+(m-1)u-R.

The previous proof used S in [ku,mu], V>=k(u-S/m), and R>=V/(d+1).
Consequently W+R is at least the minimum of an affine expression on that
S interval. Its relevant endpoint is

    k[1+(d+2)d/(m(d+1))]u.

Requiring it to be at least (m-1)u gives exactly

    m(2d+1) >= d^2(d+2).

This argument is correct, including u=0, m=1, d=0, and arbitrary off-path
history dependence. It is sufficient, not necessary. No general terminal
payment inequality is inferred: the earlier full-SPE certificate
`R-18e993ca519949aba29e030d3d7b15b3/terminal_balance/refined_failure.json`
has m=5, W=39, u=53/5, R=14/5, and (m-1)u-W-R=3/5>0.

## 2. The sharper actual-prefix deviation guarantee

For any fixed catalog theme T, let n_i(x) be the number of players before
actual node i whose actual themes do not cover x. If player i deviates to T,
each x in T has fixed past load (i-1)-n_i(x), and at most m-i+1 current or
future covering players. Therefore, regardless of the real continuation,

    u_i >= sum_{x in T} 1/(m-n_i(x)).                         (1)

SPE optimality compares against the original strategy's continuation at
the changed ordered history. Equation (1) does not freeze followers. It
holds simultaneously for every T, although adding such guarantees alone
does not encode off-path followers' optimality.

Specialize T=B and list the d non-B players in their actual relative order.
For a fixed x in B, suppose exactly r of those players cover x. Thus its
actual terminal load is t=k+r. At a non-B player covering x, the lower-bound
term in (1) is at least 1/m. At successive non-B players not covering x,
the terms are exactly 1/m,1/(m-1),...,1/(k+r+1). Their sum does not depend
on where the covering players occur. Hence, writing H_j=sum_{a=1}^j1/a,

    sum_{i: S_i != B} 1/(m-n_i(x))
       >= r/m + H_m-H_{k+r}.                                (2)

Equality in this scalar rearrangement is possible by putting all r covering
non-B players before all d-r missing non-B players. A direct adjacent-swap
argument gives the same minimum: moving a covering player before a missing
player decreases, or leaves unchanged, its own denominator term and leaves
the missing player's rank among missing players unchanged.

Let X_r count B customers of terminal load k+r. The non-B players' actual
profit on B is sum_r r X_r/(k+r); their total profit outside B is exactly V.
Summing (1), using (2), and subtracting that actual profit on B gives

    V >= sum_{r=0}^d X_r A_r,
    A_r = r/m + H_m-H_{k+r} - r/(k+r)
        = H_m-H_t - (t-k)(m-t)/(mt), t=k+r.                  (3)

Every A_r is nonnegative. Indeed H_m-H_t >= (m-t)/m, so
A_r >= k(m-t)/(mt). This also proves that (3) contains the previous
V>=k(u-S/m) bound customer by customer.

## 3. Harmonic sufficient criterion

Every outside-B customer is covered by at most d actual players, so
R>=V/(d+1). Put a=(d+2)/(d+1). From (3),

    W+R >= S+aV >= sum_r X_r(1+a A_r).

Since u=sum_r X_r/(k+r), define

    C_t = t+a[t(H_m-H_t)-(t-k)(m-t)/m],  k<=t<=m,
    gamma(m,k) = min_{k<=t<=m} C_t.                         (4)

Then the proved inequality is

    W+R >= gamma(m,k) u.                                   (5)

In particular,

    gamma(m,k) >= m-1  =>  OPT_m <= 2W.                     (6)

All coefficients are rational. No division by u is used. For d=0,
gamma=m. For m=1 the last-node comparison already gives OPT_1=W.

The old residual criterion implies (6). To see this directly, replace
H_m-H_t by (m-t)/m in (4). The resulting coefficient is

    t + a k(m-t)/m,

which is affine in t on [k,m], with endpoints
k[1+a d/m] and m. Thus whenever the old two endpoints are at least m-1,
every new C_t is at least m-1. The inclusion is strict, for example:

| m | old largest certified d | new certified d | new gamma |
|---|---:|---:|---:|
| 6 | 2 | 3 | 85/16 |
| 8 | 3 | 4 | 1233/175 |
| 12 | 4 | 5 | 265349/23760 |
| 20 | 5 | 7 | 27649297/1447040 |
| 50 | 9 | 12 | 4212909271547/85846896135 |
| 100 | 13 | 17 | 38598461531924449/389208642094272 |

The table does not establish monotonicity in d or the best possible
repeated-theme theorem. It records exact evaluations of (4). In particular
the new criterion still does not settle five players with k=1 or k=2.

## 4. A polynomial sufficient condition and the asymptotic threshold

There is a direct sufficient condition without harmonic numbers. Set

    N = 2m d(d+2)+(d+2)k-2m^2.

Then

    [max(N,0)]^2 <= 8m^2(d+1)(d+2)k                         (7)

implies (6). This condition can be weaker than evaluating all C_t.

Proof: write q=m-t, so 0<=q<=d. The termwise inequality
1/(m-j)>=1/m+j/m^2 gives

    H_m-H_t >= q/m+q(q-1)/(2m^2).

Since t>=k and q(q-1)>=0 for integral q,

    C_t >= m-Lq+Qq^2,
    L = a d/m+a k/(2m^2)-1/(d+1)
      = N/[2m^2(d+1)],
    Q = a k/(2m^2)>0.

Completing the square on q>=0 gives C_t>=m-(max(L,0))^2/(4Q).
Condition (7) is exactly (max(L,0))^2<=4Q, proving the claim.

For any fixed lambda with

    0<lambda<sqrt(2+sqrt(3)) = 1.931851652...,

condition (7), and therefore half coverage, holds eventually whenever
d/sqrt(m)->lambda. Indeed N/m^2 tends to 2(lambda^2-1), while the right
side of (7), divided by m^4, tends to 8lambda^2. The strict inequality is
equivalent, for lambda>1, to (lambda-1/lambda)^2<2. For lambda<=1 the
positive-part condition is immediate in the limit; equality lambda=1 also
has right-hand limit 8 and left-hand limit zero.

The constant also describes the asymptotic boundary of criterion (4)
itself, not merely a fit to numerical thresholds. If d/sqrt(m)->lambda>0,
uniformly for 0<=q<=d,

    C_{m-q}-m
       = q/(d+1)-a d q/m+a q(q-1)/(2m)+o(1).

To justify uniformity, expand
1/(m-j)=1/m+j/m^2+j^2/[m^2(m-j)]. The remainder in the harmonic sum is
O(d^3/[m^2(m-d)])=O(m^(-3/2)); multiplication by t leaves O(m^(-1/2)).
Writing q/sqrt(m)=eta makes the uniform limit

    eta/lambda-lambda eta+eta^2/2, 0<=eta<=lambda.

The integer eta grid becomes dense, so

    gamma(m,m-d)-m
       -> -1/2 [max(lambda-1/lambda,0)]^2.                 (8)

Thus lambda below sqrt(2+sqrt(3)) is eventually certified by (4), and lambda
above it eventually fails this particular sufficient criterion. At the
boundary, lower-order terms decide; no equality claim is made there.

## 5. Generalization and the remaining global obligation

Equation (1) is the reusable arbitrary-theme interface. For each actual
player i and every T it retains the full customer-specific absence count.
It may be combined across several themes, with independent nonnegative
multipliers. It still uses only a continuation-robust worst-load guarantee;
it does not compare the different followers' choices at true off-path nodes.
The existing rank-one strategy obstruction already warns that on-path
guarantees plus the actual last best response cannot resolve Q-CAG-HALF.

Separately, every length-(m-1) legal history h gives

    OPT_m <= E(h):=m BR(h)+tau(h),
    tau(h)=sum_x b_x(h)/(b_x(h)+1).

Consequently OPT_m<=E_*:=min_h E(h). Also
tau(h)=sum_{j<m}payoff(h_j against h)<= (m-1)BR(h), so
E_*<=(2m-1)theta_m. The possible bridge E_*<=2W(SPE) is an unproved
candidate. It is not implied by the preceding repeated-theme criterion.
The known n-theta aggregate counterexample does not by itself refute this
tax-sensitive envelope. No claim of novelty or independent general theorem
is made for this interface.

## 6. Audit

`prefix_absence_audit.py` independently enumerates all non-B covering/missing
patterns through m=12, checks the rearrangement lower bound, the exact
coefficient identity, containment of the old residual criterion, and the
polynomial sufficient condition through m=100. It writes a small JSON report
only when `--output` is supplied. The finite checks audit formulas; Sections
1–4 establish the universal statements analytically.
