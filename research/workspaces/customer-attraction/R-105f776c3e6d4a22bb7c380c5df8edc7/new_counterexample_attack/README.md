# Counterexample attack: an analytic switch that fails original reachability

2026-10-24. Negative analysis of one proposed deletion-repair attack. No new Q-CAG-HALF counterexample, no new half range, and no claimed full-SPE counterexample to a repair theorem.

The attempted primitive makes the surviving virtual strategy have zero regret at every actual node, although its actual leaf has no complete SPE realization. Its proposed deleted controller is not rational in the original game: a continuation-independent argument gives it a strict profitable deviation in every credible continuation. Adding an earlier disjoint bank prefix does not remove this contradiction. See [the exact analysis](switch_reachability_negative.md).

The prefix-defect compiler in `R-65d0f88edf3849b39ca5eb79760e970b/credible_attack/prefix_credible_exit_compiler.md` was checked as an attack interface. No input satisfying its required strict inequality `OPT-2W>(2j+1)Delta` was obtained. The primitive below cannot supply one: its original and surviving actual covers already equal the entire catalogue union.

No discovery scan or numerical optimizer was used. This is a stopped construction attempt, not evidence for the universal half conjecture or for a general deletion-repair theorem.
