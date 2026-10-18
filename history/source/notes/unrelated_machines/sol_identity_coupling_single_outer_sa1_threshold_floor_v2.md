# One outer private-home/fallback core: full-SA1 gives epsilon-squared quality

Status: scratch structural rounding deduction. This v2 changes the threshold domain of the earlier unit-only learning note; that frozen note remains unchanged. It is not a theorem for general multicore menus, not a near-zero gap, and not a claim that every second-moment point has an actual joint state distribution. PSD is not needed for this restricted structure.

## 1. Complete physical domain and common SA1 system

There is exactly one outer group `M`, with finite indexed states `a`. State `a` has its own set of home resources `g_(a,j)`, `j in J_a`, with positive binary-rational weights `w_(a,j)` summing to one. All these homes are distinct over `(a,j)`.

For every `(a,j)` there is one helper group `H_(a,j)`. Its own indexed state is the singleton `g_(a,j)`, coefficient one. Its other states are arbitrary normalized nonnegative binary-rational fallback states on a finite resource set `B` disjoint from all homes. Fallback supports may overlap arbitrarily, including across different outer states. There are no other groups and no unprotected auxiliary cores.

Use the full ordinary normalized-flat UM matrix: one unit selector per group eligible at that group's distinct state-private machines; one original incidence job per listed state-resource pair, with time its original coefficient at its private state machine and time one at its exact resource machine; all remaining cells infinity. All unselected-state jobs and any listed zero incidences remain present. No logical side constraints are added to the actual schedule.

Fix a rational threshold `0<epsilon<=1`. For binary state indicators `A_(g,s)` and claim indicators `Z_(g,s,u)`, the base system is

\[
 \sum_s A_{gs}=1,\quad
 0\le A_{gs},Z_{gsu}\le1,\quad Z_{gsu}\le A_{gs},
\tag{1}
\]
\[
 \sum_{g,s}Z_{gsu}\le1\quad(u\in U),\qquad
 \sum_u p_{gsu}Z_{gsu}\ge\epsilon A_{gs}\quad(g,s).
\tag{2}
\]

Every row of (1)–(2) is multiplied by every one of the **same** original `A/Z` primitives and by its complement. First and symmetric second moments belong to one common array, and `Y_XX=x_X` for each binary primitive. All nonnegative/box/gate rows are included. This is the literal strong primitive-SA1 system used below. Adding whole-core quality rows, unit-FSLP rows or M1 PSD does not invalidate the conclusion.

**Conclusion.** Given a rational feasible common SA1 point, one can deterministically construct, in total-bit polynomial time, a disjoint all-group actual allocation and a complete ordinary schedule with

\[
 \boxed{V\ge\epsilon^2/4,\qquad
 C_{\max}\le2-\epsilon^2/4.}
\tag{3}
\]

For every fixed positive epsilon this rules out vanishing quality in this exact one-outer architecture. It makes no conclusion for several simultaneous outer groups or for auxiliary groups without own homes.

## 2. Singleton own states become exact across all pair moments

For any helper own state, denote its state indicator by `A` and its unique claim by `Z`. Its base rows give `Z<=A` and `Z>=epsilon A`. Multiply the latter by `1-Z`. Using `Z^2=Z` gives

\[
 Y_{AZ}\ge x_A.
\]

The box row `A<=1`, multiplied by `Z`, gives `Y_AZ<=x_Z`. Together with the first-moment gate `x_Z<=x_A`, these imply

\[
 x_A=x_Z=Y_{AZ}.
\tag{4}
\]

For any *other* primitive `F`, multiply the nonnegative gate `A-Z>=0` by `F` and by `1-F`. Since its first-moment slack is zero by (4), both inequalities force

\[
 Y_{AF}=Y_{ZF}.
\tag{5}
\]

This argument uses only degree-two rows already in the same SA1 array. It does not condition a conditioned point a second time or introduce an unprovided triple moment. Thus every own singleton's claim equals its state indicator under every original primitive condition.

## 3. One outer-state condition gives joint fallback claims

Choose any outer state `a` of positive marginal `lambda_a` and condition the common moments on `A_(M,a)=1`. By construction every base row is feasible under this single condition. Write `b_j` for the resulting conditional claim on home `g_(a,j)`. The outer quality row says

\[
 \sum_{j\in J_a}w_jb_j\ge\epsilon.
\tag{6}
\]

Let `f_j` be helper `j`'s total conditional fallback-state mass. Its own claim equals its own-state probability by (5); the home resource capacity therefore yields

\[
 f_j\ge b_j.
\tag{7}
\]

For a helper fallback state `s`, denote its conditional state mass by `mu_js` and its conditional claims by `t_jsu`. The same condition gives all the rows

\[
 \sum_s\mu_{js}=f_j,\qquad
 0\le t_{jsu}\le\mu_{js},\qquad
 \sum_u p_{jsu}t_{jsu}\ge\epsilon\mu_{js},
\tag{8}
\]
\[
 \sum_{j\in J_a,s}t_{jsu}\le1\qquad(u\in B).
\tag{9}
\]

Rows of all other helpers/cores were present under the condition; their nonnegative claims can be omitted to obtain (9). Equations (8)–(9) are **one common** fallback point. They are not separately chosen perspective flows, and there is no claim that this conditional point is integral.

