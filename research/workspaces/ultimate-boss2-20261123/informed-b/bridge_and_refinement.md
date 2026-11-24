# Dimension-free bridge calculations and version audit

Author role: execution/proof worker. Date: 2026-11-23.

Status: proved elementary reductions and an independent review of the obstruction worker's exact text. No proof of the full geometric mission and no novelty claim.

## 1. The exact Li 2023 version being used

The inspected primary text is Zhan Li, arXiv:2309.04673v1, 9 September 2023, <https://arxiv.org/html/2309.04673v1>. Its Conjecture 1.1 concerns `Mov_+`, `Amp_+`, and “(weak)” domains. Section 2 assumes connected fibres and Q-factorial X; its groups preserve boundary support. Theorems 1.3, 1.4 and 1.8 assume terminality, good minimal models in relative dimension, and a generic polyhedral covering. Their respective outputs include rational movable coverage, model finiteness, and a weak domain. Theorem 1.5 has a klt hypothesis and an additional relative covering hypothesis. Section 5 constructs neutral-group translations and handles vertical classes; it does not prove the nef part of Conjecture 1.1. Definition 3.3 permits setwise stabilizers for weak domains and excludes them for domains. No equality of an effective intersection with a rational hull is automatic.

AMS-indexed primary journal metadata records a later paper with the same title: DOI <https://doi.org/10.1090/jag/864>, electronically published 24 August 2026, J. Algebraic Geom. 36 (2027), 1–50. The final PDF could not be retrieved in this check; the author's public publication list still points to arXiv. **A theorem-by-theorem comparison with that final text is incomplete.** The 32-page arXiv text must not be represented as a checked copy of the 50-page final article. Secondary metadata uses “weak log canonical models”; that wording alone is not a verified final theorem.

For exact arithmetic notation, put

\[
 C_M^e=\overline{\operatorname{Mov}}(X/S)\cap\operatorname{Eff}(X/S),
 \qquad
 C_N^e=\operatorname{Nef}(X/S)\cap\operatorname{Eff}(X/S),
\]

whereas the source's plus constructions are

\[
 \operatorname{Mov}_+=\operatorname{Conv}
 (\overline{\operatorname{Mov}}\cap N^1(X/S)_{\mathbb Q}),
 \qquad
 \operatorname{Amp}_+=\operatorname{Conv}
 (\operatorname{Nef}\cap N^1(X/S)_{\mathbb Q}).
\]

These four symbols are retained separately. The mission's effective versions and Li's 2023 plus versions are separate proof obligations.

## 2. A finite-index covering lemma

**Lemma.** Let V be a finite-dimensional rational vector space extended to the reals. Let C be a convex cone, invariant under a group G of rational linear automorphisms. Suppose P is a rational polyhedral subcone of C and GP=C. If H is a subgroup of finite index in G, there is a rational polyhedral subcone Q of C satisfying HQ=C.

**Proof.** Choose finitely many right coset representatives g_1,...,g_m, so G is the union of H g_i. Set

\[
 Q=g_1P+\cdots+g_mP.
\]

Each summand is rational polyhedral, hence so is their Minkowski sum. As C is a convex cone, Q is contained in C. It contains every g_iP because each cone contains zero. Thus

\[
 C=GP=\bigcup_i H(g_iP)\subset HQ\subset C.
\]

The equalities prove the claim. No pointedness or dimension restriction was used. \(\square\)

This lemma supplies a **covering**, not separation of translates. Taking the convex hull of several translated domains can introduce overlaps. A passage from a cover to a strong fundamental domain requires a separate theorem with its hypotheses checked.

**Boundary-group consequence.** Suppose a birational group G preserves the finite set of r components of Supp Delta. Its subgroup G_coeff preserving Delta contains the kernel of the permutation homomorphism G to the symmetric group on those components. Hence [G:G_coeff] is finite. The lemma transfers rational polyhedral *coverings* from G to G_coeff whenever the cone is invariant. It does not silently transfer a strong fundamental domain. Replacing a boundary by another with the same support preserves the support group exactly; it can change the coefficient group.

## 3. An exact obstruction to upgrading rational coverage

Let

