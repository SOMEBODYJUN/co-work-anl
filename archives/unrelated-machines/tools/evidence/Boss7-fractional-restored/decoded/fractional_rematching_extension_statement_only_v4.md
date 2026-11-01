# Fractional rematching and deterministic normalized-menu robust-gap boundary — statement-only Exact v4

Date: 2026-10-18. Prepared by general_query_response_review jointly with root, after disclosed collaborative derivations and actual reading of the two standalone tool records. This is a scratch-only co-developed statement for a new independent Exact-first review. It is not a blind review record, a full author proof, a software claim, or a mature asset registration. All earlier versions and objections remain immutable process sources.

Section A below is byte-for-byte identical to its frozen v1/v2/v3 text. B is a new, strictly scoped deterministic **finite-grid explicit-XOS** backend. C uses the grid backend only after an internal floor with Q=4m, and concerns the original binary-rational normalized menus. The old generic-subadditive v3 numerical backend is not carried forward. Algorithm descriptions below specify the finite input/output contract and are included so the statement is independently auditable; derivations are not included.

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

## B. Deterministic finite-grid explicit-XOS backend

### B1. Exact domain, input charge, and output interface

Let n>=1, let U be a finite explicit item set of size m, and give each agent a nonempty finite indexed clause list
\[
v_i(T)=\max_s\sum_{j\in T}p_{i,s,j},\qquad
p_{i,s,j}\in\{0,1/Q,2/Q,\ldots\},\qquad
\sum_{j\in U}p_{i,s,j}\le1,
\tag{B0}
\]
where Q>=1 is an integer. Zeros, duplicate indexed clauses, unused items, and clauses of total zero are allowed. Running time in B is polynomial in the explicit input bit length, n, m, and the **value** of Q. No total-bit-polynomial conclusion for arbitrary binary Q, or for arbitrary tiny binary XOS coefficients without this charge, is asserted.

The algorithm first finds a true maximum-product singleton matching tau from all agents to distinct original items. If no positive singleton matching exists, it reports that fact. All conclusions below concern the positive-matching branch. Every finite positive benchmark y satisfying (A1) implies that this branch exists. Thus no positive benchmark is excluded by this branch condition. Empty residual item sets and zero residual agents are handled directly.

Put H=tau([n]), B=U\H, and A={i:v_i(B)>0}. A grid value query and an attaining indexed clause are computed directly from the explicit table. The backend returns nonnegative rational targets V_i, finite residual configurations, and one actual disjoint allocation. It uses no actual optimal allocation and does not need the comparison benchmark y as an algorithm input.

### B2. Pure rational residual solver, with c=2

If A is empty set all V_i=0 and omit the solver. Otherwise let a=|A|. Use only the residual coefficients on B. The fixed lift polytope has variables lambda_(i,s), z_(i,s,j) satisfying
\[
\lambda_{i,s}\ge0,\quad\sum_s\lambda_{i,s}=1,\quad
0\le z_{i,s,j}\le\lambda_{i,s},\quad
\sum_{i\in A,s}z_{i,s,j}\le1.
\tag{B2}
\]
Its utility image R consists of the vectors
\[
u_i=\sum_{s,j\in B}p_{i,s,j}z_{i,s,j}.
\tag{B3}
\]
All vectors in R lie in [0,1]^a. Let b_i=v_i(B)/a, and construct a lift of b by choosing one clause attaining v_i(B) and assigning every residual item marginal 1/a in that clause. Let
\[
\ell={1\over4Qa},\qquad h={\ell^2\over2}
 ={1\over32Q^2a^2},\qquad R'=b/4+3R/4.
\tag{B4}
\]

The specified rational solver starts at x=b with a feasible lift. At every iteration solve the rational LP
\[
M=\max_{w\in R}\sum_{i\in A}{w_i\over x_i}.
\tag{B5}
\]
The LP must return a basic optimal vertex of the fixed lift polytope, with its utility vector w; a fixed deterministic tie rule may be used. If M<=2a stop. Otherwise form y=b/4+3w/4 and update the full lift by the same convex combination that gives x<-(1-h)x+h y. Every point remains in R', with x_i>=ell. This algorithm terminates after at most 128Q^3a^3 updates. Its arithmetic, LP calls, and total bit complexity are polynomial in the B1 charge. In particular, the vertex-coordinate bit bound is a bound for the fixed constraint matrix, independent of the current objective 1/x; repeated updates do not recursively compound an LP-output bit bound.

