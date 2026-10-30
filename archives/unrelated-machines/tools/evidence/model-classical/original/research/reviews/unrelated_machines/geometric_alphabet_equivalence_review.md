# 几何字母表正规形的实际正文与精确程序复核

Reviewer: integer_gap. This is an actual-text/code read after an independent statement-first reconstruction; its key obligations are recorded below. No repository edits were made.

## Read versions

- Initial actual §7, full model_and_classical_barriers.md SHA256: b78e0606742f20d5c29c8204b49030f557532c78ef814c709b1a3760fc25d97c.
- Final reread of actual §7 after explicitly restricting the minimization exponents to nonnegative integers, full-file SHA256: 251dc664bc623901df0841cf791345745d6c4ccfc12ce0e3eec208c27245ec4b.
- Full audit_geometric_alphabet_normalform.py read; SHA256 remained 5ddaf740aae1e40f03f74840b898db94666851b225548d66a509bfc3188051d1 before and after the independent run.

## Mathematical result

PASS; no standing mathematical objection. The actual text agrees with the independent reconstruction. I checked all displayed formulas (7.1)--(7.6), integer rounding, strict inequalities and branches:

1. h=ceil(log2(n+1)) is the integer bit length; b^h>=2 gives the stated R and threshold-grid bounds. The induction n>=2^(h-1)>2(h+2) is valid from h=5 onward. Minimality gives b^R<(h+1)n, and the displayed ceiling chain is strictly below n^2. The alphabet has O(log^2 n) elements and O(log n)-bit entries.
2. The empty and exact-zero branches precede use of positive L. The small-h exhaustive branch covers n<16 and has a fixed finite exponent for each fixed k. All B calls therefore have n>=16 and use the same original m,n.
3. The least qualifying **power**, followed by ceiling, satisfies z<=q<=bz+1 including z=0, z=1 and p=T. Sentinel substitution and rejection are based on original unavailable/p>T edges. Rejection has no false lower-bound semantics.
4. At the first T>=OPT, the stronger first bound in (7.5) yields the claimed additive n and the strict sentinel exclusion alpha(h+2)n<n^2. At least one output survives. Pullback uses the same stronger bound and T<=b OPT, giving alpha b^2. The expansion in (7.6) is exact; its remainder is strictly negative.
5. Rational powers have O(log^2 n loglog n) bits; all candidate construction, comparisons, ceilings and original load sums are bit-polynomial. No denominator-value loop is hidden. The existence equivalence properly chooses a fixed integer k below any positive real improvement and does not require encoding that real number.
6. The fixed-palette comparison correctly distinguishes one fixed palette/uniform gcd margin from palettes depending on n or on the fixed hardness accuracy. No hardness claim is inferred.

The only precision suggestion on the initial version was to make the exponents' integer domain explicit; the final reread contains that clarification. No inequality or algorithmic branch required correction.

## Audit-code result

PASS within the stated finite scope. I read the full script, including the new actual-large-branch fixture. The binary search uses unrounded rational powers. The per-matrix enumerator checks every complete transformed assignment, rejecting sentinels by the correct original-edge predicate. The k identity is exact Fraction arithmetic.

The n=32768 fixture has six nonzero original jobs and 32762 labeled zero jobs. The zero jobs have original times (0,0) and transformed times (1,1), so every complete schedule has exactly the loads of one of 64 flexible patterns and one integer zero-job count t in 0..32762, and every such pair is attainable. Enumerating these load types is therefore exhaustive for makespan, edge rejection and the pullback inequalities. The closed-form transformed optimum is independently checked against all enumerated load types. Endpoint checks of the machinewise pullback extend to every intermediate t by monotonicity. This does not assume or implement the unknown algorithm B.

Independent invocation:

    python /workspace/scratch/147f2d9f533d/audit_geometric_alphabet_normalform.py --max-n 128 --large-bits 64

Output: geometric_alphabet_actual_review_run.json, SHA256 1ff79c431975bdb6b403eef3e4e7d03139ea070492ca058ee42d6c84632d0f46.

Observed scope: 113 ordinary grid sizes with 9900 probes; the script's four large grid-only sizes; 7871 small-h matrices, 29648 threshold instances, 246196 transformed assignments and 25533 qualifying-output checks; k=2..1000 exact ratio identities; and 2096832 actual-large-branch load types, of which 262104 qualify under alpha=3/2. All passed. I did not run the author's default n=16..4096 grid interval and do not claim that coverage.

These are finite checks, not a proof substitute. The normal-form equivalence is a standard scaling/rounding corollary; no general sub-2 algorithm, integer hardness gap, decoder, novelty claim or external review is established.

## 主研究者最终复现与归档

主研究者完整读取最终§7与全部405行审计，在规范路径以`--max-n 4096 --large-bits 128 --seed 20261019`重跑。JSON数学结果与作者冻结输出逐字段相等；版本、命令、代码及证明hash附于evidence/runs/unrelated_machines/geometric_alphabet_equivalence.json。规范代码tests/audits/unrelated_machines/geometric_alphabet_equivalence.py与被审scratch源码逐字相同，重跑不覆盖冻结记录。只冻结实际承重的作者精确源稿；规范程序没有另一份实现。
