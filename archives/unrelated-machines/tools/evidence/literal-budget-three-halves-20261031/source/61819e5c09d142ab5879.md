# Author-Proof read-after audit, preserving the Exact-first independent record

Date: 2026-10-18. This audit was written after the root explicitly released the author Proof, and after the independent Exact-first attack had already been frozen and reported.

## Chronology and actual read scope

1. Before author-Proof access, I actually read the complete Exact statement `/workspace/scratch/038d9dcc4cac/weighted_direct_literal_pool_three_halves_statement_only_v2.md`, SHA256 `d3e958202875617bd2bf2f189fee6b98606ce346ab0342b46cd5c5632b3f743f`.
2. I independently reconstructed the all-original-jobs matching algorithm and froze `/workspace/scratch/038d9dcc4cac/sol_literal_budget_exact_first_attack.md`, SHA256 `c7595ac3593377a94ea61da549abac5cc0bdc466160bd29443021548b79d4c74`.
3. Only after the root reported actually reading that complete frozen record and expressly released the author Proof, I used `cat` to read the entire `/workspace/scratch/038d9dcc4cac/weighted_direct_literal_pool_three_halves_author_proof_v2.md`. Its complete tool output was 833 tokens and was not truncated. I separately used `sha256sum` and verified SHA256 `d882cfde4ea352687eb86ad4ad5e54ef621ac10594ef99e52a0b95aca4934f3e`.

The author Proof predates this new audit. Its own disclosed provenance says root wrote it after actually reading typed's earlier independent reconstruction, and root is not a blind reviewer. I have not read typed's reconstruction or any other typed review. Neither the author-Proof read nor this audit is being represented as a new independent derivation. My independent status applies to the frozen Exact-first record, which predates my author-Proof access.

Before freezing this audit I have not read any canonical repository file, other proof, other review, or other mathematical source. No repository edits, Git commands, external communications, credentials, or network research were used.

## Verdict on the released author Proof

The author Proof establishes the Exact claim. I found no fatal gap or unsupported extension of scope.

Its construction differs from my frozen one. The author matches **only clauses** to computational slots that contain actual occurrence identities. For each variable, the two first occurrences, one from each nonempty sign, share one special slot; if just one sign is nonempty the special slot contains that sign's first occurrence. The later occurrences of each sign occupy separate sorted pairs `(2,3),(4,5),...`, with a possible singleton. In contrast, my independent construction matches **every original job** to original root slots and separate pool slots; an `f_v` connects the two first pool slots, and each query connects its root to one pool slot. Both constructions use exactly the same sorted even-index estimate.

The constructions are equivalent for this purpose. In my construction, the two separate first pool slots have total capacity two, and `f_v` consumes one of them. Hence at most one of the two first occurrence queries can use its first pool slot. Eliminating that `f_v` choice gives the author's shared unit-capacity special slot for the two first occurrences. Root/query choices can likewise be eliminated: selecting an occurrence root for a clause exports that occurrence's query; all unselected queries may stay at their own roots. The author's graph performs these eliminations before matching, while my graph performs a full-job matching and then returns any extra exported queries to unused roots.

## Checks of the author's smaller matching graph

Every actual occurrence belongs to one clause and one computational slot. A clause with `k_c>=2` occurrences sends mass `1/k_c` through each occurrence to its slot. Thus its row sum is one. A slot contains at most two occurrences, and every occurrence mass is at most `1/2`, so its column sum is at most one. Hall's counting argument gives a matching covering all clause vertices.

If two occurrences of the same clause occupy the same slot, their masses add on the coalesced clause-slot edge. This causes no problem: the edge retains an actual occurrence witness, and the slot's total mass remains at most one. When the integral matching chooses that edge, choose any one of its original witnesses by a fixed identity rule. No witness can be used by another clause, since a computational slot is matched only once, and each occurrence is in only one clause. The construction therefore selects exactly one original occurrence for every clause, including clauses consisting of repeated literal or variable occurrences.

At most one first occurrence of a variable is selected because the two first occurrences share one slot. Thus there is a sign with an unselected first occurrence, unless a sign has no occurrences; an empty sign is immediately suitable for `f_v`. When both signs are empty, either pool works. On the chosen sign the first occurrence is absent, and at most one occurrence is selected from each remaining sorted pair. Therefore its selected query sum is at most

`w_2+w_4+... <= (w_1+w_2+w_3+...)/2 <= 1/2`.

Here the comparison uses the disjoint pairs `(w_1,w_2),(w_3,w_4),...`; any final odd-index weight merely increases the right-hand side. The other sign's selected weight is a subset of its complete eligible weight, bounded by one. All weights are nonnegative, and sorting and this inequality retain and allow zeros.

## Actual scheduling and all machine loads

For each clause, place its selector on the root of the chosen witness occurrence and put that exact query on its original literal pool. Keep every other original query on its own original root. Distinct clauses have disjoint occurrence identities and roots. Each root consequently contains exactly one time-one job: its selector when selected, otherwise its query.

Put `f_v` on the sign identified above. Its pool has total load at most `1+1/2`; the other pool has total load at most one. This is a simultaneous bound on every original machine, with no jobs omitted. The construction does not depend on interpreting a zero-weight export as a strict SAT implication.

Unused variables have no occurrence queries and their `f_v` has load one on either pool. An empty formula handles all unused-variable jobs in this way. If `N=L=0`, the clause-size condition forces `M=0`, and the prescribed idle machine has zero load and the assignment is empty. Repeated occurrences, retained zero queries, and unselected roots are all explicitly accounted for.

## Total-bit complexity and scope

The author graph has `M` left vertices and at most linear-in-`N+L` slots; it has at most `L` distinct clause-slot edges, each with an original occurrence witness. Sorting uses exact rational comparisons and deterministic identity tie-breaking. Comparing binary rationals by cross multiplication has polynomial bit complexity. Matching itself needs only integer graph operations and a fixed-order augmenting-path implementation; no fractional matching certificate need be constructed. The final schedule requires only original job and machine identities.

If the input budgets are also checked by exact rational summation, intermediate numerators and denominators can be kept with bit lengths polynomial in the total original encoding length: a common denominator formed as a product has bit length bounded by the sum of the input denominator bit lengths. Such checking is optional under the stated input promise. The scheduling construction needs no weight sums, denominator expansion, reciprocal weight, or numerical discretization.

The claim remains the failed-source salvage for this exact independent full-budget direct-pool compiler. Neither construction proves a general UM approximation, handles larger eligible budgets or additional guards/endpoints, nor supports a claim of novelty of standard matching machinery. Those limits in the author Proof agree with the Exact statement.

## Frozen conclusion

Accepted after actual full author-Proof reading, with the chronology above. The author construction is a different but equivalent clause-only realization of the independent all-job sorted-slot matching argument. The independently frozen Exact-first record remains unchanged, and this read-after audit does not relabel it or the root as blind.
