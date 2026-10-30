# Sharp same-topic dilution for every decreasing Shapley marginal

Research proof, 2026-10-21. Identity **TC-DIL-1**: exact statement below.
Root and credible_search independently reconstructed the full clock coupling
and found no fatal objection; the latter's review is
`../credible_search/submodular_dilution_independent_review.md`. No external
review or global novelty claim. This is a representation comparison, not Q-CAG-HALF.

## TC-DIL-1: exact statement

Let P be a finite topic set and fix a in P. Let g be a nonnegative decreasing
function on subsets of P minus {a}: R subset S implies g(R)>=g(S)>=0.
For a nonnegative real rate vector q with q_a>0 define

\[
 L_a(q;g)=\int_0^\infty e^{-q_a t}
      \mathbb E[g(R_q(t))]dt,
\tag{1}
\]

where each b!=a enters R_q(t) independently by time t at exponential rate
q_b. A zero rate means it never enters. The integral is finite because
0<=g(R)<=g(empty) and q_a>0.

For another such vector r put

\[
 \kappa=\max_{T\subseteq P,\ a\in T}\frac{r(T)}{q(T)}.
\tag{2}
\]

Every denominator is positive. Then

\[
 \boxed{L_a(q;g)\le\kappa L_a(r;g).}
\tag{3}
\]

The constant is the sharp uniform constant over all nonnegative decreasing
g: choose a maximizing T, and let g(R)=1_(R avoids T minus {a}); then
L_a(q;g)=1/q(T), L_a(r;g)=1/r(T), so their ratio is kappa.

## Proof by a pathwise clock coupling

Set s=kappa q. By (2), s_a>=r_a. Let
D={b!=a:r_b>s_b}, delta_b=r_b-s_b for b in D, and take T={a} union D in (2).
This gives the stronger inequality

\[
 s_a-r_a\ge\sum_{b\in D}\delta_b.
\tag{4}
\]

Use the following mutually independent exponential clocks (zero rates are
omitted):

* a common kill clock of rate r_a for both processes;
* for each b!=a, a common b-activation clock of rate min(s_b,r_b);
* for each b with s_b>r_b, an extra b-activation clock of rate s_b-r_b
  in the s process;
* for each b in D, a clock of rate delta_b that both activates b in the r
  process and kills the s process;
* an extra s-kill clock of rate s_a-r_a-sum_(b in D)delta_b, nonnegative by (4).

Within the s process, its kill clock has total rate s_a and is independent
of all its activation clocks; every b has activation rate s_b. Within the
r process, its kill clock has rate r_a, independent of all its activation
clocks, and every b has activation rate r_b. Thus both marginal laws are
exactly the laws used in (1). Shared clocks only correlate the two processes.

Write A_s,A_r for the kill times. Always A_s<=A_r. Before A_s no r-only
activation clock has rung, since it would itself kill s. Consequently
R_s(t) contains R_r(t) whenever t<A_s. Therefore, pathwise,

\[
 \int_0^{A_s}g(R_s(t))dt
 \le\int_0^{A_r}g(R_r(t))dt.
\tag{5}
\]

Expectation and Tonelli identify these integrals with L_a(s;g) and L_a(r;g).
Changing time in (1) gives L_a(kappa q;g)=L_a(q;g)/kappa. This proves (3).

## Consequence for common monotone submodular moments

Let C(empty)=0 and let C be monotone and submodular. Its a-marginal
g(R)=C(R union {a})-C(R) is nonnegative and decreasing. The common Shapley
payoff representation in `common_shapley_coupling.md`, after t=exp(-u), is
precisely

\[
 U_a(q)=L_a(q;g).
\]

Hence every sharp same-topic customer dilution inequality

\[
 U_a(q)\le\max_{T\ni a}r(T)/q(T)\,U_a(r)
\]

already holds for common monotone submodular Shapley payoffs. Nonnegative
customer realizability is not needed.

The same conclusion holds for a truncated C defined only on |S|<=m, with
monotonicity and submodularity whenever the involved union has size<=m, when
q,r have integer total counts at most m. Only g-values on |R|<=m-1 enter
either marginal law. At the pathwise comparison in (5), R_r(t) is contained
in R_s(t), whose size is at most |supp(q) minus {a}|<=m-1; the required
decreasing comparison is therefore within the defined truncated domain.
Equivalently extend g decreasingly beyond that domain before coupling.

This means the explicit dilution constraints in the fixed-strategy
common-submodular LP are redundant. Its finite 3/2 result also holds for
that same complete strategy/T submodular relaxation without separately
imposing dilution. This remains one fixed-cone statement and does not
establish the proposed general full-tree submodular half theorem.

## Finite diagnostic

`dilution_marginal_probe.py --players 5 --topics 7` reduced all ordered
same-topic q,r pairs to 418 topic-permutation orbits and searched the cone
of decreasing marginals directly. It found no positive exact feasible
violation. This finite diagnostic is separate from the general coupling
proof; it is not used to infer the latter or to claim a universal bound.
