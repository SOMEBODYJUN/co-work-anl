# 全种子拒绝证书：最终正文读后审查

Reviewer: amplification / boss30. Date: 2026-10-19.

## Exact object read

I first independently reconstructed the seed statement without reading its proof. I then actually read every line of the final appended section, beginning `## 全种子完备源的拒绝种子证书`, and read the complete preceding v2, v3 and v5 source contracts and the conditional fee bridge. On the author's follow-ups I read the changed probability paragraph at line 374 and the final expected-time correction at line 350; the author confirms there were no other changes. The hashes below identify that frozen final version. I did not read the linked canonical review or revalidate the external PCP papers.

- File: `/workspace/scratch/147f2d9f533d/co-work-anl/research/current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md`.
- Whole-file SHA256: `33f5fb337e3d002e91aad79c6fb99f273ed01c1978d02fd0131e995a948e2114` (33,322 bytes).
- Reviewed appended section: lines 331–378, from its unique heading through EOF.
- Section SHA256: `40d7d2f0406f50aba5358140967a32deaf3404f3d2cef65bd7e72c0b6c2cf1fa` (5,377 bytes, exact UTF-8 file suffix including its final newline).

## Verdict

**No fatal objection.** The deterministic seed-certificate conclusion and the stated conditional probability upgrade are correct. No repository file was edited.

The UNSAT verifier guesses the polynomial-length seed, rejects FAIL, and accepts exactly when the total deterministic composite rejects. Universal SAT soundness excludes every false certificate; an UNSAT rejection seed supplies a certificate. This yields NP=coNP, without finding seeds or claiming one common seed for all inputs.

With a uniform worst-case polynomial sampler and one inverse-polynomial rejection bound for every UNSAT input, independent repetition gives SAT in coRP. The inclusions RP⊆NP and coRP⊆coNP then give NP=RP=coRP=coNP. These are stronger than NP⊆BPP, and do not assert P=NP. The final text explicitly retains hard seed/time bounds, fixed parameters and universal YES soundness.

The final expected-time sentence is also correct: an expected-time construction requires a truncation and a renewed probability analysis before this hard-bound lemma applies. It does not claim that expected polynomial time can never be converted. With an available uniform expectation bound and inverse-polynomial rejection bound, a sufficiently large polynomial cutoff can often preserve an inverse-polynomial rejection probability; that conversion remains a separate argument.

## Source-contract comparison

| Source | Universal YES / FAIL behavior actually read | Unconditional good-NO probability | Assessment |
| --- | --- | --- | --- |
| v2 | Every deletion preserves the singleton labeling; the empty edge set is explicitly a YES output. | At least 0.9, with nonempty output. | Matches the appended table. D must include empty-edge YES outputs in its correctness domain. |
| v3 | Every nonFAIL output copies the perfect original labeling; capped permutation sampling and cycle rejection return an explicit FAIL. | At least 0.8 jointly with nonFAIL. | Matches the table. FAIL is answered YES without calling D. Fixed G and the Qγ domain retain the hard polynomial bounds. |
| v5 | Every nonFAIL typed output preserves the perfect labeling; alphabets are nonempty, and capped sampling returns explicit FAIL. | At least 0.8 jointly with nonFAIL. | Matches the table. Fixed-parameter tag padding is separated from the uniform transformation's Qγ domain. |

This comparison checks applicability of the appended lemma to the source contracts. It is not a new independent certification of every earlier probabilistic inequality or of the external PCP theorem.

## UM thresholds and remaining scope

For a hypothetical (2−ε) actual-schedule algorithm, the choice **1/k<ε** is necessary. Equality does not separate the promises. A fixed such integer k can be encoded without encoding ε. The strict YES test C<β_k T and its rejection complement C≥β_k T correctly retain the NO equality case. Positive rational T, legal outputs on all nonFAIL seeds, exact rational load calculation, zero OPT and empty jobs are all handled correctly. The UM approximation index k is independent of any exact-k-to-1 PCP fiber parameter.

**Probability caveat resolved in the final paragraph.** Numbered UM hypothesis 2 promises at least one seed having the compiled NO/decoder property, which suffices for NP=coNP. The final line 374 now explicitly requires inverse-polynomial probability of nonFAIL seeds satisfying the **compiled NO/all-output decoder contract**, and explicitly says that the probability of a larger source-NO event cannot replace this requirement. I actually read this changed paragraph. It correctly removes the earlier potential ambiguity without supplying an unproved compiler guarantee.

The direct verifier proof only needs the composite's universal SAT acceptance and existential UNSAT rejection. It does not additionally require D_A to classify source instances outside the compiler image. The source-only promise-decider application has the stronger global promise correctness as stated.

The earlier v2/v3 statements that a decider implies NP⊆BPP remain true weaker consequences. Their “only/random source reduction” wording distinguishes randomized reductions from deterministic hardness under P≠NP; it does not mathematically claim BPP is the strongest consequence. The final paragraph explicitly clarifies this, as does the revised v5 paragraph. Cross-references from v2/v3 would be optional editorial improvements, not corrections of false statements.

There is still no actual UM compiler, fixed-fee realization, or all-output source decoder. The section correctly leaves the general target and its negation OPEN.

## 主研究者有限接口核验与可复现代码

主研究者读取最终正文及上述两轮修正文句。第二独立实际审读提出期望时间需可截断而非绝对禁止，最终文字已修正。下列标准库代码实际运行通过；它只核对四种抽象输出、promise外判别器两种行为和有理阈值边界，不构造或执行真实source、D、UM编译器或假设中的A。四seed表共512次、其中32次全YES、350次存在NO；阈值索引j=2..1000共999次。普遍结论由正文验证器证明承担。

```python
from fractions import Fraction as F
from itertools import product

yes_cases = no_cases = total = 0
for table in product(('FAIL', 'YES', 'NO', 'GRAY'), repeat=4):
    for gray_rejects in (False, True):
        def rejects(z):
            return z == 'NO' or (z == 'GRAY' and gray_rejects)
        if all(z in ('FAIL', 'YES') for z in table):
            assert not any(map(rejects, table))
            yes_cases += 1
        if 'NO' in table:
            assert any(map(rejects, table))
            no_cases += 1
        total += 1
for j in range(2, 1001):
    alpha, beta = 2 - F(1, j), 2 - F(1, j + 1)
    assert beta - alpha == F(1, j * (j + 1)) > 0
    T, C = F(7, 11), beta * F(7, 11)
    assert C >= beta * T and not C > beta * T
assert (total, yes_cases, no_cases) == (512, 32, 350)
print(total, yes_cases, no_cases)
```

没有随机seed参数或浮点算术。任一YES输入容许一个假NO种子就会使该验证器不健全；仅保证source好事件概率不会修复这个全称缺口。该有限核验只是接口审计，不是复杂度分离的实验性证明。
