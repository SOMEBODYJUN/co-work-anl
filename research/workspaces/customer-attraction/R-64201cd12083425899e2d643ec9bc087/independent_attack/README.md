# Independent reconstruction and finite uniform-interface attack

Status: exploratory work, 2026-10-21. The general Q-CAG-HALF target remains OPEN.

## Reconstructed bottleneck

Write U for an actual SPE terminal covered set, and let T_1,...,T_m be an
optimal tuple. Last-player optimality gives, for every j,

    |T_j \ U| <= u_m.

The non-repeated outside optimum union is therefore at most m*u_m. This
would prove half coverage if u_m were always at most W/m, but that auxiliary
claim is false: the existing complete two-player residual witness has payoffs
(4,5), hence last payoff 5 exceeds average 9/2. Earlier players' deviations
can induce later players to overlap the newly entered theme. The associated
cross-branch loss is the essential obstruction; the terminal best reply alone
does not close the desired total budget.

No monotonic-payoff, static-NE, individual-security, or fixed matching claim is
being asserted here.

## Finite full-cone search on the stronger uniform interface

The conjectural interface from
`research/current/customer_attraction/global_new_uniform_portfolio_two.md` is

    m*|union_j T_j| <= (m-1)*W + sum_{i,j} V_{i,j},

where V_{i,j} follows the original complete strategy after player i deviates
to T_j at that player's actual prefix. For each fixed complete strategy,
`attack_uniform.py` builds all nonempty customer incidence types, all ordered
history SPE inequalities, and W=1. It maximizes the difference between the
left and right sides over this full nonnegative customer-multiplicity cone,
for every distinct comparison support of size min(m,k).

Completed floating LP runs:

| Complete strategy source | m | k | Comparison supports | Positive violation found |
| --- | ---: | ---: | ---: | --- |
| individual_security_failure.json | 3 | 6 | 20 | No |
| aggregate_theta_failure.json | 3 | 6 | 20 | No |
| root_tax_failure.json | 4 | 6 | 15 | No |
| global_decorrelation_failure.json | 4 | 6 | 15 | No |

Sources are under `evidence/certificates/customer_attraction/`. The two
three-player strategies may coincide; these rows count source runs, not four
distinct mathematical cones. Only distinct comparison supports were tested;
the script does not certify arbitrary comparison multisets. These are finite
numerical observations, with no rational dual proof and no universal claim.
Had a positive candidate occurred, the script would have rationalized it and
checked every resulting SPE slack exactly before saving it. None occurred.

The script was initially run on root_tax_failure before inferring k from the
complete action tree; that run exited on a missing optional terminal_counts
field and produced no mathematical result. The subsequent completed run uses
the corrected parser.

## Next work / cleaner handoff

An independent cleaner review of branch_transport's exact rank-at-most-one
obstruction has priority once its files are supplied. No shared mathematical
assets have been edited and no git operation has been run by this subagent.
