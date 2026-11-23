# A domain for an extension of a cone action by a lattice of translations

This theorem describes the exact action on a cone over a rational base chamber. All geometric verifications needed for any application are outside its hypotheses-to-conclusion assertion.

## Hypotheses

All vector spaces are finite dimensional, and all vector spaces and structural linear maps are defined over \(\mathbb Q\) and are extended to \(\mathbb R\) when discussing cones. Let
\[
0\longrightarrow U\longrightarrow L\xrightarrow{\pi} R\longrightarrow0
\]
be exact. Let a countable faithful group of rational linear operators \(G\subset\mathrm{GL}(L_\mathbb Q)\) act preserving this sequence and a convex cone \(\mathcal C\subset L\) with nonempty interior. Write \(\bar G\) for the image on \(R\), \(G_0\) for the kernel, and assume \(\pi\mathcal C\) has a strong rational polyhedral domain \(B\) for \(\bar G\), including weak separation against the whole closed translate as in Li–Zhao, Definition 3.4. Let \(T:R\to\operatorname{End}(U)\) be rational linear, \(T_H=1\) at a specified rational point \(H\). Suppose:

1. \(U\) admits a rational positive definite scalar product for which each \(T_D\), \(D\in B\), is self-adjoint and positive semidefinite. Some positive combination of operators at finitely many rational generators of \(B\) is positive definite.
2. There is a rational linear section \(s:R\to L\) such that for every **real** \(D\in B\),
   \[
   \mathcal C\cap\pi^{-1}(D)=s(D)+\operatorname{im}T_D .
   \]
3. A full lattice \(\Lambda\subset U\) is realized as a normal subgroup of finite index in \(G_0\) by \(\tau_z(x)=x+T_{\pi x}z\). The extension of the finite point group by this lattice need not split. No splitting compatible with the group action is assumed in (2).

Then \(\mathcal C\) has a rational polyhedral weak domain with finite stabilizer and hence a strong rational polyhedral domain by the refinement proved below. The construction never adjoins directions over faces where \(T_D\) has smaller image.

## Normalization in the kernel of the base action

For \(g\in G_0\), let \(A_g\) be its restriction to \(U\) and \(B_g\) its conjugation action on the abstract lattice \(\Lambda\), extended linearly to \(U\). Then \(A_g T_D=T_D B_g\) on every \(D\in R\), by applying \(g\tau_z g^{-1}=\tau_{B_gz}\) to a lift of \(D\). At \(H\) this gives \(A_g=B_g\), hence \(A_g\) commutes with every \(T_D\). The \(A_g\) form a finite group since translations act trivially on \(U\). Averaging the original scalar product over this finite group preserves rationality, positivity and self-adjointness: for example each summand \(\langle A_gu,T_D A_gu\rangle\) is nonnegative. We now use the averaged product.

