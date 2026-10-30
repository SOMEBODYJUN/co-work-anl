# Referee report, round 1 — structural methods article

## Scope and protocol

- **Manuscript audited (read-only):** `structural_methods_article.tex`, current local copy, 1018 lines.
- **Local material read:** the complete manuscript; `README.md`, `REVISION-NOTES.md`, and `WRITING_STATE.md`; the eight local source notes named by the README; the local mathematical proof-review protocol (`skills_sources/math-proof-review/protocol/review-protocol.md` and `pass-b-common.md`); the read-research-paper exposition standard and skeptical-editor protocol (`skills_sources/math-paper-skills/skills/write-research-paper/references/exposition-standard.md` and `.../read-research-paper/references/skeptical-editor-review.md`).
- **Mechanical check:** `tex-proof-sanity.py` reports 0 duplicate labels, 0 undefined refs, 0 undefined cites, 0 environment warnings, and 0 unlabeled theorem-like blocks.
- **Review status:** This is a referee audit, not a publication certificate. The classifications below distinguish what follows from the displayed manuscript from what remains imported or unverified.

## Recovered mathematical contract and section jobs

The manuscript has a coherent four-section route: model and scope (Section 1), local marginal/scale/depth/repair interfaces (Section 2), an explicit finite all-state counterexample family and its uniform near-degree specialization (Section 3 plus Appendix A), and positive stability/social-cost applications (Section 4). The key separation is mathematically correct: a local scale-contract failure is not itself nonexistence, and the all-state theorem needs the explicit front coverage plus legal same-degree gates.

## Verification ledger (high-level)

- **Endpoint/area estimates (L97–L172): verified as written.** The right-sum error telescopes for nondecreasing (f); the normalized endpoint formula and finite-window threshold have the displayed directions. The proof correctly keeps the endpoint mass (M), total window mass (Q), and mesh (h) separate.
- **Common-player-scale lemma (L76–L92): verified as written.** Applying the lower insertion bound to deleted resources and the upper bound to added resources gives the displayed retained-resource correction; nonnegative retained cost justifies the second inequality. Finite state space then gives termination and a minimum-potential equilibrium.
- **Two-type scale/cycle tools (L203–L355): verified within their stated contract/domain.** The ordered insertion bounds, (D/U) mixture, cycle difference constraints, and finite-population interval projection are internally consistent. “Exact” is correctly restricted to the specified potential dictionary/common-scale contract, not the best equilibrium factor of the original game.
- **Player-height potential and inverse (L360–L418): verified as written.** The rank ordering gives the three marginal regimes, the geometric mixture identity is valid also at (t=1), and the two logarithmic branches in the inverse are handled with the correct inequality reversal. The statement is a sufficient potential guarantee and a necessary depth condition, not a depth-suffices claim.
- **Stable-core gates (L421–L500): verified as written.** The (010/101) trigger characterization and earliest-error single-player repair are correct. A correction need only clear gates involving the mover; other gates may remain triggered and do not affect that mover’s deviation bound. The approximate tolerance in (L445–L448) is necessary for α>1.
- **Uniform-family parameter proof and front coverage (L503–L567, L764–L955): verified/plausible as written.** I re-derived the key inequalities (H>0), (1<S\le bR), (J/H\ge K/8), (Z\ge N/2), (N>gK), the defect budget, both parity cases of the return test, and the same-degree gate budget. Direct small-(N) resource simulations reproduce the heavy/light/return endpoint formulas and gate characterization. The proof covers every product-front phase vector by the mismatch/short-difference split and every nonfront bit string by an explicit current-state single-player correction.
- **Uniform near-degree quantifiers (L559–L590, L957–L991): verified as written.** With (n=\lceil d/(1200\lceil\log_2d\rceil^2)\rceil), the displayed rounding, (d\ge8n), (T>16nd), and (200n(\log d)^2<d\log(3/2)) estimates give the stated “for every integer (d\ge2^{20})” quantifier. Nonnegative target costs correctly transfer the strict factor from α to (d-1200\ell^2\).
- **Positive small-share, regularization, social decomposition, and social-repair statements (L595–L726): verified/plausible within the displayed assumptions.** The integral-potential share bound, social insertion externality bound, gate constant-shift identity, SD/RD separation, and regularized-core transfer have the required hypotheses. These are finite selection/quality statements; they do not imply a polynomial equilibrium algorithm.
- **Imported material:** the (d)-approximate existence theorem attributed to Caragiannis–Fanelli and the prior Θ(√d/log d) historical bound are not re-proved in this manuscript. Their use is properly marked as imported, but their external statements were not independently source-checked in this local audit.

