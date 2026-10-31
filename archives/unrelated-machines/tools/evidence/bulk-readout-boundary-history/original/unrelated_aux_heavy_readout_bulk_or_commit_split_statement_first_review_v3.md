# Unrelated internal aux and heavy readouts — independent statement-first review v3

Reviewer: general_query_response_review. Date: 2026-10-18.
Verdict: VALID in the complete supplied v3 domain. No fatal or standing objection found.

## 1. Actual source reading and scope

I actually read only the new statement source

/workspace/scratch/038d9dcc4cac/unrelated_aux_heavy_readout_bulk_or_commit_split_statement_only_v3.md

SHA256: bf2c908ed53faafb3f8c725eea36b5e2480ac4ac2fc9b7fd8bae3173d9191849.

I have not read any author v1/v2/v3 Proof, root proof, or other agent's new fee/typed strategy. This independent reconstruction follows the exact v3 statement and my prior frozen independent v1/v2 work. Those prior artifacts remain unchanged. The source identifies root and the author as common developers; no blind-originality assertion is made here. The statement file has no formal ID line, and this review does not pretend that a later proposed mature ID was present in its frozen bytes.

This v3 is the prospective single mature contract. The v1 and v2 records are distinct process history, not extra mature results. In particular:
- v3 internal I remains arbitrarily unrelated, with output bound 3/2, not one;
- two distinct one-True complete witnesses are input;
- all finite J readout times are in the open-closed interval (1/2,1], and may differ by job on the same C;
- output C machines contain one original job, but their actual load need only be at most one. A C holding a J job is not asserted to have load exactly one.

The proof below includes every original q/b/f/J identity, all original machines, arbitrary zero internal endpoints, and the data-dependent K_a quotas.

## 2. Why heavy readouts still give count capacities and displacement

Consider any strict actual witness, with all original machine loads at most one.

First, a positive C cannot hold two J jobs: the sum of their two original times is strictly greater than one, since each finite J endpoint there is strictly greater than 1/2. Thus the number of J jobs on any positive C is at most one even though their actual times are nonuniform.

Second, if C_(a,i) holds a J job, the corresponding original b_(a,i) cannot also execute on that C. The b time is one and the J time is positive, so their total exceeds one. For a positive i<=k, b's only other endpoint is its own M_(a,i), at time rho.

These facts are about original processing times. Replacing a C by an integer count-capacity-one vertex in the rounding network is a proof device, not a modification of J's original times.

The strict lower endpoint 1/2 is used in the first fact. At equality 1/2, two J jobs could share a strict C, and the count-capacity/branch-count argument would require a different contract. This review does not include that boundary. The upper endpoint one is included and makes every singly assigned output J legal with C load at most one.

## 3. A strict False branch has at most one J on its positive C block

Fix a branch a with f_a on its actual A_(a,0) endpoint in a strict witness. The selector has unit time there, so no positive q_(a,i), i<=k, can export to A_(a,0): each has positive export time 1/k.

Suppose the positive C's occupied by J include indices h<h'. The displacement fact forces b_(a,h) onto M_(a,h), at time rho. Then q_(a,h) cannot execute on its own M: the two times would sum to 2rho>1. It cannot export to its full positive pool, so it must execute on its successor M_(a,h+1), at time one.

