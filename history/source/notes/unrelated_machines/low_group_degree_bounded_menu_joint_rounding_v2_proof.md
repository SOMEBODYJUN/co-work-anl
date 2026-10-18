# Proofs v2: degree-two bounded-menu weighted UM approximation

Paired Exact file: `low_group_degree_bounded_menu_joint_rounding_v2_exact.md`.

Candidate identity: `UM-DEGREE-TWO-BOUNDED-MENU-JOINT-ROUNDING-v2`.

Frozen scratch proof, 2026-10-18. Exact was supplied for independent review before this proof was written. Root independently reconstructed the group-average mechanism, exact UM/XOS identity, relative bound, and normalization before authorizing this proof. No independent reviewer is claimed to have read this proof yet. The new mechanism after importing the published additive algorithm is precisely group averaging, original-job UM accounting, and private-bonus normalization. It is a direct structural corollary, not a new additive Santa Claus algorithm or a general unrelated-machines approximation.

## 1. Elementary schedule from a disjoint weighted allocation

Assume first that every state's total private work is 1. Given pairwise disjoint original resource sets B_g, select a state s(g) attaining f_g(B_g). Such a state exists because every menu is finite and nonempty. Trim B_g to its intersection with this chosen state; this neither changes its achieved value nor creates a resource conflict.

Place selector J_g at M_g,s(g). For each resource u in the trimmed B_g, export precisely the chosen state's incidence job I_g,s(g),u to R_u. Keep every other incidence job at its own private state machine. In particular all jobs of every unselected state are kept, not deleted or silently treated as absent.

Each resource machine gets at most one exported unit job. Each unselected state machine gets private load exactly 1 and no selector. The chosen state machine's actual load is

`1 + sum_{u in S_g,s(g) minus B_g} p_g,s(g),u = 2-f_g(B_g)`.

All original jobs are assigned once to an original eligible machine. Since each achieved value lies in [0,1], the total makespan is at most `2-min_g f_g(B_g)`; the lower bound of 1 from selectors is already included in this expression. This proves the upper half of the identity in Exact B:

`OPT(P) <= 2-V`.

## 2. Exact normalized UM/XOS identity, including the endpoint OPT=2

Selectors give OPT(P)>=1. Parking all incidence jobs privately and placing every selector at an arbitrary state machine gives OPT(P)<=2. The allocation space is finite, and the ordinary machine-assignment space is finite, so both V and OPT(P) are attained.

Let an optimal original-job schedule have makespan C<2. A group selector chooses a unique indexed state machine. Move all jobs of every unselected state back to that state's own machine. Their total private load is 1, at most C; there is no selector there, and no other state's job has an eligible edge to this private machine. This change does not increase makespan and only frees resources.

Let B_g be the resources receiving jobs from group g's selected state. As resource processing times are exactly 1 and C<2, no resource receives two such jobs. Thus these B_g are pairwise disjoint. The selected root has its unit selector plus precisely the unexported portion of its total private work 1. If its exported weight is a_g, its load is `2-a_g`, so a_g>=2-C. Since f_g(B_g) is the maximum over states, f_g(B_g)>=a_g. Consequently V>=2-C, which gives C>=2-V.

If OPT(P)=2, then V must be zero: a positive V would give the complete schedule of Section 1 with makespan strictly below 2. Thus equality also holds at this endpoint. We have proved

`OPT(P)=2-V`, `0<=V<=1`, `1<=OPT(P)<=2`.

Zero private jobs do not affect the argument: they may remain privately even at a selected root, contribute no weight, and need not be exported. Their identities are still present in the original schedule.

## 3. Group-level averaging preserves the choice coupling

For each group define the additive valuation

`v_g(B)=(1/K_g) sum_{s in A_g} a_gs(B)`.

Every a_gs(B) is nonnegative. The average is at most their maximum, and the sum is at least their maximum. Hence, pointwise,

`f_g(B)/K <= f_g(B)/K_g <= v_g(B) <= f_g(B)`.

