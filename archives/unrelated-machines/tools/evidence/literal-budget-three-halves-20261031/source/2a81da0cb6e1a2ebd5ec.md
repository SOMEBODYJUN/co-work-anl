# Frozen independent Exact-first attack: occurrence-weighted direct literal pools

Date: 2026-10-18. Role: independent internal attack, before access to any author proof, typed review, or canonical repository material.

## Actual input and read scope

I actually read the complete file `/workspace/scratch/038d9dcc4cac/weighted_direct_literal_pool_three_halves_statement_only_v2.md` using `cat`, then computed its SHA256 using `sha256sum`:

`d3e958202875617bd2bf2f189fee6b98606ce346ab0342b46cd5c5632b3f743f`.

Before freezing this document, that statement was the only mathematical source file read. In particular, I did not read any author proof, typed review, or canonical repository file. No repository edits, Git commands, external communications, credentials, or network research were used. The derivation below was reconstructed from that Exact statement.

## Result

The Exact claim is true. A deterministic bipartite matching construction gives the requested actual schedule. Rational weights are used only to sort occurrence identities within each literal pool. No expansion in a denominator or in the reciprocal of a positive weight is needed.

Let a pool have its eligible original occurrence queries ordered by nonincreasing weight:

`q_1, ..., q_d`, with `b_1 >= ... >= b_d >= 0`.

Ties are broken by original occurrence identity. Create a first matching slot containing the possible jobs `{f_v, q_1}` (or just `{f_v}` when `d=0`). For each `h=1,...,floor(d/2)`, create another slot containing `{q_(2h), q_(2h+1)}`, omitting the second member when its index exceeds `d`. Thus all occurrence queries appear in exactly one slot of their original literal pool. Create these slots separately for each of the two pools of every variable; the same `f_v` can use the first slot of either of its pools.

In addition, create exactly one matching slot for every original root `R_e`.

## Matching graph and fractional certificate

The left vertices are all actual original jobs, without removing zero queries or any other jobs. The right vertices are the pool slots above and the root slots. Add the following edges:

1. Each `f_v` is adjacent to the first slot in each of its two original pools.
2. Each occurrence query `j_e` is adjacent to its own root slot and to the unique slot containing it in its original literal pool.
3. Each clause selector `s_c` is adjacent to the root slot of each original occurrence in clause `c`.

Repeated occurrences have distinct roots, query identities, and matching edges. An occurrence belongs to exactly one original clause.

For existence only, put mass `1/2` on each edge of an `f_v` and on each edge of an occurrence query. If clause `c` has `k_c >= 2` occurrences, put mass `1/k_c` on each edge of `s_c`.

Every left vertex has total mass exactly one. The first slot of a pool receives at most `1/2` from its `f_v` plus `1/2` from `q_1`. Every other pool slot receives `1/2` from each of at most two occurrence queries. The root slot for an occurrence in clause `c` receives exactly `1/2 + 1/k_c <= 1`. Hence each right vertex has total mass at most one.

Consequently, for every set `S` of jobs, summing the masses incident to `S` gives

`|S| <= |N(S)|`.

This proves Hall's condition. Therefore a matching covers every actual original job. It can be found deterministically by the usual augmenting-path algorithm, scanning original identities and slots in a fixed order. The algorithm does not need to calculate or store the fractional certificate.

## Conversion to the exact required assignment

First interpret a matched root slot as its original root and a matched pool slot as its original pool. Thus every selector is on one of its original roots; every `f_v` is on one original pool; every query is on its own root or original literal pool.

For each occurrence whose root is chosen by its clause selector, its query must be matched to its pool: the root has only one slot and that slot is occupied by the selector. Keep that query on its pool.

For every other occurrence, place its query on its own original root, even if its initial matching assigned it to a pool. Its root contains no selector: only that occurrence's clause selector is adjacent to that root, and this selector chose another root. There is only one query eligible for that root. Moving this query therefore gives that root load exactly one and can only decrease its pool's query load.

