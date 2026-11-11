# Actual source 2: symbolic optimal-menu requery layer

Boss1; RUN `six-boss1-20261111`. This package is SYMBOLIC AND UNBOUND. No v4 point has been selected or substituted, no inequality matrix has been assembled, and no optimizer is authorized or imported here. All earlier root72/requery packages remain frozen.

Source owners read for this derivation are the [complete ordered-history model](../../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md), the [true-reply common-potential lemma](../../../../archives/customer-attraction/state/引理/真实末回复的共同潜力上限与重叠参数端点--引理.md), and the [two-tail overlap and index-aggregation lemma](../../../../archives/customer-attraction/state/引理/末两人重叠比较与任意索引聚合--引理.md), especially PAIR, P-M and COVER. The earlier [full36 comparison](../main_full_average_pair.md) explains the valid weaker row retained by previous frozen packages. Section 5 below derives the distinct-index specialization directly from the formal PAIR owner; it does not depend on a future Main note.

## 1. Exact actual history, one common X, and the new indexed branches

Fix the original finite unit-client common-label-catalog complete ordered-history pure-SPE model. Let the actual path be A1,...,A6. For each client retain the FULL old type

    v=(a1,...,a6,x,o) in {0,1}^8,

where x belongs to ONE legal X maximizing f_P over the entire common catalog for the actual first-four load P=a1+a2+a3+a4. X is selected once, not separately for a query or new branch. Let K be the genuine global maximum naked size; X need not attain K. The indicator o belongs to the union of six legal optimal labels Q1,...,Q6. Outside-O clients and the all-zero type remain in the domain.

The old atom mass is z_v; c=sum a; actual payoffs and the common potential are

    u_j=sum_{c>0} z_v a_j/c,
    F_X=sum_v z_v x/(P+1),
    b_j=sum_{k<j}a_k.

At the exact actual source-2 history (A1), force each Q_k and follow the prescribed TRUE continuation R3_k,R4_k,R5_k,R6_k. The new averaged variables are

    nu[v,q,r3,r4,r5,r6]>=0,

defined as one sixth of the client counts across these six genuine indexed branches. The q bit is membership in the SAME Q_k that generated the four successors. All new-tail products refer to that same outer index k, never independent or differently indexed tails.

For each old type v,

    sum_{q,r3,r4,r5,r6}nu = z_v,
    r_v^Q=sum_{tails}nu[v,1,tails],
    o_v z_v/6 <= r_v^Q <= o_v z_v.                  (M)

These are the exact necessary moment bounds for arbitrary overlap among the six labels. Omean is a query-averaging descriptor; it is not Q and is never an added legal action. No optimal-menu disjointness or label distinctness is assumed.

For a future fixed point with s positive old types, the layer has 32s nonnegative physical columns, s mass equations and 2s moment-bound rows, before any later phase-I auxiliary. The universal state domain for a later projected cut is all 256*32=8192 states. This domain size is NOT an instruction to build an 8192-column matrix now.

## 2. Final chosen catalogue: 243 genuine rows

The bounded core has 235 rows. We retain the eight explicitly permitted own-Q comparisons because Q_k is already a genuine stored legal role, so they add no variable or branch. The FINAL chosen raw catalogue has 243 genuine rows:

| Family | Count | Exact domain |
|---|---:|---|
| Actual source2 average IC | 1 | actual u2 versus the six Q_k true branches |
| Average size caps | 5 | Q,R3,R4,R5,R6 |
| Actual-source SAFE | 29 | four tails at all six actual sources (24); Q at sources 1,3,4,5,6 (5) |
| Common actual-P MAX | 5 | Q and four tails |
| Actual fifth-source MX | 5 | Q and four tails |
| New-branch SAFE | 52 | sources 3,4,5,6 times 13 descriptors |
| New true final PAIR | 91 | all unordered/self pairs of 13 descriptors |
| Actual RC new pairs | 55 | 5 new roles times 8 old roles (40), plus 15 unordered/self new/new pairs |
| TOTAL | 243 | all raw rows retained |

