# Fractional rematching and normalized-menu robust-gap boundary — statement-only Exact v3

Date: 2026-10-18. Prepared by general_query_response_review with root as a separate co-developer after independent primary-source reading and derivations. Scratch only; one final research contract, not registration of v1/v2 as mature claims. The previous versions remain immutable process sources.

This file contains exact hypotheses and conclusions, not the fractional-rematching proof. Section A is byte-for-byte the same standalone matching statement as in v1/v2. Later sections incorporate the conservative factor-three arithmetic correction and the explicitly scoped shared singleton REPAIR interface.

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

## B. External NSW backend: exact source obligation used

This section specifies the external backend used by the joint contract. It is not the literal statement of a published log-CONFIG theorem. The new fractional-benchmark step is A, not an attribution to the source paper.

The primary source actually read is Dobzinski–Li–Rubinstein–Vondrak, arXiv:2309.04656v1, Sections 2.1-2.5, Theorems 1/10/11, Appendix A, and Appendix B's rematching lemmas. The original main theorem compares with integral NSW optimum. The source-level obligations used here are the fractional residual bound from Appendix A and the post-Lemma-8 rounding/rematching comparison. The numerical bound below conservatively keeps the final factor three, rather than relying on the smaller printed end constant or the misprinted intermediate sum in Section 2.5.

B1. For unweighted finite monotone subadditive valuations with a positive singleton perfect matching, the backend selects a maximum-product singleton matching tau, puts H=tau([n]) and B=U\H, and computes a polynomial-support residual fractional solution with rational targets V_i. Its active set is exactly {i:v_i(B)>0}; V_i=0 on the other agents. For c=2 these targets satisfy the full fractional residual premise (A2), in fact with upper bound 2|A|.

B2. With absolute positive success probability, its residual rounding and final rematching produce a feasible actual allocation (S_i) whose NSW satisfies, simultaneously for every comparison matching pi:[n]->H,
\[
\left(\prod_i v_i(S_i)\right)^{1/n}
\ge {1\over60000d^2}
 \left(\prod_i[V_i+v_i(\{\pi(i)\})]\right)^{1/n},
\qquad d=5/2.
\tag{B1}
\]
The algorithm need not know the comparison matching used in the analysis. Its output consists of actual disjoint item subsets. Fixed constant slack and amplification are allowed, with every successful output independently verifiable. The post-Lemma-8 portion uses no integral benchmark allocation in this interface.

B3. On the explicit finite-rational XOS application below, a fixed extra factor at most two is reserved for bit-precision and sampling implementation. Values and demand queries, support construction, rational arithmetic, and random sampling have polynomial total bit cost. No actual optimal allocation, unknown configuration oracle, or derandomization is assumed.

Combining the matching conclusion A with B1-B3 gives a randomized total-bit-polynomial guarantee
\[
\mathsf{NSW}(S)\ge
{\mathcal B(y)\over 2\cdot60000(c+1)d^2}
={\mathcal B(y)\over2250000}
\quad(c=2,\ d=5/2)
\tag{B2}
\]
with absolute positive success probability, for every finite positive fractional benchmark y from A. This is a derived joint contract, not the source paper's original theorem statement.

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

Explicit XOS value, demand, and maximizing-clause queries are implementable in total bit-polynomial time. The algorithm never expands by a denominator value, inverse tiny coefficient, or reciprocal probability.

C3. A randomized total-bit-polynomial finder outputs a genuine disjoint allocation and original indexed states with, at absolute positive success probability,
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
A successful output satisfies
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

Thus deterministic rational LP feasibility for the explicit FSLP of Q^+ is a total-bit-polynomial promise-gap decider. It need not run the randomized NSW allocation finder. No numerical decision about an unknown integral NSW optimum is required.

The fixed slack gamma-a is essential. Without a positive fixed gap, no constant c_eta follows from this statement. In particular the count bound eta n cannot be silently interpreted in a larger number of variables, clauses, machines, or jobs. The added nD states are explicit; under D<=a n their size is polynomial in n.

For D=0 this includes a deterministic decider for original actual V=1 versus the robust-small-quality NO condition with gamma>eta. If an NP-complete language Karp-reduces to this explicit promise gap with the stated fixed constants, then P=NP. This deterministic conclusion uses the strong FSLP implication C; it does not follow from the published actual-OPT approximation ratio alone.

## E. Complete ordinary flat UM objects and every original job

For either Q or Q^+, the ordinary flat UM matrix has a different private root for every indexed state, a different resource machine for every listed resource, and one original unit selector per group eligible on all of that group's roots. Each state-resource incidence is a distinct original job, with its original private coefficient time or unit time at its resource, and all other endpoints infinite. All zero incidences, unselected states, and unused machines remain.

For any output allocation from C, the algorithm can also output a complete actual schedule of that same original matrix:
- every group selector executes at the root of its recovered original selected state;
- exactly the incidence jobs on its allocated positive resources execute on their original resource machines;
- the other incidence jobs of its selected state remain at that root;
- every incidence job of every unselected state remains on its own original root.

Every incidence identity and selector executes exactly once. If group g receives original quality r_g, its selected root load is exactly 2-r_g. All unselected roots have load one and all resource machines have load at most one. Thus whole-matrix makespan is at most two, and on successful C outputs fewer than eta n selected group roots can exceed 2-q_eta. This is not a claim that all original machines have makespan at most 2-c_eta.

If an actual unit allocation exists, this complete construction instead has makespan one; the unit selectors imply exact ordinary OPT one. In D1's augmented unit-YES case this includes all newly added repair-state jobs and all original jobs. No job is rounded, deleted, or executed on an algorithmic slot. Coefficients in (C2) are never substituted as physical processing times.

If S is the original state count and I the original explicit incidence count, Q's matrix has S+m machines and n+I jobs; each original selector has one finite endpoint per state in its group. The repair augmentation adds nD private roots, D resource machines, nD positive singleton incidence jobs, and nD new selector endpoints; it preserves the same n selector identities. Any explicitly listed zero incidences are also retained. Dense output size is polynomial in the explicit augmented input.

## F. Status and exclusions

This is a single unified research Exact for independent review. Section A is identical to the frozen v1/v2 Section A. The source-level backend obligation B has been actually checked against the stated primary reading range with conservative arithmetic, and C-D are the additional fractional-benchmark consequences being submitted for independent review. They are not a literal paper-stated log-CONFIG theorem. No proof of A is included in this statement-only file.

General XOS is not assumed submodular, and submodular-only NSW guarantees do not establish this general-XOS contract. The actual-V=1 promise yields a randomized robust-gap consequence from the published ratio alone; the deterministic LP decider requires the stronger C statement. These two conclusions must not be conflated.

No all-group constant max-min approximation, general UM solver, source hardness, software run, external review, global novelty, or mature asset registration is asserted here. No different shared-dummy mechanism, state-dummy SC bridge, hidden preload, or external lock is included.
