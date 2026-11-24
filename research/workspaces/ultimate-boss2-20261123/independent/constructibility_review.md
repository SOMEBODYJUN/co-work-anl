# Independent review of the constructibility addendum

Date: 2026-11-23. Reviewer role: independent obstruction worker.

Reviewed file: `research/workspaces/ultimate-boss2-20261123/informed-b/constructibility_addendum.md`.

Final reviewed SHA-256: `f54b7616c43790370ba62b78d5de85a509afbb2a8cd580f3eda6893ee26bbc29`.

Initial version also checked: `69079de0cf2c6f03501cc2ffc5be2b211dc9b306e8320fa634ae7ec900e391b7`. Its specific gap below has been removed from the final version.

Scope: the fixed-index coefficient grid, ordinary flop calculations, and the proposed deduction from fixed-volume numerical orbits to SQM finiteness. I inspected the current statements of Theorems 5.5 and 5.7 of Serebrennikov, *Constructibility aspects of the cone conjecture*, arXiv:2604.27303v2, <https://arxiv.org/html/2604.27303v2>. This is not an independent proof of that preprint's theorems.

## 1. Coefficient grid: valid

Choose compatible canonical divisors on a common smooth resolution. If \(r(K_X+B)\) is integral Cartier, its pullback is an integral divisor. Subtracting \(rK_W\) shows that the crepant boundary \(D\) on the resolution has all coefficients in \(r^{-1}\mathbb Z\). A coefficient of \(B_Y\) occurs on the strict transform of the corresponding divisor of \(Y\), so it belongs to the same grid. Effectivity and klt singularities restrict it to
\(\{0,1/r,\ldots,(r-1)/r\}\).

No claim about the Cartier index on \(Y\) follows or is needed here. This is a coefficient assertion, correctly stated for a fixed rational pair and its effective crepant klt models.

## 2. Ordinary flop: valid

With the ruling conventions in the addendum, \(p^*H|_E=\mathcal O(d,0)\), \(E|_E=\mathcal O(-1,-1)\), and \(q^*H'|_E\) has degree zero on the first ruling. This gives \(q^*H'=p^*H+dE\) and \(H'\cdot C'=-d\). The exceptional intersections are

\[
 (p^*H)^2E=0,\qquad p^*HE^2=-d,\qquad E^3=2.
\]

Expanding the cube gives \((H')^3=H^3-d^3\). The codimension-one identification of prime divisors on normal varieties identifies the spaces of rational sections in every degree, so \(\operatorname{vol}(H')=\operatorname{vol}(H)=H^3\). This section-space argument uses actual corresponding divisors, not mere numerical equivalence. The inverse flop followed by the original embedding is small onto its image; thus the transformed divisor is very movable as stated. The calculation correctly disproves the proposed transported-polarization shortcut.

## 3. Fixed numerical orbits to models: gap in the initial version

Theorem 5.7 in v2 assumes a projective klt pair with effective rational boundary and \(K_X+B\equiv0\). Its action is by the **coefficient-preserving** pseudo-automorphism group on classes in \(\mathrm{NS}(X)\), which is numerical equivalence. The addendum correctly checks that a transformed very ample divisor on a small model is Cartier on smooth \(X\), is big and very movable, and has the same positive integer volume.

The initial version's sentence “Two transforms in one orbit have isomorphic section rings” does not follow from the cited theorem: its orbit relation gives numerical equivalence, not an isomorphism of line bundles or section rings. A separate theorem or proof about uniqueness of small ample models for numerically equivalent big divisors would be needed for that route. This gap was sent to the author and Main. The final version explicitly rejects the shortcut and replaces that derivation by the bounded-polarization proof checked next.

## 4. A direct repair through bounded polarization

There is a different conditional proof using the already-cited Theorem 5.5. It avoids the numerical-class-to-section-ring inference.

Suppose every model \((Y,B_Y)\) in the fixed effective crepant klt class has a very ample Cartier divisor \(A\) with \(A^d\leq N\), where \(d\geq1\). Section 1 gives the same coefficient grid for all models, hence the divisor inequality

\[
 (B_Y)_{\mathrm{red}}\leq rB_Y.
\]

For \(d\geq2\), a general complete intersection \(C\) of \(d-1\) members of \(|A|\) is a smooth integral curve contained in the smooth locus of \(Y\): normality gives codimension at least two for the singular locus, and general hyperplanes miss that locus after this many intersections. For \(d=1\), use the smooth curve \(C=Y\). Adjunction along \(C\) gives

\[
 -K_Y\cdot A^{d-1}=(d-1)A^d+2-2g(C)
 \leq(d-1)N+2.
\]

Because \(K_Y+B_Y\equiv0\), and intersection degree is nonnegative on effective divisors against \(A^{d-1}\),

\[
 (B_Y)_{\mathrm{red}}\cdot A^{d-1}
 \leq rB_Y\cdot A^{d-1}
 =-rK_Y\cdot A^{d-1}
 \leq r\bigl((d-1)N+2\bigr).
\]

Thus the coefficient set, dimension, polarization degree, and reduced-boundary degree are uniformly bounded. This is the bounded-polarization hypothesis of Theorem 5.5, so its finiteness conclusion applies to the fixed crepant class. This conditional proof needs no smoothness assumption on the original \(X\); the smooth complete-intersection curve is enough for the intersection calculation. It is not a proof of any uniform bound \(N\), and supplies no relative statement or fundamental domain.

The final addendum has incorporated the complete argument in Section 4. I re-read the corrected final bytes, checked the positive-dimension restriction and the treatment of non-Q-factorial models by intersections near the smooth complete-intersection curve, and verified the final hash above. The coefficient grid, flop calculation, and repaired conditional finiteness statement are valid as written, assuming the externally cited Theorem 5.5. There is no remaining gap in those three checked arguments. The uniform very ample degree bound is still an explicit unproved hypothesis; no arbitrary-dimensional cone domain or relative finiteness is established.
