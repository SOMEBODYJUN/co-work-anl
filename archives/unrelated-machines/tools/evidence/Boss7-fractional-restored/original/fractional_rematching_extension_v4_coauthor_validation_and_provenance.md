# v4 coauthor validation and actual-reading provenance

2026-10-18. General_query_response_review, with root as co-developer. Scratch only.

## Identity and release boundary

This is a coauthor validation/provenance record for the new statement-only v4, not an independent blind mathematical review. Before constructing v4 I had received root's algorithmic proposals and detailed proof sketches, and actually read both standalone tools' Exact statements, independent review records, author proofs, and author-proof read-after records. I also actually read rank's frozen v3 review. None of this knowledge is being reclassified as statement-first independence.

No full NSW v4 author Proof is written here. The separate independent reviewer must receive only the v4 Exact, not this record or earlier strategy/proof messages, until their Exact-first record is frozen and root has actually read it. The old v1/v2/v3 Exact files, prior reviews, and the disputed source-numerical history were not edited.

## Actual files read

All paths below are relative to /workspace/scratch/038d9dcc4cac. The accompanying manifest records full SHA-256 values.

1. fractional_rematching_extension_statement_only_v3.md, actually read in full and used only as the immutable A/C/D/E source, with B and F replaced and downstream deterministic wording changed.
2. fractional_rematching_extension_rank_exact_first_review_v3.md, actually read in full. Its objection to the old generic-subadditive B remains standing for that old version; it is not declared disproved or silently repaired.
3. weighted_bernoulli_shifted_inverse_moment_statement_only_v1.md.
4. weighted_bernoulli_shifted_inverse_moment_independent_exact_review_v1.md.
5. weighted_bernoulli_shifted_inverse_moment_author_proof_v1.md.
6. weighted_bernoulli_shifted_inverse_moment_author_proof_read_after_review_v1.md.
7. finite_grid_label_mask_log_potential_derandomization_statement_only_v1.md.
8. finite_grid_label_mask_log_potential_derandomization_v1_independent_review.md.
9. finite_grid_label_mask_log_potential_derandomization_author_proof_v1.md.
10. finite_grid_label_mask_log_potential_derandomization_v1_author_proof_read_after.md.
11. The resulting fractional_rematching_extension_statement_only_v4.md, actually read back in full without truncation after construction.

One initial combined tool output truncated the mask-review portion. I subsequently reread both complete mask review/read-after files separately. The complete-reading claim refers to that later successful read.

I compared the full Section A excerpt, from its header to immediately before the B header, mechanically with v1, v2 and v3. All are byte-identical: 3565 UTF-8 bytes, SHA-256
1c1250fb4e62c641d2bdc1d688d967cc5334e999ad61862a2641c1e3bd0f4828.

## Primary reading actually used

Primary source: Dobzinski--Li--Rubinstein--Vondrak, arXiv:2309.04656v1,
https://arxiv.org/html/2309.04656v1

Earlier primary reading is recorded in the pre-existing research history; it is not relabeled as new reading. During this revision I additionally reopened the actual HTML text of the complete SetSplitting and finite-round argument (Section 2.3 and Section 2.4 through Lemma 5), the finishing comparison in Section 2.5, and the full Appendix B proof of arbitrary-comparison-matching Lemma 9. Anchor-only requests initially returned the beginning of the document; the subsequent line-specific open returned the intended source text. I am not claiming a new full-paper or full-PDF read in this revision.

The primary integral-OPT theorem is not a fractional log-CONFIG statement. The new fractional matching interface is A. The new residual solver, XOS support rounding, inverse moment, and grid-label DP are co-developed replacements. The generic-subadditive concentration constants and old Section 2.5 end constant are not imported as validated numerics.

## Actual checks of the new assembly

Verdict on the co-developed v4 statement: no fatal mathematical or bit-complexity obstruction found. This is a coauthor verdict pending the new independent Exact-first review.