## Findings

## Issue #1 — [S4] Undefined social optimum notation

- **Target:** `\OPT` usages in Proposition `prop:regularization` and Theorem `thm:socialrepair`/Corollary `cor:jointselection`.
- **Location:** `structural_methods_article.tex:56–58`, `:661–687`, `:716–726`.
- **What's wrong:** The manuscript defines the welfare (W) but never defines `\OPT(G)` as “\(\min_s W(s)\)” (or otherwise specifies the admissible state domain). The standard abbreviation is guessable, and no algebraic conclusion is invalidated, but the social-quality statements require the reader to reconstruct the referent.
- **Evidence:** `\OPT` is only declared as a macro at line 15 and first used as a mathematical object at line 661; no definition or minimizing display precedes it. This fails the exposition protocol's exact subject/predicate/referent test while `tex-proof-sanity.py` correctly reports no TeX-reference error.
- **Impact:** Exposition/interface precision only; no downstream proof step changes once the conventional definition is supplied.
- **Suggested fix:** Immediately after (or before) (eq:welfare), add: `For any game (G), write \(\OPT(G):=\min_{s\in\prod_iS_i}W(s)\).` If a restricted domain is intended in any displayed formula, state it there (e.g. `\OPT(G_+)`).
- **Confidence:** High.
- **What the user needs to decide:** Confirm whether `OPT` always means the complete game's minimum over all pure states; the current theorems use that meaning.

## Issue #2 — [S4] Repeated gate parameter/completion material across the main text and Appendix

- **Target:** Uniform-family completion and same-degree gate budget.
- **Location:** Main text `structural_methods_article.tex:469–500` and `:503–557`; Appendix `:913–955` (especially (eq:maincompletion), (eq:appclocks), (eq:apprepairtarget), and the two final margin displays).
- **What's wrong:** Section 3 introduces (B_*,M), the complete anchored gates, and a short theorem proof; Appendix A reintroduces the same gate count, (M=2\alpha B_*), the same monomial, and then repeats the full two-case margin argument. The repetition is understandable for a self-contained appendix proof, but the main text currently reads as if it has already supplied the construction proof while the appendix repeats its central definitions and conclusion.
- **Evidence:** `eq:maincompletion` (main text) and `eq:appclocks` (Appendix) are identical definitions; the main theorem proof (around lines 484–490) invokes the Appendix, while lines 946–955 re-establish the exact same front/nonfront margins and degree conclusion. A reader must backtrack to determine which copy is authoritative.
- **Impact:** No correctness impact; it increases length and weakens the four-section architecture's division between construction statement and technical verification.
- **Suggested fix:** Keep the complete players/resources and parameter definitions in Section 3, but in Appendix A replace the repeated gate setup by a one-sentence pointer to (eq:maincompletion), retaining only the proof-specific bounds (eq:appbasecap) and the budget calculation. Alternatively, keep all gate definitions in the appendix and have Section 3 point forward once; do not maintain two independent copies.
- **Confidence:** High.
- **What the user needs to decide:** Choose whether the target venue wants a self-contained explicit construction in the main text (recommended) or a shorter construction statement with all resource details in the appendix.

## Issue #3 — [S4] Introductory roadmap repeats the same interface inventory

- **Target:** Introduction and section opening.
- **Location:** `structural_methods_article.tex:35–46`, `:64–65`, `:70–71`, `:593–593`.
- **What's wrong:** The four introductory paragraphs (local/global problem, three tools, positive uses, and counterexample use) already give the complete narrative. The Organization block and the opening sentence of Section 2 then repeat essentially the same inventory; Section 4 repeats the positive-use inventory again. The text is clear, but the marginal reader value of the repeated roadmap is low after the first encounter.
- **Evidence:** Lines 37–41 enumerate endpoint/area, scales, front realization, positive uses, and the counterexample chain; line 65 lists the same three sections and appendix; line 71 restates the three Section-2 interfaces; line 593 restates the three positive applications. Deleting or compressing one copy would not remove a mathematical hypothesis or dependency.
- **Impact:** Exposition only; the mathematical route remains recoverable after compression.
- **Suggested fix:** Keep the Introduction's narrative plus the required Organization block. Shorten the Section 2 opening to one local handoff sentence naming its immediate first result, and shorten the Section 4 opening to the two new tasks (small-share bound and social selection) without re-listing all prior tools.
- **Confidence:** High.
- **What the user needs to decide:** Venue/detail budget; no mathematical decision is required.

