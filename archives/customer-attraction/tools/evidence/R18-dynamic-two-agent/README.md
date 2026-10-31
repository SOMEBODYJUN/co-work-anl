# R18 sqrt-arrival finite obstruction replay

This directory preserves source `c3da7e69c42b7800323f` (`sqrt_arrival_search.py`), its declared dependency source `5878a511362d7d461809` (`step_profit_search.py`), the exact pure-SPE model used to execute the dependency, stdout/stderr, and an independent exact/Fraction recomputation of the reported witness.

The source scans random finite instances (seed 912343, at most 1000 trials). For each prefix count `b` and action `a`, it compares a future static background-profit gap `F(b)-F(b+e_a)` against a proposed square-root arrival charge over customer types containing `a`, retaining a positive deficit when found. This is an exploratory obstruction to that charge formula. It does not prove failure of all non-local potentials, a universal security theorem, or a Q-CAG-HALF-6 result.

The first positive result occurs at iteration 108. `verify_instance.json` recomputes the instance with exact `Fraction` values for `F`, the SPE threshold, and the action utility, while retaining the square-root charge as a real-number evaluation.
