# Independent review: root's all-player weak adjacent-wallet counterfamily

2026-10-24, netglobal10. This review reconstructs the mathematics from the
precise family and claim supplied by root, before reading a primary proof.
**The stated family passes the analytic review.** It refutes the existential
optimal-assignment adjacent-wallet bridge for m>=7 and refutes every fixed
multiple of that wallet over unbounded m. It does not refute Q-CAG-HALF or
separate the enlarged ROLE certificate. No scan, fixed-packet replay,
external review, or novelty claim is involved.

## 1. Exact instance, policy, and candidate

Let m>=2 and k=m-1. Take mutually disjoint unit-customer blocks:

    |K|=k(k+1)=km,
    {a_1},...,{a_k}, {b}, and |E|=k.

The common catalog consists of

    C=K,
    A_i=K union {a_i}, i=1,...,k,
    B=K union {b},
    D={b} union E.

At every history consisting only of C choices, prescribe C unless the
current player is last; at that last node prescribe D. At every history
containing any non-C choice, prescribe the smallest-index A_i not previously
chosen; if every A_i has already been chosen, prescribe B. A theme is
"unused" here by its label A_i; C and B do not count as uses of an A_i.

For the actual leaf Z, define frozen utility

    f_l(T)=u_l(T,Z_(-l)),

and for an ordered optimal comparison tuple T set

    Q(T)=sum_l f_l(T_l).

The actual adjacent exit wallet is

    C_adj=sum_(l<m) sum_(x in Z_l minus Z_(l+1))
                    1/[c_Z(x)(c_Z(x)+1)].

The tested weak bridge is the existence of an optimal ordered tuple T with
Q(T)-W<=C_adj. This is distinct from requiring the inequality for all
optimal assignments or for independent frozen row maxima.

## 2. Complete-history SPE verification

Consider first a triggered prefix h, meaning h contains a non-C action.
Let its length be ell<=k and let d be the number of D actions in h.

If every A_i has already appeared, then ell=k and the k preceding actions
are exactly the k different A_i. In particular this is the last decision
node, d=0, and neither C, B, nor D has appeared. The prescribed B has core
profit |K|/m=k plus fresh b profit 1, totaling m. Any core action has core
part k and private bonus at most 1; D yields m. Thus B is optimal.

Otherwise the policy prescribes a fresh A_i. All subsequent prescribed
actions are core themes. Each fresh A_i is never copied. A B can be used
only after all A_i have been used; if that occurs, it is the last action
and b is fresh. To see the latter precisely, if there are s distinct A_i
in h then the number of unused A_i after the current fresh choice is
k-s-1, while the number of players remaining afterward is k-ell. A B can
be needed only if ell=s, in which case h consists solely of distinct A_i
and its private b has not appeared. These observations hold at arbitrary
off-path ordered histories, including repeated C, B, A_i, and D choices.

Under the prescribed fresh A_i, the final number of core players is m-d.
The current profit is consequently

    V(h)=|K|/(m-d)+1 >= |K|/m+1=k+1=m.

Any legal core deviation C, A_j, or B leaves the final core count m-d:
the prefix is already triggered and all future prescribed actions remain
core themes. Its core profit equals |K|/(m-d), and its private bonus is at
most 1. This also covers deviation to a used A_j or to B when b has already
been shared. Hence every core deviation is weakly worse than V(h).

A deviation to D is followed only by core themes. Its E customers have
load d+1, and b has load at least d+1. Its utility is therefore at most

    (|E|+1)/(d+1)=m/(d+1)<=m<=V(h).

The previous paragraph also verifies D against the prescribed B at the
only no-unused-A node. Thus all triggered subgames satisfy the full IC.

Now let h consist only of C choices. If the current player is not last,
following the policy gives the final leaf C^k,D and current profit
|K|/k=m. Choosing any A_i or B triggers an all-core continuation. Its core
load is m and its own private customer remains unshared, so it obtains
|K|/m+1=m. Choosing D triggers a continuation of fresh A_i; no later B is
needed, and D obtains its m customers alone. Thus all such deviations give
m, and prescribed C is optimal.

At the last all-C node, prescribed D gives m. A_i or B gives core part k
plus private part 1, also m; C gives only k. This last C comparison is a
necessary separate case and is consistent with the claimed SPE.

Every history is either triggered or all-C, and every legal action has
been checked with its true policy continuation. The policy is therefore
a complete ordered-history pure SPE.

## 3. Actual welfare and the unique optimal support

The actual leaf is Z=C^k,D. Each of the k core players receives
|K|/k=m, and D receives |E|+1=m. Hence

    u_l=m for every l,
    W=|K|+|E|+1=m^2.

The whole catalog universe is

    K union {a_1,...,a_k,b} union E,

with size m^2+k=m^2+m-1. The m themes A_1,...,A_k,D cover it, so

    OPT_m=m^2+m-1.

Every optimal tuple must cover each a_i, which occurs only in A_i, and
must cover E, which occurs only in D. These k+1=m required distinct themes
already consume all slots. Thus the only optimal support is exactly
{A_1,...,A_k,D}, each used once; all optimal ordered tuples are its
permutations. In particular no duplicate theme, C, or B can enter an
optimal m-tuple. This establishes the universal quantifier over optimal
assignments used below.

## 4. Frozen matrix and minimization over every optimal assignment

