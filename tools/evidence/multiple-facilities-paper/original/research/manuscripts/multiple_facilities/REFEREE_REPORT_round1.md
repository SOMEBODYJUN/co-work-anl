# Referee report (round 1): multiple facilities manuscript

## Scope and protocol

I read `skills_sources/math-proof-review/SKILL.md`, the review protocol and Pass-B checklist, the complete `main.tex`, and the internal source proofs `research/current/multi_facility/model.md`, `uniform_two.md`, and `reverse_review.md`. I also ran the mechanical proof sanity check on `main.tex` with `references.bib` (no duplicate labels, undefined references/citations, or environment mismatches). The report below audits the formal TeX statement and proof; it does not treat finite computational tests as evidence for a universal theorem.

**Overall status:** one concrete proof-writing defect must be fixed before the theorem proof is formally closed. It is a one-line invariant correction, and the underlying argument appears sound after that correction. I found no counterexample and no separate S0 or S1 issue. The remaining items are exposition or scope clarifications.

## Issue #1 — S2: the cap lemma's formal invariant contradicts its intended application

- **Target:** `lem:capped`, used by `lem:deviation` and `thm:main`.
- **Location:** `main.tex:153--167` (hypothesis at lines 153--155; invariant argument at 157--167), with the applications at `main.tex:186--197`.
- **What's wrong:** The lemma assumes that every client with weight (>2a) is alone at a facility other than (f), **and** that “all other facilities have load at most (2a).” Literally, “all other facilities” includes the facilities hosting those heavy singleton clients, whose loads are their weights and therefore exceed (2a). Thus the premise is impossible whenever the packing step creates a heavy client. The proof of `lem:deviation` explicitly allows exactly this case: lines 188 and 195 say that a stationary facility may host a single client heavier than (2a), then invoke `lem:capped`.
- **Evidence:** `lem:packing` permits a singleton part of weight (>2a) (`main.tex:139--149`). In Case 1, the resulting profile is stated to have facilities that “either have load at most (2a) or host a single client heavier than (2a)” (`main.tex:186--188`); Case 2 repeats the heavy-singleton construction (`main.tex:193--195`). The cap proof itself uses the intended weaker invariant: it reasons separately about an isolated heavy client and about facilities of load at most (2a) (`main.tex:157--161`).
- **Impact:** As written, the formal invocation of `lem:capped` does not cover deviations containing any (>2a) client, so the proof of `lem:deviation` and hence the written proof of `thm:main` has a gap for those instances. The claim itself is likely true; no new argument is needed once the invariant is stated correctly.
- **Suggested fix:** Replace the final conjunct in the lemma statement by, for example:

  > “every facility that does not host one of these clients of weight (>2a) has load at most (2a), and (f) hosts no such client.”

  Equivalently: “all non-heavy facilities (including (f)) have load at most (2a), while each heavy client is isolated on a stationary facility.” Replace the corresponding sentence “every other facility has load at most (2a)” at `main.tex:195` by the same non-heavy formulation. The sentence at `main.tex:188` already has the correct disjunctive form. After this textual patch, the three invariant checks in `lem:capped` are valid and the deviation proof applies.
- **Confidence:** High (literal formal statement and the downstream profiles cannot simultaneously satisfy the stated condition when a heavy client exists).
- **What the user needs to decide:** Only whether to use “non-heavy facility” terminology or spell out the disjunction. No mathematical strategy choice remains.

## Verified mathematical obligations

The following parts re-derive correctly from the stated model, subject to the cap-invariant correction above.

### Model, quantifiers, and zero cases

- `main.tex:32--54` fixes a finite client set, positive atomic weights, a finite nonempty common catalog, labeled facilities, co-location, compulsory service whenever a client has an accessible facility, independent client randomization, and expected loads. The continuation is quantified over every labeled placement, while the facility inequality is imposed only at the selected on-path placement (`def:spe`, lines 47--55). This matches how the completion proof uses the quantifiers.
- If (R=max_t w(C_t)=0), positivity of weights implies every (C_t) is empty, so every client is unserved and every facility load is zero at every layout. The (R=0) branch of `thm:main` (`main.tex:206--208`) is therefore valid. If the client set is empty, the same branch applies.
- For (R>0), co-locating all facilities at a maximum-reach site gives the finite-family profile with all loads (R/k); lexicographic maximality then gives a strictly positive load for every selected facility (`main.tex:85--99`). Thus the later division by (a=W_u/q_u) is legitimate.

