# Second aggregate-security investigation — private checkpoint

2026-10-21. Scope remains Q-CAG-HALF: every full ordered-history pure SPE,
arbitrary finite common catalog and arbitrary number of unit providers.
Neither the general half-coverage theorem nor the strong aggregate-security
bridge has been proved or refuted here. No shared assets or git state changed.

## Candidate being attacked

For a legal fixed prefix b, r >= 3 remaining actors and their actual first
two actions A,B, write V=v_r(b) and V'=v_(r-2)(b+A+B). The candidate is

    u_1 + u_2 + (r-2)V' - rV >= 0.                 (PAIR)

This is the sum of two consecutive strong security-chain increments. If
PAIR held at all legal prefixes, grouping consecutive actors in blocks of
two and applying the known terminal one/two-actor floor would telescope to
P_r(b) >= r v_r(b), including W >= n v_n(0) at the root. This is a
conditional reduction, not a proof of PAIR. PAIR is stronger than the target;
its r=3 instance already contains the three-actor aggregate-security bridge.

Every security LP here uses an opponent distribution fixed independently of
the query. The root lower bound holds against *all* r-1-action backgrounds;
the upper bound after two moves uses a single independent distribution over
all r-3-action backgrounds. Neither is the last-move minimax theta.

## Exact harmless normalization

A customer liking every catalog label contributes 1/(|b|+r) to every actor,
every pure static query and every v_s encountered along a completion of b.
It changes no incentive row. Consequently its coefficient in PAIR is
2/(|b|+r)+(r-2)/(|b|+r)-r/(|b|+r)=0. Universal-interest mass may therefore
be deleted without losing a strict PAIR counterexample. The later cone and
joint-MILP runs enforce that deletion. This removes one trivial zero-gap
face, though other exact equality families remain.

## Material and present status

- `pair_attack.py`: exact integer set-valued SPE outcome recursion, followed
  by choosing the worst realizable first-two-action/terminal combination
  for the numerical PAIR objective. It expands a complete policy at every
  ordered history, builds every exact incentive row, and alternates root
  query p, tail independent opponent Q, and a full customer-mass-cone LP.
  Fixed legal backgrounds are supported. Output LP gaps are numerical only.
- `pair_n4k6.json`, `pair_n5k6.json`: completed 120 and 60 new policy cones,
  respectively, eight alternating LP steps per cone. No negative gap was
  found. These initial runs allowed universal mass; their saved best
  witnesses actually lie on nonuniversal disjoint-resource equality faces.
- `pair_joint.py`: a different joint MILP candidate generator, restricted
  to count-dependent policies and then unfolded to all ordered histories.
  It fixes a root query p and an independent tail opponent Q and varies the
  policy and customer masses jointly. The initial two 50-second runs found
  only numerical zero incumbents; both stripped variants timed out before
  finding an incumbent. Their bounds are not mathematical certificates.
- `phase_cones.py`: screens all two-group phase strings relative to either
  first or last action, with fresh/cyclic/repeated within-group choices. It
  includes the pattern of two early same-group players then two opposite-
  group players, which the earlier three named rule patterns did not cover.
- `disjoint_copy_probe.py`: exact deterministic backward induction on two
  disjoint copies of the 36-customer gadget, testing whether opening copies
  early can delay compensation across two steps. Root static security is
  exactly computable by uniform queries when the copies have equal mass,
  using transitivity of their label automorphisms. Intermediate security
  values are numerical screens.

All listed PAIR batches have now completed. The later runs were 300 new
four-actor/seven-theme cones, 120 five-actor/seven-theme cones, 150 cones at
each of the legal backgrounds 001 and 012345, plus 48 and 96 phase policies.
They found no negative gap beyond floating error. These are finite numerical
discoveries only. No more expansion of this negative sample route is planned.
The method has not supplied a general nonnegative dual, and these samples
do not establish PAIR or either global bridge.

## Exact static replication boundary and a different global mechanism

Read `disjoint_replication_bound.md` and its independent-definition audit:
for K disjoint old gadgets, one common query-independent opponent distribution
gives v_(3K)<=15/2+5/(2K). Thus profiles preserving 34 coverage per copy have
strict positive aggregate-security slack. The all-K statement concerns this
static dual; full SPE was computed only for the two-copy instances.

The next route is `cartesian_limit.md`: unlike the disjoint catalog,
Cartesian-product catalogs have additive security. It gives an exact
all-root-actions menu theorem for three actors, the rational convexification
limit of root security thresholds, and a finite-product counterexample
criterion. A two-copy full-history SPE shows that individually unavoidable
component root payoffs cannot be added. The 108-row compiler-cone LP and
300-instance product-limit screen found no aggregate-security counterexample.
The general product menu and finite example are candidate research assets
awaiting independent review. Neither half coverage nor strong security has
been solved or refuted.
