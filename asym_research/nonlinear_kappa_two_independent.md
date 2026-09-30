# Independent note: exact two-leader equilibrium selection with polyhedral continuations

2026-09-30. Independent mathematical derivation and internal audit; not external peer review. This note is separate from the main manuscripts. The theorems below have complete proofs in this note; no implementation of the nonlinear extension is claimed.

## 1. A general polyhedral-continuation theorem

Two leaders have finite nonempty action sets A and B and nonnegative payoffs. At each labeled action profile (a,b), admissible follower continuations may be chosen separately from those at every other profile. Assume their attainable leader payoff pairs have a finite exact representation as follows: for each j in a finite index set J_ab there is a nonempty bounded rational polytope P_abj, two rational affine payoff maps u_1(z),u_2(z), and an effective realization procedure turning every rational z in P_abj into an admissible continuation with those payoffs. Every admissible payoff pair is represented in at least one cell. Empty cells may instead be provided and removed by linear programming. The total cell description and the realization procedures are the algorithm's input.

**Theorem 1.** In time polynomial in that explicit representation, one can compute the minimum multiplicative approximation factor alpha >= 1 achievable with pure leader actions and admissible continuations at every action profile. If finite, the optimum factor is rational and is attained by a rationally represented continuation in one of the supplied cells. If no finite factor exists, this is correctly detected. Realization time is added to the linear-programming time.

### Proof

For every action profile compute, by minimizing affine functions over all its cells,

    m_1(a,b) = min admissible u_1,
    m_2(a,b) = min admissible u_2.

Retain a realizing point for each minimum. Compactness gives attainment. Define full-action deviation thresholds

    D_1(b) = max_{a' in A} m_1(a',b),
    D_2(a) = max_{b' in B} m_2(a,b').

An admissible on-path continuation at (a,b), with payoffs (u_1,u_2), extends to an alpha-approximate equilibrium exactly when

    D_1(b) <= alpha*u_1,
    D_2(a) <= alpha*u_2.

Necessity follows from the defining minima. For sufficiency, after each genuine unilateral leader deviation choose a continuation attaining the deviator's minimum. The profiles (a',b), a' != a, and (a,b'), b' != b, are disjoint labeled profiles, so these prescriptions never conflict. At the original profile the no-change option requires nothing extra, since alpha >= 1 and m_i(a,b) <= u_i. Fill all remaining profiles with arbitrary admissible continuations.

For each on-path cell solve the rational linear program

    maximize lambda
    subject to z in P_abj,
               0 <= lambda <= 1,
               u_1(z) >= lambda*D_1(b),
               u_2(z) >= lambda*D_2(a).

All coefficients D_i are already computed rational constants. Let Lambda be the largest optimum over every cell and action profile. If Lambda > 0, the answer is alpha* = 1/Lambda and an optimizing point supplies an on-path continuation. If Lambda = 0, no finite alpha can satisfy the necessary inequalities at any profile. This convention also handles zero payoffs: D_i = 0 imposes no positive lower bound on u_i; if both thresholds vanish, lambda = 1 is feasible. Bounded rational LPs have rational optimum points of polynomial encoding length. Together with the stored unilateral-deviation minima, this proves the theorem.

The theorem does NOT require the two leader payoffs to have constant sum. It does require the polyhedral description to be supplied or generated efficiently; it is not a general efficient algorithm for arbitrary follower Nash games.

## 2. Arbitrary realized-load costs when cross-overlap is at most two

Consider two facilities with finite nonempty, possibly different allowed location sets U_1,U_2. Customers have positive rational weights and fixed accessibility sets. Covered customers must choose one accessible facility; customers randomize independently. A facility's payoff remains its expected total customer weight. A customer's cost may be

    E[f_{i,j,s}(L_j)],

where j identifies the facility, s is its chosen location, and L_j is its realized total load including that customer's weight. The functions may differ between customers, facilities, and locations. Monotonicity is not needed for the algorithmic theorem. Costs at all attainable arguments must be finite.

Let

    kappa = max_{s in U_1,t in U_2} |C_s intersect C_t|.

**Finite-evaluation assumption.** Each cost value used below is given as an exact rational number, or is produced by an evaluator in polynomial time with polynomial output bit length. Equivalently, runtime may be measured in the bit length of all evaluated rational values plus the cost of obtaining them. Merely supplying an arbitrary real-valued black box, or an expression whose evaluated values have exponentially many bits, does not meet the polynomial-time claim.

**Theorem 2.** If kappa <= 2, the exact minimum approximation factor alpha* over pure facility locations and full exact independently mixed customer Nash continuations can be computed in polynomial time. If finite, alpha*, the returned probabilities, and expected facility payoffs are rational with polynomial bit length. An attaining continuation and a compact SPE certificate can be output. No finite factor, if that case occurs in this more general cost model, is correctly detected.

For N_1 = |U_1|, N_2 = |U_2| and n customers, a direct implementation uses O(N_1 N_2 (n+1)) exact rational operations apart from the cost evaluations and their bit-operation cost. There are at most eight strategic-client cost evaluations per location pair and at most nine constant-dimensional support cells per pair.

### Local reduction and complete support treatment

Fix a layout. Let A_0,B_0 be its exclusive customer weights, and let k <= 2 common customers have weights w_i. Exclusive customers have no choices and need no incentive constraints. For a common customer i, use p_i for the independent probability of choosing the first facility.

