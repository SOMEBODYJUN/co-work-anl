# SC-K-THREE-SITE-CHAIN-BOX-EXISTS: arbitrary unequal light weights on an opening-directed three-site chain

## Exact statement and scope

Run SC-K-GREEDY-BUDGET on an explicit positive rational MF-MODEL instance with positive reach and arbitrary explicitly represented k>=2. Let gamma>0 be its last score, q_t its final multiplicities, and A_i each customer's occupied-site options. Freeze single-option customers and every multi-option customer with weight at least gamma at their greedy initial sites. All remaining variable customers have 0<w_i<gamma.

Consider a component of the light overlap graph that consists of the three occupied sites H,M,L, with precisely the edges HM and ML. Every variable customer consequently has exactly the options HM or ML; there is at least one on each edge. Require the greedy opening order in this component to be H before M before L. (Equivalently, its edge orientation by initial opening is H->M->L.) Then every global minimum of the exact weighted customer potential among assignments of these variable clients that obey the three full greedy boxes is an exact customer NE within this component. In particular a full-box site-uniform customer NE exists on this same greedy occupancy for arbitrary numbers and arbitrary unequal weights on both edges.

The assertion is componentwise. A whole greedy occupancy whose light components are of this kind, constant-multiplicity components, or the already proved polynomial path/star types therefore has a full-box NE and an existential complete factor-two continuation, with polynomial off-path completion once a minimizer is supplied. Here the chain proof establishes **existence and correctness of a specified finite optimization selector**, not an input-bit-polynomial way of finding its global minimizer. Heavy customers can cross components but remain fixed and are stable once the full box is obtained. No result for longer unequal-edge paths, merging/forking orientations, or general overlap graphs is asserted.

## Reduction to the residual three-site problem

Every HM customer was initially first covered at H and every ML customer at M. By SC-K-GREEDY-MAX-MULT, Q=q_H>=q=q_M>=r=q_L. Let the frozen/private total weights be a,b,c. Write X for the multiset of HM light weights and Y for the multiset of ML light weights. The initial greedy totals are

    (W_H^0,W_M^0,W_L^0)=(a+sum X,b+sum Y,c).

They lie in the full boxes [Q gamma,(Q+1)gamma], [q gamma,(q+1)gamma], [r gamma,(r+1)gamma]. Thus the finite constrained assignment set is nonempty and has a global minimum of

    P = sum_t (W_t^2-sum_{i assigned t} w_i^2)/(2q_t).

Its exact single-customer difference for weight w from s to v is

    delta P = w[W_v/q_v-(W_s-w)/q_s].

Frozen customer squared weights add constants to the variable optimization and need not be aggregated as a single customer.

## Which improving moves could a full-box minimizer fail to perform?

A strictly improving transfer never violates the source lower box: its source weight after leaving is larger than q_s times its target normalized load, and that target is at least gamma. It only decreases its source upper bound and increases its target lower bound.

The target upper box is also preserved for any strict move toward weakly smaller multiplicity, by the same inequality used in PATH-EDGE and STAR: if q_s>=q_v and w<gamma, target overflow would force

    W_v/q_v > gamma+(gamma-w)/q_v
               >= gamma+(gamma-w)/q_s
               >= (W_s-w)/q_s,

contrary to strict improvement. Therefore H->M and M->L are feasible strict moves.

An HM customer returning M->H is also always upper-feasible: at H it rejoins a subset of its original greedy HM pool, so the new H total is at most W_H^0. Thus a constrained minimum cannot leave such a profitable return undone either.

The only remaining possible blocked improvement is an ML customer i of weight w currently at L, returning to M, with

    E=(W_L-w)/r > W_M/q,                 (C1)
    W_M+w>(q+1)gamma.                    (C2)

The following exchange shows this cannot happen at a constrained global minimum.

## Return-all-incoming exchange

Let X_M be all HM customers currently assigned to M. Put

    S=sum_{j in X_M} w_j,
    T=sum_{j in X_M} w_j^2,
    A=W_H, M=W_M.

Since H has no incoming variable edge, A+S=W_H^0. The initial H upper box and current H lower box imply

    0<=S<=gamma,    A+S<=(Q+1)gamma.       (C3)

Let R be the total weight of all ML customers currently at L; it includes i, so R>=w. Then M=W_M^0-R+S. In fact S>0 under (C2), since otherwise M+w=W_M^0-R+w<=W_M^0.

Make one simultaneous reassignment: send every customer in X_M back to H, and send i from L to M. All other customers stay. This respects every customer's own choices. The new totals are

    H:A+S=W_H^0,
    M:M-S+w,
    L:W_L-w.

H is in its initial box. The new M total equals W_M^0-R+w<=W_M^0: it comprises precisely the frozen M weight and a subset of its original ML customers. It is above its lower box because

    M-S+w > (q+1)gamma-S >= q gamma

by (C2)-(C3). L's new total is above its lower box by (C1) and M/q>=gamma, and its upper box only decreases. Thus the exchange is a feasible full-box assignment.

## Exact potential decrease

Sending the whole multiset X_M into H contributes

    A S/Q + (S^2-T)/(2Q).

Removing it from M and adding i contributes

    -M S/q +(S^2+T)/(2q) + w(M-S)/q.

Removing i from L contributes -wE. Therefore the exact total difference is

    Delta P = S(A/Q-M/q)
              +(S^2-T)/(2Q)+(S^2+T)/(2q)
              +w[(M-S)/q-E].                       (C4)

By (C1), the final term is strictly below -wS/q, giving

    Delta P < S[A/Q-(M+w)/q]
              +(S^2-T)/(2Q)+(S^2+T)/(2q).

By A+S<=(Q+1)gamma and (C2), this is in turn strictly below

    (1/q-1/Q)[(S^2+T)/2-S gamma].                   (C5)

Every weight is positive, so T<=S^2; S<=gamma gives (S^2+T)/2<=S gamma. Since Q>=q, (C5) is nonpositive, hence Delta P<0. This contradicts global minimality within the full box. The strict inequalities cover Q=q, S=gamma, and every initial upper/lower equality; no genericity or unique minimizer is needed.

Every variable client at every full-box potential minimizer therefore has no strict alternative. Heavy frozen multi-option customers are stable from w_i>=gamma and the box, and single-option customers have no alternative. Uniform independent mixing among each assigned site's facilities yields exact original-game NE.

## What this advances and what remains

The previous two-light lower-constrained potential family does not contradict this statement: it omits the upper constraints, and its preferred ML state lies outside the box. The old descending-only trap with one HM customer and two different-weight ML customers is also covered by this **existence** statement but lies outside the per-edge-uniform polynomial PATH-EDGE class. Its mandatory upward return is compatible with the exchange proof.

The new argument replaces equal-weight one-unit transport cancellation by returning the entire upstream pool S, whose total is at most gamma because H is an upstream endpoint. On a longer chain, that pool may itself have incoming mass from an earlier site, so the key S<=gamma bound need not hold; a recursive exchange needs a new argument. The theorem does not supply such an argument or claim polynomial potential minimization. External review and novelty certification remain unrecorded.
