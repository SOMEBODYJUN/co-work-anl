# 辅助阶跃依赖游戏：有向无环图的精确阈值

Claim **WC-R1-DAG-STEP v1**, 2026-10-14. This is an auxiliary step-cost theorem, outside the polynomial class of WC-TARGET. Origin: R1 main reconstruction and the independent `tree_review` agent (requested gpt-6.1-sol / ultra). No priority claim or external review is made.

## Exact identity

**Objects / domain / assumptions.** A finite simple directed acyclic graph D on m light vertices; a root player of weight 1; positive light weights satisfying total light weight <1 and, for every u, sum of weights of its outgoing neighbors <w_u. The graph need not be transitive. All amplitudes A_0,A_v are nonnegative. Two resources a_0,b_0 have cost A_0 at load >=1 and zero otherwise. Resources a_v,b_v have cost A_v at load >=1+w_v and zero otherwise. The root chooses all a resources or all b resources. Light v chooses a_0, all a_u with u->v, and b_v; or its symmetric counterpart b_0, all b_u with u->v, and a_v. Strategies are sets: parallel edges are excluded.

**Quantifiers / conclusion / scope.** For every such graph, weight vector and amplitude vector a q_D-PNE exists. The supremum, over these amplitude vectors, of the instance-optimal factor is exactly q_D and is attained by positive amplitudes. Here P_k is the number of nonempty directed paths on k vertices, including the m one-vertex paths, and q_D is the unique solution in [1,infinity) of

    q_D = 1 + sum_{k=1}^m P_k q_D^(-k).

For m=0, q_D=1. For m>0, q_D>1. A degree bound or polynomial smoothing assertion is not part of this claim.

**Dependencies.** Elementary threshold-load reduction, a finite topological recursion and monotonicity. The general proof is below; finite computations are corroboration. Relation to Paper Fact: the complete transitive ordered graph recovers Christodoulou et al., arXiv:2002.07466v3, Section 6, Theorem 5; its full symmetric strategies and breakpoint convention were reread online in this session.

**Evidence / objections / status.** General proof independently reconstructed in independent_review.md; literal-resource Fraction checks in verify.py and independent_audit.py. Strict load inequalities are essential; equality can activate a supposedly inactive resource. This is a complete internally reviewed auxiliary theorem, unrefereed. Truth: supported by the proof; Value: a reusable exact topology interface; Novelty: unchecked; Mechanism: path amplification; Ambition: auxiliary, not a polynomial lower-bound breakthrough.

## 1. Exact reduction

Fix the root column. Let Z contain light vertices whose own resource is in this column. Without the root no resource charges: all light weight <1. With the root, a vertex resource charges precisely when its own light player uses that column. Otherwise its other users are outgoing neighbors of that vertex, with total weight <w_v. Consequently the current and alternative costs are exactly

    root: A_0 + sum_{v in Z} A_v  vs  A_0 + sum_{v notin Z} A_v;
    v in Z: A_v vs P_v;
    v notin Z: P_v vs A_v,
    P_v = A_0 + sum_{u->v, u in Z} A_u.

The formulas recompute loads after the moving player switches. No assumption that only a particular canonical state is relevant is needed. Dyadic weights w_v=2^(-j) in a topological ordering j=1,...,m meet all strict inequalities, so every finite simple DAG has a legal realization.

## 2. Recursion and upper bound

For r>=1 define in a topological ordering

    h_v(r) = (1 + sum_{u->v} h_u(r))/r.

Expanding this recursion yields h_v(r)=sum over paths ending at v of r^(-number of vertices). Thus sum_v h_v(r)=sum_k P_k r^(-k). The right side of the threshold equation is strictly decreasing for m>0, whereas its left side increases from 1 to infinity; existence and uniqueness follow.

Construct Z in topological order by inserting v if A_v<=P_v/q_D. An inserted player's current cost is at most its alternative divided by q_D, hence is q_D-stable. An excluded player's cost satisfies P_v<q_D A_v. Inductively every inserted v has A_v<=A_0 h_v(q_D). Therefore

    A_0 + sum_Z A_v <= A_0 (1 + sum_v h_v(q_D)) = q_D A_0
                   <= q_D (A_0 + sum_notZ A_v),

which proves root stability. When A_0=0, the same greedy rule inserts only zero amplitudes and all current costs are zero: it gives an exact PNE. This includes the all-zero game and avoids division by zero.

## 3. Attainment and rational certificates

Choose A_0>0 and A_v=A_0 h_v(q_D). If Z is all vertices, the root improves by exactly q_D. If Z is not all vertices, select its first missing vertex in a topological ordering; all incoming neighbors belong to Z and P_v=q_D A_v. That vertex improves by exactly q_D. Thus every profile has an improvement of at least q_D, and the previous upper bound proves the optimum is q_D. The endpoint q_D itself admits a PNE in the approximate sense; strict nonexistence holds only below it.

More generally, for any rational r>=1 choose A_v=A_0 h_v(r) with rational A_0>0. The exact instance factor is

    beta_D(r)=min{r, 1+sum_v h_v(r)}.

The same first-missing argument and the all-in root show every state has an improvement at least beta. In the all-in state only the root improves, by 1+sum h; in the all-out state a source vertex improves by r and every light improves by at most r (h_v>=1/r). These states attain the smaller bound. For m=0 the factor is 1. Therefore rational r<q_D supplies completely rational instances of exact factor r.

## 4. Structural bounds

For any simple DAG, P_1=m and P_k<=binom(m,k). Hence

    (1+sqrt(1+4m))/2 <= q_D <= Phi_m,
    Phi_m = (1+1/Phi_m)^m.

The lower extremum is the empty dependency graph and the upper extremum the complete transitive ordered graph. For a tree with edges from every strict light ancestor to its descendant, h_v(r)=r^(-1)(1+1/r)^(depth(v)-1), where root depth is zero, reproducing the tree formula.

If maximum incoming degree is Delta, P_k<=m Delta^(k-1). For R>Delta, sum h_v(R)<=m/(R-Delta). Setting (R-1)(R-Delta)=m gives

    q_D <= (Delta+1+sqrt((Delta-1)^2+4m))/2.

For m=0 use q=1 separately. If Delta=o(sqrt(m)), the preceding upper and lower bounds imply q_D~sqrt(m). A small longest-path length alone is insufficient: the two-layer complete bipartite graph with s vertices per layer has P_1=2s,P_2=s^2 and q~s^(2/3), even though every directed path uses at most two vertices.

## Reproduction and remaining bridge

Run `python3 tests/audits/weighted_congestion/step_dag/verify.py` and `python3 tests/audits/weighted_congestion/step_dag/independent_audit.py`. The first uses actual resource sets and threshold loads for every checked deviation, then compares the reduced equations; it enumerates all forward-labelled DAGs through four vertices and selected larger graphs. No numerical root is used. Output verification.json records the exact finite coverage.

This theorem identifies incidence path counts, rather than geometric depth alone, as the amplification mechanism. Turning any such instance into nonnegative polynomial costs still requires a separate proof controlling all loads and overshoot. No polynomial growth inference follows from this step theorem alone.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
