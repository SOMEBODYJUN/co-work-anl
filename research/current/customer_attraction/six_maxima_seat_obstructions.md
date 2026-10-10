# Dynamic superset seats: exact six-maxima path obstructions

Direct mechanism audit, 2026-10-10. These are **not SPE welfare
counterexamples**. They do not challenge the
[six-maxima no-private theorem or the unrestricted `n>=9` corollary](six_maxima_no_private.md).

## 1. The precise interface being tested

Use [CAG-MODEL](model.md): a finite common customer-subset catalog, unit
providers moving sequentially with observed histories, unit customers,
equal final customer shares, and complete ordered-history pure SPE.
Let `B_0,...,B_5` be six distinct inclusion-maximal coverage sets. Route
every catalog action to a containing maximum, and let `p_j` be the routed
prefix counts with `r` providers remaining. Let `w_I` be the number of
customers belonging to exactly the maxima indexed by the nonempty set `I`.
The common core has incidence `{0,...,5}` and mass `c`.

Define the dynamic shared term and private seats by

\[
 v_j(p,r)=\sum_{\substack{I\ni j\\2\le|I|\le5}}
 \frac{w_I}{p_I+r},\quad p_I=\sum_{j\in I}p_j,
 \qquad q_{j,k}(p,r)=\frac{w_{\{j\}}}{p_j+k}+v_j(p,r),
 \quad1\le k\le r.
\tag{SO1}
\]

Let `xi(p,r)` be the `r`th-largest value among these `6r` seats, with
multiplicity. This is a valid all-history current-player floor:

\[
 u\ge c/n+\xi(p,r),\qquad
 W\ge c+\sum_{t=0}^{n-1}\xi(p^t,n-t).
\tag{SO2}
\]

To see validity, every shared term is nondecreasing along routing
successors: each denominator stays fixed or decreases. The selected route
shifts away its first private seat, while other routes truncate their last
seat. If at least `r` seats meet a threshold, at least `r-1` successor
seats do. If a route has all `r` qualifying seats, that route alone retains
`r-1`; otherwise only the selected route can lose a qualifying seat.
Thus `xi` is nondecreasing. At a decision node choose a full maximum whose
first seat meets `xi`. If no follower is assigned to that maximum, its
private load is at most `p_j+1` and its shared payoff is at least `v_j`.
If a follower is assigned there, the current full maximum contains its
actual action; the current player dominates that follower's actual payoff.
Backward induction over all ordered histories gives (SO2), including core
omissions by internal actions.

The proposed global payment would be

\[
 \sum_t\xi(p^t,n-t)\ge\operatorname{OPT}_n/2
 \quad\text{for every routed legal path.}
\tag{SO3}
\]

The four exact instances below disprove (SO3), separately at every
`n=5,6,7,8`. No minimality or LP optimality is asserted.

## 2. Exact sparse customer incidence certificates

In each instance the catalog consists of the six maxima themselves. Each
listed incidence type is a disjoint block of the stated number of distinct
unit customers; all unlisted types have mass zero. The maxima are distinct
and pairwise incomparable. All common cores are empty.

The complete integer weights and rational seat sequences are frozen in
[`customer_attraction_six_maxima_seat_obstructions.json`](../../../evidence/runs/2026-10-10/customer_attraction_six_maxima_seat_obstructions.json).
Incidences there use binary masks with zero-based indices. These are
ordinary unit-customer instances, not weighted providers.

| Providers n | Routed prefix string (zero-based) | U=OPT_n | Sum of dynamic seat floors | Ratio to OPT_n |
| ---: | --- | ---: | ---: | ---: |
| 5 | `(0,1,2,3)` | 97 | 46 | `46/97` |
| 6 | `(0,0,1,2,3)` | 504 | `495/2` | `55/112` |
| 7 | `(0,1,2,3,4,5)` | 8071 | `140687/35` | `140687/282485` |
| 8 | `(0,1,0,2,3,4,5)` | 10212 | `121471/24` | `3283/6624` |

Every last column is strictly below `1/2`. The strings have length `n-1`
and specify the routed prefix before each player's decision; no final
action needs to be selected to determine the listed budget. For `n>=6`,
all six maxima fit, so `OPT_n=U`. For `n=5`, maxima `0,1,2,4,5` already
cover the full union of the instance.

The two new larger instances each use only eight positive customer types:

| Incidence | n=7 multiplicity | n=8 multiplicity |
| --- | ---: | ---: |
| `{0}` | 0 | 3185 |
| `{3}` | 1822 | 0 |
| `{0,2}` | 1638 | 0 |
| `{1,3}` | 0 | 1795 |
| `{0,4}` | 690 | 0 |
| `{1,4}` | 1236 | 1321 |
| `{2,4}` | 534 | 1296 |
| `{3,4}` | 0 | 209 |
| `{0,5}` | 405 | 0 |
| `{1,5}` | 1224 | 69 |
| `{2,5}` | 522 | 1434 |
| `{3,5}` | 0 | 903 |

For `n=7`, literal sorting of the `6r` Fraction-valued seats at each prefix
gives

\[
 (\xi_t)_{t=0}^6=
 (2733/7,410,2421/5,492,615,717,911).
\]

For `n=8`, it gives

\[
 (\xi_t)_{t=0}^7=
 (3185/8,455,455,546,637,1413/2,802,3185/3).
\]

These calculations concern a legal routed path, which need not be a root
equilibrium path. In particular they do not set actual SPE welfare equal
to the seat-floor sum. They show that proving the valid lower bound (SO2)
does not by itself close half coverage through (SO3); a further global
equilibrium payment or a stronger interface is needed in all four critical
provider counts.

## 3. Reproduction and verification

The independent audit
[`customer_attraction_six_maxima_seat_obstructions.py`](../../../tests/audits/customer_attraction_six_maxima_seat_obstructions.py)
imports no repository model or solver. It verifies the integer customer
construction, all six maximal coverages, the empty core, full optimal
coverage, every literal seat list and order statistic, and all four strict
ratio inequalities using `Fraction`. It also counts immediate joins
directly from the constructed customer blocks; no numerical LP output is
accepted as evidence.

Run from the repository root:

```sh
python3 tests/audits/customer_attraction_six_maxima_seat_obstructions.py
```

The frozen verification is
[`customer_attraction_six_maxima_seat_obstructions_audit.json`](../../../evidence/runs/2026-10-10/customer_attraction_six_maxima_seat_obstructions_audit.json).

The subsequent [CA-SIX-MAXIMA-HALF joint-budget theorem](six_maxima_joint_bound.md) proves unrestricted six-maxima half coverage for every player count. These exact path examples retain their stated role as obstructions only to summing the dynamic-seat floors; the joint theorem adds true action membership, final maximal best responses and valid last-two tax information.
