# 多 small 原生任务的全局实际 flow 算法与位复杂度

Read the separate exact-statement file for the complete scope. These are direct bipartite flow/Hall consequences; no originality or best-known-ratio claim is made.

## Fast assignments

Build a bipartite graph with one vertex per J_F job and one vertex per machine, using precisely its small eligible edges. Give each job demand1 and each machine capacity c=ceil(k/q). Fractionally assign each job uniformly among all its small endpoints. Since its degree d_j>=q, each incidence carries at most1/q. A machine has at most k small incidences, so its incoming fractional amount is at most k/q<=c. Integer network flow therefore saturates every job at capacity c and returns an actual assignment with at most c jobs per machine. Alternatively Hall's condition follows by counting q|S|<=k|N(S)|<=cq|N(S)| for every job subset S. No unit eligibility of J_F is used.

Find the minimum integer fast count F for which such a flow saturates all J_F. The bound above gives F<=ceil(k/q), and a binary search over 0..|J_F| with an integer-flow oracle computes F and an actual minimizing allocation. Empty J_F has F=0. Capacity values can always be capped at |J_F|, so a very large binary k never causes a loop of k steps or exponentially many flow vertices.

## Unit assignments and the actual schedule

Independently find the minimum integer B such that all J_U can be assigned to unit-eligible machines with at most B per machine, again by integer flow and binary search over 0..|J_U|. Empty J_U has B=0. Overlay the two actual assignments, using disjoint job sets. Every machine's actual load is its integer unit count plus its fast count/k, hence at most B+F/k. Each job is assigned exactly once to an original finite endpoint.

If a capacity-one unit matching is supplied, use it rather than solve B; the same fast flow gives C<=1+ceil(k/q)/k. If no such matching exists, every complete schedule puts at least two J_U jobs on some machine, so its makespan is at least2. Unit choices of J_F cannot repair that lower bound.

## Approximation and empty cases

When J_U is nonempty, B>=1 and OPT>=B because the unit-only subinstance alone has optimum B. Thus
 C/OPT <= (B+F/k)/B <= 1+F/k <= 1+ceil(k/q)/k.
This is a ratio proof relative to actual OPT, not a configuration threshold. If B>=2 it even gives 1+F/(2k).

When J_U is empty, F/k is attained using all fast endpoints. Since q>=2 and k>=2,
 F/k <= ceil(k/2)/k <1.
Every schedule using even one unit endpoint has makespan at least1, so any better schedule must use fast endpoints only. By the definition of F, no such schedule improves F/k. Therefore this branch is exact, including J_F empty, for which F=0 and the empty allocation has OPT0.

For even k the ratio upper bound at q>=2 is at most3/2. For odd k>=3 it is at most3/2+1/(2k)<=5/3, with its largest numerical bound at k3. This is only an upper bound; no sharp-ratio claim follows.

If q>=k, c=1, so fast jobs admit an ordinary one-to-one small matching. Overlay any capacity-one unit-only matching to obtain the near-unit strict threshold1+1/k. Native jobs' large endpoint A can even coincide with other jobs' small endpoints; overlay accounts for the resulting 1+1/k load. Within one job each eligible endpoint is one machine with one processing time, as required by the UM input.

## Total bit complexity and dependencies

The two networks have one job node per explicit job, one machine node per explicit machine and one edge per original eligible incidence. Capacities are integers between0 and the explicit number of relevant jobs. Edmonds--Karp, for example, is deterministic polynomial in these vertex/edge counts and returns an integral flow; binary search adds O(log n) flow calls. Rational load evaluation uses integer counts divided by the input integer k, with binary arithmetic polynomial in log k and input length. There is no enumeration of all subsets, all configurations, q labels or k numerical slots. Input degrees and the membership in {1/k,1,infinity} can be checked by exact rational comparisons.

The only external standard primitive is integral bipartite max flow; the displayed Hall witness also proves existence directly. The proof does not import Feige, configuration-LP rounding, scalar relaxed source satisfaction, or a promise-copy theorem. No software execution or broad-input performance test is claimed in this proof file.
