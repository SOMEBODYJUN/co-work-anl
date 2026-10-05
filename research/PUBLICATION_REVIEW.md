# Publication assessment and independent internal audit — 2026-10-01

**Historical assessment snapshot.** The judgments below refer to the 2026-10-01 state. The later [five-site decision-hardness audit](FIVE_SITE_AUDIT_2026-10-02.md) and [arbitrary-facility audit](K_FACILITY_AUDIT_2026-10-02.md) change the global-complexity and multi-facility landscape. Use [the live research state](../RESEARCH_STATE.md) and [claim ledger](current/claims.md) for current scope. The historical judgments are retained rather than rewritten as if they were made after these results.

This is a research and editorial assessment of `main@9a15cf8` and the local follow-up scope corrections. It is **not** a mathematical proof, a novelty certificate, an external referee report, or a prediction of acceptance. The exact claims and proofs remain in `current/claims.md` and the linked mathematical files. Five independent Astra review lines examined the sparse universal proof, long-cycle families, shared/heterogeneous/exact branches, paper architecture, and primary literature; the maintainer separately checked the dependencies and ran the commands below. No surviving fatal objection was identified in the examined proof chains. Internal review cannot rule out later counterexamples or prior work.

## What the new theorem changes

The new [`SPARSE-RHO-ALL`](current/heterogeneous/sparse_unbounded_rho.md) removes the restriction that one catalog have at most two locations. For **two** labeled facilities with arbitrary finite nonempty catalogs, positive atomic customer weights, mandatory service, realized linear load cost, and at most **one common customer per legal cross-catalog pair**, any fixed reach-and-priority pure exact-NE continuation rule admits a location profile with all original-catalog unilateral improvements bounded by

\[
\rho=2\cos(\pi/7).
\]

The inherited strict-unique-NE `2×2` family gives a positive-integer counterexample to every smaller universal factor, even when all independent mixed customer NE are allowed. This makes the unrestricted-length single-overlap threshold sharp. The proof uses full-catalog best responses, a strictly descending high-reach region, and the first high-to-low edge: two alleged distinct common customers cannot both fit in the maximum-reach action, forcing the same customer identity and then `r³−r²−2r+1<0`, impossible at `r=ρ`. It **does not** show that every customer-NE selection works, that the general heterogeneous class has factor below 2, or that any analogous result holds for three facilities.

The formerly known restricted [`HC-RHO`](current/heterogeneous/restricted_rho.md) remains a correct narrower theorem and supplies the matching lower family; its long upper-bound classification is no longer the best exposition of the universal-length result. The review also yielded the **new quantified version** [`SPARSE-BAD-LONG-ALL`](current/heterogeneous/sparse_bad_long_cycles.md): the genuinely `r`-bad unique full-response cycle can have arbitrarily many actions for *every* `1≤r<ρ`. Its open-parameter proof for `1<r<ρ` and separate `r=1` transfer are recorded there; the original `SPARSE-BAD-LONG` claim retains `3/2<r<ρ`. This is a structural limitation on **exact full-response-closed cores**. It does not preclude a smaller sufficient certificate that preserves only selected bad deviations, and it is best presented as a supporting theorem, not a separate flagship paper.

## Scope and contribution map for publication

| Result | Exact class and status | Contribution that can be claimed after priority check | Must not be claimed |
| --- | --- | --- | --- |
| `SC-PHI-E/A` | Two facilities, same finite catalog, positive weights, complete independently mixed exact customer-NE selection; explicit rational input for polynomial bit-time construction. Full current proof and multiple internal reviews. | New optimal **upper construction**, finite menus, exchange/chord mechanism and polynomial certificate, closing the shared-catalog two-facility gap. | A theorem for arbitrary facility count or arbitrary heterogeneous catalogs. |
| `SC-PHI-SHARP` | Same shared class; existing IJCAI 2024 lower family recomputed with a documented source-figure correction and rational perturbation. | Sharpness **by combining** new upper with properly attributed earlier lower. | Discovery of the golden-ratio lower bound itself. |
| `HC-2-UP/LOW` | Two facilities, arbitrary finite catalogs, complete pure exact-NE continuation; new four-seed full-cycle argument and distinct near-2 lower family. Current ledger conservatively says internal candidate. | Full construction and a matching class lower bound, subject to final author-level proof and priority audit. | First ever numerical statement of a factor-2 bound; application of its lower bound to the shared class. |
| `SPARSE-RHO-ALL` | Two facilities, arbitrary catalog lengths, cross-pair common-customer count at most one; complete fixed pure rule. New full proof multiply internally attacked. | Removal of the length restriction, sharp universal constant, simple polynomial construction, new first-boundary mechanism. | General overlap count ≥2, arbitrary customer NE selection, or more facilities. |
| `SPARSE-BAD-LONG-ALL` | Same sparse incidence; for every `1≤r<ρ`, arbitrary length and unique exact continuation. New quantified version, algebra internally reviewed. | Obstruction to any constant-size **exact response-closed core** below the sharp threshold. | A kernelization or complexity lower bound, or a counterexample at `ρ`. |
| `EXACT-KAPPA`, DP, MITM, FPT-D, `LOCAL-HARD` | Two-facility instance optimum or fixed-layout local optimization, with each separate parameter/input restriction. Different implementation and review states. | Computational supporting section; explain why a universal certificate can be efficiently found despite difficult local exact optimization. | Global NP-hardness of deciding `α*(I)≤α`; a short attainment certificate proving instance optimality. |

