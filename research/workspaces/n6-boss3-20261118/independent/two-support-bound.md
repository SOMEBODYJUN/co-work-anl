# Six players with at most two realized coverage sets

## Claim, model, and exact scope

In the original finite common-label-catalogue model with exactly six equal-weight providers and unit clients, let sigma be ANY complete-history pure SPE. If its realized six labels have at most two distinct coverage sets, then

    70 OPT_6 <= 137 W < 140 W       when W>0.

The universally meaningful conclusion is 70 OPT_6<=137W, including W=0. In particular 2W>=OPT_6. No sharpness is claimed for 137/70.

This concerns only the number of coverage sets on the realized path. The finite catalogue may have arbitrarily many other labels, empty labels, and several labels with the same coverage. Every comparison below is at a specified history of the SAME complete strategy sigma, using the true successor at an earlier-player deviation. No strategy is made Markovian and no off-path equilibrium is selected independently. The proof is self-contained and does not use the attainable-outcome recursion or a finite search.

Permitted mathematical input: only this RUN's packet-obstacle.json and this independent line's own preceding work. No other line or review was read.

## 1. Canonical naming and private-part constraints

Suppose first that exactly two distinct sets occur. Name the coverage of the actual final label B, and name the other coverage A. Let k be the number of A-covering realized labels and ell=6-k the number of B-covering realized labels. Thus 1<=k<=5, 1<=ell<=5, and the final coverage is B. The actual labels realizing A or B need not coincide.

Partition the realized union into

    P=A minus B,   Q=B minus A,   R=A intersect B,
    a=|P|,        b=|Q|,         c=|R|.

Hence W=a+b+c. Every realized A-provider has payoff a/k+c/6, and every realized B-provider has payoff b/ell+c/6.

Let t be the position of the LAST A-covering realized label. Its actual prefix has k-1 A-covering labels and j=t-k B-covering labels. If this player deviates to the actual final B-label and then follows sigma's genuine successor strategies, each client of Q has total load at most

    j+1+(6-t)=7-k=ell+1.

Each client of R has total load at most 6. These are unconditional upper bounds on loads under that true continuation, whatever off-path labels sigma chooses. SPE at this on-path t-node implies

    a/k+c/6 >= b/(ell+1)+c/6,
    hence             k b <= (ell+1) a.                 (1)

At the actual final node, choosing any A-covering catalogue label would pay a/(k+1)+c/6. Consequently

    b/ell+c/6 >= a/(k+1)+c/6,
    hence             ell a <= (k+1) b.                 (2)

Neither argument requires a,b,c to be positive. In particular a=0 forces b=0 by (1), and b=0 forces a=0 by (2). Thus a nontrivial two-distinct-set SPE path cannot have one set contained in the other. Empty-set and zero-private-part cases are not silently discarded; these inequalities settle them.

## 2. The final-node charge settles k=1,2,3,4

Fix any catalogue label T, and put

    p=|T intersect P|, q=|T intersect Q|,
    r=|T intersect R|, z=|T minus (A union B)|.

At the actual final history, T would pay

    p/(k+1)+q/ell+r/6+z.

The final player's actual best-response inequality is therefore

    p/(k+1)+q/ell+r/6+z <= b/ell+c/6.                  (3)

Take an optimal tuple T_1,...,T_6, whose existence follows from the finite nonempty catalogue. For their union D, denote its four partition sizes by p_*,q_*,r_*,z_*. Sum (3) over the six labels. All coefficients are nonnegative, so the corresponding weighted union is bounded by that sum. Using p_*<=a, q_*<=b and r_*<=c gives

    OPT_6 <= [k/(k+1)] a + [1+5/ell] b + (11/6)c.

Call this right side F_k. This includes duplicated optimum labels without any change.

Here is an exact nonnegative decomposition proving F_k<=(137/70)W for every k<=4. Let

    M_k=((ell+1)/k)a-b >=0

by (1). Then

    (137/70)W-F_k = d_k M_k + e_k a + (13/105)c,

with the following rational coefficients:

| k | ell | number of canonical words ending B | d_k | e_k |
|---|---|---|---|---|
| 1 | 5 | 5 | 3/70 | 6/5 |
| 2 | 4 | 10 | 41/140 | 67/120 |
| 3 | 3 | 10 | 149/210 | 47/180 |
| 4 | 2 | 5 | 54/35 | 0 |

All quantities on the right are nonnegative, so no division by a, b, c, or W is needed. The argument permits every possible position of the last A: only its already-counted k-1 A predecessors were used in (1).

## 3. The only remaining canonical word is A A A A A B

When k=5, ell=1 and final coverage B, all first five coverages must be A. This is the one canonical arrangement not settled by Section 2. Its name-swapped form is B B B B B A; canonical naming makes these the same case.

Let h be the actual ordered prefix of the first four LABELS. Write a_0 for the actual fifth label and b_0 for the actual sixth label, so cov(a_0)=A and cov(b_0)=B. For ANY candidate label T, define

    S = sigma_6(h,T).

Thus S is the actual last response of this very same sigma after the fifth player deviates to T. It is not chosen independently. In set expressions S below means its coverage, but h,T,S retain their original labels as strategy histories.

