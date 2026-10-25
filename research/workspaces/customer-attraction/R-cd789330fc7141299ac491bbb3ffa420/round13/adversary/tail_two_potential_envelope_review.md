# Fixed-background two-player potential envelope: independent review

2026-10-25. Candidate supplied by security13; the algebra below was rebuilt
directly from the payoff definitions, without importing its code or proof.
**Valid local component. It does not establish the five-provider half bound.**
No external-review or novelty claim is made.

## Exact statement

Use the common finite catalog, unit clients/providers, and arbitrary complete
ordered-history pure SPE. Fix any legal ordered background whose client loads
are `q_x >= 0`, followed by exactly two remaining providers. Let their prescribed
actions at this node be `(B,C)`. The original strategy may use any history
dependent ties. For any legal comparison themes `(T,S)`, including empty or
repeated themes, define

`Phi(q) = sum_x H_(q_x)`, with `H_0=0`.

Then

`Phi(q+T+S) - Phi(q+B+C)
 <= sum_(x in B minus C) 1/[(q_x+1)(q_x+2)]`.

Consequently the same upper bound holds with the first potential maximized
over all legal pairs. All sums count actual distinct unit clients; integer
type multiplicities merely compress them.

## Direct proof from three genuine incentives

For legal themes A,D write

`f(A)=sum_(x in A) 1/(q_x+1)`,

`g(A,D)=sum_(x in A intersection D) 1/[(q_x+1)(q_x+2)]`.

The utility of A against D is `f(A)-g(A,D)`, and the two-action potential
increment is

`P(A,D)=Phi(q+A+D)-Phi(q)=f(A)+f(D)-g(A,D)`.

These formulas remain exact for A=D. Let Q be the **same original strategy's**
last action after the first remaining provider is forced to choose T. The
following three quantities are nonnegative:

`I1 = f(B)-g(B,C) - f(T)+g(T,Q)`;

`I2 = f(Q)-g(T,Q) - f(S)+g(T,S)`;

`I3 = f(C)-g(B,C) - f(Q)+g(B,Q)`.

I1 is the first remaining provider's actual-node deviation to T, I2 is Q's
genuine last-node comparison to S after T, and I3 is C's genuine last-node
comparison to the legal catalog theme Q after B. Q is not frozen from any
other branch. Adding gives the exact identity

`P(B,C)-P(T,S) = I1+I2+I3 + g(B,C)-g(B,Q)`.

Since `B intersection Q` is contained in B, `g(B,Q) <= g(B,B)`. Thus

`P(T,S)-P(B,C)
 <= g(B,Q)-g(B,C)
 <= g(B,B)-g(B,C)`,

and the last difference is exactly the displayed B-minus-C sum.

## Relation to the existing two-player tax identity

This is the same three-IC mechanism used in
`research/current/customer_attraction/two_remaining_tax.md`, with the
comparison-overlap term retained. The existing remainder-profit expression is
`R(T,S)=f(T)+f(S)-2g(T,S)`. Since `P(T,S)=R(T,S)+g(T,S)`, the complete identity
there already supplies this potential version before discarding its
nonnegative comparison-overlap credit. This review certifies the reformulated
interface; it does not claim a newly discovered incentive mechanism.

## Scope limitations

The bound controls a fixed genuine two-provider subgame. Its tax belongs to
that same node and its prescribed first tail theme B. Taxes from mutually
exclusive nodes cannot be added and charged to root welfare without an
additional joint budget. Applying the statement to a five-provider root's
last two providers is valid, but no unproved relation between the resulting
potential envelope and `OPT5` is used here.
