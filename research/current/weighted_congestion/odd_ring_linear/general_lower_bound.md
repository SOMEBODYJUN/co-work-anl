# OC-AMPLIFIER-LIMIT-v1: a linear reset gives d/(ln d+2)

Status: complete mathematical derivation, pending independent review and literature/priority audit. This note asserts a construction in WC-TARGET v1, not novelty. Contributors: R1/odd_cycle proposed and derived the directed-ring coefficient interface and the linear-reset amplification; the R1 coordinator independently reconstructed literal player costs and the H_d criterion; R1/odd_cycle/pair_obstruction independently checked the interface, uniform families, and the linear-reset proof. Mathematical dependencies are reconstructed in full below; `README.md` is the broader reusable interface account.

## Exact statement and objects

For every integer d≥4 there is a finite binary weighted congestion game with positive weights, nonnegative monomial latencies of degrees 1 and d, and no α-PNE at

    α = d/(ln d+2).

The game's player and resource counts may grow rapidly with d. In particular this proves the model-wide threshold lower bound a_*(d)≥d/(ln d+2) for d≥4. The state-wise deviations are strictly greater than α, so the endpoint is covered by this individual game; no inference about universal attainment of the infimum is needed.

More generally, for an integer d≥1 and t∈(0,1), define

    H_d(t) = [(1+t)^d+t^(d+1)]/[1+t(1+t)^d].

For every 1<α<H_d(t), the same construction produces a finite game with no α-PNE. Consequently, for d≥2,

    a_*(d) ≥ sup_{0<t<1} H_d(t).

Here H_d(t)>1 for d≥2: at d=2 the numerator minus denominator is t−t²>0, and for fixed t∈(0,1), H_d(t) increases with y=(1+t)^d because its derivative as a function of y is (1−t^(d+2))/(1+ty)²>0 if the small numerator term is held fixed; alternatively the direct difference (1−t)(1+t)^d−1+t^(d+1) increases with d, since its one-step increment is t(1−t)[(1+t)^d−t^d]>0. Only this direct increment is needed. The strict α<H_d(t) quantifier, rather than nonexistence at the supremum itself, is what proves the threshold inequality.

The general claim has no assertion when H_d(t)≤1. All assumptions are α>1, integer d≥1, 0<t<1, and α<H_d(t); there is no upper or lower restriction on individual player weights beyond positivity.

## The finite congestion game and its full-state certificate

Let m≥3 be odd. Indices i are modulo m. Hub H_i has positive weight u_i and bit h_i∈{0,1}. Cohort i consists of n_i≥1 independent players of weight v_i, each choosing a bit l. Create two main resources A_i^0,A_i^1 with latency a_i z^{k_i} and, for every cohort member j, two side resources B_ij^0,B_ij^1 with latency b_i z^d. All coefficients a_i,b_i are positive. A hub H_i at bit h uses A_i^h and all B_(i−1),j^h. Cohort member (i,j) at bit l uses A_i^l and B_ij^(1−l). Costs are sums of latencies, without multiplying by player weight.

For the amplifier, set t_i=v_i/u_(i+1)=t, x_0=v_0/u_0=t^(2m−1), and x_i=v_i/u_i=1/t for i≥1. Explicit positive weights are

    u_0=1, u_i=t^{2(m−i)} (1≤i<m),
    v_0=t^{2m−1}, v_i=t^{2(m−i)−1} (1≤i<m).

Take k_0=1, n_0=n, and k_i=d,n_i=1 for all i≥1. Let

    q_i=a_i u_i^{k_i}, p_i=b_i u_(i+1)^d,
    N_i=(1+x_i)^{k_i}−α(n_i x_i)^{k_i},
    M_i=α(1+n_i x_i)^{k_i}−1,
    P=α(1+t)^d−t^d, Q=(1+t)^d−α.

It suffices to choose positive q_i,p_i such that

    q_iN_i>p_iP,
    n_i p_iQ>q_(i+1)M_(i+1).                  (*)

Indeed, if any cohort player uses the same bit as its own hub, its current cost is at least q_i(1+x_i)^{k_i}+p_i t^d and its post-deviation cost is at most q_i(n_i x_i)^{k_i}+p_i(1+t)^d. The first strict inequality gives an α-improvement; the count n_i includes the deviator after switching and is valid even when n_i=1. Otherwise all cohort-i members choose 1−h_i. An odd ring of hub bits has some h_i=h_(i+1). Hub H_(i+1) then collides with every incoming cohort-i player, and with no player on its own main resource. Its exact current cost minus α times its switching cost is n_i p_iQ−q_(i+1)M_(i+1)>0. This covers every pure state.

For positive N_i,Q define

    F_i=n_i N_i Q/(M_i P), K_i=n_iN_iQ/(P M_(i+1)), G=∏F_i=∏K_i.

