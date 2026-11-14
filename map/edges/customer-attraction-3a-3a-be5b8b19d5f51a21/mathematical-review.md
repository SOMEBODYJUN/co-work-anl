# Positive-depth root-regret cones: finite exact boundary

This review covers the complete object `customer-attraction/positive-depth-root-regret-cones-230-rational-certificates` and its sixteen staged reading spans. It records the exact finite result and its quantifier boundary; it does not turn the finite probe into a universal welfare theorem.

## Model and cone

The shared model has a finite nonempty **labeled** topic catalog with an arbitrary coverage map. Labels may have the same coverage; empty labels, repeated actions, and weak ties remain legal. There are `m` ordered unit-weight providers. A complete pure strategy is defined at every ordered history. If a player deviates at a history, the continuation is the same strategy evaluated on the changed history, so all positive-depth rows use the true changed-history terminal. Customer types are the nonempty topic masks `M`; nonnegative masses `x_M` are the linear extension of distinct unit-customer multiplicities, and zero mass types may be omitted.

For a terminal count vector `q`, the coefficient of type `M` in the payoff of label `a` is

\[
 f_a(q)_M = {\bf 1}_{a\in M}/\sum_{b\in M}q_b,
\]

with the zero numerator convention. At each positive-depth history `h` with prescribed action `t`, the exact row is `f_t(q(h)) - f_b(q(h,b))` for every alternative `b`. The probe regenerates these rows directly from all positive-depth histories and then removes only duplicate/zero rows. A set difference from a de-duplicated all-row matrix is invalid because a coefficient can occur both in a root row and a genuine successor row.

The selected root action `a` is allowed to be non-optimal. The root rows are relaxed with one nonnegative `Delta` coordinate:

\[
 f_a(q(a))x-f_b(q(b))x+\Delta\ge0,
\]

and positive-depth rows have zero `Delta` coefficient. The actual root regret is

\[
 \delta=\max_b f_b(q(b))x-f_a(q(a))x\ge0.
\]

The objective is normalized at `w x=1`, where `w` is coverage of the actual root, and for each support `J` of size `min(m,p)` uses `v^J_M={\bf1}_{M\cap J\ne\varnothing}`:

\[
 \max\{v^Jx-3\Delta:G(x,\Delta)\ge0,\ wx=1,\ x,\Delta\ge0\}.
\]

Since `-3` is strict, every exact optimum takes `Delta=delta`; the checker verifies this for all 230 saved records. The dual certificate checks the coordinate inequalities

\[
 \beta(w,0)-G^\mathsf T\mu-(v^J,-3)\ge0,
\]

including the `Delta` coordinate, with `\mu\ge0`; the root-row multiplier sum is therefore constrained by the coefficient `3`.

## Four fixed policy cones

The four inputs are complete ordered action tables with respectively `259`, `21`, `43`, and `85` decision records (`\sum_{d=0}^{m-1}p^d`). For each actual root and every legal support `J`, the saved rational primal and sparse dual are replayed exactly.

| input | `(m,p)` | full ordered nodes | root × supports | certified maximum |
|---|---:|---:|---:|---:|
| `root_tax_failure` | `(4,6)` | 259 | 6 × 15 = 90 | `7/4` |
| `eight_cce_welfare_gap` | `(3,4)` | 21 | 4 × 4 = 16 | `3/2` |
| `aggregate_theta_failure` | `(3,6)` | 43 | 6 × 20 = 120 | `33/23` |
| `fractional_actual_load_failure` | `(4,4)` | 85 | 4 × 1 = 4 | `9/8` |

All 230 primal points satisfy nonnegativity, every rebuilt positive-depth row, `w x=1`, and the exact objective/dual equality. All 230 duals satisfy every customer-type residual and the `Delta` residual. The maxima are strictly below `2`, so no saved point satisfies the finite-cone compiler trigger `OPT-2W>3\delta`.

The first three groups have zero positive-regret records. In the fractional group, the two records with actual roots `2` and `3` have `delta=Delta=1/24`; their coverage gap above `2W` is `-3/4`, and the penalized optimum is `9/8`. These records are valid positive-depth policy-cone points with a root that is not an SPE root. They must not be relabeled as complete-root SPEs.

At `W=0`, the four inputs have at least two providers. The second provider's realized profit is zero; a legal deviation to any nonempty theme would yield positive share, so every type mass is forced to zero by positive-depth IC. Hence coverage and root regret are both zero. The finite result therefore includes, rather than silently deletes, this boundary.

## Independent exact replay and auxiliary finite records

`check_saved.py` uses only the standard library. It reconstructs each action table's true terminal counts, rebuilds the positive-depth row set in sorted order, expands every sparse primal/dual coordinate, and checks all rows and dual residuals with `Fraction`. It does not import the original probe, `StrategyCone`, NumPy/SciPy, or a solver. The saved verification reports exact primal/dual checks for all 230 records.

The same verification file contains seven separate finite suffix-insurer maxima. Their `3e-D` scores are all nonpositive:

| input | `(m,p)` | score `3e-D` | winning suffix welfare |
|---|---:|---:|---:|
| `root_tax_failure` | `(4,6)` | `-9` | 38 |
| `eight_cce_welfare_gap` | `(3,4)` | `-2` | 8 |
| `aggregate_theta_failure` | `(3,6)` | `-30` | 36 |
| `fractional_actual_load_failure` | `(4,4)` | `-11` | 14 |
| `individual_security_failure` | `(3,6)` | `-55/2` | 33 |
| `prefix_balance_failure` | `(4,6)` | `-6` | 14 |
| `portfolio_matching_failure` | `(2,5)` | `-36` | 42 |

These seven rows are finite exact input checks only. They do not add a new universal insurer theorem and do not alter the four-cone objective.

## Boundary and unpaid obligations

The general strategy-cone theorem supplies the semantic interpretation of a fixed complete strategy's nonnegative rational customer cone and its fixed-`J` primal/dual certificate. This package specializes that theorem to four named policies, all roots, and all `min(m,p)` supports. It does not quantify over all complete strategies, all catalog sizes, all player counts, or all root choices. It does not run the original LP, regenerate a candidate, prove the threefold compiler itself, or produce a unit-customer half-coverage counterexample. The two positive-regret rows are evidence that root relaxation can be nontrivial even when the penalized finite objective remains below `2`.
