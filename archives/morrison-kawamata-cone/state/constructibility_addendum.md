# A bounded-polarization route for birational finiteness

Date: 2026-11-23. Execution/proof worker addendum. The earlier bridge report remains frozen.

No novelty claim. The conventional calculations below are reductions; the universal degree bound is unproved.

## Primary text and exact checked scope

Source: Daniil Serebrennikov, *Constructibility aspects of the cone conjecture*, <https://arxiv.org/html/2604.27303v2>, revised 5 October 2026. The revision notes a repaired gap. This check uses v2, not April's v1. The statements and the relevant proofs were read; this is not a complete independent certification of the preprint.

- Theorem 5.5: a crepant birational class of projective klt pairs with effective rational boundary and numerically trivial log canonical divisor has finitely many log isomorphism classes, provided it admits bounded polarization.
- Definition 2.11: dimension is fixed, boundary coefficients lie in one finite set, and each pair has a very ample Cartier divisor A with both A^d and B_red·A^{d-1} uniformly bounded. For zero boundary only A^d remains.
- Theorem 5.6: for one such pair, numerical ample Cartier classes of any fixed positive integer volume have finitely many orbits under coefficient-preserving Aut.
- Theorem 5.7: the corresponding fixed-volume orbit assertion holds for big **very movable** Cartier classes under coefficient-preserving PsAut. Here the complete linear system map must be small onto its image.

The assertions have no dimension bound. They are absolute. They neither assert rational polyhedral fundamental domains nor include all effective boundary classes.

## A precise numerical target to investigate

For a fixed crepant birational class of absolute projective klt rational Calabi–Yau pairs, define

\[
 p(X_i,B_i)=\min_{A\;\text{very ample Cartier}} A^d.
\]

The minimum exists because the displayed set is a nonempty set of positive integers. The concrete outstanding boundedness problem is

\[
 \sup_i p(X_i,B_i)<\infty.
\]

The coefficient-grid argument below, followed by the adjunction calculation in the last section, makes this scalar bound sufficient for the exact bounded-polarization definition and thus for absolute log isomorphism finiteness. Finite log isomorphism classes also imply the bound by choosing one very ample divisor on each representative, so this is an exact numerical reformulation of this finiteness question, not a reduction in logical strength. Its potential advantage is that one may try to bound embedding degrees geometrically without constructing a polyhedral domain first. It proves neither nef nor movable fundamental domains, and no relative analogue is supplied here.

For a fixed rational pair the coefficient condition can in fact be verified separately. Choose r>0 such that r(K_X+B) is an integral Cartier divisor. On a common smooth resolution g:W to X of a crepant model h:W to Y, crepancy gives

\[
 r(K_W+D)=g^*r(K_X+B)=h^*r(K_Y+B_Y).
\]

The right-hand divisor obtained from X and rK_W are integral, so rD is integral. The coefficient of D along the strict transform of a divisor of Y is its coefficient in B_Y. Thus every effective klt B_Y has coefficients in the finite set

\[
 \{0,1/r,2/r,\ldots,(r-1)/r\}.
\]

This argument concerns coefficients; it does not assert that r(K_Y+B_Y) is Cartier on Y. Extracted models may introduce coefficients outside the original list, but not outside the displayed finite grid. Theorems about relative minimal models and contraction targets still need further arguments.

## A worked test: fixed volume survives a flop while ampleness fails

Suppose X and Y are smooth projective threefolds related by an ordinary flop of a smooth rational curve C with normal bundle O(-1) plus O(-1). Let p:W to X be the blow-up of C, with exceptional E isomorphic to P^1 times P^1, and q:W to Y contract the other ruling. Let H be a very ample Cartier divisor on X, put d=H·C>0, and let H' be its strict transform on Y. Let C' be the flopped curve.

The restrictions to E are

\[
 p^*H|_E=\mathcal O_E(d,0),\qquad
 \mathcal O_E(E)=\mathcal O_E(-1,-1).
\]

Pullbacks by q have degree zero on its contracted ruling. Comparing restrictions therefore gives

\[
 q^*H'=p^*H+dE,\qquad H'\cdot C'=-d<0.
\]

