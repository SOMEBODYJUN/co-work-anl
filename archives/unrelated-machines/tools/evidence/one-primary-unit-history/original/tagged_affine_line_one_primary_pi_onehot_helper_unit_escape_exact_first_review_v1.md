# Tagged affine LINE / one-primary / PI / onehot helper — independent Exact-first review v1

Reviewer: general_query_response_review. Date: 2026-10-18.
Verdict: VALID. No counterexample, fatal issue, or standing objection found.

## 1. Actual reading and exact reviewed object

I actually read the entire statement-only Exact

/workspace/scratch/038d9dcc4cac/tagged_affine_line_one_primary_pi_onehot_helper_unit_escape_exact_v1.md

SHA256: 59e71e7d7c496b9dda2a993af5d0253072601190b5e78a8599dd06093fb47bbd.

The source ID is UM-TAGGED-AFFINE-LINE-ONE-PRIMARY-PI-ONEHOT-HELPER-UNIT-ESCAPE-v1.

Before this independent reconstruction I did not read an author Proof, root derivation, or other agent's new rainbow strategy. The source itself discloses that root had seen earlier strategy messages; this review makes no claim that root was blind. I use only the supplied exact hypotheses, elementary finite-field geometry, and a finite matching argument proved below. The standard rational-LP feasibility theorem is used only to check the optional LP-certificate-finding clause, not as an oracle for an unknown actual allocation.

This file is a new scratch-only frozen record. No original source or repository/Work/Git file is changed.

## 2. Fix the arbitrary specified main state and condition each helper

Let s_M be the main indexed state specified by the input request. For each primary variable x in P, write
\[
t_x=a_{M,s_M}(x).
\]
Keep every intercept j_x(g) exactly as input. In particular, do not normalize the main intercept to zero or relabel the groups.

For a helper h with its unique primary u=u(h), retain its states whose primary label equals t_u. The primary marginal condition gives
\[
\sum_{s:a_{h,s}(u)=t_u}\lambda_{h,s}=1/R.
\]
Thus this set is nonempty. Define the conditional state probabilities
\[
\mu_{h,s}=
\begin{cases}
R\lambda_{h,s},&a_{h,s}(u)=t_u,\\
0,&\text{otherwise}.
\end{cases}
\tag{1}
\]
They sum to one, including when some original state probabilities are zero. If only a real feasible lambda exists, (1) is a mathematical conditional distribution; none of the matching algorithm below needs to evaluate that real distribution.

For each auxiliary x in A_h and each a in F_R, the given primary-auxiliary equalities imply
\[
\sum_{s:a_{h,s}(x)=a}\mu_{h,s}
=R\sum_{s:a_{h,s}(u)=t_u,\ a_{h,s}(x)=a}
 \lambda_{h,s}
=1/R.
\tag{2}
\]
No joint distribution between different auxiliary labels is needed. Helpers in different primary blocks may be conditioned on different t_u; (2) still holds separately for each helper.

## 3. Primary geometry separates main and helper positive cells

Every retained state of h has, on u, the line
\[
L_{h,u}=\{(u,z,t_u z+j_u(h)):z\in F_R\}.
\]
It is independent of h's remaining labels or indexed state. The main line on u is
\[
L_{M,u}=\{(u,z,t_u z+j_u(M)):z\in F_R\}.
\]
Their slopes coincide and their fixed intercepts differ, so they are disjoint. For distinct helpers with the same primary u, their lines are likewise pairwise disjoint, because their intercepts on u differ. Different primary variables have disjoint tags.

Main participates in no auxiliary. Therefore every onehot positive cell of a retained helper state is disjoint from all main positive cells:
- if the cell lies on its primary, it lies on L_(h,u), disjoint from the whole main line;
- if it lies on an auxiliary, its tag is absent from main.

This avoids the entire main line, not merely a designated parking point or the current subset of main positive cells. It works for any fixed main state, any state-dependent main norm-one weight pattern, and arbitrary nonzero main intercepts.

For primary tagged cells, at most one helper can assign positive conditional probability to that cell. Indeed every helper participating in that primary is conditioned to the same slope, and the corresponding lines are pairwise disjoint. Thus total conditional onehot mass at a primary cell is at most one.

## 4. Auxiliary geometry gives unit column capacities

Let e_h(s) denote the unique positive cell of helper h's full original indexed state s. Its value is exactly one by the all-states onehot hypothesis.

Fix an auxiliary x and a tagged cell c=(x,z,y).

If z=0, the line of helper h on x can contain c only when y=j_x(h), regardless of its slope. Intercepts of all helpers participating in x are distinct, so at most one such helper can ever use c. Its conditional probability of choosing c is at most one. Hence the total mass at c is at most one.

If z is nonzero, for a particular h participating in x, membership of c in its line forces the unique slope
\[
a=(y-j_x(h))/z\quad\text{in }F_R.
\]
The event e_h(s)=c is a subset of that slope-label event. By (2),
\[
\Pr_{\mu_h}[e_h(s)=c]\le1/R.
\tag{3}
\]
This inequality holds even when the onehot cell is an arbitrary adversarial function of the entire original state, all its auxiliary labels, its intercepts, and other input data. It uses only the necessary condition that its positive cell lies on its stated line.

