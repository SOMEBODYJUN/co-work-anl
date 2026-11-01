# Fractional rematching and deterministic explicit-XOS robust-gap boundary — statement-only Exact v5

Date: 2026-10-18. Prepared by general_query_response_review jointly with root after disclosed collaborative proposals, actual source/tool reading, and separate checks of residual normalization and candidate-local relative flooring. This is a scratch-only co-developed statement for a new independent Exact-first review. It is not a blind review record, a full author proof, a software claim, or a mature asset registration. All earlier versions and objections remain immutable process sources.

Section A below is byte-for-byte identical to its frozen v1/v2/v3/v4 text. B now concerns arbitrary explicitly given finite nonnegative binary-rational XOS clauses, with no global normalization or grid input promise. It normalizes residual rows exactly for its rational LP solver, and floors only already fixed candidates' relative clause weights for an internal polynomial-size mask DP. C continues to concern the original normalized menu object and no longer requires a global utility floor. Algorithm descriptions specify auditable finite input/output promises; derivations are not included.

## A. Standalone fractional-benchmark matching statement

### A1. Finite object and rational input

Let n>=1 be an integer. There is a finite item set U and an explicitly specified subset H of exactly n distinct items. Write B=U\H.

For each agent i in [n], v_i:2^U -> Q_{\ge0} is finite, monotone and subadditive, with v_i(empty)=0. These are semantic hypotheses on the valuations. The explicit application may represent them as normalized XOS clause tables. More generally, a value-query interface may be used, with all queried rational values returned in finite binary encoding. Running time below is charged for the actual input and the polynomially many queried rational values; no enumeration of 2^U is required.

Give nonnegative binary rationals V_i and a binary rational c>=1. Put A={i:V_i>0}. For each i outside A, require v_i(B)=0.

Give a finite explicit rational configuration list y=(y_{i,S}) with y_{i,S}>=0, such that
\[
\sum_{S\subseteq U}y_{i,S}=1\quad(i\in[n]),\qquad
\sum_{i,S:j\in S}y_{i,S}\le1\quad(j\in U).
\tag{A1}
\]
Only nonzero entries need be listed, and every entry y_{i,S}>0 must have v_i(S)>0. The value on each listed configuration may be supplied or obtained by a value query. Configurations are ordinary subsets of the original items, not independent coordinate labels.

### A2. Fractional residual welfare premise

Assume that every feasible fractional configuration family z=(z_{i,T}) for the agents in A on item set B satisfies
\[
\sum_{i\in A}\sum_{T\subseteq B}
 z_{i,T}\frac{v_i(T)}{V_i}\le c n,
\tag{A2}
\]
where feasibility means
\[
z_{i,T}\ge0,\quad
\sum_{T\subseteq B}z_{i,T}=1\ (i\in A),\quad
\sum_{i\in A,T:j\in T}z_{i,T}\le1\ (j\in B).
\]
This is a semantic bound for all fractional families, not just integral allocations. If A is empty it is vacuous. A stronger bound c|A| also suffices.

The theorem does not claim that its algorithm verifies this global premise or obtains the V_i. They are hypotheses of the matching interface. In a downstream application they must be supplied by an independently justified backend.

Define the positive benchmark
\[
\mathcal B(y)=
\exp\left(\frac1n\sum_{i,S}y_{i,S}\ln v_i(S)\right).
\tag{A3}
\]

### A3. Exact matching conclusion and finite-bit construction

There exists a bijection pi:[n] -> H satisfying
\[
\left(\prod_{i=1}^n
 [V_i+v_i(\{\pi(i)\})]\right)^{1/n}
\ge\frac{\mathcal B(y)}{c+1}.
\tag{A4}
\]
In particular every factor on the left is strictly positive.

Such a pi can be found deterministically in total bit-polynomial time, using only the finite rational numbers V_i and the n^2 singleton values on H, apart from any input/promise checks. One may compute a true maximum-product perfect matching with factors V_i+v_i({h}). This assertion does not require an exact representation of logarithms or of the generally irrational benchmark B(y).

The finite-bit statement includes zero singleton values and V_i=0: zero-factor matching edges may be excluded, and the conclusion asserts feasibility of a perfect matching using positive-factor edges. It also includes B empty, A empty, and repeated configuration subsets represented by different list entries.

