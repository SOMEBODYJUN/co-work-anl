# Credible construction attack — current checkpoint

2026-10-21. No genuine Q-CAG-HALF counterexample and no general half proof were obtained. Only this directory was written; no Git operation was performed by this researcher.

The substantive result is the short same-terminal exchange lemma and its conditional load-distortion perfect-matching certificate (including collision-free paths) in [common_terminal_exchange.md](common_terminal_exchange.md). They use two genuine comparisons from one full ordered-history SPE, with every terminal-equality and load condition stated explicitly. They imply a many-punisher extension of the existing 3/2 collision-free family cannot improve its asymptotic ratio if early and last punitive entrants return to the same final multiset and leave other groups unaffected. The obstruction survives arbitrary internal punitive rewards, overlap in a common reservoir, heterogeneous group sizes and any number of punishers. Root checked the original proof and suggested the general load-distortion version; a separate review is being prepared; no new shared claim status is implied.

Exact expanded-unit arithmetic for 14 literal cases is in `common_terminal_audit.py` and `common_terminal_audit.json`. This is an obstruction audit, not a full strategy certificate. The proposed t>2 actual path has an explicit profitable *last* deviation, so cannot have a full SPE certificate.

`collisionfree_joint.py`, `cf_m3p6.json`, `cf_m4p7_failed.json` preserve two low-information finite MILP attempts and their exact scope. The m3,p6 ratio-one endpoint has a complete action graph and was exact-verified at all ordered histories. The m4,p7 run produced no preserved candidate and its report failure is recorded candidly. No solver upper bounds are asserted.

Next: attack different continuation layouts breaking the same-terminal permutation, or show that the exchange graph admits a useful partial matching in a broader class. Do not infer a universal collision-free 3/2 bound: the perfect-matching condition is unproved for arbitrary SPEs and can fail.
