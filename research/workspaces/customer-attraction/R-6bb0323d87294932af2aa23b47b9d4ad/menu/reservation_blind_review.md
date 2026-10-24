# Independent definition-level audit: reservation lift positive-depth security witness

2026-10-24. **PASS for the precise finite counterexample below.** General Q-CAG-HALF, aggregate security, Mfull, and Mpath remain OPEN. This review does not claim a new SPE construction or prove the general reservation lift: it independently checks the supplied concrete full policy and the exact static minimax certificates.

The audited claim is the negation of the universal positive-depth original-total-population floor

    for every full-history pure SPE with m players and every i≥2,
    u_i≥v_m(0).

Here v_m(0)=max_p min_(B∈S^(m−1)) E_(T~p) Σ_(x∈T)1/[1+c_x(B)]. The rivals are a static joint tuple independent of the query draw. This is not an iid benchmark and not the extra-one value v_(m+1).

## Raw inputs and independence

Only the following source data are read:

- sibling `../security/positive_depth_floor_game.json`: four players, seven common topics and unit-customer type multiplicities;
- sibling `../security/positive_depth_floor_certificate.json`: a complete ordered-history action table and rational primal/dual minimax candidates.

`reservation_blind_review.py` imports only Python standard-library modules. It does not import the canonical model, SPE solver, source audit, discovery script, numerical optimization library, or source audit outputs. Every multiplicity is expanded into distinct unit customers. The 53-customer catalog has seven pairwise different nonempty covered sets. Topic B (label 6) consists of 19 customers disjoint from the other six topics.

## Full-history SPE verification

The policy specifies exactly all

    1+7+7²+7³=400

ordered decision histories. The auditor independently rebuilds every terminal leaf by following the policy; it does not use claimed terminal targets to compute continuation payoffs. It then checks every history and every legal forced current action using that action's true prescribed later continuation.

All 2,800 comparisons, including self actions, pass exactly in Fraction arithmetic. Among the 2,400 nonself comparisons, 2,219 are strict and 181 tie. Thus arbitrary equal-count histories are not identified, and all off-path histories are checked. This is sufficient by backward induction for the supplied full policy to be a pure SPE.

The actual path, final payoffs and welfare are

    (B,X0,Y0,Y1),
    u=(19,29/3,67/6,67/6),  W=51.

Root forcing any old topic yields root payoff 29/3; root B yields 19. Enumerating all 7⁴ ordered comparison tuples gives OPT_4=53. None of these facts relies on the general lift theorem.

The finite data also satisfy the announced lift hypotheses: old topic sizes are `(23,23,21,23,23,21)`, each δ_T=min_S|T∩S| is 11, max_T(|T|−δ_T/2)=35/2≤19, and min_T|T|/2=21/2>19/3. The inherited all-old tail policy has minimum prescribed payoff η=29/3≥19/2.

## Exact security value from both directions

The supplied primal query distribution is

    p=(570,570,1197,570,570,1197,1174)/5848.

Its entries are nonnegative and sum to one. For each of all 7³=343 ordered three-rival tuples, including repeats and every permutation, the independent auditor computes its expected query payoff directly from the 53 distinct unit customers. The minimum is exactly

    v=28481/2924.

There are 48 tight ordered rival tuples. Therefore p proves the lower bound v_4(0)≥v.

For the upper bound, the supplied static rival distribution is supported on

    012,016,026,126,346,356,456

with respective probabilities

    (370,3941,1481,1481,4089,1629,1629)/14620.

The auditor verifies normalization and independently evaluates each of the seven pure query topics. All seven expected payoffs are exactly 28481/2924. Thus every mixed query is at most v against this one independent rival distribution. This proves v_4(0)≤v without treating the LP's numerical output or support selection as proof.

Together the certificates give

    v_4(0)=28481/2924,
    v_4(0)−u_2=647/8772>0.

Position 2 is at the genuine positive-depth actual history `(B)`. Hence the claimed positive-depth original-total-m floor is false.

## Limits and replay

This witness strictly satisfies the aggregate and half inequalities:

    W−4v_4(0)=8800/731>0,
    2W−OPT_4=49>0.

It does not refute either statement, the extra-one bridge, or any unrestricted full-menu bridge. The audit proves one complete strategy is a counterexample to a universal position-wise assertion; it makes no assertion about every SPE of this instance.

Replay from the repository root:

    python research/workspaces/customer-attraction/R-6bb0323d87294932af2aa23b47b9d4ad/menu/reservation_blind_review.py

The exact output is `reservation_blind_review.json` in this directory. The supplied raw policy remains the source witness; this review is an independent verification layer.
