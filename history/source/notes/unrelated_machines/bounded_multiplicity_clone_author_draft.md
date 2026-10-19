# 有界重数克隆接线的配置包络与共同循环复制反例

Purpose: diagnose selected sparse clone wiring in the attempted integer-gap amplification route. This is a new bounded-multiplicity interpolation of the existing permutation-cover and complete-clone statements, together with an explicit common-wiring counterexample. It is not a source hardness theorem, an algorithm for general unrelated machines, or a negation of UM-TARGET-v1. No global novelty is certified.

## 1. Exact bounded-wiring object

Let P be any UM-MODEL-v1 instance: m>=1 machines, n>=0 jobs, nonnegative binary-rational finite times and unavailable edges; each job has a finite edge. Fix an integer c>=1. For q>=1, a c-wiring Q of P has machine copies (i,s) and job copies (j,r), r,s in [q]. For every original finite incidence (i,j), select c permutations pi_ij^h of [q], h in [c]. Permutations may repeat. Its finite clone edges are precisely

    (j,r) -> (i,pi_ij^h(r)), with processing time p_ij.

Repeated edges are merged. There are no other jobs, machines, or finite edges. Equivalently, an incidence is the union of at most c permutation matchings. Allowing repeated permutations is part of the definition; requiring c disjoint matchings would be a different object.

For T>=0 let A_i^c(T) be all integer vectors a in {0,...,c}^J, with a_j=0 on unavailable incidences and sum_j p_ij a_j<=T. Define MC_c(T) by

    y_ia>=0, sum_a y_ia=1 for every i,
    sum_i sum_a a_j y_ia=1 for every j.

Let t_c(P) be the minimum feasible threshold. These are finite rational LPs; the definition does not supply their solver. Configurations include the empty vector. Unlike the unrestricted-multiset case, zero processing times require no special preprocessing because every coordinate is bounded.

## 2. Exact theorem and actual witness conversions

**Candidate ID: UM-BOUNDED-MULTIPLICITY-CLONE-ENVELOPE-v1.** For every P and every c>=1:

1. Every actual makespan-T schedule of every c-wiring with q copies projects to a feasible MC_c(T) point whose probabilities have denominators dividing q.
2. Every finite rational MC_c(T) point with common denominator q is realized, with exactly its prescribed machine-type configuration frequencies, by an actual schedule of some c-wiring with q copies.
3. Every original actual schedule lifts without load loss to every c-wiring.
4. Consequently

       t_c(P) = min_{q>=1, Q a c-wiring of P} OPT(Q),
       t_c(P) <= OPT(Q) <= OPT(P).

   The minimum is attained. Moreover t_1=T_CONF and t_(c+1)<=t_c. The theorem includes empty jobs, zero times, zero optimum, and unavailable edges.

**Proof of 1.** At one machine copy (i,s), any fixed original type j has at most c neighboring job copies: at most one preimage under each selected permutation. Its actual schedule therefore induces a multiplicity vector in A_i^c(T). Give the empirical frequency of each vector mass 1/q. Every original job type has exactly q actual copies and every copy is executed once, so its projected expected multiplicity is exactly one.

**Proof of 2, including all original job identities.** Instantiate q machine copies of every type. Place configuration a on precisely q y_ia of them. For each original j, the total number of demanded j-slots is q; list these slots with multiplicity and biject them with the q distinct job copies (j,r). This specifies the actual assignment and guarantees its loads.

For a fixed original finite incidence (i,j), its used assignment edges form a bipartite star forest: a job-copy vertex has degree zero or one, and a machine-copy vertex has degree at most c. Color the used edges with c colors by giving distinct colors to edges with the same machine-copy endpoint. Each color is a partial matching, because no job-copy is used twice. Complete each partial matching to a bijection between all q job-copy labels and all q machine-copy labels by arbitrarily pairing their unused labels. These c completed permutations define the required incidence wiring. Different colors are allowed to add the same unused edge. Every previously assigned edge remains eligible; all q copies of every original job were already assigned exactly once. This gives the full ordinary matrix and full actual schedule, not only aggregated counts.