When k=2, write j for the other common customer. Conditional cost differences are

    d_i^A = f_{i,first}(A_0+w_i+w_j) - f_{i,second}(B_0+w_i),
    d_i^B = f_{i,first}(A_0+w_i) - f_{i,second}(B_0+w_i+w_j).

Here the subscripts include the current locations. The expected cost of choosing the first facility minus the cost of choosing the second is the affine function

    g_i(p_j) = p_j*d_i^A + (1-p_j)*d_i^B.

For k=1 the corresponding function g_i is constant. For k=0 there are no strategic variables.

Enumerate each common customer's three designated support states:

1. first only: p_i=1 and g_i <= 0;
2. second only: p_i=0 and g_i >= 0;
3. both: 0 <= p_i <= 1 and g_i=0.

All resulting constraints are rational and linear. A both-designated variable may be an endpoint: indifference then makes it a valid pure best response, so the closed cells contain no false equilibria. Every actual independently mixed NE is included by selecting its true supports. Zero coefficients and identically zero indifference conditions are retained as ordinary linear constraints; they may give intervals or two-dimensional cells. No division by a possibly zero payoff difference is needed.

Each nonempty cell is a bounded rational polytope in at most two probability variables. For every point in the cell, the facilities' expected loads are affine:

    L_1 = A_0 + sum_i w_i p_i,
    L_2 = B_0 + sum_i w_i (1-p_i).

Thus Theorem 1 applies directly. Its on-path LP has at most three variables including lambda, and can be solved by constant-size rational vertex enumeration. The default continuation at every other layout may be obtained by enumerating these same support cells and choosing any rational feasible point. Nonemptiness also follows from existence of mixed NE in this finite customer game.

### Load intervals and independent realization

If desired, a cell can be compressed into its first-load interval [ell,u] by two LPs. Its total covered weight W is constant, so the second load is W-L_1. Every point of this interval is attained: if p^- and p^+ attain the two ends, then for x in [ell,u], the probability vector

    p = (1-theta)*p^- + theta*p^+,
    theta = (x-ell)/(u-ell),

lies in the same cell and attains x. When ell=u, use either endpoint witness. Customers independently use the resulting coordinates p_i. This is a convex combination of probability VECTORS inside one Nash-support polytope, not correlated randomization between two joint outcome distributions.

The previous clipped-balance formula is therefore also valid, but the lambda LP avoids separate divisions by zero and extends beyond constant-total-load models.

### Complexity, output, and certification

Directly determining exclusive/common customer sets costs O(n) per layout. Each layout needs at most nine cells, each of constant dimension and with a constant number of inequalities. Rational vertex coordinates, extrema, D-values, and the final lambda have polynomial encoding length in the input and evaluated-cost bit lengths. Exact comparison and arithmetic therefore have polynomial bit complexity.

A compact achieving-SPE certificate stores the on-path NE and minimum-payoff NE witnesses at the N_1+N_2-2 genuine unilateral-deviation profiles; inaccessible and exclusive customers need no probability entries. A fixed local enumeration rule specifies valid continuations at all remaining profiles. Direct checking of the displayed NE conditions and leader deviation ratios verifies the achieved factor. To certify GLOBAL OPTIMALITY, the verifier must also recompute the local cells/extrema and optimizing LPs, or receive their LP certificates; an achieving SPE certificate alone is not a lower-bound certificate for alpha*.

## 3. Response cores: exact utility and limitations

For the setting of Theorem 1, let A' subset A and B' subset B be nonempty and suppose each b in B' has a full-action maximizer of m_1(a,b) in A', and each a in A' has a full-action maximizer of m_2(a,b) in B'. Then computing D using only A',B' gives the original full D-values at core actions. Consequently every alpha-feasible on-path witness in A' x B' extends to the full game. Any cycle of the chosen colored maximin-response graph supplies such a core, with equal numbers of actions of each color.

This is a useful restriction lemma, but it neither gives a universal approximation factor for arbitrary two-leader games nor preserves the globally optimal on-path factor. For the latter point, consider singleton continuations with the 2x2 core payoff matrix

    (1,2) (2,1)
    (2,1) (1,2).

Its response graph is a four-cycle and its optimal factor is 2. Add one action to each leader, give their joint new profile payoff (3,3), and give all new-to-old cross profiles payoff (0,0). The old core remains response closed and retains all its D-values, but the full game has an exact equilibrium at (3,3). Replacing the 2s in the original core by any M>1 also shows that the abstract response-core structure alone gives no uniform finite approximation bound.

## 4. Recommended reusable next target

The highest-priority generalization is to package Theorem 1 as an exact equilibrium-selection procedure with independently checkable LP certificates, and instantiate it with several explicit continuation representations. The nonlinear kappa<=2 result above is a first complete instance. CE/CCE continuation polytopes are another natural instance when their finite outcome representation is supplied. The role of a response core should be candidate restriction for existence or a specified factor, never an unsupported shortcut for preserving global optimality.

The nonlinear kappa<=2 theorem does not extend by the same linear reasoning to kappa>=3: a client's expected deviation cost can then be multilinear in two or more other probabilities, so fixed-support Nash sets need not be polytopes. Any such extension needs a separate algebraic or structural argument.
