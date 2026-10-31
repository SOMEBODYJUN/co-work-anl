# Conditional leaf Hall v3: new-clause-first independent reconstruction

Reviewer: /root/sol_literal_budget_attack, 2026-10-18.

Verdict: PASS for the new common-leaf-edge-marginal clause and its exact projection assertion. I independently reconstructed a preserving extension for every feasible old point, with all boundary cases, and found no fatal counterexample.

This is not a fresh blind review of the whole candidate: I had already independently reconstructed Exact v2 and then read its released author proof. This record concerns the new v3 clause before reading any proof of that clause.

## Identity and actual read scope

I checked the whole-file SHA-256 of
/workspace/scratch/038d9dcc4cac/conditional_leaf_hall_consistent_marginals_exact_v3.md:
34244f9737bbbe7baa858482d31f8154f0e4146be0f1464c9e0598a402bfb38b.
I actually read its entire identity header and entire new §9, in one untruncated 895-token tool result. I did not reread unchanged §§1–8 in this version; my reviewed v2 source and frozen records remain identified separately.

The v2 Exact-first record is f5e2bbfc15066eff1969a8a91106d92c22103c1c245b80f65eda365e85518812. Its author-read-after record is ca41d9f2bde78ceee5a2905ad00ac3ee871467ecfcdc909aa16c2c85d47264f5. Neither was modified.

I have not read a v3 author transport proof, author checker, sol_nsw draft, or another author's v3 derivation before this freeze. My new audit is self-contained standard-library Python and imports no author or v2 helper module.

## 1. Hole variables reduce the new requirement to transport

Fix one old resource u. Its d positive neighboring groups have ordered ports 1,...,d. For d>=1 write

\[
 b_j=\sum_s z_{c_j s u},\qquad
 \sum_j b_j\le1.
\]

Choose one global rational hole distribution pi with pi_j>=b_j and sum pi=1. For definiteness add all slack to the last coordinate. A path matching with hole j matches leaf i to port i when i<j and to port i+1 when i>=j. Its mixture with hole law pi defines the same global y^0 as in my v2 prefix construction.

For a particular original core c, seek a table q_(s,j) with

\[
 q_{s j}\ge0,\qquad
 \sum_j q_{s j}=\lambda_{cs},\qquad
 \sum_s q_{s j}=\pi_j. \tag{1}
\]

It represents the unnormalized hole mass for state s. If c owns port i, the conditional column only requires q_(s,i)>=z_(csu). If c has no port, there is no positive conditioned z on this path. Such a table gives conditional leaf flows by the same linear matching map:

\[
 y^{cs}_{\ell_i,u_i}=\sum_{j>i}q_{s j},\qquad
 y^{cs}_{\ell_i,u_{i+1}}=\sum_{j\le i}q_{s j}. \tag{2}
\]

Its leaf rows equal lambda. A port j's leaf load equals lambda-q_(s,j), so the conditional capacity follows from the own-port lower bound and nonnegativity. Summing (2) over s and using the column sums in (1) gives exactly y^0 on each leaf edge. Thus (MC) is a transport-marginal condition, with the same global hole law for every core.

## 2. Explicit transport table for arbitrary fractional z

If c owns port i, put theta_s=z_(csu), interpreting zero/nonpositive incidences as zero, and beta=sum_s theta_s=b_i. Let delta_j be one at i and zero elsewhere. If c has no port, put every theta_s=0, beta=0, and every delta_j=0.

For beta<1 define

\[
 q_{s j}
 =\theta_s\delta_j+
 \frac{\lambda_{cs}-\theta_s}{1-\beta}
       \bigl(\pi_j-\beta\delta_j\bigr). \tag{3}
\]

All factors are nonnegative: theta_s<=lambda_cs, beta<=pi_i when an own port exists, and pi is nonnegative. The residual column totals sum to 1-beta. Therefore the row sum is lambda. The residual row totals sum to 1-beta, so the column sum is

\[
 \beta\delta_j+\pi_j-\beta\delta_j=\pi_j.
\]

At the own port q_(s,i)>=theta_s. If c has no port, (3) simply reduces to lambda_cs*pi_j.

For beta=1, c necessarily has an own port i. Since sum_s theta_s=sum_s lambda_cs=1 and theta_s<=lambda_cs coordinatewise, theta_s=lambda_cs for all s. Also pi_i=1. Set q_(s,i)=lambda_cs and every other entry zero. This is the required table, without division by zero.

Zero lambda automatically makes theta and its entire table row zero. A state that is zero on u may have positive lambda, and (3) explicitly assigns its residual hole mass; omitting this case would invalidate the proof. When d=1, pi_1=1, there are no leaf edges and the table reduces to q_(s,1)=lambda regardless of theta. When d=0, retain the unused resource and make no hole table or leaf flow. The basic old column is identically zero there. Explicit zero incidence jobs do not enter theta, b, or the flow constraints.

The original R1, lambda normalization, and core z are preserved exactly. Applying (1)–(3) independently to every old resource supplies all global and conditional flows and all (MC) rows simultaneously.

For the reverse inclusion, R_cons is a subset of the reviewed v2 system. Summing each path's d global resource columns and its d-1 unit leaf rows gives the old capacity sum b_j<=1. Nothing in the new rows weakens that argument. The two projections are therefore equal for the exact supplied point, not merely equivalent in feasibility.

