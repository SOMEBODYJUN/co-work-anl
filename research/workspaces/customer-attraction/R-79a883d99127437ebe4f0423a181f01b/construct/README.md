# General counterexample construction attack

2026-10-24. Q-CAG-HALF remains **OPEN**. No genuine counterexample was found,
and this directory does not certify a general upper bound from finite LP runs.

The direct attack target is the existing constant-3 insurer interface: construct
a complete plan that is SPE at every positive-depth history and has

    OPT_m-2W-3Delta > 0,

where Delta is its exact maximum root regret over all legal root actions.
The existing compiler, not a new result here, would turn such a source into a
full-history pure SPE half counterexample after integer scaling. The dependency
is `R-d3981c0168644971803a9c3380ed687c/compiler/padded_insurer_repair.md`.

## Actual analytic increment

[homogeneous_screen.md](homogeneous_screen.md) gives a necessary intrinsic
catalogue condition for any genuine counterexample. If a legal B is a static
best response against r-1 copies of itself, then

    K=|B|,       OPT_m <= [1+(m-1)/r]K.

Every full SPE has W>=K. Thus r=m-1 already screens half for m>=2; any genuine
counterexample must have a strictly profitable escape from every homogeneous
topic at that replication count. The source version uses W+Delta>=K and gives
nonpositive insurer margin. The r=m case also supplies a sound symbolic prune
for fixed source-strategy cones. Root and independent-audit each independently
checked the derivation; the r=m-1 strengthening came from independent-audit.
This is a counterexample screen, not a continuing subclass project or a proof
of the general target in the residual catalogue class.

## Reproducible finite discovery only

[root_regret_attack.py](root_regret_attack.py) constructs complete ordered source
plans, optimizes every nonempty customer incidence type in each fixed plan's
cone, and imposes all positive-depth IC plus all root-regret bounds. It checks
each proposed positive LP witness with Fraction and rejects duplicate coverage
topics. No positive witness was produced. The small sampled cones are not an
exhaustive strategy search, and their negative floating optimum values are not
exact mathematical upper-bound certificates.

`root_regret_discovery_report.json` records the deterministic discovery run.
`seed_source_*.json` freeze the actual unit-client seed inputs and every ordered
action of the corresponding source plan. These plans need not be optimal at
the root. [audit_frozen_sources.py](audit_frozen_sources.py) imports neither the
SPE solver nor the LP code and exactly checks all positive-depth comparisons,
every root deviation, topic distinctness, actual coverage, and OPT. Its output
is `frozen_sources_exact_audit.json`. These frozen seeds are reproducibility
artifacts, not main-claim counterexamples or new positive theorems.

Reproduce from the repository root:

```sh
python3 research/workspaces/customer-attraction/R-79a883d99127437ebe4f0423a181f01b/construct/root_regret_attack.py --players 3 4 5 --variants 2 --sources 2
python3 research/workspaces/customer-attraction/R-79a883d99127437ebe4f0423a181f01b/construct/audit_frozen_sources.py
```

No further size expansion is justified by these negative samples. A next direct
attempt should use a new credible branching mechanism that survives the
intrinsic screen, rather than extend the same scan.
