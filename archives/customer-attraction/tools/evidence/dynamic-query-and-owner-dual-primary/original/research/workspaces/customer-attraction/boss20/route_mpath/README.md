# Mpath route: dynamic continuation debt

This branch records an exact general identity for the free complete path-menu candidate. The main file is `dynamic_query_debt_identity.md`; `audit_dynamic_query_debt.py` rechecks the identity with arbitrary finite continuation loads using exact `Fraction` arithmetic (5,000 random rational trials passed on 2026-10-24).

The identity isolates the only potentially positive term in `C_i(p)-D_i(p)` as a conditional reciprocal-load covariance caused by changing continuation after a forced action. The fixed-suffix/static-Nash corollary proves the free-menu bound in that restricted class; it does not address arbitrary history-dependent pure SPE.

Current open obligation: control the aggregate continuation covariance across all positions by the collision discounts, IC slacks, defensive-column gains, or a new cross-history relay. A finite counterexample would need a genuine positive aggregate covariance surviving all those payments and all off-path SPE checks. No general proof or Q-CAG-HALF resolution is claimed.

Files:

- `dynamic_query_debt_identity.md`: exact identity, interpretation, static corollary, and remaining gap.
- `audit_dynamic_query_debt.py`: independent exact arithmetic audit of the identity.
