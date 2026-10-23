# Independent reconstruction and maximal-topic reduction boundary

This directory belongs to the sixth independent agent under parent
R-5d61c5324e744dc0a66133207fcbd010. Only files here were edited; no git or
credentials were used.

Current result: `maximal_catalog_boundary.md` gives an all-k proof that the
maximal-only subcatalog of the existing collision-free family has minimum SPE
welfare 3k+1, whereas the full catalog has a complete SPE of welfare 2k+2. This
refutes the proof-transfer bridge L(full)>=L(maximal), with an asymptotic 3/2
comparison loss, for unbounded players and catalog size. It does not refute the
opposite monotonicity claim and does not solve Q-CAG-HALF.

`check_maximal_catalog_boundary.py` performs exact finite reconstruction and
full ordered-history certificate verification. `maximal_catalog_boundary.json`
records the actual run when present. The uniform proof is independent of the
finite run, and its full-catalog dependence is stated exactly.

Remaining: independent attack of the symbolic suffix lemmas and the attainment
strategy, then parent review. A more ambitious useful next question is whether
there is any universal reverse comparison L(maximal)<=3/2 L(full); the present
family supplies only a necessary factor and no affirmative evidence.
