# R275 full-history nearest/global walk

This directory preserves the full-history walk source and two frozen outputs. The `nearest` output has 48 rounds and 13 distinct full-tree cones; the `global_submodular` output has 72 rounds and 15 cones. Both outputs explicitly keep `Q_CAG_HALF=OPEN` and `customer_realizability=not_claimed` in their best witnesses.

The replay summary is a field-derived audit of the frozen JSONs. It does not claim a fresh rerun of the 149-second/280-second floating LP walks, and it retains the source/output provenance differences already visible in the earlier 36-round summary.
