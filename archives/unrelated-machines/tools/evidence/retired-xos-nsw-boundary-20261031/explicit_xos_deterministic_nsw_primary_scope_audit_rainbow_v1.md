# Primary-source scope audit: deterministic constant NSW for explicit weighted XOS

Author: rainbow_gap_source, 2026-10-18. Scratch only. This is a nonblind source audit, not an independent proof review. Root supplied the proposed geometric-label / conditional-expectation / integer-DP strategy before this task. I have not read root's or another author's new derandomization proof file.

## Finding

I did not locate a primary theorem explicitly asserting a deterministic constant-factor NSW approximation for arbitrary explicitly listed, weighted XOS valuations. This is a bounded search finding, not a proof that no such theorem exists and not a novelty certification.

DLRV gives the relevant constant-factor NSW framework, including the independent geometric item labels and fixed-candidate analysis. Its checked versions still use random filtering. Turning its conclusion into a deterministic one by computing conditional expected logarithmic potentials is an additional algorithmic step that requires its own correctness and bit-complexity proof. Once that step is proved in the stated explicit representation, the appropriately modest description is a representation-specific derandomization corollary of DLRV, using standard conditional expectations and dynamic programming. It should not be called a new NSW framework, a general demand-oracle derandomization, or the first deterministic XOS result.

## 1. DLRV: the closest applicable primary framework

