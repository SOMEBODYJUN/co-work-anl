# Venue recommendation, round 1 (2026-10-24)

This memo evaluates the three live manuscript artifacts against the venue set used in the project publication notes (TEAC, Algorithmica, SIDMA, MOR, GEB, ACM Transactions on Algorithms, Artificial Intelligence, JAIR, TCS, and DAM; SICOMP is treated as a high-risk stretch). It is an editorial recommendation, not an acceptance forecast, originality certificate, or external referee report. The recommendations use the actual theorem scopes and current proof/review records.

## Current artifacts and evidence limits

| Manuscript | Current source/PDF | Current layout and metadata | Mathematical identity actually in the manuscript | Evidence limits |
|---|---|---|---|---|
| Shared catalog | [main.tex](shared_catalog/main.tex), [main.pdf](shared_catalog/main.pdf) | amsart, 11pt; 25 pages, US letter; PDF Title and Author fields are blank; source has title but no author block | Two facilities, one common finite location catalog, positive atomic client weights: a complete selection of exact client NE supports a \(\phi=(1+\sqrt5)/2\)-approximate SPE; explicit rational coverage input gets an O(N²(n+1)^4) construction with polynomial bit length. The matching \(\phi\) lower bound is prior IJCAI 2024 work. | Build and visual checks pass. The final independent mathematical/editorial reading was not completed; no external referee or novelty certification. The theorem is for existence of one complete continuation rule, not every client-NE selection, and only for two facilities with a common catalog. |
| Common catalog, arbitrary facility count | [main.tex](multiple_facilities/main.tex), [main.pdf](multiple_facilities/main.pdf) | amsart, 11pt; 8 pages, US letter; PDF Title and Author fields are blank; source has title but no author block | For any k facilities sharing a finite catalog, positive atomic weights and exact client-NE continuations, a factor-two approximate SPE exists. On path the covered clients independently randomize uniformly; off-path continuations can be pure. This is an existence/finite-certificate result; the manuscript makes no polynomial-time search claim and does not prove sharpness. | Compilation and the repaired bounded-delta check pass. The original isolated editorial reading found necessity PASS but referential precision FAIL; three fixes were implemented and self-checked, without a new isolated review. No external referee or novelty certification. |
| Weighted congestion structural methods | [structural_methods_article.tex](../../current/weighted_congestion/structural_reconstruction/structural_methods_article.tex), [structural_methods_article.pdf](../../current/weighted_congestion/structural_reconstruction/structural_methods_article.pdf) | article, 11pt, 1-inch geometry; 26 pages, US letter; PDF title is set, Author is blank, date is Research manuscript | Weighted congestion games with nonnegative-coefficient polynomial latencies: endpoint/area, common-scale, weight-depth, and realization tools; explicit rational degree-d games with no \((d-1200\lceil\log_2 d\rceil^2)\)-approximate PNE for every d≥2²⁰. Combined with the known d upper bound, this gives the leading asymptotic threshold ratio 1. Positive results are conditional (small actual shares, compatible scales/depth, and social-selection interfaces). | Internal integration reviews and finite audits are recorded, but this is not external review. The asymptotic leading constant is settled; the finite-d threshold and best additive gap are open. There is no general polynomial-time equilibrium algorithm. |

The source hashes at this snapshot are 6aaa893e... (shared-catalog TeX), 04190dd... (factor-two TeX), and f6f65fd... (weighted-congestion TeX); exact hashes and PDF hashes remain in each WRITING_STATE.md and MANUSCRIPT_REVIEW.md.

## Recommendation

### 1. Shared catalog, golden-ratio equilibria

**Primary: Algorithmica.** The manuscript has a genuine algorithmic deliverable: explicit coverage-set/rational input, finite equilibrium menus, a full-catalog response search, a polynomial-time strong-chord construction, and a stated O(N²(n+1)^4) bound. The factor is sharp only after correctly attributing the lower-bound family to Krogmann–Lenzner–Skopalik–Uetz–Vos (IJCAI 2024). The paper should be pitched as a common-catalog algorithmic closure of a weighted two-facility existence gap, with the exact continuation quantifier and common-catalog restriction on the first page.

