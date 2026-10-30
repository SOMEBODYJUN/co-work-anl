# Referee report (round 1)

**Manuscript audited:** `main.tex` (shared-catalog manuscript), including Appendices `app:cycle`, `app:cross-chord`, and `app:polynomial-chord`.

**Scope.** I checked the model equations, the repair lemma, menu definitions, the continuation-rule argument, and the displayed algebra in the local chord construction. I also ran the mechanical TeX sanity checker (no duplicate labels, undefined references/citations, or environment mismatches). The long response-cycle proof has several dependencies whose hypotheses are not always stated at the point of use; those are reported as unverified rather than silently accepted. No explicit S0 counterexample to the main existence claim was found in this pass.

## Findings

## Issue #1 — [S2] Equal-reach parenthetical is false and can invalidate the menu if implemented literally

- **Target:** `con:menu`, `lem:chord`
- **Location:** `main.tex:122-134` (especially lines 131-133)
- **What's wrong:** The text says that when the reaches are equal, family E “itself meets these targets” ((L_U,L_V) >= (qV,qU)), and that one may use E instead of the strong-chord output. E is the independent half split, with load (R/2) at each endpoint. Since (q ≈ 0.618 > 1/2), this does not meet (qR) in general.
- **Evidence:** At equal reaches (U = V = 1) with no private clients and one common client of weight (1) (a co-location is exactly this case), E gives loads (1/2, 1/2), while the stated targets are ((q,q). More generally, at a co-location with reach (R = W > 0), E gives (R/2 < qR). The chord hypothesis (W < qV) fails at this co-location, so E is the only menu member there; it is still sufficient for the actual menu-cover threshold (q,d(s)), but not for the claimed (qR) targets.
- **Impact:** The parenthetical is mathematically false. If an implementation follows “use E instead,” the asserted local quota and the later menu-cover proof are not justified. The main theorem can retain its intended proof only if the strong-chord member is kept whenever the chord hypotheses hold, and the equal-reach sentence is removed/rephrased.
- **Suggested fix:** Delete “At equal reaches E itself meets these targets; one may use it instead” and state precisely: “When the strict chord hypotheses hold (including (U = V) for distinct locations), include the chord output. E is retained separately for the equal-half argument at co-location; it is not a (qR)-quota witness.”
- **Confidence:** Verified.

## Issue #2 — [S2] The “exactly one member of a large pair” paragraph silently assumes an oriented best-response edge

- **Target:** cycle proof, `chord-retaining-exactly-one-member-of-a-pair`
- **Location:** `main.tex:321-341), especially lines 337-341
- **What's wrong:** The displayed hypotheses only say that s has pair {h,j}, t contains h but not (j), and (R_s <= R_t). The conclusion
  [
  d(s)>phi(R_t - H)
  ]
  does not follow from these local reach/coverage hypotheses alone. It uses the no-witness inequalities for a specifically oriented (b)-edge, but the edge orientation (whether (t -> s) or (s -> t)) is never stated in this sublemma.
- **Evidence:** The construction gives a pure equilibrium with loads (U=R_s-sigma) and (V=R_t-H), and hence a menu upper bound on whichever endpoint is the responder. To turn this into d(s) > phi V, one needs the no-witness inequality Q < q d(s) with Q = V, i.e. the oriented edge (t -> s). With the opposite orientation (s -> t), the same profile has incumbent load U > q and yields a different contradiction. As written, the proof moves between these two orientations without declaring one.
- **Impact:** Later uses (“an edge to a different pair cannot weakly increase reach,” lines 436 and 434) depend on this lemma. The intended conclusion may be correct, but the current statement/proof leaves a quantifier and orientation gap.
- **Suggested fix:** State the exact hypothesis, e.g. “Assume (t -> s) is a response edge in the normalized no-witness cycle.” Then write the two orientation cases separately and derive (d(s)>phi(R_t - H)) from (Q=R_t-H<q,d(s)). If the intended claim is that no edge (s -> t) can exist, state that instead and use the U > q contradiction.
- **Confidence:** Verified as a missing hypothesis/quantifier; the underlying intended edge claim is plausible but not established by the text as written.

## Issue #3 — [S1] The common-(h) transport step uses an unproved reach-order implication

- **Target:** cycle proof, `a-common-h-edge-with-d-above-q-has-unique-transport`
- **Location:** `main.tex:469-485`, first sentence of line 471
- **What's wrong:** The proof says “Equation (9-2) first implies R_t < R_s” for an edge (s -> t) with d(s) > q. Equation (9-2) only states
  [
  u(t,s)=d(s)le R_t-H.
  ]
  This gives R_t >= H + d(s) > H + q; it does not by itself imply R_t < R_s.
- **Evidence:** No inequality relating R_s and R_t is derived before the strict order is used in the definitions Delta = R_s - R_t > 0 and sigma < R_s - R_t (lines 479-485). A separate argument using the oriented no-witness bounds, the pure menu member, or a prior reach-capacity lemma is required. Without it, the subsequent “reverse assignment,” strict dominance, and unique-transport conclusion are not licensed.
- **Impact:** This is a gate step for the two-anchor lemma and for the closure of the empty/single-pair cases (lines 691-741). A missing proof here blocks the structural lemma, hence the main theorem.
- **Suggested fix:** Add a derivation of R_t < R_s from already established hypotheses (including the exact edge orientation and the menu member used), or replace the claim by the weaker inequality actually proved and rework lines 479-485 accordingly. The repair must explicitly establish (Delta>0) before using it.
- **Confidence:** High that the displayed implication is unsupported; I did not prove the intended conclusion false under all cycle hypotheses.

## Issue #4 — [S2] Strong-chord polynomial constructor is specified only by reference to “finite case choices”

- **Target:** algorithmic part of `lem:chord` and Theorem `thm:main`
- **Location:** `main.tex:1074-1112`, especially lines 1085-1092
- **What's wrong:** After the exchange algorithm, the constructor says “follow the finite case choices” from the existence appendix and “select the prescribed third mixer, a decreasing-weight prefix, or the stated pure seed,” but it does not give a complete decision procedure identifying which case applies or how the quota test is performed before each transition.
- **Evidence:** The existence proof is a contradiction argument with branches such as d > U, d < -Z, “if some latter client has weight v in [d/3, d],” and prefix selection. The algorithmic paragraph does not state how the current equilibrium is represented after a branch, how equality/end-point cases are assigned, or which exact inequalities are tested. The stated (O((k+1)^4)) bound therefore has a plausible outline but not a fully checkable algorithm.
- **Impact:** The existence theorem may survive, but the claimed polynomial-time construction and rational output are not publication-grade until the branch logic is made executable.
- **Suggested fix:** Give pseudocode (or a numbered branch table) with the exact tests, tie rules, coordinate updates, and a proof that each branch returns an NE satisfying both quotas. Then charge each scan/sort and update to the stated operation bound.
- **Confidence:** Verified as an exposition/algorithm-specification gap; no running-time counterexample found.

## Issue #5 — [S2] Fixed-client stability is asserted, not propagated through the repair sequence

- **Target:** polynomial constructor, S < delta branch
- **Location:** `main.tex:1090-1104`
- **What's wrong:** In the S < delta branch, the largest client (x) is held fixed and the other clients are repaired. The text says “The fixed customer's stability is proved there and is preserved throughout,” then treats fixed customers as private base load in the move-count argument. It never checks that each intermediate move preserves the inequality that keeps (x) from deviating.
- **Evidence:** A move changes the two facility loads by ± w, so the load difference relevant to x's deviation changes at every step. The static inequality at the initial seed (lines 831-837) is not automatically invariant under arbitrary largest-improvement moves. The move-count proof (lines 1094-1104) only proves termination/no-repeat for movable clients; it does not prove x's best-response condition after each move or at the final profile.
- **Impact:** The algorithm may output a pure profile that is an NE for movable clients but not for the fixed client, invalidating the chord output and the complexity theorem in this branch.
- **Suggested fix:** State the invariant explicitly (e.g. a bound on the absolute gap relative to (x)) and prove it is preserved by every permitted move; or re-check x's NE inequality at the final profile and, if it fails, specify a repair that also moves (x).
- **Confidence:** High that the preservation argument is missing; the intended invariant may be repairable.

## Verified portions

- Equations (38)-(45) correctly derive individual mixed-strategy NE conditions from expected loads, including the client's own atomic weight.
- Lemma `lem:repair` is consistent with the strict-improvement condition: before reversal the gap decreases, initial lower-side clients cannot become improving, and at reversal previously moved clients remain stable.
- Menu T's probability formula is valid when D = B - A + Z in [0, min(w_h,w_j)]; it yields gap Delta = D, making designated clients indifferent and the remaining clients at the lower-load side stable.
- The continuation-rule inequality in Theorem `thm:main` follows once Lemma `lem:menu-cover` is granted: u(r,t) <= d(t) <= phi L_s(e) and symmetrically for the other facility. The two ordered deviation families are disjoint.
- The box-slice exchange identities and the sign conditions in eqref{eq:old-B-1}--eqref{eq:old-B-2} are algebraically consistent on their stated feasible segments.
- Mechanical audit: `tex-proof-sanity.py main.tex --bib references.bib` reports no duplicate labels, undefined references/citations, or environment mismatches.

## Overall assessment

The headline claim is **plausible but unverified** from the current text. The local NE algebra, repair operation, and continuation logic are sound once the structural lemma is supplied. Issues #2 and #3 occur inside the proof of the structural lemma and must be repaired before the theorem can be called proved. Issue #1 is a concrete false sentence that should be removed even if the intended menu construction remains salvageable. Issues #4 and #5 block the stated polynomial constructor until the branch algorithm and fixed-client invariant are made explicit.

