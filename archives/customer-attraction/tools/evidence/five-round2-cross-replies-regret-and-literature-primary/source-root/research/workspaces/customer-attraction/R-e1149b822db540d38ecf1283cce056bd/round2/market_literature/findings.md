# Five-player market-sharing literature and an actual continuation mechanism

2026-10-25. This branch does **not** prove Q-CAG-HALF-5 and does not produce a
half-coverage counterexample. Its useful outputs are an exact additive-defect
version of the literature's payoff-guarantee mechanism, and a compact fully
audited five-player obstruction to removing that defect.

## Primary-source checks (not new mathematical results)

Source: J.-T. Brethouwer, *The quality of equilibria in generalized market
sharing games*, University of Twente MSc thesis, 2018,
https://essay.utwente.nl/76986/1/Brethouwer_MA_EEMCS.pdf .

* Definition 6.15, printed p.33 / PDF p.33 (zero-index page 32): covering games
  allow arbitrary player-specific catalogs. Generalized market sharing games
  retain downward closure (§4.1, printed p.14).
* Definition 7.2, printed p.39 / PDF p.39: shared misery requires an entrant who
  harms an earlier player to have instantaneous utility no greater than that
  player's new instantaneous utility. Lemma 7.4, p.40, turns nondecreasing
  availability bounds into terminal payoff guarantees. Theorem 7.5, p.41,
  gives welfare at least `n*l` for symmetric shared-misery games.
* Theorem 7.6, printed p.41, remains a symmetric **singleton** theorem.
  Arbitrary topic bundles do not satisfy its hypotheses.
* Theorem 6.22, printed p.38, reports a four-player lower bound above two for
  arbitrary player-specific catalogs; it supplies no incidence matrix there.

Retrieval evidence: the original PDF was opened and the relevant passages read;
the tool references for parent reopening are attached to the source claims:
genui{"citation":{"refs":["turn29view0","turn29view1","turn2view2","turn3view0"]}}

The 2019 one-page author abstract was also located at
https://ris.utwente.nl/ws/portalfiles/portal/101071923/Abstract.pdf . It is not a
replacement for the thesis's exact hypotheses. The direct open failed, so no
new theorem is inferred from that failure. Current targeted searches found no
additional directly applicable theorem; this is not a nonexistence or novelty
claim. Deng et al. v2 was opened at
https://arxiv.org/html/2307.07174v2 ; its conclusion still states the conjecture.

## Claim ML-DEFECT-5: actual continuation payoff guarantee with a paid defect

### Exact statement and domain

Use exactly CAG-MODEL with five unit providers, finite unit customers, arbitrary
finite nonempty common catalog, empty topics and repetitions allowed. Fix any
complete ordered-history pure SPE, with all history-dependent ties retained.
For each partial ordered history `h`, write `w_i(h)` for player `i`'s payoff if
the game stopped at `h`. Define the global last-seat availability

`theta = min_(|h|=4) max_(T in S) w_5(h,T)`.

For `j=2,3,4,5` define `epsilon_j` as the maximum of zero and all numbers

`w_j(h,T) - w_i(h,T)`

over legal ordered histories `|h|=j-1`, earlier `i<j`, and legal `T` such that
`w_i(h)>w_i(h,T)`. These maxima exist (the indexing sets are finite); an empty
index set gives zero. Let `E=max(epsilon_4,epsilon_5)`. Then every such SPE obeys

`u_5,u_4 >= theta`,

`u_3 >= theta-E`,

`u_2 >= theta-epsilon_3-E`,

`u_1 >= theta-epsilon_2-epsilon_3-E`,

and hence

`W >= 5 theta - epsilon_2 - 2 epsilon_3 - 3 E`.                 (D5)

In particular, with `epsilon=max_j epsilon_j`,

`W >= 5 theta - 6 epsilon`.                                  (D5-uniform)

Using the already proved `theta>=OPT_5/9`, the sufficient condition

`epsilon_2+2 epsilon_3+3 E <= theta/2`

implies `2W>=OPT_5`. This is a **conditional** five-player theorem, not the
unconditional target. No bound paying this defect in general is claimed.

### Dependencies and proof

Every partial decision history has an instantaneous action worth at least
`theta`: pad that history arbitrarily to length four, choose a best final
action there, and use monotonicity under the removal of the padded providers.
This uses common catalogs, retains repetitions, and does not assert a chosen
SPE ever follows the padding.

The last two players each receive at least `theta`, at every legal length-three
history. For the penultimate player this is the existing exact identity

`U_p(A,B)-U_p(B,A)=F_p(A)-F_p(B)`,

where `F_p(A)=sum_(x in A)1/(p_x+1)`. Choose a legal maximizer of `F_p`; every
true last reply to that deviation gives the deviator at least the last reply's
payoff, which is at least `theta`. This imports only the already established
CA-LAST-TWO-FLOOR mechanism, not any SPE-to-PNE assertion.

Now induct backward from these last two guarantees. At the current decision
node let the current player deviate to an instantaneous action worth at least
`theta`, and follow **the original strategy's true continuation**. If no later
entrant harms the current player, its terminal payoff is at least `theta`.
Otherwise let `j` be the last entrant that harms it. Its terminal payoff equals
its instantaneous payoff just after entrant `j`, so the definition of
`epsilon_j` gives

`u_current >= w_j(after j)-epsilon_j >= u_j-epsilon_j`.

The induction hypothesis applies to player `j` in this genuine off-path
subgame, because it is a restriction of the same complete SPE. Thus the
current deviation gives at least the stated lower bound; current-node SPE IC
pays that same bound to the actual player. For player 3 the loss is at most
`E`; for player 2 it is at most `epsilon_3+E`; for player 1 it is at most
`epsilon_2+epsilon_3+E`. Summing proves (D5).

