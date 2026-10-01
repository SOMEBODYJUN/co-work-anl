> **Historical research note (superseded frontier statements).** Preserve the derivation below as provenance; use [the current mathematical map](../../../README.md), [claim registry](../../curation-2026-10-01/CLAIMS.md) and [source-status guide](../../curation-2026-10-01/PROVENANCE.md) for current scope.

# A factor-2 theorem for a closed bipartite maximin four-cycle

Research note, 2026-09-30. This note concerns two facilities with potentially different finite action sets. It allows arbitrary finite positive customer weights, arbitrary accessibility, and exact independent mixed customer Nash equilibria. It does not use the common-action-set golden-ratio theorem.

## 1. Definitions and the contradiction setup

Treat each action as a colored vertex, even if the underlying physical location is available to both facilities. For opposite-color vertices s,t, let m(t,s) be the minimum possible expected load of the facility at t among exact independent mixed customer Nash equilibria of the layout (s,t). Let

    D(s) = max_{t of the opposite color} m(t,s),
    b(s) in argmax_t m(t,s).

All maxima defining D retain the full allowed action sets.

For a fixed layout (s,t), an equilibrium with loads L_s,L_t is 2-stable under suitable exact off-path continuation selection if

    L_s >= D(t)/2,       L_t >= D(s)/2.

The reason is that each unilateral deviation can be assigned a customer equilibrium minimizing the deviator's load; the two players' nontrivial unilateral deviation profiles are different labeled layouts.

Suppose no legal layout has such an equilibrium. On a directed maximin edge s -> t=b(s), every customer equilibrium therefore satisfies

    L_t >= D(s),         L_s < D(t)/2.                 (1)

The first inequality already supplies t's stability threshold, so failure of the second threshold is necessary.

Take any closed directed cycle and normalize its positive maximum D-value to 1. If the maximum were zero, any edge would immediately supply a stable layout. Write R_s for the total weight of customers who can use s. Compactness of the customer equilibrium set gives

    R_s <= weight(C_s union C_t)
        = D(s) + max_NE L_s
        < D(s) + D(t)/2 <= 3/2.                      (2)

Here the equality uses an equilibrium minimizing the responder's load, and conservation of the total covered weight.

## 2. No visible customer weighs at least one half

We use the following elementary pure repair fact: if one side initially has smaller load A<B and every common customer currently on that side has weight at least B-A, repeatedly move a largest improving customer from the original higher side to the original lower side, stopping at the first load reversal or at equilibrium. The resulting assignment is a pure customer equilibrium and the original lower side has load at least A. This is the pure repair lemma in Section 3.1 of `history/proofs/shared/existence_candidate.md`; its proof does not use common facility action sets.

Suppose a customer of weight H>=1/2 is visible somewhere on the cycle. By (1), it must remain visible at the next vertex: otherwise it is forced to the incumbent and gives that incumbent load at least H>=1/2. Thus this customer is visible at every cycle vertex.

For an edge s->t, let S be the weight of its other common customers. Assign H to s and all other common customers to t. The initial loads are

    Q0 = R_s-S >= H,          P0 = R_t-H.

Assume R_t>=Q0. If Q0>=P0, this assignment is already a pure equilibrium: the H-customer is stable precisely because Q0<=R_t, and all other common customers are on the smaller-load side. If Q0<P0, then (2) gives

    P0-Q0 < 3/2-2H <= 1/2 <= H.

Pure repair applies and leaves s with load at least Q0>=1/2. Either case contradicts (1). Therefore every edge must have

    R_t < Q0 <= R_s,

which is impossible around a cycle. Hence

    every customer visible on the cycle has weight < 1/2.       (3)

## 3. No bad four-cycle

Suppose the cycle consists of four alternating-color vertices

    v1 -> v2 -> v3 -> v4 -> v1,

and rotate it so that

    D(v1)=1,       D(v2)=b,       D(v3)=c,       D(v4)=e.

Thus b,c,e<=1. Let R_i=R_{v_i} and C_i=C_{v_i}.