## Issue #4 — [S4] Social-cost symbols are introduced by use rather than a single notation sentence

- **Target:** Positive/social applications.
- **Location:** `structural_methods_article.tex:645–654`, `:661–687`, `:719–726`.
- **What's wrong:** (W^B), (W^+), (C_i^B), and (C_i^+) are inferable from the base/augmented-game context, but the manuscript never gives one explicit notation sentence defining them before the first decomposition. The lack of a local referent is especially noticeable because `W` was defined globally at line 56.
- **Evidence:** The first formal appearance is (W^+(s)=W^B(s)+K_0+\cdots) at (eq:allsocial), followed later by base-game margins and `OPT(G_+)`; no preceding sentence says (W^B) is the welfare of (G_B), (W^+) that of (G_+), or that (C_i^pm) use the corresponding resource sets.
- **Impact:** Exposition/notation precision only; the decomposition and quality inequalities are mathematically interpretable.
- **Suggested fix:** Before (eq:socialgate), add one sentence: `Write (C_i^B,W^B) for costs/welfare in (G_B), and (C_i^+,W^+) for those in the augmented game (G_+).` Define `OPT` in the same notation block (Issue #1).
- **Confidence:** High.
- **What the user needs to decide:** None beyond choosing whether to combine this with Issue #1 as one notation repair.

## Issue #5 — [S4] Repeated boundary caveats could be consolidated

- **Target:** Scope qualifications around contract failure, finite selection, and all-state coverage.
- **Location:** `structural_methods_article.tex:255–256`, `:286–288`, `:466–468`, `:726`, `:750`, `:754–758`.
- **What's wrong:** The manuscript repeatedly warns that a failed scale contract is not an original-game counterexample, that finite enumeration is not a polynomial algorithm, and that a single improvement sweep is not all-state nonexistence. These are useful once near each relevant theorem, but the final Section 4 discussion restates several of them after they have already been made locally.
- **Evidence:** The same negative-scope distinctions appear after the cycle theorem, after the core theorem, in the regularization paragraph, in the enumeration paragraph, and again in the concluding interpretation. The protocol's necessity audit treats a qualification as earning space only when it prevents a new plausible false inference; the late repetitions protect against inferences already blocked at first use.
- **Impact:** Exposition only; no hypotheses should be deleted from the theorem statements.
- **Suggested fix:** Retain the local caveat immediately after each theorem where it blocks a likely misreading; compress the final three paragraphs to a short cross-reference to those local boundaries.
- **Confidence:** Medium-high.
- **What the user needs to decide:** Preserve any venue-required limitations paragraph; otherwise merge the repeated warnings into a single end-of-section “scope of certificates” paragraph.

## Unresolved / unverified items (not findings of falsity)

1. I did not independently verify the external Caragiannis–Fanelli theorem or the historical CGGPW bound against the cited papers. The manuscript marks these as imported; publication review should source-check the exact model and degree convention.
2. The asymptotic lower bound is only as strong as the displayed Appendix-A all-state proof. The local finite audits and small simulations support the incidence formulas, but they do not replace a fresh full independent proof pass over every quantifier. I found no concrete endpoint, parity, degree-budget, or state-coverage counterexample in this audit.
3. No publication/novelty judgment is made. The conclusion (d-1200\lceil\log_2 d\rceil^2\le a_*(d)\le d) follows algebraically if the imported upper theorem and `thm:near` are accepted.

## Overall referee verdict

**Mathematical status:** No S0 (false/contradicted), S1 (serious gap), S2 (proof incomplete), or S3 (missing hypothesis) issue was found in the local manuscript. The structural implications, parameter inequalities, front parity split, nonfront repair, and near-degree quantifiers are internally coherent and are at least plausible/verified at the displayed level. The paper should not be certified publication-ready solely from this audit because the external theorem/model match and a fresh independent full proof pass remain outside the local check.

**Editorial status:** The paper is coherent but has S4 notation/interface repairs and repeated roadmap/completion material. Fixing Issues #1 and #4 is mechanical; Issue #2 is a worthwhile compression/authority decision; Issues #3 and #5 are optional shortening edits.
