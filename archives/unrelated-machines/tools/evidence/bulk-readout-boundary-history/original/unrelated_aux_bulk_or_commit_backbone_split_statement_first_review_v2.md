# Unrelated-aux bulk OR-commit split — independent statement-first review v2

Reviewer: general_query_response_review. Date: 2026-10-18.
Verdict: VALID. The full v2 contract follows by the explicit construction below. No fatal issue or standing objection found.

## 1. Source, reading order, and changed domain

The only newly read source is

/workspace/scratch/038d9dcc4cac/unrelated_aux_bulk_or_commit_backbone_split_statement_only_v2.md

SHA256: aca76d26e2536e770143076b0c09df909a86e7f3422ac8b67189168b3427fa64.

I read its entire statement before deriving this review. No v1/v2 author Proof, root proof, or other agent's new fee/typed strategy has been read or requested. The source itself describes root and the author as common developers; I make no blind-originality claim for that background. My prior independently frozen v1 review is SHA256 b26bf9c4b75a74e00838216089fd5a1c507f3dc11a3d98bc47ab73492f260987 and remains unchanged.

The v1 internal count-capacity proof does not cover v2: on an internal machine, job times now differ. Here I replace it with an explicit paired-occurrence rounding proof. The internal output bound is 3/2, not one. Only two specified different one-True witnesses are needed, and every output J destination is restricted to the same job's two actual witness destinations.

## 2. Strict False forces at most one positive readout J job

Fix a variable a in any complete actual witness of makespan at most one with f_a on A_(a,0). Its unit selector fills the positive pool, so no positive q_(a,i), i<=k, can export to that pool: its export time 1/k is strictly positive.

Every positive C can host at most one J job, since each such job has time one there. If J occupies C_(a,h), the positive b_(a,h), whose only endpoints are that C and its own M, must execute on M_(a,h) at time rho.

Suppose J occupies two positive readouts with indices h<h'. Then q_(a,h) cannot use its own M because b there would give load 2rho>1; it cannot use the full positive pool. It must therefore use its successor M_(a,h+1), at time one. Propagating through the positive block, each subsequent q through q_(a,h'-1) must also use its successor. The latter lands on M_(a,h'), already occupied by b_(a,h') at positive time rho, a contradiction. Thus the strict False branch has at most one J job at its positive readouts.

This uses all J jobs, not only named guards, and allows arbitrary exports/returns elsewhere in the input witness. It does not require a global ring orientation. The only lower-bound use of rho>1/2 is exclusion of the initial own-M q/b pair.

For the supplied two modes, each branch outside {u,v} is False in both, whereas u and v are True in only their own witness. Therefore
\[
c_u^u,c_v^v\le k,\quad
c_u^v,c_v^u\le1,\quad
c_a^u,c_a^v\le1\ (a\notin\{u,v\}).
\]
With k even,
\[
K_u,K_v\le\left\lceil{k+1\over2}\right\rceil
={k\over2}+1,\qquad
K_a\le1\ (a\notin\{u,v\}).
\tag{1}
\]
Also every K_a is between zero and k, since both individual counts are at most k.

## 3. A paired-list inequality for arbitrary unrelated times

For an internal machine h, form a list of occurrences, not just distinct jobs:

- for every z with sigma^u(z)=h, include one occurrence (z,u) with value p_(h,z);
- for every z with sigma^v(z)=h, include one occurrence (z,v) with the same original endpoint value.

If both witnesses put the same original job on h, its two occurrences are both retained. They are not new physical jobs. Let the list's length be d_h, and sort its values in nonincreasing order
\[
p_1\ge p_2\ge\cdots\ge p_{d_h}\ge0,
\]
with a deterministic identity/mode tie order. Pair consecutive occurrences (1,2), (3,4), and so on, keeping a singleton last pair if the list is odd. Call these pairs slots only as an algorithmic matching device.

Two elementary bounds follow from the strict actual witnesses:
\[
\sum_{\ell=1}^{d_h}p_\ell
=\operatorname{load}_{\sigma^u}(h)+\operatorname{load}_{\sigma^v}(h)\le2,
\qquad p_1\le1
\tag{2}
\]
for a nonempty list. These statements include zeros and arbitrary same-machine heterogeneity. A finite endpoint greater than one cannot be a destination in either strict witness, so it does not appear in this list.

If an output selects at most one occurrence-job from each pair, its real h load is at most
\[
p_1+p_3+p_5+\cdots
\le {1\over2}\left(\sum_{\ell=1}^{d_h}p_\ell+p_1\right)\le {3\over2}.
\tag{3}
\]
For completeness, put O=sum of odd-indexed p's and E=sum of even-indexed p's. Monotonicity gives
\[
O-E=p_1-(p_2-p_3)-(p_4-p_5)-\cdots
\]
with an additional nonpositive last term when d_h is even. Hence O-E<=p_1 and O<=(O+E+p_1)/2. Thus (3) is exact, including an odd singleton. If the list is empty, output load is zero; if all entries are zero, both sides of the load bound are zero.