Recover finite configurations from the final lift as follows. For each positive lambda_(i,s), represent the marginals z_(i,s,j)/lambda_(i,s) by nested threshold subsets of B, using at most |B|+1 subsets for that clause. Combine the resulting clause distributions. Evaluate their actual XOS values, not merely their selected-clause sums, and put
\[
V_i=\sum_T x_{i,T}v_i(T)\quad(i\in A),\qquad V_i=0\quad(i\notin A).
\tag{B6}
\]
The recovered configurations have row sums one and item columns at most one; they have polynomial support and rational bit length. They satisfy V_i>=x_i>0 on A and the full fractional residual bound
\[
\sum_{i\in A,T}z_{i,T}{v_i(T)\over V_i}\le2a
\tag{B7}
\]
for every feasible fractional residual configuration family z, not just for the recovered family or for integral allocations. Thus the hypotheses required of the targets in A hold with c=2. The solver uses rational LPs and rational updates only; it never computes a logarithmic potential.

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

### B5. XOS inverse-moment replacement and deterministic finite-grid mask

For each fixed candidate S_i choose a clause attaining v_i(S_i), and let w_(i,j) be its coefficient on j in S_i. These are multiples of 1/Q, sum to at most one, and lie in [0,nu_i]. Let t_i be that agent's fixed round. For a complete label assignment r put
\[
W_i(r)=\sum_{j\in S_i}w_{i,j}\mathbf1[r_j=t_i],
\qquad
\Phi(r)=\sum_{i\in A''}\ln{V_i\over\nu_i+W_i(r)}.
\tag{B11}
\]

The inverse-moment interface used here is specifically the following XOS-valid statement: for independent Bernoulli retention of a fixed set S with probabilities at least p>0, a clause attaining v(S)>0, and nu>=max_j v({j})>0,
\[
\mathbb E\ln{V\over\nu+\sum_{j\in S}w_jX_j}
 \le\ln{V\over p\,v(S)}\quad(V>0).
\tag{B12}
\]
It is not a claim about arbitrary correlated masks or about arbitrary subadditive valuations.

Apply the finite-grid label-mask algorithm with error epsilon=1 to B10-B11. It deterministically fixes one positive-probability label for every item, with
\[
\Phi(r)\le\mathbb E\Phi(r)+1.
\tag{B13}
\]
This implementation uses exact rational DPs for the distribution of the integer weight QW_i in {0,...,Q}, and rational approximations of the finitely many logarithms to a prescribed absolute error. It is polynomial in the explicit input, Q, n, m and L; it does not exactly compare transcendental quantities or expand by 1/nu_i. The standalone interface includes empty item/agent branches.

Return T_i={j in S_i:r_j=t_i} for i in A'', and T_i=empty otherwise. These are globally disjoint actual subsets of B. The asserted numerical output property is
\[
\left(\prod_{i\in A''}{V_i\over\nu_i+v_i(T_i)}\right)^{1/|A''|}
 <{200\over\delta^2}<10000d^2
 \quad\text{when }A''\ne\varnothing .
\tag{B14}
\]
No sampling, success-probability premise, generic-subadditive lower-tail inequality, or claim about the old source constants is used in B12-B14.

### B6. Final rematching and all fractional benchmarks

Find a maximum-product matching sigma from all agents onto H for the positive rational factors v_i(T_i union {sigma(i)}), and output those disjoint actual bundles. True maximum-product singleton and final matchings can be computed in total bit-polynomial time by using the rational product-separation bound to choose sufficient logarithmic precision; zero-factor edges are excluded. There is no demand for exact symbolic logarithms.

For every comparison bijection pi:[n]->H, this deterministic output satisfies
\[
\left(\prod_i v_i(T_i\cup\{\sigma(i)\})\right)^{1/n}
 \ge {1\over60000d^2}
 \left(\prod_i[V_i+v_i(\{\pi(i)\})]\right)^{1/n},
\qquad d=5/2.
\tag{B15}
\]
A zero comparison product makes this inequality vacuous; the algorithm's final product is positive. The comparison matching is not needed by the algorithm.

Consequently, for every finite positive fractional benchmark y satisfying A1 for this same grid object,
\[
\mathsf{NSW}_v\ge{\mathcal B_v(y)\over60000\cdot3\cdot(5/2)^2}
={\mathcal B_v(y)\over1125000}
\ge{\mathcal B_v(y)\over2250000}.
\tag{B16}
\]
The last inequality deliberately retains a factor-two reserve for the unified downstream numerical contract; it is not a random-success or an unproved precision allowance. There is no claim that the algorithm takes the benchmark y or an optimal allocation as input.

### B7. Exact external/source scope

The inherited framework is the initial singleton matching, residual set splitting, iteration by satisfied agents, and arbitrary-comparison-matching rematching of Dobzinski--Li--Rubinstein--Vondrak, arXiv:2309.04656v1, Sections 2.1-2.5 and Appendix B:
https://arxiv.org/html/2309.04656v1

Its published actual-integral-OPT theorem is not being restated as a log-CONFIG theorem. B2 replaces the source relaxation implementation by a fixed explicit lift and rational LP algorithm. B3 supplies its own deterministic support-respecting XOS welfare rounding. B12 replaces the old generic-subadditive concentration route by an additive-clause inverse moment, and B13 replaces random label sampling by the finite-grid DP interface.

