# Reverse review of SC-K-2-E

**Review scope:** the complete quantifiers and arbitrary-k proof in
[uniform_two.md](uniform_two.md), not its numerical plausibility.
**Review date:** 2026-10-02.

**Independence statement.** This is a separate reverse mathematical
reconstruction and a second code path in the same research execution, not a
claim that a second person, a separate AI agent, or external peer review has
endorsed the proof. The second exhaustive checker does not import the proposed
constructor, its packing routine, or its pure-improvement dynamics. No voting or
model-confidence score is used as evidence.

## A. Reverse derivation from a hypothetical violation

Fix a proposed on-path layout and one facility's load a>0. We first ignore how
the layout was chosen and ask: what is SUFFICIENT to refute the assertion that
every exact NE after a specified deviation gives that facility more than 2a?

It is sufficient to build one feasible pure assignment with (i) the deviator's
load at most 2a, (ii) all clients heavier than 2a isolated on stationary
facilities, and (iii) all other facility loads at most 2a. Every full-game
strict improving pure move preserves this set: a heavy client already incurs
its absolute minimum cost, no ordinary client can improve by joining it, and
an ordinary destination after an improving move is lighter than the old
source. The finite squared-load potential then supplies a pure exact NE in
this same set. No minimum-over-mixed-NE oracle is used.

To obtain such an initial assignment using h stationary facilities at one
physical site, the budget W<=(h+1)a suffices. Verify this independently by
merging bins of combined load at most 2a. If more than h bins remained, all
pair sums would exceed 2a, implying W>(h+1)a. Heavy bins remain singleton.
It is important that a bin exceeding the ordinary cap is permitted ONLY for
one heavy atom; a collection of small atoms cannot be called a macro.

We can now reverse the entire layout condition. If the old site of the
moving facility remains occupied, its assigned mass is exactly (h+1)a.
Any other occupied site with W>(h+1)a would permit moving the facility there,
keeping site assignments fixed, and increasing every old source coordinate a
without introducing a load at most a. Likewise, newly served weight >a at an
unoccupied target gives such an improvement. Thus a global lexicographic
maximum of the finite site-uniform family precludes every packing-budget
failure in this case.

If the old site DISAPPEARS, denote its assigned client set by J, w(J)=a.
A remaining site's budget must include all potentially rerouted J-clients
accessible there. If W_t+w(J cap C_t)>(q_t+1)a, moving the facility to t and
sending J cap C_t to t improves the sorted vector. Crucially, its old load was
also above a because w(J cap C_t)<=a. Remaining still-covered J-clients can
be reassigned without decreasing any other site's load. For a new target r,
the relevant new-facility budget is N_r+w(J cap C_r), and a value >a similarly
contradicts lexicographic maximality.

Consequently any arbitrary-k counterexample to the proposed factor-two theorem
would have to violate at least one of these elementary steps. No such violation
survives the checks below. The reverse argument neither assumes the selected
profile was already a facility equilibrium nor maintains a facility-response
potential across all off-path subgames.

## B. Specific fatal-objection tests

| Objection | Resolution / exact scope |
|---|---|
| Uniform mixing treats atoms as splittable | Each client chooses a single occupied site deterministically, then independently samples one facility. Conditional cost includes full w_i; equation (2) subtracts w_i/q_t. |
| Lexmax is taken only over equilibria, making modifications illegal | The finite optimization is over ALL feasible site assignments and layouts. It is shown afterwards to be a customer NE. |
| Customer leaves one site for another but the lex direction is wrong | A strict customer improvement gives (W_t-w_i)/q_t>W_u/q_u. Both modified site groups are strictly above the old lower level. |
| A low source may have zero load | Positive maximum reach gives feasible full colocation with every load R/k. Thus every selected load is at least R/k>0. Zero reach is separately trivial. |
| Source departure strands old customers | The q=1 proof explicitly reallocates J and includes w(J cap C_t), N_r+w(J cap C_r) in both transfer inequalities. |
| Target receives a huge atom that cannot be suppressed | Every >2a atom in the initial profile is on a stationary facility. The deviator's initial total is <=a. |
| Packing silently solves NP-hard bin packing | Pair merging uses <=n-1 merges; its h-bin guarantee follows from a pairwise-sum contradiction. No optimality assertion is made. |
| A heavy atom moves to an empty facility | It may be indifferent, but is not strictly improving. A NE requires no strict improvement, not movement on ties. |
| An ordinary client joins a heavy facility | It would cost >2a versus present cost <=2a, so it cannot improve. |
| The restricted invariant set hides improving moves in the actual game | Every possible improving full-game move either is excluded by an explicit cost inequality or remains in the set. |
| Pure equilibrium is not mixed-strategy Nash | Against deterministic others, expected cost is linear in the client's own distribution. No improving pure action implies no improving mixed action. |
| Different deviators demand incompatible continuations | Actual unilateral moves from one fixed LABELED layout produce pairwise distinct layout tuples. |
| Default subgames lack prescribed equilibria | A least-index pure initial assignment and strict pure best replies terminate by the same finite potential identity at every layout. |
| The chosen continuation must make every layout facility-stable | The definition requires customer NE at every layout and facility stability only at the on-path layout. |
| Heterogeneous facility catalogs also satisfy the proof | Not established: moving an arbitrary facility to any occupied site is essential in the transfer inequalities. |
| Small bit probabilities imply a polynomial algorithm | False. Global lexmax search and the improvement trajectory may be exponential; the theorem does not claim polynomial time. |
| A bad symmetric menu gives an unbounded lower bound | False, by SC-K-SYMMETRIC-MENU-OBSTRUCTION: the same displayed layout admits an exact SPE under asymmetric pure off-path equilibria. |
| The packing threshold proves global sharpness of 2 | False. The h+1 equal jobs example only refutes a stronger version of this scalar packing lemma. |