## 3. A polynomial full-matching mixture, without a product blowup

For a fixed core-state h=(c,s), each resource path's q row has total lambda_h. To realize all these path marginals by full integral matchings, consider the interval [0,lambda_h]. For each path partition that interval into consecutive subintervals of lengths q_(h,1),...,q_(h,d).

Take the union of all rational partition endpoints and sort it. On each resulting nonempty interval, every path has one fixed hole. Concatenate its one-hole matchings across all paths. Because paths have disjoint resources and leaves, this is one integral matching of every added leaf. Weight it by the interval length.

The weighted sum reproduces all conditional flows in (2). There are at most one plus the sum of the path port counts many pieces. For lambda_h=0 the empty weighted family gives zero flow. No division by lambda or exponential enumeration of independent path choices is required. Thus each conditional flow really is lambda times a rational convex mixture of full integral leaf matchings, with polynomial explicit support if desired.

This construction is performed separately for different cores and states. It does not assert a common probability law on complete global matchings for every core; it asserts only the stated common edge marginals.

## 4. Why the v2 single-matching clause cannot be transferred

In Q_t, on any A_(a,h) path there are D core ports, each with usage 1/D. The global column sum is tight, so the global hole law is forced to be uniform.

For a helper H_(a,j), its parking state has lambda=1/D and z=lambda on its own port j. Its conditional hole mass is therefore all 1/D at j. Consistency then forces the home state's conditional hole mass to be zero at j and 1/D at each of the other D-1 ports. Its total mass is (D-1)/D.

Since D>=4, that home conditional cannot be lambda times one integral matching: a single one-hole matching would place all (D-1)/D mass on one hole, exceeding its required 1/D column mass. A mixture is necessary. The new Exact correctly states this weaker conditional-matching scope, and formula (3) supplies it.

The same family lambda,z=lambda is an old basic feasible point, so §§1–3 extend it to R_cons. The original menu and full processing matrix have not changed. The reviewed value proof V=1/t and complete all-job optimum 2-1/t therefore still apply. At each fixed epsilon, t>1/epsilon retains the same automatic partition and relaxes R1, while the new (MC) rows are unchanged. The gap conclusion follows.

## 5. Partition, necessity, and total bit complexity

All original groups are designated cores and exactly the added paths are leaves. Automatic threshold elimination is compatible only under the same previously reviewed non-threshold-original-group precondition. No reclassification is hidden in this proof.

A deterministic actual-allocation witness chooses one state per core. It uses y^0 as that state's conditional matching and zero for every other state. Hence its state-summed conditional flows equal y^0 and necessity survives the new condition.

There are at most |C|E_L new linear equalities, so explicit rational LP feasibility remains deterministic polynomial time. The internal table construction uses polynomially many entries. Unlike my v2 construction, (3) does divide by 1-beta, and its zero case must be branched. A nonzero 1-beta may be numerically tiny but its numerator and denominator have polynomial binary length in the supplied rational point. One rational reciprocal and multiplication per entry therefore preserve polynomial bit length. Interval endpoint sums, rational comparisons, and matching concatenations are likewise polynomial in the explicit old data and point length.

The source claim does not require polynomial time in log(t) for a t-polynomial output. It also does not claim a full CONFIG or PSD hierarchy, a common matching law, joint-core capacities, computational hardness, or an actual-OPT approximation lower bound.

## 6. Actual independent audit

I wrote and ran exact Fraction-arithmetic checks of (1)–(3), the complete R2 rows/columns, every (MC) edge row, and the interval full-matching decomposition:

| Fixture | Core states | New resources | Leaves | MC rows | Conditional rows / columns | Integral matching pieces |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Q_2, same original lambda,z | 36 | 64 | 40 | 1360 | 1440 / 2304 | 176, maximum 6 per state |
| Partial z, zero-lambda duplicate, zeros, d0/d1/d2 | 3 | 7 | 1 | 4 | 3 / 18 | 4, maximum 2 |
| beta=1 boundary with d2 and zero states | 4 | 7 | 1 | 4 | 4 / 24 | 2, maximum 1 |

The beta=1 fixture actually exercises six state cases of the separate branch; its original menus are also non-threshold-unit-demand at epsilon=1. The partial-z fixture uses epsilon=2/5 and 1/3 coefficients, so its original groups also satisfy the automatic-partition precondition. Both retain a d=0 unused resource and explicitly listed zeros.

These checks concern the new flows. The unchanged Q_2 full matrix, including all 201 jobs and every machine load, was already independently audited in the frozen v2 code; I did not represent this new audit as another full scheduling optimization or a proof by finite enumeration.

Code:
/workspace/scratch/038d9dcc4cac/sol_conditional_leaf_consistent_marginals_independent_audit.py
SHA-256 d4b8a93458e584057108414aa0d883a0ea16423f255beab627aa45abed8c5e71.

Exact hole tables, all flows, and full integral matching mixtures:
/workspace/scratch/038d9dcc4cac/sol_conditional_leaf_consistent_marginals_independent_audit.json
SHA-256 579293d74df98b8461d41f51f836404dbb1a56a92a0585d24ec6f66cb19950b3.

The script is self-contained and uses only the standard library. Its sole output path is the relative JSON filename in the current working directory; JSON keys are sorted. No candidate author proof/checker or repository file was read or edited for this new-clause reconstruction.
