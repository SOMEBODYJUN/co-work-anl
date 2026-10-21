# Boss7 aggregate-security checkpoint, 2026-10-21

Scope: general common finite catalog, unit customers/providers, all ordered-history pure SPE, arbitrary historical ties. The main half-coverage claim and strong/weak aggregate static-security bridges remain OPEN here. No shared files, git state, external service, or messages outside this team were modified.

## Exact new boundary

Read `strong_iid_failure.md` first. The previously known eight-client SPE/CCE counterexample also disproves **strong iid payment W≥Z₃**, where Z₃ is specifically the expected coverage at a maximizer of the concave harmonic iid potential. The iid maximizer is uniquely

    q=(0,1−2t,t,t), t=(sqrt669−23)/14,
    Z₃=(4344−156sqrt669)/49≈6.307237698167356 > W=6.

The proof verifies concavity, global KKT sufficiency, uniqueness and exact strict signs; it does not label an arbitrary symmetric mixed Nash as the designated Z₃. `verify_strong_iid_failure.py` is self-contained: expanded unit customers; all21 SPE nodes and84 deviations; exact rational arithmetic in Q(t); independent coverage formula and matched primal/dual v₃=44/23. `strong_iid_failure_verified_v2.json` is the latest frozen report; `strong_iid_failure_exact.json` preserves the initial same-value report. This is a new implication/value calculation on an existing input, not a new input instance. Awaiting parent/independent review.

The weak iid bridge survives this example: (5/6)Z₃<6; strong aggregate static security survives: 3v₃=132/23<6. The main half claim also survives: OPT₃=8.

## Search checkpoints (numerical, not theorems)

- `probe.py`: fixed complete policy Γ cones; all static opponent backgrounds; alternating fixed-p LP/customer mass and exact finite-game security LP. Completed135 random cones at (players,labels)=(3,6),(4,6),(5,7),(6,7), maximum observed m*v/W=1. The named-instance loop had a string-seed bug and skipped those six entries on this run; it is fixed in the script, not counted here. `best.json` is merely a numerical cone point, not a counterexample.
- `leaf_support_probe.py`: allow Q to use any background obtained by deleting any player from a terminal leaf with at most one deviation relative to σ, then arbitrary mixing. This is wider than both already-failed actual-terminal deletion support and root-reply-menu support. Completed six named inputs plus130 random complete policy cones, maximum restricted m*v/W=1.
- `random_policy_probe.py`: same one-deviation-leaf support,1200 completely random full formal policies at (3,4),(3,5),(4,4),(4,5),(5,5). Every formal cone contains the all-interest customer ray. Maximum numerical restricted m*v/W=1. Alternation over p is not exhaustive global optimization.
- `prefix_pair_probe.py`: exact set-valued SPE outcomes and ordered-prefix admissibility, numerical static-security LP. Completed1000 random instances at (3,6),(4,6),(5,7),(6,7). The stronger candidate u₁+u₂≥2v_m had minimum observed ratio1; no proof.
- `pair_cone_probe.py`: full Γ cones, same first-two-payment candidate; completed320 random cones at (3,6),(4,6),(5,7),(6,7), max 2v/(u₁+u₂)=1. Not a theorem.
- `structured_pair_probe.py`: complete formal policies attempting two or more sacrificed early groups, followed by same-group concentration. Completed18 full formal policies at (players,labels)=(4,6),(5,9),(5,8), five q/p starts per policy; maximum 2v/(u₁+u₂)=1; no positive witness.
- `weak_iid_probe.py`: root harmonic-potential KKT rows plus full Γ, fixed root q, optimize Z/W. Completed640 random complete policy cones /1920 fixed-q LPs; maximum reported Z/W=1.0239989866135253 at m=3, weak ratio=.8533324888446044, far below a weak-bridge violation. Numerical only; exact reconstruction required for any new claim.
- `extract_leaf_dual.py` / `one_leaf_dual.json`: one sparse numerical coefficientwise certificate in an arbitrary full policy cone. λ can use deeper off-path nodes even when Q support is only one-deviation-leaf deletions. This is an interface illustration only, not a universal flow construction.

## Open candidates and next obligations

1. The one-deviation-leaf support conjecture: for every actual SPE, does some Q on those deletions satisfy every pure query payoff≤W/m? Static safety duality makes this sufficient for the strong aggregate bridge, but no proof is provided; all-p/whole-cone scope is not exhausted by the experiments.
2. A stronger local pair candidate is: for every legal background with r≥2 remaining players and every full SPE, its first two players receive at least2v_r(background). If true, apply it to disjoint adjacent pairs along the actual path; background embedding makes each local v at least the root v, and any last singleton gets at least the root v. This would prove W≥m v_m. It is stronger than the older open PAIR chain condition u_i+u_(i+1)+(r−2)V_(i+2)≥rV_i and is not established here.
3. Continue weak iid/full-tree static Q construction; do not reuse strong iid W≥Z after the eight-client boundary. Avoid the already-failed individual-security, all-p decorrelation, static-CCE welfare, pure-static-PNE, and actual-deletion-only bridges.
