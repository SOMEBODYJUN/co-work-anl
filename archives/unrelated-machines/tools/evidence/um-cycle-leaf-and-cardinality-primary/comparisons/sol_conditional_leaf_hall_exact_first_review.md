# Conditional leaf Hall v2: independent Exact-first reconstruction

Reviewer: /root/sol_literal_budget_attack, 2026-10-18.

Verdict: PASS for the stated relaxation, family, and projection theorem, with the designated-partition precondition exactly as written. I found no fatal counterexample. This is a reconstruction, not a vote or a review of the author's proof.

## Identity and actual read boundary

The sole candidate input actually read was the complete file
/workspace/scratch/038d9dcc4cac/sol_general_repair_conditional_hall_exact_v2.md,
SHA-256 828c6a178729bf4ce03855ef8e1f53d9efaf85fb9aaa680a6cd4c5a0e012bb4f.
I checked the whole-file hash and read its entire header and §§1–8, in one untruncated 3114-token tool result, before deriving the arguments below.

I did not read this candidate's author proof, author checker, sol_nsw draft, or other candidate messages. My own code below imports no author file. The later primary-source side reply to global_certificate concerned only the already authorized Bamas paper, not this candidate. This record is frozen before any author-proof release.

## 1. Full ordinary matrix: exact value identity

Every state has coefficient sum one. Therefore all its incidence jobs, including any explicitly listed zeros, have total tail processing time one at that indexed state's private root. Selectors are original unit jobs. Each resource assignment of an incidence costs exactly one, independently of its coefficient.

Given pairwise-disjoint bundles with minimum value v, choose one maximizing indexed state for each group. Put its selector at that state root, and export exactly the positive incidence jobs of that chosen state whose resources are in its bundle. Keep every other incidence job at its own original private root, including all jobs of unselected states and all zeros. Each selected root has load at most 2-v, each unselected root has load one, and each resource has load at most one. Since 0<=v<=1, the makespan is at most 2-v.

Conversely, take any complete schedule of makespan T<2. Each resource receives at most one incidence job because each costs one there. For each group g, inspect the indexed state s whose root receives its unit selector. The root load is

\[
 1+\sum_{\text{incidences retained at }M_{gs}}p_{gsu}
 =2-\sum_{\text{incidences exported from }M_{gs}}p_{gsu}.
\]

The resource sets exported from these selected roots are pairwise disjoint; their selected-state values are at least 2-T. Thus V(Q)>=2-T. If T>=2 the lower bound T>=2-V(Q) is immediate. Taking optima gives OPT(P(Q))=2-V(Q). Finite bundles and indexed states attain the menu optimum. No original job is removed by this argument.

## 2. Exact automatic threshold classification

For fixed epsilon, if B meets H_g, one of its resources has coefficient at least epsilon in some state, so v_g(B)>=epsilon. If B avoids H_g, every state values it by at most b_g<epsilon. Conversely, if b_g>=epsilon, the entire set U\H_g itself is a witness with value at least epsilon and no intersection with H_g. Thus the strict b_g<epsilon test is precisely the advertised threshold-unit-demand test; equality belongs in C.

The test only requires maxima, rational sums, and comparisons over the explicit data. Every singleton-unit menu is in L. For the family, at epsilon=1 the M group has H empty and b=1. Each H group has its home resource in H but its parking state has all value one outside H, so b=1 and it stays in C. Whenever t>1/epsilon, both 1/t and 1/D are below epsilon, giving the same conclusion. Port transfer preserves these tests because each original group's positive coefficient coordinates are transferred injectively to its own group ports.

## 3. Necessity and size of the relaxation

Suppose disjoint bundles have value at least epsilon. For each core choose one witnessing state, set its lambda to one, and set z to one on its positive allocated coordinates and zero elsewhere. All other core-state lambda,z are zero. Every leaf has an allocated resource in its H neighborhood by §2; choose one for each leaf. These choices give one integral matching of all leaves, disjoint from every used core coordinate. Use it as y^0 and also as the conditional matching for each lambda-one state. Use zero conditional flow for every lambda-zero state.

This satisfies every global and conditional row and column, including columns that contain only the one conditioned state's z. It proves necessity for the complete matrix via §1. Empty C or L is literal; with L empty there are no leaf-flow coordinates, and with C empty there are only the matching rows and columns.

The variable count is exactly S_C+I_C+(1+S_C)E_L. Apart from nonnegativity and lambda normalization, there are I_C upper bounds, S_C value rows, |L|+|U| global rows/columns, and S_C(|L|+|U|) conditional rows/columns. This is the stated asymptotic bound. The coefficients are explicit binary rationals of polynomial bit length, so rational LP feasibility is a deterministic polynomial-time necessary test. Nothing here proves sufficiency.

## 4. General projection: independent extension formulas

Use the designated partition of §8: all original groups are cores, exactly the newly added adjacent-path groups are leaves. For one old resource u, let its distinct positive neighboring groups be c_1,...,c_d and let

\[
 \beta_i=\sum_s z_{c_i s u},\qquad
 B_i=\sum_{j=1}^i\beta_j.
\]

