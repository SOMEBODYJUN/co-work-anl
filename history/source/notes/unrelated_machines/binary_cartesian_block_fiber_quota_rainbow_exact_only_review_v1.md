# Independent Exact-first reconstruction: binary Cartesian block-fiber quota

Reviewer: `/root/rainbow_gap_source`, 2026-10-18.

Reviewed identity: `UM-BINARY-CARTESIAN-BLOCK-FIBER-QUOTA-v1`.

Actually read in full: `/workspace/scratch/038d9dcc4cac/binary_cartesian_block_fiber_quota_exact_v1.md`.

Measured Exact SHA-256: `8d16b510b4064e6ddaaf59edb04549fc5f2eb42c19ed1356d0129efb34e30a98`.

**Reading boundary.** For this Exact-first task I actually read only the specified Exact, then independently reconstructed the arguments below. I have not read its author Proof or another root/agent derivation. Before the task I had received a short statement-only message about the naked Cartesian family's value, without its proof; the new block-fiber, union, integer allocation, and chain proofs below were reconstructed from this Exact. No finite computational enumeration was used as a proof. No repo, Work, or Git action was performed.

**Verdict: PASS for the precise binary block-fiber quota, universal/attained union bound, exact floor, bounded-block decay, fixed-chain value, explicit construction, and ordinary-UM scope.** No mathematical fatal issue was found. A nonfatal alphabet-typing qualification concerning the final generic YES-lifting sentence is recorded in Section 8 below; it does not affect the main binary Claim.

## 1. Reconstructed object and why block independence matters

Let n=2^t with t>=1. A selected state family is one label vector ell(g) for each group g in F_2^t. Its support contains exactly one b for every a, namely

`b=ell(g)+a odot g`,

where odot is coordinatewise multiplication in F_2. Thus every selected support has n distinct resources.

For the fixed partition into nonempty blocks I_j, let r_j=2^{b_j}. Admissibility says that block j's output label is one globally shared function F_j of that block's input group coordinates only. For any such family, its selected support factors by blocks, and so does its union:

`union_g S_g,ell(g) = product_j (union_x S^j_x,F_j(x))`.

Both inclusions follow directly: each chosen global resource gives block resources in those unions, and any independent choices of block witnesses x_j combine into a legitimate full group g. This uses the full Cartesian group set and the fact that F_j is not secretly changed for different outside-block coordinates. It does not require F_j to be linear, injective, or nonconstant.

## 2. Universal one-block union bound for arbitrary nonlinear maps

Fix one block of length b>=1 and write r=2^b. Pair its groups x and x+1, where 1 is the all-one vector. These r/2 disjoint pairs partition all block groups.

For any map F:F_2^b to F_2^b, the two selected supports of x and x+1 have exactly one common resource. Indeed their equations imply

`a=F(x)+F(x+1)`,

and then `bvec=F(x)+a odot x` is determined. Conversely that resource satisfies both equations. There are no remaining free coordinates because the two groups differ in every coordinate.

Each pair's union has size 2r-1. The union over all pairs has size at most their summed union sizes, hence

`|union_x S_x,F(x)| <= (r/2)(2r-1) = r^2-r/2`.

Other cross-pair intersections can only decrease the union. This establishes the asserted upper bound for every nonlinear map without enumerating maps or using an average-density surrogate.

Applying the exact factorization of Section 1 gives the universal global bound

`|union_g S_g,ell(g)| <= product_j(r_j^2-r_j/2)`

`= n product_j(r_j-1/2) = n H`.

If every group receives at least m actual resources, their disjoint bundles have total size at least nm. Therefore m<=H. The minimum bundle count is an integer, so the optimum common count is at most q=floor(H). This upper bound permits every arbitrary partial subset B_g and never assumes that a bundle is Cartesian or fiber-shaped.

## 3. Explicit maps attaining the union bound

In each block choose F to be a cyclic coordinate shift. A one-coordinate block uses the identity shift. For fixed a, the map from x to the resource's b-coordinate is the linear map

`T_a x = F(x)+a odot x`.

