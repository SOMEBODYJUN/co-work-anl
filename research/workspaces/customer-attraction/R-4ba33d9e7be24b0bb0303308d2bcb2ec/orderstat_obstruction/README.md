# Exact obstruction to the n=6 seven-maxima mixed-floor/L/tax certificate

**Status: FAILURE / method boundary.** This is an independent exact reconstruction of a restricted row-family LP; it is not a counterexample to Q-CAG-HALF-6 and does not change the theorem's OPEN status.

For a seven-maxima instance with six providers, fix the actual final maximal action as `B_0`. Compress each customer by maximal incidence `I⊆{0,…,6}` and actual membership `J⊆{0,…,5}`, with the full-history seat assumptions used in the seven-maxima source: the last actual membership is `1_{0∈I}`. There are `127·2^5=4064` literal columns.

The tested row family is exactly:

- six mixed-floor slacks `M_t` (`t=0,…,5`) using the suffix minima of the seven-maxima private/shared floors;
- seven genuine final-response slacks `L_j` (`j=0,…,6`);
- 28 genuine two-remaining tax slacks `T_{j,l}` (`0≤j≤l≤6`, including repeated pairs).

For a column, `r = 1_{J≠∅}−1/2−Σ λ_s s_s` is the residual in the standard decomposition of `W−U/2`. Any nonnegative multipliers `λ_s` with all 4064 residuals nonnegative would prove `U≤2W` for this row family.

The script `dual_obstruction.py` gives an exact Farkas witness. It averages under all permutations of labels `1,…,6`; the eight nonzero orbit masses are:

| orbit `(f, |I|, E)` | mass |
|---|---:|
| `(1,1,∅)` | `7017572/321392367` |
| `(1,1,{3})` | `3133900/321392367` |
| `(0,1,∅)` | `111186481/214261578` |
| `(0,1,{4})` | `2017043/71420526` |
| `(1,2,{2,3})` | `42350/3967807` |
| `(1,2,{1,2,3})` | `387200/35710263` |
| `(1,2,{0,1,2,3})` | `3573215/71420526` |
| `(1,2,{0,1,2,3,4})` | `8325175/23806842` |

(The orbit mass is distributed uniformly over its `S_6` orbit.) The masses sum to one. Direct Fraction evaluation over every literal column gives every row average nonnegative; the only positive classes needed for the certificate are `M_5=3883672/321392367`, `T_{0,0}=40802035/964177101`, and the symmetric tax classes listed by the script. Yet the averaged base coefficient is

\[
\mathbb E[1_{J\ne\varnothing}-1/2]
 = -2027846/107130789 < 0.
\]

Therefore for every nonnegative multiplier vector `λ`,
\[
\mathbb E[r] = -2027846/107130789 - \sum_s λ_s\,\mathbb E[s_s] < 0,
\]
so at least one customer column has negative residual. This proves no certificate using only the six mixed floors plus `L_j` and `T_{j,l}` rows can establish `U≤2W` at `n=6`; a new row family or a direct `OPT_6`-specific payment is necessary.

This obstruction is narrower than the target: `U` can exceed `OPT_6` when seven maxima are available but only six providers. It does not supply a target welfare counterexample. It also does not invalidate the legal order-statistic aggregate seat row; it only shows that the older row family, even with all genuine `L/T` rows, cannot close the union target.

Reproduce:

```sh
python3 research/workspaces/customer-attraction/R-research18-orderstat-obstruction/dual_obstruction.py
```
