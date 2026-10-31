# Scope and source-boundary notes

The eight frozen source blobs are identified by `cleanup/inventory.jsonl` and their expected blob IDs, SHA-256 values, and sizes are copied into `manifest.json`. `GIT_NO_LAZY_FETCH=1 python3 co-work-anl/work.py clean show <id>` was run for each source; every command returned nonzero with `fatal: bad object <commit>:<path>` because this checkout lacks the promised blob. A normal lazy fetch was also unavailable because `browser-proxy:8889` was unreachable. No source bytes were invented.

Semantic review used the complete related source archive and state objects already present in the repository. Those objects state that the harmonic source family was read in full in the earlier source archive, and they preserve the model, policies, caveats, and exact finite checks. Fresh local replays are in `replay/harmonic_11/`, `replay/promoted_family/`, and `replay/family_related/`.

The joint collision-free artifacts are retained as finite exploratory MILP records. The preserved scope is m=3, q=6 with topic-subproblem intersection slices k=0,1,2 and 15-second limits; observed candidate ratios above one, timeout and floating solver states are not impossibility proofs. No m=4 expansion was run.

The promoted-family oracle was only a three-point historical check. The exact statement now relied on is the terminal-node calculation in `archives/customer-attraction/state/障碍/多个围堵块的目标终局末位障碍--障碍.md`: for t>2, a last C_i deviates from t to 2t−1 and a last D_r deviates to t/2+t−1, both strictly larger; for t=2 the D_r deviation is tied at 2 and the last C_i still fails. This excludes that prescribed family, not every collision-free route and not the general half target.
