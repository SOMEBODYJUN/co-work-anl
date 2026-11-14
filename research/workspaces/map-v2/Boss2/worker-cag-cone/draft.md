# CAG finite cone / terminal pair exact-boundary reading

Assigned core: `cag-actual-prefix-floor-terminal-pair-four-exact-cone-boundaries` (registry pin `eec62dcffad4af1b26c8e2495e4d055e7c1aa5a3072b8efba95f3418ba570ac2`). No read-only endpoints or overlap comparisons were declared, so this is an object-internal 3A review; deferred candidate names are not evidence.

The common model is a finite nonempty tagged catalog `S`, finite unit customers, and `m` unit providers choosing in order while observing all previous ordered actions. A complete pure strategy is an all-history function. SPE requires the stated continuation IC at every ordered history and every unilateral catalog deviation, with the true post-deviation continuation; same-load histories may use different continuations. Welfare is the covered-customer count and `OPT_m` is the best `m`-tuple catalog cover. The assigned result applies only to necessary rows valid for any such SPE, without claiming the row cone itself is strategy-realizable.

For `m in {5,6,7,8}`, a customer type is `e in {0,1}^m`, with `d` the count among the `m` comparison themes and `ell` the terminal reply count. The rows are all `m^2` copy rows, `m` copy-opt rows, one fixed menu-G row, and the three aggregate terminal PAIR families plus `m` opt-actual and `m(m+1)/2` actual-pair rows, for `(3m^2+5m+8)/2` rows. Rows are valid after summing the customer coefficients over all customers; individual coefficients need not be nonnegative. The LP is `max o^T mu` subject to `R mu >= 0`, `w^T mu=1`, `mu>=0`.

For fixed `(e,d)`, every intermediate `ell` column obeys `C(e,d,ell)=(1-ell/m)C(e,d,0)+(ell/m)C(e,d,m)`. Since all other rows are independent of `ell` and `G` is affine, endpoint columns generate the same nonnegative cone as the full `ell=0,...,m` domain. This is an affine finite-cone equivalence only; it does not construct a single legal catalog/strategy after splitting customer mass.

Exact Fraction primal/dual recovery certifies the finite LP. The beta values are:

| m | rows / columns | exact beta | primal support | positive dual rows | rank |
|---:|---:|---:|---:|---:|---:|
| 5 | 54 / 384 | `245128999/112807105` | 8 | 7 | 8/8 |
| 6 | 73 / 896 | `6138981/2543692` | 13 | 12 | 13/13 |
| 7 | 95 / 2048 | `2819026521859751/1066002346290848` | 15 | 14 | 15/15 |
| 8 | 120 / 4608 | `761909597306298999/265719514705067684` | 16 | 16 | primal 16/16; dual 17/17 after an exact active-column equation fixed the first underdetermined rationalization |

For each m, the recovered mass has `W=1`, objective `O=beta`, every enumerated row slack is nonnegative, and every enumerated column remainder `eta=beta*w-o-sum(lambda*R)` is nonnegative. The reports retain 342 row slacks and 7936 column remainders across the four runs. All four exact duals assign zero weight to every PAIR row; all four primal points nevertheless have strictly positive slack on every PAIR row. Thus adding these PAIR rows does not improve the optimum of this specified finite necessary-row cone. It does not show that PAIR rows are useless in other prefixes, with common-menu constraints, or in the full strategy model.

Summing the valid necessary rows over customers gives `O <= beta W`; hence, for every genuine complete pure SPE in the stated model, `W >= OPT_m/beta` for the corresponding finite m. The finite points are formal nonnegative customer masses; they do not supply a common catalog, a full strategy, consistency of repeated queries, or all earlier off-path histories. Therefore they neither refute the five-person half theorem nor prove a universal half theorem or a sharpest possible bound.

No cross-object comparison was assigned or completed. Open continuation is to compare this finite cone, with its exact boundary values and PAIR-inactive duals, against a separately assigned full-history/half theorem or a cone containing missing intermediate-history/common-menu constraints; that comparison must be a new 3B/3C task.