The final assignment has exactly one selected original occurrence for each clause. Its query alone among that clause's queries goes to its pool; every other query stays on its own root. Every actual original job is assigned exactly once. All original zero queries and all original roots remain present.

## Pool bound, including the pool receiving `f_v`

Consider either pool with sorted weights `b_1,...,b_d`. If it receives `f_v`, then `f_v` occupies its first matching slot. Consequently `q_1` cannot initially be assigned there, and each later slot supplies at most one query. The largest possible query contribution from the slot containing `q_(2h), q_(2h+1)` is `b_(2h)`. Therefore its initial query-only load is at most

`sum_(h=1)^floor(d/2) b_(2h)`.

By sortedness,

`2 sum_(h=1)^floor(d/2) b_(2h) <= sum_(h=1)^floor(d/2) [b_(2h-1) + b_(2h)] <= sum_(i=1)^d b_i <= 1`.

So the query-only load of the pool receiving `f_v` is at most `1/2`. The cleanup conversion above only removes queries from pools. Adding the time-one `f_v` gives final total load at most `3/2`.

The other pool has no `f_v` and contains a subset of its own eligible occurrence queries. Their full eligible weight sum is at most one, so its total final load is at most one. This argument applies independently to every variable and every pool, while the matching and cleanup account for every job globally. No unrelated machine loads are added together or ignored.

At every selected root the only executing job is its time-one selector; at every unselected root the only executing job is its time-one query. Thus every root has load exactly one whenever roots exist. The scheduling makespan is at most `3/2` over the entire original matrix.

## Degenerate inputs and identities

- **Duplicate literals or variables in a clause:** treated as distinct original occurrences, roots, and queries. The selector's fractional mass uses the occurrence count, not a count of distinct literals or variables. The construction and bound are unchanged.
- **Weights equal to zero:** retained as jobs and graph vertices; deterministic tie-breaking gives an order. The sorted-sum inequality allows zero. A selected zero query still goes to its original pool as required.
- **Unused variables:** both pools have one first slot and no queries. Their `f_v` is matched to one of them, giving load one there and zero on the other.
- **No clauses:** there are no occurrence queries or root slots. All variable jobs are handled as above.
- **`N=L=0`:** since every clause must have at least two occurrences, `M=0`. There are no jobs. Return the stipulated idle machine and the empty assignment, with makespan zero.
- **Odd numbers of occurrences at a pool:** its last slot contains a pair when possible, or a singleton `q_d` when `d` is even; the even-index sum above covers both cases. For `d=1`, only the first slot exists and a pool receiving `f_v` receives no query.
- **Weights equal to one / ordering ties with `f_v`:** the construction explicitly puts `f_v` in the first slot and sorts only queries, so no implicit processing-time tie convention is needed.

## Determinism and total-bit complexity

There are `N+L+M` left vertices. A literal pool with `d` queries has `1+floor(d/2)` slots. Hence the pool slots number at most `2N+L/2`, and there are exactly `L` root slots. The matching graph has exactly `2N+3L` edges: two per variable job, two per occurrence query, and one per occurrence for selectors. This is linear in the explicitly listed original matrix size. The condition `k_c>=2` also gives `M<=L/2`.

Sorting within all literal pools uses polynomially many rational comparisons (for example at most `O(L log(max(2,L)))`). For nonnegative binary rationals written as numerator/denominator, compare by cross multiplication; the bit lengths of the resulting integer products are at most sums of input bit lengths. Fixed-order integer matching uses at most `N+L+M` augmentations, each polynomial in the graph size. It manipulates only graph indices, not numerical weights. The cleanup is linear in the original job and occurrence lists.

Thus the algorithm is deterministic and polynomial in the complete explicit input's total bit length. It never expands by a denominator, never divides by a weight, and requires no schedule witness or SAT solution. The argument proves only the Exact compiler's upper bound and does not claim a general UM approximation or novelty of matching techniques.

## Freeze statement

This complete construction and proof is the independent pre-author-proof result. It finds no fatal flaw in the Exact claim. The only statement source actually read before this freeze was the SHA-verified Exact v2 file named above.