There are at most R helpers participating in x, by the distinct-intercept hypothesis and the fact that no main group participates in x. Summing (3) therefore gives total mass at most one.

The z=0 and z!=0 cases are both necessary. Uniform slope alone would not give a 1/R bound at z=0; fixed distinct intercepts supply the correct bound there. Arbitrary sharing of any auxiliary between different primary blocks is allowed in this argument. It uses neither independent helpers nor independent auxiliary coordinates.

## 5. Hall matching selects real full indexed states

Make a finite bipartite graph:
- left vertices are all helpers h;
- right vertices are original tagged resource cells;
- an edge (h,c) exists if some original indexed state s of h has primary label t_(u(h)) and onehot cell e_h(s)=c.

Store one such complete original state as an edge witness. The graph may include conditioned states with lambda zero; this is legal. Alternatively it may retain only states with positive conditional mass. The former option has the advantage that the construction needs no numerical lambda at all.

All graph right cells are disjoint from main's positive cells by Section 3. Define a fractional edge assignment, only for the proof, by
\[
w_{h,c}=\sum_{s:e_h(s)=c}\mu_{h,s}.
\]
Every helper row sums to one. Sections 3-4 show that every resource column sums to at most one. Each positive w lies on an edge of the displayed graph.

For any helper subset B, let N(B) be its resource neighborhood. Then
\[
|B|=\sum_{h\in B,c}w_{h,c}
\le\sum_{c\in N(B)}1=|N(B)|.
\tag{4}
\]
Thus the finite graph satisfies the matching condition for all left subsets.

A deterministic augmenting-path matching covers every helper. To see existence directly, if a maximum matching omitted a helper, the alternating-reachable left set B from unmatched left vertices would have fewer adjacent right vertices than left vertices: all reached right vertices are matched, and their matched left partners are in B, while at least one reached left vertex is unmatched. This contradicts (4). A fixed vertex/edge order makes the construction deterministic; at most |H| augmentations suffice.

For each matched edge, choose its stored original indexed state. This is a genuine whole input state: its complete slope vector and its onehot cell are taken together from the table. The algorithm never independently splices a primary label, auxiliary labels, and a cell from incompatible states.

Matched positive cells are pairwise distinct. They also avoid every main positive cell. Give each helper its matched onehot cell and give main all positive cells of its specified original state. Each helper receives mass one, and main receives mass exactly its original normalization sum one. Full selected supports need not be disjoint: in particular auxiliary zero cells may overlap arbitrary other selected supports. They are not selected positive resources and create no allocation conflict.

Every state is norm one, so no partial resource allocation can give a group mass above one. The displayed simultaneous allocation gives all groups mass one, hence V=1.

## 6. Explicit finder, local certificates, and real-existence version

With rational lambda supplied, all marginal equalities, nonnegativity, and normalization can be checked by exact rational summation in polynomial total bit time. The matching construction uses the actual state table and its unique positive cell; it need not sample lambda or expand probabilities into copies. Zero-probability states cause no difficulty.

More strongly, under the promise that a real feasible lambda exists, the same direct table graph in Section 5 can be built and matched without obtaining lambda first. Its existence proves (4), while the graph and deterministic matching are purely explicit. Thus the actual finder is not an inference from a nonconstructively given optimal actual allocation.

The source's optional LP-first route is also valid. For each helper, it has |S_h| nonnegative variables, a normalization equation, R primary-marginal equations, and |A_h|R^2 primary-auxiliary equations, all on the explicit indexed-state table. Coefficients are zero/one and right sides are 1, 1/R, or 1/R^2. Their encoding lengths and row counts are polynomial in the complete explicit input. Unused auxiliary variables create no extra hidden state variables.

If feasible over the reals, this bounded rational polytope has a rational vertex of polynomial bit length. For example, a basic solution uses a nonsingular zero/one matrix of dimension at most |S_h|, and the common right-side denominator R^2 together with determinant bounds gives polynomial numerator/denominator bit lengths. Standard deterministic rational linear-programming feasibility can find a rational feasible certificate in polynomial total bit time. This is the only standard LP algorithmic dependency in the optional route; it is not general UM feasibility or a configuration oracle.

If that LP is infeasible, reporting failure of this interface is correct. It does not imply the underlying ordinary UM matrix is infeasible at unit load, because another actual allocation or different labels might still work outside the PI premise. Conversely, the existence promised in this Exact gives all the matching conclusions without any unknown global source-label assignment or source-CSP solution.

## 7. Construct the complete ordinary actual schedule

Fix the chosen main state and the matched original helper states. Let s_g be the resulting selected state for each group. Use only the original P endpoints as follows:

1. Put the original unit selector of group g on the private root of s_g.
2. For each positive incidence job of s_g, put that original job on its own original resource machine, where its time is one.
3. Put every zero-weight incidence job of s_g on that selected private root.
4. For every unselected indexed state of every group, put every one of its original incidence jobs, positive or zero, on its own private root.

