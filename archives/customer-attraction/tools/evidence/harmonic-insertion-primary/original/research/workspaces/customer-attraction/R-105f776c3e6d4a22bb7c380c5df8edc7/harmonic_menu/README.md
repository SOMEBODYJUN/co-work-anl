# Harmonic/menu sensitivity exploration

2026-10-24. General Q-CAG-HALF work only; target remains OPEN.

`insertion_pool_and_dynamic_regret.md` derives a common-customer insertion
pool, a sufficient cross-leaf occupancy condition for transporting a
weighted IC collection across root deletion, and the all-input stability
bound `sum epsilon_j <= sum k_j-E_A(q) <= n K_b(A)-E_A(q)` for retaining
the same complete strategy after deleting one fixed root. It then shows, by an explicit
arbitrary-depth credible child family, that the original root's one-leaf
profit/externality cannot by itself bound summed adaptive deletion defects;
the n-dependent K bound is attained exactly.
This is a precise failed sensitivity candidate, not a welfare counterexample
or a general obstruction to proving half coverage. No new PEEL drift sign
or general positive welfare relation was obtained.

`audit_insertion_sensitivity.py` and its output independently compute all
ordered-history IC comparisons of the displayed child family for n<=5 using
exact rational arithmetic. The general proof is analytic in the note.

Next useful step would be a genuine cross-leaf occupancy invariant, or a
direct induction that never transports the unchanged child across deletion.
Do not repeat unstructured scans or treat fixed-terminal conservation as
the missing full-tree stability theorem.