\[
 A=\begin{pmatrix}2&1\\1&1\end{pmatrix},\qquad
 v=(1,0),\qquad \phi=(1+\sqrt5)/2,
\]

and put u_+=(phi,1), u_-=(1,-phi). These are eigenvectors of A with eigenvalues lambda_+=phi^2 and lambda_-=phi^{-2}. Define

\[
 C=\mathbb R_{\geq0}u_++\mathbb R_{\geq0}u_-,
 \qquad P=\mathbb R_{\geq0}v+\mathbb R_{\geq0}Av,
 \qquad G=\langle A\rangle.
\]

The closed convex cone C is G-invariant. P is rational polyhedral and lies in its interior except at zero. Write v=a u_++b u_-, where a=phi/(phi^2+1)>0 and b=1/(phi^2+1)>0. For an interior vector x=s u_++t u_- use the positive coordinate ratio r=s/t. The interval of ratios occurring in A^nP is

\[
 [\phi(\lambda_+/\lambda_-)^n,
   \phi(\lambda_+/\lambda_-)^{n+1}].
\]

These intervals, for n in Z, cover all positive real ratios. Therefore

\[
 GP=\operatorname{Int}_V C\ \cup\{0\}.
\]

Neither boundary ray of C contains a nonzero rational vector: the coordinate ratios of u_+ and u_- are irrational. Consequently GP contains every rational point of C. Nevertheless it omits every nonzero point on both boundary rays. Thus

\[
 G(P\cap V_{\mathbb Q})=C\cap V_{\mathbb Q}
 \quad\not\Longrightarrow\quad GP=C.
\]

The action preserves Z^2 and is faithful. This is an exact convex counterexample to an invalid inference, not a counterexample to the geometric effective cone conjecture. Here C_+=Int C union {0}: every real interior vector is a positive combination of two rational interior vectors on opposite sides of its ray, while neither extreme ray contributes a nonzero rational point. Adjoining the irrational boundary changes the target.

## 4. Independent review of the finite-stabilizer and lifting arguments

I read `../independent/cone_obstructions_and_lifting.md`, Sections 1–5. The following are valid with precisely the hypotheses written there.

1. In the shear example, every point in the lineality subspace is fixed, so coverage forces the entire subspace into a convex candidate domain. One positive-height point then forces the whole half-plane; strong separation fails. The example does not assert a geometric realization.
2. A full-dimensional weak rational polyhedral domain D with finite stabilizer H can be cut by a rational linear functional with trivial H-stabilizer. The finite maximum on each orbit gives coverage. Strict inequality in the interior, compared against the inverse element, gives separation against the *whole* translated cone. Full dimension follows because finitely many lower-dimensional polyhedra cannot cover D. Faithfulness and full dimension are necessary to the generic-functional argument as written.
3. The quotient lift assumes explicitly that K is finite and D=C intersect p^{-1}(Q) is rational polyhedral and full-dimensional. Since p(D)=Q and p is open, p(Int D) is contained in Int Q. This proves separation outside K; the preceding finite cut handles K. There is no covert assumption that C is pointed.
4. The rank-one irrational positive-semidefinite matrix on E^2 is an extreme irrational ray. No rational polyhedral nef subcone can contain it, so all closed nef coverage is too strong. Its failure of effectiveness prevents it from refuting the mission.
5. The mixed Poincare class on E^2 over E is globally nonzero but relatively numerically zero under curve-tested equivalence. The proposed use as an invisible nonzero *relative* class was correctly rejected.

This is an independent check of these elementary proofs, not a review of every theorem in either geometric manuscript or a substitute for external expert review.

## 5. Why the old relative-dimension-two mechanism does not prove the new mission

The inspected local source is `archives/relative-mk-cone/state/strong-rel2/informed-b/proof.md`, in particular Sections 1–6, together with the stated assumptions of the companion operator argument.