This covers all selectors and all incidence identities exactly once. Unselected states are not deleted, and no zero incidence is silently omitted.

Every selected private root has one unit selector plus only zero-time incidence jobs, so load one. Every unselected private root has all of its state incidences, whose original private times sum exactly one, so load one. The offloaded resource jobs are exactly the selected positive cells. They are globally distinct by the matching and primary-line arguments; hence every resource machine receives at most one unit job. All unused cells/planes are empty original machines with load zero.

Thus all original machines simultaneously have load at most one. There is at least one original selector, namely main's, and every selector has only unit finite endpoints. Any complete actual schedule therefore has makespan at least one. The constructed complete schedule has C_max=1, proving OPT(P)=1.

This argument is a direct complete original-job proof, not just a V=1 invocation of an abstract value bridge. It does not require the selected complete line supports to be disjoint: zero selected jobs remain privately executed, and all unselected jobs remain on their own roots.

## 8. Exact counts and total bit complexity

Within one state, variable tags are disjoint and each line has R distinct points, one per z. Thus that state has exactly R|X_g| different resource incidences, and
\[
I=R\sum_g|S_g||X_g|
\]
is the exact total number of incidence jobs. The complete P has:
- S private roots plus (|P|+|A|)R^2 original resource machines;
- n=1+|H| unit selectors plus I original incidence jobs;
- S selector finite endpoints plus 2I incidence finite endpoints.

Zero private times are included in those counts. Dense matrix dimensions are products of polynomially many explicitly represented objects, so materialization is polynomial in the stated expanded input. Unused auxiliary planes are retained among the original machines.

The graph can be built by reading every helper state once, testing its primary label against the chosen main state, and extracting its unique positive cell from the original full weight table. After coalescing duplicate h/c edges, it has at most sum_h|S_h| edges and at most that many relevant right cells. A cached original indexed state witnesses each edge. Repeated indexed label vectors, different onehot choices for identical vectors, and duplicate cell edges are all handled by keeping original state identities.

Matching is polynomial in the explicit graph. Main positive-cell extraction and the complete schedule output take polynomial time in I+S+the full plane list. Exact field arithmetic and rational checks cost polynomial bit time; R is a promised prime, so nonzero z has an inverse in F_R. No algorithm changes any input intercept. The geometric inverse used in the proof can also be computed by polynomial-bit field arithmetic if desired; the table-based finder need not enumerate inverses at every cell.

There is no R!, reciprocal-lambda, rational-denominator-value, or hidden-configuration expansion. Multiplying rational lambda by R in (1) adds only O(log R) bit length. The optional rational LP has explicitly polynomial size, and the direct matching finder does not require computing conditional probabilities.

This does not promise poly(log R) time for a compact/oracle input that has not expanded the R^2 resource planes or all state incidences. R, all variables, all states, and all full line weight tables are charged according to the supplied explicit representation.

## 9. Edge cases and exact exclusions

- H empty: matching is empty; main's arbitrary specified state already gives mass one and the complete unit schedule above.
- A empty: helpers only use their unique primary; conditioning gives disjoint parallel primary lines directly.
- Unused auxiliary variables: their original full resource planes remain empty in the output, and do not alter capacities.
- R=2: the same field and bounds apply, including conditional probabilities 1/2 and 1/4 and the z=0 case; no asymptotic or strict-large-R argument is used.
- Zero main weights: only its positive cells are offloaded, while all of its selected zero jobs remain with the selector.
- Zero helper-state probability: it does not remove that original state or its jobs; the all-conditioned-state graph may use such a state if matched, and its complete original labels/cell are still legal.
- Arbitrary onehot cell choice: the auxiliary nonzero-z proof needs only its membership in the original line, so even fully state-dependent choices obey (3).
- Main intercept nonzero: equal slope plus unequal actual intercept is sufficient; no coordinate renumbering is needed.
- Arbitrary shared auxiliaries: degree at most R and helper-local conditional uniformity suffice; no auxiliary joint independence or global consistency is required.

The proof genuinely uses each helper's single primary, the onehot property for every original state, main's absence from auxiliary variables, distinct fixed intercepts, and the primary-auxiliary pairwise marginals. It does not cover diffuse helper states, extra groups, external preloads, helpers with several primaries, or missing conditional marginals.

The output is not a global source-label assignment and does not show source CSP satisfiability. It does not identify the family with any Chan/LST hard image, prove new hardness, or rule out every pairwise-independent line construction. Its conclusion is precisely the stated actual unit escape for this explicit interface.

## 10. Final assessment

Every clause of the Exact holds, including arbitrary preselected main state, all legal original helper indexed states, arbitrary helper-only auxiliary sharing, explicit rational local PI certificates or real feasibility, V=1, a full original-job unit schedule, OPT=1, and deterministic total-bit-polynomial construction on the expanded input.

No correction is requested. No author Proof, code, finite experiment, or other agent's derivation was read as part of this first-stage independent reconstruction. A future author-Proof or canonical read-after must be recorded separately without changing this file.
