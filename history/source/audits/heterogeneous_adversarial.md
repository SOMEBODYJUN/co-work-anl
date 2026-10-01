# Independent adversarial audit of the universal factor-2 proof

Date: 2026-09-30. Auditor: adversarial_audit. The source proof and implementation were read without relying on the conclusions of existing team audit files. No source file was changed.

## Scope and verdict

Primary source: `universal_two.md`, SHA-256 `462ffcadb38fdc0841eb273915a61c0f757e3e84c5291681003b5d844c577b64`.

Implementation spot check: `r_menu_solver.py`, SHA-256 `3c122793bf5c0a698bbc258ab2e178e1f81b525d209715f2fa963694b8785e4e`.

**Verdict: no mathematical gap or counterexample found in the universal factor-2 existence argument.** All seven sections pass the adversarial checks below under the customer-game definition in `paper/main.tex`: covered customers must use an accessible facility, there is no outside option, and a customer's cost is that facility's realized total customer weight, including its own weight. This audit does not independently establish the matching lower-bound family or a publication-priority claim.

The strongest issue found in the requested Markdown source is expository: it calls itself self-contained but does not explicitly state those customer-cost and participation conventions. They are explicit in the manuscript's model section. Adding them to the standalone note would remove this ambiguity; no change to the proof is required.

## 1. Pure repair: passed

Write the current higher and lower loads as P and Q, with gap g=P-Q>0. A common customer of weight w on the higher side strictly improves exactly when w<g. Its move creates loads P-w and Q+w, each strictly between the previous two loads.

Before the first reversal, only original higher-side customers move. The gap decreases. Any customer eligible at a later step was eligible at the earlier step, so choosing a largest eligible weight makes the sequence of moved weights nonincreasing.

At a reversal caused by w, the new absolute gap is 2w-g<w. Earlier moved customers have weight at least w. Original lower-side common customers have weight at least the initial gap, which is at least the pre-move gap. Thus every common customer on the new higher side is stable. Customers left on the other side are now on the lower side and are stable. A load tie is also immediately stable.

If no reversal occurs, the original lower-side customers remain on the lower side, and stopping because no original higher-side customer strictly improves is precisely the pure Nash condition. No customer moves twice; the original lower side never loses load.

An all-common-on-one-side seed either is already a pure NE or has an empty original lower-side common set, so its repair is valid. The finite menu is therefore nonempty. The strict-improvement test must remain w<g, not w<=g. The implementation uses the correct strict test.

## 2. Continuation selection and deviation payoffs: passed

At an on-path labeled pair (s,t), a first-facility deviation produces (r,t), and its selected payoff is the first facility's load in the chosen minimizing continuation. This equals u(r,t), which is at most D(t). The second facility's deviation is handled by the other load coordinate and D(s). The two on-path quotas therefore imply both factor-2 deviation inequalities.

The two families of nontrivial unilateral-deviation profiles are disjoint. Their only possible intersection would have r=s and the second deviating action equal to t, which is the excluded on-path pair. There is no requirement to minimize both facilities' payoffs at one off-path profile.

The proof uses one common finite menu per labeled pair for both payoff minima. It does not identify a pure-menu minimum with a minimum over all independent mixed equilibria. A menu minimum may be larger, but the construction actually selects that pure continuation, so its deviating payoff is exactly the quantity bounded in the proof.

Pure deviation bounds also cover independently mixed facility deviations: with the opponent's location fixed and the continuation selection fixed, a mixed deviation produces a convex combination of the corresponding pure-deviation payoffs.

## 3. Colored copies and co-location: passed

The graph vertices are facility actions, including their colors. Two colors at the same physical site are distinct vertices with identical accessible customer sets. A legal layout remains an ordered facility-action pair, even at co-location.

This distinction preserves alternating cycles, the legality of opposite-color chords, and the disjointness of the two unilateral-deviation families. No strict inequality in the argument assumes distinct physical sites or distinct coverage sets.

The implementation's response-graph nodes are `(color,site)`. Its continuation table is keyed by ordered `(s,t)` with s in U1 and t in U2. It uses separate response maps for the two colors. Therefore shared physical site identifiers are not incorrectly collapsed.

## 4. Selected response cycles and heavy customers: passed

On a selected edge s->t, the same menu supplies both the responder's guaranteed minimum D(s) and the incumbent's strict failed-quota inequality. A two-cycle is immediately impossible under the failed-quota assumption. A zero maximum D on a selected cycle is also directly handled without division.

For positive normalization, choosing a responder-minimizing witness gives R_s<=V_st<D(s)+D(t)/2<=3/2. A customer weighing at least 1/2 visible at a cycle vertex must be visible at the next vertex, since otherwise it would be forced onto an incumbent with load strictly below 1/2. It therefore propagates around the cycle.

For the single-H seed, Q0=R_s-S and P0=R_t-H are the correct loads, with Q0>=H. If R_t>=Q0 and Q0>=P0, the H-customer's pure Nash inequality is Q0<=P0+H=R_t; the seed is stable. If Q0<P0, then P0-Q0<3/2-2H<=H, so the guarded repair applies and preserves at least H on the incumbent. Both outcomes contradict the failed quota. The resulting strict reach decrease around the cycle is impossible.

