# Boss3 sparse and shared-menu audit replay (2026-11-01)

This directory preserves the four clean-exported audit programs and the local replay outputs. The two sparse programs were run in a temporary source-shaped tree with their frozen JSON inputs; the shared-menu and strong-chord programs were run against the preserved replay packages under `tools/evidence` (the package files were only staged in the temporary runner, not copied into the result tree).

- `sparse_bad_long_cycles.run.json`: exact Fraction audit for n = 1, 2, 3, 10, 30, 100 at r = 7/4; it checks the closed response ring and a finite best-factor certificate. It does not prove the universal n or all-r < rho statements.
- `sparse_high_reach.run.json`: exact Fraction replay of the sharp lower input, a tie negative control, a six-action long cycle, and 400 seeded random instances. Counts include `pure_bad=2`, `mixed_bad=0`, `balanced=25`, `ties=272`, `zero_reach=31`; this is attack evidence only.
- `strong_chord_iff.run.txt`: 2,500 exact local checks. It found one `PUREFAIL` witness (`r=811/1000`, common weights `19521/100000, 28679/100000`) where a local feasible continuation exists but no pure continuation passes the tested condition; no `TWOFAIL` was found. This is a finite obstruction to a pure/two-mixer shortcut, not a failure of the complete strong-chord theorem.
- `shared_menu.run.json`: 10,206 local exact support cases and 1,771 exhaustive three-client multisets; maximum factor in that finite family was `4/3`. The forced-three-mixer witness has reaches `(100,99)`, common weights `(20,20,20)`, pure loads `(60,79)`, two-mixer loads `(79,60)`, and a three-mixer load `(277/4,279/4)` with probabilities `(39/80,39/80,39/80)`.

All outputs are finite exact evidence. They do not upgrade the existing sparse rho proof or shared-catalog phi proof, and they do not transfer to the six-provider CAG-HALF model.