An approximate version is also allowed: for each explicit rational epsilon>0, a deterministic algorithm may instead return pi satisfying
\[
\left(\prod_i[V_i+v_i(\{\pi(i)\})]\right)^{1/n}
\ge\frac{\mathcal B(y)}{(c+1)(1+\epsilon)},
\tag{A5}
\]
with total bit-polynomial complexity in the input and the precision parameter. No guarantee of exact comparison of arbitrary transcendental expressions is assumed.

## B. Deterministic binary-rational explicit-XOS backend

### B1. Exact domain and total output interface

Let n>=1, let U be a finite explicit item set of size m, and give every agent a nonempty finite indexed clause list
\[
v_i(T)=\max_s\sum_{j\in T}p_{i,s,j},\qquad
p_{i,s,j}\in\mathbb Q_{\ge0}.
\tag{B0}
\]
Every coefficient is explicitly given in finite binary encoding. Clause totals need not be one, bounded by one, mutually equal, or on a common numerical grid. Zeros, duplicate indexed clauses, unused items, and clauses of total zero are allowed. Running time in B is polynomial in the total explicit input bit length and the explicit agent, item, and clause counts. There is no dependence on the value of an original denominator, the reciprocal of an original positive coefficient, or an unknown utility scale.

The total algorithm first finds a true maximum-product positive singleton matching tau from all agents to distinct original items, if such a matching exists. If no positive singleton matching exists, it returns the empty bundle for every agent. In this branch the actual optimal NSW is zero and no finite positive fractional benchmark satisfying A1 exists. This includes m=0, all-zero tables, and an agent with no positive singleton.

All following backend constructions concern the positive-matching branch. Put H=tau([n]), B=U\H, and A={i:v_i(B)>0}. Value queries, singleton values, and attaining indexed clauses are obtained by direct rational evaluation of the table. The backend returns rational targets V_i, finite residual configurations, and an actual disjoint allocation. It needs neither an actual optimal allocation nor the comparison benchmark y as an algorithm input. Empty residual item sets and zero residual agents have direct branches.

### B2. Residual normalization and a pure rational solver, with c=2

If A is empty set all V_i=0 and omit the solver. Otherwise let a=|A| and, for each i in A, compute
\[
W_i=v_i(B)>0,\qquad
\widehat p_{i,s,j}=p_{i,s,j}/W_i\ (j\in B),\qquad
\widehat v_i(T)=v_i(T)/W_i\ (T\subseteq B).
\tag{B1}
\]
Every normalized residual clause has total at most one, and at least one clause has total exactly one for each active agent. These are exact rational divisions with polynomial binary length; they are not expansions by the value of 1/W_i.

Use the fixed lift polytope with variables lambda_(i,s), z_(i,s,j) satisfying
\[
\lambda_{i,s}\ge0,\quad\sum_s\lambda_{i,s}=1,\quad
0\le z_{i,s,j}\le\lambda_{i,s},\quad
\sum_{i\in A,s}z_{i,s,j}\le1.
\tag{B2}
\]
Its normalized utility image R consists of
\[
u_i=\sum_{s,j\in B}\widehat p_{i,s,j}z_{i,s,j},
\qquad 0\le u_i\le1.
\tag{B3}
\]
Let b_i=1/a for every i in A. A lift of b is constructed by choosing a clause attaining v_i(B) and assigning every residual item marginal 1/a in that clause. Set
\[
\ell={1\over4a},\qquad h={\ell^2\over2}={1\over32a^2},
\qquad R'=b/4+3R/4.
\tag{B4}
\]

The rational solver starts at x=b with its feasible lift. At each iteration solve
\[
M=\max_{w\in R}\sum_{i\in A}{w_i\over x_i}.
\tag{B5}
\]
The LP must return a basic optimal vertex of the fixed lift polytope with its utility vector w; a fixed deterministic tie rule may be used. If M<=2a stop. Otherwise let y=b/4+3w/4 and update the full lift by the convex combination giving x<-(1-h)x+h y. All points remain in R', with x_i>=ell. The algorithm terminates after at most 128a^3 updates.

Every LP is on the same fixed lambda/z polytope. Its basic-vertex bit bound is independent of the current objective 1/x. Consequently coordinate bit lengths grow additively over polynomially many rational updates, rather than recursively compounding an unspecified LP-output bound. The entire solver has total bit-polynomial cost. It computes no logarithmic potential and uses no minimum-positive-grid assumption.

