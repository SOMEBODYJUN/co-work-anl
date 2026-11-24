# Cone obstructions and a finite-kernel lifting theorem

Author role: independent obstruction worker. Date: 2026-11-23.

Status: conventional proofs below, with the standard abelian-variety matrix description identified explicitly as an external input. No novelty claim. None of the examples disproves the effective Morrison–Kawamata conjecture in the mission. The abstract counterexample is not asserted to arise from a Calabi–Yau fibration.

## 1. A quotient cone can conceal an obstruction to a strong domain

Put

\[
 V=\mathbb R^2,\quad V_{\mathbb Q}=\mathbb Q^2,\quad
 C=\{(x,y):y\geq0\},\quad W=\mathbb R(1,0).
\]

Let \(g(x,y)=(x+y,y)\), and let \(\Gamma=\langle g\rangle\subset\mathrm{GL}_2(\mathbb Z)\).
The action is faithful, \(W\) is the lineality space of \(C\), and \(g\) fixes \(W\) pointwise. The induced action on \(V/W\) is trivial. Thus the quotient cone \(p(C)=\mathbb R_{\geq0}\) has the strong rational polyhedral domain \(p(C)\) for the faithful quotient image \(\bar\Gamma=\{1\}\).

**Claim.** There is no convex cone \(\Pi\subset C\) such that

\[
 \Gamma\Pi=C,\qquad
 g^n\Pi\cap\operatorname{Int}_V(\Pi)=\varnothing\quad(n\ne0).
\]

**Proof.** Every point of \(W\) is fixed by \(\Gamma\). Coverage therefore forces \(W\subset\Pi\). Coverage also forces \(\Pi\) to contain a point \(z=(a,b)\) with \(b>0\). Since \(\Pi\) is a convex cone, it is closed under addition and nonnegative scaling. For every \(y>0\), it contains \((y/b)z+W\), the whole horizontal line at height \(y\). It follows that \(\Pi=C\). But then \(g\Pi=\Pi=C\), whose interior is nonempty, contradicting separation. This argument does not even need polyhedrality. \(\square\)

The whole cone \(C\) is a weak rational polyhedral domain if equality of translates is allowed. Its setwise stabilizer is the infinite group \(\Gamma\). Hence this example also disproves the abstract assertion that every weak rational polyhedral domain can be cut into a strong one without a stabilizer hypothesis. The lost information is exactly the infinite kernel of \(\Gamma\to\bar\Gamma\).

## 2. What finite stabilizer cutting actually proves

Let \(V_{\mathbb Q}\) be a finite-dimensional rational vector space, \(V=V_{\mathbb Q}\otimes\mathbb R\), and let \(\Gamma\subset\mathrm{GL}(V_{\mathbb Q})\) act faithfully. Suppose a full-dimensional rational polyhedral cone \(D\) satisfies

\[
 \Gamma D=C,
 \qquad \gamma D=D\ \text{or}\ \gamma D\cap\operatorname{Int}_V D=\varnothing
 \quad(\gamma\in\Gamma).
\]

Assume \(H=\{\gamma:\gamma D=D\}\) is finite. Then \(C\) has a strong rational polyhedral domain.

**Proof.** Choose \(\ell\in V_{\mathbb Q}^*\) outside the finitely many proper fixed subspaces
\(\{\ell:\ell\circ h=\ell\}\), \(h\in H\setminus\{1\}\). Such a rational functional exists. Define

\[
 P=\{x\in D:\ell(x)\geq\ell(hx)\text{ for every }h\in H\}.
\]

This is rational polyhedral. The maximum of \(\ell\) on every finite \(H\)-orbit is attained, so \(HP=D\). Consequently \(\Gamma P=C\). Since \(D\) is a finite union of the closed sets \(hP\) and is full-dimensional, \(P\) is full-dimensional.

