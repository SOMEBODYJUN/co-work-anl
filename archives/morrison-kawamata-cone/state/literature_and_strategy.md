# Full cone-conjecture mission: verified benchmarks and proof routes

Date of literature check: 2026-11-23. Scope: arbitrary dimension, absolute and relative, effective nef and movable cones, and the two finiteness conclusions in the user's mission. Status: the full conjecture is not proved here. This is a targeted primary-source audit, not a claim to have re-proved or exhaustively audited every published proof.

## 1. Benchmarks and their actual reach

The statements below are existing results, not results of this project. A theorem on a rational hull or a geometric finiteness version is not silently promoted to the effective-cone fundamental-domain statement. Numerical action images, boundary-preserving groups, and the source's model-equivalence convention must be retained when importing a theorem.

| Class | Verified source and statement | Reach and remaining distinction |
|---|---|---|
| Complex projective klt Calabi–Yau surfaces, including K3 surfaces | Totaro, *The cone conjecture for Calabi–Yau pairs in dimension two*, Theorem 4.1 | Rational polyhedral domain for the effective nef cone; finite contraction-face orbits. This is absolute dimension two. Surface pseudo-isomorphisms introduce no higher-dimensional flop problem. |
| Abelian varieties | Prendergast-Smith, *The Cone Conjecture for Abelian Varieties*, Theorem 0.1 | Effective nef domain in every dimension over an algebraically closed field. The proof uses Rosati-symmetric endomorphisms and arithmetic reduction of homogeneous cones. It does not establish a relative theorem for arbitrary abelian fibrations. |
| Projective IHS manifolds | Markman and Amerik–Verbitsky; inspected the later paper arXiv:1604.03927, Theorem 3.17 | The primitive MBM classes have bounded Beauville–Bogomolov square and finitely many monodromy orbits under its stated hypothesis \(b_2\ge5\). Keep that hypothesis when quoting this particular theorem. The original 2014/2017 paper had a different technical exception \(b_2\ne5\). |
| Singular primitive symplectic varieties | Lehn–Mongardi–Pacienza, arXiv:2207.14754 | The source expressly requires projective primitive symplectic, Q-factorial terminal singularities, and \(b_2\ge5\). Its abstract also gives finiteness of minimal models. This is not the general klt theorem. |
| Very general Wehler varieties | Cantat–Oguiso, arXiv:1107.5862v3 | Explicit birational involutions and a Coxeter-group movable-domain construction in arbitrary dimension. A family in unbounded dimensions is not all varieties of those dimensions. |
| Smooth Schoen threefolds with the stated generic-fibre hypothesis | Gachet–Lin–Stenger–Wang (GLSW), arXiv:2406.07307; published 2026 | Their application proves the movable and effective versions for the stated fiber products; it does not settle all CY threefolds. Their main equivalence theorem assumes good minimal models for its strongest implications. |
| Smooth CY threefolds under deformation | Lutz, arXiv:2410.05949v3, Theorem 1.1; revised 2026-09-14 | Nef and movable rational-hull conjectures are invariant under smooth deformation. A solved representative therefore solves that deformation class. The theorem does not produce such a representative in every class. The introduction still states the general \(n>2\) problem is wide open. |
| Pairs of large anticanonical Iitaka dimension | Fulin Xu, arXiv:2405.20899v3, Theorem 1.9; revised 2026-11-19 | Q-factorial klt CY pairs of dimension \(d\) over a characteristic-zero field, with \(\kappa(X,-K_X)\ge d-2\). This is an arbitrary-dimensional result with a real geometric restriction. For \(K_X\sim0\) and \(d\ge3\), \(\kappa=0<d-2\), so it leaves strict CY varieties untreated. |
| Relative dimension at most two, klt pairs | Moraga–Stark, arXiv:2409.13068v1, Theorem 1.2 | Finite Mori chamber and face orbits in the effective movable cone: the geometric cone conjecture. Do not call this automatically a strong polyhedral fundamental domain. |
| Relative IHS fibrations | Höring–Pacienza–Xie, arXiv:2410.11987, author PDF, Theorems 1.3–1.4 | Between Q-factorial normal projective varieties, klt total space, and very general fiber one of the four known projective IHS deformation types: movable domain and finitely many SQMs, each satisfying nef. Theorem 1.4 instead assumes every nef divisor on that fiber is semiample. |

For the last relative equivalence machinery, the source's general setup also has vanishing irregularity of the very general fiber and a Q-factorial base; its argument uses non-degeneracy of the relative movable cone. Those conditions cannot be deleted in the universal parent mission. The same paper constructs a family of Kummer surfaces for which relative automorphisms are finite while relative birational maps and fiber automorphisms are infinite. Thus regular extension from fibers is a substantive issue, even among K3 families.

