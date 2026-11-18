# Independent obstacle line journal

- Identity: independent obstacle line, Boss3 six-agent original-problem RUN.
- RUN: n6-boss3-20261118; session_tag: boss3-20261118-live1.
- Repository: co-work-anl-boss3; expected branch rebuild/research-v2; starting HEAD e0b8e7d28c5164fbd5fd0ef689886c1279e380b7.
- Permitted mathematical input: only the original problem, definitions, and obstacles excerpts contained in research/runs/n6-boss3-20261118/packet-obstacle.json. Exact section-limited source excerpts only if explicitly routed there. No full packet, hyperedges, other Boss, other lines' notes, or complete archive.
- Permitted operational input: AGENTS.md and prompts/research-line-design.md.
- Task: independently investigate the exact six-person full-history pure SPE half-coverage problem, seeking either an original-model obstruction or reusable full-history local lemmas. Preserve all-history quantification, genuine continuations under one strategy, arbitrary tie breaking, and finite catalogues; do not claim a path or relaxed witness is an SPE counterexample.
- Write scope: this independent/ directory only. No git commit/push, no studio line/save, no registry or official mathematics edits.
- Starting state: initialized; no mathematical packet read yet; no external search or credentials accessed.

## Activity

- 2026-11-18: Initialized journal before mathematical reading. Next: read allowed operational instructions and packet-obstacle.json, then derive independently.

- Read only AGENTS.md, prompts/research-line-design.md, and packet-obstacle.json. The obstacle list is empty; no archive files opened.
- Derived exact continuation-set recursion preserving full-history SPE quantifiers and arbitrary ties; proof and scope saved in `full-history-recursion.md` §§1,3.
- Derived universal residual bound 169 W >= 49 OPT_6, below the half target; proof saved in §2. It identifies that arbitrary-successor guarantees alone are too weak.
- Implemented exact integer DP for six providers and <=8 catalogue labels in `exact_spe_search.cpp`; initial A=6 finite-instance search running. No result is promoted beyond its checked finite scope.

## First self-contained checkpoint

- `near-example.json` records the strongest of the 10000 sampled A=6 integer-atom instances (seed712046); its exact generation domain and first-best round819 are in the JSON provenance. No exhaustive claim is made.
- `export_spe_certificate.py` reconstructs a full-history pure strategy via the exact recursion. `near-example-strategy.csv` contains all9331 ordered decision histories. `verify_spe_certificate.py` does not use the DP: it recursively replays the one supplied strategy at all46656 terminal histories, checks all55986 deviations against actual child continuations, and separately computes exact OPT_6 over all terminal count vectors.
- `near-example-verification.json`: all-history SPE passed, W24, OPT6=32, ratio3/4, non-counterexample. Strategy SHA256608ad6ea5dd2225bca77354036f2e1184e0f6cd0fc6f2098e396afb5db0b1dfb. This is a finite certificate only.
- Recursion proof and weak universal bound169W>=49OPT6 are in `full-history-recursion.md` §§1-2; no half theorem is claimed.
- Binary moved under ignored `tmp/`; `.gitignore` contains `/tmp/`. Source and exact logs remain reviewable. Build command: `g++ -O3 -std=c++17 research/workspaces/n6-boss3-20261118/independent/exact_spe_search.cpp -o research/workspaces/n6-boss3-20261118/independent/tmp/exact_spe_search`; run arguments `6 10000 712046`.

## Local mechanism extracted from the strongest sample

- The sampled worst outcome repeats one coverage set six times. An independent argument now proves the sharp general bound6OPT6<=11W for EVERY such SPE outcome, using only genuine final-mover comparisons. Proof is in `single-support-sharp-bound.md`.
- Constructed a sharp original-model example with seven labels and66 unit clients: one36-client core label A; six labels each take a disjoint six-client core block and five private clients. Constant action A at EVERY history is a full pure SPE. The proof explicitly checks any arbitrary prefix via k prior non-A choices and q_j prior choices of each T_j; the prescribed-vs-deviation utility gap is sum_{l!=j}6/(6-k+q_l)-5/(q_j+1)>=0.
- Result: W36, OPT6=66, exact ratio6/11. This is NOT a half-coverage counterexample. It proves the uniform-realized-coverage local bound sharp and excludes all such paths from counterexample search.
- `tight_single_support.py`, `tight-single-support.json`, full strategy CSV, and exact independent replay output preserve reproduction. Next action: non-author review of recursion and sharp single-support lemma; then extend final-node weighted charges to exactly two distinct realized coverage sets. No additional packet/archive input was read.

- Exact sharp-example replay completed:19608 decision histories,117649 terminal histories,137256 actual-continuation deviation comparisons; all-history SPE=true, W36, OPT6=66, minimum scaled slack0. Strategy SHA256=1ad25728029576ce343f922f9c39ac4eeded3d9841908dcd89e579e3372f78e7. Output in `tight-single-support-verification.json`.
- Handoff state: this subround is self-contained and ready for Main save and non-author review. No git/studio/registry/formal-archive writes performed. No external search, credentials or disallowed mathematical input accessed. General half-coverage theorem remains open on this line; next mathematically distinct task is two realized coverage sets (or use this exact recursion for a targeted, explicitly bounded family).
