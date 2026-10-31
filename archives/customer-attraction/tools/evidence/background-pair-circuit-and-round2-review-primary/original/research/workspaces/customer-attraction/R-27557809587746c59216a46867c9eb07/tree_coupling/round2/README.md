# Round2 global half work

General Q-CAG-HALF remains OPEN. No round2 global proof or stronger-class
counterexample has yet been obtained.

- `pair_scope_correction.md`, `complete_pair_v2.py`,
  `complete_pair_v2.json`, `verify_complete_pair_v2.py`: fatal scope correction
  to round1's 15/7 layer. Complete pair coupling actually gives exact2 on
  that strategy/comparison. Optimizer-free check passed all2778 inequalities,
  61equalities,126dual coordinates, and90direct pair-payoff reconstructions.
- `full_history_walk.py`: adjacent-cone attack using the canonical set-valued
  SPE recursion with an abstract common-Shapley payoff table. Nonminimal
  credible offpath continuations are allowed; every accepted policy is
  checked at every ordered history. `--global-submodular` imposes a genuine
  global set function, not merely truncated local constraints. This is an
  exploratory stronger-class search, not a nonnegative-customer realization.
- `full_history_walk.json`: initial random-minimal continuation search;
  `full_history_walk_nearest.json`: nonminimal nearest-credible walk reaches2
  in the truncated class. That exact2 mechanism is already covered by Boss6's
  `R-acd974.../round3_moments/local_positive_boundary.md`; no novelty claimed.
- `global_submodular_walk*.json`: ongoing global-submodular searches; finite
  no-counterexample outputs are not global bounds.
- `prefix_ghost_rent_budget_boundary.md`: explicit legitimate two-topic SPE
  showing an unweighted sum of prefix ghost-rent errors exceeds root coverage.
  This only refutes the written naive reserve, not a valid weighted circuit
  transport or the general half statement.

Next substantive target remains a global nonnegative budget, or a certified
counterexample in the genuinely global monotone-submodular stronger class.