No assumption of uniform processing time, a tiny/medium bound, a lower bound on positive times, or division by a processing time is used.

## 4. One integral flow enforces all pair, C, and branch quotas

Let N=|J|. Build a directed integer-capacity network:

- source to each individual original job z in J: capacity one;
- for each of z's two witness occurrences at an internal machine, job z to the slot containing that occurrence: capacity one;
- for each of z's witness destinations that is a positive C, job z to that original C vertex: capacity one;
- each internal slot to sink: capacity one;
- each positive C_(a,i) to a branch vertex v_a: capacity one;
- each v_a to sink: capacity K_a.

If the same job has two identical job-to-slot or job-to-C edges, they may be merged into one capacity-one edge. The fractional construction below then combines their two half-units. All slots are attached to a specific original h. Every job-to-slot edge is justified by that same job actually being placed on h in at least one witness.

There is a fractional flow of value N: give each original job half a unit along its sigma^u route and half along its sigma^v route.

An internal slot contains at most two occurrences, so receives at most one total unit. A positive C receives half its number of witness J occurrences, at most one because each strict witness puts at most one unit J job there. Branch a receives
\[
(c_a^u+c_a^v)/2\le K_a.
\]
Each job sends total one. Repeated occurrences of one fixed job cause no problem: if paired together, that job can send its total one to the same slot; if separated, it sends a half to each slot. Shared internal machines, cross-branch jobs, guards, and auxiliaries are all handled in the same graph.

All capacities are integers. Starting from zero and repeatedly taking a deterministically chosen residual augmenting path produces integral flows. It must reach value N, since otherwise a final residual source-reachable cut would have capacity smaller than N, contradicting the displayed fractional flow across that cut. Source capacity is N; every augmentation has positive integral value, so at most N augmentations are required. This supplies a direct deterministic polynomial construction without an appeal to an unspecified rounding oracle.

At value N, each original job chooses exactly one outgoing edge. Assign it to the original internal machine associated with that slot, or to the chosen original C. Then:

1. its destination belongs to {sigma^u(z),sigma^v(z)} and is an original finite endpoint;
2. each slot selects at most one original job, so (3) bounds every internal machine load by 3/2;
3. each positive C hosts at most one J job;
4. branch a hosts at most K_a J jobs on its positive C's.

Although a job may have two occurrences, the source edge allows it only one integral unit, so no job is duplicated. Different slots might contain occurrences of the same job, but the integral flow can assign that job only once. A selected job's actual time on h equals its occurrence value, and is at most the maximum value of its chosen slot; thus the real-load deduction from (3) is valid.

The slots are never output as machines or jobs. Decoding returns only the original job-to-original-machine assignment.

## 5. Complete backbone for the resulting C occupancy

Fix variable a and suppress its label. Let
\[
S=\{h_1<\cdots<h_t\}\subseteq[k]
\]
be exactly the positive C indices receiving J jobs after the preceding flow. Then t<=K_a<=k.

Put f on A_0. Put b_i on its own M_i for i in S; every other positive b_i goes to C_i; every negative b_i also goes to C_i. These are all original endpoints. Consequently each C contains exactly one unit J job or one unit b job.

If t=0, put every q_i on its own M_i. All M's contain exactly one q of time rho, the positive pool contains only f, and the negative pool is empty.

For t>=1, make the following explicit q assignment:
- for i<h_1, q_i goes to its own M_i;
- for each j<t, q_i goes to M_(i+1) for h_j<=i<=h_(j+1)-2, while q_(h_(j+1)-1) is exported to A_0;
- for h_t<=i<=k, q_i goes to M_(i+1);
- q_(k+1) is exported to A_1;
- for k+2<=i<=2k, q_i goes to its own M_i.

An empty interval contributes no assignments. In particular consecutive selected indices are allowed: the q at the earlier selected index is then precisely the positive exported q preceding the next selected M.

These lists cover all q identities exactly once. The M-machine partition is explicit:
- before h_1, own q's;
- at each h_j, the selected b_(h_j);
- between h_j and h_(j+1), predecessor q's;
- after h_t through k+1, predecessor q's;
- from k+2 through 2k, own q's.

Thus every M holds exactly one q or b, of actual time rho or one. The successor q_k uses its genuine M_(k+1) endpoint, and the exported q_(k+1) is genuinely in the negative block. No cycle closure, additional endpoint, or padding job is introduced.

