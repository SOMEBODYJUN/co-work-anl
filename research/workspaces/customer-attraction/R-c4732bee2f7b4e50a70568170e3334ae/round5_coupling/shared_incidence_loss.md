# 共同客户匹配损失的非负层分解

Status: proved algebra and necessary SPE inequalities; exact computational checks below.
This is an arbitrary-player interface, **not** a proof of Q-CAG-HALF.
The new 727-row-point separation is exact, but does not exclude all above-two points.

## 1. General final-player families

Use the unit-client common-catalog model, with a pure SPE defined at every ordered history.
Take any q genuine last-player histories indexed by i, repeated histories allowed.
For client x, let p_i(x) be the load just before that last action and f_i(x) its
membership in the actual final action. Put d_i=1/(p_i+1), A_x=sum_i f_i d_i,
and D_x=sum_i d_i. Let Z_i^j, j=1,...,s, be arbitrary indexed legal menu topics;
these need not be continuations of the source histories. Their client bits are z_i^j.
All families share an index label t_i (for example membership in anchor T_i), which
must be retained when matching compressed states.

For one menu j, summing the real last-player comparisons over i!=k gives

    (q-1) sum_x A_x - sum_x K_j D_x + sum_x sum_i d_i z_i^j >= 0,
    K_j=sum_i z_i^j.

Every term compares the real reply at history i against a legal single topic Z_k^j.
No reply from another branch is substituted as a continuation. The analogous
diagonal row is sum_x[A_x-sum_i d_i z_i^j]>=0.

For positive weights w_j on offdiagonal rows, let S_i=sum_j w_j z_i^j. Within each
retained label t, arrange the d_i and S_i in the same decreasing order. This is the
exact common-matching maximum. Define Top_d(k) as the sum of the k largest d_i,
and Top_S(r) as the sum of the r largest S_i in that label group.
If k_j=sum_i z_i^j in the group, the difference between separately maximized
rows and the jointly maximized row is

    Delta_t = sum_j w_j Top_d(k_j) - sum_i d_(i) S_(i).

The following exact decomposition makes its positivity explicit:

    Delta_t = sum_(r=1)^(n_t-1) (d_(r)-d_(r+1))
              * [sum_j w_j min(k_j,r) - Top_S(r)].                 (1)

Every factor and bracket in (1) is nonnegative. Indeed, any r selected slots
contain at most min(k_j,r) members of menu j; maximizing the weighted sum over
the r slots gives Top_S(r). Thus a genuine SPE satisfies

    sum_j w_j (separate upper-envelope row j) >= sum_x sum_t Delta_(x,t). (2)

The right side is an explicit amount lost by independent optimization. It is
not an assumption that each menu can separately take the best matching.

**Proof of (1).** For every integer k in [0,n],

    Top_d(k)=d_(n) k + sum_(r=1)^(n-1)(d_(r)-d_(r+1)) min(k,r).

Likewise, summation by parts gives

    sum_i d_(i) S_(i)=d_(n) sum_i S_i
       + sum_(r=1)^(n-1)(d_(r)-d_(r+1)) Top_S(r).

The d_(n) terms cancel because sum_i S_i=sum_j w_j k_j. Empty label groups have
zero contribution. These are finite identities, valid for all q and all loads.

Diagonal rows also fit (1): a coefficient -w_j z_i^j equals
w_j(1-z_i^j)-w_j. Replace each diagonal menu bit by its complement and use its
complement count. The constant -w_j D_x is independent of the matching and
cancels from the separate-versus-joint difference. Thus (1) applies to any
nonnegative combination of diagonal and offdiagonal menu comparisons, with
arbitrary menu weights and all target tuple intersections retained.

## 2. Two menus and the common-prefix three-player family

For two unit-weight offdiagonal menus M,N in one label group, write k,l for
individual membership counts, h for their same-index intersection and u=k+l-h.
Then S_i has h twos, u-h ones and n-u zeros, so

    Delta=Top_d(k)+Top_d(l)-Top_d(h)-Top_d(u).                      (3)

