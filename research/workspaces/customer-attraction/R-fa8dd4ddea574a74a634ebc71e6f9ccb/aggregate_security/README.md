# Boss9 aggregate security checkpoint (2026-10-21)

Task: Q-CAG-HALF under the exact current model: any finite common catalog, unit customers and providers, all ordered-history pure SPE, arbitrary historical ties. Strong/weak aggregate mixed security remain OPEN here. No git, credentials, or shared-file edits.

Read the current model/state/failed routes and the exact safety/debt interfaces. Prior finite probes of the stronger first-two candidate `u1+u2 >= 2 v_r(b)` did not find a counterexample; they do not prove it. This candidate implies the global strong safety bridge by grouping adjacent real players and using background embedding. The earlier PAIR telescope is weaker and also open.

## Current independent attack

`pair_full_milp.py` searches the entire three-player ordered-history policy space for each fixed query distribution and fixed equality pattern of the root outcome. It keeps all nonempty customer-interest types. Binary action selectors specify every ordered-history node; continuous `u[h,a]` record terminal payoff of theme a along the selected continuation, and leaf expressions are the exact reciprocal-load rows. Every SPE comparison is enforced using big-M. Normalization is actual first-two sum=1. A hypothetical positive `2 min_B E_p u - 1` witness would refute the first-two candidate but not automatically aggregate safety or half coverage.

Justification of finite big-M: root utility <=1; deviating to any topic always guarantees its size/3, so each theme has mass <=3. Thus every continuation payoff is in [0,3], and each equality/optimality difference is in [-3,3]. A total customer-mass bound 3k follows by assigning every nonempty interest type to one contained theme. No all-interest type is removed.

This is floating discovery only. Any positive witness must be rationally recovered and every historical deviation independently checked. Floating solver bounds and finite absence of witnesses are not proofs.

Current run: k=6, path=(0,1,2), p uniform, 45 second time limit. Results will be saved in `pair_milp_k6_p012.json`. Next: inspect the witness or run other equality patterns, then seek a direct structural proof or precise failure mechanism rather than indefinitely expand finite searches.
