# A threshold potential for boxed equilibria at every greedy occupancy

Version 1, 2026-10-07. This note reconstructs the complete mathematical
argument supplied in the user's 2026-10-07 conversation, and includes an
independent extension allowing arbitrary orders of home returns. The supplied
conversation linked a ZIP, source code and audit report; those linked artifacts
were not available to this review and their reported test counts are not used
as repository evidence. The proof below is self-contained at the abstract
on-path level. Its original-model conclusion uses the explicitly identified
greedy and off-path interfaces. Internal proof review has been completed;
external peer review and literature priority have not been established.

The main conclusions are universal boxed-equilibrium existence, an exact
finite construction at the canonical greedy occupancy, and polynomial space
for the on-path algorithm without stored trajectories. A polynomial bound in
the general input bit length on its total running time remains unproved.
The structured polynomial corollaries use existing exact dynamic programs;
they do not obtain their runtime from the improvement trajectory.

## 1. Abstract data and exact target

There are \(m\ge1\) sites and \(n\ge0\) movable customers. For each site \(t\),
the multiplicity \(q_t\) is a positive integer and \(c_t\in[0,1]\). Customer
\(i\) has a weight \(0<w_i<1\), a nonempty allowed set
\(A_i\subseteq\{1,\ldots,m\}\), and a designated home \(h_i\in A_i\).
The home has maximum accessible multiplicity:

\[
q_{h_i}\ge q_t\qquad(t\in A_i).                                      \tag{1}
\]

For the deterministic site-order rule below, number sites so that
\(q_1\ge\cdots\ge q_m\) and \(h_i=\min A_i\). These stronger ordering
conditions hold for the forward greedy normalization in Section 7. The
arbitrary-return proof only needs (1), not an ordering among tied sites.

A complete allowed assignment is \(a\in\prod_i A_i\). Define the normalized
surplus loads, prices, exterior prices, and fixed customer thresholds by

\[
\begin{aligned}
X_t(a)&=c_t+\sum_{i:a_i=t}w_i-\sum_{i:h_i=t}w_i,\\
p_t(a)&=X_t(a)/q_t,\\
e_i(a)&=(X_{a_i}(a)-w_i)/q_{a_i},\\
r_i&=(1-w_i)/q_{h_i}>0.
\end{aligned}                                                       \tag{2}
\]

Thus \(X_t(h)=c_t\) and \(\sum_tX_t(a)=\sum_tc_t\). Arbitrary allowed
assignments can have negative surplus loads; all states reached by our
algorithm will have \(X_t\ge0\). The target consists of the three conditions

\[
0\le X_t(a)\le1\quad(t=1,\ldots,m),                                \tag{B}
\]

\[
e_i(a)\le p_v(a)\quad(i=1,\ldots,n,\ v\in A_i),                     \tag{NE}
\]

\[
e_i(a)\le r_i\quad(i=1,\ldots,n).                                  \tag{H}
\]

The strict improvement test for moving \(i\) from its current site to \(t\)
is \(p_t(a)<e_i(a)\). It is tested on every original allowed site, without
requiring the resulting assignment to satisfy the upper box. A strict move
cannot choose the current site because \(w_i>0\).

The mathematical existence and termination statements permit real \(c_t,w_i\).
Exact algorithmic bit bounds below assume their explicit binary-rational
encoding, with explicit sites, customers and allowed incidences. Let

\[
E=\sum_i|A_i|,\qquad S=\prod_i|A_i|.                                \tag{3}
\]

For no movable customers, \(S=1\), the initial assignment already satisfies
all three conditions, and no move is needed.

## 2. The clipped, interleaved lexicographic potential

List the distinct fixed thresholds as
\(\rho_1<\cdots<\rho_d\). Equal thresholds are grouped by exact equality.
For every \(\rho>0\), put

\[
\Lambda_\rho(a)=\operatorname{sort}_{\uparrow}
 \bigl(\min\{p_1(a),\rho\},\ldots,\min\{p_m(a),\rho\}\bigr),          \tag{4}
\]

and define the number of away customers in each threshold group by

\[
N_\ell(a)=\#\{i:r_i=\rho_\ell,\ a_i\ne h_i\}.                       \tag{5}
\]

The potential is the concatenated vector

