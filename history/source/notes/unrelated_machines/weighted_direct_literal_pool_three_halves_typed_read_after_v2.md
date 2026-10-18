# Weighted direct literal pools v2 — actual author-proof read-after

Date: 2026-10-18. Reviewer: typed_edge_gap. Scratch only; not a new canonical claim or asset.

## Read order and provenance

I first read the new v2 Exact and independently reconstructed its full weighted scheduling upper bound. That reconstruction was frozen before the author Proof or its algorithm was supplied to me:

`weighted_direct_literal_pool_three_halves_typed_exact_first_v2.md`

SHA256 `5aa835cabfe7bf94ef43c554692e132ad6d06e80f6e38707970d6b07e32265be`.

The Exact source was:

`weighted_direct_literal_pool_three_halves_statement_only_v2.md`

SHA256 `d3e958202875617bd2bf2f189fee6b98606ce346ab0342b46cd5c5632b3f743f`.

After root actually read that frozen record, root released the author Proof. I have now actually read its entire contents, without truncation, and verified its SHA:

`weighted_direct_literal_pool_three_halves_author_proof_v2.md`

SHA256 `d882cfde4ea352687eb86ad4ad5e54ef621ac10594ef99e52a0b95aca4934f3e`.

My prior candidate authorship and familiarity with standard matching remain disclosed. Root's author Proof states that root derived its construction before routing the Exact and wrote the file after reading my frozen reconstruction; root is not being described as a blind reviewer. This read-after does not change or retroactively replace the earlier frozen proof.

## Actual proof check

Verdict: PASS. No mathematical, object-domain, or bit-complexity discrepancy was found within the stated v2 scope.

The author's construction uses an auxiliary slot for the top occurrence of each sign of a variable, merging those two top occurrences into the same slot. The remaining occurrences on each sign are paired as ranks (2,3), (4,5), and so on, with a possible final singleton. Every slot therefore contains at most two original occurrences, including the merged top slot. For every clause c the fractional mass 1/k_c on each of its original occurrences supplies row sum 1 and slot sums at most 1, since k_c>=2. This remains true when two occurrences of one clause enter the same slot. Integral bipartite matching covers all clauses, with an original occurrence witnessing every chosen edge.

At most one top occurrence of a variable's two signs can be selected. Its original f job is placed at a sign whose top occurrence was not selected, or at an empty sign. On that sign, the selected weights are bounded by w_2+w_4+..., because each remaining pair contributes at most its first and larger weight. Since w_(2t)<=w_(2t-1), this sum is at most half of the full eligible weight sum, hence at most 1/2. The other sign uses only a subset of its full eligible budget and has load at most 1. This is a simultaneous construction over all variables and clauses; choosing f destinations afterward does not alter any clause choice.

The final schedule exports exactly the actual matched query of every clause and puts that clause's actual selector at its now-empty original root. Every unselected original query remains at its own root. Every f uses one of its two original time-1 pool endpoints. Distinct occurrence identities guarantee no root collision even with repeated variables or literals. Therefore every root has load 1, every f-occupied pool has total load at most 3/2 and query-only load at most 1/2, and every other pool has load at most 1. There are no extra physical slots or virtual executed jobs.

Zero weights are retained in the sorted lists and actual assignment. Empty signs and unused variables present no difficulty. An empty formula leaves only the original f jobs, and the fully empty case uses the specified idle machine. The construction only needs the listed arity and nonnegative full-sign-budget assumptions; it does not use SAT, supplied strict witnesses, or a positivity assumption. In particular this certification does not add a strict-SAT equivalence for zero-weight inputs.

The graph has linear size in the explicit occurrence description and sorting uses binary-rational comparisons. Fractional masses are only feasibility certificates; the algorithm does not copy occurrences by denominators or by inverse processing times. Deterministic integral matching and the final actual assignments are total-bit-polynomial. Original counts and all finite processing entries remain those of the Exact.

## Relationship of the two reconstructions and scope

My frozen proof instead puts each f half at each pool and makes unit slots from the sorted fractional occurrence lengths 1/k_c. An f can occupy only a first slot; a query touching later slot ell has rank at least 2ell-2, giving the same even-rank half-budget estimate. The author's merged-top and remaining-pairs construction is a different, simpler discrete realization of the same estimate. Neither proof is represented as the other's prior independent evidence.

Only the v2 compiler with its full eligible-sign budgets at most 1 and independent occurrence roots is certified. Extra endpoints, guards, changed budgets, or general UM are outside this conclusion. There is no new sharpness, complexity-hardness, or global originality claim. No numerical test was necessary or run, and no repository, Work, or Git change was made.
