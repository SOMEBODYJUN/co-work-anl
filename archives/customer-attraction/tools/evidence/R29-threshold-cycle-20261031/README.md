# R29 threshold cycle finite audit evidence

This package preserves the two assigned `new_representation` source versions byte-for-byte and records a direct replay plus an independent exact checker.

| file | source ID | bytes | SHA-256 |
|---|---|---:|---|
| `source/audit_opt_threshold_cycle.py` | `cb9df3377d9e31979119` | 2250 | `b223f6e4acfd2cf373ec6315b332bb8f8207fe6c44767ad55998bb24dd577845` |
| `source/opt_threshold_cycle_audit.json` | `835cbdc7c9f3c7efe65e` | 14921 | `29ebd343038c81a207199706702238789318c7c0b64c33b0cb8290aa8ddb8869` |

The source script was replayed in `replay/workdir` with `PYTHONDONTWRITEBYTECODE=1 python audit_opt_threshold_cycle.py`. It exited 0, wrote no stderr, printed `{"cases": 4, "menus": 42, "all_checks": true}`, and regenerated the frozen JSON byte-for-byte. The independent `replay/verify_threshold_cycle.py` re-enumerates the three-action coverage optimum for each `k=9,10,11,12`, recomputes every root menu and all last-player actions with `Fraction`, and returns `PASS` for 42 menus.

The exact result is an abstract three-player ring menu calculation: `OPT=9`, threshold `3/2`, root utility `4/3`, both prescribed tails `11/6`, and a disjoint action with utility `3` and gain `7/6`. The source explicitly says it has no SPE oracle. The evidence therefore records failure of the proposed root-tail threshold bridge, with no full ordered-history SPE construction, integer customer realization, or six-player half theorem.
