# Independent scope and routing review of the parent opening

Reviewer: ultimate_ideas worker, not the author of the reviewed parent files.
Date: 2026-11-23.
Scope: task fidelity, Li-2023 interpretation, and archive links. This is not a proof audit or a declaration that the conjecture is solved.

## Reviewed versions

| Path under archives/morrison-kawamata-cone | SHA-256 at review |
|---|---|
| state/mission_original.md | f1aa7ca43bcff65f02bd5f0e99c78278f6b5720cbec4d56e9c182e51444da16c |
| state/definitions.md | 3728e0bb32149dcf7022275a00ff2606f238c2dd5c84a79def5e596ae3a7b299 |
| README.md | a7387607b38d22f2516a5e05265da3e0d3466d922fc0f84705b2c0987407f893 |
| prompts/pro-loop.md | 9bc16595f51f8d2e3adc467ee49ec1aa326616ed33c8eea36ff1c4629d08b540 |
| subarchives/relative-movable-rel2/README.md | 44c6e7dd366b6aae4a1674841a409f5dcb97e4523757f22850bca27436f8ffc2 |
| archive_relations.json | 34d9a460bd94d989064e2a19735dd8a712f35535d03b68e9f4ab879ef84568d3 |

## Findings

1. **Parent target preserved.** The mission retains all dimensions, both absolute and relative settings, nef and movable domains, and both finiteness conclusions. Its PASS condition is conjunctive. No K3, relative-dimension-two, irregularity-zero, deformation-type, or pointedness condition has been inserted into the parent target.

2. **Li variant correctly identified, with one definition needing precision.** I independently opened https://arxiv.org/html/2309.04673v1 . Conjecture 1.1 indeed uses the movable and ample rational hulls and permits weak domains. Its section-2 setup has connected fibers and Q-factorial total space. Section 3, Definition 3.3, defines a weak domain by coverage plus
   \[
   \gamma P=P\quad\hbox{or}\quad\gamma P\cap\operatorname{Int}(P)=\varnothing.
   \]
   An ordinary domain additionally has trivial setwise stabilizer in the faithful numerical group. The reviewed definitions.md says “disjoint interiors for distinct numerical translates,” which is ambiguous if distinct refers to distinct sets; it also tracks trivial stabilizer as an optional stronger condition. **Recommended correction:** state Li's two displayed alternatives and the ordinary-domain stabilizer condition explicitly, then distinguish the customary interior/interior wording. The user requested Li's precise definitions, so that stabilizer condition should not be silently omitted from Li's ordinary-domain version.

3. **Non-Q-factorial extension needs a representation obligation.** The parent correctly leaves the non-Q-factorial scope open. However, it first speaks of the pseudo-automorphism action on the Cartier numerical space as though its existence were automatic. Strict transform is directly available on Weil divisors, and the Q-factorial source setup is relevant to obtaining an action on the stated Cartier numerical space. **Recommended correction:** explicitly require construction/justification of the representation and preservation of the cone for the unrestricted non-Q-factorial setting. Do not assert that a proof on a Q-factorialization alone supplies this.

4. **Other formulation bridges remain open.** The draft correctly records support-preserving versus coefficient-preserving groups, numerical versus relative linear triviality, generic versus geometric-generic versus very-general fibers, and rational hull versus actual effective cones as matters requiring evidence. Its finite-index observation is elementary and does not pretend to prove the required domain transfer in a degenerate cone.

5. **Child status not promoted.** Both parent and child correctly say that even a correct proof of the previous terminal, relative-dimension-at-most-two movable target is PARTIAL for the new problem. The canonical old proof is indexed rather than copied or moved. The new parent does not turn its historical internal reviews into external certification or a new general theorem.

6. **Canonical routing checked.** From the child README, ../../README.md resolves to the new parent and ../../../relative-mk-cone/README.md resolves to the old canonical archive. Both scopes in archive_relations.json exist. The JSON explicitly calls the relationship a logical index rather than a physical migration.

7. **Three parent links still pending during this review.** README.md linked to state/research_status.md, state/literature_and_strategy.md, and state/cone_obstructions_and_lifting.md; these files did not yet exist at the checked moment. This is a deliverable-assembly issue, not a mathematical objection. They must exist or the links must be changed before final publication.

8. **Execution prompt stays on the full target.** It requires real mathematical work, preserves the three-worker arrangement, and makes saving/pushing distinct from success. It requires honest OPEN/PARTIAL reporting and does not introduce Lean/Coq as a requirement. It does not certify that the full research or literature audit has already been completed.

## Review conclusion

The parent opening preserves the intended unrestricted problem. Before calling the opening package internally checked, resolve findings 2, 3 and 7. This review establishes neither a proof of the parent conjecture nor a proof of the old child theorem. The claimed full-conjecture status must remain OPEN.