There is one auxiliary agent for a whole original group. We have not expanded it into separately satisfied state agents, and the final maximum still selects one single state.

Take an allocation attaining V for the XOS functions. For every group its additive-average value on the same bundle is at least V/K. This is a valid disjoint additive allocation, proving that the auxiliary additive max-min optimum A is at least V/K.

For any auxiliary item u, its positive-value agents are a subset of the original groups whose menus contain u. There are at most two such groups by hypothesis, even if u occurs in many states of either group. The auxiliary instance therefore satisfies the published degree-two additive input condition directly at the group level.

## 4. Importing the published additive algorithm and recovering original jobs

Apply Verschae--Wiese, arXiv:1011.4957v1, Section 5.1, Theorem 12, to these group-level additive valuations. This yields a deterministic polynomial-time disjoint allocation C_g with

`min_g v_g(C_g) >= A/2 >= V/(2K)`.

This is the sole imported approximation result. Its condition is at most two positive-value agents per item; no restriction that the two values agree is required. We do not import any makespan LP statement, a theorem for state-agent degree 2K, or a configuration-LP separation oracle.

Choose for each group a single original state maximizing a_gs(C_g). By the pointwise average inequality, this state's achieved private mass is at least v_g(C_g), hence at least V/(2K). Apply the complete original-job scheduling rule from Section 1. The resulting normalized-instance makespan is at most

`2-V/(2K) = 2-(2-OPT(P))/(2K)`.

The selection of heavy versus diffuse states happens after the same joint additive resource allocation. It is not an independent heavy matching followed by a second allocation with resources already consumed. All original jobs of unchosen states remain parked privately at load 1.

The case A=0 requires no special oracle: any allocation with minimum value zero has the factor-2 guarantee, and the recovery gives the baseline makespan at most 2. The theorem's positive-value threshold procedure and its binary search supply the stated optimization algorithm without knowing A or V.

## 5. Exact private-bonus normalization for W_gs<=1

For each state with private sum W_gs<1, add its unique resource z_gs and the bonus job with private time 1-W_gs and external time 1. Every state of N(P) has total private work exactly 1. The additional resources have group-degree one; all old resource group degrees and all original eligibility edges remain unchanged.

Every schedule of N(P) projects to a schedule of P by deleting bonus jobs and their dedicated resource machines. This can only reduce loads, so OPT(P)<=OPT(N(P)).

Conversely let sigma be any complete schedule of P with makespan C. There is a selector, so C>=1. Keep every original assignment unchanged, and export every added bonus job to its own dedicated resource machine. This includes bonuses of unselected states. Each new resource gets one job of external time 1, at most C, and no old machine receives extra work. Thus sigma extends to a schedule of N(P) with the same makespan bound. This proves OPT(N(P))<=OPT(P).

The two actual optima are therefore equal. Apply Sections 1--4 to N(P), and project its returned schedule to the original jobs. Writing O=OPT(P)=OPT(N(P)), the projected complete original-job schedule satisfies

`C_max <= 2-(2-O)/(2K)`.

Private bonuses are used only in this polynomially sized algorithmic normalization. No added bonus job or artificial state remains in the delivered schedule of the original input.

## 6. Relative factor and strict-unit promise

Set R=2-1/(2K). For every O>=1,

`R O - [2-(2-O)/(2K)] = (2-1/K)(O-1) >= 0`.

Hence C_max<=R OPT(P). In particular OPT(P)<=1 implies OPT(P)=1 and the returned actual schedule has makespan at most R.

The promise decision algorithm runs the scheduling algorithm and computes its actual machine loads. If its makespan is at most R, return YES; otherwise return NO. On the YES promise the first outcome is guaranteed. On the NO promise OPT(P)>R, no complete legal schedule can have makespan at most R, so the second outcome is guaranteed. Intermediate instances need not be classified. This does not assert that every input has absolute makespan at most R.

