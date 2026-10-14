# A six-resource integer quadratic game

## WC-R1-INTEGER-TRIAD v1

- **Exact statement / conclusion.** The explicit game below has instance-optimal pure-equilibrium approximation factor exactly `286/267`: it has no α-PNE for every real `1≤α<286/267`, and has a `286/267`-PNE. Consequently `a_*(2)≥286/267` in MODEL; the same game belongs to G_d for each d≥2.
- **Objects / domain / quantifiers.** Three players, weights `(16,2,5)`, two actions per player, six resources, polynomial costs of degrees one and two with positive integer coefficients. All pure profiles and all unilateral deviations are covered.
- **Assumptions / definitions / scope.** Costs are the unweighted sum of resource latency values, with deviated loads recomputed as in MODEL.md. This is one fixed game. It is not an unbounded-in-d lower family.
- **Dependencies.** MODEL.md and the literal resource construction below. No external theorem is needed for this finite proof.
- **Evidence.** Complete cost table; exact independent resource-load implementation in `verify.py` and frozen `verification.json`; independent reconstruction is recorded in `../../../toolbox/R1/resource_cone/review.md` when available.
- **Counterevidence / objections.** None to the finite cost table after exact replay. Literature priority and the global best known degree-two lower bound have not been exhaustively audited. A comparison with the specific source equation (3) is a separate claim.
- **Status.** Exact finite construction and complete proof, internal review tracked separately. Truth: explicit certificate. Value: compact reusable non-symmetric weight triad. Novelty: unverified. Mechanism: a directed cycle in the complement quotient of the action cube. Ambition: local result; WC-TARGET v1 remains open.

## Construction

An integer mask entry `0` means absent from both actions, `1` means present only in action zero, `2` only in action one. For each row introduce the indicated resource and a second resource obtained by swapping entries 1 and 2, with the same cost. A player's action consists of exactly the resources whose mask permits that action.

| Mask | Cost of each resource in the pair |
| --- | --- |
| `(0,1,1)` / `(0,2,2)` | `13x²` |
| `(1,1,2)` / `(2,2,1)` | `59x` |
| `(1,2,1)` / `(2,1,2)` | `2x²` |

All six resources have distinct identities. All weights are positive, each strategy is nonempty, and the model has no player-specific costs or resource-dependent weights.

## Complete finite proof

Write s=(s₀,s₁,s₂). A simultaneous complement of all actions interchanges resources within pairs and preserves every player's current and deviated costs. Thus four rows represent all eight profiles. The following pairs give `(current cost, cost after flipping one's action)` separately for each player.

| Profile | Player 0 | Player 1 | Player 2 | Largest improvement ratio |
| --- | --- | --- | --- | --- |
| `000` | `(1944,1887)` | `(1707,1523)` | `(1814,1780)` | `1707/1523` |
| `001` | `(1869,2002)` | `(1507,1403)` | `(1780,1814)` | `1507/1403` |
| `010` | `(2002,1869)` | `(1523,1707)` | `(1796,1926)` | `286/267` |
| `011` | `(1887,1944)` | `(1403,1507)` | `(1926,1796)` | `963/898` |

Direct integer cross multiplication gives that the smallest of the four displayed largest ratios is `286/267`. Every α below it has a strict improving deviation in each profile. At α=`286/267`, profile `010` and its complement `101` satisfy every player's weak inequality, including player 0's equality. This proves the exact instance threshold, including the endpoint.

The improvement cycle in the quotient is `000 → 010 → 001 → 000`; `011` has its own exit to the cycle. The table, rather than the existence of a cycle alone, proves nonexistence over the full state space.

## Exact replay and comparison boundary

Run from the repository root:

```sh
python3 research/weighted_congestion_frontier/assets/R1/integer_triad/verify.py
```

Standard-library Fraction arithmetic reconstructs resource membership, loads, all eight profiles and all 24 deviations, confirms the endpoint profiles and complement symmetry, and exercises zero-cost, empty-action, constant-cost and common-membership conventions. No random seed, tolerance, truncation or floating point enters the certificate.

The independent source-envelope proof concerns only arXiv:2002.07466v3, Theorem 1, equation (3), not the entire class G₂. The reviewed algebraic certificate gives `α_source(2)≤19/18`, and `286/267−19/18=25/1602>0` gives a strict comparison to that certified ceiling; it does not assert a new globally best lower bound, and does not constitute the requested infinite-family breakthrough.

## Provenance and continuation

The main R1 process reconstructed this candidate using a complement-paired membership-cone search after the previous local workspace had disappeared. Floating MILP selected a support; small integer coefficients were then chosen and all mathematical assertions rebuilt from the game itself. The verifier and proof are the persistent mathematical assets; an unpushed historical decimal result is not used as evidence.

For growth, adding more copies of three-player resources cannot yield an unbounded factor if every resource remains usable by at most three players; see WC-R1-RESOURCE-SUPPORT v1 in `../cyclic_layers/resource_support.md`. The next useful test must allow resource user support to grow, or establish a different general existence mechanism.
