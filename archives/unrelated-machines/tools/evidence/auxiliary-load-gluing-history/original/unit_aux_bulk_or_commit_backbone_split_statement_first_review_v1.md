# Unit-aux bulk OR-commit backbone split: independent statement-first review v1

Reviewer: general_query_response_review. Date: 2026-10-18.
Verdict: VALID. I find no fatal issue or standing objection in the entire supplied contract.

## 1. Exact reading scope and provenance

Before this reconstruction I read only the supplied new statement file:

/workspace/scratch/038d9dcc4cac/unit_aux_bulk_or_commit_backbone_split_statement_only_v1.md

SHA256: 7ebc7224661903bb08e17b907702caf1d12363f33b7e6efafc38e854cbfc9860.

I did not read an author Proof, root proof, other agent's new strategy, or related new fee/typed strategy. The statement itself attributes a common-capacity-flow direction to root; that visible attribution is part of the input. This is an independent proof after the stated contract, not a claim of blind originality of the general flow idea.

The argument below constructs the complete actual allocation, with all original job identities. It uses no supplied optimal allocation other than the explicitly promised r strict witnesses, no finite enumeration, and no software audit.

## 2. A forced strict-False occupancy bound

Fix a variable a in any complete actual load-at-most-one witness with its selector on A_(a,0). The unit selector already fills that pool, so none of the positive-block q jobs can be exported to it: each such export would have additional time 1/k>0.

Let S be the set of positive indices i for which some J job occupies C_(a,i). Every J job has time one there, so at most one J job can occupy each C, and |S| is exactly the number of J jobs on this variable's positive readouts. For i in S, the original b_(a,i) cannot remain on that C, which is already full. Its only alternative is its original M_(a,i), at time rho.