Shared catalog and single-overlap are **incomparable restrictions**. The three sharp values `φ` (shared), `ρ` (heterogeneous single-overlap), and `2` (all heterogeneous) form a condition table, not a one-parameter hierarchy. `φ` and `ρ` lower constructions belong to their own exact classes. The older unrestricted-client-equal-weight exact-SPE result is a different axis from the weighted two-facility claims.

## Independent scrutiny and reproducible checks

1. The `ρ` reviewer independently reconstructed the full statement, then checked the fixed pure customer NE, maximum over the **whole** catalogs, strict high-region descent under ties/zero loads, `β≤b` rather than `β=b`, forced common-customer identity, equality at `r=ρ`, rational lower perturbation, and exact cubic comparison. No fatal gap was found.
2. The cycle reviewer checked every incidence, unique customer NE, five exhaustive layout classes, strict full-catalog best responses, all-`n` rationalization, and `n=1`; the new all-sub-`ρ` quantifier was proved by explicit positive margins. Exact finite runs are only arithmetic attacks.
3. A separate reviewer reconstructed shared `G1–G3` and chord `L1–L2`, the heterogeneous arbitrary even-cycle cases and sharp-2 payoff table, the local support spectrum and exact instance criterion. No fatal gap was found. `HC-2` and several exact-computation ledger entries **remain candidate** until their final paper-specific sign-off; this review did not silently promote them.
4. The paper reviewer found that the heterogeneous historical LaTeX `history/source/manuscripts/heterogeneous/main.tex` still states the both-long sparse case as open in its abstract/conclusion. It is a source manuscript, not a submission version containing `SPARSE-RHO-ALL`.
5. The literature reviewer verified the precise IJCAI 2024 and Vos 2023 boundaries. A later Simon Krogmann dissertation, *Two-Sided Facility Location Games*, DOI [`10.25932/publishup-69272`](https://doi.org/10.25932/publishup-69272), was identified but its full text could not be retrieved during this review. Its weighted-atomic chapters are a **specific unresolved priority check**; directed search not finding a matching `ρ` result does not prove originality.

Run from the repository root; these checks were completed on 2026-10-01:

```sh
python3 -m tests.test_shared_phi
python3 -m tests.test_four_seed
python3 -m tests.test_heterogeneous
python3 -m tests.test_lazy_ring
python3 -m unittest discover tests -v
python3 tests/audits/sparse_bad_long_cycles.py | sha256sum
sha256sum evidence/runs/2026-10-01/sparse_bad_long_cycles.json
python3 research/build_map.py --check
python3 research/build_crosswalk.py --check
python3 research/check_assets.py
```

Results: 753 shared full certificates; 2,406 four-seed certificate checks; heterogeneous tests with 500 random and 1,500 general-catalog certificates plus support comparisons; 30 lazy/full comparisons; 11 independent shared-verifier tests; the regenerated `7/4` cycle report matched the frozen SHA256 `4b34dd94c35bbbc714f73dbfa0f6c3602da1e4a81f3c99cb664048a96fa5bcac`. After the new version was entered, the three research metadata checks passed with 73 nodes, 55 hyperedges, and 161 indexed paths. These are finite implementation and structural checks, **not** universal mathematical proofs.

## Recommended paper architecture

**Paper A — shared-catalog sharp golden ratio.** Main theorem `SC-PHI-E/A` with the known lower bound attributed to Krogmann et al.; explain the fixed menu, global response cycle, heavy pairs, star/anchors, chord quota and polynomial construction. Put the complete local exchange cases, lower-family source correction, and implementation certificates in appendices. Local hardness is a supporting contrast with exact oracle computation. This is the strongest self-contained paper line.

**Paper B — heterogeneous catalogs and sharp overlap boundary.** Main theorem for general sharp 2 plus the new arbitrary-length single-overlap sharp `ρ`; formulate a precise result table before proof. Present the short fixed-pure `ρ` proof and its lower family, the four-seed/cycle `2` proof and near-2 family with **two** common customers at legal pairs, and a short section on genuinely bad long response cycles. The old restricted-`ρ` upper classification is historical support/appendix, not a second competing main proof. A bounded-overlap exact-instance solver can support, but should not crowd out, the sharp classification.

An integrated paper is also possible if a unified conceptual narrative emerges and the combined proof remains readable. Simply concatenating the two long historical LaTeX sources is not a stronger article. The current DP/MITM/FPT/local-complexity bundle is not yet a strong independent third paper: a global `α*` decision classification, a matching parameter lower bound, or a new generally reusable spectrum theorem would change that assessment.

## Conditional journal judgment and actual delivery gaps

| Venue | Judgment **if** priority and proof scrutiny remain favorable and a new submission manuscript is completed |
| --- | --- |
| [SIAM Journal on Discrete Mathematics](https://www.siam.org/publications/siam-journals/siam-journal-on-discrete-mathematics/) | Serious main target for either paper: sharp discrete thresholds, combinatorial response structure, constructive algorithms. |
| [Algorithmica](https://link.springer.com/journal/453/aims-and-scope) | Serious main target, particularly if algorithm complexity and actual construction are foregrounded. |
| [Mathematics of Operations Research](https://pubsonline.informs.org/page/moor/editorial-statement) | Reasonable stretch target for a polished equilibrium/OR framing and clear priority advantage. |
| [SIAM Journal on Computing](https://www.siam.org/publications/siam-journals/siam-journal-on-computing/) | High-risk stretch; its scope includes algorithmic game theory but calls for significant technical contribution. Current two-facility classification alone does not justify treating acceptance as likely. |
| [SIAM Journal on Optimization](https://www.siam.org/publications/siam-journals/siam-journal-on-optimization/) | Lower topical fit for the present combinatorial equilibrium existence argument. |

This is **fit and contribution assessment**, not a probability or ranking of journals. Immediate submission is premature because neither current English manuscript integrates the new all-length `ρ` theorem and precise scope table, `HC-2` still needs a final paper-level proof sign-off, and the 2025 dissertation needs full-text priority inspection. External peer review has not occurred, but prior external certification is not a prerequisite to submitting a paper. Dedicated `ρ` CLI and independent verifier would improve software delivery; they are not mathematical submission gates. Additional undirected random trials have low information value compared with the above tasks.

### Primary literature boundaries

- [Krogmann, Lenzner, Skopalik, Uetz, Vos, IJCAI 2024](https://www.ijcai.org/proceedings/2024/0315.pdf): its Theorem 5 is the weighted golden-ratio lower bound; Theorem 6 is NP-completeness only for a fixed `α<φ`. Observation 4 states a general `k` bound, whereas its displayed co-location argument directly applies to a common feasible location. Do not call the lower bound ours or transfer the hardness to `α=φ`.
- [Vos MSc thesis 2023, Chapter 8, Theorem 17](https://essay.utwente.nl/96484/1/Vos_MA_EEMCS.pdf): its `k` co-location bound is explicitly *unrestricted*; it says that proof does not work for different location sets. Its equivalence chapter uses zero-weight augmentation; transferring a claim to our strictly positive weighted model needs checking.
- [Krogmann PhD dissertation, official DOI](https://doi.org/10.25932/publishup-69272): identified but full text uninspected; inspect before a definitive novelty statement.

### Next actions in order

1. Obtain and read the 2025 dissertation's relevant chapters and check citations forward from IJCAI 2024; write a theorem-by-theorem priority table. If an overlapping result exists, revise the contribution claim before manuscript drafting.
2. Independently sign off `HC-2` for a publication proof; keep the exact `HC-2-UP`, `HC-2-LOW`, `SPARSE-RHO-ALL` scopes separate.
3. Write **new** English submission manuscripts from current proofs, with accurate authorship, theorem dependency, primary-source attribution and new `ρ` theorem in the abstract and introduction. Do not overwrite historical source drafts.
4. Have an external subject-matter reader reconstruct each main theorem without relying on this internal review, then revise exposition and choose the target journal on the finished manuscript.
