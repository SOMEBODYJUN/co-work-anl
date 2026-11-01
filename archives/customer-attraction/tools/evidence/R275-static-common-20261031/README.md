# R-275 static common finite LP evidence

This directory preserves the two assigned source versions and the two imported runtime dependencies byte-for-byte.

| file | source ID | bytes | SHA-256 |
|---|---|---:|---|
| `source/static_common_attack.py` | `6ba99015cb5ee1e1d5fb` | 1354 | `d707d5d70afac70e96420f6a58c542bd285c6afed6ab84e14a2f06846247b9fd` |
| `source/static_common_best.json` | `7fd962b12560d5e640b7` | 80604 | `b7d4fb878fd95ea812cef1ffdd16bb11245ba87eeabb7af0307262868c222914` |
| `source/cone_floor_attack.py` | `dbf018232df702a3cfaf` | 2986 | `af4f1f7f4e65a9c27d6b433e24dd1e3ff2cd7819cfd09dc140a580833d85ddb0` |
| `source/floor_scan.py` | `90578ba48285bc04f0c3` | 1817 | `ba406363e5a12959096613530441ae171df58ca9cd18a182cfc49d5dd1dbc66d` |

The full driver was run in a fresh copy:

```text
cd source
PYTHONDONTWRITEBYTECODE=1 python static_common_attack.py
```

It exited 0, wrote no stderr, printed three improving records and `DONE 0.19999999999999996`, and reproduced `static_common_best.json` byte-for-byte. The independent checker is:

```text
PYTHONDONTWRITEBYTECODE=1 python replay/verify_static_common.py
```

It checks the candidate's exact one-support objective (`1/5`), coverage normalization, policy history count and all source hashes. `serialization_policy_comparison.json` records that regenerating `Cone.policy` from the serialized LP weights changes 2797 of 2801 actions; this is expected because the original driver formed hidden child-terminal terms from the random pre-LP point and did not serialize them.

The evidence is a finite floating-point fixed-cone diagnostic. It contains no LP dual, Fraction Gamma certificate, integer-client reconstruction, universal SPE quantifier, or six-provider half theorem.