| Old step | Dependence that needs a replacement in arbitrary dimension |
| --- | --- |
| Geometric smoothness of the generic fibre | Terminal singularities have codimension at least three; this excludes generic singularities only when relative dimension is at most two. |
| Generic pseudo-automorphisms are automorphisms | On smooth surfaces a map that contracts no curve in either direction is regular. Higher-dimensional flops prevent this inference. |
| Restrict a movable class and conclude nefness | Movable divisors on surfaces are nef; the analogous statement fails in higher dimension. |
| Effective nef classes decomposed using their finite support | Distinct effective prime curves on a smooth surface have nonnegative intersection. The resulting finite inequalities do not describe higher-dimensional nefness. |
| Good models for all required effective perturbations | Surface abundance supplies the old input. A universal higher-dimensional good-model assertion is not established here. |
| All irregularity handled by q=0,1,2 | The classification uses a curve or surface fibre; in the q=2 branch the fibre becomes an abelian surface torsor. A higher-dimensional fibre with q=2 need not be such a torsor. |
| Numerical generic covering | Totaro supplies the surface benchmark. There is no corresponding arbitrary klt Calabi–Yau theorem proved in this work. |
| One global family of positive-semidefinite translation operators | Its realization on the actual Picard quotient, including all effective boundary classes, is established only in the old branches. The abstract operator lemma does not supply the geometric realization. |

The finite-stabilizer refinement and the finite-kernel quotient lift themselves are dimension-free. Their *geometric hypotheses* are where the old argument uses its restricted scope.

## 6. Exact conditional conclusion and the unpaid hypotheses

For any dimension, suppose the actual effective movable cone C, its faithful actual pseudo-automorphism image Gamma, and a rational invariant quotient p satisfy all three conditions in Section 3 of the independent report: finite kernel, a strong quotient domain, and rational polyhedral full-dimensional inverse intersection. Then the proof there constructs a strong rational polyhedral domain for C. This is the strongest dimension-free lifting statement checked here.

This conditional theorem does not imply the mission by itself. Its still-unproved universal inputs are:

- A quotient covering and separation supplied by the actual generic automorphisms or pseudo-automorphisms, rather than an enlarged geometric group.
- Finite-kernel control and polyhedral intersection in every degenerate and irregular case.
- Effective-boundary control, so neither a rational-point cover nor a plus-cone statement is silently enlarged.

Even after movable coverage, separate model-geography hypotheses are needed to infer nef-domain and birational/contraction finiteness conclusions. No combination of the elementary reductions removes the unresolved arbitrary-fibre cone problem. In the absolute case S is a point, so a claimed universal generic-to-relative bridge does not eliminate that case at all.

There is no claim that a unique smallest missing theorem has been isolated. A full proof must pay a geometric covering input and the model/boundary transfer inputs; calling that package one lemma does not reduce its mathematical content.

## 7. Reducing finite vertical kernel to a finite chamber orbit

**Lemma.** Let Gamma be a faithful linear group on a finite-dimensional real space V, and let T be invariant. Put K=ker(Gamma to GL(V/T)). Suppose:

1. The image of K in GL(T) is finite.
2. There is a full-dimensional closed pointed convex cone N in V whose orbit under K is finite.

Then K is finite.

**Proof.** Let K_T be the kernel of the action of K on T, and let K_N be the stabilizer of N in K. Both have finite index by the two hypotheses. Hence their intersection H has finite index in K. For h in H, write u=h-I. Triviality on V/T implies u(V) is contained in T; triviality on T implies u(T)=0. Thus u^2=0, and

\[
 h^n=I+nu\qquad(n\in\mathbb Z).
\]

For every x in N and each positive integer n, preservation of N gives

\[
 n^{-1}h^n x=n^{-1}x+ux\in N,
 \qquad
 n^{-1}h^{-n}x=n^{-1}x-ux\in N.
\]

Closedness yields both ux and -ux in N on taking limits. Pointedness implies ux=0. Since N is full-dimensional it spans V, so u=0 and h=I. Thus H is trivial. A group with a trivial subgroup of finite index is finite, proving the lemma. \(\square\)

For a relative numerical space, the relative nef cone is pointed: a divisor class nef with both signs has zero intersection with every contracted curve, and is therefore zero by definition. It is full-dimensional because it contains the relatively ample cone. Thus the substantive extra input in this lemma is a **finite orbit of marked nef cones** under K, not pointedness of the movable cone. This separates a model-geography obligation from the subsequent elementary group argument. The finite chamber-orbit hypothesis is not asserted in arbitrary dimension here.