Write the cyclic kernel equations as `x_(i-1)=a_i x_i`, with indices modulo b. If any a_i is zero, one x-coordinate is zero and these equations propagate zero around the cycle; the kernel is trivial. Thus for a not all one, T_a is invertible. If a is all one, the kernel consists exactly of the two constant vectors, so its dimension is one and its image size is r/2. This includes b=1.

Consequently for each of the r-1 ordinary a-vectors all r resource b-vectors occur once, and for the exceptional a=1 exactly r/2 occur twice. The block union size is exactly

`(r-1)r+r/2=r^2-r/2`.

Every block group is incident to r-1 resources of selected-support degree one and one resource of selected-support degree two. Products of these cyclic block maps are admissible and attain the product union bound nH.

## 4. A single integral allocation attaining floor(H)

Use that explicit product family. For every resource in its union, allocate fraction 1/deg(u) to each adjacent selected group. A global resource's selected-support degree is the product of its block degrees, each one or two. Every resource's fractional allocations sum to one.

For a fixed group, the received fractional count factors by blocks. In one block the count is `(r_j-1)+1/2=r_j-1/2`; therefore its global count is exactly H. Scaling all these fractions by q/H gives a feasible fractional allocation with row sum q for every group and resource capacity at most one.

Build one ordinary integral-capacity flow network: source-to-group capacity q, selected-group-to-resource capacity one, resource-to-sink capacity one. The displayed fractional allocation is a feasible flow of total nq. Integer max flow gives that full value, hence q distinct resources for every group simultaneously. Extract B_g from this one common integral flow.

This is not a separate independent allocation per block and does not require the final B_g to factor. It proves the lower bound q/n for the actual arbitrary-partial-bundle optimization. Together with Section 2 it proves exactly

`Q=floor(product_j(2^{b_j}-1/2))/2^t`.

## 5. Integer floor, parameter bounds, and explicit construction size

The exact numerator for H is `product_j(2r_j-1)` and its denominator is 2^k. Its binary description and the floor q have O(t) bits. Each factor r_j-1/2 is strictly below r_j, so q<n. The cyclic maps, selected supports, and flow graph can be generated directly without enumerating nonlinear functions or global state families.

There are n groups and n selected incidences per group, so the allocation graph has n^2 edges and at most n^2 resource nodes. Total assigned resources nq<n^2. The stated complete scheduling input already has n^3=8^t incidence jobs, in addition to n^2 private and n^2 resource machines. Thus exact arithmetic, state evaluation, explicit graph construction, integer flow, and output of all B_g are polynomial in the complete explicit input length. This does not assert polynomial-size output in t. There is no hidden enumeration of functions or numeric denominator copies.

Since

`H/n=product_j(1-2^(-b_j-1))`,

the ordinary floor identity gives

`0 <= H/n-Q < 1/n=2^(-t)`.

If every b_j<=L, each factor is at most `c=1-2^(-L-1)` and k>=ceil(t/L). Because 0<c<1,

`Q<=H/n<=c^k<=c^ceil(t/L)`.

This proves the fixed-L exponential decay for the **logical admissible family**, with the directions of both inequalities checked. One block gives H=n-1/2 and q=n-1, hence Q=1-1/n. Singleton blocks give H=(3/2)^t and the stated integer floor. When t=1, q=1 and Q=1/2. The excluded t=0 case is not needed for any integer quota.

## 6. Fixed acyclic chain: independent exact proof

For the fixed family ell_1=0 and ell_i=g_(i-1), write its selected resource equation as

`b=T_a g`,

where T_a is lower bidiagonal: diagonal entries a_i and subdiagonal entries one. For t>=2, the minor consisting of rows 2 through t and columns 1 through t-1 is upper triangular with diagonal entries one, so rank(T_a)>=t-1. For t=1 this lower bound is zero and remains valid. Since the full matrix is triangular, its determinant is `product_i a_i`.

Thus the all-one a gives rank t; every other a gives rank t-1. For a=1, every resource b has one group preimage; otherwise every reachable b has exactly two preimages, and there are n/2 such b. Therefore

`|selected union| = n+(n-1)n/2 = n(n+1)/2`.