\[
\mathcal P(a)=
\bigl(\Lambda_{\rho_1}(a),-N_1(a),\ldots,
       \Lambda_{\rho_d}(a),-N_d(a)\bigr),                            \tag{6}
\]

ordered lexicographically, with a larger vector meaning progress. Each site
occurs once in each load block; there is no repetition by \(q_t\). Each away
count follows its own threshold block, rather than following all load blocks.
The potential is defined even while some upper boxes are violated.

**Strict-improvement lemma.** If a customer strictly improves from \(s\) to
\(t\), then every \(\Lambda_\rho\) is lexicographically nondecreasing. It
strictly increases whenever the old destination price satisfies \(p_t<\rho\).

**Proof.** Write \(\alpha=p_t(a)\) and
\(\beta=(X_s(a)-w_i)/q_s\), so that \(\alpha<\beta\). The two changed
prices are

\[
\left(\beta+\frac{w_i}{q_s},\alpha\right)
 \longmapsto
\left(\beta,\alpha+\frac{w_i}{q_t}\right).                          \tag{7}
\]

If \(\alpha\ge\rho\), both changed coordinates are clipped to \(\rho\)
before and after the move. If \(\alpha<\rho\), their old smaller clipped
coordinate is \(\alpha\), and both new clipped coordinates are strictly
greater than \(\alpha\). All other coordinates are unchanged. The multiset
of values below \(\alpha\) is unchanged, and the multiplicity of
\(\alpha\) decreases by one. The increasing sorted vector therefore
strictly increases lexicographically. This argument permits arbitrary load
ties. QED.

**Home-return lemma.** Suppose \(i\) is away from home and strictly violates
(H), and move it to \(h_i\). For every \(\rho\le r_i\), the vector
\(\Lambda_\rho\) is lexicographically nondecreasing.

**Proof.** The source price after removal is \(e_i(a)>r_i\ge\rho\).
Its clipped coordinate is therefore \(\rho\) both before and after the
return. The home price increases and every other price is unchanged. All
clipped coordinates are individually nondecreasing, so their sorted vector
is nondecreasing as well. A return is not asserted to be a strict improvement
in the customer game. QED.

**Microstep theorem.** Each of the following operations strictly increases
\(\mathcal P\):

1. A customer currently satisfying its own (H) makes a strict improvement.
2. A customer away from home and strictly violating its own (H) returns home.

**Proof.** Let the moved customer have \(r_i=\rho_\ell\). For an improvement,
all earlier threshold load blocks are nondecreasing and their away counts
are unchanged. If an earlier block strictly increases, the result follows.
Otherwise,

\[
p_t(a)<e_i(a)\le r_i=\rho_\ell,                                    \tag{8}
\]

so the strict-improvement lemma gives strict increase in
\(\Lambda_{\rho_\ell}\), before the potentially adverse change of
\(-N_\ell\). For a return, all load blocks up to and including \(\ell\)
are nondecreasing and earlier away counts are unchanged. If none of those
load blocks strictly increases, the first changed coordinate is
\(-N_\ell\), which increases by one. Later blocks cannot reverse either
lexicographic comparison. QED.

## 3. Home repair restores all boxes in any order

Assume an allowed assignment has \(X_t\ge0\) at every site. Repeatedly choose
any customer \(i\) with \(a_i\ne h_i\) and \(e_i>r_i\), and return it home.
Stop only when no such customer exists.

Every return preserves nonnegativity: at its source,

\[
X_{a_i}(a)-w_i=q_{a_i}e_i(a)>q_{a_i}r_i>0,                          \tag{9}
\]

and the destination load increases. Every returned customer stays home for
the remainder of this repair phase. Consequently at most \(n\) returns are
possible, irrespective of their order.

At termination suppose \(X_s>1\). Since \(c_s\le1\), formula (2) implies
that at least one customer \(i\) is currently at \(s\) with \(h_i\ne s\):
without an incoming customer the final surplus cannot exceed \(c_s\).
For that customer, (1) and \(1-w_i>0\) give

\[
e_i=\frac{X_s-w_i}{q_s}>
\frac{1-w_i}{q_s}\ge\frac{1-w_i}{q_{h_i}}=r_i.                      \tag{10}
\]

It could still be returned, a contradiction. Thus all upper boxes hold.
The stopping rule gives (H) for every away customer. For every home customer,

