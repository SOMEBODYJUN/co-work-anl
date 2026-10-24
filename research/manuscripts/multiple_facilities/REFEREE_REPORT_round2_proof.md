# Independent proof review (round 2): multiple facilities manuscript

## Scope and method

I independently re-derived the statements and proofs in `main.tex:31--221`, with special attention to the quantifiers in the continuation definition, clients that are newly covered or become unserved, the disappearance of a source location, isolated heavy atoms, the pure-improvement potential, simultaneous continuation choices, and the rational certificate claim.  I did not use the round-1 report as a proof premise.  I also ran the mechanical proof sanity audit:

```text
python3 skills_sources/math-proof-review/scripts/tex-proof-sanity.py \
  co-work-anl/research/manuscripts/multiple_facilities/main.tex \
  --bib co-work-anl/research/manuscripts/multiple_facilities/references.bib
```

It reports zero duplicate labels, undefined references, undefined citations, environment mismatches, and unlabeled theorem-like blocks.  The present file already contains the round-1 wording repair in `lem:capped` (`main.tex:153--155`) and in deviation Case 2 (`main.tex:195`).

## Independent statement and dependency map

1. Construction `con:selection` (`74--81`) chooses, over a finite family, a placement and a site assignment maximizing the sorted vector of expected facility loads.  Every covered client is assigned to one occupied location and then independently chooses one of the facilities there uniformly.
2. `lem:onpath` (`85--100`) uses that lexicographic maximum both to lower-bound every on-path facility load by `R/k` and to rule out a strict client deviation.
3. `lem:transfer` (`108--132`) derives budgets for the weight that can be present at an occupied destination or newly covered at an empty destination when one facility moves.  The `q_u=1` case accounts for clients assigned to the disappearing source.
4. `lem:packing` (`139--149`) partitions each budget of at most `(h+1)a` into at most `h` parts, allowing a heavy singleton.
5. `lem:capped` (`153--168`) runs strict pure client improvements while preserving a `2a` cap on every non-heavy facility and keeping heavy singleton clients fixed.
6. `lem:deviation` (`172--198`) applies the transfer and packing bounds to each unilateral move and obtains a pure continuation with moving-facility load at most `2L_f(p)`.
7. `thm:main` (`203--208`) combines the on-path mixed equilibrium, the finitely many actual-deviation continuations, and pure potential-based continuations at all remaining placements.
8. `prop:certificate` (`214--221`) gives a finite exhaustive procedure and a polynomial-size description for rational input; it does not claim polynomial-time search.

## Constructive re-derivation and adversarial checks

### Model and quantifiers (`31--65`)

- A placement is a labeled tuple in `S^k`; hence facilities co-located at a site remain distinguishable.  `A_i(s)` is exactly the set of facilities at occupied locations whose coverage set contains client `i`.
- A continuation is required at every labeled placement, while the facility inequality in `def:spe` is required only for unilateral deviations from the selected initial placement.  The completion proof uses exactly this quantifier scope.
- If `R=0`, positivity of weights implies each `C_t` is empty, so every client is unserved and every facility load is zero at every placement.  The zero branch in `thm:main` is therefore valid.
- For `R>0`, placing all facilities at a maximum-reach site yields the feasible uniform profile with load `R/k` on every facility.  Lexicographic maximality then gives `min_f L_f(p) >= R/k > 0`, so every later `a=L_f(p)` is positive.

### Lexicographic on-path equilibrium (`73--100`)

For a client assigned to `t`, the conditional cost at a facility at `t` is `w_i+(W_t-w_i)/q_t`; at a different accessible occupied site `v` it is `w_i+W_v/q_v`.  A strict improvement implies `(W_t-w_i)/q_t > b:=W_v/q_v`.  Reassigning only `i` to `v` changes every old `v` coordinate from `b` to `b+w_i/q_v>b`, leaves the other assigned locations unchanged, and changes the `t` coordinates to `(W_t-w_i)/q_t>b`.  Thus the count of coordinates at or below `b` strictly decreases, which makes the sorted vector lexicographically larger.  Since each client's expected cost is linear in its own probabilities, ruling out pure deviations rules out mixed improvements as well.

### Transfer bounds and coverage bookkeeping (`102--132`)

