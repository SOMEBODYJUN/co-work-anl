# Local weight diversity and bounded site-primal width: exact box NE DP

Independent draft for internal review, 2026-10-04. No canonical implementation, external review, or priority assertion.

## SC-K-BOX-STRUCTURED-POLY-2: local-weight case, version 2026-10-07

The original SC-K-LOCAL-WEIGHT-BOX-DP below retains its exact decision statement
and fixed site-primal width `tau` and local distinct light-weight count `d`.
[SC-K-GREEDY-BOX-EXISTS](greedy_box_global_progress.md) now guarantees feasibility
for every legal canonical greedy input while freezing the same heavy and
singleton-option customers. The existing DP must therefore return a witness
throughout this fixed-parameter class, without any two-option or directed-depth
restriction. Combining its existing bit-polynomial bound with
SC-K-GREEDY-BOX-TO-2 yields a complete bit-polynomial factor-two continuation.
These are three joint premises of the newly versioned corollary.

This supersedes the need for height-two existence in the older application
below, without changing the older IDs' hypotheses. The DP and the imported
polynomial off-path scheduler remain unimplemented; the connected finite
greedy-box executable does not implement this polynomial construction.

## Exact claim

MF-MODEL has explicitly listed k>=2 labeled facilities, common finite catalog S, explicitly listed positive binary rational weights and coverage sets. Run the canonical polynomial greedy layout with positive maximum reach; write O for occupied sites, q_s>=1 for their multiplicities, gamma>0 for the last insertion score. Freeze customers with a single occupied option, and customers w_i>=gamma at their original greedy sites. I* consists of all other served customers: 0<w_i<gamma, |A_i|>=2, where A_i consists of the occupied sites covering i. Unserved clients do not enter on-path constraints.

Define the SITE PRIMAL graph G on O: join s,t if they both lie in A_i for some i in I*. Include isolated occupied sites. Define

    d_s = #{w_i : i in I*, s in A_i}.

Thus d_s counts EXACT DISTINCT RATIONAL WEIGHTS, not individual clients or coverage types. Assume max_s d_s<=d and a supplied width-tau tree decomposition of G. For every fixed tau,d, an input-bit-polynomial algorithm decides whether these prescribed fixed customers admit a site-pure/within-site-independent-uniform exact customer NE inside ALL boxes

    q_s gamma <= W_s <= (q_s+1)gamma.

If yes, it outputs a labeled assignment and hence the exact independent mixed on-path profile. The graph may have unbounded site degree, arbitrarily many individual clients on an edge, and unbounded GLOBAL distinct weight count. The original DP theorem alone is a decision statement; the new corollary above supplies existence separately. Given the standard fixed-treewidth decomposition theorem already imported by SC-K-INCIDENCE-BOX-DP, the supplied decomposition can be dropped for fixed tau, or handled as an explicit additional input.

For two-option light clients whose opening-directed graph has every directed path of length <=2, the independent HEIGHT-TWO-BOX-EXISTS theorem guarantees yes. On this simultaneous class the DP plus BOX-TO-2 gives a polynomial complete factor-two continuation. In particular, inward stars with bounded weight diversity at the center may have arbitrarily many leaves and arbitrarily many unequal-weight clients on every leaf edge; the center need not be first-opened. Arbitrary orientation of a star has directed depth <=2, and the new algorithm therefore covers every star orientation under local d. This remains conditional on fixed tau,d, not the all-input target.

## Exact compressed objects

Let N=|I*|; let F_s be the total weight of all frozen customers assigned to s. Group I* into types a=(w_a,A_a), with count n_a. Identical exact rational weights are tested by equality, and option sets are the actual occupied options. Each type has n_a individually labeled clients. Its option set A_a is a clique in G, hence |A_a|<=tau+1; every clique of a graph lies in some bag of every tree decomposition. Assign each type to one such bag, once.

At each site s list its d_s distinct incident variable weights as lambda_s,1,...,lambda_s,d_s. Let m_s,j be the total number of variable clients of weight lambda_s,j with s as an option. A possible FINAL COUNT VECTOR c_s satisfies

    c_s,j in {0,...,m_s,j}.

Given c_s, its final site total is

    W_s(c_s)=F_s+sum_j lambda_s,j c_s,j.

There are <=(N+1)^d possibilities per site. Discard vectors violating either full box. It is unnecessary to assume that different count vectors give different numeric totals; the DP retains counts so conservation is exact.

For type a choose nonnegative integers x_a,s, s in A_a, satisfying sum_s x_a,s=n_a. Enumerate the weak compositions; their count is <=(N+1)^(|A_a|-1)<= (N+1)^tau. If x_a,s>0, check EVERY t in A_a\{s}:

    q_t [W_s(c_s)-w_a] <= q_s W_t(c_t).              (NE-a)