From the final lift recover finite configurations: for each positive lambda_(i,s), represent the marginals z_(i,s,j)/lambda_(i,s) by nested threshold subsets of B, using at most |B|+1 subsets for that clause, and combine clause distributions. Evaluate actual normalized XOS values and put
\[
\widehat V_i=\sum_T x_{i,T}\widehat v_i(T),\qquad
V_i=W_i\widehat V_i=\sum_T x_{i,T}v_i(T)\quad(i\in A),
\qquad V_i=0\quad(i\notin A).
\tag{B6}
\]
The configurations have row sums one, item columns at most one, polynomial support and polynomial rational bit length. On A they satisfy \widehat V_i>=x_i>=1/(4a) and 0<V_i<=W_i. The targets in original utility units satisfy the full fractional residual bound
\[
\sum_{i\in A,T}z_{i,T}{v_i(T)\over V_i}\le2a
\tag{B7}
\]
for every feasible fractional residual configuration family z, not only for integral allocations or the recovered family. Thus A's residual premise holds with c=2.

### B3. Deterministic welfare rounding that respects a support set

For any finite rational feasible configuration family on a subset of agents, with positive actual expected values U_i, the following deterministic procedure is part of the backend. For every listed configuration T choose an actual clause attaining v_i(T). Initially regard agents' configurations as independent draws from their own finite distributions. An agent drawing T bids p_(i,s,j)/U_i on j in T and zero elsewhere, where s is its chosen attaining clause.

Fix one agent's configuration at a time, enumerating its positive-probability configurations and choosing a conditional-expectation maximizer of the total proxy sum_j max_i bid_(i,j). The conditional expectation is evaluated by exact rational arithmetic from each item's finitely many ordered bid values and CDF products. Give each item with a positive maximum bid to one maximum-bid claimant; unclaimed items may remain unallocated.

The resulting disjoint actual bundles A_i are each subsets of one original positive-support configuration of that agent, and satisfy
\[
\sum_i{v_i(A_i)\over U_i}\ge {1\over2}\#\{i\}.
\tag{B8}
\]
The procedure is deterministic and total-bit-polynomial in the finite configuration representation and coefficient bit length. It observes no label masks. The joint backend conservatively uses d=5/2, although (B8) itself permits d=2.

### B4. Fixed candidate bundles and finite round labels

Let nu_i=max_(j in B) v_i({j}), with max(empty)=0. Put A''={i in A:V_i>=6nu_i}. For agents in A'' use the following finite preprocessing of their recovered configurations.

Discard configurations T of value <V_i/3. For every other T let k=floor(3v_i(T)/V_i). Choose a clause attaining v_i(T). Using that clause's weights, greedily extract k-1 disjoint subsets of weight at least V_i/3-nu_i and at most V_i/3, and use the remaining subset as the kth part. From every part delete items while its actual XOS value exceeds V_i. Inherit the original configuration probability on each resulting part, combine equal parts if desired, and normalize each agent's total inherited mass to one. The modified finite feasible family x' has
\[
 V_i/3-\nu_i\le v_i(T)\le V_i
 \quad\text{on every positive-support configuration}.
\tag{B9}
\]
In this branch nu_i>0 and k<=|T|/2, so no expansion by a tiny coefficient or a reciprocal target is used. Write V'_i=sum_T x'_(i,T)v_i(T); then V_i/6<=V'_i<=V_i.

Set d=5/2 and delta=1/(7d)=2/35. Starting with all agents in A'', apply B3 to x' restricted to the current agents, using U_i=V'_i. Fix the actual candidate bundle S_i for every agent that satisfies v_i(S_i)>=delta V'_i, remove those agents, increment the round index, and repeat. The candidate bundles assigned within one round are pairwise disjoint. The algorithm is deterministic and does not inspect any eventual labels; its candidate sets and round indices are all fixed first.

If a_0=|A''|>0, at least one agent leaves each round, so at most L=a_0 rounds are used. Give every residual item an independent formal label in {0,...,L}, with the rational distribution
\[
\Pr(r_j=t)=\delta(1-\delta)^{t-1}\ (1\le t\le L),
\qquad
\Pr(r_j=0)=(1-\delta)^L.
\tag{B10}
\]
These distributions are an analysis and derandomization interface; the final algorithm draws no random bits. When A'' is empty, omit B4-B5 and take all T_i=empty.

