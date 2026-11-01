# 相邻真实前缀负载的精确联合恢复

Status: elementary exact identity, arbitrary player count. This is a representation
and nonnegativity test for shared source states, not a root welfare bound.

Suppose q genuine histories are recorded just before the last two actions.
For one client and one retained index-label group, let P_i be its load before
the penultimate action and Q_i its load before the final action along that same
strategy branch. Then Q_i=P_i+a_i, where a_i is the actual penultimate topic's
client membership, hence a_i in {0,1}.

Let L(c)=#{i:P_i=c}, M(c)=#{i:Q_i=c}. The two marginal load histograms determine
**the entire joint histogram** of (P,Q), not just its two margins. Write

    X_c=#{i:P_i=c,Q_i=c+1},   Y_c=#{i:P_i=c,Q_i=c}.

The unique solution is

    X_c = sum_(j<=c) [L(j)-M(j)],
    Y_c = L(c)-X_c
        = sum_(j<=c)M(j)-sum_(j<c)L(j).                         (1)

All unspecified load counts are zero. Necessity follows from L(c)=X_c+Y_c
and M(c)=Y_c+X_(c-1), with X_-1=0. The recurrence gives (1).
Conversely, if all X_c,Y_c in (1) are nonnegative and both marginals have the
same finite total, the entries define the required joint histogram. Their
integrality is automatic for integer margins. Thus the exact compatibility
test is the cumulative interlacing

    F_L(c-1) <= F_M(c) <= F_L(c)     for every c,                (2)

where F_L(c)=sum_(j<=c)L(j), and likewise for M.

This matters when jointly optimizing real final-player menu rows and retained
last-two pair-query rows. The final-player cost uses 1/(Q+1); the pair-query
cost uses 1/(P+1) and 1/((P+1)(P+2)). A single common matching sees both P and Q
in the same source slot. Usually, fixing separate background histograms would
lose their correlation. Here (1) recovers that correlation exactly because
the backgrounds differ by exactly one actual action bit. Consequently a
conditioned pricing implementation may enumerate the two marginal signatures,
reject those failing (2), recover their joint with (1), and optimize any
combined final-player/pair-query transport cost without loss from this step.
Actual own-share sums and the retained H-source sums remain functions of the
full source histogram; they are not determined by L,M alone.

The qualification is essential. If Q-P may be 0,1,2, marginals do not in
general determine their joint. For L supported once each at 0,1 and M once
each at 1,2, both {(0,1),(1,2)} and {(0,2),(1,1)} are legal and have the same
margins. General mixed costs would then need a joint vector signature or an
explicit transport optimization. Formula (1) does not recover memberships of
unrelated actions or all histories from separate load margins.

`verify_adjacent_load.py` exhausts finite integer margins for small q and load
ranges, checks uniqueness against all individual (P_i,Q_i) lists, and tests (2)
against reconstruction. The arbitrary-q proof is the recurrence above.