There are exactly t-1 positive exports and one negative export for t>=1, and no exports for t=0. Hence every negative pool has load at most 1/k, while
\[
\#\text{ positive exported q's}
=\max(0,t-1)\le\max(0,K_a-1),
\]
\[
\operatorname{load}(A_0)
=1+{\max(0,t-1)\over k}
\le1+{\max(0,K_a-1)\over k}.
\tag{4}
\]
The formula includes t=0 correctly.

## 6. Simultaneous actual bound and all-job audit

Combine the J allocation with these variablewise backbone assignments. All original jobs are present:
- every J identity is assigned once by its one integral source unit;
- every b is assigned once, on its own allowed C or its positive allowed M;
- every q is assigned once by the displayed lists;
- every f is on its original A_(a,0).

J has no M/pool/negative-C endpoint, and backbone jobs have no I endpoint. Thus the simultaneous assembly creates no cross-part collision. Every positive C contains exactly one J or b, every negative C exactly one b, and every M exactly one q or b. The internal shared J workload has already been bounded globally by the same flow; it is not separately budgeted per branch.

By (1) and (4), branches outside {u,v} have no positive export and their positive pools have load one. At u and v,
\[
\max(0,K_a-1)\le k/2,
\]
so their positive-pool loads are at most 3/2. Negative pools are at most 1/k<=1/2. Internal I is at most 3/2 by (3), C is exactly one, and M is at most one. Thus all original machines simultaneously satisfy
\[
C_{\max}(\tau)\le3/2.
\]

This does not assert that the whole output is bounded by the v1 quantity B_data: even when all pool bounds are lower, unrelated internal machines here are only proved at most 3/2. Nor does it assert internal load at most one.

All f's read False by their actual original destinations. No auxiliary state labels, virtual executions, duplicate jobs, removed jobs, or free branch relocation is used.

## 7. Input counts, zero and empty cases, and total bit complexity

The original counts are unchanged and correct: each variable contributes 4k+2 machines, 4k+1 jobs, and 10k+2 finite entries (6k from q, 4k from b, two from f). Adding the internal machine set, J identities, and E_J gives the statement's counts and dense mn size.

There are exactly two occurrences per J job across the two actual destinations, so at most 2N internal occurrences and at most 2N witness J-to-C occurrences. There are at most 2N internal slots, and at most two distinct choice edges out of each job, after merging parallel duplicates. Together with the rk explicit C vertices and r branch vertices, the flow graph has polynomial size in the full explicit input. Unused original machines and unused finite entries remain in P even though they need no flow-choice edge.

Occurrence sorting uses exact comparison of the original nonnegative rational times and deterministic identity ties. Its bit cost is polynomial in their binary encodings. Capacities are one or K_a, and K_a is an integer at most k; all sums and ceiling calculations use the supplied assignment destination lists. The integral network has at most N positive augmentations and uses ordinary integer residual arithmetic. No capacity is floor(1/p), and there is no denominator, inverse tiny-time, inverse-rho-precision, or implicit-padding expansion.

The two complete witnesses can be verified first by checking each job once, its finite eligibility, its original selector destination, and every exact rational machine load. This is polynomial in the given matrix and two explicit witness lists. The algorithm never seeks unknown witnesses or an optimal allocation.

If J is empty, the flow and all occurrence lists are empty, all K_a=0, and the no-export backbone case gives the complete all-False schedule. If I is empty, the C/quota portion of the fractional flow is still feasible by the two supplied witnesses, and the same integer proof applies. Internal zero times can be sorted and paired normally, with actual load zero and no division. An unused finite time greater than one remains a legal original matrix entry but cannot be a used endpoint in a strict witness, so it cannot be chosen by this witness-end-restricted output. All-zero and empty internal lists likewise pose no issue.

## 8. Existential version, ordinary OPT, and exact scope

If two distinct one-True complete strict modes merely exist, choose them existentially, run the mathematical construction, and obtain the stated all-False existence bound. This yields conditional OPT(P|all False)<=3/2 but no algorithm for finding the unknown input modes.

Unrestricted OPT(P)=1: each original selector has only unit endpoints, so every actual allocation has peak at least one, and either strict witness gives a complete peak-at-most-one allocation. This result is about a specified all-False actual selector readout, not a source NO or large ordinary optimum.

The proof genuinely uses unit J times on positive C, J's absence from negative C/ring/pool, the exact backbone endpoints, rho>1/2, and two complete distinct one-True modes. It permits arbitrary unrelated internal times and all auxiliary identities. It does not assume branchwise auxiliary isolation, unchanged guard locations, a unique ring direction, or special witness exports.

This review supplies no software execution, finite-enumeration evidence, new general UM solver, source hardness, near-two obstruction, external review, or global novelty claim. Only the stated complete v2 contract is certified. The v1 record remains a different, stronger-internal-bound contract under its own uniform-time and r-witness premises.

Final status: v2 is valid in full. No correction is requested. Any later author Proof or canonical reading must be recorded separately without modifying this statement-first artifact.
