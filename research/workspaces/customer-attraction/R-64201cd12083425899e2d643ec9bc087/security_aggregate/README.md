# Aggregate security investigation, 2026-10-21

Scope: finite common catalog, unit customers, arbitrary historical ties, full
ordered-history pure SPE.  No general half-coverage proof or aggregate-security
proof has been obtained here.  These are private research checkpoints, not
promoted claims.  No shared maps or git state were modified.

## Exact obstruction to a restricted static dual

A tempting aggregate bridge is to draw the static opponent background by
deleting one player from the actual terminal profile.  Even **arbitrary**
mixing on those deletions is insufficient.

Use the existing 36-client, six-theme instance: X={0,1,2}, Y={3,4,5}; every
cross pair has one unit customer, and every two-X/two-Y subset has three.
The full strategy chooses 0 at root, the opposite group's least label second,
then the second action's group's least unused label.  It is a full SPE at all
43 ordered histories, with terminal z=(0,3,4), payoffs (10,12,12), and W=34.

The actual deletion backgrounds are (3,4), (0,4), (0,3).  Query label5 receives
12 against **each** of them.  Consequently every static distribution supported
on actual deletions has maximum query payoff at least12>34/3.  It cannot certify
v_3<=W/3.  This is only a support restriction failure: the actual v_3 is10,
so W>3v_3.  The already-known root-menu obstruction and this deletion-support
obstruction concern different menus.

There is also a nearby fractional version.  Put L_x=(2/3)c_x(z), and define
g(a)=sum_{x in a}1/(1+L_x).  The exact six action values are

    (43/5,373/35,373/35,65/7,65/7,397/35).

Thus max g(a)-W/3=1/105>0.  Replacing the random deletion background by its
mean load almost repairs this particular example, but does not give the exact
candidate max g<=W/3.  No universal weakened coefficient was established.

`deletion_obstruction.py` independently expands all 36 unit customers, checks
all 258 action comparisons, and verifies both obstructions by Fraction.

## Exploratory residual-aggregate tests

Candidate (OPEN): for every legal fixed background b and r remaining players,
their aggregate payoff P_r(b) is at least r times the static mixed-security
value v_r(b).  This is stronger in scope than the root aggregate bridge.
The known negative one-step security-chain increment does not refute it.

`probe.py` computes all realizable pure-SPE terminal count vectors with the
set-valued backward recursion.  Integer payoff scaling makes those comparisons
exact.  It screens security by a numerical LP, so positive or negative
security gaps require exact follow-up.  Three completed runs found no failure:

* r=3, six themes, three legal background actions: 1000 random games.
* r=4, seven themes, two legal background actions: 1000 random games.
* r=5, seven themes, one legal background action: 300 random games.

Customer types were independently present at density .1, .3, or1, with integer
multiplicities1..10.  The minimum observed ratio P_r/(r v_r) was1 in simple
repeat equilibria.  The saved JSON files state the exploratory status; none of
these runs proves a universal inequality.

`cone_probe.py` instead fixes the old three-player two-group full rule, adds
one through six legal background actions, and varies the whole nonnegative
customer-mass cone.  For each sampled query distribution p it solves the
linear cone separation problem max(3t-P), with t bounded by all static opponent
backgrounds.  In1500 samples it found no positive gap.  This tests fixed p
samples only, and does not prove even that one residual policy cone safe.

`pair_probe.py` screens the new two-step-chain candidate

    u_i+u_(i+1)+(r-2)V_(i+2)-r V_i >=0,

using exact ordered paths recovered from the full outcome sets and numerical
security values.  Its run status and any completed sample count must be read
from the saved JSON; it is not a proof.

Next useful work: prove or refute a two-step/global background budget using
all independent off-path histories.  Actual-profile deletion support is
definitively unavailable; the static dual needs genuinely off-path action
combinations.  No permission, plan, or finite test substitutes for that bridge.
