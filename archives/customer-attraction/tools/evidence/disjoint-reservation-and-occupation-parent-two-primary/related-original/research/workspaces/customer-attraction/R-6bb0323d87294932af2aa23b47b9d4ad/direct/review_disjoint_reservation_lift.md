# Independent audit: one disjoint reservation topic and one earlier player

2026-10-24. Parent supplied the proposed general statement and its intended
proof. I independently checked the quantifiers, reconstructed the proof,
compared the prior safe-padding/gluing interfaces, and performed a separate
expanded-unit exact replay. **No fatal objection found.** This is an internal
mathematical audit, not blind review, novelty certification, or a general
half-coverage proof. Q-CAG-HALF remains OPEN.

## 1. Exact audited statement

Let S be a finite nonempty old common catalog, n≥2 the number of old unit
providers, and σ a fixed complete ordered-history pure SPE. Assume that at
every old ordered decision history, the prescribed mover's final payoff
under σ is at least η. This hypothesis concerns every old history and the
true specified continuation, not only the actual path or an immediate payoff.

For each legal old theme T define

    δ_T=min_(S∈old catalog) |T∩S|.

Take an integer J≥0 and a new theme B consisting of J distinct new customers,
disjoint from every old customer. Add B to the common catalog and put one
new player before the old n positions. Assume

    J/2≤η,
    J≥max_T (|T|−δ_T/2),
    |T|/2>J/n for every old T.                    (H)

Then the enlarged n+1-player game has a complete pure SPE whose root action
is B and which follows exactly the original σ at every history beginning
with B and containing only old actions afterwards. All original on-path
payoffs are preserved and the new root receives J.

Unit-client requirements mean J is an integer. A rational version is valid
after one common positive integer scaling of all old and new multiplicities.
That scaling scales η, δ_T, and all sizes/payoffs together.

## 2. Full-history construction

Call a decision history nice if its first action is B and it has no later
B. At such a history prescribe σ on its old-action suffix. There are two
kinds of remaining domains:

1. Root's first action is an old theme T.
2. Root's first action is B and a later player has already selected B.

Both are irreversible: every descendant remains in the same domain. Choose
one complete pure backward-induction SPE in each first-old root child, and
one in each minimal first-extra-B subtree. These subtrees are mutually
disjoint. “Arbitrary BI fill” must mean a consistent full policy on each
such subtree; it need not mean independently incompatible choices of SPE
continuations at every descendant. A single recursive BI selector is one
explicit implementation.

At nice histories, continuing with the prescribed action keeps every
subsequent action old. Since B is disjoint from old customers, the mover's
prescribed payoff is exactly its original σ payoff, at least η.

An old-action deviation also remains nice and thereafter follows exactly the
original old σ. Its comparison is therefore precisely an original full SPE
comparison, with no frozen or changed old continuation. A deviation to B
may change the whole later continuation, but the old first B player is still
present. Every new customer then has at least two B providers, so this
mover's final payoff is at most J/2≤η regardless of the chosen bad-domain
continuation. Hence all nice-node comparisons hold. Other positive-depth
nodes are SPE by their selected complete subtree fill.

At the enlarged root, choosing B yields J. Consider instead root old T and
any complete SPE of that first-old child. If all n followers chose B on its
actual path, the last follower would receive J/n. Choosing old T at that
last history would receive exactly |T|/2, because the root T and this last
player would be its only old providers. The strict condition in (H) rules
out this all-B terminal outcome even with arbitrary ties.

Consequently some follower selects an old theme S. In that same terminal
profile, the old root receives at most 1/2 per customer in T∩S and at most
one per other customer in T. Thus its payoff is at most

    |T|−|T∩S|/2≤|T|−δ_T/2≤J.

This bound needs neither a particular old follower identity nor particular
offroot tie breaking. It uses actual follower optimality at the last node
to force one old follower, then same-profile common resource sharing. The
root is therefore optimal. This proves the complete SPE claim for every
old history and every offroot/bad history included in the construction.

## 3. Edge cases and precise limits

- Repeated old themes and duplicate old coverage labels cause no problem:
  δ_T is a minimum over all legal old actions and the same-terminal
  intersection bound still holds.
- Empty old themes or zero instances cannot satisfy (H). Indeed δ_T≤|T|
  gives J≥|T|/2; J=0 forces all old themes empty, contradicting the strict
  last-player condition. Thus a feasible instance has J>0 and every old
  theme nonempty, so the new disjoint B is distinct from all old themes.
  This is a restriction of this sufficient lift, not a restriction of
  Q-CAG-HALF.
- η may be a rational lower bound; it need not be attained, equal across
  histories, or a static security value.
- Arbitrary weak inequalities are allowed in the root upper bound and the
  nice B-deviation bound. The last-player exclusion uses the strict
  inequality as stated. Replacing it with a weak inequality is not
  justified by this proof.
- Nothing asserts that every enlarged SPE has this path, or that the added
  root's arbitrary offroot children preserve the old policy.
- The resulting offroot subtrees can be any complete pure SPEs; BI is a
  sufficient way to choose them.

## 4. Comparison with prior saved interfaces

I read:

    R-5d61c5324e744dc0a66133207fcbd010/security/
      safe_catalog_padding.md
    R-b8d328d492094423bb0c639039a1ea75/independent/
      disjoint_policy_gluing.md

Safe catalog padding keeps the player count fixed and adds cheap disjoint
actions. This lift instead adds a first player and an occupied B, using its
existing occupancy to halve every later B deviation. It is therefore not
the same population-preserving conclusion.

The generic nice-domain/irreversible-BI gluing device is already present in
these assets. This lift's root condition uses a true last-follower
comparison and a forced old-follower intersection. It does not replace that
condition by an immediate root outside-option cap. No global originality
claim is made for this proof component.

## 5. Independent exact old34/J19 regression

The old input is the existing 34-customer, six-theme full SPE in
`examples/customer_attraction/individual_security_failure.json`, with the
published complete policy: root0; second3 after X and0 after Y; last the
least unused label in the second player's group. The independent script
expands types into 34 distinct old unit clients and checks every old
ordered decision history and every legal action. It obtains

    η=29/3,
    old sizes=(23,23,21,23,23,21),
    δ_T=11 for every T,
    max_T(|T|−δ_T/2)=35/2,
    J/2=19/2≤29/3,
    min_T |T|/2=21/2>19/3=J/n.

The sibling security certificate had 14 different terminal ties on nice
histories, although its actual path was the same. To test the literal
preservation theorem, the independent script restores the published old σ
on all nice histories, while retaining the sibling's valid closed bad and
offroot subtrees. Direct unit-client evaluation verifies the resulting
entire policy:

    root path=(B,0,3,4),
    u=(19,29/3,67/6,67/6),
    W=51, OPT_4=53.

The separate static security certificate is unchanged by this tie
restoration. The script independently checks its rational primary
probabilities against every ordered three-rival background, and checks all
pure queries against its rational dual distribution. Both meet at

    v_4=28481/2924,
    v_4−u_2=647/8772>0.

Thus the nonroot original-instance security floor is false. This concrete
counterexample does not refute the aggregate security bridge, the
all-history floor-sum candidates, or Q-CAG-HALF.

Files:

- `audit_disjoint_reservation_lift.py`: independent expanded-unit audit; no
  canonical solver, construction code, sibling checker, or optimizer import.
- `disjoint_reservation_lift_audit.json`: exact results.
- `disjoint_reservation_literal_certificate.json`: full modified policy and
  unchanged exact p/Q security certificate.

The general proof is Section2, not the finite replay. All displayed example
numbers were recomputed in Python with Fraction arithmetic.
