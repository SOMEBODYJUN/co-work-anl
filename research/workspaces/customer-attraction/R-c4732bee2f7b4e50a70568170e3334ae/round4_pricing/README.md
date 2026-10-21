# Full histogram pricing of retained-overlap pair partitions

Status: exact primal and full-universe dual certificates agree for the full
557-row system, at

178528430822287579296070598592537012737 /
87421565922360356032366460363114422206 = 2.042155490337931... > 2.

The target Q-CAG-HALF remains OPEN.

This directory develops unrestricted column generation for the 437 original
five-player indexed rows, ten terminal offdiagonal rows, and 110 retained-
overlap pair-partition rows. All 1024 fixed masks, six optimal multiplicities,
792 histograms for each third-position family, and 15,504 histograms for the
second-position family are admitted. The common optimal multiplicity is the
only cross-family histogram coupling in this stated relaxation. Menu overlap
variables retain their full permitted integral range.

No resulting relaxation point is automatically a genuine SPE or an actual
OPT certificate. No bound on the old 64 support types is treated as universal.

`exact_primal_overlap1.json` is a self-contained 60-atom rational point with
W=1 and comparison coverage about 2.04202004419. All 557 necessary row slacks
are recorded and checked exactly by `exact_primal.py`. Its source-CG hash is
provenance for an intermediate 1,581-column discovery state that was not
separately frozen; that discovery input is not needed to verify this point.
The parent has independently reconstructed the exact rows and the new
index-partition sums without importing the pricing implementation.

`cg_overlap1_final.json` freezes the completed full-universe floating column
generation: 2,183 generated columns and numerical optimum 2.042155490337931.
`exact_optimum_primal_overlap1.json` gives 67 positive rational masses with
all 557 exact nonnegative slacks. `exact_dual_overlap1.json` gives 51
nonnegative rational multipliers with the same beta; `exact_dual.py` prices
them using arbitrary-size integers over all fixed masks, common d values,
all three histogram universes, and all menu overlap corners. The minimum
scaled integer residual is zero. Numerical LP chooses bases only.

These certificates establish the optimum of this necessary-condition
template. They also supply a better universal five-player upper bound if
the necessary-row derivations and pricing implementation are independently
accepted. The parent and another team member are reviewing those obligations;
the directory does not claim external review or a general-player theorem.

Further necessary conditions already separate the first 60-atom point:
the sibling `round4_coupling` directory records exact joint cross-family
terminal-menu and pair-query cuts. The full SPE completion question is
strictly stronger than this template.

`cross_pair_pricing.py` is a new exploratory 717-row system. It adds all 160
cross-family pair-partition rows with source AB or AE; these retain
separability because their last-two background is p_fixed+t_i and optimal
membership t_i is shared across all families. Every batch of priced columns
was checked against the direct Fraction evaluator of all 717 rows.
`exact_primal_cross_pair.json` supplies a 61-atom rational point with W=1,
comparison coverage about 2.0421195368768834, and all 717 slacks nonnegative.
Thus even these extra rows do not establish half coverage. This point is
self-contained and was recovered from an intermediate 558-column numerical
state. The completed numerical 717-row optimum is about 2.042123288694712,
saved in `cg_cross_pair_final.json`; its optimum is not claimed exact here.

Reproduce the exact 557-row optimum from this directory by running
`python3 exact_primal.py 1 --final` and `python3 exact_dual.py 1`.
The latter performs full-universe arbitrary-size integer pricing.
`exact_cross_primal.py` recovers a rational 717-row feasible point from the
current `cg_cross_pair.json`; `separate_cross_point.py` applies the sibling
transport row evaluators to the delivered 61-atom point.