This is the correct own-weight-discount condition: client i assigned at s independently uses its q_s facilities uniformly, so its conditional expected cost is w_i+(W_s-w_i)/q_s, and at an alternative site t it would pay w_i+W_t/q_t. The common w_i cancels. (NE-a) must not be replaced by comparing W_s/q_s against W_t/q_t or by subtracting w_a x_a,s.

When a type composition is accepted, add x_a,s to the running contribution of the weight-coordinate for w_a at each s. Types do not need support bits: x_a,s>0 is directly checked. Later clients of a type have identical weights and option sets; arbitrary expansion to labels preserves all inequalities.

## Tree decomposition DP

Convert the supplied decomposition to a rooted nice decomposition with introduce, forget and join operations and empty root/leaf bags, retaining width tau. Add one local type-processing operation for each type at its selected bag. Multiple types assigned to one bag are processed in sequence. The polynomial bag count is O((tau+1)|O|+T), up to ordinary decomposition-size normalization; a supplied decomposition's size is included in input length.

For bag B store:

1. guessed final c_s for each s in B;
2. accumulated vector p_s for each s in B, counting variable clients contributed by types processed in the subtree below and including this operation.

Maintain coordinatewise 0<=p_s<=c_s. Stored table entries also have a witness predecessor. A table state is feasible exactly if one can allocate every already processed type, meet its whole-scope NE-a inequalities, and have final counts matched at every site already forgotten. Each unforgotten site's final guess is kept identical throughout its connected bag subtree.

Operations, working upward:

* Empty leaf: the empty state.
* Introduce s: choose any box-feasible c_s; set p_s=0. No descendant processed type can touch s, since s is absent from the child bag and bags containing s form a connected subtree.
* Process type a: all A_a lie in this bag. Enumerate its weak compositions, check NE-a using the already guessed FINAL loads at all A_a, add contributions to the p_s coordinates, and retain if p<=c. This is why guesses of final loads are separate from running partial loads.
* Forget s: require p_s=c_s coordinatewise; then remove both vectors of s. Every type touching s is already processed below this forget, because its designated bag contains s and s has no occurrence above the forget.
* Join: the two children have the same bag. Require identical c_s guesses on both sides; replace their partial contributions by p_s=p_s,left+p_s,right, rejecting p>c. Each type is assigned exactly once, so there is no duplicated contribution. Frozen totals F_s appear only in final loads and are never counted in p.
* Empty root: yes exactly when the empty state survives; witness backtracking recovers all accepted compositions.

Correctness follows by induction over these operations. A genuine feasible NE induces c_s and compositions, so survives every check. Conversely a surviving root state assigns each type's n_a clients exactly once; every site's final count is accounted for at forgetting; all box checks and every active-type NE-a comparison have been passed. Expanding integer counts gives a labeled on-path assignment. Fixed single-option clients have no alternative, and a fixed heavy client i at s has

    (W_s-w_i)/q_s <= ((q_s+1)gamma-gamma)/q_s = gamma <= W_t/q_t

for every occupied alternative t. Thus every served customer, not merely the variable customers, is at exact NE. Unserved clients remain unserved in the fixed on-path occupancy.

## Bit complexity and scope

A bag has <=tau+1 sites and <=d(tau+1) coordinates per vector collection. There are <=(N+1)^[2d(tau+1)] possible (c,p) states. A naive join scans pairs of child states, <=(N+1)^[4d(tau+1)] combinations. Each type operation enumerates <=(N+1)^tau compositions per state and checks O((tau+1)^2) inequalities. Therefore, for fixed tau,d, a conservative upper bound is

    poly(L, size(decomposition)) * (N+1)^[4d(tau+1)+tau+1],

where L is the explicit input encoding length. The exponent is deliberately not optimized. No iteration over weight magnitudes or a common numerical denominator occurs. Final/partial counts have O(log(N+1)) bits; each W_s is a sum of the fixed-customer total and <=d binary rational products lambda*c. Its bit length is polynomial in input length, even when frozen clients have arbitrarily many weights. q_s<=k, and all cross-multiplied NE/box inequalities therefore have polynomial encoding length. Decomposition checking, type grouping, label expansion and the inherited off-path completion are polynomial as well. Empty I* is handled by directly checking the original fixed boxed state; all-zero reach gives the known empty continuation separately.

This drops the individual-degree restriction by paying for bounded local
WEIGHT DIVERSITY. It subsumes the prior fixed-incidence-treewidth-and-degree
selector: its width conversion gives a fixed site-primal width, and the
local distinct-weight count is at most the old individual site degree.
It also covers unbounded-size components under the stated parameters,
where the component-size-bounded type method does not apply. The solver's
constraints still concern the prescribed frozen-heavy site-pure box. The new
existence theorem guarantees that a correct DP cannot return a negative decision
on legal canonical greedy inputs in this class. General independently mixed NE
at arbitrary non-greedy occupancies remain outside this selector's scope.
