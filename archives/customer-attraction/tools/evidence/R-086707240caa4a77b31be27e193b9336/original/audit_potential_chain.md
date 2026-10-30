# Independent audit: harmonic-potential chain obstruction

Status: **verified obstruction; not a Q-CAG-HALF counterexample**.

I independently ran

```sh
python3 research/workspaces/customer-attraction/R-23ab27f8efb44f1faca2699d45886250/general_n/verify_zero_regret_promotion.py --t 1
```

The fixed four-theme, three-player strategy is checked at all 21 ordered histories (84 action comparisons). The actual path is `(A,B,C)` with payoffs `(2,2,3)`, `W=7`, and `OPT_3=7`; promoting the actual last theme at the root gives `(C,D,C)` with payoffs `(2,2,2)`, `W=6`. The source regret is exactly `Gamma=0`, while harmonic potential drops from `Phi=9` to `Phi=8`. The replay path `(C,A,B)` also has zero middle-player IC slack, and deleting the middle action changes potential from `6` to `7`.

Thus for the comparison-prefix chain `r^k`, the exact identity

`Phi(r^0)-Phi(r^m) = sum_k Gamma_k + sum_k Delta_k^rem`

has a genuine positive future-response term `Delta^rem` that is invisible to the source and replay IC slacks. This rules out paying every harmonic-potential reset by a finite multiple of those same slacks. It does not refute Q-CAG-HALF because the witness has `2W=14 >= OPT_3=7`.

Next task: seek a different weighted/truncated potential or a complete six-player SPE certificate; do not promote this obstruction to a target counterexample.
