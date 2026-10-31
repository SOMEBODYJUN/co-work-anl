# Direct-cover weak-matching LP diagnostic comparison

- source ID: `72e45e29364108da001a`
- source path: `research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/lp_weak_matching.py`
- source SHA-256: `1dd36dfc20d6bceb04b07b312282da3b370be2424782647b9a675fb4c740a4fd`
- source size: 5104 B

The source is a diagnostic random-search program, not a theorem prover or production solver. It samples customer multiplicities on all nonempty subsets of k topics, optionally uses `ExactSPESolver` to choose a complete strategy certificate, builds true-deviation rows and coverage rows, and solves a finite LP with `scipy.optimize.linprog` for `match`, `strong_average`, or average-style bridges. A negative candidate is written only after a strategy certificate passes `verify_certificate` and then `check_weak_matching.evaluate`.

Compared with the archived direct-cover README and `弱匹配与分区查询的精确核验--计算`, this script is an exploratory finite cone search. It does not establish universal weak matching, weak/strong average, PFR-OPT-v1, or Q-CAG-HALF. It was not executed in this pass because it imports the canonical customer-attraction solver and auxiliary checker, and a random finite search would not strengthen the existing mathematical boundary. No result file is claimed.