### Lexicographic on-path equilibrium

For a client (i) assigned to site (t), the conditional cost on a facility at (t) is (w_i+(W_t-w_i)/q_t), because (i)'s own probability must be excluded from the congestion term (`main.tex:91--94`). At another occupied accessible site (v), the cost is (w_i+W_v/q_v). A strict improvement gives ((W_t-w_i)/q_t>W_v/q_v=b). Reassigning only (i) makes every old (v)-coordinate (b) strictly larger and every (t)-coordinate strictly larger than (b), with all remaining coordinates unchanged (`main.tex:95--99`), so the sorted load vector increases lexicographically. No pure deviation improves; linearity in the deviating client's own probabilities rules out a mixed improvement. This check covers occupied-site ties and keeps unserved clients out of the assignment domain.

### Transfer budgets and covered/unserved clients

- For (q_u\ge2), moving the facility from (u) to an occupied (t\ne u) leaves (q_u-1) source facilities with load (q_u a/(q_u-1)>a). If (W_t>(q_t+1)a), the new (q_t+1) target coordinates and the old (q_t) target coordinates are all (>a), while the old (q_u) coordinates equal to (a) disappear. This is a strict sorted-vector improvement. Moving to an unoccupied (r) and assigning the genuinely newly covered set (C_r\setminus\bigcup_{t\in O}C_t) gives the analogous bound (N_r\le a) (`main.tex:108--121`).
- For (q_u=1), the source site disappears. The proof correctly includes (J\cap C_t) in an occupied target budget and (J\cap C_r) in an unoccupied-target budget (`main.tex:123--131`). Clients in (J) that lose the source but retain another occupied-site option can be reassigned there; clients with no remaining option become unserved. The two sets in the new-target case are disjoint because (J\subseteq C_u\subseteq\bigcup_{t\in O}C_t), while (N_r) consists of clients outside that union. No load other than the disappearing source coordinate decreases in either contradiction. These are the exact orphan/stranded-client cases required by the quantifiers.

### Packing and pure equilibration

- The pairwise merge argument in `lem:packing` is valid for positive real weights, including equality at ((h+1)a), empty lists, singleton heavy clients, and (h=1). If (b\ge h+1) parts remain and every pair sums to (>2a), summing the pair inequalities yields total (>(b)a\ge(h+1)a), contradicting the budget (`main.tex:139--149`). It is a constructive scalar packing argument, not an NP-hard optimal bin-packing claim.
- After the cap-statement correction, the invariant in `lem:capped` is valid. An isolated client of weight (>2a) has current cost exactly its own weight and cannot strictly improve. An ordinary client cannot strictly improve by joining such a facility because its current load is at most (2a). Any strict ordinary move satisfies (L_g+w_i<L_h\le2a), preserving the cap on source and destination. The weighted squared-load potential changes by (w_i(L_g+w_i-L_h)<0), so finitely many pure assignments imply termination at a pure exact client NE (`main.tex:156--167`). No strict pure move implies no mixed improvement because each client's expected cost is linear in its own probabilities.

### All deviations and complete continuation

- In Case 1 of `lem:deviation`, the stationary source has (h_u=q_u-1) facilities and mass ((h_u+1)a); every other surviving site has the budget from the transfer lemma. Newly covered clients at an unoccupied target have total at most (a), while an occupied target gives the deviator no initial client. Case 2 redistributes source-site clients with the stated stationary-option rule, packs the union of original and rerouted clients at each surviving site, and bounds the deviator by (N_r+w(J\cap C_r)\le a) when the target is new (`main.tex:181--197`). These assignments serve exactly the covered clients after the move and leave clients with no accessible facility unserved.
- The moving facility is never assigned a heavy singleton in the constructed seed, so the corrected cap lemma returns a pure NE with (L_f\le2a=2L_f(p)). The strict-improvement process is run in the full client game; no resource or option is silently deleted.
- Distinct unilateral deviations from a fixed labeled layout yield distinct labeled tuples (`main.tex:200--207`), so the selected pure equilibria can be assigned simultaneously. Every remaining layout receives a deterministic pure-NE continuation by starting with any feasible pure assignment and applying strict improvements. The same squared-load potential proves termination. Facility stability is required only at the selected on-path layout, so no off-path facility-stability condition is missing.

### Encoding and complexity claims