The following three payoff differences are all nonnegative:

    F_5(T)   = u_5(h,a_0,b_0) - u_5(h,T,S) >=0,
    F_old(S) = u_6(h,a_0,b_0) - u_6(h,a_0,S) >=0,
    F_new(T) = u_6(h,T,S)     - u_6(h,T,b_0) >=0.

Their exact origins are:

- F_5 is fifth-player SPE at the actual history h; its deviation uses the TRUE successor S=sigma_6(h,T).
- F_old is last-player SPE at the actual history (h,a_0), comparing its actual b_0 with the catalogue label S.
- F_new is last-player SPE at the possibly off-path history (h,T), comparing its actual S with b_0.

The common catalogue makes both cross-comparisons legitimate. The last player has no successors, so these last comparisons require no frozen continuation. All three are constraints on one complete sigma; no distinct strategies or arbitrary equilibrium selections are glued together.

### 3.1 Exact slack identity

With p,q,r,z as in Section 2, the following identity holds:

    7a/30+c/6-p/5-q/2-r/6-z
      = F_5(T)+F_old(S)+F_new(T)+|A minus S|/30.        (4)

Every term on the right is nonnegative. Hence for every label T,

    p/5+q/2+r/6+z <= 7a/30+c/6,                     (5)

or, equivalently,

    6p+15q+5r+30z <= 7a+5c.

For a direct derivation of (4), let

    x=|A intersect T intersect S|,
    y=|(T intersect S) minus A|,
    v=|(A intersect S) minus T|,
    g(X)=|X minus A|+|X intersect A|/6.

Then g(B)=b+c/6 and

    u_5(h,T,S) = (p+r)/5+q+z-x/30-y/2,
    u_6(h,T,S) = g(S)+v/30-y/2,
    u_6(h,T,b_0) = g(B)+(c-r)/30-q/2,
    u_5(h,a_0,b_0) = a/5+c/6.

Substituting these expressions into F_5+F_old+F_new cancels g(S),g(B),y. Since x+v=|A intersect S|, adding |A minus S|/30 gives exactly the left side of (4). All formulas also hold when any region is empty.

### 3.2 Aggregate (5) over the optimum

Let D again be the optimum union. Summing (5) over its six labels and passing to the weighted union gives

    p_*/5+q_*/2+r_*/6+z_* <= 7a/5+c.

Therefore

    OPT_6
      <= 7a/5+c+(4/5)p_*+(1/2)q_*+(5/6)r_*
      <= (11/5)a+(1/2)b+(11/6)c.

Call the last quantity G. In this case (2) reads b>=a/6. An exact decomposition now gives

    (137/70)W-G
       = (51/35)(b-a/6)+(13/105)c >=0.                (6)

Thus the same bound holds for A A A A A B. A simpler direct half-gap, also following from G and b>=a/6, is

    2W-OPT_6 >= -a/5+(3/2)b+c/6 >= a/20+c/6 >=0.

## 4. Completeness over all arrangements and labels

There are 62 binary six-letter words using both coverage names. For a specified final name B, the numbers with k=1,2,3,4,5 copies of the other name A are respectively 5,10,10,5,1. Swapping the names doubles these counts. Sections 1-2 cover 60 words; Section 3 covers the two words AAAAA B and BBBBB A. Thus no order or multiplicity is omitted.

The classification is by COVERAGE, not by label identity. Arbitrarily many distinct labels can realize A and B at different positions. In Section 1 one deviates to a particular available B-label; in Section 2 every catalogue label is compared; in Section 3 h is the actual label prefix and S is the value of the actual strategy at precisely (h,T). Thus duplicate labels cannot cause an unexamined order or continuation identification.

If only one coverage A occurs, final-player SPE gives 6|T minus A|+|T intersect A|<=W for every label T. Summing over an optimum and taking its union yields 6 OPT_6<=11W. Since 11/6<137/70, the claimed at-most-two-set theorem follows as well. This paragraph supplies the whole single-set argument; the earlier frozen single-support files are not necessary dependencies of this proof.

If W=0, the same inequalities imply OPT_6=0; no ratio 0/0 is formed. Finite empty/duplicate labels and zero-client instances are therefore included.

## 5. Exact arithmetic audit and its limits

`audit_two_support.py` checks identity (4) on all16 one-client membership atoms of (A,B,T,S), using fractions.Fraction; by additivity this is an independent exact algebra check of the identity. It also checks every rational decomposition in Section 2 and (6), and enumerates all62 binary words to audit the case partition. Exact output is `two-support-audit.json`.

Reproduction from repository root:

    python research/workspaces/n6-boss3-20261118/independent/audit_two_support.py

The audit is not a finite SPE search or a substitute for the all-history proof: nonnegativity of the three slacks is established at the explicitly identified true histories above. No finite catalogue or client bound is assumed in the proof.

## Result and remaining obligation

The entire at-most-two-realized-coverage subclass satisfies the stronger inequality70OPT_6<=137W. Therefore any counterexample to the original half-coverage assertion must have at least THREE distinct realized coverage sets. The unrestricted six-person problem is not settled here. Next useful work would formulate an analogue of the three-slack identity for a prefix whose realized coverages are not all identical, or study a specified three-set arrangement; no such extrapolation is claimed.
