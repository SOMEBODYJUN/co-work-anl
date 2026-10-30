# Source record: user-supplied greedy-box proof, 2026-10-07

This is a curated mathematical extraction of the research report pasted by
the user in this conversation on 2026-10-07. It preserves the supplied
definitions, claims and proof mechanism. It is **not** a downloaded source
manuscript or a verbatim copy of the unavailable ZIP. The linked `/mnt/data`
artifacts and the report's claimed test counts were not obtained or replayed.
The new current account reconstructs and independently reviews these arguments
in `research/current/multi_facility/greedy_box_global_progress.md`.

No theorem from the separately discussed OpenAI mathematics catalogue or its
preprints is a premise. The source here is the user's pasted Pro research
report, together with its previously pasted repair argument.

## Supplied abstract model and repair

There are finitely many occupied sites, with positive integer multiplicities
`q_1 >= ... >= q_m`, initial excesses `0 <= c_t <= 1`, positive movable
weights `0 < w_i < 1`, and nonempty allowed sets `A_i`. The home is
`h_i = min A_i`. For every legal assignment `a_i in A_i`, put

\[
 X_t(a)=c_t+\sum_{a_i=t}w_i-\sum_{h_i=t}w_i,\qquad
 p_t=X_t/q_t,\quad e_i=(X_{a_i}-w_i)/q_{a_i},\quad
 r_i=(1-w_i)/q_{h_i}>0.
\]

The full box is `0 <= X_t <= 1`. Condition H is `e_i <= r_i` for
every movable customer. The original site-uniform customer NE is `e_i <= p_v`
for every customer and every allowed occupied destination `v in A_i`.

The prior supplied repair visits sites in decreasing index. At a site it
returns a foreign customer strictly violating H to that customer's home,
choosing minimum `(r_i,i)`. Such a return leaves source excess
`X_t-w_i > q_t r_i > 0`, and the target excess increases. Each customer
returns at most once during a repair-only phase. If a home customer violates
H, its site has excess `>1`; that implies some foreign customer is present,
and every such foreign customer violates H because
`w_i + q_t r_i <= 1`. Thus the procedure restores H and the full box in
at most `n` returns. Intermediate states may exceed the upper box.

From a box+H state, a strict improvement has
`p_t < e_i <= r_i`. It preserves the box, leaves the mover satisfying H,
and can introduce H violations only among other customers at the target.
Returning violated foreign customers then propagates toward earlier homes.
The designated mover remains at its improving destination through this
repair phase. This was a local batch theorem, without a global termination
claim until the following new potential.

## Supplied threshold potential and microstep proof

Sort the distinct fixed `r_i` values as `rho_1 < ... < rho_d`. Define

\[
 \Lambda_\rho(a)=\operatorname{sort}_\uparrow
       (\min(p_1(a),\rho),\ldots,\min(p_m(a),\rho)),
 \qquad N_\ell(a)=\#\{i:r_i=\rho_\ell,\ a_i\ne h_i\}.
\]

The interleaved lexicographic potential is

\[
 \mathcal P(a)=(\Lambda_{\rho_1}(a),-N_1(a),\ldots,
                     \Lambda_{\rho_d}(a),-N_d(a)).
\]

For an improving customer moving from `s` to `t`, write
`alpha=p_t(a)` and `beta=(X_s(a)-w_i)/q_s`, so `alpha<beta`. The two
affected prices change as

\[
 (\beta+w_i/q_s,\alpha)\longmapsto
 (\beta,\alpha+w_i/q_t).
\]

At every threshold the sorted clipped vector does not decrease. If
`alpha<rho`, one occurrence of the original smaller value `alpha` disappears,
both replacement values exceed `alpha`, and the block strictly increases;
otherwise both clipped values are unchanged. This multiset argument includes
all ties.

For a foreign H-violating return of customer `i`, the source price after
removal is `>r_i`, so at every `rho<=r_i` the source clipped coordinate is
unchanged. The home clipped coordinate cannot decrease. Earlier threshold
groups' home counts do not change. If all clipped blocks up to `r_i` are
unchanged, the group's away count decreases by one, giving strict progress.

For a strict improvement by a customer currently satisfying H, its
destination has `p_t<e_i<=r_i`. Hence some earlier clipped block increases,
or its own threshold block strictly increases before the corresponding
away-count coordinate can matter. Every permitted improvement and return
therefore strictly increases the same potential.

## Supplied global conclusion and complexity boundary

Starting from `a=h`, repeatedly choose any strict improving customer and any
strict improving destination, then apply repair. Batch boundaries stay
box+H. Each microstep strictly increases the potential. There are only
`S=product_i |A_i|` legal assignments, including repair intermediates.
No assignment repeats, so at most `S-1` microsteps occur. The terminal state
is box+H and satisfies every original customer NE inequality.

For rational inputs let `D` be a common denominator of `c,w`, and let
`L=D*lcm(q_1,...,q_m)`. Since `0<r_i<1`, multiplying clipped coordinates
by L and replacing `-N_l` by `n-N_l` gives bounded integer digits. A base
`1+max(L,n)` representation preserves the lex order and has polynomial
bit length. The supplied result proves finite termination and polynomial
working space with no trajectory storage; it does not prove a polynomial
number of steps. It also does not prove an exponential lower bound.

## Original-model interface in the supplied report

At the canonical greedy layout, freeze single-option customers and all
customers with original weight at least the last score `gamma`. Normalize
remaining weights by gamma, and take
`c_t=W_t^0/gamma-q_t`. The greedy home has maximum reachable multiplicity.
The final actual weight is `W_t=gamma*(q_t+X_t)`. Thus the abstract full box
is precisely the old complete greedy load box, and adding back gamma turns
the abstract NE comparison into `(W_s-w_i)/q_s <= W_v/q_v`.

The current reconstruction proves this interface directly; reverse
realization, perturbation and additional auxiliary sites are unnecessary.
The repository's existing `SC-K-GREEDY-BOX-TO-2` theorem supplies complete
factor-two continuations once this on-path NE is found.

## Source status

The source is a user-provided report. The present repository adds a full
current proof and independent exact implementation attacks. Source authorship,
literature priority, original downloadable code and external peer review are
not certified by this record. The source's self-reported finite checks are
not counted in the new frozen repository audit.