The Li (2023) and Li–Zhao (published correction incorporated in v8, 2025) results are being checked separately by the Main/execution line. This report does not infer the strong effective-domain version from those sources' weak or rational-hull statements.

## 2. A necessary theorem that abundance alone will not supply

Take \(S=\operatorname{Spec}\mathbf C\), \(\Delta=0\), and any smooth projective strict CY threefold. This is literally a special case of the new parent mission, with no fibration-lifting issue. Any successful full-scope proof must therefore solve the absolute problem for all such threefolds. Good minimal models for effective klt pairs are already available in dimension at most three (the dimensional boundary recorded by GLSW), whereas the general absolute CY-threefold cone conjecture is still open in the checked 2026 sources. Consequently, replacing all unfinished work by “assume/prove abundance” does not identify the full obstruction.

There are at least two logically distinct jobs:

1. Construct enough **actual** automorphisms/pseudo-automorphisms to obtain a finite rational orbit covering, controlling the non-big boundary.
2. Supply the model-existence, geography, and contraction machinery needed to turn such a covering into both cone statements and both finiteness conclusions, with the correct relative and degeneracy hypotheses.

There is no verified theorem here reducing these jobs to one smaller universally sufficient hypothesis. Naming the first job “universal polyhedral orbit covering” is useful as an obligation, but by itself is close to a reformulation of the cone conjecture.

## 3. An elementary mandatory test for any proposed construction

**Lemma.** Let \(C\) be a convex cone in a rational vector space tensored with \(\mathbf R\). Let a finite group \(\Gamma\) preserve \(C\). If a rational polyhedral cone \(P\subset C\) satisfies \(C=\Gamma P\), then \(C\) itself is rational polyhedral.

**Proof.** Write \(P=\operatorname{cone}(v_1,\ldots,v_r)\) with rational \(v_i\). The finite set \(\{\gamma v_i\}\) lies in \(C\), so its conical hull lies in \(C\) by convexity. Conversely, every element of \(C\) lies in some \(\gamma P\), hence in that hull. Thus \(C=\operatorname{cone}\{\gamma v_i\}\). This proof also permits linear subspaces inside \(C\). \(\square\)

This elementary observation is not a new cone-conjecture result. It is a sharp test against the idea that one can always manufacture an infinite automorphism group from a nontrivial cone. Oguiso's arXiv:1206.1649 proves that an odd-dimensional CY manifold of Picard number two has finite automorphism group. On that class a proposed proof of the nef conjecture must actually prove rational polyhedrality of the effective nef cone; inventing extra integral symmetries would contradict the geometry. Finiteness of the group is not a counterexample to the conjecture.

## 4. Route A: actual birational identifications plus finite geography

**Goal.** Produce a rational polyhedral cone \(Q\subset\operatorname{Eff}(X/S)\) with \(\operatorname{PsAut}(X/S,\Delta)Q\) covering the entire effective movable cone; then pass from movable to model-wise nef domains and finiteness with a checked geography theorem. This is a proof strategy, not a theorem proved here.

**Construction problem.** Associate to marked minimal models a small collection of geometric data that are realized by algebraic isomorphisms. An isomorphism \(u:Y_1\to Y_2\) between two marked models induces an actual pseudo-automorphism of \(X\) by composing markings. The missing theorem is a finite-type description of all marked chambers, modulo these identifications, including chambers accumulating at the non-big boundary. Finite model *targets* alone do not bound marked chambers; a single target can have infinitely many markings.

**First mathematical tests.**

- Recover the Coxeter generators and chamber reduction for a very general Wehler variety from its double-cover maps.
- Recover Rosati reduction for an abelian variety using actual endomorphisms, not arbitrary lattice isometries.
- Treat a CY threefold with finite numerical automorphism image. The preceding lemma forces a direct polyhedrality argument for the nef part.

The K3/IHS benchmark uses a global Torelli/monodromy realization mechanism unavailable as a blanket theorem for arbitrary CY varieties. An argument that simply substitutes the full integral isometry group for the geometric group has not done this construction.

## 5. Route B: deformation and descent, keeping the missing steps explicit

Lutz provides a valid transport theorem in dimension three. For a given smooth CY-threefold deformation class, find a representative with an explicit domain, then transport the rational-hull conclusion. The full mission would additionally need effective-boundary comparison and an argument reaching every deformation class. Neither is established merely by knowing that one large family satisfies the conjecture.

