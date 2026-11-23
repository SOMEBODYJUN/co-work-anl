# Strong relative effective movable domains in relative dimension at most two

## Geometric hypotheses

Work over \(\mathbb C\). Let \(f:(X,\Delta)\to S\) be any terminal Calabi–Yau fibre space in the terminology of Li–Zhao. Thus the total space is normal, projective and \(\mathbb Q\)-factorial, the base is normal quasi-projective, the morphism is a projective contraction and \(K_X+\Delta\equiv_S0\). The terminal condition concerns the pair. Allow every effective real boundary in this definition. Assume \(r=\dim X-\dim S\) belongs to \(\{0,1,2\}\). In \(V=N^1(X/S)_\mathbb R\) use numerical equivalence on all complete curves contracted by \(f\). Put
\[
 C=\overline{\operatorname{Mov}}(X/S)\cap\operatorname{Eff}(X/S),\qquad
 \Gamma=\operatorname{im}\big(\operatorname{PsAut}(X/S,\Delta)\longrightarrow
 \operatorname{GL}(V)\big).
\]
Here the relative pseudoautomorphisms act over the identity on \(S\) and preserve \(\operatorname{Supp}\Delta\), in the sense of Li–Zhao. Let \(T\subset V\) be the span of the classes of all vertical prime divisors, and write \(p:V\to L=V/T\) for the quotient.

Section 1 of the complete proof constructs a rational terminal working boundary \(\Delta_0\) with the same support. It pays the real perturbation's ordinary relative Kodaira-dimension condition by an integral floor identity. Both \(C\) and the full \(\Gamma\) above are identical for the working and original pairs.

## Realization on the generic Picard group

For \(r>0\) and \(\dim X\ge2\), let \(F\) be the generic fibre over \(k=\mathbb C(S)\) and let \(R=N^1(F/k)_\mathbb R\) be the numerical space of actual \(k\)-line bundles, after extension of scalars. The map taking a generic divisor to its horizontal closure induces a surjection \(e:\operatorname{Pic}(F)_\mathbb Q\to L_\mathbb Q\). Its kernel \(J\) lies in \(\operatorname{Pic}^{0}(F)(k)_\mathbb Q\), using the natural identification of rationalized line bundles and rationalized points of the Picard scheme. For \(U_\mathbb Q=\operatorname{Pic}^{0}(F)(k)_\mathbb Q/J\) the resulting rational exact sequence is
\[
 0\longrightarrow U_\mathbb Q\longrightarrow L_\mathbb Q
 \xrightarrow{\pi} R_\mathbb Q\longrightarrow0.
\]
The cone \(p(C)\) consists exactly of the images of the effective real Picard classes of \(F\) having nef numerical class. Its image in \(R\) is \(D=\operatorname{Nef}(F/k)\cap\operatorname{Eff}(F/k)\). The image on \(R\) of the specified relative group has a strong rational polyhedral domain \(B\subset D\). When \(U=0\), \(p(C)\) identifies with \(D\) under \(\pi\).

When \(U\ne0\), the following assertions hold together. There exist a rational linear section \(s:R\to L\), a rational linear map \(d\mapsto T_d\in\operatorname{End}(U)\), and a rational positive definite scalar product on \(U\). For the generic numerical class \(H\) of a relatively ample integral divisor, \(T_H=I\). The operators on \(D\) are self-adjoint and positive semidefinite. For a finite set of rational generators of \(B\), a positive combination of their operators is positive definite. For every real \(d\in B\), including all faces,
\[
       p(C)\cap\pi^{-1}(d)=s(d)+\operatorname{im}T_d .
\]
Put \(G=\operatorname{im}(\Gamma\to\operatorname{GL}(L))\), and let \(G_0\) be its kernel on \(R\). A full lattice \(\Lambda\subset U\) is realized as a normal subgroup of finite index in \(G_0\), acting by \(x\mapsto x+T_{\pi x}z\) for \(z\in\Lambda\). This statement concerns the faithful image of the full relative group and the real effective fibres. It specifies neither a splitting of \(G_0\) nor a finite kernel for the projection onto generic numerical classes.

For the numerical chamber over the generic field, Section 2 uses Totaro’s complex surface theorem and descends it through a finite Galois-stable subset of the Albanese torsor. The descent yields genuinely field-defined automorphisms and rational effective generators. The finite-index lifting by pluricanonical forms supplies the actual relative-group image.

