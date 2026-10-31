# R-275 direct_global cone/floor finite evidence

This directory preserves the three assigned frozen artifacts and a bounded
record-level replay.  The source files were obtained with `work.py clean show`
from legacy-cleanup commit `68fad804ec5946cb296f77dc5b336308a66abf12` and
their SHA-256 values match `cleanup/inventory.jsonl`.

## Replayed records

Run from the repository root:

```sh
python archives/customer-attraction/tools/evidence/R275-direct-global-cone-floor-20261031/replay/verify_records.py
```

The checker reconstructs the finite continuation recursion from
`cone_floor_attack.py`, verifies the cone normalization and weighted
inequalities for the stored decimal weights, recomputes the reported cone
objective/ratio, and re-runs `floor_scan.Fast.run` on `floor_best.json`.
The saved output is `replay/verification.json`.

The cone policy has 2,801 stored nodes and 16,806 deviation rows.  Decimal
reload gives the same target, normalization `1`, objective
`0.1111111111111111`, and ratio `1.1111111111111112`; its policy action table
differs at 865 nodes because the source recursion resolves floating-point
ties by first eligible action.  This is a reproducibility boundary, not an
exact certificate.  The smallest recomputed weighted cone residual is about
`-2.5e-16`.

The floor record replays exactly at the recorded precision: `p=5`, `n=3`,
`v=48.5`, `OPT=204`, covered count `[0,2,1,0,0]`, and ratio
`1.426470588235294`.

## Interpretation

`cone_best.json` is a finite fixed-policy-cone LP candidate.  Its support row
normalizes the total mass of customer types touching topics 0 through 4; it
does not normalize the actual welfare of a complete SPE and has no LP dual or
exact rational recovery.  The target terminal count is
`[0,1,1,1,2,0,0]`, with action `4` and support `[0,1,2,3,4]`.  The ratio is
`2*n*u=10u`, where `u` is the selected target provider's weighted payoff under
that normalization.  A value above one is therefore only a finite diagnostic
of this cone objective; it is not an `OPT/W` value and cannot be a Q-CAG-HALF
counterexample.

`cone_floor_attack.py` samples `(p,n)=(5,3),(6,4),(7,5)` with respectively
30, 20, and 10 iterations, drawing sparse weights from
`[0,0,0,1,2,4,8,16]`; it minimizes the selected target payoff subject to the
constructed policy-cone inequalities and a support-mass equality.  The
`floor_scan.py` record samples `(p,n)` pairs `(5,3),(6,3),(6,4),(7,4),(7,5)`
for 3,000, 3,000, 2,000, 1,000, and 500 random weight vectors.  Neither
finite loop is exhaustive, and neither source has a universal quantifier over
catalogs, SPE continuation tables, or integer customer instances.

The companion direct_global README and residual-family note establish the
actual scope: Q-CAG-HALF remains open; the nine-topic, six-provider
common-query bridge counterexample is a separate complete-SPE result, while
the padded residual family has its own analytic four-payoff floor.  Those
objects are linked from the cleaned mathematics page and are not silently
identified with these cone/floor diagnostics.