The main risks are scope inflation and proof-readiness: the result does not solve the heterogeneous-catalog or general-k problem, does not make a claim for every client equilibrium, and still lacks a completed independent reading. A concise priority comparison with IJCAI 2024 and Vos (2023) is essential.

**Fallback: SIAM Journal on Discrete Mathematics (SIDMA).** The fixed-menu/cycle-elimination argument, star/anchor structure, and rational exchange certificate have a strong discrete-combinatorial presentation even if an algorithm editor is not interested. SIDMA is a better fallback than MOR unless the introduction develops a clear operations-research consequence.

**Concrete pre-submission work:** complete an independent proof read; state exactly what is prior (the lower family and repair ingredients) versus new (the menu-cover theorem and polynomial strong chord); add authors/affiliations; provide keywords/MSC; convert the generic amsart source only after selecting the venue.

### 2. Common catalog, factor two for any number of facilities

**Primary: SIDMA.** The strongest current identity is a finite combinatorial existence theorem: lexicographic load selection, transfer-budget inequalities, atomic packing, and a continuation repair that works for every facility count. SIDMA explicitly covers discrete optimization, combinatorial optimization, and approximation algorithms. The current 8-page draft is too compressed for this proof burden; expand the model/quantifiers, the packing and repair lemmas, the distinction between finite construction and polynomial search, and the exact relationship to the earlier k-dependent observation.

The paper should not be sold as a new factor-two numerical bound in the broad heterogeneous model, as that would overstate the scope and ignore prior k-type guarantees. It also should not imply an efficient algorithm: the present finite-certificate statement is weaker.

**Fallback: ACM Transactions on Economics and Computation (TEAC), conditional on reframing.** The two-stage strategic-location model and exact client equilibria are squarely in algorithmic game theory and computation of equilibria. TEAC becomes realistic only if the paper foregrounds the game-theoretic consequence, explains why the common-catalog restriction is substantive, and gives a mature comparison with the prior k-dependent guarantee. In its current terse existence-only form, SIDMA is the safer first submission; Algorithmica is not a good fallback until a real polynomial-time search theorem is added.

**Concrete pre-submission work:** obtain a fresh independent editorial/math read after the three repairs; enlarge the 8-page exposition; add a precise prior-result table; make the no-polynomial-search boundary explicit in the abstract and conclusion.

### 3. Structural methods for approximate stability in weighted congestion games

**Primary: TEAC.** The core object is algorithmic game theory: weighted congestion games, approximate PNE, equilibrium nonexistence, and the cost of strategic behavior. The all-state construction is stronger than a method-only obstruction: it gives a rational near-d lower bound for every sufficiently large degree and therefore closes the leading asymptotic constant against the known d upper bound. The article also has positive equilibrium-selection and social-quality applications that can be framed for an economics/computation audience.

TEAC is not automatic. The introduction must separate the full-class near-d nonexistence theorem from conditional positive tools, state that finite thresholds remain open, and explain why the realization mechanism is a reusable game-theoretic contribution. The current article has no polynomial-time algorithm and should not be marketed as one.

**Fallback: SIDMA.** The endpoint/area inequalities, finite-state realization, and weight-depth/combinatorial constructions fit SIDMA’s broad discrete mathematics and approximation scope. This fallback avoids forcing an OR/MS application story that the current paper has not developed.

**Stretch only: MOR.** MOR’s scope includes game theory, discrete optimization, and location/service-type applications, but its current official submission rule asks for 35–45 pages, 1.5 spacing, 11-point type, 1-inch margins, and a fully anonymized manuscript. The current 26-page single-spaced-style article draft would require substantial expansion and a much clearer OR/MS motivation. MOR is therefore not the first target for this version.

**Concrete pre-submission work:** complete the remaining independent diff/editorial read; make the lower-bound theorem and the imported d upper bound visibly distinct; state the finite-d/additive-gap open problem; decide whether the social-selection material is central or supplementary; add a sharper comparison to Christodoulou–Gairing–Giannakopoulos–Poças–Waldmann and Caragiannis–Fanelli.

