# Full-tree dual exploration: node-specific flow remains necessary

Repository is read-only. This report gives exact obstructions to two concrete
certificate templates. It does not prove or refute general aggregate
`W >= n v_n`, and does not use a query-independent optimal primal distribution
across a strategy cone.

## 1. Exact hybrid-flow identity

Fix complete ordered-history strategy sigma and a theme distribution q.
Let Z_k have its first k actions independently sampled from q, followed by
the genuine sigma continuation. Thus Z_0 is the actual terminal profile and
Z_n is iid q. At level k, write

`G_k = E_{h~q^(k-1),a~q} Gamma_(h,a) w >= 0`.

Every comparison in this expectation is a genuine full-tree incentive;
no future actions are frozen. Let `Phi(z)=sum_T w_T H_(load_T(z))` and

`Delta_(k,i)=E Phi(Z_(k-1) without position i)-E Phi(Z_k without position i)`.

Since an agent's payoff is exactly its harmonic-potential removal marginal,

`G_k=E Phi(Z_(k-1))-E Phi(Z_k)-Delta_(k,k)`.

The exact welfare identity

`W(z)=n Phi(z)-sum_i Phi(z without position i)`

therefore yields

`W(Z_0)-E W(Z_n) = n sum_k G_k + sum_k [(n-1)Delta_(k,k)-sum_(i!=k)Delta_(k,i)]`.

The iid endpoint welfare is `Psi_n(q)`. When q is a static symmetric mixed
Nash distribution it supplies a valid static security upper bound
`n v_n <= Psi_n(q)`, as independently proved by security_bridge. The final
delete-slot remainder above does not have a universal nonnegative sign.

## 2. Genuine SPE obstruction to the unmodified flow

Use the existing 36-client, three-player, six-theme instance and its original
complete strategy: root 0; second player selects the minimum opposite-group
theme; last player selects the minimum unused theme in the second player's
group. Use q uniform on all six themes. Direct Fraction computations give

| quantity | exact value |
| --- | ---: |
| actual terminal profile | (0,3,4) |
| W | 34 |
| Psi_3(q) | 97/3 |
| W-Psi | 5/3 |
| G_1 | 0 |
| G_2 | 1/2 |
| G_3 | 31/18 |
| sum G_k | 20/9 |
| target minus unit flow | -5/9 |
| target minus n-times flow | -5 |

All six static Nash inequalities are equalities at this point. Consequently,
if one fixes either the unit iid-prefix flow or its n-fold multiple, the
remaining vector cannot be supplied solely by nonnegative static-optimality
multipliers and nonnegative client residuals: its inner product with this
nonnegative actual SPE instance is already negative. A valid proof needs to
change the full-tree incentive allocation itself.

## 3. No arbitrary depth-only repair of this flow

The preceding overspending could conceivably be repaired by arbitrary
nonnegative depth coefficients a_k. This stronger template also fails for
the same formal strategy and q:

`c-psi(q) = sum_(k=1)^3 a_k G_k + E(q)^T eta + r`,

where `a_k,eta,r >= 0`, G_k denotes the entire level-averaged vector, and
E(q) is the static Nash matrix. The following exact nonnegative integer
client vector separates the proposed cone:

| interest mask | mass |
| --- | ---: |
| 4 | 11988 |
| 25 | 17316 |
| 26 | 12481 |
| 29 | 7312 |
| 34 | 19357 |
| 37 | 12481 |

The total is 80935. Independently rebuilding all utility vectors gives

`E(q) w = 0`,

`(G_1 w,G_2 w,G_3 w)=(0,0,607489/216) >= 0`,

but `W-Psi_3(q)=-472195/36 < 0`.

This is an exact impossibility certificate for every choice of a_k and eta
in this depth-only template. It is intentionally not a counterexample to
SPE welfare: the full strategy has 57 negative incentive rows on this
vector; root deviation to 1 gains 2827 and deviation to 2 gains 6216. The
full tree contains essential node-specific information that iid layer
averaging removes. The known node-specific conditional-cone certificate for
this sigma,q is consistent with this obstruction.

