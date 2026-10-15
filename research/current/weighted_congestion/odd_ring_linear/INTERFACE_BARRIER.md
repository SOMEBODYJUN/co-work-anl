# OC-INTERFACE-BARRIER-v1

Status: proved algebraic obstruction for the sufficient coefficient interface, pending independent review. Contributor: R1/odd_cycle. Scope is exactly the inequalities of OC-INTERFACE-v1 in `README.md`; this is not an existence theorem for all games in that architecture, and not a universal upper bound for WC-TARGET.

## Exact claim

Fix d≥1 and α>1. Consider any ring size m, any positive x_i,t_i with ∏x_i=∏t_i, any integers n_i≥1 and 1≤k_i,D_i≤d. If all N_i,Q_i>0 and ∏F_i>1 in OC-INTERFACE-v1, then

    (α−1)(α^(1/d)−1) < 1.

Thus the interface cannot certify asymptotically more than (1+o(1))d/ln d. OC-AMPLIFIER-LIMIT-v1 attains (1−o(1))d/ln d, so its leading asymptotic constant within this certificate mechanism is sharp.

## Proof

Write z=α^(1/d)>1 and L=z−1. Since k_i≤d, N_i>0 implies

    n_i x_i < (1+x_i) α^(−1/k_i) ≤ (1+x_i)/z.

Since n_i≥1, this also gives x_i<1/L. Since D_i≤d, Q_i>0 gives t_i>α^(1/D_i)−1≥L. Multiplication and the closure identity yield

    ∏ n_i < ∏(1+x_i)/(z^m∏x_i)
           < (1+1/L)^m/(z^m L^m)
           = L^(−2m).

Also, since n_i≥1 and x_i>0,

    M_i=α(1+n_i x_i)^{k_i}−1
        ≥(α−1)(1+x_i)^{k_i},
    N_i<(1+x_i)^{k_i}.

Therefore n_i N_i/M_i<n_i/(α−1). Writing y=(1+t_i)^{D_i} and r=t_i^{D_i}, we have

    P_i−(α−1)Q_i = y−r+α(α−1)>0,

so Q_i/P_i<1/(α−1). Combining all bounds,

    ∏F_i < [ (α−1)L ]^(−2m).

If the product exceeds 1, then necessarily (α−1)L<1.

For the asymptotic interpretation, this inequality and exp(s)−1≥s imply (α−1)lnα<d. Its positive root is asymptotic to d/ln d: substitution of α=(1±ε)d/ln d and then d→∞ proves the assertion for every fixed ε>0. This argument needs no invocation of a special function or an unverified external asymptotic theorem.

## Limits

The obstruction assumes both the light inequalities and the hub inequalities hold at every ring position, and the ensuing product is the certificate used to cover all states. A game could conceivably admit a different strict-improvement certificate beyond this range. The note does not rule out that possibility and does not assert a PNE for the underlying game at the displayed boundary.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
