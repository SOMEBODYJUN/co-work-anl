# Weighted direct literal pools v2 — independent Exact-first reconstruction

Date: 2026-10-18. Reviewer: typed_edge_gap, internal boss11 collaborator.

This is a scratch review, not a new repository claim or asset. The reviewer is the original direct-pool candidate proposer and is familiar with standard fractional-slot matching and the previous uniform special case. This is therefore an independent reconstruction from the new Exact, not a claim of blindness to those general techniques or to the candidate's history.

The only new v2 source read before this record was frozen was
`weighted_direct_literal_pool_three_halves_statement_only_v2.md`, SHA256
`d3e958202875617bd2bf2f189fee6b98606ce346ab0342b46cd5c5632b3f743f`.
The source was actually read in full. No root author Proof or root algorithm for this v2 was read or supplied before this freeze. The prior uniform-case reconstruction is not being applied as an unproved weighted flow assertion. The proof below includes its own weighted rounding argument.

Verdict: PASS, with the stated domain and scope. All original jobs receive actual assignments; the simultaneous query-only bound on every pool containing its original f job holds.

## 1. Exact object and scope reconstructed

Let the explicitly listed CNF have N variables, M clauses, and L occurrence identities. Every clause c has k_c >= 2 occurrences. Repeated variables and repeated literals are still distinct occurrences. Each occurrence e has a nonnegative binary rational b_e. For each variable v and each of its two signs,

    sum of b_e over all eligible occurrences of that sign of v <= 1.

Thus every individual b_e is at most 1. These are budgets over all eligible occurrences, not merely over the occurrences ultimately selected by the algorithm.

The actual unrelated-machines instance has pools A_v+, A_v- and job f_v, with processing time 1 on either pool. Each occurrence e has its own distinct root R_e and query j_e, with processing times 1 at R_e and b_e at its own literal pool. Clause selector s_c has processing time 1 at each of that clause's occurrence roots. All other processing times are infinity. There are no extra tasks, guards, preloads, side constraints, or witness schedules.

The counts are machines 2N+L, jobs N+L+M, finite entries 2N+3L. When N=L=0, add one idle machine. In a well-formed CNF with these clause arities this case also has M=0.

We prove exactly the stated scheduling upper bound. We do not infer a general UM approximation, a hardness result, or an additional strict-SAT equivalence with zero weights. Positivity is unnecessary for this upper bound.

## 2. A fractional matching that includes the actual f jobs

The following graph and fractional quantities are computational devices; they do not split any job in the final schedule and their slot vertices are not new physical machines.

Create one left vertex for each clause c and one left vertex for each original f_v. For every occurrence e in clause c, give the clause a fractional entry of length

    x_e = 1/k_c <= 1/2

at e's literal pool, with weight equal to the real processing time b_e. Give f_v a fractional entry of length 1/2 at each of A_v+ and A_v-, with weight 1. Every left vertex has total fractional length exactly 1.

At each pool, sort all these entries by nonincreasing weight. Put its f entry first among ties of weight 1. The f entry is therefore the first entry and occupies the interval [0,1/2]. Lay the remaining fractional entries consecutively after it. Divide the resulting interval into consecutive slots of length 1, allowing a final partially occupied slot. Positive-length overlap defines adjacency: a clause vertex is adjacent to each slot touched by one of its own occurrence entries, and f_v is adjacent to the first slot of each of its two pools. Store an actual witnessing occurrence for each clause-slot edge. Parallel occurrence witnesses may be retained, or any deterministic witnessing occurrence may be stored if edges are coalesced.

Assign to an edge the total length of its corresponding overlaps. This is a fractional matching: every left vertex has total incident value 1 and every slot receives at most 1. A unit-capacity bipartite matching therefore covers every clause vertex and every f vertex. Equivalently, use the integral maximum-flow theorem on the graph with unit source-to-left, left-to-slot, and slot-to-sink capacities. This can be found deterministically.

For each matched clause c, let e(c) be an original occurrence witnessing its matched slot. For each f_v, its matched slot is the first slot of one of its two original pools. The matching simultaneously chooses one such destination for every original f_v and one original occurrence for every clause.

## 3. Weighted half-budget lemma at an f-occupied pool

Fix a pool containing its matched original f_v. Its first slot is consumed by f_v, so a matched clause at this pool must use a slot with index ell >= 2.

List every eligible query occurrence at this pool in its sorted order, with weights

    w_1 >= w_2 >= ... >= w_n >= 0,