I claim |S|<=1. Suppose h<h' are two indices of S inside [k]. Since b_(a,h) occupies M_(a,h), q_(a,h) cannot use its own M: the two times would sum to 2rho>1. It cannot use A_(a,0), so it must execute on M_(a,h+1), at time one. Inductively, for h<i<h', the preceding q already fills M_(a,i), so q_(a,i) cannot execute there and cannot export to the full positive pool; it must execute on M_(a,i+1). In particular q_(a,h'-1) must occupy M_(a,h') at time one, contradicting b_(a,h') on the same machine at positive time rho. This is entirely within the positive block, so no circular-order or boundary assumption is hidden.

Thus every strict False branch has at most one J job at its positive readouts. In a strict True branch the trivial bound is k, since there are k readouts and each accepts at most one unit J job.

Applied to the given r witnesses, for each a:
\[
c_{a,j}\le1\quad(j\ne a),\qquad c_{a,a}\le k.
\]
Consequently
\[
0\le K_a\le k,\qquad
K_a=\left\lceil {1\over r}\sum_jc_{a,j}\right\rceil
 \le1+\left\lceil{k-1\over r}\right\rceil.
\tag{1}
\]
The upper bound K_a<=k follows separately because every c_(a,j)<=k. The proof counts every J job, including all guards and aux; its name or branch interpretation is irrelevant.

The assumption rho>1/2 is used exactly when excluding the initial q/b cohabitation on M_(a,h). No nonuniform auxiliary-time assumption has entered this backbone lemma.

## 3. Repack all J identities by an integral capacity flow

Let N=|J|. For an internal machine h define an integer job capacity
\[
u_h=\begin{cases}
N,&c_h=0,\\
\min\{N,\lfloor 1/c_h\rfloor\},&c_h>0.
\end{cases}
\tag{2}
\]
This includes c_h>1, for which u_h=0. For positive c_h, at most u_h J jobs imply real load at most one. For c_h=0, any subset of the N distinct jobs has real load zero. Truncating at N loses no actual assignment and avoids numerical capacity expansion.

Make a finite directed network:
- source to each individual original J-job vertex, capacity one;
- that job vertex to every original internal-machine vertex h on which it has a finite endpoint, capacity one;
- that job vertex to each original positive C-machine vertex on which it has a finite endpoint, capacity one;
- internal h to sink, capacity u_h;
- each positive C_(a,i) to a variable-quota vertex v_a, capacity one;
- v_a to sink, capacity K_a.

Edges exist only for original eligible job/machine pairs. No virtual output jobs or machines are proposed; the flow network is an algorithmic device.

The average of the r actual J assignments from the witnesses defines a rational feasible flow of value N:
- each J job sends 1/r along the destination used by each witness, giving total one;
- each positive C receives at most one J job in each witness, so its average is at most one;
- each internal h receives at most u_h J jobs in each witness, because all their times on h are the same c_h;
- the flow through v_a is the actual average (sum_j c_(a,j))/r, which is at most K_a by definition.

This averages identities, not anonymous demand. Every path chosen by any witness uses the same original job's actual finite endpoint. Jobs moved between branches or internal machines across witnesses cause no difficulty.

All capacities are integers. An augmenting-path algorithm starting from zero preserves integral flow. It can reach value N: if it terminated earlier, the vertices reachable from the source in the residual graph would determine a saturated cut of capacity equal to that smaller integral value, contradicting the displayed fractional flow of value N across the same cut. Deterministic breadth-first choice with fixed vertex ordering gives a deterministic construction. Since the total source capacity is N and every positive augmentation has integer value at least one, at most N augmentations are needed; no unit-capacity slot expansion is necessary.

At value N, each job sends exactly one integral unit to exactly one eligible machine. Place the original job at that machine. Each positive C has at most one J job; at most K_a of those C's belong to variable a. Internal load is at most one by (2). This assigns all original J jobs exactly once, including every auxiliary job, without deleting a guard or assuming that some auxiliary moves are free.

For N=0 the flow has value zero immediately, all K_a=0, and the later empty-occupancy backbone construction applies. Empty I is also harmless. Internal zero endpoints and unused c_h>1 endpoints are covered by (2).

## 4. Explicit actual backbone completion for an arbitrary selected C subset

It remains to show that the particular C destinations produced by the integral flow can always be accommodated by the original q/b/f jobs. I give a construction for each variable independently. Drop a from notation.

Let S={h_1<...<h_t} be the positive C indices receiving J jobs. We have 0<=t<=K_a<=k. Put f on its original A_0, so the target selector is False.

Place b_i as follows:
- if i in S, put positive b_i on its own M_i, at time rho;
- for every other positive i, put b_i on C_i, at time one;
- for every negative i>k, put b_i on C_i, at time one.

Thus every C already has exactly one unit J job or one unit b job. The construction uses no negative b's rho endpoint, but each negative b's original C endpoint is legal.

If t=0, place every q_i on its own M_i at time rho. Every M then holds exactly one q, and no q is exported. This completes this case.

If t>=1, assign q's as follows:
1. For 1<=i<h_1, put q_i on its own M_i.
2. For each j=1,...,t-1:
   - for h_j<=i<=h_(j+1)-2, put q_i on M_(i+1);
   - export q_(h_(j+1)-1) to its positive pool A_0.
   An empty interval is simply skipped. This covers consecutive selected indices correctly.
3. For h_t<=i<=k, put q_i on M_(i+1).
4. Export the negative q_(k+1) to A_1.
5. For k+2<=i<=2k, put q_i on its own M_i.

Every mentioned endpoint is one of that original q's three specified endpoints. In particular step 3 uses q_k's successor M_(k+1), and step 4 uses a genuine negative-block q with its A_1 endpoint. No wraparound edge is needed.

Every original q appears in exactly one of these lists. There are exactly t-1 positive q exports and one negative q export. The M-machine occupancy can be checked as a disjoint partition:
- M_1,...,M_(h_1-1) hold their own q's;
- each M_(h_j) holds b_(h_j);
- between successive h_j and h_(j+1), the intervening M's hold their predecessor q's;
- M_(h_t+1),...,M_(k+1) hold their predecessor q's;
- M_(k+2),...,M_(2k) hold their own q's.

Hence all 2k M machines hold exactly one original q or b. Its time is rho for an own q or positive b, and one for a successor q, so every such load is at most one.

The pools have exact loads:
\[
\operatorname{load}(A_0)=1+{t-1\over k},
\qquad
\operatorname{load}(A_1)={1\over k}
\quad(t\ge1).
\tag{3}
\]
For t=0 their loads are one and zero respectively. Thus in all cases positive-pool q count is max(0,t-1), and negative-pool load is at most 1/k. Since t<=K_a,
\[
\#\{\text{positive exported q}\}
=\max(0,t-1)\le\max(0,K_a-1).
\tag{4}
\]

There is no need to preserve the witnesses' q exports, b returns, or individual J locations. Only original finite eligibility is preserved, as requested.

## 5. Complete output identity and makespan bound

Combine the integral J placement with the independent backbone completions:
- every J job is assigned once by its own flow vertex, on an original eligible endpoint;
- every q, b, and f is assigned once by the explicit backbone lists;
- the backbone has no internal endpoints, and J has no M, pool, or negative C endpoints;
- occupied positive C's contain exactly one J and no b; all other C's contain exactly one b;
- every M contains exactly one q or b; internal load is at most one;
- all selectors execute on their original A_(a,0).

Thus this is a complete ordinary actual allocation of the same P, with no split jobs, omitted jobs, virtual output entities, or accidental overlap between subnetworks. All original machines, including unused internal machines and unused finite endpoints, remain part of the matrix.

The only possible load above one is a positive pool. By (3)-(4),
\[
C_{\max}(\tau)\le
1+{1\over k}\max_a\max(0,K_a-1)=B_{\rm data}.
\tag{5}
\]
From (1), and since ceil((k-1)/r)>=1 for k>=2 and r>=2,
\[
\max(0,K_a-1)\le\left\lceil{k-1\over r}\right\rceil.
\]
Therefore
\[
B_{\rm data}\le
1+{\lceil(k-1)/r\rceil\over k}.
\tag{6}
\]
As r>=2 and k is even,
\[
\left\lceil{k-1\over r}\right\rceil
\le\left\lceil{k-1\over2}\right\rceil={k\over2}.
\]
This proves the simultaneous makespan bound at most 3/2. For r=2 and even k, the final uniform expression in (6) is exactly 3/2; this is not a claim that every input attains that value, or that B_data is its conditional optimum.

## 6. Total bit complexity and quantitative input audit

Let N=|J|. The flow graph has O(N+|I|+rk+r) vertices and O(E_J+N+|I|+rk+r) edges. All capacities are nonnegative integers bounded by N except that a raw K_a may be as large as k, which has polynomial bit length anyway. An optional truncation of K_a to N does not change the feasible J assignments. No such truncation is needed for correctness or complexity.

The displayed fractional flow is only used to prove feasibility. The algorithm can compute the integers c_(a,j), K_a from the witness destination lists, build the integer network, and run integral augmentations without storing that fractional flow.

For a positive binary rational c_h=p/q, floor(1/c_h)=floor(q/p) is exact integer division; it is immediately truncated to N. Numerator and denominator encoding lengths, not their numeric values, determine the arithmetic cost. Zero c_h is detected before division. A huge denominator does not create slots or more flow augmentations.

All J identities and original endpoints are explicit. Witness validity and selector destinations can first be checked by exact rational load summation, in polynomial time in the complete matrix and r explicit assignments. The flow construction and the backbone lists are also polynomial in that input. The total r witness size is already charged as input; no unknown witnesses must be computed.

The statement's counts are correct: per variable, 4k+2 machines and 4k+1 jobs; q jobs contribute 6k finite entries, b jobs 4k, and the selector two, giving 10k+2. Adding I, J, and E_J yields exactly the stated m,n and finite-entry count. A dense mn input only increases the input length. Zero and unusable finite endpoints remain counted in that original matrix size.

Every internal-machine argument depends on its same c_h for all eligible J jobs. This is what converts load into an integer count capacity. Arbitrary heterogeneous times on one internal machine are not covered. Likewise the unit positive-C times, J's absence from M/pools/negative C, and original backbone endpoints are genuinely used assumptions.

## 7. Existential form, ordinary OPT, and remaining limits

If the r complete strict witnesses merely exist, choose such witnesses existentially and apply the same proof; then an all-False actual allocation exists with the uniform bound in (6). This does not produce or promise computation of those unknown witnesses. The data-dependent K_a are read from the provided witnesses in the algorithmic version.

For the unrestricted P, a selector always runs at a unit endpoint, so every complete actual allocation has makespan at least one. At least one given strict witness has makespan at most one, hence ordinary OPT(P)=1. The newly constructed allocation concerns a specified all-False selector readout. There is no source-NO or ordinary high-OPT conclusion.

All auxiliary identities have been retained. The proof never assumes guards stay on a fixed branch, that auxiliaries on other branches can be ignored, or that a part of the internal network can be deleted. It also does not assert a general UM solver, NP-hardness, exact conditional optimum, near-two obstruction, new software validation, global novelty, or failure of every possible OR-commit construction outside this explicit domain.

Final conclusion: all clauses of the supplied candidate, including the data-dependent B_data bound, are valid under exactly its stated input assumptions. No correction is requested. Author-Proof and canonical reading, if subsequently supplied, require separate immutable read-after records.