## Official submission/template checks (current pages)

These are current publisher instructions, not a template conversion. Each manuscript is still a generic research draft.

| Venue | Official scope/author page | Current requirement relevant to these files |
|---|---|---|
| **Algorithmica** | [Aims and scope](https://link.springer.com/journal/453/aims-and-scope), [submission guidelines](https://link.springer.com/journal/453/submission-guidelines) | Publishes original algorithm papers with significant theoretical analysis. LaTeX is submitted with PDF plus all editable source files; Springer Nature’s LaTeX template is encouraged, not a requirement to use a special class. Abstract 150–250 words; 4–6 keywords; decimal headings at no more than three levels; numbered square-bracket references; title/author/affiliation/corresponding-email metadata and declarations are required. The current shared and factor-two amsart sources need conversion/cleanup if sent here. |
| **SIDMA** | [Scope](https://epubs.siam.org/journal/sidma/editorial-policy), [instructions for authors](https://epubs.siam.org/journal/sidma/instructions-for-authors) | Submit manuscript PDF and cover letter through the SIAM tracking system; figures must be inline. SIAM standard macros are strongly encouraged for TeX (accepted papers must provide TeX files); no special class is required at initial PDF stage. Brief title plus running head ≤50 characters; one-paragraph abstract ≤250 words; keywords and MSC codes; SIAM reference style; no simultaneous submission. Current amsart/article drafts are not final SIDMA source. |
| **TEAC / ACM journals** | [ACM journal submission instructions](https://www.acm.org/publications/authors/submissions), [TEAC journal page](https://dl.acm.org/journal/teac) | Current ACM primary article template is acmart v2.20 (August 2026); review submissions use acmart with the manuscript option in single-column format and the approved-package list. Submit editable source and PDF through the ACM journal submission site; ACM journals are OA from 2026, with APC/waiver implications. The current amsart/article sources cannot be treated as TEAC-ready. |
| **MOR (stretch only here)** | [Editorial statement](https://pubsonline.informs.org/page/moor/editorial-statement), [submission guidelines](https://pubsonline.informs.org/page/moor/submission-guidelines), [INFORMS LaTeX styles](https://pubsonline.informs.org/authorportal/latex-style-files) | Foundational mathematical OR/MS relevance is required; correctness alone is insufficient. Current submission format: 35–45 pages, 1.5 spacing, 11-point font, 1-inch margins, fully anonymized; ScholarOne submission; source + main-paper PDF; e-companion as separate PDF; OR/MS classifications. Use the INFORMS MOR LaTeX style when this route is actually chosen. The 26-page weighted-congestion draft is below the stated length range. |

## Cross-manuscript blockers before any venue conversion

1. **Independent review status:** do not describe any manuscript as externally validated or fully independently passed. Shared-catalog and weighted-congestion final independent reads are incomplete; factor-two repairs were self-checked after an earlier editorial FAIL.
2. **Attribution and novelty:** the \(\phi\) lower bound, standard repair/potential ingredients, known d upper bound, and prior weighted-congestion bounds must remain attributed. No acceptance or priority claim follows from internal proof records.
3. **Quantifiers:** preserve “there exists one complete exact-client continuation rule”; do not silently strengthen to every client equilibrium, heterogeneous catalogs, general facility count, all finite d, or a polynomial-time search algorithm.
4. **Metadata:** all three sources omit author/affiliation/email information; the first two PDFs have blank Title and Author metadata, and the third has blank Author metadata. Fill this only from the author’s supplied information.
5. **Template conversion:** choose the venue first, then convert the relevant source and rerun the venue-specific checks. The current generic classes are not evidence of submission-format compliance.

## Decision summary

- Shared-catalog \(\phi\): **Algorithmica → SIDMA**.
- Common-catalog factor two for arbitrary k: **SIDMA → TEAC (conditional on a game-theoretic reframing)**.
- Weighted-congestion structural paper: **TEAC → SIDMA**; MOR is a stretch after expansion and stronger OR/MS framing.

