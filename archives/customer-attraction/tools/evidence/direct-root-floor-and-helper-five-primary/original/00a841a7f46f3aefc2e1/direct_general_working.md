# Direct adaptive-portfolio proof: the rent transfer is exact, the payment is not

2026-10-24. Arbitrary m, arbitrary finite common catalog, every complete
ordered-history pure SPE. **Q-CAG-HALF remains OPEN.** This is a working
attempt, not a new unconditional welfare approximation.

## 1. Fixing the general net target

Fix an actual complete SPE leaf z and an optimal m-tuple with union O. Write
B=union(z), R=O\B, E=B\O, W=|B|. The desired inequality is

\[
|R|-|E|\le W,
\]

equivalently |O|-W<=W. In particular a direct omission-only requirement
|R|<=W would be an unjustified strengthening; E must be retained.

One possible sufficient target is the actual-minimum net ROW. At a position
i with t=u_i=min_j u_j, let d_i(T) be the current player's payoff after
forcing T at the actual prefix and following the same original strategy.
For an optimal ordered m-tuple (T_1,...,T_m), the statement

\[
\sum_{j=1}^m d_i(T_j)\ge |O|-W\tag{ROW?}
\]

would imply |O|-W<=m t<=W by the m true IC inequalities. ROW? is a
sufficient auxiliary target here, not a proved assertion. No arbitrary
background or frozen-continuation version is being assumed.

## 2. Exact arrival-rent identity

For an arbitrary fixed preceding load b and a current entrant A, let Y be
any full later tuple. Define

\[
d_A(Y)=\sum_{x\in A}\frac1{1+b_x+c_x(Y)},\qquad
Q_A(Y)=\sum_{x\in A}\frac{b_x+c_x(Y)}{1+b_x+c_x(Y)}.
\]

Q_A(Y) is the combined payoff on A of all the other players in this same
terminal profile. Pointwise conservation gives

\[
d_A(Y)+Q_A(Y)=|A|.\tag{RENT}
\]

Thus for two different later tuples Y and Y',

\[
d_A(Y)-d_A(Y')=Q_A(Y')-Q_A(Y).\tag{TRANSFER}
\]

This keeps the earlier background in Q as well. It remains true when some
customers have zero previous load, A is empty, or themes repeat. On an
actual-omitted subset X=A\B the previous load is zero and RENT reads

\[
\sum_{x\in X}\frac1{1+c_x(Y)}
+\sum_{j\text{ later}}\sum_{x\in X\cap Y_j}
  \frac1{1+c_x(Y)}=|X|.\tag{NEW-RENT}
\]

So the loss in a deviator's query due to later crowding is exactly other
players' increased rent on that query. This is a valid whole-utility
identity; it does not identify the rent in a different branch with any
actual wallet.

## 3. What the attempted portfolio step would have required

The attempted argument chose a frozen portfolio q whose minimum payoff was
t, then tried to retain t as a future frozen response floor while a forced
comparator topic was being crowded. That floor is false: see
[the exact all-m star family](frozen_portfolio_floor_obstruction.md).
Replacing q by a full SPE's actual profile is a different statement and has
not been established here.

Even an available static response floor does not directly survive an
adaptive current choice. If an earlier player's true root action has
payoff at most t, only the originally prescribed continuation leaf is
subject to that cap. A descendant's alternative child is a different
history; the ancestor is not allowed to choose that descendant action.
The ancestor's cap therefore cannot be copied into all deeper children.
This is the same exact promise-reset issue recorded in the shared general
proof, now appearing in the portfolio language.

## 4. The unpaid quantity and the five-player substitution

For each T_j in ROW?, let Y_j^0 be the frozen actual later tuple and let
Y_j^sigma be the real later tuple after forcing T_j. Define

\[
\mathcal A_i
=\sum_{j=1}^m\left[Q_{T_j}(Y_j^\sigma)-Q_{T_j}(Y_j^0)\right]
=\sum_{j=1}^m\left[d_{T_j}(Y_j^0)-d_i(T_j)\right].
\]

The equality is TRANSFER, with the same actual preceding load in both
terms. Positive A_i is the adaptation loss of the entire comparator row.
It can contain positive and negative customer terms. This attempt supplies
no general bound paying A_i from the actual utilities and E. In particular
RENT does not justify summing different Y_j^sigma rents and paying the
sum with one actual player's or one actual customer's money.

At m=5, the true IC inequalities still give sum_j d_i(T_j)<=5t<=W.
Consequently ROW? would indeed yield OPT_5<=2W for every catalog and every
complete SPE. The exact arrival identity remains valid but has not paid
A_i, so the argument has not passed that pressure test unconditionally.

No finite scan, fixed-player expansion, external-stability assumption, or
background WP/Mfull floor was used. The all-m star family refutes only the
named static portfolio-floor step. It does not prove that all adaptive
portfolio mechanisms fail, nor refute ROW? or HALF.

## 5. Stronger root helper: FALSE, including a full m-slot comparison

A further helper considered in messages was

\[
\sum_{j=1}^{m}d_1(T_j)\ge
\left|\bigcup_{j=1}^{m}T_j\right|-K,
\qquad K=\max_{T\in\mathcal S}|T|.\tag{ROOT-K: FALSE}
\]

It is not an open route. Root supplied a named complete-SPE counterexample,
independently reconstructed here: m=6, six disjoint themes of sizes
(3,3,1,1,1,1). Full backward induction, comparing fully completed children
and breaking ties by smallest label, gives actual counts (3,3,0,0,0,0), W=6,
OPT=10, K=3. Each of the six true root query payoffs is 1, so the row is
6<10-3=7. All 9,331 ordered decision histories and 55,986 IC comparisons,
including the prescribed action, pass an exact independent reconstruction.

The actual net ROW has right side 10-6=4, and HALF has 10<=12, so both hold
on this instance. The counterexample only rejects replacing the actual
coverage credit W by the largest-theme credit K. Details, exact strategy
definition, and the audit are in
[the helper counterexample note](root_size_helper_counterexample.md).
