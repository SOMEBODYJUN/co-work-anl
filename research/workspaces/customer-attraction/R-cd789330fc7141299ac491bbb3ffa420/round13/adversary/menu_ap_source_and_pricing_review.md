# Independent review: menu AP sources and closed pricing

2026-10-25. Sources read: `../certificate/menu_ap_pricing.py`,
`../certificate/audit_menu_ap.py`, and the AP proof in
`R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation.md`.
No fatal mathematical issue was found in the extension below. This is a
source-node and algebraic pricing review, not a rerun of the full oracle,
an exact optimum certificate, or a five-provider half proof.

## AP and its source nodes

At any genuine decision history let p_x be old load, k>=2 remaining players,
and v the original strategy's prescribed current payoff. For legal themes C,D,
write `s=sum_C 1/(p+k)` and
`F=sum_(C intersection D)1/(p+k)+sum_(D minus C)1/(p+1)`.
The old arbitrary-theme AP statement with total-player bound M=5 is

`F <= s + [4(k-1)+k^2/2](v-s)`.

This need not choose a weighted-maximal C. The genuine deviation to C gives
v>=s. Independently rebuilding the proof: put e=v-s, force C and use the
original true continuation. Its weighted missing-C seat sum d satisfies
d<=4e. Every legal topic's outside-C weight is at most its missing-C weight
plus e. If d_L is the last follower's missing-C weight, the middle followers'
outside weight is at most d-d_L+(k-2)e. Last-follower optimality against D gives

`F <= v_C+(k/2)d+(k/2-5/4)d_L+(k^2/2)e`,

where s<=v_C<=v. For k>=3 use d_L<=d; for k=2 there are no middle followers
and d_L=d. This yields the stated coefficient. All followers are evaluated
on the true C-deviation branch. Coarsening a smaller load bound to M=5 is safe
because e>=0.

The code's seven sources are actual positions 1,2,3,4; second-path positions
3,4 after `(A,E)`; and third-path position 4 after `(A,B,E)`. These are genuine
optimizing nodes with k>=2. The forced second and third deviation actions and
all last-player sources are correctly excluded.

The AB/AE menus are the original final two replies after `(A,B,T_i)` and
`(A,E,T_i)`; Sbranch menus are the original final three replies after `(A,T_i)`.
Every menu action is a legal theme in the common catalog, hence may be C or D
at any source. Same-strategy construction preserves coincident histories;
repeated themes are retained as repeated indices in all sums.

## Root final-reply versus optimal menu

Set a=8(k-1)+k^2. The doubled per-client AP row is

`a v_x -[(a-2)c+2cd]/(p+k)-2d(1-c)/(p+1)`.

Its client sum is nonnegative; its individual client coefficients may have
either sign. At the root k=5,p=0,a=57 this is
`57u1-11|C|-2|D|+(8/5)|C intersection D|>=0`.

Take C over all five genuine Sbranch final replies J_i and D over all five
optimal topics T_j, independently. Let J_x and t_x be the two membership
counts. Summing all 25 legal pair rows and multiplying by five gives exactly

`7125u1-275 sum_x J_x-50 sum_x t_x+8 sum_x J_x t_x>=0`.

The equality-pattern i=j is included. This Cartesian sum factors through
counts and needs no unrecorded matching between menu indices.

## Closed pricing algebra

For lists of lengths n_C,n_D and client membership counts c,d, the Cartesian
sum has coefficient

`n_C n_D a v_x -(a-2)n_D c/(p+k)-2n_C d/(p+1)
 +2[1/(p+1)-1/(p+k)]cd`.

These are the constant, two linear, and one quadratic count terms used by
`ap_value` and `family_score`. New rows combine one recorded family with fixed
labels, the optimal list, or menus of that same family. Thus, fixing ten
original bits and optimal count t, each new objective depends on only one
complete family histogram. The three maximizations remain separable; old
ell,h menu variables are absent from these terms, preserving their affine
endpoint maximization. Fixed-label/optimal-optimal rows depend only on the
original bits and t and correctly enter the fixed base tensor.

The new cache key retains the old family key plus all new monomial
coefficients. The fixed base oldids append the corresponding extra tensor
columns, while cross-family inherited weights retain their original
557:717 indices. These structures agree with the algebraic separation.

This closes pricing only for this stated AP collection. Cross-family C,D
comparisons and full ordered-history continuation constraints are not thereby
represented. A rational ratio-above-two primal refutes this necessary-row
closure only. A universal bound additionally needs exact nonnegative dual
weights and full-domain residual certification; finite replay and floating
pricing do not provide those by themselves. No novelty claim is made for AP.
