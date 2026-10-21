# Orbit overlap gives an unrestricted fractional-price certificate

Research backup, 2026-10-21. Exact analytical result; not independently
reviewed. General Q-CAG-HALF remains OPEN. No external review or novelty
claim is made.

Version note: this file retains the original transitive-orbit statement
as version 1. The independently suggested stronger balanced-cell and
maximum-mass statement is version 2, recorded separately in
`balanced_partition_price_certificate.md`. The original statement follows
as its transitive-catalog corollary.

The object throughout is the exact common-catalog, unit-customer,
unit-provider CAG. The principal lemma is a statement about one terminal
profile and does not assume equilibrium. Its application below uses the
existing genuine-last-two-player price certificates, with the full-history
pure-SPE hypothesis retained.

## 1. Original transitive-catalog criterion

Suppose a finite group acts on the customers and on the q catalog themes,
preserves incidence, and is transitive on themes. Decompose the customers
into group orbits O. Every customer in an orbit O belongs to the same
number t_O of themes. Set p_O=t_O/q. Double counting and theme transitivity
give

    |T intersect O| = p_O |O|                    for every catalog theme T.

Fix an arbitrary terminal profile S_1,...,S_m and a provider i. Suppose
that on every orbit O,

    sum_(j != i) |S_i intersect S_j intersect O|
        <= (m-1) p_O^2 |O|.                    (OC)

Then, writing u_i for this provider's terminal utility, for every
nonnegative real theme-weight vector z with total weight tau,

    C(z) := sum_x min(1, sum_(T contains x) z_T)
        <= (tau+m-1) u_i.                      (1)

Consequently

    B(u_i) := sup_(z>=0) [C(z)-u_i sum_T z_T]
        <= (m-1) u_i.                          (2)

If i has minimum actual utility, then (2) yields

    B(min_j u_j) <= W-u_i < W                  when u_i>0,

and the non-strict inequality holds also when u_i=0. In particular, this
condition implies half coverage without any SPE assumption: give weight
one to an optimal m-theme portfolio in (1), to obtain

    OPT_m <= (2m-1)u_i <= (2-1/m)W <= 2W.

### Proof, including unrestricted tau

For each customer x in S_i intersect O, put

    L_x = sum_(j != i) 1_(x in S_j).

Cauchy-Schwarz, or Jensen for the convex function 1/(1+s), gives

    u_i(O)
      = sum_(x in S_i intersect O) 1/(1+L_x)
      >= |S_i intersect O| /
         [1 + sum_(j != i)|S_i intersect S_j intersect O| /
                    |S_i intersect O|]
      >= |O| p_O / [1+(m-1)p_O].               (3)

When p_O=0 both sides are zero and no division is used.

Average z under the incidence-preserving group. The function C is
concave in z and invariant under this group, so averaging cannot decrease
C and preserves tau. Theme transitivity makes the averaged vector
uniform: each theme has weight tau/q. Hence

    C(z) <= sum_O |O| min(1,tau p_O).          (4)

For every p in [0,1] and tau>=0,

    min(1,tau p) <= (tau+m-1) p/[1+(m-1)p].   (5)

If tau p<=1, clearing the positive denominator reduces (5) to
(m-1)tau p <= m-1. If tau p>=1, it reduces to 1<=tau p.
Thus (5) includes tau=0 and all real tau without a normalization or
integer-menu restriction. Sum (5), use (3), and obtain (1). Taking the
supremum gives (2). The implication for a minimum-utility provider uses
W>=m u_i and therefore (m-1)u_i<=W-u_i.

## 2. Two symmetric groups: every minority-group provider satisfies (OC)

There are two groups X,Y of k themes each, k>=2. The customer incidence
multiset is invariant under all permutations within each group and under
exchanging X and Y. The induced theme sets are required to be a valid
common catalog; duplicate labels do not enlarge the model.

Consider any terminal profile of m providers which uses distinct themes,
with r themes in X and m-r in Y. Necessarily r<=k and m-r<=k. Fix an X
provider, and suppose

    r <= (m+1)/2.                              (6)

