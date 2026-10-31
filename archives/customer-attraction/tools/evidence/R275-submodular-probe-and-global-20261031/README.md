# R275 submodular probe and random-root global walk

This package preserves three assigned source versions from `tree_coupling`:

| source ID | file | bytes | SHA-256 |
|---|---|---:|---|
| `2773e2344f8ba9d30ec7` | `global_submodular_walk_random_root.json` | 332492 | `2b314710b7879725395e2f602cb355433969b3ec876d141ab488111d6b67e541` |
| `aaa22bcdc88fa1b0d6ab` | `submodular_probe.json` | 53366 | `ace97dd7268ba15386f58ce8ac89a6aa7e6794a24533b1f1cbfb8994a07c1f1d` |
| `f4d58c08869c30c45c41` | `submodular_probe.py` | 7412 | `fdbdb171f795cb748eb0a20ea4da3e4f2022c23fcdddfc8b5193928888f8240f` |

The global source is a frozen 72-round, 45-cone, five-player/seven-topic walk with `global_submodular=true`, random roots, `nearest` continuations, 19,607 ordered comparisons per round, and best abstract exact ratio `9/5`. It explicitly leaves customer realizability unclaimed and `Q_CAG_HALF` open. The same archived walk implementation was exercised with identical parameters: a 10-round test completed with empty stderr; a longer run hit the session runtime boundary before 72 rounds, so the frozen 72-round JSON remains the authoritative source record and no full replay claim is made.

The probe source was replayed fully with `--samples 12 --seed 749811`; it exited 0 with empty stderr. The regenerated JSON has the same 12 records and complete best witness as the frozen JSON; only elapsed time differs. The best exact value is `9/5`, and every recorded exact value is nonnegative. `verification.json` records these checks.

Both source families are abstract common monotone-submodular moment relaxations. They do not encode nonnegative unit-customer multiplicities, so their positive finite ratios cannot be read as customer welfare ratios or a six-player theorem. The evidence keeps the runtime boundary and all open quantifiers explicit.
