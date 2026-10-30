# 文献两攻击公式锐渐近：上下两侧独立攻击

Reviewer: R3 parent agent; 2026-10-14. The source researcher reconstructed
the full proof independently. This reviewer rebuilt the lower-parameter
limits and the upper elimination before reading the completed manuscript,
then checked every displayed implication against that manuscript.

## Exact targets and conclusions

The reviewed object is only the source two-test supremum F_d, in its original
positive-weight parameter domain. No upper estimate for a_*(d) is claimed.
The conclusions are the complete sharp asymptotic and the legal explicit
nonexistence family, with the source's full-state coverage reconstructed below.

Lower attack: ceil(k) has the correct direction because nw≤exp(−J)<1, so
(nw)^k≤d^(−1/2); no asymptotic expansion of a rounded exponential is used.
Floor(n) has relative error at most 1/N→0, and its effect on k·nw tends to
zero. The denominator (1+nw)^k tends to e while nβ tends to zero. The light
denominator's (nw)^k/q is at most √H/(cD), which tends to zero. β lies in
(0,1) for all sufficiently large d, and the source allows the resulting real
coefficients and weights. The claim uses strict α<min(A,B), retaining the
equilibrium boundary correctly.

Upper attack: from the two inequalities one obtains
(ft−1)(f−θ)≤np and hence (f−1)²≤np/t. The inequality r≤p/f does not drop a
term of the wrong sign: (f−θ)q≥0 because f>1 and θ≤1. These give
n≥(f−1)², w<2/n, and w≥ln(f)/d. Consequently every sequence with f≥cS
has ln(f)=D/2+O(H). If nw stays above a fixed positive ε, the factor p/t is
at most f^(−c_ε), contradicting that same lower scale. This localizes nw→0
without assuming the desired upper order beforehand.

The remaining estimates are sequential, rather than an unsupported uniform
Taylor bound over every legal parameter: along each candidate maximizing
sequence, w/(nw)=1/n→0 gives a/b∼nw/ln(1/(nw)). The one-dimensional supremum
bound is exact for λ≥exp(e), by its split at x=1/λ. Applied to every possible
violating sequence this proves the supremum bound; nonattainment of a
parameter optimum is harmless. F_d is finite from A≤2^d, so choosing a
near-supremum point requires no compactness assertion.

## Reconstructing every-state coverage

With the heavy player fixed in A, let m light players use a_0. For m=0 its
deviation ratio is exactly A. For m≥1 a same-column light player has ratio

    [(1+mw)^k+βw^d]/[((n−m+1)w)^k+β(1+w)^d] ≥ B.

Both inequalities use monotonicity with m≥1 and n−m+1≤n; all denominators
are positive for legal w. Complementing the columns covers the heavy
player's other action. Thus no pure state is left outside the certificate.
This is an independent reconstruction of the import obligation, rather
than reliance on an improvement cycle or a numerical search.

## Review status

No fatal objection found in the claimed domain. The explicit legality
threshold is a convenient asymptotic threshold, not a practical near-optimal
parameter choice for modest d. Decimal checks are reproducible diagnostics,
not interval-certified mathematics; none is used to infer the universal
inequalities. The sharpened growth refines the known source construction's
exhibited asymptotic. It does not exceed the already-defined exact source
supremum. External peer review and global novelty remain unverified.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