The obstruction can be strengthened while retaining all 43 separate nodes.
Set `M_h=(1/6)sum_a Gamma_(h,a)` and allow arbitrary nonnegative multipliers
on every M_h, together with arbitrary static E multipliers and residuals.
This also cannot certify c-psi for this formal sigma,q. The independent
verifier contains a 15-positive-type integer separation vector with
`M_h w>=0` at every node and `E(q)w=0`, but
`(c-psi)w=-1085816540911589/12<0`. Thus node-specific weights alone are
insufficient if each node still averages all deviations using the same q:
the proof must retain deviation-specific weights or change its static
background construction. The large integer masses are a recovered exact
LP vertex, not a minimality claim; the smaller six-type separator above is
the simplest displayed obstruction.

## 4. Actual-terminal deletion is a separate failed template

For Q_del uniform over the n ways of deleting one action from actual z,
the harmonic identity simplifies exactly to

`W(z)-n beta_(Q_del)(p) w = n[Phi(z)-E_(i uniform,a~p) Phi(z with position i replaced by a)]`.

Hence using Q_del requires aggregate frozen potential non-improvement,
which SPE does not guarantee. Already with two players and three themes,
take interest masses `{B}:1`, `{A,C}:2`, `{B,C}:2`. Let root choose A and
last responses be A->B, B->C, C->C. All 12 full-tree comparisons pass;
actual profile AB has payoffs (2,3), W=5. Querying C against Q_del gives 3,
which exceeds W/2=5/2. Both the pure query C and pure static background C
certify v_2=2, so this is not an aggregate security counterexample.

The obstruction is minimal in player and theme counts: one player is
trivial, and with two players and two themes the deletion certificate
always works. For two themes with exclusive masses x,y and common mass z,
a repeated actual theme gives the required cap directly from the last
player's best response. For actual AB, the last best response gives
y>=x/2. If after B the last player chooses A, root optimality gives x>=y;
if it chooses B, last and root optimality together give y=2x. In either
case x<=2y and y<=2x, which are precisely the two uniform-deletion cap
inequalities. No assertion of minimal client count is made.

## 5. Two-player stationary interface (existing one-follower mechanism)

This section records a useful certificate form, not a new main theorem.
For n=2 let b(a) be the specified last-player response after root action a,
and choose any stationary probability pi for the deterministic map b,
so `b_push(pi)=pi`. Such pi exists by taking a cycle. For every query t,

`u_root-f_pi(t) = sum_a pi_a Gamma_(root,a) + sum_a pi_a Gamma_(history a,t)`.

The identity holds pointwise in every client type: the difference between
root and last utility on terminal (a,b(a)) is `|a|-|b(a)|`, whose pi average
vanishes by stationarity. This proves one fixed, fully static Q=pi caps
all queries throughout the entire two-player strategy cone. For the actual
last player use Q concentrated on actual root action. Averaging these two
static backgrounds yields the full aggregate certificate with r=0.
It does not extend by replacing b(a) with a tuple of later responses:
action-marginal stationarity no longer equates role utilities, and the known
three-player root-menu failures explicitly expose that distinction.

## 6. Status and verification

The universal node-specific gluing remains unproved. The strongest useful
deduction here is negative but concrete: a proof cannot collapse all
off-path constraints to iid prefix averages by depth, even after freely
using static Nash optimality. It must preserve or recreate the individual
node budgets, or choose another static Q rather than the iid benchmark.

Run `python verify_flow_barriers.py`. The verifier uses only the standard
library and exact Fraction arithmetic; it imports no repository solver or
saved policy. It reconstructs the genuine SPE, the static Nash rows, both
flow barriers, all negative rows of the separation vector, the deletion
obstruction, and the exact hybrid identity independently.
