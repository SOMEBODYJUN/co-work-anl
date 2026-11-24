# Internal independent review of the initial auxiliary publication

Reviewer agent: `/root/ultimate_ideas`.
Evidence level: `internal-independent`.
Freeze ID: `MKC-INITIAL-AUXILIARIES-v1`.
Freeze revision pin: `59f43b2f9062da42d0b7dd4dc241566257eb2bbb2abfc447c91f10ca2cd8a8a3`.
Verdict: **approve the exact four-object registration payload at its stated scope**.

## Independence and scope

I did not author the mathematical proofs in `cone_obstructions_and_lifting.md`; its authors are the Main and the obstruction worker. I had earlier authored a separate literature/route report and a scope review. Neither my own literature report nor the old relative-dimension-two proof is being mathematically certified by this review. I inherited surrounding conversation context, so this is an internal nonauthor check, not a blind experiment or external peer review.

I read every distinct frozen content file and the registration batch, checked all fourteen content references against their SHA-256 values, and inspected the referenced proof sections in full. Repeated section references point into the same checked proof bytes. The parent conjecture is registered OPEN; only the abstract finite-kernel implication and two exact obstructions are registered proved. There are no parent-closing implication edges in the batch.

## 1. Finite-stabilizer cutting

The rational action and faithfulness ensure that, for each nonidentity member of the finite stabilizer, its fixed subspace on the dual is proper. A rational linear functional outside their finite union exists. The inequalities defining the cut cone are finitely many rational linear inequalities, so the cut is rational polyhedral even when the original cone has lineality.

For each point of the old weak domain, maximizing the functional on its finite stabilizer orbit places some translate in the cut. Thus the stabilizer translates cover the old domain. Full dimension is retained: a finite union of closed cones contained in proper linear subspaces cannot cover a full-dimensional cone. Interior of the cut is contained in interior of the old domain.

For a nonidentity stabilizer element, the pertinent comparison functional is nonzero and nonnegative on the cut, hence strictly positive in its interior. Applying its inverse comparison to a hypothetical intersecting translate gives two contradictory inequalities. Elements outside the stabilizer are excluded by the original weak-domain separation. This establishes closed-translate/interior separation and trivial setwise stabilizer, not merely weak separation. No missing infinite-group or pointedness assumption was used.

## 2. Finite-kernel lift

I checked all three substantive hypotheses rather than treating them as conclusions: the rational equivariant quotient, finite kernel, and full-dimensional rational polyhedral lifted cone. The quotient-domain image identity used in the proof follows directly: because Q is contained in p(C), every point of Q has a preimage in C that belongs to D, so p(D)=Q. Full dimension of D also forces full dimension of Q in the quotient; this agrees with the registration statement.

Given quotient coverage, any point of C is moved by an actual group lift to D, giving coverage upstairs. An open linear quotient sends an interior point of D to an interior point of Q: project a sufficiently small open neighborhood contained in D. Thus an element outside the kernel cannot send D into its interior. The kernel preserves D exactly because it acts trivially on the quotient. Hence the setwise stabilizer is exactly that finite kernel; the preceding finite-cutting proof applies.

The registered statement accurately retains the finite-kernel and lifted-polyhedrality hypotheses. It does not establish them for an arbitrary Calabi–Yau fibration. This dimension-free implication is fully proved, but it does not prove the parent cone conjecture.

## 3. Integral-shear obstruction

For the displayed half-plane, the lineality is rational and fixed pointwise. The faithful quotient numerical image is trivial. Coverage of the fixed boundary line forces the full boundary line into any proposed convex conical domain. Coverage of a positive-height point forces one positive-height point into that domain. Convex-conical closure under addition and nonnegative scaling then includes every horizontal line at positive height, so the domain equals the whole half-plane. Its shear translate equals itself and meets its nonempty interior, contradicting ordinary-domain separation.

The proof does not rely on polyhedrality and correctly identifies the infinite quotient kernel. The entire half-plane is a rational polyhedral weak domain. The registration explicitly limits this to a counterexample to an abstract automatic-lifting assertion and does not claim a geometric Calabi–Yau counterexample.

## 4. Closed-nef obstruction on E × E

I independently reopened the primary input, Prendergast-Smith, *The Cone Conjecture for Abelian Varieties*, J. Math. Sci. Univ. Tokyo 19 (2012), the polarization construction in section 4 and Theorem 4.3, pp. 254–256:

https://www.ms.u-tokyo.ac.jp/journal/pdf/jms190202.pdf

For an elliptic curve with End(E)=Z, the product principal polarization gives the rational symmetric-matrix model; the ample cone is positive definite, and its closure is the positive-semidefinite cone. This is a standard cited input, not a theorem newly proved in this increment.

The rank-one matrix vvᵀ with v=(1,√2) is positive semidefinite and spans an extreme ray. Indeed a positive-semidefinite summand must annihilate the kernel of vvᵀ, hence has image on its one-dimensional image and is a nonnegative multiple. A nonzero rational matrix cannot be on this ray: its (1,1) entry forces the multiplier rational, and its off-diagonal entry then gives a contradiction.

Any proposed rational polyhedral subcone is generated by finitely many rational positive-semidefinite matrices. Extremality forces each active generator in a representation of a point on the ray to lie on that ray, which is impossible. Every numerical automorphism translate remains a rational polyhedral nef subcone, so no such domain covers the full closed nef cone.

