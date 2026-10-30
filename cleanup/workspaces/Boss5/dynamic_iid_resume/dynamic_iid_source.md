# History-dependent iid potential: an exact actual-prefix obstruction and the remaining global budget

2026-10-10. Research result from the read-only checkout `co-work-anl` at `8e214ad`.
The unrestricted aggregate bridges `W >= Z_n` and `W >= (1-1/(2n))Z_n`
remain unresolved. This note proves a finite counterexample to a proposed
state-local sufficient condition, including at a prefix on an actual complete
SPE path. It does not prove a counterexample to either aggregate bridge.

## 1. Model and background iid benchmark

There are `n >= 1` identical unit providers, a finite nonempty common catalog
of `m` labels, and unit customers compressed into nonnegative integer weights
`w_T`, where a nonempty type `T subseteq [m]` consists of the labels attracting
those customers. Repeated choices and identical coverage labels are allowed.
For each complete ordered history the pure strategy supplies one label. Every
node comparison is evaluated after the deviation followed by that same complete
strategy. All ties and all off-path histories are retained.

For a legal prefix `h`, put `r=n-|h|` and `p_T=number of earlier labels in T`.
For `q in Delta([m])` let `t_T=q(T)`. Define

\[
F_{r,p}(q)=\sum_T w_T\,\mathbb E[H_{p_T+B_T}-H_{p_T}],\qquad
 B_T\sim\operatorname{Bin}(r,t_T),
\]

\[
g_{r,p}(t)=\mathbb E\frac1{p+1+\operatorname{Bin}(r-1,t)},\quad
\alpha_a(q)=\sum_{T\ni a}w_Tg_{r,p_T}(t_T),
\]

\[
Z_{r,p}(q)=r\sum_Tw_Tt_Tg_{r,p_T}(t_T)
          =\sum_Tw_T\mathbb E\frac{B_T}{p_T+B_T}.
\tag{1}
\]

The last quotient is zero when both numerator and denominator are zero.
Set `Z_{0,p}=0`. These are remaining providers' total payments, not total
coverage when a nonempty prefix exists.

For `r>=1`, binomial differentiation gives

\[
\frac{d}{dt}\mathbb E[H_{p+\operatorname{Bin}(r,t)}-H_p]
 =r g_{r,p}(t).
\]

For `r>=2`, differentiating again gives

\[
-r(r-1)\,\mathbb E
\frac1{(p+1+\operatorname{Bin}(r-2,t))(p+2+\operatorname{Bin}(r-2,t))}<0.
\tag{2}
\]

Consequently `F_{r,p}` is concave, and a distribution maximizes it exactly
when

\[
\alpha_a(q)\le v,\quad q_a>0\Rightarrow\alpha_a(q)=v,
\qquad v=\sum_aq_a\alpha_a(q)=Z_{r,p}(q)/r.
\tag{3}
\]

These are the symmetric iid Nash conditions of the residual static game
with prefix loads fixed. Equation (2) makes all positive-weight `t_T` unique
among maximizers for `r>=2`, and hence makes `Z` unique. For `r=1`, `F=Z`
is linear and its maximum value is unique. Thus `Z_{r,p}(w)` is a well-defined
number even when the maximizing distribution is not unique. At the empty
prefix, `Z_{n,0}` is the original static iid coverage benchmark `Z_n`.

## 2. The failed local sufficient condition

A tempting way to prove the weaker aggregate bridge is to claim at each
actual decision node, with actual selected action `a`,

\[
u(h)\stackrel{?}{\ge}
\left(1-\frac1{2n}\right)
[Z_{r,p}(w)-Z_{r-1,p+\mathbf1_a}(w)].
\tag{L}
\]

Here `n` is the original total population, not the number `r` remaining.
If (L) held at every actual node, summing would telescope to the desired
aggregate bridge. The exact instance below disproves (L) on an actual SPE
path. Restricting it from arbitrary legal histories to actual histories does
not repair it.

## 3. A 60-customer, seven-label, five-provider complete SPE

Let old labels be `X0,X1,X2,Y0,Y1,Y2`, encoded `0,...,5`.
For every `x in X, y in Y`, include one customer of type `{x,y}`.
For every two-element `I subset X` and two-element `J subset Y`, include
three customers of type `I union J`. These give 36 old unit customers.
Add label `P=6`, attracting 24 new customers attracted by no old label.
There are five providers.