Consequently every customer visible on the cycle has weight strictly below 1/2, including equality-boundary cases in the original supposition.

## 5. Transferred batch and arbitrary-length Case 1: passed

At A->B the load gap exceeds 1/2. Purity and the preceding weight bound exclude every common customer from B. Thus L_A=R_A<b/2 and the private set E=C_B\C_A has weight at least 1. The last response edge gives e<=R_A<b/2 and weight(C_F\C_A)<1/2.

For X, the E-customers assigned to C at B->C, weight(X)>1-c/2>=1/2. Every x in X satisfies w_x>=L_C-L_B>b-c/2=h. Since X is disjoint from C_A, it cannot be contained in C_F. Thus the legal C--F chord gives z=weight(C_C\C_F)>h and z<=e, implying c>2b-2e>2e and c>b.

In Case 1, z>h>=e/2 forces the C quota at layout (C,F). Failure of the simultaneous quotas forces every menu witness's F load below c/2. A C-minimizing pure witness also gives C load at most e<c/2. Since every covered customer is assigned wholly to one facility, every customer visible at C or F has weight below c/2.

The extension to the full A-colored catalog is valid and essential. For any action s of that color, weight(C_s\C_F)<=D(F)=e uses a full-catalog maximum. A customer at s weighing at least c/2>e would have to belong to C_F, a contradiction. Thus all common customers at all legal layouts have weight below c/2. No bound on customers exclusive to the opposite color is needed.

The subsequent induction works through both colors and cycles of every even length. Its hypotheses D(s)>=c and R_s>=c/2 pass to a successor unless D(t)<=c; that alternative would create a gap exceeding c/2 and force all s-customers to remain at s, contradicting R_s>=c/2. Reaching F contradicts e<c/2. For a four-cycle, the possible coincidence G=C causes no problem.

## 6. Arbitrary-length Case 2: passed

From h<e/2 and b>2e, one gets c>2b-e>3e, hence e<1/3. If g>=(1+e)/2, the G->F load gap exceeds 1/2, giving R_G<e/2. The legal B--G chord then yields g>1-e/2, while the response edge and the reach estimate give g<=R_F<e+1/2. Together these would require e>1/3. Thus g<(1+e)/2 and g+e<1.

The set inclusion E intersect C_G subset (C_G\C_F) union (C_F\C_A) is correct. Both private-set weights have the strict upper bounds used in the source, so weight(C_B\C_G)>(1-e)/2>g/2.

The B quota is consequently forced at (B,G). Choosing a B-minimizing menu witness gives 1<=R_B<=V_BG<g+b/2<(1+e+b)/2. Hence b>1-e and c>2b-e>2-3e>1, contradicting the normalized maximum. No division by e, g, b, or c is used; the zero-D edge cases do not invalidate this case.

## 7. Implementation refinements checked

The solver searches only the cross-product of a selected response cycle's two color classes. The proof supports this stronger search restriction: all layouts at which failed simultaneous quotas are invoked are cycle edges or the two cycle-vertex chords. The extension to actions outside the cycle in Case 1 uses only the unconditional private-load inequality and the original full-global D(F). Thus one need not assume failed quotas at off-core layouts.

The solver defaults to four seeds, retaining only a largest common customer as the designated singleton, whereas the standalone note states the larger all-singleton menu. This smaller menu is also justified by the proof, but the justification should be stated explicitly if this default is claimed from the note. If a cycle-visible customer of weight at least 1/2 exists, every edge has such a common customer. At each edge choose the largest common customer H_e. Its weight is at least 1/2, and the same single-seed reach-decrease argument applies edge by edge. The identities of H_e do not need to coincide around the cycle. The remaining proof never requests another singleton seed.

The implementation's verifier recomputes pure Nash inequalities and uses the actual deviator's load coordinate. Its default off-path continuation, repair of the all-first seed, is always well-defined by the menu nonemptiness argument.

## 8. Independent finite checks

A fresh integer implementation of the guarded repair and all-singleton menus was written for this audit in an execution cell; it did not call the existing solver or read existing verification reports. Every retained output was checked directly against every common customer's pure Nash inequality. Every selected quota witness was checked against the actual minimum-load continuation payoff for each unilateral deviation.

Coverage:

- All 27 ordered three-customer weight vectors in {1,2,3}^3, and all 4,096 ordered 2-by-2 catalogs of customer reach sets for each weight vector: 110,592 games.
- All 65,536 ordered 2-by-2 catalogs for four customer weights (1,2,4,7).
- 10,000 seeded random games with six customers, positive integer weights in [1,30], and 3 through 6 actions per facility. Random seed: 30092026.

Totals: **125,850 distinct local menus checked; 186,128 games checked; zero failures.** Catalog enumeration permits repeated coverage sets and empty reaches, so coverage aliases, zero-load boundaries, and possible colored co-location are included. These checks support the audit but do not replace the all-cycle proof above.

## Final disposition

The universal factor-2 upper bound passes this independent adversarial audit. Recommended edits are limited to explicitly stating the standalone model and documenting the already valid cycle-core and largest-singleton implementation refinements. The lower bound and literature-priority assessment remain separate claims requiring their own evidence.