The proof that the ray is not effective is also correct: translating an effective divisor avoids any given curve and does not change its numerical class, so every effective divisor is nef on an abelian variety. A finite real effective decomposition would therefore be a positive-semidefinite decomposition by rational generators, already excluded. The same argument excludes the ray from the rational hull. This is consequently a counterexample only to the stronger entire-closed-cone formulation; it does not contradict the effective conjecture.

## 5. Additional frozen calculations and scope language

The rejected E × E mixed-class test in section 5 has the stated intersection numbers: the three elliptic divisors have self-intersection zero and pairwise intersection one, so P·H₂=0 and P²=−2. All contracted curves are fibers, and hence P is relatively numerically trivial. The proof correctly refuses to promote this into a nonzero relative class invisible on the generic fiber.

The clarification `formulation_precision.md` resolves the two ambiguities raised in my earlier scope review: it writes Li's ordinary and weak domain conditions explicitly, and it leaves the non-Q-factorial Cartier-action representation as an open formulation obligation. The original frozen packet bytes are transparently preserved, and the precision file is an additional frozen input. The registration keeps the unrestricted mission open and does not add hidden dimensional assumptions.

The artifact-note descriptions of other research and literature are context; this review does not validate unregistered mathematics outside the displayed proofs, audit every cited paper, or independently verify my own separate literature report. No originality assessment is made.

## 6. Final scope of approval

No blocking gap was found in the finite-stabilizer proof, the finite-kernel implication, or either registered obstruction. All exact hypotheses match the registration batch. Approval covers only this small publication increment, with the parent registered OPEN. It is not approval of the full Morrison–Kawamata conjecture, the previous child manuscript, exhaustive literature verification, external peer review, or formal certification.

## Exact frozen content references read

1. `research/runs/ultimate-boss2-20261123/studio/artifact-notes/5c8f760e5341b2fd79bf7f6c623b0a2488ef8fc990894006cfeda0b055d5d430.md` — SHA-256 `5c8f760e5341b2fd79bf7f6c623b0a2488ef8fc990894006cfeda0b055d5d430`

2. `archives/morrison-kawamata-cone/state/cone_obstructions_and_lifting.md` — SHA-256 `a25e938d5c633fee83fe72b20cfaf5f55e982f67cd2e538367302e5ed869d82b`

3. `research/workspaces/ultimate-boss2-20261123/records/registration-batch.json` — SHA-256 `79ad9de232622998188a14d11f1e7211bce3d09a07ff809492f15f359797c0df`

4. `research/runs/ultimate-boss2-20261123/studio/artifacts/MKC-INITIAL-AUXILIARIES/3d7102ff04551c64211e615a0c86defd726314d6f910a775b44d928983cf7728.json` — SHA-256 `7b7ec39a862882d8d4f18e2f53e9bc9556ffe32d00329052dbe757e0d14f46a9`

5. `research/workspaces/ultimate-boss2-20261123/spec.json` — SHA-256 `45579c17f5e6b4e811141d62e5f44df8a38677979d25f98dccc0067241fa6718`

6. `research/runs/ultimate-boss2-20261123/packet-full.json` — SHA-256 `34bf2e1ea1dd04552da8f9723cd6164ef49965081432bfcc840c6a17f4d7789a`

7. `archives/morrison-kawamata-cone/state/mission_original.md` — SHA-256 `f1aa7ca43bcff65f02bd5f0e99c78278f6b5720cbec4d56e9c182e51444da16c`

8. `archives/morrison-kawamata-cone/state/definitions.md` — SHA-256 `3728e0bb32149dcf7022275a00ff2606f238c2dd5c84a79def5e596ae3a7b299`

9. `research/runs/ultimate-boss2-20261123/packet-obstacle.json` — SHA-256 `d39ab7b75d9208f480b2b4537472266f1d241ee2eb28e229fb50c60f13978c93`

10. `archives/morrison-kawamata-cone/state/formulation_precision.md` — SHA-256 `e2c46e5b098ade7c41f9c25a73c75556ec57fd634d7da86f4e39354071a53953`

11. `archives/morrison-kawamata-cone/state/cone_obstructions_and_lifting.md` — SHA-256 `a25e938d5c633fee83fe72b20cfaf5f55e982f67cd2e538367302e5ed869d82b`; section `3. A precise finite-kernel lifting theorem`

12. `archives/morrison-kawamata-cone/state/cone_obstructions_and_lifting.md` — SHA-256 `a25e938d5c633fee83fe72b20cfaf5f55e982f67cd2e538367302e5ed869d82b`; section `2. What finite stabilizer cutting actually proves`

13. `archives/morrison-kawamata-cone/state/cone_obstructions_and_lifting.md` — SHA-256 `a25e938d5c633fee83fe72b20cfaf5f55e982f67cd2e538367302e5ed869d82b`; section `1. A quotient cone can conceal an obstruction to a strong domain`

14. `archives/morrison-kawamata-cone/state/cone_obstructions_and_lifting.md` — SHA-256 `a25e938d5c633fee83fe72b20cfaf5f55e982f67cd2e538367302e5ed869d82b`; section `4. A geometric counterexample to replacing the effective cone by the entire closed nef cone`

