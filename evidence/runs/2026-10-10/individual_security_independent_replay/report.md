# Independent exact review of the 34-customer candidate

Input: `/workspace/scratch/4fa21fc3d3cc/co-work-anl/history/source/notes/customer_attraction/individual_security_2026-10-10/compressed_34.json`

SHA-256: `d0dbcd994e1ac697669599638e38c6a3d8dcd50cd32bca5d3710cb4533015b68`

The verifier reads only the self-contained JSON. It imports no author-side game,
solver, or verification code. Every payoff and budget entry is evaluated with
Python `Fraction` directly from the weighted customer sets.

## Conclusion

The supplied candidate is a valid pure subgame-perfect strategy in the stated
sequential equal-sharing coverage game, and its first player's individual
static-security inequality fails: `29/3 - 2411/246 = -11/82`.
The welfare-based aggregate and half-coverage inequalities remain strictly
satisfied. Exact budget calculations also confirm the claimed positive GB.

## Input and exhaustive checks

- `3` players, `6` topics, `34` distinct unit customers represented by `13` distinct customer types.
- All topic indices and multiplicities are integers, within range, with strictly positive multiplicities. Customer topic sets have no repeated index; no compressed customer type is duplicated.
- All 15 topic-pair symmetric differences are positive, so all 6 topic coverages are distinct as sets of unit customers.
- Exactly `43` ordered nonterminal histories are supplied, with one legal action per history; no missing or repeated policy node.
- All `216` ordered terminal profiles are evaluated; sum of player payoffs equals coverage in each.
- All `258` one-action continuations are evaluated. All `215` nonprescribed deviations are unprofitable: `144` strictly worse and `71` tied.
- All `21` unordered static rival backgrounds (equivalently `36` ordered backgrounds), including repeated topics, and all `126` pure queries are evaluated.
- All `1548` continuation-background query entries are evaluated for the supplied p budgets at every policy node.
- The provided p and Q have nonnegative exact rational entries and each sums to 1.

## Exact security certificate

`min_B E_p[f_B(a)] = max_a E_Q[f_B(a)] = 2411/246`.
The minimum is checked over every static rival background; the maximum is checked over every pure query. Thus no numerical LP approximation is used.

| Query | E_Q[f_B(a)] | v - E_Q[f_B(a)] |
|---|---:|---:|
| X0 | 2411/246 | 0 |
| X1 | 2411/246 | 0 |
| X2 | 2411/246 | 0 |
| Y0 | 2411/246 | 0 |
| Y1 | 2411/246 | 0 |
| Y2 | 2411/246 | 0 |

The primary optimum is unique: the positive Q-support constraints must all
bind for any optimal p, while every query with strictly positive dual slack
must receive zero probability. On the `6` remaining
coordinates, the normalization and positive-support equations have exact
rank `6`. The supplied p solves those equations, so it is the
only optimum. The complete equation rows are retained in `results.json`.

The square positive-support coefficient matrix on these coordinates has
determinant `-12055/48` (rows follow the JSON Q-support
order). This is an additional exact invertibility certificate whenever the
determinant is nonzero.

## Actual path and claimed comparisons

Actual ordered profile: `(0, 3, 4)` = `X0 / Y0 / Y1`.

| Quantity | Exact value |
|---|---:|
| Payoffs | `['29/3', '67/6', '67/6']` |
| Welfare | `32` |
| OPT | `34` |
| First player u - v | `-11/82` |
| Second player u - v | `56/41` |
| Third player u - v | `56/41` |
| W - 3v | `213/82` |
| W - OPT/2 | `15` |
| Root D(p) | `29/3` |
| Root C(p) | `2411/246` |
| GB = W - sum C | `60/41` |
| Sum e | `161/164` |
| Sum kappa | `79/164` |

The actual policy counts agree with the supplied terminal count vector.
For the root, `D = 29/3` and `C = 2411/246`, hence `e = 0` and
`kappa = -11/82`. The positive sum across the actual three budgets therefore
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
| `()` | 29/3 | 2411/246 | 0 | -11/82 |
| `(0,)` | 5311/492 | 1252/123 | 61/164 | 101/164 |
| `(0, 3)` | 2597/246 | 2597/246 | 25/41 | 0 |

All terminal payoffs, all node/deviation comparisons, all static query values,
all cross-query budget matrices, optimal profiles, coverage differences, and
the uniqueness equations are saved in `results.json`.

Reproduce with:

`python /workspace/scratch/4fa21fc3d3cc/co-work-anl/tests/audits/customer_attraction_individual_security_independent.py /workspace/scratch/4fa21fc3d3cc/co-work-anl/history/source/notes/customer_attraction/individual_security_2026-10-10/compressed_34.json`

This review establishes failure of the individual inequality in this supplied
candidate. It does not establish global minimality or chronological priority
among all possible or previously examined games.