The full input is `actual_padding_input.json`. The complete pure strategy,
with all `1+7+49+343+2401=2801` decision histories, is stored in
`actual_padding_certificate.json`.

For a concise executable definition of that strategy, perform exact backward
induction on the entire ordered tree. At history `h`, replay each action's
already selected continuation and choose one maximizing the acting player's
final payoff. Resolve only exact ties by this priority list:

1. `P`, if fewer than two previous choices are `P`.
2. The old three-provider action applied to `h` after deleting all `P`
   entries, if that filtered history has length below three. The old action
   is `X0` at the empty history, the opposite group's smallest label after
   one old choice, and the second old choice's group's smallest unused label
   after two old choices.
3. All other labels in ascending order.

Every decision is an exact argmax. Therefore the constructed strategy is a
pure SPE at every ordered history. The separate definition-level audit reads
the frozen input and strategy, imports neither this construction nor a solver,
and checks all 19,607 action comparisons using integer shares scaled by 60.
The actual terminal is

\[
(P,P,X0,Y0,Y1),\qquad (u_1,\ldots,u_5)=(12,12,10,12,12),\qquad W=58.
\]

For transparency, actual-node deviation payoffs, in label order `0,...,6`, are:

| Actual prefix | Selected label | Seven deviation payoffs |
| --- | --- | --- |
| empty | P | `10,10,10,10,10,10,12` |
| P | P | `10,10,10,10,10,10,12` |
| P,P | X0 | `10,10,10,10,10,10,8` |
| P,P,X0 | Y0 | `9,12,12,12,12,12,8` |
| P,P,X0,Y0 | Y1 | `25/3,12,12,25/3,12,12,8` |

This table establishes the displayed path; the frozen complete strategy and
full audit establish all off-path SPE requirements.

## 4. Exact residual Nash values at the offending actual node

At actual prefix `(P,P)`, three providers remain. Give probability `1/6`
to each old label and zero to `P`. The old labels' expected unilateral static
payments are all `97/9`, whereas `P` gives `24/(2+1)=8`. Hence (3) proves
this distribution maximizes the residual `F`, and

\[
Z_{3,p(P,P)}=3(97/9)=97/3.
\]

At prefix `(P,P,X0)`, two providers remain. Give probabilities `1/2,1/2`
to `X1,X2`, and zero elsewhere. The seven expected payments are

\[
(9,21/2,21/2,10,10,10,8).
\]

Again (3) proves residual optimality, and `Z_{2,p(P,P,X0)}=21`.
Thus at the actual third player's node,

\[
u_3=10<\frac9{10}\left(\frac{97}3-21\right)
       =\frac{51}5,
\]

with exact violation `1/5`. No floating calculation enters this conclusion.

This is not an aggregate counterexample. The five-provider optimum is 60:
`P,X0,X1,X2` cover all customers and a repeated fifth action completes the
profile. Since any iid profile's expected coverage is at most this optimum,
`Z_5<=60`, and therefore

\[
W=58\ge\frac9{10}Z_5
\]

with certified slack at least four. No exact value for the root `Z_5` is
claimed.

The strong root comparison `W >= Z_5` has not been tested or decided in this
witness. Only the weak global comparison is certified by this upper bound.

## 5. What the global budget must carry

For any selected residual Nash distribution `q_h`, let

\[
A_h=\sum_Tw_T\mathbb E\frac{p_T}{p_T+B_T},\qquad
C_h=\sum_Tw_T\Pr(p_T+B_T>0).
\]

For the prefix-rent quotient specifically, `p_T=B_T=0` contributes zero
(`0/0=0`), so rent at the empty prefix is zero. The exact identity is

\[
C_h=A_h+Z_{r,p}(q_h).
\tag{4}
\]

`A_h` is all prefix providers' expected total payment, and `C_h` is complete
expected coverage. Residual `F` maximization does not maximize `Z` or `C`.
For example at `(P,P,X0)`, keeping the preceding uniform old distribution
would give remaining expected payment `194/9`, exceeding the residual
`F` maximizer's payment 21. The latter transfers more payment to the prefix.

