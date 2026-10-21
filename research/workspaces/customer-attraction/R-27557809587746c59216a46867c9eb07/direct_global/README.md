# Direct global / common-query regret exploration

Exact target **Q-CAG-HALF** remains **OPEN**. No general proof or counterexample to half coverage was found in this workspace.

The substantive finite result is `common_query_regret_counterexample.md`: a nine-topic,30-unit-client,six-provider complete pure SPE disproves the newly proposed auxiliary common-query bound F(T)<=W+min_i u_i. Root path P0,P1,P2,P3,A,B has W25,OPT26,minimum utility4,and F(T)=30. It does not disprove the refined fractional bridge or aggregate security bridge.

`padded_residual_m6_dag.json` is the compact full-history SPE witness (5,440 count-and-target nodes). `padded_residual_dag.py` constructs it with the canonical exact recursion. The independent definition-level audit and frozen report are in the sibling `security_global` workspace, named in the note. `padded_residual_uniform_floor.md` gives a standalone analytic universal four-payoff floor for this particular padded family, with a complete all-history induction; this is separate from the finite path-existence claim.

Other Python/JSON files are exploratory floating-point policy-cone diagnostics or earlier larger gadget experiments. No successful LP run, finite no-separator scan, or saved floating vector is a universal theorem. The earlier `multigadget_m*.json` files are discovery artifacts; use the independently audited padded residual m6 DAG as the bridge-counterexample evidence. Some early candidate metadata were corrected during exploration; the counterexample note and audited DAG give the final numbers.

Next useful steps: independently attack the family-specific four-payoff floor; seek an analytic arbitrary-k SPE completion for the padded target path only if useful; return to a different global payment mechanism, since the common-query minimum-utility payment is now false.