**`q_u>=2`.**  At an occupied target `t`, failure of `W_t <= (q_t+1)a` makes the new `q_t+1` loads larger than `a`; it also implies the old target loads `W_t/q_t>a`.  The source's remaining `q_u-1` loads become `q_u a/(q_u-1)>a`.  All old source coordinates equal to `a` are therefore replaced by coordinates above `a`, with no load elsewhere decreased.  At an empty target `r`, the newly covered set is exactly `C_r\setminus\bigcup_{t\in O}C_t`, of weight `N_r`; assigning it to the moving facility replaces one source coordinate `a` by `N_r`, while source-stationary loads increase.  A violation of `N_r<=a` again contradicts maximality.

**`q_u=1`.**  Here `J=J_u` has weight `a` and the source location disappears.  At an occupied target `t`, the added source clients are exactly a subset of `J\cap C_t`; clients in `J\setminus C_t` that still have a stationary accessible site can be assigned there, and the rest become unserved.  If `W_t+w(J\cap C_t)>(q_t+1)a`, then `w(J\cap C_t)<=a` implies `W_t>q_t a`, so old and new target coordinates are both above `a` while the sole source coordinate `a` disappears.  At an empty `r`, `N_r` and `J\cap C_r` are disjoint because `J\subseteq C_u\subseteq\bigcup_{t\in O}C_t`; a violation of `N_r+w(J\cap C_r)<=a` raises the new moving-facility coordinate above `a` while all other changed loads are nondecreasing.  Clients that lose all stationary coverage are correctly left unserved.

### Packing and pure potential (`139--168`)

The merge process stops only when every pair of distinct parts has sum greater than `2a`.  If `b>=h+1` parts remained, summing pair inequalities gives `(b-1)\sum_j B_j > 2a {b\choose2}=ab(b-1)`, hence total weight `>ab>= (h+1)a`, contradicting the budget.  Heavy parts are singletons by construction.

In `lem:capped`, the current statement is now the correct invariant: each client with `w_i>2a` is isolated at a stationary facility, and every facility that hosts no such client (including `f`) has load at most `2a`.  A heavy singleton's cost is its own weight and cannot strictly improve.  A non-heavy client at a facility of load at most `2a` cannot profitably join a heavy singleton, whose destination cost is `w_i+w_h>2a`; any other strict move satisfies `L_g+w_i<L_h<=2a`, preserving the cap at both destination and source.  The potential change is exactly `w_i(L_g+w_i-L_h)<0`.  The finite assignment space therefore forces termination at a pure Nash equilibrium, and linearity in a client's own mixing rules out a mixed improvement at the terminal profile.

### All deviations and continuation compatibility (`172--208`)

In Case 1 of `lem:deviation`, the source has `h_u=q_u-1` stationary facilities and mass `(h_u+1)a`; each other old site has the budget `(h_t+1)a`; an empty target receives only `N_r<=a` on the moving facility.  In Case 2, source clients are redistributed only to stationary accessible locations or to the moving facility when the new target covers them; the surviving-site mass is bounded by `W_t+w(J\cap C_t)`, and an empty target receives at most `N_r+w(J\cap C_r)`.  Every client covered after the move is assigned to an accessible facility, while clients that lose all access are left unserved.  The moving facility starts with load at most `a` and never hosts a heavy singleton, so `lem:capped` yields a pure equilibrium with moving load at most `2a`.

Distinct unilateral deviations from a fixed labeled placement change distinct coordinates, so the `k(|S|-1)` actual-deviation placements are distinct and their selected equilibria can be stored simultaneously.  At every other placement, a feasible pure assignment exists by choosing one accessible facility per covered client; the same finite decreasing potential gives a pure client equilibrium.  No facility condition is required at off-path placements under `def:spe`.

### Certificate and bit complexity (`212--223`)

For binary-rational weights, exhaustive enumeration of the finite placement/assignment family and exact rational comparisons is a valid finite procedure.  The on-path probabilities are `0` or `1/q_t`; actual-deviation profiles are pure; the number of stored profiles is `1+k(|S|-1)`, polynomial in an explicit input listing the clients, locations/incidences, and facilities.  A load denominator divides the product of input denominators times a single integer `q_t<=k`, so its bit length is the sum of input denominator bit lengths plus `O(log k)`.  The stored profiles and their facility inequalities are checkable by direct cost/load comparisons; correctness of the implicit default rule is supplied by the potential proof.  The proposition does not assert a polynomial-time search procedure.