and fractional lengths x_1,...,x_n, each at most 1/2. Zero weights remain in this list. Let Q_j = x_1+...+x_j. Then Q_j <= j/2. The right endpoint of the j-th query entry on the slot line is 1/2+Q_j.

If the j-th query entry has positive overlap with slot ell >= 2, its right endpoint is strictly greater than ell-1. Consequently

    1/2 + Q_j > ell-1,
    j/2 >= Q_j > ell-3/2,
    j > 2ell-3,
    j >= 2ell-2.

The strict inequality is important: touching a slot boundary at one endpoint alone creates no matching edge. Thus any actual witnessing occurrence chosen from slot ell has processing time at most w_(2ell-2). If such a slot is adjacent to a query entry, that index exists. Since the matching uses each slot at most once, the total actual query load assigned to this f-occupied pool is at most

    w_2 + w_4 + w_6 + ...
      <= (w_1 + w_2 + ... + w_n)/2
      <= 1/2.

The first inequality pairs w_(2t) with the no-smaller w_(2t-1); any final unpaired odd term only improves the bound. This argument holds for every pool that the one global matching chooses for an f job. It does not require preselecting each f destination separately.

For the other pool of the same variable, the chosen query occurrences are a subset of its original eligible occurrences. Each clause is matched once, and each occurrence belongs to exactly one clause, so no query is duplicated. Its load is at most its full eligible budget 1, regardless of which slots were used there.

## 4. Actual complete schedule

For every clause c put its actual selector s_c at its actual root R_e(c), and move exactly its witnessing query j_e(c) to that occurrence's own literal pool. Put every other original query at its own root. Put each original f_v on the pool whose first slot matched f_v.

Occurrence roots are distinct, including for repeated literals. Thus a selected root contains only its clause selector, of load 1; every other root contains only its query, also of load 1. A pool with f has total load at most 1+1/2. Its other pool has load at most 1. All assignments use finite entries of the original matrix, and all N+L+M original jobs execute exactly once. No virtual task or slot is included in the actual schedule.

This proves actual makespan at most 3/2, root loads at most 1, and query-only load at most 1/2 at every f-occupied pool, with the exact selected-query form required by the statement.

## 5. Boundary cases and computational size

Zero b_e entries are retained as real query jobs. They may be chosen as witnesses and then contribute load zero; otherwise they execute at their original roots with time 1. The fractional entry lengths depend on k_c, not on b_e, so zero or extremely tiny weights cause no missing jobs or denominator expansion. Sorting with f first among ties also handles b_e=1 exactly.

An empty formula with unused variables has only the f jobs and their two pools; the same matching or a direct arbitrary pool choice schedules them with makespan 1. If N=L=0, the specified idle machine gives a legal instance with no jobs and load 0. Nonempty clauses always have at least two occurrences, so x_e<=1/2 is valid; unit and empty clauses are outside this Exact. Repeated occurrences have separate roots, query identities, and fractional entries; a clause node still selects exactly one original occurrence.

Each pool receives one length-1/2 f entry and occurrence entries of length at most 1/2. Therefore the number of slots over all pools is O(N+L). Each occurrence entry overlaps at most two slots and each f has two first-slot edges, so the bipartite graph has O(N+L+M) vertices and O(N+L) witnessing edges before optional parallel-edge coalescing. A standard deterministic augmenting-path algorithm is sufficient.

Exact sorting uses the binary rational b_e values. Fractional endpoints are sums of 1/k_c and 1/2. Their numerators and denominators can be represented with polynomial bit length: a product of the input arities has logarithm at most the sum of their logarithms over the explicitly listed occurrences. No expansion by that product is performed. Rational comparison, taking integer slot boundaries, construction of positive-overlap edges, and matching are all total-bit-polynomial. No runtime factor depending on 1/b_e is used. The graph construction and schedule also remain polynomial relative to an explicitly listed dense original matrix.

## 6. What this establishes

The occurrence-weighted direct-pool compiler in this Exact is ruled out as a near-2 source, including nonuniform weights within a single sign of a variable. The weighted argument genuinely differs from the prior uniform variable-capacity count flow: it jointly rounds the f choices and clause choices, and uses the half-length/even-rank bound to protect the occupied pool.

This is a standard sorted-slot matching technique with the displayed problem-specific estimate, not an originality claim. Extra endpoints, extra guards, cross-clause coupling, or budgets exceeding the stated full eligible sums are not covered. No experiments were needed or run, and no root author Proof was read before freezing this record.
