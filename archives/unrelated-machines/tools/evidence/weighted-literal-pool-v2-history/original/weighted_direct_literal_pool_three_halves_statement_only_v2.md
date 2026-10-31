# Occurrence-weighted direct literal pools: Exact-only v2

2026-10-18 root/boss11, scratch. A new object domain extending the prior uniform-per-variable candidate; no author proof or algorithm included. Not a repository claim/asset.

Give an explicitly listed CNF with N variables, M clauses, L literal occurrences; every clause has at least two occurrences. Repeated literal/variable occurrences count separately. To each occurrence e assign a binary rational b_e>=0, with the full eligible-occurrence budgets

    sum_(e positive occurrence of v) b_e <=1,
    sum_(e negative occurrence of v) b_e <=1

for every variable v. The coefficients may differ for each occurrence, including within the same polarity/variable. Zero is allowed for the scheduling upper bound; an equivalence to strict SAT would additionally require all b_e>0.

The ordinary UM matrix contains two distinct pools A_v+,A_v- per variable and one f_v with time1 to either; one distinct private root R_e and one query j_e for every occurrence, with times1 at R_e and b_e at its literal pool; and one selector s_c per clause with time1 to each of that clause's occurrence roots. All unspecified times are infinity. No other jobs, machines, guards, side constraints or supplied schedule witnesses. Retain all zero queries and all unselected private roots/jobs. If N=L=0, add one idle machine to meet m>=1. Counts otherwise: machines2N+L, jobsN+L+M, finite entries2N+3L.

Exact claim: There is a deterministic total-bit-polynomial algorithm that returns a complete legal actual assignment of this same matrix with makespan at most3/2. Each clause selector chooses one original occurrence root, exactly that original query goes to its own literal pool, every other query stays at its own root, and every f_v executes on one of its two original pools. Simultaneously every root has load at most1; the pool containing f_v has query-only load at most1/2 (hence total at most3/2); the other pool has load at most1. Empty formula/unused variables/zero b_e/binary tiny coefficients/duplicate occurrences are included. Runtime is polynomial in the explicit original matrix/CNF and rational encodings, without expanding by any denominator or 1/b_e.

Scope: This rules out this exact independently budgeted occurrence-weighted private-root/direct-pool compiler as a near2 hardness source. It does not cover extra cross-clause endpoints/guards, changing full eligible budgets, or imply a general UM approximation. No sharpness/newness claim is made. All actual job identities and global loads must be accounted for in review.