If \(\gamma\notin H\), then \(\gamma P\subset\gamma D\), while \(\operatorname{Int}P\subset\operatorname{Int}D\), so these sets do not meet. Now let \(1\ne h\in H\), and suppose \(x=hy\in\operatorname{Int}P\) with \(y\in P\). The nonzero linear functional \(\ell-\ell\circ h^{-1}\) is nonnegative on \(P\), so it is strictly positive on \(\operatorname{Int}P\). Therefore

\[
 \ell(x)>\ell(h^{-1}x)=\ell(y).
\]

On the other hand \(y\in P\) gives \(\ell(y)\geq\ell(hy)=\ell(x)\), a contradiction. Thus
\(\gamma P\cap\operatorname{Int}P=\varnothing\) for every \(\gamma\ne1\). In particular the setwise stabilizer of \(P\) is trivial. \(\square\)

## 3. A precise finite-kernel lifting theorem

Let \(W\subset V\) be a rational \(\Gamma\)-invariant subspace, and let \(p:V\to\bar V=V/W\). Let \(C\subset V\) be a \(\Gamma\)-invariant convex cone. Write \(\bar\Gamma\) for the faithful image on \(\bar V\). Assume:

1. The kernel \(K=\ker(\Gamma\to\bar\Gamma)\) is finite.
2. A rational polyhedral cone \(Q\subset p(C)\) satisfies \(\bar\Gamma Q=p(C)\) and \(\bar\gamma Q\cap\operatorname{Int}_{\bar V}Q=\varnothing\) for every \(\bar\gamma\ne1\).
3. The cone \(D=C\cap p^{-1}(Q)\) is rational polyhedral and full-dimensional in \(V\).

Then \(C\) has a strong rational polyhedral domain for \(\Gamma\).

**Proof.** Quotient coverage gives \(\Gamma D=C\). The kernel preserves \(D\). If \(\gamma\notin K\) and \(x\in\gamma D\cap\operatorname{Int}_V D\), then \(p(x)\in\bar\gamma Q\). Since \(p\) is an open linear surjection and \(p(D)=Q\), the point \(p(x)\) lies in \(\operatorname{Int}_{\bar V}Q\), a contradiction. It follows that \(D\) is a weak domain whose stabilizer is precisely \(K\): inclusion \(K\subset\operatorname{Stab}(D)\) was noted, and any other stabilizing element contradicts nonempty interior. Apply Section 2. \(\square\)

The statement does not assume that \(C\) is pointed. It also does not prove either of its essential geometric hypotheses: finiteness of \(K\), or polyhedrality and fullness of \(C\cap p^{-1}(Q)\). Establishing a quotient fundamental domain alone pays neither obligation. The shear example violates the finite-kernel hypothesis.

## 4. A geometric counterexample to replacing the effective cone by the entire closed nef cone

Let \(E/\mathbb C\) be an elliptic curve with \(\operatorname{End}(E)=\mathbb Z\), and let \(A=E\times E\). This is a smooth projective klt Calabi–Yau pair \((A,0)\).

The standard product principal polarization identifies the rational Néron–Severi space with \(\operatorname{Sym}_2(\mathbb Q)\), its real extension with \(\operatorname{Sym}_2(\mathbb R)\), and the ample cone with the positive-definite matrices. Consequently its closed nef cone is \(\operatorname{Sym}_2(\mathbb R)_{\geq0}\). This is the external geometric input: Prendergast-Smith, *The Cone Conjecture for Abelian Varieties*, J. Math. Sci. Univ. Tokyo 19 (2012), Theorem 4.3 and the preceding polarization construction, pp. 254–256: <https://www.ms.u-tokyo.ac.jp/journal/pdf/jms190202.pdf>.

Consider

\[
 M=\begin{pmatrix}1&\sqrt2\\\sqrt2&2\end{pmatrix}
   =vv^{\mathsf T},\qquad v=(1,\sqrt2)^{\mathsf T}.
\]

