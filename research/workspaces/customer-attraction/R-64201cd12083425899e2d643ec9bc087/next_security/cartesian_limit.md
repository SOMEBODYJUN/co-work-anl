# Three-actor Cartesian catalogs: exact credible aggregate menus

2026-10-21; private candidate theorem, not independently reviewed. This gives
a general representation and a counterexample-generation criterion. It does
not prove or refute general CAG half coverage, strong aggregate security, or
the PAIR candidate. The earlier Cartesian-catalog note in
`R-3d6f7a072d5e489eb5a0bdc4d32bb769/security_bridge/` already established
security additivity and an example of cross-component punishment. The new
content here is the exact three-actor menu and its replication limit.

## Exact finite product menu

Take any finite list of CAG components j with disjoint customer sets and
possibly different finite nonempty catalogs. There are exactly three unit
providers, and the common joint catalog contains every tuple of component
themes. Payoffs and coverage add across components. All joint ordered
histories remain available; last-player ties may depend on the entire joint
prefix. Write u_i^j(a,b,c) for a component payoff.

For every component and first action define

    L_j(a,b) = argmax_c u_3^j(a,b,c),
    phi_j(a) = max_b min_(c in L_j(a,b)) u_2^j(a,b,c).

For a joint first action A=(a_j), let M(A) be the following **terminal menu**:

    choose (b_j,c_j) with c_j in L_j(a_j,b_j) for every j,
    and require sum_j u_2^j(a_j,b_j,c_j) >= sum_j phi_j(a_j).       (1)

Then M(A) is exactly the set of terminal outcomes attainable by a complete
pure SPE of the two remaining providers after A.

Necessity: the third player's best responses factor across components.
For any joint second action B, minimizing the second player's payoff over
these best responses also factors. Therefore the second player's worst
credible best-action value is exactly

    max_B min_(C in product L_j(a_j,b_j)) sum_j u_2^j
      = sum_j max_b min_(c in L_j(a_j,b)) u_2^j
      = sum_j phi_j(a_j).                                  (2)

Every complete SPE must pay the second player at least (2).

Sufficiency: for the selected second action B*, use the selected C* from
(1). At every other B choose, in each component, a third-player best reply
minimizing the second player's payoff. Each such off-path payoff is at most
(2), while B* pays at least (2). Thus the second player is best responding,
and every last node is best responding. These are actual continuations of
one complete strategy, with no frozen followers or anonymous-tie restriction.

Define U_i(z)=sum_j u_i^j(z_j) and

    G = max_A min_(z in M(A)) U_1(z).                         (3)

The menu is nonempty by the maximizing actions in (2). A joint terminal z
with first action A is attainable by a complete root SPE **if and only if**

    z in M(A), and U_1(z) >= G.                              (4)

Necessity follows by comparing every first action with its actual credible
continuation. For sufficiency, at every alternative A choose a minimizer in
(3), complete its remaining strategy by the previous construction, and use
the prescribed z at its own A. Every alternative first-action payoff is at
most G, while the selected one is at least G. Different first-action branches
are separate ordered histories, so these completions are compatible.

Equations (1)-(4) retain **all** root actions and all genuine suffix incentive
comparisons. They show the precise way in which component second-player
slack can pay a deficit in another component; component SPE is not assumed.

## Identical components: an exact replication limit

Now take K identical copies of one component, with finite catalog S. For
each first theme a define the finite rational LP value

    g_a = min E u_1(a,b,c)
          over distributions on c in L(a,b),
          subject to E u_2(a,b,c) >= phi(a),
    g = max_a g_a.                                         (5)

Let G_K be (3) for K copies. There is an explicit finite constant C depending
only on the base component such that

    K g <= G_K <= K g + C.                                 (6)

In particular, G_K/K tends to g. This is a limit of exact full-history pure
SPE root thresholds, not a relaxed-equilibrium claim.

For the lower bound choose A=(a*,...,a*) with g_(a*)=g. Any terminal in M(A)
gives an empirical distribution feasible in (5), so its U_1 is at least K g.

