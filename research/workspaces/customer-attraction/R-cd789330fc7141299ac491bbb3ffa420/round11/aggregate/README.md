# Round 11 aggregate checkpoint

Original Q-CAG-HALF, true security aggregate, fractional aggregate and AFC remain OPEN. No new unconditional welfare bound or original target counterexample.

- `shared_load_components_and_exact_sign_boundary.md`: shared-load relaxation of AFC, exact positive variance credit, universal pure-query payment, independently checked Bregman/KKT balance, and exact rejection only of the stronger C<=0 helper on the already proved insurance family. Correct mixed payment C<=D+sum IC remains OPEN. Root's companion draft is `../parent/shared_load_bregman_working.md`.
- `insurance_shared_covariance_exact.py` / `insurance_shared_covariance_m6_exact.json`: no numerical optimizer; exact rational q/KKT and balance for the named auxiliary sign. Full-history SPE theorem is inherited from peer's all-m proof, not newly audited here.
- `insurance_shared_saddle_exact.py` / `insurance_shared_saddle_m6_exact.json`: strengthened exact rejection of C<=0 at every global active-query saddle of this inherited game. The minimax load is unique and every optimal query has nonanchor support, on which each row's C is constant. Thus favorable choice of optimal query and preserving row/query transport cannot repair this stronger sign. Independently verified by matching11, including the uniqueness/complementarity argument; see its `insurance_saddle_independent_review.md`. The correct balance still pays comfortably.
- `extra_fractional_local_plateau.md` / `check_extra_fractional_plateau.py` / JSON: old PB fractional plateau extends directly to extra indexing and refutes local extra supersolution. Actual aggregate of that old source still pays its fractional bound. This is not a new game or welfare progress.
- `check_shared_load_old36.py` / JSON: earlier named C<=0 diagnostic; no separation, rational q feasible, floating optimality uncertified. Not evidence for general sign or SHARED.
- `insurance_shared_covariance_probe.py` / floating m6 JSON: discovery only; exact result supersedes it.

Next mathematical obligation is a full-history mechanism for C<=D+sum IC at the shared convex optimizer, or an alternative direct payment of OPT-W. Do not retry C<=0, local extra delta induction, old actual-load banks, or treat these exact interfaces as paid general money. All writes confined to this branch; no git/work.py calls.
