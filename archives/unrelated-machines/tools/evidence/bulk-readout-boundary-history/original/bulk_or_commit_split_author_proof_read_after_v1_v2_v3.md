# Bulk OR-commit split v1/v2/v3 — actual author-Proof read-after

Reviewer: general_query_response_review. Date: 2026-10-18.
Verdict: VALID for each supplied version within its own stated domain. No fatal issue, standing objection, or requested mathematical correction.

## 1. Reading order and exact frozen files

This is a new post-Proof record. Before release of any author Proof, I froze these complete independent statement-first reconstructions:
- uniform-internal v1: b26bf9c4b75a74e00838216089fd5a1c507f3dc11a3d98bc47ab73492f260987;
- unrelated-internal/unit-readout v2: ab4b2c6bccadcb7a5f6925534ec8f40d3b21f49adeabeb49a5a1f71553698c44;
- unrelated-internal/heavy-readout v3: 69811afdcc491a360fc3a341e3915955f8b7534c92ac65c584e0d933d55f9b4b.

Only after the parent had actually read all those independent records and explicitly released the author sources, I actually read all three author Proofs in full. Hashes checked at reading time:
- unit_aux_bulk_or_commit_backbone_split_proof_v1.md:
  585218e87c4e109acd2d3e420a22a5c0bc000153c02b9f17b6520077c32c851f;
- unrelated_aux_bulk_or_commit_backbone_split_proof_v2.md:
  525b141344d2dd098e6d0d68cf21301a01ebde4a1c8b295b7ef77790fe079db5;
- unrelated_aux_heavy_readout_bulk_or_commit_split_proof_v3.md:
  0fb9dbe18248e46f8b319ebea531b0f519cc3d7ed89c5c69357bb0502be48aef.

All three are in /workspace/scratch/038d9dcc4cac. No source or earlier review was modified. No canonical text has yet been read for this task; that will need its own actual full-text scope record. No other new agent strategy was consulted.

The v3 statement source has no formal ID line. The parent's intended mature label is prospective metadata; I do not retroactively claim it is in the raw statement. v1/v2 remain immutable process sources rather than separately multiplied mature results.

## 2. Strict-False counting: different correct proofs

The author's three Proofs obtain the same strict-False positive-C J count as my independent records.

Their counting route is:
- every actual M holds at most one original q/b in a strict witness, since all such endpoint times are at least rho>1/2;
- when f is on the positive pool, no positive q can export there;
- the k positive q jobs and all returned positive b jobs must lie in the k positive M's, except that only q_k can leave this block, by its successor endpoint M_(k+1);
- hence k plus the positive-b-return count minus one is at most k, so at most one positive b returns;
- each J-occupied positive C forces its original b to return.

This is valid even if negative q/b jobs enter a positive M: such extra jobs only reduce available M capacity. It requires no special input ring orientation.

My independent proof instead took two occupied indices h<h' and propagated the q successor chain until it collided with the second returned b. Both proofs handle arbitrary positive-C locations and full actual witnesses. Neither assumes that the J jobs there are only named guards; all aux count.

For v1 and v2, unit J times give at most one J per strict C. For v3, two J times are each strictly greater than 1/2, so they still cannot share a strict C, while any positive J time conflicts with the unit b there. Thus the heavy-readout count and displacement reasoning is correct without changing the original times.

The authors derive the right respective quotas:
- v1: K_a<=1+ceil((k-1)/r), using all r one-True witnesses;
- v2/v3: K_u,K_v<=k/2+1 and every other K_a<=1, using only the two supplied different one-True modes.

## 3. Uniform-internal v1 Proof

The v1 integer network is correct. Each internal machine's J cardinality capacity is |J| if c_h=0, otherwise min(|J|,floor(1/c_h)); each positive C has count capacity one and each branch gate capacity K_a. Average actual destinations from all r complete witnesses give a fractional full flow. Integrality then assigns every original J identity once on an original eligible endpoint, with internal actual load at most one.

