> **Historical research note (superseded frontier statements).** Preserve the derivation below as provenance; use [the current mathematical map](../../../README.md), [claim registry](../../../CLAIMS.md) and [source-status guide](../../../PROVENANCE.md) for current scope.

# Excluding a general alternating six-cycle at factor 2

Research proof, 2026-09-30. This proof concerns arbitrary positive customer weights and arbitrary numbers of common customers. It uses only legal opposite-color layouts and a common finite menu of exact **pure** customer Nash equilibria at each layout. All response maxima below are over the full allowed action sets.

## 1. Setup and previously proved prerequisites

Use the pure repair menu R(s,t) of `upper.md`, Section 10: both orientations of a layout use the same finite output set of exact pure customer NE. The menu contains the retained all-to-one-side seeds and single-designated-customer seeds with the permitted pure repair operation. Set

    u(t,s) = min_{sigma in R(s,t)} L_t(sigma),
    D(s)   = max_{t of the opposite color} u(t,s),
    b(s)   in argmax_t u(t,s).

The minimum is attained by a **pure** menu equilibrium. It need not equal the minimum over all independently mixed customer NE. The pure minimum is used essentially in Section 4 below.

A layout and menu witness are 2-stable if their loads satisfy

    L_s >= D(t)/2,        L_t >= D(s)/2.

Such a witness yields the desired 2-approximate SPE by assigning each unilateral deviation a menu witness minimizing the deviator's load. Suppose, for contradiction, that no legal layout and menu witness meet both quotas.

On every selected response edge s->t=b(s), every menu equilibrium satisfies

    L_t >= D(s),          L_s < D(t)/2.                 (1)

Suppose there is a simple alternating six-cycle v1->...->v6->v1. Rotate and normalize so that its positive maximum D-value is D(v1)=1, and write

    (D(v1),...,D(v6)) = (1,b,c,f,g,e).

All six values lie in [0,1]. A zero maximum would directly give a stable edge witness. Write C_i for the customers visible at v_i, R_i=weight(C_i), and V_ij=weight(C_i union C_j).

We use the following prerequisites already proved from the same menu in `upper.md`, Sections 1-4, and in `general_four_cycle.md`:

1. **Reach bound on a response edge.** Minimizing the responder's menu load and using conservation of covered weight gives

       R_i <= V_{i,i+1} < D(v_i)+D(v_{i+1})/2.

   Also R_{i+1}>=D(v_i).

2. **No heavy visible customer.** Every customer visible anywhere on this closed cycle has weight strictly less than 1/2. The proof propagates a hypothetical weight H>=1/2 around the cycle, then uses a single-H seed and pure repair to force strict reach decrease on every edge. The menu was defined to contain every invoked repair witness.

3. **Maximum-edge consequence.** At v1->v2, the responder has load at least 1 and the incumbent less than b/2<=1/2. A common customer placed at the higher-load responder would need weight greater than 1/2, impossible. Thus in a pure menu witness every common customer is assigned to v1, giving

       R_1 < b/2,       R_2 >= 1,
       weight(C_2 minus C_1) >= 1,
       e <= R_1 < b/2.                                (2)

   In particular, b>2e.

4. **Global private-load chord inequality.** For every opposite-color pair s,t, selected edge or not,

       weight(C_s minus C_t) <= u(s,t) <= D(t).         (3)

   The first inequality holds in every equilibrium because those customers are forced to s. The second uses the full global response maximum. This inequality also holds for menu minima; it needs no unlisted equilibrium.

The cross-color chords used below are v3--v6 and v2--v5. Their endpoints have opposite colors.

## 2. The first transferred batch

Put E=C_2 minus C_1. In any pure menu equilibrium on v2->v3, take X to be the members of E assigned to v3. If the two loads are Q_2,P_3, then Q_2<c/2 and P_3>=b. Consequently

    weight(X) >= weight(E)-Q_2 > 1-c/2 >= 1/2,
    w_x >= P_3-Q_2 > b-c/2 for every x in X,
    X is disjoint from C_1.                           (4)

Write

    h = b-c/2.

At the last edge v6->v1, the incumbent load is less than 1/2. Therefore

    weight(C_6 minus C_1) < 1/2.                      (5)

By (4)-(5), some member of X is absent from C_6. Define

    z = weight(C_3 minus C_6).

This absent member is visible at v3 and weighs more than h, so

    z > h,                  z <= e.                  (6)

The second inequality is the legal chord (3). In particular,

    h<e,          c>2b-2e>2e,          c>b.            (7)

The last two consequences use b>2e.

We split into the two exhaustive cases h>=e/2 and h<e/2.

## 3. Case h>=e/2