\[
e_i=(X_{h_i}-w_i)/q_{h_i}\le(1-w_i)/q_{h_i}=r_i,                    \tag{11}
\]

so it too satisfies (H). The entire repaired assignment satisfies (B)+(H).

This proof does not require the reverse-site or smallest-threshold order.
Those orders can be imposed for a deterministic implementation. Under the
ordered input convention, processing sites from \(m\) down to (1), and
at each site returning its violating away customers in increasing
\((r_i,i)\) order, suffices: every return goes to a smaller site index and
cannot create a new violation at an already processed site.

**Ordered-batch mover preservation.** Under \(h_i=\min A_i\), suppose an
entire assignment satisfies (H), and customer \(i\) strictly improves to
\(t\). The arriving customer immediately has
\[
e_i(a')=p_t(a)<e_i(a)\le r_i.
\]
Only customers at \(t\) can acquire a new (H) violation: the source load
decreases and every other site is unchanged. Every home return goes to
a strictly smaller index, so no site with index greater than \(t\) can
become active during repair. Consequently \(t\) receives no home returns
and its load after the initial arrival can only decrease. Customer \(i\)
continues to satisfy (H) and cannot itself be returned during this batch.
This justifies the deterministic implementation's additional assertion
that the batch's initial mover remains at its chosen destination. It is
not needed for the potential or existence proof, and is not asserted
under the weaker unordered maximum-home-multiplicity hypothesis alone.

## 4. `SC-K-GREEDY-BOX-EXISTS`: universal existence and global termination

**Abstract theorem.** Every input satisfying Section 1 admits an assignment
satisfying (B), all original (NE) inequalities, and (H). Starting at \(a=h\),
the following algorithm terminates for every choice of improving customer,
every strictly improving destination, and every valid home-repair order:

```text
a := h
while some original allowed strict improvement exists:
    choose any customer i and t in A_i with p_t(a) < e_i(a)
    move i to t
    while an away customer j has e_j(a) > r_j:
        choose any such j and return j to h_j
return a
```

At most \(S-1\) single-customer moves occur, counting both improvements and
home returns and including intermediate upper-box violations.

**Proof.** Initially (B)+(H) hold because \(X_t(h)=c_t\in[0,1]\).
At every outer-loop start all customers satisfy (H), so its chosen move is
of the first kind in the microstep theorem. A strict improvement from a
nonnegative state preserves the lower boxes because its source residual
price is strictly greater than the old nonnegative destination price.
Section 3 therefore applies and restores (B)+(H). Every repair move is of
the second kind in the microstep theorem. Hence every move strictly
increases one fixed potential, including during repair.

There are exactly \(S\) allowed complete assignments. All intermediate states
remain among them, even when above an upper box. No state can repeat, so no
run has more than \(S-1\) moves. At the final repaired state, every original
strict improvement has been checked and is absent. Thus all (NE)
inequalities, (B), and (H) hold. QED.

**Stronger guarded interleaving.** One may interleave the two microstep
operations arbitrarily, without waiting for an entire repair phase before
the next improvement, provided each improving customer currently satisfies
its own (H). Starting from \(h\), every move still preserves nonnegativity
and increases \(\mathcal P\). Every maximal sequence has at most \(S-1\)
moves. With no permissible return, (10)--(11) give (B)+(H); with no
permissible guarded improvement, all customers then satisfy (NE).

The guard on an improving customer is essential to this proof. It must not
be dropped when improvements are allowed during an unfinished repair.
The batched algorithm imposes it automatically through the batch invariant.
An upper-box constraint must not be inserted into the customer's allowed
deviation test.

**Equivalent finite selection principle.** Let
\(\mathcal S_H=\{a:a\text{ satisfies (B)+(H)}\}\). It is nonempty because
it contains \(h\). Every global lexicographic maximizer of \(\mathcal P\)
over \(\mathcal S_H\) satisfies all (NE) inequalities: otherwise one
improvement and its terminating repair would give a strictly larger
potential within the same set. This is a selection principle, not a
polynomial-time global-optimization assertion.

## 5. Deterministic rule and exact bit bounds

The deterministic rule used for the on-path construction is:

```text
a := h
precompute r_i and customer order (r_i, i)
while a strict improvement exists:
    choose the first improving customer in order (r_i, i)
    choose its destination minimizing (p_t(a), t) over all t in A_i
    perform that move
    process sites in reverse order:
        while this site contains an away customer violating H:
            return its smallest (r_i, i) violating customer home
return a
```

If a customer has any strict improvement, its minimum-price allowed site
is strictly improving. The theorem does not depend on either priority.
In the executable, destination-price ties use the original physical catalog
label; the separate decreasing-\(q\), opening-order rank controls the
reverse repair scan. Both are fixed deterministic index orders covered
by the proof.
Sites with equal multiplicities, customers with equal thresholds and equal
destination prices retain exact ties and deterministic index tie breaking.
Neither \(X_t=0\), \(X_t=1\), nor \(e_i=r_i\) triggers a fictitious strict
move.

A direct implementation takes \(O(E+mn+n^2)\) rational operations per
batch, after preprocessing: scan original allowed destinations, then
perform at most \(n\) repairs with direct customer scans. This is a bound on
work per batch when progress is certified by the proof. The delivered
implementation additionally recomputes the exact potential before and
after each microstep, adding
\(O((n+1)(dm\log m+n))\) rational comparisons and operations per batch.
Both bounds are polynomial per batch; neither bounds the number of batches
by a polynomial.

For rational data let \(D\) be the least common multiple of all denominators
of \(c_t,w_i\). Its bit length is at most the sum of their denominator bit
lengths. Every intermediate \(X_t\) lies on \(D^{-1}\mathbb Z\), and

\[
0\le X_t\le\sum_uc_u\le m.                                        \tag{12}
\]

All loads, thresholds and exact cross-multiplied comparisons consequently
have polynomial bit length in the explicit input. Storing the current
assignment, loads, fixed thresholds and scan indices requires polynomial
space. No visited-state set or complete trajectory is needed for correctness.
Optional trajectory recording can consume exponentially more space and is
not part of this space bound.

The potential itself has a polynomial-size integer encoding. Put

\[
L=D\operatorname{lcm}(q_1,\ldots,q_m),\qquad
B=1+\max\{L,n\}.                                                    \tag{13}
\]

Every price and threshold is an integer multiple of \(1/L\). Since
\(q_{h_i}\ge1\) and \(0<w_i<1\), every threshold lies in \((0,1)\).
For a nonnegative state each clipped coordinate in (6) therefore lies in
\([0,1]\), even if its unclipped price exceeds one. Multiply each such
coordinate by \(L\), and replace \(-N_\ell\) by \(n-N_\ell\). The resulting
digits all belong to \(\{0,\ldots,B-1\}\). Read the fixed-length string as a
base-\(B\) integer, using

\[
M=d(m+1)\le n(m+1)                                                   \tag{14}
\]

digits. Its ordering agrees exactly with \(\mathcal P\), and its bit length
is \(O(M\log B)\), polynomial in the input. When \(n=0\), take the empty
potential to have integer value zero.

The valid general move bound is \(S-1\le m^n-1\). A polynomial-bit integer
can have exponentially many distinct values, so this encoding proves no
polynomial total-time bound. An exponential upper bound also proves no
exponential lower bound for this rule. Both a general bit-polynomial
constructor and any claimed superpolynomial lower bound require additional
arguments.

## 6. What has and has not been selected

This potential differs from the original exact weighted customer potential
and from untruncated sorted facility revenues. It also restricts the global
selection principle to (B)+(H). The counterexamples in
[depth_three_box_boundary.md](depth_three_box_boundary.md) and
[boxed_lexmax_boundary.md](boxed_lexmax_boundary.md) remain valid for their
own selectors. The unrestricted strict-improvement trajectories refuted by
`SC-K-GREEDY-REPAIR-ORDER-NO` do not enforce these home repairs and are not
covered by the new safety assertion.

An individual customer may leave home repeatedly across different batches,
return repeatedly, or revisit a previously occupied site. The proof neither
forbids nor needs to count such revisits separately. An away-count decrease
may later be undone only after an earlier load block has already increased;
the complete interleaved potential is never undone.

## 7. Forward normalization of the original common-catalog model

Use [MF-MODEL](model.md): positive atomic customer weights, a common finite
site catalog, explicitly listed \(k\ge2\) labeled facilities, compulsory
service when covered, and independent customer randomization. Here write
original weights as \(u_i\), to distinguish them from normalized \(w_i\).

Run the canonical \(k\)-insertion greedy procedure. An occupied site with
fixed original customer pool \(J_t^0\), weight \(W_t^0\), and current
multiplicity \(q_t\) has next-seat score \(W_t^0/(q_t+1)\). An unopened
site's score is its currently uncovered weight. Select a maximum using
fixed site tie breaking. On first opening a site, assign to its original
pool all previously uncovered customers it covers. These pools remain fixed
throughout greedy. Let \(O\) be the finally occupied sites and \(\gamma\)
the last selected score.

For positive maximum reach, \(\gamma>0\). The selected maxima are
nonincreasing: adding to an occupied site decreases its next-seat score,
and opening a site only removes uncovered customers elsewhere. Hence

\[
q_t\gamma\le W_t^0\le(q_t+1)\gamma\quad(t\in O),\qquad
N_v\le\gamma\quad(v\notin O),                                      \tag{15}
\]

where \(N_v\) is the weight covered by \(v\) but by no site in \(O\).
The lower bound is the site's last selected average; the upper bound is
its final next-seat score. The same comparison gives the unopened bound.

The original home of every served customer has maximum accessible final
multiplicity. Indeed, suppose \(i\) first enters \(J_h^0\) and is also
covered by another occupied site \(t\). Site \(t\) opens later. When \(h\)
opens, \(t\)'s uncovered weight includes all of \(J_t^0\) and the positive
weight \(u_i\), so \(W_h^0>W_t^0\). If \(q_t>q_h\), at \(t\)'s last insertion
the already occupied \(h\) has score at least

\[
\frac{W_h^0}{q_h+1}>
\frac{W_t^0}{q_h+1}\ge\frac{W_t^0}{q_t},                            \tag{16}
\]

contradicting the greedy choice. Thus \(q_h\ge q_t\). Sorting sites by
decreasing final multiplicity, and by opening order within equal
multiplicities, makes this original home equal to \(\min A_i\).

Freeze every served customer with just one occupied option, and every
customer with \(u_i\ge\gamma\), at its original greedy site. Let \(I^*\)
consist of the remaining customers; each has at least two occupied options
and \(0<u_i<\gamma\). Use all their original occupied options \(A_i\), their
original homes, and set

\[
w_i=u_i/\gamma,\qquad c_t=W_t^0/\gamma-q_t.                         \tag{17}
\]

Equations (15)--(16) verify all abstract assumptions. With frozen customers
unchanged, the actual total at every occupied site is

\[
W_t(a)=\gamma\bigl(q_t+X_t(a)\bigr).                               \tag{18}
\]

Therefore the abstract full box is exactly the full greedy box
\(q_t\gamma\le W_t\le(q_t+1)\gamma\). Assign each served customer to the
site produced by the abstract algorithm and let it independently choose
uniformly among that site's \(q_t\) labeled facilities.

For a variable customer \(i\) assigned to \(s\), the conditional cost of
any facility at \(s\) is \(u_i+(W_s-u_i)/q_s\); at an alternative site \(v\)
it is \(u_i+W_v/q_v\). Uniform mixing makes all facilities within the
chosen site equivalent. The cross-site exact NE comparison is

\[
\frac{W_s-u_i}{q_s}\le\frac{W_v}{q_v}
\quad\Longleftrightarrow\quad
\frac{X_s-w_i}{q_s}\le\frac{X_v}{q_v}.                              \tag{19}
\]

Thus (NE) is precisely the original customer test, including the own-weight
subtraction; no related-link cost formula has been substituted. A frozen
one-option customer has no alternative occupied site. A frozen heavy
customer at \(s\) satisfies, for every occupied alternative \(v\),

\[
\frac{W_s-u_i}{q_s}
\le\frac{(q_s+1)\gamma-\gamma}{q_s}
=\gamma\le\frac{W_v}{q_v}.                                        \tag{20}
\]

It too is at an exact best response. Unserved customers remain unserved.
Consequently `SC-K-GREEDY-BOX-EXISTS` gives a full-box, site-pure and
within-site independent-uniform exact customer NE at every canonical
greedy occupancy, with the frozen customers retained. Its variable customers
also satisfy the normalized (H). This forward argument does not assume
that every legal abstract input has a reverse realization by greedy.

If maximum reach is zero, no site covers any positive-weight customer.
Every layout has no served customers and zero facility revenue. An
arbitrary labeled layout and the empty customer profile at every layout
solve the problem; no division by \(\gamma\) is performed. If positive
reach holds but \(I^*\) is empty, (20) and the one-option observation already
certify the initial greedy profile.

## 8. `SC-K-GREEDY-BOX-FINITE-2`: complete factor-two construction

**Theorem.** Every explicit rational MF-MODEL input has an exact finite
construction of a canonical greedy labeled layout and a complete exact
customer-equilibrium continuation such that no facility deviation gains
more than factor two. The on-path profile is site-pure and uniform within
each chosen site, lies in every full greedy box, and is obtained with at
most \(S-1\) variable-customer relocations. Every actual one-facility
deviation can use a pure exact customer NE. No general polynomial bound
on the complete construction's running time is asserted.

**Joint premises and proof.** Section 7 supplies an explicit on-path
witness for
[`SC-K-GREEDY-BOX-TO-2`](polytime_frontier.md#sc-k-greedy-singleton-reset-and-sc-k-greedy-box-to-2).
That interface uses the original greedy budgets and the following two
source cases, not (H) at an off-path layout.

For a facility leaving \(u\) with \(q_u\ge2\), its payoff is
\(a=W_u/q_u\ge\gamma\), and \(u\) survives with \(q_u-1\) facilities.
Its total \(W_u=q_ua\) has exactly the \((h+1)a\) packing budget with
\(h=q_u-1\). Every other occupied site's total satisfies
\(W_t\le(q_t+1)\gamma\le(q_t+1)a\). The standard merging lemma packs
these pools into their stationary facilities under cap \(2a\), except for
isolated customers whose individual weight exceeds that cap. An occupied
target starts the deviator empty; at an unopened target it initially
receives only newly served weight \(N_v\le\gamma\le a\). Capped exact
Nashification then keeps its payoff at most \(2a\).

For \(q_u=1\), use `SC-K-GREEDY-SINGLETON-RESET`: reset old customers to
the original greedy pools at the actual deviation layout, assign surviving
orphans using their actual remaining options, and use the original pooled
singleton budget. The resulting pure seed has deviator payoff at most
\(2\gamma\le2a\) and admits capped completion. This case needs no private
reserve or orphan budget for the newly selected on-path assignment.

The interface's packing lemma, singleton reset and capped-completion proof
are all joint premises of this factor-two conclusion. They are recorded
in [polytime_frontier.md](polytime_frontier.md); the threshold potential
alone is not an off-path theorem.

If the physical catalog has \(p\) sites, there are \(k(p-1)\) actual
nontrivial labeled deviations. Their resulting layouts are distinct, so their chosen
witnesses define compatible continuation entries. At the on-path layout
use the constructed uniform profile; at every other layout use a fixed
exact pure-NE default. Strict pure best responses provide a finite default,
because one half of the squared-load sum decreases by
\(u_i(L_g+u_i-L_f)<0\) on each improving move from facility \(f\) to \(g\).
No facility-optimality requirement is imposed at those other layouts.
This gives one complete exact continuation, rather than unrelated
on-path and deviation certificates. QED.

The existing `BOX-TO-2` theorem supplies an input-bit-polynomial off-path
completion using its imported restricted-identical-link Nashification
primitive, once the on-path witness is given. The executable construction
in [greedy_box.py](../../../multi_facility_spe/greedy_box.py) instead uses
the repository's finite `merge_pack` and cap-preserving `pure_improve`
routines. It does not implement that imported polynomial primitive and
does not claim polynomial off-path runtime. Its complete-certificate
interface and mathematical polynomial-completion interface must be kept
separate.

Without stored histories, the on-path construction uses polynomial space;
the finite off-path/default searches can also be implemented with only a
current assignment and polynomial-size certificate output. A diagnostic
implementation that retains all visited states or its entire move trace
does not inherit this space bound for its diagnostic data. A complete
continuation is represented by the polynomial number of actual-deviation
entries and a default rule, not by writing all catalog-size-to-the-\(k\)
layout entries.

## 9. `SC-K-BOX-STRUCTURED-POLY-2`: unconditional structured corollaries

For the explicit rational MF-MODEL input, form \(I^*\) and \(O\) exactly as
in Section 7. The universal existence theorem uses these same prescribed
frozen customers. It therefore makes each of the following existing exact
selectors a total constructor on its stated structural class.

**Individual-client incidence condition.** Fix nonnegative integers
\(\tau,d\). Let the bipartite graph on \(I^*\cup O\) have an edge \(it\)
exactly when \(t\in A_i\), include isolated occupied sites, bound its
treewidth by \(\tau\), and bound its maximum degree on **both sides** by
\(d\). The exact selector
[`SC-K-INCIDENCE-BOX-DP`](bounded_incidence_box.md) has a feasible boxed
NE by `SC-K-GREEDY-BOX-EXISTS`, so it outputs one in input-bit-polynomial
time for fixed \(\tau,d\). Combining it with `SC-K-GREEDY-BOX-TO-2` gives
a polynomial complete factor-two constructor on this class.

**Site-primal and local-weight condition.** Fix nonnegative integers
\(\tau,d\). Join two occupied sites when some \(i\in I^*\) has both in
\(A_i\), include isolated sites, and bound this site-primal graph's
treewidth by \(\tau\). At every site \(t\), require

\[
\#\{u_i:i\in I^*,\ t\in A_i\}\le d,                                \tag{21}
\]

counting exact distinct weights, not customers or types. Use a supplied
width-\(\tau\) decomposition or the fixed-width decomposition theorem
already imported by the existing selector.
[`SC-K-LOCAL-WEIGHT-BOX-DP`](local_weight_box_dp.md) is bit-polynomial for
fixed \(\tau,d\); universal boxed existence guarantees its success, and
`SC-K-GREEDY-BOX-TO-2` completes the factor-two continuation in polynomial
time. Scaling weights by \(\gamma\) changes none of the equal-weight
classes in (21).

Each conclusion uses **all three** premises jointly: universal fixed-heavy
boxed existence, the applicable exact DP with its structural and encoding
hypotheses, and the original-model box-to-continuation interface. A DP
output need not satisfy (H), since `BOX-TO-2` requires only the full box and
exact NE. No directed-depth bound, two-option restriction, or tree/star
orientation condition is now needed for either existence input to the DP.

The first condition still bounds individual incidence degrees; the second
still bounds local weight diversity and site-primal width. Their different
graphs and meanings of \(d\) must not be conflated. Neither theorem gives a
uniform polynomial bound when its parameters vary with the input. In
particular bounded treewidth alone is not the asserted algorithmic class.
The former height-two intersections remain valid special cases. Their
selector-specific potential proofs and small move bounds are not replaced
by a claim that the new general trajectory is polynomial.

## 10. Provenance, implementation and verification scope

The threshold clipping, interleaving with away counts, and microstep proof
were supplied in the user's complete conversation text on 2026-10-07.
The present note reconstructs that text with explicit abstract hypotheses,
an independent arbitrary-return proof, the forward original-model map,
and the exact structured-DP consequences. The linked conversational ZIP
and its advertised finite report were not ingested; no test count from
them is certified here.

The canonical exact implementation is
[multi_facility_spe/greedy_box.py](../../../multi_facility_spe/greedy_box.py),
with `construct_on_path` for the greedy boxed assignment and `construct`
for the complete finite certificate. The CLI selects it with
`--method greedy-box`. Independent definition-level checks belong to
[tests/audits/kfac_greedy_box_global.py](../../../tests/audits/kfac_greedy_box_global.py)
and regressions to
[tests/test_greedy_box_global.py](../../../tests/test_greedy_box_global.py).
The reproducible fixture is
[examples/multi_facility/greedy_box_global.json](../../../examples/multi_facility/greedy_box_global.json);
recorded outputs are
[the audit run](../../../evidence/runs/2026-10-07/greedy_box_global.json)
and [the finite certificate](../../../evidence/certificates/multi_facility/greedy_box_global.json).
These artifacts verify their stated finite cases and executable contracts;
the universal quantifiers follow from Sections 2--4 and 7--9, not from
successful runs. The source proof, current reconstruction, internal review,
external review and software checks are separate status dimensions.