## 4. A real fallback allocation has weighted welfare at least epsilon-squared/2

Independently for every helper in this row, choose fallback state `s` with probability `mu_js`, or choose inactive with probability `1-f_j`. Given a chosen fallback state of positive `mu_js`, independently request resource `u` with probability `t_jsu/mu_js`. Zero state mass has zero claims and requires no division. At every requested resource, give it uniformly to one requesting helper. This is a legitimate disjoint actual fallback allocation.

The marginal request probability of helper `j` at `u` is `sum_s t_jsu`; (9) bounds the total by one. Conditional on one helper's selected state and its request for `u`, the other helpers' request indicators remain independent of it and have expected total at most one. If that number is `N`, the integer inequality

\[
 \frac1{1+N}\ge1-N/2
\]

therefore gives conditional winning probability at least one half. Hence the selected-state value `q_j` in this actual random allocation obeys

\[
 \mathbb E q_j\ge\frac12\sum_{s,u}p_{jsu}t_{jsu}
 \ge\frac\epsilon2 f_j.
\tag{10}
\]

Inactive helpers have `q_j=0`; always `0<=q_j<=1`. Weighting (10) by the original outer coefficients, and using (6)–(7), gives

\[
 \mathbb E\sum_jw_jq_j\ge\epsilon^2/2.
\tag{11}
\]

No all-group quality guarantee is asserted for this temporary fallback allocation; it is only a welfare estimate used in the next recombination.

## 5. Deterministic bit-polynomial realization of that welfare bound

For completeness, the expectation in (11) can be derandomized without a welfare oracle. Choose helper states one at a time by conditional expectation. Under any partial choices the remaining helpers' state choices are still independent. For every resource `u`, compute for every helper its conditional request probability `r_ju` and its conditional weighted value-request mass

\[
 m_{ju}=w_j\,\mathbb E[
 p_{j,s,u}\,\mathbf1\{j\text{ requests }u\}].
\]

The expected welfare at that resource is exactly

\[
 \sum_jm_{ju}\,
 \mathbb E\frac1{1+N_{-j,u}},
\tag{12}
\]

where `N_(-j,u)` is a sum of independent Bernoulli variables with parameters `r_hu`, `h!=j`. Its distribution is computed by the usual count-convolution DP with at most the explicitly present number of helpers as count. All parameters are exact rationals determined by the supplied point and the partial state choices. Summing (12) over resources computes the full conditional expectation. One candidate state/inactive choice attains at least its current expectation; choose such a candidate and continue.

After all states have been chosen, allocate each resource deterministically to a chosen-state helper maximizing `w_j p_jsu` among helpers having positive request probability there, or leave it unused if none. This value is at least the expected value from the remaining request coins and uniform-winner step, resource by resource. The resulting actual selected-state values therefore satisfy

\[
 \sum_jw_jq_j\ge\epsilon^2/2.
\tag{13}
\]

The DP, candidate scans and state choices are polynomial in the explicit instance and rational point size. Products/sums involve polynomially many input rationals; the count factors `1/(1+N)` use denominators at most the helper count, so all intermediate bit lengths are polynomial. No loop over `1/epsilon`, a weight denominator, or an implicit number of states is needed.

## 6. Actual all-group recombination and all original jobs

Put `tau=epsilon^2/4`, and let `R={j:q_j>=tau}`. Their total outer weight `W_R` satisfies

\[
 \epsilon^2/2\le W_R+\tau(1-W_R),\qquad
 W_R\ge\frac{\epsilon^2}{4-\epsilon^2}\ge\tau.
\tag{14}
\]

Keep the pairwise-disjoint fallback bundles only for helpers in `R`. Give their distinct original home resources to the outer group in state `a`. Give every other helper, including every helper of every other outer state, its own home. Because `B` is disjoint from every home and there are no other groups, this is a genuine disjoint all-group allocation. The outer group obtains at least `W_R>=tau`, retained fallback helpers obtain at least `tau`, and all remaining helpers obtain one.

Finally put every original selector at its witnessing original state. Export only that selected state's allocated original incidence jobs, and keep every other original incidence job at its own private machine. Every original unselected state still contributes its complete normalized private load one. Selected private machines have load at most `2-tau`; resource machines have at most one unit job; zero incidences may remain at their own zero endpoints. This proves (3) as a complete actual schedule rather than a partial conditional allocation.

## 7. Scope and remaining main obligation

The independent-state/contention estimate is a standard welfare tool; no novelty for that estimate or conditional-expectation machinery is claimed. This record isolates where strong all-other-core SA1 conditions give a real rounding consequence for a proposed one-outer weight-compression architecture. At epsilon one it recovers the earlier `1/4` floor, without requiring a PSD point or an actual conditional joint distribution.

If several outer cores choose rows simultaneously, the separate conditional points in §3 need not form a joint resource-feasible fallback point. If extra fallback auxiliary groups have no private home, §6 cannot restore low-value ones to own resources. Those are genuine limits. This record provides neither a general normalized multicore approximation nor the requested strong-SA1/M1-PSD near-zero counterexample. Directly nesting a contextual menu must account for those missing joint conditions and all auxiliary groups, rather than treating one conditional fallback point as a global solution.
