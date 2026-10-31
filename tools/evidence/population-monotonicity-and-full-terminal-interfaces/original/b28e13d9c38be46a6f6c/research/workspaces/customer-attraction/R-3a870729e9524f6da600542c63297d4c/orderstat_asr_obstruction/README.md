# Aggregate order-statistic rows: exact obstruction on one seven-maxima route

**Status:** exact mechanism boundary, not a Q-CAG-HALF-6 counterexample.

At a prefix with `r=6-t` providers left and seven maximal coverages, define
seat values
\[
q_{j,k}=w_{\{j\}}/(p_j+k)+\sum_{I\ni j,|I|\ge2}w_I/(p_I+r),\qquad 1\le k\le r.
\]
The legal seat theorem gives only `u_t >= xi`, where `xi` is the `r`-th largest
of the `7r` seats. For every set `H` of `r-1` seat indices and the valid upper
bounds `U_{j,k}=|B_j|/(p_j+k)`, the following aggregate row is legal:
\[
u_t\ge ASR_H:=\frac{\sum_{j,k}q_{j,k}-\sum_{(j,k)\in H}U_{j,k}}{7r-r+1}.
\]
Indeed at most `r-1` seats can exceed `xi`, so `sum q <= sum_H U +(6r+1)xi`.
Unlike the invalid per-seat rows, every `ASR_H` is a genuine whole-row SPE
necessary inequality and has linear customer coefficients.

The old exact Farkas witness for the six mixed-floor rows plus all seven final BR
rows and 28 two-remaining tax rows (stored in
`R-4ba33d9e7be24b0bb0303308d2bcb2ec/orderstat_obstruction/dual_obstruction.py`)
has negative target base average `-12442/3967807` for `W-|O_K|/2` when
`K={1,2,3,4,5,6}` (the actual final maximum `B_0` is omitted), while all old
row averages are nonnegative. For route `(0,0,0,0,1,0)`, the script
`audit_asr_dual.py` computes exact orbit averages of **every** ASR row. It uses
the identity
\[
E[ASR_H]=b_t+\sum_{h\in H}d_{t,h},
\]
so the minimum over all `H` is obtained by sorting the seat deltas; no subset is
sampled. The six exact minima are:

| `t` | `r` | minimum `E[ASR_H]` |
|---:|---:|---:|
| 0 | 6 | `10564271/1468088590` |
| 1 | 5 | `677380141/99631633770` |
| 2 | 4 | `3454574/599612625` |
| 3 | 3 | `495326117/122129099460` |
| 4 | 2 | `74904707/83562015420` |
| 5 | 1 | `19909061/3749577615` |

All are strictly positive. Therefore adding any nonnegative multipliers on any number of legal ASR rows leaves
the exact witness expectation strictly below zero. This is directly an
`OPT_6`-specific obstruction for the six-set target omitting the actual final
maximum (`K=126` in the canonical missing-route naming), for the old
M/L/T+ASR row family. It still does not supply an SPE welfare violation: the
witness is a customer-column Farkas distribution over necessary inequalities,
not a realizable strategy. Other target six-sets (omitting labels 1,...,6) have
positive base under this witness and are not covered by this obstruction.

Reproduce from repository root:

```sh
python3 research/workspaces/customer-attraction/R-3a870729e9524f6da600542c63297d4c/orderstat_asr_obstruction/audit_asr_dual.py
```