For positive binary-rational input, exhaustive enumeration of the finite placement/assignment family and finite improvement paths is a valid terminating exact procedure. On-path probabilities are (0) or (1/q_t), actual-deviation profiles are pure, and the number of stored labeled deviations is polynomial in an input that explicitly lists all (k) facilities (`main.tex:214--221`). Rational loads have polynomial bit length: a common product of input denominators, with one extra factor (q_t\le k) for an on-path facility, suffices. The manuscript correctly distinguishes this short/succinct certificate from a polynomial-time search procedure (`main.tex:212--223`).

## Plausible but not independently verified in this audit

- The bibliographic claims in the Introduction about Krogmann--Lenzner--Skopalik--Uetz--Vos (Theorem 5, Observation 4, and the Section 6 question) were not re-derived from the cited paper here. They are not used in the proof of the factor-two theorem; the citation and exact wording should be checked before submission.
- The proposition's phrase “their client optimality ... can be checked in time polynomial in their explicit encoding length” is clear for the stored on-path and actual-deviation profiles. It is less clear whether “their” is intended to include the implicit default rule for exponentially many layouts. The proof establishes universal correctness of that rule analytically via the potential, but does not present a polynomial verifier that expands all default executions. The existence and certificate claims remain plausible under the intended interpretation.
- No external theorem is used by the main proof. The real-weight theorem is non-effective as an algorithmic statement, while the rational-input proposition supplies only a finite exhaustive procedure; this distinction is correctly acknowledged but should remain explicit in any abstract or algorithmic summary.

## Exposition-only suggestions (S4)

### Issue #2 — S4: state the target-site load comparison explicitly in the (q_u\ge2) transfer proof

- **Location:** `main.tex:120--121`.
- **What's unclear:** The proof says that, if (W_t>(q_t+1)a), the new target loads and their previous loads are above (a), but does not spell out (W_t/q_t> a). The implication is immediate because (W_t/q_t>((q_t+1)/q_t)a>a), yet one sentence would make the sorted-vector argument self-contained.
- **Suggested fix:** Add “The failure also gives (W_t/q_t>((q_t+1)/q_t)a>a), so the old target coordinates were above (a) as well.”
- **Confidence:** Certain; this is an exposition gap only.

### Issue #3 — S4: disambiguate what is polynomially checkable in Proposition `prop:certificate`

- **Location:** `main.tex:214--223`, especially lines 215 and 220.
- **What's unclear:** The output contains an implicit default-rule program for all other labeled layouts, but the final sentence can be read as claiming a polynomial-time verifier for the universal correctness of that program. The proof actually gives a polynomial check for each stored on-path/deviation profile and a symbolic potential argument for the default rule.
- **Suggested fix:** Replace the final sentence of the proposition by: “The stored on-path and actual-deviation profiles, and the facility inequalities for those deviations, can be checked in time polynomial in their explicit encoding length; correctness of the default rule follows from the potential argument.”
- **Confidence:** High that this removes an avoidable scope ambiguity; no mathematical change.

### Issue #4 — S4: repeat the heavy-facility exception consistently in Case 2

- **Location:** `main.tex:193--197`.
- **What's unclear:** After packing, line 195 says “every other facility has load at most (2a)” immediately after saying that every (>2a) client is isolated. Line 188 uses the clearer “either ... or hosts a single ...” disjunction. This is the same terminology defect as Issue #1 in an explanatory sentence.
- **Suggested fix:** Say “every non-heavy facility has load at most (2a), and every heavy client is isolated at a stationary facility.”
- **Confidence:** Certain; exposition consistency only after Issue #1 is fixed.

## Findings by severity

- **S0 (false/contradicted):** None found.
- **S1 (serious gap requiring a new proof strategy):** None found.
- **S2 (claim likely true but proof incomplete):** Issue #1, the literal cap invariant in `lem:capped`; one-line statement correction repairs all downstream uses.
- **S3 (missing hypothesis):** None separate from Issue #1; the issue is a malformed/overly strong invariant rather than a missing mathematical premise.
- **S4 (exposition only):** Issues #2--#4 above.

## Minimal close condition

Change the cap lemma and the repeated Case-2 sentence to refer to non-heavy facilities (or state the equivalent disjunction), then rerun the mechanical sanity check. With that correction, the lexicographic transfer, atomic packing, full-game strict-improvement, labeled-continuation, and finite-rational-certificate obligations all pass this audit. The manuscript should retain the existing limitation that the construction is finite/exhaustive rather than a polynomial-time algorithm.
