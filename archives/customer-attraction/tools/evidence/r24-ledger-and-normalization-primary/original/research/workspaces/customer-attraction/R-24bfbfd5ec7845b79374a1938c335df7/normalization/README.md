# Tail normalization obstruction checkpoint

2026-10-21; researcher representation. General Q-CAG-HALF remains OPEN.

- `candidate.md` states the rejected auxiliary minimum-payoff tail-normalization candidate separately from the proof.
- `tail_minimum_obstruction.md` gives G1, a general obstruction from the existing last-two theta floor, and E1, an exact 36-unit-customer relocation gap: minimum SPE welfare 34 versus minimum tail-minimum SPE welfare 36. No new general welfare bound is claimed.
- `audit_tail_minimum.py` independently expands the 36 clients, checks both complete policies at every ordered node, theta at every last prefix, all terminal pattern values, and all ordered SPE outcomes. It imports neither the canonical model nor solver. Output is `audit_tail_minimum.json`.

Independent same-session definition-level audit passed: 43 nodes and 258 action comparisons for each policy, theta over 36 prefixes, 216 terminal paths, 48 ordered SPE paths, and exactly 12 tail-minimum SPE paths. General obstruction proof is analytic; these finite checks support only E1.

Next question: a softer relocation must explicitly pay positive welfare increase; the exact two-unit gap forbids welfare-preserving normalization even when changing the whole complete strategy. No compensated relocation theorem is currently claimed. No Git operation or external message was performed.
