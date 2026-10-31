# Two automorphic images cover every benchmark with bounded support

Research backup, 2026-10-21. Mechanism proposed by the parent researcher;
the construction below spells out its exact support and repetition scope.
This is a deterministic coverage statement, independent of incentives.
It does not resolve general Q-CAG-HALF.

## General image-cover principle

Let a finite group act on customers and themes preserving incidence and
unit-customer multiplicities. Let A be the support of an actual action
profile, and W its coverage. Suppose that for every benchmark support K
in a specified class there exist group elements g_1,...,g_r,h such that

    h(K) is contained in g_1(A) union ... union g_r(A).

Every image g_j(A) has coverage W, while h(K) has the same coverage as K.
Coverage is monotone and subadditive. Consequently every such benchmark
has coverage at most rW. No equilibrium assumption is used, and repeated
actual actions affect this statement only through their distinct support.

## Two equal blocks with full exchangeability

There are two groups X,Y, each of k themes. Customer incidence is invariant
under all permutations within groups and under exchanging the groups.
Let actual distinct support A contain a themes in X and b themes in Y,
and put d=a+b. Choose an automorphism g which exchanges the groups,
followed by independent within-group permutations, so that

    |(A union g(A)) intersect X| = min(k,d),
    |(A union g(A)) intersect Y| = min(k,d).       (1)

This is possible because g(A) has b X-themes and a Y-themes. In X, a
fixed a-element set and a freely placed b-element set can have union
min(k,a+b). In Y the same independent construction applies to a fixed
b-element set and a freely placed a-element set.

Every benchmark support with at most d distinct themes has at most
min(k,d) themes in either block. Independent within-group permutations
therefore move it inside A union g(A). The image-cover principle proves

    OPT_d <= 2W.                                (2)

More generally, for a game with m providers, if

    d >= min(k,m),                              (3)

then every m-theme benchmark also has at most min(k,m)<=min(k,d) themes
in either block. Thus

    OPT_m <= 2W.                                (4)

When m<=k, condition (3) requires d=m, meaning all actual actions are
distinct. When m>k, (3) only requires d>=k and allows repeated actual
themes. In particular, every all-distinct actual profile satisfies (4),
for every split between the blocks and every order, without an SPE
hypothesis. Empty support gives W=OPT_0=0 in (2); the actual CAG has
m>=1, and (4) retains the stated support condition.

The unresolved strategic cases in this symmetric class have support
d<min(k,m). The general common-catalog question has no such automorphism
cover guarantee.