## Issue list by severity

## Issue #1 — S4: make the old target-load comparison explicit in `lem:transfer`

- **Target:** `lem:transfer`.
- **Location:** `main.tex:120--121`.
- **What's wrong:** In the `q_u>=2`, occupied-target contradiction, the proof says that the new `q_t+1` coordinates and the previous target coordinates are above `a`, but the inequality `W_t>(q_t+1)a` implies the latter only after dividing by `q_t` and observing `(q_t+1)/q_t>1`.
- **Evidence:** The missing line is the elementary implication `W_t/q_t>((q_t+1)/q_t)a>a`; the rest of the sorted-vector argument is valid.
- **Impact:** Expository only. No downstream theorem is blocked.
- **Suggested fix:** Add after the failure assumption: `The old target load was also above a, since W_t/q_t>((q_t+1)a)/q_t>a.`
- **Confidence:** Certain.
- **What the user needs to decide:** None; this is a one-sentence clarity patch.

## Issue #2 — S4: state the finite tie-breaking rule for the selected lexicographic maximum

- **Target:** `con:selection` and `prop:certificate`.
- **Location:** `main.tex:73--81` and `main.tex:217--220`.
- **What's wrong:** The construction says to “choose” a lexicographic maximum, and the certificate proof says to “retain a lexicographic maximum.” Because maxima need not be unique, a deterministic implementation should state the fixed enumeration/tie rule used when several placements/assignments have the same sorted vector.
- **Evidence:** The finite family guarantees existence but not uniqueness. Any maximizer works mathematically, while a deterministic output procedure benefits from an explicit first-in-enumeration tie rule.
- **Impact:** Expository/algorithm-description only. The existence theorem is unchanged.
- **Suggested fix:** Add `Fix a lexicographic enumeration of placements and site assignments and retain the first maximizer among equal sorted vectors.`
- **Confidence:** High.
- **What the user needs to decide:** None for the theorem; choose any fixed total order for the certificate.

## Issue #3 — S4: clarify the scope of “all other placements” in the certificate

- **Target:** `prop:certificate`.
- **Location:** `main.tex:214--220`.
- **What's wrong:** The proposition correctly separates stored-profile verification from the symbolic potential proof of the default rule, but “a deterministic default rule for all other placements” can still be read as requiring an explicit table for exponentially many placements.
- **Evidence:** The proof stores only the on-path and actual-deviation profiles and stores the default rule as a fixed program; this is consistent with the final sentence but worth stating at the output-format level.
- **Impact:** Expository only. No correctness or size claim fails under the intended succinct-program interpretation.
- **Suggested fix:** Say `the default rule is output as a fixed program, not as an expanded table over all placements.`
- **Confidence:** High.
- **What the user needs to decide:** None; this makes the certificate model explicit.

## Severity summary

- **S0 (false/contradicted):** None found. I found no counterexample to the theorem or to any lemma under the stated assumptions.
- **S1 (serious gap):** None found. The source-disappearance and client-coverage cases are fully accounted for.
- **S2 (claim likely true but proof incomplete):** None remaining in the current file. The former heavy-singleton wording defect is repaired at `main.tex:153--155` and `195`.
- **S3 (missing hypothesis):** None found. Positivity, finiteness, common location set, and `k>=2` are used where required.
- **S4 (exposition only):** Issues #1--#3 above.

## Recommendation and second-round status

The mathematical proof is ready to enter a second round (indeed, no correctness blocker remains in the current `main.tex`). Apply the three optional wording patches if a deterministic certificate description and a more self-contained transfer contradiction are desired. If the journal's second round requires only correctness fixes, the manuscript can proceed without changing the proof strategy. The previous round's S2 wording issue should be marked closed after the present statement check.

## Audit trail

- Raw source reviewed: `co-work-anl/research/manuscripts/multiple_facilities/main.tex:31--221`.
- Mechanical check: `tex-proof-sanity.py` (all hard-failure counters zero).
- Independent attack categories attempted: endpoint/zero-reach cases; quantifier drift at off-path placements; loss and gain of client coverage; source-location disappearance; heavy singleton moves; inequality directions in all lexicographic transfers; finite-potential termination; labeled-placement collisions; and rational encoding/verification scope.