Here z>h>=e/2, so at layout (v3,v6) the v3-load in every menu equilibrium exceeds its quota e/2. Failure of stability therefore forces the v6-load to be less than c/2 in every menu equilibrium.

Choose a menu equilibrium minimizing the v3-load. Its v3-load is u(v3,v6)<=e by the global maximum at v6. By (7), e<c/2. Thus this chosen **pure** equilibrium has both facility loads strictly below c/2. Every covered customer is assigned wholly to one facility, so

    every customer visible at v3 or v6 has weight < c/2.       (8)

Conservation of weight in the same witness gives

    V_36 < e+c/2.

Since V_36=R_6+z, R_6>=g, and z>h=b-c/2,

    g < e+c/2-z < e+c-b < c.                         (9)

Next suppose f<=c. On edge v3->v4, every menu witness has responder load at least c and incumbent load less than f/2. The load gap exceeds c-f/2>=c/2. By (8), no customer visible at v3 can be assigned to the higher-load responder in a pure equilibrium. Consequently every v3-customer is assigned to v3, and

    R_3 < f/2 <= c/2 <= b.

The last inequality follows from h=b-c/2>=e/2>=0. This contradicts R_3>=b. Hence

    f>c.                                             (10)

Now take a pure menu equilibrium on edge v4->v5. Its incumbent load is less than g/2, while R_4>=c>g. Therefore at least one v4-customer is assigned to the responder v5. Call its weight H. Pure customer Nash stability, (9), and (10) give

    H > f-g/2 > c/2.                                 (11)

This customer is visible at v5. On edge v5->v6, the v5-load is less than e/2. Since H>c/2>e/2, the customer must also be visible at v6; otherwise it would be forced to v5. But (8) says every customer visible at v6 weighs less than c/2. This contradiction excludes h>=e/2.

## 4. Case h<e/2

The case assumption and b>2e yield

    c>2b-e>3e,          hence e<1/3.                 (12)

### 4.1 An upper bound on g

We first prove

    g < (1+e)/2.                                     (13)

Suppose otherwise. On edge v5->v6, responder load is at least g and incumbent load is less than e/2. The gap is therefore greater than 1/2. Since every cycle-visible customer weighs less than 1/2, no common customer can be assigned to the responder in a pure menu witness. All v5-customers are assigned to v5, and

    R_5 < e/2.

The legal v2--v5 chord and (2) then give

    g >= weight(C_2 minus C_5) >= R_2-R_5 > 1-e/2.

On the other hand, the edge v6->v1 gives

    g <= R_6 < e+1/2.

Combining these inequalities forces e>1/3, contradicting (12). This proves (13). In particular,

    g+e < 1.                                         (14)

### 4.2 The v2--v5 chord closes the contradiction

The customers of E=C_2 minus C_1 that are visible at v5 satisfy

    E intersect C_5
       subset (C_5 minus C_6) union (C_6 minus C_1).

The first set has weight less than e/2 by the incumbent bound on v5->v6. The second has weight less than 1/2 by (5). Since weight(E)>=1,

    weight(C_2 minus C_5)
       >= weight(E)-weight(E intersect C_5)
        > (1-e)/2
        > g/2.                                       (15)

The last inequality uses (14). Thus at the legal layout (v2,v5), the v2-facility always exceeds its stability quota g/2 using forced private customers alone. Failure of stability implies that the v5-load is less than b/2 in every menu equilibrium.

Choose a menu equilibrium minimizing the v2-load. By the full global response maximum at v5, this v2-load is at most g. Hence

    1 <= R_2 <= V_25 < g+b/2 < (1+e+b)/2,

where the last inequality is (13). Therefore

    b>1-e.

Using (12) again,

    c>2b-e>2-3e>1,

contrary to the normalization c<=1. This excludes h<e/2 and completes the six-cycle contradiction.

## 5. Consequence and scope

Every simple directed cycle of the global pure-menu response map is alternating. If min(|U1|,|U2|)<=3, a cycle has length 2, 4, or 6. The two-cycle case directly supplies an exact-stable menu witness; `general_four_cycle.md` excludes a bad four-cycle; the argument above excludes a bad six-cycle. Therefore a menu witness satisfying the factor-2 quotas exists.

Combined with the finite pure-repair menu construction in `upper.md`, this proves existence and a polynomial-time construction of a 2-approximate SPE for min(|U1|,|U2|)<=3. All customer continuations can be exact pure Nash equilibria of the original customer game. Allowing independent mixed continuations therefore preserves the conclusion.

This note does not exclude alternating cycles of length eight or greater. It makes no claim that a minimum over all mixed customer equilibria is attained purely. Instead it deliberately defines and uses the polynomial finite pure menu throughout.