This matrix spans an extreme ray \(R\) of the positive-semidefinite cone. Indeed, if \(M=M_1+M_2\) with both \(M_i\) positive semidefinite, then every \(w\perp v\) has \(w^{\mathsf T}M_iw=0\). Positivity implies \(M_iw=0\). Symmetry now implies that \(\operatorname{im}M_i\subset\mathbb Rv\), so both \(M_i\) are nonnegative multiples of \(M\).

There is no nonzero rational matrix on \(R\). If \(tM\) were rational, its upper left entry would give \(t\in\mathbb Q\), whereas its off-diagonal entry would give \(t\sqrt2\in\mathbb Q\); hence \(t=0\).

**Claim.** No rational polyhedral subcone of the closed nef cone contains a nonzero point of \(R\).

**Proof.** Write such a subcone as \(\sum_{i=1}^r\mathbb R_{\geq0}Q_i\) with each \(Q_i\) rational and positive semidefinite. If a nonzero point of \(R\) were a nonnegative combination of the \(Q_i\), extremality would force every active nonzero \(Q_i\) to lie on \(R\), which is impossible. \(\square\)

Every automorphism acts rationally on the Néron–Severi space and preserves nefness. Its translate of a rational polyhedral nef subcone is therefore another such subcone. The claim proves that no translates of any rational polyhedral nef subcone can cover the entire closed nef cone. In fact allowing arbitrarily many rational polyhedral subcones still does not cover \(R\).

This is **not** a counterexample to the mission's effective statement. Every effective divisor on an abelian variety is nef: to intersect it with a curve, translate the divisor so that it does not contain that curve; translations preserve its numerical class and proper effective intersection is nonnegative. If \(M\) belonged to the real effective cone, it would be a finite nonnegative real combination of integral effective divisor classes, all positive semidefinite. Extremality would again force a nonzero rational class on \(R\), a contradiction. Thus \(M\) is nef but not effective. It is also absent from the rational hull of the closed nef cone by the identical finite-combination argument.

The forbidden stronger formulation is coverage of **all** closed nef boundary rays. Effective and rational-hull formulations deliberately exclude the ray above.

## 5. The proposed mixed-class product test is rejected, with exact intersections

Take the same \(A=E\times E\), but now let \(f=\operatorname{pr}_2:A\to E\). Put

\[
 H_1=\{0\}\times E,\qquad H_2=E\times\{0\},\qquad
 P=\Delta_E-H_1-H_2.
\]

The three elliptic divisors have self-intersection zero, and any two distinct ones have intersection one. Hence

\[
 P\cdot H_2=1-1-0=0,\qquad
 P^2=-2.
\]

The class \(P\) is nonzero in absolute \(N^1(A)\), and it is not a pullback from the base: every base pullback is a real multiple of \(H_2\), whose square is zero. On the generic fibre \(P\) has degree zero and is numerically trivial.

Nevertheless \(P\equiv_f0\). Every irreducible curve contracted by \(f\) is an entire fibre \(E\times\{s\}\), numerically equivalent to \(H_2\), and \(P\) has intersection zero with all of them. Indeed \(N^1(A/E)\) has dimension one under numerical equivalence tested on contracted curves, with relative degree giving an isomorphism to \(\mathbb R\).

Thus \(N^1(A)/f^*N^1(E)\) is not interchangeable with this relative numerical space. The example has positive fibre irregularity, and \(K_A\sim0\), but it does **not** exhibit a nonzero relative numerical class invisible on the generic fibre. Using it for that assertion would manufacture a false geometric obstruction.

## 6. What remains for the full mission

The proofs above settle elementary convex implications and refute two overstrong auxiliary assertions. They do not construct the required automorphisms for arbitrary klt Calabi–Yau pairs, establish generic-to-relative descent, prove uniform polyhedral control at all effective boundary classes, or prove birational/contraction finiteness in unrestricted dimension. The finite-kernel lifting theorem supplies an exact conditional bridge, not a replacement for those geometric theorems.
