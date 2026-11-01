# All-reset same-client kernel: independent check, old sources, and repair directions

2026-10-24, menu9. Candidate supplied by root after the first menu work. General arbitrary-player/common-catalog/all-history pure-SPE scope is unchanged. This review proves legality of the proposed local family and its density extension. It does **not** prove common ROLE feasibility, a new welfare bound, or Q-CAG-HALF. No novelty claim is made.

## 1. Exact local family

Work only with R clients, which no actual topic covers. At a natural context t of role k, let V be the prescribed completion and A the genuine actual-prefix reset for the same current action. Fix one input client x in that current action. Write

    v=c_V(x)>=1, a=c_A(x)>=1, h=h_tx>=0,
    Q={j>k:x in A_j}.

There are exactly a-1 recipients in Q: A has no R-coverer before k, and current k covers x. Root proposes

    0<=z_j<=h/a   (j in Q),
    L=h-sum_(j in Q)z_j,
    L<=v h/a.                                      (ALL)

The edge bounds themselves give

    h/a<=L<=h.

Thus ALL is equivalently

    h/a<=L<=min(h,v h/a),
    sum_jz_j>=h(a-v)_+/a.

The all-uniform point z_j=h/a, L=h/a is always feasible. Empty input h=0 forces every amount to zero. These are linear conditions for fixed data a,v.

Let n be the number of new A-coverers, c the number of common future coverers, and ell the number of V-coverers absent from A. Current k is common. Then

    a=1+c+n, v=1+c+ell, a-v=n-ell.

The old raw point has all n new edges h/a, all common edges zero, and current h(1+c)/a. It satisfies ALL because 1+c<=v. The old optional-common family is therefore contained in ALL.

## 2. Same-client density proof survives

This uses root's round8 initial source contract without changing its payment budgets. Every future edge still enters the genuine prescribed context on A, and its mass is at most h/a. All outgoing mass is at most (a-1)h/a<h, so each client and origin has a substochastic strictly-increasing-role flow. In particular its total incoming mass over one role layer is at most its initial future mass.

For any nonactual target context s, let r be its history's first deviation from the actual history. Every reset parent of s has role r, though there may be many such parent histories. Its reset leaf is the target's completion V_s. Therefore the density contribution of each parent edge is

    c_Vs(x) z_parent <= h_parent.

The same-role parent antichain pays all such contributions together. With direct query entries treated exactly as in round8, the unchanged argument gives

    c_Vs(x)h_sx
       <=sum_(source owner=r)p_source,x
         +sum_(source owner<r)A_source,x
       <=1.

No old/new recipient requirement is used in this argument. Only the true reset domain, edge cap h/a, mass conservation, and strict role increase are needed. Hence ALL preserves the full same-client density invariant, including actual mergers and arbitrary choices of its local variables.

## 3. One complete query IC remains legal

For one context, put f_tx=c_V(x)h_tx. With no input on other clients, ALL gives

    sum_(x in R)L_tx
       <=sum_(x in R) f_tx/c_A(x)
       <=sum_(x in current action)1/c_A(x)
       =D_t<=u_k.

The second inequality uses the global density f_tx<=1. The last inequality is one genuine complete actual-prefix query IC. Thus this is not customer-reweighted IC. Current is a source label and is paid from actual role k's complete wallet, as before; actual k need not cover x.

## 4. Old-source check and exact distinction

Same-client cancellation itself is old. Two explicit sources are:

- `../../round5/credible/all_fresh_submarkov_elimination.md`, section 6, NET-CANCEL: cancel min(new,lost) equal-price positive/negative units at one context and one client.
- Peer `../../../R-d3981c0168644971803a9c3380ed687c/next_general/credible/clock_cycle/source_preserving_kernel_review.md`, section 4: the same cancellation is explicitly applied to the source-preserving per-client kernel. Its surviving same-client edges have strictly increasing load.

For this R-only setting, the maximal old NET cancellation leaves total new outflow h(a-v)_+/a and current min(h,vh/a). No common recipient is used at that corner. Hence increasing current by canceling new edges up to the lost-coverer amount is already old NET, not a new mechanism here. `../../round6/credible/safe_coupon_netting.md` also has stronger complete-profit scalar CLIP, but explicitly does not preserve individual source clients; it must not be silently identified with ALL.

ALL additionally makes the necessary outgoing mass fungible among **all** reset coverers. This is more than maximal NET followed by optional common-edge additions. For example, take local counts n=2,c=1,ell=1, hence a=4,v=3. ALL allows both new edges zero, the sole common edge h/4, and L=3h/4. NET alone must retain at least h/4 of new outflow; adding a common edge afterward cannot remove that requirement. This is a strict local feasible-set comparison at those counts, not a claim that this count pattern has been realized here by a new SPE example or that it improves global welfare.

