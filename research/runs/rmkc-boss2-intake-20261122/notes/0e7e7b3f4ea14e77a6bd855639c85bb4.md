# Candidate convex audit: weak domains, finite stabilizers, and lineality

Report date: 2026-11-22, America/Los_Angeles. Abstract proofs below are supplied in full and remain candidates pending independent review. No theorem for all terminal log Calabi–Yau fibrations is asserted.

**Conclusion.** A full-dimensional weak rational polyhedral fundamental domain with finite stabilizer always contains a single strong rational polyhedral fundamental domain. Lineality causes no exception to this assertion. The unresolved geometric task is to produce such a finite-stabilizer weak domain on the **specified effective cone**, rather than merely on its rational hull.

## 1. Conventions

Let $V=V_{\mathbb Q}\otimes_{\mathbb Q}\mathbb R$, let $\Lambda\subset V_{\mathbb Q}$ be a full lattice, and let $\Gamma\subset\mathrm{GL}(\Lambda)$ act faithfully. Let $C\subset V$ be a full-dimensional convex cone containing $0$; $C$ need not be closed. Interiors below are ordinary interiors in $V$, unless another ambient space is named.

A weak domain is a closed rational polyhedral cone $\Pi\subset C$ satisfying

\[
\Gamma\Pi=C,\qquad
\gamma\Pi=\Pi\ \text{or}\ \gamma\Pi\cap\operatorname{Int}\Pi=\varnothing
\quad(\gamma\in\Gamma).
\]

It is strong when its setwise stabilizer is trivial. This uses the stronger closed-cone/interior separation, not just disjointness of two interiors.

For the geometric target, fix

\[
V=N^1(X/S)_{\mathbb R},\quad
M=\overline{\operatorname{Mov}}(X/S),\quad
C=M\cap\operatorname{Eff}(X/S),\quad
\Gamma=\operatorname{im}\bigl(\operatorname{PsAut}(X/S,\Delta)\to\mathrm{GL}(V)\bigr).
\]

Since $\operatorname{Mov}(X/S)\subset C\subset M$, one has $\overline C=M$. The image convention removes the kernel on all of $V$. It does **not** remove a kernel on a subsequent quotient.

## 2. Finite-stabilizer refinement: complete abstract proof

**Proposition A.** If a full-dimensional weak rational polyhedral domain $\Pi$ has finite stabilizer $H=\Gamma_\Pi$, then there is a full-dimensional strong rational polyhedral domain $D\subset\Pi$. Moreover the cones $hD$, $h\in H$, form a finite polyhedral subdivision of $\Pi$.

**Proof.** Because $H\subset\mathrm{GL}(V)$ is faithful and finite, choose a rational covector $\ell\in V_{\mathbb Q}^{*}$ such that

\[
\ell\circ h\ne\ell\quad\text{for every }h\in H\setminus\{1\}.
\]

Each forbidden equality defines a proper rational linear subspace of the dual, and a finite union of such subspaces cannot contain all rational covectors. Set

\[
D=\{x\in\Pi:\ell(x)\le\ell(hx)\text{ for every }h\in H\}.
\]

This is a closed rational polyhedral cone. For each $x\in\Pi$, choose $g\in H$ minimizing $\ell(gx)$. Then $gx\in D$, since $hg$ ranges over $H$. Therefore $HD=\Pi$.

The cone $D$ is full-dimensional: otherwise each of the finitely many closed cones $hD$ has empty interior, and their union cannot cover the nonempty open set $\operatorname{Int}\Pi$. This is the finite closed-set form of the Baire argument (or follows from their being contained in finitely many proper linear subspaces). Hence

\[
\varnothing\ne\operatorname{Int}D\subset\operatorname{Int}\Pi.
\]

For $h\ne1$, the nonzero linear form $\ell\circ h-\ell$ is nonnegative on $D$, and so is strictly positive at every point of $\operatorname{Int}D$. Consequently, if $y\in hD\cap\operatorname{Int}D$ and $z=h^{-1}y\in D$, then

\[
\ell(z)\le\ell(hz)=\ell(y)
<\ell(h^{-1}y)=\ell(z),
\]

a contradiction. For $\gamma\notin H$,

\[
\gamma D\cap\operatorname{Int}D
\subset\gamma\Pi\cap\operatorname{Int}\Pi=\varnothing.
\]

Thus every nonidentity $\gamma$ satisfies the required stronger separation. Also $\Gamma D=\Gamma HD=\Gamma\Pi=C$. A nonidentity element stabilizing $D$ would violate separation because $D$ has nonempty interior. Hence $D$ is strong.

For the subdivision assertion, put $f_h=\ell\circ h^{-1}$. Then

\[
hD=\{x\in\Pi:f_h(x)\le f_k(x)\text{ for all }k\in H\}.
\]

