# Equal movable weights: an unconstrained flow selector for every greedy box

Version 1, 2026-10-07. This note independently reconstructs the user's
[equal-weight source argument](../../../history/source/notes/multi_facility/equal_light_flow_pro_report_2026-10-07.md).
The two claim IDs below distinguish an abstract
on-path selector from its original-model factor-two corollary. No external
peer review or literature-priority certification is claimed.

The MF-MODEL input class was already covered by
[`SC-K-UNIFORM-LIGHT-FLOW-2`](polytime_frontier.md#sc-k-uniform-light-flow-2-partial-overlaps-without-a-common-anchor).
The present contribution is an **unconstrained** selection theorem: every
global minimizer automatically has both greedy boxes and the home condition
(H), without lower-bound constraints in the flow network. Section 8 gives
the exact relation to the older objective. This does not settle the general
unequal-movable-weight polynomial-time problem.

## 1. `SC-K-EQUAL-LIGHT-FLOW-BOX`: precise input and conclusion

There are explicitly listed sites \(1,\ldots,m\), with \(m\ge1\), positive
integer multiplicities \(q_1\ge\cdots\ge q_m\), and rational numbers
\(0\le c_t\le1\). There are \(n\ge0\) individually labeled movable
customers. Each has the same rational weight \(0<\delta<1\), a nonempty
allowed **set** \(A_i\subseteq\{1,\ldots,m\}\), and home
\(h_i=\min A_i\). Every original allowed site remains available in every
deviation test. Repeated site entries in an input row represent one set
element; repeated customer types remain different labeled customers. Set

\[
\begin{aligned}
H_t&=\#\{i:h_i=t\},&
N_t(a)&=\#\{i:a_i=t\},\\
b_t&=c_t-\delta H_t,&
X_t(a)&=b_t+\delta N_t(a),
\end{aligned}                                                     \tag{1}
\]

for a complete allowed assignment \(a\in\prod_i A_i\). Negative \(b_t\)
are permitted: these are offsets in a normalized surplus, not physical
background loads. The home assignment has \(X_t(h)=c_t\).

Define, on **all** allowed assignments, with no box constraints,

\[
\Psi(a)=\sum_{t=1}^m
 \frac{b_tN_t(a)+\delta N_t(a)(N_t(a)-1)/2}{q_t}.                    \tag{2}
\]

**Theorem (`SC-K-EQUAL-LIGHT-FLOW-BOX`).** Every global minimizer of (2)
satisfies all of

\[
\begin{split}
&0\le X_t\le1 &&(t=1,\ldots,m),                                  \tag{B}\\
&\frac{X_{a_i}-\delta}{q_{a_i}}\le\frac{X_v}{q_v}
  &&(i=1,\ldots,n,\ v\in A_i),                                   \tag{NE}\\
&\frac{X_{a_i}-\delta}{q_{a_i}}\le\frac{1-\delta}{q_{h_i}}
  &&(i=1,\ldots,n).                                               \tag{H}
\end{split}
\]

A minimizer can be constructed in time polynomial in the joint binary
input length, using a unit-capacity minimum-cost flow with exactly \(n\)
unit augmentations. Multiplicities are binary integers; this abstract
selector does not expand \(q_t\) into individual facilities. The correctness
proof also works for real \(c_t,\delta\); the bit-complexity assertion uses
rational input. When \(n=0\), the empty assignment gives \(X=c\), (NE)
and (H) are vacuous, and no augmentation is required.

## 2. Exact deviations and labeled home edges

If one customer moves from \(s\) to a distinct allowed site \(t\), direct
subtraction of (2) gives

\[
\Psi(a')-\Psi(a)
 =\frac{X_t(a)}{q_t}-\frac{X_s(a)-\delta}{q_s}.                     \tag{3}
\]

Consequently every global minimizer satisfies (NE). There is no restriction
that this trial move preserve a box or (H). The comparison with \(v=a_i\)
is automatic because \(\delta>0\).

For each away customer draw a **labeled** edge \(h_i\to a_i\); omit home
loops. The resulting directed multigraph is acyclic, because every edge
strictly increases the site index. Parallel edges are distinct customers.
At a site write \(\operatorname{in}(t)\) and
\(\operatorname{out}(t)\) for the numbers of these incoming and outgoing
edges. Then

\[
X_t=c_t+\delta\bigl(\operatorname{in}(t)-\operatorname{out}(t)\bigr).
                                                                    \tag{4}
\]

On a directed path, return each selected edge's customer from its current
site to its own home. This is a single simultaneous comparison of two
legal assignments, not a claim that individual returns improve utility.
Its customers are distinct: a strictly increasing site path cannot repeat
an edge, and each customer supplies exactly one edge. Each selected home
belongs to that customer's full allowed set. Intermediate sites lose one
and gain one customer of the same weight, so their counts, loads and
contributions to (2) are unchanged. The unrestricted domain in Section 1
allows the comparison without imposing intermediate box feasibility.

## 3. First path: the lower box

Suppose a global minimizer has \(X_s<0\). Equation (4) and \(c_s\ge0\)
imply that \(s\) has an outgoing edge. Follow outgoing edges until a site
\(z\) with no outgoing edge is reached. Acyclicity makes this a simple
finite path, of length at most \(m-1\), and \(z\) has at least the final
incoming edge. Therefore

\[
X_z=c_z+\delta\operatorname{in}(z)\ge\delta.                       \tag{5}
\]

Return the path customers simultaneously. Only the endpoint counts change:
\(s\) gains one customer and \(z\) loses one. By the marginal costs in
(3), the objective difference is

\[
\Delta\Psi=\frac{X_s}{q_s}-\frac{X_z-\delta}{q_z}<0.               \tag{6}
\]

The first term is strictly negative and the second is nonnegative. This
contradicts global minimality, proving \(X_t\ge0\) at every site. This
part of the argument needs no ordering of the multiplicities.

## 4. Second path: (H) and the upper box

Suppose an away customer \(i\), currently at \(t\), violates (H), so

\[
e_i:=\frac{X_t-\delta}{q_t}>
       \frac{1-\delta}{q_{h_i}}.                                 \tag{7}
\]

Start from \(u=h_i\). There is already a selected outgoing edge from
\(u\) toward \(t\). If \(X_u\le1-\delta\), stop. Otherwise \(u\)
must have an incoming away customer: without one, (4) and the selected
outgoing edge give

\[
X_u=c_u-\delta\operatorname{out}(u)\le1-\delta,
\]

a contradiction. Select one such incoming edge and continue to its home.
Each backward step strictly decreases the site index, and each newly
visited site again has a selected outgoing edge. The procedure must stop
at a site \(z\) satisfying

\[
X_z\le1-\delta,\qquad q_z\ge q_{h_i}.                             \tag{8}
\]

Indeed, an earliest visited site cannot continue without an incoming edge;
the preceding implication forces it to meet the stopping test. Read in
the forward direction, the selected edges form a simple path
\(z\to\cdots\to h_i\to t\), including customer \(i\). Return all its
customers. Only \(z\) gains one customer and \(t\) loses one, giving

\[
\begin{aligned}
\Delta\Psi
 &=\frac{X_z}{q_z}-e_i\\
 &\le\frac{1-\delta}{q_z}-e_i\\
 &\le\frac{1-\delta}{q_{h_i}}-e_i<0.                              \tag{9}
\end{aligned}
\]

Here \(1-\delta>0\) and the nonincreasing multiplicity order justify
the second comparison, including equal multiplicities. This proves (H)
for every away customer.

If some site \(t\) had \(X_t>1\), then (4) and \(c_t\le1\) would
give an incoming away customer \(j\). Since \(h_j<t\) and
\(q_{h_j}\ge q_t\),

\[
\frac{X_t-\delta}{q_t}>
\frac{1-\delta}{q_t}\ge
\frac{1-\delta}{q_{h_j}},                                        \tag{10}
\]

contradicting the result for away customers. Thus \(X_t\le1\) everywhere.
A home customer's (H) now follows directly from
\((X_{h_i}-\delta)/q_{h_i}\le(1-\delta)/q_{h_i}\). Together with
Sections 2--3 this proves every conclusion for **every** global minimizer.

Zero surplus, \(c_t=0\), \(c_t=1\), exact best-response ties, equal
multiplicities and equality in (H) cause no failure: each contradiction
starts with a strict violation. No tie-breaking assumption selects a
preferred global minimum.

## 5. Integral flow encoding and the complete augmentation argument

Let \(E=\sum_i|A_i|\) and \(M_t=\#\{i:t\in A_i\}\). Construct a
network with source \(S\), one node per individual customer, one node per
site, and sink \(T\). Every edge below has unit capacity:

* \(S\to i\), with cost zero, for each customer;
* \(i\to t\), with cost zero, for every original allowed incidence;
* \(M_t\) parallel edges \(t\to T\), with costs
  \(d_{t,\ell}=(b_t+(\ell-1)\delta)/q_t\),
  for \(\ell=1,\ldots,M_t\).

There are \(V=n+m+2\) vertices and \(R=n+2E\) forward edges. Sending
\(n\) units is feasible: assign each customer to any allowed site and
use distinct slots at that site. Capacity \(M_t\) suffices because only
those \(M_t\) customers can select \(t\).

Any integral flow of value \(n\) assigns exactly one whole customer to
exactly one allowed site. Identical weights and identical allowed sets do
not merge customer identities. If a site receives \(N_t\) units, a
minimum-cost flow uses its first \(N_t\) slots: an unused earlier slot
could replace a used later slot without changing any other edge, and the
slot costs are strictly increasing. Their sum is exactly the \(t\) term
of (2). Conversely, every assignment yields a prefix-slot flow of that
cost. Thus minimum-cost integral flows and minimizers of (2) correspond
under extraction of the assigned sites; extraneous nonprefix flows cannot
be optimal.

For completeness, the following algorithm handles negative slot costs and
gives the total, rather than per-iteration, bound. Start with zero flow.
For \(r=0,\ldots,n-1\), find a shortest \(S\)-\(T\) path in the
residual network, and augment one unit. Reverse residual edges carry
the negative of their forward cost.

Initially the forward network is acyclic, so its residual network has no
negative cycle. Inductively, a flow is minimum-cost among flows of its
current value if and only if its residual network has no negative-cost
cycle. The forward implication follows by augmenting a negative cycle;
the reverse implication follows by decomposing the difference from any
same-value competitor into residual cycles. If the current flow is
minimum-cost at value \(r\), the difference from any integral flow of
value \(r+1\) decomposes into an \(S\)-\(T\) residual path and
residual cycles. Its cost is at least the shortest-path cost, since the
cycles are nonnegative. Augmenting a shortest path therefore gives a
minimum-cost flow of value \(r+1\), with no negative residual cycle.
Such a path exists whenever \(r<n\), because a feasible value-\(n\)
flow exists. This proves the invariant and final optimality.

Use Bellman--Ford on the integer-scaled costs in Section 6. It tolerates
negative edges; no Dijkstra assumption is being made. A shortest path
may be chosen simple. For a completely explicit tie-safe extraction,
compute shortest distances, then search the residual edges satisfying
\(d(v)=d(u)+c(u,v)\) for a simple source-to-sink path. This avoids any
ambiguity from zero-cost cycles in a predecessor graph. Fixed vertex and
edge orders make the algorithm deterministic without perturbing costs.

The canonical implementation instead retains predecessor edges only on
strict distance decreases. This is also safe at zero-cost ties. At the end
of Bellman--Ford every retained predecessor edge is tight: the destination's
last update used an earlier predecessor distance, while the final shortest
labels satisfy the opposite inequality. If the predecessor distance had
strictly decreased after that last update, tightness would fail. Thus the
predecessor's last decrease occurs strictly before the destination's last
decrease. Timestamps decrease along a backward predecessor chain, so it
cannot cycle and must reach the source. Updating predecessors on equal
distances would invalidate this argument and is not done.

Every residual capacity is one, every augmentation raises the flow value
by one, and the target value is \(n\). Thus exactly \(n\) augmentations
are made, irrespective of the numeric sizes of the weights or costs.
Bellman--Ford uses \(O(VR)\) additions and comparisons per augmentation;
path extraction and updating use \(O(V+R)\). For \(n\ge1\), the total
is

\[
O\bigl(m+E+n(n+m+2)(n+E)\bigr)                                   \tag{11}
\]

integer operations, plus polynomial input validation and scaling. With
\(n=0\), return immediately after reading the site data. No customer
improvement trajectory is simulated or bounded by this algorithm.

## 6. Input-bit complexity, including very large multiplicities

Let \(B\) be the total binary input length, including rational numerators
and denominators, all \(q_t\), all individual customers and all incidences.
Put

\[
D=\operatorname{lcm}\bigl(\operatorname{den}(\delta),
                    \operatorname{den}(c_1),\ldots,
                    \operatorname{den}(c_m)\bigr),\qquad
L=D\operatorname{lcm}(q_1,\ldots,q_m).                             \tag{12}
\]

The logarithm of an lcm is at most the sum of the input logarithms, so
\(\log L=O(B)\). Repeated integer gcd/lcm computations have polynomial
bit complexity. Since \(D c_t,D\delta\) and \(L/(Dq_t)\) are integers,
every scaled slot cost \(L d_{t,\ell}\) is an integer. Neither capacities
nor customers are multiplied by \(D\) or \(L\).

For \(1\le\ell\le M_t\le n\),

\[
\left|b_t+(\ell-1)\delta\right|
 =\left|c_t+\delta(\ell-1-H_t)\right|\le n+1.
\]

Hence every scaled residual cost has magnitude at most
\(C=L(n+1)\), and therefore \(O(B+\log(n+1))\) bits. A finite shortest
distance has a simple realizing path of at most \(V-1\) edges, so its
magnitude is at most \((V-1)C\). Synchronous Bellman--Ford labels also
represent walks of at most \(V-1\) edges and satisfy this bound; an
in-place implementation still has polynomial-length arithmetic operands,
since at most \(O(VR)\) relaxations can extend a represented walk in one
call. A flow uses at most \(n\) priced slots, so its total cost has
magnitude at most \(nC\). Stored counts, residual capacities and edge
indices have polynomial bit length as well.

Thus every arithmetic operation counted in (11) acts on polynomial-bit
integers, and the entire computation, not only each augmentation, has
input-bit-polynomial time and space. For example, an exponentially large
binary-encoded \(q_t\) changes cost bit lengths, but creates no additional
nodes, edges or augmentations. Exact output loads and objective values
also have polynomial bit length. This is not a loop bounded by a numerical
denominator, a potential range, or \(\sum_t q_t\).

## 7. `SC-K-EQUAL-LIGHT-FLOW-2`: the MF-MODEL corollary

**Input class.** Use [MF-MODEL](model.md), with positive binary-rational
atomic weights \(u_i\), explicit site incidence, a common finite catalog,
and explicitly listed \(k\ge2\) labeled facilities. Run canonical
`SC-K-GREEDY-BUDGET` with its fixed site tie order. Let \(O\) be the
occupied sites, \(J_t^0\) the original customer pools, \(W_t^0\) their
weights, \(q_t\) the final multiplicities and \(\gamma\) the last
insertion score. Freeze every served one-occupied-option customer and
every served customer of weight at least \(\gamma\) at its original
site. Require all remaining movable customers, if any, to have one common
weight \(u\). There is no bound on customer count, incidence structure,
treewidth, path depth, multiplicity diversity or the weights of frozen
customers.

**Corollary (`SC-K-EQUAL-LIGHT-FLOW-2`).** Throughout this recognizable
class, the same greedy labeled layout has an input-bit-polynomially
constructible full-box exact site-pure/within-site-independent-uniform
customer NE, with the frozen customers retained. Jointly with
`SC-K-GREEDY-BOX-TO-2`, it has a polynomially represented complete exact
customer-equilibrium continuation under which every facility's unilateral
deviation revenue is at most twice its on-path revenue. This mathematical
complexity assertion uses the polynomial off-path and default scheduling
primitive specified by BOX-TO-2.

**Forward normalization.** For positive maximum reach, greedy gives
\(\gamma>0\) and

\[
q_t\gamma\le W_t^0\le(q_t+1)\gamma,
\qquad N_v\le\gamma\quad(v\notin O),                             \tag{13}
\]

where \(N_v\) is the newly served weight at an unopened site. Each
customer's original pool home has maximum accessible occupied
multiplicity. Sorting occupied sites by decreasing final multiplicity,
then by opening order for ties, makes that home the smallest index in
its complete occupied-option set. The greedy score comparisons proving
these facts are reconstructed in
[the forward normalization](greedy_box_global_progress.md#7-forward-normalization-of-the-original-common-catalog-model).
Set

\[
\delta=u/\gamma\in(0,1),\qquad
c_t=W_t^0/\gamma-q_t\in[0,1].                                    \tag{14}
\]

The flow theorem now applies, and its selected assignment has actual
site total

\[
W_t=\gamma(q_t+X_t),\qquad
q_t\gamma\le W_t\le(q_t+1)\gamma.                                \tag{15}
\]

For a movable customer at \(s\), uniform independent choice among its
site's facilities yields conditional source cost
\(u+(W_s-u)/q_s\), and conditional cost \(u+W_v/q_v\) at an alternative
site \(v\). Their comparison is exactly (NE), after cancelling the
common term \(u+\gamma\). A frozen one-option customer has no other
occupied site. A frozen customer of weight \(u_i\ge\gamma\) at \(s\)
satisfies

\[
\frac{W_s-u_i}{q_s}\le\gamma\le\frac{W_v}{q_v}
\]

at every alternative occupied site. All facilities within a customer's
assigned site have equal conditional cost. Thus the entire profile is
an exact MF-MODEL customer NE, including all original alternatives.

**Joint off-path premises.** Apply
[`SC-K-GREEDY-BOX-TO-2`](polytime_frontier.md#sc-k-greedy-singleton-reset-and-sc-k-greedy-box-to-2)
to (15). For a departing facility at a site of multiplicity at least two,
its on-path revenue \(a=W_s/q_s\ge\gamma\) supplies the surviving-source
packing budget; all other site pools have the required upper budget.
For a singleton source, the original-pool reset lemma handles the
disappearing site and surviving orphans. The packing lemma and
`MF-PURE-CAP-POLY` then construct a pure exact customer NE at each actual
deviation, with deviator revenue at most \(2a\). This step does not use
(H). A fixed polynomial pure-NE default handles every other queried
layout. There are at most \(k(|S|-1)\) actual nontrivial deviations, and
distinct single-coordinate deviations yield distinct labeled layouts.
The finite table of these entries, the on-path profile, and a default
algorithm form one complete continuation; no exponential table of all
layouts is printed.

The greedy pass, normalization, flow call and polynomially many completion
calls all have polynomial bit complexity in the **explicit** MF input.
Unlike the abstract selector, this full-model conclusion measures time
polynomially in \(k\), not in \(\log k\) for succinctly encoded facilities.
Zero maximum reach is handled before division by \(\gamma\): every
layout and continuation then has no served customer and zero revenue.
If reach is positive but there are no movable customers, the greedy
assignment itself already satisfies the box and exact NE conditions.

The canonical complete executable still uses finite cap-preserving pure
improvements for actual deviations and finite pure improvements for its
default. Those routines are not the imported polynomial scheduling
algorithm. A polynomial on-path flow implementation therefore does not
by itself make the executable's entire continuation runtime polynomial.

## 8. Relation to the older flow theorem and the unequal-weight boundary

Let \(P_t\) be the frozen physical weight at site \(t\). From (14),
\(P_t/\gamma=q_t+b_t\). The older lower-constrained objective (31F),
using physical common weight \(u=\gamma\delta\), obeys

\[
\frac{F(a)}{\gamma}
 =\sum_t\frac{(q_t+b_t)N_t+
                   \delta N_t(N_t-1)/2}{q_t}
 =n+\Psi(a).                                                       \tag{16}
\]

The former lower constraints say precisely \(X_t\ge0\). Section 3
proves that every unconstrained minimizer already satisfies them, so the
old constrained problem and the new unconstrained problem have the same
set of optimal assignments. The new proof also supplies (H) to all those
optima. It removes lower-bound machinery and strengthens the abstract
selector statement; it does not enlarge the old MF equal-light input
class or remove its equal-weight hypothesis.

**Global optimization cannot be replaced by arbitrary customer NE.**
There is a strict greedy realizable counterexample with
\(q=(3,2,1,1)\), \(c=(1/10,1/10,1/25,0)\), \(\delta=1/2\),
and menus \(\{1,2\},\{2,3\}\). In the following table the two entries
are the assigned sites of the two labeled movable customers:

| Assignment | \(\Psi\) | \(X\) | Exact NE | Full box |
| --- | --- | --- | --- | --- |
| \((1,2)\) | \(-1/3\) | \((1/10,1/10,1/25,0)\) | yes | yes |
| \((1,3)\) | \(-7/75\) | \((1/10,-2/5,27/50,0)\) | no | no |
| \((2,2)\) | \(-3/20\) | \((-2/5,3/5,1/25,0)\) | no | no |
| \((2,3)\) | \(-4/25\) | \((-2/5,1/10,27/50,0)\) | yes | no |

All four assignments satisfy (H). The last one has both cross-site NE
comparisons strict, yet violates the lower box; the home assignment is
the unique global optimizer. For original realization use four sites
H,M,L,R with private weights 130,80,52,50, two weight-25 customers on
HM and ML, and seven facilities. The greedy scores are strictly
155,105,155/2,105/2,52,155/3,50 at H,M,H,M,L,H,R. The resulting
\(\gamma=50\), multiplicities and initial loads give the displayed
normalization. The away profile has original totals 130,105,77,50;
its movable exterior costs are 40 and 52, whereas the alternative
site prices are 130/3 and 105/2. Both strictly resist moving home.
Private clients have no cross-site alternatives. The exact input and
independent complete calculation are stored in
[the fixture](../../../examples/multi_facility/equal_light_flow_local_ne.json)
and [adversarial audit](../../../tests/audits/kfac_equal_light_flow_adversary.py).

To isolate the equal-weight hypothesis, allow different movable weights \(w_i\)
and define the normalized exact weighted potential

\[
\Phi(a)=\sum_t\frac{X_t(a)^2-
                           \sum_{i:a_i=t}w_i^2}{2q_t}.             \tag{17}
\]

A single move of weight \(w\) from \(s\) to \(t\) changes it by
\(w[X_t/q_t-(X_s-w)/q_s]\). In the equal-weight case,

\[
\Phi(a)=\sum_t\frac{b_t^2}{2q_t}+\delta\Psi(a).                   \tag{18}
\]

For unequal weights take distinct sites
\(u_0,\ldots,u_{\ell+1}\), and distinct customers indexed
\(j=0,\ldots,\ell\): customer \(j\), of weight \(w_j\), is currently
at \(u_j\) and is returned to its home \(u_{j+1}\). Every \(X\) below
is measured **before** all simultaneous returns. The internal site's
load change is \(w_{j-1}-w_j\), and direct expansion of (17) gives

\[
\begin{aligned}
\Delta\Phi={}&-w_0\frac{X_{u_0}-w_0}{q_{u_0}}\\
&+\sum_{j=1}^{\ell}(w_{j-1}-w_j)
                       \frac{X_{u_j}-w_j}{q_{u_j}}\\
&+w_\ell\frac{X_{u_{\ell+1}}}{q_{u_{\ell+1}}}.                    \tag{19}
\end{aligned}
\]

The local identity establishing each internal term is

\[
\frac{(X+x-y)^2-X^2-(x^2-y^2)}{2q}
   =(x-y)\frac{X-y}{q}.                                          \tag{20}
\]

The endpoint terms use the same identity with one of \(x,y\) zero.
For \(\ell=0\), (19) is just the single-move formula, with an empty
internal sum. When all selected weights equal \(\delta\), the internal
sum vanishes, recovering the endpoint comparisons after division by
\(\delta\). With unequal weights its internal terms have no uniform sign.
But controlling that sum alone would not repair the proof: the endpoint
weights can differ, and the backward path no longer has a common
\(1-\delta\) stopping threshold.

This distinction already occurs in the normalized parameter-45 member of
[`SC-K-TWO-LIGHT-LOWER-POTENTIAL-NO`](polytime_frontier.md#sc-k-two-light-lower-potential-no-lower-bounded-potential-can-overflow-with-two-weights).
Use

\[
q=(3,2,1,1),\quad c=(44/45,44/45,2/45,0),\quad
(w_1,w_2)=(4/5,44/45),\quad
A_1=\{1,2\},\ A_2=\{2,3\}.
\]

The homes are \((1,2)\). The four values of (17), for assignments
\((1,2),(1,3),(2,2),(2,3)\), respectively, are

\[
326/6075,\quad 590/6075,\quad 2414/6075,\quad302/6075.
\]

Thus the unique unrestricted minimizer is \((2,3)\), with
\(X=(8/45,4/5,46/45,0)\), which violates the upper box and the second
customer's (H). Returning both customers along \(3\to2\to1\) gives
the three contributions in (19)

\[
-88/2025,\qquad0,\qquad32/675,
\qquad\text{whose sum is }8/2025>0.
\]

The internal contribution vanishes exactly, but the path still raises the
potential. Its receiving endpoint has \(X_1=8/45\), which is at most
\(1-4/5=1/5\) and exceeds \(1-44/45=1/45\). Thus the proposed general
extension must control internal load changes **and** the unequal endpoint
weights and threshold comparisons, or supply another global mechanism.
This example is a selector obstruction, not a complexity lower bound or
a failure of general boxed-NE existence.

The two path arguments used here need a fixed acyclic orientation of all
home-to-option edges with \(q\) nonincreasing along them. The displayed
site-order assumptions guarantee it. This note does not silently replace
that input contract by an unordered maximum-home-multiplicity contract;
such an extension requires a separately stated path or cycle argument.
The maximum-home-multiplicity requirement cannot simply be deleted. With
two sites, \(q=(1,3)\), \(c=(1,1)\), one weight-\(1/2\) customer having
\(A_1=\{1,2\}\) and home 1, the two objective values are \(1/2\) at
home and \(1/3\) away. The unique global minimizer therefore has
\(X=(1/2,3/2)\), violating the upper box. This input is outside the
ordered theorem and outside the asserted greedy normalization.

## 9. Review and evidence scope

The current reconstruction supplies the objective identity, both labeled
path contradictions, full-option best responses, the integral flow
reduction, negative-cost optimality invariant, total augmentation count,
bit-length analysis, and the joint MF-MODEL/BOX-TO-2 corollary. Internal
review specifically covered ties, negative offsets, zero surplus, duplicate
customer types without merging their identities, path-customer
distinctness, complete allowed sets, large binary multiplicities, no
movable customers, and the unequal-weight identity.

The supplied conversation text included executable source, claimed audit
counts, and links to a ZIP and other artifacts that were not attached.
Those linked files and reported counts are not repository verification
evidence. Independently rerun repository audits, their actual outputs and
canonical implementation status are recorded separately in the claim
ledger and asset index. Finite audits check instances and implementation;
the universal theorem and polynomial bound rest on the preceding proofs.

## 10. Canonical implementation and reproducible repository evidence

The unique normalized selector is
[`multi_facility_spe/equal_light_flow.py`](../../../multi_facility_spe/equal_light_flow.py).
It uses signed integer-scaled costs, strict Bellman--Ford relaxations and
whole individually labeled customer nodes. The original-model bridge in
`greedy_box.py` preserves physical labels separately from normalized
site ranks, freezes the prescribed customers and checks original exact
NE, full boxes and (H). Unequal movable weights are rejected explicitly.

Run from the repository root:

```sh
python3 tests/audits/kfac_equal_light_flow.py
python3 tests/audits/kfac_equal_light_flow_adversary.py
python3 tests/audits/kfac_equal_light_flow_continuation.py
python3 -m multi_facility_spe examples/multi_facility/equal_light_flow_complete.json --method equal-light-flow --output NEW_certificate.json
```

The core [frozen report](../../../evidence/runs/2026-10-07/equal_light_flow.json)
records independent checks of all legal assignments and all their global
minima on its exact grid, including negative offsets, ties, multiple
optima, invalid input rejection and residual reassignment fixtures. A
[second independent report](../../../evidence/runs/2026-10-07/equal_light_flow_adversary.json)
uses a separate oracle on both the canonical selector and the locked
attached implementation; its instrumented residual negative/zero-cycle
counts refer specifically to the attached code, not canonical internals.
The [continuation report](../../../evidence/runs/2026-10-07/equal_light_flow_continuation.json)
checks actual labeled deviations and queried default layouts directly
from original conditional expected costs. Each report stores parameters,
its own counts and source hashes; their instance sets need not be disjoint.
Default runs do not overwrite frozen evidence.

The flow optimality method is standard; see the primary
[MIT min-cost-flow notes](https://courses.csail.mit.edu/6.854/20/Notes/n09-mincostflow.html).
The result specific to this interface is the automatic-box/H theorem and
the redundant-constraint comparison, not the classical flow algorithm.
No complete general unequal-weight polynomial selector or canonical
polynomial off-path scheduler is claimed.