Shahar Dobzinski, Wenzheng Li, Aviad Rubinstein, Jan Vondrák, *A Constant-Factor Approximation for Nash Social Welfare with Subadditive Valuations*, STOC 2024, DOI [10.1145/3618260.3649740](https://doi.org/10.1145/3618260.3649740).

The preprint is [arXiv:2309.04656v1](https://arxiv.org/abs/2309.04656v1). I actually read its Section 1.3, Theorem 1 interface, Section 2.4 Algorithm 1 and Lemmas 4–6, Section 2.5, and Section 3 Theorem 10/11 and proof. Algorithm 1 on PDF/printed page 9 samples each item's geometric round label independently. Candidate sets and the removal of satisfied agents depend on the welfare procedure and valuation thresholds, not on those sampled labels. Lemma 6 on page 10 explicitly treats the candidate set as fixed and attributes the remaining randomness to the round-item set. Section 2.5 subsequently uses a constant-probability event.

These are genuine primary precedents for the proposed arrangement of randomness. They do not themselves state the required computable conditional-expectation oracle for arbitrary XOS log potentials.

The STOC proceedings PDF, obtained from [the NSF public-access copy](https://par.nsf.gov/servlets/purl/10525757), was also checked at its introduction, Algorithm 1, and main theorem regions (PDF pages 2–3, 6–8). It continues to describe independent randomized contention resolution and random filtering. A text-wide search for the stems “determin” and “derandom” returned zero matches in both checked DLRV text versions. This lexical check supplements the actual reading; it does not establish a universal negative about the literature.

Local files:

| Version | Local filename | SHA256 |
|---|---|---|
| arXiv v1 PDF | dlrv_2023_subadditive_nash_social_welfare_v1.pdf | 3ae5ff599f9c5cc367adc1923fdd571d342d967dc2d64e6ad5ff948f3905fc6d |
| arXiv v1 text | dlrv_2023_subadditive_nash_social_welfare_v1.txt | 10fb320d3a7aaccb3baf579b657b3bcfecd931c45133df3f14337ce1e94829fb |
| STOC proceedings PDF | dlrv_2024_stoc_subadditive_nsw_nsf.pdf | fac5407c5f2257dccee502609f64eec239fb9aef89bf6a994201d5fd636569c8 |
| STOC proceedings text | dlrv_2024_stoc_subadditive_nsw_nsf.txt | 81f712ba674c9df4e103ea9a3961d568dc881a315eed343f9458aed09a82a574 |

The numerical constant audit from the separate NSW Exact v2 remains separate from this source search. Finding a deterministic implementation does not by itself validate the paper's reported numerical factor.

## 2. A direct methodological precedent: additive NSW log potentials and coarsened DP

Yuda Feng and Shi Li, *A Note on Approximating Weighted Nash Social Welfare with Additive Valuations*, ICALP 2024, [primary PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol297-icalp2024/LIPIcs.ICALP.2024.63/LIPIcs.ICALP.2024.63.pdf), DOI 10.4230/LIPIcs.ICALP.2024.63.

I actually read Theorem 1, the configuration LP, Lemma 4, the end of Section 2.3 on printed page 63:6, and Appendix A on printed page 63:9. The end of Section 2.3 explicitly derandomizes its additive rounding by computing a logarithmic NSW potential and choosing rotation operations that do not decrease it. Appendix A explicitly coarsens item values around a guessed largest item and uses dynamic programming for a logarithmic configuration separation problem.

These are clear precedents for the general techniques “computable log potential” and “coarsened DP.” The paper's algorithm and potential concern additive valuations and a matching/slot rounding. They are not a theorem about the DLRV geometric filter for arbitrary XOS. The paper cannot be imported as a deterministic XOS backend without a further reduction or proof.

Local PDF: feng_li_2024_weighted_additive_nsw_icalp.pdf, SHA256 126ba75ce63d2073c58f626e42e52f37e66c52bd0fb89c34d50d2228f0d35cfe.

Local text: feng_li_2024_weighted_additive_nsw_icalp.txt, SHA256 f916a80203b922b3cd121afd5d503879c20bb3c2af15c1404af978484e66b8b6.

## 3. Nearby results whose domains must not be widened

- Garg, Husić, Li, Végh, Vondrák, *Approximating Nash Social Welfare by Matching and Local Search*, STOC 2023, [arXiv:2211.03883](https://arxiv.org/abs/2211.03883), explicitly gives a deterministic constant approximation for submodular valuations. I checked its primary abstract/theorem summary, not the entire proof. General weighted XOS is a larger domain, so this statement does not settle the present question.
- Barman and Verma, *Approximating Nash Social Welfare Under Binary XOS and Binary Subadditive Valuations*, WINE 2021, [arXiv:2106.02656v2](https://arxiv.org/abs/2106.02656v2), gives a constant NSW guarantee for binary XOS. I actually read its binary-marginal definition and equivalent representation theorem: the additive clauses have coefficients in \(\{0,1\}\), equivalently every marginal is \(0\) or \(1\). Polynomially bounded integer weights after scaling a general grid are not binary marginals. Splitting one physical item into value units is not a value-preserving reduction for indivisible allocation.
- Dobzinski, Nisan, Schapira, *Approximation Algorithms for Combinatorial Auctions with Complement-Free Bidders*, Mathematics of Operations Research 2010, DOI [10.1287/moor.1090.0436](https://doi.org/10.1287/moor.1090.0436), has a deterministic factor-2 algorithm for XOS **utilitarian** welfare. The primary abstract was checked. This is a relevant welfare precedent, not a deterministic NSW theorem, and I have not certified its exact support-respecting LP-rounding interface from the abstract.

## 4. Search scope and safe conclusion

The search included combinations of “Nash social welfare,” “XOS,” “fractionally subadditive,” “explicit representation,” “XOS representation,” “deterministic,” “derandomized,” and “derandomization,” plus follow-up primary papers and the DLRV published copy. Search hits that merely repeated the same abstracts were not treated as additional mathematical evidence. Nonprimary summaries were not used to establish an algorithmic theorem.

The sources establish that constant NSW under demand-accessible XOS is already known, that DLRV exposes the fixed-candidate independent-filtering structure, and that NSW log-potential derandomization and coarsened DP already occur in additive work. They do not, among the statements actually checked, directly assert the proposed deterministic weighted-XOS implementation.

Accordingly, the source-safe statement is: “We use the DLRV framework and standard conditional-expectation/DP techniques; the following separately verified finite-representation implementation derandomizes the needed filter.” A claim of global originality, a deterministic theorem for arbitrary demand-only subadditive or XOS oracles, or a stronger approximation scope requires additional evidence beyond this audit.
