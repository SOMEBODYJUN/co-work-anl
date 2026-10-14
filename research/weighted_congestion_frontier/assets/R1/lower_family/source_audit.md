# Source audit for WC-R1-LF-SHARP v1

Checked online 2026-10-14 by R1/lower_family.

Primary source:
https://arxiv.org/pdf/2002.07466.pdf

The retrieved PDF is 26 pages, dated March 7, 2022 on its title page and marked
arXiv:2002.07466v3 [cs.GT], 27 Mar 2022 in the margin. The abstract landing page
https://arxiv.org/abs/2002.07466 separately confirms that v3 is the latest revision
and dates it 27 March 2022. The direct versioned HTML/PDF endpoint was unavailable
through the search service; the unversioned PDF was successfully fetched and its
v3 marker was inspected. Search-service refs: turn5view0 (PDF), turn2view0
(metadata), turn7view0 (Section 3 continuation). These refs identify this
session's retrieval and are not portable citation identifiers.

Facts checked in the primary PDF:

- Section 2, PDF page 4: arbitrary positive player weights; player cost is the
  sum of resource latencies, without multiplying by its own weight; nonnegative
  coefficients; non-strict approximate-equilibrium inequality.
- Section 3, PDF pages 5–7: one heavy player, n equal light players, the strategy
  architecture used here, and Theorem 1's four-parameter supremum, equation (3).
- The same theorem prints the asymptotic lower estimate
  Omega(sqrt(d)/log d), and the explicit eventual bound sqrt(d)/(2log d).
- The source's proof splits states into heavy-alone versus shared main resource.
  Our full-state formulas and changed asymptotic parameters were independently
  derived; they are not claims quoted from the paper.

The original ICALP primary publication was also opened:
https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2020.32
and its 18-page PDF. We use the arXiv v3 statement as the authoritative version
for this comparison.

Novelty search queries included combinations of weighted congestion games,
approximate equilibria, nonexistence, and log log, plus the paper title. No source
was found reporting the sharp equivalent in this note. This is only a preliminary
search and does not establish absence from the literature. Search results also
identified Clara Waldmann's dissertation, Congestion Games: Equilibria, Networks,
and Complexity, whose abstract reports the original sqrt(d)/log d rate.

Crucial comparison: the new asymptotic is *inside* the pre-existing supremum.
Calling it a construction stronger than the paper's full parameterized theorem
would be inaccurate. Calling it a sharper asymptotic evaluation of that theorem
and a stronger explicitly proved growth rate is mathematically justified, subject
to independent proof review and a deeper novelty search.