For an arbitrary source list, (1) becomes

    Delta=sum_(r=1)^(n-1)(d_(r)-d_(r+1))*delta_r,
    delta_r=max(0,min(r-h,k-h,l-h,u-r)).                           (4)

To verify the bracket formula, assume k<=l (the other order is symmetric).
As r crosses h,k,l,u, the bracket respectively is 0, r-h, k-h, u-r, 0.
This proves (4), including equal counts and zero intervals.

Now fix any genuine ordered prefix h0 with exactly three players left, with
client load p_x. Let its next player choose each indexed anchor T_i; let A_i,B_i
be the same strategy's real last two replies after h0 T_i. Retain t_i=1_(x in T_i).
At the final-player source history h0 T_i A_i,

    d_i=1/(p_x+t_i+1+1_(x in A_i)).

In a t-group there are only two possible inverse denominators. If r is the
number of A_i nonmembers in the group, the larger denominator-inverse level
occurs r times. Consequently (4) reduces exactly to

    Delta_t = max(0,min(r-h,k-h,l-h,k+l-h-r))
              / ((p_x+t+1)(p_x+t+2)).                             (5)

This formula applies for **every total player count m>=3**, every q, arbitrary
common catalog and arbitrary histories and ties. The hypothesis is a genuine
common-prefix three-player deviation family; arbitrary unrelated histories can
have more than two load levels, in which case the full decomposition (1) applies.

The loss is positive exactly when the two menus' exclusive memberships compete
for the same high-inverse-denominator slots. Source load heterogeneity and target
same-index intersection are both essential. Merely retaining menu counts gives
no positive lower bound uniform over all target overlaps.

## 3. Exact strictness on the unrestricted 727-row point

The sibling `round5_pricing/exact_optimum_primal_terminal_cross.json` has 69
positive rational atoms, W=1 and comparison coverage about 2.0421101417004013.
It is a necessary-condition template point, with no actual OPT or full SPE claim.
Its SHA-256 is `e2caa8f504da61dd41c6980671f2ce3d0c715f5d4dcce4b16dd656af25363acb`.

Take source AB, target second, and its positions 2 and 3 (the target final-two
menu topics V,W). Both separate offdiagonal upper-envelope slacks are positive,
about 0.0140649 and 0.0767854. But their shared-matching OO envelope is

    -1986982543309346411409324987349550640449892779560449694465 /
     14981334465482123235868977333713366662779525538289172031104
    = -0.1326305442207082... < 0.

Thus this point has no full SPE completion retaining the stated family marginals.
Unlike the earlier 557- and 717-row-point separations, this exclusion cannot be
attributed to a negative single component row. Formula (5) gives the exact
positive loss that those two individually positive envelopes fail to pay.

`verify_shared_loss.py` reconstructs the source denominators, own shares and
both target menus directly from the histograms; it does not import the earlier
transport implementation. It verifies (1), (4), the exact 69-atom sum, and the
joint maximum against literal label-preserving permutations. Output is
`shared_incidence_loss_checks.json`.

## 4. Further coupling and limits

`multimarginal_feasibility.py` builds one common three-family customer histogram
for all 220 cross-pair orbit rows and selected cross-terminal rows. It retains
all five equality patterns and the full pair-intersection contribution; it does
not replace pair rows by a diagonal or overlap-free form.

For the exact 717-row optimum, all 220 pair rows plus all 20 individually
nonnegative cross-terminal envelopes are numerically feasible under a common
three-family transport. No extra exclusion is claimed there.
For the exact 727-row optimum, the analogous system of 220 pair rows plus 23
individually nonnegative cross-terminal rows is numerically infeasible. Its LP
dual discovers precisely the two equal-weight AB-to-second offdiagonal rows
above; the independent exact verification supersedes that floating discovery.
These calculations remain fixed-marginal tests, not unrestricted welfare bounds.

The still-open obligation is to charge the losses (1) over genuine histories to
the root outcome's welfare, or to find another argument that forbids all
above-two points. Adding the displayed row excludes this point only. The
full-pricing teammate is recomputing the unrestricted template after adding it.
