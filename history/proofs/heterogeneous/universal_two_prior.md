> **Historical research note (superseded frontier statements).** Preserve the derivation below as provenance; use [the current mathematical map](../../../README.md), [claim registry](../../curation-2026-10-01/CLAIMS.md) and [source-status guide](../../curation-2026-10-01/PROVENANCE.md) for current scope.

# Universal factor-2 existence for two facilities with arbitrary action sets

Proof for independent audit, 2026-09-30. This note is self-contained at the level of the finite customer game. It allows arbitrary finite positive customer weights, arbitrary accessibility, and arbitrary nonempty finite facility-specific action sets. The customer continuations constructed below are exact pure Nash equilibria, and therefore also valid independently mixed equilibria.

## Theorem

For two facilities with arbitrary finite allowed action sets U1,U2, there exist pure facility locations and exact pure customer Nash equilibrium continuations at every legal layout such that neither facility can improve its expected customer weight by a factor greater than 2.

Locations are treated as colored actions. If one physical location belongs to both allowed sets, it has one copy of each color. All legal layouts pair opposite colors. The proof never requires the two allowed sets to coincide.

## 1. A common finite menu of pure customer equilibria

For each legal pair s,t, use one common menu R(s,t) for both load orientations. It consists of exact pure customer Nash equilibria obtained as follows.

For each orientation, include the seed with all common customers at one end. Also, for each designated common customer H and each orientation, include the seed placing only H at one end and all other common customers at the other end. Exclusive customers are forced throughout.

If a seed is already a pure NE, retain it. Otherwise apply the following repair only if its hypothesis holds; discard seeds for which it does not hold.

**Pure repair.** Suppose initial loads are A<B and every common customer initially on the lower-load side has weight at least B-A. Repeatedly move a largest-weight strictly improving customer from the original higher side to the original lower side, stopping when there is no improvement or at the first reversal of load order. The output is a pure NE, and the original lower side has final load at least A.

To verify this, an improving move of weight w satisfies w<B'-A' and leaves both new loads strictly between A' and B'. Before the first reversal the gap decreases, so moved weights are nonincreasing. At the first reversal the new absolute gap is smaller than the last moved weight. Thus every earlier moved customer and every original lower-side common customer is stable; all customers remaining on the original higher side now occupy the lower-load side and are stable. If there is no reversal, all customers already on the lower side stay stable, and stopping for lack of improvements gives a pure NE. Only original higher-side customers move, each at most once.

The menu is nonempty. For an all-common-on-one-side seed, if that side has no larger load, the seed is already a pure NE. Otherwise the lower side has no common customers, so the repair hypothesis holds vacuously. Fix any deterministic tie rule when constructing the menu.

The proof uses only retained outputs of these seeds. In particular, it never assumes that a minimum over all mixed customer equilibria is attained purely.

## 2. Menu response values and stability quotas

For opposite-color actions s,t, define

    u(t,s) = min_{sigma in R(s,t)} L_t(sigma),
    D(s)   = max_{t of the opposite color} u(t,s).

Every maximum defining D is over the **full** allowed action set of the other facility. Choose a maximizing response b(s).

If some legal layout (s,t) has a menu equilibrium with

    L_s >= D(t)/2,         L_t >= D(s)/2,              (1)

then it extends to a factor-2 SPE. After each unilateral deviation choose a menu equilibrium minimizing the deviator's load; that payoff is at most the corresponding D-value. Different players' nontrivial unilateral deviation profiles are distinct labeled layouts, so these choices do not conflict. Fill remaining layouts with arbitrary menu equilibria.

Suppose for contradiction that no legal layout and menu witness satisfy (1). On a selected response edge s->t=b(s), every menu equilibrium satisfies

    L_t >= D(s),          L_s < D(t)/2.                (2)

The responder already meets its quota, so the incumbent must fail its own quota.

The finite response graph has an alternating directed cycle. A two-cycle s->t->s immediately contradicts failure of (1): in the same common menu, every witness has L_t>=D(s) and L_s>=D(t). We may therefore use a simple cycle of even length ell>=4.

