# Owner-tax pressure test (finite diagnostic)

This note attacks the explicit recursive diagnostic from `recursive_state/README.md` and `root_route/threshold_budget.md`. For a fixed complete pure-SPE certificate, actual ordered path `a`, and ordered optimal tuple `T`, for each unit customer `x` in `OPT \ actual` we force each eligible owner slot `i` at the actual prefix, follow the same complete strategy on the resulting off-path history, and set

\[
R_{\min}(T)=\sum_{x\in OPT\setminus actual}\min_{i:x\in T_i}\frac{k_i(x)}{1+k_i(x)}.
\]

Here `k_i(x)` is the number of post-`i` responders that cover `x` on that forced branch. The diagnostic bound checked is `R_min <= |I|+2|G|`, with `I=OPT\cap actual` and `G=actual\setminus OPT` as unit-customer sets. This is only a pressure test; it is not claimed to be equivalent to Q-CAG-HALF.

`owner_tax_exhaustive.py` exactly enumerates all 127 nonempty binary customer-type supports for `k=3,m=3`, every pure-SPE terminal outcome returned by the canonical arbitrary-history solver, and every ordered optimal 3-tuple. It checks 3,984 `(instance, SPE outcome, optimal tuple)` combinations. The largest observed `R_min-|I|-2|G|` is `-1`; no violation occurs. The same script checks the all-big family for `m=1,...,8`; every returned SPE outcome has `R_min=0` for the displayed optimal tuple.

The companion `owner_tax_search_random.py` is retained as a bounded random stress harness (seed 7, sparse binary type supports); it is diagnostic only and is not used for the exact conclusion. The JSON report contains only exact integer/Fraction outputs. This finite negative result does not establish the bound for general inputs, nor does it refute the main theorem.
