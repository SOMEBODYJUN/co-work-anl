# Independent review of the maximum-theme root capacity cuts

2026-10-25. Internal independent mathematical and exact-arithmetic review of
`../five_structure/max_theme_root_capacity.md`. No external review, novelty
claim, five-player half theorem, or new SPE counterexample is asserted.

## Scope and conclusion

The reviewed argument is valid for the stated five-player complete-history pure
SPE model. The root reference topic must be a **global** maximum topic, and the
proof does choose that topic at the original root before following the original
strategy. It never replaces the actual root topic by a maximum topic in an
incentive inequality. All four displayed integer capacity rows are correct.

The stronger binary-tail dependency with outside coefficient `1999/1000` was
independently recomputed here from its thirteen submitted rational multipliers,
the raw actual/off-path terminal shares, and all six individually indexed
comparator pairs. No author audit or author coefficient routine was imported.
All 4096 raw client-membership states have a nonnegative exact residual; the
minimum is zero, with 19 compressed zero states. The already available original
dependency review separately establishes the legality of its optimizing nodes.

## Mathematical checks

Let the forced maximum topic have size K, its true root payoff be z, and the
actual root payoff be u. Original root IC gives z<=u. Every follower topic has
size at most K, regardless of ties. On a customer inside the forced topic, its
integer final load c is in {1,...,5}; the followers receive (c-1)/c there.
Consequently V1=K-z exactly, while outside coverage equals outside follower
profit V0. Counting follower memberships gives

    V0 <= 5K-sum_(x in T)c_x.

For every k in {1,2,3,4},

    c+k(k+1)/c-(2k+1)=(c-k)(c-k-1)/c>=0.

The sign uses integral c, not convex interpolation. Summing it proves all four
simultaneous bounds V0<=(4-2k)K+k(k+1)z.

For a customer in j>=1 of the optimal five indexed topics, averaging the five
four-topic complements gives outside contribution 4/5 when j=1 and 1 when
j>=2. Inside the forced topic the contribution is
`1-6/[5(j+1)]`, at least 2/5. Thus the same binary-tail budget pays the average
of those five legal comparators, and

    (4/5)OPT_5 <= (1999/1000)V0+(5/3)V1+(2/5)K.

The coefficient of z after substitution is positive for every k, so replacing
z by u is safe. Direct fraction arithmetic reproduces exactly

    1200OPT_5 <= 9097K+3497u,
    1200OPT_5 <= 3100K+15491u,
    1200OPT_5+2897K <= 33482u,
    600OPT_5+4447K <= 28735u.

Rows three and four can replace K on the left by the size of **any** catalogue
topic. The negative right-side K coefficients are the reason this replacement
is safe. No assumption that a represented topic is globally largest is needed.

Applying the same complement estimate at the actual root topic of size L uses
V0=W-L and V1=L-u exactly. It gives

    2400OPT_5 <= 5997W-5000u+203L.

Since the L coefficient is positive, L<=K gives the reviewed weaker global-K
version. All statements remain valid for K=0 by the direct zero-instance case.

## Scalar diagnostic

The submitted scalar point

    W=1, OPT_5=83705/36641,
    u=8897/73282, K=16741/36641

exactly satisfies the scalar rows. An explicit dual, using the actual-root
global-K inequality divided by 2400, the k=3 row divided by 1200, and OPT_5<=5K,
has respective nonnegative weights

    66964000/73245359,
    5000000/73245359,
    641/36641.

Their sum is one; both u and K coefficients cancel. The resulting bound is
`OPT_5<=(83705/36641)W`. This certifies only that stated scalar relaxation.
Its optimum above two is not a complete SPE.

## Reproduction

`audit_capacity_independent.py` reads only the submitted thirteen binary-tail
multipliers as certificate data. It independently checks their 4096 raw states,
the 20 integer-load factorizations, all 64 raw five-comparator complement
assignments, the four integer rows, and the scalar primal and explicit dual.
The exact successful output is `audit_capacity_independent.json`.
