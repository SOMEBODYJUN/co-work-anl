# R1 odd-cycle pair-resource obstruction

## Claim R1-PAIR-2PNE v1

**Exact Statement.** Every finite binary complementary pair-resource game described below has a 2-PNE. In fact every global minimum of the explicit potential Φ below is a 2-PNE, and every strict 2-improvement decreases Φ.

**Objects.** A finite graph on strategic players, allowing parallel edges but no loops. Player i has weight w_i>0 and action b_i∈{0,1}. Each edge e={i,j} has two resource columns e^0,e^1 with the same nonnegative nondecreasing cost function c_e. Player i selects exactly one column on each incident edge, according to b_i; a fixed endpoint-specific bit may swap the column labels. Thus flipping b_i toggles collision/noncollision on every incident edge. No third strategic player uses these resources. Optionally the two columns have the same fixed background load h_e≥0. Player i can additionally incur arbitrary nonnegative private action costs P_i(0),P_i(1), which are independent of all other strategic actions.

**Domain.** All positive real weights; all finite graphs; any nonnegative nondecreasing resource costs. In particular every nonnegative-coefficient polynomial of arbitrary degree in MODEL.md is allowed. Fixed-background players, if used, have singleton strategies and are therefore not additional strategic participants.

**Quantifiers.** For every such game, there exists a pure state s satisfying C_i(s)≤2C_i(1−b_i,s_{−i}) for every strategic player i. This is a subclass result and says nothing about resources used by three or more strategic players.

**Assumptions.** Identical columns, including identical fixed background loads; private costs nonnegative; every relevant action is a complementary column choice. Action-dependent private costs ARE permitted.

**Definitions.** Write

    T_e = c_e(h_e+w_i+w_j),
    S_ie = c_e(h_e+w_i),
    0 ≤ S_ie ≤ T_e.

At a state, let A_i be the incident edges on which i collides and B_i the incident edges on which i does not. Define

    Φ(s) = Σ_{colliding edges e} T_e + Σ_i P_i(b_i).

**Scope.** Includes the requested odd cycle with costs a_e x^d and its arbitrary graph extension. Includes common private bases, arbitrary action-dependent private bases, and symmetric fixed cohorts. Does not include moving cohorts or resources with three or more strategic users. Does not include unequal column costs/backgrounds.

**Conclusion and proof.** At a local minimum of Φ with respect to player i, set

    U = P_i(b_i) + Σ_{e∈A_i} T_e,
    V = P_i(1−b_i) + Σ_{e∈B_i} T_e.

The potential inequality is U≤V. The actual costs are

    C_i = U + Σ_{e∈B_i} S_ie,
    C_i' = V + Σ_{e∈A_i} S_ie.

Nonnegativity and S_ie≤T_e give

    C_i ≤ U+Σ_{e∈B_i}T_e ≤ U+V ≤ 2V ≤ 2C_i'.

