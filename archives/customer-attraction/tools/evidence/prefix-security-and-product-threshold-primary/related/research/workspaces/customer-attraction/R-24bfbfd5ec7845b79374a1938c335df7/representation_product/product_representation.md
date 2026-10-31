# Cartesian menus: exact additive and price-convolution representations

2026-10-21. Analytic representation lemma, not a proof of Q-CAG-HALF. The original finite unit-customer/common-menu/full-history pure-SPE model is retained. No external review or novelty certification is claimed.

## Objects

Take k finite CAG instances G_j with the same number m>=1 of unit providers. Their customer sets N_j are disjoint. Each has a finite nonempty menu S_j consisting of distinct customer subsets. Define the product instance by

\[
 N=\bigsqcup_{j=1}^kN_j,\qquad
 S=\left\{\bigsqcup_j A_j:A_j\in S_j\right\}.
\]

Product themes are distinct: if tuples differ in coordinate j, their coverage differs inside N_j. Empty component themes cause no difficulty. All customers remain separate unit customers.

For each component define its fractional capped-coverage curve and price envelope, for t,v>=0,

\[
 F_j(t)=\max_{z\ge0,\ \sum_Az_A=t}
 \sum_{x\in N_j}\min\left(1,\sum_{A\ni x}z_A\right),\qquad
 B_j(v)=\sup_{t\ge0}[F_j(t)-vt].
\]

These expressions use fractional weights only as comparison objects. Providers in the game still select one pure theme each.

## P1: full-policy products, welfare, optimum, and security

Given one complete pure SPE sigma^j in each component, there is a complete pure SPE in the product instance: after each full ordered tuple history, project that history into each coordinate and follow the corresponding original sigma^j. Every provider's final utility is the sum of its coordinate utilities. At every history, a deviating tuple changes each coordinate according to that coordinate's same complete policy, so its utility gain is the sum of nonpositive component gains. This checks every ordered history and does not identify histories with equal count vectors.

For the resulting product policy,

\[
 u_i^{\rm prod}=\sum_j u_i^j,\qquad
 W^{\rm prod}=\sum_jW_j,\qquad
 \operatorname{OPT}_m^{\rm prod}=\sum_j\operatorname{OPT}_m^j.
\]

The optimum equality holds independently of policies. A tuple profile projects to m feasible choices per component, giving the upper bound. Pair each component's m optimal choices by provider index to attain the sum.

The oblivious static security value is additive as well:

\[
 v_m^{\rm prod}(0)=\sum_jv_m^j(0).
\]

For the lower bound, independently sample each coordinate's optimal query distribution. Every fixed product background projects to a legal m-1-action background in each component, so expected payoffs sum to at least the claimed value. For the upper bound, independently sample component optimal opponent-background distributions and pair their m-1 coordinates by index into product themes. This is a legal background distribution independent of the query; it caps every pure tuple query by the sum. Both distributions are ordinary finite minimax strategies, not additional provider strategies.

## P2: exact shared-mass coverage curve

For every t>=0,

\[
 \boxed{F_{\rm prod}(t)=\sum_jF_j(t).}
\]

Every product weight array z has coordinate marginals z^j of the same total mass t. A customer's fractional load depends only on its component marginal, so its total coverage is at most the sum of the component maxima.

Conversely, for t>0 take maximizing marginals z^j, and couple them by

\[
 z_{A_1,\ldots,A_k}=\frac{\prod_j z^j_{A_j}}{t^{k-1}}.
\]

Its marginals are exactly the selected z^j, and hence it attains the sum. At t=0 every weight is zero. This argument is exact, uses no strategic independence assumption, and concerns the menu alone.

## P3: exact nonnegative price splitting

For every v>=0,

\[
 \boxed{B_{\rm prod}(v)=
 \min_{v_j\ge0,\ \sum_jv_j=v}\sum_jB_j(v_j).}
\]

The minimum is attained. One direction follows at once from P2: for every admissible split and every t, sum_j F_j(t)-vt <= sum_j B_j(v_j).

For completeness, each F_j is continuous, piecewise linear, concave, nondecreasing, and eventually constant. Concavity follows by mixing feasible weight arrays and the concavity of capped coverage; piecewise linearity follows from the finite linear formulation with variables for the capped customer loads. It saturates by t=|S_j| because weight one on every component theme covers every coverable customer, and additional mass can be placed on any theme.

If v=0, choose v_j=0; eventual saturation gives equality directly. If v>0, choose a maximizer t_* of sum_j F_j(t)-vt, which exists by eventual saturation. If t_*>0, its maximizing condition is

\[
 \sum_j F'_{j,+}(t_*)\le v\le\sum_jF'_{j,-}(t_*).
\]

The one-sided slopes are nonnegative. Choose v_j inside each interval [F'_{j,+}(t_*),F'_{j,-}(t_*)] so that their sum is v. Each chosen slope supports the concave F_j at t_*, whence B_j(v_j)=F_j(t_*)-v_jt_*. Summing proves equality. If t_*=0, v>=sum_jF'_{j,+}(0); choose v_j>=F'_{j,+}(0) with sum v. These are supporting slopes at the left endpoint, so every B_j(v_j)=F_j(0)=0, again giving equality.

## P4: the minimum-player price budget tensorizes for product policies

Let a_j=min_i u_i^j in each component policy. Suppose that each selected component policy obeys B_j(a_j)<=W_j. Its componentwise product policy then obeys the same minimum-player price budget:

\[
 B_{\rm prod}(\min_i u_i^{\rm prod})\le W^{\rm prod}.
\]

Indeed, min_i sum_j u_i^j >= sum_j min_i u_i^j = sum_j a_j. Every B is nonincreasing. Applying P3 with the split a_j therefore gives

\[
 B_{\rm prod}(\min_i u_i^{\rm prod})
 \le B_{\rm prod}(\sum_ja_j)
 \le\sum_jB_j(a_j)\le\sum_jW_j.
\]

Thus taking naive independent products of already-valid component policies cannot create a counterexample to the open minimum-player price budget. Welfare ratios also only average component ratios, and aggregate security gaps simply add.

## Boundary: arbitrary product-game SPE need not be componentwise policies

P1 is a one-way construction. The definition of complete pure SPE in the product instance permits a continuation choice in coordinate j to depend on the entire history in every coordinate. A unilateral coordinate change can therefore change future outcomes in other coordinates, so one cannot project an arbitrary product-game SPE and declare each projection an SPE. No converse decomposition or theorem for those coupled policies is claimed. Any product-based amplification beyond P4 must use this missing coupling mechanism or a different menu restriction.

The usual fractional price-envelope definition is the same one used in the current penultimate-price work; this note provides its exact menu-product behavior. It neither proves B(min_i u_i)<=W in the original model nor produces a half-coverage counterexample.
