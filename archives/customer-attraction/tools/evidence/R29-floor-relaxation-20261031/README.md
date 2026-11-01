# R29 robust-floor relaxation audit

This package preserves the two assigned `security_bridge` source versions and a direct replay plus an independent exact checker.

| source ID | file | bytes | SHA-256 |
|---|---|---:|---|
| `8e5b63c67ac400200ec6` | `source/audit_floor_relaxation.py` | 3441 | `96d3898ddf5c3b07f1905024165e691639e24b3735227df37251c1ca3706aacc` |
| `0e33010d28fc24721425` | `source/floor_relaxation_audit.json` | 750 | `652e6087a0a3110c71c961afa6036b2d8d78868165a10b06471fd75bd8cae0cc` |

`audit_floor_relaxation.py` was run with Python's exact `Fraction` arithmetic. It exited 0, wrote no stderr, and regenerated the frozen JSON byte-for-byte. `verify_floor_relaxation.py` independently reruns the source function and checks every reported value, returning `PASS` with no stderr.

The exact object has four players and five themes. It tests terminal counts `(0,0,0,1)`, payoffs `(5/4,5/4,5/4,9/4)`, welfare `6`, robust necessary floors `(1,1,5/4,9/4)`, all 70 static four-slot multisets, and a uniform static-query lower bound `8/5`. The resulting extra-one aggregate gap is `2/5`. At history `(0,0)`, forcing current action `2` makes every true last best reply one of `[1,3,4]`; the deviating player's payoff is `7/3`, producing a strict penultimate IC gain `13/12` over `5/4`.

The terminal therefore satisfies necessary floor inequalities and a static security calculation while failing true sequential rationality. It is a discarded relaxation diagnostic and does not provide a complete SPE, an integer customer half counterexample, or a six-player theorem.
