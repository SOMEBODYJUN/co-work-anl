# tree13: complete-tree terminal-budget attempt

2026-10-25. Scope: exactly five providers, arbitrary finite customers/catalog,
all complete ordered-history pure SPEs. **HALF5 remains OPEN.** This branch
has no target counterexample and no new unconditional welfare bound.

The only exact new diagnostic retained here is
[the root-source necessary-row relaxation](terminal_share_full_tree_attempt.md):
its all-atom feasible point shows that one root deviation to the actual last
theme, together with every conservative deviation among all named themes,
does not prove the proposed terminal aggregate budget. Both its actual and
source last-two tails fail the exact canonical M threshold. This is a
failure of that relaxation, not a failure of the aggregate budget or HALF5.

`root_source_relaxation_exact.json` has exact rational normalized rows,
integer-unit instances and explicit failed local tail checks;
`audit_root_source_relaxation.py` regenerates and verifies them. The
symbolic builder is `terminal_share_symbolic.py`.

A generated complete-strategy-cone QA (`attack_terminal_share.py`) did not
break the weaker terminal aggregate candidate. That candidate was already
OPEN in actor R-18e993ca519949aba29e030d3d7b15b3; no novelty or positive
all-input evidence is claimed. The stronger individual candidate is already
FALSE by that actor's seven-client complete SPE and was stopped as soon as
root restored it.

The teleportation source-drift idea and the exact query-center correction
were sent to exchange13 and are maintained only in
`../exchange/source_capacity_two_interface.md`, not duplicated here. Its
capacity/source/KKT compatibility and the Cov-to-signed-flow amount remain
unproved.