### B5. Candidate-local relative grid and deterministic label mask

Assume A'' is nonempty, so m_B=|B|>=1. For every fixed candidate S_i choose an original clause attaining v_i(S_i), and let w_(i,j) be its original coefficient on j in S_i. These are arbitrary binary rationals. They satisfy
\[
\delta V_i/6\le\sum_{j\in S_i}w_{i,j}=v_i(S_i)\le V_i,
\qquad 0\le w_{i,j}\le\nu_i.
\tag{B11}
\]
Define an internal local grid and shift by
\[
Q=210m_B,\qquad
a_{i,j}={1\over Q}\left\lfloor {Qw_{i,j}\over V_i}\right\rfloor,
\qquad \beta_i={\nu_i\over V_i}>0.
\tag{B12}
\]
The integer grid parameter Q is polynomial in the explicit residual item count, irrespective of the scales of the original coefficients or targets. These local weights obey
\[
0\le a_{i,j}\le\beta_i,\qquad
{\delta\over12}\le\sum_{j\in S_i}a_{i,j}\le1.
\tag{B13}
\]
They are only auxiliary weights for already fixed candidate sets. They do not replace an original valuation, clause, state, job, or processing time.

For a complete label assignment from the finite label space B10 put
\[
A_i(r)=\sum_{j\in S_i}a_{i,j}\mathbf1[r_j=t_i],
\qquad
\Phi(r)=\sum_{i\in A''}\ln{1\over\beta_i+A_i(r)}.
\tag{B14}
\]
The inverse-moment interface used here is the following additive statement. If beta>0, weights a_j in [0,beta], and independent Bernoulli X_j have M=sum_j a_j Pr(X_j=1)>0, then
\[
\mathbb E\ln{1\over\beta+\sum_j a_jX_j}\le\ln{1\over M}.
\tag{B15}
\]
It is not a claim for correlated item masks or a general-subadditive concentration theorem.

Use the finite-grid label-mask algorithm with its tool inputs V_i^(tool)=1, nu_i^(tool)=beta_i, weights a_(i,j), and total potential error epsilon=1. It deterministically fixes one positive-probability label for every residual item with
\[
\Phi(r)\le\mathbb E\Phi(r)+1.
\tag{B16}
\]
The implementation uses exact rational DPs for the distribution of QA_i in {0,...,Q}, with rational logarithm approximations to prescribed absolute errors. It has total bit-polynomial complexity in the original explicit input and all intermediate rational representations, since Q=210m_B and L<=n. In particular a tiny beta_i increases binary precision cost only; it does not cause expansion by 1/beta_i. The total algorithm draws no random bits.

Return T_i={j in S_i:r_j=t_i} for i in A'', and T_i=empty otherwise. They are globally disjoint subsets of the original residual items, and
\[
{v_i(T_i)\over V_i}\ge A_i(r).
\tag{B17}
\]
The asserted output estimate, including the local-grid loss, is
\[
\left(\prod_{i\in A''}{V_i\over\nu_i+v_i(T_i)}\right)^{1/|A''|}
 <{200\over\delta^2}<10000d^2
 \quad(A''\ne\varnothing).
\tag{B18}
\]
No global grid, globally bounded original clause total, sampling success event, or disputed generic-subadditive numerical tail bound is a premise.

### B6. Final rematching and all fractional benchmarks

Find a maximum-product matching sigma from all agents onto H for the positive rational factors v_i(T_i union {sigma(i)}), and output those disjoint actual bundles. True maximum-product singleton and final matchings can be computed in total bit-polynomial time by using the rational product-separation bound to choose sufficient logarithmic precision; zero-factor edges are excluded. There is no demand for exact symbolic logarithms.

For every comparison bijection pi:[n]->H, this deterministic output satisfies
\[
\left(\prod_i v_i(T_i\cup\{\sigma(i)\})\right)^{1/n}
 \ge {1\over60000d^2}
 \left(\prod_i[V_i+v_i(\{\pi(i)\})]\right)^{1/n},
\qquad d=5/2.
\tag{B19}
\]
A zero comparison product makes this inequality vacuous; the algorithm's final product is positive. The comparison matching is not needed by the algorithm.