All arguments tolerate exact equalities at 2a and at (h+1)a. Positive rational
or real weights, identical site coverage, unserved clients, an empty client
set, one site, and every source/target multiplicity are included. Permuting
facility labels affects no existence argument but layouts are never identified
when constructing the complete continuation.

## C. Independent arithmetic paths actually run

First batch, seed 20261002: 563 exact inputs, 2220 actual deviations, 2770
unlisted labeled subgames independently completed by pure-NE enumeration,
11 independently recomputed labeled lexicographic optima, 43 true pure-NE
coordinate-extremum checks, 267 packing inputs, and 3 deliberately damaged
certificates rejected. There are 91 singleton-source and 2026 nonsingleton-source
nonzero-reach deviations, plus zero-reach cases; 1470 isolated-macro occurrences
and 885 strict client moves were exercised. k reached 50.

Second batch, seed 20261003: 612 inputs, ALL 1728 tied labeled lexicographic
maximizers examined, 6845 actual-deviation pure-NE minima verified directly,
3479 distinct subgames exhaustively enumerated, and 6845 independent transfer
budget checks. These include 83 positive overlapping-orphan budget occurrences
and 555 disappearing-source checks. The symmetric-menu family was checked at
7 q-values up to q=63 (k=64), covering all 274 actual labeled deviations, each
with deviator load zero in the full-model witness.

The two batches overlap in some tiny inputs; their instance counts must NOT be
summed and reported as distinct instances. The second batch does not depend
on the construction being correct: it directly enumerates all relevant pure
NE and checks the extremal inequality. It does not assert that all mixed NE
are pure or that they have bounded deviator payoff. Such a universal claim
would be stronger than, and unnecessary for, the existence theorem.

Reproduce with:

```sh
python3 tests/multi_facility/run_exact_audit.py --output /tmp/kfac_two_exact.json
python3 tests/multi_facility/run_reverse_audit.py --output /tmp/kfac_two_reverse.json
python3 tests/multi_facility/verify_delivery.py --output /tmp/kfac_two_delivery_validation.json
```

The last script is a delivery check, NOT the upstream repository's structural
or regression suite. Actual frozen data are in `evidence/runs/`.

A third, separate barrier audit checks 20 pairs (k,h), 1552 actual deviation
witnesses for both the bad lexmax layout and the good exact-SPE layout, and six
independent labeled lexmax enumerations. The proof in `lexmax_boundary.md`
excludes all NE choices at the bad occupancy by total mass and a strict forced
best response, while explicitly exhibiting an exact SPE elsewhere. This is
an obstacle to the *layout rule*, not a contradiction of SC-K-2-E and not a
factor-two lower bound for the original problem.

Delivery validation additionally evaluates the actual complete-rule evaluator
on all 351 labeled layouts of three saved instances, including 324 defaults,
checks four serialized certificates, rejects 15 malformed inputs and one bad
default declaration, and runs the CLI including its refusal to overwrite an
existing output. The earlier validation record belongs to the first checkpoint;
the final v2 record includes the later barrier audit and current source hashes.

## D. Outcome and residual obligations

**Internal mathematical review outcome:** the proof establishes the constant
existence branch for every k, with C=2; no remaining fatal objection is known
in this review. This conclusion rests on the general argument, not the finite
experiments. The unbounded-optimal-factor alternative is excluded in this exact
common-catalog model.

**Not established:** sharpness of 2, a phi upper bound for all k, a polynomial-time
construction, a lower bound >phi for the uniform constant, facility-dependent
catalogs, or externally peer-reviewed priority.

**Original delivery state:** this reverse review was written before a real
repository checkout was available; at that point merge, structure checks,
regressions, commit and push were pending. The later independent mathematical
review and actual integration checks are recorded in the
[repository audit](../../K_FACILITY_AUDIT_2026-10-02.md). A delivery-only check
does not by itself establish any of those subsequent operational steps.