The same calculation shows that Φ(s')≥Φ(s) implies C_i≤2C_i'; its contrapositive proves that every strict 2-improvement decreases Φ. A global minimum exists because the state set is finite. Zero costs cause no problem: if C_i'=0 then the inequality forces C_i=0.

**Dependencies.** MODEL.md cost convention and α-PNE definition only.

**Evidence.** Complete algebraic proof above.

**Counterevidence/Objections.** None within the stated assumptions. This does not assert that 2 is sharp. Asymmetric columns and moving/multi-user cohorts invalidate the displayed decomposition or its comparison S_ie≤T_e for the post-deviation collision column.

**Status.** PROVED, internally verified.

**Related Files.** ../../../../MODEL.md; this file's pure-ring refinement below.

## Claim R1-ODDRING-EXACT v1

**Exact Statement.** For a pure odd cycle with the identical monomial columns specified below, all-state nonexistence of an α-PNE is equivalent to one consistent direction of strict α-improvements of single-defect states. The corresponding coefficient-product conditions are necessary and sufficient.

**Objects / Domain.** Let n≥3 be odd, indices modulo n, edge e_i={i,i+1}, weights w_i>0, coefficients a_i>0, and costs a_i x^d on BOTH columns of edge e_i, where integer d≥1. Player i chooses one color on both incident edges. No private costs and no background loads are included in this refinement. α≥1 is arbitrary.

**Quantifiers.** First, the exact criterion below applies to every fixed weights/coefficient instance and every α≥1. Second, the product criterion characterizes whether there exist positive coefficients for fixed weights, d, α. The same characterization with d=0 is unnecessary, since every state is then an exact PNE.

**Definitions.** Put

    δ_i = 1{b_i=b_{i+1}},
    T_i = a_i(w_i+w_{i+1})^d,
    q_i = (w_i/(w_i+w_{i+1}))^d,
    p_i = (w_{i+1}/(w_i+w_{i+1}))^d.

Because n is odd, the number of collision edges Σ_iδ_i is odd. Every prescribed odd collision pattern is feasible and corresponds to two globally complemented action states. Those two states have identical costs.

For player i, write A=T_{i−1}, B=T_i, u=p_{i−1}A, v=q_iB. The exact current/deviation costs and improvement ratios are:

| (δ_{i−1},δ_i) | Current | After flip | Ratio |
|---|---:|---:|---:|
| (0,0) | u+v | A+B | (u+v)/(A+B)≤1 |
| (0,1) | u+B | A+v | r_i=(B+u)/(A+v) |
| (1,0) | A+v | u+B | 1/r_i |
| (1,1) | A+B | u+v | D_i=(A+B)/(u+v) |

Every state has a strict α-improvement if and only if

    (r_i>α for every i) OR (r_i<1/α for every i).             (E)

Equivalently, the best pure-state approximation factor of this fixed game is exactly

    γ(G) = max{1, min_i r_i, min_i(1/r_i)}.

**Proof of necessity.** Consider the n single-defect collision patterns, each with just edge e_i colliding. Only the endpoints of e_i can improve. A flip at vertex i moves a defect from e_i to e_{i−1} with ratio r_i; the opposite transfer has reciprocal ratio 1/r_i. For α≥1, at most one of these two arrows at each vertex can be a strict α-improvement. If every single-defect state is unstable, all n defect positions require an outgoing arrow. There are at most n arrows, so every position has exactly one outgoing arrow and every vertex contributes exactly one arrow. On a cycle these arrows must all point in the same direction. This proves (E).

**Proof of sufficiency.** Suppose all r_i>α. Any feasible collision pattern other than all ones has at least one collision (odd parity) and at least one noncollision, hence a cyclic boundary (δ_{i−1},δ_i)=(0,1). That vertex has improvement ratio r_i>α. For the all-ones pattern, D_i≥r_i because A≥u and B≥v; thus it too has a strict α-improvement. The reverse orientation is identical. Boundary equality is respected: r_i=α does not constitute a strict improvement.

**Positive-coefficient feasibility.** Let z_i=T_i/T_{i−1}, so Π_i z_i=1. The first branch of (E) is equivalent to

    (1−αq_i)z_i > α−p_{i−1} for every i.

Since d≥1 and positive weights imply p_i,q_i∈(0,1), the right sides are positive. Therefore positive coefficients with this orientation exist if and only if

    αq_i<1 for every i,
    Π_i(α−p_i) < Π_i(1−αq_i).                              (F+)

For the reverse orientation, swap p and q:

    αp_i<1 for every i,
    Π_i(α−q_i) < Π_i(1−αp_i).                              (F−)

These are strict criteria. For example, under (F+) set

    k_i=(α−p_{i−1})/(1−αq_i),
    z_i=k_i(Π_jk_j)^(−1/n).

Then z_i>k_i and Π_i z_i=1. Reconstruct positive T_i from these cyclic ratios and set a_i=T_i/(w_i+w_{i+1})^d. This is an explicit coefficient construction.

**Immediate obstruction to degree-growing α.** If α≥2, then α−p_i>1 while 1−αq_i<1 whenever the latter is positive; (F+) and (F−) are impossible. More directly, a single defect placed at an edge of minimum T_i is a 2-PNE: each endpoint's current cost is at most T_i+T_neighbor≤2T_neighbor, while its deviation cost is at least T_neighbor. Every other vertex has zero collisions and cannot improve. Thus no pure pair ring can realize a lower bound diverging with d, regardless of weights or coefficients.

**Linear special case.** For d=1 and α=1, Π_i(1−p_i)/(1−q_i)=Π_iw_i/w_{i+1}=1, so neither strict product condition can hold. This proves existence of an exact PNE in every such linear pure ring.

**Small explicit nonpotential example.** Degree d=2, n=3, cyclic weights (1,3,2), coefficients (1,11/25,93/50) give

    (r_0,r_1,r_2)=(893/887,500/499,925/922).

All exceed one. Hence this legal game has no α-PNE for every α<500/499, and its best factor is exactly 500/499. This illustrates that the 2-PNE obstruction does not claim exact PNE existence for nonlinear costs.

**Dependencies.** MODEL.md only; elementary finite-cycle combinatorics.

**Evidence.** Full local algebra, necessity/sufficiency proof, and explicit construction above.

**Counterevidence/Objections.** The oddness assumption is essential: an even cycle has a zero-collision state, which is an exact PNE. With arbitrary action-dependent private costs, globally complemented single-defect states need not have identical costs, so the exact orientation/product characterization need not apply; Claim R1-PAIR-2PNE v1 still applies.

**Status.** PROVED, internally verified.

**Related Files.** MODEL.md; Claim R1-PAIR-2PNE v1 above.


---
整理来源与当前文件用途见[逐文件登记](../../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