### 3.1 The maximum edge and elementary set constraints

Take any pure customer equilibrium on edge v1->v2. Its responder load is at least 1, and its incumbent load is less than b/2<=1/2. The load gap is therefore greater than 1/2. By (3), no common customer can be assigned to the higher-load responder in a pure equilibrium: such a customer would need weight at least the gap. Consequently all common customers are assigned to v1, and

    R_1 < b/2,           R_2 >= 1,
    weight(C_2 minus C_1) >= 1.                       (4)

Also e=m(v1,v4)<=R_1. In particular,

    b > 2e.                                           (5)

On edge v4->v1, choose an equilibrium minimizing the responder's load. Its two loads are e and a number less than 1/2. Hence

    c <= R_4 <= weight(C_4 union C_1) < e+1/2.          (6)

The set inclusion

    C_2 minus C_1
       subset (C_2 minus C_3)
          union (C_3 minus C_4)
          union (C_4 minus C_1)

uses only the three cycle edges v2->v3, v3->v4, v4->v1. Each set difference consists of customers forced to the corresponding incumbent. By (1), its weight is respectively less than c/2, e/2, and 1/2. Together with (4), this gives

    1 < (c+e+1)/2,        hence c+e>1.                 (7)

Combining (6) and (7),

    e > 1/4.                                          (8)

In particular, (5), (6), and (8) imply

    2b > 4e > 2e+1/2 > c+e,
    so b-c/2 > e/2.                                   (9)

### 3.2 Route a whole set of customers through the next edge

Write E=C_2 minus C_1, so weight(E)>=1 by (4). Take any pure equilibrium on edge v2->v3, and denote its incumbent and responder loads by Q_2 and P_3. Let X be the customers in E who are assigned to v3 in this equilibrium. The E-customers assigned to v2 have total weight at most Q_2. Thus X consists of common customers of v2,v3, none of whom can use v1, and

    weight(X) >= weight(E)-Q_2 > 1-c/2 >= 1/2.        (10)

For every x in X, pure Nash stability at the higher-load responder gives

    w_x >= P_3-Q_2 > b-c/2 > e/2.                     (11)

Consider any pure equilibrium on the next edge v3->v4. Its v3-load is less than e/2. Since every x in X is visible at v3 and has weight greater than e/2, each x must also be visible at v4: otherwise it would be forced to v3, contradicting that load bound. Thus X is a subset of C_4 minus C_1. This inference actually needs only accessibility and the incumbent-load bound; the nonexistence of v4 accessibility would force the whole customer to v3 even in a mixed equilibrium.

At layout (v4,v1), all customers in X are forced to v4. Equation (10) implies that every customer equilibrium gives v4 load greater than 1/2. This contradicts (1) on edge v4->v1, where the incumbent v4-load is less than D(v1)/2=1/2.

This proves that a closed bipartite maximin four-cycle cannot occur under failure of factor-2 stability.

## 4. Consequence for one facility with at most two actions

**Theorem.** If min(|U1|,|U2|)<=2, the two-facility game admits pure facility locations and exact independent mixed customer Nash equilibrium continuations forming a 2-approximate subgame-perfect equilibrium.

**Proof.** Choose a maximin response b at every colored action vertex. A directed cycle alternates colors. If one color has at most two vertices, a simple directed cycle has length two or four. A two-cycle s->t->s supplies a layout in which every customer equilibrium satisfies L_s>=D(t) and L_t>=D(s), so it is already exact-stable under minimizing off-path continuations. A four-cycle contradicts Section 3 under failure of factor-2 stability. Therefore a 2-stable layout exists, and the exact continuation criterion in Section 1 completes the construction. QED.

## Scope

- No bound on the number of shared customers at a layout is assumed.
- No off-cycle chord, same-color layout, or co-location is used.
- The proof permits zero reach at irrelevant vertices; the bad-cycle inequalities themselves rule out degeneracies where needed.
- This proves an upper bound 2 for the stated asymmetric action-set subclass. It does not prove a strict bound below 2, nor settle arbitrary numbers of actions on both sides.