At any early actual core role l<=k, the other roles contain k-1 copies of
C and one D. At the actual final role, the other roles are k copies of C.
The full frozen matrix is therefore

| Role | C | Any A_i | B | D |
| --- | ---: | ---: | ---: | ---: |
| l<=k | m | m+1 | m+1/2 | m/2 |
| l=m | k | m | m | m |

For example, an early frozen D shares every one of its m customers with
the actual final D, giving m/2. An early B shares only b with D, explaining
its bonus 1/2. These denominators are frozen-profile denominators, not
claimed true deviation continuations.

If D is assigned to the final role, all k A_i go to early roles and

    Q_last=k(m+1)+m=k(k+2)+(k+1)=OPT_m.

If D is assigned to an early role, k-1 A_i occupy the other early roles
and one A_i occupies the final role. Hence every such assignment gives

    Q_early=(k-1)(k+2)+(k+1)+(k+1)/2.

The difference Q_last-Q_early=(k+3)/2 is positive for every k>=1.
Consequently the exact optimum over all optimal ordered tuples is

    min_T Q(T)=Q_early,
    min_T Q(T)-W=(k-3)/2=(m-4)/2.

This minimizes over the complete optimal-assignment set rather than merely
exhibiting one expensive assignment.

## 5. Adjacent wallet, strict separation, and fixed multiples

All adjacent C-to-C transitions contribute zero. The only nonzero
transition is the final C-to-D transition. Its leaving customers are
exactly K, each with actual load k, giving

    C_adj=|K|/[k(k+1)]=1.

Thus

    min_T [Q(T)-W-C_adj]=(m-6)/2.

The weak existential adjacent-wallet bridge is strictly false for every
m>=7. More generally C_adj remains 1 while min_T Q(T)-W=(m-4)/2 diverges.
For every fixed finite alpha>=0, choosing an integer m>2alpha+4 gives

    Q(T)-W>alpha*C_adj for every optimal ordered T.

So replacing the adjacent wallet by a fixed universal multiplier cannot
repair this particular bridge. This statement is about this exact wallet
and frozen-assignment interface; it does not rule out other actual
credits, the existing payment certificate, or a different general proof.

The original welfare ratio is

    OPT_m/W=1+(m-1)/m^2<2.

The construction therefore satisfies HALF and is solely an auxiliary
bridge counterexample.

## 6. Five-player pressure substitution

At m=5, k=4, the same formulas give

    |K|=20, |E|=4,
    actual=C^4,D, u_l=5, W=25, OPT_5=29,
    C_adj=1, min_T Q(T)=51/2,
    min_T Q(T)-W=1/2,
    min_T Q(T)-W-C_adj=-1/2.

Thus this all-m derivation does not separate the existential bridge at
five players. Its strict m>=7 failure is nevertheless a complete
refutation of the proposed arbitrary-m bridge. Neither observation proves
or refutes arbitrary five-player HALF. No five-player-only modification
or computation was used.

## 7. Full primary postread review

After completing the reconstruction above, I read root's full
[primary proof](../parent/optimal_assignment_adjacent_wallet_counterfamily.md).
Its analytic definitions, all-history SPE proof, unique optimal support,
frozen matrix, minimum over all optimal assignments, fixed-alpha claim,
five-player substitution, and separation from HALF all agree with the
independent derivation. **The full analytic primary passes this postread
review; no mathematical correction was needed.** This is an internal
review, not an external review or a novelty assessment.

The principal domain points were checked explicitly:

1. The no-unused-A fallback entails at least k prior actions. Since a
   current player still exists, the prior length is exactly k, so all
   previous actions are the distinct A_i and d=0. The prescribed B has a
   fresh private b and no later continuation. The primary does not use
   this last-node argument at an arbitrary earlier fallback state.
2. In a triggered prefix, the non-C event is already in the fixed past.
   A current deviation to C cannot remove that trigger. Every later
   prescribed action is consequently a core theme for both the
   prescribed branch and every core deviation. The final core count
   m-d is therefore identical in these comparisons, as claimed. A D
   deviation increases the number of non-core players and is treated
   by its own independent bound m/(d+1).
3. Requiring every a_i and E forces exactly the k distinct A_i and D.
   These already use all m slots, so neither a different optimum nor
   repetition can evade the two assignment cases. All A_i columns and
   all early rows have the same relevant costs. The claimed Q_min is a
   global minimum over optimal tuples and assignments.
4. The fixed-alpha claim retains its quantifiers: for each fixed finite
   real alpha>=0, an integer m>2alpha+4 gives a strict violation for
   every optimal assignment. Alpha is not permitted to grow with m.
   The result rules out precisely a fixed multiple of C_adj in this
   interface and makes no broader impossibility assertion.

The primary's additional wider-wallet arithmetic also checks directly.
For Z=C^k,D, the actual base wallet is

    J_base=|K|/(k+1)+|D|/2
          =k+m/2=(3m-2)/2,
    J_base-(Q_min-W)=m+1>0.

Thus this family does not refute payment of the optimized frozen sum by
J_base. Also Q_min-W=(m-4)/2<=m=W/m, so it does not refute the wider weak
assignment bound Q<=(1+1/m)W. These scope limitations in the primary are
mathematically correct.

No new tests were run for this postread review. The independent proof
above supports the all-m analytic claims; it does not independently
authenticate the primary's separately reported finite implementation QA.