For the upper bound choose a rational optimal distribution for each g_a and
let D_a clear its probabilities' denominators. Set M=max_(a in S)|a|, which
bounds every base first-player payoff. At any A let n_a be the number of
copies whose first action is a. Partition n_a into full blocks of size D_a
and a remainder r_a<D_a. Fill each full block with the chosen mixture; its
second-player payoff is at least D_a phi(a), and its first payoff is D_a g_a.
For each remaining copy choose any pure terminal with second payoff at least
phi(a), which exists by (2). Its first payoff is at most M. The resulting
terminal belongs to M(A) and has

    U_1 <= sum_a[n_a g_a + r_a(M-g_a)]
        <= K g + M sum_a(D_a-1).

Thus C=M sum_a(D_a-1) suffices for every K and every A. No unproved uniform
selection of root continuations is hidden in (6).

## A finite-product counterexample criterion

Suppose there is a **rational** distribution x over component triples
(a,b,c) with c in L(a,b), satisfying

    E_x[u_2-phi(a)] >= 0,
    E_x u_1 > g,
    E_x(u_1+u_2+u_3) < 3 v_3(base).                         (7)

Then a sufficiently large finite Cartesian power is an actual CAG
counterexample to the strong aggregate-security bridge. Indeed, take K
divisible by all probabilities' denominators and large enough that
K(E_x u_1-g)>=C. Realize exactly K x_(a,b,c) copies of each triple. The selected
terminal lies in M(A), and its first payoff is at least K g+C>=G_K, so (4)
constructs a complete pure SPE. Its welfare is K E_x W. The static security
value is exactly K v_3(base), by the already established Cartesian security
additivity; the static opponents remain independent of the sampled query.
The strict third inequality in (7) is therefore preserved at finite K.

The first-margin condition in (7) is material. A numerical optimum with
E_x u_1=g alone is not automatically compilable using the stated rounding
bound. A negative numerical LP value is also not a rational certificate.

## Exact finite evidence for cross-component root loss

The four-label base customer masses, in mask order 1,...,15, are

    (0,0,5,9,5,4,7,9,6,3,8,9,1,6,0).

They expand to 72 unit customers. Direct exact menu enumeration gives

    phi = (161/6,55/2,55/3,161/6),
    G_1 = 161/6,
    g = 55/3,
    G_2 = 271/6 < 2 G_1 = 161/3.

For the action a=2, the mixture 17/18 on (2,2,3) and 1/18 on (2,3,0)
achieves the convexified value 55/3. For a=3, use 17/24 on (3,2,3) and
7/24 on (3,3,2). The other actions have pure minimizing triples.

`cartesian_finite.py` constructs a complete two-copy joint SPE with actual
component theme tuples

    ((2,3),(3,2),(3,3)),
    (U_1,U_2,U_3) = (146/3,146/3,110/3), W=134.

Here U_1=146/3<2G_1, so two individually unavoidable component root-payoff
floors cannot simply be added for a general joint SPE. This is a precise
finite failure of componentwise first-player induction. It is **not** a
failure of aggregate security or half coverage.

The script independently unfolds the sixteen joint labels and every one of
the 273 joint ordered-history decision nodes; it expands all 144 unit
customers and checks all 4368 action comparisons by Fraction. The full game
and strategy are saved in `cartesian_two_copy_exact.json`. These are author
checks, not an independent review. The all-product theorem is proved above,
not by this example.

## Discovery and remaining boundary

`cartesian_limit.py` computes (5) and minimizes the left welfare in (7) with
the other two constraints. A completed 300-instance six-label numerical
screen did not yield a negative gap; this proves no universal claim.
`cartesian_cone.py` fixes root minimizers, a selected mixture, and worst
credible replies from one seed, then varies the entire nonnegative base
customer cone while constraining every last reply, second-player floor,
root budget, and all static backgrounds for a fixed query. Its current
108-row four-label LP has positive numerical minimum gap. Neither result
establishes a general payment.

What is new is a small-base, genuinely cross-node compilation mechanism in
which the target's static security is additive rather than diluted. The
missing step is an exact witness for (7), or a CAG-specific proof that (7)
is impossible. For more than three actors the earlier suffix menus no longer
factor at the last stage; (1)-(6) have not been asserted for those horizons.