If its maximum D-value is zero, any edge witness satisfies both zero quotas. Otherwise normalize all weights so that this maximum is 1 and rotate the cycle to make D(v1)=1. All D-values at cycle vertices are now at most 1; they remain the full global maxima defined above.

Write C_s for the customers who can use s, R_s=weight(C_s), and V_st=weight(C_s union C_t). Total load at layout (s,t) is always V_st. Minimizing the responder on a selected edge gives

    R_s <= V_st < D(s)+D(t)/2 <= 3/2.                (3)

Also R_t>=D(s), since the responder's reach bounds every possible payoff.

We will repeatedly use a legal chord inequality. For any opposite-color s,t, whether or not they are consecutive on the cycle,

    weight(C_s minus C_t) <= u(s,t) <= D(t).           (4)

The customers in the set difference are forced to s in every equilibrium; the upper bound is the global maximum at t.

## 3. No cycle-visible customer weighs at least one half

Suppose a customer of weight H>=1/2 is visible at some cycle vertex. By (2), it is also visible at the next vertex: otherwise it is forced to the incumbent, whose load must be less than D(next)/2<=1/2. It follows that this customer is visible at every cycle vertex.

On an edge s->t, let S be the weight of the other common customers. Take the single-H seed assigning H to s and all other common customers to t. Its loads are

    Q0=R_s-S>=H,         P0=R_t-H.

Assume R_t>=Q0. If Q0>=P0, the seed is already a pure NE: the H-customer is stable because Q0-H<=P0 is equivalent to Q0<=R_t, and the other common customers occupy the smaller-load side. If Q0<P0, then (3) gives

    P0-Q0 < 3/2-2H <= 1/2 <= H.

The pure repair hypothesis holds, so the menu contains a repaired equilibrium giving s load at least Q0>=1/2. Both cases contradict (2). Therefore every cycle edge satisfies R_t<Q0<=R_s, an impossible strict reach decrease around a cycle. Hence

    every customer visible at a cycle vertex has weight <1/2. (5)

## 4. The maximum edge and one transferred batch

Use the following vertex names and D-values:

    A=v1,  B=v2,  C=v3,  F=v_ell,  G=v_(ell-1),
    D(A)=1, D(B)=b, D(C)=c, D(F)=e, D(G)=g.

If ell=4, G=C; all arguments below permit this coincidence. The relevant chords C--F and B--G are legal opposite-color pairs.

At A->B, every pure menu witness has responder load at least 1 and incumbent load less than b/2<=1/2, so its load gap exceeds 1/2. By (5), no common customer can occupy the higher-load responder. Thus all common customers are assigned to A, giving

    R_A<b/2,          R_B>=1,
    E=C_B minus C_A has weight at least 1,
    e<=R_A<b/2.                                      (6)

In particular b>2e. The last response edge F->A also gives

    R_F<e+1/2,       weight(C_F minus C_A)<1/2.         (7)

Take any pure menu witness on B->C. Let X be the E-customers assigned to C. Since the incumbent B-load is less than c/2 and the responder C-load is at least b,

    weight(X)>1-c/2>=1/2,
    w_x>b-c/2 for every x in X,
    X is disjoint from C_A.                          (8)

The weight bound is the pure Nash inequality for a customer assigned to the responder: w_x>=L_C-L_B. This is valid even if the load difference is nonpositive. Put h=b-c/2.

By (7)-(8), X cannot be contained in C_F. Thus, writing z=weight(C_C minus C_F), some member of X contributes weight greater than h to z. The chord (4) gives

    z>h,             z<=e.

Consequently

    h<e,           c>2b-2e>2e,           c>b.          (9)

We split into the two exhaustive cases h>=e/2 and h<e/2.

## 5. Case h>=e/2: a small-common-customer invariant around the full cycle

Here z>h>=e/2. At the legal layout (C,F), the C-facility therefore exceeds its quota e/2 in every menu witness, using forced private customers alone. Failure of (1) implies that every menu witness gives F load less than c/2.

Choose a menu witness minimizing the C-load. Its C-load is u(C,F)<=e<c/2 by (4) and (9). This witness is pure, and both loads are strictly below c/2. Therefore

    every customer visible at C or F has weight <c/2.        (10)