For higher-dimensional or singular varieties, a proposed general deformation theorem is an additional open obligation. Beauville–Bogomolov decomposition of smooth \(K\)-trivial varieties is also not a proof: even when factors are understood one must control mixed divisor classes on products, equivariance under the finite covering group, and descent of sufficient actual symmetries. General klt pairs with nonzero boundary do not automatically lie in the same smooth decomposition setup.

**First mathematical test.** On a finite étale quotient of a product of known factors, identify exactly which factor automorphisms normalize the deck group. Compute their image on the invariant Néron–Severi subspace and prove orbit covering for that image. A proof on the cover under the larger group does not imply a proof downstairs.

## 6. Route C: generic-fiber/Picard lifting in arbitrary irregularity

Keep three different objects separate:

\[
N^1(X/S),\qquad \operatorname{Pic}(X_\eta)\text{ modulo the actual relative numerical kernel},\qquad N^1(X_\eta).
\]

The middle space can retain arithmetic Picard information invisible to the last. Relative translations can act nontrivially on it while acting trivially on the fiber Néron–Severi space. The previously studied low-dimensional operator construction suggests the following precise task, without asserting it for all fibers:

Find a finite-dimensional rational quotient \(U\), a lattice of translations realized over \(\mathbf C(S)\) and extendable to the required relative group, a linear family \(d\mapsto T_d\) of rational self-adjoint positive-semidefinite operators, and compatible sections \(s(d)\), such that the **actual effective** fiber over every boundary class \(d\) is exactly

\[
s(d)+\operatorname{im}T_d.
\]

Uniform arithmetic reduction may then be studied on this explicit data. Arbitrary-rank lattice arguments alone do not construct the data. For general irregular fibers, their Albanese fibers can themselves be unresolved higher-dimensional CY varieties. The orbit model must also be equivariant for the relevant birational extension group, rather than for an artificially enlarged semidirect product.

**First mathematical tests.**

1. For an abelian torsor of arbitrary dimension, prove that its actual relative numerical kernel is stable under the relevant endomorphism action. Determine the translation lattice after quotienting the constant trace.
2. Check every positive-semidefinite rank-drop face. Do not replace effective classes by their topological closure.
3. Add an unresolved \(q=0\) CY factor. This demonstrates exactly what the Picard translation mechanism does not settle; it cannot remove the absolute CY obstruction.

## 7. Exact outcome of this worker's contribution

No general geometric theorem, universal domain, or counterexample to the full conjecture has been established by this worker. The elementary finite-group lemma above is completely proved. The verified literature yields powerful but differently scoped benchmarks. The leading mathematical obligations are actual geometric orbit reduction already in the absolute \(q=0\) case, and a relative lift preserving the actual effective boundary, with model geography and contraction finiteness under explicitly proved assumptions. There is currently no justification for calling the full mission PASS.

## Primary references actually opened

- Totaro, author PDF: https://www.math.ucla.edu/~totaro/papers/public_html/cone.pdf — Theorem 4.1 and proof introduction inspected.
- Prendergast-Smith, journal PDF: https://www.ms.u-tokyo.ac.jp/journal/pdf/jms190202.pdf — Theorems 0.1, 4.2–4.3 and arithmetic-reduction proof sections inspected.
- Amerik–Verbitsky: https://arxiv.org/pdf/1604.03927 — Theorem 3.17 and its monodromy context inspected; earlier technical hypotheses distinguished.
- Lehn–Mongardi–Pacienza: https://arxiv.org/abs/2207.14754 — abstract theorem scope inspected; full proof not independently audited here.
- Höring–Pacienza–Xie: https://math.univ-cotedazur.fr/u/hoering/articles/a50-rel-cone-conjecture.pdf — Theorems 1.3–1.7, general setup, and selected proof passages inspected.
- Moraga–Stark: https://arxiv.org/html/2409.13068v1 — Theorem 1.2 and stated proof reductions inspected.
- Lutz: https://arxiv.org/html/2410.05949v3 — Theorem 1.1, rational-hull conventions, proof outline, and later proof/application passages inspected.
- Fulin Xu: https://arxiv.org/html/2405.20899v3 — Theorems 1.3, 1.7, 1.9 and reduction assumptions inspected.
- Cantat–Oguiso: https://arxiv.org/abs/1107.5862 — abstract and version scope inspected; full proof not independently audited here.
- Oguiso: https://arxiv.org/abs/1206.1649 — abstract and version scope inspected.
- GLSW: https://doi.org/10.1515/crelle-2026-0046 — published abstract and date inspected; Main is examining the full theorem separately.

The 2026 preprint *Generalised Cone Conjecture, I: Beyond Calabi–Yau*, arXiv:2608.26079, was discovered but its primary page failed to open in this worker's check. No result from it is used here.
