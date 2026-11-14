# Cartesian root-reset obstruction support

Core: `M-189d60bfb78140709755f3477e6a10c5` (pin
`0430076fef32e956cdc2af28e1a62408a281c554df0dc933e62333b5a0cbee5a`). This package records
the core's exact finite base obstruction and its all-positive-integer Cartesian lift; the
context edge is scoped to the labelled-catalogue/full-history model and does not assert a
general six-player half failure.

The two four-topic blocks have unit-customer multiplicities `2,4,6,3,1` for
`{A}`, `{B,D}`, `{A,C}`, `{C,D}`, `{A,B,C,D}`. The complete eight-player DAG has SHA
`6190bc98dedda4fb22a1af6339702c03a6cb3b04cd8dfe6b18a577782e5d2f95`, 13,872 reachable
nodes, 6,435 terminal nodes and 59,496 exact IC comparisons. The independent verifier exits
zero and agrees with the frozen report: actual path `(3,0,2,3,4,4,5,6)`, root utility
`13/4`, welfare and optimum `32`, and root 3/7 cross-query `37/10`.

The local requirement `R(A,T)≤e(A)+e(T)+J(A,T)` fails exactly at `(A,T)=(3,7)`:
`e(3)=e(7)=J(3,7)=0`, while `R(3,7)=9/10`. The same finite kernel has all-p quadratic
maximum `1717/560`, strictly below `u=13/4`; the 3/7 half mixture has maximum `123/40`.
These values establish a quantifier separation between a local pair-payment contract and
fixed-kernel mixed averages.

For every `k≥1`, the all-coordinate product directory and coordinate-projected continuation
strategy preserve every full-history IC inequality by summing the independent customer
blocks. The exact additive identities give `R^(k)=9k/10` at the coordinatewise `(3,7)` pair,
zero coordinatewise `e/e/J`, and `W=OPT_8=32k`. This is the reusable mathematical contribution.

The read-added peer `M-d2dd649a6dc549b493268251dc9a5e4d` supplies a finite audit of the same
base DAG; the existing accepted edge `ca-732c-finite-reset-audit-checks-cartesian-obstruction`
already records that interface. No new implication, refutation of half, or all-policy welfare
claim is supported here.