This argument genuinely depends on uniform times per internal machine, and the Proof does not claim that its load-one conclusion extends to heterogeneous I. Its zero, empty-J, and c_h>1 cases are correctly handled, with truncation and binary integer division rather than reciprocal expansion.

The authors' full backbone completion and the K bound give the data-dependent B_data conclusion and the uniform three-halves conclusion in the v1 statement. v1 is not being substituted for the changed v2/v3 internal contract.

## 4. Author fixed-same-end route versus my duplicate-occurrence route

The author's v2/v3 internal rounding proof first fixes every J job whose two witness destinations are identical. This is a legitimate preprocessing choice and is not made in my independently frozen route.

For an internal h, let F_h be the actual total load of all fixed jobs there. Those exact fixed identities occur there in both witnesses, so F_h<=1. Each remaining half-occurrence of value w at h coexists with all those fixed jobs in one strict witness. Therefore
\[
\sum_iw_i\le2(1-F_h),\qquad
w_i\le1-F_h.
\]
Consecutive nonincreasing pairs have at most one chosen job, so the selected residual load is at most
\[
O=w_1+w_3+\cdots
 \le(\sum_iw_i+w_1)/2.
\]
Adding fixed load yields
\[
F_h+O\le3/2-F_h/2\le3/2.
\]
This is correct for odd lists, empty lists, arbitrary heterogeneous endpoint values, and zero values. If F_h=1, all remaining values there can be zero and the proof still works. No time reciprocal or lower bound on positive I times is used.

The fixed-C treatment is also legal. A fixed J at a positive C is present there in both strict witnesses; no second J can use that C in either witness, by unit times in v2 or heavy times in v3. Removing that C for the residual flow therefore removes no residual witness destination. If d_a is the fixed positive-C J count in a branch, both original c counts include d_a. Thus K_a-d_a is nonnegative, and residual average branch occupancy is at most K_a-d_a. The proof does not allocate these fixed C jobs for free or count them twice.

Each residual job has two different witness machines, each retained with half mass. The global integer network enforces all internal pair slots, C count capacities, and residual branch gates simultaneously. Fixed jobs remain on their original common destination; every residual job chooses one of its own two original witness destinations. Thus the output-end restriction is exact.

By contrast, my independent v2/v3 reconstruction keeps both witness occurrences of every job, including duplicate occurrences at the same h, sorts that full list, and pairs it. Source-to-job capacity one prevents the repeated bookkeeping entries from duplicating the physical job. The full-list sum is at most two and its largest entry at most one, so my bound is directly
\[
\operatorname{load}_h\le
(p_1+p_3+\cdots)
\le(\sum p_i+p_1)/2\le3/2.
\]
My construction gives the required three-halves guarantee without isolating F_h. It need not give the author's finer 3/2-F_h/2 bound or the same chosen assignment. The two routes are different and both valid; no amendment of either earlier independent record is needed.

## 5. Correct heavy C behavior in v3

The v3 Proof preserves actual J readout times in (1/2,1]. Its C flow capacity is explicitly a count capacity, not an assumption of unit processing time. The half-witness flow is feasible there because each strict witness has at most one J at a C. After integral selection, a C with J has exactly that one original job at its original time, hence actual load at most one.

The same C cannot also contain its unit b, so backbone completion moves that b to the original M endpoint. A C without J gets its own unit b. Negative C has no J eligibility and always contains its original unit b. Hence the correct v3 conclusion is:
- every C has exactly one original job;
- positive C load is at most one and may be less than one;
- negative C load is exactly one.

The v3 Proof updates these conclusions in its construction and final global bound. It does not retain the erroneous unit-time statement from v2. The strict lower readout boundary 1/2 is genuinely needed for count capacity and is not silently included. The upper endpoint one is included. Unused finite values greater than one mentioned in v3's edge-case discussion concern I; the statement explicitly excludes such C endpoints.