If G>1, choose a rational δ>1 with δ^{m−1}<G. Set q_0=1 and q_(i+1)=K_iq_i/δ for i=0,…,m−2. For the final index use q_m=q_0; G/δ^{m−1}>1 ensures q_(i+1)<K_iq_i also there. Set

    p_i=1/2 [ q_(i+1)M_(i+1)/(n_iQ) + q_iN_i/P ],
    a_i=q_i/u_i^{k_i}, b_i=p_i/u_(i+1)^d.

The two bracket endpoints are strictly ordered, so (*) holds at every index. A fully deterministic rational δ is obtained by starting δ=2 and replacing δ by 1+(δ−1)/2 until δ^{m−1}<G. All coefficients and weights are rational when α and t are rational; for arbitrary real α,t the coefficients are legal positive reals. Finite positive monomials introduce no zero-cost boundary or negative coefficient.

## Finite, explicit parameter choice

Fix 1<α<H_d(t). Put

    Q=(1+t)^d−α,  P=α(1+t)^d−t^d,  B=Q/P.

The denominator P is positive. Rearranging α<H_d(t) gives Q>tP>0, hence B>t. Choose an integer R congruent to 1 modulo 4, with R≥5, satisfying

    R > ln(4α)/ln(1/t),
    R > ln(8α²)/ln(B/t).

For example take the least integer in that congruence class above all three displayed thresholds. Set

    m=(R+1)/2  (odd and at least 3),
    x_0=t^R, k_0=1, n_0=floor[1/(2α x_0)].

At each of the other m−1 ring positions set x_i=1/t, k_i=d, n_i=1. All side degrees are d and every t_i=t. Use the explicit weights and coefficient recipe just given. This fully specifies a finite game; no search, limit game, or infinite strategy set is used.

## Strict product proof

Write x=x_0 and n=n_0. The first threshold gives x<1/(4α), so 1/(2αx)>2 and

    1/(4αx) < n ≤ 1/(2αx).

(Replacing the first strict inequality by ≥ would also suffice.) For the linear reset,

    N_0=1+x−αnx ≥1/2+x>1/2,
    M_0=α(1+nx)−1 ≤α−1/2<α.

Consequently

    A_0 := nN_0/M_0 > 1/(8α²x).

Every buffer has N_i=t^(−d)Q and M_i=t^(−d)P, so F_i=B². The reset has F_0=A_0 B. Thus

    ∏ F_i = A_0 B^(2m−1)
           > (B/t)^R/(8α²)
           > 1.

The coefficient recipe and full-state proof above now produce a game in which every pure state has a strict α-improvement. The reset uses degree 1; the buffers and all side resources use degree d. Every individual strategy remains finite even when n_0 is large.

## Uniform lower bound

For d≥4 set D=ln d and t=D/d∈(0,1). The elementary inequality ln(1+s)≥s−s²/2, strict for s>0, gives

    y:=(1+t)^d > exp[D−D²/(2d)].

For d≥1, elementary differentiation shows D²/(2d)≤2/e²<ln 2. Therefore y>d/2, and

    H_d(t) = [y+t^(d+1)]/[1+ty]
             > 1/[t+1/y]
             > d/(ln d+2).

The proposed α exceeds 1 for all integer d≥4: d−ln d−2 is increasing for d>1 and is positive at d=4. Hence the finite explicit construction applies at α=d/(ln d+2). As d→∞ this is (1−o(1))d/ln d.

No external theorem is required for the mathematical derivation. The logarithm inequality can be checked by differentiating ln(1+s)−s+s²/2, whose derivative is s²/(1+s)>0.

## Exact finite-d interpretation

The formula H_d(t) is an achievable strict lower threshold for this amplifier family, not an asserted upper bound on the original model. For rational t and rational α<H_d(t), every parameter can be chosen rational, including all weights and resource coefficients. A direct exact test is the product formula

    n(1+x−αnx)/[α(1+nx)−1] × [( (1+t)^d−α )/( α(1+t)^d−t^d )]^R > 1,

with x=t^R and n=floor[1/(2αx)]. The threshold-based m is sufficient; smaller m can already pass the same exact test.

## Objections checked and remaining scope

- Large buffers are permitted: a cohort player can be heavier than its own hub and lighter than the next hub. WC-TARGET imposes no ordering of weights.
- The cohort n_0 grows with d and with the slack H_d(t)−α. Fixed-player existence bounds do not apply uniformly to this family.
- The coefficient system closes around the ring because ∏x_i=∏t_i exactly, and the strict product inequality is sufficient, not merely necessary.
- The proof covers all bit/count states through the light-versus-hub dichotomy, including n_i=1 at every buffer.
- The degree d endpoint is used exactly; no higher-degree approximation or negative coefficient is introduced.
- Independent review and primary-literature priority checks remain distinct from the algebraic proof. No claim of first discovery is made here.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