This is the useful repair of the thesis's mechanism: its exact stopping rule
is the **last actual harm in the true continuation**, and every loss has an
explicit additive bill. The argument never freezes a follower's terminal
action and never assumes ties at different histories agree.

### Explicit model bounds on the bill

If the entrant chooses `B` and the earlier player chose `A`, then immediately
after entry the common customers contribute equally to both. Consequently

`w_j-w_i = sum_(x in B\A) 1/(p_x+1) - sum_(x in A\B)1/p_x`

where `p_x` is the pre-entry load, positive on `A`. Harm requires `A∩B` nonempty.
Therefore

`epsilon_j <= max_(A∩B nonempty) [|B\A|-|A\B|/(j-1)]_+`

and also `epsilon_j <= max_(A∩B nonempty)|B\A|`. For `j=2` the exact expression
is `epsilon_2=max_(A∩B nonempty)[|B|-|A|]_+`; in particular equal topic sizes
give `epsilon_2=0`. These are legitimate resource-level shared-misery bounds,
but they can be too large to pay (D5) for a general catalog.

### Status, objections, evidence

Status: author-layer exact argument, not independently peer reviewed. It uses
the existing last-two theorem and existing last-seat lower bound. The new
five-position defect recursion is stated and proved above. Zero customers or
all-empty catalogs give all quantities zero. Negative displayed payoff lower
bounds are allowed and harmless. Prefixes remain ordered throughout.

The unresolved objection to an unconditional half proof is not a gap hidden
in (D5): it is the genuinely missing universal payment of its explicit defect.
The next section proves the defect cannot simply be set to zero, even for
equal-size themes and a particularly simple five-player complete strategy.

## Claim ML-AVAILABILITY-5-NO: compact exact obstruction to zero defect

This is a newly computed, separately audited **representation** of a mechanism
already known to fail for every `n>=3` in
`research/current/customer_attraction/aggregate_theta_counterexample.md`.
It does not claim a new failure theorem. Its reusable value is a small
positive-integer five-player instance without a huge Möbius bias or an opaque
stored policy, with equal topic sizes and one simple rule on all histories.

Split ten themes into `X={0,...,4}` and `Y={5,...,9}`. For every subset
`I subset X`, `J subset Y` of the indicated sizes, create the indicated number
of distinct unit customers interested in exactly `I union J`:

| `|I|` | `|J|` | customers for **each** such pair `(I,J)` |
|---:|---:|---:|
|0|2|37|
|1|2|24|
|1|3|3|
|2|0|37|
|2|1|24|
|2|4|5|
|2|5|24|
|3|1|3|
|4|2|5|
|4|4|61|
|5|2|24|

All other interest types have zero multiplicity. There are 5,945 unit customers
and 365 positive types; every topic has size 2,844.

The complete strategy is:

* root chooses `0`;
* player 2 chooses the smallest unused label in the group opposite player 1;
* every player from position 3 onward chooses the smallest unused label in
  **player 2's group**.

This rule is defined at every ordered history, including repetitions: fewer
than five labels have appeared, so the specified group of five has an unused
label. It retains the second ordered action; it is not a policy on counts alone.

The exact results are

`actual path = (0,5,6,7,8)`,

`u=(1107,1115,1115,1115,1115)`,

`W=5567`, `theta_5=1115`, `OPT_5=5575`,

`W-5theta_5=-8`, `2W-OPT_5=5559>0`.

Thus even equal topic sizes and this simple full-history policy do not let
last-seat availability pay each player or total welfare at rate five. The
weaker possible sufficient bridge `W>=(9/2)theta_5` is **not** refuted here.

The same exact verifier also computes the defect parameters in (D5):

`(epsilon_2,epsilon_3,epsilon_4,epsilon_5)=(0,644,2576/3,966)`.

Their bill is `4186`, much larger than `theta_5/2=1115/2`. In this example
the largest violations are witnessed at repeated off-path prefixes; for
instance `(9,9,9,9)` followed by `0` gives the earlier provider `3166/5`
and the entrant `7996/5`, a gap of `966`. Thus taking the **global** misery
defect seriously gives a correct but weak continuation guarantee. Deleting
repeated histories is not a legal way to improve that global definition.

### Exact finite proof and reproduction

`audit_five_availability.py` is a standalone exact verifier containing the
entire instance and rule. It imports neither discovery code, the repository
solver, old certificates, nor an optimizer. Multiplying every payoff by
`lcm(1,...,5)=60` gives integer arithmetic. The script directly reconstructs
customer interest masks and checks every one of the 11,111 ordered decision
histories against all ten legal deviations, following the stated **true**
continuation in each comparison. All 111,110 comparisons pass. It also checks
the 10,000 ordered final prefixes for the exact availability and all 100,000
ordered terminal tuples for the exact optimum. The resulting frozen local
output is `audit_five_availability.json`.

Reproduce from the repository root:

```sh
python research/workspaces/customer-attraction/R-e1149b822db540d38ecf1283cce056bd/round2/market_literature/audit_five_availability.py
```

Discovery only: `probe_availability.py` searched fixed complete count-policy
cones (a subset of allowed strategies), and `probe_group_availability.py`
retained the group of the second ordered action. Their floating results are
not evidence for a universal bound, and not needed by the exact verifier.
The 35-orbit group cone produced rational weights with denominator 1115;
clearing that denominator produced the displayed integer instance.

## What the parent can safely reuse

1. The exact original-source locations, preserving the shared-misery and
   singleton hypotheses.
2. The last-actual-harm proof of (D5), with its explicit still-unpaid bill.
3. The fully reproducible compact five-player zero-defect obstruction.

None of these changes the status of Q-CAG-HALF-5. No finite search or failed
retrieval has been used as a mathematical nonexistence claim.
