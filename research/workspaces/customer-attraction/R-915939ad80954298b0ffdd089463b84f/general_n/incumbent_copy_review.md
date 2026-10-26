# Independent scope and arithmetic review of the incumbent-copy obstruction

Reviewer: delegated researcher in R-915939ad80954298b0ffdd089463b84f.
This review inspected `../incumbent_copy/obstruction.md`, `verify.py`, and
`exact.json`. It did **not** rerun the 19,531-node ordered-tree calculation.
It is an independent mathematical/code inspection, not a second independent
execution or an external review.

The statement being refuted is correctly quantified over *all* SPE
continuations after a fixed first action, followed by existence of a
minimum-incumbent-payoff continuation satisfying static copy stability.
If the reported terminal-count enumeration is correct, uniqueness of the
count vector is enough to refute this existential repair: both the
incumbent payoff and each topic holder's static copy payoff depend only on
that vector, not on the terminal order.

The implemented recursion is exact. At ordered history h, let R_a be the
SPE endpoint set of child a. Endpoint z in child a can be selected precisely
when its current-player payoff is at least
`max_b min_{y in R_b} u_current(y)`. Necessity follows by considering the
actually selected off-path continuations. For sufficiency select z in the
chosen child, and independently select a minimizing endpoint in every
other child. Those child subtrees are disjoint ordered histories. Including
the chosen child's minimum in the maximum adds no restriction beyond
`u_current(z)>=min_{R_a} u_current`. Thus no anonymous tie rule is imposed.

The arithmetic has a particularly transparent decomposition. The reported
actual count vector is q=(1,1,1,2,1), and replacing the topic-4 player by
topic 0 while freezing its successors gives q_static=(2,1,1,2,0).
The actual continuation after that deviation instead has
q_true=(2,1,0,2,1). Direct per-type summation gives

* current topic-4 payoff: 20/3;
* static topic-0 copy payoff: 41/6;
* true topic-0 copy payoff: 37/6.

Moreover, the entire static-to-true loss of 2/3 comes from the four
customers interested in {0,4}: their contribution to the copying player
drops from 4/2=2 to 4/3. The customer of type {0,2,4} has denominator 3 in
both profiles; all remaining topic-0 customer types also have unchanged
denominators. Hence

`static gain 1/6 - continuation-reset loss 2/3 = true gain -1/2`.

The actual theme payoffs
(31/3,19/3,19/3,23/3,20/3) sum with counts q to 45. Every listed customer
type is covered, so W=45=OPT_6 without any optimization calculation.
All later players' payoffs are below 31/3, also disproving the stronger
suggested individual incumbent-payoff floor at such a minimum leaf.

No flaw was found in the stated scope, arithmetic, or exhaustive-recursion
contract. Acceptance of the *computed* uniqueness claim here remains
conditional on the recorded execution of the inspected exact program;
the parent has two separate executions. This is not a counterexample to
half coverage, and does not rule out a joint budget retaining the 2/3
continuation-reset loss.
