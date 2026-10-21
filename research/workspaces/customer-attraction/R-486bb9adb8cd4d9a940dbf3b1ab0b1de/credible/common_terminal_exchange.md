# Common-terminal exchange blocks the many-punisher lift

2026-10-21. Research candidate with a complete short proof; root independent attack requested. All topics are in one finite common catalog, all players and customers have unit weight, and the fixed pure SPE specifies every ordered history with arbitrary ties. This is an auxiliary structural lemma and a failed construction template. **Q-CAG-HALF remains OPEN.** No global collision-free upper bound or main counterexample is claimed.

## 1. An exact exchange lemma for the same complete strategy

Fix one complete-history pure SPE sigma. Let h be any decision history, with current actual payoff u(h). Choose a legal action b there and let q be the terminal topic-count vector obtained after h,b by following the *same* sigma. Suppose there is a legal last-player history g such that sigma(g)=b and its terminal count is also q. The histories need not be comparable, have the same length before appending b, or have symmetric replies. Then for every legal topic T,

    u(h) >= U_b(q) = u_m(g,b) >= sum_(x in T) 1/(1+c_x(g)).       (1)

The first inequality is h's real deviation comparison. The equality uses identical action b and identical terminal counts q, which preserve equal-share payoffs. The last inequality is the last player's real optimality at the *particular ordered history g*. These are two true comparisons; equality of terminal counts never identifies g with another history or constrains their tie choices.

A particularly useful case is g lying on the continuation after h,b and the last player also choosing b. More generally g can lie in a different real branch. The hypothesis must be verified in the given complete strategy; a possible continuation, arbitrary permutation of a terminal multiset, or a terminal count achievable in another SPE is insufficient.

If T=X union Y with X,Y disjoint, c_x(g)<=1 on X and c_y(g)=0 on Y, (1) gives

    u(h) >= |X|/2 + |Y|.                                      (2)

This proof works unchanged for integer type multiplicities because those are distinct unit customers.

## 2. A load-distortion matching certificate, including collision-free paths

This strengthening was suggested by root after independently checking Section 1. Fix the actual terminal load c*_x and actual player payoffs u_i. No collision-free assumption is required. Select an index set I. For h in I, suppose a legal expansion topic T_h=S_h union E_h exists, where S_h is player h's actual topic and E_h is disjoint from the actual covered union. In particular S_h and E_h are disjoint. The E_h may overlap.

Fix a number alpha in [0,1]. Draw an edge i -> h if there is an action b and a *real* last-player history g satisfying Section 1 with the actual prefix of i, and the following pointwise conditions hold:

    alpha*(1+c_x(g)) <= c*_x        for every x in S_h,
    c_y(g)=0                       for every y in E_h.         (3)

Writing the condition without division includes alpha=0 and empty S_h. Every customer in S_h has c*_x>=1. Section 1 and (3) therefore certify

    u_i >= alpha*sum_(x in S_h) 1/c*_x + |E_h|
        = alpha*u_h + |E_h|.                                 (4)

If this bipartite graph has a perfect matching pi from I to I, summing only its selected true comparisons gives

    sum_(h in I) |E_h| <= (1-alpha)*sum_(i in I) u_i
                         <= (1-alpha)*W.                     (5)

Consequently, if all customers in an optimal m-topic union that are omitted by the actual union belong to union_(h in I) E_h, then

    OPT-W <= sum_h |E_h| <= (1-alpha)*W,
    hence OPT <= (2-alpha)*W.                                (6)

The omitted-customer condition means `(optimal union) \ (actual union)` is contained in union E_h. It does not require every E_h to be optimal-covered. The inequality OPT-W<=the size of this difference holds even if some actually covered customers are omitted by the chosen optimum.

For alpha=1/2 the load condition is c_x(g)<=2c*_x-1 on S_h. This gives the conditional 3/2 certificate for *arbitrary* actual congestion. In the collision-free case c*_x=1 on every actual topic, so the condition reduces to c_x(g)<=1, and u_h=|S_h|. Thus the earlier collision-free form is the special case

    u_i >= |S_h|/2 + |E_h|,
    sum_h |E_h| <= (1/2)*sum_(i in I) u_i.                    (7)

These are sufficient structural certificates, **not** assertions that the graph has a perfect matching for every SPE. Establishing a useful matching universally remains a separate unproved obligation. An edge may use its own b and g; the matching never merges their histories. The bounds concern the original unit-player game and do not introduce weighted providers.

## 3. Why replacing the one-punisher 3/2 family by q punishers fails