Consequently, for every finite positive fractional benchmark y satisfying A1 for this same original explicit-XOS object,
\[
\mathsf{NSW}_v\ge{\mathcal B_v(y)\over60000\cdot3\cdot(5/2)^2}
={\mathcal B_v(y)\over1125000}
\ge{\mathcal B_v(y)\over2250000}.
\tag{B20}
\]
The last inequality deliberately retains a factor-two reserve for the unified downstream numerical contract; it is not a random-success or an unproved precision allowance. There is no claim that the algorithm takes the benchmark y or an optimal allocation as input.

### B7. Exact external/source and revision scope

The inherited framework is initial singleton matching, residual set splitting, iteration by satisfied agents, and arbitrary-comparison-matching rematching of Dobzinski--Li--Rubinstein--Vondrak, arXiv:2309.04656v1, Sections 2.1-2.5 and Appendix B:
https://arxiv.org/html/2309.04656v1

Its published actual-integral-OPT theorem is not being restated as a fractional log-CONFIG theorem. B2 replaces the residual solver by a normalized explicit lift and exact rational LP procedure; B3 gives its own deterministic support-respecting XOS welfare rounding. B15 replaces the disputed generic-subadditive concentration route by a shifted additive inverse moment; B16 replaces random labels by a candidate-local finite-grid DP.

The standalone tools are "Weighted Bernoulli shifted inverse moment -- Exact-only v1" and "Finite-grid label-mask logarithmic potential -- Exact-only v1", with their Exact files, independent reviews, author proofs and actual read-after records disclosed in the prior v4 provenance and new v5 record. Their use here is co-developed and known, not blind.

v4's correctly scoped global-grid backend remains an immutable earlier version without a new independent review or full NSW author proof. v5 adds residual normalization and candidate-local relative flooring, which remove that global-grid input restriction and its numerical-Q running-time charge. This strengthened statement is being submitted for a fresh independent Exact-first review. It does not retroactively validate the disputed generic-subadditive B of v3. The present B concerns unweighted explicit XOS; no weighted-agent objective or general-subadditive backend is asserted.

## C. Strong normalized-XOS unit-FSLP conclusion

Let n>=1 agents and m=|U|>=1 original resources be explicit. Each agent g has a nonempty finite indexed menu S_g of binary-rational clauses
\[
v_g(T)=\max_{s\in S_g}\sum_{u\in T}p_{g,s,u},\qquad
p_{g,s,u}\ge0,\qquad\sum_{u\in U}p_{g,s,u}=1.
\tag{C0}
\]
Zeros, unused resources, and duplicate indexed clauses are allowed. The quality of an actual partial allocation is read from one original state per group and a subset of its resources, with the subsets globally disjoint. Equivalently, use the XOS utility v_g on disjoint item sets and recover a maximizing original indexed clause. All utilities are between zero and one.

For P_(g,s)={u:p_(g,s,u)>0}, the explicit unit-FSLP is
\[
\lambda_{g,s}\ge0,\quad\sum_s\lambda_{g,s}=1,\quad
\sum_{g,s:u\in P_{g,s}}\lambda_{g,s}\le1.
\tag{C1}
\]
Coefficients are positive-support indicators, not the private processing-time weights and not zero incidences.

C1. If (C1) is feasible, there is a finite positive fractional configuration benchmark on the original positive supports with B_v(y)=1. The unweighted log-CONFIG LP with original utilities and item capacities at most one has optimum zero. The monotone item-equality version has the same optimum. This does not provide a method to solve a general exponential log-CONFIG LP.

C2. The finder uses the original binary-rational clause table. The residual normalization in B2 and the candidate-local auxiliary floor (B12) are internal arithmetic only. They preserve the identity of every original state and resource and do not change any original coefficient. There is no global replacement of the menu table by a floored grid instance. The local DP grid Q=210|B| is polynomial in the explicit residual item count.

Explicit XOS value, demand and attaining-clause queries are implementable by rational evaluation of the finite table. The algorithm never expands by an original denominator value, inverse tiny coefficient, reciprocal original utility, or reciprocal probability. Intermediate exact ratios are stored in binary rational representation. The returned original state for an output bundle is chosen by maximizing the original, unfloored clause value.