Two rational sections differ by a member of \(\operatorname{Hom}(R,U)\). In that space the subspace \(T(U)=\{D\mapsto T_Du:u\in U\}\) is invariant under the action \(A_g\). The induced affine action of \(G_0\) on the space of rational sections modulo \(T(U)\) factors through \(G_0/\Lambda\). Take representatives \(g_j\) for this finite quotient and form the actual rational section \(s'=\frac1{[G_0:\Lambda]}\sum_j g_j s\). Its class modulo \(T(U)\) is fixed. Accordingly there is a unique \(n_g\in U_\mathbb Q\) such that
\[
  g s'(D)=s'(D)+T_D n_g\qquad(D\in R).
\]
Uniqueness follows on evaluating at \(H\). Every \(g_js(D)\) lies in \(s(D)+\operatorname{im}T_D\) for \(D\in B\), so \(s'\) still satisfies (2). The group law gives \(n_{gh}=n_g+A_g n_h\), and \(n_{\tau_z}=z\). Therefore
\[
S=\{n_g:g\in G_0\}
\]
is a finite union of \(\Lambda\)-cosets and contains the zero coset. The lattice lies in \(U_\mathbb Q\) since evaluating each rational translation at a rational lift of \(H\) gives the parameter \(z\). Its full rank, together with rationality of the finitely many offsets, puts every coset inside one finite superlattice of \(\Lambda\). The subgroup \(G_*=\{g\in G_0:n_g=0\}\) embeds into \(G_0/\Lambda\).

## Finitely many linear inequalities

Define
\[
\Pi=\bigl\{s'(D)+w:D\in B,\ w\in U,\
 2\langle m,w\rangle\le \langle m,T_Dm\rangle \quad(m\in S)\bigr\}.
\]
Write \(B=\sum_i\mathbb R_{\ge0}d_i\) with rational generators and \(q_i(m)=\langle m,T_{d_i}m\rangle\). Every \(q_i\) is rational and positive semidefinite. The sum is positive definite, since a positive linear combination is. Clear denominators for all \(q_i\) on a finite superlattice containing \(S\). Partition \(S\) into its finitely many congruence classes modulo \(2\Lambda\). In each such class, the coordinatewise minimal elements of \(\{(q_i(m))_i\}_m\subset\mathbb N^k\) form a finite set by Dickson's lemma. There are finitely many \(m\) realizing each fixed tuple, since its total \(q=\sum q_i\) has bounded level sets. Retain every such minimal representative.

For any other \(m\), choose \(n\) in the same congruence class with \(q_i(n)\le q_i(m)\) for every \(i\), with one strict. Set \(a=(m+n)/2,\ b=(m-n)/2\). Then \(a\in m+\Lambda\subset S\), \(b\in\Lambda\subset S\), and
\[
 a+b=m,\qquad q_i(a)+q_i(b)=\tfrac12(q_i(m)+q_i(n))\le q_i(m).
\]
Both \(q(a),q(b)\) are strictly less than \(q(m)\). Induction on the common-denominator integral values of \(q\) proves the inequality for \(m\) from the finite retained inequalities, using \(T_D=\sum t_iT_{d_i}\) for \(D=\sum t_id_i,\ t_i\ge0\). Thus \(\Pi\) is a closed rational polyhedral cone even when some face operators are degenerate.

## Exact fibres, covering and stabilizer

For fixed \(D=\sum t_i d_i\) with \(t_i\ge0\), let \(K_D=\ker T_D\). Positivity gives \(K_D=\bigcap_{t_i>0}\ker T_{d_i}\), so \(K_D\) is rational, including at zero. Since \(S\) contains both signs of every lattice vector of \(K_D\), the inequalities imply \(\langle w,K_D\rangle=0\). Thus \(w\in K_D^\perp=\operatorname{im}T_D\), exactly the permitted fibre directions in (2). In particular the closedness and finite description of \(\Pi\) have not enlarged the effective boundary.

If \(x=s'(D)+T_Du\in\mathcal C\) with \(D\in B\), the inequalities for \(\Pi\) say precisely that \([0]\) in \(U/K_D\) is a nearest centre to \([u]\) among the images of \(S\), using the positive definite squared norm induced by \(\langle u,T_Du\rangle\). As \(K_D\) is rational, the image of \(\Lambda\) is a full lattice of this quotient. The images of \(S\) are a finite union of its cosets; thus a nearest centre \([n_g]\) exists. The affine map \(u\mapsto n_g+A_g u\) descends to a norm isometry on differences in \(U/K_D\) and permutes the centres. Its inverse sends \([u]\) to a point having \([0]\) as nearest centre; equivalently \(g^{-1}x\in\Pi\). For any other base class take an element of \(\bar G\) moving it to \(B\) and lift it to \(G\). This establishes \(G\Pi=\mathcal C\). Countability and nonempty interior of \(\mathcal C\) imply \(\Pi\) is full-dimensional.

For \(g\) with nonidentity image in \(\bar G\), a point of \(g\Pi\cap\operatorname{Int}\Pi\) would project to \((\bar g B)\cap\operatorname{Int}B\). This is empty because \(\pi\) is open and \(B\) satisfies exact strong separation. For \(g\in G_0\) with \(n_g=0\), \(A_g\) preserves \(S\) and all forms, so \(g\Pi=\Pi\). If \(g\in G_0\) with \(m=n_g\ne0\), the functional
\[
 s'(D)+w\longmapsto \langle m,T_Dm\rangle-2\langle m,w\rangle
\]
is nonzero on \(L\) (vary \(w\)). It is strictly positive on \(\operatorname{Int}\Pi\). For \(x=s'(D)+w\in g\Pi\), apply the inequality for \(n_{g^{-1}}=-A_g^{-1}m\) to \(g^{-1}x=s'(D)+A_g^{-1}(w-T_Dm)\). Orthogonality and commutation give \(2\langle m,w\rangle\ge\langle m,T_Dm\rangle\). Hence \(g\Pi\cap\operatorname{Int}\Pi=\varnothing\). The setwise stabilizer is exactly \(G_*\), which is finite.

For completeness the finite stabilizer can be removed on this very cone. Choose a rational covector whose stabilizer in the finite group of setwise chamber symmetries is trivial. Intersect the chamber with the finitely many closed halfspaces on which its value is minimal in the finite orbit. The translates under that finite group cover the original chamber. Discreteness is unnecessary: a minimum over a finite set exists. On the interior of the new cone, every comparison with a nonidentity chamber symmetry is strict because its defining linear functional is nonzero. Comparing the inequalities for an element and its inverse proves that its whole closed translate misses the interior. Every element outside the original stabilizer already misses the original interior. The new cone has nonempty interior by finite coverage, so its setwise stabilizer is trivial.