- Fixed lift and solver: arbitrary finite fractional residual utility vectors map into R by choosing an attaining clause separately on each configuration. Nested thresholds recover an actual configuration family with utility V>=x. Baseline b lies in R; the maintained set b/4+3R/4 supplies the lower bound ell. With M>2a the logarithmic progress estimate is at least a*ell^2/8 per update. The bound 128Q^3a^3 is conservative. The actual algorithm uses only rational LPs and rational convex updates.
- Bit length: every LP is on the same fixed lambda/z polytope and returns a basic optimal vertex. Its vertex bits have a fixed-matrix bound, independent of the objective 1/x. Coordinate bits of the maintained lift therefore grow additively over polynomially many updates, not by iterating an unspecified polynomial bit bound. All divisions are rational representations, not expansions by reciprocal numerical values.
- Support rounding: independent configuration choices give itemwise bid-event probability sum at most one. Conditional expectation of the finite maximum-bid proxy is exactly rational and is fixed one agent at a time. The final bundle stays within that agent's chosen support configuration, and the welfare factor 1/2 is valid. The conservative joint choice remains d=5/2.
- Preprocessing: for XOS, an attaining clause gives the required disjoint parts directly. k=floor(3v(T)/V) is at most |T|/2 in the large-agent branch. Deleting items until actual value is at most V preserves the stated lower bound; inherited mass is at least one before normalization, so item capacities do not increase.
- Candidate rounds are fixed before any labels. There are at most |A''| rounds, and each round removes at least a delta fraction, rounded up. Thus the geometric label bound is valid for each agent's fixed candidate set. No candidate set, attaining clause, or remaining-agent choice depends on later labels.
- Inverse moment and mask: all clause weights are at most nu and on the 1/Q grid, with total at most one. The standalone inverse inequality applies to the independent per-item label marginals. The label DP fixes those same actual items, preserving within-round and across-round disjointness. With total potential error one, the average log bound is at most ln(6/delta^2)+1+1/|A''| <= ln(6e^2/delta^2) < ln(54/delta^2) < ln(200/delta^2).
- Rematching: the source's arbitrary-pi structural lemma is applicable to the same initial maximum-product singleton matching and actual residual bundles. Combining it with the deterministic 200/delta^2 estimate keeps the extra factor three. The resulting safe backend is 60000d^2, not the smaller printed end constant. Zero comparison products are vacuous; the final product is positive because the initial singleton matching remains available.
- Normalized interface: Q=4m flooring is internal only, preserves every original support benchmark at value at least 3/4, and has polynomial numerical Q. B with A gives at least 1/1125000 of a grid fractional benchmark; the statement deliberately retains the weaker 1/2250000 reserve, yielding C's 1/3000000 > 2^-24. Original states are recovered using the original coefficients, not the floor table.
- Quantifiers and jobs: C's counts are over the same n original groups. D's only augmentation is n groups sharing D added singleton resources, with no extra agents. Its promised NO count loses at most D; deterministic FSLP feasibility is a sufficient promise test. E assigns every original selector and incidence once, including zeros and all unselected-state jobs; original selected-root load is 2-r_g, with no floor-coefficient substitution.
- Limits: unweighted geometric mean supplies only the stated low-quality count/tradeoff. It does not rule out arbitrary fixed positive robust fractions at arbitrary fixed thresholds, a core fraction depending on a target accuracy, or all-group min-quality gaps. The grid algorithm is not asserted for unrestricted tiny binary XOS benchmarks at bit cost independent of Q.

## Freeze identity

v4 Exact:
fractional_rematching_extension_statement_only_v4.md

SHA-256:
de055b02aca6d3876628671638bd509c16a1716d052b489d265e2303d37c400a

All old byte strings remain intact. This record asserts mathematical/finite-representation validation and actual source reading, not an implementation run, software audit, external independent approval, or mature research registration.