The old basic column says sum_i beta_i<=1. Repeated indexed states of one group contribute to the same beta_i and the same group port; no state port is substituted for the group port.

For d>=2, define the global flow of leaf i, adjacent to ports i and i+1, by

\[
 y^0_{i,u_i}=1-B_i,\qquad
 y^0_{i,u_{i+1}}=B_i,\qquad 1\le i<d. \tag{A}
\]

It is nonnegative and each leaf row sums to one. At port 1 its load is 1-beta_1. At an interior port i its load is B_{i-1}+1-B_i=1-beta_i. At the last port its load is B_{d-1}<=1-beta_d. Adding the core usages gives all global columns at most one. Equivalently, this is a mixture of the path matchings omitting port j, with weights beta_j and with the unused slack 1-sum beta placed on the last omitted-port choice.

For any one core-state (c,s), construct its conditional matching separately in every old-resource block. If c is a positive neighbor of u, omit its own group port, even if this particular state's coefficient on u is zero. If c is not a positive neighbor, omit a fixed port. The path matching omitting port j is explicitly

\[
 i\longmapsto
 \begin{cases}
  u_i,&i<j,\\
  u_{i+1},&i\ge j.
 \end{cases} \tag{B}
\]

Concatenate these independent block matchings to cover all added leaves. Multiply this one integral matching by lambda_cs. At the omitted own port, the conditional column contains at most z_csu<=lambda_cs and no leaf flow. At every other port its leaf flow is at most lambda_cs, with this state's z zero. If the group is not a neighbor, its z is zero throughout the block. Thus every conditional column and row holds. This argument applies to arbitrary fractional z; z=lambda is unnecessary. It performs no division by lambda, so lambda=0 gives identically zero flow without a limiting convention.

For d=1, there is one group port and no added leaf; the global column is just the old beta_1<=1 and the conditional bound is z<=lambda. For d=0, keep the unused old resource and add no leaf or positive z. Explicit old zero incidences are retained at the port prescribed by the Exact, but have no z variable and no value or flow contribution.

The reverse projection is equally direct. Sum all d lifted global columns in this block. The d-1 leaf rows contribute exactly d-1, hence

\[
 \sum_i\beta_i+(d-1)\le d.
\]

This is exactly the old basic column. R1, lambda normalization, and z bounds are unchanged under coefficient transfer. Therefore projection is equality and preserves the supplied point (lambda,z), including zero lambda, shared-state ports, d=0, and d=1.

## 5. Actual value and positive-support FSLP projection

To lift an old positive-value allocation, assign each valued old resource to the corresponding owner's group port. At most one core owns it. Match its path leaves to all other ports using (B); if no core uses it, omit an arbitrary port. Original core values are preserved and every new leaf gets value one. Since old values are at most one, this preserves the minimum. The zero-value case only requires the trivial nonnegative inequality.

In the reverse direction, consider any positive-value allocation in the lifted menu. Every adjacent singleton leaf must receive one of its own two ports. Those d-1 distinct leaves consume d-1 distinct ports of their old-resource block, leaving at most one port for positive original-core value. Ignore unvalued ports and map every valued group-owned port back to its old resource. The resulting original bundles are pairwise disjoint and preserve each selected-state value. Thus V(Q^path)=V(Q). The nonempty-original-core assumption is used: original groups remain in the minimum. Combining with §1 gives equality of the two distinct full matrices' optimal values, not identity of matrices or machines.

For precision, I interpret the label positive-support FSLP(1) in its usual explicit sense: state weights sum to one per group, and for every resource the sum of weights of indexed states with positive coefficient there is at most one. At epsilon=1, R1 and z<=lambda force z=lambda on every positive incidence, because state coefficient sums are one. Under this definition the same global formula (A), taking leaf singleton-state weights equal to the two endpoint flows, proves the exact FSLP(1) projection and preserves core lambda. The reverse follows by summing the path columns. No claim about a full scheduling CONFIG hierarchy is involved.

The automatic partition cannot be silently substituted for the designated one. The proof above keeps every original group as a core. It is compatible with automatic elimination only when every original group is non-threshold-unit-demand at that same epsilon, exactly the precondition stated in the Exact. Port transfer preserves that property. I did not find a conflict between §§2 and 8 under this precondition.

## 6. Family: witness, exact menu value, and all-job schedule

For the proposed lambda,z=lambda witness, each old g_(a,j) has total core usage

\[
 \lambda_{M,a}+\lambda_{H_{a,j},{\rm home}}
 =1/D+(1-1/D)=1.
\]

Each old A_(a,h) has total usage D times 1/D, also one. Thus the old basic columns are all tight. Formula (A) gives the complete global leaf flow. Specifically, a g path has left/right flows 1-1/D and 1/D; on an A path, leaf i has left/right flows 1-i/D and i/D. All lifted resource columns are tight. Formula (B) gives, for every core-state, lambda times one integral matching covering every added leaf. R1 is equality at epsilon=1, and the all-group positive-support FSLP(1) point follows as in §5.