Take k>=2 disjoint early groups X_i,Y_i, with x_i=|X_i| and a_i=|Y_i|. Set C_i=X_i and A_i=X_i union Y_i. Let Z be a reservoir disjoint from every early group. Allow q>=1 punitive topics B_(i,1),...,B_(i,q), each contained in X_i union Y_i union Z. Their coverage inside their own group and the reservoir may be arbitrary and may overlap. Add q actual tail topics D_1,...,D_q inside Z. The proposed actual path is

    C_1,...,C_k,D_1,...,D_q,                                  (6)

so each early player earns x_i. We do not require the D topics to be disjoint for the template obstruction; if they are, (6) is collision-free.

At the real early prefix of player i, require the following proposed continuation behavior:

* After deviating to A_i, the later early players choose the remaining C_h, and the q tail players choose all B_(i,l), once each, in any order. Let l_i be the last tail topic in this branch.
* After deviating instead to B_(i,l_i), the later early players again choose the remaining C_h, and the q tail players choose A_i and every B_(i,l) with l!=l_i, once each, in any order.

These two terminal multisets are exactly equal:

    Q_i = {C_h : h!=i} multiset-union {A_i,B_(i,1),...,B_(i,q)}. (7)

The early B_(i,l_i) deviation and the last B_(i,l_i) in the A_i branch therefore have equal final payoff. At the last history g_i of the latter branch, every group h!=i has exactly its single C_h in the prefix: c(g_i)=1 on X_h and 0 on Y_h. Hence Section 1, with legal comparator A_h, yields

    x_i >= x_h/2 + a_h                  for every h!=i.        (8)

This only uses two required comparisons, so incompatible values rule out *every* completion of all unspecified histories. It does not assume those unspecified continuations are already SPEs.

Since k>=2, choose any permutation pi of {1,...,k} having no fixed point. Summing (8) for h=pi(i) proves

    sum_i a_i <= (1/2) sum_i x_i.                             (9)

For equal group sizes this gives a<=x/2 regardless of q, reward reservoir, tail order, cross-overlap of punitive rewards, or how the remaining histories are filled. If the comparison portfolio A_1,...,A_k,D_1,...,D_q covers every customer, then OPT-W=sum_i a_i (provided no Y_i occurs in Z, as stipulated), so (9) bounds this lift's efficiency ratio by 3/2. In that additional full-coverage statement the displayed portfolio uses exactly m=k+q topics and therefore is a legal optimum.

The k>=2 condition is essential for this proof: there is no outside group h!=i when k=1. The statement does not assert any global bound on arbitrary one-group gadget extensions.

## 4. The initially attractive integer parameters and their concrete failure

The literal attempted lift set q=t-1 and used k early groups, where each X_i has t customers and each Y_i has t-1. The reservoir contains disjoint blocks b_l of size t-1 and d_l of size 1. Topics are

    A_i=X_i union Y_i, C_i=X_i,
    B_(i,l)=X_i union b_l, D_l=b_l union d_l.

The intended actual welfare and full-cover comparison are

    W=t(k+t-1),   OPT=W+k(t-1).

If the intended path were an SPE, taking k much larger than t would give a collision-free ratio near 2-1/t. But for every t>2 even the intended actual *last* D topic fails optimality: its payoff t is beaten by any A_i, whose payoff is t/2+t-1>t. Also, in the proposed A_i punishment branch the last B has payoff t, and an outside A_h gives that same strict improvement. Thus the direct lift fails twice before any full-tree issue arises.

Increasing reservoir rewards to fix the latter comparison cannot fix the common-terminal construction: the matching argument is independent of those rewards and still forces a<=x/2. To escape this obstruction, one must break the shared multiset (7), let punitive topics also change other early groups' loads, or find a different branch geometry that defeats the matching. Merely adding more identical shared-X punishers is insufficient.

## 5. Exact evidence and limits

`common_terminal_audit.py` expands the literal integer customers, checks every displayed common-terminal identity and utility comparison for t=2,...,8 and k=2,3, and stores exact Fraction strings. These are audits of the formulas, not sampled SPE certificates. No full strategy certificate is supplied for t>2 because the stated last-node improvement proves the intended path impossible.

`collisionfree_joint.py` is a separate finite full-history MILP candidate generator adapted from the canonical joint interface. It zeros every type meeting two actual path topics; after extracting a complete action graph it solves its true strategy cone with those same zero restrictions and independently checks a recovered integer endpoint at every ordered history. Floating MILP bounds are excluded from mathematical conclusions. The m3,p6 finite attempt timed out and certified only a ratio-one endpoint; it adds no universal or sharp bound. A parallel m4,p7 attempt had no recoverable result and hit an inherited `mip_gap=None` metadata conversion bug; its parameters and failure are retained in `cf_m4p7_failed.json`. The guard was fixed without repeating either low-information search.

Root independently checked the original same-terminal and many-punisher arguments and suggested the load-distortion extension in Section 2; a separate review is being prepared. The short lemmas have not been promoted to a shared claim here. No external novelty or peer-review status is asserted.