## 6. Backbone comparison and full original-job audit

The authors use another valid complete backbone construction. For the selected positive-C subset F, put p=max F when nonempty. They return b_i to M_i for all i in F and put every other b, including all negative b, on its own C. They put f on A_0.

If F is empty, all q use their own M. If F is nonempty:
- positive q indexed by F except p export to A_0;
- positive q before p and outside F use their own M;
- positive q from p through k use their successor M;
- negative q from k+1 through 2k-1 use their successor M;
- negative q_(2k) exports to A_1.

Every q identity appears once. Before p, each M_i contains its own q or returned b_i; M_p contains b_p; from M_(p+1) through M_(2k), each machine receives its predecessor q. The last negative export avoids a wraparound collision at M_1. All these destinations are original finite endpoints, and every M holds exactly one original q/b of time rho or one.

The authors therefore export exactly |F|-1 positive q jobs and one negative q when F is nonempty; otherwise none. Their pool loads are the same as my independent construction.

My frozen reconstruction instead routes successive positive intervals, exports the positive q just before the next selected index, exports q_(k+1), and leaves subsequent negative q on their own M. This is a different legal route with the same count and load bounds. Both cover arbitrary F, including noncontiguous or consecutive indices, not merely a prefix or a single witness pattern.

All Proofs retain every original J, q, b, and f exactly once. The integer flow handles all shared J resources jointly. Backbone completion then only uses mutually separate variable rings/pools and the C slots left according to that global J result. J cannot use ring/pool/negative-C endpoints, and backbone cannot use I. Slots and gates are analysis nodes and are never actual output executions.

## 7. Quantifiers, global bounds, and binary complexity

The final simultaneous bounds match each Exact:
- v1: I<=1, C=1, M<=1, negative pool<=1/k, and positive pool bounded by its data K_a; hence whole output<=B_data<=1+ceil((k-1)/r)/k<=3/2;
- v2: I<=3/2, C=1, M<=1, and the two-mode K bounds give all pools<=3/2;
- v3: I<=3/2, C<=1 with negative C=1, M<=1, and the same two-mode pool bounds give whole output<=3/2.

The proofs do not assert arbitrary unrelated I<=1, or a smaller whole-output bound based solely on pools in v2/v3.

The algorithmic versions take the complete actual witnesses as input and restrict v2/v3 J outputs to the same job's two destinations. Existence-only premises yield only an existence statement; no unknown strict schedules are computed. Unrestricted OPT(P)=1 follows from a supplied strict witness and each f's unit endpoints. An all-False conditional allocation is not a high original optimum, source NO, or hardness gap.

Graph sizes, witness checking, rational sorting, partial sums, integer capacities, at most |J| augmentations, decoding, and actual-load verification are polynomial in the explicit complete matrix and the given witness lists. The v1 floor operation is truncated before numerical expansion; v2/v3 use no processing-time reciprocals at all. Zero/empty I or J, repeated stationary job destinations, zero internal times, and unused internal finite times above one are covered. Original count formulas and dense input size agree with the statements.

No additional mode is used in v2/v3. No numerical precision reciprocal or hidden padding is introduced. Auxiliary identity is never replaced by anonymous branch mass.

## 8. Verdict and remaining read-after boundary

The authors' three Proofs are mathematically consistent with the corresponding frozen statements and with my independent full reconstructions. Differences in strict-False proof style, fixed-job preprocessing, and backbone routing are legitimate proof choices. No standing fatal or nonfatal correction is requested.

This record certifies the supplied mathematical Proofs and their precise version domains. It does not certify any unread canonical page, software run, audit, global originality, new source hardness, near-two result, or general UM solver. v1/v2 process history is preserved; only the future final v3 is intended as a mature registered contract. A later canonical text must be actually read and certified in a separate scope artifact.
