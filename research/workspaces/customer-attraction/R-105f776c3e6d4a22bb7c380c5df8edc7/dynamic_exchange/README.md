# Dynamic exchange research checkpoint

2026-10-24. Task Q-CAG-HALF, arbitrary finite common catalogs and every full
ordered-history pure SPE. The main target remains **OPEN**. No git commit,
push, shared-file mutation, or external message was performed by this agent.

The substantive result is
[static_optimal_assignment_counterexample.md](static_optimal_assignment_counterexample.md):
a complete m=3, six-topic, 1953-unit-customer SPE disproves the exact seq242
static assignment bridge `exists optimal T, permutation pi: sum_i
u_i(T_pi(i),z_-i)<=W`. Unique optimum {1,2,5}, actual (0,3,4), W1735,
OPT1740, minimum assignment cost1736. This is **not** a half counterexample.

The raw frozen certificate is
[assignment_instance.json](assignment_instance.json) plus
[assignment_full_policy.json](assignment_full_policy.json). The author exact
audit [audit_assignment_witness.py](audit_assignment_witness.py) checks all
43 ordered histories, 258 action comparisons, all 56 terminal multisets, the
unique optimum, and all six static assignments. Its frozen report is
[assignment_exact_audit.json](assignment_exact_audit.json). Independent raw
audit was requested by the parent and is pending at the time of this note.

[assignment_witness.json](assignment_witness.json) is the small integer subset
potential source. Discovery and fixed-policy simplification scripts/outputs
remain separate; optimizer feasibility is not used as proof. The construction
uses exact uniform-bias cancellation on three distinct labels, based on the
[existing Möbius transform](../../../../current/customer_attraction/mobius_compiler.md).

The parent has been notified of the exact failure. Next useful work must use
true changing continuation branches or another global mechanism; do not
continue scanning this disproved static assignment bridge. The same-node ROW
net-gap candidate and direct all-player OPT/(2m) floor were identified as
existing open obligations, not new results. The stronger omitted-optimum
mass <=W target was discarded after the parent supplied the old 71-customer
counterexample. No independent fixed-cone negative scan was started.