We next extend the needed part of this bound to the full allowed action sets. Let s be **any** action of A's color. If a customer of weight at least c/2 were visible at s, its weight would exceed e. The legal chord inequality weight(C_s minus C_F)<=D(F)=e would force that customer to be visible at F, contradicting (10). Thus

    every customer visible at any action of A's color
    has weight <c/2.                                      (11)

Every customer common to a legal layout is visible at an action of A's color. Hence every common customer on every cycle edge has weight less than c/2. Customers visible only at actions of the other color need not obey this bound; they are exclusive on all legal layouts and never move.

Now start at C=v3 and follow the response cycle toward F. Initially D(C)=c and R_C>=b>=c/2, the last inequality following from h>=e/2>=0.

Suppose a visited vertex s has D(s)>=c and R_s>=c/2. If its successor t had D(t)<=c, a pure menu witness on s->t would have responder load at least c and incumbent load less than c/2. Its gap exceeds c/2. By (11), no common customer can be assigned to the higher-load responder. Therefore all s-customers are assigned to s, giving

    R_s=L_s<D(t)/2<=c/2,

contradicting R_s>=c/2. We conclude that D(t)>c. Also R_t>=D(s)>=c, so the induction hypothesis holds at the next vertex.

This induction applies through either color: only common customers require the weight bound (11). It forces every successor through F to have D-value greater than c. In particular e=D(F)>c, contrary to (9). This excludes h>=e/2 for a cycle of any length.

## 6. Case h<e/2: the penultimate chord

Here

    c>2b-e>3e,        so e<1/3.                      (12)

We first show

    g<(1+e)/2.                                      (13)

If instead g>=(1+e)/2, then on the response edge G->F the responder has load at least g and the incumbent less than e/2. The gap exceeds 1/2. By (5), no common customer can be assigned to the responder in a pure menu witness. Thus every G-customer stays at G and R_G<e/2.

Using the legal B--G chord (4) and R_B>=1 gives

    g>=weight(C_B minus C_G)>=R_B-R_G>1-e/2.

But g<=R_F<e+1/2 by the last two response edges and (7). Combining these inequalities forces e>1/3, contradicting (12). This proves (13), and hence

    g+e<1.                                          (14)

Recall E=C_B minus C_A, with weight(E)>=1. The following set inclusion uses only the last two cycle edges:

    E intersect C_G
       subset (C_G minus C_F) union (C_F minus C_A).

The first set has weight less than e/2 because it is forced to the incumbent on G->F. The second has weight less than 1/2 by (7). Therefore

    weight(C_B minus C_G)
       >= weight(E)-weight(E intersect C_G)
        > (1-e)/2
        > g/2,                                      (15)

where the last inequality is (14).

At the legal layout (B,G), the B-facility always exceeds its quota g/2, using private customers alone. Failure of (1) therefore forces the G-load to be less than b/2 in every menu witness. Choose a witness minimizing the B-load. This load is u(B,G)<=D(G)=g, so

    1<=R_B<=V_BG<g+b/2<(1+e+b)/2.

It follows that b>1-e. But then (12) yields

    c>2b-e>2-3e>1,

contradicting the normalized cycle maximum. This excludes h<e/2.

## 7. Conclusion and quantifiers

Every possible response cycle leads to a contradiction under the assumption that no menu witness meets (1). Hence some legal layout has a menu witness satisfying both factor-2 quotas. The continuation construction in Section 2 gives the theorem.

The proof uses full global D-values at its two legal chord types. It does not replace them by maxima restricted to the cycle. It works with arbitrary overlap of U1,U2, colored copies of the same physical location, reach ties, zero-reach actions, and zero D-values. No positive D-value is divided by except the positive cycle maximum used for normalization. Every invocation of purity concerns an explicitly pure menu witness, including the minimizing C-load witness in Section 5. No assertion is made that all mixed customer NE are pure or that their true minima equal the menu minima.

The six-customer family in `tight_two_lower.md` independently approaches factor 2 from below with unique customer continuations. Together with this theorem, it establishes the sharp universal factor 2 for arbitrary facility-specific allowed sets.
