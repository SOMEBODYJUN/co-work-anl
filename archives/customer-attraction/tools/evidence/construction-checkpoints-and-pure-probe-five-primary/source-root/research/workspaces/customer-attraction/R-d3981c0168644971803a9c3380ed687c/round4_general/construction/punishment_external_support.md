# Credible punishment requires support outside the queried topic

2026-10-24. **Elementary all-input identity/necessary bound; exploratory, not an independently reviewed new asset.** It does not close half. No extra restriction on the common catalogue, the number of players, duplicate actions, client incidence, or off-path histories is imposed.

Fix any complete-history pure SPE sigma, an actual node i, and its actual final profit u_i. Force a legal query topic T at that node and then follow the original complete strategy. Write z^T for the resulting genuine terminal, d(T) for the queried player's final profit, c_x for its full terminal loads, and S_j for a follower j's chosen topic. Root/node optimality gives d(T)<=u_i.

Every unit follower has exactly the same per-customer share as the queried player on their intersection. Hence, defining

    I_j(T) = sum_{x in S_j intersect T} 1/c_x,
    E_j(T) = sum_{x in S_j minus T} 1/c_x,

we have the exact split u_j(z^T)=I_j(T)+E_j(T), with

    0 <= I_j(T) <= d(T) <= u_i.

Let ell_j be any valid lower guarantee for the follower at its genuine branch history. For example, if its prefix loads are b^j and it has r_j players remaining including itself, full-history optimality gives

    ell_j = max_{Q in catalogue} sum_{x in Q} 1/(b^j_x+r_j).

It follows that

    E_j(T) >= (ell_j-d(T))_+ >= (ell_j-u_i)_+.

Summing these are compatible payments from one terminal client pool, because every customer outside T pays at most one unit across all followers. Consequently

    |(union z^T) minus T| >= sum_{j>i} (ell_j-d(T))_+
                          >= sum_{j>i} (ell_j-u_i)_+.

One may replace the left side by the followers' exact total outside-T shares, which is smaller when fixed past players also cover those customers. The displayed count bound is only a convenient weakening.

At the final follower, its exact guarantee is its ordinary best response value. If U denotes customers omitted by the original actual outcome and P is the union of its genuine branch prefix, then every Q supplies at least |Q intersect (U minus P)| from entirely new omitted customers. Thus its outside-T shares must be at least

    [max_Q |Q intersect (U minus P)| - u_i]_+.

This isolates the difficulty with direct multi-real attacks: a late punisher whose total target-intersection shares cannot exceed the low queried payoff must obtain its large remaining profit elsewhere. If other fresh queried themes have not been covered, they remain legitimate outside options at its last node.

## Why this does not prove the target

The supporting pool is a *branch* pool, not the actual pool. It may include omitted customers outside T that become covered only after this query. Entry through the topic S_j is itself controlled by a different true continuation, so its support cannot be charged to original W without another cross-branch relation. Summing the displayed inequalities over T double counts these supporting clients and supplies no such relation. Arbitrary history dependence prevents treating the original branch continuation as the continuation after entering directly through S_j.

The same limitation blocks a proposed proof by following a chain T -> last chosen topic S_m(T): finite cycles of topic labels do not identify the full ordered histories or their continuation loads. No telescoping argument has been proved. This is the current unresolved obligation, rather than a claimed general impossibility or counterexample.
