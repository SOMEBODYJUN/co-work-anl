# Round 4 direct-general branch

Q-CAG-HALF remains OPEN. No general proof or true SPE counterexample was found.
All files stay in this personal branch directory; no shared files or commits
were changed by this agent.

- `hybrid_truncation_obstruction.md`: self-contained arbitrary-player failure
  of combining every exact actual-path comparison with every true terminal-k
  history. Ratio is unbounded for fixed k. The first missing off-path row is
  explicit. Includes relation to the existing bounded-tail and fixed-rank
  obstructions, without novelty claims.
- `audit_hybrid_obstruction.py`, `hybrid_obstruction_audit.json`: exact literal
  strategy verification, including m=10,k=2 with ratio2800/1321 and exhaustive
  smaller terminal subgames. Finite checks are not the source of the theorem.
- `terminal_transport_probe.py`, `probe_m5.json` through `probe_m8.json`:
  floating-LP exploration using exact-prefix clone floors, terminal menu G,
  and all strong actual/optimal pair-envelope aggregates. Relaxation optima
  exceed two. These are numerical relaxation records only, not SPEs or exact
  optimality certificates; the analytic obstruction supersedes them.

Next: a positive proof needs intermediate off-path credibility across
unbounded depths. Increasing only the final-two pair/query closure cannot
repair the explicitly retained row system above.