The separate standalone statements used in this new assembly are "Weighted Bernoulli shifted inverse moment -- Exact-only v1" and "Finite-grid label-mask logarithmic potential -- Exact-only v1". Their actual Exact files, independent reviews, author proofs and read-after records are disclosed in the accompanying v4 provenance record. They are not being presented as unseen strategies or as additional registered assets. B is restricted to the unweighted grid-XOS domain B0. Nothing here validates the disputed generic-subadditive numerical chain of v3, gives a deterministic arbitrary-binary-XOS NSW theorem with an arbitrary tiny benchmark, or makes the source's original integral benchmark into a fractional one by attribution.

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

C2. For the finite-bit implementation, the algorithm may use only internally
\[
\widetilde p_{g,s,u}={1\over4m}\lfloor4m p_{g,s,u}\rfloor,\qquad
\widetilde v_g(T)=\max_s\sum_{u\in T}\widetilde p_{g,s,u}.
\tag{C2}
\]
These are algorithmic utility coefficients, not changes to original job processing times or to the original instance's state table. Their clause totals belong to [3/4,1], all positive utilities are multiples of 1/(4m), and tilde v<=v. After scaling by 4m, coefficients and utilities are integers at most 4m. The same original-support benchmark satisfies B_(tilde v)(y)>=3/4.

Explicit XOS value, demand, and maximizing-clause queries are implementable in total bit-polynomial time. The algorithm expands only in the internal grid parameter Q=4m, which is polynomial in the original explicit input. It never expands by an original denominator value, inverse tiny coefficient, or reciprocal probability.

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

If an actual unit allocation exists, this complete construction instead has makespan one; the unit selectors imply exact ordinary OPT one. In D1's augmented unit-YES case this includes all newly added repair-state jobs and all original jobs. No job is rounded, deleted, or executed on an algorithmic slot. Coefficients in (C2) are never substituted as physical processing times.

If S is the original state count and I the original explicit incidence count, Q's matrix has S+m machines and n+I jobs; each original selector has one finite endpoint per state in its group. The repair augmentation adds nD private roots, D resource machines, nD positive singleton incidence jobs, and nD new selector endpoints; it preserves the same n selector identities. Any explicitly listed zero incidences are also retained. Dense output size is polynomial in the explicit augmented input.

## F. Status, quantitative limits, and exclusions

This is the single revised Exact being submitted for independent review. Section A is unchanged from all three earlier versions and remains a general monotone-subadditive semantic matching interface. B has a different valuation domain and a different deterministic implementation from the disputed B of v3. The old files and the rank v3 objections are preserved without retroactive edits. No part of this file is a claim that the old generic-SA numerical source chain passed review.

The actual source framework and the co-developed replacements are separated in B7. A is the new fractional-benchmark matching step; it is not attributed to the source paper as a published fractional log-CONFIG theorem. The final v4 statement has not yet undergone its new independent Exact-first review, and this file contains no full author proof.

Only unweighted NSW is covered. Grid cost is polynomial in Q by value, and the original binary-rational normalized application C uses Q=4m. Internal utility flooring never modifies the original menu object, an original job, or a physical processing time. Nothing asserts deterministic constant NSW for an arbitrary tiny benchmark in an unrestricted binary XOS instance.

For a unit-FSLP-feasible normalized object and fixed 0<delta<1, if every actual allocation has at least gamma n groups of quality at most delta, then a necessary quantitative consequence of C is
\[
\gamma\ln(1/\delta)\le\ln\rho,\qquad \rho=2^{24}.
\tag{F1}
\]
In particular the prohibited regime is the explicit small threshold delta<=c_eta with gamma>eta, as in C-D. The statement does not prohibit every pair of positive constants gamma,delta. Gamma may depend on a chosen target delta and still be a positive constant for each fixed delta. No conclusion that a core fraction must tend to zero with the source input size, or that auxiliary size must grow with that input rather than with a fixed target parameter, is asserted.

All cardinality statements use the same n menu groups. They cannot be transferred to a different larger machine/job/state-agent count. C gives a constant unweighted geometric mean and a bound on the number of low-quality groups; it gives no constant minimum quality for all groups. Weighted NSW, arbitrary shared-dummy mechanisms, state-dummy SC, and general UM configuration relaxations are outside this contract.

D concerns only the explicit shared singleton REPAIR alternatives described there. Its deterministic LP promise decider follows from the strong unit-FSLP implication C; it is not a consequence of a published actual-integral-OPT ratio alone. General XOS is not assumed submodular, and a submodular-only theorem is not being applied to it.

No source hardness, universal near-two barrier, all-group max-min algorithm, generic UM solver, implemented backend, external-review verdict, global novelty, or additional mature asset ID is asserted. The ordinary UM conclusion E keeps every original selector and incidence identity and has whole makespan at most two; only the stated selected-root count has a stronger threshold.