The thirteen new-branch query descriptors are

    A1,A2,A3,A4,A5,A6,X,Q,R3,R4,R5,R6,Omean.

The old eight roles are A1,...,A6,X,Omean, and the new five are Q,R3,...,R6. Actual RC's full thirteen-role closure would have 91 rows; its 36 old/old pairs belong to the baseline and are NOT silently duplicated here. The chosen 55 contain 50 pure/pure and 5 pure/Omean pairs. In particular the only mean/mean pair INSIDE the new 243-row catalogue is the new-branch PAIR(Omean,Omean).

The 8 own-Q additions are CAP(Q), MAX(Q), MX(Q), and five actual SAFE rows. Source2 SAFE(Q) is omitted because it is explicitly paid by the source2 IC and nonnegative load slack; see section 7. Actual SAFE1(tail) already is size(tail)/6<=u1, so no extra root-size family is added.

## 3. Row convention and actual budgets

Use one convention throughout:

    A_R nu <= b_R(z,K),     true nonnegative slack R=b_R-A_R nu.

The right side is expressed as a full old-type linear form and, where applicable, one K coefficient. Actual payoffs are always computed from the actual six bits; they are not new-branch payoffs.

### Source2 IC: 1 row

The genuine source2 payoff after forcing Q_k has coefficient

    q/(a1+1+r3+r4+r5+r6).

When q=1 this is the true total load; when q=0 the numerator is zero. Averaging the six actual source2 ICs gives

    sum nu q/(a1+1+sum tails) <= u2.

The outer factor 1/6 is already in nu and is not applied again.

### Caps, MAX and MX: 5+5+5 rows

For each stored pure role L in Q,R3,...,R6, with membership l,

    sum nu l <= K,
    sum nu l/(P+1) <= F_X,
    sum nu l/(P+1+x) <= u5.

The cap and MAX average the six legal labels L_k. Both potential rows use the SAME ACTUAL P, not the new branch's first-four load. MX is the actual fifth-source necessary inequality. For the actual true reply J_L after forcing L at (A1,...,A4), source5 IC, J_L's BR against X, and F_X-f_P(J_L)>=0 give u5>=U_P(L,X). The reply J_L is this actual-history reply, not any R6 from the generating source2 branch.

### Actual SAFE: 29 rows

At actual source j, any stored L_k is a common-catalog legal query. Its own prescribed true continuation gives at least l/(b_j+7-j), hence

    sum nu l/(b_j+7-j) <= u_j.

Use all six j for the four tails, and j=1,3,4,5,6 for Q. Membership is supplied by the generating new branch, while the payment history is the actual source's own history. No generating tail is frozen after a different deviation.

## 4. New genuine internal histories: 52 SAFE rows

The new branch's six memberships are

    ell'=(a1,q,r3,r4,r5,r6),  c'=sum ell'.