For distinct $h,k$, their intersection is exactly the face of $hD$ cut out by (f_h=f_k), and is likewise a face of (kD). Adding their faces gives a finite polyhedral subdivision. $\square$

Faithfulness matters: if an abstract acting group has a nontrivial kernel on $V$, no cone can have trivial stabilizer for that abstract group. The proposition applies to the numerical image $\Gamma$.

**Corollary A1.** If $C\cap(-C)=\{0\}$, every rational polyhedral weak domain for $C$ upgrades to a strong one.

**Proof.** Such a domain is pointed. Its lattice stabilizer permutes its finitely many extremal rays and therefore their primitive lattice generators. An element fixing every ray fixes every primitive generator, because it is a lattice automorphism. These generators span $V$, so this permutation action is faithful and the stabilizer is finite. Proposition A applies. Full dimension is automatic when $C$ has nonempty interior: $\Gamma$ is countable, and countably many translates of a lower-dimensional closed cone cannot cover an open set. $\square$

## 3. Two distinct lineality spaces

Put

\[
W=\overline C\cap(-\overline C),\qquad L=C\cap(-C).
\]

Both are vector spaces, and $L\subset W$. They need not coincide. The elementary identities are

\[
C+L=C,\qquad \overline C+W=\overline C,
\qquad \operatorname{Int}C+W=\operatorname{Int}C.
\]

For the first two identities, a convex cone is closed under addition and both signs of every lineality vector belong to the relevant cone. For the third, a full-dimensional convex set has the same interior as its closure, and translation by a vector of $W$ preserves $\overline C$. The standard interior equality follows, for example, by approximating the vertices of a small simplex around an interior point of the closure by points of $C$.

In general $C+W=C$ fails; indeed, since $0\in C$, it would imply $W\subset C$. Thus

\[
C=p^{-1}(pC)\quad\Longleftrightarrow\quad W\subset C
\quad\Longleftrightarrow\quad L=W,
\]

where $p:V\to V/W$. The forward implication uses $p^{-1}(0)=W$; the reverse uses closure under addition by $\pm W$.

The quotient of $\overline C$ by $W$ is closed and pointed. To see closedness, choose a linear splitting $j$; saturation identifies the quotient cone with the closed cone $\overline C\cap j(V/W)$. If both $q,-q$ lie in that quotient cone, then $j(q),-j(q)\in\overline C$, so $j(q)\in W\cap j(V/W)=0$.

For a rational $W$, the rational hull

\[
T=\operatorname{Conv}(\overline C\cap V_{\mathbb Q})
\]

contains $W$ and is $W$-saturated. Indeed the positive and negative vectors of a rational basis generate $W$ as a cone. A rational splitting also proves

\[
pT=\operatorname{Conv}\bigl(p(\overline C)\cap(V/W)_{\mathbb Q}\bigr).
\]

Every rational quotient point has its rational split lift in $\overline C$, by saturation. Linear images commute with finite convex combinations. These assertions concern $T$; they do not identify $T$ with the actual effective cone $C$.

## 4. Saturated lifting and the quotient kernel

**Proposition B.** Suppose $W$ is rational, $W\subset C$, and $\bar\Pi\subset pC$ is a full-dimensional strong rational polyhedral domain for the image $\bar\Gamma\subset\mathrm{GL}(V/W)$. Then

\[
\Pi=p^{-1}(\bar\Pi)=j(\bar\Pi)+W\subset C
\]

is a weak rational polyhedral domain whose stabilizer is exactly

\[
K=\ker\bigl(\Gamma\to\mathrm{GL}(V/W)\bigr).
\]

If $K=1$, this lift is strong. If $K$ is finite, Proposition A refines it to one strong rational polyhedral domain.

**Proof.** The rational splitting and a signed rational basis of $W$ give finite rational generators for $\Pi$. Saturation gives containment in $C$, and quotient coverage gives $\Gamma\Pi=C$. Under the product description,

\[
\operatorname{Int}\Pi=p^{-1}(\operatorname{Int}\bar\Pi).
\]

For $\gamma\notin K$, quotient separation therefore gives $\gamma\Pi\cap\operatorname{Int}\Pi=\varnothing$. Every element of $K$ preserves $\Pi$, because it preserves each fiber of $p$. Conversely a stabilizer of $\Pi$ stabilizes $\bar\Pi$, so its quotient is the identity by strongness downstairs. $\square$

Faithfulness upstairs alone does not make the quotient faithful. With a rational splitting $V=W\oplus U$, every $g\in K$ has block form

\[
g=\begin{pmatrix}A_g&B_g\\0&I_U\end{pmatrix},
\qquad (A,B)(A',B')=(AA',AB'+B).
\]

