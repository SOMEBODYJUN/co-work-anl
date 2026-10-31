# Exact-only: flat unit-resource path preserves one explicit degree-four contract

Author: /root/sol_literal_budget_attack, 2026-10-18. Scratch candidate, not independently reviewed or claimed novel. This is separate from the already reviewed R_cons claim and does not modify it.

Input is any complete explicit normalized-flat P(Q), including all original indexed states, positive and zero incidence jobs, and unused resources, with nonempty groups and states. Apply the positive-neighbor group-port operation D_+ already defined in the frozen conditional-leaf Exact: each original incidence job keeps its private endpoint and time, while its unit resource endpoint is routed to its designated port; retain the d=0 old resource. Add the two-root, two-singleton-state unit flat jobs for each adjacent path leaf. All original jobs remain.

For fixed binary rational 1<=T<2 define K2(P,T) as follows.

- A supplied finite rational machine-CONFIG certificate has per-machine weight one and legal load at most T.
- Its first and same-machine pair membership marginals agree with a global rational Boolean moment functional of degree at most four on all finite job-machine assignment indicators.
- The functional is normalized, is PSD on squares of all polynomials of degree at most two (M2), and satisfies Boolean and exact one-hot job identities throughout degree four. Thus the linked CONFIG job marginals cover every job exactly once.
- For every physical machine i, its global linear-load localizer satisfies L((T-load_i)q^2)>=0 for every globally indexed affine-linear q.

No positivity for arbitrary global quartic literal monomials, no joint distribution of complete schedules, and no moments of CONFIG-list weights are added by this definition.

**Claim.** For every Q and every 1<=T<2, K2(P(Q),T) is feasible if and only if K2(P(D_+(Q)),T) is feasible. Given a complete finite rational certificate on either side, one can construct a certificate on the other side in deterministic time and total bit size polynomial in the explicit instance and supplied certificate lengths.

The forward map preserves every original assignment moment and every old private-root CONFIG list; it extends the functional to the new leaf-job variables. The reverse map preserves the principal functional on all original job-assignment variables, with each original resource indicator identified with that job's routed port indicator, and preserves the old private-root lists. Unit resource configuration lists may be reconstructed from first moments. All load localizers remain part of the contract in both directions.

The same assertion holds if the load-localizer requirement is omitted on both sides. It is a certificate transformation, not an SDP solver or a general CONFIG/UM approximation. It does not assert arbitrary stronger C2 conventions, preservation at T>=2, preservation of a given full matching law, or computational hardness. Both sides are infeasible for T<1 because they retain an original unit selector.