Latest ownership changes the initial p variables and support. It does not by itself implement this local recipient redirection. The two enlargements are compatible if the full initialization and density contracts are kept and all payment amounts are recomputed.

## 5. Concrete conditional capacity-repair directions

The family supplies actual directions in a fixed source flow, not just an unnamed LP enlargement. Freeze all downstream routing ratios rho_sj(x)=z_sjx/h_sx at one feasible flow; at zero-input nodes choose any feasible ratio, for example full-uniform. Let pi_s(x) be the resulting vector of final current payments by actual role per one mathematical unit entering s. The finite homogeneous role DAG defines

    ell_s=1-sum_jrho_sj(x),
    pi_s=ell_s e_role(s)+sum_j rho_sj(x)pi_target(s,j),
    pi_s>=0, sum_l pi_s(l)=1.

This unit vector is a linear propagation coefficient, not a claim that an independently injected unit respects IC density.

Two local changes are valid:

**Cancel toward current.** For a child j with existing flow z_j, any

    0<=delta<=min(z_j, min(h,vh/a)-L)

may be removed from that edge and added to current. Recomputing all descendants with the frozen ratios changes the actual role-payment vector by

    delta[e_k-pi_target(j)].

**Redirect between recipients.** For two distinct reset recipients j and q, any

    0<=delta<=min(z_j,h/a-z_q)

may be moved from j to q, leaving L unchanged. The resulting role-payment change is

    delta[pi_target(q)-pi_target(j)].

Removing part of an existing edge never makes descendant inputs negative. Added flow is propagated with legal ratios. The new global density theorem applies to the recomputed whole flow, so it is not necessary to assume that descendants had an independent unit of unused density. Initial source quantities are fixed throughout and source clients are preserved.

These changes strictly improve any role-price objective whenever the destination probability vector is cheaper. They can repair a concrete overloaded role if the receiving payment vector fits the actual remaining capacities. What is unproved is that suitable directions exist to repair **every** instance/SPE and every remaining cut. No universal balancing gain follows merely from the local directions.

## 6. Exact local price rule and limitation

For h>0 set y_j=a z_j/h and q=(a-v)_+. Given current price lambda_k and downstream unit prices psi_j, the local minimum is

    min lambda_k+(1/a)sum_j y_j(psi_j-lambda_k)
    over 0<=y_j<=1, sum_jy_j>=q.

Choose all recipients with psi_j<lambda_k. If fewer than q recipients have been chosen, fill the remaining required amount at the cheapest further prices; ties can be split. This gives a precise order-statistic recursion in the finite DAG. When all role prices are 1, every pi has price 1 and every local choice still costs one unit: total mass is unchanged. Therefore this optimization does not pay HALF's constant-price cut.

## Status

ALL, global density preservation, one-whole-IC legality, old NET attribution, strict recipient freedom, and the conditional repair directions check analytically. No new finite search was used. The new freedom can move payment between actual roles while preserving the source and local IC envelope; common role capacity and general half remain open.

## 7. Further whole-row cancellation, proposed to root

There is a still larger local family if one wishes to spend all of the same context's one actual-row wallet rather than impose the clientwise upper envelope. Retain the all-reset edge caps and source conservation, but use

    sum_(x in R)L_tx<=u_k                         (ROW)

instead of every L_tx<=v_tx h_tx/a_tx. This is a single complete actual-role monetary cap, not separate customer ICs. For fixed h with f_tx<=1, the full-uniform point has

    L_min=sum_x h_tx/a_tx<=sum_x f_tx/a_tx<=D_t<=u_k.

It follows that ROW has a feasible point at the maximum total current

    sum_xL_tx=min(sum_xh_tx,u_k).

Indeed start from the uniform point and cancel a total

    min(sum_xh_tx,u_k)-L_min

of existing future-edge mass. This lies between zero and all outgoing mass. Every canceled edge's own source x remains as current L_tx, so there is no source-customer resampling. The residual edges still satisfy 0<=z<=h/a and every L_tx>=h/a. Consequently the global density proof in section 2 continues to apply to the recomputed DAG. The uniform point supplies a topological construction; after any such whole-row cancellations, complete payment amounts and role totals must be recomputed.

The perclient ALL family is contained in ROW because sum_xL_tx<=sum_xf_tx/a_tx<=u_k. Inclusion can be strict when the complete query has unused clients or density slack. This is the familiar scalar CLIP idea applied *after* source-preserving routing; the local financial cancellation is old, while no assumption of old complete-profit customer resampling is needed for this application. It is best recorded as a compatible enlargement, not a new welfare mechanism.

ROW does not assert that this context owns a distinct unspent copy of u_k. Different histories of the same role still compete for the same overall ROLE amount. Thus neither ROW nor its maximal-current point settles the distinct-action query budget or HALF. Root was sent the exact statement and proof for independent assessment; it is not included in the review endorsement of root's original ALL family above.