The selected residual distributions in this example give:

| Prefix | Remaining `Z` | Prefix rent `A` | Complete expected coverage `C` |
| --- | ---: | ---: | ---: |
| P,P | `97/3` | `24` | `169/3` |
| P,P,X0 | `21` | `75/2` | `117/2` |
| P,P,X0,Y0 | `12` | `46` | `58` |
| P,P,X0,Y0,Y1 | `0` | `58` | `58` |

For the last-but-two, last-but-one, and last old providers, define
`d_h=Z_h-Z_child-u(h)`. Their exact debts are
`4/3,-3,0`, whose sum is `-5/3`. The positive early debt is repaid at a later
node. It cannot be assigned the original-total-`n` proportional local budget
in (L).

More generally, put `R_h=A_child-A_h-u(h)`. Equations (1) and (4) give

\[
u(h)-[Z_h-Z_{child}]=C_{child}-C_h-R_h.
\tag{5}
\]

Along a complete actual path, `sum R_h=0`: initially prefix rent is zero;
finally all welfare is prefix rent, and all actual provider payoffs sum to
welfare. Equation (5) is a legitimate global accounting identity. It proves
no sign for the summed coverage drift. A successful proof must bound total
debt or transfer it across nodes; the present exact failure rules out paying
it independently at each actual node using (L).

## 6. Exact unresolved matrix condition with changing backgrounds

Fix a full formal strategy `sigma` and a real probability field `q_h`, one
distribution for each decision history. Let `Gamma_sigma` retain every
individual SPE deviation row. For each `h,a`, define the residual stationarity
row

\[
E_{h,a;T}=\zeta_{h,T}-r\mathbf1_{a\in T}g_{r,p_T(h)}(q_h(T)),
\qquad
\zeta_{h,T}=r q_h(T)g_{r,p_T(h)}(q_h(T)).
\]

Then `E_h w>=0` is exactly residual symmetric iid Nash optimality, because
`sum_a q_h(a)E_{h,a}=0`. Let `c_sigma,T` indicate root terminal coverage.
For fixed strategy and field, the implication

\[
w\ge0,\quad\Gamma_\sigma w\ge0,\quad E_h w\ge0\ \forall h
\ \Longrightarrow\ (c_\sigma-\kappa_n\zeta_\varnothing)\cdot w\ge0,
\qquad\kappa_n=1-1/(2n),
\]

is equivalent, by finite Farkas duality, to

\[
\boxed{c_\sigma-\kappa_n\zeta_\varnothing
 =\Gamma_\sigma^T\lambda+\sum_hE_h^T\eta_h+r_0,
 \qquad\lambda,\eta_h,r_0\ge0.}
\tag{6}
\]

Each multiplier in `lambda` belongs to a specific history and a specific
individual deviation. No node-internal averaging has occurred. Every actual
instance admits a field of residual maximizers. Therefore certificates (6)
for every `n,m,sigma` and every real field would prove the weaker global
bridge, and the global bridge would conversely imply these certificates for
each field's feasible weight cone. The matrix entries are rational when the
field is rational; this does not justify restricting the universal field
quantifier to rational distributions.

The equivalence uses the nonnegative real-mass extension of the model. An
integer-customer global theorem would extend to that setting: the fixed
strategy SPE cone is rational polyhedral and has dense rational points;
clearing denominators handles those points, and the static benchmark is
continuous in weights because its value is unique across all concave-potential
maximizers. No approximation of a fixed irrational field is being assumed.

No uniform construction of (6), no global debt upper bound
`sum_actual d_h <= Z_n/(2n)`, and no aggregate counterexample has been obtained
in this task. The background iid stationary conditions, rent identities, and
actual-path failure of (L) are proved. Any claim beyond those requires new
cross-node budget control.

## 7. Reproducibility and scope of the checks

Run `python audit_actual_padding.py` from this directory. The audit verifies
all 2801 histories, all 19,607 action comparisons, both displayed residual
Nash distributions, all exact state values in the table, the `1/5` local
violation, `W=58`, and `OPT_5=60`. The construction script is
`actual_padding.py`. The finite certificate proves the stated finite
counterexample; it does not stand in for an arbitrary-population theorem.
No repository files were modified. No external peer review or novelty claim
is made.
