# Independent mathematical text review

Review date: 2026-11-22, America/Los_Angeles. Scope: the three archive files listed below, read directly. This reviews the root's adapted text and its conditional logic; it does not certify the geometric target, the problem contract, or other review documents. No repository file was changed and no Git command was used.

Archive root: /workspace/scratch/b46ebabc059e/co-work-cone-boss2/archives/relative-mk-cone.

| Reviewed file | SHA256 |
|---|---|
| state/proof.tex | 1563a7e5e14a308d332b7489eff0bb326cd4ef836cb5145118c887eb72dc75c3 |
| state/main_theorem.tex | 1b902c267c149b94ad548c8f3eaad88ff9e92a7070a74f2265fcaedfc668e399 |
| state/finite_route.md | 2a5ffd49ea52cd1b7cbd594353e3efe4a81fc8947463866494f0d614def44033 |

**Verdict:** the finite-stabilizer reduction and conditional route are valid. The archive does not prove or claim the full geometric theorem. Two conventions should be made explicit before treating every proposition's wording as fully unambiguous.

1. In Proposition prop:shear, replace “the action of Γ … has a strong … domain on the quotient” with “the induced quotient **image** has a strong … domain.” The proof already uses the correct image group. The original Γ acts trivially downstairs and has infinite stabilizer there, so it has no strong domain downstairs when stabilizers are computed in Γ itself.
2. In Lemma lem:pointed, specify that “rational polyhedral” means rational with respect to Λ ⊗ Q (and that Λ is a full lattice). Its proof then applies exactly. Rationality relative to an unrelated rational structure would not justify primitive lattice generators on the rays.
3. For local precision, the strict-inequality paragraph in Lemma lem:finite should say h ∈ H \ {1}. That is its correct contextual meaning; the argument for elements outside H is separate.

## Proof checks

In Lemma lem:finite, a generic rational covector exists because each nonidentity element of the finite subgroup H has a proper fixed covector subspace. Minimization over H gives HD = P, and therefore coverage by Γ. If D had smaller dimension, finitely many proper linear subspaces would cover the nonempty ambient interior of P, which is impossible.

For each nonidentity h ∈ H, the nonzero linear form ℓ ∘ h − ℓ is strictly positive on Int(D). If y ∈ hD ∩ Int(D), applying this strict comparison to h⁻¹ at y and the weak comparison to h at h⁻¹y gives opposite inequalities. For g ∉ H, containment in P and the original weak separation give gD ∩ Int(D) = ∅. This proves the required separation involving the **closed translate**, not merely disjoint interiors. Full dimension then forces the stabilizer of D to be trivial. No pointedness, closedness of C, or geometric hypothesis was silently used.

With the lattice-rationality convention in item 2, the pointed stabilizer proof is valid: the stabilizer acts faithfully on the finite set of primitive extremal-ray generators, since those vectors span V. The pointed-cone corollary follows.

The closed-half-plane shear argument is valid for every convex covering cone P: pointwise fixed boundary coverage forces W ⊂ P, and one positive-height vector forces P = C. The nonclosed half-plane example also has the stronger boundary separation; for y > 0, a nonzero integer translate's closed slope interval misses (0,1). At y = 0, only the origin belongs to D, and it is not an ambient interior point.

## Target and joint implication

The file main_theorem.tex labels the original strong-domain statement as a conjecture and explicitly says it remains unproved. The concluding section of proof.tex keeps both the exact-cone existence premise and the finite-stabilizer premise unpaid. No geometric counterexample is inferred from the shear construction.

The implication in finite_route.md is correct: assume uniformly that every target object has a full-dimensional weak rational polyhedral domain on its **actual** effective movable cone with finite numerical stabilizer; apply lem:finite to each object's faithful rational numerical image. This yields coverage, rational polyhedrality, the stronger separation, and trivial stabilizer on that same cone. The inference needs neither a comparison with Mov₊ nor a quotient-lifting assertion. The uniform geometric premise remains open. This review does not verify the document's separate procedural claim about an earlier reader.

These findings apply to the bytes with the hashes above; later edits require a fresh hash-bound review.

The three wording qualifications were subsequently clarified in proof.tex. The recorded hashes identify the earlier reviewed snapshot, not the later wording revision.