For i=3,...,6 let the true branch payoff be V'_i=sum nu r_i/c', zero if c'=0, and let b'_i=sum_{k<i}ell'_k. For every one of the thirteen query descriptors,

    sum nu query/(b'_i+7-i) - V'_i <=0.

Pure queries use their stored bits: old A_j remains a_j, X remains the single old x, Q uses q, and each R uses its same-index tail bit. Omean is obtained by averaging six actual legal Q_l deviations at this new history and weakening the menu count d to o, giving o/6.

Thus there are two different averages: nu already averages the OUTER source2 branches k; Omean averages the INNER six legal query indices l. They cannot be merged into an invented averaged action. Denominators depend on the true outer branch history and are independent of the inner query index.

## 5. New PAIR: 91 rows, with the valid inner30 mean/mean strengthening

The new true final two-player prefix is (A1,Q_k,R3_k,R4_k). Its denominator is

    D_new=1+a1+q+r3+r4,

and its genuine wallet is

    H_new=sum nu [r5/(D_new+r6)+r6/(D_new+r5)
                         +r5/(D_new(D_new+1))].

For a pure/pure query pair L,R use cost

    (l+r)/D_new - l*r/[D_new(D_new+1)].

For a pure/Omean pair use the six-inner-query weak cost

    l/D_new + o/(6D_new) - l*o/[6D_new(D_new+1)].

This includes Q/Omean with the stored q*o/6 overlap. Own Q/Q remains a repeated PURE query with q*q=q; it is not a menu/menu average. The new new-tail pairs use their literal same-index joint product, not a product of separate marginals.

For Omean/Omean use the stronger valid average over the 30 ordered INNER positions i!=j of the same six-query menu, at each fixed outer history. With actual menu multiplicity d,

    cost_30(d)=d/(3D)-d(d-1)/[30D(D+1)].

The overlap identity is literal: sum_{i!=j}q_i q_j=d(d-1). It remains true when two positions carry the same label; their pure PAIR(L,L) is legal. For 1<=d<=6,

    cost_30(d)-cost_30(1)
       =(d-1)[10(D+1)-d]/[30D(D+1)] >=0.

Therefore the paid weak union cost is exactly o/(3D_new). It does NOT subtract the full36 term o/[36D_new(D_new+1)]. The older full36 row remains valid but is weaker for this union purpose; it is not being called an error.

Every pure PAIR is paid by the source5 true IC, the true reply after that query comparing with the second query, the original new terminal comparing with the SAME true reply, and the nonnegative self-overlap difference. Averaging 30 such valid rows uses the same H_new. Then the outer average preserves validity. This gives 78 pure/pure, 12 pure/mean, and 1 mean/mean row, totaling 91.

## 6. Actual RC: the 55 new pairs

At the actual first-four history define D_actual=P+1. For any two legal queries L,R,

    f_P(L)+f_P(R)-g_P(L,R) <= u5+F_X.

Payment uses actual source5 IC for L, its actual-history true reply J_L comparing with R, and the common maximum F_X-f_P(J_L). J_L is not frozen to a source2 branch's R6. The common F_X is chosen for the actual P only and bounds the whole legal catalog.

For each new role L_k and each old pure role, average this RC over k. For two new roles L_k,R_k, use the SAME index k and their stored joint product. For new role/Omean, first average the INNER six legal queries, weaken their count to o, then use the outer k average. The cost is the section-5 pure/pure or pure/mean formula with D_actual, never D_new.

The 55 appended rows are new/new unordered/self pairs (15) and new/old pairs (40). No off-diagonal rule is applied to a new/new pair merely because both roles come from indexed families: that would require unknown cross-index joint information. The only 30-index rule is for the SIX ORIGINAL OPTIMAL QUERY LABELS against themselves.

The baseline actual RC(Omean,Omean) can independently use the same valid 30-pair strengthening, giving u5+F_X>=sum o/[3(P+1)]. It is an OLD/OLD row and is not counted in these 55. Main owns the baseline version; the future point release must identify the exact baseline input and certificate.

## 7. Known redundancy, retained raw identities, and omitted source2 SAFE(Q)

No row is claimed to be a new cone ray merely because its name is new. For each of the five pure new roles L,

    A_RC(L,X)-A_MX(L)=x/(P+1) at every state,
    b_RC(L,X)-b_MX(L)=F_X.

Thus with E_v=sum nu_v-z_v,

    slack_RC(L,X)-slack_MX(L)=-sum_v x_v/(P_v+1)*E_v.

The five MX rows are retained as explicit requested raw budgets, despite this equivalence modulo the mass equations. This identity must not be checked only at one numerical support.

There is also a literal global duplicate among the new-branch rows:

    A_NEW_PAIR(R5,R6)=A_NEW_SAFE5(R5)
                    =-r5*(1-r6)/[D_new(D_new+1)].

Both have zero right side. They remain distinct raw entries of the stipulated full SAFE/PAIR catalogue; the 243 count is not a claim of linear or conic independence.

Actual source2 SAFE(Q) is deliberately not an extra row:

    u2-sum nu q/(a1+5)
      = [u2-sum nu q/(a1+1+sum tails)]
        +sum nu q[1/(a1+1+sum tails)-1/(a1+5)] >=0.

The second coefficient is pointwise nonnegative since four tail bits sum to at most 4. The chosen catalogue therefore has 243 rather than 244 genuine rows. The own terminal new SAFE6(R6) zero row and any later fixed-point duplicates remain raw rows and will not be silently deleted.

## 8. Future fixed-point binding and universal cut contract

No point is bound in this package. The supplied release template has NULL source paths/hashes/values, NULL support, and NULL matrix fields. The next actual v4 point must be explicitly released by Main with its exact full256 atom identity, common-X membership, K, and input/primal certificate hashes. Neither the earlier root128 points nor any old global point may be substituted.

After such a release, only s actual positive old types are needed for the fixed layer because nu>=0 and each zero mass forces all its 32 columns to zero. Dimensions are exactly 32s columns, 243+2s raw inequalities and s mass equations. If this is not a small local LP, report the actual count to Main before building or solving; no arbitrary support restriction may be introduced.

If a future exact Farkas uses nonnegative weights lambda on the 243 genuine rows, let

    W_v(q,tails)=sum_R lambda_R A_R(v,q,tails),
    a_q(v)=min_{16 tail states} W_v(q,tails),
    m(v)=a0                              when o=0,
         min((5*a0+a1)/6,a1)            when o=1.

Compute this for ALL256 old types and ALL8192 states. Then

    sum_R lambda_R b_R(z,K)-sum_v m(v)z_v >=0

is the valid universal projected cut. The lower and upper moment multipliers extend as delta=max(a1-a0,0) and gamma=max(a0-a1,0); the mass multiplier is a0, with unrestricted sign. Its state residual is W_v+(gamma-delta)q-a0=W_v-a_q>=0. With E_v=sum nu_v-z_v and r_v=sum q*nu_v the unrestricted identity is

    sum_R lambda_R b_R - sum_v m(v)z_v
      = sum_R lambda_R(b_R-A_R nu)
        + sum_v delta_v(r_v-o_v*z_v/6)
        + sum_v gamma_v(o_v*z_v-r_v)
        + sum_{v,q,tails}(W_v-a_q(v))*nu[v,q,tails]
        + sum_v a0(v)*E_v.

Thus the sign of each moment row is explicit, including when a0 or a1 is negative. All omitted zero-support, o=0 and all-zero types must be restored here. No weighted cut, exact feasibility conclusion or Farkas is claimed before a real point and weights exist.

## 9. Concrete Main decisions at the next release

1. Supply the actual future v4 release with exact input/certificate hashes and the selected common X/K. The template remains unbound until then.
2. Confirm the baseline row version, particularly its already-owned old/old actual RC and PAIR mean/mean treatment. The selected new block is 243; a self-contained view that also repeats the 36 old actual RC pairs would have 279 genuine rows and must be an explicit different view, not a silent expansion.
3. Inspect the actual positive support count s and authorize the resulting fixed size/one-call phase-I scope before any optimizer. The source catalogue itself does not authorize solving.

All remaining implementation choices are fixed here: 243 true rows, no extra source2 Q SAFE, no extra duplicated tail root-size family, same-index new/new intersections, same actual P for MAX/MX/RC, and only the one new PAIR mean/mean row using inner30. Empty labels, aliases, repeated actions, zero clients and arbitrary weak ties remain allowed. Feasible averaged nu would still not certify individually realizable indexed branches, full optimal-label memberships, conditional alias identities or a complete SPE.