Every resource in that union has selected-support degree at most two, while every group has n selected incidences. Sending one-half on each incidence gives each group n/2 fractional resource units and keeps every resource capacity at most one. One common integral flow or b-matching therefore assigns each group n/2 distinct resources.

For the reverse bound, any common integer count m satisfies

`m<=floor(|union|/n)=floor((n+1)/2)=n/2`,

because n is even. Hence `Q_chain=1/2`. The total union density alone would give the slightly larger fractional number `(n+1)/(2n)`; its integer floor is necessary here as well.

The family's actual cross-coordinate dependencies are precisely 1->2->...->t, with no self-dependence and at most one other-coordinate input per output. At t=1 there are no edges. This fixed family therefore witnesses that either of the two stated weaker dependency restrictions admits value at least one-half. It does not prove an upper bound of one-half when optimizing all acyclic maps, and the Exact makes no such claim.

The chain need not be block-fiber admissible for an arbitrary partition: an edge crossing two blocks violates that stricter condition. The fixed-chain counterexample and the bounded-block decay therefore concern different allowed choice families and do not contradict one another.

## 7. Ordinary UM assignment and the missing physical condition

Given an admissible selected family and disjoint B_g, place every selector at its chosen state machine, export just the B_g incidence jobs of that state, and park every other original incidence privately, including all unselected states. Selected private load is exactly `2-|B_g|/n`, unselected private load is one, and every used resource has one unit job. This is a complete legal actual schedule of makespan at most `2-min_g |B_g|/n`.

For the unmodified P_t, ordinary selectors have no block-fiber side condition. Every unrestricted state family is a map F:F_2^t to F_2^t, namely the one-block case. The universal one-block union bound and integer quota limit the minimum selected-state export count in every schedule below two to at most n-1: selected-state exports are disjoint because resources have unit cost. Thus the ordinary load is at least `2-(n-1)/n=1+1/n`. For C>=2 that lower bound is automatic. The explicit cyclic family and quota construction attain load 1+1/n, proving the asserted ordinary OPT.

Unselected-state exports in an arbitrary schedule can be ignored in this lower-bound extraction; they only consume resources. All original jobs remain present in the constructed upper-bound schedule. The normalized private masses, unit selectors, and unit external times are essential to this accounting.

It follows that the restricted logical value 2-Q is not the ordinary optimum for a multi-block P_t. No guard, coherence job, physical rejection rule, or other mechanism was introduced to enforce block-fiber admissibility. In particular logical exponential decay of Q is not a near-two UM NO promise or computational hardness. The unmodified resource degree over all menus is n, since each resource belongs to exactly one indexed state of each group. The counts n groups, n^2 private machines, n^2 resource machines, n^3 incidence jobs and n selectors are correct.

## 8. YES lifting, typing qualification, and final scope

For a binary base with the corresponding two group labels and state-label alphabet, let h(g_i) be a full-support disjoint-state witness. On a product group choose the coordinatewise labels h(g_i). Each output coordinate depends only on its own input coordinate, hence each block function can apply h componentwise and is admissible for every partition. If two product groups differ in any coordinate, their base witness supports in that coordinate are disjoint; their full Cartesian supports are consequently disjoint. The logical restriction therefore preserves that typed full-support YES witness.

The phrase in Exact section 5 referring to “any other base menu” needs the usual alphabet typing if intended beyond this binary setup. With arbitrary group/state alphabets, the same elementary YES-lifting argument works after **explicitly generalizing the block functions' domains and codomains to those alphabets**. The literally written F_2-domain functions do not themselves define choices for an arbitrary nonbinary base. I reported this as a nonfatal scope clarification, not an obstruction to the binary quota or chain theorem. This review does not manufacture a base reduction, preserve resource degree for such a reduction, or certify a physical source decoder from that generic sentence.

The exact mathematical conclusions and their explicit construction are self-contained and pass. The logical selection constraint, the fixed-chain counterexample, ordinary P_t, and a genuinely implemented UM coherence mechanism remain distinct objects. No source hardness, general tensor impossibility, or implementation of the admissibility condition has been established by this Claim or by this review.