C3. A deterministic total-bit-polynomial finder outputs a genuine disjoint allocation and original indexed states satisfying
\[
\mathsf{NSW}_v\ge {1\over3000000}>2^{-24}.
\tag{C3}
\]
The finite certificate of (C1) may be supplied or first found by deterministic rational LP feasibility. There is no need for a supplied actual optimal allocation. If FSLP is infeasible, no actual unit allocation is asserted, and no general UM infeasibility claim is made.

Fix rho=2^24. For each fixed rational eta in (0,1), let
\[
K=\lceil1/\eta\rceil,\qquad q_\eta=\rho^{-K},
\qquad c_\eta={q_\eta\over2}=2^{-24K-1}.
\tag{C4}
\]
The output satisfies
\[
\#\{g:v_g(T_g)<q_\eta\}<\eta n,\qquad
\#\{g:v_g(T_g)\le c_\eta\}<\eta n.
\tag{C5}
\]
Both thresholds are explicit rational constants for fixed eta. The lower c_eta includes strict safety at the equality boundary. For variable eta, threshold/output arithmetic is polynomial in K and the original bit size; no polynomial-in-log(1/eta) bound is claimed.

C4. Consequently unit-FSLP feasibility alone rules out any fixed-fraction robust-small-quality condition of the following form:
\[
\text{every actual disjoint allocation has at least }\gamma n
\text{ groups of quality }\le\delta,
\quad \gamma>\eta,\quad 0\le\delta\le c_\eta.
\tag{C6}
\]
This is a statement about the same n menu groups, not n machines, incidence jobs, or a different collection of state agents. It does not guarantee a constant minimum quality for all groups.

## D. Shared singleton REPAIR alternatives and deterministic promise decision

This is the only dummy/repair augmentation covered here. It is not the state-dummy SC construction and does not introduce extra agents.

Let an original normalized explicit menu instance Q have n>=1 groups and original resources U. Let D>=0 be an integer. Create D new distinct resources d_1,...,d_D shared globally by all the same n groups. To every group add exactly D indexed alternative states; its ell-th added state has its single positive coefficient one on d_ell. All other coefficients there are zero/absent. Keep every original state, coefficient, and resource. Call this augmented instance Q^+.

D1. If an actual disjoint allocation in Q gives quality one to at least n-D of its original groups, then Q^+ admits an actual allocation of quality one to all n groups. This includes D=0. The group count in Q^+ remains n.

D2. If every actual disjoint allocation in Q has at least gamma n groups of quality at most delta, then every actual disjoint allocation in Q^+ has at least gamma n-D groups of quality at most delta. Groups receiving a shared repair resource still count as original groups. The claim does not assign one repair resource to more than one group.

D3. Fix rational constants 0<=a<gamma<=1 and choose a fixed rational eta with 0<eta<gamma-a. Fix 0<=delta<=c_eta. Suppose D<=a n. Under the promise that the original Q is in one of the following two cases:
- YES: there exists an actual original allocation giving quality one to at least n-D groups;
- NO: every actual original allocation has at least gamma n groups of quality at most delta,

the unit-FSLP of Q^+ is feasible in the YES case and infeasible in the NO case. The promise cases are separated by that test. Outside the promise, either LP outcome is permitted.

Thus deterministic rational LP feasibility for the explicit FSLP of Q^+ is a total-bit-polynomial promise-gap decider. It need not run the deterministic NSW allocation finder. No numerical decision about an unknown integral NSW optimum is required.

The fixed slack gamma-a is essential. Without a positive fixed gap, no constant c_eta follows from this statement. In particular the count bound eta n cannot be silently interpreted in a larger number of variables, clauses, machines, or jobs. The added nD states are explicit; under D<=a n their size is polynomial in n.

For D=0 this includes a deterministic decider for original actual V=1 versus the robust-small-quality NO condition with gamma>eta. If an NP-complete language Karp-reduces to this explicit promise gap with the stated fixed constants, then P=NP. This deterministic conclusion uses the strong FSLP implication C; it does not follow from the published actual-OPT approximation ratio alone.

## E. Complete ordinary flat UM objects and every original job

For either Q or Q^+, the ordinary flat UM matrix has a different private root for every indexed state, a different resource machine for every listed resource, and one original unit selector per group eligible on all of that group's roots. Each state-resource incidence is a distinct original job, with its original private coefficient time or unit time at its resource, and all other endpoints infinite. All zero incidences, unselected states, and unused machines remain.

