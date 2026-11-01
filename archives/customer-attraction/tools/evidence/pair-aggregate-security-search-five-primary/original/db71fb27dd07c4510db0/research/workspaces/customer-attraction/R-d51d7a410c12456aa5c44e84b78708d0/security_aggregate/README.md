# Boss8 aggregate-security checkpoint, 2026-10-21

Input: general finite common catalog, unit customers, arbitrary number of unit
providers, full ordered-history pure SPE. The general half-coverage claim and
both strong/weak aggregate mixed-security bridges remain OPEN here. No shared
maps or git state are modified.

Read before exploration: root AGENTS/README, current model/math map,
FAILED_ROUTES, oblivious_security, security_chain_and_local_boundary,
security_cone_duality, global_security_budget_boundaries, and previous
R-642.../security_aggregate checkpoints. In particular, actual-profile deletion
support and one-step security-chain nonnegativity are already false.

## Two-step chain candidate (unproved)

For a real path with r remaining providers at a given node, let V be the static
mixed security at that node and V++ the static security after the next two real
actions, with r-2 providers left. Candidate:

    u_i + u_(i+1) + (r-2) V++ >= r V.                 (PAIR)

If PAIR holds for every legal background and every full SPE with r>=3, then
sum over disjoint consecutive pairs. The middle security terms telescope;
a final singleton has utility equal to its terminal security, and a final pair
has aggregate at least twice its security by the already valid last-two floor.
Thus the strong global bridge W>=m v_m follows. This is a sufficient new local
condition, not a proven result; it may be too strong despite allowing the
already-known negative individual D_i.

The previous workspace's 1500 random five-provider/seven-theme root screens
reported no negative PAIR (minimum zero). They are finite numerical evidence.

## Current cone separation

`pair_cone_probe.py` is copied from the previous workspace with its missing
source-directory import fixed. It tests the saved full five-provider,
seven-theme policy cones in `new_policy_security_cones.json.gz`. For fixed
root query p and tail dual background Q, a linear program over the complete
nonnegative customer-mass cone minimizes

    u_1+u_2 + 3 max_a E_Q f_tail(a) - 5 min_B E_p f_root(B).

The fixed-p root term is a lower bound on the root security and the fixed-Q
tail term an upper bound on tail security, so a strict negative exact witness
would refute PAIR. Re-optimizing p and Q, plus fresh cone-extreme restarts,
can discover candidates but cannot certify that PAIR holds. The full policy
Gamma retains all real ordered-history incentives (deduplicating identical
coefficient rows only). Numerical candidates need exact reconstruction and
independent checking before any result claim.

Run command:

    python3 research/workspaces/customer-attraction/R-d51d7a410c12456aa5c44e84b78708d0/security_aggregate/pair_cone_probe.py --iterations 100 --output research/workspaces/customer-attraction/R-d51d7a410c12456aa5c44e84b78708d0/security_aggregate/pair_cone_output.json

At this checkpoint the process was still running; the only reported incumbent
was floating gap 1.11e-16 (numerical zero), first policy, first iteration.
No new theorem or counterexample has been obtained.