Then (OC) holds for this provider, on every customer orbit. Thus (1)-(2)
hold for its payoff a, with no equilibrium or off-path policy assumption.

### Exact orbit calculation

An orbit consists of customers with a memberships in one group and b in
the other, together with the swapped type if a!=b. Here 0<=a,b<=k;
t=a+b and p=t/(2k). For a uniformly selected customer from this orbit,
the probability of membership in two specified distinct same-group themes
is

    rho_same = [a(a-1)+b(b-1)]/[2k(k-1)],

and the probability of membership in a specified cross-group pair is

    rho_cross = ab/k^2.

These formulas also cover a=b, where the swapped orbit is not counted
twice. They give

    rho_cross <= p^2,
    rho_same + rho_cross <= 2p^2.              (7)

The first is 4ab<=(a+b)^2. For the second, the exact difference is

    rho_same+rho_cross-2p^2
      = [(a-b)^2 - t(2k-t)]/[4k^2(k-1)] <= 0,

because (a-b)^2+t^2=2(a^2+b^2)<=2k(a+b)=2kt.

There are r-1 same-group opponents and m-r cross-group opponents. By
(6), m-2r+1>=0, and (7) gives

    (r-1)rho_same+(m-r)rho_cross
      = (r-1)(rho_same+rho_cross)
          +(m-2r+1)rho_cross
      <= (m-1)p^2.

Multiplying by |O| is precisely (OC). All customers in a given orbit
are actual unit customers; multiplicities only express invariance.

In particular, every provider in a strictly smaller group qualifies;
when the two selected group counts are equal, all providers qualify.

## 3. A complete-SPE consequence with one minority theme

Assume m>=3, k>=m-1, the two-group invariance above, and an arbitrary
full ordered-history pure SPE whose actual terminal profile uses one
theme from X and m-1 distinct themes from Y. The order of these choices
and all off-path actions/ties are arbitrary. Let a be the minority
provider's utility and b the common utility of the majority providers.
Then

    B(min(a,b)) <= W.                          (8)

Therefore this class satisfies 2W>=OPT_m.

If a<=b, the minority provider satisfies (6), so (2) gives
B(a)<=(m-1)a<=W-a. If b<a, at least one of the last two providers belongs
to Y, since there is only one minority provider. If the last provider is
in Y, the genuine-last-player certificate gives B(b)<=W-b. Otherwise
the penultimate provider is in Y, and the genuine-penultimate certificate
gives B(b)<=W-kappa_m b<=W, where

    kappa_m=(m+1)/[2(m-1)]>0.

These are existing endpoint theorems, not a claim that the terminal
profile is a static Nash equilibrium. Their proof and precise defect
term are in
`../parent_tail/penultimate_price_defect.md` of workspace
R-e5d83af532dc495c966f99cf70cda2a2. If the minority provider moves first,
the last provider is in Y and both cases give the stronger
B(min(a,b))<=W-min(a,b).

No assertion b>=a is needed for this arbitrary-SPE consequence. Such an
ordering of the two payoffs would be false for general invariant customer
multisets. The fixed full-history policy in which provider 2 switches
groups and every later provider chooses a fresh theme from provider 2's
group is one special case, but it is not an assumption of (8).

## 4. Boundary and remaining gap

The incidence symmetry and orbit overlap condition carry the proof.
Neither follows for a general common catalog. Repeated actual themes are
also not covered by the two-group calculation: their pair-intersection
probability is p rather than rho_same. The unrestricted (1) itself does
allow repetitions when the independently stated (OC) is valid.

When a group has more than (m+1)/2 selected providers, (OC) can fail.
Customers interested in all of that group and none of the other group
already show this: rho_same=1/2, rho_cross=0, and p=1/2. Thus this
criterion does not simply apply to every minimum provider in an arbitrary
two-group profile, and it does not close general Q-CAG-HALF.

The numerical discovery script in scratch
`/workspace/scratch/255f7bc2eb33/b_charging/two_group_price_probe.py`
independently builds all repeated-prefix constraints for the fixed
second-group policy and checks m=3,...,8. It is not needed by this proof,
and its numerical cone includes degenerate duplicate-label boundary
points. No finite optimization result is used to establish (1)-(8).