For any output allocation from C, the algorithm can also output a complete actual schedule of that same original matrix:
- every group selector executes at the root of its recovered original selected state;
- exactly the incidence jobs on its allocated positive resources execute on their original resource machines;
- the other incidence jobs of its selected state remain at that root;
- every incidence job of every unselected state remains on its own original root.

Every incidence identity and selector executes exactly once. If group g receives original quality r_g, its selected root load is exactly 2-r_g. All unselected roots have load one and all resource machines have load at most one. Thus whole-matrix makespan is at most two, and on C outputs fewer than eta n selected group roots can exceed 2-q_eta. This is not a claim that all original machines have makespan at most 2-c_eta.

If an actual unit allocation exists, this complete construction instead has makespan one; the unit selectors imply exact ordinary OPT one. In D1's augmented unit-YES case this includes all newly added repair-state jobs and all original jobs. No job is rounded, deleted, or executed on an algorithmic slot. Residual normalization and the candidate-local auxiliary grid are never substituted as physical processing times.

If S is the original state count and I the original explicit incidence count, Q's matrix has S+m machines and n+I jobs; each original selector has one finite endpoint per state in its group. The repair augmentation adds nD private roots, D resource machines, nD positive singleton incidence jobs, and nD new selector endpoints; it preserves the same n selector identities. Any explicitly listed zero incidences are also retained. Dense output size is polynomial in the explicit augmented input.

## F. Status, quantitative limits, and exclusions

This is the single revised Exact being submitted for independent review. Section A is unchanged from all four earlier versions and remains a general monotone-subadditive semantic matching interface. B is an unweighted explicit-XOS backend, with a different domain and implementation from disputed generic-subadditive B of v3. The old files and all prior objections are preserved without retroactive edits. Nothing asserts that the old generic-SA numerical chain passed review.

v5 specifically strengthens v4 by exact residual row normalization and a local relative grid on fixed candidate clauses. v4 is preserved as a validly scoped process statement; this document does not claim any new independent approval or full author proof for it. The v5 statement itself awaits fresh independent Exact-first review, and this file contains no full author proof.

Only unweighted NSW is covered. B permits arbitrary nonnegative binary-rational explicit XOS coefficients and arbitrary positive finite fractional benchmarks; its time bound is polynomial in their binary descriptions, with no global numerical grid parameter. Its internal local grid is computed from the explicit residual item count. C additionally assumes original normalized clause sums one so that original utilities are at most one. This boundedness is used for the group-count consequences, not as a restriction silently imposed on B.

The primary framework and co-developed replacements are separated in B7. A is the new fractional-benchmark matching step and is not attributed to the source paper as a published log-CONFIG theorem. General XOS is not assumed submodular, and a submodular-only theorem is not being applied to it. No general-subadditive or weighted-agent analogue of the new deterministic backend is asserted. This scope exclusion does not assert an impossibility of weighted approximation relative to actual weighted optimum.

For a unit-FSLP-feasible normalized object and fixed 0<delta<1, if every actual allocation has at least gamma n groups of quality at most delta, then a necessary quantitative consequence of C is
\[
\gamma\ln(1/\delta)\le\ln\rho,\qquad \rho=2^{24}.
\tag{F1}
\]
The prohibited regime is the explicit small threshold delta<=c_eta with gamma>eta, as in C-D. Not every pair of positive constants gamma,delta is prohibited. Gamma may depend on a chosen target delta and remain positive for each fixed delta. No conclusion that a core fraction must tend to zero with the source input size, or that auxiliary size must grow with that input rather than with a fixed target parameter, is asserted.

All cardinality statements use the same n menu groups. They cannot be transferred to a different larger machine/job/state-agent count. C gives a constant unweighted geometric mean and a bound on the number of low-quality groups; it gives no constant minimum quality for all groups. D covers only the explicit shared singleton REPAIR alternatives described there. Its deterministic LP promise decider uses the strong unit-FSLP implication C and is not a consequence of a published integral-OPT ratio alone.

No different shared-dummy mechanism, state-dummy SC bridge, general UM configuration relaxation, source hardness, universal near-two barrier, all-group max-min algorithm, generic UM solver, implemented backend, external-review verdict, global novelty, or additional mature asset ID is asserted. E keeps every original selector and incidence identity and has whole makespan at most two; only its stated selected-root count has the stronger threshold. Exact normalization and local auxiliary flooring never alter physical processing times.

