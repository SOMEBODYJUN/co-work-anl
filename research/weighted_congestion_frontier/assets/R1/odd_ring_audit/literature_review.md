# WC-TARGET v1: literature collision audit for the odd hub/cohort ring candidate

Audit date: 2026-10-14 UTC. Author: internal literature-audit subagent of R1.
Status: primary-source baseline checked; no stronger nonexistence collision found in this focused search. This is a search result, not a certification of novelty or completeness. Mathematical validity of the candidate is a separate obligation.

## Baseline and exact scope

**Christodoulou–Gairing–Giannakopoulos–Poças–Waldmann (CGGPW).**
[arXiv:2002.07466v3](https://arxiv.org/html/2002.07466v3), last displayed revision 2022-03-27; [ICALP 2020 primary record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2020.32); [MOR journal record, 2023](https://pubsonline.informs.org/doi/abs/10.1287/moor.2022.1272).

Exact locations: §2, equations (1)–(2); §3, construction before Theorem 1 and equation (3); §6, Theorems 4–5; §7.
The model uses arbitrary positive real player weights, arbitrary subsets of resources as strategies, nonnegative polynomial coefficients, degree at most d, and C_i(s)=Σ_{e∈s_i}c_e(x_e(s)). It agrees with WC-TARGET's cost convention and strict-improvement boundary. Theorem 1 applies for every integer d≥2 and gives nonexistence for all α below the supremum α(d) in equation (3), with proved Ω(√d/ln d) growth. Its polynomial gadget has one heavy player, n equal light players, two strategies each, paired resources with x^k and βx^d costs. It is a two-sided star, not an odd hub ring. Theorem 4 guarantees n-PNE for n players, so an unbounded lower bound requires growing player counts. Theorem 5's Ω(n/ln n) uses step costs and is outside WC-TARGET's polynomial class. §7 asks to close the polynomial gap to d.

**Caragiannis–Fanelli (CF).**
[arXiv:1902.07173v5](https://arxiv.org/html/1902.07173v5), displayed revision 2020-11-06; [ICALP 2019 primary PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol132-icalp2019/LIPIcs.ICALP.2019.133/LIPIcs.ICALP.2019.133.pdf).
Exact locations: §1 model; §2 Theorem 2(a), its displayed supremum; §3 Theorem 7; §4 conclusion.
The coarse general existence guarantee is d. Theorem 2(a) also gives a finite-degree expression below d: improvements merely below d are therefore not automatically new. The formal resource description uses positive monomials; general polynomial scope is made explicit in the next primary source. CF's costs are again sums of latencies. The §4 conjecture about their local potential method is expressly unproved, not an impossibility theorem.

**Giannakopoulos–Poças.**
[arXiv:2005.10101v3](https://arxiv.org/html/2005.10101v3), displayed revision 2022-03-30; [Theory of Computing Systems 2023 primary journal record](https://link.springer.com/article/10.1007/s00224-023-10133-z).
Exact locations: §4.1, Lemmas 2–3 and Theorem 2; Table 1. They explicitly cover polynomials with nonnegative coefficients, including degree-zero constants, and recover existence with approximation λ∈[d,d+1] and social-cost factor (d+1)/λ. This does not establish a stronger nonexistence bound or a universal o(d) existence guarantee.

## Later and mechanism-adjacent leads screened

| Primary source | Exact location / scope | Collision assessment |
| --- | --- | --- |
| [Ren–Wu–Xu–Yang, arXiv:2208.11309v1](https://arxiv.org/pdf/2208.11309), 2022; later title [Computing approximate pure Nash equilibria for weighted congestion games](https://www.sciencedirect.com/science/article/pii/S2667325825006338), DOI 10.1016/j.fmre.2025.11.014 | Preprint abstract, pp. 3–4 introduction/contribution: weights are normalized into [1,W], with W a fixed constant; algorithms use ρ/(1−ε), ρ=2W(d+1)/(2W+d+1) or d!. | Bounded weight-range computation, not arbitrary-weight nonexistence. The 2025 full article returned 403; exact scope verified against the primary preprint, not presumed for unread journal text. |
| [Hansknecht–Klimm–Skopalik, APPROX/RANDOM 2014](https://drops.dagstuhl.de/storage/00lipics/lipics-vol028-approx-random2014/LIPIcs.APPROX-RANDOM.2014.242/LIPIcs.APPROX-RANDOM.2014.242.pdf) | §7, Theorem 16, printed p. 256; Table 1. Tight two-player extremal ratio and four-resource construction; constant examples for small degrees. | Older local construction and finite-degree upper factors; no near-linear asymptotic nonexistence found. |
| [Harks–Klimm, MOR 2012, author-group primary record](https://www3.math.tu-berlin.de/disco/research/publications/?author=Max+Klimm) | Entry “On the Existence of Pure Nash Equilibria in Weighted Congestion Games,” 2012; continuous-cost consistency characterization, valid already for three-player games. | Exact equilibrium structural precedent; no quantitative growing-degree approximate nonexistence theorem identified. Full journal PDF could not be retrieved in this pass. |
| [Kleinberg–Ligett–Piliouras–Tardos, Beyond the Nash Equilibrium Barrier, ICS 2011](https://conference.iiis.tsinghua.edu.cn/ICS2011/content/paper/15.pdf) | §1.1, printed p. 126: asymmetric cyclic matching pennies on an odd player cycle; each payoff depends on a predecessor. | Odd-cycle anti-matching is established strategic-game reasoning. This source does not supply the proposed weighted polynomial resource implementation or degree-dependent bound. Avoid claiming the abstract odd-cycle contradiction itself is novel. |
| [Christodoulou–Gairing–Giannakopoulos–Spirakis, weighted price of stability, ICALP 2018](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2018.150) | Primary abstract: Ω(Φ_d)^{d+1}, Φ_d∼d/ln d, concerns price of stability. | A recurrent false collision in search: welfare loss among equilibria is a different quantity from the factor needed for equilibrium existence. |

## Comparison that may be stated conditionally

The repository-supplied sharper star-family envelope
(2/√e)√(d log log d)/log d is **repository-derived**, not a theorem statement read in CGGPW. A valid Ω(d/log d) nonexistence family in WC-TARGET would exceed both that working envelope and the published coarse Ω(√d/log d) baseline in asymptotic order. It would leave a logarithmic gap to the coarse d upper bound; it would not determine a_*(d) exactly. No collision found here means only that the candidate remains worth independent mathematical and broader bibliographic review.

## Search log and limits

Both web search engines were used. Routine discovery was checked with the stronger engine for coverage. Date-sensitive searches used recency windows of 365 or 1460 days; unrestricted searches also covered older mechanisms. The following query families were issued on 2026-10-14 (quotes preserved where material):

- `weighted congestion games approximate pure Nash equilibria nonexistence lower bound polynomial degree 2025 2026`
- `weighted congestion games "non-existence" "log" "degree"`
- `weighted congestion games polynomial latency approximate equilibria "linear" "lower bound"`
- `"weighted congestion games" "approximate" "lower bound" "2024"`
- `"weighted congestion games" "approximate" "nonexistence" "2025"`
- `"weighted congestion games" "d/log" equilibria`
- `"weighted congestion games" "odd" ring`
- `"A Unifying Approximate Potential for Weighted Congestion Games"`
- `"weighted congestion games" "nonexistence" "2023"`
- `"weighted congestion games" "cohort" OR "ring" OR "hub" approximate`
- `"weighted congestion" "nonexistence" -site:researchgate.net -site:ideas.repec.org` (1460-day window)
- `"weighted congestion" "lower bound" "equilibria" "sqrt"` (1460-day window)
- `"weighted congestion" "pure Nash" "2026"` (365-day window)
- `"weighted congestion games" "Ω" "nonexistence"`
- `"weighted congestion games" "non-existence" "polynomial"`
- `"weighted congestion games" "equilibria" "2024" "approximate"`
- `"congestion games" "approximate equilibria" "nonexistence"`
- `"congestion games" "approximate equilibria" "non-existence"`
- `"weighted" "congestion" "log d" "equilibria"`
- `"weighted polynomial congestion" equilibria "lower"`
- `"congestion games" "odd cycle" weighted`
- `"weighted congestion" "ring" approximate equilibrium`
- `"weighted congestion games" "three" "non-existence" polynomial`
- `"weighted congestion games" "hub"`
- `"On the existence of pure Nash equilibria in weighted congestion games" Harks Klimm pdf`
- `"weighted congestion games" "ring" "lower bound"`
- `"weighted congestion games" "cycle" "approximate" "lower bound"`
- `"weighted congestion" "d/log" -"price"`
- `"weighted congestion" "d/ln" -"price"`
- `"weighted congestion" "nonexistence" "2026"`
- `"weighted congestion" "nonexistence" "2024" "2025"`

Results repeatedly led to the 2020/2023 CGGPW paper, its thesis/journal versions, the sources above, or different models (mixed equilibria, matroid restrictions, splittable games, player-specific costs, Shapley sharing, welfare bounds). Search snippets sometimes lost a square-root symbol and falsely rendered the CGGPW bound as soft-Θ(d). Only the primary theorem text was used for the baseline.

This pass did not exhaust all forward citations, private manuscripts, author correspondence, or unindexed work. Some primary URLs errored; successful alternate HTML/PDF reads are identified above. No theorem of absence is inferred from failed retrieval or missing search hits.
