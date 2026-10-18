# 稠密小整数正规形的独立正文后审

Reviewer: `/root/negation_scope` (internal mathematical review, not external peer review).

## Review scope and frozen identity

The actual mathematical read-after covered **section 6 only**, lines 69–130 of:

`/workspace/scratch/88ab8e647e3d/co-work-anl-boss3/research/current/unrelated_machines/model_and_classical_barriers.md`

Full-file SHA-256 at the completed read-after and again after the audit run:

`dcb5d4cf41c3fe47e4d05e2e62b1f1449ecedc938b41ad6a9f9bb3b978007061`

The hash covers the entire file; the mathematical review does not claim to cover sections 1–5. The repository AGENTS.md and section headings were also inspected for routing and scope. No earlier classical claim or global originality claim is promoted by this review.

## Verdict on the final proof text

**Fatal issues: none. Required nonfatal corrections: none.** The final section gives a correct algorithm-existence equivalence and its explicit fixed-k construction. It does not produce the hypothetical dense-domain approximation algorithm, a new general approximation algorithm, or a near-two hardness theorem.

| Obligation | Actual final text | Finding |
| --- | --- | --- |
| Replace an arbitrary positive real improvement by a fixed reciprocal integer gap | Line 71 | Correct; the finite program is unchanged and need not compute the real constant. |
| Define the dense promise with actual job count | Lines 73, 82–89 | Correct; all entries are finite positive integers at most n², with exactly the same n jobs and m machines. |
| Empty inputs and zero optimum | Line 75 | Correct; for nonnegative times OPT=0 exactly when every job has a zero edge. |
| Positive lower bound and bounded threshold range | Lines 78–80 | Correct: 0<L≤OPT≤U≤nL on the remaining branch. |
| Exact small-job branch | Lines 82, 126 | Correct; the exponent is fixed because k is fixed. The final wording explicitly distinguishes the fixed exponent from the input-dependent machine count. |
| Generate an implementable grid covering the optimum | Lines 82, 94, 126 | Correct; generate every rational threshold through the first one at least U. The first threshold at least OPT exists and is at most g·OPT. |
| Rounding, including zero edges | Lines 87, 94–98 | Correct; max(1,ceil(Sp/T))≤Sp/T+1 is non-strict at zero, which is sufficient for the stated bound. |
| Dense-domain promise for every oracle call | Lines 94–98 | Correct; n≥8k ensures 4kn≤n², and every other edge is replaced by n². |
| Strict exclusion of finite sentinel edges | Lines 101–107 | Correct: α(4k+1)n=(8k−2−1/k)n<n². A single sentinel would already violate that bound. |
| Retain the sharper rounded-optimum bound during lifting | Lines 109–120 | Correct; the first term of (6.2), rather than only its coarse bound, gives α[OPT+T/(4k)]. |
| Exact ratio calculation | Lines 116–120 | Correct: α(1+1/(4k)+1/(16k²))=2−1/(2k)−1/(8k²)−1/(16k³). |
| Return a legal schedule rather than a threshold estimate | Lines 92, 107, 124 | Correct; discard any output selecting a pruned edge, and the good threshold guarantees at least one retained assignment. Taking the smallest original makespan preserves the bound. |
| Input-bit polynomial running time | Line 126 | Correct; H≤4k ceil(log₂ n), rational numerator/denominator lengths grow only polynomially, each Q has O(mn log(n+1)) bits, and the enumeration exponent depends only on fixed k. |
| Preserve the distinction between equivalence, finite evidence, and hardness | Lines 128–130 | Correct; the section explicitly separates these statuses. |

The bit-complexity argument covers arbitrarily small positive rational times, arbitrarily large rational values, large denominators, zero edges, and unavailable edges. It does not use numerical-value loops or a decision oracle for testing OPT≤T. Existence of the good threshold is used only in the proof; the actual construction runs every generated candidate.

## Prior independent Exact-first reconstruction

Before reading the author's section 6, this reviewer received only the exact dense-normal-form statement and its proposed constants, then independently reconstructed the full argument. That reconstruction checked the zero branch without removing jobs, the fixed-exponent small-job branch, the actual-n² promise, strict sentinel exclusion, the stronger rounded-optimum estimate, the exact lifting identity, and rational bit complexity.

An independently implemented exact-fraction/subset-sum check was first executed before reading the final proof or canonical audit source. It used twelve fixed-seed two-machine instances at n=16,k=2 and exhausted every assignment on each instance. It checked 27,595 assignments meeting the assumed approximation bound, with zero edges, unavailable edges, denominators 2^160, and 121-bit numerators. Exact identities were also checked at k=2,3,10,10^6. This was finite evidence, not the universal proof.

That independent method is archived afterward at:

`/workspace/scratch/88ab8e647e3d/dense_integer_independent_subset_audit.py`

It imports neither the canonical audit nor repository mathematics. This scratch source is optional independent evidence; no additional canonical asset is requested by this review.

## Canonical audit code read-after and execution

This reviewer actually read the complete audit source, lines 1–217:

`/workspace/scratch/88ab8e647e3d/co-work-anl-boss3/tests/audits/unrelated_machines/dense_small_integer_equivalence.py`

Full source SHA-256:

`8bd2ddee874cbeb93284f7fd2e6b74aa5fb795834c177de5df4c0065590ae108`

**Fatal code issues: none. Required nonfatal code corrections: none.** Fraction arithmetic, ceiling computation, original and rounded assignment indexing, unavailable-edge flags, exact optima, every qualifying adversarial output, per-machine pullback, and JSON counts are consistent. The script does not implement or assume an available implementation of the unknown B; it exhausts every output assignment meeting B's hypothetical bound on its finite fixtures.

The unmodified canonical script was executed successfully, with standard Python assertions enabled. Scratch-only output:

`/workspace/scratch/88ab8e647e3d/dense_integer_independent_audit_run.json`

Output SHA-256:

`2ca13b6d0b7b9b77ea09af285aa3d554c0f992cb2c28a57eef1c3e9be5a5bdd4`

| Actual run coverage | Count |
| --- | ---: |
| Exact constant identities, k=2 through 10000 | 9,999 |
| Boundary examples | 4 |
| Dense exhaustive fixtures, each m=2,n=16,k=2 | 4 |
| Assignments exhausted across those fixtures | 262,144 |
| Qualifying approximate outputs | 9,474 |
| Qualifying per-machine pullback checks | 18,948 |

All assertions passed. The four common-scale bit lengths were 8, 9, 65, and 333. The audit's stated finite scope and limitations match its source; it does not establish the theorem for arbitrary input sizes and does not change the approximation or hardness status.

## Review status

The universal construction is present in the reviewed section and passed this independent internal read-after. Independent reconstruction, finite exact checks, actual code review, and actual code execution are recorded separately above. No external peer review, source-priority judgment, or broad literature-originality certification is claimed.


## 主研究者复现与保存范围

主研究者实际完整读取新增§6与全部规范审计代码，独立检查强式(6.2)、零边取整误差和严格替代边排除；重跑命令为：

```sh
python3 tests/audits/unrelated_machines/dense_small_integer_equivalence.py
```

正式冻结输出位于 `evidence/runs/unrelated_machines/dense_small_integer_equivalence.json`，其SHA256与上述独立运行输出一致。复跑可重定向至clone外scratch，不能覆盖冻结记录。未将其他子线的局部复制、张量或占位尝试作为已审canonical资产保存。
