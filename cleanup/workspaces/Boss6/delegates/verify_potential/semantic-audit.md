# Semantic audit: CA-HARMONIC-BRANCH-DELETION-OBSTRUCTION-v1

## Review boundary and provenance

The assigned source is stable ID `f3001ca6d7e2a9123d95`, the frozen file `research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/route1/verify_potential_branch_obstruction.py` (blob `d299a5b2c7f6db319ab997b6c3bf621dd0f109eb`, SHA-256 `5055f6dbc9f582231f23279213b8e9e1004fa53a408f3453e8002372643a7779`). I read the source, its JSON certificate, its Markdown explanation, the workspace README, cleanup startup/receipt instructions, and related route and archived objects. The source path is marked `in-progress` in checklist 0016; no archive target was changed during this audit.

The runtime package was copied read-only from `tools/evidence/cag-coupled-seats-and-upload-audits/replay-tree/customer_attraction`. The replay was staged under a path with the same five-parent layout expected by the source (`sys.path.insert(0, Path(__file__).resolve().parents[5])`). This avoids changing source code or silently resolving a different installed package. The command transcript and fingerprints are in `commands-and-results.md`.

## Mathematical input

The JSON instance has six common themes and three sequential unit players:

- (T_0={1,2}), (T_1={2}), (T_2={1,3}), (T_3={0,1}), (T_4={0,3}), (T_5={3}).
- Four unit customer types have interest signatures ({T_0,T_1}), ({T_0,T_2,T_3}), ({T_2,T_4,T_5}), and ({T_3,T_4}). All multiplicities are one.
- The certificate supplies an action at every ordered history of length 0, 1, or 2. There are (1+6+36=43) such histories, and each node has five unilateral alternatives, so 215 deviation comparisons.

For a terminal count vector (c), the source computes
[
\Phi(c)=\sum_x H_{\ell_x(c)},\qquad H_k=\sum_{j=1}^k\frac1j,
]
where (ell_x(c)) is the number of selected themes containing customer (x). It uses exact `Fraction` arithmetic. For a selected topic of the current player, the source deletes one count in that topic and checks the resulting potential difference against the topic payoff.

The source imports `ExactSPESolver` but does not use it. The certificate path is checked by `verify_certificate`, which recursively evaluates every complete continuation and checks the prescribed action against every alternative at each history. This is the right finite-tree condition for pure SPE in this one-action-per-player perfect-information model; no Markov/count-state consistency is assumed.

## Primary execution

The primary command exited with status 0 and returned `status: passed`:

- prescribed path: `(T1,T3,T4)` (indices `[1,3,4]`);
- forced root action `T0` path under the same complete certificate: `(T0,T0,T4)` (indices `[0,0,4]`);
- 43 history nodes and 215 unilateral deviations checked;
- root prescribed payoff and forced-`T0` payoff are both 1, hence the root deviation is a tie allowed by SPE;
- actual counts `[0,1,0,1,1,0]`; forced counts `[2,0,0,0,1,0]`;
- actual welfare 4 and exact optimum `OPT_3=4`;
- (Phi_{m actual}=9/2), (Phi_{T_0}=5), so the prescribed branch is lower by `-1/2`;
- deleting the root action gives potentials `7/2` and `4`, again a `-1/2` gap.

The customer-load vectors explain the arithmetic. The prescribed path has loads `(2,1,1,1)` and therefore (H_2+3=9/2). The forced path has loads `(1,2,2,1)` and therefore (2H_2+2=5). After removing the root action, the loads give (7/2) and 4. The actual and forced branches both cover all four customers, which is why this is not a low-welfare witness.

## Independent checks

`independent_audit.py` regenerated all 43 nonterminal histories and evaluated all 258 branches, counting the prescribed branch as well as the 215 deviations. It checked the exact marginal identity
[
u_i(z)=\Phi(z)-\Phi(z^{-i})
]
for every branch and found zero failures. It found four root alternatives with lower potential than the prescribed branch: alternatives `T0`, `T2`, `T3`, and `T4`, each tied with root payoff 1. The required `T0` branch is therefore not an artifact of selecting a single alternative. Its output is saved as `independent-audit-output.json`.

This independent replay still uses the frozen `customer_attraction` model/verifier for game semantics, while recomputing the harmonic potential and marginal differences directly. It is an implementation cross-check, not an external theorem or peer review.

## What the finite evidence establishes

1. The supplied complete ordered-history certificate is a valid pure SPE for this one finite common-catalog instance, under the exact model semantics used by `verify_certificate`.
2. Full-history SPE inequalities do not imply that the prescribed continuation maximizes terminal harmonic potential among current root actions. A utility tie can coexist with a strict potential loss.
3. The deletion term in the identity (u_i=\Phi-\Phi_{-i}) has a signed branch difference: here it is exactly `-1/2`, and dropping it from the SPE inequality gives a false branchwise potential comparison.
4. The object is reusable as a mechanism-boundary/route obstruction: any proof using pointwise (Phi(z_\sigma)\gePhi(z_A)) at every complete-history node is invalid on this witness.

## What it does not establish

- It does not refute Q-CAG-HALF. The witness has (W=OPT_3=4), so it satisfies the target half bound with room to spare.
- It does not prove a universal theorem about all catalogs, all player counts, all customer multiplicities, or all pure SPEs, and it does not show that every SPE in this instance has the same potential behavior.
- It does not rule out a different potential, a telescoping sum of signed deletion gaps, a cross-branch relay, or a proof that uses the `m`-theme cap directly.
- It does not certify arbitrary metadata in the JSON. The source ignores `raw["verification"]` and `raw["target_counts"]`; only the parsed certificate and recomputed strategy outcome are used. The verifier checks the certificate's own terminal count declaration against its root outcome.
- It does not independently prove the general customer-by-customer identity. The source evaluates the two selected branches, while the independent replay checks all 258 branches for this finite certificate. A general proof remains the one-line customer-level harmonic increment stated in the Markdown object.

## Relation to nearby objects

The source workspace README identifies this route as a common-catalog Q-CAG-HALF route. The related `complete_pair_incidence_lp_obstruction.md` is a different root incidence-LP stress test: it shows a one-deviation maximal-incidence budget cannot by itself exploit the `m`-theme optimum, but it supplies no SPE certificate. The corrected `cross_branch_welfare_relay_identity.md` retains old-player and deletion terms at non-root nodes; the present certificate gives concrete finite evidence that the deletion term can reverse potential order. The `route3/smoothness_bridge_obstruction.md` proves static `(1,1)` smoothness but separately shows why frozen-profile deviations cannot be substituted for true SPE continuations. These three pieces are complementary route/interface boundaries, not one combined counterexample.

The already archived `调和势链未来回应项--障碍.md` uses a different four-theme, three-player witness and a finite m=6 search. It records a future-response term that remains positive when selected source/replay IC slacks are zero. This six-theme certificate should remain separately provenance-tracked (or be added as a clearly labeled second witness), rather than silently replacing or duplicating that object.

## Recommendation

Recommend `retained` for the script, certificate JSON, and source Markdown as a unique executable finite obstruction. A concise archive object could be added at `archives/customer-attraction/state/障碍/完整历史强制分支调和势单调性障碍--障碍.md`, with the executable evidence under `archives/customer-attraction/tools/evidence/harmonic-branch-deletion-obstruction/`. The recommendation is recorded in `receipt-recommendation.json`; no target file was written by this delegate.
