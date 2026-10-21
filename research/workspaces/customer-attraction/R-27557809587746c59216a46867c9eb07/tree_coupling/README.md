# Tree coupling research backup

General Q-CAG-HALF remains OPEN. Work is confined to this directory; no shared
canonical claim or external publication status was changed.

- [common_shapley_coupling.md](common_shapley_coupling.md): exact positive
  marginal/common signed representation; local efficiency + balanced
  contributions characterization; a new conservation-strengthened 9/4
  template obstruction; a 15/7 obstruction retaining all two-topic coupling;
  seven precisely scoped rational coupling-layer optima.
- [coupling_probe.py](coupling_probe.py): finite floating candidate generator
  with Fraction primal/dual acceptance; all full-history deviations retained.
- [coupling_layers.json](coupling_layers.json): complete rational primal and
  dual witnesses for one 3-provider, 6-topic strategy and T={1,2,4}.
- [verify_coupling.py](verify_coupling.py): optimizer-free Fraction verifier,
  rebuilding the payoff/moment map by independent Boolean inversion.
- [submodular_probe.py](submodular_probe.py): finite attack on the stronger
  common-monotone-submodular-moment conjecture, sampling complete policies
  from sums of budget-additive set functions; no genuine-customer realization
  is claimed for its optimized moments.
- [submodular_dilution_coupling.md](submodular_dilution_coupling.md): general
  lemma TC-DIL-1 by exponential-clock coupling: sharp same-topic dilution
  is automatic for every nonnegative decreasing Shapley marginal, including
  monotone submodular truncated coverage moments. Root analytically accepted
  the mechanism; full-text review pending.
- [dilution_marginal_probe.py](dilution_marginal_probe.py) and its JSON output:
  a separate finite 418-orbit diagnostic, not the proof of that general fact.

Next positive target: attack the explicitly conjectural full-tree/common
monotone-submodular-moment half statement, or construct a global nonnegative
dual using the local Shapley coupling identities. Conservation and sharp
same-topic dilution alone are now exactly ruled out even together.