**Proof of 3.** If original j is assigned to i, choose the first selected permutation for that incidence and assign every (j,r) to (i,pi_ij^1(r)). Each machine copy of type i receives exactly one copy of each original job assigned to i. Its load is exactly the original load.

**Existence/minimum.** Original schedules are allowed MC_c configurations, so some threshold is feasible. There are only (c+1)^n multiplicity vectors per row, hence only finitely many configuration loads. At the minimum feasible threshold the finite rational LP has a rational feasible point. Part 2 realizes its common denominator and proves attainment. The remaining conclusions follow immediately. For n=0 use the empty configuration in every row; the actual assignment and all job coverage equations are empty. For OPT=0 the same construction executes every job on a zero edge and preserves zero exactly.

**Bit and output size.** With r=m+n, a basic feasible point can be chosen whose common denominator q satisfies q<=(c sqrt(r))^r: the equality matrix has at most r rows, integral entries of magnitude at most c, and right-hand side one; apply Cramer and Hadamard to a nonsingular basis minor. Thus log q is polynomial in the original dimensions and log c. The numerical value q, and therefore the explicit wiring, may still be exponentially large. Given a rational configuration certificate, the construction is deterministic and polynomial in its expanded configurations, q, c, the original input size, and the output size. It is not generally polynomial in log q or log c. No claimed source reduction may use the denominator bound alone to call its output polynomial size.

## 3. Genuine interpolation and its strictness

After removing all entire job types with a zero endpoint, let U=sum_j min_i p_ij and p_min be the minimum remaining positive finite processing time. If positive types remain, put K=floor(U/p_min). The existing unrestricted multiset threshold t_+ equals t_c for all c>=K: a configuration of load at most U cannot have more than K jobs. Removing zero-end types preserves every t_c because each removed type can be inserted once on a fixed zero endpoint in every configuration of that row. If no positive types remain, all thresholds are zero. This connects the existing endpoints without conflating them.

Every adjacent level can be strictly different. For c>=1, take c+1 machines, c distinct global unit jobs available everywhere, and one private job u_i of size 1/(c+1) on machine i. Then

    t_c = 1+1/(c+1),             t_(c+1) = 1.

For any T<1, no global unit job is coverable. At T=1, no configuration may mix a unit job with a positive private job. Write b_i for the probability of a unit configuration at row i. Private coverage and multiplicity cap c imply 1<=c(1-b_i), so sum_i b_i<=(c+1)(1-1/c)=c-1/c<c. But the c global unit jobs require sum_i b_i=c. Thus MC_c(1) is infeasible. Configuration loads have no breakpoint in (1,1+1/(c+1)), so t_c>=1+1/(c+1). An actual original schedule with this load supplies the reverse bound.

For cap c+1, at each row give weight 1/(c+1) to the configuration consisting of c+1 copies of its private job, and the same weight to each of the c singleton global unit configurations. Row normalization and all job-type coverage equations are exact, and every configuration has load one. A unit gives the lower bound one. This proves the strict hierarchy without an optimization oracle.

## 4. Uniform connected degree-two wiring collapses a near-two seed

**Candidate ID: UM-COMMON-CYCLIC-TWO-WIRING-NEAR-TWO-COLLAPSE-v1.** For every m>=2 define P_m as follows. There are machines i in Z_m, one global unit job B available on all machines, and m-1 distinct private jobs U_it, t=1,...,m-1, each available only on i and of size 1/m. Then

    OPT(P_m) = t_1(P_m) = 2-1/m,
    t_2(P_m) = 1.

The cap-two minimum has an explicit polynomial-size realization using q=m copies and **the same two permutations on every original finite incidence**:

    identity x -> x,       cyclic shift x -> x+1 mod m.

Every incidence graph is a connected 2m-cycle. The choice of permutations does not depend on the machine or job type. The resulting ordinary instance Q_m has m^2 machines, m+m^2(m-1) jobs, and 2m^3 finite clone edges. Every job and finite time remains exactly as prescribed by the clone definition.

**Complete actual schedule.** Assign B-copy x to (x,x). For a private job-copy (U_it,x), put d=(x-i) mod m, represented in {0,...,m-1}. Assign it to

    (i,x+1) if d<t,       (i,x) otherwise.

