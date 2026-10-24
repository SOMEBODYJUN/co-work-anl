# Distinct-action menu aggregation: working derivation and exact stop

2026-10-24, menu9. General Q-CAG-HALF remains **OPEN**. This work concerns arbitrary finite common catalogs, arbitrary player counts, and every complete history-dependent pure SPE. No fixed-player positive project or restricted-catalog result was pursued.

## Recovered interface

For actual role j and catalog action a, define the original actual-prefix query and client vector

    A^(j,a)=finish_sigma(B_<j,a),
    z_(j,a,x)=1_(x in a)/c_A^(j,a)(x),
    D_(j,a)=sum_x z_(j,a,x)<=u_j.

For a raw source-preserving reset at natural context t of role j, let a_t be its prescribed action, h_tx the incoming source, and r_t(x) the number of x-coverers common to the context's original leaf and A^(j,a_t). The current source is

    g_tx=h_tx r_t(x)/c_A^(j,a_t)(x).

If all sources at role j admit a common nonnegative complete-query cover

    g_j(x)<=sum_a lambda_(j,a) z_(j,a,x),

then their total amount is at most u_j sum_a lambda_(j,a). The still unpaid claim is the joint coefficient budget, or a weaker cross-role monetary inequality. The local f_tx<=1 theorem already makes one context legal; it does not supply a sum over contexts or actions. See `../../round8/credible/joint_query_compression.md` for the full contract.

## Same-action corner is old and distinct actions remain

At the all-common-future-full (uniform-reset) corner for R clients, current is h_tx/c_A(x). For fixed (j,a), all histories have the same reset and denominator. Their role/client antichain gives aggregate H_(j,a,x)<=1, so one complete query pays the whole same-action group. With uniform initial R splitting, the initial source at role j and action T_j can join this same coefficient: its p_jx and earlier-origin incoming masses are bounded together by the prefix inventory sum_(i<=j)p_ix.

This is not a new mechanism. `../../round8/residual/common_action_reset_deduplication.md` identifies the same state (j,a,x), uniform flow, and HIT bound as round3's increasing-role capture flow. I sent this source check to payment9 after its independent reconstruction.

Even in that corner, source inventory only gives

    sum_a H_(j,a,x)<=1  for each x.

The available direct complete-query coefficient is max_x H_(j,a,x). The inventory inequality does not imply sum_a max_x H_(j,a,x)<=1: different actions may attain their maxima on different customers. No genuine SPE implication restricting that actionwise envelope has been derived here.

## Why the obvious off-history regrouping has not closed

For context t=(g,j), let V_t be its prescribed leaf, A_t its actual-prefix reset, and U_t=finish_sigma(g,B_j) the genuine return-action leaf. The selected-vs-return off-history IC is u_j(V_t)>=u_j(U_t). Together with D_(j,a_t)<=u_j this gives the round8 rectangle, whose off-history advantage is nonnegative. It is not a negative refund that can be deleted to upper-bound the total current. I found no valid common sign beyond the already retained individual ICs.

A second attempted route was ordinary demand/revealed-preference geometry. At the terminal role, all alternatives at a fixed history are evaluated against one fixed prefix-load vector, so the usual linear-demand description is valid. Before the terminal role, each alternative action changes its own original-strategy continuation and therefore its final load vector. One cannot replace these genuine complete continuation payoffs by an action-independent price vector, nor assume cyclic monotonicity between different histories, without a separate theorem. The valid terminal description alone has not controlled the incoming source weights, which depend on both history and prescribed action.

## Unproved action-upgrade idea

On a given full query leaf, two providers who choose the same topic obtain exactly the same full profit. Thus if a future source receiver chooses the original source owner's topic, its complete profit is already the owner's query payoff and is subject to that owner's actual-node IC. For a receiver choosing another topic that merely overlaps the source client x, the extra clients of its new topic may be needed to make it optimal. A possible proof route would couple those action upgrades to exchanges in the optimal comparison portfolio or to the actual topics the receivers could copy.

No exact cross-history inequality implementing that route was established. It is a mechanism suggestion, not a result. Customer support and role/client antichains alone do not pay these extra complete-action rows.

## Retained positive review and pressure test

`terminal_wallet_independent_review.md` reconstructs exchange9's all-m actual terminal-wallet relation

    C'<=W/(2H_m+1).

Its proof uses earlier players' genuine complete deviations to the actual penultimate topic and spends those same actual profits once. At m=5 it yields C'<=30W/167<W/5. This is unconditional but only caps the reduced terminal wallet. Earlier frozen taxes and distinct-action query amounts remain open, so it does not prove OPT_5<=2W.

No new finite policy search, SPE search, or no-counterexample claim was produced. All mathematical stops above are limitations of this derivation, not impossibility statements about Q-CAG-HALF.
