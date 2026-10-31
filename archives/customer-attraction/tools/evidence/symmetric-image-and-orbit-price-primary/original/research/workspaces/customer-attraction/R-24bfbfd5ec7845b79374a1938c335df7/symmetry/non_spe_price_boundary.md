# A symmetric all-distinct profile can violate the minimum-price bridge

Exact boundary example, 2026-10-21. This profile is not SPE. It refutes
only an extension of B(min_i u_i)<=W to arbitrary symmetric all-distinct
profiles; it does not refute that candidate for full SPE or half coverage.

Take ten X-themes and ten Y-themes. In each block there is one distinct
unit customer for every five-element subset of its ten themes. That
customer likes exactly the five themes in that subset and no theme from
the other block. There are 2 binom(10,5)=504 unit customers. All twenty
theme sets are distinct, and the incidence multiset is invariant under
all within-block permutations and swapping the blocks.

There are ten providers. Consider the all-distinct profile consisting of
one X-theme and nine Y-themes. The X-provider covers binom(9,4)=126
customers alone, so its utility is 126. The nine Y-themes cover all 252
Y-customers. By symmetry their provider utilities are equal, hence each
is 252/9=28. Thus

    W=126+252=378,        min_i u_i=28.

Give every theme fractional query weight 1/5, total weight tau=4. Each
customer belongs to exactly five themes, so every customer's truncated
fractional coverage is one. Therefore

    B(28) >= 504-4*28 = 392 > 378=W.

This does not contradict the minority-provider orbit theorem: the
minority provider has utility 126, while the minimum belongs to the
majority group.

For a concrete failure of sequential optimality, order the minority
provider first and the nine majority providers afterwards. The last
provider receives 28. Switching to a fresh X-theme gives 126 customers,
of which binom(8,3)=56 are also in the earlier X-theme, and hence utility

    126-56/2=98>28.

Thus this ordered profile cannot be an SPE terminal path. More generally,
at least one of its last two providers lies in the majority group, so the
known genuine-last-two price endpoint excludes every ordering from a
full SPE: each would contradict B(28)>W.

The maximum ten-theme coverage in this instance is 502. Indeed, a
benchmark using r distinct X-themes and 10-r distinct Y-themes covers

    504-binom(10-r,5)-binom(r,5),

where binomial terms with upper argument below five are zero. For r=5
the missed count is two; for r<=4 or r>=6 one term is at least six.
Hence OPT_10=502<2W=756, consistent with the deterministic automorphic
image half bound.
