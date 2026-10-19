# Raw SH3 正质量入口的 canonical 分数子树流

Scratch addendum to `sol_raw_sh3_root_conditioned_layer_flow_boundary_v1.md`; no earlier bytes changed. Author proof, no independent review. This is an existence-preserving *new first-moment flow*, not a moment-preserving canonicalization of the supplied raw point and not an integer decoder.

## 1. Precise assertion

Use the frozen boundary's native home-budget-one original jobs, a finite simple layered DAG, 1<=T<2, common M3, original Boolean/one-hot ideals through degree six, unit-row same-pair zeros and every global degree-two load localizer. Let E be one original unit-arrival endpoint at a vertex v, with p=L(E)>0. Put r_u=k_u(2-T)>0.

Then the descendants of v admit a canonical fractional subtree flow with root activity p: nonnegative activities a_u<=p, original-token head fluxes f_u,a,w>=0, root a_v=p, every other a_w equal to its total incoming head flux, every original token's total export at most a_u, every graph arc's aggregate head flux at most a_u, and

    sum_(a,w) f_u,a,w >= r_u a_u.                 (1.1)

The flow may be reduced to equality in (1.1). It uses only original unit-head menus. It is a new feasible flow and need not preserve any first, second or higher moment of the raw certificate. On dividing by p, every vertex has capacity one and v is the sole fractional source. This is stronger than the naive assignment-flow consequence, but weaker than a common full CONFIG+M2 point or an actual forest.

When every (T-1)k_u is an integer, the new first moments also have canonical full CONFIG(T) row decompositions: inactive rows keep all home tokens, active rows have one original incoming unit and exactly (T-1)k_u retained home tokens. This claim is only about first moments. It does not match a prescribed same-row pair table.

## 2. Shared conditional weights and projection positivity

Keep homogeneous weights, without dividing by p:

    b_u=L(E C_u),
    y_u,a,w=L(E C_u x_u,a,w),
    S_u=sum_(a,w) y_u,a,w.

Here C_u is the unit incoming occupancy. The pair-zero/M3-null argument of the frozen boundary makes C_u, and each subset of a unit row's incoming endpoints, a linear Boolean projection inside every expectation below. A product of at most three such commuting projections has nonnegative expectation: square the degree-at-most-three product and reduce the Boolean/null identities. In particular,

    0<=b_u<=p,  y_u,a,w>=0,
    sum_w y_u,a,w<=b_u,                           (2.1)
    sum_a y_u,a,w<=b_u.                           (2.2)

The first job inequality uses that a token's export indicator is 1 minus its home endpoint. The arc inequality uses that all those token heads are a subset of the unit row at w. Their complements are projections as well. For example, E C_u(1-F_uw) has degree three, where F_uw=sum_a x_u,a,w. Its square differs from itself by

    E(C_u^2-C_u)(1-F_uw)^2 + E C_u(F_uw^2-F_uw),

whose expectations vanish: each same-row pair null is paired with a polynomial of degree at most three. This pays (2.2) without a free nonnegative triple rule.

The frozen inactive-hole square gives y_u,a,w<=L(E x_u,a,w), hence

    sum_(u,a incoming at w) y_u,a,w<=b_w.         (2.3)

Selectors, if any, only add nonnegative terms to b_w. The load localizers q=E R_j give

    S_u>=r_u b_u.                                (2.4)

Since E is itself an incoming endpoint at v, unit-pair zeros give b_v=p.

## 3. Explicit topological construction

Initialize a_v=p, set every other vertex at or above v's layer to zero, and visit lower layers in topological order. At a visited u, its activity is the sum of previously constructed incoming fluxes. Inductively a_u<=b_u, by (2.3). If b_u=0, set its outgoing fluxes to zero. Otherwise choose

    f_u,a,w=(a_u/b_u)y_u,a,w.

Equations (2.1)-(2.4) prove all stated bounds and the cover (1.1). For exact real demand one may instead use f_u,a,w=(r_u a_u/S_u)y_u,a,w whenever a_u>0; (2.4) ensures the factor is at most a_u/b_u. Each next activity remains at most b_w. Unreachable vertices receive zero. The DAG is essential to this one-pass proof; no cyclic version is claimed.

At an integral threshold grid, let h_u=(T-1)k_u and use the exact cover. For a_u>0, the vector of normalized active retained-home marginals is

    1-sum_w f_u,a,w/a_u,  a in [k_u].

Each entry is in [0,1], and their sum is k_u-r_u=h_u. It lies in the ordinary h_u-subset hypersimplex, so it is a convex combination of h_u-element home subsets. Pair this home law with the incoming original-unit label distribution f_in/a_u; root v uses E as its fixed incoming label. Give this active row law mass a_u/p after normalization, and its all-home inactive configuration the remaining mass. These are full legal row CONFIG lists matching the new first moments. No claim about old first moments or old pair moments is made.

Given rational original moment entries, the displayed construction is polynomial-bit time in the explicit DAG and certificate. Each transition factor is a fixed rational y/b or r y/S; rational dynamic programming on a DAG has a common denominator dividing a product of polynomially many transition denominators. No path enumeration is needed. Feasibility of the resulting ordinary canonical first-moment subtree LP can also be tested directly from the input by rational linear programming, without finding the original raw point.

## 4. Scope of the resulting FAIL test

If this canonical fractional subtree LP is infeasible at v, every original unit endpoint entering v must have zero first moment in every stated raw SH3 certificate. This can be combined with selector one-hot or other forced arrivals to reject the entire relaxation. It is also a sound necessary test for actual T schedules. A rejected candidate endpoint or one raw point alone is not a proof that the whole original instance is infeasible.

The old shared three-block 49-machine core still has feasible canonical first flows at the binary target while lacking an actual binary forest; joint owners remain unresolved by this projection. Thus this addendum narrows a prospective SH3 gap source to shared integer ownership after all these per-input canonical subtree flows are already feasible. It supplies neither a general approximation guarantee nor a true near-two stronger-relaxation gap.