Thus the same strict transform is not nef, let alone very ample. This is an exact local intersection calculation whenever such a projective ordinary flop is present; no assertion is made that an arbitrary Calabi–Yau contains such a curve.

The codimension-one isomorphism identifies rational sections of corresponding Cartier divisors. For every positive integer m,

\[
 H^0(X,mH)\cong H^0(Y,mH'),\qquad
 \operatorname{vol}_Y(H')=\operatorname{vol}_X(H)=H^3.
\]

In particular, fixed birational volume does not turn the strict transform of one chosen polarization into a polarization on every model. Its complete linear system gives the inverse flop followed by the original embedding, so it is very movable. Even its top self-intersection changes:

\[
 (p^*H)^2E=0,\quad p^*H E^2=-d,\quad E^3=2,
 \qquad (H')^3=H^3-d^3.
\]

The inequality of cubic intersection and volume is consistent because H' is not nef. Confusing the two would create a false boundedness proof.

This cuts off the attempted shortcut “choose one ample H on X, transport it to every model, and use its fixed volume to apply bounded-polarization finiteness.” The missing step is selecting actual very ample divisors of uniformly bounded degree on all the models; strict transform alone does not accomplish it.

## What fixed-volume orbit finiteness can and cannot contribute

**Proved conditional corollary.** Let (X,B) be a fixed projective klt rational Calabi–Yau pair of positive dimension d. Let C be any class of effective projective klt pairs (Y,B_Y) crepant birational to (X,B). Assume that there is an integer N such that every Y admits a very ample Cartier divisor A_Y with A_Y^d at most N. Then C has finitely many log isomorphism classes, using Theorem 5.5 as the external literature input.

**Proof of the bounded-polarization implication.** The earlier common-resolution argument places every boundary coefficient in one grid with denominator r, where r(K_X+B) is Cartier. For a given Y, choose d-1 sufficiently general members of the very ample linear system. Their complete intersection curve C_Y is smooth and integral and misses the singular locus of the normal variety Y: the latter has codimension at least two. Successive Bertini theorems give smoothness along the intersection. For d=1, take C_Y=Y, which is already a smooth projective curve. Adjunction near the curve gives

\[
 2g(C_Y)-2=(K_Y+(d-1)A_Y)\cdot A_Y^{d-1}.
\]

All intersections involving K_Y here can be computed on the smooth neighborhood of C_Y; the curve avoids the singular locus. Because K_Y+B_Y is numerically trivial,

\[
 B_Y\cdot A_Y^{d-1}
 =-K_Y\cdot A_Y^{d-1}
 =(d-1)A_Y^d+2-2g(C_Y)
 \leq(d-1)N+2.
\]

Every nonzero coefficient of B_Y is at least 1/r. Positivity of the degrees of prime divisors against A_Y^{d-1} consequently gives

\[
 (B_Y)_{\mathrm{red}}\cdot A_Y^{d-1}
 \leq r B_Y\cdot A_Y^{d-1}
 \leq r((d-1)N+2).
\]

Thus one finite coefficient set and the uniform bound max{N,r((d-1)N+2)} satisfy Definition 2.11 exactly. Theorem 5.5 yields the stated finiteness. No smoothness of Y or uniform Cartier index on Y was assumed. \(\square\)

This includes extracted crepant models with effective boundary; it is still an absolute finiteness result and does not preserve a specified base morphism. The missing geometric input remains the uniform very ample degree bound.

**Rejected shortcut.** Theorem 5.7 concerns orbits of *numerical* classes. From two divisors lying in one such orbit one cannot directly conclude that their section rings are isomorphic: numerical equivalence does not imply linear equivalence. An initial version of this addendum used that unjustified implication; the independent reviewer caught it. The adjunction proof above replaces it completely and does not use that implication.

Finally, for every individual positive integer n, finiteness on the slice of volume n gives no uniform information as n tends to infinity. Even on an elliptic curve, numerical ample classes are indexed by their positive degree: each fixed-degree slice has one class, while the union over degrees is infinite. This does not give infinitely many minimal models; it diagnoses precisely the quantifier error in replacing a uniform bound by separate fixed-volume finiteness assertions.

**Current result:** a checked recent literature input and an exact candidate boundedness obligation, together with the flop calculation rejecting an attempted proof of that obligation. Full A+B+C remains open in this work.
