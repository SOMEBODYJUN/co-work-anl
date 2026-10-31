# Maximum-mass cells and low overlap give a fractional-price certificate

Research backup, 2026-10-21. Exact identity BPC-v2; analytical proof below.
This strengthens the original transitive-orbit certificate, which remains
separately recorded as version 1 in `orbit_overlap_price_certificate.md`.
The direct balanced-cell Jensen step was suggested independently by the
adversarial reviewer; the maximum-mass relaxation was suggested by the
parent researcher. No external review or novelty claim is made. General
Q-CAG-HALF remains OPEN.

## Exact statement

Use the exact common-catalog unit-customer CAG, and fix any terminal
profile S_1,...,S_m. No equilibrium is required. Fix a provider i and a
partition of the customer set into nonempty cells O. Put

    p_O = |S_i intersect O|/|O|.

Assume that on every cell,

    |T intersect O| <= |S_i intersect O|       for every catalog theme T,
                                                        (MM)
    sum_(j != i)|S_i intersect S_j intersect O|
        <= (m-1)p_O^2 |O|.                            (LO)

For any nonnegative real query weights z_T, let

    tau=sum_T z_T,
    C(z)=sum_x min(1,sum_(T contains x)z_T).

Then, for the actual terminal utility u_i,

    C(z) <= (tau+m-1)u_i                        for every z>=0,  (1)
    B(u_i)=sup_(z>=0)[C(z)-tau u_i] <= (m-1)u_i.              (2)

If i is a minimum-utility provider, this gives

    B(min_j u_j) <= W-u_i,
    OPT_m <= (2m-1)u_i <= (2-1/m)W.                          (3)

No sharpness within this structural class is asserted. Repeated actual
themes and arbitrary customer incidence are permitted when (MM)-(LO)
hold. The assumptions are properties of this one terminal profile.

## Proof

Write a_O=|S_i intersect O|=p_O|O|. If a_O=0, condition (MM) implies
that no catalog theme covers a customer in O. Both the fractional
coverage and player i's utility on that cell are zero.

For a_O>0, put L_x=sum_(j != i)1_(x in S_j). Jensen for 1/(1+s), or
Cauchy-Schwarz, and (LO) give

    u_i(O)=sum_(x in S_i intersect O)1/(1+L_x)
      >= a_O/[1+sum_(j != i)|S_i intersect S_j intersect O|/a_O]
      >= |O|p_O/[1+(m-1)p_O].                              (4)

Put d_x=sum_(T contains x)z_T. Condition (MM) gives

    sum_(x in O)d_x=sum_T z_T|T intersect O|
        <= tau p_O|O|.

The truncation min(1,s) is concave and nondecreasing. Its cellwise Jensen
inequality is therefore

    sum_(x in O)min(1,d_x) <= |O|min(1,tau p_O).            (5)

For every p in [0,1] and tau>=0,

    min(1,tau p) <= (tau+m-1)p/[1+(m-1)p].                 (6)

For tau p<=1, clearing the positive denominator reduces (6) to
(m-1)tau p<=m-1. For tau p>=1, it reduces to 1<=tau p.
The case m=1 is included: both conditions give equality in their
respective nonzero regimes. Thus this proof uses all real tau, including
zero, and never normalizes an arbitrary query to unit mass.

Sum (5)-(6) over the cells and apply (4). This proves (1). Subtract
tau u_i and take the supremum to obtain (2). For a minimum provider,
W>=m u_i, hence (m-1)u_i<=W-u_i. Finally, assign weight one to each
occurrence in an optimal length-m portfolio. Its fractional coverage is
OPT_m and total weight is m, so (1) gives the second line of (3).

## Explicit consequences and original-version recovery

For a single cell O=N, it suffices that S_i is a largest catalog theme
and

    sum_(j != i)|S_i intersect S_j|
        <= (m-1)|S_i|^2/|N|.                              (7)

If such a provider also has minimum utility, (3) holds without any SPE
hypothesis. Uncoverable customers may be removed first; the empty
customer instance directly has W=OPT_m=0 and needs no division.

If a finite incidence-preserving group is transitive on themes, its
customer orbits satisfy |T intersect O|=p_O|O| for every T. Thus (MM)
holds with equality, and the original orbit theorem is precisely this
version's corollary with (LO) unchanged. In the fully symmetric two-block
catalog, every provider in a group represented at most (m+1)/2 times in
an all-distinct actual profile satisfies the orbitwise (LO), as proved in
the original file.

The theorem does not supply (MM)-(LO) for a general SPE or a general
minimum provider. In particular, a player covering a small theme may fail
(MM), and heavy same-theme repetition may fail (LO). These are genuine
restrictions, not consequences of sequential optimality established here.
