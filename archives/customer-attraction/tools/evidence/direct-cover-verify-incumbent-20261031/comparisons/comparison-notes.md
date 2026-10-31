# Direct-cover incumbent obstruction verifier comparison

- source ID: `c885e1e95fad531e7e7c`
- source path: `research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/verify_incumbent_obstruction.py`
- source SHA-256: `227c15293633967e7e6508afa517828018c0c897b037f60654d1b5774cc556c3`
- source size: 1811 B

The standalone script was read and executed once. It uses only `Fraction`, `itertools.product`, and hard-coded topic sets `({0,2},{1,2},{3,4})`; it does not import the canonical model, solver, or exploratory LP. For 102 positive background counts (`1..100`, `1000`, `10**6`) it checks payoff tables, unique best responses, first-player values, final values, and the ratio comparison, exiting 0 with `PASS: all histories and payoff formulas for 102 positive background counts; ratio bridge 1 < 4/3.`

This is finite regression evidence for the stated formulas. It does not itself prove an all-background theorem, a complete original SPE certificate, weak matching failure, or a Q-CAG-HALF counterexample. The broader all-k claim remains bounded by the accompanying mathematical note and direct-cover route, while the script proves only the listed finite sample checks.