Inductively through the positive block, q_(a,h+1),...,q_(a,h'-1) must also execute on their respective successor M's, since each own M is already filled by the preceding successor q and the positive pool remains unavailable. Therefore q_(a,h'-1) occupies M_(a,h') at time one. But J at C_(a,h') has displaced b_(a,h') onto that same M at positive time rho, a contradiction.

Thus there is at most one occupied positive C, and Section 2 shows that it holds at most one J job. This proves the count bound c_a<=1 in every strict False branch, regardless of auxiliary names, other exports/returns, or any unstated ring orientation.

For the two input witnesses:
\[
c_u^u,c_v^v\le k,\quad c_u^v,c_v^u\le1,
\qquad c_a^u,c_a^v\le1\quad(a\notin\{u,v\}).
\]
The bounds by k use the per-C at-most-one fact. Hence, because k is even,
\[
K_u,K_v\le\left\lceil{k+1\over2}\right\rceil=k/2+1,
\qquad K_a\le1\quad(a\notin\{u,v\}).
\tag{1}
\]
Also 0<=K_a<=k for all a. Every c here counts all original J identities, including aux placed on a False branch; none is discarded as a supposedly free guard or auxiliary.

## 4. Pair the two witness occurrences at each internal machine

For each internal h, list one occurrence (z,t) whenever sigma^t(z)=h for t in {u,v}. Keep both occurrences if the same original job goes to h in both witnesses. Such occurrences are bookkeeping, not new physical tasks.

Sort their actual original values in nonincreasing order
\[
p_1\ge p_2\ge\cdots\ge p_d\ge0.
\]
Use a deterministic job/mode tie order. Pair consecutive occurrences (1,2), (3,4), and so forth; an odd final occurrence is a singleton pair. These pairs will be matching slots only.

The two actual strict witnesses imply
\[
L_h:=\sum_{\ell=1}^d p_\ell
=\operatorname{load}_{\sigma^u}(h)+
  \operatorname{load}_{\sigma^v}(h)\le2,
\qquad p_1\le1
\tag{2}
\]
when d>0. Internal machines have no backbone jobs, so these sums account for their entire actual loads. Empty lists have output load zero.

If at most one original job is selected through each pair, its actual h load is at most the sum O of the odd-indexed p's. With E the sum of the even-indexed p's, monotonicity gives O-E<=p_1: after the first entry, group terms as -(p_2-p_3), -(p_4-p_5), etc., and for even d include the final negative term. Therefore
\[
O\le(L_h+p_1)/2\le3/2.
\tag{3}
\]
This includes odd lists, zero times, and arbitrary same-machine unrelated values. A job selected through a pair has its original time bounded by that pair's largest value. If the same original job occurs in two different pairs, the global job constraint below still selects it only once.

No processing-time reciprocal, uniform-time hypothesis, or separation between tiny and medium tasks is used.

## 5. One integer flow rounds all identities and quotas together

Let N=|J|. Make a finite integer-capacity network:
- source to each original job z: capacity one;
- job z to each internal pair-slot containing one of its witness occurrences: capacity one;
- job z to each positive C that equals one of its two actual witness destinations: capacity one;
- each internal pair-slot to sink: capacity one;
- each positive C_(a,i) to its branch vertex v_a: capacity one;
- v_a to sink: capacity K_a.

Parallel copies of the same job-to-slot or job-to-C edge may be merged into one capacity-one edge. A slot is labelled with its original internal machine. No other possible destination is introduced.

Send half a unit from each job along the route of its sigma^u occurrence and half along its sigma^v occurrence. This is a feasible fractional flow of value N:
- each slot contains at most two half-unit occurrences;
- by the strict heavy-readout count fact, each C receives at most one unit across the two half-weighted witnesses;
- branch a receives exactly (c_a^u+c_a^v)/2<=K_a;
- each job sends total one, even if both routes coincide.

All capacities are integers. Start from zero and augment along a deterministic residual path until no augmenting path remains. If the integral value were below N, the residual source-reachable cut would have capacity equal to that smaller value, contradicting the fractional flow of value N across the same cut. Thus integral value N is reached. There are at most N positive integral augmentations, because total source capacity is N.

Each original job now sends one unit to exactly one outgoing choice:
- through a slot it is assigned to that slot's original h;
- through a C vertex it is assigned to that actual C.

Its output destination is in {sigma^u(z),sigma^v(z)}. It remains the same original job with the same original time. Every C receives at most one J job, and each branch receives at most K_a. Since each slot has at most one selected job, (3) bounds every original I machine by 3/2.

The flow graph explicitly couples all jobs across all shared internal machines and branches. It assumes neither branchwise isolated aux nor a free reassignment for any named guard. It never splits one physical job: the half-unit construction only certifies feasibility of the integer network, and the output uses its integral unit.

At C, one selected J uses its original nonuniform time in (1/2,1], so its actual C load is at most one. The algorithm does not replace that time by one.

## 6. Complete original backbone for every rounded positive-C pattern

For each variable a independently, let S={h_1<...<h_t} be exactly the positive C indices receiving J after the flow. Here t<=K_a<=k. Suppress a in the formulas.

Set f to its original A_0, giving the required actual False selector readout. Place:
- b_i on its own M_i for i in S;
- every other positive b_i on its own C_i;
- every negative b_i on its own C_i.

Thus every positive C holds exactly one original J or unit b, with actual load at most one. Every negative C holds its original unit b, with load exactly one.

If t=0, put every q_i on its own M_i, at time rho. There are no exports.

If t>=1:
- for i<h_1, put q_i on its own M_i;
- for each j<t, put q_i on M_(i+1) for h_j<=i<=h_(j+1)-2, and export q_(h_(j+1)-1) to A_0;
- for h_t<=i<=k, put q_i on M_(i+1);
- export q_(k+1) to A_1;
- for k+2<=i<=2k, put q_i on its own M_i.

Empty intervals are ignored. All these endpoints are original: q_k has successor M_(k+1), and q_(k+1) is a negative-block job with its original A_1 endpoint. No wraparound routing is needed.

The q lists are disjoint and exhaustive. The M-machine partition is:
- own q's before h_1;
- b_(h_j) at each selected h_j;
- predecessor q's strictly between selected indices;
- predecessor q's from h_t+1 through k+1;
- own q's from k+2 through 2k.

Hence every M holds exactly one original q or b, with time rho or one. In particular all M loads are at most one, including adjacent selected indices and t=k.

For t>=1 the q export counts are exactly t-1 positive and one negative. For t=0 they are zero and zero. Therefore
\[
\operatorname{load}(A_1)\le1/k,\qquad
\#\{\text{positive exported q}\}
=\max(0,t-1)\le\max(0,K_a-1),
\]
\[
\operatorname{load}(A_0)
=1+\max(0,t-1)/k
\le1+\max(0,K_a-1)/k.
\tag{4}
\]

This completion depends only on the rounded occupied C subset. It does not preserve, assume, or need any particular original witness q pattern, b return, or ring direction.

## 7. Simultaneous all-job schedule and global bound

Take the J assignment from Section 5 and all backbone assignments from Section 6. Every original identity executes exactly once:
- all J by their individual integral source units;
- all b by the explicit S/C distinction;
- all q by the exhaustive disjoint lists;
- all f at their own A_0.

J has no M/pool/negative-C endpoints, while backbone jobs have no I endpoints. Thus their combination has no unintended overlaps. Each positive C contains exactly one original J or b, negative C its own unit b, every M one q or b, every internal load at most 3/2, and every selector is actually False.

From (1) and (4), a branch outside {u,v} has no positive q export because K_a<=1. At u and v, max(0,K_a-1)<=k/2. Therefore all positive pools have actual load at most 3/2. Negative pools have load at most 1/k<=1/2; C and M have loads at most one. All original machines simultaneously satisfy C_max<=3/2.

C's containing J need not have load one and are not asserted to. Internal I is bounded by 3/2 and not by one. The entire schedule is not claimed to obey a smaller pool-only data bound when the internal rounding bound dominates.

## 8. Complexity and all zero/empty/unused cases

There are two witness destination occurrences per J job, so at most 2N internal occurrences and at most 2N witness C occurrences. There are at most 2N pair-slots and at most two job-choice edges per original job after merging duplicates. Together with the rk original positive C vertices, r branch vertices, N job vertices, and source/sink, the auxiliary flow graph has polynomial size in the explicit matrix and two complete assignments.

Sorting uses exact rational comparison and fixed identity ties. Capacities are integer one or K_a<=k. The flow uses at most N integral augmentations and ordinary residual arithmetic. No time reciprocals, rational-denominator enumeration, rho-precision reciprocals, or implicit padding occurs. Decoding is linear in the produced job assignment. Slots are discarded as an algorithmic device; only original machine names are output.

The complete strict witnesses can first be verified by exact rational load sums, finite-endpoint checks, selector modes, and one occurrence of every original job. This costs polynomial total bit time in the given input. The method never computes unknown modes or calls a general UM solver.

Empty J gives empty flow, K_a=0, no exports, and the all-own-q/all-C-b completion. Empty I leaves the C/quota portion, which remains fractionally feasible by the supplied witnesses. Internal zero endpoints sort and pair with value zero; their jobs still each receive one actual assignment. Empty/all-zero internal lists have zero output load. Unused internal finite values above one remain in P but cannot be a used strict witness destination and thus cannot be selected by this witness-end-restricted output.

All finite J readout endpoints, including unused ones, are assumed in (1/2,1] exactly as stated. This review does not add endpoints at or below 1/2 or above one. The strict lower boundary is not replaced by a closed boundary. Zero readout time is excluded; zero internal time is allowed.

The stated matrix counts are correct: per variable 4k+2 machines, 4k+1 jobs, 6k q finite entries, 4k b entries, and two selector entries. Adding |I|, |J|, E_J gives exactly the specified m,n, finite count, and dense mn encoding. Unused finite entries remain part of input size and do not disappear from the original object.

## 9. Existential form, ordinary optimum, and limits

If only the two distinct complete strict one-True modes are assumed to exist, choose them existentially and apply the construction as an existence proof. It yields conditional OPT(P|all False)<=3/2 but does not compute unknown witnesses. With supplied witnesses, the algorithm is deterministic total-bit-polynomial as shown.

Unrestricted OPT(P)=1: every selector has only original unit endpoints, so every complete actual allocation has peak at least one; either supplied complete strict witness achieves peak at most one. This does not become a source NO or high ordinary-optimum statement. The conclusion concerns the specified actual all-False selector readout.

The proof crucially retains every auxiliary/guard/demand job, uses the exact original backbone, unit b C times, heavy J C times in the stated range, J's absence from negative C/M/pools, rho>1/2, and two different one-True complete modes. It does not certify arbitrary nonunit readouts outside the heavy interval or arbitrary modified backbones.

No software, finite enumeration, general UM novelty, NP-hardness, near-two source obstruction, external review, or global originality is claimed. Formal v3 certification is limited to the supplied statement and the proof above; prior v1/v2 raw sources retain their own historical scope.

Final status: all clauses of the complete v3 contract are valid, with C target correctly weakened from equality one to at most one. No correction is requested. Any subsequently released author Proof or final canonical needs a separate read-after record.
