# R1 directed odd-ring certificate

Status: candidate construction with a complete local coefficient interface; independent review is in progress. This file is not a claim of priority. Model: WC-TARGET v1. Mathematical contributors: R1 root, R1/odd_cycle, and R1/odd_cycle/pair_obstruction. Requested research configurations are recorded by the coordinating R1 session; this note does not infer a runtime model identity.

## Claim OC-INTERFACE-v1

Let m≥3 be odd. Indices are modulo m. Hub H_i has weight u_i>0 and bit h_i∈{0,1}. Cohort i contains n_i≥1 players, each of weight v_i>0 and each choosing a bit independently. There are two main resources A_i^0,A_i^1 with common latency a_i z^{k_i}, and, for each cohort member j, two side resources B_ij^0,B_ij^1 with common latency b_i z^{D_i}. Here a_i,b_i>0 and 1≤k_i,D_i≤d.

Hub H_i at bit h uses A_i^h and every B_(i−1),j^h. Light/cohort player (i,j) at bit l uses A_i^l and B_ij^(1−l). (The word cohort is preferable to light: its weight can exceed its own hub's weight.) Thus all strategies are finite binary multi-resource strategies, and every weight is a positive scalar independent of the resource.

Fix α>1. Write

    x_i=v_i/u_i,  t_i=v_i/u_(i+1),
    q_i=a_i u_i^{k_i},  p_i=b_i u_(i+1)^{D_i},
    N_i=(1+x_i)^{k_i}−α(n_i x_i)^{k_i},
    M_i=α(1+n_i x_i)^{k_i}−1,
    P_i=α(1+t_i)^{D_i}−t_i^{D_i},
    Q_i=(1+t_i)^{D_i}−α.

The parameters x_i,t_i come from positive u_i,v_i if and only if ∏x_i=∏t_i. Indeed set u_0=1 and u_(i+1)=u_i x_i/t_i, then v_i=u_i x_i; the product identity closes the ring.

Suppose N_i,Q_i>0 for every i. Then the following strict inequalities have a positive solution q_i,p_i if and only if

    ∏ F_i > 1,    F_i = n_i N_i Q_i/(M_i P_i):

    q_i N_i > p_i P_i,             (light inequality)
    n_i p_i Q_i > q_(i+1) M_(i+1). (hub inequality)

Whenever they hold the game has no α-PNE. Therefore it also has no β-PNE for 1≤β≤α. Equivalently, the same construction can certify nonexistence for every β below any limiting bound obtained with strict margins.

## Full-state proof

If a cohort player i chooses l=h_i, its current cost is at least q_i(1+x_i)^{k_i}+p_i t_i^{D_i}. After switching, its main-resource load is at most n_i v_i, and its side-resource load is at most u_(i+1)+v_i. Its deviating cost is at most q_i(n_i x_i)^{k_i}+p_i(1+t_i)^{D_i}. The light inequality therefore proves strict α-improvement, irrespective of all other bits and counts. In particular the upper bound n_i v_i includes the deviator and remains valid at n_i=1.

If no such cohort player exists, every member of cohort i chooses 1−h_i. Because m is odd, some adjacent hub pair has h_i=h_(i+1). Hub H_(i+1) then shares every incoming side resource with its cohort-i user, and shares its own main resource with no cohort-(i+1) user. Switching makes all incoming side resources solo and moves to the main resource containing all n_(i+1) own-cohort players. Its exact current-minus-α-times-deviating cost is

    n_i p_i Q_i − q_(i+1) M_(i+1) > 0.

Thus every state admits a strict α-improvement. This is a state-cover argument, not an improvement-cycle argument. All costs are positive in this construction, so no zero-cost quotient occurs.

## Coefficient consistency and exact rational realization

Put K_i=n_i N_i Q_i/(P_i M_(i+1)). Necessity follows from q_(i+1)<K_i q_i and multiplying around the ring. Conversely, write G=∏K_i=∏F_i>1. Choose any rational δ>1 with δ^{m−1}<G (if the input parameters are rational, such a rational exists). Set q_0=1 and q_(i+1)=K_i q_i/δ for 0≤i<m−1. The last bound q_0<K_(m−1)q_(m−1) follows from G/δ^{m−1}>1. For each i choose

    p_i = 1/2 [q_(i+1)M_(i+1)/(n_i Q_i) + q_i N_i/P_i].

The bracket endpoints are strictly ordered. Finally a_i=q_i/u_i^{k_i}, b_i=p_i/u_(i+1)^{D_i}. Every quantity is positive and rational when the input is rational. This provides an explicit finite exact construction without relying on a numerical LP or a floating-point feasibility tolerance.

## Amplifier specialization OC-AMPLIFIER-v1

Use D_i=d, a common t∈(0,1), and odd m. At i=0 set x_0=t^{2m−1}, n_0=n, k_0=k. At each i≥1 set x_i=1/t, n_i=1, k_i=d. The closure identity is exact. The hub and cohort weights can be written

    u_0=1, u_i=t^{2(m−i)} for 1≤i<m,
    v_0=t^{2m−1}, v_i=t^{2(m−i)−1} for 1≤i<m.

Write B=Q/P, Q=(1+t)^d−α, P=α(1+t)^d−t^d. Each buffer i≥1 obeys the exact identities N_i=t^(−d)Q, M_i=t^(−d)P, so F_i=B². The ring feasibility condition is therefore exactly

    n [(1+x_0)^k−α(n x_0)^k] / [α(1+n x_0)^k−1] × B^{2m−1} > 1.

This is the key discriminating change from a homogeneous star: the one large-cohort reset node is balanced by m−1 one-player buffers on ascending weight scales. The explicit asymptotic theorem and its constants are supplied in the companion reviewed supplement; until reviewed, do not replace a universal result or literature ledger with this candidate.

## Evidence and scope

`verify_ring.py` reconstructs exact rational coefficients from compact input and checks all local inequalities with `fractions.Fraction`. It can also enumerate all compressed states for tractable cohorts. Such enumeration preserves every deviation type because players within a cohort are symmetric; each count 0,…,n and each hub bit is checked. Large-instance validation uses the general full-state proof above plus exact endpoint certificates, not a claim to enumerate exponentially many individual profiles.

`pair_obstruction/` contains an independently reconstructed obstruction: symmetric complementary pair-sharing resources alone always admit a 2-PNE. The main resources above are shared by an entire cohort, so that obstruction does not apply.

Open obligations at this checkpoint: independent algebraic/full-state attack; explicit uniform d→∞ parameter proof; literature and priority search beyond the earlier star envelope; integration into the root claim and asset registries by the coordinator.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