All bounds use K as the largest explicit menu size. The running time remains polynomial when K grows; only the approximation factor's positive improvement over 2 ceases to be uniform. No sharpness of R is proved.

## 7. Explicit binary complexity and published-backend scope

At most one bonus resource and one bonus job are added for each indexed state. Thus normalization has polynomial size in the original explicit machine, state, resource, and incidence lists. The new times use rational subtraction from 1 and have polynomial bit length.

For each original resource, the auxiliary positive-value group list has size at most two. The values are formed by summing its explicitly listed private times over a group's states and dividing by K_g. Their total binary encoding length is polynomial in the input encoding length: a common denominator may use the product or least common multiple of the input denominators, whose bit length is at most the sum of denominator bit lengths. Dividing by K_g adds only its logarithmic bit length.

If an integer-valued implementation of the imported theorem is used, clear rational denominators by multiplication. This scales objective values uniformly and preserves the factor; it does not duplicate resources, agents, jobs, or states by the numerical denominator. The resulting integer encoding still has polynomial bit length. Theorem 12 explicitly states polynomial running time in binary input encoding. Degree-zero auxiliary items and zero-value edges can be omitted; single-agent items are allowed by its definition.

The winning state for each group is obtained by scanning its explicitly indexed menu and summing its actual allocated private weights. All selector and incidence-job destinations are then output one by one. Projection removes only the algorithm's added bonus jobs. The final output has one original machine identifier for each original job. No running-time claim is made for implicit exponentially many states or resources.

This proof does not claim that the published backend or the full scheduling algorithm has been implemented in this repository. Mathematical constructibility and software implementation remain separate statements.

## 8. Tagged-cube specialization and the two-state exact unit threshold

Fix a resource `(x,a)` in a tagged coordinate cube. If group g has some state containing this resource, then for some coordinate ell its injective incidence index j_x(g) equals a_ell. Thus j_x(g) must lie in the set of at most Q coordinate values. The injectivity of j_x limits the possible groups to at most min(d,Q). Tags prevent any other variable from contributing groups to this same resource. In particular Q=2, or more generally min(d,Q)<=2, satisfies the input degree condition across all states.

This proves the stated Q=2 consequence for arbitrary private cell weights, arbitrary d and group arity, and arbitrary slice cardinalities. For K<=7, R<=2-1/14=27/14. The original unweighted unconditional cube bounds remain stronger on their smaller domain; the present result adds arbitrary private weights and handles the heavy/diffuse state coupling.

Finally suppose every menu has at most two states. For each state let its positive support be the resources whose private job times are strictly positive. At makespan 1, a selected root already has its unit selector and therefore must export every positive-support job. Resource jobs have time 1, so positive supports of the selected states must be pairwise disjoint. Conversely disjoint positive supports give a unit schedule: export those jobs, keep selected zero-time jobs privately, and park all jobs of unselected states at total load W_gs<=1.

Encode each two-state group by a Boolean choice and each one-state group by a forced Boolean choice. Every pair of state choices whose positive supports intersect contributes the 2CNF clause forbidding their simultaneous choice. The conjunction is satisfiable exactly when the original UM instance has OPT<=1. All pairs and support intersections can be generated from the explicit input in polynomial time. This is only an exact unit-threshold algorithm, not an exact optimum algorithm for larger makespans. It is separate from the quantitative approximation proved above.

## 9. Limits of the result

The proof uses group-degree two only in the imported additive allocation step. It does not infer a constant algorithm from state-agent degree 2K or from arbitrary constant degree at least three. It uses exactly-unit resource times in the normalized UM/XOS identity; resources with smaller processing times may fit several jobs below makespan 2 and require a different proof. The method does not eliminate the factor K when menus grow and does not solve the general unrelated-machines approximation problem.

No finite experiment, exhaustive instance enumeration, LP integrality gap, or guessed source promise replaces any step of this proof. The claim is a direct structural corollary of the cited additive theorem and the explicit transformations proved here.
