# Exact six-player all-big SPE family (nonviolating)

**Status:** exact full-history pure-SPE certificate; this is a lower-bound witness with (OPT/W=11/6), not a Q-CAG-HALF counterexample.

There are six providers and six common topics:

- (B=\{q_1,\ldots,q_6\}),
- five singleton topics (\{q_7\},\ldots,\{q_{11}\}).

The strategy chooses (B) at every ordered history. At a node with (k) prior selections of (B) and (r) providers remaining (including the current provider), choosing (B) gives (6/(k+r)\ge1), while every singleton deviation gives exactly (1), because all later continuation actions are (B). This proves all 55,986 ordered-history/action deviations directly; `verify_all_b.py` reruns the check with exact `Fraction` arithmetic.

At the root, (W=6). An optimal six-topic sequence chooses (B) once and each singleton once, so (OPT_6=11), (2W-OPT_6=1), and (OPT_6/W=11/6). The family realizes the known (2-1/m) lower-bound ratio at (m=6) while satisfying the target strictly.

This family has **six** maximal catalog topics (one big topic plus five singleton topics). It must not be conflated with the separate seven-maxima seat LP obstruction, which uses seven maximal labels against six provider positions and rejects only a specified auxiliary row family; that obstruction is not an SPE certificate or an original-model welfare counterexample.

Run:

```sh
python research/workspaces/customer-attraction/R-4ba33d9e7be24b0bb0303308d2bcb2ec/all_b_m6/verify_all_b.py
```