Both destinations are original finite clone edges. For a fixed private type U_it, the shifted copies form the cyclic interval i,...,i+t-1. Its occupancy on machine copies of type i is zero at copy i, two at copy i+t, and one elsewhere: the interval start loses its job, the interval end's successor receives an extra, and all interval interiors have one entering and one leaving.

At the reserved copy (i,i), all m-1 private types have occupancy zero and B-copy i contributes exactly one. At any other copy (i,s), exactly one private type, namely t=s-i mod m in {1,...,m-1}, has occupancy two; the other m-2 types have occupancy one. Thus this machine runs exactly m small jobs, of total load one, and no unit. All m^2 machines have load exactly one. There are m distinct actual B copies, so every legal schedule has makespan at least one. Hence OPT(Q_m)=1, giving t_2=1.

For the original instance, all private jobs are forced, making the baseline (m-1)/m at every row. Whichever row receives B has load 2-1/m, which is attainable. At cap one, every private job has expected occurrence one on its unique row and occurrence at most one in every configuration. It must therefore occur in every positive-weight configuration of that row; whichever row covers positive B mass needs threshold 2-1/m. This proves t_1 exactly. More strongly, **every one-permutation clone wiring of this seed retains actual optimum 2-1/m**, because every clone machine has one forced copy of each private type. Thus one extra neighbor per original incidence is already enough to cross from universal preservation on this family to exact collapse, even with uniform connected cycle wiring.

The construction of the common-cycle witness was supplied independently by boss30's consistency_gadget statement reviewer after seeing the bounded-multiplicity theorem; it strengthens the author's initial type-dependent-shift construction. This provenance is retained rather than claimed as independent author priority.

## 5. Meaning for attempted amplification

The two existing endpoints already say that permutation covers can realize CONFIG, whereas complete clone pools realize unrestricted multiset configurations. The new exact statement identifies the whole bounded-multiplicity interpolation. The explicit common-cycle family shows that full cross-clone connectivity is not needed for a near-two actual seed to become unit feasible: degree two, connected single cycles on every incidence, translation-invariant wiring, and polynomial q already suffice.

This is an existential minimum over selected c-wirings, and a fixed explicit counterexample family. It does not say that every c-wiring collapses, that arbitrary randomized wiring collapses, that every source image admits the exhibited certificate, or that all possible gap compositions fail. In particular identity-only wiring always preserves the original seed. These results do not yield near-two NP-hardness or refute UM-TARGET-v1.

The remaining hardness obligation is unchanged: construct a source-related selected wiring with polynomial explicit size, retain YES schedules, and decode **every** actual load below an absolute NO threshold into a source witness or violation. Bounded degree, connected incidence cycles, and the absence of complete clone pools do not alone supply that decoder. No escaping gap composition was found in this subtask.

## 6. Finite exact audit

The sibling `bounded_multiplicity_clone_audit.py` uses only Python integers and Fraction. It constructs full ordinary matrices and actual assignments for the common-cycle family; checks every finite incidence against its two defining permutations; checks every job once, all finite endpoints, and every row load; exhausts all c<=2 incidence-wiring graphs on the m=2,q=2 seed and all of their actual assignments; and implements the general rational certificate-to-wiring conversion for the strict hierarchy plus zero/empty boundary cases. Its JSON report records precise finite ranges. These runs do not prove the general theorem or implement an MC_c optimizer.

The common-cycle finite range m=2,...,17 has 1,784 machines, 21,776 jobs, and 46,816 finite edges in total. All of its machine loads are exactly one. The m=2,q=2 exhaustive test checks 81 distinct incidence-wiring graphs and 2,448 actual assignments: 72 graphs have optimum 3/2 and nine have optimum one. The 16 one-permutation wirings are all among the former. An additional complete common-cycle m=2 enumeration checks 256 assignments and confirms optimum one. General realization is also checked on all 22 ordered denominator-two configuration arrays (eight distinct laws) for one explicit two-machine/two-job heterogeneous matrix. The latest report is `bounded_multiplicity_clone_audit_v2.json`; the earlier report is retained with its original source hash.