The kernel of the restriction $K\to\mathrm{GL}(W)$ consists of shears $\left(\begin{smallmatrix}I&B\\0&I\end{smallmatrix}\right)$. After choosing compatible lattices it is an additive subgroup of a lattice in $\operatorname{Hom}(U,W)$, hence free abelian of finite rank. A nonzero shear has infinite order, since its $n$-th power has upper-right block $nB$. In particular, finite $K$ injects into its restriction on $W$; if such a finite $K$ also fixes $W$ pointwise, it is trivial.

## 5. Shear model: what it disproves and what it does not

Let $V=\mathbb R^2$, $\Lambda=\mathbb Z^2$, and

\[
T^n(x,y)=(x+ny,y),\qquad\Gamma=\langle T\rangle\cong\mathbb Z.
\]

For the **closed** half-plane $C_{\rm cl}=\{y\ge0\}$, one has $W=\{y=0\}$, trivial quotient image, and infinite quotient kernel $K=\Gamma$. The quotient ray has a strong domain for its trivial image group; its saturated lift is all $C_{\rm cl}$, stabilized by $\Gamma$.

In fact $C_{\rm cl}$ has no strong convex polyhedral domain for this action. If a cone $P\subset C_{\rm cl}$ satisfies $\Gamma P=C_{\rm cl}$, each $w\in W$ belongs to $P$, since every $T^n$ fixes $w$. Coverage also forces $P$ to contain some point with $y>0$. Convexity, scaling, and $W\subset P$ then imply $P=C_{\rm cl}$, with infinite stabilizer. This refutes unconditional strong lifting from a faithful quotient **image** and refutes weak-to-strong refinement without finite stabilizer.

For the **nonclosed** cone

\[
C_{\rm eff}=\{y>0\}\cup\{0\},
\qquad D=\operatorname{cone}((0,1),(1,1)),
\]

the same action has a strong rational polyhedral domain $D$. Its translates cover exactly the slope strips $n\le x/y\le n+1$, plus the origin; different strips meet only along boundary rays. Here $L=0$, while the lineality of the closure is still $W\ne0$. Also $p^{-1}(pC_{\rm eff})=C_{\rm cl}\ne C_{\rm eff}$. The rational hull of the closure adds precisely the missing boundary line.

This pair is an **abstract convex model**, not a geometric counterexample to the requested fibration statement. It also proves that an infinite quotient kernel does not by itself obstruct a strong domain on a nonclosed effective cone.

## 6. Primary-source audit and the smallest geometric gap

The following are literature statements; the preceding propositions are independent proofs.

| Primary source | Exact location and relevant scope |
|---|---|
| [Li–Zhao, arXiv:2206.13701v8](https://arxiv.org/html/2206.13701v8) | Definition 3.4 fixes weak/strong domains. Lemma 3.5 treats the nondegenerate case. Lemma 3.7 and Proposition 3.8 use rational closure-lineality; the constructed stabilizer is the quotient kernel. |
| Same source | Proposition 4.4 gives rationality of closure-lineality. Lemma 4.8 proves finite quotient kernel for terminal Calabi–Yau fiber spaces with $R^1f_*\mathcal O_X=0$. |
| Same source | Proposition 5.3(1), (3), (4) has explicit polyhedral-cover and minimal-model hypotheses. Remark 5.4 cites an irregular elliptic example with effective movable cone different from its rational hull and with $W$ absent from the movable cone. |
| [Li, arXiv:2309.04673v1](https://arxiv.org/pdf/2309.04673v1) | Theorem 1.8 is a conditional result for terminal pairs on $\operatorname{Mov}_+$. Corollaries 1.9 and 6.4 state the relative-dimension-$\le2$ application with $\Delta=0$. Section 6.2 notes that $\operatorname{Mov}_+$ need not be effective. The paragraph after Corollary 6.3 identifies the generic-field log-surface issue. |

The shortest sufficient geometric statement to seek is:

> For every fibration in the target class, the actual cone $C=\overline{\operatorname{Mov}}\cap\operatorname{Eff}$ admits a rational polyhedral weak domain whose stabilizer in the numerical image $\Gamma$ is finite.

Proposition A would then finish the strong-domain problem. If $L=0$, the finite-stabilizer clause follows automatically from Corollary A1. If using saturated quotient lifting instead, one must justify **both** containment of the lift in $C$ and finiteness of $K$. Neither follows merely from faithfulness on $V$, rationality of $W$, or a strong domain for the quotient image.

Accordingly the bounded abstract claim is **proved**; unconditional saturated strong lifting is **disproved abstractly**; passage to all terminal log Calabi–Yau fibrations on the specified effective cone is **not established here**. A weak-domain theorem on a different cone, or a conditional theorem whose generic-fiber hypothesis has not been checked, does not close that geometric gap.
