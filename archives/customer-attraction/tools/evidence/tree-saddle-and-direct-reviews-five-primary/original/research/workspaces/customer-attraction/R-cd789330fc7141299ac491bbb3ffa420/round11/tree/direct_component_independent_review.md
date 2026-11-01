# Direct11 terminal bank and endpoint reduction: independent review

2026-10-25, tree11. Scope is the original arbitrary-player/common-catalog/
complete ordered-history model, with arbitrary ties and repeated/empty themes.
**General HALF, ROW, root-free ROW and favorable matching remain OPEN.**

Source checked:
[`../direct/direct_general_working.md`](../direct/direct_general_working.md).
This is internal mathematical review, not external review or a novelty claim.

## Terminal identity

Let P be the actual prefix support before the last player, b its load, and S
the last chosen theme. For any legal whole T, direct expansion of the last
payoff difference Gamma(T) gives

    W-|T|=Gamma(T)
              +sum_(x in P\T)b_x/(b_x+1)
              +sum_(x in P\S)1/(b_x+1).

For example x in (P intersect T)\S contributes -1/(b+1) in Gamma and the
same positive amount in the last bank; x in (P\T) intersect S contributes
1/(b+1)+b/(b+1)=1. For x outside P the identity is just the difference of the
two membership indicators. These cases exhaust all memberships.

Only actual last best-response optimality makes Gamma>=0. Hence W is at
least every legal theme's size even when all earlier prescribed actions are
arbitrary. An earlier fixed background beta with support H is contained in P
with b>=beta, so dropping nonnegative terms gives

    W>=|T|+sum_(x in H\T)beta_x/(beta_x+1).

My first independent all-tail argument had denominator beta+r. Direct11's
last-BR form is stronger and supersedes it. These banks remain tied to this
one actual terminal prefix; no sum over forced-root branches is paid here.

## Endpoint envelopes

Fix the actual child A and a realizable actual endpoint Z with current
payoff t. In every other immediate ordered child T, the minimum current
payoff p_h(T) over complete tail SPEs exists. Off-child histories are disjoint,
so independently choose each minimizing SPE and splice them with the given
actual child realizing Z. This proves the exact least comparator-row value

    n_A t+sum_(T!=A)n_T p_h(T).

The coefficient n_A must multiply t: that branch is already fixed. Current
node SPE support is equivalent to t>=max_T p_h(T), since p_h(A)<=t already.
This verifies ENV and its diagonal correction. At a nonempty h it is an
envelope for the local node class, not a statement that such an endpoint
extends to a whole-game SPE which reaches h.

Small terminology precision: same-count histories have the same possible
terminal **count** outcomes (or corresponding suffix outcomes after retaining
their respective fixed prefixes). Their full ordered profiles cannot be
literally identical when their fixed prefix orders differ. The argument does
not identify their independently selected original-policy continuations.

## Optimal tuple exchange

Write D_j=T_j\union_(l!=j)T_l for the exclusive block of slot j in an
optimal m-tuple with union C. Replacing slot j by a legal B gives

    |B\C|+|B intersect D_j|<=|D_j|,

so |B\C|<=|D_j\B| exactly. Replacing an arbitrary equal number of slots by
arbitrary legal topics gives the stated joint OPT-EX inequality by the same
union comparison. No equilibrium fact is used. Reusing D_j's capacity for
several branch topics is not authorized by this one-exchange relation.

## Named root-free pressure

[`attack_rootfree_named.py`](attack_rootfree_named.py) independently reads
three explicitly named old raw-policy packets, rechecks all strict-descendant
ICs with Fraction, permits every possible root action as the actual root,
and enumerates every m-slot comparator multiset. The precise candidate is

    W(arbitrary prescribed root)+sum_j d_root(T_j)>=|union_j T_j|.

The minimum gaps are 11/2 for the compact ten-client policy, a positive
650970032217399586 for the old huge StrongA five-player packet, and 2 for the
six disjoint themes of sizes (3,3,1,1,1,1). Full exact outputs and source
hashes are in [`rootfree_named_pressure.json`](rootfree_named_pressure.json).
There was no policy/customer/parameter search and no general inference from
these finite nonseparations. The five-player named packet is only pressure on
this general candidate; it is not a five-player positive theorem or HALF
counterexample.