The proof is in Sections 2–6 of the [complete proof](strong-rel2/informed-b/proof.md). The cases with \(r=0\) or \(\dim X\le1\) are treated in Section 1. A zero-dimensional relative fibre induces the trivial birational automorphism group over \(S\) and \(V=T\). For a contraction of absolute dimension at most one the possible relative numerical spaces and effective cones are zero or the degree line and its nonnegative ray.

## Strong relative movable-cone theorem

For **every** fibre space satisfying the geometric hypotheses, there exists one rational polyhedral cone \(\Pi\subset C\) such that
\[
 C=\bigcup_{\gamma\in\Gamma}\gamma\Pi,\qquad
 \gamma\Pi\cap\operatorname{Int}(\Pi)=\varnothing
 \quad\text{for every }\gamma\in\Gamma\setminus\{1\},
 \qquad
 \operatorname{Stab}_\Gamma(\Pi)=\{1\}.
\]
The interior is taken in \(V\); the covering cone \(\Pi\) has full dimension there, with the usual convention for \(V=0\). This is the strong condition of Li–Zhao, Definition 3.4, including separation from each entire translated closed cone. There is no assumption on the absolute dimension of \(X\), on \(\mathbb Q\)-factoriality of \(S\), on the type of a positive-dimensional generic fibre, or on pointedness of \(\overline{\operatorname{Mov}}(X/S)\).

For the proof apply the realization theorem above in positive relative dimension. In the case \(U\ne0\), the [operator domain construction](projected_operator_domain.md) gives the strong chamber on the actual image \(p(C)\). In the case \(U=0\), the chamber \(B\) gives it directly. In relative dimension zero the chamber on \(p(C)=0\) is \(\{0\}\). The [vertical kernel and lifting theorem](vertical_kernel_and_domain_lift.md) then gives the strong chamber for all of \(\Gamma\) on \(C\) in the klt cases. The elementary absolute-dimension cases from Section 1 cover any low-dimensional terminal convention. The [complete proof](strong-rel2/informed-b/proof.md) gives the geometric verification and all exceptional cases. Its [operator proof](strong-rel2/informed-a/operator_domain_v1.md) contains the finite-inequality construction used on singular faces.

### Applying the three conclusions across all dimensions

1. **Absolute dimension at most one.** For \(V=0\) take \(\{0\}\). For a curve over a point the numerical group acts trivially on the degree line, so its nonnegative ray is the required cone. These arguments also cover any coefficients permitted only by the low-dimensional terminal convention.
2. **Positive absolute dimension and relative dimension zero.** A contraction is birational and every divisor is vertical, so \(L=0\) and the relative birational group is trivial. In absolute dimension at least two the terminal pair is klt. The effective polyhedral-intersection part of the vertical theorem applies to \(V=T\subset\operatorname{Eff}(X/S)\) and gives polyhedrality of \(C\).
3. **Relative dimension one or two, \(\dim X\ge2\), and \(U=0\).** The realization identifies \(p(C)\) with \(D\) equivariantly for the actual numerical images. Its strong chamber \(B\) transfers to \(p(C)\); the vertical theorem gives the asserted chamber for \(\Gamma\) on \(C\).
4. **Relative dimension one or two, \(\dim X\ge2\), and \(U\ne0\).** The realization gives the exact rational sequence, countable faithful action, full-dimensional cone and strong base chamber. Its rational section, PSD operators, definite combination, normalization and finite-index normal lattice meet all the operator theorem's assumptions. In particular for a *real* point of each boundary face the fibre is precisely \(s(d)+\operatorname{im}T_d\), also when \(T_d=0\). The operator theorem therefore yields a strong rational polyhedral chamber on \(p(C)\). The vertical theorem establishes effective polyhedral lifting, coverage and finite stabilizer for the full inverse-image action, and removes the latter by finite covector comparison.

In cases 2–4 the low-dimensional good-model hypothesis of the vertical theorem holds by abundance in relative dimension at most two, as verified in Section 1 of the complete proof. The finite holonomy and the finite kernel in the last case are taken at different projections. The operator theorem handles the former inside \(G=\operatorname{im}(\Gamma\to\operatorname{GL}(V/T))\); the vertical theorem handles the latter inside \(\Gamma\). This gives the full original group and every real point of \(C\).
