# Independent mathematical review of heterogeneous prefix repair

2026-10-24. Reviewer: potential/exchange subagent. The blind reconstruction
`blind_repair_reconstruction.md` was saved before reading the author's
`../credible/heterogeneous_prefix_repair.md`. This review is a direct analytic
check, independent of the finite ordered-history audit. Original Q-CAG-HALF
remains OPEN. No new welfare theorem is inferred.

## Verdict

The claimed repair construction is correct, including arbitrary interleaved
marked positions, every ordered-history continuation, joint Cartesian-product
deviations, and the common integer scaling. I find no fatal objection.
The useful new statement is an exact reduction with half-gap repair loss
`2 sum_i delta_i + max_i delta_i`; it is not an unconditional robust upper
bound or an unconditional half proof.

## Input and exact reduction

Let an arbitrary m-player target terminal z have a specified genuine complete
SPE after a normal prefix of length j<m. The special contract in the task has
j=m-1 and only requires that the last target action be a best reply.
For each earlier normal prefix h_i, define

  ell_i(A)=min over complete SPEs in the true child (h_i,A) of player i's payoff,
  M_i=max_A ell_i(A), delta_i=(M_i-u_i(z))_+,
  D=max_i delta_i, R=sum_i delta_i.

Finite-tree pure SPE existence and finiteness give genuine attaining child
strategies. For D>0 the repaired product instance has, before common scaling,

  W_new=W+mD+R,
  OPT_new,m=OPT_m+(2m-1)D,
  OPT_new,m-2W_new=OPT_m-2W-(2R+D).

The minima in ell are over complete child SPEs with the exact old ordered
prefix fixed. Replacing ell by the utility of an arbitrary frozen old tail
would change the statement and invalidate the product proof.

## Independent all-history verification of the insurer

Take a layer of size s, marks I subset [m-1], k=|I| and d=m-k>=1. Divide by s.
There are k disjoint banks of size 2, a reservoir Y of size d, and d-1 leaves
of size 1. A normal terminal chooses each bank at its marked position and Y
elsewhere. Thus marked utility is 2, unmarked utility 1, welfare m+k, and
m-action optimum 2m-1. The last position is unmarked.

Fix any normal prefix and force an arbitrary current action. A previously
occupied bank already has load at least 2, and any leaf has size 1. The fixed
current player then has raw payoff <=1, regardless of future behavior;
attach an arbitrary complete BI continuation.

For forced Y use Y mode: clean histories have each bank at most once, no
leaves, and Y at most d times. Prescribe a fresh bank while one exists, then
Y. After every clean choice, including choices in an order different from
the prescription, the cleanup terminal has all k banks once and Y exactly
d times, since these counts total m. Every future fresh-bank chooser earns
2 and every Y chooser earns 1. Choosing a different fresh bank gives 2 and
choosing a clean early Y gives 1. Every first dirty action has raw payoff
<=1: a repeated bank, a leaf, or a Y beyond load d. Switch permanently to
an arbitrary complete BI strategy at every first dirty child. Backward
induction on every clean ordered history proves the remaining strategy SPE.
The fixed forced Y finally has payoff 1.

For forced fresh bank F use F mode: keep F at load 1, all other bank loads
at most 1, leaves absent, and Y at most d-1. Prescribe fresh banks first,
then Y until load d-1, then a final duplication of F. If p earlier banks
and q earlier Y copies existed, the number of remaining actions is

  (k-p-1)+(d-1-q)+1=m-i.

Hence every clean history reaches the same counts just before the last
choice: all banks once and Y d-1 times, totaling m-1 actions. That final
player duplicates F. Future fresh banks earn 2; future Y players earn
`d/(d-1)` when d>1, a number in (1,2]; the final F copier earns 1.
At a fresh-bank node, a different fresh bank also earns 2 and clean Y
earns at most 2. At a Y-phase node every non-Y action has raw cap 1.
A first dirty action is a repeated bank (including an early copy of F),
a leaf, or Y reaching at least d; each has raw cap <=1. Attach permanent
complete BI continuations there. At the final copier node, Y gives d/d=1
and every bank or leaf gives at most 1. This proves SPE at every clean
ordered history and every dirty subtree. The initially forced F earns 1.
For d=1 the Y phase is empty; the same terminal and raw-cap argument
applies without writing d/(d-1).

This is stronger than checking a static NE terminal. In particular, the
proof handles early clean Y choices, permutations of fresh-bank choices,
and all first exits. The permanent-mode rule prevents an off-path history
from reentering a clean or normal path by matching counts later.

## Independent product and layer accounting

For distinct positive deficit levels 0=e_0<...<e_L=D use thickness
s_l=e_l-e_(l-1) and marks I_l={i:delta_i>=e_l}. Then

  sum_l s_l=D,
  sum_(l:i in I_l) s_l=delta_i,
  sum_l |I_l|s_l=R.

Thus normal position i earns insurance D+delta_i (D in the genuine old
tail). If the first joint old/layer deviation occurs at normal position i,
use the ell_i(A)-attaining old child and one low-exit child in each layer.
The joint deviation payoff is at most

  ell_i(A)+sum_l s_l <= M_i+D <= u_i+delta_i+D,

exactly the planned total payoff. This covers changing several coordinates
at once, keeping the old coordinate while changing insurance, and keeping
all insurance coordinates while changing the old coordinate. No component
continuation is asserted to be SPE before it is selected: all permanent
threat children are genuine complete component SPEs. In a permanent product
mode, every joint deviation changes total payoff by the sum of independent
component payoff changes, each nonpositive. Backward induction over normal
prefixes therefore gives a complete product SPE retaining z in its old
coordinate.

The insurer has exactly m catalog blocks. Each component optimum can be
realized with m actions and paired positionwise with an old m-action
optimum; the full Cartesian catalog permits each pairing. This proves exact
OPT additivity, not merely an upper or lower estimate.

D, R and layer sizes are rational. Multiplying every old and new client
block by a common denominator L restores literal integer multiplicities;
all clients/providers remain unit, and all identities are multiplied by L.

If D=0 no layer is needed. Starting at the genuine tail and going backwards,
retain the normal action and attach ell-attaining complete threats for each
different old action. These give at most M_i<=u_i, so z itself is realizable
by a complete SPE. This separately handles the zero endpoint without
zero-size insurer blocks.

## General and m=5 stress test

The construction is uniform in m and the old catalog; no fixed-player
lemma carries its correctness. Directly setting m=5, j=4 gives

  W_new=W+5D+R,
  OPT_new,5=OPT_5+9D,
  repaired half gap=(OPT_5-2W)-(2R+D).

Here D<=R<=4D. A single isolated positive deficit costs 3D; four equal
deficits cost 9D. Interleaving of marks is unrestricted by the clean proof.
A positive old gap exceeding 2R+D yields a genuine five-player half
counterexample after repair. No such path is supplied by this theorem.
Conversely OPT_5<=2W+2R+D is obtained only conditional on the original
general half statement (or on an independently proved robust budget).
For an actual SPE all deltas vanish, so that conditional robust inequality
returns exactly the original missing half conclusion. The pressure test
therefore confirms the reduction and a sharper nonuniform repair cost;
it does not cross factor two unconditionally.

## Relation to prior potential route

The repair does not permit dropping old-player refunds in the nonroot
identity DeltaW=DeltaV+DeltaP_old-Gamma. Each insurance component is paid
in its actual terminal and all altered branches are genuine SPEs, so the
construction bypasses a cross-branch refund estimate rather than proving
one. The earlier endpoint-potential and optimal-prefix insertion obstacles
remain logically unaffected.