Here is a short upper bound on the actual old menu value. Take any allocation of strictly positive minimum value and choose a maximizing state a for M. Let q be the number of g_(a,j) resources assigned to M. Each of those q corresponding H_(a,j) groups has lost its only home resource. To have positive value it must receive at least one of the t parking resources A_(a,h). Disjointness gives q<=t. Therefore M's value q/D is at most t/D=1/t. A zero minimum is already at most 1/t.

The matching lower construction chooses a=1 (or the first index), gives M exactly t of its g resources, gives each of the t displaced H groups a distinct parking resource in that block, and gives every other H group its home g resource. M and the displaced H groups each have value 1/t, and all others have value one. This proves V(Q)=1/t. Section 5 transfers it to the complete lifted menu.

For a full legal UM schedule, choose these witnessing states and the path-leaf singleton states selected by the omitted-port matchings. Place every selector at its chosen indexed root. Export only chosen-state jobs on their allocated resources. Keep every other original incidence job at its own indexed root. Selected low-value roots have load 2-1/t; other selected roots and all unselected roots have load at most one; every resource has load at most one. All original positive jobs execute. The lower bound of §1 ranges over all complete schedules, so OPT=2-1/t exactly.

Explicit zeros can all stay at their original private endpoints with time zero. Duplicate indexed states can be assigned zero lambda in the fractional witness, while their entire ordinary payload stays at their new private roots with load one. Unused resources do not alter value or feasibility. For fixed epsilon>0 and t>1/epsilon, the same witness satisfies R1, all original groups remain in C, and 1/t<epsilon gives the asserted failure under its own automatic preprocessing.

## 7. Sizes and total bit cost

The old g resources contribute 2D^2 ports and D^2 path leaves. The old A resources contribute D^2 t ports and Dt(D-1) leaves. Hence P_0=D^2(t+2) and L_0=D^2+Dt(D-1). Core-state count is D+2D^2. Each port is positive in exactly one core indexed state in this particular family, and each added leaf contributes two positive singleton incidences. Thus I=P_0+2L_0.

Every port is positive for its one core group/state and at most two adjacent leaf groups/states, proving both degree-three assertions. Normalization has not been changed and unit coefficients are genuinely present in the home states.

The stated machine, job, and finite-eligibility counts follow:

\[
 \#M=S_C+2L_0+P_0,\qquad
 \#J=K+L_0+I,\qquad
 \#\text{finite}=S_C+2L_0+2I.
\]

At t=2, these are 180 machines, 201 jobs, and 404 finite entries, with 17 cores, 40 leaves, 64 resources, 116 states, and 144 positive incidence jobs. The positive family description has O(t^5) entries with O(log t)-bit indices and rational data. A dense matrix has polynomially many entries in t. The entire conditional-flow witness can be much larger than the positive menu, but only by the stated polynomial product in core states and leaf edges.

For the general projection, each beta and each prefix sum is a rational sum of supplied z coordinates. Adding binary rationals may multiply denominators, but the resulting bit length is bounded by the sum of their input bit lengths plus polynomial indexing overhead. Conditional flows are zero or the supplied lambda, with no inverse or normalization by a small lambda. Thus the construction, whole LP, and extension have polynomial total bit length and deterministic output time in the explicit old data and supplied point. No polynomial-in-log(t) claim is needed.

## 8. Actual independent finite audit

I wrote and actually ran an independent Fraction-arithmetic implementation, using only this Exact. It materializes t=2, verifies the core witness, all complete global rows/columns and every complete conditional row/column, and builds the full 180-machine, 201-job, 404-finite-entry matrix. It assigns every original job and checks every physical machine load. The peak is exactly 3/2. It also verifies the lifted all-group positive-support FSLP(1) witness.

A separate normalized example has epsilon=2/5, positive coefficients 1/3, two original groups, a duplicate indexed state of lambda zero, partial z, a shared resource with slack, d=0/d=1/d=2 resource blocks, and four explicitly listed zero incidences. It checks the extension and preservation of each original threshold test. Its complete 12-machine, 18-job matrix has an audited all-tail schedule of peak two, retaining all four zero jobs at their private roots. This second schedule is only an execution/zero-retention check, not a claimed value computation.

Code:
/workspace/scratch/038d9dcc4cac/sol_conditional_leaf_hall_independent_audit.py
SHA-256 a27da8f52dc4fbe2bf719214c1d38ea2fbc75d3ef0a310fcb75b54bb0457fc38.

Complete finite matrix, assignments, all machine loads, and flow data:
/workspace/scratch/038d9dcc4cac/sol_conditional_leaf_hall_independent_audit.json
SHA-256 e547154c40c14ae882ffb5bf83903b70724fd55e0fc96421e4173ee4789fa48c.

No exhaustive bundle optimization, author checker, or LP oracle was used. The universal value and projection bounds above are mathematical proofs; the finite audits check the concrete matrices and formulas. The PASS conclusion is limited to this relaxation and these preservation claims. It gives no computational hardness, actual-YES approximation barrier, full-CONFIG/PSD result, or resolution of the main unrelated-machines target.
