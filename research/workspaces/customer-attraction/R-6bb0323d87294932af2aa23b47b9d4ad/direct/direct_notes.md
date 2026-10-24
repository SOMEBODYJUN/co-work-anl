# Direct owner charging: current deductions and unclosed links

2026-10-24. This is an exploratory checkpoint, not a claimed theorem or a new
mathematical asset. All references below are internal repository derivations;
no external theorem was imported. Main Q-CAG-HALF remains OPEN.

## 1. Correct direct charge and a withdrawn stronger candidate

Fix a complete pure SPE with actual covered set C, welfare W=|C|. Fix one
optimal m-index tuple T, with union O. Write

    D=O\C,  I=O∩C,  G=C\O.

The correct target is |D|−|G|≤W, equivalently |D|≤|I|+2|G|.
A tempting stronger residual claim max_(m legal topics B)|union B\C|≤W was
withdrawn immediately when the parent supplied its exact existing refutation:

    research/workspaces/customer-attraction/
    R-acd97406d8c4409d962eab2adcdc520c/global_proof/
    residual_coverage_bridge_failure.md

That source has an explicit full two-player SPE with unique optimal union and
|D|>W. It is not a counterexample to Q-CAG-HALF. No duplicate boundary or new
counterexample is claimed here.

## 2. Same-branch leakage identity really uses shared resource control

For any actual ordered node h, force a legal root action A and follow the
original complete strategy. Let b_x be the fixed earlier load, K_x the number
of later players covering x, and d_A the root payoff in this true branch.
For a particular true follower action B in the same terminal profile, let

    L(A,B)=sum_(x in B\A)1/(b_x+1_A(x)+K_x)
             −sum_(x in A\B)1/(b_x+1_A(x)+K_x).

Only customers in A∪B are used; each denominator is positive. Same-terminal
unit shares give the exact identity

    u_B−d_A=L(A,B).

Thus a universal successor floor t, if established for the relevant true
successor subgames, would force L(A,B)≥t−d_A for every follower whenever
root IC gives d_A below t. For all r−1 followers together,

    sum_followers u_B−(r−1)d_A
      =sum_x [K_x−(r−1)1_A(x)]/[b_x+1_A(x)+K_x].

This is a real common-resource identity in a single branch. It does not
compare u_B in that branch with the same position's actual root-path payoff.
The latter substitution would be invalid. The min-remaining-player relay in
`extreme_maximal_membership_floor.md` does obtain the needed true successor
floor in its explicitly restricted incidence class; its scalar stationary
remainder is not nonnegative on arbitrary intermediate incidences.

The direct target would need to pay positive leakage jointly, across roots
and histories, from original I/G capacity. Merely summing the displayed
identities does not perform this payment.

## 3. Optimal exchange constraints were found to be existing assets

For an optimal m-index tuple, put

    E_J={x∈O: every optimal index covering x belongs to J}.

Replacing |J| optimal slots by any |J| legal topics with union B gives

    |B\O|≤|E_J\B|.

Averaging deletion subsets gives corresponding hypergeometric multiplicity
bounds. These are correct, but they are subsumed by the already stronger
owner/Bernoulli/Beta hybrid cuts and flows in

    R-cd789330fc7141299ac491bbb3ffa420/round3/shared/
      owner_exchange_potential.md
    R-cd789330fc7141299ac491bbb3ffa420/round3/credible/
      owner_hybrid_transport.md
    R-cd789330fc7141299ac491bbb3ffa420/round3/relay/
      optimal_exchange_potential_and_query_credit.md

They are therefore not presented as newly proved components. In particular,
these assets already have the exact decomposition u_i=ell_i+e_i, the one-leaf
I/G joint budget, complete-prefix ROLL identity, all-role Hall transport, and
actual-leaf cancellation capacities. The remaining connection is genuinely
dynamic: branch prices and which clients remain available change after a
true successor response. One leaf's cuts cannot be reused as independent
capacity in mutually exclusive rollout leaves.

The existing increasing-role capture flow reads true successor actions but
resets each new query to its original actual prefix. Its unproved capacity
bound is where additional successor IC must enter. Its PAY-FLOW equality and
SLACK identity alone do not advance Q-CAG-HALF.

## 4. General all-SPE depth-floor candidate

This candidate came from asking whether all-history optimality can be used
through depth minima rather than pointwise or actual-prefix balances.
For an original instance with m players define

    L_i=min_(|h|=i−1) min_(complete pure SPE τ after h)
             current mover's final payoff in τ.

Every actual SPE has u_i≥L_i, hence W≥sum_i L_i. The proposed sufficient bridge
is

    OPT_m≤2 sum_(i=1)^m L_i.                     (UNPROVED)

This is stronger than Q-CAG-HALF, not an equivalent reformulation. It does
not assert monotonicity of L_i; selected exact inputs already have
nonmonotone depth floors. It differs from min over histories in one fixed
full σ, which can only be larger.

The finite all-SPE sets are computed with the canonical complete-continuation
recursion: at a prefix count b each child has its entire realizable SPE set;
M(b)=max_A min_(z in child A) u_A(z). M is exactly the minimum attainable
current payoff at that prefix. The lower-bound direction follows from all
children's true IC, while attainability chooses a child attaining M and
its minimum-root-payoff continuation, then chooses independent minimizing
threats at other ordered children. Consequently count caching is only an
all-continuation representation; it does not impose a count-only policy.

`check_depth_floor.py` computes every depth's minimum M over legal count
prefixes and uses Fraction arithmetic internally. `depth_floor_checks.json`
contains selected known counterexample inputs for earlier failed bridges.
All selected checks have nonnegative 2 sum L−OPT. This supplies no universal
proof or implication beyond the displayed conditional bridge. The security
sibling was informed so that this candidate is not explored redundantly.

## 5. What is not established

No new full-input inequality here bounds the cross-rollout leakage by one
original W. The direct charge is still |D|−|G|≤W. A valid continuation must use
true successor optimality and share one finite original I/G capacity, as
opposed to merely renaming the missing budget. No new result is promoted.
