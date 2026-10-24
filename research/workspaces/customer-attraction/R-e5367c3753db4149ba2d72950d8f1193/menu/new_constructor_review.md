# Independent audit: first-reservation insertion at every no-B history

2026-10-24. Independent reconstruction from the parent's theorem statement,
before reading the other auditor's proof. **PASS** for the general n>=2
constructor below. This is a full-history embedding theorem for arbitrary old
common catalogues; it is not a proof or counterexample for Q-CAG-HALF. No
external review or novelty certification is claimed.

## Precise constructor and hypotheses

Let n>=2. Take any finite old unit-customer common-catalogue game and any
complete history-dependent pure SPE sigma for n players. Assume every
prescribed final payoff at every old ordered decision history is at least
eta>0. Define

    delta_T = min_(S in old catalogue) |T intersect S|,
    L = max_(T in old catalogue) [|T|-delta_T/2].

Add a disjoint topic B consisting of J distinct new unit customers and add
one new first player, where J>0 is an integer and

    J/2 <= eta,   J >= L.                           (H)

On every new nonterminal ordered history h use the following policy:

1. If h contains no B, prescribe B.
2. If h contains exactly one B, erase that B, retaining the order of all old
   actions, and prescribe sigma on the resulting old history.
3. In every subtree rooted when the second B first occurs, choose an arbitrary
   complete pure SPE by backward induction.

All of these second-B subtrees are disjoint, and their descendants never
return to the first two regions. Every nonterminal history belongs to exactly
one of the three cases. In case 2, erasing B leaves at most n-1 actions, so the
old policy call is well-defined. Repeated old actions, arbitrary off-path old
histories, and history-dependent old tie choices remain valid.

## Independent full-history proof

### Exactly one B

Fix any such h, and erase B to obtain the old ordered history g. If all later
players follow the policy, every later action is old and is prescribed by
sigma on its erased history. Thus the old-action projection of the full
terminal is exactly the terminal obtained from g under the original sigma.
The unique B has no effect on any old customer's load.

For a deviation to another old topic T, the B count is still one. The
projected terminal is therefore exactly the original old forced-T terminal
at g, followed by the same old sigma. Consequently the new comparison equals
one genuine old SPE IC row, including the old policy's true history-dependent
continuation. The prescribed old payoff is at least eta.

For a deviation to B, there are already two B coverers. The deviator's payoff
is at most J/2, regardless of which complete SPE was selected in that second-B
subtree. It is therefore at most eta and cannot beat the prescribed action.

This argument works at the last player as well as every earlier history.

### No B

Let h be any no-B nonterminal history of length d<=n. The prescribed B is the
only B in its prescribed continuation: afterward case 2 always prescribes
old actions. Thus the current player's prescribed payoff is exactly J.

Force an old action T instead.

- If d<n, the next player is at another no-B history and therefore chooses B.
  Thereafter case 2 gives only old actions. The terminal contains n old
  actions, including the forced T. Since n>=2, at least one **other** old
  action S occurs.
- If d=n, the deviator is last and the terminal has n+1 old actions. Again at
  least one other old S occurs.

Every customer in T intersect S has at least two coverers, and all other
customers of T yield at most one unit to the deviator. Hence its actual
forced-terminal payoff, without any condition on the order of S, is

    d_T <= |T|-|T intersect S|/2
         <= |T|-delta_T/2 <= L <= J.

This proves every no-B IC row, including root deviations and last-player
deviations. It needs no condition saying that an arbitrary continuation after
T must avoid an all-B suffix: the policy itself prescribes exactly one first
B and then the original old policy.

### Two or more B

Every such history lies in a chosen complete BI subtree. All its IC rows hold
by that subtree's SPE property. The estimates above did not impose any
further restriction on its selected tie choices.

Together these three cases prove a complete pure SPE on all ordered new
histories. Its actual path is (B,z(sigma)). At every history after initial B
and without another B it literally follows the entire old sigma, not just the
old actual path. In particular all old forced-action menu columns are retained
as required in `reservation_menu_budget_closure.md`.

## One old player: the necessary extra condition

For n=1, let K=max_T |T|. The same constructor works under J/2<=eta and J>=K.
The one-B comparisons are unchanged. At a no-B root, forcing T is followed
by the final player's first B, so the root gets |T|<=K<=J. At a no-B last
history, an old deviation earns at most K, again no more than J.

Moreover J>=K is **necessary for this exact policy**: at the root, forcing
a maximal old topic yields K, while prescribed B yields J. The intersection
condition J>=L alone cannot replace this. For old catalogue {A} with |A|=3
and J=2, eta=3 and L=3/2, so both displayed conditions (H) hold, yet root B
pays 2 and root A followed by prescribed B pays 3.

This n=1 failure does not contradict the audited n>=2 theorem: its no-B
forced-root terminal contains only one old action, so the proof's second old
coverer does not exist.

## Exact boundary checks

`audit_stronger_constructor.py` imports neither the canonical CAG model nor
the original reservation audit. It expands distinct unit customers, constructs
all ordered histories, fills all second-B subtrees by exact backward
induction, and computes every forced-action payoff with Fraction.

The general n>=2 theorem does not depend on these finite checks. They verify
a concrete boundary excluded by the previous strict constructor, and the
precise n=1 scope issue:

| Input | Full histories / IC comparisons | Outcome |
| --- | --- | --- |
| old n=2, catalogue {A}, A has 3 customers, J=3 | 7 decision histories, 14 comparisons | Complete SPE; actual B,A,A; minimum slack 0 |
| old n=1, catalogue {A}, A has 3 customers, J=2 | 3 decision histories, 6 comparisons | Root IC fails by exactly 1 |
| old n=1, catalogue {A}, A has 3 customers, J=3 | 3 decision histories, 6 comparisons | Corrected constructor is a complete SPE |

In the first row, eta=3/2 and J/2=eta; the former extra condition
|T|/2>J/n fails at equality 3/2=3/2. Thus this is a real full-history test of
the strengthened theorem's additional coverage, rather than a test already
covered by the old strict hypotheses. Full policies and all exact rows are
in `audit_stronger_constructor.json`.

## Audit conclusion and remaining limits

No fatal objection found. The old strict condition |T|/2>J/n is unnecessary
for n>=2 under this new global first-B policy. This is a new explicit credible
constructor, while the separate quantitative menu-budget closure needs only
the existence of a literal lift and its stated numerical bounds. Neither
result proves that arbitrary SPEs satisfy the unrestricted menu budget.
