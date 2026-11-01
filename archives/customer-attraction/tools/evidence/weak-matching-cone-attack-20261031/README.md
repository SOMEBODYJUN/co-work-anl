# Weak matching finite policy-cone attack evidence

This package preserves the three assigned source versions from `R-27557809587746c59216a46867c9eb07/weak_matching/` byte-for-byte and records the imported runtime dependencies needed to rerun the probe. The assigned sources are:

| source | bytes | SHA-256 |
|---|---:|---|
| `p6m4_seed104211.json` | 52831 | `3897844396918eb9bdc4253fe17579def2a4138da70ec569c23ed7bf5ea1ae5d` |
| `p7m5_seed104212.json` | 475501 | `7926d9e3a6dd7c4fd87754767f9f2d45b036fc631c38546d612ace289ed1b8dd` |
| `probe.py` | 7852 | `4bbd3280c6a2eda7ca461fa2cc713b1183b5c0fecae2c0295c5488dccd997f15` |

The original reports are finite floating-point searches over policy cones. `p6m4_seed104211.json` has 19 distinct cones and 57 successful LP records from 20 requested games; its best saved ratio is `1.0469067998756625` on the source-complete 52-client policy, with target `(0,1,4,5)`, actual root `(3,3,2,2)`, 372 LP rows, and 259 complete-history actions. The full query bridge threshold used by the script is `1+1/m=1.25` for `m=4`, so this saved value is below the requested separator. `p7m5_seed104212.json` has 98 distinct cones, 294 records from 100 requested games, 258 successful LPs and 36 infeasible records. Its best saved value is `1.0000000000000002` on game 40, mode `max_credible_payoff`, target `(2,3,4,5,6)`, actual root `(0,0,0,0,0)`, and 1260 LP rows; the full query threshold is `1.2` for `m=5`. Two duplicate policy keys were skipped in the p7 run, explaining 98 cones from 100 games.

`probe.py` constructs a fixed policy cone from a complete-history certificate, enumerates ordered histories, imposes nonnegative customer weights and a welfare normalization, then minimizes a matching-query objective with SciPy/HiGHS. It explicitly describes the result as evidence about finitely many policy cones. The JSON reports do not serialize all pre-LP child terminal terms or an exact rational dual certificate; positive floating values require integer recovery and full exact auditing before they have mathematical meaning.

The replay directory contains a one-game p6 and one-game p7 execution using the archived dependency copies (`exit 0`, empty stderr) plus `verify_weak_matching.py`. The checker verifies source hashes, report structure, record counts, best fields, complete-history action counts, and the one-game replay values. It reports `PASS` for those finite checks. The replays do not rerun the 20-game/100-game searches, and no universal weak-matching bridge, complete exact SPE theorem, integer-client reconstruction, or six-provider half result is claimed.

The p6 best instance has 52 unit clients represented by 22 customer types and welfare 47; the p7 best instance has 70 unit clients represented by 10 types. Those counts are metadata of the saved candidates, not a proof that the LP weights are realizable by the original integer-client model. All full-history, duplicate, empty-theme and arbitrary-tie quantifiers remain outside this finite diagnostic.
