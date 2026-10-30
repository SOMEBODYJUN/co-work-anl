# Independent exact review of the 360-customer candidate

Input: `/workspace/scratch/4fa21fc3d3cc/security_cone_attack/individual_security_failure_360.json`

SHA-256: `4fe2fa90e3da48441cf5463baac7f72e12be56e6edcd8a94e371d5b820383d55`

The verifier reads only the self-contained JSON. It imports no author-side game,
solver, or verification code. Every payoff and budget entry is evaluated with
Python `Fraction` directly from the weighted customer sets.

## Conclusion

The supplied candidate is a valid pure subgame-perfect strategy in the stated
sequential equal-sharing coverage game, and its first player's individual
static-security inequality fails: `102 - 93177/908 = -561/908`.
The welfare-based aggregate and half-coverage inequalities remain strictly
satisfied. Exact budget calculations also confirm the claimed positive GB.

## Input and exhaustive checks

- `3` players, `6` topics, `360` distinct unit customers represented by `19` distinct customer types.
- All topic indices and multiplicities are integers, within range, with strictly positive multiplicities. Customer topic sets have no repeated index; no compressed customer type is duplicated.
- All 15 topic-pair symmetric differences are positive, so all 6 topic coverages are distinct as sets of unit customers.
- Exactly `43` ordered nonterminal histories are supplied, with one legal action per history; no missing or repeated policy node.
- All `216` ordered terminal profiles are evaluated; sum of player payoffs equals coverage in each.
- All `258` one-action continuations are evaluated. All `215` nonprescribed deviations are unprofitable: `164` strictly worse and `51` tied.
- All `21` unordered static rival backgrounds (equivalently `36` ordered backgrounds), including repeated topics, and all `126` pure queries are evaluated.
- All `1548` continuation-background query entries are evaluated for the supplied p budgets at every policy node.
- The provided p and Q have nonnegative exact rational entries and each sums to 1.

## Exact security certificate

`min_B E_p[f_B(a)] = max_a E_Q[f_B(a)] = 93177/908`.
The minimum is checked over every static rival background; the maximum is checked over every pure query. Thus no numerical LP approximation is used.

| Query | E_Q[f_B(a)] | v - E_Q[f_B(a)] |
|---|---:|---:|
| X0 | 93177/908 | 0 |
| X1 | 93177/908 | 0 |
| X2 | 93177/908 | 0 |
| Y0 | 93177/908 | 0 |
| Y1 | 90699/908 | 1239/454 |
| Y2 | 93177/908 | 0 |

The primary optimum is unique: the positive Q-support constraints must all
bind for any optimal p, while every query with strictly positive dual slack
must receive zero probability. On the `5` remaining
coordinates, the normalization and positive-support equations have exact
rank `5`. The supplied p solves those equations, so it is the
only optimum. The complete equation rows are retained in `results.json`.

## Actual path and claimed comparisons

Actual ordered profile: `(0, 3, 4)` = `X0 / Y0 / Y1`.

| Quantity | Exact value |
|---|---:|
| Payoffs | `['102', '117', '117']` |
| Welfare | `336` |
| OPT | `360` |
| First player u - v | `-561/908` |
| Second player u - v | `13059/908` |
| Third player u - v | `13059/908` |
| W - 3v | `25557/908` |
| W - OPT/2 | `156` |
| Root D(p) | `102` |
| Root C(p) | `93177/908` |
| GB = W - sum C | `65339377/3710088` |
| Sum e | `2100/227` |
| Sum kappa | `31016977/3710088` |

The actual policy counts agree with the supplied terminal count vector.
For the root, `D = 102` and `C = v`, hence `e = 0` and
`kappa = -561/908`. The positive sum across the actual three budgets therefore
does not rescue the invalid per-player safety inequality.

## Definitions and budget details

For ordered history h of length i, each action b is followed by the supplied
policy to a full terminal profile. Its i-th entry is removed to obtain B_i(b).
For every query a, the independent evaluator uses

`f_B(a) = sum_(T contains a) w_T / (1 + # rivals whose topic belongs to T)`.

`D_i(p) = sum_a p_a f_(B_i(a))(a)` and
`C_i(p) = sum_(a,b) p_a p_b f_(B_i(b))(a)`.

`e_i = u_i - D_i`, `kappa_i = D_i - C_i`, and
`GB = W - sum_i C_i = sum_i e_i + sum_i kappa_i`.

These continuation backgrounds are recomputed separately for every action.
They are derived from the complete observable policy, including off-path
branches. No background is frozen across deviations.

| Actual history | D | C | e | kappa |
|---|---:|---:|---:|---:|
| `()` | 102 | 93177/908 | 0 | -561/908 |
| `(0,)` | 52091/454 | 392378429/3710088 | 1027/454 | 33309223/3710088 |
| `(0, 3)` | 49945/454 | 49945/454 | 3173/454 | 0 |

All terminal payoffs, all node/deviation comparisons, all static query values,
all cross-query budget matrices, optimal profiles, coverage differences, and
the uniqueness equations are saved in `results.json`.

Reproduce with:

`python /workspace/scratch/4fa21fc3d3cc/individual_security_review/verify_independently.py /workspace/scratch/4fa21fc3d3cc/security_cone_attack/individual_security_failure_360.json`

This review establishes failure of the individual inequality in this supplied
candidate. A global claim that it is the first such failure among all prior
games is outside what a single JSON candidate can establish.
